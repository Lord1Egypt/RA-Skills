# Test Cases

## API Key Tests

### TC-01: No API Key Configured
```
Input: Generate a cat image
Expected: Return configuration guide
"You have not configured your Novita AI API Key.

Quick setup (copy and run):
mkdir -p ~/.novita && echo '{"api_key": "YOUR_KEY"}' > ~/.novita/config.json

Get Key: https://novita.ai/settings/key-management"
```

### TC-02: Invalid API Key
```
Input: Generate a cat image (with invalid key)
Expected: Return 401 error
"API Key invalid, please check configuration. Get valid Key: https://novita.ai/settings/key-management"
```

### TC-03: Valid API Key
```
Input: Generate a cat image
Expected:
1. Show generation prompt
2. Call /v3/seedream-5.0-lite
3. Return image URL
```

## Text-to-Image Tests

### TC-04: Basic Text-to-Image
```
Input: Generate a blue sky with white clouds landscape
Expected:
1. Call /v3/seedream-5.0-lite
2. Request: {"prompt": "blue sky white clouds landscape"}
3. Return image URL
```

### TC-05: Detailed Prompt
```
Input: Generate a cyberpunk city at night with neon lights
Expected:
1. Call /v3/seedream-5.0-lite
2. Request includes detailed prompt
3. Return image URL
```

### TC-06: Multiple Images
```
Input: Generate 3 different cat images
Expected: Make 3 separate API calls, return 3 URLs
```

## Image Editing Tests

### TC-07: Style Transfer
```
Input: Convert this photo to watercolor style [attached image]
Expected:
1. Call /v3/seedream-5.0-lite
2. Request: {"prompt": "watercolor style", "reference_images": ["image_url"]}
```

### TC-08: Background Replacement
```
Input: Change the background to a beach [attached image]
Expected: Call /v3/seedream-5.0-lite with edit instruction
```

### TC-09: Object Modification
```
Input: Make the sky more dramatic [attached image]
Expected: Call /v3/seedream-5.0-lite with specific edit
```

## Text-to-Video Tests

### TC-10: Basic Text-to-Video
```
Input: Generate a 4-second ocean waves video
Expected:
1. Call /v3/async/vidu-q3-pro-t2v
2. Request: {"prompt": "ocean waves", "duration": 4}
3. Return task_id
4. Poll /v3/async/task-result?task_id=xxx
5. Return video URL
```

### TC-11: Specific Duration
```
Input: Generate an 8-second sunset timelapse
Expected: Request includes "duration": 8
```

### TC-12: Complex Scene
```
Input: Generate a video of rain falling on a city street
Expected:
1. Call /v3/async/vidu-q3-pro-t2v
2. Detailed prompt in request
```

## Image-to-Video Tests

### TC-13: Animate Image
```
Input: Make this landscape move [attached image]
Expected:
1. Call /v3/async/vidu-q3-pro-i2v
2. Request: {"prompt": "animate with gentle motion", "images": ["image_url"]}
```

### TC-14: Specific Motion
```
Input: Add wind blowing effect to this image [attached image]
Expected:
1. Call /v3/async/vidu-q3-pro-i2v
2. Request: {"prompt": "wind blowing leaves and grass", "images": ["image_url"]}
```

## TTS Tests

### TC-15: Basic TTS
```
Input: Convert "Hello world" to speech
Expected:
1. Call /v3/async/minimax-speech-2.8-turbo
2. Request: {"text": "Hello world", "voice_setting": {"voice_id": "male-qn-qingse"}}
3. Return audio URL
```

### TC-16: Female Voice
```
Input: Read "Welcome" with female voice
Expected: Request includes "voice_id": "female-shaonv"
```

### TC-17: Speed Adjustment
```
Input: Read this at 1.5x speed
Expected: Request includes "speed": 1.5
```

### TC-18: Long Text TTS
```
Input: Read a 500-word article
Expected: Execute normally, return complete audio
```

## STT Tests

### TC-19: Basic STT
```
Input: Transcribe this recording [attached audio]
Expected:
1. Call /v3/glm-asr
2. Request: {"file": "audio_url"}
3. Return transcribed text
```

### TC-20: Different Audio Formats
```
Input: Transcribe this MP3/WAV/M4A file
Expected: Handle various audio formats correctly
```

## Error Handling Tests

### TC-21: Insufficient Balance
```
Input: Generate an image (account balance is 0)
Expected: Return 402 error
"Insufficient balance, please top up at https://novita.ai/billing"
```

### TC-22: Rate Limit Exceeded
```
Input: Send many requests in short time
Expected: Return 429 error, suggest waiting
```

### TC-23: Invalid Parameters
```
Input: Generate a 99999-second video
Expected: Return 400 error with parameter guidance
```

## Boundary Tests

### TC-24: Empty Input
```
Input: Generate an image (no description)
Expected: Prompt user to provide description
```

### TC-25: Very Long Text TTS
```
Input: Read a 10000-character article
Expected: Handle correctly or indicate text too long
```

### TC-26: Unsupported File Type
```
Input: Transcribe this video file
Expected: Indicate audio files only are supported
```

## Async Task Tests

### TC-27: Task Status Polling
```
Input: Generate a video
Expected:
1. Submit task returns task_id
2. Polling shows status: TASK_STATUS_QUEUED → TASK_STATUS_PROCESSING → TASK_STATUS_SUCCEED
3. Return video URL on success
```

### TC-28: Task Failure Handling
```
Input: Generate video with invalid content
Expected:
1. Task status becomes TASK_STATUS_FAILED
2. Return failure reason
```

## Combined Task Tests

### TC-29: Image Analysis + Generation
```
Input: Analyze this image and generate similar style [attached image]
Expected:
1. Analyze image content and style
2. Call /v3/seedream-5.0-lite to generate new image
```

### TC-30: Text Summary + TTS
```
Input: Summarize this and convert to audio [attached text]
Expected:
1. Generate summary
2. Call /v3/async/minimax-speech-2.8-turbo with summary
```
