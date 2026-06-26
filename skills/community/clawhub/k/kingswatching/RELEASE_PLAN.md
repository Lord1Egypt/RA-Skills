# King's Watching (kingswatching) v0.4.0 Release Plan

## 📦 Packaged Files

**File**: `kingswatching-v0.4.0.tar.gz`  
**Size**: ~42KB  
**Contains**: Source code + examples + docs (all in English)

---

## 🚀 Local Installation Test (Completed)

### Installation Methods

```bash
# Method 1: Extract and use directly (recommended as skill)
tar -xzvf kingswatching-v0.4.0.tar.gz -C /path/to/openclaw/skills/

# Method 2: pip install (as Python package)
cd kingswatching
pip install -e .  # Development mode
# or
pip install .     # Normal install
```

### Verify Installation

```python
from overseer import Overseer, TaskTranslator, translate_and_run

# Test basic functionality
wf = Overseer("Test Workflow")

@wf.step("Step 1")
def step1(ctx):
    return "Result 1"

@wf.step("Step 2")
def step2(ctx):
    return "Result 2"

print(f"✅ Installation successful, {len(wf.steps)} steps")
```

---

## 📋 Publish to ClawHub Steps

### Step 1: Preparation

```bash
# Confirm logged into clawhub
clawhub whoami

# If not logged in
clawhub login  # Opens browser for auth
```

### Step 2: Enter Project Directory

```bash
cd /path/to/kingswatching
ls  # Confirm contains: SKILL.md, setup.py, overseer/
```

### Step 3: Publish

```bash
clawhub publish . \
  --slug kingswatching \
  --name "King's Watching" \
  --version 0.4.0 \
  --changelog "Initial release: AI workflow enforcer inspired by the Steam game 'The King Is Watching'. Features forced sequential execution, state persistence, heartbeat anti-timeout, auto task chunking, and step verification. Makes AI work like game subjects - only productive when watched."
```

**Parameters**:
- `--slug kingswatching`: Unique identifier, users install with `clawhub install kingswatching`
- `--name "King's Watching"`: Display name
- `--version 0.4.0`: Version number
- `--changelog`: Release notes

### Step 4: Verify Publication

```bash
# Search to confirm
clawhub search kingswatching

# View details
clawhub inspect kingswatching
```

---

## 📝 Release Copy (Ready to Use)

### Title
**King's Watching (kingswatching)** - AI Workflow Enforcer, Makes AI Stop Slacking

### Summary
Inspired by the Steam hit game *The King Is Watching*: just like how subjects in the game only work when the King's gaze is upon them, this tool ensures AI agents cannot cut corners and must execute every step to completion.

### Core Capabilities
1. **Forced Sequential Execution** - Hard constraints, AI cannot skip steps
2. **State Persistence** - Auto-saves execution state, supports checkpoint resume
3. **Heartbeat Mechanism** - Prevents 15-minute timeout disconnect
4. **Task Translator** - Converts natural language to execution plans with auto-chunking (e.g., "Download 100" → 10 Steps)
5. **Step Verification** - Every Step has forced verification, cannot cut corners
6. **Periodic Reports** - Natural language interval configuration (e.g., "Every 5 minutes")

### One-liner Selling Point
> User says "Download 100 items", King's Watching auto-splits into 10 Steps, reports every 5 minutes, AI cannot cut corners.

### Use Cases
- Complex multi-step tasks (research, reporting, data processing)
- Scenarios requiring strict sequential execution
- Long-running tasks (anti-timeout)
- Auditable, recoverable execution processes
- Preventing AI from cutting corners on large tasks

### Quick Example
```python
from overseer import translate_and_run

# One-liner starts complete workflow
result = translate_and_run("Download 100 photochemistry research reports")
```

---

## 🎯 Promotion Strategy

### Channels
1. **ClawHub Homepage** - Appears in latest list after publication
2. **OpenClaw Discord** - Share in #skills channel with screenshots
3. **Reddit/Hacker News** - Post to r/OpenClaw, r/AIAutomation
4. **Twitter/X** - Thread about the game-inspired design
5. **Technical Blog** - Article explaining the design and use cases

### Key Selling Points
- **Game Reference**: *The King Is Watching* players get it instantly
- **Pain Point Solved**: AI cutting corners is a universal problem
- **Ease of Use**: One natural language command starts complex workflows

### Future Iterations
- v0.5.0: Native OpenClaw messaging integration
- v0.6.0: Visual execution diagrams
- v1.0.0: Deep Workflow Engine integration

---

## 📁 File Manifest

```
kingswatching/
├── SKILL.md              # Skill definition (ClawHub reads this)
├── setup.py              # Python package config
├── README.md             # Project intro (English)
├── INSTALL.md            # Installation guide
├── USER_GUIDE.md         # User manual
├── DEVELOPMENT_LOG.md    # Development log
├── test_overseer.py      # Test suite
├── overseer/             # Core source code
│   ├── __init__.py       # Main entry
│   ├── translator.py     # TaskTranslator
│   └── reporter.py       # ProgressReporter
└── examples/             # Example code (6 examples)
    ├── demo_translator.py      # Translator demo
    ├── demo_reporter.py        # Reporter demo
    ├── demo_features.py        # Feature demo
    ├── demo_v040_full.py       # v0.4.0 full demo
    ├── test_dev_scenarios.py   # Dev task tests
    └── test_multi_scenarios.py # Multi-scenario tests
```

---

## ✅ Pre-release Checklist

- [x] Code tested and working
- [x] SKILL.md metadata complete
- [x] README.md clear and understandable
- [x] All documentation in English
- [x] Version consistent (0.4.0)
- [x] Bullma examples removed
- [x] Package file generated
- [ ] ClawHub login confirmed
- [ ] Publish command executed
- [ ] Post-publish search verification

---

**Status**: Local testing passed ✅, Ready for release ⏳
