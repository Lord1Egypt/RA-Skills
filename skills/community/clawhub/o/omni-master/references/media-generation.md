# Media Generation & Editing

## Image Generation

### Available Tools
- **openai-image-gen** — OpenAI DALL-E batch generation
- **nano-banana-pro** — Gemini 3 Pro image gen/edit
- Web APIs via browser for other generators

### Workflow
1. Craft detailed prompt (subject, style, composition, lighting)
2. Generate with appropriate tool
3. Iterate on prompt for refinement
4. Save to workspace

### Prompt Engineering
- Be specific: "A golden retriever puppy on a beach at sunset, warm light, shallow depth of field, Canon 85mm"
- Include: subject, setting, style, mood, technical details
- Negative prompts for what to avoid

## Video Processing

### Tools
- **ffmpeg** — Swiss army knife for video
- **video-frames** skill — Frame extraction
- **browser** — Screen recording, YouTube

### Common Operations
```bash
# Extract frames
ffmpeg -i video.mp4 -vf fps=1 frame_%04d.png

# Trim video
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy output.mp4

# Convert format
ffmpeg -i input.mov output.mp4

# Extract audio
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# Create GIF
ffmpeg -i video.mp4 -vf "fps=10,scale=320:-1" output.gif
```

## Audio Processing
- **ffmpeg** for conversion, trimming, mixing
- **songsee** for spectrograms and visualization
- **whisper** / **whisper-api** for transcription
- **sag** / **sherpa-onnx-tts** for text-to-speech

## Screen Capture
- **browser screenshot** — Web page captures
- **peekaboo** — macOS UI automation
- **camsnap** — RTSP/ONVIF camera frames

## Image Editing (CLI)
```bash
# ImageMagick
convert input.png -resize 50% output.png
convert input.png -crop 200x200+10+10 output.png
convert *.png -append panorama.png
```
