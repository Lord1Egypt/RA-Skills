# hudl-model-switch

An OpenClaw skill for switching between 29 LLM models on the [Huddle01 GRU gateway](https://gru.huddle01.io).

## What it does

Lets you switch your OpenClaw agent's model by just asking in chat:

- "switch to opus"
- "use grok"
- "go back to minimax"
- "use deepseek r1"
- "switch to gemini pro"
- "what model am I on?"

The skill validates your GRU gateway config, edits your OpenClaw config, and restarts the agent automatically.

## Requirements

- OpenClaw with a `hudl` provider configured pointing at `https://gru.huddle01.io`
- A valid GRU gateway API key
- `jq` installed on the system

## Install

```bash
# Clone into your OpenClaw skills directory
git clone https://github.com/huddle01/openclaw-skills.git
cp -r openclaw-skills/hudl-model-switch ~/.openclaw/skills/hudl-model-switch

# Or if using clawhub
clawhub install hudl-model-switch
```


## Paste this prompt to install

### OpenClaw prompt (fun mode)

```text
Yo OpenClaw, let's do a clean install party for `hudl-model-switch` 🚀🤖

Please install and verify this skill end-to-end with zero chaos.

Do exactly this:
1) Check if ClawHub CLI exists:
   `command -v clawhub >/dev/null 2>&1`
2) If not installed, install it:
   `npm i -g clawhub`
3) Install from ClawHub:
   `clawhub install hudl-model-switch`
4) Verify the skill directory exists at `~/.openclaw/skills/hudl-model-switch`
5) Verify required files exist:
   - `~/.openclaw/skills/hudl-model-switch/SKILL.md`
   - `~/.openclaw/skills/hudl-model-switch/scripts/validate.sh`
   - `~/.openclaw/skills/hudl-model-switch/references/models.md`
6) Ensure `validate.sh` is executable; if not, run:
   `chmod +x ~/.openclaw/skills/hudl-model-switch/scripts/validate.sh`
7) Run:
   `bash ~/.openclaw/skills/hudl-model-switch/scripts/validate.sh`
   - If it fails, show the exact error and stop.
8) Before restart, tell me:
   - gateway is restarting now
   - it can take a couple of minutes to come back online
   - you will confirm the applied model changes as soon as it's back
9) Restart OpenClaw:
   `openclaw restart`
10) Confirm completion as soon as it is back with:
   - installed path ✅
   - validation result ✅
   - current active model from the detected OpenClaw config (`~/.openclaw/config.json` or `~/.openclaw/openclaw.json`) (`model.primary`) ✅

Constraints:
- Do not modify unrelated files.
- Do not edit provider base URLs or API keys.
- If a command fails, report the failing command + stderr and stop.
```

### Generic prompt (GitHub fallback)

```text
Install `hudl-model-switch` from GitHub and verify it for OpenClaw.

Steps:
1) Create skills directory:
   `mkdir -p ~/.openclaw/skills`
2) Clone repo to temp folder:
   `tmp_dir="$(mktemp -d)" && git clone https://github.com/huddle01/openclaw-skills.git "$tmp_dir/openclaw-skills"`
3) Replace skill folder:
   `rm -rf ~/.openclaw/skills/hudl-model-switch`
   `cp -R "$tmp_dir/openclaw-skills/hudl-model-switch" ~/.openclaw/skills/hudl-model-switch`
4) Ensure script is executable:
   `chmod +x ~/.openclaw/skills/hudl-model-switch/scripts/validate.sh`
5) Run validation:
   `bash ~/.openclaw/skills/hudl-model-switch/scripts/validate.sh`
   - If validation fails, print exact error and stop.
6) Before restart, tell me gateway restart may take a couple of minutes and that you'll confirm changes once it's back.
7) Restart:
   `openclaw restart`
8) Report immediately after gateway is back:
   - install path
   - validation output
   - active `model.primary` in detected OpenClaw config (`~/.openclaw/config.json` or `~/.openclaw/openclaw.json`)

Constraints:
- Do not edit unrelated files.
- Do not change provider URLs or API keys.
- Stop immediately on command errors and show stderr.
```

## Supported models (29)

| Provider | Models |
|---|---|
| OpenAI | gpt-5.4, gpt-5.4-pro, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, o3, o4-mini, gpt-4o-mini |
| Anthropic | claude-opus-4.6, claude-sonnet-4.6, claude-sonnet-4.5, claude-haiku-4.5, claude-sonnet-4 |
| Google | gemini-3.1-pro, gemini-3.1-flash-lite, gemini-2.5-pro, gemini-2.5-flash |
| DeepSeek | deepseek-v3.2, deepseek-r1 |
| xAI | grok-4.1-fast, grok-3-mini |
| Qwen | qwen3-235b, qwen-2.5-coder-32b |
| MiniMax | minimax-m2.5 |
| Moonshot | kimi-k2.5 |
| Meta | llama-4-maverick, llama-3.3-70b |
| Mistral | mistral-large, codestral |

All models are automatically prefixed with `hudl/` in the config.

## Structure

```
hudl-model-switch/
├── SKILL.md              # Main skill instructions
├── scripts/
│   └── validate.sh       # Checks hudl provider config before any switch
│   └── switch-model.sh   # Deterministically updates active/default model values
├── references/
│   └── models.md         # Full model catalog with aliases
└── README.md
```

## How it works

1. User says "switch to opus"
2. Skill runs `validate.sh` to confirm `hudl` provider with `gru.huddle01.io` exists
3. Maps "opus" to `hudl/claude-opus-4.6` using the model catalog
4. Runs `scripts/switch-model.sh` (not manual edits), which updates:
   - `agents.list[*].model.primary` for the active agent
   - `agents.defaults.model.primary` for consistency
5. Runs `openclaw restart`

If the hudl provider isn't configured, the skill refuses to proceed and tells the user what's missing.
`models.providers.hudl.models` is only a catalog list and does not determine the active model.
