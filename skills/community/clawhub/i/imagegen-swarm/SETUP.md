# imagegen-swarm setup

This file is in the skill folder. For a plain-folder install, copy or symlink this folder to the
Claude Code skills directory, or the Codex skills directory, and name the folder `imagegen-swarm`.
An older copy installed as `image-gen` can be moved to `imagegen-swarm`. Plugin commands are in the
repository README. You need Node.js 18+ and Python 3 with Pillow (`python3 -m pip install pillow`; series mode uses it to score palette similarity)
on macOS, Windows or Linux; on Windows the scripts call `python`, or set `PYTHON`. The Muse engine
also needs Playwright. The skill contains no accounts or keys. Each engine keeps its login in its
own folder, so never bundle those folders when you share the skill. Set up only the engines you
want.

These are prerequisites for you to run. The agent runs the scripts in this folder and does not
download or execute installers. If a step below is not done, the agent should ask you to do it. The
`mkdir` commands in this file are first-time setup. Run each one only when you set up that engine.
Generation does not create these directories.

## What setup stores

| Path | What | Why |
|---|---|---|
| Codex home, file `auth.json` | Login created by `codex login`. The readiness check only tests that the file exists | Know whether Codex is logged in |
| Codex home, directory `generated_images` | Images Codex already wrote. This skill lists and hashes that directory only | Reject an older image reused after a failed call |
| `~/.grok` | Grok CLI login | Grok image and video |
| `~/.gemini` | Antigravity CLI login | Gemini image |
| `~/.dreamina_cli` | Dreamina CLI login | Jimeng image and video |
| `$HOME/.config/imagegen-swarm/muse-browser` | Playwright profile directory. Created by `scripts/muse-image.py --login` only | Stay signed in to Muse. Generation does not create it |
| `$HOME/.lovart/env` | `LOVART_ACCESS_KEY`, `LOVART_SECRET_KEY`, optional `LOVART_BASE_URL`. Mode 600. Read as text, not executed | Sign Lovart requests. Other lines in this file are ignored |
| `$HOME/.lovart/state.json` | Project and thread ids. Updated only when `$HOME/.lovart` already exists. Setup does not create this file | Resume a Lovart project |
| `$HOME/.config/imagegen-swarm/api.json` | Provider, model, estimated price, budgets. No API key | Paid last resort. This is the only file the paid setup command below creates |
| `$HOME/.config/imagegen-swarm/api-key` | API key, mode 600, only if you choose a key file | Paid last resort. Read at request time |
| `$HOME/.config/imagegen-swarm/api-spend.jsonl` | One JSON line per attempt with confirmed returned image bytes | Compare the batch reservation with the monthly cap |
| `$HOME/.config/imagegen-swarm/engine-off/<engine>` | One empty file named for that engine | Pause that engine until you delete the file |

| Engine | Install and log in | Login lives in |
|---|---|---|
| codex | Install the Codex CLI (`npm i -g @openai/codex`) or Codex.app, then `codex login`. The script looks for `--codex` / `CODEX_BIN`, then PATH, then the Codex.app binary, and on Windows the Codex `codex.exe` under the user profile | Codex home (`CODEX_HOME`). Generation reads only `generated_images` |
| grok | Install the Grok Build CLI and log in; `grok models` should list models | `~/.grok` |
| gemini | Install the Antigravity CLI (default `~/.local/bin/agy`, or set `AGY_BIN` / `--agy`) and log in; `agy models` should list Gemini models | `~/.gemini` |
| jimeng | Install the pinned Dreamina binary below, reopen the terminal, then `dreamina login` (scan with the Douyin app); `dreamina user_credit` should show your credits. The script looks in `DREAMINA_INSTALL_DIR`, `~/bin`, `~/.local/bin`, then PATH | `~/.dreamina_cli` |
| muse | `pip install playwright && playwright install chromium`, then `python3 scripts/muse-image.py --login` and sign in to muse.ai in the window that opens; afterwards `--list-chats` should list your side chats | `$HOME/.config/imagegen-swarm/muse-browser` |
| lovart | See below | `$HOME/.lovart/env` and, once that directory exists, `$HOME/.lovart/state.json` |

## Muse approvals

The local output parent is created before Muse starts. The approval policy permits only
"Allow once" for exactly one decoded image-save operation with one path matching this run's
cloud output after `~`, `.`/`..`, and existing symlink resolution. Creating a cloud directory is
not auto-approved. Extra operations, paths or arguments, commands, reads and network requests
are refused; permission is never inferred from descriptive text.

