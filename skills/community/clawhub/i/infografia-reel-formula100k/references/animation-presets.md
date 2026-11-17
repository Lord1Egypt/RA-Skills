# Animation Presets — Prompts para kling3_0 / seedance_2_0

Cada arquetipo tiene un motion prompt específico. Se invoca con
`mcp__higgsfield__generate_video` pasando como `medias[0].value` el `job_id` de la imagen base
(o un media UUID si subiste la imagen) con `role="start_image"`.

**Modelo default**: `kling3_0` con `sound: "off"` y `mode: "std"`.
**Modelo alternativo**: `seedance_2_0` (probar primero si el prompt es 100% genérico, sin nombres de marca).
**Duración estándar**: 8 segundos. Loopeable. (subir a 10-12s si el arquetipo tiene reveal en cascada).
**Aspect ratio**: 9:16 (heredado de la imagen).
**Count**: 1 por defecto.

---

## ⚠️ REGLAS CRÍTICAS (aprendidas en producción)

### Regla 1 — Text Lock (OBLIGATORIO en TODOS los arquetipos)

Los modelos de video tratan el texto como pixeles deformables. Si no se bloquea explícitamente,
una palabra puede romperse en frames intermedios (ej: "sensibles" → "sens egbies"). Por eso
SIEMPRE inyectar este bloque al final del motion prompt:

```
CRITICAL TEXT LOCK: ALL TEXT in the image must remain COMPLETELY FROZEN, PIXEL-PERFECT, and
UNCHANGED throughout the entire animation. Every label, every header, every caption MUST NOT
shift, blur, morph, change letters, warp, fade, or distort at ANY frame. Treat all text as a
locked, immutable overlay layer. Letters stay sharp and readable from frame 1 to last frame.
The exact texts to lock are: '{TEXT_1}', '{TEXT_2}', ... '{TEXT_N}'. Every character stays
identical throughout.
```

Listar TODOS los textos visibles en la imagen, palabra por palabra. Esto le da al modelo el
"target" que debe preservar.

### Regla 2 — Fallback NSFW: kling3_0 antes que seedance_2_0

`seedance_2_0` tiene un moderador NSFW agresivo que da falsos positivos con palabras como
"FURminator", "anti-flea", "deshedding", o nombres de marca. Si el primer intento devuelve
status `"nsfw"`:

1. NO regenerar con seedance_2_0 (mismo bloqueo).
2. Cambiar a `kling3_0` con `sound: "off"`.
3. Suavizar el prompt: quitar nombres de marca, evitar "anti-X" o "deshedding", usar
   sinónimos genéricos ("grooming tool", "fine-tooth comb", "rake").

Por eso el default ahora es `kling3_0`. Sólo usar seedance_2_0 cuando el prompt es 100% limpio
y se requiere identity preservation extrema.

---

## A1 — CROSS-SECTION + DOSAJE

```
Continuous loop animation, no scene cuts, no camera angle changes. Liquid drops continuously fall from each glass dropper bottle at the top into the cross-section below. New drops form at the dropper tips and fall in a loop every 1.5 seconds, with realistic gravity and a small splash where they meet the tissue. The cross-section pulses very subtly as if alive (3% breathing motion). The caption pills at the bottom flicker softly with a 1-frame brightness pulse every 2 seconds. Camera performs a very slow zoom-in (5% over 6 seconds) toward the center of the cross-section. Particles of mist or steam rise gently from the cross-section. Maintain hyperrealistic 3D render style throughout.
```

---

## A2 — DUALIDAD SUCIO/LIMPIO + MINI-TRABAJADORES

```
Continuous loop animation. The mini orange-suit workers on the left half walk in slow motion across the damaged organ surface, some climbing with pickaxes, swinging their arms, releasing small puffs of dust. The mini green-suit workers on the right half spray jets of clean water from their hoses onto the healthy organ — visible water streams arc through the air, splashing on the tissue and sliding down. Some workers scrub with brushes in repetitive arc motion. Subtle parallax on both halves: foreground workers move slightly faster than background. The grid of products at the bottom pulses softly (each item with a 2% breathing scale). Camera holds steady, no zoom. Maintain cinematic dramatic lighting and Octane render style.
```

---

## A3 — PERSONA PARTIDA + BULLETS

