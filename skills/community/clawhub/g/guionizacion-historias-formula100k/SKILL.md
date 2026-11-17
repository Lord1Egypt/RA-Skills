---
name: guionizacion-historias-formula100k
description: "Skill para crear guiones de SECUENCIAS DE HISTORIAS de Instagram (3-6 stories) usando la metodología FÓRMULA 100K. Activar cuando el usuario o un usuario pida: \"guioniza una historia\", \"arma una secuencia de stories para vender X\", \"estructura mis historias\", \"necesito un guion de stories\", \"haz una secuencia de historias para mi lanzamiento\", \"escribe stories para [oferta]\", \"diseña la secuencia de historias del jueves\", o cualquier variación que combine intención de vender/comunicar con el formato historias de IG. Genera UNA secuencia completa con: categoría detectada (Urgencia/One-Shot/ Lead Magnet/Libre/Encuestas), estructura de guion (1 de 24 disponibles), copy slide-by-slide, formato audiovisual por slide (🎥/📸 con uno de los 15 formatos), y briefing visual de diseño (paleta, capas, capturas, emojis). Guarda el output en guiones/historias/ como .md listo para ser tomado por la skill historias-a-imagenes-nanobanana."
argument-hint: "<idea, oferta o objetivo de la secuencia>"
metadata: {"version": "1.0.0", "openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Guarda en `guiones/historias/` respetando al pie de la letra `references/output-template.md`: otra skill lo parsea.
> - Entrega por Telegram el resumen de la secuencia y el `.md` completo como documento.

---

## 🧭 ANCLAJE DE RUBRO (leer PRIMERO — manda sobre cualquier ejemplo de esta skill)

Esta skill enseña un **método**. El método es agnóstico de industria: sirve igual para
formulación cosmética, nutrición, repostería, fisioterapia, finanzas o jabonería.
Los ejemplos escritos aquí abajo son ilustraciones **del método**, nunca del tema.

**Antes de escribir nada:**

1. Identifica el **RUBRO real** de la persona (léelo de su Segundo Cerebro, de su perfil o
   pregúntaselo en una línea si no está claro). Decláralo: *"Rubro: ___"*.
2. Todos los ejemplos, analogías, comparaciones, objeciones, métricas y vocabulario salen
   de **ESE** rubro.
3. Si el rubro **no** es marketing, redes sociales, creación de contenido, ventas online o
   negocios digitales → queda **PROHIBIDO** el vocabulario de ese mundo (reels, algoritmo,
   embudo, lead magnet, engagement, "publicar sin vender", "clientes de alto ticket",
   "escalar tu negocio", "posicionarte como referente"), salvo que la persona lo escriba primero.
4. Si el rubro es **técnico, científico o de oficio**: NO borres el tecnicismo para
   "simplificar". Úsalo y **tradúcelo en su primera mención**. El término preciso ES la
   autoridad de esa creadora; quitarlo borra justo lo que la diferencia.
5. Si no tienes datos suficientes del negocio, dilo y usa marcadores explícitos
   (`[TU OFERTA]`, `[TU RESULTADO]`). **Nunca asumas que el rubro es marketing.**

**El método viaja, el rubro no.** El mismo molde, vestido con rubros distintos:

| Rubro | El mismo molde |
|---|---|
| Cocina | "Así es mi cena favorita para no dormir con el azúcar alta." |
| Relaciones | "5 señales de que estás forzando una relación que ya no funciona." |
| Finanzas | "La principal causa de un divorcio no es una infidelidad." |
| Formulación cosmética | "El conservante decide si tu crema dura tres meses o te da una infección. No el aceite." |
| Jabonería | "Si tu jabón se pone blando a los dos días, no fue el aceite. Fue la sosa." |
| Fisioterapia | "Ese dolor de rodilla al bajar escaleras casi nunca nace en la rodilla." |
| Repostería | "Tu bizcocho se hunde en el centro por la temperatura, no por la harina." |
| Jardinería | "Tu planta no se está muriendo de sed. Se está ahogando." |

Mismo molde en todos; ninguno menciona reels ni embudos. Haz exactamente eso.

---

# Skill: Guionización de Historias FÓRMULA 100K

Convierte una idea, oferta u objetivo en una **secuencia completa de 3-6 historias de Instagram** lista para grabar y diseñar, siguiendo la metodología FÓRMULA 100K.

---

## ⚠️ ANTES DE EMPEZAR — LEE ESTOS REFERENCIALES

Cargar **siempre** estos archivos del directorio `references/` antes de generar:

1. `references/categorias.md` — las 5 categorías de historia
2. `references/estructuras.md` — las 24 estructuras de guion disponibles
3. `references/formatos.md` — los 15 formatos audiovisuales
4. `references/ctas.md` — guía de CTAs con consecuencia
5. `references/briefing-visual.md` — paleta de colores y reglas visuales
6. `references/output-template.md` — formato exacto del .md de salida

No es opcional: la skill depende de estos referenciales para la calidad del output.

---

## QUÉ HACE

Toma como input la idea/oferta/objetivo del usuario y devuelve un **archivo .md** con:

- **Metadata:** título, categoría, estructura, objetivo, palabra clave del CTA
- **Tabla slide-by-slide** con 6 columnas: `#`, `Frase principal`, `Capa visual`, `Formato (🎥/📸)`, `Qué grabar/buscar`, `Briefing de diseño`
- **Briefing visual general** de la secuencia (mood, paleta, recursos a preparar)
- **Notas de producción** (ej: "graba 3 clips en el mismo escenario para slides 1, 3, 5")

---

## INPUT

El usuario te dará alguna combinación de:
- Una **idea** ("quiero contar el caso de Brenda")
- Una **oferta a vender** ("vender el GPT del primer segundo")
- Un **objetivo** ("captar leads para el banco de historias")
- Una **categoría preferida** ("hagamos un Lead Magnet" / "esto es de urgencia")
- Una **estructura específica** ("usa la #14 Mini documental")
- **Día/hora** dentro de un calendario ("para el jueves a las 6pm")

Si el input es ambiguo, hacer **máximo 1 pregunta clarificadora** corta antes de generar. Ejemplos de buena pregunta:
- "¿Esto es para captar leads o cerrar venta?"
- "¿Es de la oferta del Banco de Historias o del GPT?"

No pidas más de un dato: con la oferta + objetivo basta.

---

## FLUJO DE 6 PASOS

### Paso 1 — Identificar la CATEGORÍA (de 5)

Lee `references/categorias.md`. Decide cuál encaja:

| Categoría | Cuándo usar |
|---|---|
| 🔥 URGENCIA | Cierre de carrito, últimas horas, sube precio, cupos limitados |
| 💥 ONE-SHOT | Pico de vistas, tema viral, sacudir cuenta |
| 🎁 LEAD MAGNET | Captar leads, regalo a cambio de DM, antes de lanzamiento |
| 💛 LIBRE/Lifestyle | Recuperar bajada de vistas, humanizar, día a día |
| 📊 ENCUESTAS | Activar interacción, calentar antes de venta, leer audiencia |

Si el usuario ya te dijo la categoría, respétala. Si no, dedúcela del objetivo.

### Paso 2 — Elegir la ESTRUCTURA (de 24)

Lee `references/estructuras.md`. Cada estructura tiene:
- Número (#1-24)
- Nombre (ej: "Soltamos la bomba")
- Patrón (ej: Tensión → Problema → Revelación → Beneficio → CTA)
- Cuándo usar
- 5-6 historias de ejemplo aplicado

Reglas para elegir:
- Si el usuario ya te dijo la estructura → úsala
- Si la oferta es **un caso de cliente** → estructura #14 Mini Documental
- Si quieres **anunciar algo nuevo** → #10 Soltamos la bomba
- Si tienes un **dato sorprendente** → #9 Algo me ha sorprendido
- Si es **lead magnet con regalo** → #3 Hice esta cosa nueva o #11 Si haces X mira esto
- Si es **urgencia con consecuencia** → #6 Esto es lo que sucede cuando + CTA con deadline real
- Si es **storytelling personal** → #1 Storytelling Chisme, #15 Lección Inesperada o #18 Diario Personal
- Si es **corregir un error común** → #7 Error Fatal o #4 Solo tuve que hacer un cambio

Si dudas entre 2, elige la más usada en el patrón observado en sus 11 ejemplos: #9, #10, #14, #6 son los caballos de batalla.

### Paso 3 — Determinar la CANTIDAD de slides

| Estructura | Slides recomendados |
|---|---|
| Lead Magnet con caso | 4-5 |
| Anuncio/Bomba | 5-6 |
| Storytelling chisme | 4-5 |
| Error/cambio educativo | 5 |
| Urgencia | 3-4 |
| Mini documental | 4-5 |

Mínimo 3, máximo 6. Si el usuario pide otro número, respétalo.

### Paso 4 — Asignar FORMATO por slide

Lee `references/formatos.md`. Reglas extraídas de los 11 ejemplos analizados:

- **Slide 1 (gancho):** SIEMPRE 🎥 video (movimiento atrapa). Formatos preferidos: F1 Selfie, F5 POV, F7 0.5x, F2 Tercera persona
- **Slides 2-3 (problema/prueba):** mayoritariamente 📸 foto (deja leer info densa). Formatos: F4 Captura DM, F13 Objetos, F15 Selfie+texto
- **Slide 4 (demo/solución):** 📸 foto con mockup del producto + bullets. Formato F15 ideal
- **Slide final (CTA):** 🎥 video con escenario bonito (cierre emocional) o 📸 con regalo emoji + escena

Regla universal: **NUNCA dos slides seguidos del mismo formato visual**.

### Paso 5 — Escribir COPY slide-by-slide

Para cada slide produce 6 datos:
1. **#** (número de slide)
2. **Frase principal** (la caja blanca/negra/amarilla del slide — máx 12 palabras)
3. **Capa visual** (qué captura/mockup/elemento va sobre el fondo — describe en 1 línea)
4. **Formato** (🎥 [F1-F15] o 📸 [F1-F15])
5. **Qué grabar/buscar** (instrucción concreta para el usuario: "graba caminando frente al Buda" o "captura de tu calendario lleno")
6. **Briefing de diseño** (cajas de qué color, dónde, qué emoji, qué flecha — usa `references/briefing-visual.md`)

Reglas de copy:
- Frases cortas (máx 12 palabras por slide).
- Resalta 1-2 palabras clave por slide (las que irán con highlight amarillo/verde).
- El último slide tiene **palabra clave fácil de tipear** (yo, GPT, INFO, BOMBA, TESIS, 100K, GUÍA…).
- El penúltimo slide muestra **el entregable** (mockup, dashboard, captura).
- Si la categoría es URGENCIA: añade consecuencia real ("solo hoy", "mañana lo borro", "se cierra a las 23:59"). Lee `references/ctas.md` para 80+ frases.

### Paso 6 — BRIEFING VISUAL general

Al final del archivo, agrega una sección con:
- **Mood general** (ej: "viaje + autoridad + cercanía")
- **Paleta** (qué cajas vas a usar más: blancas/negras/amarillas/verdes/rojas)
- **Capturas/mockups a preparar** (lista de los assets que el usuario necesita tener listos)
- **Sesiones de grabación recomendadas** (ej: "1 sesión de 4 clips en escenario A + 1 sesión de 2 clips en escenario B")

---

## OUTPUT

Guarda en: `guiones/historias/`

Nombre del archivo:
```
[YYYY-MM-DD]_[categoria]_[slug-corto-de-3-palabras].md
```

Ejemplos:
- `2026-05-06_lead-magnet_gpt-primer-segundo.md`
- `2026-05-06_one-shot_caso-brenda-39-sesiones.md`
- `2026-05-06_urgencia_ultimo-dia-banco-historias.md`

El **formato exacto del archivo** está en `references/output-template.md`. Síguelo al pie de la letra: la skill `historias-a-imagenes-nanobanana` lo va a parsear.

Después de guardar, muestra al usuario:
1. **Preview de la tabla slide-by-slide** en el chat (markdown)
2. **Ruta del archivo guardado**
3. **Próximo paso sugerido**: "¿Quieres que pase esto a imágenes con `historias-a-imagenes-nanobanana`?"

---

## ⚠️ ESPAÑOL NEUTRO OBLIGATORIO

El usuario escribe en **español neutro**, NO argentino. Todo el output (frases de slides, briefings, notas de producción, variantes A/B) debe usar:

| ❌ Argentino | ✓ Neutro |
|---|---|
| vos, sos | tú, eres |
| tenés, podés, querés, sabés | tienes, puedes, quieres, sabes |
| usás, mirás, escribís, pensás | usas, miras, escribes, piensas |
| copiá, pegá, mandá, contá | copia, pega, manda, cuenta |
| escribí, elegí, pedí, decí | escribe, elige, pide, di |
| pedile, contale, decile | pídele, cuéntale, dile |
| seguime, mandame, contame | sígueme, mándame, cuéntame |
| acá | aquí |
| laburo, plata | trabajo, dinero |
| che, dale | (omitir) |
| ¿viste? | ¿ves? |

Antes de guardar el .md, hacer un escaneo final buscando: "vos", "tenés", "podés", "querés", "acá", "decime", "dale", "che", "laburo". Si aparece, reemplazar.

**Razón:** la audiencia del usuario es panhispana (México, Colombia, España, USA Latino, Argentina). El voseo excluye a la mayoría.

---

## NO HACER

- No generar más de una secuencia por invocación (eso lo hace `calendarizador-historias-formula100k`).
- No diseñar las imágenes (eso lo hace `historias-a-imagenes-nanobanana`).
- No copiar literal el copy del PDF de estructuras: usa los patrones, pero el copy debe ser específico al objetivo del usuario.
- No usar emojis decorativos en el copy de los slides excepto los que indiquen función (⚠️ alerta, 🎁 regalo, ✅/❌ comparativa, 💰 dinero, 🤖 producto IA).
- No proponer formatos genéricos como "fondo plano con texto" en el slide 1 — el slide 1 SIEMPRE tiene movimiento o escenario real.
- No dejar el último slide sin palabra clave + acción concreta + (si aplica) consecuencia.
- **No usar voseo ni argentinismos** (ver tabla arriba).
