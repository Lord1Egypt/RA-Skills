# SkillSpector audit — lygo-automation-workflows v1.0.0

Upstream inspiration `jk-0001/automation-workflows` had:

| Finding | LYGO response |
|---------|----------------|
| Vague Triggers (Medium) | Narrow description; LYGO/workflow-design scoped |
| Missing User Warnings (Medium) | SECURITY.md + plan JSON privacy block + playbook rules |

## Static posture

- No subprocess / network / shell  
- Advisor + optional local JSON planner only  
- VirusTotal N/A until publish; expect clean (docs+stdlib)

## Proof

```bash
python scripts/self_check.py
python scripts/workflow_planner.py demo
```
