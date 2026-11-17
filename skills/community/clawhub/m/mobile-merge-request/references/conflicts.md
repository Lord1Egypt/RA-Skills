# Conflict resolution for mobile projects

Load this when a rebase or merge stops on conflicts. The goal is a result that contains both sides'
intent and builds, not a result with no conflict markers.

## General procedure

1. See what conflicted and why.

```bash
git status
git diff --name-only --diff-filter=U            # only the conflicted files
git log --oneline --merge -- <file>             # during a merge: commits on both sides touching the file
```

2. Know which side is which.

| Operation | `--ours` / HEAD | `--theirs` |
|---|---|---|
| `git merge origin/main` | your branch | main |
| `git rebase origin/main` | main (plus your already-replayed commits) | the commit being replayed |

3. Resolve per file using the rules below. Never `git checkout --ours .` or `--theirs .` for the
   whole tree.
4. Check nothing is left behind:

```bash
git diff --check                                # reports leftover conflict markers
git add <file>
git rebase --continue                           # or: git merge --continue
```

5. Rebuild and retest every affected platform before pushing. A clean merge can still be broken.

```bash
./gradlew assembleDebug testDebugUnitTest lint
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=<simulator name>' build test
flutter analyze && flutter test
```

6. If the conflict is large or unclear, `git rebase --abort` and ask the other author, rather than guess.

## Source files (Kotlin, Java, Swift, Dart)

- Read both versions and the commit messages that produced them. Merge the intent, not the lines.
- Watch for semantic conflicts that git does not flag: a function renamed on main and called by its old
  name in your branch, a new required parameter, a changed default. The build catches most; tests catch
  the rest.
- Imports: keep the union, then let the formatter or IDE remove unused ones.

## Lockfiles

Never hand-merge a lockfile. Resolve the manifest, take main's lockfile, regenerate.

| Lockfile | Manifest to resolve first | Regenerate with |
|---|---|---|
| `pubspec.lock` | `pubspec.yaml` | `flutter pub get` (or `dart pub get`) |
| `Podfile.lock` | `Podfile` | `pod install` (not `pod update`, which bumps everything) |
| `Package.resolved` | Xcode project or `Package.swift` | `xcodebuild -resolvePackageDependencies`, or resolve packages in Xcode |
| `gradle.lockfile` (dependency locking) | `libs.versions.toml`, `build.gradle.kts` | the project's lock task, for example `./gradlew dependencies --write-locks` per affected module |

```bash
# during a rebase, --ours is main's version
git checkout --ours pubspec.lock
flutter pub get
git add pubspec.lock
```

Review the regenerated lockfile diff: only the packages your branch intended to change should move.

## Generated code

Do not hand-merge generated output. Resolve the sources, then regenerate.

- Dart `*.g.dart`, `*.freezed.dart`, mocks: `dart run build_runner build --delete-conflicting-outputs`.
- Flutter localizations: `flutter gen-l10n` after merging the `.arb` files.
- Protobuf or OpenAPI generated clients: rerun the generator from the merged schema.
- Room exported schemas (`schemas/<Database>/<version>.json`): a conflict here usually means both
  branches bumped the database to the same version. This is a real conflict: renumber one branch's
  migration to the next version, then rebuild so the schema is exported again.

If generated files should not be in git at all, raise it as a separate MR.

## Xcode `project.pbxproj`

- Each added file appears in several sections (file reference, build file, group children, build
  phase). Keep both sides' entries in every section; dropping one side silently removes files from
  the target.
- Remove only the conflict markers and true duplicates (same object ID listed twice).
- Validate the file and then build:

```bash
plutil -lint App.xcodeproj/project.pbxproj
xcodebuild -scheme App -destination 'platform=iOS Simulator,name=<simulator name>' build
```

- Open the project in Xcode and confirm the files from both sides appear in the right targets.
- If the file is badly mangled, abort, take main's version and re-add your files in Xcode.
- Prevention: synchronized folder groups (Xcode 16 and later) stop most per-file entries; project
  generators (XcodeGen, Tuist) avoid committing the project file altogether.
- Do not set `merge=union` for `*.pbxproj` in `.gitattributes`; it produces duplicate or dangling
  entries that only fail later.

## Gradle version catalog (`libs.versions.toml`)

- New entries from both sides: keep both.
- Same alias, different versions: choose deliberately, usually the newer one, and check compatibility
  (Kotlin and Compose compiler, AGP and Gradle, BOM-managed libraries).
- Same library added under two different aliases: keep one alias and update usages.
- Keep each table sorted alphabetically; it makes future conflicts rare and trivial.
- Run a Gradle sync and a full build after resolving; a catalog mistake fails at configuration time.

## Android resources and manifest

- `strings.xml` and translations: keep both sides' keys; make sure no key was renamed on one side.
- `AndroidManifest.xml`: keep both sides' components and permissions, remove duplicates, and recheck
  `android:exported` on every component either side added.
- Navigation graphs and XML layouts: resolve by hand and open the editor preview to confirm.

## iOS resources

- `Localizable.xcstrings` is JSON: keep both sides' keys, then confirm it still parses by building.
- `Info.plist` and entitlements: keep both sides' keys and call out the result in the MR description.
- Asset catalogs (`Contents.json`): keep both entries; duplicated asset names fail the build.

## After resolving

- [ ] No conflict markers (`git diff --check`)
- [ ] Lockfiles and generated code regenerated, not hand-edited
- [ ] Build and tests green for every affected platform
- [ ] `git range-diff origin/main @{u} HEAD` reviewed before `git push --force-with-lease`
- [ ] Non-trivial resolutions mentioned in an MR comment so reviewers can check them