No captured card currently verifies Muse's operation/path layout. All live approval cards
therefore fail closed: the job stops with an error saying the shape was not recognized and was
not clicked. This can stop otherwise legitimate saves. Jobs that require no approval continue
as before. A verified decoder needs a real captured card before auto-approval can resume; do not
work around this by matching keywords. See [references/muse.md](references/muse.md).

## Jimeng binary

The Dreamina CLI is a binary you install yourself. Publisher `version.json` reports version
**1.4.22** (release date 2026-10-28). The download names are not versioned, so the sha256 is the
pin. If the checksum does not match, stop and do not install the file.

| Platform | File | sha256 |
|---|---|---|
| macOS Intel | `dreamina_cli_darwin_amd64` | `df195a76cfc23263b44663186f5136240aec935e2e019da071c4e5b2e1f067ff` |
| macOS Apple silicon | `dreamina_cli_darwin_arm64` | `85ba083d85e3a37a40edaac482ec832b9e6e8372e35c9e41159ce49b57a5fcb6` |
| Linux x64 | `dreamina_cli_linux_amd64` | `d831fd5f6820ddbd8afcc39afaf0194cd63b17f780057dcc6c486bc7e152d7b6` |
| Linux arm64 | `dreamina_cli_linux_arm64` | `55d086f054464e79f4099e50ce6c51d5e920ccfb59a24a154f4cfc4f8565c378` |
| Windows x64 | `dreamina_cli_windows_amd64.exe` | `27f92ce763035af10e41b31f4c161e8349d40e5fdaa90c5fa98e7869da5d492d` |

Base URL:
`https://lf3-static.bytednsdoc.com/obj/eden-cn/psj_hupthlyk/ljhwZthlaukjlkulzlp/dreamina_cli_beta/`

Download one file, then compare the checksum. On macOS or Linux, `sha256sum` (or `shasum -a 256`)
must print the hash in the table. Move the file to `~/.local/bin/dreamina` and mark it executable.
On Windows, move `dreamina_cli_windows_amd64.exe` to `%USERPROFILE%\bin\dreamina.exe`. Reopen the
terminal, run `dreamina login`, then `dreamina user_credit`.

## Lovart

The Lovart client is already in this folder. `scripts/lovart_agent.py` is the command entry.
`scripts/lovart_client.py` is the HTTP client and `scripts/lovart_state.py` is the local project
list. Together they are the readable v1.1.1 client from
[lovartai/lovart-skill](https://github.com/lovartai/lovart-skill/releases/tag/v1.1.1) (zip sha256
`d96eae1b382ba81829733f2c63e8520b0b7fae9acb77f0df23ad95ca3cdac0cd`), split so each file can be
reviewed. `scripts/lovart.mjs` runs the entry file. You do not need another copy.

On lovart.ai open the avatar menu → "OpenClaw for Lovart" → Create API Key → Copy. The entry is not
under account settings, and the secret key is shown only once. Store it in a credentials file, never
in chat or git:

Run this only the first time you set up Lovart. It stores the two keys in the file
`$HOME/.lovart/env` and sets that file to mode 600. The parent directory exists only so this
file has a place to live. `chmod 600` restricts the credential file to its owner so other local
users cannot read the API keys. Do not run it again on later generations.

```bash
umask 077
mkdir -p -- "$HOME/.lovart"
cat > "$HOME/.lovart/env" <<'EOF'
export LOVART_ACCESS_KEY="ak_your_key"
export LOVART_SECRET_KEY="sk_your_key"
EOF
chmod 600 "$HOME/.lovart/env"
```

`scripts/lovart.mjs` reads that file as text and checks that its mode is owner-only. It keeps only
`LOVART_ACCESS_KEY`, `LOVART_SECRET_KEY`, and `LOVART_BASE_URL`. It does not execute the file. A
mode such as `644` is refused; `600` is accepted. If the mode cannot be read, the client still runs,
so a real API error such as no credits is not replaced by a permissions failure. The optional
wrapper applies the same rule with `stat -c` on Linux and `stat -f` on macOS, and it also copies
only those three names. It does not source the file.

An optional wrapper is `examples/lovart-lv.example.sh` in the git repository (it is not part of the installed skill). It runs `scripts/lovart_agent.py`. If you
copy the wrapper out of this folder, set `LOVART_AGENT_SKILL` to the copy of
`scripts/lovart_agent.py` inside the skill. Check the key with the shipped client:

