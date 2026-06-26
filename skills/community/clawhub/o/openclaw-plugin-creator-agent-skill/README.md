# OpenClaw Plugin Creator Skill

An expert agent skill for building, testing, and publishing native OpenClaw plugins.

## 🚀 The Core Motive: Seamless Self-Extensibility

The primary goal of this skill is to grant **OpenClaw the capability to create plugins for itself.** 

By equipping your agent with this skill, you transform it into a self-evolving system. Instead of waiting for manual updates, the agent can:
- **Write its own tools:** Dynamically generate new tool definitions to handle specialized tasks.
- **Create new channels:** Connect itself to new platforms (Slack, Discord, Telegram) on the fly.
- **Integrate new providers:** Add support for the latest LLM providers or specialized APIs.

Essentially, OpenClaw can now build its own capabilities as easily as creating a custom skill, making its feature set truly seamless and limitless.

## 🛠️ How to Use This Skill

Once installed, this skill is triggered whenever you ask the agent to perform OpenClaw development tasks.

### Example Prompts:
- **"Create a new tool for searching my local database."**
- **"Build an OpenClaw provider for the XYZ API."**
- **"I want to add a Discord channel to my OpenClaw gateway."**
- **"Help me debug my custom plugin manifest."**

The agent will use its expert knowledge of the OpenClaw SDK, manifest schema, and runtime helpers to guide you through the entire development lifecycle—from scaffolding files to final testing.

## 📦 Publishing to ClawHub

ClawHub is the central marketplace for OpenClaw skills. Publishing is handled locally through the official `clawhub` command-line interface.

### 1. Prerequisites
- **GitHub Account:** Must be at least one week old.
- **`clawhub` CLI:** Install the official CLI tool:
  ```bash
  npm install -g @openclaw/clawhub-cli
  ```

### 2. Prepare Your Skill
Ensure your directory contains the following mandatory files:
- `SKILL.md` (with updated version and `metadata.clawdbot: true`)
- `CHANGELOG.md`
- `README.md`
- `scripts/` folder

### 3. Validate and Publish
Open your terminal in the skill directory and run:
```bash
clawhub skill publish .
```

### 4. Verification
The CLI will validate your structure and version. Once uploaded, wait a few minutes for the skill to appear in the registry. Users can then install it using:
```bash
npx clawhub install openclaw-plugin-creator-skill
```

---

*Built for the OpenClaw Ecosystem.*
