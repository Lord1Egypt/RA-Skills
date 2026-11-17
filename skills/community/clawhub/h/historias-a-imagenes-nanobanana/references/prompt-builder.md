# PROMPT BUILDER — Cómo construir el prompt para cada slide

Esta es la fórmula exacta para que el motor (Banana o Higgsfield) genere un slide con el look IG de la marca.

---

## ESTRUCTURA DEL PROMPT (5 capas en orden)

```
[CAPA 1: Aspect ratio y formato]
[CAPA 2: Subject — foto base o escena a generar]
[CAPA 3: Estilo Instagram Stories nativo]
[CAPA 4: Composición — qué va en cada zona del slide]
[CAPA 5: Negative prompts]
```

---

## TEMPLATE COMPLETO

```
A 1080x1920 vertical Instagram Story image (9:16 aspect ratio).

[SUBJECT]
{Si hay foto base: "Use the provided reference photo as the background scene.
The subject is the creator (use the user's reference selfie — never another person's face).
Preserve her exact face and outfit from the reference photo."}
{Si NO hay foto base: "Generate a [describe la escena: ej. close-up of an OpenAI ChatGPT
custom GPT interface on a clean white background]"}

[STYLE — INSTAGRAM STORIES NATIVE]
This is a CLEAN creative asset that will be uploaded TO Instagram as a story.
DO NOT render Instagram's app UI (no username header, no profile-picture circle,
no "See translation" link, no progress bars, no 3-dots menu, no X close button,
no "Send message" bar, no heart/DM icons, no IG logo). The canvas is purely the
creative content; Instagram itself adds its UI at display time.

Apply only the TEXT/STICKER aesthetic that the IG Stories editor produces:
- Use a default modern sans-serif (similar to SF Pro Display or Helvetica Neue Bold)
- Text boxes have rounded corners (14px border radius)
- Solid color backgrounds on boxes (no gradients): white #FFFFFF, black #000000,
  neon yellow #FFE93C, neon green #4ADE80, bright red #EF4444
- NO drop shadow on text boxes
- Apple-style emoji rendering
- High-quality, sharp, no blur on text
- NEVER duplicate, repeat, or echo the same word/line/phrase. Render every text
  string exactly once, exactly as written in the prompt.

[COMPOSITION]
Layer the following elements on the image, from background to foreground:

1. BACKGROUND: {foto base o escena generada}
   {Si la foto es muy clara: "Apply a subtle dark gradient overlay at 15% opacity
   to ensure text legibility."}

2. {Slide Cabeza | Mid | CTA — describir cada layer:}

   PRIMARY TEXT BOX:
   - Position: {top-center | center | bottom-center}
   - Background: {white #FFFFFF | yellow #FFE93C | red #EF4444 | etc.}
   - Text color: {black | white}
   - Font: bold sans-serif
   - Content: "[FRASE EXACTA DEL SLIDE]"
   - Highlight the word "[KEYWORD]" with [yellow #FFE93C | green #4ADE80] background

   {SI HAY CAPTURA/MOCKUP:}
   FLOATING SCREENSHOT:
   - Position: {center-right | center | top-right}
   - Content: [descripción del mockup, ej. "an Instagram analytics dashboard
     showing '+40K USD revenue' with member count 1,703"]
   - Style: rounded corners 16px, subtle drop shadow, slightly rotated 2°
   - Size: occupies ~40% of frame width

   {SI HAY FLECHA AMARILLA:}
   YELLOW HAND-DRAWN ARROW:
   - Color: #FFE93C (neon yellow)
   - Style: hand-drawn, slightly wobbly, 10px stroke width
   - Curves from [origen] to [destino]
   - Has triangular arrowhead

   {SI HAY X o ✓:}
   {N} red X marks (#FF3B3B, 80px, hand-drawn) over [los elementos malos]
   {N} green check marks (#4ADE80, 80px, hand-drawn) over [los elementos buenos]

   {SI HAY EMOJI GRANDE:}
   LARGE APPLE-STYLE EMOJI:
   - Emoji: {🎁 | ⚠️ | 🤖 | 💰 | etc.}
   - Position: top-center, 16px above text box
   - Size: 100-140px

   {SI ES SLIDE CTA:}
   CTA BOX (final layer):
   - Position: lower-center
   - Background: white #FFFFFF, rounded corners 14px
   - Content: "Responde **[PALABRA_CLAVE]** y te [acción]"
   - The word "[PALABRA_CLAVE]" in blue #3B82F6 inline text color
   - Below the box: ⬇️ ⬇️ ⬇️ three small white down arrows

3. SAFE ZONE: ensure no critical text or elements in the top 250px or bottom 250px
   (those are blocked by Instagram's UI when displayed in app).

[NEGATIVE PROMPTS]
Do NOT include:
- Blurry or distorted text
- Custom decorative fonts (only sans-serif)
- Drop shadows on text boxes
- Gradient backgrounds on boxes
- AI watermarks or generation artifacts
- Duplicated or morphed faces
- DUPLICATED, REPEATED, OR ECHOED TEXT/WORDS/LINES anywhere in the image
- Stock-photo Latin women (use the provided face)
- Over-saturated colors
- Pixelated emoji
- Hand artifacts (extra fingers)
- Text outside the safe zone
- ⚠️ INSTAGRAM APP CHROME/UI baked into the image. The output is a CLEAN CREATIVE
  ASSET that will be uploaded TO Instagram as a story — Instagram itself will add
  its own UI on top at display time. So the image MUST NOT contain ANY of the
  following rendered as part of the picture:
    · profile-picture circle, username header (e.g. "@tuhandle · 27m"), or "See translation" link
    · 3-dots menu, X close button, or progress bars at the top
    · "Send Message" reply input bar at the bottom
    · heart, paper-plane, or DM icons
    · IG logo, story timer, or any other Instagram interface element
  The canvas is the FULL 1080×1920 creative; Instagram chrome is rendered by the
  app at runtime, NOT by the model.
```

