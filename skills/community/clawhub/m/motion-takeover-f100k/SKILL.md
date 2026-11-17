---
name: motion-takeover-f100k
description: "Planea TAKEOVERS faceless a pantalla completa para un video de YouTube 16:9 grabado con tu cara, estilo 'Claude Routines': en los momentos clave la pantalla se llena de mockups paso a paso, trazos SVG e imágenes IA, y luego vuelve tu cara. A partir del .srt del video ya cortado arma el plan de 2 carriles (takeovers + overlays ligeros), renderiza cada takeover como PNG 1920×1080 y, si quieres movimiento, lo anima con Higgsfield. Entrega las piezas + una hoja de montaje con el segundo exacto de cada takeover para ponerlas encima en tu editor. En este agente no edita ni compone el video. Activar cuando se diga: 'takeovers para mi video', 'motion graphics fullscreen tipo el video que te mandé', 'mockups paso a paso', 'estilo Claude Routines', 'cortes a gráfica'. NO usar para 9:16 (motion-reels-f100k)."
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion, Skill"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - **No corren aquí:** Paso 0 (corte semántico), transcripción con Whisper, `hyperframes render`, la composición ffmpeg del Paso 7 ni `verify_audio_sync.py`. Nada se monta sobre su video.
> - Entrada: la usuaria corta su video en su editor y te manda por Telegram el `.srt` de ESA versión cortada (los tiempos tienen que coincidir) + 1 captura de un cuadro con su cara. Con eso armas `motion_board.json` (Paso 4) y lo apruebas con ella antes de gastar nada.
> - Cada takeover: llena `templates/takeover-template.html` y renderízalo a PNG 1920×1080 con Chromium headless; antes de la captura adelanta la animación al final con `window.__timelines['takeover'].progress(1)` para que se vean mockups y trazos completos. Imágenes de escena con el plugin de Higgsfield (`nano_banana_2`, 16:9).
> - Si quiere movimiento: anima cada PNG con Higgsfield imagen → video (16:9, movimiento suave, que no deforme el texto), con la duración del takeover. Costo total → ✅ → generar. Revisa que el texto siga legible; si se deforma, entrega el PNG.
> - Overlays de modo cara: PNG con fondo transparente (Chromium, fondo omitido) o `capturas-tutorial-formula100k`. Sin fondo verde.
> - Entrega en `entregables/takeover-<fecha>/`: `motion_board.json`, `HOJA_MONTAJE.md` (inicio y fin de cada takeover en el video cortado, «colócalo encima, opaco, sin mover la pista de voz») y un `.zip` con PNG/MP4, por Telegram.

---

# Motion Takeover para YouTube — FÓRMULA 100K

Toma un **video grabado con la cara del usuario (16:9)** y produce un `video_final.mp4` que **alterna dos modos**:

- **Modo cara** → overlays ligeros en zonas seguras (hereda los 6 templates de `motion-youtube-f100k`).
- **Modo takeover** → en los momentos clave la pantalla **se llena** de motion graphics faceless (SVG paths que se dibujan + mockups paso a paso + imágenes IA/capturas). La voz sigue debajo; luego regresa la cara.

Reproduce el lenguaje visual del video de referencia "Claude Routines Just Launched" (`KpG2yBi5I10`).

Formato: **1920×1080 (16:9)** @30fps.

---

## ⛔ Reglas duras (NO negociables)

1. **El audio NUNCA se desfasa.** Los takeovers se montan como **overlay OPACO encima de la base** con `enable='between(t,inicio,fin)'`. **JAMÁS** se corta ni concatena el video base. La base (`_source_cut.mov`) no cambia de duración una vez cortada. Verificación ffprobe post-render OBLIGATORIA (Paso 8). *(memoria: render-audio-sin-desfase)*
2. **Corte semántico SIEMPRE** como Paso 0. *(memoria: editor-corte-semantico)*
3. **16:9 horizontal** siempre (nunca 9:16). *(memoria: youtube-horizontal-16x9)*
4. **NO stock.** Imágenes solo banana/Higgsfield o capturas de la usuaria. *(memoria: no-stock-imagenes)*

---

## Cuándo activar

- "edita este video con takeovers" / "cortes a gráfica a pantalla completa"
- "motion graphics fullscreen tipo el video que te mandé" / "estilo Claude Routines"
- "ponle SVG paths a pantalla completa", "mockups paso a paso"
- Un video grabado con cara (16:9) que quiera enriquecer con takeovers faceless

