---
name: meeting-minutes-qa-tts
description: Read meeting minutes, produce a short summary with the current conversation model, save the meeting text and summary into local memory, answer follow-up questions about that same meeting in the current conversation model, and generate spoken audio for both the initial summary and later answers with the SenseAudio TTS API. Use when the user wants to ask detailed follow-up questions about one meeting note after it has been read and remembered, and wants both a text answer and an mp3 answer. If no meeting source is available, ask for a local file path or URL first. Before asking the user for a SenseAudio API key, first check whether `SENSEAUDIO_API_KEY` is already configured in the environment and use it directly when present. Before any audio generation, ask the user where the mp3 should be saved.
---

# Meeting Minutes QA TTS

Use this skill to read one meeting note, summarize it, save it to local memory, answer follow-up questions about that meeting, and convert both the initial summary and later answers into local audio files.

## Trigger Rules

Use this skill when:

- The user wants to read one meeting note, save it for follow-up questions, and hear the summary as audio.
- The user wants both a text answer and an audio answer for a meeting-related question.
- The user wants the meeting note remembered for follow-up questions in the same workflow.

Do not use this skill when:

- The user only wants a one-shot summary audio without later Q and A.
- The user wants general knowledge unrelated to the meeting text.
- The user wants speech recognition from audio or video.

## Workflow

1. Look for one of these inputs in the conversation:
   - direct meeting text
   - a local text file path
   - a readable URL
2. If none is available, ask for the meeting text or a local file path or URL first.
3. First check whether `SENSEAUDIO_API_KEY` is configured in the environment and use it directly when present.
4. If `SENSEAUDIO_API_KEY` is not configured, ask the user for a SenseAudio API key and point them to `https://senseaudio.cn/docs/api-key`.
5. Before generating the initial summary audio, ask the user where the mp3 file should be saved.
6. Read the meeting text from the provided source.
7. Summarize the meeting text in the current conversation model with a short spoken-style Chinese summary.
8. Use `scripts/create_meeting_summary_audio_session.py` to save the source location, meeting text, and summary into local memory and generate the summary mp3 at the requested path.
9. When the user asks a follow-up question, answer using the saved meeting text and summary in the current conversation model.
10. Output the text answer first in OpenClaw.
11. Before generating the answer audio, ask the user where the answer mp3 file should be saved.
12. Use `scripts/create_meeting_answer_audio.py` to convert the final answer text into an mp3.
13. After the text answer, explicitly tell the user where the generated audio file was saved.

## Rules

- Keep the meeting memory local to this skill directory unless the user asks for a different path.
- Prefer an in-memory or local-JSON flow; do not require a database.
- Output the text answer first, then the generated audio file location.
- Ask for an output path before generating any mp3.
- Use the current conversation model for summarization and question answering.
- Use SenseAudio only for TTS.
- Accept a user-provided output path and write the mp3 there when requested.
- Standardize the environment variable name as `SENSEAUDIO_API_KEY` for all Python skill calls.
- Prefer `SENSEAUDIO_API_KEY` automatically, and only ask the user for the API key when it is not available.

## Resource

- Memory helper: `scripts/meeting_memory.py` relative to this skill directory
- Memory saver: `scripts/save_meeting_memory.py` relative to this skill directory
- Summary session creator: `scripts/create_meeting_summary_audio_session.py` relative to this skill directory
- Answer audio creator: `scripts/create_meeting_answer_audio.py` relative to this skill directory
- Answer-to-audio script: `scripts/answer_meeting_question_audio.py` relative to this skill directory
- Summary-to-TTS script: `scripts/generate_summary_audio.py` relative to this skill directory
- Product brief: `PRD.md` relative to this skill directory
