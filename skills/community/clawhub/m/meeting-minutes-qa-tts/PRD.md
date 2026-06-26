# Meeting Minutes QA TTS PRD

## Goal

Create a parallel skill that extends the summary-audio workflow into a meeting-specific question-answering workflow with local memory.

Keep the original `meeting-minutes-summary-tts` skill unchanged.

## User Outcome

The user provides a meeting note, then asks follow-up questions such as:

- “这次会议为什么要做这个决定？”
- “谁负责这个 action item？”
- “这次会议里提到的某个细节是什么？”

The skill should:

1. Read the meeting note
2. Summarize it with the current conversation model
3. Save meeting text and summary into local memory
4. Ask where the summary mp3 should be saved, then generate it there
5. Answer follow-up questions against that saved context
6. Show the text answer in OpenClaw first
7. Ask where the answer mp3 should be saved, then generate it with SenseAudio
8. Show where the mp3 file was saved

## External Docs

- SenseAudio API key docs: `https://senseaudio.cn/docs/api-key`

## Storage

- Store the latest meeting context in a local JSON file under `memory/latest_meeting.json` by default
- Allow override when needed

## Notes

- The current conversation model handles summarization and question answering.
- SenseAudio handles only TTS.
- The skill should remain local-file-based and simple in v1.
