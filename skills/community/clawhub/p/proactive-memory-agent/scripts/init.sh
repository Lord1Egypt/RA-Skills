#!/bin/bash
# Proactive Memory Agent - Initialization Script
# Sets up the complete memory architecture

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
LEARNINGS_DIR="$WORKSPACE/.learnings"

echo "🧠 Proactive Memory Agent - Initialization"
echo "=========================================="
echo ""

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$MEMORY_DIR"/{hot,warm,cold,episodic,semantic,procedural}
mkdir -p "$LEARNINGS_DIR"
mkdir -p "$WORKSPACE/memory/snapshots"

echo "   ✓ memory/hot/     — Current session (HOT tier)"
echo "   ✓ memory/warm/    — Recent context (WARM tier)"
echo "   ✓ memory/cold/    — Archive (COLD tier)"
echo "   ✓ .learnings/     — Error/Learning logs"
echo ""

# Create template files
echo "📝 Creating template files..."

# SESSION-STATE.md
cat > "$WORKSPACE/SESSION-STATE.md" << 'EOF'
# Session State (HOT Memory)

**Last Updated:** [Auto-updated by WAL protocol]
**Status:** Active

## Current Task
[Current task description]

## Key Decisions
- [Decision 1]
- [Decision 2]

## User Preferences
- [Preference 1]
- [Preference 2]

## Next Steps
1. [Next step]
2. [Next step]

## Working Notes
[Temporary notes, cleared on task completion]
EOF

# HOT_MEMORY.md (for context budgeting)
cat > "$MEMORY_DIR/hot/HOT_MEMORY.md" << 'EOF'
# HOT Memory — Context Budget 10% Zone

**Updated:** [timestamp]
**Session:** [session_id]

## Current Status
[1-2 sentence status]

## Key Decisions Made
- [Decision with rationale]

## Next Immediate Step
[What to do next]

## Blockers (if any)
- [Blocker and potential solution]
EOF

# WARM memory placeholder
cat > "$MEMORY_DIR/warm/WARM_MEMORY.md" << 'EOF'
# WARM Memory — Context Budget 40% Zone

## User Preferences (Stable)
- Timezone: [user timezone]
- Communication style: [preferences]

## Recurring Tasks
- [Task pattern]

## Tool Configurations
- [Tool setups]
EOF

# Working Buffer
cat > "$MEMORY_DIR/working-buffer.md" << 'EOF'
# Working Buffer (Danger Zone Log)

**Status:** INACTIVE
**Purpose:** Capture exchanges when context > 60%

## Activation Trigger
When context usage exceeds 60%, this buffer becomes ACTIVE
and logs every exchange until compaction or session end.

---
EOF

# .learnings templates
cat > "$LEARNINGS_DIR/ERRORS.md" << 'EOF'
# Error Log

## Format: [ERR-YYYYMMDD-XXX] command_name

**Logged:** ISO-8601 timestamp
**Priority:** high
**Status:** pending

### Summary
Brief error description

### Error Output
```
Actual error message
```

### Context
- Command attempted
- Parameters used

### Suggested Fix
How to resolve

---
EOF

cat > "$LEARNINGS_DIR/LEARNINGS.md" << 'EOF'
# Learnings Log

## Format: [LRN-YYYYMMDD-XXX] category

**Logged:** ISO-8601 timestamp
**Priority:** medium
**Status:** pending

### Summary
What was learned

### Details
Full context

### Suggested Action
What to do differently

### Metadata
- Source: conversation | error | user_feedback
- Related Files:

---
EOF

cat > "$LEARNINGS_DIR/FEATURE_REQUESTS.md" << 'EOF'
# Feature Requests

## Format: [FEAT-YYYYMMDD-XXX] capability

**Logged:** ISO-8601 timestamp
**Priority:** low
**Status:** pending

### Requested Capability
What user wanted

### User Context
Why they needed it

### Complexity
simple | medium | complex

---
EOF

echo "   ✓ SESSION-STATE.md"
echo "   ✓ memory/hot/HOT_MEMORY.md"
echo "   ✓ memory/warm/WARM_MEMORY.md"
echo "   ✓ memory/working-buffer.md"
echo "   ✓ .learnings/ERRORS.md"
echo "   ✓ .learnings/LEARNINGS.md"
echo "   ✓ .learnings/FEATURE_REQUESTS.md"
echo ""

# Create state file
cat > "$MEMORY_DIR/.proactive-memory-state.json" << EOF
{
  "initialized": true,
  "version": "1.0.0",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "stats": {
    "context_checks": 0,
    "checkpoints": 0,
    "tiering_operations": 0
  },
  "config": {
    "danger_zone_threshold": 60,
    "checkpoint_threshold": 80,
    "budget_zones": {
      "objective": 10,
      "short_term": 40,
      "decision_log": 20,
      "background": 20
    }
  }
}
EOF

echo "✅ Initialization complete!"
echo ""
echo "Next steps:"
echo "   1. Run: detect.sh (check current context usage)"
echo "   2. Review: SESSION-STATE.md template"
echo "   3. Add to HEARTBEAT.md for automatic monitoring"
echo ""
echo "📚 Documentation: skills/proactive-memory-agent/SKILL.md"
