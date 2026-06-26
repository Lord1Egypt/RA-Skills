# Morfeo Content Engine Pipeline

## Descripción

Pipeline autónomo que genera videos TikTok para Morfeo Labs.
Cada video simula contenido orgánico de una marca argentina real,
con un plot twist final que revela que fue creado con IA por Morfeo Labs.

**Frecuencia:** 4x/día — 11:00, 15:00, 19:00, 23:00 UTC  
**Proceso:** PM2 (`morfeo-content`)  
**Proyecto:** `/home/ubuntu/clawd/projects/morfeo-content-engine/`  
**Repo marcas:** `https://github.com/PauldeLavallaz/marcas-argentinas`

---

## Flujo completo (8 pasos)

```
Marca → Modelo → Hero Image → Multishot → Ver shots → Guión → VEED ×5 → ffmpeg → Postiz DRAFT
```

⚠️ **El guión se escribe DESPUÉS de ver los shots** — nunca antes.
El diálogo debe describir lo que se ve realmente en cada imagen, no situaciones inventadas.

---

## PASO 1 — Elegir marca

Lee de `~/clawd/projects/marcas-argentinas/marcas.json` (34 marcas argentinas reales).  
Cada entrada tiene: `id`, `nombre`, `categoria`, `descripcion`, `imagen` (path a imagen del producto).

**Para agregar marca:** subir imagen a `images/`, agregar entrada en `marcas.json`, hacer push.

---

## PASO 2 — Selección de modelo

**Opción A — Catálogo (default):**
- Pool: 114 modelos en `~/clawd/models-catalog/catalog/`
- Archivo: `catalog/images/model_XX.jpg`
- Filtros disponibles: `body_type` (curvy, slim, athletic, etc.)

**Opción B — Portrait Generator (cuando el guión lo requiere):**
- Deployment ID: `0b82e690-9a08-4d1f-85f8-28849d16caa4`
- Usar cuando: personaje con edad muy específica, etnia exacta, rasgos únicos
- Output: `imagen_1` = siempre vista frontal = correcta para `model` en Morpheus

---

## PASO 3 — Morpheus (imagen hero)

**Deployment ID:** `1e16994d-da67-4f30-9ade-250f964b2abc`  
**Skill:** `morpheus-fashion-design@1.4.0`

**Inputs:**
```python
{
    "product": "<URL pública imagen del producto>",  # del repo marcas-argentinas
    "model": "<URL pública imagen del modelo>",      # catálogo o Portrait Generator
    "brief_text": "...",  # en INGLÉS — evita filtros de moderación de Gemini en español
    "environment_pack": "...",   # NUNCA "auto"
    "time_weather_pack": "...",
    "body_language_pack": "...",
    "clothing_pack": "...",
}
```

**Outputs — siempre 3:**
1. Banana (preview)
2. Upscale
3. **Grain ← SIEMPRE usar este** (`grain_only=True`)

⚠️ **No existe campo `logo`.**

---

## PASO 4 — Multishot (variaciones de ángulo)

**Deployment ID:** `9ccbb29a-d982-48cc-a465-bae916f2c7fd`

- Input: hero image (Grain)
- Output: 10 variaciones de ángulo/perspectiva

⚠️ **Si los shots ya están en disco → NO volver a correr Multishot.**

---

## PASO 5 — Selección de shots y análisis visual

**Este paso es crítico. El guión se escribe a partir de aquí.**

1. Mostrar/evaluar los 10 shots
2. Seleccionar los 5 mejores (por diversidad de ángulo, calidad, expresión)
3. Para cada shot seleccionado, hacer descripción visual con Gemini:
   - ¿Qué hace el personaje?
   - ¿Qué sostiene o muestra?
   - ¿Qué expresión tiene?
   - ¿Dónde está?

```python
# Descripción de cada shot antes de escribir el guión
prompt = "Describí en 1-2 oraciones qué se ve en esta imagen: qué hace el personaje, qué sostiene, dónde está, qué emoción tiene. Sé específico y literal."
```

---

## PASO 6 — Guión (DESPUÉS de ver los shots)

**Modelo:** Gemini 2.5 Pro  
**Estructura — 5 escenas, una por shot:**

| Escena | Shot | Función | Duración |
|--------|------|---------|----------|
| HOOK | shot_1 | Engancha en el primer segundo | ≤ 10s |
| STORY_1 | shot_2 | Primer paso de la historia | ≤ 15s |
| STORY_2 | shot_3 | Sube la tensión / genera duda | ≤ 15s |
| PLOT_TWIST | shot_4 | Revela que es una IA de Morfeo Labs | ≤ 15s |
| CTA | shot_5 | Automatización de contenido + morfeolabs.com | ≤ 10s |

### Reglas del guión

**Contenido:**
- El diálogo debe describir/reaccionar a lo que se ve LITERALMENTE en el shot — nada inventado
- El plot twist SIEMPRE menciona "Morfeo Labs" y que es una IA
- El CTA habla de **automatización de contenido para marcas**, no solo de "crear videos"
- El CTA termina en `morfeolabs.com`

**Formato:**
- Solo diálogo hablado — CERO anotaciones `[así]`, `*así*`, `(así)`
- VEED rechaza scripts con anotaciones de dirección
- Máximo 15 palabras por escena

