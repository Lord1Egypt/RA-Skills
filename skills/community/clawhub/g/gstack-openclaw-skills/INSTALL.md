# gstack-skills Installation Guide

Three ways to install gstack-skills: **Interactive (Recommended)**, **One-Click**, or **Manual**.

---

## 🎯 Method 1: Interactive Installation (Recommended)

**Easiest method** - Just tell OpenClaw/WorkBuddy to install it!

### Step 1: Ask OpenClaw/WorkBuddy to Install

Simply say:

```
Please install gstack-skills for me
```

Or:

```
Help me install gstack-skills from GitHub: AICreator-Wind/gstack-openclaw-skills
```

### Step 2: Follow the Instructions

OpenClaw/WorkBuddy will:

1. **Clone the repository**
   ```bash
   git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
   cd gstack-openclaw-skills
   ```

2. **Detect your platform**
   - OpenClaw: `~/.openclaw/skills/`
   - WorkBuddy: `~/.workbuddy/skills/`

3. **Copy skills to the right location**
   ```bash
   cp -r gstack-skills ~/.openclaw/skills/
   # or
   cp -r gstack-skills ~/.workbuddy/skills/
   ```

4. **Verify installation**
   ```bash
   ls ~/.openclaw/skills/gstack-skills/SKILL.md
   ```

5. **Tell you it's ready**
   ```
   ✅ gstack-skills installed successfully!
   
   Try: /gstack
   ```

### Step 3: Restart OpenClaw/WorkBuddy

Restart your OpenClaw/WorkBuddy to load the new skills.

### Step 4: Test It

Say to OpenClaw/WorkBuddy:

```
/gstack
```

You should see:

```
Available gstack commands:
• /office-hours - Product ideation and validation
• /review - Code review with automatic fixes
• /qa - Test and fix bugs
• /ship - Automated deployment
• ... and 11 more commands
```

✅ **Installation complete!**

---

## ⚡ Method 2: One-Click Installation

**Fastest method** - Run a single script.

### macOS/Linux

```bash
# Clone the repository
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills

# Run the installer
chmod +x install.sh
./install.sh
```

### Windows

```batch
# Clone the repository
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills

# Run the installer
install.bat
```

The installer will:
- ✅ Detect OpenClaw or WorkBuddy
- ✅ Copy skills to the correct location
- ✅ Verify installation
- ✅ Print usage instructions

---

## 🔧 Method 3: Manual Installation

**Most control** - Install manually step by step.

### Step 1: Clone the Repository

```bash
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
```

### Step 2: Choose Installation Location

**Option A: Install for OpenClaw**

```bash
cp -r gstack-skills ~/.openclaw/skills/
```

**Option B: Install for WorkBuddy**

```bash
cp -r gstack-skills ~/.workbuddy/skills/
```

**Option C: Install in a Specific Project**

```bash
cp -r gstack-skills/ /path/to/your/project/
```

### Step 3: Verify Installation

```bash
# Check if files exist
ls ~/.openclaw/skills/gstack-skills/SKILL.md
ls ~/.openclaw/skills/gstack-skills/scripts/command_router.py
```

### Step 4: Restart OpenClaw/WorkBuddy

Restart to load the new skills.

---

## 🚀 After Installation

### Test Installation

Ask OpenClaw/WorkBuddy:

```
/gstack
```

You should see the command overview.

### Try a Simple Command

```
/review
```

Or:

```
/qa
```

---

## 📖 How to Use gstack-skills

Once installed, using gstack-skills is simple!

### Basic Usage

Just say any gstack command to OpenClaw/WorkBuddy:

```
User: /review

AI: Reviewing your current branch...

Files changed: 12
Lines added: +342
Lines removed: -89

Critical Issues Found:
1. SQL Injection Risk in src/db/queries.py:42 ❌

Auto-fixes Applied:
✅ Fixed 2 unused imports

Status: ⚠️ DONE_WITH_CONCERNS
NEXT: Run /qa for testing
```

### Common Commands

#### Code Review

```
User: /review

AI: Automatically reviews your code and fixes issues
```

#### Testing

```
User: /qa

AI: Runs tests and fixes bugs automatically
```

#### Deployment

```
User: /ship

AI: Automates the entire deployment workflow
```

#### Product Ideation

```
User: /office-hours I have an idea for an AI code reviewer

AI: Validates your startup idea using YC's framework
```

#### Debugging

```
User: /investigate the login bug

AI: Systematically finds the root cause
```

### Complete Workflow Example

