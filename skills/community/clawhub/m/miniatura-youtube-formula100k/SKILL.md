---
name: miniatura-youtube-formula100k
description: "Skill especializada en generar miniaturas y portadas virales para YouTube usando las fotos del usuario. Usar SIEMPRE que alguien pida: crear una miniatura de YouTube, generar una portada para video, diseñar thumbnail, hacer la imagen de mi video de YouTube, analizar miniaturas de la competencia, optimizar mi miniatura, crear variaciones de thumbnail. Modo estrella CLONAR ESTILO: replica el estilo de UNA captura de referencia (la miniatura de otra persona) poniendo la cara del usuario y manda a generar con Nano Banana (Gemini) — activarlo cuando digan 'quiero esta miniatura con mi cara', 'clona este estilo', 'réplica esta portada usando mi foto' o adjunten una referencia + una selfie. Basada en la metodología de FORMULA 100K con análisis de competencia real."
argument-hint: "<palabra clave o tema del video>"
metadata: {"version": "2.0.0", "author": "TU-HANDLE", "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Motor: **Gemini directo con `GEMINI_API_KEY`** (sección 3.1 del puente), que es el mismo Nano Banana. Si no hay llave pero sí el plugin de Higgsfield (`nano_banana_pro`), úsalo. Costo de las 4 variantes → ✅ → generar.
> - La selfie y la captura de referencia llegan por Telegram como archivo; las fotos guardadas están en `cerebro/fotos/`. Con Gemini van como partes `inline_data`, **selfie primero**; no hay widget de subida.
> - Sin ningún motor: entrega el concepto, el texto de la miniatura y el prompt listo.
> - Entrega en `entregables/miniaturas/` y por Telegram.

---

# Skill: Miniatura YouTube FORMULA 100K

Genera miniaturas optimizadas para YouTube usando tus fotos, con análisis de la competencia. Metodología basada en FORMULA 100K: menos es más, CTR primero. Motor de imagen: **Nano Banana** — por defecto Gemini directo con `GEMINI_API_KEY`; el plugin de Higgsfield (`nano_banana_pro`) queda como alternativa si no hay llave.

---

## ELEGIR EL MODO (primero que todo)

| Modo | Cuándo | Motor |
|------|--------|-------|
| **🅐 CLONAR ESTILO** (estrella) | El usuario adjunta **una captura de referencia + su selfie** y quiere "esta miniatura con mi cara" / "clona este estilo" / "mándalo a generar" | Nano Banana (Gemini; Higgsfield si no hay llave) |
| **🅑 DESDE CERO** | No hay referencia; se diseña la miniatura con la metodología FORMULA 100K (fondo negro + amarillo u otro estilo de la tabla) | Nano Banana (Gemini; Higgsfield si no hay llave) |

- **Modo 🅐** → leer `references/clonar-estilo-higgsfield.md` y seguir ese pipeline (subir selfie + referencia, etiquetar FIRST/SECOND image, generar 4 variaciones, descargar, recomendar). El texto/logo se montan en Canva al final. Puedes saltarte el Paso 2 de investigación si la referencia ya es el estilo elegido.
- **Modo 🅑** → seguir el PROCESO OBLIGATORIO completo de abajo.

---

## PROCESO OBLIGATORIO (Modo 🅑 — desde cero)

### PASO 1 — Recolectar inputs del usuario

Si no se proporcionaron en el mensaje, preguntar (una sola vez, todo junto):

1. **Palabra clave / tema del video** — ¿Qué buscaría alguien para encontrar tu video? (ej: "cómo ganar dinero en Instagram")
2. **Título tentativo del video** — Para que la miniatura complemente sin repetir
3. **Fotos disponibles** — ¿Tienes una foto tuya de fondo removido (PNG) o quieres usar una foto nueva? Pide que arrastren el archivo o den la ruta
4. **Palabras para la miniatura** — 2 a 5 palabras máximo que irían en el cartel. Si no sabe, sugerir basado en el tema
5. **Estilo de miniatura** — ¿Cuál prefieres? Ver tabla en `references/estilos-plantillas.md`. Si no sabe, usar el **Estilo FORMULA 100K (fondo negro + amarillo)**

Si el usuario solo da la palabra clave, continuar con defaults: estilo FORMULA 100K, generar palabras sugeridas tú mismo.

---

### PASO 2 — Investigar miniaturas de la competencia

Usar **WebSearch** para buscar miniaturas similares al tema del video:

```
Buscar: site:youtube.com "<palabra clave>" thumbnail miniatura
Buscar: youtube "<palabra clave>" miniaturas más clickeadas
```

También usar **Playwright** para capturar resultados visuales de YouTube si es necesario:
- Navegar a `https://www.youtube.com/results?search_query=<palabra+clave>`
- Tomar screenshot de los primeros 8-12 resultados
- Analizar visualmente qué patrones se repiten

**Qué analizar de la competencia:**

| Elemento | Qué observar |
|----------|--------------|
| 🎨 **Paleta de colores** | ¿Qué colores dominan? ¿Hay un color que destaca? |
| 📝 **Texto en miniatura** | ¿Cuántas palabras? ¿Qué palabras usan más? |
| 😄 **Expresiones** | ¿Cara de sorpresa, seria, sonriente, señalando? |
| 🖼️ **Composición** | ¿Persona a la izquierda? ¿Centrada? ¿Con objetos? |
| 📊 **Patrones de nicho** | ¿Hay un estilo que se repite en los top videos? |
| ⚡ **Oportunidad de diferenciación** | ¿Qué hace NADIE que podría funcionar? |

Generar un reporte breve de 3-5 observaciones clave antes de crear la miniatura.

---

### PASO 3 — Planificar la miniatura (brief creativo)

Basado en la investigación, armar el **Brief Visual** siguiendo la metodología FORMULA 100K:

**Checklist obligatorio (leer `references/metodologia-miniaturas.md`):**
- [ ] Entendible en menos de 1 segundo
- [ ] Complementa el título (NO repite el mismo mensaje)
- [ ] Expresión facial de emoción (sonrisa, sorpresa, confianza)
- [ ] Colores contrastantes (amarillo+negro, rojo+blanco, azul+amarillo)
- [ ] Elemento de tracción visual (flecha, ícono, cartel)
- [ ] Espacio negativo — no sobrecargar
- [ ] Máximo 3-5 palabras en el texto de la miniatura

**Definir para el prompt de generación:**
- Fondo: negro sólido (default FORMULA 100K) o alternativo según estilo elegido
- Posición de la persona: centrada o ligeramente a la derecha/izquierda
- Texto del cartel: 2-5 palabras en MAYÚSCULAS, color amarillo vibrante (#FFD700)
- Expresión que necesita la foto: indicar al usuario si necesita una foto específica
- Elementos adicionales: íconos de plataformas, flechas, checkmarks, etc.

---

### PASO 4 — Generar la imagen (Nano Banana)

**Motor por defecto: Gemini directo** con `GEMINI_API_KEY`, modelo `gemini-3.1-flash-image-preview`
(es Nano Banana), `aspectRatio:"16:9"`, `imageSize:"2K"`. El comando exacto, incluido cómo mandar
la selfie y la referencia juntas, está en la **sección 3.1 de `f100k-puente`**: cópialo de ahí.

**Resumen del flujo con Gemini:**
1. Junta las fotos. No se suben a ningún lado: viajan en la misma llamada como `inline_data`.
2. Una llamada por variante, **selfie primero** y referencia después, con el prompt en inglés en modo instrucción. Guarda cada una como `miniatura-1.png`, `miniatura-2.png`…
3. Abre cada PNG con `Read` para evaluarla antes de entregarla.

**Si no hay `GEMINI_API_KEY` pero sí el plugin de Higgsfield**, el flujo equivalente es
`media_upload` → `generate_image` con `model:"nano_banana_pro"`, `medias[]` (selfie primero),
`count:4` → `job_status(jobId, sync:true)` → `curl` de `results.rawUrl`. Está en
`references/clonar-estilo-higgsfield.md`.

**Modo 🅑 (desde cero) — prompt base con foto del usuario:**

```
[descripción de la persona / o "use the EXACT face and identity of the woman
in the FIRST reference image"], confident [smiling/surprised/determined]
expression looking directly at camera, on a [pure solid black background /
estilo elegido]. Negative space preserved — clean, uncluttered composition.
MUST NOT INCLUDE: no text, no captions, no logos (el texto se pone en Canva).
High-contrast YouTube thumbnail, photorealistic, professional quality, 16:9.
```

**Modo 🅐 (clonar estilo):** usar la plantilla `FIRST/SECOND reference image` de `references/clonar-estilo-higgsfield.md`. Con Gemini la plantilla es la misma: cambia solo cómo viajan las fotos (dos `inline_data` en vez de `medias[]`), y el orden importa igual.

**Generar 4 variaciones** para tener opciones de iteración: con Gemini son 4 llamadas seguidas (no hay `count`); con Higgsfield, `count:4` en una sola corrida.

> El **texto del cartel, logos y burbujas** se montan SIEMPRE después en Canva, no en la generación. Imagen limpia = más nítida y editable.
> (Histórico: la v1 usaba la API de Gemini `gemini_edit_image`/`gemini_generate_image` con fondo quemado y texto incluido — quedó deprecado en favor de Higgsfield.)

---

### PASO 5 — Post-procesamiento (si es necesario)

Si la imagen necesita ajustes exactos de dimensiones:

```bash
# Recortar a dimensiones exactas YouTube (1280x720)
magick input.png -resize 1280x720^ -gravity center -extent 1280x720 thumbnail_final.png

# Si el usuario quiere remover fondo de su foto antes de componer
magick foto.jpg -fuzz 15% -transparent white foto_sin_fondo.png
```

Verificar ImageMagick disponible:
```bash
which magick || which convert || echo "Instala: brew install imagemagick"
```

---

### PASO 6 — Entregar resultado con análisis estratégico

Después de generar, siempre entregar:

1. **Las 4 imágenes generadas** con sus rutas (carpeta de entrega: `entregables/miniaturas/AAAA-MM-DD_<slug>/`)
2. **Recomendación de cuál usar primero** (parecido + nitidez + composición + "set" del fondo)
3. **Recordar montar el texto/logo/burbuja en Canva** sobre la ganadora (la generación va limpia a propósito)
4. **Estrategia de iteración CTR:**
   - Si CTR < 4% en las primeras 2 horas → cambiar el TÍTULO primero
   - Si CTR sigue bajo tras otras 2 horas → cambiar a otra variación de miniatura
   - Máximo 3-4 cambios de miniatura por video
5. **Palabras de alto impacto** sugeridas para el cartel si aún no está optimizado
6. **Próxima acción**: ¿Quieres que genere también el título optimizado?

---

## DEFAULTS Y ESTILO FIRMA F100K

Cuando el usuario no especifica estilo, aplicar el **Estilo FORMULA 100K**:

- **Fondo**: Negro sólido (#000000)
- **Posición persona**: Centrada o ligeramente derecha
- **Texto**: Cartel amarillo vibrante (#FFD700) con 2-4 palabras en bold sans-serif
- **Expresión**: Sonrisa de confianza / dominio
- **Íconos**: Instagram, TikTok, o emojis de plataforma según nicho
- **Composición**: Limpia, mucho espacio negativo
- **Palabras de alto impacto para redes sociales**: DOMINA, SECRETO, ALGORITMO, VIRAL, MILLÓN, ESTRATEGIA

---

## GUARDRAILS

- NUNCA generar miniaturas con más de 7 palabras de texto visible
- NUNCA sobrecargar con múltiples elementos visuales (máx 3 elementos: persona + texto + 1 ícono)
- NUNCA repetir el mismo mensaje que el título del video en la miniatura
- SIEMPRE hacer 4 variaciones (count:4) para tener opciones de iteración
- NUNCA quemar el texto/logo/burbuja en la generación de Higgsfield — van en Canva al final (imagen limpia = más nítida)
- En modo CLONAR: selfie SIEMPRE primero en medias[], etiquetar FIRST/SECOND image, incluir `MUST NOT INCLUDE` y `Do not alter her facial features`
- Si el usuario no tiene fotos, generar con descripción detallada pero AVISAR que usar foto real propia convierte más
- Si la generación falla por filtros de seguridad, simplificar la descripción y reintentar

---

## REFERENCIAS

Cargar bajo demanda — NO cargar todas al inicio:
- `references/clonar-estilo-higgsfield.md` — **Modo CLONAR ESTILO**: pipeline completo Higgsfield (subir selfie+referencia, plantilla de prompt FIRST/SECOND image, generar, descargar). Leer SIEMPRE en modo 🅐.
- `references/metodologia-miniaturas.md` — Checklist completo + teoría CTR de FORMULA 100K
- `references/estilos-plantillas.md` — 9 estilos de miniatura con prompts base
- `references/banana-thumbnail-config.md` — (histórico) Config de la API de Gemini NanoBanana, deprecado en favor de Higgsfield
