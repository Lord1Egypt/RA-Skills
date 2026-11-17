---
name: loudkit-voice
description: Set up free, open-source Loudkit voice notes for an existing agent and messenger. Use to check compatibility, run the companion on an Apple Silicon Mac, and configure Hermes, OpenClaw or another agent without replacing its session. The companion is a developer preview.
license: MIT-0
metadata:
  version: "0.1.1"
---

# Loudkit voice notes — developer preview

Help the user speak to the agent they already use and receive a spoken reply in
the same chat. Loudkit supplies speech synthesis; the free, open-source
[Loudkit Voice companion](https://github.com/loudreader/loudkit-voice) adds
Parakeet transcription and connection options. Its service and command are
currently called LoudTalk. Installing this skill adds setup instructions;
running the companion and downloading models are separate setup steps.

Read the current [agent setup guide](https://loudkit.loudreader.io/agents/llms.txt)
before configuring a connection. It is the authoritative source for provider
examples, tested revisions and preview availability. The
[product page](https://loudkit.loudreader.io/agents/) has voice samples and the
human explanation. If the guide is unavailable, give a compatibility assessment
from the constraints below; do not guess release-specific configuration fields.

## Assess the existing setup

Identify the agent and installed version, messenger, agent host, and whether an
ordinary text conversation already works. Inspect available local information
first; ask only for missing facts. Determine whether the companion is already
running or needs to be cloned from its public repository. An installed Loudkit
SDK alone is not the voice-note companion.

The current companion requires an **Apple Silicon Mac, Python 3.12–3.13, `uv`
and FFmpeg**. Allow about 3 GB for models and keep at least 20 GB of disk free during
setup. Check these on the intended speech host with read-only commands such as
`uname -sm`, the intended Python interpreter's `--version`, `command -v uv`,
`command -v ffmpeg` and `df -h`. A different current agent host can still be assessed, but needs a
deliberately configured authenticated connection to the Mac; its own
`127.0.0.1` does not point to the user's Mac.

The source is available without a signup, subscription or access request. If
the intended speech host lacks a requirement, report that concrete blocker and
continue any useful compatibility assessment. `pip install loudkit` installs
the speech SDK, not LoudTalk. The user's agent or messenger provider may have
its own costs. Do not open a public issue on the user's behalf unless asked.

## Choose the connection

| Existing agent | Preferred route | Verified scope |
| --- | --- | --- |
| Hermes or OpenClaw | Use its existing gateway and configure speech providers | Pinned upstream speech-provider code tested with real local speech models; full gateway and real messenger delivery still need validation |
| Codex | Local CLI voice pipeline | Real local agent round trip; messenger transport mocked |
| Grok Bot | Agent-managed local inbox | Experimental; actual Grok Bot execution not validated |
| Muse Code | CLI or MCP adapter | Configuration recipe; runtime validation pending |
| Other agent | Its supported CLI/API adapter or an active agent-managed inbox | Assess the actual interface; no blanket compatibility claim |

Keep the existing agent's sessions, memory, tools, model credentials, messenger
connection and approval rules. A generic model API is not a connection to that
agent's existing session. An MCP inbox needs an active agent to read and reply;
it does not wake a stopped agent. This skill does not expose a hosted MCP server.

## Run the companion and configure speech

Install missing prerequisites on the intended speech host within the user's
setup request. With Homebrew, `brew install uv ffmpeg` supplies those two tools.
Clone and run the companion:

```sh
git clone https://github.com/loudreader/loudkit-voice.git
cd loudkit-voice
./start.command
```

The launcher installs locked dependencies, including Discord support, then opens
`http://127.0.0.1:8765`. Prepare the speech models in that local setup page. A
separate Loudkit checkout is not required. For updates and command-line options,
use the [source README](https://github.com/loudreader/loudkit-voice#readme).

For Hermes and OpenClaw, read the current official
[Hermes voice documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode)
or [OpenClaw audio](https://docs.openclaw.ai/nodes/audio) and
[TTS configuration](https://docs.openclaw.ai/tools/tts/configuration) for the
installed release, then merge only the required speech fields from the Loudkit
guide into the active profile.

The preview speech API defaults to `http://127.0.0.1:8765/v1`, with transcription
model `parakeet`, speech model `loudkit` and English voice `sophie`. The local SDK
placeholder `loudtalk-local` belongs to speech configuration only; it must not
replace the agent's conversation-model credentials. Preserve a recoverable copy
of any configuration you change. Use the existing gateway as the sole receiver
of its bot's messages; do not start another Telegram poller with the same token.

Optional standalone messenger bridges are protocol-tested, not verified on real
accounts: Telegram, Discord, WhatsApp **Business Cloud API**, Slack and
BlueBubbles/iMessage. WhatsApp does not provide a personal-account QR login;
Slack uses audio attachments. Select a bridge only when it fits the user's
existing agent and requested messenger. Keep credentials in local configuration,
not chat or public issues, and preserve the agent's enabled tools and permissions.

## Verify the actual journey

First confirm an ordinary text response. Generate a short sample and transcribe
a clear recording locally, then send a harmless voice note such as “Tell me a
short joke” through the user's messenger. Confirm that the reply arrives in the
same chat and plays. If it fails, isolate transcription, agent dispatch, speech
synthesis and message delivery; avoid repeated account or configuration changes
without a new diagnosis.

Report the exact agent version, messenger and observed result. Distinguish
compatibility assessed, locally verified speech, and a verified messenger round
trip. Speech runs locally after model download; the agent and messenger may
still use online services.
