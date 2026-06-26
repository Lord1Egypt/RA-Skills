# Paired: Phone Agent

**Give your AI agent a body. Use the phone in your pocket.**

> *Your assistant can already answer questions. Now it can answer calls, send texts, read your notifications, and speak in your own voice — all through the phone you already own.*

---

## The pitch in one screen

Today, when an AI agent needs to "do something in the real world," it almost always means renting infrastructure:

* A Twilio number to send an SMS
* A Vapi/Bland account to make a phone call
* An ElevenLabs subscription for a voice
* A cloud TTS bill that grows with every notification

You end up with **three monthly subscriptions, a stack of API keys, and a robot voice that isn't yours** — just to do what the phone on your desk already does.

**Paired: Phone Agent** takes the other path. It bridges your OpenClaw agent to your **own** phone over Bluetooth and ADB, and now in v2.0.0 it adds **on-device voice cloning** so the agent speaks with **your** voice. No second SIM. No rented number. No cloud TTS. Your existing phone, your existing number, your existing voice — driven by an agent that knows your context.

---

## What you can actually do

Once installed and paired, your agent gets these commands. They run against the phone in your pocket, on your carrier, with your number on the caller ID.

| Command | What it does | Uses |
|---------|--------------|------|
| `/sms send "Tell mum I will be late"` | Sends a real SMS from your phone | ADB |
| `/sms read` | Pulls your unread texts into the agent context | MAP profile |
| `/call dial 0123...` | Places a real phone call through your carrier | HFP profile |
| `/call answer` | Picks up an incoming call | HFP profile |
| `/say "Hello from your agent"` | Speaks through the phone over BT — generic neural voice | piper |
| `/voice "Hi, this is me"` ⭐ NEW v2.0.0 | Speaks **in your cloned voice** at 48kHz studio quality | VoxCPM2 |
| `/contacts find "John"` | Searches your phone contacts | PBAP profile |
| `/media play / pause / next` | Controls whatever music app is open | AVRCP profile |
| `/file send report.pdf` | Pushes a file to your phone | OBEX |
| `/tether on` | Brings up phone-as-router | PAN/NAP |

Inbound is just as alive — incoming SMS, missed calls, and notifications get bridged to OpenClaw automatically so your agent can react to them in real time.

---

## What is new in v2.0.0

### The agent now sounds like you

Five minutes of you reading six sentences is enough to clone your voice. From that moment on, every voice note your agent sends, every line it speaks over Bluetooth, every reply it dictates back through your phone — all of it goes out in **your** voice.

> The person on the other end of a Telegram voice note hears **you**. Not a stock voice. Not a robot. You.

### Word-level audio splicing

A small but huge detail: voice-cloning models routinely mispronounce unusual names (yours, your spouse, your kids, your dog, your company). Paired solves this by letting you record any specific word once, in your real voice. That clip gets spliced directly into the synthesised output every time the word appears.

**Result: your name is pronounced perfectly, by you, every single time.**

You can have as many splice clips as you like. Family names. Brand names. Place names. Pet names. The agent learns to use them automatically.

### 30 languages, all in your voice

Type in English, Hindi, French, German, Italian, Malay, Spanish, Japanese — and 22 more — the agent speaks them in your cloned voice. Language is detected from input text; no flag needed.

> If you have family abroad, you can now send them voice notes in their language, in your voice, without ever having spoken that language yourself.

### Four-level fallback ladder

The voice path is engineered to not fail.

| Tier | Engine | When it kicks in |
|------|--------|------------------|
| 1 | VoxCPM2 (Apache-2.0) | Cloned voice, 48kHz studio quality |
| 2 | XTTS v2 | Cloned voice, 24kHz, if VoxCPM2 GPU is busy |
| 3 | piper | Generic neural voice, if no cloning service is up |
| 4 | espeak-ng | Robotic last resort, but the reply still ships |

GPU restart? Network blip? Container crash? **The voice note still goes out.**

### Long-form support

The synth wrapper chunks long input at sentence boundaries before calling the cloning engine. Tested up to 2-minute voice notes; scales cleanly to 10+ minutes for dictations, audiobooks, or sermons. Concatenation is seamless — listeners cannot hear the joins.

---

## Why install this skill

### Because you already own the phone

Your phone has a SIM, a carrier, a real number, contacts, message history, a microphone, a speaker, and a screen. Other skills ignore all of that and ask you to pay a third party for a subset of the same features. Paired uses what is already on your desk.

### Because you do not want a robot voice on your behalf

