---
name: pizarra-explicativa-f100k
description: "Convierte un video grabado (talking head) en un clip de PIZARRA de apoyo para pantalla dividida: lo que dice se va escribiendo, encerrando y conectando a mano. Con el .srt del video arma el mapa de 8-12 beats anclado al rubro real de quien habla, PIDE APROBACIÓN con el costo, genera un clip por beat con los presets Whiteboard Doodle o Hand Drawn de Higgsfield, los junta en un solo pizarra.mp4 y entrega un LEEME con el segundo de cada beat para alinearlo en su editor. En este agente no edita ni compone el video. Activar cuando se pida 'hazme la pizarra de este video', 'clip de pizarra para este reel', 'apoyo visual explicativo en pantalla dividida', 'motion graphics de pizarra', 'acompaña este video con una pizarra'. NO caza b-roll (recursos-de-video-formula100k)."
argument-hint: "[ruta al video] [opcional: estilo o nota]"
allowed-tools: "Bash, Read, Write, Edit, AskUserQuestion, Glob, Grep"
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - **No corren aquí:** Whisper (Paso 1), HyperFrames (Pasos 0, 3, 4 y 5), `render_pizarra.sh`, el HEVC con alfa ni la previsualización del montaje. La plantilla y las trampas de HyperFrames no vienen en este paquete.
> - Paso 1: pídele el `.srt` del video ya cortado (CapCut: Subtítulos automáticos → Exportar). Los tiempos de cada beat salen de ahí; corrige los errores de transcripción igual que dice la skill.
> - Paso 2 igual: mapa de 8-12 beats, qué se dibuja en cada uno, y **aprobación por Telegram antes de gastar**. Suma el costo total en Higgsfield (clips × duración) al mapa.
> - Generación: un clip por beat con el preset explainer **Whiteboard Doodle** o **Hand Drawn** del plugin de Higgsfield (`get_explainer_presets` → `resolve_explainer_preset`), duración = la del beat. Pocas palabras por beat (1-4): la IA deforma el texto largo; revisa cada clip y regenera el que salga con letras rotas.
> - Junta los clips en orden con ffmpeg concat simple (`ffmpeg -f concat -safe 0 -i lista.txt -c copy pizarra.mp4`; todos del mismo formato y fps). Sin alfa, sin audio, sin subtítulos, sin montaje sobre su video.
> - Entrega en `entregables/pizarra/<fecha>_<slug>/`: `pizarra.mp4`, los clips sueltos y `LEEME.md` con la tabla de beats (segundo de entrada de cada clip) para que ella la alinee en pantalla dividida en su editor. Por Telegram; si pesa más de 50 MB, manda los clips por separado.

---

# Pizarra Explicativa — FÓRMULA 100K

Convierte una toma hablando a cámara en el clip de pizarra que la acompaña en pantalla dividida: lo que dice se va **escribiendo, encerrando, tachando y conectando a mano** al ritmo exacto de su voz.

## 🧭 ANCLAJE DE RUBRO

**Antes de escribir una sola palabra en la pizarra, identifica el rubro real de quien habla** (escúchalo en la transcripción; si no queda claro, pregúntalo).

Todo el texto de la pizarra sale de SU vocabulario, no del de marketing. El método de construcción es de F100K; **el rubro es de la usuaria**. Si vende jabón artesanal, la pizarra habla de saponificación y curado, no de "pilares de contenido". No traigas ejemplos de otro nicho ni jerga de marketing si su nicho es otro. Traduce el tecnicismo en su primera mención en vez de borrarlo.

La prueba: ¿esta pizarra seguiría teniendo sentido si quien habla fuera formuladora cosmética? Si solo funciona para una creadora de contenido, está mal anclada.

## Cuándo activar

Ambas condiciones:
1. Se provee un archivo de video local (`.mov`, `.mp4`, `.m4v`).
2. Se pide pizarra / apoyo explicativo / pantalla dividida / anotación a mano / motion graphics que sigan la explicación.

## NO activar para

- Editar el video final con cortes y subtítulos → `editor-video-formula100k`.
- Cazar b-roll o recursos de stock → `recursos-de-video-formula100k`.
- Gráficos scrapbook sueltos por timestamp → `graficos-de-video-formula100k`.
- Overlays de YouTube 16:9 → `motion-youtube-f100k`.

---

## Paso 0 · Comprobar el terreno (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
hyperframes --version          # necesita >= 0.7.9
which ffmpeg whisper
ffprobe -v error -show_entries format=duration -show_entries stream=width,height,r_frame_rate \
  -of default=noprint_wrappers=1 "$VIDEO"
