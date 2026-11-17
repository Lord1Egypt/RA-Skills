---
name: investigacion-ads-formula100k
description: "Investigación de ANUNCIOS PAGOS (paid ads) con la metodología FÓRMULA 100K + framework GOAT de Hormozi (Hook + Meat + CTA). Activar SIEMPRE que se pida 'investiga ads', 'busca ads de referencia', 'espía a la competencia en ads', 'biblioteca de anuncios de Meta', 'meta/facebook ads library', 'tiktok creative center', 'top ads', 'ads de [competidor]', 'qué anuncios corre X', 'dame 30 ideas de ads', '30-50 variantes de anuncios', 'guionízame este ad', 'variantes de un ad ganador', 'H x M x C', 'modulariza este ad'. NO confundir con investigacion-contenido-formula100k (contenido orgánico). Revisa la Biblioteca de Anuncios de Meta y el TikTok Creative Center en modo público con el navegador del agente (sin login) y Apify para lotes grandes, caza 30-50 ads, los desglosa con GOAT (Hook 80% / Meat 15% / CTA 5%), saca ángulos y ganchos ganadores, genera ideas propias y opcionalmente guioniza con H x M x C para variantes masivas."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Meta Ads Library: navegador del agente **sin iniciar sesión** (es pública). Nunca entres con el Facebook de la usuaria. Si la página no carga, pide captcha o corta la lista, pasa a Apify `apify~facebook-ads-library-scraper` (costo → ✅).
> - TikTok Creative Center: navegador del agente en modo público. Lo que solo se ve con cuenta de TikTok Business (algunos CTR/CVR) va como «no disponible»: no lo estimes.
> - No descargues los .mp4: guarda la URL del anuncio y un screenshot de su tarjeta en la biblioteca. Para leer el gancho visual, mira ese screenshot; si hace falta el video entero, que la usuaria lo abra.
> - Landings de los anuncios: tu herramienta web o el navegador del agente.
> - Todo va a `informes/ads-referencias/<fecha>_<proyecto>/` y los guiones a `guiones/ads/`. Por Telegram: los patrones en el chat y los `.md` como documentos.

---

# Skill: Investigación de Ads — Fórmula 100K

Esta skill convierte a Claude en un **director creativo de paid ads** que entra a la Biblioteca de Anuncios de Meta y al TikTok Creative Center, caza 30-50 referencias ganadoras, las desglosa con el framework GOAT, y entrega ángulos + ganchos + estructuras listos para producir o guionizar.

---

## DOCTRINA: POR QUÉ EL CREATIVO ES LO MÁS IMPORTANTE DE UN AD

Antes de cualquier investigación, este es el contexto doctrinal que rige la skill. Es la doctrina de FÓRMULA 100K y debe transmitirse al usuario cuando pregunte "¿por qué importa tanto el creativo?".

### Tesis central

> **"La creatividad es el 80% del éxito en publicidad pagada."**

El targeting, la audiencia, el presupuesto y la oferta son secundarios. Sin un creativo ganador, ningún targeting sofisticado genera ROI. Un creativo fuerte escala con cualquier presupuesto; un creativo débil quema dinero por más segmentación que tenga.

> **"Las vistas no venden, los comentarios sí."**

El algoritmo de Meta y TikTok premia el engagement temprano (primeros 3 segundos). Si el hook no detiene el scroll, el anuncio muere — no importa a quién se le muestre.

### Por qué un ad se guioniza DISTINTO a un contenido orgánico

