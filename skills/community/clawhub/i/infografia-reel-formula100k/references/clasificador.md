# Clasificador de Arquetipo

Árbol de decisión para mapear `brief` → arquetipo A1–A7.

---

## Paso 1 — Detectar la INTENCIÓN del brief

Lee el brief (output de `input-pipeline.md`) y responde estas preguntas en orden:

### Pregunta 1: ¿El brief muestra el EFECTO de N sustancias sobre UN órgano/tejido?

**SÍ** → **A1 Cross-section + dosaje**

Señales: el brief menciona ingredientes / ácidos / bebidas / suplementos / vitaminas / aceites + un
órgano específico (piel, cabello, hígado, riñón, corazón, intestino, pulmón).

Ejemplos disparadores:
- "5 ácidos para tu piel"
- "bebidas que limpian los riñones"
- "qué le pasa al hígado cuando tomas X"
- "ingredientes activos para el pelo"
- "vitaminas que llegan al cerebro"

---

### Pregunta 2: ¿El brief compara DAÑO vs BENEFICIO con grid de items?

**SÍ** → **A2 Dualidad sucio/limpio + mini-trabajadores**

Señales: el brief tiene 2 listas opuestas (lo que daña / lo que sana, foods to avoid / foods to support)
+ mención de un órgano o sistema (sangre, riñón, hígado, corazón).

Ejemplos disparadores:
- "alimentos que limpian la sangre vs que la ensucian"
- "kidney care: foods to limit / foods to support"
- "lo que destruye tu hígado vs lo que lo regenera"
- "rutinas que arruinan tu pelo vs que lo salvan"

---

### Pregunta 3: ¿El brief compara dos ESTADOS de UNA persona?

**SÍ** → **A3 Persona partida + bullets**

Señales: el brief habla de hábitos, estados emocionales, condiciones hormonales, actitudes,
"antes/después" sobre el cuerpo o cara de UNA persona.

Ejemplos disparadores:
- "high cortisol vs low cortisol cómo se ve"
- "hábitos que te envejecen vs que te rejuvenecen"
- "señales de deficiencia de magnesio en la cara"
- "el efecto del estrés en tu cuerpo"

---

### Pregunta 4: ¿El brief es una LISTA/RANKING de items con verdict?

**SÍ** → **A4 Grid comparativo**

Señales: 6-10 items con un atributo binario o categórico simple. El brief NO requiere mostrar el efecto
sobre un órgano. Es educativo/curatorial puro.

Ejemplos disparadores:
- "mejores apps de productividad 2026"
- "alimentos que comes mal: el momento correcto del día"
- "11 IAs que tienes que conocer"
- "top series de Netflix por país"
- "tipos de inversión por nivel de riesgo"

---

### Pregunta 5: ¿El brief muestra el efecto de cambiar UN parámetro?

**SÍ** → **A5 Stack de variantes**

Señales: el brief tiene UNA escena/sujeto + un parámetro variable (distancia, apertura, luz, dosis,
edad, tiempo, temperatura).

Ejemplos disparadores:
- "85mm vs 50mm vs 35mm: cómo cambia la foto"
- "el mismo plato a 60°, 100°, 180°"
- "tu piel a los 20, 30, 40, 50"
- "hot vs warm vs cold: el mismo café"

---

### Pregunta 6: ¿El brief compara DOS ERAS / PERSONAJES / ARQUETIPOS?

**SÍ** → **A6 Dual character**

Señales: el brief opone dos figuras enteras (eras, generaciones, perfiles profesionales,
pasado/futuro) y enumera atributos de cada una.

Ejemplos disparadores:
- "IA en 2025 vs IA en 2026"
- "freelancer vs empleado: 5 diferencias clave"
- "novato vs experto en X"
- "marketer del pasado vs del presente"

---

### Pregunta 7: ¿El brief muestra TIPOS/CATEGORÍAS de un mismo objeto?

**SÍ** → **A7 Diorama 3D**

Señales: el brief enumera 6-10 variantes del MISMO tipo de objeto (techos, peinados, formas
geométricas, tipos de letra, modelos de auto).

Ejemplos disparadores:
- "tipos de techos en arquitectura"
- "formas de cara: ovalada, redonda, cuadrada..."
- "tipos de cortes de pelo para hombre"
- "formas de packaging para skincare"

---

## Paso 2 — Si hay más de un match

Prioridad cuando varios arquetipos aplican:

```
A1 > A2 > A4 > A3 > A6 > A7 > A5
```

Razón: A1, A2 y A4 son los más virales según el análisis de las 14 referencias.

---

## Paso 3 — Si NINGÚN arquetipo aplica claramente

Caer al **default A4 Grid comparativo** (es el más versátil, funciona con casi cualquier lista).

Si el tema NO es enumerable, NO es comparativo, y NO tiene anatomía clara → **decirle al usuario que
el tema no es ideal para infografía-reel** y sugerirle:
- Usar `carrusel-viral-formula100k` en su lugar
- O repensar el ángulo del tema para hacerlo enumerable

---

## Paso 4 — Validar con el usuario

NUNCA generes la imagen sin confirmar el arquetipo elegido. Muestra el mockup ASCII (definido en
`arquetipos.md` para cada arquetipo) y pregunta:

> "Voy a usar el arquetipo **AX — [nombre]**. Funciona así: [descripción 1 línea].
> Mockup:
> [ASCII]
> ¿Confirmamos o cambiamos a otro arquetipo?"

Si el usuario propone un arquetipo distinto, respeta su elección.
