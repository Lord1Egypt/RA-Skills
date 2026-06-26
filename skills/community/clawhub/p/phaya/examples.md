# Phaya API — Usage Examples

Set these before running any example:

```bash
export PHAYA_API_KEY="your_api_key_here"
export PHAYA_BASE="https://your-api-host/api/v1"
```

---

## Helper: Poll Until Done

**Python** (reusable across all examples):

```python
import httpx, time

def poll(base: str, path: str, job_id: str, headers: dict,
         result_field: str = "video_url", interval: int = 4,
         terminal_ok: str = "completed", terminal_ok_upper: str = "COMPLETED"):
    """Poll a job until completed or failed. Returns the final status dict."""
    url = f"{base}/{path}/{job_id}"
    while True:
        r = httpx.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        status = data.get("status", "")
        print(f"  [{status}]")
        if status in (terminal_ok, terminal_ok_upper, "COMPLETED", "completed"):
            return data
        if status in ("failed", "FAILED", "cancelled"):
            raise RuntimeError(f"Job {job_id} {status}: {data}")
        time.sleep(interval)
```

---

## 1. Check Credits

**Python:**
```python
import httpx, os

BASE = os.environ["PHAYA_BASE"]
HEADERS = {"Authorization": f"Bearer {os.environ['PHAYA_API_KEY']}"}

r = httpx.get(f"{BASE}/user/credits", headers=HEADERS)
data = r.json()
print(f"Credits: {data['credits_balance_formatted']}")
```

**curl:**
```bash
curl -s "$PHAYA_BASE/user/credits" \
  -H "Authorization: Bearer $PHAYA_API_KEY" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['credits_balance_formatted'])"
```

---

## 2. Text-to-Image

**curl:**
```bash
JOB=$(curl -s -X POST "$PHAYA_BASE/text-to-image/generate" \
  -H "Authorization: Bearer $PHAYA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A neon-lit Tokyo street at night, cinematic","aspect_ratio":"16:9"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB"

while true; do
  DATA=$(curl -s "$PHAYA_BASE/text-to-image/status/$JOB" \
    -H "Authorization: Bearer $PHAYA_API_KEY")
  S=$(echo $DATA | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $S"
  [ "$S" = "COMPLETED" ] && echo $DATA | python3 -c "import sys,json; print(json.load(sys.stdin)['image_url'])" && break
  [ "$S" = "FAILED" ] && echo "Failed!" && break
  sleep 4
done
```

**Python:**
```python
import httpx, os
BASE = os.environ["PHAYA_BASE"]
HEADERS = {"Authorization": f"Bearer {os.environ['PHAYA_API_KEY']}"}

r = httpx.post(f"{BASE}/text-to-image/generate", headers=HEADERS, json={
    "prompt": "A neon-lit Tokyo street at night, cinematic",
    "aspect_ratio": "16:9"
})
r.raise_for_status()
job_id = r.json()["job_id"]

result = poll(BASE, "text-to-image/status", job_id, HEADERS)
print("Image URL:", result["image_url"])
```

---

## 3. Seedream 5.0 Image Generation

**Python:**
```python
r = httpx.post(f"{BASE}/seedream/create", headers=HEADERS, json={
    "prompt": "A mythical Thai warrior in golden armor, epic fantasy",
    "aspect_ratio": "9:16",
    "quality": "high"
})
job_id = r.json()["job_id"]
result = poll(BASE, "seedream/status", job_id, HEADERS)
print("Image URL:", result["image_url"])
```

**Image-to-image** (pass an existing image):
```python
r = httpx.post(f"{BASE}/seedream/create", headers=HEADERS, json={
    "prompt": "Same scene but at night with neon lights",
    "image_urls": ["https://example.com/source.jpg"],   # list, max 1 item
    "quality": "high"
})
```

---

## 4. Nano Banana 2

**Python:**
```python
r = httpx.post(f"{BASE}/nano-banana/create", headers=HEADERS, json={
    "prompt": "Ultra-detailed portrait of a Thai empress, 4K render",
    "resolution": "2K",          # 2.0 credits at 1K, 3.0 at 2K, 4.0 at 4K
    "aspect_ratio": "3:4",
    "output_format": "png"
})
job_id = r.json()["job_id"]
result = poll(BASE, "nano-banana/status", job_id, HEADERS)
print("Image URL:", result["image_url"])
```

---

## 5. Image-to-Video (Local FFmpeg — fast, cheap)

**Python (simple):**
```python
r = httpx.post(f"{BASE}/image-to-video/create", headers=HEADERS, json={
    "image_url": "https://example.com/photo.jpg",
    "duration": 6
})
job_id = r.json()["job_id"]
result = poll(BASE, "image-to-video/status", job_id, HEADERS)
print("Video URL:", result["video_url"])
```

