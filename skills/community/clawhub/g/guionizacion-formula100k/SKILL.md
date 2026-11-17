---
name: guionizacion-formula100k
description: "Skill especializada en guionización estratégica con los frameworks de FORMULA 100K. Usar SIEMPRE que alguien pida: crear un guion, estructurar un video, hacer un reel, escribir un script, elegir una estructura de contenido, hacer un gancho viral, guionizar una idea, crear contenido para Instagram/TikTok/YouTube, o cualquier solicitud relacionada con escribir o planear un video. También usar cuando alguien comparta una idea y quiera saber qué estructura usar. Contiene 35 estructuras de guion, sistema de hooks (gancho verbal, visual y textual), criterios de ideas virales, ficha de viralidad, y módulo de verificación de viralidad que busca referencias reales en TikTok/Instagram con millones de vistas para basar el gancho en contenido probado. Incluye una capa de OFICIO a nivel de frase (resbaladero, especificidad, verbo filmable, cadencia, kill-list de muletillas) y un pase de reescritura obligatorio, para que el guion no salga plano ni genérico."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Módulo de verificación de viralidad: busca referencias con tu búsqueda web; si hay `APIFY_TOKEN`, confirma vistas con Apify. Nunca navegador logueado. Si no encontraste una referencia verificada, dilo; no inventes vistas.
> - La sección «Setup para Claude Desktop» (Xpoz, MCP sociales) no aplica aquí: sáltala.
> - Pase de voz: usa `cerebro/voice-guide.md` si existe. Si no existe, no abras Instagram: ofrece correr `guionizacion-humanizada`, que lo arma con textos que la usuaria te mande.
> - Guarda cada guion en `guiones/` con fecha en el nombre.

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

# Skill: Guionización Fórmula 100K

Esta skill contiene todos los frameworks de guionización de FORMULA 100K para crear videos virales con estructura estratégica.

---

## PROCESO OBLIGATORIO ANTES DE ESCRIBIR CUALQUIER GUION

### Paso 1 — Hacer estas 4 preguntas (si no las respondió ya)
1. ¿Qué mensaje principal quieres comunicar con este video?
2. ¿Qué tono prefieres? (jocoso, serio, directo, emotivo)
3. ¿Qué valor final quieres aportar a tu audiencia?
4. ¿Hay algún dato único o historia personal que quieras incluir?

### Paso 1.5 — Fijar el rubro (OBLIGATORIO, antes de evaluar nada)

Declara: **"Rubro: ___"**. Sácalo del Segundo Cerebro, del perfil o pregúntalo en una línea.
Los criterios del Paso 2 se leen **dentro de ese rubro**, no en abstracto. Ver el
🧭 ANCLAJE DE RUBRO al inicio de esta skill.

### Paso 2 — Evaluar si la idea es ganadora (9 criterios)

> Estos criterios miden **claridad**, no falta de profundidad. Se evalúan contra
> **el público de ESE rubro**, no contra el público general. Una formuladora cosmética
> le habla a gente que ya sabe qué es un emulsionante: para ellos, eso *es* lenguaje claro.

1. ¿La entiende alguien que recién empieza **en ese rubro**?
2. ¿Genera controversia o invita al comentario?
3. ¿Está inspirada en alguna referencia viral?
4. ¿Alguien pagaría al menos $3 por este contenido?
5. ¿50 de 100 personas **de esa audiencia** se identificarían o conocen a alguien así?
6. ¿Los tecnicismos que usa están **traducidos en su primera mención**?
   ⚠️ El criterio NO es "evita tecnicismos". En rubros técnicos, científicos o de oficio
   (formulación, salud, ingeniería, repostería, derecho) el término preciso **ES la autoridad**:
   quitarlo borra la diferencia de quien habla y la deja sonando genérica. La regla es
   **usarlo y traducirlo**: "el conservante —lo que evita que te crezcan hongos en la crema—".
7. ¿Muestra una transformación clara de punto A a punto B?
8. ¿Es alcanzable para el espectador promedio **de ese rubro**?
9. ¿Tiene un giro propio si parte de una idea conocida?

### Paso 3 — Identificar el Pilar de Valor (OBLIGATORIO)

Aportar valor no es solo "dar un tip". Antes de proponer estructuras, identificar qué pilar de valor sostiene el video — aunque el valor sea implícito o tácito. **Elegir UNO solo como pilar central.** Si no se identifica ninguno con claridad, la idea no está lista para guionizar: regresar al Paso 1 y reformular.

Los 7 Pilares de Valor:

