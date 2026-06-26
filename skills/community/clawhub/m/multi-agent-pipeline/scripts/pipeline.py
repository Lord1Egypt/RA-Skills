"""
Story pipeline — Anansi (story gen), Ogma (dual-STT), Devi (narration).
Wires the demo flow: voice input → story → narration → playback.
"""
import os
import base64
import json
import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import database as db
import prompt_cache

router = APIRouter()

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")

# --- Models ---
class StoryRequest(BaseModel):
    child_name: str
    language: str = "en"
    prompt: str
    voice_id: Optional[str] = None

class NarrateRequest(BaseModel):
    text: str
    voice_id: str = "pNInz6obpgDQGcFmaJgB"
    language: str = "en"

# --- Ogma: Dual-STT (ElevenLabs + Voxtral) ---
@router.post("/api/voice/transcribe")
async def transcribe_voice(audio: UploadFile = File(...)):
    audio_data = await audio.read()
    results = {}

    # ElevenLabs STT (Scribe v1)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post("https://api.elevenlabs.io/v1/speech-to-text",
                headers={"xi-api-key": ELEVENLABS_API_KEY},
                files={"file": (audio.filename or "audio.wav", audio_data, audio.content_type or "audio/wav")},
                data={"model_id": "scribe_v1"})
            if r.status_code == 200:
                el_data = r.json()
                results["elevenlabs"] = {
                    "text": el_data.get("text", ""),
                    "language": el_data.get("language_code", "en")
                }
    except Exception as e:
        results["elevenlabs"] = {"error": str(e)}

    # Voxtral (Mistral) STT — via Mistral's audio endpoint
    try:
        from mistralai import Mistral
        import base64
        if MISTRAL_API_KEY:
            mclient = Mistral(api_key=MISTRAL_API_KEY)
            b64_audio = base64.b64encode(audio_data).decode()
            resp = mclient.chat.complete(
                model="mistral-large-latest",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Transcribe this audio exactly. Also detect the language. Respond as JSON: {\"text\": \"...\", \"language\": \"en\"}"},
                        {"type": "audio_url", "audio_url": f"data:audio/wav;base64,{b64_audio}"}
                    ]
                }]
            )
            voxtral_text = resp.choices[0].message.content.strip()
            # Try to parse JSON response
            try:
                results["voxtral"] = json.loads(voxtral_text)
            except json.JSONDecodeError:
                results["voxtral"] = {"text": voxtral_text, "language": "en"}
    except Exception as e:
        results["voxtral"] = {"error": str(e)}

    # Consensus: prefer ElevenLabs, fall back to Voxtral
    el = results.get("elevenlabs", {})
    vx = results.get("voxtral", {})
    final_text = el.get("text") or vx.get("text") or ""
    final_lang = el.get("language") or vx.get("language") or "en"

    return {
        "prompt": final_text,
        "language": final_lang,
        "ogma_consensus": results,
        "tool": "ogma_dual_stt"
    }

# --- Anansi: Story Generation (Mistral Large) ---
@router.post("/api/story")
async def create_story(req: StoryRequest):
    # Check cache
    cached = await prompt_cache.get_cached(req.prompt, req.child_name, req.language)
    if cached:
        return {
            "id": cached.get("id", 0), "title": cached.get("title", "Cached"),
            "scenes": cached.get("scenes", []), "mood": cached.get("mood", "magical"),
            "language": req.language, "child_name": req.child_name,
            "agent": "cache_hit", "tool": "prompt_cache", "cached": True
        }

    if not MISTRAL_API_KEY:
        raise HTTPException(status_code=500, detail="MISTRAL_API_KEY not set")

    from mistralai import Mistral
    mclient = Mistral(api_key=MISTRAL_API_KEY)

    lang_names = {"en": "English", "fr": "French", "ja": "Japanese", "hi": "Hindi",
                  "es": "Spanish", "pt": "Portuguese", "de": "German", "zh": "Chinese",
                  "ar": "Arabic", "ko": "Korean"}
    lang_name = lang_names.get(req.language, "English")

    system_prompt = f"""You are Anansi 🕷️, the master storyteller. Create a magical bedtime story for a child named {req.child_name}.

Rules:
- Write entirely in {lang_name}
- 4-6 short scenes/paragraphs, each 2-3 sentences
- Gentle, dreamy, calming tone — this is a bedtime story
- Include the child's name as the main character
- End with the child falling peacefully asleep
- Return as JSON: {{"title": "...", "scenes": ["scene1", "scene2", ...], "mood": "calming|adventurous|funny|magical"}}"""

    resp = mclient.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.prompt}
        ],
        response_format={"type": "json_object"}
    )

    story_raw = resp.choices[0].message.content.strip()
    try:
        story = json.loads(story_raw)
    except json.JSONDecodeError:
        story = {"title": f"A Story for {req.child_name}", "scenes": [story_raw], "mood": "magical"}

    # Save to DB
    content_json = json.dumps(story, ensure_ascii=False)
    voice_id = req.voice_id or "pNInz6obpgDQGcFmaJgB"
    result = await db.execute(
        "INSERT INTO stories (title, content, voice_id, child_name, language) VALUES (?, ?, ?, ?, ?)",
        [story.get("title", "Untitled"), content_json, voice_id, req.child_name, req.language]
    )

    # Get the inserted ID
    id_result = await db.execute("SELECT MAX(id) FROM stories", [])
    story_id = id_result.rows[0][0] if id_result.rows else 1

    await prompt_cache.set_cached(req.prompt, req.child_name, req.language,
        {"id": story_id, "title": story.get("title"), "scenes": story.get("scenes", []), "mood": story.get("mood", "magical")})

    return {
        "id": story_id,
        "title": story.get("title", "Untitled"),
        "scenes": story.get("scenes", []),
        "mood": story.get("mood", "magical"),
        "language": req.language,
        "child_name": req.child_name,
        "agent": "anansi",
        "tool": "mistral_large"
    }

