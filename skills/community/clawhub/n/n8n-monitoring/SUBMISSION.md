# ClawhHub Skill Submission

## Metadata

- **slug:** `n8n-monitor`
- **display_name:** Monitor n8n Automations with OpenClaw
- **version:** 1.0.0
- **category:** DevOps / Monitoring
- **tags:** n8n, monitoring, workflow automation, alerting, debugging, DevOps, Telegram

## Summary

Automated monitoring and debugging of self-hosted n8n workflow executions. Connects OpenClaw to your n8n instance via a webhook, provides health checks (GREEN/YELLOW/RED), failure analysis with per-workflow metrics, error debugging with failed node identification, and formatted Telegram alerts. Includes notification templates for cron-based monitoring with alert deduplication.

## Author

- **name:** Samir Saci
- **url:** https://www.samirsaci.com
- **linkedin:** https://www.linkedin.com/in/samir-saci

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition with endpoints, templates, and usage instructions |
| `README.md` | Setup guide with n8n workflow template and tutorial links |
| `SUBMISSION.md` | This file (ClawhHub submission metadata) |

## Dependencies

- Self-hosted n8n instance with API access
- n8n webhook workflow (template provided)
- `N8N_WEBHOOK_URL` environment variable

## Links

- **n8n Workflow Template:** https://n8n.supply-science.com/workflows/DevOps/AI_Agent_for_Debugging_Workflow_Executions
- **Video Tutorial:** https://youtu.be/oJzNnHIusZs
- **Article:** https://towardsdatascience.com/deploy-your-ai-assistant-to-monitor-and-debug-n8n-workflows-using-claude-and-mcp/
- **GitHub (MCP Server):** https://github.com/samirsaci/mcp-n8n-monitor
