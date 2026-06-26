# Runtime Paths

## Fixed Local Paths

- Project root: `D:\APP\meeting to text`
- Python environment: `D:\APP\meeting to text\envs\asr\Scripts\python.exe`
- Skill entrypoint: `D:\APP\meeting to text\skills\meeting-to-text\scripts\meeting_to_text.py`
- FFmpeg: `D:\APP\meeting to text\tools\ffmpeg\bin\ffmpeg.exe`
- SenseVoice model: `D:\APP\meeting to text\models\SenseVoiceSmall`
- VAD model: `D:\APP\meeting to text\models\fsmn-vad`
- 3D-Speaker repo: `D:\APP\meeting to text\repos\3D-Speaker`
- 3D-Speaker cached models: `D:\APP\meeting to text\models\3d-speaker\hub`
- Suggested workspace: `D:\APP\meeting to text\meeting-to-text-skill-workspace`

## Command Template

```powershell
& 'D:\APP\meeting to text\envs\asr\Scripts\python.exe' 'D:\APP\meeting to text\skills\meeting-to-text\scripts\meeting_to_text.py' --input '<SOURCE_PATH>' --output '<OUTPUT_TARGET>'
```

Optional temp dir:

```powershell
& 'D:\APP\meeting to text\envs\asr\Scripts\python.exe' 'D:\APP\meeting to text\skills\meeting-to-text\scripts\meeting_to_text.py' --input '<SOURCE_PATH>' --output '<OUTPUT_TARGET>' --work-dir 'D:\APP\meeting to text\meeting-to-text-skill-workspace\temp'
```

## Output Convention

- If `--output` ends with `.txt`, the transcript is written exactly there.
- Otherwise `--output` is treated as a directory and the script writes `<source-stem>_transcript.txt`.
- Transcript blocks use this format:

```text
[00:00:12 - 00:00:26] 说话人1：今天先同步一下上周的测试结果。
```

## Parsing Result JSON

The script may print library messages before the final result.

Always read the last non-empty stdout line as JSON.
