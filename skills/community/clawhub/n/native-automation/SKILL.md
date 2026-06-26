---
name: native_automation
description: Apple Native Automation & Testing Skill
version: 1.0.0
domain: ios-macos
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/native_automation
metadata:
  clawdbot:
    emoji: 🤖
---

# Native Automation Skill

> **Philosophy**: Use Apple's first-party tools (XCTest, XCUITest, Instruments) as the source of truth for quality.

## Capabilities

1.  **Unit Testing Logic**: fast, isolated logic verification.
2.  **UI Testing**: End-to-end user flow verification.
3.  **Snapshot Testing**: Visual regression testing.
4.  **Performance Testing**: XCTMetric verification.
5.  **Accessibility Testing**: Automated audit via XCUITest.
6.  **Hero Flow Verification**: Integrated critical path testing (Input -> Process -> Connect).

## Usage

### 1. Execute Tests via Script
Always use the wrapper script to ensure correct scheme and destination settings.

```bash
./tools/run_native_tests.sh [mode]
```

**Modes:**
- `unit`: Run unit tests only (Logic layer).
- `ui`: Run UI tests only (Interaction layer).
- `fast`: Run unit + critical UI paths.
- `full`: Run ALL tests (including performance and snapshots).

### 2. Writing Tests
- **Unit**: Inherit from `XCTestCase`. Use `XCTAssert...`.
- **UI**: Inherit from `XCTestCase`. Use `XCUIApplication`.
- **Performance**: Use `measure(metrics:options:block:)`.

## Best Practices
- **Isolation**: Reset state before each UI test (`app.launchArguments += ["-reset"]`).
- **Accessibility**: Use `app.buttons["identifier"]` over static texts.
- **Concurrency**: Use `XCTestExpectation` for async code.