| # | Pilar | Qué es | Impacto en la audiencia |
|---|-------|--------|------------------------|
| 1 | 💡 **Revelación (Insight)** | Información basada en experiencia propia o investigación que pocos conocen | El usuario siente que accede a un 'secreto' que beneficia su vida |
| 2 | 🛠️ **Utilidad Práctica** | Tutoriales o simplificación de conceptos complejos | Genera GUARDADOS. Lo conserva porque le ahorra tiempo o esfuerzo futuro |
| 3 | ❤️ **Validación Emocional** | Reflexiones que validan cómo se siente el usuario | Genera COMPARTIDOS. Lo envía: 'Esto es exactamente lo que me pasa' |
| 4 | 🎮 **Desafío (Gamificación)** | Tests, retos o diagnósticos que invitan a participar | Toca el ego positivo. Se siente inteligente o desafiado al participar |
| 5 | 📰 **Actualidad (Curiosidad)** | Noticias o revelaciones de interés público vinculadas al nicho | Te posiciona como fuente relevante y 'al día' |
| 6 | 🔍 **Curaduría** | Filtrar el ruido: 'Analicé 50 herramientas y estas 3 sirven' | El valor es el TIEMPO que le ahorras al otro |
| 7 | ⚡ **Disrupción (Anti-consejo)** | Cuestionar lo que todos dicen con lógica y datos | Genera DEBATE y pensamiento crítico, demuestra autoridad superior |

**Cómo aplicarlo:**
1. Declarar explícitamente: "El pilar de valor de este video es **[N - Nombre]**".
2. Justificar en 1 frase cuál es el valor concreto que recibe el espectador (aunque sea tácito).
3. Si la idea no calza con ningún pilar → advertir al usuario que el video corre riesgo de ser "contenido vacío" y proponer cómo reformularlo para activar uno.
4. El pilar elegido condiciona la estructura del Paso 4 (ej. Validación Emocional → estructura 13 El Espejo; Curaduría → estructura 9 Regla de 3 o 17 How to Template; Disrupción → estructura 10 Gancho Controversial o 19 Desafío Contracorriente).

### Paso 4 — Proponer 2 o 3 estructuras posibles
Revisar TODAS las estructuras disponibles (ver references/estructuras.md) y seleccionar las más adecuadas según:
- **Pilar de valor identificado en Paso 3** (filtro principal)
- Objetivo del video (ventas, comentarios, autoridad, educación, viralidad)
- Nivel de consciencia del público
- Tipo de transformación (emocional, práctica, económica, identidad)
- Potencial de controversia o conversación

Explicar brevemente POR QUÉ cada estructura es adecuada para ese pilar y caso específico.

### Paso 5 — Dejar que el usuario elija la estructura
Solo después de que confirme, desarrollar el guion completo.

### Paso 6 — Verificación de Viralidad con Referencia Real (OBLIGATORIO)
Antes de entregar el guion final, ejecutar el módulo de verificación de viralidad.
Ver instrucciones completas en: `references/verificacion-viralidad.md`

Resumen del proceso:
1. Extraer palabra clave del tema del guion
2. Buscar en web videos virales reales sobre ese tema (TikTok, Instagram, YouTube Shorts)
3. Analizar el patrón del gancho de los videos encontrados
4. Proponer 3 versiones del gancho basadas en esa referencia real
5. Dejar que el usuario elija la versión y reescribir el guion con ella

Este paso garantiza que el gancho no sea genérico sino basado en lo que ya probó funcionar con millones de vistas.

### Paso 6.5 — El pase de reescritura (OBLIGATORIO)

Nadie escribe bien de una. Lo que acabas de terminar es el **borrador**, no el entregable.
Antes del Chequeo Neuro, córrele los cuatro movimientos contra la sección **EL OFICIO**
(más abajo en esta skill). Cada movimiento deja un número: si no puedes mostrar el número,
no lo corriste.

**Movimiento 1 — Corta el 20% de las PALABRAS.**
De las palabras, no de las líneas. Cuenta antes, cuenta después. Lo primero que cae: los
adjetivos, los adverbios en *-mente*, "realmente", "básicamente", "un poco", "muy", y toda
oración que solo exista para explicar la anterior.

**Movimiento 2 — Un verbo filmable por línea.**
Recorre línea por línea. Cada verbo que no se pueda grabar (Regla 4) se cambia por uno que sí.
Si una línea no admite ningún verbo filmable, es que no tenía contenido: bórrala.

**Movimiento 3 — Parte la línea más larga.**
Busca la frase más larga del guion y pártela en dos. La segunda mitad se queda corta a propósito:
esa es la que pega (Regla 5).

**Movimiento 4 — El resbaladero, línea por línea.**
Tapa cada línea y mira la anterior. ¿Te obliga a destaparla? Si no, se fusiona con la siguiente
o se va (Regla 1).

**Movimiento 5 — Caza de frases recogidas.**
Busca cada frase de tu guion dentro de esta skill y de `references/estructuras.md`. Si aparece
textual o casi textual, la recogiste de una tabla en vez de escribirla: reescríbela (Regla 7).
Y si escribiste varios guiones en esta sesión, ponlos **lado a lado**: ninguno puede abrir el
primer ni la sobredimensión con la fórmula del anterior.