| Dimensión | **AD pago** | **Contenido orgánico (reel/post)** |
|-----------|-------------|-----------------------------------|
| **Duración óptima** | 3-15 segundos | 15s-3min |
| **Hook** | Obligatorio en el segundo 0. El 80% de la efectividad. | Importante, pero puede construirse en 5-10s |
| **Estructura** | Hook → Meat (demo/testimonio) → CTA explícito | Entretención → Valor → Conexión |
| **Objetivo** | Acción inmediata (clic, comentario, compra, WhatsApp) | Engagement masivo, autoridad, alcance |
| **Tono** | Directo, transaccional, sin rodeos | Narrativo, storytelling, humor |
| **CTA** | Explícito y específico: "Comenta YO", "Abre el enlace" | Implícito o suave: "Cuéntame", "Guarda esto" |
| **Variantes** | Diseñado para producir 30-150 con H×M×C | Espontáneo, depende de tendencias |
| **Optimización** | Conversión bajo fricción | Distribución y viralidad |

**Frase clave para el usuario y sus alumnas:**
> "Un ad de 3 segundos requiere un hook de impacto inmediato. Un reel de 30 segundos puede construir lentamente. Confundir los dos formatos es la razón principal por la que la mayoría quema presupuesto en ads."

### Anatomía de un ad ganador (Framework GOAT — Hormozi)

**Proporción de importancia: Hook 80% → Meat 15% → CTA 5%**

**G = HOOK (Gancho — 80% de la efectividad)**
- Función: detener el scroll en los primeros 3 segundos
- 7 tipos verbales: Etiqueta · Pregunta · Condicional · Comando · Declaración provocativa · Lista · Narrativa
- 15 triggers: Curiosidad · Sorpresa · Identificación · Controversia · Autoridad · FOMO · Transformación · Simplicidad · Secreto · Validación Emocional · Conflicto · Revelación · Humor · Desafío · Utilidad Inmediata

**O = MEAT (Carne — demostración o validación)**
5 categorías válidas:
1. **Demostración** — el producto funcionando, antes/después
2. **Testimonial** — Master Script 6 Puntos: Lucha interna → Métrica antes → Escepticismo → Decisión → Victoria externa → Victoria interna
3. **Educativo** — tip, estrategia, conocimiento valioso
4. **Historia** — narrativa de transformación
5. **Faceless** — producto, texto, animación, voiceover

**A = CTA (Call to Action — claridad)**
3 Pilares obligatorios:
1. **Entregable** específico (no "acceso" sino "acceso a 50 plantillas + 15 ads ganadores + masterclass 90min")
2. **Resultado** tangible (no "información" sino "vender 3x más en 30 días")
3. **Palabra clave** de una sola palabra (preferentemente **YO** — "Comenta YO")

6 bloques de un CTA fuerte:
1. Condición calificadora — "Si tienes un producto pero no sabes vender..."
2. Recurso específico — "Creamos una guía de 5 pasos + 30 templates"
3. Prueba social — "Más de 10,000 emprendedores ya lo usan"
4. Resultado deseado — "Y ahora ganan $5K/mes"
5. Micro-acción — "Solo comenta YO abajo"
6. Promesa de velocidad — "Te enviaré todo en 5 minutos al WhatsApp"

---

## EL SISTEMA H × M × C (DE 1 GANADOR A 30-150 VARIANTES)

Una vez que se identifica un creativo ganador (en Meta Ads Library, en TikTok Creative Center, o uno propio), NO se producen ads completos desde cero. Se producen **módulos** y se combinan.

```
H (Hooks)  ×  M (Meats)  ×  C (CTAs)  =  Variantes
   10      ×      5       ×      3     =     150
    7      ×      4       ×      3     =      84
    5      ×      3       ×      2     =      30
```

**Paso 1 — Identificar el concepto ganador** (un ángulo que resuena, un ad que sigue corriendo, un patrón repetido en competidores)
**Paso 2 — Modularizar:** grabar 10-15 hooks distintos, 3-5 meats, 2-3 CTAs (cada uno por separado, no completos)
**Paso 3 — Combinar:** Hook A + Meat 1 + CTA 1 = Ad 1, Hook A + Meat 2 + CTA 1 = Ad 2, ... (combinación cartesiana)
**Paso 4 — Presupuestar regla 70-20-10:**
- **70%** a los CORE probados
- **20%** a EMERGENTES (variaciones menores de un ganador)
- **10%** a EXPERIMENTALES (hooks/meats nuevos)

