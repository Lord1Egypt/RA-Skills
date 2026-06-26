# Execution Resource Collaboration Profile

> Records capabilities, communication preferences, collaboration history, and platform invocation methods for all execution resources.
> This is the system's address book - read it once to know how to collaborate with each executor.

---

## 1. Profile Management Mechanism

### First Time Using the System

If this file contains only empty placeholders (no profiles yet), this is your first use. Initialize with these steps:

1. **Inventory available resources** - What executors are available in current environment? (agents, CLI tools, humans)
2. **Explore one by one** - Follow philosophy.md Capability 1 steps to understand each executor's type, capabilities, boundaries
3. **Create profiles** - Document each executor using the profile template below
4. **Fill communication infrastructure** - Record available communication tools in Section 7
5. **Dispatch first task** - Choose the best matching executor based on profiles

**Do not fill all profiles at once.** Fill what you need now; others can be filled at first collaboration.

### When to Create a Profile

- **First collaboration** - Create profile immediately when first collaborating with an executor
- **New tool introduced** - After installing new CLI tool or connecting new platform, explore then create profile
- **Team changes** - When new member joins, create profile based on initial interaction

### When to Update a Profile

- **After each project collaboration** - Append summary and lessons to collaboration records
- **After receiving feedback** - Write remember-this items into profile's accumulated rules
- **When discovering new capabilities/boundaries** - Update capability and boundary descriptions
- **When communication method changes** - Update invocation method

### Where Profiles Are Stored

All in this file (resource-profiles.md). Organized by type in sections.

### When to Use Profiles

- **Before dispatching tasks** - Read corresponding executor's profile
- **Before first collaboration** - Explore first, then create profile
- **After review/feedback** - Update profile's collaboration records and accumulated rules

## 2. Profile Template

Each executor has one profile, format as follows:

```markdown
### [Name]

**Basic Info**
- Type: [Agent with persistent memory / One-time executor / CLI tool / Human]
- First collaboration: [Date]
- Recent collaboration: [Date]

**Capabilities**
- [What they are good at, list]

**Boundaries**
- [What they cannot do / not good at, list]

**Communication Preferences**
- Language: [Chinese/English/Mixed]
- Format preference: [Structured instructions / Natural language / Code blocks]
- Special notes: [If any]

**Invocation Method**
- [Specific invocation command/API/operation method for current platform]

**Accumulated Rules** (from feedback)
- [Remember-this items received]

**Collaboration Records**
| Date | Project/Task | Performance | Lessons/Notes |
|------|--------------|-------------|---------------|
| | | | |
```

## 3. Agent Team Profiles

(Below are profile placeholders, fill based on actual collaboration experience)

### [To be filled - create after first collaboration]

## 4. CLI Coding Tool Profiles

(Fill based on tools you actually use)

### [CLI Tool Name]

**Basic Info**
- Type: CLI tool
- First collaboration: (To be filled)
- Recent collaboration: (To be filled)

**Capabilities**
- (To be filled based on actual usage experience)

**Boundaries**
- (Other boundaries to explore)

**Communication Preferences**
- Format: Specific coding instructions

**Invocation Method**
- (To be filled based on current environment)

**Accumulated Rules**
- (To accumulate after collaboration)

**Collaboration Records**
| Date | Project/Task | Performance | Lessons/Notes |
|------|--------------|-------------|---------------|
| | (To be filled) | | |

## 5. Subagent (Generic Model) Profiles

| Model ID | Strengths | Weaknesses | Suitable Tasks | Cost | Notes |
|----------|-----------|------------|----------------|------|-------|
| (To be filled based on actual usage) | | | | | |

## 6. Context Pruning Principles

Follow these when giving information to executors:
1. **Only relevant** - Give only what is needed to complete the task
2. **Conclusions not processes** - Use Node >= 18, not we tried 16 it did not work then...
3. **Mention known pitfalls** - Save executor trial time
4. **Sanitize sensitive info** - Use placeholders for API keys
5. **Less is more** - Information overload is worse than insufficient; executors will ask

## 7. Current Communication Infrastructure

This section records specific communication tools available in current environment. Change here when platform changes; other system files do not need updates.

| Scenario | Current Tool | Invocation Method | Notes |
|----------|--------------|-------------------|-------|
| (To be filled based on actual environment) | | | |

**Filling guide:** When first using the system, evaluate available communication tools and fill in the table above. Include:
- How to dispatch tasks to agents
- How to append messages/track progress
- How to invoke CLI tools
- How to communicate with humans

## 8. Runtime Environment Experience Records

This section records practical experience accumulated on current runtime platform - pitfalls encountered, techniques discovered, platform-specific usage.

### Experience Records

(Below are experiences accumulated through actual use, initially empty)

| Date | Experience | Source |
|------|------------|--------|
| | | |

---

This file is continuously updated with each collaboration