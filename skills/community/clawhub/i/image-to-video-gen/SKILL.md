---
name: image-to-video-gen
description: Generate video from supplied image using Veo-3.0 async API. Gemini vision analyzes image, Veo creates video via predictLongRunning. All outputs in ~/.openclaw/workspace/tibetanProc/ with yymmddHHMM prefix.
version: 3.0.1
user-invocable: true
category: media
metadata:
  openclaw:
    emoji: 🎥
    requires:
      env: ["GOOGLE_API_KEY"]
      bins: ["python3", "date", "mkdir"]
      packages: ["google-generativeai", "requests"]
---

# Image to Video Generator (v3.0.0 – Working Veo-3.0 REST API)

**Status**: ✅ Tested & Working  
**Last Updated**: 2026-04-11  
**Example**: Golden Tibetan offering → 2.4 MB video in ~60 seconds

---

## What it does

Generates cinematic 5-second video from any image using Google's Veo-3.0:

1. **Gemini Vision** (2.5-flash) analyzes image for motion/scene description
2. **Veo-3.0 predictLongRunning** generates video asynchronously via REST API
3. **Polling loop** monitors operation until video is ready (~60-90 seconds)
4. **Download** saves MP4 to `~/.openclaw/workspace/tibetanProc/` with `yymmddHHMM` prefix

**Key Fix (v3.0.0)**: REST payload must use `bytesBase64Encoded` field (not `data` or `inline_data`)

---

## Inputs

- **Image**: Local path or URL
- **Duration**: 5-10 seconds (optional)
- **Style**: Hint like "cinematic", "ethereal", "smooth" (optional)

---

## Quick Start

```bash
python3 << 'PYEOF'
import os
import sys
import json
import time
import base64
import requests
import google.generativeai as genai
from pathlib import Path
from datetime import datetime

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WORKSPACE = Path.home() / ".openclaw" / "workspace" / "tibetanProc"
WORKSPACE.mkdir(parents=True, exist_ok=True)
TIMESTAMP = datetime.now().strftime("%y%m%d%H%M")

# Step 1: Load image
IMAGE_PATH = WORKSPACE / f"{TIMESTAMP}_input_image.jpg"
if not IMAGE_PATH.exists():
    print("✗ Image not found")
    sys.exit(1)

print(f"✓ Image: {IMAGE_PATH.name}")

# Step 2: Analyze with Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
image_file = genai.upload_file(str(IMAGE_PATH), mime_type="image/jpeg")

prompt = """Analyze for cinematic video: describe subject, setting, lighting, textures, 
suggested camera movements (dolly, pan, orbit, zoom, rack focus)."""

response = model.generate_content([prompt, image_file])
analysis = response.text

prompt_path = WORKSPACE / f"{TIMESTAMP}_prompt.md"
with open(prompt_path, "w") as f:
    f.write(analysis)
print(f"✓ Analysis: {prompt_path.name}")

# Step 3: Create enhanced prompt
enhanced = f"""VIDEO GENERATION PROMPT
Duration: 5 seconds
Quality: High Definition

SCENE ANALYSIS:
{analysis}

MOTION GUIDELINES:
- Smooth, deliberate camera movement
- Enhance visual depth with elegant transitions
- Maintain consistent lighting
- Cinematic color grading
"""

enhanced_path = WORKSPACE / f"{TIMESTAMP}_enhanced_prompt.txt"
with open(enhanced_path, "w") as f:
    f.write(enhanced)
print(f"✓ Enhanced prompt: {enhanced_path.name}")

# Step 4: Call Veo API with CORRECT field names
with open(IMAGE_PATH, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

VEO_URL = f"https://generativelanguage.googleapis.com/v1beta/models/veo-3.0-generate-001:predictLongRunning?key={GOOGLE_API_KEY}"

# ✅ CORRECT PAYLOAD (v3.0.0)
payload = {
    "instances": [{
        "prompt": enhanced,
        "image": {
            "bytesBase64Encoded": image_b64,  # ← CRITICAL: NOT "data" or "inline_data"
            "mimeType": "image/jpeg"
        }
    }]
}

print("\n🎬 Calling Veo API...")
response = requests.post(VEO_URL, json=payload, timeout=60)

if response.status_code not in [200, 202]:
    print(f"✗ API error: {response.json()}")
    sys.exit(1)

result = response.json()
operation_name = result.get("name")
if not operation_name:
    print(f"✗ No operation name")
    sys.exit(1)

print(f"✓ Operation: {operation_name}")

# Step 5: Poll until complete
POLL_URL = f"https://generativelanguage.googleapis.com/v1beta/{operation_name}?key={GOOGLE_API_KEY}"

for attempt in range(1, 121):
    time.sleep(5 if attempt > 1 else 2)
    
    poll_response = requests.get(POLL_URL, timeout=10)
    poll_result = poll_response.json()
    
    if poll_result.get("done"):
        print(f"✓ Complete in {attempt * 5}s")
        
        # Extract video URL
        try:
            video_uri = poll_result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
        except (KeyError, IndexError):
            print(f"✗ No video in response")
            print(json.dumps(poll_result, indent=2)[:500])
            sys.exit(1)
        
        # Step 6: Download video
        print(f"⬇️  Downloading...")
        video_response = requests.get(f"{video_uri}&key={GOOGLE_API_KEY}", timeout=120, stream=True)
        
        if video_response.status_code == 200:
            output_path = WORKSPACE / f"{TIMESTAMP}_video.mp4"
            with open(output_path, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✓ Video: {output_path.name} ({size_mb:.1f} MB)")
            sys.exit(0)
        else:
            print(f"✗ Download failed: {video_response.status_code}")
            sys.exit(1)

print("✗ Timeout")
sys.exit(1)

PYEOF
```