**Salida obligatoria del paso** (va antes del guion final):

```
🔁 PASE DE REESCRITURA
Palabras: 312 → 244 (−22%)
Verbos cambiados: 7
Líneas eliminadas por resbaladero: 3
Kill-list cazada: "la verdad es que" ×1 · "esto lo cambió todo" ×1
Frases recogidas de una tabla: 1 → reescrita ("no le sirve a todo el mundo")
Contraste con los otros guiones de la sesión: primer y sobredimensión distintos ✅
```

> Si el conteo bajó **menos del 15%**, no cortaste: volviste a leer. Corre el Movimiento 1 otra vez.

### Paso 7 — Chequeo Neuro (OBLIGATORIO, automático)
Antes de entregar el guion final, pásalo por el **Chequeo Neuro** (no le pide nada extra a la usuaria, es texto, no gasta créditos). Carga `references/rubrica-neuro.md` y corre sus 6 reglas sobre el guion recién escrito:

1. Hook 0-3s manda · 2. Pico temprano · 3. Anti-Default-Mode · 4. Visual temprano · 5. Voz = ancla · 6. Sin valle en s1-2.

Devuelve el bloque corto de salida (ver `rubrica-neuro.md`): veredicto por regla + **el arranque ya reescrito** para clavar los primeros 2s (resultado-primero / visual antes de s2). Si alguna regla sale BAJO, aplica su instrucción de reescritura sobre el guion antes de entregarlo.

> Esto es una **predicción heurística sobre texto**, no la medición real. La medición real (correr `tribe v2` sobre el video grabado) vive en `remix-viral-formula100k`; ambas usan el mismo vocabulario.

### Paso 7.5 — Pase de voz (OPCIONAL — se ofrece, no se asume)

El guion que sale del Paso 7 está bien **escrito**. Todavía no está escrito **como ella**.

Esa es la diferencia entre un guion que no da vergüenza y uno que nadie más habría podido
escribir. Sin este paso, dos creadoras del mismo rubro reciben guiones correctos que **suenan
igual entre sí** — el piso sube para todas y la diferencia entre ellas desaparece.

**Va al final a propósito.** El Paso 6.5 corta y aprieta; el Paso 7 ajusta el arranque. Si la voz
entrara antes, esos dos pases se la llevarían por delante.

**Cómo se ofrece** (una línea, sin sermón):

> "¿Te lo paso por tu voz? Necesito tu @ de Instagram. La primera vez me toma unos minutos
> porque leo tus posts; después queda guardado y es instantáneo."

- **Si dice que sí** → corre la skill `guionizacion-humanizada` sobre el guion final. Si esa
  persona todavía no tiene Voice Guide, la skill lo construye sola (analiza su perfil, una vez).
- **Si dice que no, o no hay handle** → el guion del Paso 7 es el entregable. **No inventes una
  voz.** Un registro fabricado es peor que uno neutro.

**⚠️ Los tres límites del pase de voz** — la voz cambia el CÓMO, nunca el QUÉ:

| No puede | Por qué |
|---|---|
| **Devolver muletillas de la kill-list** | "Así habla ella" no es excusa. Solo pasan si están **en SU Voice Guide**, documentadas con un caption real suyo — nunca por defecto. |
| **Alargar el guion** | Si crece más del 10% sobre el conteo del Paso 6.5, deshizo el pase de reescritura. Vuelve a cortar. |
| **Tocar estructura, gancho o CTA** | Eso ya se decidió y se midió. La voz reescribe el registro de las líneas, no el esqueleto. |

Si el pase de voz corrió, dilo en la entrega: **"Voz: @handle (Voice Guide del [fecha])"**. Si no
corrió, dilo también: **"Voz: sin calibrar — guion en registro neutro."** Que se note cuál de las
dos cosas recibió.

---

## ORDEN DE ENTREGA AL ESCRIBIR EL GUION

1. Indicar el **pilar de valor** identificado (1 de los 7) + justificación de 1 frase
2. Indicar la estructura elegida + listar sus componentes
3. Ejecutar verificación de viralidad (referencias reales) → ver `references/verificacion-viralidad.md`
4. Desarrollar el sistema completo de ganchos (verbal, visual, textual) basado en referencia viral
5. Si el formato es **hablando a cámara de autoridad**, escribir los dos beats post-gancho **en orden**: 🧷 **el primer** (1 línea, seg ~3, empieza con "pero", resta a la promesa) y después la **sobredimensión de valor** (2–4 líneas, seg ~5–12, prueba + promesa amplificada + filtro). Si es storytelling/POV/skit, marcar N/A los dos.
6. Correr el **pase de reescritura** (Paso 6.5) y entregar su bloque `🔁 PASE DE REESCRITURA`
7. Entregar el guion completo paso a paso — la versión **ya reescrita**, nunca el borrador
8. Ejecutar el **Chequeo Neuro** (`references/rubrica-neuro.md`) y entregar el arranque ajustado
9. Ofrecer el **pase de voz** (Paso 7.5) y declarar en la entrega si corrió o no
   (`Voz: @handle` / `Voz: sin calibrar`)