⚠️ **CRITICAL — clean canvas rule:** every prompt MUST contain an explicit line such as
"This is a clean creative asset for Instagram Stories upload. Do NOT render Instagram's
app interface (no username header, no profile circle, no 'Send message' bar, no reply
icons, no progress bars, no 3-dots menu) — the canvas is purely the creative content."

This is non-negotiable: if the model bakes IG UI into the image, the user gets duplicated
UI when posting the story.

---

## EJEMPLO REAL — SLIDE 1 (Lead Magnet del GPT)

**Frase del slide:** "Algo me sorprendió hoy…"
**Formato:** 🎥 F2 Video Tercera Persona
**Capa visual:** la creadora caminando frente al Buda en Japón
**Briefing:** Fondo: viaje, plano general; Cajas: blanca arriba; Highlight: "sorprendió" en amarillo

**Prompt construido:**

```
A 1080x1920 vertical Instagram Story image (9:16 aspect ratio).

SUBJECT: Use the provided reference photo as the background. The subject is
the creator (from the reference selfie), walking in front of a giant green Buddha
statue in Japan. Preserve her exact face and outfit from the reference.

STYLE — INSTAGRAM STORIES NATIVE: The image must look like a screenshot taken
directly from the Instagram Stories editor. Use Instagram's default sans-serif
font (SF Pro Display or Helvetica Neue Bold). Text boxes have 14px rounded
corners and solid color backgrounds.

COMPOSITION:

1. BACKGROUND: full-frame photo of the creator walking toward the Buddha statue,
   bright daylight, blue sky.

2. PRIMARY TEXT BOX:
   - Position: top-center, ~280px from top
   - Background: solid white #FFFFFF
   - Text color: black #000000
   - Font: SF Pro Display Bold, 64pt
   - Content: "Algo me sorprendió hoy…"
   - Highlight the word "sorprendió" with neon yellow #FFE93C background
     (subtle, just behind that word)

3. SMALL EMOJI: 😱 emoji at 80px, just left of the text box, slightly tilted.

4. SAFE ZONE: keep top 250px and bottom 250px clear of any text.

NEGATIVE: no blurry text, no custom fonts, no drop shadow on box, no gradient,
no AI artifacts, no morphed face, no stock photo replacement.
```