```bash
python3 scripts/lovart_agent.py query-mode
```

`query-mode` returning JSON means the client and the key work. It does not prove the account has
credits.

## Pay-per-image API line (optional)

Optional. Off until this file exists and `api` is in the batch's engine list. You pay
`price_per_image` USD for every charged image, including discarded images, and the line stops before `budget_per_batch` or
`budget_per_month`. For one image, the paid line starts only when it can take that image and either
the job sets `"engine": "api"` or no enabled subscription engine can take it. A subscription engine
can take an image when it is in the batch's engine list, is not shut down, has not already tried
the image, the job does not name a different engine, and the image's ratio, reference count, and
video fit it. Exhausted quota, no login, and no install shut an engine down. The paid line does not
tail-steal, and it does not take an image a subscription engine can still take. Creating this file
is your consent to that spend. The agent must ask you before it creates this file, changes the
budgets, or generates paid images you did not ask for.

Create a pay-as-you-go API key with your provider (OpenAI Platform or Google AI Studio), then save
the config in `$HOME/.config/imagegen-swarm/api.json`. Run the directory step only the first time.

Each started paid attempt reserves one image against both caps. A returned image keeps that
reservation even if style screening, aspect checks, duplicate checks, or a lost steal race discard
it. Only known uncharged failures release reservations; unknown failures keep their slot for this
batch. API failures before a provider request and provider HTTP error responses report
`charged: false`. A down/rate-limit rejection without an image also releases the slot.
The API script records only confirmed returned image bytes in `api-spend.jsonl`, before local
validation. Attempt IDs deduplicate those charges. The batch parent never writes unknown
outcomes to the ledger, so they do not consume future batches' month budget. Redos and retries check both budgets
again. If no subscription engine can take the job and another paid image would exceed either
cap, the job fails as "stopped by the paid budget". The summary and `out/batch-results.json`
include confirmed charged images in `paid.images` / `paid.usd`, unknown attempts with retained
reservations in `paid.uncertain` (0 when none), confirmed charged attempts without a kept image
in `paid.discarded`, and the number of blocked jobs in `paid.stopped_by_budget`. Blocked failed
results also carry `stopped_by_budget: true`.

The budgets below cap the estimated spend (`price_per_image` times images), not the provider invoice:

```bash
umask 077
mkdir -p -- "$HOME/.config/imagegen-swarm"
cat > "$HOME/.config/imagegen-swarm/api.json" <<'EOF'
{
  "provider": "openai",
  "model": "gpt-image-2",
  "quality": "medium",
  "price_per_image": 0.05,
  "budget_per_batch": 1,
  "budget_per_month": 10,
  "lanes": 4
}
EOF
```

| Field | Meaning |
|---|---|
| `provider` | `openai` or `gemini` |
| `model` | openai e.g. `gpt-image-2`, `gpt-image-1.5`; gemini e.g. `gemini-nano-banana-2.1`, `gemini-3-pro-image` |
| `price_per_image` | estimated USD per image from your provider's price list for your quality and size; used for budgets and the ledger |
| `budget_per_batch` / `budget_per_month` | most USD one batch or one calendar month may spend; the line stops before going over |
| `quality` | openai only, default `medium` (`low` is cheaper, but gpt-image-2 at low shows blocky artifacts) |
| `image_size` | gemini only: `1K` (default), `2K`, `4K` |
| `base_url` | optional, an OpenAI-compatible gateway |
| `key_env` / `key_file` | which environment variable holds the key (default `OPENAI_API_KEY` / `GEMINI_API_KEY`), or a file with mode 600 |
| `lanes` | lane count, default 4 |
| `ratios` / `max_refs` | optional overrides when your model supports different ratios or reference counts than the built-in table |

To keep the key in a file, `chmod 600` restricts it to its owner so other local users cannot read
the API key:

```bash
umask 077 && printf '%s' 'your-key' > "$HOME/.config/imagegen-swarm/api-key" && chmod 600 "$HOME/.config/imagegen-swarm/api-key"
```

Then add `"key_file": "$HOME/.config/imagegen-swarm/api-key"` to `api.json`. The spend ledger is
the file `$HOME/.config/imagegen-swarm/api-spend.jsonl`, one line per attempt with confirmed returned image bytes, including discarded images. Unknown failures never append a row.

## Check

```bash
node scripts/check.mjs
```
