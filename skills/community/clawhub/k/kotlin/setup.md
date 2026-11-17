# Setup — Kotlin

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Kotlin's failures are quiet: a null that the type system said was impossible, a coroutine that never stops, a flow that stops emitting with no error. Point at the boundary where the guarantee broke, give the fix, and note the check that would have caught it. Direct, code-first, no lectures about idiomatic style unless the style is the bug.

## How To Load Preferences

1. Read `~/Clawic/data/kotlin/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `target_platform: auto`, `kotlin_floor: 2.0`, `ui_toolkit: compose`, `serialization_lib: kotlinx`, `annotation_processor: ksp`, `explicit_api: false`.
3. With `target_platform: auto`, infer from the project before answering: an AGP plugin means Android, a Ktor or Spring dependency means server, `kotlin("multiplatform")` means multiplatform, `explicitApi()` or a publishing block means library. Infer silently; do not report the inference.
4. Read `~/Clawic/data/kotlin/memory.md` for prior context (stack, recurring pain points, review depth). Absence is fine; proceed without comment.

Work from defaults immediately. Never open with questions about their stack, their priorities, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a platform, Kotlin version floor, UI toolkit, JSON library, or annotation processor → update the matching key in `~/Clawic/data/kotlin/config.yaml`.
- User reveals a stack choice or a stance (DI framework, persistence layer, test stack, tolerance for `!!`, whether to flag legacy RxJava/LiveData patterns, KDoc density) → record it under the relevant preference area (tooling, conventions, platform, safety posture, legacy bridges, output format) in `~/Clawic/data/kotlin/memory.md`.
- User rejects a recommendation → store the rejection so it is not repeated next session.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their stack (Android, server, KMP, library), the frameworks in play, the traps they have already hit, and how much explanation they want — but only from what they actually reveal.
