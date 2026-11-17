---
name: graficos-de-video-formula100k
description: "Convierte lo que dice un video grabado por la usuaria en una serie de gráficos scrapbook listos para superponerse sobre la toma. Parte de la transcripción con tiempos (el .srt que exporta CapCut/Premiere/DaVinci o el texto con marcas mm:ss), identifica los momentos visuales clave, propone gráficos con la estética scrapbook FÓRMULA 100K (paleta crema, washi tape, post-its, Caveat + Poppins) y los genera con Higgsfield nano_banana_2 (costo + ✅). Activar SIEMPRE que la usuaria mande un video o su transcripción y diga \"hazme gráficos\", \"saca timestamps y genera scrapbook para este reel\", \"haz los b-roll de este video\", \"convierte este video en gráficos\", \"acompáñame esta toma con scrapbook\", o cualquier variación que combine un video grabado con overlays visuales. No edita ni compone el video: entrega los PNG + plan de superposición en entregables/graficos-video/."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Pasos 1 a 3 (ffprobe, ffmpeg, mlx-whisper) NO corren aquí: mlx-whisper es solo para Mac y procesar el video es demasiado pesado para el servidor. Pide por Telegram la transcripción CON tiempos: el `.srt` que exportan CapCut, Premiere o DaVinci con subtítulos automáticos, o el texto con marcas mm:ss. Si pega texto sin tiempos, propón los momentos por orden y avisa que los timestamps son aproximados.
> - Desde el Paso 4 la skill corre igual. Paso 5: las dos preguntas van por Telegram con opciones numeradas. Paso 7: genera con el plugin de Higgsfield (`nano_banana_2`), una imagen por gráfico; antes di el costo total (N gráficos × créditos) y espera ✅. Sin Higgsfield: entrega la tabla de momentos + los prompts listos para pegar.
> - Paso 8: guarda en `entregables/graficos-video/AAAA-MM-DD_<nombre>/` los PNG y `TRANSCRIPCION.md`; manda las imágenes por Telegram como archivo (no como foto, para que no las comprima) y el plan de superposición. `job_display` y `open "$DEST"` no aplican.
> - La superposición sobre la toma la hace la usuaria en su editor: tú no compones el video.
> - La paleta crema + Caveat/Poppins es el scrapbook F100K por defecto; si `cerebro/` trae la identidad visual de la usuaria (colores, tipografías), úsala en su lugar.

---

# Gráficos de Video — FÓRMULA 100K

Pipeline automatizado para convertir un video grabado por el usuario en una serie de gráficos scrapbook listos para superponer sobre la toma.

## Cuándo activar

Activar cuando se cumplan AMBAS condiciones:
1. El usuario provee un archivo de video local (`.mov`, `.mp4`, `.m4v`, `.mkv`).
2. Pide gráficos / scrapbook / b-roll / overlays / acompañamiento visual / timestamps.

Frases gatillo: "transcribe y hazme gráficos", "saca timestamps de este video", "scrapbook para este reel", "convierte este video en gráficos", "acompáñame la toma", "graficos sobre este video".

## NO activar para

- Stories de Instagram diseñadas a pantalla completa → usar `historias-a-imagenes-nanobanana`.
- Carruseles de IG → usar `carrusel-render-formula100k`.
- Miniaturas de YouTube → usar `miniatura-youtube-formula100k`.
- Generar UN solo gráfico aislado sin video fuente → usar `banana` o Higgsfield directo.

## Pipeline (8 pasos)

### Paso 1 — Validar input

Verifica que el archivo existe y es un video procesable.

```bash
file "$VIDEO_PATH"  # debe decir "ISO Media" o similar
ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$VIDEO_PATH"
```

Si la duración supera 5 minutos (300s), avisa al usuario que la transcripción tomará más y confirma antes de seguir.

### Paso 2 — Extraer audio

```bash
ffmpeg -i "$VIDEO_PATH" -vn -acodec mp3 -ar 16000 -ac 1 -y /tmp/audio_video.mp3
```

### Paso 3 — Transcribir con mlx-whisper

Apple Silicon nativo, no necesita API:

```bash
uvx --from mlx-whisper mlx_whisper /tmp/audio_video.mp3 \
  --model mlx-community/whisper-large-v3-mlx \
  --language es \
  --output-format srt \
  --output-dir /tmp
```

Lee `/tmp/audio_video.srt`. La salida en `stdout` ya viene con `[mm:ss.ms --> mm:ss.ms]` por segmento.

Si `uvx` no está disponible, fallback a la skill `transcripcion-youtube-formula100k` para subir el video como referencia o pedir al usuario un upload.

### Paso 4 — Analizar y proponer gráficos

Lee la transcripción y agrupa segmentos en **4 a 8 momentos visuales** (1 gráfico por momento). Criterios:

- Cada momento dura entre 8 y 20 segundos típicamente.
- Detecta cambios de idea / pivots argumentativos como puntos de corte.
- Cada gráfico debe tener UN concepto visual claro (no acumular ideas).
- Si el video dura <30s → 2-3 gráficos. Si dura 30-90s → 4-6. Si >90s → 6-8.

Para cada gráfico propon:
- **Timestamp** (entrada y salida en mm:ss)
- **Concepto visual** (en una línea)
- **Texto principal** que va en el post-it / sticker
- **Tipo de elemento dominante** (pantalla simulada de IG, comparación, diagrama, sello, números grandes, etc.)

### Paso 5 — Confirmar plan con el usuario

Muestra una tabla con timestamps + concepto + texto y pregunta:

```
AskUserQuestion:
  - Aspect ratio del set de gráficos (default: 1:1 cuadrado)
    → 1:1 (Cuadrado, mejor para tomas verticales)
    → 16:9 (Horizontal, mejor para tomas horizontales / pantalla)
  - ¿El plan de gráficos te encaja o quieres ajustar?
    → Sí, generar tal cual
    → Modificar antes de generar
```

**Regla establecida:** para overlays sobre toma se usa 1:1 o 16:9. NO ofrecer 9:16 salvo que el usuario pida explícitamente full-screen. Si en sesiones anteriores el usuario fijó otra preferencia, respétala.

### Paso 6 — Construir prompts con brandkit FÓRMULA 100K

Cada prompt sigue esta plantilla (en inglés, da mejores resultados con nano_banana_2):

```
A scrapbook collage page in [ASPECT_RATIO_DESC] format on a cream beige textured paper background.
[ELEMENTO PRINCIPAL — ej: simulated Instagram screenshot showing X / two polaroids comparing X /
3x3 grid of bot profiles / inverted pyramid diagram / giant number comparison].
[TEXT POST-IT: large [color] sticky post-it note tilted slightly with bold handwritten Caveat font
text "[TEXTO EN ESPAÑOL NEUTRO]"].
[ACCENTS: washi tape (color), hand-drawn arrows in marker, small stickers, slight shadows under
each layered element].
Composition: layered scrapbook style, paper texture, slight tape edges, soft shadows.
FORMULA 100K scrapbook aesthetic — cream palette with [accent colors] accents, handwritten Caveat
+ bold Poppins typography mix. Bold readable text. High quality print-ready scrapbook page.
```

**Reglas críticas del brandkit:**
- Fondo: papel crema/beige texturizado.
- Tipografías: Caveat (handwritten para títulos) + Poppins Bold (para datos/números).
- Paleta: crema + un acento por gráfico (amarillo, rosa, mint green, rojo para alertas).
- Elementos: post-its tilteados, washi tape (rosa, mint, amarillo, rojo según contexto), polaroids con borde blanco grueso, flechas dibujadas a marcador, pequeños stickers/sparkles.
- Capturas de IG simuladas cuando aplique (perfil, reel, comentarios) — pero NUNCA dibujar la UI completa de IG, solo lo necesario.
- Texto SIEMPRE en español neutro (tú, no vos / tienes, no tenés / aquí, no acá). 

**Aspect ratios:**
- `1:1` → "square format"
- `16:9` → "horizontal landscape format"

### Paso 7 — Generar en paralelo con Higgsfield

Llama a `mcp__higgsfield__generate_image` UNA vez por gráfico, EN PARALELO (todas las llamadas en un solo mensaje):

