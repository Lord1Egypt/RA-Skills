# Los 7 Arquetipos Visuales

Destilados del análisis de 14 referencias virales (mayo 2026). Cada arquetipo tiene:
- **Cuándo se usa** (caso de uso)
- **Layout** (diagrama ASCII)
- **Elementos obligatorios** (lista)
- **Mood** (paleta + iluminación)
- **Motion preset** (cómo se anima en el video)

---

## A1 — CROSS-SECTION HIPERREALISTA + DOSAJE

**Caso de uso:** mostrar cómo N ingredientes/sustancias/ácidos/bebidas afectan a un órgano o tejido.
Ejemplos: ácidos para la piel, bebidas para el riñón, suplementos para el hígado, vitaminas para el pelo.

**Layout (9:16):**

```
┌─────────────────────────────┐
│  @watermark (top center)    │
│  🧪 🧪 🧪 🧪                │  ← N frascos (3-5) alineados arriba
│  💧 💧 💧 💧                │  ← gotas cayendo (animar)
│  ┌─────────────────────┐   │
│  │  CROSS-SECTION      │   │  ← vista en corte hiperrealista del órgano
│  │  hiperrealista      │   │     con N reacciones visibles donde
│  │  del órgano/tejido  │   │     cae cada gota
│  │                     │   │
│  └─────────────────────┘   │
│  [PILL][PILL][PILL][PILL]  │  ← caption pills blancas con beneficio
│  HOOK PRINCIPAL UPPERCASE   │
└─────────────────────────────┘
```

**Elementos obligatorios:**
- N frascos cuentagotas / tubos de ensayo / botellas alineados horizontalmente arriba
- Cada frasco etiquetado con el nombre del ingrediente (UPPERCASE pequeño, blanco)
- Líquidos de colores distintos cayendo en gota (suspendida en el aire)
- Cross-section con detalle anatómico hiperrealista (capas, poros, glandulae, túbulos)
- Pills de caption blancas con texto negro debajo del cross-section
- Hook UPPERCASE bold abajo

**Mood:** clínico dramático. Fondo negro / dark navy / dark teal. Iluminación tipo quirófano + frasco
con backlight. Reflejos vidrio hiper-detallados.

**Motion preset (video):**
- Líquidos cayendo en loop continuo de gota
- Zoom in suave 5% durante los 6s
- Las pills hacen subtle flicker/breathing
- Sin cambio de cámara — un solo plano

---

## A2 — DUALIDAD SUCIO/LIMPIO + MINI-TRABAJADORES 3D

**Caso de uso:** comparar lo que daña vs lo que sana / antes vs después / saludable vs tóxico.
Es el arquetipo MÁS VIRAL de los 7 según las referencias. Ejemplos: foods to avoid vs foods to support,
limpieza de sangre con alimentos, hábitos buenos vs malos sobre el cuerpo.

**Layout (9:16):**

```
┌─────────────────────────────┐
│      HOOK PRINCIPAL          │
│  [SUB-A]    │   [SUB-B]      │
│   rojo      │   verde        │
│   ─────────┼─────────       │
│  [ÓRGANO    │  [ÓRGANO       │
│   DAÑADO]   │   SANO]        │  ← split vertical 50/50
│   oxidado   │   limpio       │
│   marrón    │   rosa fresco  │
│  👷👷       │   👷👷         │  ← mini-trabajadores 3D
│  hazmat     │   hazmat       │     escala Playmobil escalando
│  naranja    │   verde        │     y operando sobre el órgano
│   ─────────┼─────────       │
│  [GRID 4-8 │  [GRID 4-8      │
│   items]   │   items]        │  ← productos con foto + label
└─────────────────────────────┘
```

**Elementos obligatorios:**
- Split vertical exacto al 50%
- Lado izquierdo: órgano oxidado/dañado en tonos marrón/rojo opaco/grumoso
- Lado derecho: el mismo órgano sano, brillante, rosa/rojo fresco
- 4-6 mini-figuras 3D estilo Playmobil/diorama con cascos y trajes hazmat
  - Lado izquierdo: trajes naranjas (operarios de daño)
  - Lado derecho: trajes verdes/blancos (limpiadores) con manguera/spray/cepillo
- Grid inferior de productos con foto realista + etiqueta de nombre
- Hooks coloreados: rojo (mal lado) + verde (buen lado)

