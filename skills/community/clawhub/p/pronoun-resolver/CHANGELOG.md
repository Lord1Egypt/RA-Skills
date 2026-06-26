# Changelog

All notable changes to the Pronoun Resolver skill are documented here.

## [0.11.0] - 2026-05-31

### Added
- **Always-present logging directive.** The hook now injects a
  `[PRONOUN-RESOLVER-LOG: ...]` directive on every flagged message, carrying the
  exact `bin/log-resolution.py` command and ledger path. The hook prints the
  directive; Claude runs it to record a resolution. The directive is now in
  context on every fire even when `SKILL.md` isn't loaded (previously the logging
  instruction lived only in the skill body, so the ledger almost never updated).
- **`bin/log-resolution.py`** — a locked, sanitizing ledger writer that owns all
  ledger mutations.
- **`tests/test_log_resolution.py`** — dependency-free unit tests for the
  sanitizer, ledger I/O, validation, and concurrency.

### Security
- **Secret/PII redaction** on every free-text field before it touches disk:
  API keys, tokens (OpenAI/Stripe/GitHub/GitLab/Slack/npm/Google), JWTs, PEM
  private keys, credentials in DB URLs, Bearer/Basic auth, emails, SSNs, phone
  numbers, and long hex/base64 blobs. Control characters (except tab/newline)
  stripped; over-long values truncated.
- **`prompt_hash` validated** as a hex digest (raw text is dropped), and the
  emitted hook directive single-quotes install-derived paths so a checkout path
  containing shell metacharacters can't become executable syntax.

### Fixed
- **Concurrency race:** ledger writes now run under an exclusive `flock` across
  the full read-modify-write, so parallel hook fires no longer drop entries.
- **Corruption safety:** a non-empty ledger that can't be parsed (or isn't the
  expected object shape) is backed up to `*.corrupt` instead of being silently
  overwritten; `confidence` is clamped to `[0,1]` (non-finite → `0.5`) and the
  writer refuses to emit `NaN`/`Infinity` (`allow_nan=False`).
