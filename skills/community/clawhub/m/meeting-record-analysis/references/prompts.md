# Prompt Templates

## Transcript Cleaning

```text
You are an assistant that cleans meeting transcripts.

Clean the transcript below:
- remove filler words
- remove repeated phrases
- improve readability
- preserve facts, names, numbers, decisions, and action items

Transcript:
{transcript}

Return only the cleaned transcript text.
```

## Structured Summary

```text
You are an AI assistant that generates meeting minutes.

Analyze the following meeting transcript and return JSON with these fields:
- topic
- discussion_points
- decisions
- action_items
- voice_summary_text

Rules:
- do not fabricate missing facts
- discussion_points should be concise
- decisions should only include confirmed conclusions
- action_items should include owner if mentioned

Transcript:
{transcript}
```
