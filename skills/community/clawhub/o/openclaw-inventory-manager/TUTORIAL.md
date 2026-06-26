# 5-Minute Quick Start Tutorial: "Where are you from" 📦🦀

Welcome! This tutorial will guide you from installation to your first cloud-synced skill inventory in just 5 minutes.

## Step 1: The Grand Welcome (`bootstrap`)

Instead of manually editing config files, let's use the guided setup. Open your terminal in your preferred project folder and run:

```bash
node .agents/skills/openclaw-inventory-manager/inventory.js bootstrap
```

**What happens?**
- You'll see a beautiful ASCII splash screen.
- A default configuration is created in `~/.openclaw/inventory.json`.
- A local Git repository is initialized in your current folder.
- A first-ever scan is performed to find your skills.

## Step 2: Check Your First Report

After the bootstrap finishes, look for a new file named **`SKILLS_MANIFEST.md`** in your folder. Open it to see:
- A list of all your installed skills.
- Their versions and origins (GitHub, NPM, etc.).
- Their privacy status (Locked/Unlocked).

## Step 3: Link to GitHub

Now, let's make this inventory persistent. If you haven't already, create a new **private** repository on GitHub naming it something like `my-skills-inventory`. Then run:

```bash
node .agents/skills/openclaw-inventory-manager/inventory.js init https://github.com/yourusername/my-skills-inventory.git
```

## Step 4: Your First Cloud Sync

Let's push your data to the moon! 🚀

```bash
node .agents/skills/openclaw-inventory-manager/inventory.js sync --push
```

**Note**: You'll see a confirmation message before the push happens. This ensures you've reviewed the manifest and no sensitive data (like unmasked keys) is being uploaded.

## Step 5: Track Changes Over Time

As you install or remove skills, run `status` to see what's new or changed since your last commit:

```bash
node .agents/skills/openclaw-inventory-manager/inventory.js status
```

This compares your current `SKILLS_MANIFEST.json` against the last Git commit using `git diff`. If the file has changed, you'll see a warning prompting you to run `sync`.

> [!NOTE]
> **Ghost Skill Detection** (removed skills that are still in the manifest) is on the roadmap for a future release. For now, running `sync` after removing a skill will update the manifest to reflect only currently-found skills.

---

### Pro Tip: Natural Language Control
Since this is an AI agent skill, you don't always need to type commands. Just ask your agent:
- *"Analyze my skills"*
- *"Where did my skills come from?"*
- *"Sync my inventory to GitHub"*

The agent will know exactly which scripts to run!