## NO activar para

- Videos 9:16 (reels/shorts) → `motion-reels-f100k`
- Overlays ligeros SIN takeover fullscreen → `motion-youtube-f100k`
- Solo corte de silencios/muletillas → `editor-video-formula100k`
- Carruseles → `carrusel-render-formula100k`

---

## Paso 1 — Onboarding (auto-install) (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

Reutiliza **íntegro** el bloque de instalación de `motion-youtube-f100k` (Node 22+, `hyperframes` CLI, paquetes `@hyperframes/*`, `ffmpeg`, `yt-dlp`, Whisper). No lo dupliques: ejecútalo y confirma con `hyperframes doctor` (Chrome + FFmpeg ✓) y `hyperframes --version` (≥0.7).

```bash
command -v hyperframes &>/dev/null || npm install -g hyperframes
command -v ffmpeg &>/dev/null || brew install ffmpeg
hyperframes doctor
```

Definir variables:
- `$VIDEO_SRC` — ruta al video grabado (archivo local con cara).
- `$DEST` — carpeta de trabajo (la del archivo, o `entregables/takeover-$(date +%Y%m%d)/`).
- `$SKILL` — `skills/motion-takeover-f100k` (templates + scripts de esta skill).
- `$OUTPUT` — `$DEST/video_final.mp4`.
- `$USER_SHOTS` — `$DEST/USER/` (capturas reales opcionales que deje el usuario).

---

## Paso 0 — Corte semántico (OBLIGATORIO, va PRIMERO) (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

Los takeovers y overlays se cronometran sobre el transcript y se incrustan sobre el video. Si cortaras después, los cortes caerían encima de las animaciones. Por eso el recorte va aquí y **el resto del pipeline trabaja siempre sobre el video ya limpio**.

```bash
CUT_SCRIPT="skills/editor-video-formula100k/scripts/cut_silences_and_fillers.py"
[ -f "$CUT_SCRIPT" ] || echo "⚠ Falta cut_silences_and_fillers.py — instala editor-video-formula100k"
python3 -c "import numpy" 2>/dev/null || pip3 install --quiet numpy 2>/dev/null || true

mkdir -p "$DEST"
python3 "$CUT_SCRIPT" "$VIDEO_SRC" "$DEST"

# 🔑 La base SAGRADA a partir de aquí:
VIDEO_SRC="$DEST/_source_cut.mov"    # video+audio limpio; NO se vuelve a cortar
echo "✅ Base cortada: $VIDEO_SRC"
ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$VIDEO_SRC"
```

El corte deja `captions.json` (word-level, sobre la línea cortada). Se reutiliza en el Paso 2.

> Si el usuario insiste en "ya está editado, no cortes" → saltar, pero **advertir** que el corte semántico es la regla de la casa. Por defecto SIEMPRE se corta.

---

## Paso 2 — Transcripción (reutiliza el corte)

```bash
if [ -f "$DEST/captions.json" ]; then
  python3 - << 'EOF'
import json
words = json.load(open("$DEST/captions.json"))
segments = [{'text': w['word'].strip(), 'start_ms': int(w['start']*1000), 'end_ms': int(w['end']*1000)} for w in words]
json.dump(segments, open("$DEST/transcript.json", 'w'), indent=2, ensure_ascii=False)
print(f"♻️  {len(segments)} palabras reutilizadas del corte (sin re-transcribir)")
EOF
fi
```

Si por alguna razón no hay `captions.json`, usa el bloque Whisper de `motion-youtube-f100k` Paso 2.

---

## Paso 3 — Analizar la cara en el frame (para los overlays de modo cara)

Idéntico a `motion-youtube-f100k` Paso 1.5: extrae un frame medio, léelo con `Read`, determina `SUBJECT_X`/`SUBJECT_Y` y calcula `SAFE_PILL_CSS`, `SAFE_CARD_CSS`, `SAFE_FLOAT_CSS`. Estas variables se usan **solo** para los overlays de modo cara (los takeovers cubren todo el frame, no necesitan zona segura).

```bash
DURATION=$(ffprobe -v error -show_entries format=duration -of default=nokey=1:noprint_wrappers=1 "$VIDEO_SRC")
MIDPOINT=$(python3 -c "print(round($DURATION * 0.5, 2))")
ffmpeg -ss $MIDPOINT -i "$VIDEO_SRC" -vframes 1 -q:v 2 /tmp/frame_cara.jpg 2>/dev/null
```

---

