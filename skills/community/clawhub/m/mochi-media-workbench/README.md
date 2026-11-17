# Audio and Video Workbench

[Simplified Chinese guide](README.zh-CN.md)

Inspect media, extract audio, cut clips and frames, and export SRT/VTT subtitles locally, with optional local speech recognition and resumable chunk caches.

## Features

Inspect media, extract audio, cut clips and frames, and export SRT/VTT subtitles locally, with optional local speech recognition and resumable chunk caches.

## Usage examples

After installation, send any example below to your AI. Include the files or URLs it refers to.

```text
Inspect my uploaded video and list duration, resolution, audio/video codecs and file size.
```

```text
Save seconds 12 through 35 of this video as a new clip and extract two preview frames.
```

```text
Extract this video's audio track and turn my timestamped text into SRT and VTT subtitles.
```

Processes files locally and exports clips, previews, subtitles and manifests. Optional transcription needs a local model download on first use; no MochiLab backend or transcription API key.

## Requirements

Python 3.10+, FFmpeg (or imageio-ffmpeg 0.6+), PyAV 14–16, Pillow 12+; optional faster-whisper 1.2+ for local transcription

## Installation and first use

### MochiLab Skills assistant (recommended)

[Set up and connect the assistant](https://mochilab.bz/Skills/Connect.aspx?lang=en), then send:

```text
Install mochi-media-workbench
```

### ClawHub

[Open the Skill page](https://clawhub.ai/hznetnewpower/skills/mochi-media-workbench), or run from the active agent workspace:

```text
npx clawhub@latest install @hznetnewpower/mochi-media-workbench
```

### GitHub

[Open the source folder](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-media-workbench). Download the repository ZIP and copy `skills/mochi-media-workbench` into the active agent workspace's `skills/` directory.

Start a new conversation after installation.

## Detailed operation contract

Read [SKILL.md](SKILL.md) for the exact workflow, commands, permission boundaries and supporting references. Use the active agent workspace and verify actual outputs.
