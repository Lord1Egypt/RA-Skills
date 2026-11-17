# Recetas Higgsfield — foto gancho + animación cinemagraph

## 1) Foto gancho (si no la tienes ya)

Genera el montaje de portada con `generate_image`. Receta validada para la cara del usuario
(ver memoria `feedback_avatar_imagen`): **nano_banana_2 + 2k/4k + 3 selfies + prefijo identity-emphasis**.

```
mcp__higgsfield__generate_image
  model: "nano_banana_2"
  params:
    resolution: "2k"            # 2k basta para 1080×1350; usa 4k si quieres margen
    aspect_ratio: "4:5"         # formato carrusel vertical
    prompt: "identity-emphasis. Photorealistic cinematic portrait of the EXACT SAME person
             from the reference photos — <rasgos: pelo, etc.>, soft confident smile.
             <Escena/mundo del estilo que clonas>. ...
             Subject framed in the lower two-thirds, LOTS of empty clear sky/space in the
             upper third for text. No text, no logos, no watermark."
    medias: [ {role:"image", value:<selfie1>}, {role:"image", value:<selfie2>}, {role:"image", value:<selfie3>} ]
```

Pasos previos para las selfies locales (cliente CLI, sin widget):
1. `media_upload` con `files:[{filename, content_type:"image/jpeg"}]` → devuelve `upload_url` + `media_id`.
2. `curl -X PUT -H "Content-Type: image/jpeg" --data-binary @archivo.jpg '<upload_url>'`
3. `media_confirm` con `type:"image"` y `media_ids:[...]`.

Carpeta de selfies del usuario, si la tiene configurada: `cerebro/fotos`. Si no existe, pregúntale la ruta.

> **DEJA CIELO/ESPACIO LIBRE ARRIBA.** El título va en el tercio superior; si la foto llena
> todo el cuadro, el texto pierde legibilidad.

## 2) Animación cinemagraph (la foto que se mueve)

Anima la foto gancho con `generate_video`. Usa la propia foto como `start_image`.

```
mcp__higgsfield__generate_video
  model: "seedance_2_0"
  params:
    aspect_ratio: "3:4"         # ⚠️ NUNCA "auto" → devuelve 16:9 horizontal (inservible)
    resolution: "1080p"
    mode: "std"
    duration: 5
    prompt: "Cinemagraph: keep the EXACT same framing, crop and composition as the still
             start photo, locked camera, no zoom and no reframe. Only these move subtly:
             clouds drift slowly, a few hair strands sway, she breathes and blinks once with a
             calm micro-smile, <mascota/elemento> tilts head and blinks. Pose and frame stay
             perfectly in place. No camera movement, no text."
    medias: [ {role:"start_image", value:<job_id de la foto gancho>} ]
```

Salida: **1080×1440** (3:4). Se recorta a 1080×1350 en el paso de composición.

### Gotchas de la animación (aprendidos en producción)
- **`aspect_ratio:"auto"` da 16:9 horizontal**, no respeta el 4:5 de entrada. Para vertical usa `3:4`
  (lo más cercano, recorte mínimo) o `9:16` si quieres más alto.
- Prompt = **cinemagraph con cámara fija**. Si pides "push-in" o "zoom", reencuadra y deja de
  parecer "la misma foto". Pide explícitamente *locked camera, no zoom, no reframe*.
- Mueve solo lo ambiental (nubes, pelo, parpadeo, respiración, mascota). El resto, quieto.
- `seedance_2_0` tarda ~2-3 min. Sondea con `job_status(..., sync:true)`.
- Higgsfield hace fallback silencioso (nano_banana_2 → flash); el resultado igual sirve.
