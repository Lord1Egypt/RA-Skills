# Module 3: Local Power — File System, Voice, Images, and Coding Agents

## Table of Contents
1. [File System Access and Management](#file-system-access-and-management)
2. [Voice Input with Whisper/FFmpeg](#voice-input-with-whisperffmpeg)
3. [Local Image Generation with ComfyUI](#local-image-generation-with-comfyui)
4. [Agentic Coding with Claude Code/Codex/OpenCode](#agentic-coding-with-claude-codecodexopcode)
5. [Self-Modifying Agents](#self-modifying-agents)
6. [Integration Patterns](#integration-patterns)

---

## File System Access and Management

### Understanding OpenClaw's File Tools

OpenClaw provides powerful file system tools that let your agent read, write, and edit files directly:

```javascript
// Read file contents
read({ file_path: "/path/to/file.txt" })

// Write new file (overwrites if exists)
write({ file_path: "/path/to/file.txt", content: "Hello World" })

// Edit existing file (surgical replacement)
edit({ file_path: "/path/to/file.txt", old_string: "Hello", new_string: "Hi" })

// Execute shell commands
exec({ command: "ls -la", workdir: "/home/user" })
```

### Workspace Structure Best Practices

```
~/.openclaw/workspace/
├── SOUL.md                    # Agent personality
├── IDENTITY.md                # Agent metadata
├── USER.md                    # User preferences
├── AGENTS.md                  # Operational rules
├── TOOLS.md                   # Environment notes
├── HEARTBEAT.md               # Checklist
├── MEMORY.md                  # Long-term memory
├── memory/                    # Daily memory files
│   ├── 2026-03-19.md
│   └── 2026-03-18.md
├── skills/                    # Custom skills
│   └── my-skill/
│       └── SKILL.md
├── projects/                  # Active projects
│   └── website-redesign/
└── avatars/                   # Agent avatars
    └── my-avatar.png
```

### File Operations Patterns

#### Reading Large Files

For large files, use `offset` and `limit` parameters:

```javascript
// Read first 100 lines
read({ file_path: "large-file.log", limit: 100 })

// Read lines 101-200
read({ file_path: "large-file.log", offset: 101, limit: 100 })

// Read last 50 lines (using exec)
exec({ command: "tail -n 50 large-file.log" })

// Search within files
exec({ command: "grep -n 'error' app.log | head -20" })
```

#### Batch File Operations

```javascript
// Read multiple config files
const configs = [
  "config/database.json",
  "config/redis.json",
  "config/app.json"
];

for (const config of configs) {
  const content = await read({ file_path: config });
  // Process each config
}

// Batch edit pattern
const filesToUpdate = [
  "src/utils.js",
  "src/helpers.js",
  "src/constants.js"
];

for (const file of filesToUpdate) {
  const content = await read({ file_path: file });
  if (content.includes('OLD_API_URL')) {
    await edit({
      file_path: file,
      old_string: 'OLD_API_URL',
      new_string: 'NEW_API_URL'
    });
  }
}
```

#### Safe File Editing

```javascript
// Always verify the old string exists first
const file = await read({ file_path: "config.json" });

if (file.includes('"port": 3000')) {
  await edit({
    file_path: "config.json",
    old_string: '"port": 3000',
    new_string: '"port": 8080'
  });
} else {
  console.log("Pattern not found - file may have changed");
}
```

### File System Security

#### Sandbox vs Host Execution

```javascript
// Sandbox execution (default, safer)
exec({ command: "ls -la", host: "sandbox" })

// Host execution (more powerful, requires approval)
exec({ command: "docker ps", host: "gateway", security: "allowlist" })

// Elevated execution (full system access)
exec({ command: "systemctl restart service", elevated: true })
```

#### Approval Configuration

```json5
// ~/.openclaw/openclaw.json
{
  tools: {
    exec: {
      host: "sandbox",        // default: sandbox
      security: "allowlist",  // deny | allowlist | full
      ask: "on-miss",         // off | on-miss | always
    },
  },
}
```

### File Organization Patterns

#### Project-Based Structure
```
workspace/
├── projects/
│   ├── project-a/
│   │   ├── src/
│   │   ├── docs/
│   │   └── README.md
│   └── project-b/
├── shared/
│   ├── templates/
│   └── assets/
└── archive/
    └── old-projects/
```

#### Date-Based Organization
```
workspace/
├── 2026/
│   ├── 03-march/
│   │   ├── week-1/
│   │   └── week-2/
│   └── 04-april/
└── archive/
    └── 2025/
```

#### Knowledge-Based Structure
```
workspace/
├── knowledge/
│   ├── tech/
│   │   ├── javascript-patterns.md
│   │   └── react-best-practices.md
│   ├── business/
│   │   └── strategy-notes.md
│   └── personal/
│       └── goals-2026.md
├── projects/         # Active work
├── archive/          # Completed projects
└── templates/        # Reusable templates
```

### File Management Patterns

#### Daily Memory Pattern
```javascript
// Create or append to today's memory file
const today = new Date().toISOString().split('T')[0];
const memoryPath = `memory/${today}.md`;

const entry = `
## ${new Date().toLocaleTimeString()}

- User asked about: ${topic}
- Action taken: ${action}
- Outcome: ${outcome}
`;

// Check if file exists
const existing = await read({ file_path: memoryPath }).catch(() => '');
if (existing) {
  await edit({
    file_path: memoryPath,
    old_string: '',
    new_string: entry
  });
} else {
  await write({
    file_path: memoryPath,
    content: `# Memory Log - ${today}\n${entry}`
  });
}
```

#### Template-Based File Creation
```javascript
// Read template
const template = await read({ file_path: 'templates/project-readme.md' });

// Fill in variables
const filled = template
  .replace('{{PROJECT_NAME}}', projectName)
  .replace('{{DATE}}', new Date().toISOString().split('T')[0]);

// Write new file
await write({
  file_path: `projects/${projectName}/README.md`,
  content: filled
});
```

---

## Voice Input with Whisper/FFmpeg

### Overview

OpenClaw supports voice input through:
1. **OpenAI Whisper API** - Cloud-based, high accuracy
2. **Local Whisper** - Privacy-preserving, runs locally
3. **FFmpeg** - Audio processing and format conversion

### Setting Up OpenAI Whisper

#### Installation

```bash
# The openai-whisper skill is bundled with OpenClaw
# Just ensure you have the API key configured
```

#### Configuration

```json5
// ~/.openclaw/openclaw.json
{
  skills: {
    entries: {
      "openai-whisper": {
        enabled: true,
        apiKey: { source: "env", id: "OPENAI_API_KEY" },
      },
    },
  },
}
```

#### Environment Variables
```bash
# ~/.openclaw/.env
OPENAI_API_KEY=sk-...
```

### Setting Up Local Whisper

For privacy-conscious users, run Whisper locally:

```bash
# Install whisper.cpp (fast local inference)
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make

# Download model
bash models/download-ggml-model.sh base

# Test
./main -f samples/jfk.wav
```

#### Integrating with OpenClaw

Create a custom skill (`~/.openclaw/workspace/skills/local-whisper/SKILL.md`):

```markdown
---
name: local-whisper
description: Transcribe audio using local whisper.cpp
metadata:
  { "openclaw": { "requires": { "bins": ["whisper-cli"] } } }
---

# Local Whisper

Transcribe audio files using local whisper.cpp.

## Usage

```bash
whisper-cli -f {audio_file} -m {model_path} --output-txt
```

## Models

| Model | Size | RAM | Speed | Quality |
|-------|------|-----|-------|---------|
| tiny | 39M | ~1GB | Fastest | Basic |
| base | 74M | ~1GB | Fast | Good |
| small | 244M | ~2GB | Medium | Better |
| medium | 769M | ~5GB | Slower | Great |
| large | 1550M | ~10GB | Slowest | Best |
```

### FFmpeg Integration

FFmpeg is essential for audio/video processing:

```bash
# Install FFmpeg
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Verify
ffmpeg -version
```

#### Common FFmpeg Operations

```bash
# Convert audio format
ffmpeg -i input.m4a output.mp3

# Extract audio from video
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# Trim audio
ffmpeg -i input.mp3 -ss 00:00:30 -t 30 output.mp3

# Adjust volume
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3

# Convert to Whisper-friendly format
ffmpeg -i voice.ogg -ar 16000 -ac 1 -c:a pcm_s16le voice.wav

# Batch convert folder
for f in *.m4a; do ffmpeg -i "$f" "${f%.m4a}.wav"; done
```

### Whisper Setup Details

#### OpenAI Whisper API (Cloud)

**Pros:**
- Highest accuracy
- Multiple languages
- No local resources needed

**Cons:**
- Requires API key
- Data leaves your machine
- Per-minute costs

**Cost:** ~$0.006/minute of audio

**Best for:** Production use, high accuracy needs

#### Local Whisper Setup (Privacy-First)

**Step-by-step:**

```bash
# 1. Install dependencies
# Ubuntu/Debian
sudo apt-get install build-essential libsdl2-dev

# macOS
brew install sdl2

# 2. Clone and build
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make

# 3. Download model (start with base)
bash models/download-ggml-model.sh base

# 4. Test
echo "Testing 1 2 3" | ffmpeg -f lavfi -i "sine=frequency=1000:duration=3" -ar 16000 test.wav
./main -m models/ggml-base.bin -f test.wav

# 5. Add to PATH
sudo cp main /usr/local/bin/whisper-cli
```

**Performance tips:**
- Use `tiny` or `base` for real-time applications
- Use `medium` or `large` for archival transcription
- Enable GPU acceleration if available (`WHISPER_CUDA=1`)

### Voice Message Workflow

```javascript
// Complete voice-to-action workflow

// 1. Receive voice message (e.g., from WhatsApp)
const voiceFile = "voice_message.ogg";

// 2. Convert to format Whisper accepts
await exec({
  command: `ffmpeg -i ${voiceFile} -ar 16000 -ac 1 -c:a pcm_s16le voice.wav`
});

// 3. Transcribe (using local whisper)
const transcription = await exec({
  command: "whisper-cli -m models/ggml-base.bin -f voice.wav --output-txt"
});

// 4. Process transcription
const userIntent = parseIntent(transcription);

// 5. Take action
await handleUserRequest(userIntent);
```

### Voice Wake (macOS/iOS)

For hands-free activation:

```json5
{
  nodes: {
    voicewake: {
      enabled: true,
      phrase: "Hey Assistant",
      sensitivity: "medium",  // low | medium | high
    },
  },
}
```

**Supported phrases:**
- "Hey Assistant"
- Custom phrases (3+ syllables recommended)

**Platforms:**
- macOS: Full support
- iOS: Full support
- Android: Wake word support

---

## Local Image Generation with ComfyUI

### Overview

**ComfyUI** is a powerful node-based UI for Stable Diffusion that runs entirely locally. OpenClaw can control ComfyUI for:
- Text-to-image generation
- Image-to-image editing
- Batch processing
- Custom workflows

### Installation

#### Method 1: Direct Installation

```bash
# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt

# Download models (place in models/checkpoints/)
# - SDXL Base
# - SDXL Refiner
# - Custom LoRAs
```

#### Method 2: Docker (Recommended)

```bash
# GPU-enabled ComfyUI
docker run -d \
  --name comfyui \
  --gpus all \
  -p 8188:8188 \
  -v ~/ComfyUI/models:/app/models \
  -v ~/ComfyUI/output:/app/output \
  yanwk/comfyui-boot:latest

# CPU-only (slower but no GPU needed)
docker run -d \
  --name comfyui \
  -p 8188:8188 \
  -v ~/ComfyUI/models:/app/models \
  -v ~/ComfyUI/output:/app/output \
  -e CLI_ARGS="--cpu" \
  yanwk/comfyui-boot:latest
```

### ComfyUI Integration Steps

#### Step 1: Download Models

```bash
# Create directories
mkdir -p ~/ComfyUI/models/checkpoints
mkdir -p ~/ComfyUI/models/loras
mkdir -p ~/ComfyUI/output

# Download SDXL Base (6.9GB)
curl -L -o ~/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors \
  "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"

# Download SDXL Refiner (6.1GB)
curl -L -o ~/ComfyUI/models/checkpoints/sd_xl_refiner_1.0.safetensors \
  "https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors"
```

#### Step 2: Create OpenClaw Skill

```markdown
---
name: comfyui
description: Generate images using local ComfyUI
gated:
  { "openclaw": { "requires": { "config": ["comfyui.enabled"] } } }
---

# ComfyUI Image Generation

Generate images using local ComfyUI instance.

## Prerequisites

ComfyUI running at http://localhost:8188

## API Endpoints

- GET /object_info - List available nodes
- POST /prompt - Queue a prompt
- GET /history - Get generation history
- GET /view - View generated images

## Example Workflows

### Basic Text-to-Image

```json
{
  "prompt": {
    "3": {
      "inputs": {
        "text": "beautiful landscape, mountains, sunset",
        "clip": ["4", 1]
      },
      "class_type": "CLIPTextEncode"
    },
    "4": {
      "inputs": {
        "ckpt_name": "sd_xl_base_1.0.safetensors"
      },
      "class_type": "CheckpointLoaderSimple"
    }
  }
}
```

### Using the Tool

```javascript
// Queue a prompt
fetch('http://localhost:8188/prompt', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: workflow })
});
```
```

#### Step 3: Configuration

```json5
{
  comfyui: {
    enabled: true,
    baseUrl: "http://localhost:8188",
    defaultModel: "sd_xl_base_1.0.safetensors",
    outputDir: "~/.openclaw/workspace/generated-images",
  },
}
```

### Hardware Requirements

| GPU | VRAM | Performance |
|-----|------|-------------|
| RTX 3060 | 12GB | ~8-12 sec/image (SDXL) |
| RTX 4070 | 12GB | ~4-6 sec/image (SDXL) |
| RTX 4090 | 24GB | ~2-3 sec/image (SDXL) |
| Apple M3 Max | 36GB | ~10-15 sec/image (SDXL) |
| CPU only | N/A | ~5-10 min/image |

### Cost Comparison

| Method | Cost per 1000 images | Notes |
|--------|---------------------|-------|
| DALL-E 3 | $20-40 | API-based |
| Midjourney | $10-30 | Subscription |
| **Local ComfyUI** | **$0** | One-time hardware cost |

### Common ComfyUI Workflows

#### 1. Basic Text-to-Image
```json
{
  "prompt": {
    "1": {
      "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
      "class_type": "EmptyLatentImage"
    },
    "2": {
      "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"},
      "class_type": "CheckpointLoaderSimple"
    },
    "3": {
      "inputs": {"text": "professional headshot, business attire, neutral background", "clip": ["2", 1]},
      "class_type": "CLIPTextEncode"
    },
    "4": {
      "inputs": {"samples": ["1", 0], "vae": ["2", 2]},
      "class_type": "VAEDecode"
    }
  }
}
```

#### 2. Image-to-Image
```json
{
  "prompt": {
    "1": {
      "inputs": {"image": "input.png", "upload": "image"},
      "class_type": "LoadImage"
    },
    "2": {
      "inputs": {"pixels": ["1", 0], "vae": ["3", 2]},
      "class_type": "VAEEncode"
    }
  }
}
```

---

## Agentic Coding with Claude Code/Codex/OpenCode

### Overview

OpenClaw can delegate coding tasks to specialized AI coding agents:

| Agent | Provider | Best For | Cost | PTY Required |
|-------|----------|----------|------|--------------|
| **Claude Code** | Anthropic | Complex refactoring, code review | $$$ | No |
| **Codex** | OpenAI | New features, bug fixes | $$ | Yes |
| **OpenCode** | Open Source | Free alternative | Free | Yes |
| **KiloCode** | Open Source | Multiple models | Free/Paid | Yes |
| **Pi** | Multiple | Lightweight tasks | Free | Yes |

### Setting Up Claude Code

#### Installation

```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or via Homebrew (macOS)
brew install claude-code
```

#### Configuration

```bash
# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Or configure in OpenClaw
openclaw config set agents.defaults.models."anthropic/claude-opus-4-6".apiKey "$ANTHROPIC_API_KEY"
```

#### Usage Patterns

```bash
# Quick one-shot task (no PTY needed)
claude --print --permission-mode bypassPermissions "Refactor this function"

# Interactive session (PTY required)
claude
```

From OpenClaw:
```javascript
// Delegate to Claude Code
exec({
  command: 'claude --print --permission-mode bypassPermissions "Add error handling to auth.js"',
  workdir: "~/my-project",
  pty: false  // Claude Code uses --print, no PTY needed
});
```

**Critical:** Claude Code requires `--print --permission-mode bypassPermissions`. Do NOT use `--dangerously-skip-permissions` with PTY — it can exit after the confirmation dialog.

### Setting Up Codex

#### Installation

```bash
# Install
npm install -g @openai/codex

# Configure
export OPENAI_API_KEY=sk-...
```

#### Usage

```bash
# Full auto mode
codex exec --full-auto "Add user authentication"

# With yolo mode (less confirmation)
codex exec --yolo "Fix the bug in utils.py"
```

From OpenClaw:
```javascript
exec({
  command: 'codex exec --full-auto "Implement JWT authentication"',
  workdir: "~/my-project",
  pty: true  // Codex requires PTY
});
```

**Note:** Codex requires a git repository. For scratch work:
```bash
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "Your prompt"
```

### Setting Up OpenCode

#### Installation

```bash
# Install
npm install -g opencode

# Or use npx
npx opencode run "task"
```

#### Usage

```bash
# Run task
opencode run "Create a React component for user profiles"
```

From OpenClaw:
```javascript
exec({
  command: 'opencode run "Create API endpoint for user data"',
  workdir: "~/my-project",
  pty: true  // OpenCode requires PTY
});
```

### Setting Up KiloCode

#### Installation

```bash
npm install -g kilocode
```

#### Configuration

```bash
# Set API key for chosen provider
export OPENROUTER_API_KEY=sk-or-...
# or
export ANTHROPIC_API_KEY=sk-ant-...
```

#### Usage

```bash
# Run with default model
kilo run "Implement pagination"

# Run with specific model
kilo run --model claude-sonnet-4 "Complex refactoring"
```

### Agentic Coding Examples

#### Example 1: Quick Feature Implementation

```javascript
// User: "Add a login form to my React app"

// Step 1: Navigate to project
const projectDir = "~/projects/my-app";

// Step 2: Spawn Claude Code (best for complex UI)
await exec({
  command: 'claude --print --permission-mode bypassPermissions "Create a login form component with email/password fields, validation, and error handling. Use modern React hooks."',
  workdir: projectDir
});

// Step 3: Verify changes
const newFiles = await exec({
  command: "git status --short",
  workdir: projectDir
});

// Step 4: Report to user
console.log("Created login form components:");
console.log(newFiles);
```

#### Example 2: Background Refactoring

```javascript
// User: "Refactor the auth module in the background"

// Step 1: Start background session
const result = await exec({
  command: 'codex exec --full-auto "Refactor auth module to use JWT instead of sessions"',
  workdir: "~/projects/my-app",
  pty: true,
  background: true
});

// Returns: { sessionId: "xxx" }

// Step 2: Monitor progress
setInterval(async () => {
  const status = await process({ action: "poll", sessionId: result.sessionId });
  if (!status.running) {
    const output = await process({ action: "log", sessionId: result.sessionId });
    await notifyUser("Refactoring complete!", output);
  }
}, 60000);
```

#### Example 3: Parallel PR Reviews

```javascript
// Review multiple PRs in parallel

// Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*';

// Deploy the army - one Codex per PR
const prs = [86, 87, 88];
const sessions = [];

for (const pr of prs) {
  // Create worktree for isolation
  await exec({
    command: `git worktree add /tmp/pr-${pr}-review origin/pr/${pr}`
  });
  
  // Launch reviewer
  const session = await exec({
    command: `codex exec "Review PR #${pr}. Check for bugs, style issues, and security concerns."`,
    workdir: `/tmp/pr-${pr}-review`,
    pty: true,
    background: true
  });
  
  sessions.push({ pr, sessionId: session.sessionId });
}

// Monitor all
for (const { pr, sessionId } of sessions) {
  const log = await process({ action: "log", sessionId });
  await postPRReview(pr, log);
  
  // Cleanup
  await exec({ command: `git worktree remove /tmp/pr-${pr}-review` });
}
```

#### Example 4: Auto-Notify on Completion

```javascript
// Long-running task with completion notification

const task = `
Build a complete REST API for a todo app with:
- CRUD endpoints
- JWT authentication
- SQLite database
- Input validation

When completely finished, run this command to notify me:
openclaw system event --text "Done: Built todos REST API with CRUD endpoints" --mode now
`;

await exec({
  command: `codex --yolo exec '${task}'`,
  workdir: "~/projects",
  pty: true,
  background: true
});
```

### When to Use Which Agent

| Task | Recommended Agent | Why |
|------|-------------------|-----|
| Large refactoring | Claude Code | Best context understanding |
| New feature | Codex | Fast implementation |
| Bug fix | Codex/Claude | Depends on complexity |
| Code review | Claude Code | Thorough analysis |
| Documentation | Any | All handle this well |
| Learning/exploration | OpenCode | Free to experiment |
| Budget-conscious | OpenCode/KiloCode | Free options |

### Safety and Approvals

```json5
// Configure approval levels
{
  tools: {
    exec: {
      security: "allowlist",  // Only allowlisted commands
      ask: "on-miss",         // Ask if not in allowlist
      
      // Safe binaries for coding agents
      safeBins: ["git", "npm", "node", "python3"],
    },
  },
}
```

### Create a Coding Agent Skill

```markdown
---
name: coding-agent
description: Delegate coding tasks to specialized AI agents
---

# Coding Agent Delegation

Delegate coding tasks to Claude Code, Codex, or OpenCode.

## Choosing an Agent

**Claude Code (claude)**
- Best for: Complex refactoring, architecture decisions
- Cost: Higher
- Usage: `claude --print --permission-mode bypassPermissions "task"`

**Codex (codex)**
- Best for: Quick features, bug fixes
- Cost: Medium
- Usage: `codex exec --full-auto "task"`

**OpenCode (opencode)**
- Best for: Learning, experimentation
- Cost: Free
- Usage: `opencode run "task"`

**KiloCode (kilo)**
- Best for: Flexibility, multiple models
- Cost: Free/Paid
- Usage: `kilo run "task"`

## Important Flags

- `--full-auto` / `--yolo`: Less confirmation prompts
- `--print`: Non-interactive output
- `--permission-mode bypassPermissions`: Skip per-action approval

## PTY Requirements

- Codex/Pi/OpenCode/KiloCode: **Require PTY**
- Claude Code: **No PTY needed** with `--print`

## Never Run In

- `~/.openclaw/` directory
- `~/clawd/` directory
- System directories

## Best Practices

1. Use `workdir:` to set project directory
2. Start with descriptive, specific prompts
3. Review changes before committing
4. Use version control (git) for safety
```

---

## Self-Modifying Agents

### Overview

One of OpenClaw's most powerful features is the ability for agents to **modify their own configuration** — updating skills, configuration, and even their own "personality files" based on experience.

### Safe Self-Modification Patterns

#### 1. Memory Updates (Safe)

```javascript
// Agent updates its own memory based on new information
edit({
  file_path: "memory/2026-03-19.md",
  old_string: "",
  new_string: "- User prefers dark mode in all applications\n"
});
```

#### 2. Skill Improvements (Cautious)

```javascript
// Agent improves its own skills
edit({
  file_path: "skills/my-skill/SKILL.md",
  old_string: "## Common Error: X",
  new_string: "## Common Error: X and Y"
});
```

#### 3. Configuration Updates (With Approval)

```javascript
// Suggest config changes
const suggestion = {
  path: "agents.defaults.heartbeat.every",
  value: "1h",
  reason: "Current 30m interval is too frequent"
};

// Wait for user approval before applying
```

### Self-Modification Guardrails

```markdown
---
name: self-modify
description: Guidelines for self-modification
---

# Self-Modification Rules

## Allowed (No Approval Needed)

- Update `memory/YYYY-MM-DD.md` files
- Append to `MEMORY.md` (if not in shared context)
- Update `TOOLS.md` with new discoveries
- Create new skill files

## Requires User Approval

- Modify `SOUL.md` (personality changes)
- Modify `IDENTITY.md` (identity changes)
- Change `~/.openclaw/openclaw.json`
- Delete any existing files
- Modify installed skills

## Never Allowed

- Access/modify `~/.openclaw/.env` (secrets)
- Modify Gateway configuration files directly
- Change channel authentication tokens
- Delete `BOOTSTRAP.md` until instructed
```

### Learning Loop Implementation

```javascript
// At end of session, agent reflects and updates
async function learningLoop() {
  // 1. Review session
  const sessionReview = await reviewSession();
  
  // 2. Identify lessons learned
  const lessons = extractLessons(sessionReview);
  
  // 3. Update relevant files
  for (const lesson of lessons) {
    if (lesson.type === "preference") {
      await updateUserMd(lesson);
    } else if (lesson.type === "tool") {
      await updateToolsMd(lesson);
    } else if (lesson.type === "behavior") {
      await requestSoulUpdate(lesson);  // Needs approval
    }
  }
}
```

---

## Integration Patterns

### Pattern 1: Voice → Transcription → Action

```
Voice Message → FFmpeg → Whisper → OpenClaw → Action
     ↑                                              ↓
     └────────────── Response ← TTS ←───────────────┘
```

**Use Case:** Hands-free assistant while driving

**Implementation:**
```javascript
async function voiceWorkflow(audioFile) {
  // Convert and transcribe
  await exec({ command: `ffmpeg -i ${audioFile} -ar 16000 voice.wav` });
  const text = await exec({ command: "whisper-cli -f voice.wav --output-txt" });
  
  // Process
  const response = await processRequest(text);
  
  // Convert to speech (if TTS available)
  await exec({ command: `say "${response}"` });  // macOS
}
```

### Pattern 2: Screenshot → Analysis → Response

```
Screenshot → OCR/Analysis → OpenClaw → Response
```

**Use Case:** "What's wrong with this error message?"

**Implementation:**
```javascript
// User sends screenshot
// OpenClaw receives image, uses vision model
const analysis = await analyzeImage(image);
const solution = await findSolution(analysis);
```

### Pattern 3: Code Change → Review → Commit

```
File Change → Coding Agent → Review → OpenClaw → Git Commit
```

**Use Case:** Automated code review pipeline

**Implementation:**
```javascript
// Watch for file changes
// Trigger coding agent review
// Post review as comment
// Commit if approved
```

### Pattern 4: Multi-Agent Orchestration

```
Main Agent
    ├── Sub-agent: Research
    ├── Sub-agent: Coding
    ├── Sub-agent: Testing
    └── Sub-agent: Documentation
```

**Use Case:** Complex project implementation

**Implementation:**
```javascript
// Main agent coordinates specialized sub-agents
const research = await spawnAgent("research", "Find best practices for X");
const code = await spawnAgent("coding", "Implement X based on research");
const test = await spawnAgent("testing", "Write tests for X");
const docs = await spawnAgent("docs", "Document X");
```

### Complete Integration Example

```javascript
// Voice-triggered coding task with full pipeline
async function voiceCodingWorkflow(audioFile) {
  // 1. Transcribe voice
  await exec({ command: `ffmpeg -i ${audioFile} voice.wav` });
  const transcription = await exec({
    command: `whisper-cli -f voice.wav --output-txt`
  });
  
  // 2. Parse intent
  const intent = await parseIntent(transcription);
  
  // 3. Delegate to coding agent
  if (intent.type === "coding") {
    const result = await exec({
      command: `claude --print "${intent.task}"`,
      workdir: intent.project,
      background: true
    });
    
    // 4. Generate preview image (if UI work)
    if (intent.includes("UI") || intent.includes("component")) {
      await generatePreview(intent.project);
    }
    
    // 5. Monitor and report
    await monitorAndReport(result.sessionId);
  }
}
```

---

## Hardware Recommendations

### For File System + Basic Operations
- **Minimum:** Any modern computer
- **Recommended:** SSD for faster file operations
- **Optimal:** NVMe SSD, 16GB RAM

### For Voice (Local Whisper)
- **Minimum:** 8GB RAM
- **Recommended:** 16GB RAM, fast CPU
- **Optimal:** GPU with 8GB+ VRAM

### For Image Generation (ComfyUI)
- **Minimum:** GPU with 8GB VRAM
- **Recommended:** GPU with 12GB+ VRAM (RTX 4070+)
- **Optimal:** GPU with 24GB VRAM (RTX 4090)

### For Coding Agents
- **Minimum:** 8GB RAM
- **Recommended:** 16GB RAM
- **Optimal:** 32GB RAM for large codebases

---

## Troubleshooting

### File Permission Issues
```bash
# Fix ownership
sudo chown -R $(whoami) ~/.openclaw/workspace

# Fix permissions
chmod 755 ~/.openclaw/workspace
```

### Whisper Not Found
```bash
# Add to PATH
export PATH="$HOME/whisper.cpp:$PATH"

# Or create symlink
sudo ln -s ~/whisper.cpp/main /usr/local/bin/whisper-cli
```

### ComfyUI Connection Refused
```bash
# Check if running
docker ps | grep comfyui

# Check logs
docker logs comfyui

# Restart
docker restart comfyui
```

### Coding Agent Hangs
```bash
# Check process list
process action:list

# Kill hung process
process action:kill sessionId:xxx

# Check for git repo (Codex requires it)
git status
```

---

**Estimated Time:** 2-4 hours for full setup
**Cost:** Free (open source tools) to $20-100/month (API costs)
**Difficulty:** Intermediate to Advanced