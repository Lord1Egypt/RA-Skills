# Hilt and Room reference

Load this when adding injected classes, DI modules, entities, DAOs, migrations or serialization models.

## Hilt setup

```kotlin
@HiltAndroidApp
class App : Application()

@AndroidEntryPoint
class MainActivity : ComponentActivity()

@HiltViewModel
class DeviceViewModel @Inject constructor(
    private val savedStateHandle: SavedStateHandle,
    private val repository: DeviceRepository,
) : ViewModel()
```

- Constructor injection for every class the app owns. Modules exist only for interfaces and third-party types.
- Compose obtains ViewModels with `hiltViewModel()` at the route level only.

## Modules

```kotlin
// Interface to implementation: @Binds in an abstract module, no body to maintain
@Module
@InstallIn(SingletonComponent::class)
abstract class DataModule {
    @Binds abstract fun deviceRepository(impl: OfflineFirstDeviceRepository): DeviceRepository
}

// Third-party types: @Provides
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides @Singleton
    fun json(): Json = Json { ignoreUnknownKeys = true }

    @Provides @Singleton
    fun database(@ApplicationContext context: Context): AppDb =
        Room.databaseBuilder(context, AppDb::class.java, "app.db")
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
            .build()

    @Provides
    fun deviceDao(db: AppDb): DeviceDao = db.deviceDao()
}
```

## Scopes

| Annotation | Component | Lives as long as |
|---|---|---|
| `@Singleton` | `SingletonComponent` | The process |
| `@ActivityRetainedScoped` | `ActivityRetainedComponent` | Activity, across configuration changes |
| `@ViewModelScoped` | `ViewModelComponent` | One ViewModel |
| `@ActivityScoped` | `ActivityComponent` | One Activity instance |

- Unscoped is the default and the right choice for stateless classes. Scope only when the instance holds
  shared state or is expensive to create.
- A `@Singleton` must never hold an Activity, View, or screen state.
- `@ApplicationContext` for any `Context` in a singleton. Never inject an Activity context into it.
- Use `@Qualifier` annotations for two bindings of the same type (dispatchers, scopes, base URLs).
- `Lazy<T>` or `Provider<T>` to defer expensive construction off the startup path.

## Room entities and DAOs

```kotlin
@Entity(tableName = "device", indices = [Index("serial", unique = true)])
data class DeviceEntity(
    @PrimaryKey val id: String,
    val serial: String,
    val name: String,
    @ColumnInfo(defaultValue = "0") val lastSeenEpochMs: Long,
)

@Dao
interface DeviceDao {
    @Query("SELECT * FROM device ORDER BY name")
    fun observeAll(): Flow<List<DeviceEntity>>

    @Query("SELECT * FROM device WHERE id = :id")
    suspend fun byId(id: String): DeviceEntity?

    @Upsert
    suspend fun upsert(devices: List<DeviceEntity>)

    @Query("DELETE FROM device")
    suspend fun clear()

    @Transaction
    suspend fun replaceAll(devices: List<DeviceEntity>) {
        clear()
        upsert(devices)
    }
}
```

- `Flow` queries for observed data, `suspend` for one-shot reads and writes. Room runs them off the main
  thread; no `withContext` needed around DAO calls.
- Flow queries re-emit on any write to the observed tables. Add `distinctUntilChanged()` when the UI only
  cares about actual changes.
- Multi-step writes in one `@Transaction`.
- Entities stay in the data layer. Map to domain models (with value-class IDs) in the repository.
- Never `allowMainThreadQueries()` outside tests.

## Migrations

```kotlin
@Database(
    entities = [DeviceEntity::class],
    version = 3,
    exportSchema = true,
    autoMigrations = [AutoMigration(from = 1, to = 2)],
)
abstract class AppDb : RoomDatabase() {
    abstract fun deviceDao(): DeviceDao
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE device ADD COLUMN lastSeenEpochMs INTEGER NOT NULL DEFAULT 0")
    }
}
```

- `exportSchema = true` and the schema directory committed to version control. Auto-migrations and
  migration tests need the exported JSON.
- Schema location with the Room Gradle plugin: `room { schemaDirectory("$projectDir/schemas") }`.
- Renames and deletes in auto-migrations need an `AutoMigrationSpec` (`@RenameColumn`, `@DeleteColumn`).
- `fallbackToDestructiveMigration` deletes user data. Do not ship it in release builds.
- Each migration has a test with `MigrationTestHelper` (see [Testing](testing.md)).

## kotlinx.serialization

```kotlin
@Serializable
data class DeviceDto(
    val id: String,
    @SerialName("display_name") val name: String,
    val firmware: String? = null,
)

// One configured Json instance, injected
val json = Json {
    ignoreUnknownKeys = true   // tolerate new server fields
    explicitNulls = false      // omit nulls when encoding
}
```

- Default values make fields optional on decode. A missing non-default field throws.
- DTOs are separate from entities and domain models. Map at the edge.
- Retrofit uses the official kotlinx.serialization converter with the same injected `Json` instance.
- Payloads with device identifiers are personal data: no full-body logging in release builds.
