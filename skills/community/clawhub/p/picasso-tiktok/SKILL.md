---
name: picasso-tiktok
description: |
  Full TikTok/Reels video pipeline: script → TTS voiceover (ElevenLabs) → HeyGen talking avatar → auto-subtitles (Whisper) → ffmpeg compose → 1080x1920 final video. Also supports AI B-roll generation with Runway Gen-4.5 when no source video exists.
  
  ✅ USE WHEN:
  - Creating TikTok or Instagram Reels from scratch with voiceover
  - Turning a news article, topic, or script into a 9:16 video
  - Adding a talking avatar to any video
  - Generating AI B-roll clips (Runway Gen-4.5) and editing into a Reel
  
  ❌ DON'T USE WHEN:
  - You only need an image (use nano-banana-pro)
  - You only need TTS audio (use ElevenLabs directly)
  
  Required env vars: ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, HEYGEN_API_KEY, YOUR_HEYGEN_AVATAR_ID, OPENAI_API_KEY, REPLICATE_API_TOKEN
  Required system tools: ffmpeg, yt-dlp, Python 3
version: 1.2.0
---

# Picasso TikTok 🎨

Genera videos 9:16 para TikTok/Reels combinando un video fuente + avatar HeyGen + subtítulos sincronizados.

## ⚠️ FLUJO OBLIGATORIO — paso a paso con validación

**NUNCA correr el pipeline completo de una sola vez. Siempre:**

1. Descargar + analizar video → **mostrar duración e info**
2. Escribir guión → **mostrar a Paul, esperar OK**
3. Generar audio → **enviar para escuchar, esperar OK**
4. Preguntar configuración del video (layout, música fuente) → **esperar OK**
5. Generar avatar HeyGen
6. Transcribir + corregir subtítulos contra guión original
7. Componer video final

---

## Paso 1: Descargar video

### Google Drive
```bash
pip install gdown -q
gdown "https://drive.google.com/uc?id=FILE_ID&confirm=t" -O output.mp4
```
Si falla (permisos): pedir a Paul que comparta "cualquier persona con el link" o mande por Telegram.

### TikTok / YouTube
```bash
yt-dlp -o "output.mp4" "URL"
```

### Telegram (archivo adjunto)
Los archivos adjuntos llegan a `~/.openclaw/media/inbound/`

### Verificar
```bash
ffprobe video.mp4 2>&1 | grep -E "Duration|Video:|Audio:"
```

---

## Paso 2: Guión

**Reglas:**
- Español argentino rioplatense (voseo: "grabás", "actualizás", "imaginá")
- Hook fuerte en los primeros 3 segundos
- Dinámico, sin relleno
- Sin notas de dirección, solo el texto que se lee
- CTA al final (ej: "sumate a Morfeo Labs")
- Duración objetivo: igual o levemente mayor que el video fuente

**Mostrar guión y esperar aprobación antes de generar audio.**

---

## Paso 3: Audio — TTS

### ✅ DEFAULT: ElevenLabs Paul Pro

**SIEMPRE generar 3 variaciones de voz y enviar para que Paul elija antes de continuar.**

```python
import requests, time

CACHE = "/home/ubuntu/clawd/projects/picasso-tiktok/cache/JOB_NAME"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/$ELEVENLABS_VOICE_ID"
HEADERS = {"xi-api-key": "$ELEVENLABS_API_KEY", "Content-Type": "application/json"}

# Variación A — expresivo, pausas fuertes
# Variación B — DEFAULT ganador: guiones largos para pausas dramáticas (stability 0.45)
# Variación C — fluido y periodístico, sin cortes (stability 0.62)

configs = [
    ("A", script_a, {"stability": 0.35, "similarity_boost": 0.80, "style": 0.25}),
    ("B", script_b, {"stability": 0.45, "similarity_boost": 0.82, "style": 0.15}),  # ← ganador recurrente
    ("C", script_c, {"stability": 0.62, "similarity_boost": 0.78, "style": 0.05}),
]

for ver, text, settings in configs:
    r = requests.post(BASE_URL, headers=HEADERS,
        json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": settings})
    with open(f"{CACHE}/audio_{ver}.mp3", "wb") as f:
        f.write(r.content)
    print(f"✅ V{ver} {len(r.content)//1024}KB")
    time.sleep(1)
```

