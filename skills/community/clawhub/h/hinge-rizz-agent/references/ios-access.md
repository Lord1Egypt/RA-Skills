# iOS Access

There is no practical public Hinge API for the workflow this skill needs. On iOS, the realistic access path is UI automation.

## Recommended Path

Use Appium 2 with WebDriverAgent on a Mac.

What that gives you:

- launch or attach to the Hinge app by bundle id
- inspect the current view hierarchy
- tap buttons and tabs
- type into compose fields
- capture screenshots and page source for analysis

What you need:

- a Mac with Xcode installed
- an iPhone connected by USB or a booted iOS simulator
- Appium 2
- WebDriverAgent signing configured in Xcode
- the Hinge app already installed and logged in on the device

## Setup Outline

Use an Appium runtime workspace with Node and Appium available (for example `~/.openclaw/workspaces/hinge-automation`).

Useful commands from that workspace:

- `npm run appium`
- `npm run appium:doctor`
- `npm run appium:driver:list`
- `npm run sim:list`
- `npm run sim:boot`

The daemon can resolve this workspace in three ways:

1. `--workspace-dir <path>`
2. `HINGE_AUTOMATION_WORKSPACE=<path>`
3. default fallback: `../../workspaces/hinge-automation` relative to the skill, then current working directory

Suggested flow:

1. Start an iPhone or simulator and confirm the target app opens manually.
2. Start Appium locally from the runtime workspace.
3. Create a session with `scripts/appium-ios.js --create-session ...`.
4. Use `scripts/hinge-ios.js --session-id <id> --activate` to foreground Hinge.
5. Use `scripts/hinge-ios.js --session-id <id> --snapshot` to read the current state.
6. Use `--go-tab`, `--open-thread`, `--open-thread-profile`, `--scroll-down`, `--skip-current`, `--send-reply`, `--send-like-with-comment`, and `--send-rose-with-comment` for app-specific control.
7. Use `scripts/hinge-ai.js --mode profile|reply|rose --context-file ...` to generate analysis and suggested messages from live snapshots.
8. Fall back to `scripts/appium-ios.js --source`, `--find`, `--tap`, and `--type` only when a Hinge-specific action is missing.

## Why This Is Better Than OCR Mirroring

Screen mirroring alone can show the app, but it does not give reliable structured controls. Appium gives an accessibility tree and repeatable actions, which is the minimum needed for a useful agent workflow.

## What To Avoid

- private or jailbreak-only automation frameworks
- packet interception or reverse-engineering app traffic
- assuming selectors stay stable forever

Hinge will change UI details. Build around visible labels and be ready to re-tune selectors.

## Practical Limitation

The skill can be made operational against an Appium session, but the iOS bridge is still only as good as the app's accessibility tree. If key controls are unlabeled, the fallback is screenshot analysis plus coordinate taps, which is more fragile.

For Hinge specifically, a real iPhone is the practical target. The simulator proves the Appium stack, but Hinge itself is not a realistic simulator app target.
