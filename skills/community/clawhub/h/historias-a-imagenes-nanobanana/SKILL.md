---
name: historias-a-imagenes-nanobanana
description: "Skill que convierte un guion de secuencia de historias (output de guionizacion-historias-formula100k) en imágenes terminadas listas para subir a Instagram Stories. Activar SIEMPRE que el usuario o un usuario pida: \"renderiza este guion de historias\", \"convierte este guion en imágenes\", \"diséñame las stories de [archivo]\", \"pasa este guion a imágenes con nanobanana\", \"genera las historias diseñadas\", \"exporta este guion a PNG\", \"haz las imágenes de mi secuencia de stories\", o cualquier variación que combine un guion de historias con la intención de tener archivos visuales finales. Usa la skill Nano Banana (Gemini) como motor por defecto, con el MCP de Higgsfield como alternativa. Se conecta con una carpeta de fotos de marca personal (la pregunta y guarda como preset) y elige automáticamente la mejor foto base por slide. Imita el estilo nativo de Instagram Stories (fuentes IG, cajas redondeadas, paleta del usuario, capas de capturas/mockups, flechas amarillas, X/✓)."
argument-hint: "<ruta al .md del guion> [--motor=gemini|higgsfield] [--fotos=<carpeta>]"
metadata: {"version": "1.0.0", "depends-on": ["guionizacion-historias-formula100k", "banana"], "mcp-optional": ["higgsfield"], "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Motor de imagen, en este orden: **Gemini directo con `GEMINI_API_KEY`** (sección 3.1 del puente) — es el mismo Nano Banana; si no hay llave, el plugin de Higgsfield (`nano_banana_2`); si no hay ninguno, entrega los prompts por historia y avisa.
> - La skill `banana` no viene en este paquete: llama al motor disponible directo.
> - Fotos de la usuaria: `cerebro/fotos/`. Si está vacía, pídele por Telegram 3 a 6 fotos suyas enviadas como archivo.
> - El preset se guarda en `cerebro/preset-historias.json`, no dentro de la skill (las actualizaciones lo borrarían).
> - Siempre: costo estimado → ✅ → generar → mandar las imágenes por Telegram y guardarlas en `entregables/historias/`.

---

# Skill: Historias a Imágenes (Nanobanana + Higgsfield)

Toma un guion de stories generado por `guionizacion-historias-formula100k` y produce imágenes PNG
listas para subir a Instagram Stories, imitando el estilo nativo de IG y el look del usuario.

---

## ⚠️ ANTES DE EMPEZAR — LEE ESTOS REFERENCIALES

Cargar SIEMPRE estos archivos antes de generar:

1. `references/parser-guion.md` — cómo parsear el .md del guion
2. `references/instagram-design-system.md` — sistema visual exacto a aplicar
3. `references/prompt-builder.md` — fórmula del prompt para generar el slide
4. `references/foto-matcher.md` — algoritmo para elegir la mejor foto del folder
5. `references/motor-selection.md` — cuándo usar Banana vs Higgsfield

No es opcional.

---

## DEPENDENCIAS

- **Skill `banana`** (Nanobanana / Gemini) — para edición de imagen base + overlay del estilo IG
- **MCP `higgsfield`** (`mcp__higgsfield__*`) — para generación de slides desde cero o con character consistency
- **Skill `guionizacion-historias-formula100k`** — provee el formato de input (.md con frontmatter + tabla)

---

## INPUT

El usuario te dará alguna combinación de:

1. **Ruta al .md** del guion: `guiones/historias/[archivo].md`
2. **Pegado del contenido** del guion directamente
3. **Carpeta de fotos** (opcional la primera vez, después se guarda como preset): `--fotos=<ruta>` o pregunta interactiva
4. **Motor preferido** (opcional): `--motor=gemini` | `--motor=higgsfield` (default: gemini)

Si no hay carpeta de fotos guardada como preset, **pregúntala al usuario antes de proceder**:

> "Para diseñar las historias necesito una carpeta con tus fotos de marca personal (Japón, escritorio, playa, etc). Pásame la ruta absoluta. La voy a guardar como preset para futuras generaciones."

Guarda el preset en: `cerebro/preset-historias.json`

```json
{
  "fotos_folder": "~/.../fotos-marca",
  "default_motor": "banana",
  "last_used": "2026-05-06"
}
```

---

## PIPELINE DE 7 PASOS

### Paso 1 — Parsear el guion

Lee el archivo .md o el contenido pegado. Extrae con el método de `references/parser-guion.md`:

- **Frontmatter YAML:** título, fecha, categoría, estructura, palabra_clave_cta, slides_count, mood
- **Tabla slide-by-slide:** array de slides con `{n, frase, capa_visual, formato, qué_grabar, briefing}`
- **Bloque ⚙️:** `fotos_necesarias_de_carpeta` y `elementos_a_generar` por slide

Si el bloque ⚙️ no existe (guion legacy), la skill debe inferirlo del contenido.

### Paso 2 — Cargar carpeta de fotos

```bash
ls -la "$FOTOS_FOLDER" | grep -E '\.(jpg|jpeg|png|heic)$'
```

Si la carpeta está vacía o no existe, error claro al usuario y aborto.

Si tiene >50 fotos, sugerir al usuario crear una subcarpeta de "fotos curadas" para acelerar el matcher.

### Paso 3 — Elegir motor por slide

Lee `references/motor-selection.md`. Lógica simple:

| Slide tiene... | Motor preferido |
|---|---|
| Foto del usuario como fondo + overlay de texto/cajas | **Banana (gemini_edit_image)** |
| Slide 1 con escenario complejo cinematográfico | **Higgsfield** (si el usuario quiere "wow") o Banana |
| Slide CTA con escenario bonito + cara | **Banana** (sobre foto real) |
| Mockup puro (dashboard, GPT, captura sintética) | **Banana** (genera desde cero) |
| Composición compleja con consistencia de cara | **Higgsfield** (si tiene Soul/character) |

**Default:** si el usuario no especifica `--motor`, usa Banana para todos los slides excepto si la skill detecta que el slide 1 necesita una escena cinematográfica que Higgsfield haría mejor.

### Paso 4 — Para cada slide: matchear foto

Aplica `references/foto-matcher.md`:

- Lee el campo `fotos_necesarias_de_carpeta[slide_N]` del bloque ⚙️
- Lista los archivos de la carpeta de fotos
- Elige la mejor coincidencia por:
  1. Match por nombre de archivo si tiene tags (ej: `playa.jpg`, `escritorio_lap.jpg`)
  2. Si no hay match obvio, presenta 3 candidatos al usuario y pide que elija
  3. La elegida se cachea en una sesión: si slides 1, 3, 5 piden "playa", usa la misma foto para todos

Si NO hay foto que matchee (slide 100% mockup):
- Skip foto base
- Generar desde cero con Banana

### Paso 5 — Construir prompt por slide

Aplica `references/prompt-builder.md`. Cada prompt tiene 3 capas:

**Capa A — La foto base (si aplica):**
```
"Use this photo as background: [foto-del-usuario-en-playa.jpg]"
```

**Capa B — Estilo Instagram Stories nativo:**
```
"Compose this as an Instagram Story image (1080x1920 vertical, 9:16).
Apply Instagram's native UI style:
- Use Instagram's default sans-serif font (similar to SF Pro / Helvetica Neue Bold)
- Text boxes should have rounded corners (12-16px radius)
- Box colors: solid white, solid black, neon yellow (#FFE93C), neon green (#4ADE80), bright red (#EF4444)
- Drop shadow on boxes is subtle (10% opacity, 4px offset)
- Highlight effect on keywords: solid color background behind specific words"
```

**Capa C — El contenido específico del slide:**
```
"Place the following elements on the image:
1. [White text box] centered top: '[FRASE EXACTA DEL SLIDE]'
2. [Capture/mockup] center-right: [descripción del mockup]
3. [Yellow curved arrow] pointing from text to capture
4. [Red X marks] over the bad examples
5. [Green check marks] over the good examples
6. Highlight the word '[KEYWORD]' in [yellow/green]
7. [Emoji] 🎁 large, top-center, above the text box"
```

Ver ejemplos completos en `references/prompt-builder.md`.

### Paso 6 — Generar la imagen

**Si motor = Banana:**
```
Use the banana skill: /banana edit <foto-base-path> "<prompt-construido>"
```

Captura el output path y muévelo a la carpeta destino.

**Si motor = Higgsfield (MCP):**

1. Sube la foto base como asset:
   ```
   mcp__higgsfield__media_upload(file_path="<foto-base>")
   mcp__higgsfield__media_confirm(...)
   ```

2. Genera la imagen:
   ```
   mcp__higgsfield__generate_image(
     prompt="<prompt-construido>",
     reference_assets=[<asset-id>],
     aspect_ratio="9:16",
     ...
   )
   ```

3. Espera con `mcp__higgsfield__job_status`. Cuando esté lista, descarga vía `mcp__higgsfield__show_medias`.

**Si motor = both:** ejecutar ambos en paralelo y entregar 2 versiones (A/B) por slide.

### Paso 7 — Guardar y mostrar preview

Carpeta destino:
```
entregables/historias/[nombre-del-guion-sin-md]/
├── slide_1.png
├── slide_2.png
├── slide_3.png
├── ...
├── _comparacion_motores/   ← solo si motor=both
│   ├── slide_1_banana.png
│   └── slide_1_higgsfield.png
└── _metadata.json          ← record del run
```

Donde `_metadata.json` tiene:
```json
{
  "guion_origen": "/path/to/guion.md",
  "fecha_generacion": "2026-05-06T14:30:00",
  "motor_por_slide": {"1": "banana", "2": "banana", "3": "higgsfield", ...},
  "foto_usada_por_slide": {"1": "playa.jpg", "2": null, "3": "playa.jpg", ...},
  "prompts_usados": {"1": "...", "2": "..."}
}
```

Después mostrar al usuario:
1. Lista de imágenes generadas con tamaños
2. Preview Markdown con cada imagen embebida (o comando para abrir Finder)
3. Costo aproximado (suma de tokens Banana + créditos Higgsfield)
4. Próximo paso: "¿Quieres que regenere algún slide específico?"

---

## CASOS ESPECIALES

### Slide 100% mockup (sin foto del usuario)

Ejemplo: slide 4 que muestra solo un mockup del GPT.

- Skip el matcher de fotos
- Banana genera desde cero con prompt tipo:
  ```
  "Realistic mockup of an OpenAI ChatGPT custom GPT interface showing
  '[NOMBRE DEL GPT]'. Clean white UI, blue primary color, displayed on
  a slight 3D perspective. Below: 3 bullet points with green check marks
  saying [bullet 1], [bullet 2], [bullet 3]. Apply Instagram Stories style overlays."
  ```

### Slide con captura real (dashboard, DM, calendario)

Si el guion menciona una captura específica que el usuario ya tiene en su carpeta:
- Buscar archivos tipo `dashboard*.png`, `dm-*.jpg`, `calendario_*.png`
- Usarla como capa adicional sobre la foto base

Si NO la tiene:
- Pedirla explícitamente: "Para el slide 3 necesitas una captura de tu dashboard de Skool. ¿La tienes lista? Pásame la ruta."

### Slide de URGENCIA (fondo plano permitido)

Si el guion es categoría `urgencia` y el slide es F9 (fondo de color):
- No usar foto base
- Banana genera fondo plano con texto IG style + emoji ⏰ o ⚠️

---

## OPCIONES DE COMANDO

| Flag | Default | Función |
|---|---|---|
| `--motor=banana\|higgsfield\|both` | auto | Forzar motor |
| `--fotos=<ruta>` | preset guardado | Carpeta de fotos override |
| `--solo=1,3,5` | todos | Renderizar solo ciertos slides |
| `--variantes=N` | 1 | Generar N variantes por slide |
| `--no-cache` | false | Ignorar cache de fotos elegidas |

---

## ⚠️ ESPAÑOL NEUTRO OBLIGATORIO EN TEXTOS DE SLIDE

Cualquier texto que renderices sobre el slide debe estar en **español neutro**, NO argentino.
Si el guion del .md trae argentinismos (tenés, podés, querés, acá, decime), CORRÍGELOS antes
de meterlos al prompt del motor de imagen. Reemplazos:

vos→tú, sos→eres, tenés→tienes, podés→puedes, querés→quieres, sabés→sabes,
copiá→copia, mandá→manda, contá→cuenta, escribí→escribe, decime→dime,
acá→aquí, laburo→trabajo, plata→dinero, che/dale→(omitir).

---

## NO HACER

- No generar el guion (eso lo hace `guionizacion-historias-formula100k`).
- No subir las imágenes a Instagram (el usuario las sube manual).
- No usar fonts externas que no sean nativas de IG.
- No inventar capturas de dashboard que el usuario no tenga; pedirlas explícitamente.
- No olvidar el aspect ratio 9:16 (1080x1920).
- No olvidar guardar el preset de carpeta de fotos en la primera invocación.
- No usar `mcp__higgsfield__generate_video` — solo imagen.
- **No renderizar textos con voseo o argentinismos** sobre las imágenes (ver arriba).
