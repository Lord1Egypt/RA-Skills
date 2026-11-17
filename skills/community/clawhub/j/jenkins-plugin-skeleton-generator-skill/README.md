# Jenkins Plugin Skeleton Generator

> Describe your plugin in one sentence — the AI generates a complete Jenkins plugin project skeleton.

[![SKILLHUB](https://img.shields.io/badge/SKILLHUB-Published-3b82f6)](https://www.skillhub.cn/skills/jenkins-plugin-skeleton-generator-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-Published-f97316)](https://clawhub.ai/leoyim/skills/jenkins-plugin-skeleton-generator-skill)

[中文](README.zh.md)

## Installation

Search for "Jenkins Plugin Skeleton Generator" on [SKILLHUB](https://www.skillhub.cn/skills/jenkins-plugin-skeleton-generator-skill) or [ClawHub](https://clawhub.ai/leoyim/skills/jenkins-plugin-skeleton-generator-skill) and install, or run in terminal:

```bash
openclaw skills install @leoyim/jenkins-plugin-skeleton-generator-skill
```

## Quick Start

Say something like this to the AI in OpenCode / Codex / Claude Code to trigger the skill:

- "Create a Jenkins plugin for me"
- "I want to develop a Jenkins plugin, Jenkins version 2.401.1"
- "Generate a Jenkins Builder plugin skeleton"

The AI will ask for any missing information — no need to prepare everything upfront.

## What You'll Need

The AI will guide you through these questions:

| Information | Description | Example |
|------|------|------|
| Jenkins version | Minimum target Jenkins version | `2.401.1` |
| JDK version | Java version for the project | `11`, `17`, `21` |
| Maven version | (Optional) Local Maven version | `3.9` |
| groupId | Maven coordinate | `com.example.jenkins` |
| artifactId | Project identifier | `hello-plugin` |
| Package name | Java package path | `com.example.jenkins.hello` |
| Plugin type | Choose an extension point | See below |
| Output language | Language for generated code comments & README | `zh-CN`, `en`, `ja`, etc. |
| Async / Persistence / Global config | Extra feature toggles | Yes / No |

## Supported Plugin Types

- **Builder** — Custom build step (most common)
- **Publisher** — Post-build processing (notifications, archiving, etc.)
- **Trigger** — Cron schedules or SCM change triggers
- **Action** — Add UI action buttons
- **RunListener** — Listen for build lifecycle events
- **ComputerListener** — Listen for node online/offline events
- **QueueTaskDispatcher** — Task dispatch filtering

## Usage Examples

### Example 1: Simple Builder Plugin

**You say**:

> Create a Jenkins Builder plugin, Jenkins 2.401, JDK 17, artifactId: my-build-step

**AI generates**:

```
my-build-step/
├── pom.xml              # With Jenkins official repo config
├── README.md            # Complete usage guide
├── .gitignore
└── src/
    └── main/
        ├── java/.../
        │   └── MyBuildStepBuilder.java   # Builder extension code
        └── resources/.../
            └── MyBuildStepBuilder/
                ├── config.jelly           # Config UI
                └── help.html
```

### Example 2: Listener with Persistence

**You say**:

> Develop a Jenkins RunListener plugin, Jenkins 2.426, JDK 21, artifactId: build-auditor, with persistence config, package: com.company.audit, output in Chinese

**AI generates**:

```
build-auditor/
├── pom.xml
├── README.md
├── .gitignore
└── src/
    └── main/
        ├── java/com/company/audit/
        │   ├── BuildAuditorListener.java    # RunListener
        │   └── config/
        │       └── PluginConfiguration.java  # Persistence config class
        └── resources/
```

### Example 3: Specify Output Language

**You say**:

> Generate a Jenkins plugin, Builder type. Jenkins 2.440, JDK 17, artifactId: my-step. Output README and code comments in Japanese.

> (Or in Chinese: "生成的代码注释和 README 用中文")

## New to Jenkins Plugin Development?

Here's a 10-second overview of the key concepts:

| Concept | One-liner | What you need |
|------|-----------|-------------|
| **Extension Point** | Jenkins' "hooks" — plugins implement them to inject logic | Pick one type (Builder is most common) |
| **Descriptor** | Describes "what this plugin is called and how it displays" | Auto-generated, ignore |
| **config.jelly** | Plugin config page written in XML | The skill auto-selects controls based on your field types |
| **hpi** | Jenkins plugin package format (like WAR for web apps) | Auto-generated after `mvn clean package` |
| **DataBoundConstructor** | Marks the constructor that receives config page parameters | Auto-added, no hand-writing needed |

**First-time tip**: Just say "Create a Jenkins Builder plugin, Jenkins 2.401.1, JDK 17" — the skill handles the rest.

## After Generation

The AI will also provide follow-up guidance:

1. Run `mvn clean package` to build
2. Use `mvn hpi:run` for local Jenkins testing
3. Upload the generated `.hpi` via Jenkins Plugin Manager
4. Restart Jenkins and verify functionality

## Known Limitations

Be mindful of these scenarios:

| Scenario | Impact | Suggestion |
|------|------|------|
| Wrong version format (e.g. `Jenkins 3.0`) | May generate incorrect Parent POM version | Double-check against the [Jenkins/Java compatibility table](https://www.jenkins.io/doc/book/platform-information/support-policy-java/index.html) |
| Incompatible version combo (e.g. Jenkins 2.426 + JDK 11) | Build or runtime errors | Ensure JDK version ≥ Jenkins' minimum requirement |
| Missing required info | Incomplete generated project | Walk through the "What You'll Need" checklist |
| Custom extension point (not in the 7 standard types) | Code for that type won't be generated | Choose the closest type and manually adapt |
| Complex plugins (multiple extension points) | Only one primary extension point skeleton per generation | Generate separately and merge |

Check `references/troubleshooting.md` or describe what you're seeing in the conversation.

## Notes

- No default versions are assumed — always specify Jenkins and JDK versions
- Uses Jenkins official Maven repository by default — no extra `settings.xml` needed
- Generated code includes comments and is ready for further development
- **Multi-language support**: generated comments and README can be in Chinese, English, Japanese, or any other language — just tell the AI your preference
