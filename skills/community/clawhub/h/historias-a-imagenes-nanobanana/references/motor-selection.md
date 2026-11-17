# MOTOR SELECTION — Banana vs Higgsfield

Cuándo usar cada motor para qué tipo de slide.

---

## RESUMEN EJECUTIVO

| Motor | Fortalezas | Debilidades |
|---|---|---|
| **Banana (Gemini Nano Banana)** | Edición precisa de imagen base, texto legible, rápido, barato | Generación desde cero menos fotorrealista |
| **Higgsfield** | Generación cinematográfica, mejor con escenas complejas, character consistency | Más caro, más lento, menos preciso con texto exacto |

**Default:** Banana para todo. Higgsfield solo cuando se necesita "wow" cinematográfico.

---

## TABLA DE DECISIÓN POR TIPO DE SLIDE

| Tipo de slide | Motor recomendado | Razón |
|---|---|---|
| Slide 1 con foto base + texto + emoji | **Banana** (`gemini_edit_image`) | Edición sobre foto real preserva la cara perfecta |
| Slide 2 con captura de DM/dashboard sobre foto | **Banana** | Texto de capturas requiere alta legibilidad |
| Slide 3 con flecha amarilla + comparación X/✓ | **Banana** | Edición con overlays, Banana lo hace bien |
| Slide 4 con mockup del producto (GPT, bot) | **Banana** | Generar UI realista — Banana es bueno con interfaces |
| Slide CTA con escenario bonito + cara | **Banana** | Foto base + cajas IG |
| Slide 100% generado (sin foto base) | **Banana** (`gemini_generate_image`) | Más barato y rápido |
| Slide 1 cinematográfico complejo (apertura cine) | **Higgsfield** | Mejor para escenas dramáticas tipo película |
| Slide con efectos visuales (zoom, grano, motion blur) | **Higgsfield** | Sus modelos son mejores en cinematografía |
| Slide con character consistency en múltiples ángulos | **Higgsfield** | Mejor para mantener consistencia visual entre slides |

---

## CASOS ESPECIALES

### Categoría URGENCIA + F9 (fondo plano)

Slide tipo "ÚLTIMAS HORAS — Solo HOY" con fondo rojo o negro:

→ **Banana** (`gemini_generate_image` desde cero, sin foto base)
→ Prompt: "solid red background #DC2626, large white text 'ÚLTIMAS HORAS', emoji ⏰ above"

### Slide de mini documental con cara del cliente

Slide 1 tipo "Ella es Brenda 👇" + foto circular de Brenda:

→ **Banana** (`gemini_edit_image`)
→ Foto base: foto del usuario (paisaje)
→ Pasar también la foto del cliente como segunda referencia
→ Prompt: "place a circular photo of [cliente] (provided as reference) in the center, with white border like a polaroid"

### Slide con motion / video clip

Si el usuario quiere que ese slide se grabe como video, no como imagen estática:

→ **NO generar con esta skill**
→ La skill avisa: "Este slide es un video grabado por el usuario (formato F2/F5). No se genera con IA. Solo necesita texto y cajas, que pueden añadirse en la app de IG."

---

## MODO `--motor=both` (A/B testing)

Cuando el usuario quiere ver ambas versiones para elegir:

1. Ejecuta Banana → guarda `slide_N_banana.png`
2. Ejecuta Higgsfield → guarda `slide_N_higgsfield.png`
3. Genera composición comparativa lado a lado en `_comparacion_motores/slide_N_compare.png`
4. Muestra al usuario y pregunta: "¿Cuál prefieres? Banana, Higgsfield, o regeneramos otra"

---

## INVOCACIÓN TÉCNICA

### Banana

A través de la skill:
```
/banana edit <foto-base-path> "<prompt-construido>"
```

O directamente con el MCP tool (si está cargado):
```
gemini_edit_image(
  prompt="<prompt>",
  image_path="<foto-base>"
)
```

Para generar desde cero:
```
gemini_generate_image(prompt="<prompt>")
```

### Higgsfield (MCP)

Pipeline de 3 pasos:

1. **Subir foto base como asset:**
```
mcp__higgsfield__media_upload(file_path="<foto-base>")
→ retorna { upload_url, file_id }
mcp__higgsfield__media_confirm(file_id="<id>")
→ retorna asset_id confirmado
```

2. **Generar imagen:**
```
mcp__higgsfield__generate_image(params={
  model: "nano_banana_2",       # SIEMPRE este modelo (Nano Banana Pro de Google)
  prompt: "<prompt>",
  aspect_ratio: "9:16",
  resolution: "2k",              # mínimo 2k para evitar duplicación de texto/glitches
  count: 1,
  medias: [{ value: "<asset_id>", role: "image" }]   # solo si hay foto base
})
→ retorna job_id
```

**⚠️ Reglas obligatorias:**
- **`model` siempre `nano_banana_2`** — es el último Nano Banana de Google (Pro), el único con text-rendering confiable. Nunca downgrade a otros modelos para stories del usuario.
- **`resolution` mínimo `"2k"`** — en `"1k"` el modelo a veces duplica palabras/líneas en cajas de texto. Subir a `"2k"` (o `"4k"` si el slide tiene tabla densa o mockup con mucho texto) elimina ese artefacto.
- **`aspect_ratio: "9:16"`** explícito siempre.

3. **Esperar y descargar:**
```
mcp__higgsfield__job_status(job_id="<id>")
# poll cada 5 seg hasta estado "completed"

mcp__higgsfield__show_medias(job_id="<id>")
# retorna URL de descarga
```

Descarga la URL y guarda como `slide_N_higgsfield.png`.

---

## ⚠️ COSAS A NO HACER

- **NO usar Higgsfield Soul del usuario** para generar su cara → está deprecado, deriva la cara (ver memoria del usuario: `feedback_avatar_imagen.md`)
- **NO usar Banana solo (`generate_image`) para slides con cara del usuario** → genera caras random, no la de otra persona
- **NO mezclar motores en una sola secuencia** sin avisar al usuario (genera disparidad visual)
- **NO usar Higgsfield para texto largo** → su modelo no renderiza texto bien todavía
- **NO olvidar verificar el aspect ratio 9:16** explícitamente en el prompt

---

## COSTOS APROXIMADOS (referencia para el usuario)

| Motor | Costo por imagen | Velocidad |
|---|---|---|
| Banana (Gemini 2.5 Flash) | ~$0.01-0.04 | 5-15 segundos |
| Banana (Gemini 2.5 Pro) | ~$0.05-0.10 | 15-30 segundos |
| Higgsfield | ~créditos según plan | 30-90 segundos |

**Tip de optimización:** una secuencia de 5 slides con Banana cuesta ~$0.10-0.50. Con Higgsfield, depende del plan del usuario.

Antes de generar, confirmar con el usuario si quiere:
- "Modo económico" → Banana para todo
- "Modo premium" → Higgsfield para slides cinematográficos, Banana para resto
- "A/B test" → Both

---

## DEFAULT FINAL (si no hay especificación del usuario)

```
Para slides estándar (texto + foto + cajas) → Banana
Para slide 1 si la categoría es ONE-SHOT o LEAD MAGNET → Banana
Para slide 1 si la estructura es #16 Apertura Cinematográfica → Higgsfield
Para slide 100% sin foto (mockup puro) → Banana
Para urgencia con fondo plano → Banana
```

Es decir: **Banana en 90% de los casos**. Higgsfield solo si el usuario pide explícitamente "más cinematográfico" o usa estructura #16.
