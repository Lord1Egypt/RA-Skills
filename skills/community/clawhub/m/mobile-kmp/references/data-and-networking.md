# Data and networking reference

Load this when writing the shared Ktor client, serialization models, Room KMP or SQLDelight databases,
or moving an Android data layer into `commonMain`.

## Ktor client

### Engines

| Platform | Engine | Artifact |
|---|---|---|
| Android | OkHttp (or the `Android` engine) | `io.ktor:ktor-client-okhttp` |
| iOS | Darwin (uses `NSURLSession`) | `io.ktor:ktor-client-darwin` |

```kotlin
// commonMain: the client is built from an injected engine
fun createHttpClient(engine: HttpClientEngine, json: Json, tokens: TokenProvider) = HttpClient(engine) {
    expectSuccess = true
    install(ContentNegotiation) { json(json) }
    install(HttpTimeout) {
        connectTimeoutMillis = 10_000
        requestTimeoutMillis = 15_000
    }
    install(Auth) {
        bearer {
            loadTokens { tokens.current()?.let { BearerTokens(it.access, it.refresh) } }
            refreshTokens { tokens.refresh()?.let { BearerTokens(it.access, it.refresh) } }
        }
    }
    install(Logging) {
        level = if (isDebugBuild) LogLevel.HEADERS else LogLevel.NONE
        sanitizeHeader { it == HttpHeaders.Authorization }
    }
    defaultRequest { url("https://api.example.com/") }
}

// androidMain
fun platformEngine(): HttpClientEngine = OkHttp.create()

// iosMain
fun platformEngine(): HttpClientEngine = Darwin.create()
```

- Pass the engine through DI (or an `expect fun platformEngine()`) so tests can use `MockEngine` from
  `io.ktor:ktor-client-mock`.
- Without an engine argument, `HttpClient()` picks one from the engine dependencies on the classpath.
  Recent Ktor 3 releases also ship `ktor-client-engine-defaults` for `commonMain`; check the Ktor version
  before relying on it. Explicit engines are easier to configure and review.
- `isDebugBuild` is the project's own flag (for example from an `expect val` or injected config).
- The `Auth` plugin needs `io.ktor:ktor-client-auth`.

### Transport security

- HTTPS only. On iOS, App Transport Security blocks cleartext unless `Info.plist` has exceptions; never
  add `NSAllowsArbitraryLoads`. On Android, keep `usesCleartextTraffic` off in the app manifest.
- Certificate pinning is configured per engine: OkHttp `CertificatePinner` in the OkHttp engine config,
  and the Darwin engine's challenge handling or certificate pinner on iOS. Pin keys, not leaf certificates,
  and ship a backup pin. Escalate pinning decisions to `mobile-security`.
- Tokens live in Keystore-backed storage on Android and the Keychain on iOS, behind a common interface.
  Never in `commonMain` constants, `BuildConfig` or `Info.plist`.

### Errors

```kotlin
// BAD: swallows cancellation and hides the failure type
suspend fun readings(): List<Reading> = runCatching { api.readings() }.getOrDefault(emptyList())

// GOOD: map transport errors to domain errors in one place
suspend fun readings(): ReadingsResult = try {
    ReadingsResult.Ok(client.get("readings").body<List<ReadingDto>>().map { it.toDomain() })
} catch (e: CancellationException) {
    throw e
} catch (e: ClientRequestException) {      // 4xx with expectSuccess = true
    ReadingsResult.Rejected(e.response.status.value)
} catch (e: ServerResponseException) {     // 5xx
    ReadingsResult.ServerError
} catch (e: HttpRequestTimeoutException) {
    ReadingsResult.Timeout
}
```

- Network failure types differ between OkHttp and Darwin. Map the remaining platform IO failures in one
  shared helper so callers and Swift see a sealed result, not engine-specific exceptions.
- Anything that still escapes to Swift needs `@Throws` on the Swift-facing function.

## kotlinx.serialization

```kotlin
val appJson = Json {
    ignoreUnknownKeys = true   // new server fields do not break old clients
    coerceInputValues = true   // unknown enum value or null for non-null field falls back to the default
}

@Serializable
data class ReadingDto(
    @SerialName("device_id") val deviceId: String,
    val value: Double,
    val unit: UnitDto = UnitDto.UNKNOWN,
)

@Serializable
enum class UnitDto { @SerialName("c") CELSIUS, @SerialName("f") FAHRENHEIT, UNKNOWN }

@Serializable
sealed interface EventDto {
    @Serializable @SerialName("reading") data class Reading(val value: Double) : EventDto
    @Serializable @SerialName("alarm") data class Alarm(val code: Int) : EventDto
}
```

- The `type` field is the default class discriminator for sealed hierarchies; change it with
  `classDiscriminator` in the `Json` builder if the API uses another name.
- DTOs stay in the data layer. Map to domain types with value classes for IDs.
- The serialization plugin generates serializers at compile time. Still run a minified Android release
  build before shipping, since custom keep rules elsewhere can strip generated classes.
- Payloads with device identifiers or location are personal data. Do not log bodies.

## Room KMP

Room 3 (`androidx.room3`) is the KMP-focused major version: KSP-only, coroutines-only, backed by
`SQLiteDriver`. Projects already on Room 2.7+ in KMP can stay there and migrate later; both can coexist.

~~~toml
[versions]
room3 = "<room3>"
sqlite = "<androidx sqlite>"
ksp = "<ksp matching kotlin>"

[libraries]
androidx-room3-runtime = { module = "androidx.room3:room3-runtime", version.ref = "room3" }
androidx-room3-compiler = { module = "androidx.room3:room3-compiler", version.ref = "room3" }
androidx-sqlite-bundled = { module = "androidx.sqlite:sqlite-bundled", version.ref = "sqlite" }

