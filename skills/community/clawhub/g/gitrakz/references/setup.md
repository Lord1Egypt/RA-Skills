# gitrakz — setup

gitrakz ships as a single Docker image (`psyb0t/gitrakz`) with the Svelte UI
embedded. There are two ways to run it: the installer + `gitrakz` wrapper
(recommended), or Docker directly.

## Auth model — GH_TOKEN, injected at runtime

gitrakz shells out to the GitHub CLI (`gh`) inside the container and
authenticates with a `GH_TOKEN` environment variable. **The token is never
written to `.env` or any config file.** The wrapper captures it live with
`gh auth token`; a direct run expects it in the environment. So the host needs
`gh` installed and authenticated (`gh auth login`) — a system-wide (root)
install installs `gh` for you if it is missing, while a per-user install expects
it already present.

`GH_TOKEN` is distinct from `GITRAKZ_AUTH_TOKEN`, which is an optional bearer
token protecting gitrakz's own `/api` (see Configuration).

## Install (recommended)

**Download the installer and read it before running it — never pipe `curl`
straight into a shell.** Confirm it only fetches the pinned image, writes the
config files listed below, and installs the `gitrakz` command — then run it.

```bash
# 1. Download (do not pipe curl into a shell).
curl -fsSL https://raw.githubusercontent.com/psyb0t/gitrakz/main/install.sh -o gitrakz-install.sh

# 2. Inspect — read the whole thing.
less gitrakz-install.sh

# 3a. Per-user install (no root): command -> ~/.local/bin, config ->
#     ~/.config/gitrakz, just for the current user. Expects `gh` already present.
bash gitrakz-install.sh

# 3b. Or system-wide: command -> /usr/local/bin, config -> /etc/gitrakz
#     (root-owned, readable by the `docker` group so any docker-group user
#     drives the one shared stack). This mode also installs `gh` if missing.
sudo bash gitrakz-install.sh --system
```

The mode auto-detects from who runs it (root → system-wide, otherwise
per-user); force it with `--user` or `--system`. Either way the installer:

- pins the stack to the latest **release tag** — never `:latest` on the user's
  machine;
- writes `<config>/docker-compose.yml`, refreshes the visible
  `<config>/.env.example`, and creates the owner-only (`0600`) `<config>/.env`
  from that template only when it is missing — `~/.config/gitrakz` per-user,
  `/etc/gitrakz` system-wide;
- installs the `gitrakz` command (`~/.local/bin` per-user, `/usr/local/bin`
  system-wide);
- pulls the pinned image;
- prints the exact `PATH` one-liner (bash + zsh) when a per-user install finds
  `~/.local/bin` off `PATH`.

Then:

```bash
gh auth login      # once (a per-user install expects gh already installed)
gitrakz start      # tracks your own activity by default
```

### Wrapper commands

```
gitrakz setup      # refresh compose + .env.example; create .env only if missing
gitrakz start      # inject GH_TOKEN from `gh auth token`, pull, and start
gitrakz stop       # stop the stack
gitrakz status     # container state
gitrakz logs [...] # docker compose logs (e.g. gitrakz logs -f)
gitrakz upgrade    # snapshot data, re-pin to the latest release, then pull it
gitrakz restore ~/.config/gitrakz/backups/<timestamp>.tar.gz
gitrakz uninstall  # stop, remove the command, ask before deleting your data
```

- `gitrakz start --rolling` / `gitrakz upgrade --rolling` use the moving
  `:latest` image (built from `main`) for that one invocation only — the pinned
  release in `.env` is left untouched. Use it to try unreleased changes.
- `upgrade` snapshots the named data volume under `<config>/backups/` as
  `YYYYMMDDHHMMSS.tar.gz`, keeps the newest three, and deletes the previous
  pinned image on success so images do not pile up. `restore <backup.tar.gz>`
  validates the archive, asks before replacing the volume, saves a fresh current
  snapshot, and leaves the stack stopped for an explicit `gitrakz start`.
  `uninstall` only deletes `~/.config/gitrakz` and the data volume if you say yes.

## Run it with Docker directly

The wrapper is just a guardrail around Docker. Pass the token through — it is the
only auth gitrakz needs. Pin a released tag (not `:latest`) for a reproducible
run:

```bash
docker run --rm -p 8080:8080 \
  -e GH_TOKEN="$(gh auth token)" \
  -v gitrakz-data:/data \
  psyb0t/gitrakz:vX.Y.Z run
```

Add any `-e GITRAKZ_*` from the table below. Or run the installer's compose file
directly:

```bash
export GH_TOKEN="$(gh auth token)"
docker compose --project-directory ~/.config/gitrakz \
  --env-file ~/.config/gitrakz/.env -f ~/.config/gitrakz/docker-compose.yml up -d
```

## Configuration — edit ~/.config/gitrakz/.env

All configuration is environment variables. Edit `~/.config/gitrakz/.env` and re-run
`gitrakz start`. The installer and `gitrakz setup` refresh the adjacent
`.env.example` for newly introduced settings without replacing `.env`. Everything
has a sane default.

| Variable | Default | What it does |
|---|---|---|
| `GITRAKZ_IMAGE` | *(pinned by installer)* | Image + tag the stack runs. `upgrade` re-pins it. |
| `GITRAKZ_PUBLISH_ADDR` | `127.0.0.1` | Host interface the container's 8080 is published on. Set `0.0.0.0` to expose it (front it with a proxy). |
| `GITRAKZ_PUBLISH_PORT` | `8080` | Host port to publish on. |
| `GITRAKZ_GH_USER` | *(gh login)* | User whose activity is tracked. Empty = the `gh` authenticated login (track yourself). |
| `GITRAKZ_AUTH_TOKEN` | *(empty)* | When set, `/api` requires `Authorization: Bearer <token>`. Empty = open. |
| `GITRAKZ_SYNC_SINCE` | `2025-01-01` | Earliest activity to pull on a first sync. |
| `GITRAKZ_SYNC_INTERVAL` | `30m` | Background incremental-sync cadence. |
| `GITRAKZ_SESSION_GAP` | `30m` | Idle gap that starts a new work session. |
| `GITRAKZ_SESSION_LEADIN` | `25m` | Padding before a session's first event. |
| `GITRAKZ_ELELEM_TYPE` | `openai` | LLM provider — `openai` (or any OpenAI-compatible endpoint) or `anthropic`. |
| `GITRAKZ_ELELEM_BASE_URL` | *(empty)* | LLM API host. Leave empty to keep everything deterministic. |
| `GITRAKZ_ELELEM_MODEL` | *(empty)* | LLM model name. |
| `GITRAKZ_ELELEM_API_KEY` | *(empty)* | LLM API key. |

The LLM (`GITRAKZ_ELELEM_*`) is **optional** — it only powers the `describe-work`
transform, `text` prose blocks, and "generate a template with AI". Leave it
empty and every deterministic feature still works. gitrakz does not manage LLM
provider signup; supply your own key from OpenAI / Anthropic / a compatible host.

`GITRAKZ_DB_PATH` is fixed to `/data/gitrakz.db` on the named `gitrakz-data`
volume by the compose file — no need to set it.