---

## EJEMPLO REAL — SLIDE 4 (mockup del GPT)

**Frase:** "Ante ello, he creado este GPT 🤖"
**Formato:** 📸 F13 Objetos
**Capa visual:** mockup del GPT "Experto en Gancho Visual"

**Prompt construido:**

```
A 1080x1920 vertical Instagram Story image (9:16 aspect ratio).

SUBJECT: Use the reference photo as background (el usuario standing on Japanese
seaside rocks, cloudy sky). Generate a realistic mockup of an OpenAI ChatGPT
custom GPT interface as a floating screenshot.

STYLE — INSTAGRAM STORIES NATIVE: native font, solid color boxes, 14px
rounded corners, no shadows on boxes.

COMPOSITION:

1. BACKGROUND: El usuario on rocks, ocean behind her.

2. TEXT BOX (top):
   - Position: top-center
   - Background: black #000000
   - Text color: white #FFFFFF
   - Content: "Ante ello, he creado este GPT"
   - Highlight the word "creado" in green #4ADE80, "GPT" in blue #3B82F6 inline

3. FLOATING SCREENSHOT (center):
   - Realistic mockup of ChatGPT custom GPT interface
   - GPT icon (small avatar)
   - GPT name: "Experto en Gancho Visual"
   - GPT author: "Por [TU NOMBRE]"
   - Description: "Especialista en análisis y diseño visual del primer segundo en videos 9:16"
   - White UI, blue accent (ChatGPT blue)
   - Rounded corners 16px, subtle drop shadow, slight 2° rotation

4. CALLOUT TEXT (overlay on the mockup):
   - "🤖 Analizador del primer segundo" — blue rounded pill below the GPT card

5. THREE BENEFIT BULLETS (below mockup):
   - White boxes, rounded 14px, each with green ✓ check
   - "✅ Tomas captura y lo subes"
   - "✅ Te dice tus errores"
   - "✅ Cómo corregirlos antes de publicar tu video"

6. EMOJI ROW: ➡️ ➡️ ➡️ three blue arrow emojis at the bottom of the mockup.

NEGATIVE: ningún (lista del template).
```

---

## CONSEJOS PARA LA EJECUCIÓN

### Si el motor es Banana (gemini_edit_image):

- Pasa la foto base como input + el prompt completo como instruction
- Si el slide tiene mockup complejo, generar PRIMERO el mockup como imagen separada
  con `gemini_generate_image`, y después combinarla en una segunda llamada
- Usa `imageSize: "1024x1024"` o "auto" — Banana puede ajustar 9:16 si lo pides explícitamente en el prompt

### Si el motor es Higgsfield (mcp__higgsfield__generate_image):

- Sube la foto base con `mcp__higgsfield__media_upload`
- Pasa el asset_id como `reference_assets`
- Usa `aspect_ratio: "9:16"` explícito
- Si el usuario tiene un Higgsfield Soul de su cara, NO lo uses — está deprecado (ver memoria del usuario)

### Si el motor es BOTH:

Genera con ambos en paralelo:
- Banana → guardar como `slide_N_banana.png`
- Higgsfield → guardar como `slide_N_higgsfield.png`
- Mostrar ambas al usuario lado a lado para comparación A/B

---

## ITERACIÓN

Si la primera generación no quedó bien:

1. **Texto borroso/incorrecto:** repetir con el flag explícito "high resolution text rendering"
2. **Cara morphed:** asegurar que se está pasando la foto como reference (en Banana usar `gemini_edit_image`, NO `gemini_generate_image`)
3. **Cajas no rounded:** ser más explícito en el prompt: "border-radius exactly 14 pixels, NOT square corners"
4. **Highlight no se ve:** especificar "the entire word 'X' has a yellow background highlight, like a marker pen"
5. **Estilo no IG:** agregar al prompt "this is for Instagram, NOT TikTok or other platform"

El usuario tiene un alto estándar visual. Si la primera generación no es 9/10, regenera.
