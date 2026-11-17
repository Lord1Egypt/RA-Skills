---
name: infografia-reel-formula100k
description: "Crea infografías virales animadas en formato reel (9:16) a partir de un tema, idea, URL de artículo o URL de YouTube. Activar SIEMPRE que se pida 'haz una infografía', 'convierte esto en infografía', 'crea un reel infográfico', 'infografía animada', 'reel tipo cross-section', 'infografía estilo riñón/piel/cuerpo', 'convierte este artículo en infografía', 'convierte este YouTube en reel infográfico', 'diséñame una infografía para [tema]', o cualquier variación que combine intención educativa/divulgativa con formato reel visual denso. Usa el MCP de Higgsfield como motor único: nano_banana_2 para la imagen estática 4K con texto + seedance_2_0 / kling3_0 para animarla en video 9:16 listo para publicar."
argument-hint: "<tema | URL artículo | URL YouTube | ruta .md de guion>"
metadata: {"version": "1.0.0", "depends-on": [], "mcp-required": ["higgsfield"], "tools-optional": ["WebFetch", "mcp__claude_ai_supadara__supadata_extract", "mcp__claude_ai_supadara__supadata_transcript", "mcp__claude_ai_Tavily__tavily_research"], "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - **La imagen base sale de Gemini** (`GEMINI_API_KEY`, sección 3.1 del puente) o del plugin de Higgsfield si no hay llave. **La animación solo sale de Higgsfield**: sin el plugin no hay video. Antes muestra el costo total y espera ✅.
> - Para leer un artículo usa tu herramienta web; para un YouTube, `transcripcion-youtube-formula100k` o la transcripción que pegue la usuaria. Tavily/Supadata = tus herramientas web.
> - Sin Higgsfield pero con Gemini: entrega la **imagen 4K terminada** + el prompt del video para animarla a mano, y dilo. Sin ninguno: el brief, el texto y los dos prompts listos para pegar.
> - Todo va a `entregables/infografias/<tema>/`. El `.mp4` se manda por Telegram si pesa menos de 50 MB; si no, el link.

---

# Skill: Infografía-Reel FÓRMULA 100K

Convierte un tema, idea, URL de artículo o URL de video en una infografía animada en formato reel
(9:16, .mp4) usando Higgsfield como motor único de imagen + video.

La skill imita los patrones visuales de las infografías virales hispanas/inglesas que mejor performance
generan en Reels y TikTok: **cross-section anatómico con dosaje, dualidad sucio/limpio con mini-
trabajadores 3D, persona partida con bullets laterales, grid comparativo, stack de variantes,
dual character side-by-side, y diorama 3D de objetos**.

---

## ⚠️ ANTES DE EMPEZAR — LEE ESTOS REFERENCIALES

Cargar SIEMPRE estos archivos antes de generar:

1. `references/arquetipos.md` — los 7 arquetipos visuales con diagrama, prompt template y motion preset
2. `references/clasificador.md` — cómo elegir el arquetipo según el tema (árbol de decisión)
3. `references/prompt-builder.md` — fórmula universal del prompt nano_banana_2 + plantillas por arquetipo
4. `references/animation-presets.md` — prompts de seedance_2_0 / kling3_0 por arquetipo
5. `references/input-pipeline.md` — cómo procesar tema/URL artículo/URL YouTube → brief estandarizado
6. `references/brandkit.md` — paleta, tipografía, watermark, reglas de copy
7. `references/word-substitution.md` — sanitización del brief: triggers NSFW + palabras largas propensas a romperse en video

No es opcional.

---

## DEPENDENCIAS

- **MCP `higgsfield`** (`mcp__higgsfield__*`) — motor único de generación
  - `mcp__higgsfield__generate_image` con `model=nano_banana_2` para la imagen base 9:16 con texto
  - `mcp__higgsfield__generate_video` con `model=seedance_2_0` (default) o `kling3_0` para animar
  - `mcp__higgsfield__job_status` para polling
- **Herramientas opcionales para input:**
  - `WebFetch` o `mcp__claude_ai_supadara__supadata_extract` → extraer artículo
  - `mcp__claude_ai_supadara__supadata_transcript` → transcribir YouTube
  - `mcp__claude_ai_Tavily__tavily_research` → investigar tema libre

---

## INPUT — la skill acepta 4 formas

1. **Tema libre**: `"cómo afecta el azúcar al hígado"` → research con Tavily
2. **URL de artículo**: `https://...` → extracción con supadata_extract o WebFetch
3. **URL de YouTube**: `https://youtube.com/watch?v=...` → transcripción con supadata_transcript
4. **Ruta .md** (guion ya destilado): `entregables/`

Si el input es ambiguo, **detecta automáticamente** (regex de URL → tipo) y procede sin preguntar.
Si el tema es muy amplio (ej: "salud"), pide al usuario que lo acote en una pregunta corta.

---

## PIPELINE DE 6 PASOS

### Paso 1 — Destilar el input en un BRIEF estandarizado

Aplica `references/input-pipeline.md`. El brief tiene esta forma:

> **Paso 1.5 (post-destilación, pre-clasificación)**: aplicar `references/word-substitution.md`
> para sanitizar el brief de triggers NSFW (FURminator, anti-flea) y palabras largas propensas a
> deformarse en frames del video (sensibles, Mantenimiento, Diagnóstico). Si se aplica una
> sustitución, avisar al usuario en una línea antes de continuar.

```yaml
tema: "Limpieza de riñones con bebidas naturales"
angulo: "5 bebidas que limpian los riñones"
hook_principal: "KIDNEY CLEANING DRINKS"
sub_hook_a: null               # opcional, ej "Foods to limit"
sub_hook_b: null               # opcional, ej "Foods to support"
items:
  - { nombre: "Agua de coco", atributo: "limpia toxinas",  color: "verde claro" }
  - { nombre: "Agua de limón", atributo: "neutraliza ácido", color: "amarillo" }
  - { nombre: "Agua de pepino", atributo: "hidrata", color: "verde" }
  - { nombre: "Agua de cebada", atributo: "diurético", color: "ámbar" }
  - { nombre: "Jugo de arándano", atributo: "antibacterial", color: "rojo" }
tipo_comparacion: "ranking"     # ranking | dualidad | dosaje | variantes | personas | objetos
nicho: "salud"                  # salud | belleza | tech | comida | finanzas | educativo
idioma: "es"                    # es | en
mood: "clinico_dramatico"       # clinico_dramatico | calido_lifestyle | tech_cyber | scrapbook
```

### Paso 2 — Clasificar arquetipo

Aplica el árbol de decisión de `references/clasificador.md`:

| Si el brief es… | Arquetipo |
|---|---|
| Dosaje de N ingredientes/bebidas/productos sobre un órgano/tejido | **A1** Cross-section + dosaje |
| Comparación binaria daño-vs-cura con grid de items | **A2** Dualidad sucio/limpio |
| Comparación de hábitos/estados sobre UNA persona | **A3** Persona partida |
| Lista/ranking/menú de items con verdict 👍👎 | **A4** Grid comparativo |
| Mostrar el efecto de UN parámetro variable | **A5** Stack de variantes |
| Comparar dos eras/personajes con stack de items | **A6** Dual character |
| Tipos/categorías de UN mismo objeto | **A7** Diorama 3D |

Si el brief admite varios arquetipos, **prefiere A1, A2 o A4** (los más virales según las refs analizadas).

### Paso 3 — Confirmar arquetipo y mostrar mockup ASCII al usuario

Antes de gastar créditos en Higgsfield, muestra al usuario:

```
🎯 Arquetipo elegido: A1 — Cross-section + dosaje
📐 Layout:
  ┌─────────────────────┐
  │  [HOOK GRANDE]      │
  │ 🧪 🧪 🧪 🧪 🧪      │  ← 5 frascos goteando
  │  ↓  ↓  ↓  ↓  ↓     │
  │ [CROSS-SECTION DEL  │
  │  RIÑÓN]             │
  │ [coco][lim][pep]... │  ← 5 vasos abajo
  │  KIDNEY CLEANING    │
  └─────────────────────┘
🎨 Mood: clínico dramático, fondo dark navy
🎬 Animación: líquido cayendo loop + zoom in 5%
```

Pregunta: **"¿Confirmamos o ajustamos?"**. Si el usuario confirma, pasar al Paso 4.

### Paso 4 — Generar imagen base con nano_banana_2

Construye el prompt aplicando `references/prompt-builder.md` (plantilla específica del arquetipo).

```typescript
mcp__higgsfield__generate_image({
  params: {
    model: "nano_banana_2",
    aspect_ratio: "9:16",
    prompt: "<prompt construido>",
    count: 1
  }
})
```

Polling con `job_status` cada 10–15s. Cuando termina, **descarga el .png** a:
```
entregables/infografias/<slug-tema>/01_imagen_base.png
```

### Paso 5 — Mostrar imagen al usuario y aprobar

**Antes de animar (que cuesta más créditos)**, muestra la imagen al usuario y confirma:
- ¿El texto se lee bien?
- ¿Los items y etiquetas son los correctos?
- ¿La paleta y el mood son los adecuados?

Si NO está bien, regenerar con prompt ajustado (variar seed, reforzar instrucciones de texto).
Si está bien, continuar.

### Paso 6 — Animar con kling3_0 (default) o seedance_2_0

Aplica `references/animation-presets.md`. Cada arquetipo tiene un motion prompt específico
+ el bloque universal **CRITICAL TEXT LOCK** que protege el texto de deformarse en frames.

```typescript
mcp__higgsfield__generate_video({
  params: {
    model: "kling3_0",             // default. seedance_2_0 sólo si el prompt es 100% limpio
    aspect_ratio: "9:16",
    duration: 8,                   // 8-12s, loopeable
    sound: "off",
    prompt: "<motion prompt del arquetipo + bloque TEXT LOCK con la lista literal de textos>",
    medias: [{ value: "<job_id de la imagen>", role: "start_image" }],
    count: 1
  }
})
```

**Si seedance_2_0 devuelve `status: "nsfw"`** (falso positivo común con palabras como
FURminator, anti-flea, deshedding) → fallback automático a `kling3_0` con prompt suavizado.

Polling. Cuando termina, descarga el .mp4 a:
```
entregables/infografias/<slug-tema>/02_reel.mp4
```

### Paso 7 — Entregar al usuario

Mensaje final con:
- Ruta del .png base
- Ruta del .mp4 reel
- Hook recomendado para caption
- Hashtags sugeridos (3-5, nicho específico)
- CTA sugerido (1 línea)

---

## EJEMPLO DE INVOCACIÓN

```
Usuario: /infografia-reel-formula100k bebidas para limpiar los riñones

Skill: 
  → Detectado: tema libre
  → Investigando con Tavily…
  → Brief: 5 bebidas, A1 (cross-section + dosaje)
  → Mockup ASCII mostrado, esperando confirmación

Usuario: confirmado

Skill:
  → Generando imagen con nano_banana_2 (job abc-123)
  → Imagen lista en /FORMULA100K/INFOGRAFIAS/bebidas-rinones/01_imagen_base.png
  → ¿Confirmamos antes de animar?

Usuario: sí

Skill:
  → Animando con seedance_2_0 (job def-456)
  → Reel listo en /FORMULA100K/INFOGRAFIAS/bebidas-rinones/02_reel.mp4
  → Caption sugerido: "5 bebidas para limpiar tus riñones de forma natural 🌿"
  → Hashtags: #saludrenal #limpiezanatural #saludholistica
```

---

## REGLAS NO NEGOCIABLES

1. **Idioma**: El usuario escribe en español NEUTRO, no argentino. Aplica reemplazos vos→tú, tenés→tienes,
   acá→aquí, mirá→mira en TODO copy generado. Si el input es en inglés, mantener inglés.
2. **Output**: SIEMPRE en `entregables/infografias/<slug-tema>/`.
   Estructura por carpeta: `01_imagen_base.png`, `02_reel.mp4`, `brief.yaml`, `prompts.md`.
3. **No mockear el watermark** — agrégalo opcionalmente sólo si el usuario pide su handle (`@usuario`).
4. **No inventar datos** — si el tema requiere datos verificables (estadísticas, propiedades médicas),
   usa Tavily o WebFetch antes de poner el dato en el prompt.
5. **Confirmación obligatoria antes del video** — la imagen base se aprueba ANTES de animar.
   Animar cuesta créditos significativos y no se debe gastar a ciegas.
6. **Aspect ratio**: SIEMPRE 9:16 (1080x1920). Cualquier otro ratio rompe la skill.
7. **Si Higgsfield falla**: reintenta UNA vez con seed distinta. Si falla de nuevo, reporta el error
   al usuario con el job_id para debugging.
