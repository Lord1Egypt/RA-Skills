# MODO CLONAR ESTILO — Higgsfield (motor principal)

Replica el estilo de UNA captura de referencia (miniatura/portada de otra persona) poniendo la CARA del usuario, y manda a generar a Higgsfield vía MCP. Este es el modo que mejor convierte: copia composición + estética probada y solo cambia la identidad.

> Aprendido en producción el 2026-06-28 (caso "my secret Reels formula" → la creadora en oficina futurista). Las 4 variaciones salieron con identidad clavada, flash disposable, fecha en esquina y SIN texto.

---

## CUÁNDO USAR ESTE MODO

Activar SIEMPRE que el usuario diga algo como:
- "quiero esta miniatura pero con mi cara"
- "clona este estilo / esta portada / esta foto"
- "réplica esta miniatura usando mi foto"
- "mándalo a hacer a Higgsfield"
- o adjunte **una captura de referencia + una foto suya**.

---

## IDENTIDAD FINA (si los rasgos no salen parecidos)

Si con UNA selfie la cara no sale 100% parecida, subir la fidelidad así (fórmula probada):

1. **Usar 3 selfies frontales y nítidas** como identidad (no una sola; evitar perfil/mucho maquillaje). Idealmente una **con los mismos lentes** que la miniatura. Carpeta del usuario si la tiene configurada (p. ej. `cerebro/fotos`); si no, pídele las 3 fotos. Tip: arma un contact sheet con HTML+Chrome para escoger rápido.
2. **resolution: "4k"** (mejora bastante la fidelidad facial vs 2k).
3. **Prefijo de énfasis de identidad** al inicio del prompt:
   `"This is a photo of the SAME real woman shown in the FIRST THREE reference photos. Preserve her EXACT identity and facial structure with maximum fidelity — same face shape, eyes, eyebrows, nose, lips, cheeks, glasses. Do NOT invent a different face."`
4. **Reusar una generación previa que ya gustó como referencia de COMPOSICIÓN** (4ª imagen) + 3 selfies de identidad. Decir explícito: `"USE THE FOURTH image ONLY for pose, framing, lighting, background and style. IGNORE its face — her face comes strictly from the first three photos."` Así refinas identidad sin perder el look ganador.
5. Orden en `medias[]`: **las 3 selfies primero**, la referencia de composición al final.

## ICONOS Y "?" EN LA GENERACIÓN (opcional)

Nano Banana Pro sí puede generar los gráficos de la referencia (no solo en Canva), pidiéndolos explícitos en un bloque `GRAPHIC OVERLAYS TO INCLUDE`. Probado y sale bien:
- `A large glowing white question mark '?' on the smartphone screen she is holding (dark screen, bright white '?').`
- `A clean white Instagram camera glyph icon floating near her.`
- `A small rounded notification bubble showing a person silhouette icon and the number '25K'.`

Aun así, **el headline en español (la frase larga) va en Canva/overlay HTML**, no en la generación (evita faltas de ortografía). Tip de layout: si quieres el headline a la izquierda, elige la variación donde los iconos/burbuja quedaron a la DERECHA junto al celular para que no choquen.

---

## REGLA DE ORO (por qué Higgsfield "no entiende")

El error #1 es pasar la referencia y la selfie sin decir **qué tomar de cada una**. Nano Banana mezcla las dos caras. La solución:

1. **Etiquetar las imágenes explícitamente** en el prompt: `FIRST reference image` = identidad; `SECOND reference image` = pose/composición.
2. **Selfie SIEMPRE primero** en el array `medias[]` (prioriza la identidad del usuario).
3. **Prompt en INGLÉS y en modo instrucción** (qué SÍ / qué NO). Nada de narración en español.
4. **Bloque `MUST NOT INCLUDE`** obligatorio para matar texto, logos y burbujas de la referencia (esos se ponen después en Canva).
5. **No alterar rasgos**: `Do not alter her facial features in any way`.

---

## ESTILO FIRMA F100K (default del canal de YouTube)

Para miniaturas del canal del usuario, el default NO es overlay HTML — es **TODO horneado en Higgsfield** (nano_banana_pro/2k renderiza texto corto en español perfecto: tildes, ¿?, %, splits). Su firma validada:
1. El usuario **recortada, plano medio, GESTICULANDO** (mano abierta presentando, señala, sostiene celular). Cara real con sus 3 selfies + énfasis de identidad.
2. **Fondo con contexto oscurecido + viñeta**, NUNCA vacío negro plano. Su favorito: **"pizarra científica"** = tablero oscuro con diagramas blancos dibujados a mano (curva de tensión/story-arc, cerebros, embudos, nodos, flechas, ecuaciones abstractas). Difuminado para que cara y texto resalten.
3. **Lockup de texto horneado:** palabra(s) en BLANCO arriba (contorno negro fino) + **caja AMARILLA #FFD21E con texto NEGRO y sombra dura** abajo. Fuente condensada pesada (estilo Anton).
4. Apoyos: flecha verde +$, lápiz/ícono, logos IG/TikTok glossy, gráficas verde-bueno/rojo-malo.
Frase clave en el prompt: `"In the SIGNATURE high-CTR YouTube thumbnail style of FÓRMULA 100K"`. Mantener el texto CORTO (1 palabra blanca + 3-4 palabras en la caja). Ver [[project-miniaturas-youtube]].

> Si la usuaria dice "no me gusta, es con pizarra científica / mi estilo": NO uses overlay HTML naranja tipo tutorial — hornea el lockup en Higgsfield con la firma de arriba.

## PASO A — Decodificar el estilo de la referencia

Mirar la captura y extraer (esto alimenta el prompt):

