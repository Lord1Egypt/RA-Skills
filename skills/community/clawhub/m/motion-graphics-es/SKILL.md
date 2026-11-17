---
name: motion-graphics-es
description: |
  Skill de producción de motion graphics en español. Úsala cuando el usuario pida
  "hacer un motion graphic", "animar un logo", "tipografía cinética", "reel/short para redes",
  "explainer", "infografía animada", "lower third", "stinger", "cabecera", "video de producto",
  "presentación animada", o pregunte por brief, storyboard, animatic, ritmo, easing, safe areas,
  entregables o formatos (9:16, 16:9, 1:1, 4:5). Cubre el pipeline completo (brief → sistema →
  animatic → producción → sonido → QC → entrega), con valores por defecto de timing, escalas
  tipográficas, paletas y matrices de entrega por plataforma.
version: 1.0.0
license: MIT
---

# Motion Graphics (ES) — pipeline de producción

Skill de criterio, no de software. Sirve igual para After Effects, Blender, Remotion, canvas o
GSAP porque fija **decisiones** antes que herramientas.

## Cuándo activarse

- Peticiones de piezas animadas: stinger, kinetic typography, explainer, data motion, lower
  third, bumper, ad, demo de producto, presentación animada, loop de fondo.
- Preguntas de proceso: “¿por dónde empiezo?”, “¿cuánto debe durar?”, “¿qué formato entrego?”.
- Preguntas de craft: ritmo, easing, jerarquía, cuánto movimiento es demasiado.

No activar para: edición de material rodado sin gráficos (usar `beat-sync-editing` /
`short-form-edit`), ni para matemática pura (usar `manim`).

## Regla 0 — el brief manda

Nunca empieces a animar sin las 10 líneas del brief. Plantilla lista para copiar:
[`references/brief.md`](references/brief.md).

Si el usuario no da brief, **infiere y declara los supuestos en una lista de 5 líneas**, y
pregunta solo lo que cambia el resultado (formato, duración, tono, entregables). No interrogues.

## Pipeline (7 pasos, con entregable en cada uno)

| # | Paso | Entregable | Tiempo guía (pieza 15 s) |
|---|---|---|---|
| 1 | Brief | 1 página | 10 min |
| 2 | Guion gráfico | 1 línea de texto por beat | 20 min |
| 3 | Tabla de tiempo (EDL de diseño) | escena / in / out / movimiento / SFX | 20 min |
| 4 | Sistema visual | grid, tipografía, paleta, lenguaje de movimiento | 1–2 h |
| 5 | Animatic | pieza en cutre con música, a duración real | 30 min |
| 6 | Producción | pieza final + sonido | 60–80% del total |
| 7 | QC + entrega | matriz de formatos | 30 min |

**El paso 5 no es opcional.** Si el ritmo no funciona con rectángulos grises, no funciona con
diseño bonito.

## Valores por defecto (si no hay dirección de arte)

### Duraciones

| Acción | Duración | Easing |
|---|---|---|
| Aparición de texto corto | 0,35–0,6 s | ease-out expo |
| Salida de cualquier elemento | 0,25–0,35 s | ease-in quad |
| Transición entre escenas | 0,2–0,5 s | ease-in-out cubic |
| Logo reveal completo | 1,0–2,5 s | custom + overshoot |
| Count-up numérico | 0,8–1,2 s | ease-out expo (nunca elástico) |
| Hold mínimo para leer | 0,8 s + 0,05 s por palabra | — |
| Stagger entre elementos | 2–4 frames (0,07–0,13 s) | linear en el desfase |

### Escala tipográfica (base 1920×1080)

`96 / 64 / 40 / 24 / 16 px` (ratio ≈1.5). En 1080×1920 baja un escalón: `72 / 52 / 34 / 22`.
Máximo **dos** familias: una display (peso alto, tracking cerrado) y una de texto.

### Lenguaje de movimiento (firma de autor)

Define 4 parámetros y respétalos en toda la pieza:

```
entrada      : ease-out expo, 0.45s
salida       : ease-in quad, 0.30s
stagger      : 3 frames
overshoot    : máx 6% de escala
rotación     : solo si tiene intención física
```

### Paleta

Fondo + 1 acento + 1 soporte + 1 neutro. Contraste texto ≥ 4.5:1. Anima en OKLCH/Lab (ver skill
`color-motion`), no en RGB: evita el gris muerto en los degradados.

## Reglas de composición

- Un foco por momento. Si dos elementos compiten, el ojo no lee.
- Respeta el **grid de 12 columnas** con márgenes 5–8%.
- Safe areas por plataforma: [`references/formatos.md`](references/formatos.md).
- Deja respirar: al menos un hold por cada 3–4 s de movimiento continuo.
- El movimiento debe tener **dirección con sentido** (entra desde donde venía, sale hacia donde
  va). Nada de “vuela desde la izquierda porque sí”.

## Ritmo: deriva todo del BPM

```
frames_por_pulso = (60 / BPM) * fps
```

Con 120 BPM y 30 fps: 1 pulso = 15 frames, 1 compás = 60 frames. Cortes en pulso o medio pulso;
salidas off-beat. Detalle y tabla en [`../audio-post-motion/SKILL.md`](../audio-post-motion/SKILL.md)
y en `docs/02-guia-edicion-audiovisual.md`.

## Antipatrones (lo que delata a un aficionado)

1. Todo con `linear` o con el `easy ease` por defecto.
2. Todo entra y nada sale (o todo rebota).
3. Sombra + glow + blur + grano en la misma pieza.
4. Texto que se mueve más rápido de lo que se puede leer.
5. Rejilla rota entre escenas: cada escena inventa sus márgenes.
6. Música sin relación con los movimientos (o SFX 4 frames tarde).
7. Exportar 4:5 desde 16:9 estirando la imagen.
8. `final_final_v2.mp4`.

## Cómo elegir herramienta

```
¿La pieza se repite muchas veces con datos distintos?     → Remotion (remotion-video)
¿Es matemática/educativa con curvas y ecuaciones?         → Manim (manim)
¿Es tipografía pura, editorial, alto impacto?             → kinetic-reel / kinetic-typography
¿Es overlay con transparencia para OBS/Premiere?          → lower-thirds
¿Es edición de material rodado + gráficos encima?         → talking-head-b-roll / short-form-edit
¿Es 3D procedural o marca con volumen?                    → Blender / Cinema 4D / three.js (webgl-animation)
¿Es UI/producto interactivo?                              → Rive / Lottie
```

## Entregables por defecto

Siempre: **master ProRes** + **MP4 H.264** + **versión muda** + **poster frame**.
Si hay voz: **`.srt`**. Si es overlay: **WebM alpha + ProRes 4444**.
Si va a redes: 9:16 y 1:1 reencuadrados, no rediseñados.

Matriz completa: [`references/formatos.md`](references/formatos.md).

## QC obligatorio antes de entregar

- [ ] ¿Se entiende sin audio?
- [ ] ¿Cada elemento tiene entrada y salida?
- [ ] ¿Hay al menos un hold?
- [ ] ¿Textos dentro de safe area en el formato final?
- [ ] ¿Loudness medido (−14 LUFS web / −23 LUFS broadcast)?
- [ ] ¿El MP4 abre en VLC sin cuadros negros?
- [ ] ¿Nombres normalizados `AAAA-MM-DD_cliente_pieza_formato_v##`?

## Recursos internos del repo

- `docs/01-que-es-motion-graphics.md` — teoría, taxonomía de piezas, glosario.
- `docs/02-guia-edicion-audiovisual.md` — ritmo, sonido, códecs, color.
- `docs/03-tutorial-practico.md` — tutorial completo + 3 ejercicios.
- `demo/` — reel interactivo en canvas + WebAudio (referencia ejecutable de easing y beat sync).
- `.claude/skills/` — 37 skills de terceros para ejecutar cada parte.
