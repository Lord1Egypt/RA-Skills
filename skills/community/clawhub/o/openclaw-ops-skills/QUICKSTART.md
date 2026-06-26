# Quick Start Guide

Get your OpenClaw agent running production-ready autonomous operations in 15 minutes.

## Step 1: Install Skills (2 minutes)

```bash
# Copy skills to your OpenClaw workspace
cp skills/*.md ~/.openclaw/workspace/skills/

# Verify installation
ls ~/.openclaw/workspace/skills/
```

You should see: model-routing.md, execution-discipline.md, docs-first.md, etc.

## Step 2: Set Up Workspace Files (5 minutes)

```bash
# Navigate to workspace
cd ~/.openclaw/workspace

# Copy templates
cp /path/to/openclaw-ops-skills/templates/workspace-setup.md .

# Extract and create individual files
# (Create USER.md, MEMORY.md, Todo.md, progress-log.md, SOUL.md)

# Example: Create USER.md
cat > USER.md << 'EOF'
# User Profile
**Name**: Your Name
**Role**: Developer
**Timezone**: Your TZ

# [Fill in the rest from the template]
EOF
```

## Step 3: Configure Model Routing (2 minutes)

Edit or create `~/.openclaw/config.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": [
          "anthropic/claude-opus-4-6",
          "openrouter/moonshotai/kimi-k2.5"
        ]
      }
    }
  }
}
```

## Step 4: Set Up Overnight Cron Jobs (3 minutes)

```bash
# Early night check
openclaw cron add \
  --name "overnight-2am" \
  --cron "0 2 * * *" \
  --message "Check Todo.md. Pick up incomplete tasks. Update progress-log."

# Mid night continuation
openclaw cron add \
  --name "overnight-4am" \
  --cron "0 4 * * *" \
  --message "Continue working through Todo.md. Update progress-log."

# Morning briefing
openclaw cron add \
  --name "overnight-6am" \
  --cron "0 6 * * *" \
  --message "Final check. Summarize all overnight work."
```

## Step 5: Restart OpenClaw (1 minute)

```bash
openclaw restart
```

## Step 6: Test with a Simple Task (2 minutes)

```
You: Create a test file called test.txt with "Hello from OpenClaw" inside.

Agent: [Should follow execution-discipline.md]
      [Should update progress-log.md]
      [Should update Todo.md if applicable]
```

## Verification Checklist

After setup, verify:

```bash
# Skills are loaded
openclaw skills list

# Cron jobs are scheduled
openclaw cron list

# Workspace files exist
ls ~/.openclaw/workspace/*.md

# Test the agent
openclaw chat "Test: What skills do you have access to?"
```

## What to Expect

### Before These Skills
- Agent stops after one task
- Expensive model usage
- Lost context when sessions compress
- No visibility into overnight work
- Repeated mistakes

### After These Skills
- Autonomous task continuation
- Optimized model selection (80% cost savings)
- Persistent memory across sessions
- Complete progress logs
- Learning from failures

## Common First Tasks to Try

1. **"Set up a basic Express server with auth"**
   - Tests: docs-first, execution-discipline, scope-control

2. **"Review this PR and leave comments"**
   - Tests: communication, progress-logging

3. **"Update all dependencies in package.json"**
   - Tests: scope-control, error-recovery

4. **"Assign me a task at 10pm, check progress at 7am"**
   - Tests: task-autonomy, cron-orchestration, progress-logging

## Troubleshooting

### Skills not loading
```bash
# Check skills directory
ls -la ~/.openclaw/workspace/skills/

# Verify file permissions
chmod 644 ~/.openclaw/workspace/skills/*.md

# Restart OpenClaw
openclaw restart
```

### Cron jobs not running
```bash
# Check cron list
openclaw cron list

# Check cron logs
openclaw logs --cron

# Test cron manually
openclaw cron run overnight-2am --dry-run
```

### Workspace files not found
```bash
# Create workspace directory
mkdir -p ~/.openclaw/workspace

# Copy templates
cp templates/*.md ~/.openclaw/workspace/

# Edit each file
nano ~/.openclaw/workspace/USER.md
```

## Next Steps

1. **Customize USER.md** with your preferences
2. **Update MEMORY.md** with your project details
3. **Review skills** and customize as needed
4. **Monitor first overnight run** and adjust

## Support

- **Author**: Eric Jie <jxmerich@mail.com>
- GitHub Issues: https://github.com/Erich1566/openclaw-ops-skills/issues
- Documentation: See README.md
- Community: [Link to community/forum]

---

**Ready to transform your agent from chatbot to infrastructure?**

Let's build something amazing while you sleep. 🚀
