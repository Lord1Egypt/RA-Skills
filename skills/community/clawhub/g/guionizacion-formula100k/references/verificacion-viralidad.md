# Módulo: Verificación de Viralidad con Referencia Real

Este módulo se ejecuta DESPUÉS de elegir la estructura y ANTES de escribir el guion final.
Su objetivo es buscar videos virales reales sobre el tema del guion, extraer el patrón
de su gancho, y reescribir el hook con esa referencia como base.

---

## CUÁNDO EJECUTAR ESTE MÓDULO

Ejecutar siempre que:
- Se esté escribiendo un guion nuevo
- El usuario pida "verificar viralidad" o "buscar referencias virales"
- El usuario mencione querer basar el gancho en contenido que ya funcionó

---

## HERRAMIENTAS DISPONIBLES (usar en este orden de prioridad)

### 🥇 NIVEL 1 — MCPs Sociales (datos reales, métricas reales)
Si el usuario tiene alguno de estos MCPs conectados, usarlo PRIMERO:

| MCP | Plataformas | Cómo conectar (Claude Desktop) |
|-----|-------------|-------------------------------|
| **Xpoz** | TikTok + Instagram + Twitter + Reddit | `Settings → Connectors → https://mcp.xpoz.ai/mcp` (requiere Xpoz API token) |
| **Instagram MCP** | Instagram | `smithery mcp add instagram` |
| **Supadata** | TikTok + Instagram + YouTube | `smithery mcp add supadata-ai/mcp` |
| **davibauer/tiktok-mcp** | TikTok | `smithery mcp add davibauer/tiktok-mcp` |

Con estos MCPs activos, buscar directamente:
- `search_tiktok_posts("Asakusa Tokyo secreto viral")` → vistas reales, hashtags, ganchos exactos
- `search_instagram_reels("Japan hidden temple")` → engagement real, descripciones, hooks

### 🥈 NIVEL 2 — Búsqueda Web (fallback si no hay MCPs sociales)
Usar `web_search` con queries optimizadas para extraer lo indexado por Google de TikTok/Instagram.
Detecta patrones de ganchos pero NO métricas exactas de vistas.

### 🥉 NIVEL 3 — Análisis de patrones del nicho (sin internet)
Si tampoco hay búsqueda web, analizar patrones generales del nicho basados en conocimiento
de qué estructuras de gancho funcionan en contenido de viajes / cultura japonesa.

---

## PROCESO OBLIGATORIO: 4 PASOS

### PASO 1 — Extraer la palabra clave del guion

Antes de buscar, identificar:
- **Tema principal** del guion (ej: "Asakusa Tokyo", "templo secreto Japón")
- **Ángulo narrativo** (historia oculta, dato sorprendente, lugar desconocido, etc.)
- **Audiencia objetivo** (viajeros, curiosos, cultura japonesa, etc.)

Construir 2 queries de búsqueda:
- Query 1 → enfocada en TikTok: `site:tiktok.com [tema] viral millones vistas`
- Query 2 → enfocada en Instagram/general: `[tema] reels viral [año actual] millones`
- Query 3 → enfocada en el ángulo narrativo: `"[tema]" "secreto" OR "nadie sabe" OR "desconocido" viral`

---

### PASO 2 — Buscar videos virales reales

**Si hay MCP social conectado (Xpoz / Instagram / TikTok / Supadata):**
Usar la herramienta del MCP directamente para buscar en la plataforma con la keyword extraída.
Ejemplo: buscar `"Asakusa Tokyo secreto"` en TikTok → extraer los 3-5 videos con más vistas.

**Si solo hay web_search (fallback):**
Usar las queries construidas en el Paso 1 para detectar patrones de ganchos indexados por Google.
Google indexa páginas de TikTok/Instagram pero NO métricas exactas de vistas.

**Qué buscar en los resultados:**
- Videos con más de 1M de vistas sobre el tema
- Títulos o descripciones de videos que aparezcan indexados
- Artículos que mencionen videos virales sobre ese tema
- Comentarios o reacciones masivas que indiquen viralidad

**Si no se encuentran resultados directos de TikTok/Instagram:**
- Buscar en YouTube Shorts sobre el mismo tema (mismo patrón de consumo)
- Buscar artículos de medios que cubran contenido viral sobre el tema
- Buscar con variaciones del tema en inglés si el tema es internacional

