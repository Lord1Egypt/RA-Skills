# SECURITY — LYGO Second Brain

- **No secrets** in vault notes or prompts committed to git.
- **Local Ollama only** by default (`127.0.0.1:11434`); do not point at untrusted remote inference without user approval.
- **PDF ingest** uses `pdftotext` (subprocess) — only ingest PDFs from trusted sources.
- Agents must **not** `git push` vault or stack without explicit user request.
- **No auto-publish** to ClawHub, Moltbook, or social.
- Vault may contain **PII** — treat `LYGO_VAULT_ROOT` as sensitive path; do not upload vault to public repos.
- Kernel egg / permaweb plant requires **`lygo-kernel-egg-planter`** consent flow.