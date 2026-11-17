---
name: multiplicador-de-contenido
description: "Skill para multiplicar un guion o idea en múltiples formatos de contenido. Activar SIEMPRE que alguien pida: multiplicar un video, reciclar un guion, transformar un script en diferentes formatos, sacar más contenido de una idea, remasterizar un guion, convertir un video en varios, reutilizar contenido, o cualquier variación que implique tomar una pieza de contenido existente y expandirla a múltiples formatos. También activar cuando digan \"tengo este guion y quiero hacer más\", \"¿cómo saco más contenido de esto?\", \"quiero publicar más sin grabar tanto\", \"multiplica esto\", \"¿en qué formatos puedo usar esta idea?\"."
metadata: {"openclaw": {"emoji": "🦞"}}
---

## 🦞 Corriendo en OpenClaw

> Esta versión corre en un agente OpenClaw (servidor + Telegram), no en Claude Code.
> **Antes de seguir, lee la skill `f100k-puente`**: traduce herramientas y rutas.
> Lo específico de esta skill:
>
> - Skill de solo texto: corre tal cual.
> - La sección «Setup para Claude Desktop» (Xpoz, MCP sociales) no aplica aquí: sáltala.
> - Si la usuaria manda un link de YouTube o un video largo, pide la transcripción o usa tu herramienta para leer la página; no descargues video pesado.
> - Guarda las piezas en `guiones/` y manda el resumen por Telegram.

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

# Skill: Multiplicador de Contenido

Esta skill toma un guion núcleo y lo transforma en hasta 5 propuestas de contenido listas para grabar — en formatos distintos, con ángulos distintos, usando la misma idea de base. El objetivo es publicar más sin crear desde cero todos los días.

**Filosofía de fondo:** No necesitas 10 ideas nuevas. Necesitas un buen guion núcleo y transformarlo en 10 formatos distintos. La economía creativa: reciclar lo que ya funciona es más eficiente — y con frecuencia da mejores resultados — que inventar algo nuevo cada vez.

---

## PASO 1 — Obtener el guion núcleo

Si el usuario ya pegó su guion o idea en el mensaje, úsalo directamente.

Si no lo proporcionó, pregunta:
> "¿Cuál es el guion o idea que quieres multiplicar? Puedes pegar el texto completo, resumirlo en una o dos oraciones, o darme el tema central."

---

## PASO 2 — Extraer los elementos del guion núcleo

Antes de sugerir formatos, identifica estos 4 elementos en el guion recibido:

1. **Idea clara** — ¿cuál es el único mensaje central? (si tiene varios, identifica el más fuerte)
2. **Evidencia o dato** — ¿hay algún dato, resultado, estadística o prueba que lo soporte?
3. **Ejemplo breve** — ¿hay una historia, caso o demostración concreta?
4. **Llamado a la acción** — ¿hacia dónde apunta al final? (venta, comunidad, reflexión, guardar)

Estos 4 elementos son los que se reciclan en cada formato. Si al analizar el guion falta alguno, tómalo en cuenta al proponer las transformaciones (ciertos formatos requieren más evidencia, otros funcionan sin ella).

---

## PASO 3 — Seleccionar los 5 mejores formatos

Lee el catálogo completo en `references/formatos.md`.

Elige los **5 formatos más estratégicos** para ese guion específico. No elijas al azar — aplica estos criterios:

**Criterios de selección:**
- **Variedad de producción**: incluye al menos un formato de baja producción (puede grabarse en 10 min) y uno de producción media
- **Variedad de energía**: mezcla formatos de impacto rápido con formatos más narrativos
- **Afinidad con el contenido**: si el guion tiene datos, prioriza Descubrimiento o Desmintiendo Mitos; si tiene historia, prioriza Historia Curiosa o B-Roll Storytelling; si es educativo paso a paso, prioriza Tutorial o Pizarra
- **Potencial viral del ángulo**: elige formatos que cambien el ángulo de forma que el mismo mensaje llegue a audiencias distintas
- **Facilidad de ejecución**: prioriza que el creador pueda grabar los 5 sin agotarse

---

## PASO 4 — Presentar las 5 propuestas

Para cada propuesta, entrega exactamente esto:

```
## Propuesta [N]: [Nombre del formato]

**Por qué funciona para tu guion:** [1 oración explicando por qué este formato encaja con su idea específica]

**Ángulo nuevo:** [Cómo cambia el enfoque respecto al guion original — 1 oración]

**Gancho sugerido:** "[Frase de gancho concreta y lista para usar]"

**Estructura rápida:**
1. [Paso 1 adaptado a su idea]
2. [Paso 2 adaptado a su idea]
3. [Paso 3 adaptado a su idea]
4. [Cierre/CTA]

**Nivel de producción:** Bajo / Medio / Alto
**Tiempo estimado de grabación:** X minutos
```

Las propuestas deben estar **adaptadas al contenido real del usuario** — no genéricas. El gancho y la estructura deben mencionar su tema, sus palabras, su contexto.

---

## PASO 5 — Cierre accionable

Después de las 5 propuestas, agrega:

> "¿Quieres que desarrolle el guion completo de alguna de estas propuestas? Dime cuál y te lo escribo listo para grabar."

Esto invita al siguiente paso sin presionar.

---

## CRITERIOS DE CALIDAD

Antes de entregar las propuestas, verifica:

- [ ] ¿Cada propuesta tiene un ángulo genuinamente distinto al guion original?
- [ ] ¿El gancho de cada propuesta es concreto y específico (no genérico)?
- [ ] ¿Hay variedad en los niveles de producción?
- [ ] ¿Las estructuras están adaptadas a la idea del usuario, no son plantillas vacías?
- [ ] ¿El usuario podría empezar a grabar cualquiera de estas hoy?

---

## NOTAS IMPORTANTES

- El objetivo no es dar 5 versiones del mismo video. Es dar 5 puertas de entrada diferentes al mismo mensaje para que llegue a audiencias distintas.
- Algunos formatos funcionan mejor en ciertos nichos. Si el usuario menciona su nicho o industria, considera eso al elegir.
- Los formatos de "Faceless" o "B-Roll" son ideales para creadores que no quieren aparecer en cámara — si hay señales de eso, priorízalos.
- Si el guion es muy largo o tiene múltiples ideas, sugiérele al usuario que lo simplifique a una sola idea antes de multiplicar.
