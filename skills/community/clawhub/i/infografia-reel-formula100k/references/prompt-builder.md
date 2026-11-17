# Prompt Builder — Plantillas para nano_banana_2

Fórmulas de prompt para generar la imagen base con `mcp__higgsfield__generate_image` modelo
`nano_banana_2`. Cada plantilla está optimizada para que el modelo:
1. Mantenga el aspect ratio 9:16 estricto
2. Renderice texto LEGIBLE (nano_banana_2 es el mejor de Higgsfield para esto)
3. Mantenga consistencia visual del arquetipo

---

## FÓRMULA UNIVERSAL

Todo prompt sigue esta estructura:

```
[CALIDAD] + [TIPO DE TOMA] + [ASPECTO] + [SUJETO PRINCIPAL] + [ELEMENTOS DEL ARQUETIPO]
+ [TEXTO LITERAL] + [PALETA Y MOOD] + [ESTILO DE RENDER]
```

**Bloques fijos universales:**
- CALIDAD: `Hyperrealistic 3D render, ultra-detailed, cinematic studio lighting, depth of field, 8K`
- ASPECTO: `9:16 vertical infographic poster, full canvas composition`
- ESTILO DE RENDER: `Octane render style, photoreal materials, sharp focus on subject`

**Texto literal:**
Cuando incluyas texto que DEBE aparecer exacto, ponlo entre `""` y precedido de `with text reading`:

```
with text reading "KIDNEY CLEANING DRINKS" in bold uppercase white sans-serif at the bottom
```

---

## A1 — CROSS-SECTION + DOSAJE

```
Hyperrealistic 3D render, ultra-detailed, cinematic studio lighting, 9:16 vertical infographic poster, dark navy background.

Top of the frame: a horizontal row of {N} glass dropper bottles aligned side by side, each bottle a different liquid color. Bottle 1 contains {liquid_color_1} liquid labeled "{ITEM_1}". Bottle 2 contains {liquid_color_2} liquid labeled "{ITEM_2}". {... resto de items}. Each bottle has a single drop of liquid suspended in mid-air falling toward the cross-section below.

Center of the frame: a hyperrealistic anatomical cross-section of {órgano}, showing internal structures (capas/poros/glandulae/túbulos según corresponda), with each falling drop reaching a different visible reaction point in the tissue.

Bottom of the frame: a row of {N} white rounded caption pills with black text reading: "{BENEFICIO_1}", "{BENEFICIO_2}", {... resto}.

Above the row of caption pills, large bold uppercase white sans-serif text reading "{HOOK}".

Top center, small semi-transparent watermark text "@{HANDLE}".

Octane render, ultra-photoreal materials, glass refraction on bottles, anatomical accuracy, sharp focus, dramatic side lighting, 8K.
```

**Variables a llenar:**
- `{N}`: número de items (3-5 ideal)
- `{ITEM_i}`: nombre del ingrediente UPPERCASE
- `{liquid_color_i}`: color del líquido en inglés (clear, amber, pale yellow, deep red, milky white)
- `{órgano}`: órgano/tejido en inglés (skin layers, kidney, liver, intestine, hair follicle)
- `{BENEFICIO_i}`: 3-5 palabras describiendo el beneficio
- `{HOOK}`: 1-3 palabras UPPERCASE
- `{HANDLE}`: opcional, si el usuario quiere watermark

---

## A2 — DUALIDAD SUCIO/LIMPIO + MINI-TRABAJADORES

```
Hyperrealistic 3D render, cinematic dramatic lighting, 9:16 vertical poster split exactly 50/50 vertically.

Top center: bold uppercase text "{HOOK}" in white. Below it, two smaller pills: red pill on the left reading "{SUB_HOOK_A}" (the bad side), green pill on the right reading "{SUB_HOOK_B}" (the good side).

Left half: a hyperrealistic {órgano} that is damaged, oxidized, brown-rusty colored, cracked surface, with dark patches and tar-like buildup. {N} mini 3D Playmobil-style human workers in orange hazmat suits with helmets, scattered around the organ — some climbing on it with pickaxes, some standing in front, all in ant-scale next to the giant organ.

Right half: the SAME {órgano} but healthy, glossy, fresh pink color, clean surface, with subtle highlights. {N} mini 3D Playmobil-style human workers in green/white hazmat suits with hoses spraying clean water onto the organ, some scrubbing with brushes, some holding hoses high.

Below both halves: a 4-column or 2x4 grid of photorealistic product items. Left grid items relate to "{SUB_HOOK_A}" (bad foods like {ITEM_BAD_1}, {ITEM_BAD_2}, ...). Right grid items relate to "{SUB_HOOK_B}" (good foods like {ITEM_GOOD_1}, {ITEM_GOOD_2}, ...). Each item with a small white caption pill below it reading the item name.

Background: subtle dark gradient with hints of red on the left and green on the right.

Octane render, photoreal materials, ant-scale mini figurines for cinematic scale contrast, sharp focus, 8K.
```