**Tono y lenguaje:**
- Español argentino coloquial auténtico
- Adaptar el tono al personaje visible en los shots (no al producto)
- Jugar con contradicciones entre el personaje y el producto (eso genera humor orgánico)
- Usar slang argentino real:
  - ✅ chabón, pibe, grosso, trucho, posta, re, che, boludez
  - ❌ malote, rudo (son de España), pulpa (forzado)
- El humor surge de la situación, no de chistes forzados

### Proceso de iteración del guión

Si el guión no convence, identificar el problema específico:
- "muy pete" → el tono no condice con el personaje
- "no suena argentino" → revisar slang
- "el CTA no habla de automatización" → reformular
- Solo reescribir las escenas con problemas, no todo

---

## PASO 7 — VEED UGC × 5 (clips lip-sync)

**Deployment ID:** `627c8fb5-1285-4074-a17c-ae54f8a5b5c6`

**Reglas críticas:**

1. **SIEMPRE lanzar los 5 en paralelo** — `ThreadPoolExecutor(max_workers=5)`
2. **Cada clip = shot único + diálogo único de su escena**
   - clip_01_HOOK → shot_1 + diálogo HOOK
   - clip_02_STORY_1 → shot_2 + diálogo STORY_1
   - etc.
3. **NUNCA repetir el mismo shot o diálogo**
4. **Orden garantizado por índice** — no por orden de llegada de los runs

**Voice IDs (ElevenLabs, argentino):**
- Femenino: `9rvdnhrYoXoUt4igKpBw` (Mariana)
- Masculino: `PBi4M0xL4G7oVYxKgqww` (Franco)

⚠️ **La voz DEBE coincidir con el género visible en los shots.**
Revisar el modelo antes de elegir voice_id — nunca asumir.

**Robustez — crítico para producción:**
- `generar_clip()` tiene retry automático x3 — si un run se cancela, reintenta
- Validación de tamaño mínimo: clip < 300KB = corrupto → reintenta automáticamente
- `max_workers` se lee del `concurrency_limit` real del deployment (actualmente 2)
  - NUNCA lanzar más workers que el concurrency_limit o los jobs se cancelan por timeout
  - El deployment VEED (`627c8fb5`) tiene `concurrency_limit: 2` — solo 2 jobs simultáneos
- `run_timeout` del deployment: 600s (fue subido de 300s)

**Root causes de fallas en producción:**
| Problema | Causa raíz | Fix aplicado |
|----------|-----------|-------------|
| Jobs cancelados | max_workers > concurrency_limit del deployment | workers = concurrency_limit (leído via API) |
| Clips corruptos (56KB) pasan como éxito | No se validaba tamaño post-descarga | Validar > 300KB, retry si no |
| Video final de 69s y trabado | ffmpeg concatenó clips corruptos sin detectarlos | Validación antes del concat |

**Output API:** `data.files[]` (NO `data.images[]`)

---

## PASO 8 — ffmpeg concat

Normalizar aspect ratio ANTES de concatenar:

```bash
ffmpeg -y -i clip.mp4 \
  -vf "scale=736:1312:force_original_aspect_ratio=decrease,pad=736:1312:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -c:a aac -ar 44100 norm_clip.mp4
```

Resolución estándar: **736×1312** (9:16 para TikTok/Reels)

---

## PASO 9 — Postiz DRAFT

⚠️ **SIEMPRE publicar como DRAFT — nunca publicar directo**

Si la API da SSL/503 → es caída temporal, reintentar en 5 minutos.

---

## ComfyDeploy — IDs de deployments

| Paso | Nombre | Deployment ID |
|------|--------|---------------|
| 2b | Portrait Generator | `0b82e690-9a08-4d1f-85f8-28849d16caa4` |
| 3 | Morpheus Fashion Design | `1e16994d-da67-4f30-9ade-250f964b2abc` |
| 4 | Multishot UGC | `9ccbb29a-d982-48cc-a465-bae916f2c7fd` |
| 7 | VEED UGC | `627c8fb5-1285-4074-a17c-ae54f8a5b5c6` |

---

## Scripts disponibles

| Script | Uso |
|--------|-----|
| `pipeline.py` | Pipeline completo end-to-end |
| `continue_run.py` | Retomar desde Multishot (shots ya en disco) |
| `run_veed.py` | Solo el paso VEED con shots pre-existentes |

---

## Errores conocidos y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| Guión describe cosas que no se ven | Se escribió antes de generar los shots | Siempre analizar shots primero, guión después |
| `VEED no devolvió output` | Parser buscaba `data.images[]` | Usar `data.files[]` |
| Clips desordenados | Descarga por orden de creación | Trackear run_id → escena por `workflow_inputs.script` |
| Aspect ratio roto en concat | ffmpeg sin normalizar | Normalizar a 736×1312 antes |
| Postiz SSL 503 | API caída temporalmente | Reintentar en 5 min |
| VEED `cancelled` | Machine timeout | Aumentar `run_timeout` en deployment |
| Moderación Gemini en español | Palabras como "contextura robusta" | Escribir brief en inglés |
