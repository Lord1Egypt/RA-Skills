# Tutor Buddy Pro — Setup Instructions

Paste this entire message to your AI agent. It will set up Tutor Buddy Pro automatically.

---

## Setup Prompt

Please set up Tutor Buddy Pro by following these steps exactly:

### Step 1: Locate the skill files

Run this command to find the Tutor Buddy Pro skill files:

```bash
# Files are installed by clawhub install — no manual copy needed
```

This will output the skill directory path. Save it — you'll need it.

### Step 2: Create the data directories

From your workspace root, run:

```bash
mkdir -p data/study-plans
chmod 700 data data/study-plans
```

### Step 3: Copy configuration files

```bash
# Files are installed by clawhub install — no manual copy needed
cp "$SKILL_DIR/tutor-config.json" data/tutor-config.json
chmod 600 data/tutor-config.json
```

### Step 4: Initialize data files

Create the required empty data files:

```bash
echo '{}' > data/learner-profile.json
echo '[]' > data/quiz-history.json
echo '[]' > data/session-log.json
chmod 600 data/learner-profile.json data/quiz-history.json data/session-log.json
```

### Step 5: Set permissions on the skill directory

```bash
# Files are installed by clawhub install — no manual copy needed
find "$SKILL_DIR" -type d -exec chmod 700 {} \;
find "$SKILL_DIR" -type f -exec chmod 600 {} \;
```

### Step 6: Verify installation

Run these checks to confirm everything is in place:

```bash
echo "=== Tutor Buddy Pro Setup Verification ==="

# Check SKILL.md exists
# Files are installed by clawhub install — no manual copy needed

# Check config
test -f data/tutor-config.json && echo "✅ Config file created" || echo "❌ Config file missing"

# Check data files
test -f data/learner-profile.json && echo "✅ Learner profile initialized" || echo "❌ Learner profile missing"
test -f data/quiz-history.json && echo "✅ Quiz history initialized" || echo "❌ Quiz history missing"
test -f data/session-log.json && echo "✅ Session log initialized" || echo "❌ Session log missing"

# Check directories
test -d data/study-plans && echo "✅ Study plans directory ready" || echo "❌ Study plans directory missing"

# Check permissions
PERMS=$(stat -f "%Lp" data/tutor-config.json 2>/dev/null || stat -c "%a" data/tutor-config.json 2>/dev/null)
[ "$PERMS" = "600" ] && echo "✅ File permissions correct (600)" || echo "⚠️ File permissions: $PERMS (expected 600)"

echo "=== Verification Complete ==="
```

If all checks show ✅, you're ready! Try saying: **"Help me with my math homework"** or **"Quiz me on algebra"**

---

## Troubleshooting

- **"SKILL.md not found"** — Make sure you extracted the Tutor Buddy Pro files into your agent's skills directory.
- **Permission errors** — Re-run the chmod commands in Steps 2, 4, and 5.
- **Config file missing** — Re-run Step 3. The config template should be in the skill's `config/` folder.