```
Subtle photorealistic motion. The person at the center breathes naturally (chest rising slightly), with very subtle eye blink every 3 seconds. The split between the two halves has a soft animated wipe at second 0 (the green half reveals first from left to right over 0.8 seconds, then holds). The bullet captions on each side fade in progressively in cascade — left bullet 1 appears at 0.5s, left bullet 2 at 0.8s, ..., right bullet 1 at 2.0s, right bullet 2 at 2.3s, etc. Each bullet's connecting line draws itself in 0.3 seconds before the text appears. The person's hair has very subtle motion as if a soft breeze is blowing. Camera holds steady. Loop holds the final frame for 1 second before restarting.
```

---

## A4 — GRID COMPARATIVO

```
Cascading reveal animation. Each item in the list appears in sequence: item 1 fades in and slides up 10px at 0.0s, item 2 at 0.3s, item 3 at 0.6s, ..., item N at 0.3s × (N-1). After all items are revealed, the verdict pills (green thumbs-up / red thumbs-down) gently flicker once each in sequence (a soft brightness pulse). The cream paper background has an extremely subtle texture motion as if the paper is breathing. Camera performs a slow pan from top to bottom over 6 seconds (Ken Burns vertical pan, 8% movement). Maintain magazine editorial styling.
```

---

## A5 — STACK DE VARIANTES

```
Sequential reveal animation. The vertical bands appear one by one from top to bottom: band 1 visible at 0.0s, band 2 fades in at 1.0s, band 3 at 2.0s, ..., band N at (N-1) seconds. Each band has a subtle internal motion of the subject (e.g., a leaf gently rotating, a person taking a small breath). After all bands are revealed, the camera performs a slow vertical pan downward to highlight the comparison. The labels on the left ("85MM", "50MM", etc.) flicker into view 0.2 seconds after each corresponding band appears.
```

---

## A6 — DUAL CHARACTER

```
Cards appear in cascade. Both characters at the center are visible from frame 0 with subtle breathing motion. The white cards stacked on each character's torso fade in and slide up from below, in alternating pattern: left card 1 at 0.5s, right card 1 at 0.7s, left card 2 at 1.2s, right card 2 at 1.4s, etc. Each card has a soft glow effect when it appears. The character on the left has subtle robotic mechanical micro-movements (helmet glow pulses), the character on the right has natural human-like breathing and a small head tilt. Backgrounds have animated particles (left: red sparks, right: green digital particles) drifting upward. Camera holds steady.
```

---

## A7 — DIORAMA 3D

```
Each 3D object in the grid rotates slowly on its vertical axis in a continuous loop (one full rotation every 8 seconds), all rotating in the same direction and synchronized. As each object rotates, its label below fades in 0.2 seconds after the object becomes visible. Subtle drop shadows under each object move in sync with the rotation. The flat background has no motion. Camera holds steady. Educational, clean, minimal animation style. Maintain consistent lighting on all objects throughout the rotation.
```

---

## REGLAS DE INVOCACIÓN

1. **medias param**: la imagen base se pasa como referencia inicial. Forma:
   ```typescript
   medias: [{ value: "<job_id_de_la_imagen>", role: "start_image" }]
   ```

2. **Default model**: `kling3_0` con `sound: "off"` y `mode: "std"`. Acepta `start_image` y
   `end_image`. Duración 3-15s, default ahora 8s.

3. **Si el prompt es 100% genérico** (sin nombres de marca, sin "anti-X"), probar primero
   `seedance_2_0`. Si devuelve `status: "nsfw"`, fallback automático a `kling3_0` con prompt
   suavizado (ver Regla 2 arriba).

4. **No pasar `generate_audio`** ni `sound: "on"` salvo que el usuario explícitamente lo pida.
   Para audio, mejor agregarlo en post-producción con el módulo de guionización + voice cloning.

5. **Polling**: el video tarda ~60-180s. Llamar `job_status` con `sync: true` repetidamente
   (cada llamada bloquea hasta 25s). Si pasan 5 minutos sin completarse, abortar y reportar.

6. **Descarga**: cuando el job retorna `status: "completed"`, `results.rawUrl` es la URL del .mp4.
   Descargar con curl a `entregables/infografias/<slug>/02_reel.mp4`.

7. **Inyectar Text Lock SIEMPRE**: el bloque "CRITICAL TEXT LOCK" del header de este archivo
   debe agregarse al final de TODOS los motion prompts antes de invocar generate_video. Listar
   en él los textos visibles en la imagen literal por literal.