[plugins]
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
androidx-room3 = { id = "androidx.room3", version.ref = "room3" }
~~~

```kotlin
// shared/build.gradle.kts
plugins {
    alias(libs.plugins.ksp)
    alias(libs.plugins.androidx.room3)
}
kotlin {
    sourceSets.commonMain.dependencies {
        implementation(libs.androidx.room3.runtime)
        implementation(libs.androidx.sqlite.bundled)
    }
}
dependencies {
    add("kspAndroid", libs.androidx.room3.compiler)
    add("kspIosArm64", libs.androidx.room3.compiler)
    add("kspIosSimulatorArm64", libs.androidx.room3.compiler)
}
room {
    schemaDirectory("$projectDir/schemas")
}
```

```kotlin
// commonMain
@Database(entities = [ReadingEntity::class], version = 1)
@ConstructedBy(AppDatabaseConstructor::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun readingDao(): ReadingDao
}

// The Room compiler generates the actual implementations
@Suppress("KotlinNoActualForExpect")
expect object AppDatabaseConstructor : RoomDatabaseConstructor<AppDatabase> {
    override fun initialize(): AppDatabase
}

@Dao
interface ReadingDao {
    @Upsert suspend fun upsert(reading: ReadingEntity)
    @Query("SELECT * FROM ReadingEntity ORDER BY ts DESC") fun observeAll(): Flow<List<ReadingEntity>>
}

fun buildDatabase(builder: RoomDatabase.Builder<AppDatabase>): AppDatabase =
    builder.setDriver(BundledSQLiteDriver()).build()
```

```kotlin
// androidMain
fun databaseBuilder(context: Context): RoomDatabase.Builder<AppDatabase> {
    val appContext = context.applicationContext
    return Room.databaseBuilder<AppDatabase>(
        context = appContext,
        name = appContext.getDatabasePath("app.db").absolutePath,
    )
}

// iosMain
fun databaseBuilder(): RoomDatabase.Builder<AppDatabase> {
    val dir = NSFileManager.defaultManager.URLForDirectory(
        directory = NSDocumentDirectory,
        inDomain = NSUserDomainMask,
        appropriateForURL = null,
        create = false,
        error = null,
    )
    return Room.databaseBuilder<AppDatabase>(name = requireNotNull(dir?.path) + "/app.db")
}
```

- DAO functions in common code are `suspend` or return `Flow`. No `LiveData`, no blocking DAOs.
- `BundledSQLiteDriver` gives the same SQLite version everywhere. `NativeSQLiteDriver` uses the system
  SQLite on iOS and needs `-lsqlite3` linker options.
- The default query context is `Dispatchers.IO`. Configure another through the builder only with a reason.
- Transactions use `useWriterConnection { it.immediateTransaction { ... } }`; migrations and callbacks
  receive an `SQLiteConnection`, not `SupportSQLiteDatabase`.
- Not available in KMP: pre-packaged databases (`createFromAsset` and friends), query callbacks, auto-close
  timeout, multi-instance invalidation. Plan around them before migrating.
- Minified Android builds need `-keep class * extends androidx.room3.RoomDatabase { <init>(); }`.
- Personal data at rest: the iOS file lands in Documents (backed up to iCloud by default). Decide on file
  protection and backup exclusion with `mobile-security`.

## SQLDelight

```kotlin
// shared/build.gradle.kts
plugins {
    alias(libs.plugins.sqldelight) // app.cash.sqldelight
}
kotlin {
    sourceSets {
        commonMain.dependencies { implementation(libs.sqldelight.coroutines.extensions) }
        androidMain.dependencies { implementation(libs.sqldelight.android.driver) }
        iosMain.dependencies { implementation(libs.sqldelight.native.driver) }
    }
}
sqldelight {
    databases {
        register("AppDatabase") {
            packageName.set("com.example.shared.db")
        }
    }
}
```

```sql
-- src/commonMain/sqldelight/com/example/shared/db/Reading.sq
CREATE TABLE reading (
    id TEXT NOT NULL PRIMARY KEY,
    device_id TEXT NOT NULL,
    value REAL NOT NULL,
    ts INTEGER NOT NULL
);

selectByDevice:
SELECT * FROM reading WHERE device_id = ? ORDER BY ts DESC;

upsert:
INSERT OR REPLACE INTO reading VALUES ?;
```

```kotlin
// androidMain
fun sqlDriver(context: Context): SqlDriver = AndroidSqliteDriver(AppDatabase.Schema, context, "app.db")
// iosMain
fun sqlDriver(): SqlDriver = NativeSqliteDriver(AppDatabase.Schema, "app.db")

// commonMain
fun observeReadings(db: AppDatabase, deviceId: String, io: CoroutineDispatcher): Flow<List<Reading>> =
    db.readingQueries.selectByDevice(deviceId).asFlow().mapToList(io)
```

- Schema changes go in numbered `.sqm` migration files next to the `.sq` files. Turn on migration
  verification in the database block (check the property name for the SQLDelight version in use) and
  run it in CI.
- SQL is checked at compile time, and both teams can review the schema in plain SQL.

## Choosing between them

| Question | Room KMP | SQLDelight |
|---|---|---|
| Team background | Android, Room annotations | SQL-first, mixed teams |
| Existing Android Room database | Keep schema and migrations | Rewrite schema in `.sq`, port migrations |
| Code generation | KSP, one entry per target | Gradle plugin, no KSP |
| Query style | Annotated DAO methods | Named SQL statements generate Kotlin APIs |
| Pre-packaged database | Not available in KMP | Check driver support before relying on it |

Either way: one database instance per process, created in the app graph, and a migration test for every
version bump.
