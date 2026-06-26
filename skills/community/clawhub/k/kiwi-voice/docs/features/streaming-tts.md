# Streaming TTS & Barge-In

## Streaming TTS

Kiwi doesn't wait for the full LLM response before speaking. Instead, it uses **sentence-aware chunking** to start TTS as soon as the first complete sentence arrives.

### How it Works

1. LLM streams response tokens via WebSocket (`delta` events)
2. Kiwi's sentence chunker accumulates tokens until it detects a sentence boundary (`.`, `!`, `?`, or other punctuation)
3. The completed sentence is immediately sent to the TTS provider
4. Audio playback begins while the LLM is still generating the next sentence
5. Subsequent sentences are queued and played sequentially

This reduces perceived latency significantly — the user hears the first sentence within ~1 second of the LLM starting to respond, regardless of total response length.

### Sentence Chunking

The chunker is language-aware and handles:

- Standard punctuation (`.`, `!`, `?`)
- Abbreviations that shouldn't trigger a split (e.g., "Dr.", "U.S.A.")
- Minimum chunk length to avoid tiny audio fragments
- Maximum chunk length to prevent overly long sentences

## Barge-In

Barge-in lets you interrupt Kiwi mid-sentence by speaking over it.

### How it Works

1. While Kiwi is speaking (TTS playing), the microphone remains passively active
2. If the energy level or VAD detects speech during playback, Kiwi:
    - Immediately stops TTS playback
    - Clears the audio queue
    - Switches back to active listening mode
3. Your new command is processed normally

This creates a natural conversational flow — you don't have to wait for Kiwi to finish a long response before giving a new command.

!!! note
    Barge-in sensitivity is tied to the VAD (Voice Activity Detection) settings. If it triggers too easily, adjust the energy threshold in the audio configuration.
