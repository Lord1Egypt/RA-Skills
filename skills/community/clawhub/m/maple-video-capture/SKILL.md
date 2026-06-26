---
name: video-frame-capture
description: Capture key frames from video files at fixed time intervals. Use when you need to understand video content by extracting screenshots, or when you need to analyze video frames for content recognition. Supports skipping similar frames to avoid redundant captures.
---

# Video Frame Capture

## Overview

This skill enables capturing key frames from video files at fixed time intervals. It's designed to help you understand video content by extracting screenshots for analysis or content recognition.

## When to Use This Skill

Use this skill when:
- You need to understand video content by extracting key frames
- You want to analyze video frames for content recognition
- You need to create a visual summary of a video
- You want to skip similar frames to avoid redundant captures

## Quick Start

Capture frames from a video at 10-second intervals:

```powershell
python scripts/video_frame_capture.py --input "D:\videos\meeting.mp4" --output-dir "D:\frames\meeting" --interval-seconds 10
```

## Parameters

- `--input`: Path to the local video file (required)
- `--output-dir`: Directory where captured frames will be stored (required)
- `--interval-seconds`: Capture interval in seconds, must be greater than 0 (required)
- `--skip-similar-frames`: Skip frames that are similar to the previous saved frame
- `--similarity-threshold`: Similarity threshold in range 0-1, defaults to 0.70
- `--image-extension`: Image format for saved frames, defaults to jpg

## Output Naming

Output files follow the format: `视频文件原始名称_视频时间轴_第几次截取.jpg`

Example: `meeting_00h01m30s_0003.jpg`

## Similar Frame Skipping

When `--skip-similar-frames` is enabled, the script compares the current candidate frame with the previous saved frame:

- Similarity > threshold: Frame is skipped
- Similarity ≤ threshold: Frame is saved and becomes the new comparison baseline

## Examples

### Basic frame capture
```powershell
python scripts/video_frame_capture.py --input "D:\videos\meeting.mp4" --output-dir "D:\frames\meeting" --interval-seconds 10
```

### Skip similar frames
```powershell
python scripts/video_frame_capture.py --input "D:\videos\meeting.mp4" --output-dir "D:\frames\meeting" --interval-seconds 10 --skip-similar-frames
```

### Custom similarity threshold
```powershell
python scripts/video_frame_capture.py --input "D:\videos\meeting.mp4" --output-dir "D:\frames\meeting" --interval-seconds 10 --skip-similar-frames --similarity-threshold 0.80
```

## Resources

### scripts/
- `video_frame_capture.py`: Main script for capturing video frames

### references/
- `video_formats.md`: Supported video formats and technical details

---

**Note:** This skill requires OpenCV (opencv-python-headless) to be installed. Install dependencies with: `pip install -r requirements.txt`
