# gstack-openclaw-skills

**Complete development workflow suite from Y Combinator CEO Garry Tan's gstack, adapted for OpenClaw/WorkBuddy.**

English | [简体中文](README.zh-CN.md)

<p align="center">
  <a href="https://github.com/AICreator-Wind/gstack-openclaw-skills/stargazers"><img src="https://img.shields.io/github/stars/AICreator-Wind/gstack-openclaw-skills" alt="Stars"></a>
  <a href="https://github.com/AICreator-Wind/gstack-openclaw-skills/network/members"><img src="https://img.shields.io/github/forks/AICreator-Wind/gstack-openclaw-skills" alt="Forks"></a>
  <a href="https://github.com/AICreator-Wind/gstack-openclaw-skills/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AICreator-Wind/gstack-openclaw-skills" alt="License"></a>
  <img src="https://img.shields.io/badge/Platform-OpenClaw%20%7C%20WorkBuddy-blue" alt="OpenClaw | WorkBuddy">
  <img src="https://img.shields.io/badge/Version-2.0.0-green" alt="Version 2.0.0">
</p>

## Table of Contents

- [What is gstack-skills?](#what-is-gstack-skills)
- [What's New in v2.0](#whats-new-in-v20)
- [Quick Start](#quick-start)
- [Available Commands](#available-commands)
- [Complete Workflow Example](#complete-workflow-example)
- [Installation](#installation)
- [Philosophy](#philosophy)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## What is gstack-skills?

gstack-skills is the **OpenClaw/WorkBuddy adaptation** of [gstack](https://github.com/garrytan/gstack), the open-source development workflow created by Garry Tan, CEO of Y Combinator.

**Garry Tan used gstack to write 600,000+ lines of production code in 60 days (35% tests).**

This adaptation makes those powerful workflows available to any AI agent running on OpenClaw or WorkBuddy platforms.

### Key Features

- **15 Specialized Tools**: Complete suite covering product ideation to deployment
- **Automated Workflows**: AI executes workflows automatically based on natural language commands
- **One-Command Access**: Simply say `/ship`, `/review`, `/qa`, etc.
- **State Management**: Share context between workflow steps
- **OpenClaw Native**: Built specifically for OpenClaw/WorkBuddy skill system

## What's New in v2.0

**v2.0 is a complete rewrite** that transforms gstack from documentation into **fully executable skills**:

### ✅ New Capabilities

1. **Automated Execution**: Skills now execute automatically, not just provide guidance
2. **Command Routing**: Parse user input and route to appropriate skill
3. **State Management**: Share data and context between skills
4. **Workflow Orchestration**: Run complete workflows with single commands
5. **Native Integration**: Built for OpenClaw/WorkBuddy from the ground up

### 🔄 Changes from v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Execution | Manual | Automatic |
| Integration | Documentation only | Native skills |
| State | None | Full state management |
| Commands | 15 commands | 15 commands + routing |
| Workflows | Static | Dynamic & orchestrated |

## Quick Start

### 🎯 Method 1: Interactive Installation (Easiest)

Just tell OpenClaw/WorkBuddy to install it:

```
Please install gstack-skills for me
```

Or:

```
Help me install gstack-skills from GitHub: AICreator-Wind/gstack-openclaw-skills
```

OpenClaw/WorkBuddy will:
- Clone the repository
- Detect your platform
- Copy skills to the correct location
- Verify installation
- Tell you when it's ready!

**That's it!** Then restart OpenClaw/WorkBuddy and say `/gstack` to get started.

**For detailed instructions**, see [INSTALL.md](INSTALL.md)

---

### ⚡ Method 2: One-Click Installation

**Fastest method** - Run a single script:

#### macOS/Linux

```bash
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
./install.sh
```

#### Windows

```batch
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills
install.bat
```

---

### 🔧 Method 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/AICreator-Wind/gstack-openclaw-skills.git
cd gstack-openclaw-skills

# Copy to OpenClaw skills directory
cp -r gstack-skills ~/.openclaw/skills/

# Or for WorkBuddy
cp -r gstack-skills ~/.workbuddy/skills/
```

---

### Start Using

After installation, restart OpenClaw/WorkBuddy and simply use any gstack command:

```python
# Get help and see all commands
User: "/gstack"

# Validate an idea
User: "/office-hours I have an idea for an AI code reviewer"

# Review code
User: "/review my current branch"

# Deploy
User: "/ship the user authentication feature"
```

### 3. See Available Commands

```python
User: "/gstack"

# AI shows all available commands:
# /office-hours - Product ideation and validation
# /plan-ceo-review - CEO perspective planning
# /plan-eng-review - Engineering architecture review
# /review - Pre-merge code review
# /qa - Test application and fix bugs
# /ship - Automated release workflow
# ... (and 9 more)
```

## Available Commands

### Product Ideation Phase

| Command | Purpose |
|---------|---------|
| `/office-hours` | YC office hours for product idea validation |
| `/plan-ceo-review` | CEO perspective on feature planning |
| `/plan-eng-review` | Engineering architecture review |
| `/plan-design-review` | Design review |

### Development Phase

| Command | Purpose |
|---------|---------|
| `/review` | Pre-merge code review with automatic fixes |
| `/investigate` | Systematic root cause analysis |
| `/design-consultation` | Design system consultation |

### Testing & Release Phase

| Command | Purpose |
|---------|---------|
| `/qa` | Test application and fix bugs |
| `/qa-only` | Bug reporting only (no fixes) |
| `/ship` | Fully automated release workflow |

### Documentation & Review

| Command | Purpose |
|---------|---------|
| `/document-release` | Update project documentation |
| `/retro` | Team retrospective and weekly reports |

### Power Tools

| Command | Purpose |
|---------|---------|
| `/codex` | OpenAI Codex independent review (second opinion) |
| `/careful` | Dangerous operation warnings |
| `/freeze` | Lock file editing scope |
| `/guard` | Full safety mode (careful + freeze) |

## How to Use gstack-skills

Once installed, using gstack-skills is simple - just talk to OpenClaw/WorkBuddy!

### Getting Started

After installation, restart OpenClaw/WorkBuddy and say:

```
User: /gstack
```

You'll see all available commands.

### Example Conversations

#### Quick Code Review

```
User: /review

AI: Reviewing your current branch...

Files changed: 3
Lines added: +127, Lines removed: -45

Critical Issues Found:
❌ 1. SQL Injection Risk in src/db/queries.py:42

Auto-fixes Applied:
✅ Fixed SQL injection
✅ Added rate limiting

Status: ⚠️ DONE_WITH_CONCERNS
NEXT: Run /qa for testing
```

#### Testing

```
User: /qa

AI: Running systematic QA tests...

Test Results:
• Unit Tests: 42/42 passed ✅
• Integration Tests: 15/15 passed ✅

Health Score: 95/100

Status: ✅ READY TO SHIP
```

#### Deployment

```
User: /ship

AI: Preparing automated release...

1. Merging base branch... ✅
2. Running tests... ✅ (57/57 passed)
3. Updating version... ✅ (v2.2.0)
4. Creating PR... ✅ (#247)

Status: ✅ DEPLOYED
```

### Natural Language Works Too!

You don't need exact commands. Natural language works:

```
User: review my code

AI: Reviewing your current branch...
[Same as /review]
```

```
User: deploy to production

AI: Preparing automated release...
[Same as /ship]
```

### For Complete Guide

See [CONVERSATION_GUIDE.md](CONVERSATION_GUIDE.md) for detailed examples and tips.

---

## Complete Workflow Example

Here's how you'd use gstack-skills to develop and ship a new feature:

```python
# Step 1: Validate the idea
User: "/office-hours I want to add user profiles to my app"

AI: Let me validate your startup idea using YC's 6 questions:
1. What is the user's biggest pain point?
2. How does your solution solve it?
3. Why aren't existing solutions good enough?
4. Can you reach these users?
5. Will people pay?
6. How will users discover it?

[Guides through all questions]

# Step 2: CEO perspective review
User: "/plan-ceo-review user profiles"

AI: Analyzing from CEO perspective...
- Strategic alignment: ✅
- Market opportunity: ✅
- Resource requirements: Medium
- Risks: Identified 3 key risks

# Step 3: Engineering architecture review
User: "/plan-eng-review user profiles architecture"

AI: Reviewing technical architecture...
- Database design: PostgreSQL with JSONB
- API structure: RESTful with GraphQL fallback
- Security: JWT + OAuth2
- Scalability: Horizontal scaling ready

# Step 4: Implement the feature
[Developer writes code...]

# Step 5: Code review
User: "/review"

AI: Reviewing your current branch...

Files changed: 12
Lines added: +342
Lines removed: -89

Critical Issues Found:
1. SQL Injection Risk in src/db/queries.py:42 ❌
2. Missing Authentication in src/api/routes.py:87 ❌

Auto-fixes Applied:
1. ✅ Fixed 2 unused imports
2. ✅ Formatted code with black

Status: ⚠️ DONE_WITH_CONCERNS
Please fix critical issues before merging.

# Step 6: QA testing
User: "/qa user profiles"

AI: Running systematic QA tests...

Test Results:
- Health Score: 87/100
- Bugs Found: 5
- Bugs Fixed: 5
- Tests Passed: 42/42

Status: ✅ Ready to ship

# Step 7: Deploy
User: "/ship"

AI: Preparing automated release...

1. ✅ Merged base branch
2. ✅ Ran all tests (42/42 passed)
3. ✅ Updated version to v2.1.0
4. ✅ Generated changelog
5. ✅ Created PR #234
6. ✅ Updated documentation

Status: ✅ SHIPPED
PR: https://github.com/your/repo/pull/234
```

**Total time**: ~15 minutes for end-to-end feature development and deployment

## Installation

### Option 1: Copy to Skills Directory

```bash
# For OpenClaw
cp -r gstack-skills ~/.openclaw/skills/

# For WorkBuddy
cp -r gstack-skills ~/.workbuddy/skills/
```

### Option 2: Symbolic Link (Development)

```bash
# Create symbolic link
ln -s /path/to/gstack-openclaw-skills/gstack-skills ~/.openclaw/skills/gstack-skills
```

### Option 3: Project-Level Installation

Copy to your project root:

```bash
cp -r gstack-skills/ /path/to/your/project/
```

### Verification

```python
# In OpenClaw/WorkBuddy, test installation
User: "/gstack"

# If installed correctly, you'll see the command overview
```

## Philosophy

### Boil the Lake Principle

> "Don't be half-invested, boil the whole lake" - Garry Tan

AI-assisted development should pursue **complete implementation**, not shortcuts.

- **Identify problems, then actually fix them** (don't just note them)
- **Complete the task** (don't leave "todo: optimize" comments)
- **100% quality is achievable** with AI assistance (don't settle for "good enough")

### Intelligent Borrowing

When borrowing features from other products, always ask:

1. **Why does it work in the original product?**
2. **Will it succeed or fail in your product?**
3. **What adaptations are needed for success?**

### Specificity is the Only Currency

- **Demand specific evidence**, not vague descriptions
- **"10 people said they want it"** is worth more than **"everyone wants it"**
- **Focus on actual behavior**, not stated interest

## Documentation

- **[USAGE.md](USAGE.md)**: Complete usage guide with examples
- **[SKILL.md](gstack-skills/SKILL.md)**: Main skill documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: How to contribute

## Architecture

```
gstack-openclaw-skills/
├── gstack-skills/              # Main skill package
│   ├── SKILL.md               # Main entry point and router
│   ├── office-hours/          # Product ideation
│   ├── plan-ceo-review/       # CEO perspective
│   ├── plan-eng-review/       # Engineering review
│   ├── review/                # Code review
│   ├── qa/                    # Testing and QA
│   ├── ship/                  # Deployment
│   ├── investigate/           # Debugging
│   └── scripts/               # Helper scripts
│       ├── command_router.py  # Command routing
│       └── state_manager.py   # State management
├── USAGE.md                   # Usage guide
├── README.md                  # This file
└── CONTRIBUTING.md            # Contributing guide
```

## How It Works

### Command Routing

When you type a command:

```python
User: "/review my changes"
```

The `command_router.py` script:

1. Parses the input: `/review` + `my changes`
2. Routes to the appropriate skill: `review/SKILL.md`
3. Loads the skill instructions
4. AI executes the skill's workflow automatically

### State Management

Skills can share data through workflow state:

```python
# Workflow starts
/state_manager.py init → creates workflow ID: abc12345

# Each skill can read/write state
/office-hours → saves validation results
/plan-eng-review → reads validation, saves architecture
/review → reads architecture, saves code issues
/qa → reads code issues, saves test results
/ship → reads all state, creates deployment package
```

### Automated Execution

Unlike v1.0 (which only provided guidance), v2.0 skills:

1. **Analyze context** (git status, project structure, etc.)
2. **Execute workflows** automatically
3. **Make decisions** (what tests to run, what bugs to fix)
4. **Take actions** (run tests, fix bugs, create PRs)
5. **Report results** (comprehensive status reports)

## Comparison with Original gstack

| Feature | Original gstack | gstack-skills v2.0 |
|---------|----------------|-------------------|
| Platform | Claude Code | OpenClaw/WorkBuddy |
| Execution | Manual scripts | AI-executed workflows |
| Commands | Slash commands | Commands + natural language |
| Integration | Bun/Git specific | Platform-agnostic |
| State | File-based | Managed state system |
| Learning Curve | High | Low |

## FAQ

### Q: How is this different from the original gstack?

**A**: The original gstack was built for Claude Code with manual scripts. gstack-skills v2.0 is a complete rewrite for OpenClaw/WorkBuddy that automates execution. You don't need Bun or specific scripts - just use natural language commands.

### Q: Can I use this with any OpenClaw/WorkBuddy project?

**A**: Yes! gstack-skills is platform-agnostic and works with any project.

### Q: Do I need to install dependencies?

**A**: No, gstack-skills doesn't require external dependencies. It uses the tools you already have (git, your test framework, etc.).

### Q: What if a command fails?

**A**: Each skill provides clear error messages and suggests how to fix issues. Common issues are documented in the [USAGE.md](USAGE.md) troubleshooting section.

### Q: Can I customize the workflows?

**A**: Yes! Each skill is a separate markdown file that you can customize. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Q: Does this work with CI/CD?

**A**: `/ship` is designed to work with existing CI/CD pipelines. It runs tests, generates PRs, and updates documentation - all CI/CD compatible.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Areas where we'd love help:
- Adding more specialized skills
- Improving error handling
- Adding more examples
- Writing tests
- Translating documentation

## License

MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments

- **Garry Tan** for creating [gstack](https://github.com/garrytan/gstack) and sharing the "Boil the Lake" philosophy
- **Y Combinator** for the office hours framework
- **All contributors** to gstack-skills

## Links

- **GitHub**: https://github.com/AICreator-Wind/gstack-openclaw-skills
- **Original gstack**: https://github.com/garrytan/gstack
- **OpenClaw**: https://openclaw.ai
- **WorkBuddy**: https://codebuddy.cn

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-21  
**Status**: ✅ Production Ready
