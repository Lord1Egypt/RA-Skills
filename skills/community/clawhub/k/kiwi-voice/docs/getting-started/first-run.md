# First Run

## Start Kiwi

=== "Linux / macOS"

    ```bash
    source venv/bin/activate
    python -m kiwi
    ```

=== "Windows (PowerShell)"

    ```powershell
    .\start.ps1
    # or
    .\venv\Scripts\activate
    python -m kiwi
    ```

=== "Windows (Git Bash)"

    ```bash
    source venv/Scripts/activate
    python -m kiwi
    ```

You should see startup logs like:

```
[14:08:25.342] [INFO] [CORE] Kiwi Voice starting...
[14:08:25.500] [INFO] [STT] Loading Faster Whisper (small, cuda)...
[14:08:26.100] [INFO] [TTS] Kokoro ONNX initialized (14 voices)
[14:08:26.200] [INFO] [API] Dashboard at http://localhost:7789
[14:08:26.300] [INFO] [CORE] Listening...
```

## Open the Dashboard

Navigate to [http://localhost:7789](http://localhost:7789) in your browser. You'll see the real-time dashboard with live status, event log, controls, and more.

<figure markdown>
  ![Kiwi Voice Dashboard](../assets/dashboard.png){ .screenshot loading=lazy }
</figure>

## Register Your Voice

Say the wake word followed by the registration command:

> **"Kiwi, remember my voice"**

Kiwi will capture your voiceprint and register you as the **Owner** — the highest priority level with full access.

!!! important
    Register your voice first. Until you do, all speakers are treated as guests and may need Telegram approval for certain commands.

## Try a Command

Once registered, try:

> **"Kiwi, what time is it?"**

The flow:

1. Wake word "kiwi" is detected (text fuzzy match or ML model)
2. Your speech is transcribed by Faster Whisper
3. Speaker ID confirms you're the Owner
4. Command is sent to OpenClaw via WebSocket
5. LLM response streams back
6. TTS speaks the answer

## Use the Web Microphone

If you don't have a local microphone (or don't want to install pyaudio), click the microphone button in the dashboard to talk to Kiwi directly from the browser.

## What's Next

- [Wake Word Detection](../features/wake-word.md) — switch to ML-based detection
- [TTS Providers](../features/tts-providers.md) — choose your preferred voice engine
- [Voice Security](../features/voice-security.md) — set up Telegram approvals
- [Home Assistant](../features/home-assistant.md) — control your smart home by voice
