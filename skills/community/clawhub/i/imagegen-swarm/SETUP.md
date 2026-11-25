# imagegen-swarm setup

This file is in the skill folder. For a plain-folder install, copy or symlink this folder into your agent's skills directory and name the folder `imagegen-swarm`. Typical project paths include `.agents/skills/` (Codex, Cursor, Gemini CLI, and other agents) and `.claude/skills/` (Claude Code).
An older copy installed as `image-gen` can be moved to `imagegen-swarm`. Plugin commands are in the
repository file `docs/install.md`. You need Node.js 18+ and Python 3 with Pillow (`python3 -m pip install pillow`; series mode uses it for its local consistency score)
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
| `$HOME/.config/imagegen-swarm/engine-off/<engine>` | One file named for that engine, optionally containing a short reason | Pause generation for that engine until you remove or move the file; readiness still checks login |
| `$HOME/.config/imagegen-swarm/models/clip-vit-b32-vision-q8.onnx` | Optional CLIP image encoder, only if you download it (below). Read only | Series-mode `clip` consistency score |

| Engine | Install and log in | Login lives in |
|---|---|---|
| codex | Install the Codex CLI (`npm i -g @openai/codex`) or Codex.app, then `codex login`. The script looks for `--codex` / `CODEX_BIN`, then PATH, then the Codex.app binary, and on Windows the Codex `codex.exe` under the user profile | Codex home (`CODEX_HOME`). Generation reads only `generated_images` |
| grok | Install the Grok Build CLI and log in; `grok models` should list models | `~/.grok` |
| gemini | Install the Antigravity CLI (default `~/.local/bin/agy`, or set `AGY_BIN` / `--agy`) and log in; `agy models` should list Gemini models | `~/.gemini` |
| jimeng | Install the pinned Dreamina binary below, reopen the terminal, then `dreamina login` (scan with the Douyin app); `dreamina user_credit` should show your credits. The script looks in `DREAMINA_INSTALL_DIR`, `~/bin`, `~/.local/bin`, then PATH | `~/.dreamina_cli` |
| muse | `python3 -m pip install playwright && python3 -m playwright install chromium`, then `python3 scripts/muse-image.py --login` and sign in to muse.ai. Use the same interpreter as the skill for all commands (`"$PYTHON"` if set). `--list-chats` checks the login. Muse can fall back to system Google Chrome if installed. | `$HOME/.config/imagegen-swarm/muse-browser` |
| lovart | See below | `$HOME/.lovart/env` and, once that directory exists, `$HOME/.lovart/state.json` |

## Muse approvals

The local output parent is created before Muse starts. The cloud directory follows the selected
browser profile. The legacy profile uses `/home/hatch/workspace/image-gen` and other profiles use
`/home/hatch/workspace/imagegen-swarm`. `IMAGE_GEN_MUSE_REMOTE_DIR` can override it with a directory
under `/home/hatch/` using only `[A-Za-z0-9_./-]` and no `..`. Create the cloud directory
first on a new environment or handle the directory approval manually; the script always
refuses directory-creation cards.

Default and `legacy` accept `Allow once` text cards only for the exact output PNG, subject to
the command and metacharacter checks. `IMAGE_GEN_MUSE_APPROVAL=strict` requires a fully decoded
single-image save. See [Muse approvals](references/muse.md).

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

`scripts/lovart.mjs` reads the file as text. It keeps only `LOVART_ACCESS_KEY`,
`LOVART_SECRET_KEY`, and `LOVART_BASE_URL`. Group or other write access is refused. Group or other
read access, such as `644`, produces a warning and suggests `chmod 600`.

### Existing `lv` installations

If you already installed `~/tools/lovart-skill/lv` using the old setup, the skill prefers it.
An explicit `--lv` path takes priority, followed by `LOVART_LV` and the old default path.
New installations can use the bundled client and the credentials above. Generation JSON reports
`auth` as `lv-wrapper` or `shipped-client`.

Run `node scripts/lovart.mjs --query-mode --json` for a free billing check. Generation also
checks billing. Without `--require-free`, a mode or model that spends credits triggers a
warning and generation proceeds with credits. Pass `--require-free` to stop unless the account
is in unlimited mode and the selected model is whitelisted.
The script never switches the billing mode.

The optional `examples/lovart-lv.example.sh` wrapper in the Git checkout runs
`skills/imagegen-swarm/scripts/lovart_agent.py`. If you copy it outside the checkout,
set `LOVART_AGENT_SKILL` to the path of the client in your skill installation.
A successful `query-mode` confirms connectivity and credentials. Check its whitelist before
relying on free generation.

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

## Series consistency (optional CLIP score)

Series mode works without this. With Pillow alone it uses the `structure` score (SSIM, gradient
orientations and palette). That is a coarse layout check and cannot tell two characters drawn in
the same style apart. If you want a check that follows the subject, you can install a CLIP model
yourself. `auto`, the default method, then uses it. The skill never downloads it, and the agent
should not run these commands for you.

| | |
|---|---|
| Model | CLIP ViT-B/32 image encoder, int8 ONNX: `onnx/vision_model_quantized.onnx` from the Hugging Face repository `Xenova/clip-vit-base-patch32` (converted from OpenAI CLIP) |
| License | MIT |
| Download and disk | 89 MB (the fp32 `onnx/vision_model.onnx`, 352 MB, also works and measured about the same) |
| Python packages | `numpy` and `onnxruntime` (CPU), about 130 MB installed together (measured on Linux x86-64) |
| RAM | about 230 MB while one image is scored (fp32: about 640 MB) |
| CPU time | about 0.5 s per scored image, including model load (measured on an 8-core x86 CPU); `structure` takes about 0.1 s |
| Network | only for the download below. Scoring is local |

```bash
python3 -m pip install numpy onnxruntime
mkdir -p "$HOME/.config/imagegen-swarm/models"
curl -L -o "$HOME/.config/imagegen-swarm/models/clip-vit-b32-vision-q8.onnx" \
  https://huggingface.co/Xenova/clip-vit-base-patch32/resolve/main/onnx/vision_model_quantized.onnx
sha256sum "$HOME/.config/imagegen-swarm/models/clip-vit-b32-vision-q8.onnx"
# expect 583fd1110a514667812fee7d684952aaf82a99b959760c8d7dca7e0ab9839299
python3 scripts/imgtool.py backends   # "auto": "clip", and known_model is set
```

Set `IMAGE_GEN_CLIP_MODEL` to use a file in another place. The script checks SHA-256 during
availability checks and before loading. It rejects hashes outside the validated list unless you
explicitly set `IMAGE_GEN_CLIP_ALLOW_UNVERIFIED=yes` for a model you trust. To go back to the Pillow score, delete
the file or pass `--style-method structure`. Measured error rates and the data behind them are in
the repository at `docs/series-consistency-validation.md`.

A paid vision model (one of your image engines, or a multimodal API) as a judge is not built in.
It would likely judge identity better, but each check would cost a request, take tens of seconds,
and send every image to that provider.

## Check

```bash
node scripts/check.mjs
```

`check.mjs` reports `READY` only after that engine's latest smoke passed within 24 hours and its
current login probe succeeds. A successful login probe alone is `LOGGED IN, UNTESTED`. Use
`node scripts/check.mjs --live --engines <list>` to run generation smoke. Omit engines whose
billing you have not confirmed. Jimeng and the paid API are skipped by default. Lovart only
runs by default when the account is unlimited and the default model is on its free whitelist.