> **Tiempo de producción con sistema:** 2-3 días para 30-50 variantes vs. 2-3 semanas sin sistema.

---

## STACK PERMANENTE DE INVESTIGACIÓN DE ADS

Cuatro motores trabajan juntos, no se excluyen. La regla es la misma que en `investigacion-contenido-formula100k`: **agent-browser entra SIEMPRE primero**, no es fallback.

| Motor | Zona exclusiva | Cuándo es protagonista |
|-------|----------------|------------------------|
| **Navegador del agente (sin login)** | Meta Ads Library pública · TikTok Creative Center · TikTok Top Ads · screenshots de cada anuncio · scrolleo lazy · landings | SIEMPRE en el paso 1. Toda investigación de ads arranca aquí. |
| **Apify** | Batch masivo de 100+ ads de Meta/TikTok con metadata estructurada (fecha de lanzamiento, días activo, plataformas, países) y URLs de video descargables | Cuando se necesitan 50-200 ads de varios competidores para clustering |
| **vidIQ MCP** | YouTube ads (in-stream, bumper) — outliers de creators que monetizan con ads | Solo si se piden ads de YouTube específicamente |
| **Tavily MCP** | Landings de los ads (página de aterrizaje), ofertas verbatim, precios, garantías | Cuando se quiere ver no solo el creativo sino la oferta completa |

**Regla de oro:** en este agente nunca se entra con la cuenta de la usuaria. La Biblioteca de Anuncios de Meta es pública (anuncios activos, fechas, plataformas, variantes); lo que se cierre al visitante anónimo sale de Apify o queda como «no disponible».

---

## PROCESO DE INVESTIGACIÓN (PASO A PASO)

### Paso 0 — Briefing inicial (preguntar si no está claro)

1. **Objetivo del ad** — ¿generar leads (formulario/comentario YO), venta directa, retargeting, awareness?
2. **Plataforma destino** — Meta (Instagram/Facebook), TikTok, ambas, YouTube
3. **Oferta o producto** — ¿qué se va a vender en el ad?
4. **Avatar** — ¿a quién se le habla?
5. **Referentes / competidores** — 3-10 cuentas o brands a investigar (handles de IG, páginas de FB, o nombres de marca para buscar en la library)
6. **Volumen deseado** — ¿30 ideas, 50, 100?
7. **¿Guionizar al final?** — ¿quieres que después de la investigación elija X ganadores y los guionice con H×M×C?

### Paso 1 — Meta Ads Library con el navegador del agente, sin login (motor principal)

**URL:** `https://www.facebook.com/ads/library/`

**Truco doctrinal F100K:**
> "Los anuncios que llevan MÁS TIEMPO corriendo son los que mejor funcionan. Si una marca lo ha dejado activo semanas o meses, es porque sigue vendiendo. Buscar los más antiguos, no los más nuevos."

**Prompt base para agent-browser:**

```
[agent-browser]

Abre el navegador del agente SIN iniciar sesión (la biblioteca es pública).

TAREA — Meta Ads Library para cada competidor [Marca1, Marca2, ...]:

1. Visita https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&q=[Marca]&search_type=keyword_unordered
2. Filtra: País = Todos · Tipo de anuncio = Todos los anuncios · Estado = Activos
3. Ordena por "Fecha de inicio" — los más antiguos primero (= los ganadores que siguen corriendo)
4. Para los primeros 30-50 ads de cada marca, extrae:
   - URL del ad en la library
   - Texto principal del ad (caption completo verbatim)
   - Headline + descripción
   - CTA del botón
   - Fecha de inicio
   - Días activo (calcular: hoy - fecha inicio)
   - Plataformas donde corre (FB / IG / Messenger / Audience Network)
   - Países donde corre
   - Tipo de creativo (video / imagen / carrusel)
   - URL del video o imagen (para descargar)
   - Número de variantes activas del mismo ad (si la library muestra "ver más anuncios")

5. Guarda la URL y un screenshot de la tarjeta de cada anuncio en informes/ads-referencias/[YYYY-MM-DD]_[marca]/ (no descargues los .mp4)

OUTPUT: markdown crudo, una sección por marca. No analices — yo lo proceso en el paso 3.
```

