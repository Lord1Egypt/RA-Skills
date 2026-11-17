# Serialization — Nulls In Non-Null Fields, Defaults, And Polymorphism

Kotlin's type system stops at the parser. Every JSON library either understands Kotlin's constructors, defaults and nullability, or it works around them with reflection tricks that produce objects the type system says are impossible.

## Library Behaviour, Compared

| | kotlinx.serialization | Moshi (codegen) | Gson | Jackson (+ kotlin module) |
|---|---|---|---|---|
| Respects non-null types | Yes — missing field is an error | Yes — throws on a missing non-null field | **No** — instantiates without the constructor, leaves null | Yes with the Kotlin module, no without it |
| Respects default values | Yes (used when the key is absent) | Yes | **No** — defaults are skipped | Yes with the Kotlin module |
| Mechanism | Compiler plugin, generated serializers | Codegen (KSP) or reflection | Reflection + `Unsafe` | Reflection |
| Unknown keys | Error by default (`ignoreUnknownKeys = true` to relax) | Ignored by default | Ignored | Configurable, ignored by default |
| Sealed/polymorphic | First-class, with a class discriminator | Adapter-based | Manual | Annotation-based |
| Value classes | Supported | Limited | Not supported | Limited |

`serialization_lib` (default `kotlinx`) picks which column is authoritative: it selects the annotation set the examples use, the config defaults in the next section, and which of the non-null-field warnings below are live — under `gson` all of them are, under `kotlinx` almost none.

Gson with Kotlin is the single most common source of "NPE on a field the type says cannot be null": the `Unsafe` instantiation path never runs your constructor, so neither validation nor defaults happen. If Gson must stay, declare every field nullable and map into a validated domain type at the boundary.

## kotlinx.serialization

- Setup is the plugin plus the runtime; each `@Serializable` class gets a generated serializer with no reflection at runtime.
- Configure the `Json` instance once and inject it:

```kotlin
val json = Json {
    ignoreUnknownKeys = true      // server adds fields without breaking old clients
    encodeDefaults = false        // omit values equal to the default (the default behaviour)
    explicitNulls = false         // omit nulls rather than writing "field": null
    coerceInputValues = true      // null for a non-null field with a default → use the default
    prettyPrint = false
}
```

- `ignoreUnknownKeys = false` (the default) means the day the backend adds a field, every client fails to parse. Turning it on is the compatible choice for clients; keeping it off is the strict choice for internal contracts you control.
- `encodeDefaults = false` means a field equal to its default is not written at all — a receiver that distinguishes "absent" from "default" sees a different message than you expect. Set it to true for round-trip formats.
- `@SerialName("user_id")` maps names; `@JsonNames("userId", "user_id")` accepts several on input (JSON only).
- `@Transient` excludes a property — it then needs a default, because the deserializer cannot fill it.
- `@Required` forces presence even for a property that has a default.
- Custom types: `@Serializable(with = InstantSerializer::class)` on the property, or `@Contextual` plus a `serializersModule` registration for third-party types you cannot annotate.
- `Json.encodeToString(value)` infers the serializer from the static type: encoding a subclass through a supertype variable serializes only the supertype's fields unless the hierarchy is polymorphic.

## Polymorphism

- Sealed hierarchies are the supported case: annotate the parent `@Serializable`, and every subclass; the format writes a discriminator (`"type"` by default, changed with `classDiscriminator = "…"`).
- Open hierarchies need explicit registration in a `SerializersModule` with `polymorphic(Base::class) { subclass(Impl::class) }`.
- The discriminator must not collide with a real property name — the failure is a confusing "unknown key" or a duplicate-key error.
- `JsonContentPolymorphicSerializer` handles the schemas that discriminate by *shape* rather than by a type field (the common case for third-party APIs).

## Practical Data Modelling

- Wire type ≠ domain type. A DTO with nullable fields and permissive types, plus a mapper that validates into a non-null domain model, converts every parsing surprise into one clear error at one place (SKILL.md rule 1).
- Never expose a serialized DTO to the UI: a field rename on the backend then reaches every composable.
- Numbers: JSON has one number type, and large ids lose precision as `Double`. Type ids as `String` or `Long` explicitly, and check what the backend actually sends.
- Dates: `kotlinx-datetime` (`Instant`, `LocalDate`) for multiplatform, `java.time` on JVM-only. Store and transmit UTC instants; convert at the display edge.
- Enums: an unknown value from the server is a hard failure by default. Add an `Unknown` fallback member with `coerceInputValues = true`, or keep the raw string in the DTO and map with a `when` that has an else.
- Lists and maps of nullable elements deserialize null elements happily; if the API never sends them, model them non-null and let the failure be loud.

## Android Specifics

- `@Parcelize` (kotlin-parcelize plugin) generates `Parcelable` implementations; it is for passing state through Android's IPC, not a network format, and it inherits the saved-state size limits.
- A `@Parcelize` class with a non-parcelable property needs a `Parceler` or `@RawValue` — the latter defers the failure to runtime.
- R8 removes classes only reflection touches: reflection-based libraries need keep rules, while kotlinx.serialization and Moshi codegen mostly do not, because the generated code references the classes directly.
- Room, DataStore-proto and network models are three different schemas; sharing one class across all three couples a database migration to a backend change.

## Versioning And Compatibility

- Additive changes only, on both sides: new fields must have defaults, removed fields must stay parseable (unknown keys ignored) until every client is updated.
- Renaming a field is two releases: add the new name with `@JsonNames`, migrate, then drop the old one.
- Persisted formats (disk cache, DataStore) need a schema version field from day one; a parse failure on start-up with no version is an unrecoverable state on the user's device.
- Round-trip test per model: `decode(encode(x)) == x` catches discriminator collisions, default-omission surprises and precision loss in one assertion.

## Review Checklist

- No reflection-based parser filling non-null Kotlin properties.
- One configured `Json`/parser instance, injected, not constructed at call sites.
- DTOs separated from domain models where the API is not under your control.
- Ids and money never parsed as floating point.
- Unknown-enum and unknown-key policies chosen explicitly, not inherited from defaults.
- Persisted formats carry a version field and a round-trip test.
