---
name: landing-alta-conversion-f100k
description: "Use when someone asks to build a high-conversion landing page, a tripwire/launch sales page, a \"landing de alta conversión\", a landing with countdown, price anchoring, bonus stacking, guarantee, FAQ and creator bio, or a landing to upload to GHL or Vercel (estilo The Line Project). Triggers on \"hazme una landing de venta\", \"landing tripwire\", \"landing de lanzamiento con countdown\", \"página de ventas con bonos y garantía\", \"landing para GHL\"."
argument-hint: "[nombre del producto]"
disable-model-invocation: true
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Genera el `index.html` en `entregables/landings/<producto>/` y mándalo por Telegram como documento.
> - No despliegues en Vercel ni en ningún lado sin ✅ explícito y sin que la usuaria haya conectado su propia cuenta.
> - Mockups con Gemini (`GEMINI_API_KEY`) o Higgsfield solo si hay llave o plugin; costo y ✅ antes. Si no, deja los espacios marcados con el prompt de cada imagen.
> - Precios, bonos, garantía y testimonios salen de `cerebro/`: nunca los inventes.

---

# Landing de Alta Conversión (tripwire) — FÓRMULA 100K

Genera **un solo `index.html` self-contained** (CSS/JS/fuentes inline, imágenes data-URI) listo para pegar en **GHL** o subir a **Vercel/Netlify**. Estilo tripwire tipo *The Line Project*: mockup-forward, CTA verde, stacking de bonos con precios tachados, countdown, garantía, FAQ y bio de creadores.

**Referencias de estilo:** thelineproject.netlify.app · f100k-testimonios.vercel.app

## Archivos de esta skill
- `assets/plantilla-base.html` — esqueleto completo con las 9 secciones y `{{TOKENS}}`. **Punto de partida: cópialo y rellena.**
- `references/checklist-conversion.md` — verificación final obligatoria.
- `references/prompts-mockup.md` — cómo generar mockups/testimonios con `banana`/Higgsfield y embeberlos.
- `references/checkout.md` — integrar Hotmart / Stripe / GHL.

---

## Fase 0 — Brief conversacional (una pregunta a la vez)

NO empieces a escribir hasta tener lo esencial. Pregunta en este orden; agrupa solo si el usuario ya adelantó respuestas. Usa `AskUserQuestion` cuando ofrezcas opciones.

