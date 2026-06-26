# Installation Guide - Multi-Platform

English | [简体中文](INSTALLATION_CN.md)

Detailed installation guide for Claude Code, Cursor, Cline, and OpenClaw.

---

## 🎯 Platform Compatibility

| Platform | Status | Primary Install Method |
|----------|--------|------------------------|
| **Claude Code** | ✅ Fully Supported | `curl` + SKILL.md |
| **Cursor** | ✅ Supported | `npm install -g knowfun-skills` |
| **Cline** | ✅ Supported | `npm install -g knowfun-skills` |
| **OpenClaw** | ✅ Supported | `npx clawhub install knowfun-skills` |

---

## 📦 Claude Code Installation

Claude Code uses a native skill system. You only need to place `SKILL.md` in your skills directory.

### Method 1: curl (Recommended — no cloning needed)

```bash
mkdir -p ~/.claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o ~/.claude/skills/knowfun/SKILL.md
```

This installs the skill globally for all your Claude Code projects.

### Method 2: Project-Specific

```bash
mkdir -p .claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o .claude/skills/knowfun/SKILL.md
```

### Method 3: npm (if already installed)

```bash
npm install -g knowfun-skills
mkdir -p ~/.claude/skills/knowfun
cp "$(npm root -g)/knowfun-skills/SKILL.md" ~/.claude/skills/knowfun/SKILL.md
```

### Verification

In a Claude Code session:
```
/knowfun credits
```

Expected: Shows your credit balance.

### Usage in Claude Code

```bash
/knowfun create course "Introduction to Python"
/knowfun create poster "Climate Change Facts"
/knowfun status <taskId>
/knowfun detail <taskId>
/knowfun list
/knowfun credits
```

---

## 📦 Cursor Installation

### Step 1: Install CLI Tool

```bash
# Recommended — install from npm
npm install -g knowfun-skills
```

<details>
<summary>Alternative: symlink from local clone</summary>

```bash
git clone https://github.com/MindStarAI/KnowFun-Skills.git
sudo ln -s $(pwd)/KnowFun-Skills/scripts/knowfun-cli.sh /usr/local/bin/knowfun
chmod +x KnowFun-Skills/scripts/knowfun-cli.sh
```
</details>

### Step 2: Configure API Key

```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"

# Persist permanently
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Add Cursor Rules (Optional)

```bash
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/integrations/cursor/.cursorrules \
  -o .cursorrules
```

### Verification

```bash
knowfun credits
```

### Usage in Cursor

**From terminal:**
```bash
knowfun create course "Your topic"
knowfun status <taskId>
```

**Via natural language:**
```
Use knowfun to create a course about Python basics
```

Cursor will run the CLI command on your behalf.

---

## 📦 Cline Installation

### Step 1: Install CLI Tool

```bash
npm install -g knowfun-skills
```

### Step 2: Configure API Key

```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"

echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Step 3: Add Cline Configuration (Optional)

```bash
mkdir -p .cline
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/integrations/cline/knowfun.json \
  -o .cline/knowfun.json
```

### Verification

```bash
knowfun credits
```

### Usage in Cline

```
Create a Knowfun course about "Machine Learning basics"
```

Cline will execute the CLI commands automatically.

---

## 📦 OpenClaw Installation

### Step 1: Install Skill

```bash
npx clawhub install knowfun-skills
```

This installs the skill to your OpenClaw workspace at `~/.openclaw/workspace/skills/knowfun-skills/`.

### Step 2: Install CLI Tool

OpenClaw uses the `knowfun` binary from the npm package:

```bash
npm install -g knowfun-skills
```

### Step 3: Configure API Key

```bash
export KNOWFUN_API_KEY="kf_your_api_key_here"

echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### Verification

```bash
openclaw skills list | grep knowfun
# Should show: ✓ ready  📚 knowfun
```

### Usage in OpenClaw

**Via natural language (chat apps):**
```
Create a Knowfun course about Python
```

**Direct CLI:**
```bash
knowfun create course "Introduction to Python"
```

---

## 🔧 Common Setup (All Platforms)

### 1. Get Your API Key

1. Visit https://www.knowfun.io/api-platform
2. Click "Create API Key"
3. Name it (e.g., "Development Key")
4. Copy the key (starts with `kf_`)

### 2. Set Environment Variable

```bash
# Temporary (current session)
export KNOWFUN_API_KEY="kf_your_api_key_here"

# Permanent — zsh (macOS default)
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc && source ~/.zshrc

# Permanent — bash
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.bashrc && source ~/.bashrc
```

### 3. Test Installation

```bash
knowfun credits
```

---

## 📊 Feature Comparison

| Feature | Claude Code | Cursor | Cline | OpenClaw |
|---------|:-----------:|:------:|:-----:|:--------:|
| Slash commands (`/knowfun`) | ✅ | ❌ | ❌ | ❌ |
| Auto skill invocation | ✅ | ❌ | ❌ | ✅ |
| CLI tool (`knowfun`) | ✅ | ✅ | ✅ | ✅ |
| Natural language requests | ✅ | ✅ | ✅ | ✅ |
| Remote access (Telegram etc.) | ❌ | ❌ | ❌ | ✅ |
| npm install | ✅ | ✅ | ✅ | ✅ |

---

## 🆘 Troubleshooting

### "Command not found: knowfun"

```bash
npm install -g knowfun-skills
which knowfun  # verify it's in PATH
```

### "API Key not found"

```bash
echo $KNOWFUN_API_KEY   # check if set
export KNOWFUN_API_KEY="kf_your_key"
```

### "Permission denied" on scripts

```bash
chmod +x $(npm root -g)/knowfun-skills/scripts/knowfun-cli.sh
```

### Claude Code skill not recognized

Ensure SKILL.md is in the correct location:
```bash
ls ~/.claude/skills/knowfun/SKILL.md
```

If missing, reinstall:
```bash
mkdir -p ~/.claude/skills/knowfun
curl -fsSL https://raw.githubusercontent.com/MindStarAI/KnowFun-Skills/master/SKILL.md \
  -o ~/.claude/skills/knowfun/SKILL.md
```

---

## 📚 Next Steps

After installation:

1. Follow the [Quickstart Guide](QUICKSTART.md)
2. Browse [examples.md](examples.md) for usage patterns
3. Read [api-reference.md](api-reference.md) for advanced configuration

---