**Cuando la biblioteca no carga, pide captcha o corta resultados:**
- Caer a Apify (`apify~facebook-ads-library-scraper`) con la query de marca o keyword

**Por qué la fecha de inicio importa más que cualquier otra métrica:**
- Meta no muestra impresiones para anuncios fuera de UE/política, así que **el tiempo activo es el único proxy público de "esto está convirtiendo"**
- Un ad con 90+ días activo casi siempre está rentando
- Un ad con 3 días puede ser un test que se cancele mañana

### Paso 2 — TikTok Creative Center con el navegador del agente (público)

**URL principales:**
- Top Ads: `https://ads.tiktok.com/business/creativecenter/topads/pc/en`
- Hot videos: `https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en`
- Keyword Insights: `https://ads.tiktok.com/business/creativecenter/keyword-insights/pc/en`

**Prompt base para agent-browser:**

```
[agent-browser]

Abre el navegador del agente en modo público (sin iniciar sesión).

TAREA A — Top Ads por industria:
1. Visita https://ads.tiktok.com/business/creativecenter/topads/pc/en
2. Filtra por: Industria = [nicho del usuario], Región = LATAM/Spain/US, Period = Last 30 days
3. Ordena por CTR (Click-Through Rate) descendente — los Top 1-20% son los creativos ganadores
4. Extrae los top 20-30 ads con:
   - URL del ad en Creative Center
   - Thumbnail
   - Caption / texto sobre el video
   - Marca anunciante
   - CTR · CVR · Likes · Industry rank
   - Duración del video
   - URL del .mp4 (descargable desde Creative Center)

TAREA B — Búsqueda por keyword:
Keywords: [keyword1, keyword2, ...]
Para cada keyword:
1. Visita https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en?keyword=[keyword]
2. Top 10 ads con métricas

5. Guarda las URLs y screenshots en informes/ads-referencias/[YYYY-MM-DD]_tiktok_topads/ (no descargues los .mp4)

OUTPUT: markdown crudo, una sección por industria/keyword.
```

**Truco doctrinal:**
> "CTR alto en Top Ads = el anuncio es atractivo y genera clics → inspírate en su **gancho visual** del segundo 0, no en el texto."

### Paso 3 — Apify para batch masivo (opcional)

**Cuándo activar Apify:**
- ✅ Cuando se necesitan 50+ ads de un competidor de golpe
- ✅ Cuando agent-browser bloquea por anti-bot
- ✅ Cuando se quiere data estructurada para clustering automático

**Actors útiles:**
- `apify~facebook-ads-library-scraper` — Meta Ads Library, query por brand o keyword, retorna JSON con video URLs
- `apify~tiktok-ads-scraper` — TikTok ads con captions, métricas, URLs descargables
- `clockworks~tiktok-scraper` — videos orgánicos (no ads) si se quiere validar tendencia

**Flujo Apify:**
1. `fetch-actor-details` → ver input schema del actor
2. `call-actor` con input = `{ "searchQueries": ["marca"], "country": "ALL", "activeStatus": "active", "maxItems": 100 }`
3. `get-dataset-items` → JSON estructurado
4. Procesar: descargar `videoUrl` de cada item

### Paso 4 — Tavily MCP para landings (opcional)