Here's how to develop and ship a feature:

```
User: /office-hours I want to add user comments

AI: Validates the idea...

User: /plan-eng-review comments architecture

AI: Reviews technical architecture...

[Developer writes code...]

User: /review

AI: Reviews code and fixes bugs...

User: /qa

AI: Runs tests and fixes remaining issues...

User: /ship

AI: Deploys to production automatically...
```

---

## 💡 Conversation Examples

### Example 1: First Time Using gstack-skills

```
User: I just installed gstack-skills. How do I use it?

AI: Welcome! Here's how to use gstack-skills:

Available Commands:
• /gstack - Show all commands
• /office-hours - Validate product ideas
• /review - Code review with automatic fixes
• /qa - Test and fix bugs
• /ship - Automated deployment
• ... and 11 more commands

Quick Start:
1. Try /review to review your current code
2. Try /qa to test your application
3. Try /gstack to see all commands

Let me know what you'd like to do!
```

### Example 2: Daily Code Review

```
User: /review

AI: Reviewing your current branch...

Files changed: 3 files
Lines added: +127, Lines removed: -45

Issues Found:
• 1 Critical: SQL injection in src/db/queries.py:42
• 2 Informational: Magic numbers, missing tests

Auto-fixes Applied:
✅ Fixed SQL injection
✅ Added constant definitions

Status: ⚠️ DONE_WITH_CONCERNS
NEXT: Run /qa for testing
```

### Example 3: Debugging

```
User: /investigate users are reporting 500 errors on login

AI: Investigating the login error...

Step 1: Analyzing logs...
Step 2: Checking error patterns...
Step 3: Testing hypotheses...

Root Cause: Connection pool exhaustion
Fix: Increase connection pool size from 50 to 100

Applying fix...
✅ Fix applied

Testing under load...
✅ All tests passed

Status: ✅ FIXED
NEXT: /ship the fix
```

### Example 4: Deploying

```
User: /ship the user authentication feature

AI: Preparing automated release...

1. Merging base branch... ✅
2. Running tests... ✅ (47/47 passed)
3. Checking coverage... ✅ (92%)
4. Updating version... ✅ (v2.1.0)
5. Creating PR... ✅ (#234)

Status: ✅ SHIPPED
PR: https://github.com/your/repo/pull/234
```

### Example 5: Startup Idea

```
User: /office-hours I want to build an AI code reviewer

AI: Let me validate your startup idea using YC's framework...

Question 1: What is the user's biggest pain point?
User: Code reviews take too long, 2-3 days on average.

AI: How much evidence do you have?
User: I was at Google for 5 years, interviewed 20+ devs.

[Completes all 6 questions]

AI: VALIDATION COMPLETE ✅
Problem: Strongly validated
Solution: Perfect fit
Market: 30M developers

Recommendation: PROCEED 🚀
Next: /plan-eng-review for architecture
```

---

## 🎓 Learning Resources

- **[USAGE.md](USAGE.md)**: Complete usage guide
- **[EXAMPLES.md](EXAMPLES.md)**: Real-world examples
- **[README.md](README.md)**: Project overview

---

## ❓ Troubleshooting

### Issue: Command Not Recognized

**Problem**: AI doesn't recognize gstack commands

**Solution**:
1. Check installation: `ls ~/.openclaw/skills/gstack-skills/SKILL.md`
2. Restart OpenClaw/WorkBuddy
3. Try `/gstack` first

### Issue: Skill Not Found

**Problem**: AI says skill not found

**Solution**:
```bash
# Reinstall
cd gstack-openclaw-skills
./install.sh
```

### Issue: Git Errors

**Problem**: `/ship` fails with git errors

**Solution**:
```bash
# Check git status
git status

# Clean working directory
git stash

# Resolve conflicts
git merge main
```

---

## 💬 Getting Help

Ask OpenClaw/WorkBuddy:

```
/gstack
```

This will show all available commands and usage instructions.

Or say:

```
Help me with gstack-skills
```

AI will provide detailed guidance.

---

## 🎉 Summary

1. **Install**: Interactive (ask AI), One-Click (run script), or Manual
2. **Restart**: Restart OpenClaw/WorkBuddy
3. **Test**: Say `/gstack` to verify
4. **Use**: Say any command like `/review`, `/qa`, `/ship`
5. **Learn**: Check USAGE.md and EXAMPLES.md

**Ready to code faster with gstack-skills! 🚀**

---

**Version**: 2.0.0  
**Updated**: 2026-03-21