```

Anota **duración, ancho, alto y fps**. Todo lo demás se deriva de ahí.

## Paso 1 · Transcribir con tiempos palabra por palabra (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
WD="<scratchpad>/pizarra"; mkdir -p "$WD"
ffmpeg -y -v error -i "$VIDEO" -vn -ac 1 -ar 16000 "$WD/audio.wav"
whisper "$WD/audio.wav" --model small --language Spanish \
  --word_timestamps True --output_format all --output_dir "$WD"
```

Si el video vive en Google Drive (CloudStorage), la primera lectura descarga el archivo: lánzalo en segundo plano y no lo des por colgado.

Lee `audio.json` y saca los tiempos de las **palabras clave**, no de los segmentos. Un trazo que cae 300 ms tarde se nota; uno que cae sobre la palabra exacta se siente mágico.

**Corrige los errores de Whisper** antes de escribirlos en la pizarra (nombres de marca y tecnicismos son los que más falla: "Cloud"→Claude, "quiropráfico"→quiropráctico). Deja constancia de las correcciones en el LEEME.

## Paso 2 · Mapa de beats → **CHECKPOINT**

Agrupa la transcripción en 8-12 beats. Para cada uno: tiempo, qué dice, qué se dibuja, con qué pieza.

Reparte los beats en **cuadrantes** de un lienzo grande. Un cuadrante ≈ el cuadro de la pizarra, así la cámara encuadra uno entero sin cortar nada.

| Lo que dice | Pieza |
|---|---|
| Niega / descarta / "no hagas esto" | `hw-underline` estilo **strike** (tachón) |
| Un número o concepto que es el remate | `hw-callout-circle` (con `scribble` si es una palabra corta y grande) |
| Una lista de conceptos hermanos | `hw-box-label` en columna o rejilla |
| Un proceso, "primero… luego…" | `hw-pipeline` o cajas + `hw-arrow` |
| Señala algo concreto en pantalla | `yt-circle-pointer` |
| "aquí está la clave" | `yt-feather-highlight` |
| Crecimiento / resultado | `hw-arrow` curva `swoop` |

**PARA aquí y enseña el mapa.** El render tarda ~13 min; un beat mal colocado descubierto después cuesta esos 13 min otra vez. Usa AskUserQuestion o una tabla, y pide aprobación antes de construir.

Pregunta en este punto lo que cambie el trabajo:
- **Altura del clip** (por defecto 45 % del alto del video: 864 px en un 1080×1920).
- **Superficie**: papel crema opaco con borde a mano (por defecto), solo trazos sobre alfa, o pizarrón oscuro.
- **fps**: 30 por defecto. El temblor a mano ("boil") se ve *mejor* a 30 y el render tarda la mitad; se mezcla sin problema con una línea de tiempo a 60.

## Paso 3 · Construir la composición (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
HYPERFRAMES_SKIP_SKILLS=1 hyperframes init pizarra --example blank --non-interactive --skip-transcribe
cd pizarra
for b in hw-boil hw-callout-circle hw-arrow hw-underline hw-box-label hw-pipeline \
         yt-camera-move yt-feather-highlight yt-circle-pointer; do
  hyperframes add "$b" </dev/null
done
```

Copia `templates/composicion_base.html` de esta skill a `index.html` y rellena el bloque `CONTENIDO` y el bloque `LÍNEA DE TIEMPO`. La plantilla ya trae resueltos:

- Los helpers del kit (`hwBoil`, `hwCalloutBuild`, `hwBoxOn`, `hwMarkPath`, `ytCameraMove`…).
- **La matemática de la cámara** (`camXY`): le pasas una coordenada del lienzo y un zoom, y centra ese punto en el cuadro. No la vuelvas a derivar.
- La hoja de papel con textura, borde dibujado a mano y alfa por fuera.
- Los constructores `txt() box() mark() arrow() callout() ptr() group()`.
- `settle()` para atenuar al 32 % lo ya explicado.

`hyperframes add` **se traga la cola por stdin**: pasa `</dev/null` a cada comando o el bucle muere en silencio tras el primero.

## Paso 4 · Verificar por fotogramas (obligatorio) (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
hyperframes check
hyperframes snapshot --at 3,16,29,45,58,74,83,97,104,118,130,137 --describe false -o snaps
```

**Mira las hojas de contacto de verdad.** `check` no ve lo que importa:

- Da 2 errores falsos que puedes ignorar: `content_overlap` entre líneas de texto grandes en Caveat (mide la caja de tinta, no la línea) y `escaped_container`/`container_overflow` del `#cam` (es el zoom, es intencional).
- Y **no detecta** lo que sí rompe: encuadres que cortan un título o una caja por la mitad, elipses descentradas respecto del texto que deben envolver, o restos de un beat anterior entrando por el borde.