A generic TTS voice on a voice note from "your assistant" is uncanny. A 48kHz clone of **your** voice, with your name pronounced by you, is — strangely — completely natural to the listener. Nobody asks questions.

### Because you care about privacy

Voice reference and splice clips live in `~/.config/paired/voice/`. They are never uploaded. The cloning model runs in a Docker container on your hardware. There is no telemetry, no analytics, no cloud round-trip, and no SaaS account to delete. Pull the plug on the GPU and the voice clone is gone with it.

### Because the agent should reach the world the way you do

Phones are how humans communicate. They have for twenty years. An agent that can only speak inside a chat window is half an agent. Paired gives your agent the same surface area you have — calls, texts, voice notes, notifications, contacts — and then steps out of the way.

---

## Who is this for

* **Home-lab agent builders** running OpenClaw who want a single skill that handles every phone-shaped task
* **Founders and operators** automating personal admin without leaking it into a SaaS pipeline
* **Privacy-first users** who refuse to upload a voice sample to a cloud API
* **Multilingual households** who want one voice across all the languages they speak
* **Researchers** building embodied / agentic phone interactions and tired of stitching ten APIs together
* **Anyone** whose agent should sound like *them*, not like a stock asset

---

## Privacy promises (no asterisks)

- Voice reference, splice clips, contacts, message history — **all stay on your hardware**
- No training data leaves the machine
- Model weights are open-source (Apache-2.0 for VoxCPM2)
- No telemetry, no analytics, no phone-home
- Delete `~/.config/paired/voice/` and you are back to a generic voice; delete `~/.config/paired/` and the skill forgets you entirely

---

## Hardware floor

| Use case | Requirement |
|----------|-------------|
| Full 48kHz cloned voice | NVIDIA GPU with 6GB+ VRAM (modern mid-range card) |
| Cloned voice (24kHz only) | NVIDIA GPU with 4GB VRAM |
| Generic neural voice fallback | CPU only — no GPU required |
| Phone bridge | Android device with ADB-over-Wi-Fi or USB; Bluetooth adapter on host |

There is no minimum subscription. There is no "Pro tier." There is one skill, one license, and your hardware.

---

## Five-minute start

```bash
# 1. Install the skill
clawhub install paired

# 2. Bring up the voice-cloning service
cd skills/paired/skill/engines
docker build -t paired-voxcpm:latest -f voxcpm.Dockerfile .
docker run -d --name paired-voxcpm --gpus all --restart unless-stopped \
  -p 8056:8056 \
  -v ~/.config/paired/voice:/refs \
  paired-voxcpm:latest

# 3. Record your voice (one-time, takes ~5 minutes)
python3 skills/paired/skill/setup/paired-voice-setup.py reference

# 4. (Optional) Record splice clips for tricky words
python3 skills/paired/skill/setup/paired-voice-setup.py word yourname

# 5. Test
python3 skills/paired/skill/voice/paired-voice-synth.py \
  "Hello. This is me speaking through my own agent." /tmp/test.wav
```

That is it. Pair the phone, point the agent at it, and your assistant has a body.

---

## Built on the shoulders of

| Component | License | What it gives us |
|-----------|---------|------------------|
| [OpenBMB/VoxCPM2](https://github.com/OpenBMB/VoxCPM) | Apache-2.0 | 48kHz voice cloning, 30 languages |
| [coqui-tts (idiap fork)](https://github.com/idiap/coqui-ai-TTS) | Apache-2.0 | XTTS v2 fallback engine |
| [rhasspy/piper](https://github.com/rhasspy/piper) | MIT | Generic neural TTS |
| [espeak-ng](https://github.com/espeak-ng/espeak-ng) | GPL-3.0 | Last-resort synth |
| [BlueZ](http://www.bluez.org/) | LGPL-2.1+ | Linux Bluetooth stack |
| [Android Debug Bridge](https://developer.android.com/tools/adb) | Apache-2.0 | Phone control |
| [ffmpeg](https://ffmpeg.org/) | LGPL-2.1+ | Audio plumbing |
| [HuggingFace](https://huggingface.co/) | — | Model hosting |

Every one of these is open source. None of them ask for an API key. Full attribution in [THIRD_PARTY.md](../THIRD_PARTY.md).

Built on the [OpenClaw](https://openclaw.ai) agent framework.

---

## Get started

```bash
clawhub install paired
```

Then read [docs/PAIRING-GUIDE.md](../../docs/PAIRING-GUIDE.md) to pair your phone, and [docs/VOICE-SETUP.md](../docs/VOICE-SETUP.md) to clone your voice.

**Welcome to phone-as-hardware. Welcome to your voice, your number, your agent.**