**Variables:**
- `{HOOK}`: ej "BLOOD CLEANING"
- `{SUB_HOOK_A}` / `{SUB_HOOK_B}`: ej "DIRTY BLOOD" / "CLEAN BLOOD"
- `{órgano}`: ej "kidney", "liver", "section of blood vessels"
- `{N}`: 4-6 mini-trabajadores por lado
- `{ITEM_BAD_i}` / `{ITEM_GOOD_i}`: 4-8 items por lado

---

## A3 — PERSONA PARTIDA + BULLETS

```
Hyperrealistic editorial photography, 9:16 vertical poster, soft cinematic lighting, neutral gradient background.

Center: a single {género} {edad}, {descripción rasgos}, photographed straight-on from chest up, face looking at camera with neutral expression. The image is split EXACTLY down the vertical center of the face/body. 

Left half: warm/red-orange tone, slightly desaturated, simulating "{HOOK_A}" state ({mood_A}: e.g. tired, stressed, dull skin, dark under-eye circles, tense shoulders).

Right half: cool/green-fresh tone, slightly brighter, simulating "{HOOK_B}" state ({mood_B}: e.g. radiant, calm, bright eyes, hydrated skin, relaxed posture).

Top of frame: large bold uppercase serif text "{HOOK_A}" on the left half (in red), "vs" small in the center, "{HOOK_B}" on the right half (in green).

Around the person, on each side, 4-5 small caption text bullets with thin lines pointing to the corresponding body part. Each bullet has a tiny minimalist icon and short text:
Left bullets (3-4 words each): {BULLET_A_1}, {BULLET_A_2}, {BULLET_A_3}, {BULLET_A_4}, {BULLET_A_5}.
Right bullets (3-4 words each): {BULLET_B_1}, {BULLET_B_2}, {BULLET_B_3}, {BULLET_B_4}, {BULLET_B_5}.

Bottom: thin tagline text "{tagline}" centered in white.

Photoreal portrait style, soft skin texture, professional editorial color grading, sharp eyes, 8K.
```

---

## A4 — GRID COMPARATIVO

```
Hyperrealistic still-life photography, 9:16 vertical poster, soft natural lighting, cream paper background with subtle paper texture.

Top: large display serif text "{HOOK}" in dark color, sub-line below in smaller serif "{SUBHOOK}".

Body: a vertical zigzag layout of {N} food/object items, alternating left-right. Each item is a hyperrealistic photo of the item ({ITEM_1}, {ITEM_2}, ..., {ITEM_N}) with a soft drop shadow. Next to each item, a label reading the item name in serif typography, plus a small horizontal pill with the verdict. Verdict pill colors:
- Green pill with thumbs-up icon for {GOOD_ITEMS}
- Red pill with thumbs-down icon for {BAD_ITEMS}
- Neutral grey pill with text-only verdict for {NEUTRAL_ITEMS}

Background: warm cream tone with subtle botanical illustration ghost overlay.

Bottom: small footer line "{footer}" centered.

Photoreal food/object styling, magazine editorial layout, soft top-down lighting, sharp focus on each item, 8K.
```

---

## A5 — STACK DE VARIANTES

```
Hyperrealistic photography, 9:16 vertical poster split into {N} horizontal bands of equal height.

Each band shows the SAME {sujeto/escena}, photographed from the SAME angle, but with the parameter "{parámetro}" set to a different value:
Band 1: parameter = "{VALUE_1}", visual difference: {DIFFERENCE_1}.
Band 2: parameter = "{VALUE_2}", visual difference: {DIFFERENCE_2}.
... (continue for all bands)
Band N: parameter = "{VALUE_N}", visual difference: {DIFFERENCE_N}.

On the left of each band, a small white pill with bold uppercase text reading "{VALUE_i}".

No header text. Continuous bands without spacing between them.

Photoreal, consistent subject across bands, only the parameter changes, 8K.
```

