---
name: product-description-generator-lite
description: Convierte características reales en fichas de producto con SEO y tono de marca, sin inventar datos. Versión Lite: flujo esencial de entrada y salida, más las reglas anti-alucinación que impiden rellenar con humo.
---

# Generador de Descripciones de Productos (Lite)

Escribe fichas de producto listas para publicar a partir de datos reales: título SEO, meta descripción, descripción corta, descripción larga, viñetas y llamada a la acción.

La regla que gobierna todo lo demás: **si un dato no está en la entrada, no se escribe.** Va a `Datos pendientes`.

---

## Cómo usar

Rellena esta plantilla y pásala al agente:

```text
Producto: [nombre comercial exacto]
Categoría: [tecnología | moda | calzado | alimentos | hogar | belleza | otro]
Características: [hechos comprobables, separados por punto y coma]
Público objetivo: [quién compra, edad aproximada, necesidad principal]
Tono de marca: [cercano | profesional | divertido | premium | minimalista | técnico]
```

Opcionales: `Idioma`, `Palabras clave`, `Mercado`.

---

## Formato de salida

Entrega siempre estas secciones, en este orden:

```markdown
### Título SEO
[máximo 60 caracteres, keyword principal al inicio]

### Meta descripción
[120 a 155 caracteres, beneficio + llamada a la acción]

### Descripción corta
[1 o 2 frases]

### Descripción larga
[2 a 4 párrafos: gancho, beneficio principal, objeciones, cierre]

### Bullets
- [3 a 7 viñetas: beneficio + característica que lo respalda]

### Llamada a la acción
[1 frase, sin presión artificial]

### Datos pendientes
[lo que falta; "Ninguno" si está todo]

### Notas del agente
[1 a 3 líneas: ángulo, keywords y supuestos]
```

---

## Instrucciones para el agente

**1. Valida la entrada.** Comprueba los cinco campos obligatorios.

**2. Cuenta las características verificables.** Hechos comprobables: material, medida, capacidad, proceso, certificación. **Los adjetivos no cuentan.**

- 3 o más → escribe la ficha completa.
- Menos de 3 → no redactes. Devuelve la plantilla vacía, las preguntas agrupadas en una sola ronda y esta frase: «Con esto puedo escribir un escaparate, no una ficha».

**3. Identifica el beneficio.** Para cada característica pregunta: *¿qué cambia esto en el día a día de quien compra?* Una característica sin beneficio se queda como dato técnico, nunca como promesa.

**4. Calibra el tono.** Cercano: frases cortas, «tú». Profesional: sobrio, sin slang. Premium: cuidado, sin superlativos. Minimalista: sin adjetivos. Técnico: datos y unidades.

Si no hay tono declarado, aplica un tono **cálido-neutro** y decláralo en `Notas del agente` con esta frase: «Tono aplicado por defecto, no indicado por el usuario».

**5. Redacta.** Descripción larga en cuatro movimientos: gancho, beneficio principal, dos detalles que resuelven objeciones, cierre que invite a actuar sin presionar.

**6. Convierte a viñetas.** Entre 3 y 7. Cada una: beneficio + característica que lo demuestra. Nunca añadas una para llegar a cinco.

**7. Cierra.** En `Datos pendientes`, lista lo que falta ordenado por impacto: primero lo que desbloquearía la ficha.

---

## Reglas que no se saltan

- **No inventes** materiales, medidas, colores, certificaciones, garantías, precios, plazos ni cifras. Si no está en la entrada, va a `Datos pendientes`.
- **No conviertas una característica en otra promesa.** Si el estuche da 40 h de uso total, no escribas «40 horas de reproducción continua».
- **No infles adjetivos.** Si el usuario dijo «cómodas», puedes escribir «cómodas»; nunca «las más cómodas».
- **No prometas resultados de salud** ni propiedades «clínicamente probadas» sin respaldo.
- **Prohibido el relleno genérico:** «calidad premium», «la mejor elección», «diseño innovador», «materiales de primera».
- **No inventes logística:** envío gratis, stock, descuentos o financiación solo si te los dan.

---

## SEO mínimo

- Keyword principal (2 a 4 palabras) en el título, la meta descripción y la primera frase.
- Título ≤ 60 caracteres. Meta descripción 120–155, con beneficio y acción.
- Máximo una aparición de la keyword por cada 100 palabras. Si suena forzado, reescribe la frase.
- Viñetas escaneables y párrafos de 2 a 4 líneas: la mayoría se lee en móvil.

---

## Si falta información

Pregunta **una sola vez**, agrupando todas las dudas. Si el usuario pide avanzar igual, entrega una ficha degradada precedida de este aviso:

`⚠️ Ficha incompleta — X de 5 campos no verificables. No publicar sin completar.`

Menos viñetas, no viñetas inventadas.

---

## Dependencias

Ninguna. No ejecuta scripts, no llama a APIs, no necesita conexión.