**Mood:** dramático cinematográfico. Fondo natural del entorno (laboratorio, cocina). Profundidad de
campo cerrada. Render Octane.

**Motion preset (video):**
- Mini-trabajadores moviéndose (caminando, escalando, lanzando agua)
- Chorros de agua/spray animados
- Parallax sutil entre planos
- Sin transiciones — todo dentro de un mismo plano

---

## A3 — PERSONA PARTIDA VERTICAL + BULLETS LATERALES

**Caso de uso:** comparar dos versiones de UNA persona — hábitos buenos vs malos, estado A vs B,
high cortisol vs low cortisol, antes vs después de un cambio.

**Layout (9:16):**

```
┌─────────────────────────────┐
│   HOOK A      vs   HOOK B    │
│   subhook     │    subhook   │
│                              │
│  [bullet]  ┌───────┬───────┐ │
│   icono    │ MITAD │ MITAD │ │
│  [bullet]  │  IZQ  │  DER  │ │
│   icono    │ persona persona│ │  ← MISMA persona, mitades distintas
│  [bullet]  │ tono A │ tono B│ │
│   icono    │       │        │ │
│  [bullet]  │       │        │ │
│   icono    └───────┴───────┘ │
│            [ICON][ICON][ICON]│  ← row de íconos abajo
│            [ICON][ICON][ICON]│
│   ────────────────────       │
│   tagline o url marca        │
└─────────────────────────────┘
```

**Elementos obligatorios:**
- Foto fotorrealista de UNA persona, partida vertical exactamente por el centro de la cara/cuerpo
- Cada mitad con tratamiento de color distinto (warm/cool, rojo/verde)
- 4-6 bullets a cada lado con ícono pequeño + texto corto (3-5 palabras)
- Cada bullet conectado por línea fina al punto del cuerpo donde aplica
- Hook UPPERCASE arriba con "vs" o "&" entre las dos versiones
- Footer opcional con marca/url

**Mood:** elegante editorial. Fondo neutro o gradiente sutil. Tipografía limpia sans-serif.

**Motion preset (video):**
- Reveal progresivo de bullets (uno cada 0.4s)
- Leve breathing en la imagen central
- Las líneas de conexión se dibujan progresivamente
- Final: ambos lados completos, hold de 1s, loop

---

## A4 — GRID COMPARATIVO CON ETIQUETA + VERDICT

**Caso de uso:** listas, rankings, menús, comparativas de items con verdict (👍/👎, hora, país, etc).
Ejemplos: foods at the right time, IAs comparison, mejores app de productividad, top series por país.

**Layout (9:16):**

```
┌─────────────────────────────┐
│      HOOK PRINCIPAL          │
│      sub-hook contexto       │
│                              │
│  [foto]  ITEM 1              │
│          [verdict pill]      │
│  ITEM 2          [foto]      │  ← intercalado izq/der
│  [verdict pill]              │
│  [foto]  ITEM 3              │
│          [verdict pill]      │
│  ITEM 4          [foto]      │
│  [verdict pill]              │
│  ... (6-10 items en total)   │
│                              │
│  footer/tip                  │
└─────────────────────────────┘
```

**Elementos obligatorios:**
- 6-10 items, cada uno con foto real del item + nombre + verdict pill
- Verdict pills colorados: verde 👍 / rojo 👎 / neutro / hora
- Layout intercalado izquierda-derecha o grid 2 columnas
- Fondo neutro (crema, papel, blanco off-white o gradient suave)
- Tipografía limpia, máxima densidad

**Mood:** scrapbook / lifestyle / educativo. Fondo papel beige/crema. Iluminación natural difusa.
Sin drama, todo legible.

**Motion preset (video):**
- Cada item aparece en cascada (slide-up + fade) cada 0.3s
- Pills de verdict con flicker subtle al aparecer
- Pan vertical suave si la lista es larga
- Hold final con todos los items visibles

---

## A5 — STACK VERTICAL DE VARIANTES DEL MISMO MOTIVO

**Caso de uso:** mostrar el efecto de cambiar UN parámetro variable. Ejemplos: distancia focal de
cámara (85mm/50mm/10mm), apertura (f/1.4 → f/16), luz (golden hour vs blue hour), etc.

**Layout (9:16):**