**Python (with Ken Burns zoom + music):**
```python
r = httpx.post(f"{BASE}/image-to-video/create", headers=HEADERS, json={
    "image_url": "https://example.com/photo.jpg",
    "music_url": "https://example.com/background.mp3",   # NOT audio_url
    "duration": 10,
    "zoom": {                                             # object, not boolean
        "mode": "pan_right",
        "speed": 0.002,
        "max_scale": 1.4
    }
})
job_id = r.json()["job_id"]
result = poll(BASE, "image-to-video/status", job_id, HEADERS)
print("Video URL:", result["video_url"])
```

---

## 6. Sora 2 Image-to-Video

**Python:**
```python
r = httpx.post(f"{BASE}/sora2-video/create", headers=HEADERS, json={
    "prompt": "The warrior leaps forward in slow motion",
    "image_urls": ["https://example.com/warrior.jpg"],   # list, NOT image_url
    "aspect_ratio": "landscape",                          # NOT "16:9"
    "n_frames": "10",                                     # string, NOT integer
    "remove_watermark": True
})
job_id = r.json()["job_id"]
result = poll(BASE, "sora2-video/status", job_id, HEADERS, interval=8)
print("Video URL:", result["video_url"])
```

**With a reusable character:**
```python
r = httpx.post(f"{BASE}/sora2-video/create", headers=HEADERS, json={
    "prompt": "The character walks through a forest",
    "image_urls": ["https://example.com/scene.jpg"],
    "n_frames": "15",
    "character_id_list": ["char_abc123"]    # from sora2-character/create
})
```

---

## 7. Sora 2 Text-to-Video

**curl:**
```bash
JOB=$(curl -s -X POST "$PHAYA_BASE/sora2-text-to-video/create" \
  -H "Authorization: Bearer $PHAYA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A dragon flying over misty mountains at dawn","aspect_ratio":"landscape","n_frames":"10"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job: $JOB"
```

**Python:**
```python
r = httpx.post(f"{BASE}/sora2-text-to-video/create", headers=HEADERS, json={
    "prompt": "A dragon flying over misty mountains at dawn",
    "aspect_ratio": "landscape",    # "landscape" or "portrait", NOT "16:9"
    "n_frames": "10"                # "10" or "15" as a string
})
job_id = r.json()["job_id"]
result = poll(BASE, "sora2-text-to-video/status", job_id, HEADERS, interval=8)
print("Video URL:", result["video_url"])
```

---

## 8. Sora 2 Character Creation

```python
r = httpx.post(f"{BASE}/sora2-character/create", headers=HEADERS, json={
    "character_file_url": "https://example.com/actor_clip.mp4",  # 1-4s, max 100MB
    "character_prompt": "Young Thai woman in traditional dress"
})
job_id = r.json()["job_id"]
result = poll(BASE, "sora2-character/status", job_id, HEADERS, interval=5)
character_id = result["character_id"]   # string ID, not a URL
print("Character ID:", character_id)
# Use character_id in sora2-video.character_id_list
```

---

## 9. Seedance 1.5 Pro Video (ByteDance)

**Python:**
```python
r = httpx.post(f"{BASE}/seedance-video/create", headers=HEADERS, json={
    "prompt": "An astronaut walking on Mars, dust storm in background",
    "resolution": "720p",
    "duration": "8",            # string: "4", "8", or "12"
    "aspect_ratio": "16:9",
    "generate_audio": False
})
job_id = r.json()["job_id"]
result = poll(BASE, "seedance-video/status", job_id, HEADERS, interval=8)
print("Video URL:", result["video_url"])
```

**Image-to-video mode:**
```python
r = httpx.post(f"{BASE}/seedance-video/create", headers=HEADERS, json={
    "prompt": "The character turns and walks away",
    "input_urls": ["https://example.com/scene.jpg"],    # list, NOT image_url
    "duration": "4",
    "resolution": "1080p"
})
```

---

## 10. Kling 2.6 Motion Control

```python
r = httpx.post(f"{BASE}/kling-motion-control/create", headers=HEADERS, json={
    "prompt": "Graceful movement in the style of the reference",
    "input_urls": ["https://example.com/subject.jpg"],     # reference image (list)
    "video_urls": ["https://example.com/motion_ref.mp4"],  # motion reference (list)
    "mode": "1080p",                                        # NOT "resolution"
    "character_orientation": "video"
})
job_id = r.json()["job_id"]
result = poll(BASE, "kling-motion-control/status", job_id, HEADERS, interval=6)
print("Video URL:", result["video_url"])
```

---

## 11. Veo 3.1 Video (Google)

**Fast (15 credits):**
```python
r = httpx.post(f"{BASE}/veo31-video/create", headers=HEADERS, json={
    "prompt": "Slow motion cherry blossoms falling in a Japanese garden",
    "model": "veo3_fast",         # NOT quality="fast"
    "aspect_ratio": "16:9"
})
job_id = r.json()["job_id"]
result = poll(BASE, "veo31-video/status", job_id, HEADERS, interval=10)
print("Video URL:", result["video_url"])
```