## Paso 4 — Auto-clasificación en 2 CARRILES

Recorre el transcript y asigna cada momento a un carril. **Objetivo: 3–6 takeovers** por video (los momentos más fuertes), el resto overlays ligeros.

### Señales de TAKEOVER (pantalla completa)

| Escena de takeover | Señales en el guion | Qué se construye |
|--------------------|---------------------|------------------|
| **`steps`** — secuencia de pasos | "los 3 pasos", "primero… luego… al final", enumeración fuerte | mockups numerados 1→2→3 conectados por SVG paths |
| **`ui`** — demo de herramienta | "te muestro", "abres Claude/Canva/Notion", "aquí pones…" | mockup de navegador grande (con captura de `USER/` si existe) + path que señala |
| **`compare`** — antes/después grande | "antes me tomaba X, ahora Y", contraste central del video | dos paneles fullscreen + trazo que los divide |
| **`image`** — metáfora / escena | "imagina que…", concepto abstracto, gancho visual | imagen IA (banana/Higgsfield) fullscreen + título + path de subrayado |
| **`bignum`** — dato protagonista | una cifra que merece toda la pantalla ("+10.000", "3 horas → 20 min") | número gigante animado + path circular |

### Señales de OVERLAY (modo cara) — hereda `motion-youtube-f100k`

pill labels, comparison card, floating UI, chapter card, kinetic word, quote pull, en zona segura. **Mantiene la regla de densidad: 1 motion graphic cada 5s** cuando la cara está en cuadro.

### Motion board de 2 carriles

Genera `$DEST/motion_board.json`:

```json
[
  { "lane": "overlay", "type": "pill_labels", "start_ms": 3000, "duration_ms": 4000, "labels": ["sin código","desde cero"] },
  { "lane": "takeover", "scene": "steps", "start_ms": 42000, "duration_ms": 8000,
    "title": "Los 3 pasos, sin código", "kicker": "EL SISTEMA",
    "steps": [
      {"h":"Escribe la rutina","p":"Le dices en lenguaje natural qué quieres."},
      {"h":"Programa la hora","p":"Corre sola, sin que tú estés."},
      {"h":"Recibe el resultado","p":"Tu contenido listo al despertar."}
    ],
    "paths": ["connector","connector","circle","check"] },
  { "lane": "takeover", "scene": "image", "start_ms": 95000, "duration_ms": 6000,
    "title": "Tu equipo invisible", "image_hint": "un escritorio vacío al amanecer, luz cálida, laptop encendida sola" }
]
```

Presenta el board (los dos carriles, con los takeovers marcados 🎬) y pide aprobación:

```
AskUserQuestion:
"Este es el plan. 🎬 = takeover fullscreen, • = overlay ligero sobre tu cara.
 ¿Lo genero tal cual, ajustas algún takeover, o quieres dirección manual?"
Opciones: ["Generar tal cual", "Ajustar takeovers", "Dirección manual"]
```

---

## Paso 5 — Generar los assets de cada takeover

Para cada entrada `lane:"takeover"`:

1. **Mockups + paths (SIEMPRE)** — se construye el HTML de la escena a partir del template firma (§Firma visual). Los `paths` se eligen de la librería de gestos.
2. **Imágenes IA (cuando la escena es `image`/`bignum` o el guion pide una escena real):**
   - Genera con la skill **`banana`** (Gemini Nano Banana) o el MCP **Higgsfield** (`mcp__higgsfield__generate_image`, `nano_banana_2`, 16:9).
   - Guarda en `$DEST/assets/` y referénciala como `<img src="../assets/xxx.png">` dentro de la escena.
   - Respeta la identidad de marca del usuario (memoria: avatar-imagen) si aparece su cara.
3. **Capturas reales (`USER/`):** si existe `$DEST/USER/*.png|jpg`, slottéala **dentro del `.mock .body`** de una escena `ui` (reemplaza el placeholder de texto por `<img>`), para mostrar el software real.

> Regla: NADA de stock. Si no hay imagen IA ni captura, la escena se resuelve 100% vectorial (mockups + paths + tipografía).

---

## Firma visual — SVG paths fullscreen + mockups paso a paso

**El corazón de la skill.** Parte del template `templates/takeover-template.html` de esta skill (ya probado: fondo de marca opaco 1920×1080, kicker+título, 3 mockups numerados en secuencia, y la capa `<svg id="paths">`).

### Cómo se dibujan los paths (line-draw)

Cada `<path>`/`<polyline>` se anima con GSAP vía `stroke-dashoffset`. El helper del template lo hace solo:

```js
function drawIn(sel, at, dur, ease) {
  const el = document.querySelector(sel);
  const len = el.getTotalLength ? el.getTotalLength() : 1000;
  gsap.set(el, { strokeDasharray: len, strokeDashoffset: len });
  tl.to(el, { strokeDashoffset: 0, duration: dur, ease: ease || "power2.inOut" }, at);
}
```

### Librería de gestos (elige por escena)

| Gesto | `path` d / forma | Uso |
|-------|------------------|-----|
| **connector + flecha** | curva Bézier entre dos mockups + `<polyline>` de punta | unir pasos 1→2→3 (escena `steps`) |
| **subrayado** | línea recta/curva bajo una palabra | resaltar el título o una palabra clave |
| **círculo a mano** | Bézier cerrada irregular | encerrar el mockup/resultado importante |
| **check ✓** | `<polyline>` de 3 puntos | confirmar paso/resultado |
| **línea ambiente** | curva suave que cruza el fondo | movimiento sutil durante toda la escena |
| **flecha señaladora** | línea + punta hacia un punto del mockup | escena `ui`, apuntar a un botón/campo |

### Reglas de la escena de takeover

- **Fondo OPACO de marca** — CARBÓN `#14110F` (default) o CREMA `#F5EDE0` (variables `--bg/--ink/--accent` del template). **NUNCA `#00ff00`** aquí (los takeovers no se keyean).
- Mockups entran en secuencia (`back.out`), badges numerados con `back.out(2)`.
- Paths se dibujan **conforme** entran los mockups, no todos al inicio.
- Salida suave de toda la escena en los últimos ~0.6s.
- `data-composition-id="takeover"`, `window.__timelines["takeover"] = tl`.
- Duración de la escena = `duration_ms` del board.

Genera una carpeta por takeover: `$DEST/takeovers/takeover-N/index.html`.

---

## Paso 6 — Render de cada composición (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

### Overlays de modo cara (green screen keyed)

Igual que `motion-youtube-f100k` Paso 5–6: `$DEST/overlays/index.html` con `body{background:#00ff00}`, todos los overlays keyed.

```bash
cd "$DEST/overlays" && hyperframes render --format mp4 -o "$DEST/overlays/overlays.mp4"
```

### Takeovers (OPACOS, uno por escena)

```bash
for d in "$DEST"/takeovers/takeover-*/ ; do
  n=$(basename "$d")
  (cd "$d" && hyperframes render --format mp4 -o "$DEST/takeovers/$n.mp4")
done
```

> ⚠️ SIEMPRE `--format mp4` (WebM ignora el CSS background). Los takeovers son **opacos** → NO llevan colorkey.

---

## Paso 7 — Composición ffmpeg AUDIO-SAFE (⛔ el punto crítico) (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

**Principio:** la base (`_source_cut.mov`) es intocable en duración. Los overlays de cara se keyean encima; **cada takeover es un overlay OPACO activado solo en su ventana** con `enable='between(t,inicio,fin)'`. Como el timeline base nunca se corta ni concatena, **el audio no puede desfasarse**.

Construye el `filter_complex` dinámicamente. Ejemplo con 1 capa de overlays keyed + 2 takeovers (`t=42–50s` y `t=95–101s`):

```bash
ffmpeg -y \
  -i "$VIDEO_SRC" \
  -i "$DEST/overlays/overlays.mp4" \
  -i "$DEST/takeovers/takeover-1.mp4" \
  -i "$DEST/takeovers/takeover-2.mp4" \
  -filter_complex "
    [0:v]fps=30,format=yuv420p[base];
    [1:v]colorkey=0x00ff00:0.35:0.15[ovl];
    [base][ovl]overlay=0:0:eof_action=pass[v1];
    [2:v]setpts=PTS-STARTPTS+42/TB[tk1];
    [v1][tk1]overlay=0:0:enable='between(t,42,50)':eof_action=pass[v2];
    [3:v]setpts=PTS-STARTPTS+95/TB[tk2];
    [v2][tk2]overlay=0:0:enable='between(t,95,101)':eof_action=pass[v]
  " \
  -map "[v]" -map 0:a \
  -c:v libx264 -crf 18 -preset fast \
  -c:a copy \
  "$OUTPUT"
```