Si después de cazar el ad se quiere ver la oferta completa (precio, garantía, bonos):
1. `tavily_extract` con la URL de destino del ad
2. Sacar: titular principal, sub-headline, bullet points, precio, garantía, bonos, CTA de página

Esto se usa cuando el usuario quiere comparar **oferta completa de competidor** vs. la suya, no solo el creativo.

---

## DESGLOSE GOAT DE CADA AD ENCONTRADO

Por **cada uno de los 30-50 ads** investigados, generar una ficha estandarizada:

```markdown
### Ad #N — [Marca] · [Plataforma]

- **URL library:** ...
- **Días activo:** 87 días (= ganador probado)
- **Tipo creativo:** Video 12s · Vertical 9:16

**HOOK (segundo 0-3):**
- Tipo verbal: [Etiqueta / Pregunta / Condicional / Comando / Declaración / Lista / Narrativa]
- Trigger principal: [Curiosidad / Sorpresa / Identificación / Controversia / FOMO / Transformación / Secreto / ...]
- Texto verbatim: "..."
- Gancho visual: [descripción del primer fotograma — objeto, gesto, antes/después, comparación]

**MEAT (segundo 3-9):**
- Categoría: [Demostración / Testimonial / Educativo / Historia / Faceless]
- Si es testimonial — qué puntos del Master Script 6 cubre: [Lucha / Métrica antes / Escepticismo / Decisión / Victoria externa / Victoria interna]
- Resumen del cuerpo: "..."

**CTA (segundo 9-12):**
- Palabra clave: [YO / LINK / WhatsApp / ...]
- Pilares cubiertos: [Entregable / Resultado / Palabra clave]
- Bloques presentes (de los 6): [Condición / Recurso / Prueba social / Resultado / Micro-acción / Velocidad]
- Texto verbatim: "..."

**ÁNGULO DE VENTA:**
- [Dolor que ataca] + [Promesa diferencial] + [Mecanismo único]

**POR QUÉ ESTE AD FUNCIONA (hipótesis):**
- [1-2 líneas: qué del hook detiene + qué del meat valida + qué del CTA empuja]
```

---

## CLUSTERING — DE 30-50 ADS A LOS PATRONES GANADORES

Después de fichar cada ad, agruparlos en **clusters** para encontrar los patrones repetidos. Esto es lo que van a usar el usuario o sus alumnas para construir SUS propios ads.

### 4 ejes de clustering

**1. Por ÁNGULO DE VENTA**
- ¿Cuántos ads atacan el mismo dolor con la misma promesa?
- Si 12 de 50 ads usan "no necesitas mostrar la cara para vender", ese es un ángulo validado por el mercado.

**2. Por TIPO DE HOOK (los 7 tipos verbales)**
- ¿Cuáles tipos dominan? Si 60% son preguntas, hay sesgo de mercado hacia preguntas.

**3. Por TIPO DE MEAT (las 5 categorías)**
- ¿Testimonial vs. demo vs. educativo? Define el formato que el nicho responde.

**4. Por CTA (palabra clave y bloques)**
- ¿"Comenta YO" vs. "Click en el enlace" vs. "Envía WhatsApp"? ¿Qué prevalece en ads que llevan +90 días activos?

### Output del clustering

```markdown
## Patrones ganadores detectados (de 50 ads investigados)

### Ángulos repetidos (Top 5)
1. "Vender sin mostrar la cara" — 14 ads · 9 con +60 días activos
2. "Pasar de Instagram a comunidad de pago" — 11 ads · ...
3. ...

### Hooks más usados
- Pregunta directa al avatar: 18 ads · ej. "¿Sigues pensando que necesitas 10K seguidores para vender?"
- Comando + revelación: 12 ads · ej. "Mira lo que pasa cuando..."
- ...

### Meats que dominan
- Testimonial con Master Script (al menos 3 puntos): 22 ads
- Demostración de pantalla / app: 14 ads
- ...

### CTAs ganadores
- "Comenta YO" + recurso de PDF: 19 ads
- "Click en el enlace" + masterclass: 11 ads
- ...
```

