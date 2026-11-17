---
name: portada-video-carrusel-formula100k
description: "Portada animada para un carrusel de Instagram: genera (o toma) la foto gancho con la cara de la usuaria en Higgsfield, la anima como cinemagraph de cámara fija (5 s, sin audio) y renderiza el título como PNG transparente con Chromium. En este servidor entrega las piezas (clip animado + título transparente + portada estática en PNG) listas para unir en CapCut o Edits. Usar cuando pida una portada animada o \"tipo video\" para un carrusel, \"anima la foto gancho\", \"cinemagraph de portada\", \"la portada que se mueve\", \"convierte mi portada en video\", \"el primer slide en video\". NO confundir con carrusel-render-formula100k (slides PNG), carrusel-viral-formula100k (guion) ni clonador-carrusel-formula100k (clonar estilo): esta skill solo hace la portada."
argument-hint: "[carpeta del carrusel o foto gancho]"
disable-model-invocation: "true"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - PASO 4 (ffmpeg crop + overlay) NO corre en este servidor. Entrega por Telegram: `cover_anim_raw.mp4` (el clip de Higgsfield) + `title-overlay.png` (título transparente) + la portada estática, y dile en 2 líneas cómo unirlos en CapCut o Edits (video abajo, PNG encima a pantalla completa, lienzo 4:5).
> - Portada estática: arma un HTML de 1080×1350 con `recursos/cover.png` de fondo y el mismo título encima, y renderízalo a PNG con Chromium. Eso es render de HTML, sí se puede, y le deja `slide-01.png` listo aunque no use el video.
> - Título transparente: `CHROME_PATH="$(command -v chromium || command -v chromium-browser)" node overlay_export.js <overlay.html> --out <png> --width 1080 --height 1350 --scale 2`, después de `npm install --omit=dev` en la carpeta de la skill. El script ya busca Chromium de Linux y lanza con `--no-sandbox`. Instala la fuente Poppins vía el `<link>` de Google Fonts: el servidor necesita salida a internet.
> - Higgsfield: foto (`nano_banana_2`, 2k, 4:5) y video (`seedance_2_0`, `3:4`, 5 s) llevan costo estimado → ✅. Pon `generate_audio: false` (Seedance 2.0 genera audio si no lo apagas). Seedance no tiene 4:5: el clip sale 3:4 y el recorte a 4:5 lo hace ella al unirlo.
> - Selfies: `cerebro/fotos/`. Si hay menos de 3, pídele que las mande por Telegram como archivo. Súbelas con `media_upload` → `curl -X PUT` → `media_confirm`.
> - Muéstrale la foto gancho por Telegram y espera ✅ antes de animar: el video es lo caro.
> - Si el clip pesa más de 50 MB (límite de Telegram), manda el link de Higgsfield en vez del archivo.

---

# Portada en VIDEO para carruseles (cinemagraph + título HTML)

> Convierte la imagen gancho de un carrusel en un clip de 5s donde la foto cobra vida
> (nubes a la deriva, pelo, parpadeo, respiración) con el título nítido encima.
> El movimiento frena el scroll; Instagram permite mezclar video + imágenes en un carrusel.

Resultado: **`slide-01-ANIMADO.mp4`** (1080×1350, 5s, sin audio) — va de PRIMERO en el carrusel.

## Cuándo activar
- "Hazme la portada del carrusel en video", "anima la foto gancho", "la portada que se mueve".
- Después de armar un carrusel (con `carrusel-render`, `clonador-carrusel`, etc.) cuando quieran
  que el primer slide sea un clip animado de la foto de portada.

## Dependencias
- Higgsfield MCP (`generate_image`, `generate_video`, `media_upload/confirm`, `job_status`). Gasta créditos.
- `node` + Chromium (render del título transparente vía `overlay_export.js`). La composición con `ffmpeg` no corre en este servidor.

---

## FLUJO (5 pasos)

### PASO 0 — Recoger insumos
Pregunta / confirma:
- **Foto gancho:** ¿ya existe (path o `job_id` de Higgsfield) o hay que generarla? Si hay que generarla,
  pide/usa 2-3 selfies del usuario (si tiene carpeta configurada, p. ej. `cerebro/fotos`;
  si no existe, pregúntale la ruta — no inventes una).
- **Título:** 3 partes — línea pequeña arriba / título grande / línea pequeña de cierre — + sub tipo
  "DESLIZA PARA VER →". (Suele venir del slide 1 del carrusel que ya armaste.)
- **Carpeta de salida** del carrusel (ej. `…/CARRUSELES ESPEJO/FECHA_tema/`). Crea `recursos/` dentro.

### PASO 1 — Foto gancho (si no la tienes)
Genera el montaje con `generate_image`. Receta y subida de selfies en
[references/recetas-higgsfield.md](references/recetas-higgsfield.md).
Clave: `nano_banana_2`, `2k`, `aspect_ratio:"4:5"`, prefijo `identity-emphasis`, 3 selfies role `image`,
y **dejar el tercio superior con cielo/espacio libre** para el título.
Descarga el PNG a `recursos/cover.png` y **muéstraselo al usuario** antes de animar (evita gastar video en una foto mala).

