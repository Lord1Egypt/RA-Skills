---
name: i-skill
description: "Generates personalized interaction guides by analyzing user conversations. Invoke when users seek personalized responses, want AI assistants to better understand their preferences, or need customized service adaptation. Activation: '激活个性化' or 'personalization'."
version: "3.1.0"
tags: ["personalization", "user-profile", "ai-assistant", "conversation-analysis"]
activation_mode: "manual"
---

# i-skill - Personalized Interaction Profile

Analyzes user conversations to generate a structured personalization profile, enabling AI assistants to deliver customized service based on user preferences.

---

## 📁 Data Storage Location

**Default Location**: User data is stored in the skill's own `user_data/` directory (relative to the skill installation).

**Environment Variable Override**: You can set the `ISKILL_DATA_PATH` environment variable to specify a custom directory for storing user data.

**Important Notes**:
- All file paths referenced in this document refer to the `user_data/` directory (either default or via `ISKILL_DATA_PATH` override)
- The skill will never write outside the configured data directory
- Ensure proper permissions are set on the data directory to protect your personal information

## 🔒 Initialization Behavior & User Consent

**Key Principle**: No directories are created and no files are written to disk until the skill is manually activated.

### How It Works:
1. **Module Loading**: When the skill modules (`audit_log.py`, `consent_manager.py`, `myself_manager.py`) are first imported or instantiated, no file system operations occur.
2. **Lazy Initialization**: Directories and files are only created when the first write operation is performed, which happens *after* manual activation (user consent).
3. **Read Operations**: Reading existing files does not trigger initialization.

### Important:
- Manual activation (e.g., "激活个性化") represents user's consent to read/write personalization data
- Only destructive operations (delete/reset) require additional confirmation
- Initialization happens transparently as part of the first write operation after activation

---

## ⚡ Behavioral Anchors (High Priority — Always Obey)

> These rules remain active throughout the entire session after activation, regardless of context length.

1. **Identity Awareness**: When i-skill is active, every response should reflect understanding of the user profile. Not by mentioning it explicitly, but through word choice, recommendations, and decision-making.
2. **State Check**: **Important - Consent First**: No data is read automatically at session start. When the skill is manually activated (e.g., "激活个性化"), this action itself represents user consent. Only after activation:
   - Read `i-skill_state.json` (from data directory) to check current state
   - If `status == "active"`, read `myself.md` (from data directory) and use it as personalization context
3. **Language**: Use the user's preferred language as recorded in the profile. Default to Chinese for existing profiles.

---

## 🚀 Activation & Lifecycle

### Activation Commands
- "激活个性化" / "Activate personalization" / "Enable personalization"
- "personalization"

### Other Commands
- **View profile**: "查看档案" / "View my profile"
- **Manual update**: "更新档案" / "Update my profile"
- **Pause**: "暂停个性化" / "Pause personalization"
- **Resume**: "恢复个性化" / "Resume personalization"
- **Reset**: "重置档案" / "Reset profile"
- **Delete**: "删除档案" / "Delete profile"

### Activation Flow

1. User issues an activation command (e.g., "激活个性化")
2. **Manual activation implies consent**: The act of manually activating the skill represents user's consent to read/write personalization data
3. After activation:
   a. Read `i-skill_state.json` (from data directory) to check current state
   b. If already active, inform user: "Personalization is already active, profile version vX"
   c. If inactive, create/update `i-skill_state.json` to active, increment activation count by 1
   d. Read current `myself.md` (if it exists, from data directory), combine with conversation context, generate/update profile using the template below
   e. Display a brief profile summary to the user after generation

---

## 📋 Profile Format Specification

The profile is stored in `myself.md` (from data directory) and **must strictly follow this semi-structured template**:

```markdown
# User Profile

> Auto-generated on YYYY-MM-DD · Version vX · Refined over N iterations

## Basic Info
- **Name**: (User's name or AI-inferred)
- **Career Direction**: (Current primary career or job-seeking direction)
- **Tech Stack**: (Technologies frequently used or currently learning, comma-separated)

## Interests & Preferences
- **Core Interests**: (3-5 core interest areas)
- **Learning Focus**: (Areas currently being studied in depth)
- **Content Preference**: (Types of content preferred: hands-on projects / theoretical knowledge / industry trends / comprehensive analysis)

## Communication Style
- **Language**: (Primary language)
- **Style**: (Concise / Detailed / Casual / Professional)
- **Format Preference**: (Code examples / Plain text / Visual charts / Mixed)
- **Feedback Habit**: (Proactive / Implicit adjustment / Direct correction)

## Thinking Style
(Free-form description, 1-3 sentences. E.g.: Systematic thinker, analyzes problems holistically; pragmatic, prefers actionable solutions; curious, enjoys exploring new technology boundaries)

## Recent Focus
(2-5 recent topics or projects, in reverse chronological order)

## Observation Notes
(Free-form description of other stable traits, interesting details, or memorable preferences observed from conversations. 1-3 items, concise. Prefer prefixing each item with `[场景]` for traceability, e.g. `[2026-03-27, cogito讨论] 对"本质"有执念...`)
```

### Profile Generation Rules
- **Must include** all fixed section headers (Basic Info, Interests & Preferences, Communication Style, Thinking Style, Recent Focus, Observation Notes)
- **Fixed fields** (bold `**`-marked items) must appear under their corresponding sections
- **Free zones** ("Thinking Style", "Observation Notes") allow AI to demonstrate insightfulness, but keep it concise
- **Length limit**: Entire profile must not exceed 800 words
- **No fabrication**: Do not write information without evidence; mark uncertain fields as "To be observed"
- **On each update**: Regenerate completely rather than appending. Retain valuable content from previous versions, discard what's outdated
- **Confidence tags** (for uncertain or newly observed traits): Append `[~]` (1st observation, tentative) or `[!!]` (2nd observation, emerging) after the value. Tags are removed once confirmed (3+ consistent signals or user approval). Unmarked = confirmed. Example: `- **Learning Focus**: LLM应用开发 [~]Rust（待观察）`

---

## 🔄 Auto-Sensing Updates

> **PRIVACY FIRST**: All profile updates require explicit user consent. No automatic silent updates are performed without prior user approval.

### Update Triggers

When **any** of the following conditions are met, **ask the user for explicit consent** before updating the profile:

| Trigger | Description | Update Mode |
|---------|-------------|-------------|
| User demonstrates a new stable trait | Mentions a new career direction, new core interest, etc. | **Ask for consent first**, then update only if approved |
| User explicitly corrects profile errors | "I'm not a frontend dev, I do backend" | **Confirm correction first**, then update if approved |
| Conversation involves major changes | Career change, tech stack switch, etc. | **Show change summary first**, ask for consent before updating |
| 3+ consecutive rounds on a new topic | In-depth discussion of a topic not covered in the profile | **Ask for consent first**, then update only if approved |

### Update Thresholds

- **Do NOT trigger updates for**: Casual greetings, single technical Q&A, repeated discussions of known topics
- **Tweak vs. Rewrite**: If only 1-2 fields change, modify those fields directly; if 3+ fields change, regenerate the full profile
- **Prevent over-updating**: The same field must not be updated more than once within 5 conversation rounds (unless the user explicitly corrects it)
- **Signal exclusion**: Do NOT learn from silence/vague praise ("上次那个不错" context-dependent) / single events / hypothetical discussions / third-party preferences. Only explicit corrections, direct preference declarations, and 3+ repeated consistent signals count.
- **Gradual confirmation**: For non-explicit signals (e.g., topic drift → potential new interest), use confidence tags: 1st occurrence → `[~]` in Observation Notes only (no profile field change); 2nd → `[!!]`; 3rd → ask user before writing to profile fields.

### Consent-First Update Behavior

```
User: (Normal conversation content suggesting potential profile updates)
AI:   (Normal response content)
AI:   "I noticed some information that could update your profile. Would you like me to update it with these changes?
      - Career Direction: LLM App Development → Full-Stack Development
      - New Interest: Rust programming language
      (Reply 'yes' to confirm, 'no' to skip)"
[Only update if user explicitly says 'yes']
```