```
┌─────────────────────────────┐
│  [LABEL_A]  ┌───────────┐   │
│             │ FOTO A    │   │
│             └───────────┘   │
│  [LABEL_B]  ┌───────────┐   │
│             │ FOTO B    │   │  ← misma escena/sujeto
│             └───────────┘   │     parámetro distinto
│  [LABEL_C]  ┌───────────┐   │
│             │ FOTO C    │   │
│             └───────────┘   │
│  ... (3-6 variantes)        │
└─────────────────────────────┘
```

**Elementos obligatorios:**
- Mismo encuadre / sujeto / escena en todas las filas
- Sólo cambia UN parámetro (especificado en label)
- Label a la izquierda en pill blanca o sobre la foto
- Stack vertical SIN espacios — bandas continuas

**Mood:** depende del tema. Si es fotografía/cine, fondo cinematográfico. Si es ciencia, fondo neutro.

**Motion preset (video):**
- Cada banda transiciona como si fuera secuencial (la cámara "viaja" hacia abajo)
- O cross-fade entre variantes (mismo encuadre, valor cambiando)
- 1.5s por variante

---

## A6 — DUAL CHARACTER SIDE-BY-SIDE

**Caso de uso:** comparar dos eras / dos personajes / dos arquetipos / dos versiones de marca.
Ejemplos: IA en 2025 vs IA en 2026, gen Z vs millennial, freelancer vs CEO, novato vs experto.

**Layout (9:16):**

```
┌─────────────────────────────┐
│      @watermark              │
│  [HOOK A]    │  [HOOK B]     │
│   bg rojo    │   bg verde    │
│   ──────────┼──────────     │
│  [PERSONAJE]│ [PERSONAJE]   │
│   o avatar  │  o avatar     │  ← 2 figuras de cuerpo entero
│   completo  │  completo     │
│   ─────     │   ─────       │
│  [card 1]   │  [card 1]     │  ← cards apiladas verticalmente
│  [card 2]   │  [card 2]     │     SOBRE el cuerpo del personaje
│  [card 3]   │  [card 3]     │
│  [card 4]   │  [card 4]     │
└─────────────────────────────┘
```

**Elementos obligatorios:**
- Dos figuras de cuerpo entero o medio cuerpo, una a cada lado
- Hook coloreado arriba en pill por cada lado
- 3-5 cards rectangulares blancas apiladas verticalmente sobre el cuerpo de cada personaje
- Cada card con logo/icono + nombre de la herramienta/categoría
- Diferencia visual clara entre personajes (color, ropa, expresión, era)

**Mood:** contraste fuerte. Cinematográfico, casi editorial.

**Motion preset (video):**
- Cards aparecen en cascada de abajo hacia arriba
- Personajes con leve breathing
- Backgrounds con sutil movimiento (humo, partículas)

---

## A7 — DIORAMA 3D DE OBJETOS POR CATEGORÍA

**Caso de uso:** mostrar tipos/categorías de un mismo objeto. Ejemplos: tipos de techos, tipos de
cortes de pelo, formas de cara, estilos arquitectónicos, tipos de letras.

**Layout (9:16):**

```
┌─────────────────────────────┐
│   HOOK GRANDE BOLD           │
│                              │
│   [obj1]  [obj2]  [obj3]    │
│   nombre  nombre  nombre    │
│                              │
│   [obj4]  [obj5]  [obj6]    │
│   nombre  nombre  nombre    │
│                              │
│   [obj7]  [obj8]  [obj9]    │
│   nombre  nombre  nombre    │
│                              │
│           [obj10]            │
│           nombre             │
└─────────────────────────────┘
```

**Elementos obligatorios:**
- 6-10 objetos del mismo tipo, cada uno renderizado en 3D estilizado/realista
- Mismo encuadre / mismo ángulo / mismo lighting para todos (consistencia visual)
- Etiqueta debajo de cada objeto con nombre de la variante
- Fondo plano de un solo color (azul polvo, gris, blanco) que destaca los objetos
- Hook arriba simple, una línea

**Mood:** educativo, limpio, sin drama. Render 3D estilo "exploded view" o "isometric".

**Motion preset (video):**
- Cada objeto rota suavemente sobre su eje (loop)
- Labels aparecen en cascada
- Pan vertical opcional si son muchos
