# SwiftData reference

Load this when adding or changing persistence with SwiftData. Requires iOS 17. For Core Data projects,
do not mix in SwiftData without a migration plan agreed with the team.

## Models

```swift
import SwiftData

@Model
final class DeviceEntity {
    @Attribute(.unique) var serial: String
    var name: String
    var lastSeen: Date?
    @Relationship(deleteRule: .cascade, inverse: \ReadingEntity.device)
    var readings: [ReadingEntity] = []

    init(serial: String, name: String) {
        self.serial = serial
        self.name = name
    }
}

@Model
final class ReadingEntity {
    var value: Double
    var date: Date
    var device: DeviceEntity?

    init(value: Double, date: Date) {
        self.value = value
        self.date = date
    }
}
```

- `@Model` types are classes and are not `Sendable`. Keep them in the persistence and UI layers.
- Map to plain `struct` domain models at the repository boundary if the domain layer must stay
  framework-free or cross actors.
- Store secrets and tokens in the Keychain, not in SwiftData. Device serials and telemetry can be
  personal data; apply a file protection class and a retention policy.

## Container

```swift
@main
struct GatewayApp: App {
    var body: some Scene {
        WindowGroup { RootView() }
            .modelContainer(for: [DeviceEntity.self, ReadingEntity.self])
    }
}
```

For tests and previews use an in-memory store:

```swift
let container = try ModelContainer(
    for: DeviceEntity.self, ReadingEntity.self,
    configurations: ModelConfiguration(isStoredInMemoryOnly: true)
)
```

## Reading

```swift
struct DeviceList: View {
    @Query(sort: \DeviceEntity.name) private var devices: [DeviceEntity]
    var body: some View { List(devices) { DeviceRow(device: $0) } }
}
```

Filter that depends on input: build the query in `init`.

```swift
struct ReadingList: View {
    @Query private var readings: [ReadingEntity]

    init(serial: String) {
        _readings = Query(
            filter: #Predicate<ReadingEntity> { $0.device?.serial == serial },
            sort: \ReadingEntity.date,
            order: .reverse
        )
    }

    var body: some View { List(readings) { ReadingRow(reading: $0) } }
}
```

Outside views, fetch with a descriptor and a limit:

```swift
var descriptor = FetchDescriptor<ReadingEntity>(
    sortBy: [SortDescriptor(\.date, order: .reverse)]
)
descriptor.fetchLimit = 100
let latest = try context.fetch(descriptor)
```

## Writing

```swift
@Environment(\.modelContext) private var context

func add(_ device: DeviceEntity) throws {
    context.insert(device)
    try context.save()
}
```

- The main context autosaves, but call `save()` explicitly after user-visible writes so errors surface.
- Bulk imports and sync run in a `@ModelActor`, never on the main context.

```swift
@ModelActor
actor ReadingImporter {
    func importBatch(_ rows: [ReadingDTO], for deviceID: PersistentIdentifier) throws {
        guard let device = self[deviceID, as: DeviceEntity.self] else { return }
        for row in rows {
            let reading = ReadingEntity(value: row.value, date: row.date)
            reading.device = device
            modelContext.insert(reading)
        }
        try modelContext.save()
    }
}

// Caller
let importer = ReadingImporter(modelContainer: container)
try await importer.importBatch(rows, for: device.persistentModelID)
```

- Pass `PersistentIdentifier` (which is `Sendable`) across actors, then re-fetch in the target context.
- One context per actor. Never capture a `ModelContext` or `@Model` instance in a `Task.detached`.

## Schema changes and migration

Any change to a shipped `@Model` needs a versioned schema so existing user data migrates.

```swift
enum SchemaV1: VersionedSchema {
    static var versionIdentifier: Schema.Version { Schema.Version(1, 0, 0) }
    static var models: [any PersistentModel.Type] { [DeviceEntity.self] }

    @Model final class DeviceEntity {
        var serial: String
        init(serial: String) { self.serial = serial }
    }
}

enum SchemaV2: VersionedSchema {
    static var versionIdentifier: Schema.Version { Schema.Version(2, 0, 0) }
    static var models: [any PersistentModel.Type] { [DeviceEntity.self] }

    @Model final class DeviceEntity {
        var serial: String
        var firmwareVersion: String?
        init(serial: String) { self.serial = serial }
    }
}

enum GatewayMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] { [SchemaV1.self, SchemaV2.self] }
    static var stages: [MigrationStage] {
        [.lightweight(fromVersion: SchemaV1.self, toVersion: SchemaV2.self)]
    }
}

// The rest of the app refers to the current version only
typealias DeviceEntity = SchemaV2.DeviceEntity

let container = try ModelContainer(
    for: DeviceEntity.self,
    migrationPlan: GatewayMigrationPlan.self
)
```

- Lightweight stages cover added optional properties, renames with `@Attribute(originalName:)`, and
  removed properties. Data transformations need a `.custom` stage.
- Test migration on a store created by the previous release build, not only on a fresh install.
- Never ship a change that deletes and recreates the store to "fix" a migration error.
