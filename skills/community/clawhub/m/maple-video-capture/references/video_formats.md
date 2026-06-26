# Video Formats Supported

## Supported Input Formats

The video frame capture skill supports the following video formats:

- **MP4** (.mp4) - Most common video format
- **MKV** (.mkv) - Matroska video container
- **MOV** (.mov) - QuickTime video format
- **AVI** (.avi) - Audio Video Interleave
- **FLV** (.flv) - Flash Video
- **WMV** (.wmv) - Windows Media Video
- **WebM** (.webm) - WebM video format
- **M4V** (.m4v) - MPEG-4 video format

## Technical Details

### Frame Extraction Method

The script uses OpenCV's VideoCapture to extract frames at specified time intervals:

1. Opens the video file using `cv2.VideoCapture`
2. Calculates video duration from frame count and FPS
3. Seeks to specific timestamps using `CAP_PROP_POS_MSEC`
4. Captures and saves frames at regular intervals

### Similarity Detection

When `--skip-similar-frames` is enabled:

1. Resizes frames to 320x180 for comparison
2. Converts to grayscale
3. Calculates absolute difference between frames
4. Computes similarity score (1.0 - mean_diff/255.0)
5. Skips frames with similarity above threshold

### Output Naming Convention

Format: `video_name_hhmmss_index.jpg`

Example: `meeting_00h01m30s_0003.jpg`

- `video_name`: Original video file name without extension
- `hhmmss`: Timestamp in hours:minutes:seconds format
- `index`: Sequential capture number (4 digits, zero-padded)

## Dependencies

Required Python packages:
- `opencv-python-headless` - Video processing and frame extraction
- `numpy` - Array operations (installed with OpenCV)

Install with: `pip install -r requirements.txt`
