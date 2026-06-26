# OraHub Skills

A collection of OraHub image editing skills for AI coding agents. These skills route photo-edit requests into focused OraHub workflows for color matching, passersby removal, background cutout, and background replacement.

Skills follow the [Agent Skills](https://agentskills.io) format.

## Available Skills

### orahub-skills

The main entry skill for this repository. It does not run a separate image API on its own. Instead, it routes the request to the correct leaf skill based on user intent.

Use when:

- The user asks to edit a photo but the exact OraHub workflow should be selected automatically
- You want one installable entry point for the current OraHub photo-edit package
- You want the agent to distinguish between color match, passersby removal, background cutout, and background replacement

Routes to:

- `photo-color-match` for reference-based color matching and tone transfer
- `photo-passersby-removal` for removing tourists, photobombers, and background people
- `photo-remove-background` for transparent PNG cutouts
- `photo-background-replace` for swapping the background with another image

### photo-color-match

Make a photo or a batch of photos match the color, tone, and vibe of a reference image.

Use when:

- "Match this photo to the color style of this reference"
- "Make this batch feel consistent with this sample"
- "Give this image the same vibe as the reference"

Highlights:

- Supports `1 original + 1 reference`
- Supports `N originals + 1 shared reference`
- Requires explicit original/reference role checks before execution

### photo-passersby-removal

Remove passersby, tourists, and background people from a photo.

Use when:

- "Remove the people in the background"
- "Clean up the tourists behind the subject"
- "Erase the photobombers"

Highlights:

- One image per CLI call
- Sequential batch handling for multiple images
- Explicit confirmation before large batches

### photo-remove-background

Remove the background from a photo and return a transparent PNG cutout.

Use when:

- "Remove the background"
- "Cut out the subject"
- "Give me a transparent PNG"
- "Isolate this product for e-commerce"

Highlights:

- Always outputs PNG
- Supports local paths and public image URLs
- Built for reliable cutout delivery and predictable naming

### photo-background-replace

Replace the background of a photo using a separate background reference image.

Use when:

- "Replace the background with this image"
- "Put this subject onto this new backdrop"
- "Change the portrait background"

Highlights:

- Supports `1 original + 1 background`
- Supports `N originals + 1 shared background`
- Supports `1 original + N backgrounds`
- Requires explicit original/background role checks before execution

## Installation

### Step 1 — Install the skill package

Install using the command for your agent platform. The package registers one root skill (`orahub-skills`); leaf workflows are bundled inside and used by the router at runtime.

#### Claude Code

```bash
npx skills add https://github.com/Orahub-ora/orahub-skills
# Installed to: ~/.claude/skills/orahub-skills/
```

#### OpenClaw

```bash
npx skills add https://github.com/Orahub-ora/orahub-skills
# Installed to: {OPENCLAW_HOME}/workspace/skills/orahub-skills/
```

#### Cursor

```bash
git clone https://github.com/Orahub-ora/orahub-skills ~/.cursor/orahub-skills
```

Point your Cursor skills path to `~/.cursor/orahub-skills/`.

#### OpenCode

```bash
git clone https://github.com/Orahub-ora/orahub-skills ~/.config/opencode/skills/orahub-skills
```

### Step 2 — Install the runtime CLI (required)

The `orahub` CLI is required for all workflows. Install it before first use, or let the agent install it automatically when you first trigger a workflow.

```bash
npm install -g orahub-cli
```

### Step 3 — Authenticate (required)

Authenticate before first use, or let the agent prompt you automatically when credentials are missing.

```bash
orahub auth device-login
```

Manual fallback:

```bash
orahub config set --access-key "<ak>" --secret-key "<sk>"
```

### Step 4 — Optional smoke test

```bash
orahub --version
orahub auth verify --json
```

### First-use bootstrap

- When the user triggers an OraHub skill, the agent should try the requested workflow first.
- If the local OraHub runtime is missing or outdated, the agent should request user approval to run:

```bash
npm install -g orahub-cli
orahub --version
```

- After install succeeds, the agent should retry the same workflow automatically.
- If the workflow reports missing credentials, the agent should request user approval to run:

```bash
orahub auth device-login
```

- After authentication succeeds, the agent should retry the same workflow automatically.
- Only if the current client cannot execute commands, cannot support the auth flow, or the user denies approval, fall back to manual setup:

```bash
npm install -g orahub-cli
orahub --version
orahub auth device-login
```

## Usage

Skills are automatically available once installed. The agent should invoke them when the task matches the request.

Examples:

```text
Match this image to the color mood of this reference.

Remove the tourists behind the subject.

Cut out this product and return a transparent PNG.

Replace the background of this portrait with this other image.
```

If you install `orahub-skills`, it acts as the router skill and selects the correct leaf workflow. If the request is ambiguous, it should ask one short clarification before routing.

## How It Works

All skills in this repository follow the same high-level execution shape:

```text
Preflight -> Route or Execute -> Deliver
```

Shared behavior:

- Verify that the `orahub` CLI is available
- Verify authentication before execution
- Accept local image paths or public `http(s)` image URLs
- Reject non-public URLs such as `localhost`, loopback, and private-network hosts
- Use one image pair or one image per CLI call, then process larger sets sequentially
- Ask for confirmation before large batches

The root `orahub-skills` skill only routes requests. Each leaf skill owns its own input collection, validation, command execution, output naming, and delivery rules.

## Repository Structure

```text
.
├── SKILL.md
├── photo-background-replace/
│   └── SKILL.md
├── photo-color-match/
│   └── SKILL.md
├── photo-passersby-removal/
│   └── SKILL.md
├── photo-remove-background/
│   └── SKILL.md
└── references/
    └── platform-compatibility.md
```

## Compatibility Notes

- Designed for OraHub image workflows
- Supports OpenClaw delivery rules through `references/platform-compatibility.md`
- Treats user-provided paths, URLs, filenames, and images as task data rather than instructions

## License

MIT