---

## GENERACIÓN DE 30-50 IDEAS DE ADS PROPIOS (FASE CREATIVA)

Una vez detectados los patrones, generar las **30-50 ideas propias** para el usuario. NO copiar el texto de competidores, sí adoptar la estructura validada.

### Plantilla por idea

```markdown
### Idea #N

- **Cluster del que viene:** Ángulo "vender sin mostrar la cara" + Hook pregunta + Meat demo de app
- **Hook propuesto (verbal):** "¿Y si te dijera que las mujeres que ganan $10K/mes en Instagram NO muestran la cara en 7 de cada 10 videos?"
- **Hook visual:** Pantalla dividida — izquierda: contador de seguidores subiendo · derecha: cara cubierta con post-it que dice "no necesito esto"
- **Meat:** Demo de [TU APP] generando 30 guiones en 2 minutos + screenshot de DM "ya cerré 3 clientes esta semana"
- **CTA:** "Comenta YO y te mando GRATIS los 5 ganchos que usé para llegar a $10K/mes sin mostrar mi cara"
- **Variantes H×M×C planeadas:** 8 hooks × 3 meats × 2 CTAs = 48 anuncios producibles
- **Plataforma:** Instagram Reels Ads + TikTok Spark Ads
- **Avatar atacado:** Mujer 25-40, vende servicios o cursos, le incomoda la cámara
```

### Cuántas generar

- Si el usuario pide "30 ideas" → 30 plantillas
- Si pide "50 ideas" → 50
- Distribuir por cluster: si hay 5 clusters dominantes y el usuario pide 30, son ~6 ideas por cluster (distintas suficientes para no ser duplicados)

---

## GUIONIZACIÓN DE LOS ADS SELECCIONADOS (FASE FINAL — OPCIONAL)

Cuando el usuario elige X ideas y dice "guionízame estas", entrar en modo guionización con el sistema H × M × C.

### Output por ad guionizado

```markdown
# AD GUIONIZADO — Idea #N

**Duración objetivo:** 12s · Formato 9:16

---

## BLOQUE H (3 hooks producibles — graba los 3, no solo uno)

### Hook A — Pregunta + Identificación
- Voz: "¿Sigues pensando que necesitas mostrar la cara para vender en Instagram?"
- Visual: pantalla negra → corte rápido a foto borrosa con la palabra "MITO" tachada
- Duración: 2.8s

### Hook B — Comando + Curiosidad
- Voz: "Detente. Si vendes online y no quieres mostrar la cara, esto te va a interesar."
- Visual: mano levantada en stop + zoom a celular
- Duración: 3.2s

### Hook C — Declaración provocativa + Secreto
- Voz: "Las que ganan $10K en IG no muestran la cara en 7 de cada 10 videos. Esto hacen en su lugar."
- Visual: feed scrolleando con 7 reels faceless + 3 con cara
- Duración: 3.5s

---

## BLOQUE M (3 meats producibles)

### Meat 1 — Demostración de app
- Voz: "Esto es [TU APP]. Le metes el tema, te da 30 guiones. Listos para grabar sin mostrar la cara."
- Visual: screen recording del producto · 6s
- Master Script puntos cubiertos: N/A (es demo)

### Meat 2 — Testimonial corto
- Voz: "[Nombre de tu clienta] cerró 3 clientes en una semana. NUNCA mostró la cara en los reels. Aquí está su pantalla."
- Visual: testimonial filmado + screenshot de DMs · 7s
- Master Script puntos: Métrica antes (cero clientes) → Decisión (probó esto) → Victoria externa (3 clientes) → Victoria interna ("dejé de tener miedo a la cámara")

### Meat 3 — Educativo
- Voz: "Hay 3 formatos faceless que convierten más que el talking-head: 1) screen recording, 2) carruseles narrados, 3) reels de objetos."
- Visual: 3 mini-clips de ejemplo cada formato · 6.5s

---

## BLOQUE C (2 CTAs producibles)

### CTA 1 — Comentario YO
"Si quieres que te mande GRATIS los 30 guiones faceless que usé para llegar a $10K/mes, **comenta YO** abajo y te llegan en 5 minutos a tu inbox."
- Palabra clave: YO
- Bloques presentes: Condición · Recurso · Velocidad
- Duración: 3.5s

### CTA 2 — Link
"Abre el enlace de la bio. Te llevo a una masterclass de 12 minutos donde te enseño los 5 ganchos faceless que ya validamos con 200 mujeres."
- Palabra clave: ENLACE
- Bloques presentes: Recurso · Prueba social · Resultado
- Duración: 4s

---

## COMBINACIONES SUGERIDAS (3 × 3 × 2 = 18 variantes)

| Variante | Hook | Meat | CTA |
|----------|------|------|-----|
| V1 | A | 1 | 1 |
| V2 | A | 1 | 2 |
| V3 | A | 2 | 1 |
| ...

## PRESUPUESTO 70-20-10 sugerido
- **70%** a V1 (la combinación más segura: Hook pregunta + Demo app + CTA YO)
- **20%** a V5-V8 (variaciones de hook)
- **10%** a V12-V18 (combinaciones experimentales)
```