---

## Detailed Workflow

### Step 1: Prepare Image

```bash
WORKSPACE="$HOME/.openclaw/workspace/tibetanProc"
mkdir -p "$WORKSPACE"
TIMESTAMP=$(date +%y%m%d%H%M)
cp ./my_image.jpg "$WORKSPACE/${TIMESTAMP}_input_image.jpg"
```

### Step 2: Analyze with Gemini Vision

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

IMAGE_PATH = Path.home() / ".openclaw" / "workspace" / "tibetanProc" / "2604110411_input_image.jpg"
image_file = genai.upload_file(str(IMAGE_PATH), mime_type="image/jpeg")

analysis_prompt = """Analyze this image for cinematic video generation:
1. Main subject and focal point
2. Setting and environment
3. Lighting direction and mood
4. Materials and textures
5. Suggested camera movements (dolly, pan, orbit, zoom, rack focus)
6. Overall energy and pacing"""

response = model.generate_content([analysis_prompt, image_file])

# Save analysis
with open(WORKSPACE / "2604110411_prompt.md", "w") as f:
    f.write(response.text)
```

### Step 3: Create Enhanced Prompt

```python
# Read analysis
with open(WORKSPACE / "2604110411_prompt.md") as f:
    analysis = f.read()

# Add video instructions
enhanced = f"""VIDEO GENERATION PROMPT
Duration: 5 seconds
Quality: High Definition
Frame Rate: 24fps

SCENE ANALYSIS:
{analysis}

MOTION GUIDELINES:
- Smooth, deliberate camera movement
- Enhance visual depth with elegant transitions
- Maintain consistent lighting throughout
- Cinematic color grading
- Focus on visual storytelling

TECHNICAL SPECS:
- Resolution: 1080p minimum
- Aspect Ratio: 16:9
- Format: MP4 (H.264)
"""

with open(WORKSPACE / "2604110411_enhanced_prompt.txt", "w") as f:
    f.write(enhanced)
```

### Step 4: Call Veo API (THE CRITICAL PART)

```python
import base64
import requests