---

## A6 — DUAL CHARACTER

```
Hyperrealistic 3D render, 9:16 vertical poster split exactly 50/50 vertically, cinematic side lighting.

Top: small semi-transparent watermark "@{HANDLE}".
Below the watermark, two pills: red pill on the left reading "{HOOK_A}", green pill on the right reading "{HOOK_B}".

Left half: full-body or half-body shot of {CHARACTER_A} (e.g. retro robot from 2025, wearing futuristic plain helmet, white armor, black background gradient red).
Right half: full-body or half-body shot of {CHARACTER_B} (e.g. modern robot from 2026, sleek black helmet, casual t-shirt and jeans, background gradient green).

On each character's torso, a vertical stack of {N} white rounded cards. Each card has a small label above it ({CATEGORY_i} like "Estudio", "Pesquisa", "Automação", "Vídeo") and a logo/icon inside the card with the tool name. Cards are sized roughly the same and stacked with small gaps.

Left character cards: {CARD_A_1}, {CARD_A_2}, {CARD_A_3}, {CARD_A_4}.
Right character cards: {CARD_B_1}, {CARD_B_2}, {CARD_B_3}, {CARD_B_4}.

Octane render, photoreal materials, dramatic rim lighting, contrast between sides, 8K.
```

---

## A7 — DIORAMA 3D DE OBJETOS

```
3D isometric stylized render, 9:16 vertical poster, flat solid background ({BG_COLOR}, e.g. dusty blue, soft grey).

Top: bold display text "{HOOK}" in bold sans-serif, white or contrasting color, centered.

Body: a 3-column grid of {N} miniature 3D models of {OBJETO} variants. All renders use the SAME camera angle (3/4 perspective), the SAME lighting, and the SAME materials/style — only the FORM of the object changes per variant. Variants:
1. {VARIANT_1} — {DESCRIPTION_1}
2. {VARIANT_2} — {DESCRIPTION_2}
... (continue for all)

Below each object, white sans-serif text label reading the variant name "{VARIANT_NAME_i}".

Soft drop shadows under each object. Consistent scale across all objects.

3D educational illustration style, clean, minimal, like an architecture textbook, 8K.
```

---

## REGLAS DE TEXTO PARA NANO_BANANA_2

1. **Siempre con comillas dobles** y precedido de `text reading`.
2. **UPPERCASE** para hooks y títulos. Sentence case para descripciones.
3. **Limita el texto literal a 30-50 palabras totales** en la imagen — más texto = más errores de renderizado.
4. **Específica posición exacta**: `at the top center`, `bottom-left corner`, `under the bottle`.
5. **Específica fuente**: `bold uppercase sans-serif`, `display serif`, `monospace`.
6. **Si el texto sale mal**, regenerar con la misma seed pero reformulando el bloque de texto literal.

---

## EJEMPLO COMPLETO LLENADO (A1)

```
Hyperrealistic 3D render, ultra-detailed, cinematic studio lighting, 9:16 vertical infographic poster, dark navy background.

Top of the frame: a horizontal row of 5 glass dropper bottles aligned side by side, each bottle a different liquid color. Bottle 1 contains clear liquid labeled "COCONUT WATER". Bottle 2 contains pale yellow liquid labeled "LEMON WATER". Bottle 3 contains pale green liquid labeled "CUCUMBER WATER". Bottle 4 contains amber liquid labeled "BARLEY WATER". Bottle 5 contains deep red liquid labeled "CRANBERRY JUICE". Each bottle has a single drop of liquid suspended in mid-air falling toward the cross-section below.

Center of the frame: a hyperrealistic anatomical cross-section of a kidney showing internal structures (cortex, medulla, renal pyramids, calyces), with each falling drop reaching a different visible reaction point in the tissue.

Bottom of the frame: a row of 5 white rounded caption pills with black text reading: "Removes toxins", "Neutralizes acid", "Hydrates tissues", "Natural diuretic", "Antibacterial".

Above the row of caption pills, large bold uppercase white sans-serif text reading "KIDNEY CLEANING DRINKS".

Top center, small semi-transparent watermark text "@truebalance".

Octane render, ultra-photoreal materials, glass refraction on bottles, anatomical accuracy, sharp focus, dramatic side lighting, 8K.
```