### Confirmed Update Behavior

```
AI: Detected potential updates to your profile:
    - Career Direction: LLM App Development → Full-Stack Development
    - New Interest: Rust programming language
    Confirm update? (Reply "yes" to confirm, "no" to skip)
```

---

## 🔒 Safe Operation Confirmations

> The following destructive operations **require explicit user confirmation** before execution.

### Modify Profile (Manual Trigger)

When the user proactively requests profile modification (not auto-sensing updates):
1. Show a **change summary** (which fields were added/modified/removed)
2. Wait for user confirmation ("Reply 'yes' to confirm")
3. Execute write after confirmation

### Reset Profile

When the user requests a profile reset:
1. Warn: **"Resetting will clear all personalization data and restore to a blank template. This action cannot be undone. Reply 'yes' to confirm."**
2. After user confirmation, clear `myself.md` and write initial template, reset `profile_version` to 0
3. Keep `i-skill_state.json` `status` unchanged

### Delete Profile

When the user requests profile deletion:
1. Warn: **"Deletion will permanently remove all personalization data (including profile and state), and i-skill will return to an inactive state. Reply 'yes' to confirm."**
2. After user confirmation:
   - Delete `myself.md`
   - Reset `i-skill_state.json` to `{"status": "inactive", "activation_count": 0, "profile_version": 0}`
3. Stop personalization service

### Pause / Resume

- **Pause**: Execute immediately, no confirmation required. Change state `status` to `paused`, retain all profile data
- **Resume**: Execute immediately, no confirmation required. Change state `status` back to `active`, re-read profile to resume personalization service

---

## 📂 File Reference

### Core Files (Stored in data directory)
- **`myself.md`** — User profile (with version tracking)
- **`i-skill_state.json`** — Activation state, statistics, profile_version

### Security Files (Managed by Scripts)
- **`./scripts/myself_manager.py`** — Safe profile file read/write (with auto-rollback)
- **`./scripts/validator.py`** — Data validation and PII sanitization
- **`./scripts/audit_log.py`** — Operation audit logging
- **`./scripts/consent_manager.py`** — Cross-skill authorization management
- **`myself_operations.log`** — File-level operation audit log (from data directory)
- **`audit_log.json`** / **`defensive_log.json`** — Audit logs (from data directory)
- **`consent_state.json`** — Authorization state (from data directory)

---

## 🎯 Design Principles

1. **AI-Driven, Tool-Assisted**: All decisions (when to update, what to update, whether to confirm) are made by the AI based on conversation context; Python scripts only handle safe file operations
2. **Structured + Flexible**: The profile format has a fixed skeleton to ensure consistency, while free-form areas allow the AI to demonstrate insightfulness
3. **Consent-First**: All data reads and writes require explicit user consent; no silent or automatic operations without user approval
4. **Anti-Bloat**: Each update regenerates rather than appends; total profile length is capped at 800 words
5. **Privacy First**: Never store raw conversations, only abstracted profile traits; PII detection and sanitization is ensured by `validator.py`

---

## 🔐 Security & Privacy Guidelines

### ISKILL_DATA_PATH Environment Variable

**Purpose**: The `ISKILL_DATA_PATH` environment variable allows you to specify a custom directory for storing user data.

**Security Recommendations**:
1. **Use a dedicated directory**: Always set `ISKILL_DATA_PATH` to a dedicated, isolated directory specifically for this skill
2. **Restrict permissions**: Ensure the directory has appropriate file permissions to prevent unauthorized access
3. **Avoid system directories**: Never point `ISKILL_DATA_PATH` to system directories or directories containing sensitive files
4. **Backup regularly**: Regularly backup the data directory to prevent data loss
5. **Default is safe**: If not set, the skill will use its own `user_data/` directory which is the safest option

### Data Protection

- All personal data is stored locally only; no data is sent to external servers
- PII (Personally Identifiable Information) is automatically detected and sanitized
- File operations include automatic rollback mechanisms to prevent data corruption
- Audit logs are maintained for all file operations