**Presentar al usuario:**
```
🔍 REFERENCIAS VIRALES ENCONTRADAS:

[Video/Contenido 1]
- Plataforma: TikTok / Instagram / YouTube Shorts
- Vistas aproximadas: X millones
- Gancho detectado: "[transcripción o descripción del gancho]"
- Por qué funcionó: [análisis breve]

[Video/Contenido 2]
...
```

---

### PASO 3 — Análisis de patrón del gancho

Para cada referencia viral encontrada, extraer:

1. **Estructura del gancho verbal** → ¿Cómo abre? ¿Pregunta, afirmación, dato, provocación?
2. **Elemento de tensión** → ¿Qué genera la necesidad de seguir viendo?
3. **Palabra ancla** → La palabra o frase que "engancha" (secreto, nadie sabe, prohibido, impactante, etc.)
4. **Ritmo** → ¿Es rápido y directo, o construye suspenso?
5. **Gatillo emocional dominante** → Curiosidad / Miedo / Sorpresa / Identificación / Descubrimiento

Mostrar análisis en tabla:

| Elemento | Video Viral Referencia | Tu Guion Original |
|----------|----------------------|-------------------|
| Apertura | [tipo de apertura] | [apertura actual] |
| Tensión | [cómo genera tensión] | [tensión actual] |
| Palabra ancla | [palabra clave] | [palabra actual] |
| Ritmo | [ritmo] | [ritmo actual] |
| Gatillo | [gatillo] | [gatillo actual] |

---

### PASO 4 — Reescribir el gancho con la referencia

Con base en el patrón detectado, proponer **3 versiones mejoradas** del gancho:

**Versión A — Basada 100% en el patrón viral encontrado**
Reescribir el gancho verbal, visual y textual adoptando la estructura exacta del video de referencia.

**Versión B — Híbrido: patrón viral + estructura original del guion**
Mantener la esencia de la Estructura 24 (o la que se eligió) pero con el ritmo y palabras ancla del video viral.

**Versión C — Evolución: patrón viral + giro propio**
Tomar el patrón pero añadir un elemento diferenciador que lo haga original respecto a la referencia.

Para cada versión entregar:
- 🎙️ **Gancho Verbal** (lo que se dice)
- 📲 **Gancho Textual** (lo que aparece en pantalla)
- 🎥 **Gancho Visual** (lo que se muestra/hace)

---

## NOTA TÉCNICA — LIMITACIONES Y OPCIONES

### Con MCPs sociales conectados ✅
Con **Xpoz**, **Instagram MCP**, **davibauer/tiktok-mcp** o **Supadata** activos en Claude Desktop,
la búsqueda accede a datos reales: vistas exactas, hashtags trending, ganchos textuales de videos,
engagement real. Esta es la experiencia completa.

### Sin MCPs sociales (solo web_search) ⚠️
Google indexa *algunas* páginas de TikTok/Instagram (páginas de discover, hashtags públicos)
pero NO tiene acceso a métricas reales de vistas individuales ni al feed For You / Reels.
En este modo se detectan **patrones de ganchos** del nicho, no datos exactos por video.

### Cómo conectar MCPs sociales (Claude Desktop)
Para usuarios de **Claude Desktop**, agregar en `claude_desktop_config.json`:

```bash
# Opción recomendada (TikTok + Instagram + más):
smithery mcp add xpoz

# Solo Instagram:
smithery mcp add instagram

# Solo TikTok:
smithery mcp add davibauer/tiktok-mcp

# YouTube + TikTok + Instagram (transcripción de videos):
smithery mcp add supadata-ai/mcp
```

Para **Claude.ai web**: Settings → Connectors → Add custom MCP URL → `https://mcp.xpoz.ai/mcp`

Si no se tiene acceso a MCPs sociales, se usa web_search como fallback y se notifica al usuario
el nivel de precisión de los resultados.

---

## INTEGRACIÓN CON EL GUION FINAL

Una vez que el usuario elija una de las 3 versiones del gancho:
1. Reemplazar el gancho en el guion completo
2. Verificar coherencia entre gancho nuevo y cuerpo del guion
3. Ajustar el texto en pantalla del resto del video si el nuevo gancho cambia el tono
4. Entregar el guion completo actualizado con la referencia viral incorporada