---

## SISTEMA DE GANCHOS (HOOKS OPTIMIZER)

Todo gancho exitoso combina 3 estímulos:

**Gancho Verbal** → Qué se DICE en los primeros segundos
**Gancho Visual** → Qué se MUESTRA (resultado final, acción inesperada, expresión, objeto intrigante)
**Gancho Textual** → Qué se LEE en pantalla (texto de alerta, resultado, error común, curiosidad, promesa)

Verificar coherencia total entre los tres. Si no comunican el mismo mensaje, reescribirlos.

### Gatillos emocionales del gancho
Elegir uno principal:
- **Curiosidad** — el cerebro siente que le falta información importante
- **Miedo a cometer un error** — activa alerta y autodiagnóstico
- **Sorpresa** — algo inesperado rompe el patrón del feed
- **Identificación** — el espectador siente "eso me pasa a mí"
- **Promesa de resultado** — promete transformación clara
- **Descubrimiento** — conocimiento exclusivo o poco conocido

### Criterios cognitivos del gancho
- Estímulo núcleo claro (captura atención inmediata)
- Contexto inmediato (se entiende rápido qué está pasando)
- Baja carga cognitiva (fácil de procesar)

---

## LA ZONA POST-GANCHO — dos beats, en este orden

Ambos son **Pasos del protocolo LA APUESTA**, el marco que une el valor con el gancho:
`VALOR ESPERADO = (MAGNITUD × CREDIBILIDAD) ÷ COSTO`. La guía completa está en el Grimorio 100K
(«LA APUESTA»). Todo lo que necesitas para aplicarlo está aquí abajo, self-contained.

```
seg 0-3    GANCHO                    → la promesa   (magnitud)
seg 3-5    🧷 PRIMER                 → el límite    (credibilidad)   ← Paso 3.5
seg 5-12   SOBREDIMENSIÓN DE VALOR   → prueba + promesa amplificada + filtro  ← Paso 7
```

**El orden no es negociable:** el primer RESTA y la sobredimensión SUMA. El primer te gana el
derecho a amplificar. Amplificar sin haber puesto un límite es exactamente lo que hace sonar
a vendehumos la sobredimensión.

---

## BEAT OBLIGATORIO 1 — 🧷 EL PRIMER (seg ~3)

**UNA línea, justo después del gancho, que le quita algo a tu propia promesa.** Empieza con "pero".

Es el antídoto del *cheque sin fondos* (promesa grande sin respaldo) **sin necesitar una prueba
nueva**: convierte la limitación de la técnica en la señal cara. Paga un poco de magnitud para
comprar credibilidad — y como se multiplican, el trato sale a favor.

### Las 4 formas — elige QUÉ le quitas

> ⚠️ **Esta tabla son CATEGORÍAS, no plantillas.** La columna derecha muestra la FORMA de la
> resta, no la frase que vas a escribir. Ver **EL OFICIO · Regla 7**.

| Le quitas | Tres maneras distintas de sonar |
|---|---|
| **Universalidad** | "Pero no le sirve a todo el mundo." · "Pero si ya pesas con báscula, esto no es para ti." · "Pero solo explica el que sube y después se cae." |
| **Consistencia** | "Pero no funciona siempre." · "Pero me falla una de cada tres veces." · "Pero hay semanas que no pasa nada y toca esperar." |
| **Facilidad** | "Pero me costó seis meses entenderlo." · "Pero los primeros nueve me salieron mal." · "Pero vas a odiar las dos primeras semanas." |
| **Autoría** | "Pero no lo inventé yo." · "Pero esto me lo enseñó una señora de ochenta años." · "Pero lleva cincuenta años escrito. Yo solo lo probé." |

**La versión buena de cada forma trae el dato que la hace verdad.** "Me falla una de cada tres
veces" resta más que "no funciona siempre", porque la segunda se la puede decir cualquiera y la
primera solo quien lo contó.

### Las 2 formas de arruinarlo
- **Falsa modestia** — el límite va sobre **la técnica**, NUNCA sobre quien habla. *"Pero no soy experta"* no cuenta y además destruye autoridad.
- **Límite inventado** — tiene que ser verdad. Un límite falso es otro cheque sin fondos.

**NUNCA va antes del gancho.** Si abres con la limitación, abriste con una excusa y no hay promesa
que defender.

*(Evidencia: Ein-Gar, Shiv & Tormala 2012 · Eisend 2006 — efecto real pero pequeño. Ver el
framework, § EL PRIMER.)*

---

