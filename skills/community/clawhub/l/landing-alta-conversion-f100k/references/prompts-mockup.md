# Generación de imágenes de la landing (mockups + testimonios)

La skill genera las imágenes con IA y las embebe como **data-URI** (para mantener 1 solo archivo) o las referencia por URL.

## Motores
- **`banana`** (Gemini Nano Banana) — mejor para mockups de dispositivo limpios, sellos de garantía y composiciones de UI. Rápido y barato. **Motor por defecto.**
- **MCP Higgsfield** (`mcp__higgsfield__generate_image`, modelo `nano_banana_pro`) — cuando se quiere más realismo/fotográfico o un partner-collage complejo.

> ⚠️ Coste: cada imagen consume créditos. Genera solo lo necesario (1 mockup hero + N testimonios + 1 sello opcional). Pregunta antes de generar >6 imágenes.

## 1 · Mockup hero multi-dispositivo
Necesitas una captura real de la plataforma/producto (pídela al usuario). Prompt base:

```
Clean product mockup on a soft off-white studio background (#FBFAF7).
A MacBook laptop, an iPhone and an iPad standing together, slight angle,
soft realistic shadows, each screen showing this app UI: [DESCRIBE UI o usa la captura].
Modern, premium, minimal. No text overlays, no logos. High detail. 4:3.
```
- Si tienes la captura → úsala como imagen de entrada (banana edición / Higgsfield img2img) para que las pantallas muestren el UI real.
- Sin captura → describe el UI (dashboard de curso, módulos en cards, video player).

## 2 · Capturas de testimonio (parecen screenshots reales)
Dos rutas — elige según lo que aporte el usuario:

**A. El usuario aporta capturas reales de DM/WhatsApp/resultados** → úsalas tal cual (mejor conversión, cero coste). Recórtalas limpias.

**B. Generadas** — prompt por testimonio:
```
Realistic smartphone screenshot of a direct-message / results notification.
Shows a short message from "[NOMBRE]" celebrating growth: "[TRANSFORMACIÓN]".
Instagram/WhatsApp-style UI, believable, casual. Spanish text. Vertical 4:5.
No watermark.
```
> Nota: si se generan testimonios, aclarar internamente que son *representativos* y no inventar métricas falsas de personas reales (ver guardarraíl NUNCA inventar data).

## 3 · Sello de garantía (opcional)
La plantilla ya trae un sello en CSS puro (`.seal`). Solo genera imagen si quieren un badge fotográfico:
```
Circular guarantee badge/seal, "[N] DÍAS DE GARANTÍA · 100%", ribbon style,
green and gold, flat vector, transparent background, crisp. PNG.
```

## 4 · Logos de partners
- Pídelos al usuario (SVG/PNG oficiales) — NO los generes (marcas registradas, quedan mal en IA).
- Colócalos en grayscale vía CSS (`filter:grayscale(1)`), ya está en la plantilla.

## Embeber como data-URI (1 solo archivo)
Tras generar/recibir cada imagen, conviértela y reemplaza el `src`:
```bash
# macOS
printf 'data:image/png;base64,'; base64 -i imagen.png | tr -d '\n'
```
Pega el resultado completo en el `{{TOKEN}}` de src. Comprime antes si pesa (>300 KB): usar JPG calidad 80 para fotos, PNG para UI/sellos.
