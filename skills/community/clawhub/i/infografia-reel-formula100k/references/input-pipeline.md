# Input Pipeline — De input a brief estandarizado

La skill acepta 4 formatos de input. Este documento define cómo procesar cada uno hasta producir
el brief estandarizado que alimenta `clasificador.md` y `prompt-builder.md`.

---

## DETECCIÓN AUTOMÁTICA DEL TIPO DE INPUT

Aplicar regex al input recibido:

| Patrón | Tipo | Procesamiento |
|---|---|---|
| `^(https?://(www\.)?(youtube\.com\|youtu\.be)/...)` | URL YouTube | Path A — Transcribir |
| `^https?://...` (cualquier otra URL) | URL Artículo | Path B — Extraer |
| `^.+\.md$` (archivo en el workspace) | Ruta a guion | Path C — Parsear |
| (cualquier otro texto) | Tema libre | Path D — Investigar |

---

## PATH A — URL DE YOUTUBE

```typescript
const transcript = await mcp__claude_ai_supadara__supadata_transcript({
  url: input,
  text: true,
  lang: "es"  // o el detectado
});
```

Si supadata falla, fallback a `transcripcion-youtube-formula100k` (skill que usa yt-transcript-mcp).

Con la transcripción → destilar el brief con esta heurística:

1. Detectar el TEMA principal (primeras 3 oraciones de la transcripción).
2. Buscar enumeraciones ("primero...", "segundo...", "1.", "2.", etc.) → potenciales items.
3. Si la transcripción tiene comparaciones explícitas ("lo que daña vs lo que sana") → marcar como
   tipo dualidad.
4. Llenar el YAML del brief.

---

## PATH B — URL DE ARTÍCULO

```typescript
const article = await mcp__claude_ai_supadara__supadata_extract({
  url: input
});
// fallback si supadata no aplica:
const article = await WebFetch({ url: input, prompt: "Extract main content as markdown" });
```

Con el contenido del artículo → destilar el brief:

1. Detectar título y subtítulo (h1, h2).
2. Extraer listas (`<ul>`, `<ol>`) — son los items potenciales.
3. Detectar comparaciones en headings ("vs", "antes/después").
4. Llenar el YAML del brief.

---

## PATH C — RUTA A GUION .MD

Leer el archivo. Si tiene frontmatter YAML, parsearlo. Si tiene tabla, extraer items de las filas.

Si el guion es output de otra skill (guionizacion-formula100k, carrusel-viral-formula100k), el formato
ya está estandarizado y se mapea directamente al brief.

---

## PATH D — TEMA LIBRE

Si el tema es muy específico ("5 bebidas para los riñones") → puede destilarse directo a brief sin
investigación.

Si el tema es amplio ("salud renal") → llamar a Tavily:

```typescript
const research = await mcp__claude_ai_Tavily__tavily_research({
  query: input,
  max_results: 5,
  topic: "general"
});
```

Con los 3-5 mejores resultados, destilar:
1. Items concretos y enumerables.
2. Mejor ángulo (qué resuelve / qué muestra).
3. Hook potencial.

Si después de research el tema sigue siendo demasiado vago, **preguntar al usuario** una sola vez
con opciones concretas:

> "Tu tema 'salud renal' es muy amplio. ¿Cuál de estos ángulos prefieres?
> 1. **Bebidas que limpian los riñones** (5 bebidas, A1 cross-section)
> 2. **Alimentos que dañan vs cuidan** (8 items, A2 dualidad)
> 3. **Síntomas tempranos de fallo renal** (8 señales, A4 grid)
> 4. **Otro** (explícame qué ángulo)"

---

## ESTRUCTURA DEL BRIEF (output de cualquier path)

```yaml
tema: "string corto, descripción del tema"
angulo: "string, el ángulo específico elegido"
hook_principal: "STRING UPPERCASE 1-3 palabras"
sub_hook_a: null | "string opcional, lado izquierdo si A2/A3/A6"
sub_hook_b: null | "string opcional, lado derecho si A2/A3/A6"
items:
  - nombre: "string"
    atributo: "string corto, beneficio/efecto/categoría"
    color: "string en inglés, para el render"  # opcional, depende del arquetipo
tipo_comparacion: "ranking | dualidad | dosaje | variantes | personas | objetos"
nicho: "salud | belleza | tech | comida | finanzas | educativo | arquitectura | cine | otros"
idioma: "es | en"  # idioma del texto literal en la imagen
mood: "clinico_dramatico | calido_lifestyle | tech_cyber | scrapbook | editorial"
fuente_input: "tema_libre | url_articulo | url_youtube | ruta_guion"
fuente_url: null | "string si fuente_input es url"
notas:
  - "datos verificables encontrados en research"
  - "stats si aplica"
```

---

## VALIDACIÓN DEL BRIEF

Antes de pasar al clasificador, validar:

1. **`items` tiene entre 3 y 10 elementos** (más de 10 = ilegible en 9:16).
2. **`hook_principal` ≤ 4 palabras** (más es ilegible).
3. **Cada `atributo` ≤ 5 palabras**.
4. **`idioma` es `es` o `en`** (no mezclar idiomas en la misma imagen).

Si falla alguna validación, ajustar automáticamente:
- Si hay >10 items, recortar a los 8 más relevantes según el research.
- Si el hook es muy largo, comprimirlo a 3 palabras.
- Si los atributos son largos, abreviarlos.

---

## GUARDADO DEL BRIEF

Antes de generar la imagen, guardar el brief como YAML en:
```
entregables/infografias/<slug-tema>/brief.yaml
```

Esto permite:
- Auditar después qué se generó
- Re-generar variaciones sin volver a procesar el input
- Que otras skills (calendarizador, multiplicador) lean el brief