## BEAT OBLIGATORIO 2 — SOBREDIMENSIÓN DE VALOR (seg ~5 a ~12)

> **Dependencia dura:** este beat solo se escribe bien si antes se resolvieron el premio (Paso 1),
> la señal cara (Paso 3) y el primer (Paso 3.5). Sin eso se degrada solo a índice
> ("te voy a explicar las 3 razones").

Aplica a **formatos hablando a cámara de autoridad**: tutorial, desmitificación, análisis, curaduría,
anti-consejo. En estos, el gancho NO va directo al contenido: entre el gancho y el cuerpo va un beat
propio de 2–4 líneas cuya función es convertir la curiosidad en un **contrato de retención** —
la persona decide conscientemente quedarse.

**Posición:** inmediatamente después del primer, segundos ~5 a ~12.
**Extensión:** 2–4 líneas. Nunca más del **12% de la duración total** del video.

### Los 3 componentes (deben estar los 3)

> ⚠️ **CATEGORÍAS, no plantillas.** Cada componente admite formas muy distintas. Elige una
> distinta cada vez. Ver **EL OFICIO · Regla 7**.

**1 · Prueba** — te gana el derecho a prometer. Cuatro maneras de darla:

| Forma | Suena así |
|---|---|
| Por volumen | "Esto salió de las últimas 43 rodillas que evalué." |
| Por costo | "Este error me costó dos pedidos." |
| Por tiempo | "Llevo seis años cambiándoselo a mis pacientes." |
| Por fracaso | "Probé tres formas. Dos me salieron mal." |

**2 · Promesa amplificada** — nombra el **ESTADO del espectador**, no el tema. Tres maneras:

| Forma | Suena así |
|---|---|
| Diagnóstico | "Vas a saber cuál de los tres estabas rompiendo." |
| Pérdida evitada | "No vas a volver a botar un lote entero." |
| Reencuadre | "Vas a dejar de mirarte la rodilla." |

> 🚫 **Molde quemado — prohibido:** *"Cuando termines este video vas a entender por qué llevas
> [tiempo] sin [resultado]"* y sus variantes (*"en un minuto vas a saber por qué…"*). Fue el
> ejemplo de esta skill durante meses y salió calcado en guiones seguidos. Si tu promesa empieza
> con "vas a entender/saber por qué llevas…", reescríbela con otra de las tres formas.

**3 · Filtro / autoselección** — hace que la persona correcta levante la mano. Tres maneras:

| Forma | Suena así |
|---|---|
| Por síntoma | "Si se te hunde en el centro, quédate." |
| Por exclusión | "Si ya mides con báscula, este video no es para ti." |
| Por conducta | "Si mides con la cuchara del frasco, esto te va a doler." |

El filtro **por exclusión** es el más fuerte de los tres y el menos usado: expulsar a alguien en voz
alta es lo que le da valor a quedarse.

### El criterio de evaluación (esto es lo que se puntúa)

**La promesa nombra el ESTADO del espectador, no el CONTENIDO del video.**

- ❌ "Te voy a explicar cómo funciona el conservante" → eso es índice, NO es sobredimensión
- ✅ "No vas a volver a botar un lote sin saber qué lo dañó"

La promesa buena **diagnostica un dolor específico**, no anuncia un tema. Y ahí está la dependencia:
este beat solo funciona si sabes exactamente qué le duele a esa persona. Sin claridad sobre el
espectador, sale como hype vacío. Si no puedes nombrar el dolor concreto, no escribas el beat:
resuelve primero a quién le hablas.

### Antipatrones
- **Promesa sin prueba** → suena a vendehumos y quema autoridad
- **Más de 4 líneas** → se come el video y la gente se va antes del contenido
- **Prometer algo que el video no entrega** → mata la retención del **siguiente** video, no de este
- **Filtro demasiado amplio** ("esto le sirve a todo el mundo") → anula la autoselección

### Dónde NO aplica
Storytelling, POV, skit, confesión, diario, historia personal. En narrativa este beat rompe la
ilusión y se siente a infomercial. En esos formatos, marcarlo como **N/A** y seguir.

---

## ÍNDICE DE ESTRUCTURAS

Para el detalle completo de cada estructura, leer: `references/estructuras.md`

### ESTRUCTURAS DE VENTA (1-6)
| # | Nombre | Objetivo principal |
|---|--------|-------------------|
| 1 | Construcción de Autoridad para Venta | Credibilidad + prueba social → conversión |
| 2 | Pitch de Venta Perfecto | Problema → solución → urgencia → acción |
| 3 | Reacción a Video o Comentario | Autoridad desde contenido ajeno |
| 4 | Historias que Venden | Empatía + transformación → confianza → ventas |
| 6 | El Problema Invisible | Despertar conciencia + solución oculta |