**Trucos de puntuación para controlar ritmo:**
- Frases separadas en párrafos propios → pausas naturales largas (VA)
- Guiones largos `—` dentro de frases → pausa dramática mid-sentence (VB, ganador)
- Todo junto sin cortes → fluido tipo documental (VC)

**⚠️ IMPORTANTE:**
- Modelo: `eleven_multilingual_v2` — NUNCA `eleven_v3` (cambia el acento)
- Voice ID Paul Pro: `$ELEVENLABS_VOICE_ID`
- API Key: `$ELEVENLABS_API_KEY`

### Backup: Cartesia sonic-3
```python
r = requests.post("https://api.cartesia.ai/tts/bytes",
    headers={"X-API-Key": "$CARTESIA_API_KEY",
             "Cartesia-Version": "2025-04-16", "Content-Type": "application/json"},
    json={"model_id": "sonic-3",  # SIEMPRE sonic-3, nunca sonic-2
          "transcript": SCRIPT,
          "voice": {"mode": "id", "id": "$CARTESIA_VOICE_ID"},
          "language": "es",
          "output_format": {"container": "mp3", "sample_rate": 44100, "bit_rate": 128000}})
```

**Enviar audio para escuchar y esperar OK antes de continuar.**

---

## Paso 4: Preguntar configuración

Antes de generar avatar y componer, confirmar:
- **Layout:** 60/40 (source top), 50/50, 40/60 (avatar top)
- **Subtítulos:** sí/no
- **Audio fuente:** ¿mezclar música original? Si sí, ¿a qué volumen? (típico: 30%)
- **Título para primeros segundos** (ej: "Esta chica no existe 👁️")
- **Caption TikTok** con hashtags

---

## Paso 5: Avatar HeyGen

### Subir audio a uguu.se (requerido por HeyGen)
```python
import requests

with open("audio.mp3", "rb") as f:
    r = requests.post("https://uguu.se/upload",
        files={"files[]": ("audio.mp3", f.read(), "audio/mpeg")}, timeout=30)
audio_url = r.json()["files"][0]["url"]
```

### Generar video
```python
HEYGEN_KEY = "$HEYGEN_API_KEY"
AVATAR_ID  = "aa7ca06de7454b9caa147b97a534e813"  # Paul default

r = requests.post("https://api.heygen.com/v2/video/generate",
    headers={"X-Api-Key": HEYGEN_KEY, "Content-Type": "application/json"},
    json={
        "video_inputs": [{
            "character": {"type": "avatar", "avatar_id": AVATAR_ID, "avatar_style": "normal"},
            "voice": {"type": "audio", "audio_url": audio_url},
            "background": {"type": "color", "value": "#000000"}
        }],
        "dimension": {"width": 432, "height": 768},  # 9:16 pequeño, escala mejor
        "aspect_ratio": "9:16"
    })
video_id = r.json()["data"]["video_id"]
```

### Poll hasta completar (~2-4 min)
```python
import time
while True:
    r = requests.get(f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
        headers={"X-Api-Key": HEYGEN_KEY})
    data = r.json().get("data") or {}
    if data.get("status") == "completed":
        avatar_url = data["video_url"]
        break
    time.sleep(15)
```

### Descargar y cropdetect
```bash
curl -sL "$AVATAR_URL" -o avatar.mp4

# Auto-detect crop (quita padding negro de HeyGen)
ffmpeg -ss 2 -i avatar.mp4 -vframes 10 -vf cropdetect=24:2:0 -f null - 2>&1 | grep crop= | tail -2
# Típico resultado: crop=432:244:0:262
```

---

## Paso 6: Subtítulos — SIEMPRE contrastar con guión original

