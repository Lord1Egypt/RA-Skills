---
name: guionizacion-humanizada
description: "Skill para humanizar guiones, textos y scripts para que no suenen escritos por IA. Usar SIEMPRE que alguien pida: humanizar un texto, hacer que suene más natural, quitarle el tono de IA, reescribir con mi voz, adaptar a mi estilo, hacer sonar más humano, revisar que no parezca IA, aplicar mi tono, o escribir como yo escribo. También activar cuando digan \"esto suena muy de IA\", \"necesito que suene mío\", \"ponle mi estilo\", \"humaniza este guion\" o cualquier variación que implique personalizar el tono y voz de un texto para que refleje la forma auténtica de comunicarse del usuario."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - PASO 1 abre Instagram con el navegador: aquí NO. Construye el Voice Guide con lo que haya en `cerebro/` y pide por Telegram de 6 a 8 captions o transcripciones de sus mejores posts (o un audio hablando como le habla a su audiencia). Si hay `APIFY_TOKEN`, puedes bajar captions públicos de su perfil con un actor de Instagram.
> - El Voice Guide se guarda en `cerebro/voice-guide.md`, fuera de la skill, para que las actualizaciones no lo borren.
> - El ejemplo de Voice Guide de la versión de escritorio no viene en este paquete.

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

# Skill: Guionización Humanizada

Esta skill adapta cualquier texto al tono, voz y estilo genuino de **la persona dueña de la cuenta** — tú, o la clienta para la que estás escribiendo —, basándose en el análisis real de SUS contenidos más exitosos. El objetivo es que los guiones y escritos suenen como esa persona, no como una IA tratando de sonar como ella.

> ⚠️ **La voz es la del usuario, nunca la de otra creadora.** Si esta skill trae un archivo
> el ejemplo de la versión de escritorio (no incluido aquí), es SOLO una muestra de cómo se ve un Voice Guide bien
> hecho (construido sobre una cuenta pública, a modo de ejemplo). **Nunca escribas en esa voz.**
> Sirve para entender el formato; el contenido sale del análisis del perfil del usuario.
> Si el archivo no está, no lo busques: pasa directo al PASO 1.

---

## PASO 0 — Verificar si el Voice Guide del usuario existe

Antes de hacer cualquier cosa, revisa si existe `cerebro/voice-guide.md` (el del usuario)
Y tiene contenido de análisis real.

```
Ruta: cerebro/voice-guide.md
```

**Si el archivo NO existe o está vacío → ir al PASO 1 (Análisis de Instagram).**
**Si ya tiene el análisis completo → confirmar de quién es (el encabezado lleva el @) y, si es del usuario, saltar al PASO 2 (Humanización).**

---

## PASO 1 — Análisis de Instagram (solo la primera vez)

Este paso se corre UNA SOLA VEZ por persona para generar su Voice Guide. Avísale al usuario que vas a analizar su perfil de Instagram antes de humanizar el texto.

**Primero pregúntale su @ de Instagram** (o el de la clienta para la que escribes) si no lo dijo
ya en el mensaje. No lo asumas ni lo saques de ninguna otra skill: sin handle no hay Voice Guide.

### 1.1 — Navegar al perfil y recolectar posts

1. Abre el navegador y navega a: `https://www.instagram.com/<HANDLE-DEL-USUARIO>/`
2. Espera a que cargue el perfil completamente
3. Toma un screenshot para confirmar que cargó bien
4. Desplázate hacia abajo para cargar al menos 15-20 posts
5. Para cada post visible, anota mentalmente: cantidad de likes/comentarios visibles, si es reel o imagen, el texto del caption si es visible

### 1.2 — Entrar a los posts más exitosos

Abre los **6-8 posts que tengan más engagement** (los que más likes y comentarios muestran). Para cada uno:

1. Haz click en el post para abrirlo
2. Lee el **caption completo** (expandiéndolo si está cortado)
3. Lee los primeros 5-8 comentarios de la autora si respondió
4. Anota:
   - Palabras y frases exactas que usa
   - Cómo empieza el caption (¿con pregunta?, ¿con afirmación fuerte?, ¿con historia?)
   - Cómo termina (¿CTA?, ¿reflexión?, ¿pregunta al lector?)
   - Uso de emojis: cuáles, dónde, con qué frecuencia
   - Longitud de oraciones: ¿cortas y directas o largas y explicativas?
   - Signos de puntuación especiales: puntos suspensivos, mayúsculas, guiones
   - Expresiones o palabras propias que repite
5. Vuelve al perfil con el botón atrás

### 1.3 — Generar el Voice Guide

Con todo lo que analizaste, crea el archivo `cerebro/voice-guide.md` con esta estructura:

```markdown
# Voice Guide — [NOMBRE DEL USUARIO]
*Generado el: [fecha]*
*Basado en análisis de: [cantidad] posts de @[handle-del-usuario]*

## Tono general
[Describe el tono en 2-3 oraciones: ¿cálido? ¿directo? ¿mezcla de qué?]

## Cómo inicia sus textos
[Patrones de apertura que usa: ejemplos reales copiados de sus posts]

## Cómo cierra sus textos
[Patrones de cierre: cómo remata, qué tipo de CTA usa]

## Vocabulario y frases características
[Lista de palabras, frases y expresiones que usa con frecuencia — copiarlas exactas]

## Expresiones y quirks de escritura
[Cosas particulares: expresiones propias, giros de lenguaje, muletillas características]

## Uso de emojis
[Cuáles usa, dónde los pone, con qué frecuencia. Ejemplos reales.]

## Estructura de oraciones
[Longitud típica. ¿Usa listas? ¿Párrafos cortos? ¿Fragmentos sin verbo?]

## Puntuación y formato
[Uso de puntos suspensivos, signos de exclamación, MAYÚSCULAS, — guiones —, etc.]

## Lo que NUNCA dice (señales de IA a evitar)
[Palabras y frases que no aparecen en sus posts y sonarían artificiales]

## Ejemplos de captions reales (copiar textual)
[2-3 captions completos copiados literalmente para referencia]
```

Guarda este archivo en `cerebro/voice-guide.md` dentro de tu workspace.

---

## PASO 2 — Humanización del texto

Lee el `cerebro/voice-guide.md` completo antes de empezar.

### 2.1 — Diagnóstico rápido del texto recibido

Antes de reescribir, identifica qué señales de IA tiene el texto original:

- **Estructura demasiado perfecta**: intro → desarrollo → conclusión en tres párrafos simétricos
- **Frases de relleno de IA**: "es importante destacar que", "en definitiva", "en conclusión", "sin lugar a dudas", "es fundamental", "por supuesto", "sin duda alguna", "indudablemente"
- **Vocabulario formal que nadie habla**: "cabe mencionar", "en este sentido", "a modo de conclusión"
- **Ausencia de imperfección**: no hay dudas, titubeos, cambios de ritmo, oraciones cortadas
- **Tono neutro y sin personalidad**: no hay preferencias, no hay voz propia
- **Ausencia de lo específico**: generaliza en lugar de dar detalles concretos

### 2.2 — Aplicar el Voice Guide

Reescribe el texto aplicando lo que encontraste en el Voice Guide:

1. **Ritmo y longitud**: Ajusta las oraciones al patrón real del usuario (si esa persona escribe corto y directo, haz lo mismo)
2. **Vocabulario propio**: Reemplaza palabras genéricas con las que ella usa realmente
3. **Aperturas y cierres**: Usa los patrones reales de cómo ella empieza y termina
4. **Emojis**: Solo los que usa ella, donde los pone ella, con la frecuencia que los usa
5. **Expresiones propias**: Incorpora sus expresiones características donde encajen de forma natural
6. **Estructura**: Si ella usa párrafos cortos y saltos de línea, haz eso

### 2.3 — Aplicar principios universales de humanización

Independientemente del Voice Guide, todo texto humanizado debe:

- **Romper la simetría perfecta**: No tres párrafos del mismo largo. Mezcla uno corto, uno más largo, uno muy corto.
- **Incluir al menos una imperfección calculada**: Una oración sin terminar. Un paréntesis (porque sí). Una cosa que se contradice levemente y luego se aclara.
- **Hablar a UNA persona, no a una audiencia**: "tú" en lugar de "todos ustedes" o "las personas que..."
- **Nombrar lo concreto**: En lugar de "cuando tienes resultados", decir "cuando tus reels llegan a 50k"
- **Dejar entrar la emoción real**: Una frase que suene como que la pensó de verdad, no como que la calculó
- **Variar el ritmo deliberadamente**: Oraciones largas que fluyen... seguidas de una sola palabra. Eso.

### 2.4 — Revisión final de humanización

Antes de entregar, pasa el texto por este checklist mental:

- [ ] ¿Podría el usuario haber escrito esto sin que nadie lo note?
- [ ] ¿Hay alguna oración que suene a manual corporativo? → Reescribir
- [ ] ¿El ritmo sube y baja o va parejo? → Si va parejo, romperlo
- [ ] ¿Hay alguna frase de relleno que se podría cortar sin perder nada? → Cortar
- [ ] ¿El inicio engancha o empieza con una introducción burocrática? → Cambiar
- [ ] ¿El cierre se siente genuino o como fórmula? → Ajustar

---

## FORMATOS DE ENTREGA

### Para humanización de texto existente:
Entrega el texto reescrito directamente, sin explicar cada cambio. Si quieres, agrega una línea al final tipo: *"Humanicé X, Y y Z para que suene más tuyo."* — pero mantén el texto como protagonista.

### Para crear contenido nuevo en la voz del usuario:
Escribe el contenido directamente en su voz sin advertencias de que "intentaste capturar su estilo". Si lo hiciste bien, se nota solo.

### Si el Voice Guide no existe y no se pudo analizar Instagram:
Avísale al usuario que necesitas acceso a Instagram para hacer el análisis inicial, o pídele que comparta ejemplos de textos propios para construir el Voice Guide manualmente.

---

## RECORDATORIO

El Voice Guide es un documento vivo. Si el usuario muestra un texto propio y dice "quiero que escribas así", actualiza el Voice Guide con lo nuevo que aprendiste.