Repite `snapshot` después de cada tanda de ajustes hasta que ninguna hoja tenga nada cortado. En la pieza real hicieron falta **cuatro rondas**.

Comprueba también el peso de los PNG: uno de menos de 5 KB es un fotograma vacío.

## Paso 5 · Renderizar y comprimir (en OpenClaw NO corre: mira el bloque 🦞 de arriba)

```bash
bash <ruta-skill>/scripts/render_pizarra.sh <dir-composicion> <video-original> <dir-salida> <slug>
```

El script hace las tres cosas en orden: ProRes 4444 con alfa → HEVC con alfa ligero → previsualización del montaje con audio, y **borra el ProRes** al terminar.

Nunca entregues el ProRes: en un clip de 2:19 a 1080×864 pesa **4,1 GB**. El HEVC con alfa pesa **100 MB** con una diferencia de color de 1,86/255 de media (invisible) y lo leen CapCut, Premiere y Final Cut en Mac.

**Verifica el alfa del archivo final** en varios puntos antes de darlo por bueno:

```bash
ffmpeg -v error -ss 29 -i salida.mov -frames:v 1 -pix_fmt rgba -y /tmp/f.png
python3 -c "from PIL import Image; im=Image.open('/tmp/f.png').convert('RGBA'); w,h=im.size; \
print('esquina',im.getpixel((3,3)),'centro',im.getpixel((w//2,h//2)),im.split()[3].getextrema())"
```

Correcto = esquina con alfa ≈ 0 y centro con alfa 255. `ffprobe` dirá `pix_fmt=yuv420p` aunque el alfa esté ahí: en HEVC va en una capa auxiliar. **No te fíes de ffprobe, decodifica un fotograma.**

## Salida

`entregables/YYYY-MM-DD_slug/`

| Archivo | |
|---|---|
| `<slug>_alfa_HEVC.mov` | El entregable. Alfa real, ~100 MB. |
| `previsualizacion_montaje.mp4` | La pizarra ya montada sobre el talking head **con audio**. Para revisar la sincronía, no para publicar. |
| `transcripcion.json` | Tiempos palabra por palabra. |
| `composicion/` | El proyecto HyperFrames, para retocar. |
| `LEEME.md` | Cómo montarlo, mapa de beats con tiempos, correcciones de transcripción, trampas resueltas. |

En el LEEME di siempre: alinear al **segundo 0** sin cortar ni mover (cada trazo está clavado a una palabra) y **no aplicar croma**, que el alfa es real.

## Trampas

Están todas en `referencia/trampas.md`, con el porqué. Las cuatro que más cuestan:

1. **Los paths SVG nacen con `opacity: 0`** y se encienden en el frame exacto en que empiezan a dibujarse. Con `stroke-linecap: round`, un path "sin dibujar" pinta igual un punto de tinta desde el frame 0 y aparece como una mota suelta en la hoja.
2. **Nunca `gsap.from({opacity:0})`** sobre un elemento que ya trae `opacity:0` en CSS: anima 0 → 0 y el frame sale vacío sin avisar. Usa `.to` para la opacidad, o `fromTo`.
3. **El zoom tiene techo**: si un grupo mide N px de lienzo, por encima de `Z = ancho_cuadro / (escala_base × N)` la cámara empieza a cortarlo. Calcula el techo antes de elegir el zoom, no después de ver el fotograma.
4. **El foco (`yt-feather-highlight`) trae `--yt-hl-dim: 0.34`**, que sobre papel crema ensucia la hoja entera y se lee como viñeta sucia. Sobre superficie clara va a **0.10**.

## Notas

- **Un solo `onUpdate` por línea de tiempo**: registra cada render por frame a través de `hwOnUpdate`, nunca con `eventCallback` directo, o los boils se pisan.
- `hwBoil` es dueño de `x/y/rotation` de sus objetivos. Las animaciones de entrada van en un envoltorio, nunca en el elemento que tiembla.
- Caveat va **empaquetada** en `assets/fonts/` con ruta **relativa a la raíz** del proyecto. Chrome headless bloquea `file://` absoluto y `../` es error de lint.
- Las flechas de `hw-arrow` siempre nacen abajo-izquierda y apuntan arriba-derecha. Para otras direcciones, envuelve en un div con `transform: scaleX(-1)` o `scaleY(-1)` — nunca rotes el elemento que tiembla.
- Si el hueco entre dos beats pasa de 5 s sin dibujo nuevo, sostenlo con una **deriva lenta de cámara** (4-5 s, sin pulso de desenfoque) en vez de inventar contenido que no dice.
- macOS no trae `timeout`. Para vigilar un render largo, lánzalo en segundo plano y sondea el archivo de salida.
