---
name: Where are you from
description: An enterprise-grade asset manager that tracks, manages, and automatically syncs OpenClaw skills capabilities and sources to your GitHub.
version: 1.0.0
category: management
tags: [inventory, skills, git, openclaw]
---

# Where are you from (OpenClaw Skill Inventory Manager)

This skill comprehensively audits OpenClaw skills installed from various sources (ClawHub, GitHub, npm, local, etc.). It generates human- and machine-readable manifests (`SKILLS_MANIFEST.json` and `SKILLS_MANIFEST.md`), and securely backs them up to your personal GitHub repository.

> [!WARNING]
> **Prerequisite: Node.js Required**
> This skill manager relies on JavaScript (`inventory.js`) to perform file scanning and Git integration. 
> You **must** have **Node.js (v14 or higher recommended)** installed on your system for it to function correctly.

## Core Features

- **Targeted Scanning**: Optimizes performance by only scanning predefined paths configured in `~/.openclaw/inventory.json`. 
- **Source Detection**: Accurately tracks the origin and installation method of a skill by analyzing `.git`, `package.json`, and `clawhub.json`.
- **Security Scrubbing**: Automatically detects and masks over 10 API Key patterns (e.g., `sk-`, `ghp_`, `hf_`) to prevent sensitive data leaks in the manifest.
- **Privacy Layer**: If a `SKILL.private.md` is found, the skill is classified as a "Private Skill (Content Masked)" in the manifest, and its details are fully hidden.
- **Git Syncing**: Provides a single `sync --push` command to handle everything from detecting inventory changes to committing and pushing to GitHub.

## Detailed Command Guide

### 0. Guided Setup (`inventory bootstrap`) [RECOMMENDED]
The easiest way for first-time users to set up everything (Config + Git + Initial Scan).
```powershell
node .agents/skills/openclaw-inventory-manager/inventory.js bootstrap
```

### 1. Initialization (`inventory init`)
Initializes inventory configurations and sets up the root Git repository for tracking skills.
```powershell
# Initialize Git tracking in the current directory and generate config
node .agents/skills/openclaw-inventory-manager/inventory.js init 

# Initialize and link directly to a remote GitHub repository
node .agents/skills/openclaw-inventory-manager/inventory.js init https://github.com/yourname/my-skills-inventory.git
```

### 2. Status Check (`inventory status`)
Scans for modifications since the last inventory sync.
```powershell
node .agents/skills/openclaw-inventory-manager/inventory.js status
```

### 3. Sync & Commit (`inventory sync`)
Updates the manifest file and commits changes to the local Git repository. Add `--push` to upload to the remote.
```powershell
# Only update manifest and perform local commit
node .agents/skills/openclaw-inventory-manager/inventory.js sync

# Upload changes to the remote GitHub repository
node .agents/skills/openclaw-inventory-manager/inventory.js sync --push
```

### 4. Search Skill List (`inventory list / search`)
Outputs a quick terminal table of all installed skills.
```powershell
node .agents/skills/openclaw-inventory-manager/inventory.js list
```

## Configuration Structure

The configuration is stored in:
`~/.openclaw/inventory.json` (Local user home directory)

```json
{
  "searchRoots": ["~/.openclaw/skills", "./skills"], // Paths to scan
  "maxDepth": 5,                                     // Recursion limit
  "excludedDirs": ["node_modules", ".git", "dist"],  // Folders to ignore
  "maskPatterns": ["sk-", "ghp_", "hf_", "AIza"],    // Secret masking patterns
  "autoPush": false,                                 // Enable automatic push
  "manifestPath": "~/.openclaw/SKILLS_MANIFEST.json"           // Output location
}
```

## Instruction for Agent (Natural Language Triggers)

When the user sends a message matching one of the following trigger phrases, run the corresponding workflow. Matching should be **intent-based** — exact wording is not required.

---

### 🔍 Intent: Audit / Inspect Skills

**Trigger phrases (English)**
- "Where are you from?"
- "Where did my skills come from?"
- "Show me my skill inventory"
- "List all my installed skills"
- "What skills do I have?"
- "Audit my skills"
- "Analyze my agent environment"
- "Check my skill history"
- "Show my skill manifest"
- "What's installed?"

**Trigger phrases (Korean)**
- "내 스킬 내역 확인해줘"
- "스킬 목록 보여줘"
- "어떤 스킬 설치되어 있어?"
- "스킬 히스토리 알려줘"

**Workflow**:
1. Check if `~/.openclaw/inventory.json` exists.
2. If **NOT** exists → Inform the user that the skill has not been initialized yet and suggest:
   ```
   node inventory.js bootstrap
   ```
3. If **EXISTS** → Run `inventory status` and summarize the output (number of skills found, any changes since last sync).
4. If changes are detected, offer to run `inventory sync`.

---

### ☁️ Intent: Sync / Commit / Push to GitHub

**Trigger phrases (English)**
- "Sync my skills to GitHub"
- "Update my skill manifest"
- "Commit my inventory"
- "Push my skill list"
- "Save skill inventory to GitHub"
- "Back up my skills"

**Trigger phrases (Korean)**
- "스킬 동기화해줘"
- "깃허브에 올려줘"
- "인벤토리 업데이트해줘"
- "커밋해줘"

**Workflow**:
1. Run `inventory sync --push`.
2. Report the commit status (success, no changes, or error) to the user.
3. If push fails, suggest checking GitHub authentication (SSH or token).

---

### 🚀 Intent: First-Time Setup / Bootstrap

**Trigger phrases (English)**
- "Set up skill inventory"
- "Initialize skill tracking"
- "Get started with skill manager"
- "Configure the inventory"
- "I just installed this skill, what do I do?"

**Trigger phrases (Korean)**
- "스킬 매니저 설정해줘"
- "처음 시작하는 방법 알려줘"
- "초기화해줘"

**Workflow**:
1. Check if `~/.openclaw/inventory.json` already exists.
2. If NOT exists → Run `inventory bootstrap` and guide through each step.
3. If EXISTS → Inform that a config already exists, and ask if the user wants to re-initialize or just run `status`.

---

## Security Note (Reminder)
- Always verify your GitHub authentication before using `sync --push`.
- Use `.gitignore` to prevent sensitive credential files from being uploaded.
- Utilize `SKILL.private.md` for internal instructions that should never be public.