### ESTRUCTURAS DE VALOR (7-13)
| # | Nombre | Objetivo principal |
|---|--------|-------------------|
| 7 | La Escalera de Autoridad | Evolución progresiva paso a paso |
| 8 | Respondiendo a Comentario Polémico | Debate + autoridad desde la polémica |
| 9 | La Regla de 3 | Valor educativo simple y memorable |
| 10 | Gancho Controversial | Debate desde afirmación contraintuitiva |
| 11 | La Paradoja Personal | Idea ilógica que cobra sentido |
| 12 | La Historia Inesperada | Cotidiano + giro sorprendente + reflexión |
| 13 | El Espejo | Verbalizar lo que la audiencia siente |

### ESTRUCTURAS DE VIRALIDAD (14-20)
| # | Nombre | Objetivo principal |
|---|--------|-------------------|
| 14 | 100% Viral | Error común + solución + pasos → viralidad |
| 15 | Vacío de Información | Sensación de perder algo importante |
| 16 | El Roba Audiencia | Figura pública como gancho + insight propio |
| 17 | How to Template | Tutorial filtrante para audiencia específica |
| 18 | El Momento WTF | Hecho impactante + tensión + plot twist |
| 19 | El Desafío Contracorriente | Romper creencia popular con lógica |
| 20 | El Efecto Boomerang | Resultado primero, fracasos después |

### ESTRUCTURAS DE STORYTELLING (21-25)
| # | Nombre | Objetivo principal |
|---|--------|-------------------|
| 21 | Viaje del Héroe | Historia personal de transformación |
| 22 | Caída Doble | Doble fallo antes de la solución real |
| 23 | El Efecto Mariposa | Hecho pequeño → consecuencias gigantescas |
| 24 | El Secreto Perdido | Historia oculta o poco conocida |
| 25 | La Teoría del Loco | Idea absurda que termina siendo lógica |

### ESTRUCTURAS MODERNAS / AVANZADAS (26-34)
| # | Nombre | Objetivo principal |
|---|--------|-------------------|
| 26 | El Consejo de las Cosas | Conceptos personificados que hablan |
| 27 | El Protagonista y su Equipo | Historia + aliados + venta orgánica |
| 28 | El Esqueleto del Tiempo | Acción pequeña que escala en el tiempo |
| 29 | Esqueletos en Versus | Dos caminos paralelos con reencuadre final |
| 30 | La Máquina de Comentarios | Problema → solución → palabra clave |
| 31 | El Golpe de Valor Gratis | Elevar valor percibido → revelar que es gratis |
| 32 | Versus de Nivel Estratégico | Básico vs estratégico en situaciones reales |
| 33 | Análisis de Caso Estratégico | Desmenuzar caso real → lección implícita |
| 34 | La Escalera de Etapas (Autodiagnóstico) | Proceso en 5 etapas numeradas + "¿en qué etapa estás?" → comentarios masivos |
| 35 | Manifiesto de Serie | Episodio 0 que vende la promesa de una serie → audiencia de retorno |

---

## EL OFICIO — cómo suena la línea

> Los pasos de arriba deciden **qué se dice y en qué orden**. Esta sección decide **cómo suena**.
> Un guion puede pasar todos los pasos, tener el pilar correcto y la estructura correcta, y aun
> así estar escrito en voz de folleto. Aquí es donde se pierde o se gana.
>
> Los ejemplos de abajo ilustran **el método**. Vístelos con el rubro declarado en el Paso 1.5.
>
> **Referencia de escritura:** los bloques **🎙️ LA MISMA ESTRUCTURA, EN BOCA** de
> `references/estructuras.md` son los únicos ejemplares escritos a este estándar. Los
> "Ejemplo aplicado" de ese archivo son esqueletos etiquetados: enseñan el ORDEN, no el
> registro. **No imites su forma de escribir.**

### Regla 1 — El resbaladero: cada línea existe para que escuches la siguiente

**Test:** tapa la línea que sigue. Si la anterior no te obliga a destaparla, sobra.

❌ "Hoy te hablo de la fermentación. La fermentación es un proceso natural. Existen tres tipos."
   → cada línea se cierra sola; puedes irte después de cualquiera.

✅ "Tu masa no subió y le echaste la culpa a la levadura. La levadura estaba viva. Lo que la mató
   fue algo que hiciste doce horas antes."
   → ninguna línea se puede abandonar sin quedar debiendo.

*(Sugarman: la única función de la primera frase es que leas la segunda.)*

### Regla 2 — Especificidad: lo redondo suena a relleno

**Test:** ¿hay una cifra impar, un nombre propio, una hora del reloj o un objeto con marca? Si tu
número termina en 0 o en 00, o es el número real o lo estás inventando.

❌ "Muchas de mis pacientes llegan con dolor de rodilla."
✅ "De las últimas 40 pacientes que llegaron por la rodilla, 31 tenían el problema en la cadera."

❌ "Me tomó mucho tiempo entenderlo."
✅ "Me tomó catorce meses y tres lotes botados."

