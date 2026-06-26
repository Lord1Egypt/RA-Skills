---
name: i18n-swift
description: Swift internationalization patterns, String(localized:) usage, and semantic key naming for macOS/iOS apps
domain: ios-macos
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/i18n-swift
metadata:
  clawdbot:
    emoji: 🌐
---

# Swift Internationalization

Expert-level Swift i18n patterns for macOS/iOS applications. Covers string localization, semantic key naming, and best practices.

## When: to Use

Use this skill when:
- Adding localized strings to SwiftUI views
- Creating new localization keys
- Writing String(localized:) calls
- Organizing Localizable.strings files
- Reviewing i18n implementation in Swift projects

---

## Core Principles

### 1. String(localized:) Pattern

```swift
// Always use String(localized:) for user-facing text
Text(String(localized: "common.save"))
Button(String(localized: "sidebar.today"))

// Never hardcode strings
Text("Save")  // ❌ Wrong
```

### 2. Semantic Key Naming

Use `domain.feature.key` pattern:

```swift
// Good: Semantic keys
"app.name" = "TimeFlow"
"common.save" = "Save"
"sidebar.today" = "Today"
"settings.theme.title" = "Theme"

// Bad: Non-semantic keys
"saveButton" = "Save"
"viewTitle1" = "Today"
"themeTitle" = "Theme"
```

### 3. Localizable.strings Organization

Group by domain with MARK comments:

```swift
/*
 Localizable.strings
 TimeFlow
*/

// MARK: - App
"app.name" = "TimeFlow";

// MARK: - Common
"common.delete" = "Delete";
"common.save" = "Save";
"common.cancel" = "Cancel";

// MARK: - Sidebar
"sidebar.today" = "Today";
"sidebar.settings" = "Settings";
"sidebar.daily_note" = "Daily Note";

// MARK: - GTD Navigation
"gtd.inbox" = "Inbox";
"gtd.today" = "Today";
"gtd.projects" = "Projects";
```

---

## Key Naming Conventions

| Domain | Feature | Examples |
|--------|---------|----------|
| `app` | - | `app.name` |
| `common` | delete, save, cancel | `common.delete`, `common.save` |
| `sidebar` | today, settings, search | `sidebar.today`, `sidebar.settings` |
| `home`` today, progress, timeline | `home.today`, `home.progress` |
| `gtd` | inbox, next, projects | `gtd.inbox`, `gtd.next` |
| `settings` | theme, language, sync | `settings.theme.title` |
| `sync` | idle, syncing, failed | `sync.idle`, `sync.syncing` |

---

## SwiftUI Usage Patterns

### Text Component

```swift
struct TodayView: View {
    var body: some View {
        VStack {
            Text(String(localized: "home.today"))
                .font(.title)

            Text(String(localized: "home.no_events"))
                .foregroundStyle(.secondary)
        }
    }
}
```

### Button with Localized String

```swift
Button(String(localized: "common.save")) {
    // Save action
}
.disabled(isSaving)
```

### Navigation Titles

```swift
NavigationLink(destination: SettingsView()) {
    Label(String(localized: "sidebar.settings"), systemImage: .gear)
}
```

---

## Best Practices

| Practice | Reason |
|----------|--------|
| Use `String(localized:)` | Prevents hardcoding, enables i18n |
| Semantic key names | Self-documenting, easier maintenance |
| Group with `// MARK:` | Organized, searchable strings files |
| Use domain.feature.key | Clear ownership, prevents collisions |
| Update all languages together | Prevents missing translations |
| Avoid format strings in keys | Use Swift interpolation instead |

---

## String Interpolation

```swift
// Good: Use Swift interpolation
let message = String(localized: "sync.completed.count")
    .replacingOccurrences(of: "{count}", with: "\(count)")

// Alternative: Use String(format:) for localized format strings
let formatted = String(
    localized: "sync.completed.count",
    comment: "Number of items synced"
)

// Localizable.strings entry:
// "sync.completed.count" = "Synced %d items";
```

---

## Common Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Hardcoded strings | Can't localize | Always use `String(localized:)` |
| Non-semantic keys | Difficult to maintain | Use `domain.feature.key` pattern |
| Missing translations | Shows key name | Add entries to all .strings files |
| Format strings in keys | Ambiguous values | Use Swift interpolation |
| Duplicate keys | Confusing maintenance | Search before adding |

---

## Testing Patterns

```swift
func testLocalizationKeys() {
    // Verify all keys exist in Localizable.strings
    let keys = ["app.name", "common.save", "sidebar.today"]
    for key in keys {
        let localized = String(localized: key)
        XCTAssertNotEqual(localized, key, "Key not found: \(key)")
    }
}
```

---

## Running Tests

```bash
# Test localization
xcodebuild test -scheme YourApp \
  -destination 'platform=macOS' \
  -only-testing:'YourAppTests/LocalizationTests/testKeysExist'
```
