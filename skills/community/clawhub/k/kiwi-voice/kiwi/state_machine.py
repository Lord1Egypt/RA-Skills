#!/usr/bin/env python3
"""Dialogue state definitions for Kiwi Voice."""


class DialogueState:
    """Dialogue states - state machine for process control."""
    IDLE = "idle"           # Waiting for wake word
    LISTENING = "listening" # Listening for command
    PROCESSING = "processing" # Checking completeness/intent (LLM busy)
    THINKING = "thinking"   # Waiting for OpenClaw response
    SPEAKING = "speaking"   # TTS playback
