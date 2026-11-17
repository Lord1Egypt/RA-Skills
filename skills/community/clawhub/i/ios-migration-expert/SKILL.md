---
name: ios-cocoapods-spm-migration
description: >-
  Use when migrating iOS projects from CocoaPods to Swift Package Manager,
  or when planning a migration strategy for enterprise iOS dependencies.
  Covers dependency mapping, build settings, xcconfig translation, resource
  bundles, Objective-C interop, binary frameworks, and CI/CD adaptation.
  For iOS developers and AI coding agents involved in migration planning
  and execution.
---

# iOS CocoaPods → SPM Migration

## Overview

Systematic, dependency-first approach: audit all current CocoaPods
dependencies before writing any Package.swift. Map each pod individually,
handle build settings per dependency, then migrate incrementally.

**Never jump straight to writing a Package.swift without auditing the
existing setup first.**

## When to Use

- Project currently uses CocoaPods (`Podfile`, `Pods/`, `*.xcworkspace`)
- Need to adopt SPM-native features (build plugins, macros, binary targets)
- Build times impacted by CocoaPods integration phase
- Multiple dependency managers in a single project
- CI pipelines need simplified dependency management

### When NOT to Use

- One-off or experimental projects (migration effort exceeds benefit)
- Pods without SPM equivalents and no viable alternative
- Projects requiring CocoaPods-only features (resource bundles in subspecs)

## Decision Framework

```
Current Pod has SPM support?
├─ YES → Can migrate directly
│  └─ Check: same product name? resource bundle handling?
├─ NO → Is there an SPM alternative?
│  ├─ YES → Consider replacing (evaluate API differences)
│  └─ NO → Does the pod distribute as binary framework?
│     ├─ YES → Can wrap as SPM binary target
│     └─ NO → Keep in CocoaPods (hybrid), or vendor the source
```

## Migration Process

Each phase has a dedicated prompt template in `prompts/`:

### 1. Audit (`prompts/audit.md`)
Inventory current Podfile — list every pod, subspec, version requirement.
Check for: resource bundles, xcconfig injections, script phases, module
maps, bridging headers. Collect the full dependency tree.

### 2. Map (`prompts/migrate.md`)
Map each pod to its SPM equivalent using `mappings/` database.
For each: SPM URL, product name, version compatibility, special setup.

### 3. Build Settings Migration
Translate CocoaPods-generated settings:
- Remove `$(inherited)` from `HEADER_SEARCH_PATHS`, `FRAMEWORK_SEARCH_PATHS`
- Replace `OTHER_LDFLAGS` flags with SPM's automatic linking
- Handle `xcconfig` files — eliminate CocoaPods-generated includes
- Migrate script phases (Crashlytics upload, SwiftGen, etc.)

### 4. Configure & Verify (`prompts/verify.md`)
Add packages in Xcode, resolve dependencies, build.
Verify: no linker errors, resource bundles load, ObjC bridging intact,
all imports resolve correctly.

### 5. Adapt CI/CD
Update CI pipeline — remove `pod install` step, add `xcodebuild
-resolvePackageDependencies`. Update cache keys. Handle binary framework
distribution if applicable.

## Quick Reference

| CocoaPods | SPM Equivalent |
|-----------|---------------|
| `pod install` | `xcodebuild -resolvePackageDependencies` |
| `pod update` | Update version in `Package.swift` or Xcode |
| `Podfile` | `Package.swift` (or Xcode project settings) |
| `Pods/` directory | `SourcePackages/` (build artifacts) |
| Podspec | `Package.swift` manifest |
| `use_frameworks!` | Default for SPM (always modules) |
| `#import <Module/Module.h>` | `import Module` or `@import Module` |
| Script phases from pods | Manual script phase with `SourcePackages/checkouts/` path |
| Resource bundles | SPM `resources:` parameter or asset catalog |

## Common Mistakes

- **Skipping audit**: Writing Package.swift without knowing current state
- **Ignoring xcconfig**: CocoaPods-generated xcconfigs persist, causing conflicts
- **Firebase monolithic import**: `import Firebase` doesn't exist in SPM — use per-module imports
- **CocoaLumberjack Swift module**: Use `CocoaLumberjackSwift` product, not `CocoaLumberjack`
- **ObjC module maps**: Some SPM packages don't generate module maps automatically
- **Resource bundles**: SPM doesn't create separate resource bundles by default
- **Not cleaning DerivedData**: Stale build cache causes mysterious errors
- **Binary frameworks**: Pods distributed as binary need special handling as SPM binary targets

See `docs/` for detailed technical documentation on each topic.
See `prompts/` for reusable AI prompt templates for each phase.
See templates/ for Package.swift templates for different scenarios.
