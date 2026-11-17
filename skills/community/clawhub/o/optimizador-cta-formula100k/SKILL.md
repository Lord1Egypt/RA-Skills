---
name: optimizador-cta-formula100k
description: "Skill especializada en analizar, diagnosticar y mejorar llamados a la acción (CTAs) de guiones de video usando los patrones de FORMULA 100K de Andrea Vega. Usar SIEMPRE que alguien pida: mejorar un CTA, revisar un llamado a la acción, optimizar el final de un guion, hacer que un CTA genere más comentarios, crear variaciones de un llamado a la acción, o cuando comparta un guion y quiera que el CTA funcione mejor. También activar cuando digan: \"¿cómo remato este guion?\", \"el CTA no está funcionando\", \"quiero que genere más engagement\", \"mejora este final\"."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Skill de solo texto: corre tal cual.
> - La oferta, el lead magnet y la palabra clave de cada CTA salen de `cerebro/`. Si no están, pregúntalas por Telegram antes de proponer.

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

# Skill: Optimizador de CTAs — FORMULA 100K

Esta skill analiza cualquier llamado a la acción de un guion y produce versiones mejoradas usando los patrones probados de Andrea Vega que han generado los mayores volúmenes de comentarios en sus videos.

---

## PROCESO OBLIGATORIO

### Paso 1 — Recibir el CTA o guion

Si el usuario no pegó el CTA todavía, pedírselo directamente:
> "Pégame el llamado a la acción (o el guion completo si lo tienes) y te digo exactamente qué cambiar y cómo mejorarlo."

Si ya lo compartió, pasar directamente al diagnóstico.

---

### Paso 1.5 — Detectar el formato del CTA

Antes de diagnosticar, identificar qué formato usa el CTA:

**FORMATO A — Condicional** (apertura con filtro)
Empieza con "Si quieres...", "Si eres de las personas que...", "Si tienes [situación]..."
→ El filtro califica al espectador antes de mostrar el recurso.

**FORMATO B — Visual-first** (apertura con recurso en pantalla)
Empieza con "Este es...", "Esta es...", "En esta hoja...", "Pero bueno, he creado..."
→ El creador señala un mockup del recurso que aparece en pantalla durante la edición.
→ El recurso se VE antes de que la persona comente. Reduce la incertidumbre a cero.
→ Es válido y muy efectivo. NO corregirlo como si fuera un error — potenciarlo.

Ambos formatos son correctos. El diagnóstico y las mejoras deben respetar el formato elegido.

---

### Paso 2 — Diagnóstico (análisis de los 5 bloques)

Evaluar el CTA contra la fórmula base. Marcar cada bloque como presente, débil o ausente:

| Bloque | Pregunta de diagnóstico |
|--------|------------------------|
| CONDICIÓN CALIFICADORA | ¿Filtra al espectador correcto? ("Si quieres", "si tienes [situación] y sientes que [dolor]", "Este es" con contexto de a quién va dirigido) |
| RECURSO ESPECÍFICO | ¿Nombra algo concreto (plantilla, guía, checklist, plan, lista) o es vago? |
| PRUEBA SOCIAL DEL RECURSO | ¿Menciona que el creador lo usa o lo usa con sus estudiantes/clientes? ("que uso", "que le doy a mis estudiantes") — opcional pero muy potente |
| RESULTADO DESEADO | ¿Conecta el recurso con un resultado o dolor que la audiencia ya siente? |
| MICRO-ACCIÓN | ¿Pide una sola palabra como acción ("yo", "entrevista", "listo")? |
| PROMESA DE VELOCIDAD | ¿Incluye "en menos de 1 minuto", "te llega automáticamente", o promesa de inmediatez? |

Mostrar el diagnóstico de forma clara antes de las versiones mejoradas. Ejemplo:
```
DIAGNÓSTICO:
✅ Condición calificadora — presente
⚠️  Recurso específico — débil (dice "información" en vez de algo concreto)
✅ Resultado deseado — presente
❌ Micro-acción — ausente (pide que "visiten el link")
❌ Promesa de velocidad — ausente
```

---

### Paso 3 — Generar 3 versiones mejoradas

Producir exactamente 3 versiones con etiquetas claras:

**VERSIÓN 1 — Fiel al estilo original**
Mantener la voz y el tema del CTA original pero corregir los bloques faltantes. No cambiar más de lo necesario. Es la versión más segura para usar ya.

**VERSIÓN 2 — Más potente**
Aplicar uno de los ángulos psicológicos avanzados según lo que encaje mejor con el tema del video:
- Prueba social: "Esto es exactamente lo que le mandé a las [X] personas que me preguntaron cómo..."
- Identidad: "Si eres de las personas que quiere [resultado] sin [dolor]..."
- Arrepentimiento del creador: "Ojalá alguien me hubiera dado esto cuando empecé..."
- Consecuencia de no actuar: "Si sigues sin [recurso] vas a seguir perdiendo [costo]..."
- Pregunta + solución: "¿Cuánto tiempo llevas intentando [X] sin lograrlo?..."
- Escasez de personas: "Solo se lo voy a mandar a las primeras [N] personas que..."

**VERSIÓN 3 — Ángulo nuevo**
Usar un ángulo psicológico distinto al de la Versión 2. Puede ser más emocional, más urgente, o atacar el dolor desde otro lado. Esta versión puede alejarse más del original.

---

### Paso 4 — Explicar brevemente cada versión

Después de cada versión, una línea de por qué funciona:
> **Por qué funciona:** [razón específica en 1-2 oraciones]

No explicar lo obvio. Solo lo no-obvio: el mecanismo psicológico que activa, el elemento que reduce fricción, o por qué ese ángulo encaja con ese tema.