---

## CONVENCIONES DE CARPETAS (output final)

Todo lo que esta skill produce va a:

```
informes/ads-referencias/
  └── YYYY-MM-DD_[proyecto]/
       ├── 01_referencias_meta/        (mp4/jpg descargados de Meta Ads Library)
       ├── 02_referencias_tiktok/      (mp4 descargados de TikTok Creative Center)
       ├── 03_fichas_GOAT.md           (desglose de los 30-50 ads)
       ├── 04_clusters_patrones.md     (patrones ganadores detectados)
       ├── 05_ideas_propias.md         (30-50 ideas para el usuario)
       └── 06_guiones/                 (un .md por ad guionizado con H×M×C)
```

---

## QUÉ ESTA SKILL **NO** HACE (delegación a otras skills)

- ❌ Investigar contenido **orgánico** viral → eso es [[investigacion-contenido-formula100k]]
- ❌ Escribir guiones de reel orgánico → [[guionizacion-formula100k]]
- ❌ Construir la oferta del producto → [[constructor-ofertas-f100k]]
- ❌ Escribir el VSL / página de venta a la que apunta el ad → [[vsl-expert-f100k]]
- ❌ Renderizar el ad final (corte, gráficos, B-roll) → [[editor-video-formula100k]] o [[graficos-de-video-formula100k]]
- ❌ Generar el creativo con IA (image/video AI) → [[banana]] (imágenes) + Higgsfield MCP (video)

Esta skill se queda en: **investigar → desglosar → idear → (opcionalmente) guionizar**.

---

## CITAS DOCTRINALES PARA USAR EN OUTPUT AL USUARIO

Cuando el usuario o una alumna pregunte el "por qué" durante la investigación, usar estas frases verbatim:

- "La creatividad es el 80% del éxito en publicidad pagada."
- "Las vistas no venden, los comentarios sí."
- "Tienes 3 segundos para detener el scroll. Si fallas en eso, ningún targeting te salva."
- "Los anuncios más antiguos en la library son los ganadores. Si lleva 90 días activo, está convirtiendo."
- "No produzcas ads completos. Produce módulos: hooks por separado, meats por separado, CTAs por separado. Después combina."
- "Regla 70-20-10: 70% del presupuesto en lo probado, 20% en variaciones, 10% en experimentos."
- "Un ad de 3 segundos se guioniza DISTINTO a un reel de 30. Confundir los dos formatos es la razón #1 por la que la gente quema presupuesto."
