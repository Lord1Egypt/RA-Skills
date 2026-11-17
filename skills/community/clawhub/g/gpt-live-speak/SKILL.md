---
name: speak
description: Speak aloud through a Linux/ALSA audio device using OpenAI GPT-Live. Designed for embodied agents, robots, and other Linux systems with a speaker.
version: 1.0.0
metadata:
  openclaw:
    os:
      - linux
    requires:
      bins:
        - python3
        - aplay
      env:
        - OPENAI_API_KEY
    primaryEnv: OPENAI_API_KEY
    envVars:
      - name: OPENAI_API_KEY
        required: true
        description: OpenAI API key used for GPT-Live speech.
      - name: SPEAK_LIVE_VOICE
        required: false
        description: GPT-Live voice name. Defaults to cedar.
      - name: SPEAK_ALSA_DEVICE
        required: false
        description: ALSA playback device. Defaults to default.
      - name: SPEAK_BUFFER_MS
        required: false
        description: Initial playback buffer in milliseconds. Defaults to 200.
---

# Speak

Use this skill when the user explicitly asks the agent to speak aloud,
say something through its physical body, or when another approved workflow
requires a spoken announcement.

Do not automatically speak every normal chat response.

Run the bundled speech tool using the `exec` tool.

Set:

    SPEAK_TEXT = the message to communicate aloud

Then execute:

    python3 {baseDir}/scripts/run.py "$SPEAK_TEXT"

The tool uses OpenAI GPT-Live and streams PCM audio to ALSA.

The default GPT-Live voice is Cedar. The voice, ALSA device, and playback
buffer can be configured through environment variables.

GPT-Live may naturally paraphrase the supplied commentary slightly.

Keep spoken announcements reasonably concise.

Never speak passwords, API keys, authentication tokens, or other secrets.

If speech fails, report the failure. Do not retry repeatedly without
understanding the cause.