```json
{
  "params": {
    "model": "nano_banana_2",
    "aspect_ratio": "1:1",
    "prompt": "<prompt construido en paso 6>"
  }
}
```

Captura todos los `id` (UUIDs) que devuelve el server.

Luego llama `mcp__higgsfield__job_status` con `sync: true` para CADA uno (también en paralelo). Esto bloquea hasta ~25s por imagen pero permite que se completen concurrentemente.

Captura el `rawUrl` de cada `results`.

### Paso 8 — Descargar, guardar y entregar

**Crear carpeta destino** (convención obligatoria):

```bash
DEST="entregables/graficos-video/$(date +%Y-%m-%d)_<nombre_descriptivo>"
mkdir -p "$DEST"
```

`<nombre_descriptivo>` debe ser corto y derivado del tema del video (ej: `algoritmo_instagram_scrapbook`, `como_vender_en_dm`, `objeciones_precio`). Usa snake_case sin acentos ni espacios.

**Descargar todos los PNG en paralelo:**

```bash
curl -sSL "$URL_1" -o "$DEST/G1_<slug>_<mmss-mmss>.png" &
curl -sSL "$URL_2" -o "$DEST/G2_<slug>_<mmss-mmss>.png" &
...
wait
```

Convención de nombre: `G<n>_<slug-corto>_<inicio>-<fin>.png` donde inicio/fin son `mm-ss`. Ej: `G1_bendicion_00-00-00-06.png`.

**Generar `TRANSCRIPCION.md`** en la misma carpeta con:
- Header: video fuente, duración, fecha
- Tabla de transcripción completa con timestamps + asignación a cada gráfico
- Tabla "plan de superposición" con entrada/salida/duración de cada gráfico
- Tip de edición (fade in/out + scale 0.95→1.0 en 0.3s)

**Mostrar al usuario:**
1. Llamar `mcp__higgsfield__job_display` con todos los UUIDs para visualización widget.
2. `open "$DEST"` para abrir el Finder.
3. Resumen en chat: tabla con archivo + timestamp + concepto.

## Iteración

Si el usuario pide regenerar un gráfico específico ("regenera el G3 con X"):
1. Construye el nuevo prompt aplicando el cambio.
2. `generate_image` solo de ese gráfico.
3. Espera con `job_status sync:true`.
4. Sobreescribe el archivo en la carpeta destino con el mismo nombre.
5. Confirma al usuario.

NO regenerar todos cuando solo se pide cambiar uno.

## Errores y fallbacks

| Error | Acción |
|-------|--------|
| Video no existe / corrupto | Pide al usuario que verifique la ruta. |
| ffmpeg falla | Verifica `which ffmpeg` (esperado: `/opt/homebrew/bin/ffmpeg`). |
| `uvx` no disponible | Fallback: pide instalar `uv` (`brew install uv`) o usa un servicio externo (`mcp__claude_ai_TRANSCRIPTOR_MCP_V_2__authenticate`). |
| Whisper alucina ("Subtítulos por la comunidad de Amara") | Re-correr con `--temperature 0.2` o pedir al usuario validar segmentos cortos. |
| `generate_image` retorna error | Reintentar 1 vez. Si persiste, mostrar error y proponer ajuste de prompt (puede ser por safety filters). |
| `job_status` queda pendiente >60s | Reintentar con `sync: true`. Si sigue, usar `mcp__higgsfield__balance` para verificar créditos. |
| Carpeta destino existe | Sobreescribir solo si el usuario confirma; si no, agregar sufijo `_v2`. |

## Atajo conversacional

Si el usuario solo dice "/graficos-video <ruta>" o "transcribe y arma gráficos para este: <ruta>", asume:
- Aspect ratio: 1:1
- Estilo: scrapbook FÓRMULA 100K estándar
- Cantidad: la que el contenido sugiera (4-8)
- Saltar paso 5 si el video es corto (<60s) y el plan es claro — generar directo y mostrar resultado.

Para videos >60s o con temas sensibles (lanzamientos, sales pages), SIEMPRE confirma el plan en paso 5 antes de gastar generaciones.
