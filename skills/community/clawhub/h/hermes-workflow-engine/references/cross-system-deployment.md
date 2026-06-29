# Cross-System Deployment: Hermes → OpenClaw

When deploying workflow-engine to OpenClaw (龙虾), adapt paths and test.

## Deployment Steps

```bash
# 1. Create directories on remote
ssh root@43.173.120.234 "mkdir -p /root/.openclaw/workspace/workflow-engine"
ssh root@43.173.120.234 "mkdir -p /root/.openclaw/workspace/skills/workflow-engine"

# 2. Copy SKILL.md
scp ~/.hermes/skills/devops/workflow-engine/SKILL.md root@43.173.120.234:/root/.openclaw/workspace/skills/workflow-engine/

# 3. Adapt paths in SKILL.md
ssh root@43.173.120.234 "sed -i 's|~/.hermes/workflow-engine/|~/.openclaw/workspace/workflow-engine/|g' /root/.openclaw/workspace/skills/workflow-engine/SKILL.md"
ssh root@43.173.120.234 "sed -i 's/author: 小狗/author: 老狗/' /root/.openclaw/workspace/skills/workflow-engine/SKILL.md"

# 4. Package and copy code
cd ~/.hermes/workflow-engine && tar czf /tmp/workflow-engine-code.tar.gz --exclude='runs/*' --exclude='_community/*' --exclude='workflows/*' *.py *.md examples/
scp /tmp/workflow-engine-code.tar.gz root@43.173.120.234:/tmp/
ssh root@43.173.120.234 "cd /root/.openclaw/workspace/workflow-engine && tar xzf /tmp/workflow-engine-code.tar.gz"

# 5. Adapt paths in Python code (critical!)
ssh root@43.173.120.234 "sed -i \"s|Path.home() / '.hermes' / 'workflow-engine'|Path.home() / '.openclaw' / 'workspace' / 'workflow-engine'|g\" /root/.openclaw/workspace/workflow-engine/run.py"

# 6. Verify
ssh root@43.173.120.234 "cd /root/.openclaw/workspace/workflow-engine && python3 run.py list"
ssh root@43.173.120.234 "cd /root/.openclaw/workspace/workflow-engine && python3 run.py validate examples/ai-news-daily.yaml"
```

## Path Mapping

| Hermes | OpenClaw |
|--------|----------|
| `~/.hermes/workflow-engine/` | `~/.openclaw/workspace/workflow-engine/` |
| `~/.hermes/skills/devops/workflow-engine/` | `~/.openclaw/workspace/skills/workflow-engine/` |

## Pitfalls

- **run.py has hardcoded paths**: Must sed-replace `Path.home() / '.hermes' / 'workflow-engine'` to `Path.home() / '.openclaw' / 'workspace' / 'workflow-engine'`
- **SSH QR code banner**: Tencent Cloud shows QR code login banner on SSH, but commands still execute normally
- **Exclude runtime dirs**: tar excludes runs/, _community/, workflows/ (contain execution history, not code)
- **Author attribution**: Change `小狗` to `老狗` in SKILL.md for 龙虾 version