---

## FÓRMULAS BASE

### Formato A — Condicional
```
[Si quieres / Si eres de las personas que / Si tienes [situación] y sientes que [dolor]]
+ [RECURSO ESPECÍFICO concreto]
+ [que uso para / que le doy a mis estudiantes para]
+ [RESULTADO DESEADO]
+ comenta "[UNA PALABRA]"
+ y te lo paso / mando / regalo / llega en menos de 1 minuto
```

### Formato B — Visual-first (recurso en pantalla)
```
[Este es / Esta es] + [RECURSO ESPECÍFICO con nombre]
+ [que uso / que le doy a mis estudiantes / que he creado]
+ [condición: "así que si eres de las personas que..." / "si tienes [situación]"]
+ [RESULTADO DESEADO o dolor que resuelve]
+ comenta "[UNA PALABRA]"
+ y te llega / te lo mando gratis en menos de 1 minuto
```

**El CTA más completo combina ambos:** muestra el recurso visualmente Y añade la condición calificadora + resultado. Ejemplo de referencia:
> "Esta es mi guía personal de pronunciación y la que usan mis estudiantes así que si eres de las personas que quiere hablar inglés con confianza sin que el acento te paralice, comenta 'yo' y te llega gratis, en menos de 1 minuto."

---

## BIBLIOTECA DE ÁNGULOS PSICOLÓGICOS

Usar según qué encaje mejor con el tema del video:

### Visual-first con condición (el más completo — Formato B potenciado)
> "Esta es [recurso específico] y la que usan mis [estudiantes/clientes] así que si eres de las personas que quiere [resultado] sin [dolor/obstáculo], comenta 'yo' y te llega gratis, en menos de 1 minuto"

### Visual-first con situación urgente
> "Este es el [recurso] que debes tener si [situación específica: tienes una entrevista pronto / estás empezando / llevas meses sin resultado] y sientes que [dolor]. Comenta '[palabra]' y te llega en menos de 1 minuto"

### Visual-first con proceso detallado + regalo
> "Este es el [recurso] que utilizo con mis [estudiantes/clientes] para conseguir [resultado] y está detallado paso por paso — y a ti te lo voy a regalar, solo comenta 'yo'"

### Identidad (Formato A — el más poderoso sin visual)
> "Si eres de las personas que quiere [resultado deseado] sin [dolor/obstáculo] comenta 'yo' y te mando [recurso específico] — gratis, en menos de 1 minuto"

### Consecuencia de no actuar
> "Si sigues [haciendo X sin recurso] vas a seguir perdiendo [oportunidades/tiempo/dinero]. Comenta 'yo' y te mando [recurso] para que eso no te pase — en menos de 1 minuto"

### Dolor doble apilado (dos condiciones)
> "Si tienes [situación urgente] y sientes que [dolor específico], comenta '[palabra]' y te llega [recurso] en menos de 1 minuto"

### Prueba social
> "Esto es exactamente lo que le mandé a las [X] personas que me preguntaron cómo [lograr resultado] — si tú también lo quieres comenta 'yo' y te lo paso en menos de 1 minuto"

### Número específico
> "Tengo [número] [plantillas/pasos/ejercicios] que uso para lograr [resultado] — si las quieres todas comenta 'yo' y te las paso en menos de 1 minuto"

### Contraste antes/después
> "Antes perdía [tiempo/dinero] haciendo [cosa difícil]. Ahora lo hago con [recurso]. Si lo quieres comenta 'yo' y te lo mando ya"

### Arrepentimiento del creador
> "Ojalá alguien me hubiera dado esto cuando empecé — si quieres [recurso] para lograr [resultado] comenta 'yo' y te lo regalo ahora"

### Pregunta + solución inmediata
> "¿Cuánto tiempo llevas intentando [resultado] sin lograrlo? Comenta 'yo' y te mando [recurso específico] que cambió todo para mí — en menos de 1 minuto"

### Urgencia + regalo
> "Y solo por hoy te regalo [recurso específico] porque quiero que tengas los mismos [resultados] — comenta 'yo' y te lo paso en menos de 1 minuto"

---

## REGLAS DE LA MICRO-ACCIÓN

La palabra del comentario debe ser:
- Una sola palabra o máximo 2 ("yo", "sí", "quiero", "me interesa", "dale")
- Preferir "yo" — es la más probada y tiene mayor tasa de respuesta
- Evitar palabras largas o frases — aumentan la fricción y bajan el volumen de comentarios
- La palabra puede relacionarse con el tema cuando refuerza la identidad ("listo", "empiezo", "dentro")

---

## REGLAS DE ADAPTACIÓN AL NICHO

El tema del video del usuario puede variar (redes sociales, ingresos digitales, crecimiento, marketing, mentalidad). Adaptar el CTA a:
- El recurso específico que tenga sentido para ese tema
- El resultado deseado que mueva a esa audiencia
- El dolor o obstáculo que esa audiencia ya siente

No inventar recursos. Si el usuario no mencionó qué recurso ofrece, preguntar:
> "¿Qué recurso vas a mandar a quien comente? (ej: plantilla, PDF, clase, checklist, guía...)"

---

## LO QUE NO DEBE HACER ESTA SKILL

- No crear CTAs que pidan seguir, compartir o guardar — esos no generan comentarios
- No usar "link en bio" — saca a la persona de la plataforma antes de comentar
- No crear CTAs de más de 3 líneas — en video, lo que no entra en 10 segundos no funciona
- No usar lenguaje corporativo o formal — el tono es siempre conversacional, directo
- No inventar el recurso si el usuario no lo mencionó — preguntar primero
