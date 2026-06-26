---
name: openclaw-character-creator
description: >-
  Build high-consistency AI character personas for OpenClaw with a full 6-file
  model. Use when creating a new character (创建角色, 创建clone, 新建人物),
  switching the active character (/shift, 切换角色), or managing the character
  roster. Supports well-known public figures and fictional/original characters,
  generating 3 auxiliary files (research layer) + 3 main files (runtime layer)
  with workspace scaffolding and global role registration. Requires: python3.
  Writes to ~/.openclaw/ (names and paths only — no credentials stored).
metadata: >-
  {"openclaw":{"emoji":"🎭","requires":{"anyBins":["python3"]},"os":["linux","darwin","win32"]}}
config_paths:
  - ~/.openclaw/ROLES.json
  - ~/.openclaw/workspace
  - ~/.openclaw/workspace-*
---

# OpenClaw Character Creator

Create high-consistency AI character personas for OpenClaw. Each character gets a dedicated workspace with 6 persona files, proper tooling, and registration in the global role roster.

## Paths

All relative paths in this skill (e.g., `references/`, `scripts/`) are relative to this skill's directory — the folder containing this `SKILL.md` file. Resolve them from there.

Standard install location: `~/.openclaw/skills/openclaw-character-creator/`

## Character Types

| Type | Trigger phrases | System instruction |
|------|----------------|--------------------|
| **Well-known figure** (世界知名人物) | real person name, public figure, celebrity, historical figure | `wellknown_system_instruction.md` |
| **Fictional / original character** (虚拟人物) | original character, anime/game character, invented persona | `nonwellknown_system_instruction.md` |

## Quick Reference: 6-File Architecture

Every character produces 6 files. Three are **auxiliary** (research/reference layer) and three are **main** (runtime layer). OpenClaw only loads the 3 main files at startup, so auxiliary files must be referenced from the main files and from `AGENTS.md`.

### Well-known figures

| Layer | File | Role |
|-------|------|------|
| Auxiliary | `CHRONOLOGY.md` | Timeline & era-sensitive personality shifts |
| Auxiliary | `VOICEPRINT.md` | Speech patterns & expression model |
| Auxiliary | `BOUNDARIES.md` | What can/cannot be said & how to deflect |
| Main | `IDENTITY.md` | Surface identity — "instantly recognizable" |
| Main | `SOUL.md` | Behavioral engine — "stays in character" |
| Main | `USER.md` | Relationship memory — "feels personal" |

### Fictional / original characters

| Layer | File | Role |
|-------|------|------|
| Auxiliary | `BACKGROUND.md` | Origin, growth environment, life stage |
| Auxiliary | `VOICEPRINT.md` | Speech patterns & expression model |
| Auxiliary | `PERSONA_RULES.md` | Personality rules, values, MBTI hypothesis |
| Main | `IDENTITY.md` | Surface identity — "instantly recognizable" |
| Main | `SOUL.md` | Behavioral engine — "stays in character" |
| Main | `USER.md` | Relationship memory — "feels personal" |

## Creation Workflow

### Step 1: Determine character type

Ask the user or infer from context:
- If the character is a real, publicly known person → **well-known**
- If the character is fictional, from anime/games/novels, or an original creation → **fictional**

### Step 2: Gather character information

**For well-known figures:**
- Name (and any era/version preference, e.g. "2015-era Kobe")
- Target language for output
- Any specific relationship framing the user wants

**For fictional characters:**
- Name, age, gender
- Origin / world setting
- A photo or visual reference (optional)
- User's text description of the character
- Intended relationship mode (companion, mentor, friend, romantic interest, etc.)

### Step 3: Read the system instruction

Based on character type, read the full system instruction file bundled with this skill:

- **Well-known:** Read `references/wellknown_system_instruction.md` (relative to this skill's directory)
- **Fictional:** Read `references/nonwellknown_system_instruction.md` (relative to this skill's directory)

The system instruction defines exactly what each of the 6 files must contain, the generation logic, quality standards, and failure modes to avoid. Follow it as your primary authoring guide.

### Step 4: Generate the 6 files

Follow the system instruction's specifications for each file. Key rules:

1. **Generate auxiliary files first**, then compress them into main files
2. Each file must follow the exact section structure defined in the system instruction
3. Auxiliary files are the "truth source"; main files are compressed for runtime
4. `USER.md` starts nearly empty — it only records real interaction history, never prefilled from character research
5. Output in the language matching the character's natural expression (or user's preference)

### Step 5: Create workspace

Generate a short UUID (first 8 chars) and create the workspace:

```bash
CHAR_UUID=$(python3 -c "import uuid; print(str(uuid.uuid4())[:8])")
CHAR_NAME="<lowercase-ascii-name>"
WORKSPACE_PATH="$HOME/.openclaw/workspace-${CHAR_NAME}-${CHAR_UUID}"
mkdir -p "$WORKSPACE_PATH"/{.openclaw,avatars,generated,memory}
```

### Step 6: Write all files to workspace

Write each of the 6 generated files to `$WORKSPACE_PATH/`:

For well-known:
- `CHRONOLOGY.md`, `VOICEPRINT.md`, `BOUNDARIES.md` (auxiliary)
- `IDENTITY.md`, `SOUL.md`, `USER.md` (main)

For fictional:
- `BACKGROUND.md`, `VOICEPRINT.md`, `PERSONA_RULES.md` (auxiliary)
- `IDENTITY.md`, `SOUL.md`, `USER.md` (main)

**Referencing auxiliary files in main files:** At the top of each main file, add a metadata comment so the runtime agent knows where to find deeper context:

For well-known IDENTITY.md:
```markdown
<!-- references: CHRONOLOGY.md, VOICEPRINT.md, BOUNDARIES.md -->
```

For well-known SOUL.md:
```markdown
<!-- references: CHRONOLOGY.md, VOICEPRINT.md, BOUNDARIES.md -->
```

For fictional, replace with `BACKGROUND.md, VOICEPRINT.md, PERSONA_RULES.md`.

Also create these scaffolding files:

**HEARTBEAT.md:**
```markdown
# Heartbeat
last_seen: (will be updated automatically)
```

**TOOLS.md:**
```markdown
# Tools
(local tool notes will be added as you discover and use tools)
```

**MEMORY.md:**
```markdown
# Memory
(curated long-term memory — significant events, lessons, preferences)
```

**`.openclaw/workspace-state.json`:**
```json
{
  "version": 1,
  "createdAt": "<ISO-timestamp>",
  "characterName": "<display-name>",
  "characterType": "<wellknown|fictional>",
  "workspacePath": "<full-workspace-path>",
  "originalWorkspacePath": "<full-workspace-path>"
}
```

### Step 7: Create AGENTS.md

Read the template at `references/agents_template.md` in this skill's directory. Fill in these placeholders:

- `{{CHARACTER_NAME}}` → character's display name
- `{{AUXILIARY_FILES_SECTION}}` → replace with the appropriate block below:

**For well-known figures:**
```markdown
| File | When to consult |
|------|----------------|
| `CHRONOLOGY.md` | Era-specific questions, timeline context, personality shifts across periods |
| `VOICEPRINT.md` | Calibrating speech patterns, sentence rhythm, expression style |
| `BOUNDARIES.md` | Deciding what can be said, how to deflect, privacy boundaries |
```

**For fictional characters:**
```markdown
| File | When to consult |
|------|----------------|
| `BACKGROUND.md` | Origin story, growth environment, life stage, worldview formation |
| `VOICEPRINT.md` | Calibrating speech patterns, sentence rhythm, expression style |
| `PERSONA_RULES.md` | Personality rules, value hierarchy, MBTI-informed behavior, boundary rules |
```

Write the filled-in result to `$WORKSPACE_PATH/AGENTS.md`.

### Step 8: Register in ROLES.json

```bash
python3 ~/.openclaw/skills/openclaw-character-creator/scripts/register_role.py "<display-name>" "$WORKSPACE_PATH"
```

### Step 9: Confirm to user

Tell the user:
- Character name and type
- Workspace path
- Which files were created
- How to switch to this character with `/shift`

---

## /shift Command — Switch Active Character

When the user types `/shift`:

1. **List available roles:**
   ```bash
   python3 ~/.openclaw/skills/openclaw-character-creator/scripts/shift_role.py list
   ```

2. **Ask the user to choose** a character name from the list.

3. **Execute the switch:**
   ```bash
   python3 ~/.openclaw/skills/openclaw-character-creator/scripts/shift_role.py "<chosen-name>"
   ```

The script handles:
- Saving the current `~/.openclaw/workspace` back to its original unique path
- Moving the target character's workspace to `~/.openclaw/workspace`
- Updating `ROLES.json` with new paths

After shifting, confirm to the user which character is now active.

---

## Files Written

This skill reads and writes the following paths under the user's home directory:

| Path | Purpose |
|------|---------|
| `~/.openclaw/ROLES.json` | Role registry — maps character names to workspace paths. No credentials stored. |
| `~/.openclaw/workspace-<name>-<uuid>/` | Per-character workspace with persona files, scaffolding, and workspace state. |
| `~/.openclaw/workspace/` | Symlink-like active workspace — the currently active character is moved here by `/shift`. |

**No service keys or credentials are stored in any of these files.** `ROLES.json` contains only
`{name, workspacePath}` pairs. Workspace state files contain only paths and timestamps.

## Security Boundaries

This skill reads and writes ONLY within the paths declared in the frontmatter `config_paths`:

- `~/.openclaw/ROLES.json`
- `~/.openclaw/workspace`
- `~/.openclaw/workspace-*`

**Hard rules:**

1. **Do NOT read or write files outside `~/.openclaw/`** (except reading this skill's own
   `references/` directory for system instructions and templates).
2. **Do NOT store service keys, tokens, or any credentials** in workspace files, `ROLES.json`,
   or any other file. `ROLES.json` contains only `{name, workspacePath}` pairs.
3. **Do NOT execute arbitrary shell commands.** Only run the specific `python3` scripts bundled
   with this skill (`scripts/register_role.py`, `scripts/shift_role.py`) and standard `mkdir`.
4. **Do NOT fetch files from the network.** If the user does not provide a profile photo, leave
   the `profile.jpeg` slot empty rather than downloading images from the internet.

## Operating Rules

1. **Never skip auxiliary files.** Always generate all 6 files even if the user only asks for "a quick character." The auxiliary files prevent persona drift.

2. **Auxiliary files feed main files, not the reverse.** Generate CHRONOLOGY/BACKGROUND → VOICEPRINT → BOUNDARIES/PERSONA_RULES first, then compress into IDENTITY → SOUL → USER.

3. **USER.md starts minimal.** Only contain the template structure and update rules. Real content comes from actual interactions.

4. **Follow the system instruction strictly.** The wellknown/nonwellknown instruction files define exact section requirements, quality bars, and anti-patterns. Do not improvise the file structure.

5. **Language consistency.** Generate in the character's most natural language or the user's preferred language. If the character is Chinese-speaking or the user speaks Chinese, generate in Chinese.

6. **Profile image.** If the user provides a photo, save it as `profile.jpeg` (or `.png`) in the
   character workspace. Do NOT download images from the internet or search the local filesystem
   outside `~/.openclaw/` for photos.

7. **Existing characters.** If `~/.openclaw/ROLES.json` shows a character with the same name already exists, warn the user before overwriting.
