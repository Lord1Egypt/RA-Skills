# Freelancer Toolkit — Security

## Data Storage

Freelancer Toolkit stores all data as JSON files in `~/.freelancer-toolkit/` on whatever machine your OpenClaw agent runs on. This includes:

- Client names, contact info, and billing rates
- Project details and quoted prices
- Time entries with dates, hours, and descriptions
- Invoice records and payment status

## What This Means

- Your data lives wherever your OpenClaw agent's host file system is. That could be your laptop, a cloud VM, a Mac Mini in your closet, or any other machine.
- Freelancer Toolkit does not transmit data to external servers on its own. However, your OpenClaw agent may process data through LLM providers, cloud services, or integrations depending on your agent's configuration.
- Backups, encryption, and access control are your responsibility based on your hosting setup.

## Sensitive Data Handling

This tool stores client contact info and financial data (rates, billed amounts, payment status). Treat the `~/.freelancer-toolkit/` directory accordingly:

- Restrict file permissions (`chmod 700 ~/.freelancer-toolkit/`)
- Include in your backup strategy
- Consider your host machine's security posture (disk encryption, access controls)
- If you're on a shared machine, other users with access to your home directory can read these files

## Scripts

All scripts in `scripts/` are Bash scripts that:
- Read from and write to `~/.freelancer-toolkit/` only
- Do not make network requests
- Do not install software (except `jq` via system package manager during setup, with user confirmation)
- Use `set -euo pipefail` for safe execution

## InvoiceGen Pro Integration

When generating invoices via InvoiceGen Pro, client and billing data is passed to that tool's processing pipeline. Review InvoiceGen Pro's own security documentation for details on how it handles invoice data.

## Recommendations

1. **Use disk encryption** on the machine running your OpenClaw agent
2. **Set directory permissions**: `chmod 700 ~/.freelancer-toolkit/`
3. **Back up regularly** — these JSON files are your billing records
4. **Audit exports** — CSV and JSON exports in `~/.freelancer-toolkit/exports/` contain billing data; clean up files you no longer need
5. **Review agent config** — understand which LLM providers and services your OpenClaw agent connects to

## Reporting Issues

If you discover a security concern with Freelancer Toolkit, contact us at [normieclaw.ai](https://normieclaw.ai).