*(Kennedy: nadie se inventa un 297. Por eso $4.297 se cree y "unos 4 mil" no.)*

### Regla 3 — Le hablas a UNA persona

**Test:** si la frase funciona dicha frente a mil personas, está mal escrita. Reescríbela como si
se la dijeras a la única que ya sabes que te está viendo.

❌ "Muchas personas cometen este error sin darse cuenta."
✅ "Lo estás haciendo ahora mismo y ni cuenta te has dado."

❌ "Es importante que la audiencia entienda que…"
✅ "Necesito que entiendas una cosa:"

*(Halbert: escribes una carta, no un discurso.)*

### Regla 4 — Verbo filmable

**Test:** ¿puedes **grabar** el verbo? *Entender, mejorar, transformar, conectar, potenciar,
optimizar* no se filman. *Abrir, raspar, botar, medir, colgar, devolver* sí.

❌ "Vas a mejorar tu relación con la comida."
✅ "Vas a dejar de abrir la nevera a las once de la noche."

❌ "Esto transforma la manera en que ves tu jardín."
✅ "Vas a meter el dedo en la tierra antes de agarrar la regadera."

**Corolario:** sustantivo concreto por encima de abstracción. El adjetivo es lo primero que se corta.

### Regla 5 — Cadencia: larga, larga, corta

**La corta es la que pega. Si todas son cortas, no pega ninguna.**

**Test:** cuenta las palabras de tres frases seguidas. Si las tres caen en el mismo rango, reescribe.

❌ "El conservante importa. El pH importa. La temperatura importa."
   → tres golpes idénticos; el oído los aplana y no queda ninguno.

✅ "Puedes escoger el mejor aceite del mercado, medir el pH con tira y guardar el frasco en la
   nevera. Puedes hacer todo eso, juiciosa, durante seis meses seguidos. Y te crece hongo igual."

### Regla 6 — "Sexto grado" es sintaxis, no vocabulario

Esta regla existía antes y se estaba leyendo al revés. **Nivel sexto grado mide la ESTRUCTURA de
la frase** —una idea por oración, sujeto-verbo-objeto, sin subordinadas encadenadas— **no el léxico.**

El término técnico se queda, y se traduce en su primera mención (Paso 2, criterio 6). Quitarlo no
simplifica: borra la autoridad de quien habla y la deja sonando como cualquiera.

❌ *simplificado de más* → "Un ingrediente que protege la crema."
❌ *sin traducir* → "El conservante de amplio espectro define la vida útil del producto."
✅ "El conservante —lo que evita que te crezca hongo en el frasco— decide si tu crema dura tres
   meses o te manda al médico."

### Regla 7 — Toda tabla de esta skill son CATEGORÍAS, no plantillas

Esta skill está llena de tablas con una frase de ejemplo por fila: EL PRIMER, la sobredimensión,
la tabla del 🧭 ANCLAJE DE RUBRO, los gatillos del gancho. **La frase de la derecha es la FORMA,
no el texto.** Copiarla es la manera más rápida de que dos guiones distintos suenen iguales — y de
que todas las alumnas de un rubro publiquen la misma línea.

**Test:** busca cada frase de tu guion dentro de esta skill y de `references/estructuras.md`.
Si aparece textual o casi textual, no la escribiste: la recogiste. Reescríbela.

❌ Guion de fisioterapia que abre con *"Ese dolor de rodilla al bajar escaleras casi nunca nace en
   la rodilla"* → es la línea literal de la tabla del ANCLAJE.
✅ Misma idea, escrita: *"Llevas tres meses poniéndote hielo en la rodilla. El problema te queda
   veinte centímetros más arriba."*

**Regla de variación:** si escribes varios guiones en una misma sesión (un calendario, una serie),
ninguno puede abrir el primer ni la sobredimensión con la fórmula del anterior. Revísalos juntos,
no de a uno: el esqueleto compartido solo se ve al ponerlos lado a lado.

---

### 🚫 KILL-LIST — expresiones que no sobreviven al Paso 6.5

Estas son las muletillas que hacen sonar un guion a máquina o a vendedor de curso. Cázalas y mátalas.

**Arranques vacíos** · "La verdad es que…" · "Déjame decirte algo" · "Te voy a ser sincera" ·
"Presta atención porque esto…" · "Aquí va la parte importante" · "Spoiler:"

**Falsa profundidad** · "Esto lo cambió todo" · "Y ahí lo entendí todo" · "Nunca volví a ser la
misma" · "Y eso lo cambia absolutamente todo"

**Muletillas de IA** · "No se trata de X, se trata de Y" · "No es magia, es método" · "No es suerte,
es estrategia" · el triple paralelo ("no es A, no es B, es C") · "en un mundo donde…" ·
"la clave está en…" · "y aquí está lo mejor"