# --- Stories CRUD ---
@router.get("/api/stories")
async def list_stories():
    rs = await db.execute("SELECT id, title, child_name, language, created_at FROM stories ORDER BY created_at DESC LIMIT 50", [])
    return [{"id": r[0], "title": r[1], "child_name": r[2], "language": r[3], "created_at": r[4]} for r in rs.rows]

@router.get("/api/stories/{story_id}")
async def get_story(story_id: int):
    rs = await db.execute("SELECT id, title, content, voice_id, child_name, language, created_at, audio_cache, image_cache FROM stories WHERE id = ?", [story_id])
    if not rs.rows:
        raise HTTPException(status_code=404, detail="Story not found")
    r = rs.rows[0]
    content = json.loads(r[2]) if r[2] else {}
    scenes = content.get("scenes", [])
    scenes = [s.get("text", str(s)) if isinstance(s, dict) else str(s) for s in scenes]
    audio_cache = {}
    if len(r) > 7 and r[7]:
        try:
            audio_cache = {k: True for k in json.loads(r[7]).keys()}
        except: pass
    image_cache = {}
    if len(r) > 8 and r[8]:
        try:
            image_cache = {k: True for k in json.loads(r[8]).keys()}
        except: pass
    return {
        "id": r[0], "title": r[1], "scenes": scenes,
        "mood": content.get("mood", "magical"), "voice_id": r[3],
        "child_name": r[4], "language": r[5], "created_at": r[6],
        "has_audio": audio_cache, "has_images": image_cache
    }

# --- Devi: Narration (ElevenLabs TTS) ---
@router.post("/api/narrate")
async def narrate_scene(req: NarrateRequest):
    if not ELEVENLABS_API_KEY:
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not set")

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{req.voice_id}",
            headers={"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"},
            json={
                "text": req.text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}
            }
        )
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text[:500])
        return StreamingResponse(iter([r.content]), media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=narration.mp3"})

# --- Cached audio endpoint ---
@router.get("/api/stories/{story_id}/audio/{scene_index}")
async def get_cached_audio(story_id: int, scene_index: str):
    rs = await db.execute("SELECT audio_cache FROM stories WHERE id = ?", [story_id])
    if not rs.rows or not rs.rows[0][0]:
        raise HTTPException(status_code=404, detail="No cached audio")
    import base64
    cache = json.loads(rs.rows[0][0])
    audio_b64 = cache.get(scene_index)
    if not audio_b64:
        raise HTTPException(status_code=404, detail=f"No audio for scene {scene_index}")
    audio_bytes = base64.b64decode(audio_b64)
    return StreamingResponse(iter([audio_bytes]), media_type="audio/mpeg")


@router.get("/api/stories/{story_id}/image/{scene_key}")
async def get_story_image(story_id: int, scene_key: str):
    """Serve cached scene illustration as PNG."""
    rs = await db.execute("SELECT image_cache FROM stories WHERE id = ?", [story_id])
    if not rs.rows or not rs.rows[0][0]:
        raise HTTPException(status_code=404, detail="No images")
    cache = json.loads(rs.rows[0][0])
    key = f"img_{scene_key}" if not scene_key.startswith("img_") else scene_key
    if key not in cache:
        raise HTTPException(status_code=404, detail=f"Image {key} not found")
    from starlette.responses import Response
    return Response(content=base64.b64decode(cache[key]), media_type="image/png")
