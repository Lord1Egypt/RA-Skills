# `gui-upload.mjs` usage

Wraps the running PicGo desktop app's local upload server (default `http://127.0.0.1:36677`). Zero dependencies; requires Node ≥ 22. Use it as the **first** upload route — if the app is running, it uploads with no install and no login, reusing the image hosting the user already configured in the GUI.

## When to use it

- The PicGo desktop app might be running and you want to upload without installing/logging into the CLI.
- The script probes `/heartbeat` first, so it's safe to just try it: if the app isn't up it exits `2` and you fall back to the `picgo` CLI.

## Invocation

```bash
# Upload one or more local files (absolute or relative paths)
node scripts/gui-upload.mjs /abs/path/a.png ./b.jpg

# Upload the current clipboard image (only when the user asked for the clipboard)
node scripts/gui-upload.mjs --clipboard

# Target a non-default port
node scripts/gui-upload.mjs --port 36678 ./a.png

# Provide the server auth secret (see below)
node scripts/gui-upload.mjs --secret <value> ./a.png
```

## Output

On success, prints a single-line JSON array to stdout — the same shape as `picgo upload --format json`:

```json
[{"imgUrl":"https://...","fileName":"a.png","type":"github","size":12345}]
```

- `imgUrl` is the hosted URL (this is the field to use).
- `type` is the image hosting that handled it (e.g. `github`, `smms`, `picgo-cloud`) — use it to tell the user which host was used.
- Older PicGo apps may only return `imgUrl`; newer ones include `fileName`/`type`/`size`/`width`/`height`.

## Exit codes

| code | meaning | what to do |
|---|---|---|
| 0 | success | parse the JSON array from stdout |
| 1 | usage error (bad/missing args, file not found) | fix the arguments |
| 2 | GUI server not reachable | fall back to the `picgo` CLI |
| 3 | auth required/failed (server has a secret) | provide a secret, or fall back to the CLI |
| 4 | upload failed (server reached, upload errored) | read stderr; see `error-handling.md` |

Errors go to stderr; the JSON result only ever goes to stdout.

## Auth secret

Most users have no secret set, so no auth is needed. A secret is only required if the user enabled it in the PicGo server settings. Resolution order:

1. `--secret <value>` flag
2. a `.env` file **next to the script** (`scripts/.env`) containing `PICGO_SERVER_SECRET=...` (loaded via Node's built-in `process.loadEnvFile`)
3. the `PICGO_SERVER_SECRET` environment variable

Example `scripts/.env`:

```
PICGO_SERVER_SECRET=your-secret-here
```

> Do **not** commit `scripts/.env` to git — it holds a plaintext secret. Add it to `.gitignore`.

If you hit exit code `3` and don't have the secret, just fall back to the `picgo` CLI route (Step 2/3 in SKILL.md) — it doesn't need the GUI server.
