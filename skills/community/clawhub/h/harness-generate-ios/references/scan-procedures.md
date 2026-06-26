# iOS Project Scan Procedures

## Table of Contents

1. [Project Metadata](#project-metadata)
2. [Dependencies](#dependencies)
3. [Compiler Flags & Multi-Target](#compiler-flags--multi-target)
4. [SwiftLint Rules](#swiftlint-rules)
5. [Module Discovery](#module-discovery)
6. [Swift Code Scanning](#swift-code-scanning)
7. [Architecture Inference](#architecture-inference)
8. [Naming & Style Detection](#naming--style-detection)
9. [Script Discovery](#script-discovery)

---

## Project Metadata

### Workspace file
```bash
# Find workspace
Glob("*.xcworkspace")
# Read workspace contents to get included projects
Read("*.xcworkspace/contents.xcworkspacedata")
```

### Schemes and Targets
```bash
# List shared schemes from xcodeproj
Glob("*.xcodeproj/xcshareddata/xcschemes/*.xcscheme")

# Or use xcodebuild (more accurate)
xcodebuild -workspace "*.xcworkspace" -list 2>/dev/null | head -30
```

### Deployment target (iOS version)
```bash
Grep("IPHONEOS_DEPLOYMENT_TARGET", glob="*.xcodeproj/project.pbxproj")
```

## Dependencies

### CocoaPods
```bash
Glob("Podfile")
Grep("pod '", path="Podfile", output_mode="content")
```

### Swift Package Manager
```bash
Glob("**/Package.swift")
Glob("*.xcodeproj/**/Package.resolved")
Grep("repositoryURL|location", path="**/Package.resolved", output_mode="content")
```

## Compiler Flags & Multi-Target

```bash
# Scan #if macro usage
Grep("#if\\s+(\\w+)", glob="**/*.swift", output_mode="content", head_limit=30)
# Common patterns: #if TARGET_A, #if TARGET_B, #if DEBUG, #if targetEnvironment
# Filter out standard macros (DEBUG, targetEnvironment) — the rest indicate dual targets

# Extract from pbxproj
Grep("SWIFT_ACTIVE_COMPILATION_CONDITIONS|GCC_PREPROCESSOR", glob="*.xcodeproj/project.pbxproj", output_mode="content")
```

## SwiftLint Rules

```bash
Read(".swiftlint.yml")
```

**Extraction logic**:
1. Read `opt_in_rules` → actively enabled rules
2. Find all `severity: error` entries → error-level rules
3. Translate SwiftLint rule names into human-readable constraints

## Module Discovery

### SPM packages
```bash
Glob("Packages/*/Package.swift")
Glob("Packages/*/Sources/**/*.swift")
```

### Business modules
```bash
# List first-level subdirectories with .swift files
Bash("ls -d App/*/")  # adjust to actual main directory name
Glob("App/*/*.swift")
```

## Swift Code Scanning

### Public/Open types
```bash
Grep("^\\s*(public|open)\\s+(class|struct|enum|protocol|actor)\\s+\\w+", glob="<module>/**/*.swift", output_mode="content")
```

### Singletons
```bash
Grep("static\\s+(let|var)\\s+shared", glob="<module>/**/*.swift", output_mode="content")
```

### Delegates / Protocols
```bash
Grep("protocol\\s+\\w+Delegate", glob="<module>/**/*.swift", output_mode="content")
Grep("weak\\s+var\\s+delegate", glob="<module>/**/*.swift", output_mode="content")
```

### Async methods
```bash
Grep("\\basync\\b", glob="<module>/**/*.swift", output_mode="content", head_limit=20)
```

### Import dependencies
```bash
Grep("^import\\s+\\w+", glob="<module>/**/*.swift", output_mode="content")
# Deduplicate to get the module dependency list
```

### Dangerous patterns (for PITFALLS.md)
```bash
# Force unwrap
Grep("[^?]!\\.", glob="**/*.swift", output_mode="count")
# Force cast
Grep("as!", glob="**/*.swift", output_mode="count")
# swiftlint:disable
Grep("swiftlint:disable", glob="**/*.swift", output_mode="content", head_limit=30)
```

## Architecture Inference

**Infer from directory structure & file naming**:
- Has `ViewModel` directory or `*ViewModel.swift` files → MVVM
- Has `Presenter` files → MVP
- Has `Router`/`Coordinator` files → Coordinator pattern
- Has `Service`/`Manager` files → Service layer
- Has `Repository` files → Repository pattern

```bash
Grep("ViewModel", glob="**/*.swift", output_mode="files_with_matches", head_limit=5)
Grep("Coordinator|Router", glob="**/*.swift", output_mode="files_with_matches", head_limit=5)
Grep("class\\s+\\w+Service", glob="**/*.swift", output_mode="files_with_matches", head_limit=5)
Grep("class\\s+\\w+Manager", glob="**/*.swift", output_mode="files_with_matches", head_limit=5)
```

**Infer from imports**:
- `import SwiftUI` → SwiftUI
- `import UIKit` → UIKit
- `import Combine` → Reactive
- `import Factory` → DI framework

## Naming & Style Detection

```bash
# File naming patterns (prefix detection)
Bash("ls App/**/*.swift | head -30")
# Common prefixes: XX, YY, ZZ, etc.

# Localization method
Grep("NSLocalizedString|localized|\\.mm\\.localized", glob="**/*.swift", output_mode="content", head_limit=10)

# File organization (by feature vs. by type)
# Check whether directory structure is Model/View/ViewModel or feature-based
```

## Script Discovery

```bash
Glob("Scripts/**/*")
Glob("scripts/**/*")
Glob("tools/**/*")
# Read first 5 lines of each script (usually has comments describing purpose)
Glob("Makefile")
Glob("fastlane/**/*")
```
