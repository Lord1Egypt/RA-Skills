# Security — lygo-automation-workflows

## Permissions

| Capability | Default |
|------------|---------|
| Network | **None** |
| Subprocess / shell | **None** |
| Filesystem write | Only `--write` + `--i-consent` |
| Publish / account linking | **None** |

## Privacy (addresses upstream audit)

When users implement plans in Zapier/Make/n8n/CRM:

1. **Consent** — steward approves each new vendor connection  
2. **Least privilege** — OAuth scopes minimized  
3. **Data minimization** — only required fields  
4. **No secrets in alerts** — redacted Slack/email  
5. **Retention + disable path** — documented  

This skill **never** moves customer/payment data itself.

## Trigger hygiene

Description avoids ultra-broad triggers like bare “save time” / “automate” alone — prefer LYGO/workflow-design intent.
