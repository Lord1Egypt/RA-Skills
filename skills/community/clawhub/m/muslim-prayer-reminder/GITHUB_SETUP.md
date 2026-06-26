# GitHub Repository Setup Instructions

The GitHub token doesn't have permission to create repos automatically. Here's how to set it up manually:

## Step 1: Create the Repository on GitHub

1. Go to https://github.com/new
2. Fill in the details:

**Repository name:**
```
openclaw-prayer-times
```

**Description:**
```
🕌 Automated Islamic prayer time reminders for OpenClaw. Never forget about the most important thing in your day - Salat is your first priority. Works in background with 20+ country methods.
```

**Visibility:** ✅ Public

**DO NOT** initialize with README, .gitignore, or license (we already have these)

3. Click "Create repository"

## Step 2: Push the Code

After creating the repo, run these commands:

```bash
cd /root/.openclaw/workspace/openclaw-prayer-times

# Add the remote
git remote add origin https://github.com/diepox/openclaw-prayer-times.git

# Push to GitHub
git push -u origin main
```

## Step 3: Verify

Visit https://github.com/diepox/openclaw-prayer-times and you should see:
- ✅ Complete README with Quranic verse
- ✅ All skill files and documentation
- ✅ MIT License
- ✅ Scripts and references

## Alternative: Create via GitHub Web UI

If you prefer to do it all from the web:

1. Go to https://github.com/diepox?tab=repositories
2. Click "New" (green button)
3. Follow Step 1 above
4. After creation, run the commands from Step 2

## What's Already Prepared

The repository is ready with:
- ✅ README.md with your requested description
- ✅ All skill files (SKILL.md, scripts, references)
- ✅ MIT License
- ✅ .gitignore for clean repo
- ✅ Initial commit with proper message
- ✅ Branch: main (not master)
- ✅ Git configured with lmodir@agentmail.to

Just create the repo on GitHub and push!
