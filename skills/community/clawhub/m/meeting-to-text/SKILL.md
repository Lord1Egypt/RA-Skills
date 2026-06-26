---
name: meeting-to-text
description: Create a fully local speaker-separated .txt transcript from a meeting recording, meeting screen recording, speech audio, or local video/audio file. Use this whenever the user wants to transcribe a local recording into plain text, generate a meeting transcript, convert audio or video to txt, or explicitly asks to distinguish speakers with default labels like 说话人1, 说话人2, etc. Trigger even if the user only provides an input file path and an output path and says things like "转文字", "做逐字稿", "会议录音转 txt", or "区分发言人".
---

# Meeting To Text

Use this skill when the job is a local file-to-transcript workflow.

Do not use this skill if the user only wants audio extraction, a meeting summary, environment setup, or an explanation of the models.

## Inputs To Collect

Always collect:
- one local source file path
- one output target path

Output target rules:
- If the target ends with `.txt`, write exactly to that file.
- Otherwise treat it as a directory and write `<source-stem>_transcript.txt` inside it.

Supported source types:
- Video: `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`
- Audio: `.wav`, `.mp3`, `.m4a`, `.aac`, `.flac`, `.ogg`

## Runtime

Read [references/runtime_paths.md](references/runtime_paths.md) before running the script.

Run the bundled entrypoint with the local ASR environment:

```powershell
& '<YOUR_CONDA_ENV_PYTHON_PATH>' 'C:\path\to\your\meeting-to-text\scripts\meeting_to_text.py' --input '<SOURCE_PATH>' --output '<OUTPUT_TARGET>'
```

If you need a stable temp location, add:

```powershell
--work-dir '<YOUR_WORKSPACE_TEMP_PATH>'
```

## Result Handling

The script may print library noise before the final machine-readable result.

Always treat the last non-empty stdout line as the JSON result object.

Interpret results this way:
- Exit code `0` with `status: success`: transcript file was created with no warnings.
- Exit code `0` with `status: warning`: transcript file was created, but you must report the warnings and any skipped segments.
- Non-zero exit code or `status: error`: do not claim success; surface the warning list and the intended output path.

Important fields in the final JSON:
- `output_path`: final transcript file path
- `speaker_count`: number of detected `说话人N` labels in the written transcript
- `segment_count`: normalized diarization segments sent into transcription
- `transcribed_segment_count`: segments that produced text
- `skipped_segment_count`: dropped or failed segments
- `failed_segments`: segment-level failures with `start`, `end`, and `reason`
- `warnings`: run-level warnings such as `only one speaker detected`

## Behavior Guarantees

The entrypoint already enforces the workflow. Do not rewrite the pipeline ad hoc in the conversation.

The script will:
- normalize audio with FFmpeg instead of renaming extensions
- use local SenseVoiceSmall for ASR
- use local 3D-Speaker embeddings plus clustering for diarization
- write a plain text transcript with timestamps and `说话人N`
- stop on diarization failure instead of silently emitting a non-speaker-separated transcript

## Report Back To The User

On success, report:
- the final transcript path
- whether the source was audio or video
- the detected speaker count
- any warnings that matter for review

On failure, report:
- the exit code category
- the warning message from the JSON result
- whether the failure happened during validation, media normalization, diarization, transcription, or output writing

## References

Read these only when needed:
- [references/runtime_paths.md](references/runtime_paths.md): fixed local paths and command template
- [references/troubleshooting.md](references/troubleshooting.md): common runtime issues and how to interpret them
