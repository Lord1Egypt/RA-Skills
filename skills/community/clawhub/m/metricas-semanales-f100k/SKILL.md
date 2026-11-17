---
name: metricas-semanales-f100k
description: "Módulo del Autopilot F100K que corre cada domingo: extrae las métricas de los posts de la semana del perfil del usuario en Instagram y/o TikTok, identifica el post ganador y por qué funcionó, compara con la semana anterior, y envía un reporte claro con la recomendación de qué replicar la semana siguiente. Usar cuando alguien diga: \"muéstrame mis métricas de la semana\", \"qué funcionó esta semana\", \"cuál fue mi mejor post\", \"reporte semanal de métricas\", \"ejecutar módulo métricas\", o cuando el schedule lo invoque los domingos. Requiere cerebro/f100k-config.json con ig_handle o tiktok_handle configurado."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - El handle sale de `USER.md` o `cerebro/f100k-config.json`.
> - Instagram, en este orden: 1) Composio si Instagram profesional está conectado (trae alcance y guardados reales de la cuenta propia); 2) Apify con `APIFY_TOKEN` (solo datos públicos); 3) si no hay ninguno, pídele a la usuaria capturas de sus estadísticas. Nunca navegador logueado.
> - El informe va por Telegram (no borrador de Gmail) y se guarda en `informes/metricas-AAAA-MM-DD.md`.
> - Si la automatización que te llamó pide comparar contra la mediana, usa la mediana: un solo viral distorsiona el promedio.

---

# Skill: Métricas Semanales — Autopilot F100K

Cada domingo recibes una retrospectiva simple: qué post ganó esta semana, por qué funcionó, y qué replicar la próxima. Sin tener que revisar Instagram Insights ni TikTok Analytics manualmente.

---

## FASE 1 — CARGAR CONFIG

```bash
cat cerebro/f100k-config.json
```

Verificar que exista `ig_handle` o `tiktok_handle`. Si no → preguntar y guardar en config.

Extraer: `niche`, `email`, `ig_handle`, `tiktok_handle`

---

## FASE 2 — EXTRAER MÉTRICAS DE LA SEMANA

### Opción A — Instagram vía Apify

Usar Apify con actor para Instagram profiles:
```json
{
  "username": "[ig_handle sin @]",
  "resultsLimit": 15,
  "scrapeType": "posts"
}
```

Filtrar: solo posts publicados en los últimos 7 días.

Para cada post extraer:
- URL del post
- Caption (primeras 80 chars)
- Fecha de publicación
- Likes
- Comentarios
- Shares / guardados (si disponible)
- Tipo de contenido (Reel / Carrusel / Imagen)

### Opción B — TikTok vía Apify

Usar Apify `clockworks~tiktok-scraper` en modo perfil:
```json
{
  "profiles": ["[tiktok_handle sin @]"],
  "resultsPerPage": 15
}
```

Para cada video extraer:
- URL
- Caption (primeras 80 chars)
- Fecha
- Views (plays)
- Likes
- Comentarios
- Shares
- Duración

Filtrar: últimos 7 días.

---

## FASE 3 — ANÁLISIS

### Paso 3A — Identificar el post ganador

Ordenar posts por métrica primaria:
- **TikTok / Reels**: por Views (reproducción total)
- **Carruseles / Imágenes**: por Engagement Rate = (likes + comentarios + guardados) / alcance

**Post ganador = el #1.**

### Paso 3B — Analizar por qué ganó

Evaluar los siguientes factores comparando el ganador contra el promedio de los demás:

| Factor | Qué mirar |
|--------|-----------|
| Gancho | ¿Las primeras palabras del caption son diferentes a los otros posts? |
| Tema | ¿El tema del ganador coincide con tendencias de la semana? |
| Formato | ¿Es el único Reel / el único Carrusel de la semana? |
| Longitud | ¿Es notablemente más corto o más largo que el promedio? |
| CTA | ¿Tuvo más comentarios? ¿El CTA generó interacción? |

Identificar el factor #1 que explica el éxito.

### Paso 3C — Comparar con semana anterior

Si hay datos de la semana anterior disponibles (en memoria de sesión o historial):
- Views promedio: ↑ o ↓ X%
- Engagement promedio: ↑ o ↓ X%

Si no hay datos anteriores → omitir esta comparación (no inventar números).

### Paso 3D — Recomendación accionable

Basándose en el análisis, generar 1-2 líneas concretas:
- "Replica el formato [X] del ganador — fue el único Reel de la semana y lo demostró"
- "El tema [Y] resonó más que [Z] — prioriza ese ángulo los lunes"
- "El gancho '[texto]' funcionó mejor que los demás — úsalo como plantilla"

---

## FASE 4 — EMAIL DEL DOMINGO

Usar `mcp__claude_ai_Gmail__create_draft`:

**Para:** `config.email`

**Asunto:**
```
📊 Tu semana en números — [lunes] al [domingo] | Autopilot F100K
```

**Cuerpo:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊  MÉTRICAS SEMANALES
Semana del [lunes fecha] al [domingo fecha]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆  POST GANADOR DE LA SEMANA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"[primeras 80 chars del caption]"
📍 [tipo: Reel / Carrusel / TikTok] · 📅 [día publicado]
👁️  [views o plays]  ·  ❤️  [likes]  ·  💬  [comentarios]  ·  🔁  [shares]
🔗 [URL]

POR QUÉ FUNCIONÓ:
→ [Factor principal del éxito]
→ [Factor secundario, si aplica]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋  TODOS LOS POSTS DE LA SEMANA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DÍA       | IDEA (primeras 40 chars)   | VIEWS   | LIKES | COMENTARIOS
[día]     | [idea]                      | [views] | [n]   | [n]
[día]     | [idea]                      | [views] | [n]   | [n]
[...]

Promedio semanal: [X] views/post · [Y] likes/post
[Si hay comparación]: vs semana anterior: [↑/↓ X%]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡  RECOMENDACIÓN PARA LA PRÓXIMA SEMANA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Recomendación específica y accionable basada en los datos reales de la semana]


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autopilot F100K · fórmula100k.app
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