### Transcribir con Whisper
```python
import requests, os

with open("audio.mp3", "rb") as f:
    r = requests.post("https://api.openai.com/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        files={"file": ("audio.mp3", f, "audio/mpeg")},
        data={"model": "whisper-1", "response_format": "verbose_json",
              "timestamp_granularities[]": "word", "language": "es"})
words = r.json()["words"]
```

### ⚠️ SIEMPRE revisar y corregir contra el guión original

Whisper comete errores frecuentes en español/rioplatense + términos técnicos:

| Whisper escribe | Correcto |
|-----------------|----------|
| Cling | KLING |
| Confi / Confy | COMFY |
| Imagina | IMAGINÁ |
| Grabas | GRABÁS |
| Actualizas | ACTUALIZÁS |
| Buscas | BUSCÁS |
| Preparas | PREPARÁS |
| I A | IA |
| cualquier nombre de marca | verificar siempre |

Corregir en el .ass antes de renderizar:
```python
fixes = [("CLING", "KLING"), ("CONFI", "COMFY"), ("IMAGINA", "IMAGINÁ"), ...]
for wrong, right in fixes:
    ass = ass.replace(wrong, right)
```

### Generar .ass
```python
import sys
sys.path.insert(0, "/home/ubuntu/clawd/projects/picasso-tiktok/picasso-api/workers")
from subtitles import generate_ass

ass = generate_ass(words)
# Aplicar correcciones de marca/voseo
# Aplicar MarginV según layout (ver tabla abajo)
with open("subs.ass", "w") as f:
    f.write(ass)
```

### MarginV según layout

| Layout | Top px | Bot px | MarginV recomendado |
|--------|--------|--------|---------------------|
| 60/40  | 1152   | 768    | 720                 |
| 50/50  | 960    | 960    | 880                 |
| 40/60  | 768    | 1152   | ~1000               |

Parchear en el .ass:
```python
import re
ass = re.sub(
    r'(Style: Word,\S+,\d+,\S+,\S+,\S+,\S+,-?\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,[\d.]+,[\d.]+,\d+,\d+,\d+,)\d+,',
    lambda m: m.group(1) + str(MARGIN_V) + ',', ass)
```

---

## Paso 7: Componer video final

### Splits de altura

| Layout | top_h | bot_h |
|--------|-------|-------|
| 60/40  | 1152  | 768   |
| 50/50  | 960   | 960   |
| 40/60  | 768   | 1152  |

### Filter chain base (sin mezcla de audio)
```bash
ffmpeg -y \
  -i source.mp4 -i avatar.mp4 -i audio.mp3 \
  -filter_complex "
    [0:v]scale=1080:{top_h}:force_original_aspect_ratio=increase,crop=1080:{top_h},setsar=1[top];
    [top]pad=1080:1920:0:0:black[bg];
    [1:v]crop={crop_str},scale=1080:{bot_h}:force_original_aspect_ratio=increase,crop=1080:{bot_h},setsar=1[av];
    [bg][av]overlay=0:{top_h}[ov];
    [ov]ass=subs.ass[final]
  " \
  -map "[final]" -map "2:a" \
  -c:v libx264 -profile:v high -level 4.0 -crf 23 \
  -c:a aac -b:a 192k -movflags +faststart -shortest \
  output.mp4
```

### Con mezcla de audio (música fuente al X%)
```bash
  -filter_complex "
    [0:v]...[ov];
    [ov]ass=subs.ass[final];
    [0:a]volume=0.3[src_a];
    [2:a]volume=1.0[tts_a];
    [src_a][tts_a]amix=inputs=2:duration=shortest[mix_a]
  " \
  -map "[final]" -map "[mix_a]" \
```

### ⚠️ NUNCA estirar el avatar

```bash
# ✅ CORRECTO: scale to fill + crop (sin deformación, sin negro)
[1:v]crop={crop_str},scale=1080:{bot_h}:force_original_aspect_ratio=increase,crop=1080:{bot_h},setsar=1[av]

# ❌ MAL: escala directa deforma
[1:v]crop={crop_str},scale=1080:{bot_h},setsar=1[av]

# ❌ MAL: pad con negro (Paul no quiere franjas negras)
[1:v]crop={crop_str},scale=1080:-2,pad=1080:{bot_h}:...,setsar=1[av]
```