1. **Producto & promesa** — nombre del producto, y la promesa/transformación núcleo (con número: "+10.000 seguidores", "30M de vistas"). → sale el H1 y el subheadline.
2. **Oferta** — precio ancla (~~$397~~) y precio oferta ($27); % OFF para el banner de urgencia.
3. **Checkout** — ¿Hotmart, Stripe o GHL? Pide el link de pago. (ver `references/checkout.md`)
4. **Módulos/bonos (8)** — por cada uno: emoji + nombre + 1 línea de descripción + valor individual ($37…). Suma el **valor total** tachado.
5. **Prueba social** — 3-5 testimonios: nombre + transformación medible ("De 500 a 70.000") + 1 frase. ¿Tiene capturas reales o las genero?
6. **Mockup del producto** — ¿tiene captura de la plataforma? (para el mockup multi-dispositivo). Si no, describe el UI.
7. **Tour** — link del video (YouTube/Vimeo/Bunny) → se convierte a URL embed.
8. **Garantía** — días (default 7) + texto.
9. **FAQ** — mínimo las 3 objeciones núcleo (principiante / herramientas extra / tiempo de acceso) + las que quiera.
10. **Creadores** — nombres, historia (1 párrafo), foto, y logos de partners (que los aporte el usuario).
11. **Countdown** — evergreen (X horas por visitante, default 48) **o** fecha fija.
12. **Marca** — colores y fuentes. Default: tema claro (#FBFAF7), CTA verde (#16A34A), acento rosa/rojo para precio, Poppins títulos. Ofrece cambiar.
13. **Destino** — ¿GHL o Vercel? (afecta cómo entregas — ver Fase 4).

Si el usuario pasa un documento/ficha de producto, extrae de ahí lo que puedas y solo pregunta lo que falte.

---

## Fase 1 — Generar imágenes (mockups + testimonios)

Sigue `references/prompts-mockup.md`.

- **Mockup hero** multi-dispositivo con `banana` (motor por defecto) usando la captura real si existe.
- **Testimonios**: si el usuario tiene capturas reales → úsalas. Si no → genéralas con el prompt de la referencia.
- **Sello de garantía**: la plantilla ya trae uno en CSS puro; genera imagen solo si piden badge fotográfico.
- **Logos partners**: los aporta el usuario (no generar marcas registradas).

⚠️ Cada imagen cuesta créditos. **Pregunta antes de generar más de 6.** Prioriza capturas reales del usuario cuando existan.

Embebe cada imagen como **data-URI** (comprimida <300 KB) para mantener el archivo único, o usa URLs absolutas si el usuario prefiere.

---

## Fase 2 — Construir el HTML

1. Copia `assets/plantilla-base.html` como base de trabajo.
2. Reemplaza TODOS los `{{TOKENS}}` con el contenido del brief.
3. **Bloques repetibles** (`<!-- REPEAT:xxx -->…<!-- /REPEAT:xxx -->`): duplica el bloque una vez por ítem (1 por testimonio, 8 por módulo, N por FAQ, N por partner) y borra los comentarios REPEAT del resultado final.
4. Countdown: rellena `{{COUNTDOWN_HORAS}}` y `{{COUNTDOWN_FECHA}}` (uno de los dos; el otro = `null`).
5. Aplica los tokens de marca en `:root`.
6. Copy en **español neutro**, CTAs en 1ª persona y mayúsculas.

**Las 9 secciones (orden fijo):** banner urgencia → hero (H1+sub+mockup+ancla precio+CTA+countdown) → prueba social (carrusel) → 8 módulos + anclaje de valor + CTA → tour video → garantía + CTA → FAQ acordeón → bio creadores + partners → footer legal.

---

## Fase 3 — Verificación

Recorre **`references/checklist-conversion.md`** entero y corrige lo que falle. Presta atención especial a:
- Precio ancla ≥10× oferta; valor total de módulos >> precio.
- 3 CTAs al mismo link.
- FAQ cubre las 3 objeciones.
- Footer legal con Términos + Privacidad + disclaimer de resultados (**Meta rechaza landings sin esto**).
- Responsive a 375px sin desbordes.
- **NUNCA inventar métricas** de personas reales en testimonios ni cifras de resultados.

---

## Fase 4 — Entregar

Guarda el resultado en `entregables/landings/[nombre-producto]/index.html`.

- **Destino GHL**: entrega el HTML pensado para pegar en un bloque Custom Code. Recuerda que `.announce` (banner) y `<footer>` van **FUERA de `#wrapper`** (sticky/fixed dentro de #wrapper se recortan en GHL — regla conocida del ecosistema). Si el checkout es el order form nativo de GHL, el CTA lleva a la ruta del step de pago.
- **Destino Vercel/Netlify**: es un `index.html` listo; ofrece desplegar (`vercel` / drag&drop). Para dominio propio y más robustez, se puede exportar a Next.js con la skill `landing-producto-formula100k`.

Al terminar, muestra al usuario: ruta del archivo, cómo subirlo a su destino, y un recordatorio de reemplazar los links legales (`{{URL_TERMINOS}}` / `{{URL_PRIVACIDAD}}`) por los reales antes de pautar.

---

## Notas y guardarraíles
- **Cierre F100K**: si el producto es del usuario/F100K, todo artifact/LM puentea a la membresía cuando aplique — pero una landing de venta de UN producto NO debe distraer con otro pitch; el único objetivo es el checkout.
- **No confundir** con `landing-producto-formula100k` (Next.js + Stripe + deploy, estilo SaaS oscuro). Esta skill = HTML único, tripwire, GHL-first, mockups IA.
- **No** simular order bump/upsell en HTML estático — se configuran en la pasarela.
- **No** generar logos de marcas registradas con IA.
- **Costo IA**: pregunta antes de generar >6 imágenes; prefiere capturas reales.
- Tono: español neutro (tú/tienes/aquí), sin muletillas de IA.