**Relleno de transición** · "Dicho esto" · "Ahora bien" · "Pero eso no es todo" · "Y no solo eso"

**Promesas sin cuerpo** · "Esto te va a volar la cabeza" · "Nadie te lo va a decir" ·
"Guarda esto que lo vas a necesitar"

> El molde `no es X, es Y` está prohibido **por sobreuso, no por ser malo**. Si de verdad necesitas
> el contraste, hazlo entre dos **hechos**, no entre dos abstracciones:
> ❌ "No es falta de disciplina, es falta de sistema."
> ✅ "No te faltó disciplina. Te faltó que alguien te dijera que la masa se amasa fría."

---

### Reglas de siempre (se quedan)

- NUNCA repetir estructuras por inercia — cada elección debe ser resultado de análisis
- Cada guion debe tener: gancho fuerte + cuerpo con valor + CTA claro
- **Test del bostezo** — ninguna línea sobrevive con un estado abstracto sin escena
  ("siempre he sido insegura", "me exijo mucho"). Cambia el estado por la conducta que lo
  delata. Si borras el adjetivo y la frase se queda vacía, no había contenido.
- **El caption nunca transcribe el video.** Elige reparto: el video da los extremos y el
  caption el mecanismo (el que vende), o el video es solo la puerta y el caption lleva el arco
---

## CUÁNDO USAR CADA TIPO DE ESTRUCTURA

| Objetivo | Estructuras recomendadas |
|----------|------------------------|
| Primeras ventas / conversión | 1, 2, 4, 5, 30, 31 |
| Autoridad y posicionamiento | 1, 3, 7, 8, 33 |
| Viralidad / alcance masivo | 14, 15, 16, 18, 19, 20 |
| Engagement / comentarios | 8, 10, 11, 19, 30, 34 |
| Autodiagnóstico / etapas | 34, 28, 20 |
| Storytelling emocional | 4, 12, 13, 21, 22, 23 |
| Educación / valor | 9, 15, 17, 26, 27, 28 |
| Comparación / debate | 10, 19, 29, 32 |
| Misterio / intriga | 18, 24, 25, 33 |

---

## REFERENCIA DETALLADA

Para leer la descripción completa de cada estructura con ejemplos y análisis, ver:
→ `references/estructuras.md`

---

## 🖥️ SETUP PARA CLAUDE DESKTOP — BÚSQUEDA REAL EN TIKTOK E INSTAGRAM

> Esta sección es para usuarios de **Claude Desktop** que quieran que la verificación
> de viralidad acceda a datos reales de TikTok e Instagram, no solo a resultados de Google.

### Por qué hace falta un MCP adicional
Google indexa algunas páginas públicas de TikTok/Instagram pero no puede ver métricas
reales de vistas ni el contenido del For You / Reels feed. Para eso se necesita un
MCP social conectado a Claude Desktop.

---

### ⭐ Opción A — Xpoz (recomendada: cubre TikTok + Instagram + Twitter + Reddit)

**1. Obtener API token gratuito:**
Ir a → https://www.xpoz.ai → crear cuenta → copiar tu API token

**2. Agregar en Claude Desktop:**
Ir a `Settings → Connectors → Add custom MCP` y pegar:
```
URL: https://mcp.xpoz.ai/mcp
Header: Authorization: Bearer TU_TOKEN_AQUI
```

O si usas el CLI de Smithery:
```bash
claude mcp add --transport http --scope user xpoz-mcp https://mcp.xpoz.ai/mcp --header "Authorization: Bearer TU_TOKEN"
```

---

### Opción B — TikTok MCP (solo TikTok)

```bash
smithery mcp add davibauer/tiktok-mcp
```

---

### Opción C — Instagram MCP (solo Instagram)

```bash
smithery mcp add instagram
```

---

### Opción D — Supadata (TikTok + Instagram + YouTube, transcripción de videos)

```bash
smithery mcp add supadata-ai/mcp
```

---

### ✅ Cómo saber si está conectado
Una vez conectado, en el próximo guion que solicites, la skill usará el MCP
automáticamente en el Paso 5 para buscar videos virales reales con métricas exactas
en lugar del fallback de Google.

> Para instrucciones completas de uso de cada MCP en la verificación, ver:
> → `references/verificacion-viralidad.md`

---

## PASO FINAL — Calibración contra la data de TU cuenta (opcional)

Este guion ya es el entregable final. Si además tienes data medida de tu propia cuenta
(una auditoría de tus reels: qué ganchos retienen, qué CTAs convierten, qué formatos
se hunden), pásale un segundo filtro con `auditor-ganchos-cuenta-formula100k` y ajusta:

- El gancho del segundo 1 contra los ganchos que ya te funcionaron.
- El CTA contra el que más comentarios/DMs te trajo.
- La kill-list: lo que en TU cuenta ya demostró no funcionar.

Si no tienes esa data todavía, no inventes números: el guion se entrega tal cual.
