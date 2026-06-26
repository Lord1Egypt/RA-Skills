# Python SDK

Patterns and details specific to the `gladiaio-sdk` package.

## Contents

- Package Info
- Sync vs Async (including async live session)
- Client Method Aliases
- Typed Request Objects (dataclass-style and dict alternative)
- File Input Types
- Session ID Access
- Error Types
- Event Handling (pyee EventEmitter pattern)
- Streaming Audio from File
- Streaming from Microphone (PyAudio)
- Response Access
- Package Structure (exports)

## Package Info

- **PyPI**: [gladiaio-sdk](https://pypi.org/project/gladiaio-sdk/)
- **Version**: 1.0.2 (auto-synced by CI — see [sdk-versions.md](./sdk-versions.md))
- **Runtime**: Python 3.10+
- **Dependencies**: httpx, websockets, pyee

## Sync vs Async

The Python SDK provides both synchronous and asynchronous clients:

```python
from gladiaio_sdk import GladiaClient

client = GladiaClient(api_key="YOUR_KEY")

# Sync
result = client.prerecorded().transcribe("audio.mp3", options)

# Async
result = await client.prerecorded_async().transcribe("audio.mp3", options)
```

### Async live session

```python
import asyncio
from gladiaio_sdk import GladiaClient, LiveV2InitRequest, LiveV2LanguageConfig

async def main():
    client = GladiaClient(api_key="YOUR_KEY")
    live_client = client.live_async()
    session_done = asyncio.Event()

    session = live_client.start_session(
        LiveV2InitRequest(
            model="solaria-1",
            encoding="wav/pcm",
            sample_rate=16000,
            bit_depth=16,
            channels=1,
            language_config=LiveV2LanguageConfig(languages=["en"]),
        )
    )

    @session.once("ended")
    def on_ended(msg):
        session_done.set()

    session.send_audio(audio_bytes)
    session.stop_recording()
    await session_done.wait()

asyncio.run(main())
```

## Client Method Aliases

| Primary                      | Aliases                                             |
| ---------------------------- | --------------------------------------------------- |
| `client.prerecorded()`       | `client.pre_recorded()`, `client.pre_recorded_v2()` |
| `client.prerecorded_async()` | `client.pre_recorded_async()`                       |
| `client.live()`              | `client.live_v2()`                                  |
| `client.live_async()`        | `client.live_v2_async()`                            |

## Typed Request Objects

Python uses dataclass-style request objects for type safety:

```python
from gladiaio_sdk import (
    LiveV2InitRequest,
    LiveV2LanguageConfig,
    LiveV2MessagesConfig,
    LiveV2PreProcessing,
    LiveV2RealtimeProcessing,
    LiveV2PostProcessing,
)

request = LiveV2InitRequest(
    model="solaria-1",
    encoding="wav/pcm",
    sample_rate=16000,
    bit_depth=16,
    channels=1,
    language_config=LiveV2LanguageConfig(
        languages=["en", "fr"],
        code_switching=True,
    ),
    messages_config=LiveV2MessagesConfig(
        receive_partial_transcripts=True,
        receive_speech_events=True,
    ),
    pre_processing=LiveV2PreProcessing(
        audio_enhancer=True,
    ),
)
```

### Dict alternative

You can also pass plain dicts for pre-recorded options:

```python
result = client.prerecorded().transcribe(
    "audio.mp3",
    {
        "language_config": {"languages": ["en"]},
        "diarization": True,
        "translation": True,
        "translation_config": {"target_languages": ["fr"]},
    },
)
```

## File Input Types

```python
from pathlib import Path

# String path
result = client.prerecorded().transcribe("audio.mp3", options)

# Path object
result = client.prerecorded().transcribe(Path("audio.mp3"), options)

# URL (no upload needed)
result = client.prerecorded().transcribe("https://example.com/audio.mp3", options)

# Binary file object
with open("audio.mp3", "rb") as f:
    result = client.prerecorded().transcribe(f, options)
```

## Session ID Access

```python
# Sync: available after 'started' event fires
@session.once("started")
def on_started(response):
    print(f"Session ID: {response.id}")
    # Also: session.session_id

# Async: use await
session_id = await session.get_session_id()
```

## Error Types

```python
from gladiaio_sdk import GladiaClient

try:
    result = client.prerecorded().transcribe("audio.mp3", options)
except Exception as e:
    # HttpError for HTTP failures (401, 429, 500, etc.)
    # TimeoutError for timeout
    print(f"Error: {type(e).__name__}: {e}")
```

## Event Handling

Uses `pyee` (EventEmitter pattern):

```python
from gladiaio_sdk import LiveV2WebSocketMessage, LiveV2InitResponse, LiveV2EndedMessage

@session.on("message")
def on_message(message: LiveV2WebSocketMessage):
    if message.type == "transcript":
        if message.data.is_final:
            print(f"Final: {message.data.utterance.text}")

@session.once("started")
def on_started(response: LiveV2InitResponse):
    print(f"Session {response.id} started")

@session.on("error")
def on_error(error: Exception):
    print(f"Error: {error}")

@session.once("ended")
def on_ended(ended: LiveV2EndedMessage):
    print("Session ended")
```

## Streaming Audio from File

```python
import time

CHUNK_SIZE = 3200  # 100ms of 16-bit mono at 16kHz

with open("audio.pcm", "rb") as f:
    while chunk := f.read(CHUNK_SIZE):
        session.send_audio(chunk)
        time.sleep(0.1)  # Real-time pacing

session.stop_recording()
```

## Streaming from Microphone

Using PyAudio:

```python
import pyaudio

RATE = 16000
CHUNK = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

try:
    while True:
        data = stream.read(CHUNK)
        session.send_audio(data)
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    session.stop_recording()
```

## Response Access

Pre-recorded responses use attribute access:

```python
result = client.prerecorded().transcribe("audio.mp3", options)

# Access nested fields
print(result.status)                                    # "done"
print(result.result.transcription.full_transcript)      # Full text
for utterance in result.result.transcription.utterances:
    print(f"[{utterance.start}-{utterance.end}] {utterance.text}")
```

## Package Structure

All public types are exported from the top-level `gladiaio_sdk` module:

```python
from gladiaio_sdk import (
    GladiaClient,
    # Pre-recorded
    PreRecordedV2Response,
    # Live
    LiveV2InitRequest,
    LiveV2InitResponse,
    LiveV2EndedMessage,
    LiveV2WebSocketMessage,
    LiveV2LanguageConfig,
    LiveV2MessagesConfig,
    LiveV2PreProcessing,
    LiveV2RealtimeProcessing,
    LiveV2PostProcessing,
)
```
