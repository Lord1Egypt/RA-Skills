# CLAUDE.md

Guidance for Claude Code when working in this folder.

## What this is

The OpenClaw skill that registers any OpenClaw agent as a reduced-trust member of a NANDA chapter. Published to ClawHub as `nanda-chapter` (slug) / "NANDA Chapter Skill" (display title). Conforms to NANDA Chapter Protocol v0.3 by default; v0.2 fallback via `--scheme ed25519`.

## Working rules

1. **Nothing in the published bundle may reference any private repository.** The umbrella + sibling repos are private. Pre-publish lint:
   ```bash
   grep -rn "github.com\|Sharathvc23/\|chapter-runtime\|nanda-openclaw-skill\|\\.\\./" \
     SKILL.md README.md SECURITY.md helpers/ examples/
   ```
   Must come back empty (modulo `.clawhubignore`-d files like `CONTRIBUTING.md`).
2. **`.clawhubignore` is load-bearing.** Excludes `SESSION_STATUS_*.md`, `MIGRATED_FROM.md`, `tests/`, `CONTRIBUTING.md`, `.env*`, `*.pem`, `identity.json`. Any internal/dev artifact added to this folder must be ignored or never committed.
3. **`SKILL.md` frontmatter `version` must match the `--version` flag passed to `clawhub publish`.** Drift surfaces as moderation oddity.
4. **Default signing scheme is `ed25519+nonce` (v0.3).** Helper supports `--scheme ed25519` for older chapters that don't advertise v0.3 in `/api/version`.
5. **The `helpers/sign_request.py` Ed25519 implementation conforms to `../spec/0.3/signing.md`.** Verified by `../conformance/client/test_canonical_string*.py` with the `openclaw-skill` adapter.
6. **No example queries in tool/verb descriptions.** A leaky example (e.g. "looking for an AI infra cofounder in Boston") gets read by the LLM as in-distribution user intent and grafted onto unrelated prompts. Regex canary in `../member-sdk/tests/test_tool_parity.py`.

## Publish flow

```bash
clawhub delete nanda-chapter --reason "<reason>" --yes        # if cleaning slate
clawhub publish /home/lyra/Nanda_Chapter_Protocol/openclaw-skill \
  --slug nanda-chapter \
  --name "NANDA Chapter Skill" \
  --version <semver> \
  --tags "nanda,federation,ed25519,sovereign-identity,a2a,projectnanda,chapter" \
  --changelog "<short delta>"
clawhub inspect nanda-chapter        # confirm Moderation: CLEAN
openclaw skills install nanda-chapter --force
systemctl --user restart openclaw-gateway
```

## Layout

| Path | Purpose |
| ---- | ------- |
| `SKILL.md` | LLM-facing manifest + verb teaching. Published. |
| `README.md` | Skill consumer overview. Published. |
| `SECURITY.md` | Trust model + reporting. Published (concise version). |
| `helpers/sign_request.py` | Ed25519 signer + identity manager + hash-chained audit. Published. |
| `examples/` | Example conversation flows. Published. |
| `tests/` | E2E verb tests. NOT published (`.clawhubignore`). |
| `CONTRIBUTING.md` | Contributor guide with internal repo refs. NOT published. |
| `.clawhubignore` | Defines what's excluded from the published bundle. |

## Don't

- Don't add `shell.exec`, `fs.any`, `net.arbitrary`, `eval.code` to the capability list. The skill's value is the narrow capability set.
- Don't put any github.com URL in any published file. Use `projectnanda.org` for public references.
- Don't write multi-paragraph docstrings — one short line max.
- Don't create new top-level files in this folder without adding them to `.clawhubignore` if they're internal.
