# ERRORS.md — jobautopilot submitter quick reference

> For platform-specific quirks, see `~/.openclaw/platform/<platform>/quirks.md`

| Error | Explanation |
|-------|-------------|
| Resume not uploaded but page shows success | Submission likely failed — note it in the tracker |
| `click` before `upload` | File dialog already opened, interceptor is disarmed — file will not upload |
| Using JS injection to fill fields | Framework events won't fire, form validation will fail — use `fill`/`type` instead |
| Reusing old ref after clicking Add | New components get new refs — always re-snapshot after clicking Add |
| `grep -iF` multi-condition match fails | `-F` treats `\|` as a literal — use `-iE` for multi-condition fuzzy matching |
| `jq` fails parsing `evaluate` return value | `evaluate` returns a plain string, not JSON — use `grep`/`sed` instead |
| Old TARGET_ID used after platform redirect | Some sites redirect to a third-party system after submit — re-fetch TARGET_ID for the new page |
| Script runs without validating tab first | Script must verify TARGET_ID exists and URL matches before doing anything |
| Filling fields one by one with `type` | Never loop `type` per field — batch all fields in a single `fill` call |
| Using `sleep` to wait for page load | Use `wait --load networkidle` instead — more reliable and faster |
| `--targetId` parameter name error | Correct flag is `--target-id` (hyphenated) — CLI will suggest the right name |
| Using `write` tool to create script files | `$(date +%s)` does not expand inside `write` — use `exec` + `cat heredoc` and run with exact path `bash "$SCRIPT"` |
| Special decorators in script comments | Bash will try to execute them as commands — use only `#` comments, no em-dashes or decorative chars |
| Hardcoded uppercase in config.sh path | Linux paths are case-sensitive — use `${OPENCLAW_USER}` variable, never hardcode case |
| `type` + `press Enter` to submit | Use `type --submit` instead — single command, more reliable |
| Going straight to "Forgot password" when email exists | Try logging in with saved credentials first — only fall back to password reset if autofill does not activate |
| Re-navigating to job detail after password reset | After reset, check `tabs` first — if original tab is still open, switch back to it |
| Not handling Save password dialog | Must accept Save after login/register — browser profile won't autofill next time otherwise |