| Eje | Qué leer de la referencia |
|-----|---------------------------|
| **Encuadre** | ¿Plano medio? ¿Cabeza y hombros? ¿Persona a izquierda/derecha/centro? |
| **Pose / gesto** | ¿Sostiene un objeto (celular, producto)? ¿A qué altura? ¿Señala? |
| **Expresión** | Media sonrisa confiada, sorpresa, seria, complicidad |
| **Estética foto** | disposable/flash, cinematográfica, estudio limpio, UGC casual, grano |
| **Iluminación** | flash duro frontal, luz suave, neón, contraluz |
| **Fondo** | (se reemplaza por lo que pida el usuario, pero leer el original) |
| **Detalles firma** | date stamp, viñeta, bordes, color dominante |
| **Texto/gráficos** | anotar para REPLICAR LUEGO en Canva — NO meterlos en la generación |

Escribir 3-4 bullets de "ADN del estilo" antes de generar.

---

## PASO B — Subir las imágenes a Higgsfield

**Necesitas 2 imágenes:** (1) la SELFIE del usuario, (2) la CAPTURA de referencia.

### B.1 — Si son archivos locales (Claude Code / terminal)
Usar `mcp__higgsfield__media_upload` con `files[]` para obtener presigned URLs, subir bytes con curl, y confirmar:

```
1. media_upload  → files:[{filename:"selfie.jpg",content_type:"image/jpeg"},
                           {filename:"ref.png",  content_type:"image/png"}]
   → devuelve upload_url + media_id por cada una
2. curl -X PUT -H "Content-Type: <tipo>" --data-binary @archivo '<upload_url>'   (por cada una)
3. media_confirm → type:"image", media_ids:[<id_selfie>, <id_ref>]
```
> Tip: si el nombre del archivo tiene caracteres raros (capturas de macOS con espacios/NBSP), cópialo antes a una ruta limpia en el scratchpad (`cp "$(ls | grep <patrón>)" ref.png`).

### B.2 — Si el cliente es Apps UI (Claude Desktop/web con widget)
Llamar `mcp__higgsfield__media_upload_widget` (type:"image", min_files:2) para que el usuario suba selfie + referencia desde el navegador. Devuelve los `media_id`.

---

## PASO C — Generar con nano_banana_pro

Modelo: **`nano_banana_pro`** · `resolution:"2k"` · `aspect_ratio:"16:9"` · `count:4`.
`medias[]`: **selfie primero**, referencia segunda, ambas con `role:"image"`.

### Plantilla de prompt (rellenar los [corchetes] con el ADN del Paso A)

```
Candid [ESTÉTICA, ej: disposable-camera flash] photo for a YouTube thumbnail.

IDENTITY (use the FIRST reference image): use the EXACT face, identity,
[color/largo de pelo], and [lentes/rasgos distintivos] of the woman in the
first image. Do not alter her facial features in any way — same face, same
person, same eyes, same nose, same lips. Keep her natural skin and features.

POSE & COMPOSITION (use the SECOND reference image): [describir pose y gesto
de la referencia, ej: seated facing camera with a subtle confident half-smile,
holding up a smartphone at chest height, screen toward the camera]. Same
framing and gesture, she occupies the [right-center] of the frame.

STYLE: [estética detallada, ej: authentic point-and-shoot disposable camera
look — direct hard on-camera flash, slight film grain, slightly blown
highlights]. [Detalle firma, ej: small orange date stamp in the bottom corner].

BACKGROUND: [lo que pidió el usuario, ej: a sleek futuristic modern office,
soft neon accent lighting, glass and tech panels, softly out of focus].

MUST NOT INCLUDE: no text, no captions, no title, no words, no logos, no
follower-count bubble, no graphic overlays. Clean image, person only.

High-contrast, sharp subject, photorealistic, professional thumbnail quality, 16:9.
```

> El texto, logos y burbujas de la referencia se replican DESPUÉS en Canva (ver Paso E). Mantener la generación limpia da imágenes mucho más nítidas y editables.

---

## PASO D — Esperar y descargar

```
- job_status(jobId, sync:true) por cada job hasta status:"completed"
  (imagen ~10-20s; si in_progress trae poll_after_seconds, esperar y reintentar)
- Tomar results.rawUrl de cada uno
- curl -s -o var_X.png "<rawUrl>"   → guardar en
  entregables/miniaturas/AAAA-MM-DD_<slug>/
- Read cada PNG para evaluar parecido y elegir la ganadora
```

Verificar saldo antes con `mcp__higgsfield__balance` si hay dudas (cada imagen 2K cuesta ~créditos; `get_cost:true` en generate_image preflightea sin gastar).

---

## PASO E — Entregar + texto en Canva

1. Mostrar las 4 variaciones con sus rutas.
2. Recomendar la ganadora (parecido + nitidez + composición + "set" del fondo).
3. Recordar que el **texto/logo/burbuja** de la referencia se montan encima en Canva (manuscrito blanco, ícono de plataforma, burbuja de seguidores) — replicando la tipografía de la referencia.
4. Ofrecer iterar: cambiar fondo, expresión o reencuadre con otra corrida.

---

## CHECKLIST DEL MODO CLONAR

- [ ] Leí el ADN del estilo de la referencia (encuadre, pose, estética, firma)
- [ ] Selfie va PRIMERO en medias[], referencia segunda
- [ ] Prompt en inglés, con `FIRST/SECOND reference image` etiquetadas
- [ ] Incluí bloque `MUST NOT INCLUDE` (sin texto/logos)
- [ ] Incluí `Do not alter her facial features`
- [ ] nano_banana_pro, 2k, 16:9, count 4
- [ ] Descargué a la carpeta de entrega y revisé el parecido
- [ ] Avisé que el texto se pone en Canva al final
