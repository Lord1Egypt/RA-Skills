# Model Routing Table — Template

> Read this file when you need to choose which model to use for a specific task type.
> Customise this table for your specific models. The authoritative inventory is in your
> `orchestrator-data/models.json`.

---

## How to Customise

1. Run `/project-orchestration onboard` to catalogue your models
2. This generates `models.json` in your data directory
3. Edit this file to add your preferred routing chains
4. Model aliases are shorthand names you define in your setup

## Routing Table Template

| Task Type | Primary | Fallback 1 | Fallback 2 | Last Resort |
|-----------|---------|------------|------------|-------------|
| Heavy coding / complex logic | [Your best coding model] | [Coding ACP] | [Fast cloud model] | [Local fallback] |
| Quick code edits / simple | [Fast cloud model] | [Free tier model] | [Local model] | [Small local] |
| Deep research | [Best reasoning model] | [Free tier] | [Local] | [Fast cloud] |
| Quick lookup / research | [Fast cloud] | [Free tier] | [Small free] | [Local] |
| Creative writing / story | [Creative local model] | [Cloud model] | [Best reasoning] | [Fast] |
| Planning / design | [Best reasoning] | [Local] | [Fast cloud] | [Free tier] |
| File organization / cleanup | [Small free model] | [Fast cloud] | [Local] | [Small local] |
| Vision / image analysis | [Cloud vision model] | [Local vision] | [Laptop vision] | [Edge device] |
| Heavy reasoning / math | [Best reasoning] | [Local] | [Fast cloud] | [Creative local] |
| Documentation / summaries | [Small free] | [Fast cloud] | [Local] | [Small local] |

## Vision Fallback Chain Template
1. Primary: [Cloud vision model — cheap, fast]
2. Fallback: [Local vision model — always available]
3. Fallback: [Laptop vision model — intermittent]
4. Fallback: [Edge device — slow but always up]
5. Last resort: Describe manually

## Pro Tips
- Use `session_status` to check current model usage and limits
- Set `ORCHESTRATOR_DATA_DIR` to point to your data directory
- Run `bash scripts/check-prices.sh` periodically to track pricing changes
- Run `/project-orchestration status` to see your current orchestration state