# Encode image
with open(IMAGE_PATH, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

# Read enhanced prompt
with open(WORKSPACE / "2604110411_enhanced_prompt.txt") as f:
    prompt = f.read()

# ✅ CORRECT PAYLOAD STRUCTURE (v3.0.0)
payload = {
    "instances": [{
        "prompt": prompt,
        "image": {
            "bytesBase64Encoded": image_b64,    # ← KEY: NOT "data" or "inline_data"
            "mimeType": "image/jpeg"            # ← Must be here
        }
    }]
}

VEO_URL = f"https://generativelanguage.googleapis.com/v1beta/models/veo-3.0-generate-001:predictLongRunning?key={GOOGLE_API_KEY}"

response = requests.post(VEO_URL, json=payload, timeout=60)
result = response.json()

if response.status_code in [200, 202]:
    operation_name = result["name"]
    print(f"✓ Operation: {operation_name}")
else:
    print(f"✗ Error: {result}")
    exit(1)
```

### Step 5: Poll Operation Status

```python
import time

POLL_URL = f"https://generativelanguage.googleapis.com/v1beta/{operation_name}?key={GOOGLE_API_KEY}"

for attempt in range(120):  # 10 minutes max
    time.sleep(5)
    
    poll_response = requests.get(POLL_URL, timeout=10)
    poll_result = poll_response.json()
    
    if poll_result.get("done"):
        print(f"✓ Complete in {(attempt + 1) * 5}s")
        
        # Extract video URL from response structure
        video_uri = poll_result["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
        print(f"✓ Video URL: {video_uri}")
        break
    
    progress = poll_result.get("metadata", {}).get("progressPercentage", "?")
    print(f"  Polling ({attempt + 1}/120)... {progress}%")
```

### Step 6: Download Video

```python
# URL needs API key appended
download_url = f"{video_uri}&key={GOOGLE_API_KEY}"

video_response = requests.get(download_url, timeout=120, stream=True)

output_path = WORKSPACE / "2604110411_video.mp4"
with open(output_path, "wb") as f:
    for chunk in video_response.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)

size_mb = output_path.stat().st_size / (1024 * 1024)
print(f"✓ Video downloaded: {output_path} ({size_mb:.1f} MB)")
```

---

## Response Structure

### Initial Response (Step 4)
```json
{
  "name": "models/veo-3.0-generate-001/operations/uiw8bpjdiqbn"
}
```

### Final Response (Step 5 - when done=true)
```json
{
  "name": "models/veo-3.0-generate-001/operations/uiw8bpjdiqbn",
  "done": true,
  "response": {
    "@type": "type.googleapis.com/google.ai.generativelanguage.v1beta.PredictLongRunningResponse",
    "generateVideoResponse": {
      "generatedSamples": [
        {
          "video": {
            "uri": "https://generativelanguage.googleapis.com/v1beta/files/txg4shogthoc:download?alt=media"
          }
        }
      ]
    }
  }
}
```

---

## Output Files

```
~/.openclaw/workspace/tibetanProc/
├── 2604110411_input_image.jpg         # Original image
├── 2604110411_prompt.md               # Gemini analysis
├── 2604110411_enhanced_prompt.txt     # Motion-enhanced prompt
├── 2604110411_veo_init_response.json  # API response (init)
└── 2604110411_video.mp4               # ✅ Final video
```

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `bytesBase64Encoded isn't supported` | Wrong field name | Use `bytesBase64Encoded` (not `data`, `inline_data`, `bytesBase64`) |
| `mimeType isn't supported` | Field name case | Use exact `mimeType` (camelCase, not `mime_type` or `mimeType`) |
| `No struct value found for field expecting an image` | Missing image entirely | Provide both `bytesBase64Encoded` and `mimeType` |
| `Video generation timeout` | Operation takes >10min | Rare; usually completes in 60-90s |
| `403 PERMISSION_DENIED` on download | API key issue | Add `?key={GOOGLE_API_KEY}` to video URL |

---

## Performance

| Operation | Time |
|-----------|------|
| Gemini analysis | ~3s |
| Veo generation | ~50-90s |
| Download | ~2-5s |
| **Total** | **~60-100s** |

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 3.0.0 | 2026-04-11 | ✅ **Working REST API** - Fixed field names: `bytesBase64Encoded` instead of `data` |
| 2.0.0 | 2026-04-11 | Documented async polling (did not work) |
| 1.0.0 | Original | Initial design (gRPC-only, REST broken) |

---

## Testing

Successfully tested with:
- **Image**: Golden Tibetan offering (6.3 MB JPG)
- **Model**: veo-3.0-generate-001
- **Duration**: 5 seconds
- **Output**: 2.4 MB MP4 video
- **Status**: ✅ Working end-to-end