Notas clave:
- Cada takeover se **reubica en su timestamp** con `setpts=PTS-STARTPTS+START/TB` y se activa con `enable='between(t,START,END)'`. Fuera de su ventana no se ve → tapa la cara solo cuando toca.
- `-map 0:a` + `-c:a copy` = **el audio original pasa intacto**. (Si la fuente es `.mov` con stream de datos, usa `-map 0:1`.)
- **NO** uses `-movflags +faststart` (cuelga) ni `-r 30` al final (rompe el timing).
- Para N takeovers, encadena más bloques `[k:v]setpts…[tkK]; [vPrev][tkK]overlay…enable…[vK]`.

Generador del filtro (opcional, para muchos takeovers): construye el string en Python leyendo `motion_board.json` (entradas `lane:"takeover"` ordenadas), asignando índices de input `2,3,4…` y encadenando `[v1]→[v2]→…`.

---

## Paso 8 — Verificación (⛔ audio primero) (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
# 1) AUDIO SYNC — guardián no negociable
python3 "$SKILL/scripts/verify_audio_sync.py" "$OUTPUT" --source "$VIDEO_SRC"
#   exit 0 = ✅ SYNC OK   |   exit 1 = ❌ NO publicar, revisar Paso 7
```

Checklist visual:
- [ ] **Audio sincronizado** (`verify_audio_sync.py` → SYNC OK, Δ < 40ms) — chequear también lip-sync en un frame hablado.
- [ ] Cada takeover **cubre todo el frame** en su ventana y desaparece al terminar (la cara vuelve limpia).
- [ ] SVG paths se **dibujan** (no aparecen de golpe); mockups entran en secuencia.
- [ ] Overlays de modo cara no tapan la cara (zonas del Paso 3).
- [ ] Fondo del takeover **opaco** de marca (no verde, no negro).
- [ ] Densidad OK en modo cara (sin huecos >5s).
- [ ] Imágenes = IA/capturas (nunca stock).

```bash
open "$OUTPUT"
```

---

## Estructura de archivos generados

```
$DEST/
├── _source_cut.mov            ← base SAGRADA (Paso 0), no se re-corta
├── captions.json / transcript.json
├── motion_board.json          ← 2 carriles (overlay + takeover)
├── assets/                     ← imágenes IA / capturas procesadas
├── USER/                       ← (input) capturas reales que dejal usuario
├── overlays/
│   ├── index.html (#00ff00)   ← overlays modo cara (keyed)
│   └── overlays.mp4
├── takeovers/
│   ├── takeover-1/index.html (OPACO)   ← escena fullscreen
│   ├── takeover-1.mp4
│   └── takeover-2/ …
└── video_final.mp4            ← OUTPUT
```

---

## Errores frecuentes / gotchas

| Síntoma | Causa | Fix |
|---------|-------|-----|
| **Audio desfasado** | se usó cut/concat en vez de overlay | Paso 7: takeover = `overlay … enable='between'`, base intacta |
| Takeover fondo negro | filter_complex sin conversión de la base | `fps=30,format=yuv420p[base]` primero |
| Takeover no aparece / mal tiempo | falta `setpts=PTS-STARTPTS+START/TB` | reubicar cada takeover a su timestamp |
| Overlay de cara fondo negro | WebM ignora CSS bg | render **MP4** siempre |
| Badge numerado recortado | `overflow:hidden` del mockup | badge como **hermano** del `.mock` (ver template) |
| Path no se dibuja | falta `strokeDasharray/offset` | usa el helper `drawIn()` del template |
| `No decoder for none` en MOV | stream de datos | `-map 0:1` para audio |
| ffmpeg se cuelga | `-movflags +faststart` | quitarlo |

---

## Diferencias con motion-youtube-f100k

| Aspecto | motion-youtube-f100k | motion-takeover-f100k |
|---------|----------------------|------------------------|
| Gráficas | Solo overlays en esquinas (cara siempre visible) | Overlays **+ takeovers fullscreen** que tapan la cara por ventanas |
| Firma nueva | — | **SVG paths que se dibujan** + secuencia de mockups |
| Fondo del asset | Todo green screen keyed | Overlays keyed **+ takeovers OPACOS** de marca |
| Compositing | 1 overlay colorkey | base + colorkey + N overlays opacos con `enable=between` |
| Imágenes | No genera | banana/Higgsfield + capturas `USER/` |
| Riesgo audio | Bajo (overlay no cambia duración) | **Blindado** con verify_audio_sync.py obligatorio |

Reutiliza de motion-youtube-f100k: onboarding, análisis de cara, los 6 templates de overlay, la regla de densidad.