### PASO 2 — Animar la foto (cinemagraph)
`generate_video` con `seedance_2_0`, **`aspect_ratio:"3:4"`** (⚠️ nunca `"auto"` → sale 16:9 horizontal),
`resolution:"1080p"`, `mode:"std"`, `duration:5`, `medias:[{role:"start_image", value:<job_id de la foto>}]`.
Prompt = cinemagraph con **cámara fija, sin zoom ni reencuadre**; solo se mueve lo ambiental
(nubes, pelo, parpadeo, respiración, mascota). Prompt completo en
[references/recetas-higgsfield.md](references/recetas-higgsfield.md).
Sondea con `job_status(jobId, sync:true)` (tarda ~2-3 min). Descarga a `recursos/cover_anim_raw.mp4` (1080×1440).

### PASO 3 — Título transparente (PNG)
Escribe `recursos/overlay.html` con la plantilla de
[references/plantilla-overlay.md](references/plantilla-overlay.md) (fondo transparente, título en el
tercio superior, mismo tamaño que el video final: 1080×1350). Luego:

```bash
cd "<base de esta skill>"
node overlay_export.js "<carpeta>/recursos/overlay.html" \
  --out "<carpeta>/recursos/title-overlay.png" --width 1080 --height 1350 --scale 2
```

> Por qué un PNG aparte y no texto horneado: el video de IA deforma el texto si lo animas.
> El título se mantiene cristalino como capa encima. El `export.js` de los carruseles NO sirve aquí
> (usa `omitBackground:false`); por eso esta skill trae su propio `overlay_export.js` transparente.

### PASO 4 — Componer con ffmpeg (NO corre en este servidor: lee el bloque 🦞 de arriba)
Recorta el video de 1080×1440 a 1080×1350 (recorte central, 45px arriba) y superpón el título:

```bash
cd "<carpeta>"
ffmpeg -y -i recursos/cover_anim_raw.mp4 -i recursos/title-overlay.png \
  -filter_complex "[0:v]crop=1080:1350:0:45,setsar=1[v];[1:v]scale=1080:1350[t];[v][t]overlay=0:0[outv]" \
  -map "[outv]" -an -c:v libx264 -pix_fmt yuv420p -movflags +faststart -r 30 \
  slide-01-ANIMADO.mp4
```

Verifica el encuadre extrayendo 2 frames (inicio y mitad) y mirándolos con Read:
```bash
ffmpeg -y -ss 0.2 -i slide-01-ANIMADO.mp4 -frames:v 1 recursos/_chk0.png
ffmpeg -y -ss 3.5 -i slide-01-ANIMADO.mp4 -frames:v 1 recursos/_chk1.png
```
El título debe quedar sobre el cielo y la foto verse igual que la estática (mismo encuadre, ahora con movimiento). Borra los `_chk*.png` al terminar.

### PASO 5 — Entregar
- `slide-01-ANIMADO.mp4` va PRIMERO; luego las imágenes `slide-02…N.png` del carrusel.
- Recuerda al usuario que en Instagram un carrusel acepta video + fotos; sube el .mp4 primero.
- Deja también `slide-01.png` (estático) por si prefiere todo en imágenes.

---

## Ajuste del recorte (importante)
El offset del crop depende del aspect del video fuente:
- Fuente **3:4 (1080×1440)** → `crop=1080:1350:0:45` (quita 45px arriba y 45px abajo). **Caso normal.**
- Si usaste **9:16 (1080×1920)** → recorta más: `crop=1080:1350:0:285` (aprox; ajústalo viendo un frame).
Siempre confirma con un frame: la cara/sujeto no debe quedar cortada.

## Reglas duras / qué NO hacer
1. **`aspect_ratio` del video: `3:4`, jamás `auto`** (auto = 16:9 horizontal, inservible para 4:5).
2. **Cámara fija** en el prompt: nada de push-in/zoom; debe parecer "la misma foto que respira".
3. **Título = capa PNG transparente** compuesta con ffmpeg, nunca horneada antes de animar.
4. **Muestra la foto gancho** antes de animar (la animación cuesta créditos y tarda).
5. Output silencioso (`-an`): la portada de carrusel no necesita audio.
6. Esta skill SOLO hace la portada en video. El guion → `carrusel-viral`; los slides PNG →
   `carrusel-render` / `clonador-carrusel`.

## Convenciones
- Recursos intermedios en `recursos/` (cover.png, cover_anim_raw.mp4, overlay.html, title-overlay.png).
- Salida final junto a los slides PNG del carrusel: `slide-01-ANIMADO.mp4`.
- Cara del usuario: ver memoria `feedback_avatar_imagen` (identity-emphasis, no Soul, no 1k).
