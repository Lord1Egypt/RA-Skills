# Usage Examples

## Progress Prompt Template

When executing generation tasks, display to user:

```
Generating, please wait...
Task type: [task type]
Model: [model name]
Estimated cost: ~$[amount]
```

After completion:
```
Generation complete!
Actual cost: $[amount]
[Result URL or file]
```

---

## Text-to-Image

### 1. Generate Landscape

```
User: Generate a sunset beach landscape image

Prompt:
Generating, please wait...
Task type: Text-to-Image
Model: Seedream 5.0 Lite
Estimated cost: ~$0.035

Execute: POST /v3/seedream-5.0-lite
Request: {"prompt": "A beautiful sunset over the ocean with golden light reflecting on calm waves"}
```

### 2. Generate Character Illustration

```
User: Draw a girl in blue dress standing under cherry blossom trees

Prompt:
Generating, please wait...
Task type: Text-to-Image
Model: Seedream 5.0 Lite
Estimated cost: ~$0.035

Execute: POST /v3/seedream-5.0-lite
Request: {"prompt": "A girl in blue dress standing under cherry blossom trees, anime style"}
```

### 3. Generate Product Image

```
User: Generate a sleek smartphone on marble surface

Execute: POST /v3/seedream-5.0-lite
Request: {"prompt": "Modern smartphone on white marble surface, professional product photography, soft lighting"}
```

## Image Editing

### 4. Style Transfer

```
User: Convert this photo to oil painting style [attached image]

Prompt:
Generating, please wait...
Task type: Image Editing
Model: Seedream 5.0 Lite
Estimated cost: ~$0.035

Execute: POST /v3/seedream-5.0-lite
Request: {"prompt": "Convert to oil painting style", "reference_images": ["image_url"]}
```

### 5. Background Change

```
User: Change the image background to a beach [attached image]

Execute: POST /v3/seedream-5.0-lite
Request: {"prompt": "Replace background with tropical beach scene", "reference_images": ["image_url"]}
```

## Text-to-Video

### 6. Generate Nature Video

```
User: Generate a video of a stream flowing through a forest

Prompt:
Generating, please wait...
Task type: Text-to-Video
Model: Vidu Q3 Pro
Estimated cost: ~$0.07-0.28 (4 seconds)

Execute: POST /v3/async/vidu-q3-pro-t2v
Request: {"prompt": "A gentle stream flowing through a peaceful forest with sunlight filtering through trees", "duration": 4}
Returns: {"task_id": "xxx"}
Query: /v3/async/task-result?task_id=xxx
```

### 7. Generate Urban Scene

```
User: Generate a timelapse of city traffic at night

Execute: POST /v3/async/vidu-q3-pro-t2v
Request: {"prompt": "Night city traffic timelapse, car lights creating light trails, urban skyline", "duration": 4}
```

## Image-to-Video

### 8. Animate Landscape

```
User: Make this landscape photo come alive [attached image]

Prompt:
Generating, please wait...
Task type: Image-to-Video
Model: Vidu Q3 Pro
Estimated cost: ~$0.07-0.28

Execute: POST /v3/async/vidu-q3-pro-i2v
Request: {"prompt": "Gentle breeze moving clouds and swaying grass", "images": ["image_url"]}
```

### 9. Animate Portrait

```
User: Add subtle motion to this portrait [attached image]

Execute: POST /v3/async/vidu-q3-pro-i2v
Request: {"prompt": "Subtle head movement, blinking eyes, natural breathing", "images": ["image_url"]}
```

## TTS - Text to Speech

### 10. Basic TTS

```
User: Convert this text to speech: Hello world

Prompt:
Generating, please wait...
Task type: TTS
Model: MiniMax Speech 2.8 Turbo
Estimated cost: ~$0.001

Execute: POST /v3/async/minimax-speech-2.8-turbo
Request: {
  "text": "Hello world",
  "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0},
  "audio_setting": {"format": "mp3"}
}
```

### 11. Female Voice

```
User: Read this with a female voice: Welcome to our platform

Execute: POST /v3/async/minimax-speech-2.8-turbo
Request: {
  "text": "Welcome to our platform",
  "voice_setting": {"voice_id": "female-shaonv"}
}
```

### 12. Adjust Speed

```
User: Read this slowly: Artificial intelligence is changing the world

Execute: POST /v3/async/minimax-speech-2.8-turbo
Request: {
  "text": "Artificial intelligence is changing the world",
  "voice_setting": {"voice_id": "male-qn-qingse", "speed": 0.8}
}
```

## STT - Speech to Text

### 13. Audio Transcription

```
User: Transcribe this recording [attached audio]

Execute: POST /v3/glm-asr
Request: {"file": "audio_url"}
```

### 14. Meeting Notes

```
User: Convert this meeting recording to text [attached audio]

Execute: POST /v3/glm-asr
Request: {"file": "audio_url"}
```

## Combined Tasks

### 15. Image Analysis + New Image

```
User: Analyze this image and generate a similar style one [attached image]

Execute:
1. Analyze image style and content
2. POST /v3/seedream-5.0-lite with derived prompt
```

### 16. Text to Speech Summary

```
User: Summarize this article and convert to audio [attached text]

Execute:
1. Summarize the text
2. POST /v3/async/minimax-speech-2.8-turbo with summary
```
