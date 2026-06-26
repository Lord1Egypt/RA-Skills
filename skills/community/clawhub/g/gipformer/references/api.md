# Gipformer ASR Server API Reference

Base URL: `http://127.0.0.1:8910` (default)

## Endpoints

### GET /health

Health check and server status.

**Response:**

```json
{
  "status": "ok",
  "model": "g-group-ai-lab/gipformer-65M-rnnt",
  "quantize": "int8",
  "uptime_s": 123.45
}
```

### POST /transcribe

Transcribe audio of any length. The server handles VAD chunking, batch inference, and text merging internally.

**Request body:**

```json
{
  "audio_b64": "<base64-encoded audio bytes>",
  "sample_rate": 16000
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `audio_b64` | string | yes | Base64-encoded audio (WAV, FLAC, OGG, MP3, M4A) |
| `sample_rate` | int | no | Sample rate hint, default 16000 |

**Response:**

```json
{
  "transcript": "xin chào thế giới đây là bài phát biểu",
  "duration_s": 45.2,
  "process_time_s": 2.1,
  "chunks": [
    { "text": "xin chào thế giới", "start_s": 0.0, "end_s": 3.5 },
    { "text": "đây là bài phát biểu", "start_s": 3.5, "end_s": 8.2 }
  ]
}
```

| Field | Description |
|-------|-------------|
| `transcript` | Full merged text from all chunks |
| `duration_s` | Total audio duration in seconds |
| `process_time_s` | Server processing time in seconds |
| `chunks` | Per-chunk details with text and time offsets |

## Audio Format

- **WAV** (.wav): Native support via soundfile
- **FLAC** (.flac): Native support via soundfile
- **OGG** (.ogg): Native support via soundfile
- **MP3** (.mp3): Native support via soundfile (libsndfile 1.1+)
- **M4A/AAC** (.m4a): Supported via ffmpeg (must be installed on server)

All formats are automatically converted to WAV 16-bit PCM mono 16kHz.

## Server-side Chunking

Long audio is automatically chunked server-side using Silero VAD:
- VAD detects speech/silence boundaries
- Small segments are merged into chunks up to 20s
- Segments exceeding 30s are hard-cut as a last resort
- Chunks are inferred in batches (max 64 concurrent) via the BatchingEngine

No client-side chunking or text merging is needed.

## Server Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | 127.0.0.1 | Bind address |
| `--port` | 8910 | Bind port |
| `--quantize` | int8 | Model precision: `fp32` or `int8` |
| `--num-threads` | 4 | ONNX inference threads |
| `--decoding-method` | modified_beam_search | `greedy_search` or `modified_beam_search` |
| `--max-batch-size` | 16 | Max requests batched together |
| `--max-wait-ms` | 100 | Max wait before flushing a partial batch |

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Invalid audio data (decode failed) |
| 422 | Malformed request body |
| 500 | Internal server error |
