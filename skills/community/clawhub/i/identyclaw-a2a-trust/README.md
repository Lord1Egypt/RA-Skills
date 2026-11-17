# identyclaw-a2a-trust skill

Reference ClawHub skill for [openclaw#57387](https://github.com/openclaw/openclaw/issues/57387) — trusted inter-agent messaging via IdentyClaw HOLA collaboration envelopes.

Works with:

- **`sessions_send`** — same-gateway fleet messaging
- **`a2a_send_message`** — internet A2A via [`@identyclaw/openclaw-a2a-plugin`](https://github.com/discernible-io/openclaw-a2a-idc-plugin) (P2P RODiT wire JWT only; no mediated login to `api.identyclaw.com`)

## Quick start

```bash
cd identyclaw-a2a-trust-skill
npm install

# HOLA helpers: IdentyClaw API session (identyclaw-tools cache or POST /api/login)
export IDENTYCLAW_JWT=...
export IDENTYCLAW_NEAR_PRIVATE_KEY=ed25519:...
export IDENTYCLAW_TOKEN_ID=yourpassportid

npm run build-message -- \
  --to-token peerpassport \
  --task-type TASK_REQUEST \
  --task-json '{"summary":"Health check node-3"}'
```

Paste stdout into `sessions_send`, or pass to `a2a_send_message` with `--reply-via a2a`.

Verify inbound (HOLA trust decision):

```bash
export IDENTYCLAW_JWT=...
cat inbound-message.txt | npm run verify-message
```

## OpenClaw install (local dev)

```bash
openclaw skills install /path/to/identyclaw-a2a-trust-skill
openclaw plugins install clawhub:@identyclaw/openclaw-identyclaw-plugin
openclaw plugins install clawhub:@identyclaw/openclaw-a2a-plugin
```

| Credential | Used for |
| --- | --- |
| `NEAR_CREDENTIALS_FILE_PATH` | A2A **wire** login (`login_server` → peer `/api/login`) |
| `IDENTYCLAW_JWT` + `IDENTYCLAW_NEAR_PRIVATE_KEY` | HOLA create/verify via identyclaw-tools or CLI scripts |

GitHub issue comment drafts for maintainers live in `internal/openclaw-issue-comments.md` (gitignored, not published).

## License

MIT-0 when published to ClawHub (same as `identyclaw-skill`).
