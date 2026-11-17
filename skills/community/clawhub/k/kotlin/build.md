# Build And Compiler — Gradle Kotlin DSL, KSP, K2, Opt-In

Kotlin build problems split cleanly: toolchain/target mismatches (the build refuses), annotation processing (the build crawls), and compiler flags that change what the language allows.

## Error → Fix

| Message | Cause | Fix |
|---|---|---|
| "Inconsistent JVM-target compatibility detected … Java X, Kotlin Y" | The Java and Kotlin compile tasks target different bytecode versions | One `kotlin { jvmToolchain(17) }` for both, instead of setting each task |
| "Unresolved reference" only in the IDE | Stale IDE caches or an unsynced Gradle model | Sync, then invalidate caches; if the CLI build passes, it is not a code problem |
| "Class 'X' was compiled with an incompatible version of Kotlin" | A dependency built with a newer Kotlin metadata version | Raise the Kotlin version, or use a dependency built for yours |
| "This declaration is experimental and its usage must be marked with @OptIn" | Opt-in-required API | `@OptIn(Marker::class)` at the narrowest scope, or `-opt-in=` module-wide when it is pervasive |
| "Cannot inline bytecode built with JVM target 1.8 into bytecode being built with JVM target 1.6" | Mixed targets across modules | Align the toolchain across all modules |
| kapt task takes minutes | Stub generation for every annotated source | Migrate the processor to KSP, or reduce annotated surface |
| "Duplicate class" after adding a library | Two versions of the same artifact | `dependencies { … }` resolution report (`dependencies --configuration …`) then force one version |
| Compose compiler version error | Compiler plugin version tied to the Kotlin version | Kotlin >=2.0 ships the plugin as `org.jetbrains.kotlin.plugin.compose`, versioned with Kotlin itself |
| "Type inference failed" only after a Kotlin upgrade | Inference change in a new compiler version | Add explicit type arguments at the failing call; do not downgrade the whole build |

## Toolchain And Targets

- One declaration for the whole module: `kotlin { jvmToolchain(17) }`. Gradle then provisions a matching JDK for Java, Kotlin and tests. Setting `sourceCompatibility`, `targetCompatibility` and `jvmTarget` individually is how they drift apart.
- The toolchain is the JDK used to compile; `jvmTarget` is the bytecode level produced. Running the build on JDK 21 and targeting 17 is normal and correct.
- Android modules gate the target on the AGP/Gradle pair; a toolchain higher than what the AGP version supports fails late in the build with an unrelated-looking error.
- Multi-module: put the toolchain and compiler options in a convention plugin (`buildSrc` or an included build), not copy-pasted per module — drift between modules is the source of the inline/target errors above.

## Annotation Processing: kapt vs KSP

`annotation_processor` decides which setup snippets this skill emits and which build-speed advice applies: `ksp` (the default) emits the KSP variant of every library's wiring, `kapt` keeps the stub-pass caveat attached to each snippet, `none` omits processor wiring altogether.

- kapt generates Java stubs for every Kotlin source so a Java annotation processor can read them. That stub-generation pass is the cost, and it grows with the module, not with the number of annotations.
- KSP reads Kotlin symbols directly, with no stub pass. The KSP project's own benchmark reports roughly a 2× improvement in processing time on its test project; the practical win on a large module is usually larger, because kapt also disables some incremental paths.
- Migrate per processor: most major libraries (Room, Moshi, Hilt, Glide) ship KSP versions. A single kapt-only processor keeps the stub pass alive for the whole module — that is the argument for replacing or dropping it.
- kapt under K2 runs in a compatibility mode rather than natively; treat "still on kapt" as technical debt with a measurable build-time price.
- Generated sources belong to the build directory: never edit them, never commit them, and reference them via the source set the plugin registers.

## Compiler Options Worth Setting

| Option | Effect |
|---|---|
| `jvmToolchain(n)` | Single source of truth for JDK and target |
| `-Xjsr305=strict` | JSR-305 annotations on Java dependencies become real Kotlin types (SKILL.md rule 1); JSpecify has its own strict mode |
| `allWarningsAsErrors` | Keeps deprecation and shadowing warnings from accumulating; enable at the start of a project, not once the backlog is already there |
| `explicitApi()` | Library modules: explicit visibility and public return types required |
| `-opt-in=kotlin.RequiresOptIn` marker list | Module-wide opt-in for an API you use everywhere |
| `-Xcontext-parameters` / other `-X` flags | Experimental language features: pin the compiler version if you use them |
| `freeCompilerArgs` additions | Where the above live in the Kotlin DSL; keep them in the convention plugin |

## Build Speed

- Configuration cache and build cache are the two switches with the largest effect; both fail loudly on incompatible plugins, which is a fixable list, not a reason to leave them off.
- Incremental compilation breaks on: changes to a widely-used `inline` function, `const val` changes, annotation processors that read the whole world, and anything in `buildSrc` (which invalidates the whole build).
- Module boundaries are the real lever: `implementation` instead of `api` stops a change from recompiling every downstream module. An `api` dependency propagates its ABI to consumers.
- `--scan` or the build's own timing report tells you which task dominates. Kotlin compile time and kapt time are different problems with different fixes.
- A version catalog (`libs.versions.toml`) is not a speed feature, but it removes the version-drift class of bugs that cost whole days.

## K2 And Version Migration

`kotlin_floor` (default 2.0) gates this section and the Compose row above: below 2.0, K2 is not the default and the Compose compiler is a separately versioned artifact with its own Kotlin compatibility map, so the `org.jetbrains.kotlin.plugin.compose` advice does not apply.

- Kotlin >=2.0 uses the K2 compiler by default; the observable effects are faster compilation and stricter, more consistent inference.
- Migration failures cluster in: smart-cast cases that K1 accepted unsoundly, type inference in complex generic chains, and compiler plugins that had not been updated. All are fixed at the call site with an explicit type.
- Upgrade order: compiler plugins and processors first (Compose, serialization, KSP, Hilt), then the Kotlin version, then the language version flags. Skipping the first step produces incomprehensible errors inside generated code.
- Pin the Kotlin version and every plugin that shadows it in one place. Two modules on two Kotlin versions is the metadata error above.

## Library Modules

- `explicitApi()` and a public-API dump (binary-compatibility-validator) turn accidental API changes into a failing check with a readable diff.
- Public inline functions and `const val` are baked into consumers at their compile time: changing them requires a consumer recompile to take effect.
- Adding a parameter to a public function, even with a default, is a binary-incompatible change for existing consumers (`@JvmOverloads` and the generated `copy` included).
- Publish with the JVM target your consumers can use, not the newest one you have.

## Review Checklist

- One toolchain declaration per module, from a shared convention plugin.
- No kapt processor left where a KSP version exists.
- Opt-in markers scoped as narrowly as the usage allows.
- `implementation` unless the type genuinely appears in the module's public API.
- Library modules run explicit API mode and an API-dump check.