---

## Output final

- Resolución: 1080x1920
- Codec: H.264 high profile level 4.0
- Audio: AAC 192k
- `-movflags +faststart`

## Layouts adicionales

### 2/3 top + 1/3 bottom (Chiqui Tapia, Claude Opus style)
```
top_h=1280, bot_h=640, MarginV=640
```
```bash
[0:v]scale=1080:1280:force_original_aspect_ratio=increase,crop=1080:1280,setsar=1[top];
[top]pad=1080:1920:0:0:black[bg];
[1:v]crop=432:240:0:264,scale=1080:640:force_original_aspect_ratio=increase,crop=1080:640,setsar=1[av];
[bg][av]overlay=0:1280[ov]
```

### Video fuente que debe verse ENTERO (letterbox, sin recorte)
```bash
# Usar decrease + pad en vez de increase + crop
[0:v]scale=1080:{top_h}:force_original_aspect_ratio=decrease,pad=1080:{top_h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1[top]
```

### Loop de video fuente cuando el audio es más largo
```bash
AUDIO_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 audio.mp3)
ffmpeg -y -stream_loop 3 -i source.mp4 -t $AUDIO_DUR \
  -c:v libx264 -preset fast -crf 18 -c:a aac source_looped.mp4
```

### Recorte del inicio del video fuente
```bash
# Agregar -ss SEGUNDOS antes del -i source.mp4 en el loop
ffmpeg -y -ss 1.25 -stream_loop 3 -i source.mp4 -t $AUDIO_DUR ...
```

---

## B-roll generado con IA — Runway Gen-4.5

Cuando no hay video fuente real, generar B-roll con Runway Gen-4.5 via Replicate.

**Variables:**
- `prompt` — descripción cinematográfica del clip
- `image` — frame inicial opcional (para image-to-video)
- `duration` — segundos (default 5, máximo 10)
- `aspect_ratio` — default `16:9`; usar `768:1344` para 9:16 vertical

**Costo:** ~$0.05 por clip de 10s

```python
import requests, os, time

r = requests.post("https://api.replicate.com/v1/models/runwayml/gen-4.5/predictions",
    headers={"Authorization": f"Token {os.environ['REPLICATE_API_TOKEN']}", "Content-Type": "application/json"},
    json={"input": {
        "prompt": "DESCRIPCION_CINEMATOGRAFICA",
        "duration": 10,
        "ratio": "768:1344"  # vertical 9:16
    }})
pred_id = r.json()["id"]

# Poll
while True:
    r = requests.get(f"https://api.replicate.com/v1/predictions/{pred_id}",
        headers={"Authorization": f"Token {os.environ['REPLICATE_API_TOKEN']}"})
    status = r.json()["status"]
    if status == "succeeded":
        url = r.json()["output"]
        if isinstance(url, list): url = url[0]
        # descargar...
        break
    time.sleep(15)
```

**Workflow para videos con guión largo:**
1. Generar audio TTS primero → obtener duración total
2. Dividir guión en segmentos temáticos con timestamps aproximados
3. Asignar duración a cada clip de Runway (suma debe cubrir la duración total)
4. Generar todos los clips en paralelo (lanzar predicciones, luego poll)
5. Concatenar clips con ffmpeg, usar como source en Picasso

---

## Checklist antes de entregar

- [ ] Guión aprobado por Paul
- [ ] 3 variaciones de audio enviadas — Paul elige antes de continuar
- [ ] Layout confirmado por Paul
- [ ] Subtítulos corregidos contra guión original (errores de Whisper fixeados)
- [ ] Avatar sin deformación (AR mantenido)
- [ ] Audio fuente mezclado al volumen correcto (si aplica)
- [ ] Video es 1080x1920 verificado con ffprobe
