# Delivery and Response Reference

Reference for the pre-recorded job response shape and asynchronous delivery events.

## Contents

- Response Structure
- Callback Events
- Webhook Events

## Response Structure

```json
{
  "id": "job-uuid",
  "status": "done",
  "result": {
    "transcription": {
      "full_transcript": "Hello, welcome to the meeting...",
      "utterances": [
        {
          "text": "Hello, welcome to the meeting",
          "language": "en",
          "start": 0.5,
          "end": 2.1,
          "speaker": 0,
          "words": [{ "word": "Hello", "start": 0.5, "end": 0.8, "confidence": 0.98 }]
        }
      ]
    },
    "diarization": {},
    "translation": {},
    "summarization": {},
    "sentiment_analysis": {}
  }
}
```

## Callback Events

Callbacks are sent to the `callback_url` in your transcription request body:

- `transcription.success` — job completed successfully
- `transcription.error` — job failed

## Webhook Events

Webhooks are configured in Dashboard -> Account -> Webhooks:

- `transcription.created` — job queued
- `transcription.success` — job completed
- `transcription.error` — job failed

Webhooks are powered by Svix with signed requests for verification.