**Quality (50 credits) with image reference:**
```python
r = httpx.post(f"{BASE}/veo31-video/create", headers=HEADERS, json={
    "prompt": "The scene continues with dramatic camera movement",
    "model": "veo3",              # NOT quality="quality"
    "image_urls": ["https://example.com/ref.jpg"],  # list, NOT image_url
    "generation_type": "REFERENCE_2_VIDEO",
    "enable_translation": True
})
```

---

## 12. Text-to-Music (Suno)

**Python:**
```python
r = httpx.post(f"{BASE}/text-to-music/generate", headers=HEADERS, json={
    "prompt": "Upbeat Thai folk music with modern electronic beats",
    "style": "world fusion",
    "model": "V4",
    "instrumental": False,
    "vocal_gender": "f"
    # NOTE: no "duration" field — length is determined by the model
})
job_id = r.json()["job_id"]
result = poll(BASE, "text-to-music/status", job_id, HEADERS, interval=5)

# Returns 2 tracks
print("Track 1:", result["audio_url"])
print("All tracks:", result["audio_urls"])   # list of 2 URLs
```

---

## 13. Text-to-Speech (Google Gemini TTS)

**Python:**
```python
r = httpx.post(f"{BASE}/text-to-speech/generate", headers=HEADERS, json={
    "prompt": "สวัสดีครับ ยินดีต้อนรับสู่ Phaya API",   # field is "prompt", NOT "text"
    "voice": "Aoede",
    "language": "th",
    "slow": False
})
job_id = r.json()["job_id"]
result = poll(BASE, "text-to-speech/status", job_id, HEADERS, interval=3)
print("Audio URL:", result["audio_url"])
```

---

## 14. Thai Subtitle Generator

**Python:**
```python
r = httpx.post(f"{BASE}/thai-subtitle/generate", headers=HEADERS, json={
    "media_url": "https://example.com/my-video.mp4",   # field is "media_url", NOT "video_url"
    "animation": "word_pop_fade",
    "timing_offset_ms": 0
    # NOTE: no "burn_in" field — subtitles are always burned in
}, timeout=300)
job_id = r.json()["job_id"]
result = poll(BASE, "thai-subtitle/status", job_id, HEADERS, interval=5)
print("Subtitled video URL:", result["video_url"])
```

---

## 15. Video Download (yt-dlp)

**Python:**
```python
r = httpx.post(f"{BASE}/video-download/create", headers=HEADERS, json={
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "format": "mp4",
    "quality": "720p"    # "best" | "720p" | "480p" | "360p" | "audio"
})
job_id = r.json()["job_id"]
result = poll(BASE, "video-download/status", job_id, HEADERS, interval=5)
print("Downloaded video URL:", result["download_url"])   # field is download_url, not video_url
```

---

## 16. Phaya-GPT Chat

**curl (non-streaming):**
```bash
curl -s -X POST "$PHAYA_BASE/phaya-gpt/chat/completions" \
  -H "Authorization: Bearer $PHAYA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Write a short Thai poem about the sea"}],"stream":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['message']['content'])"
  # Access d['message']['content'], NOT d['choices'][0]['message']['content']
```

**Python (non-streaming):**
```python
import httpx, os

BASE = os.environ["PHAYA_BASE"]
HEADERS = {"Authorization": f"Bearer {os.environ['PHAYA_API_KEY']}"}

r = httpx.post(f"{BASE}/phaya-gpt/chat/completions", headers=HEADERS, json={
    "messages": [{"role": "user", "content": "Explain how Phaya API works in 3 bullet points"}],
    "stream": False
})
r.raise_for_status()
data = r.json()
print(data["message"]["content"])   # flat dict — NOT choices[0].message.content
print(f"Tokens used: {data['usage']['total_tokens']}, Credits: {data['credits_used']}")
```

**Python (streaming — raw SSE):**
```python
with httpx.stream("POST", f"{BASE}/phaya-gpt/chat/completions", headers=HEADERS, json={
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": True
}) as resp:
    for line in resp.iter_lines():          # iter_lines(), NOT iter_text()
        if line.startswith("data: ") and "[DONE]" not in line:
            import json as _json
            try:
                obj = _json.loads(line[6:]) # line[6:] strips "data: " prefix
                delta = obj.get("choices", [{}])[0].get("delta", {}).get("content", "")
                print(delta, end="", flush=True)
            except Exception:
                pass
```

---

## 17. Use as OpenAI-Compatible API

The endpoint is at `/v1/` (not `/api/v1/`) — works with any OpenAI SDK:

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["PHAYA_API_KEY"],
    base_url="https://your-api-host"    # no /api/v1 suffix
)

response = client.chat.completions.create(
    model="google/gemini-3-flash-preview",   # actual upstream default model
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

---

## 18. Embedding

```python
r = httpx.post(f"{BASE}/embedding/create", headers=HEADERS, json={
    "input": ["Text to embed", "Another sentence"],
    "model": "qwen/qwen3-embedding-8b"   # optional, this is the default
})
embeddings = r.json()["data"]
print(f"Got {len(embeddings)} embedding vectors")
```
