# Formatos, safe areas y entregables

## Resoluciones y safe areas

| Formato | Uso | Resolución | Safe area texto (aprox.) |
|---|---|---|---|
| 16:9 | YouTube, web, presentación, TV | 1920×1080 (4K: 3840×2160) | 5% márgenes; 20% inferior reservado a controles/end cards |
| 9:16 | Reels, TikTok, Shorts, Stories | 1080×1920 | 12–15% arriba y abajo, 6% laterales |
| 4:5 | Feed Instagram | 1080×1350 | 5% |
| 1:1 | Feed clásico, ads | 1080×1080 | 8% |
| 2.39:1 | Cine / cabecera | 2048×858 | 5% |
| 3:2 | Web hero / fotografía | 1620×1080 | 5% |

**Regla de reencuadre:** nunca estires. Rediseña el encuadre: en 9:16 la tipografía sube de
escala y la composición se vuelve vertical; los elementos laterales migran a arriba/abajo.

## FPS

| FPS | Cuándo |
|---|---|
| 24 | Sensación cine, motion editorial |
| 25 | Broadcast PAL / Europa |
| 30 | Default web y social |
| 50/60 | UI, deporte, movimientos muy rápidos, capturas de pantalla |

Anima siempre a la misma velocidad de fotogramas que exportas. Reescalar el tiempo al final
introduce judder.

## Matriz de entregables

| Pieza | Master | Distribución | Alpha | Extra |
|---|---|---|---|---|
| Stinger / logo | ProRes 422 HQ | H.264 MP4 | ProRes 4444 + WebM VP9 | WAV del audio logo |
| Kinetic type | ProRes 422 HQ | H.264 MP4 16:9 + 9:16 | — | `.srt`, versión muda |
| Explainer | ProRes 422 HQ | H.264 MP4 | — | SRT, capítulos, script, CSV de datos |
| Lower third | ProRes 4444 | — | ProRes 4444 + WebM VP9 | MOGRT / plantilla |
| Social ad | ProRes 422 HQ | H.264 MP4 (3 formatos) | — | poster frame, copies |
| Loop de fondo | ProRes 422 HQ | H.264 + WebM | — | primer y último frame idénticos |
| Presentación animada | ProRes 422 HQ | H.264 MP4 | — | PPTX/Keynote con clips, PDF |

## Ajustes de export H.264 (referencia)

```
Perfil           : High
Nivel            : 4.2 (1080p) / 5.1 (4K)
Pixel format     : yuv420p  (obligatorio para compatibilidad)
Color            : Rec.709 (bt709 en los tres flags), rango limitado (tv)
Bitrate / CRF    : crf 18 master · crf 20–23 distribución
Audio            : AAC-LC 48 kHz, 192 kbps estéreo
Faststart        : sí (+faststart) para streaming inmediato
Keyframe         : cada 2 s (GOP 60 a 30 fps)
```

## Nombres de archivo

```
2026-10-25_acme_lanzamiento_9x16_v03.mp4
{AAAA-MM-DD}_{cliente}_{pieza}_{formato}_{v##}.{ext}
```

Un `v##` por render entregado, con changelog de 3 líneas por versión.
