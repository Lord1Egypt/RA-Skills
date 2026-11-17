# SISTEMA DE DISEÑO INSTAGRAM STORIES NATIVO

Este es el "look and feel" exacto que el motor (Banana o Higgsfield) debe imitar para que los slides
generados se vean como hechos directamente desde la app de Instagram.

---

## DIMENSIONES Y ASPECT RATIO

- **Aspect ratio:** 9:16 (vertical)
- **Resolución:** 1080 × 1920 pixels (HD), o 1440 × 2560 (4K) si el motor lo soporta
- **Safe zone (no UI):** desde y=250 hasta y=1670 (los 250px de arriba y los 250px de abajo los ocupa la UI nativa de IG en mobile, no poner texto crítico ahí)
- **Centro de gravedad visual:** y=960 (mitad)

---

## TIPOGRAFÍA

Instagram Stories usa fuentes nativas, todas sans-serif. Imitarlas con estas equivalencias:

| Fuente IG | Equivalente para prompt |
|---|---|
| **Classic** | "SF Pro Display Regular" / "Helvetica Neue" |
| **Modern** | "Avenir Heavy" / geometric sans bold |
| **Strong** | "Helvetica Bold" / "Inter Black" |
| **Typewriter** | "Courier Prime" |
| **Neon** | hand-drawn glow font |

**Default:** Classic (la más usada por el usuario).

**Tamaños relativos:**
- Frase principal: **64-80pt** (tipografía dominante del slide)
- Apoyo / contexto: **42-54pt**
- Notas pequeñas / aclaraciones: **28-36pt**

**Tracking (espacio entre letras):** ligeramente apretado (-2 a 0%).
**Leading (espacio entre líneas):** 1.1 a 1.2.

---

## CAJAS DE TEXTO (text boxes)

Esto es lo que más distingue el "look IG nativo" de un diseño genérico.

### Especificaciones:

```
- Padding interno: 16-24px horizontal, 10-14px vertical
- Border radius: 12-16px (rounded corners)
- Drop shadow: NO (IG no aplica sombra a cajas, solo al texto si es Strong)
- Border: NO (sin bordes)
- Background: solid color (no degradados)
```

### Las 5 cajas oficiales del usuario:

| Caja | Hex Background | Hex Text | Cuándo |
|---|---|---|---|
| Blanca | `#FFFFFF` | `#000000` | Texto principal, default |
| Negra | `#000000` | `#FFFFFF` | Texto secundario, frase impactante |
| Amarilla neón | `#FFE93C` | `#000000` | Destacar el "qué" o beneficio |
| Roja brillante | `#EF4444` | `#FFFFFF` | ERROR / alerta / consecuencia |
| Verde lima | `#4ADE80` | `#000000` | Solución / SÍ / beneficio |

**Si una caja contiene una palabra resaltada en otro color**, usa color text inline:
- "Comenta **'GPT'** y te llega" → "GPT" en `#3B82F6` (azul IG), resto del texto en `#000000`

---

## HIGHLIGHTS DE PALABRA (subrayado o color de fondo dentro del texto)

Patrón usado por el usuario en 11/11 secuencias:

### Highlight de fondo color:
```css
background-color: #FFE93C  (amarillo) - "el primer segundo"
background-color: #4ADE80  (verde lima) - "vende" "regalar" "1 minuto"
background-color: #EF4444  (rojo) - "MÁS" "ERROR" "NADIE"
```

Aplicado SOLO sobre las palabras clave, no sobre la frase entera.
Padding del highlight: 2-4px horizontal, 0px vertical.

### Color de texto inline (sin fondo):
- Palabras clave especiales en `#3B82F6` (azul IG) → ej. nombres de producto, palabras CTA
- Negrita inline (`<b>`) en `#000000` o color del texto principal

---

## ELEMENTOS GRÁFICOS RECURRENTES

### 1. Flecha amarilla curva (drawn-by-hand style)

Es el ELEMENTO ESTRELLA del usuario.

```
Color: #FFE93C (amarillo neón)
Stroke width: 8-12px
Style: hand-drawn, slightly wobbly, NOT perfectly straight
Curva: típicamente arc de 90° o S-curve
Cabeza de flecha: ▶ triangular, mismo color
```

**Posición típica:** apuntando desde una caja de texto a una captura/mockup, o desde el centro a algo importante.

### 2. X roja neón

```
Color: #FF3B3B (rojo brillante con glow)
Stroke width: 6-10px
Estilo: 2 trazos cruzados manuales, glow effect leve
Tamaño: 60-100px
```

Posición: encima de capturas/elementos que representen lo MAL hecho.

### 3. ✓ Check verde neón

```
Color: #4ADE80 (verde lima con glow)
Stroke width: 6-10px
Estilo: tick mark cuadrado o redondeado
Tamaño: 60-100px
```

Posición: encima de capturas/elementos que representen lo BIEN hecho.

### 4. Subrayado curvo

```
Color: #FFE93C o #4ADE80
Stroke width: 4-6px
Estilo: hand-drawn underline (no recto, ligeramente curvo)
```

### 5. Globo de pensamiento ☁️

```
Background: #FFFFFF
Border: #000000 1px
Cola del globo: triangular, mismo border
Border radius: ~80px (muy redondo)
```

### 6. Flechas direccionales en serie ⬇️ ⬇️ ⬇️

Tres flechas blancas pequeñas (estilo emoji) ALINEADAS verticalmente, justo arriba del CTA.

---

## EMOJIS COMO ELEMENTO DE DISEÑO

Los emojis se usan **grandes y solos** como anclas visuales, no decorativos.

| Emoji | Tamaño en slide | Función |
|---|---|---|
| ⚠️ | 80-120px | Alerta, abrir slide de consecuencia |
| 🎁 | 100-140px | Regalo, abrir slide CTA de lead magnet |
| 🤖 | 80-100px | Producto IA / GPT |
| 💰 💵 | 60-80px | Dinero / resultado financiero |
| 😱 😰 | 80-100px | Sorpresa / drama |
| 👀 | 60-80px | "Mira esto" |
| 🔥 | 60-100px | Urgencia / hot |
| 🙅‍♀️ | 80-100px | Negación, "ERROR" |
| ✋ 🤚 | 60-80px | Stop / atención |
| 👇 | 40-60px | Apuntar al elemento de abajo |

Los emojis SON los de Apple (no Google) — El usuario graba desde iPhone.

---

## CAPTURAS Y MOCKUPS (capa flotante)

Toda captura que se monte sobre el fondo debe llevar:

```
- Border radius: 12-20px (esquinas redondeadas)
- Drop shadow: 0px 8px 24px rgba(0,0,0,0.15)
- Slight rotation: 0° a 4° (random, no perfecto)
- Recorte limpio sin marcos blancos extra
- Si es DM: incluir el cabezal con la foto + nombre del que escribió (anonimizado si hace falta)
- Si es dashboard: número grande visible (ej: "+40K", "1,703 Members", "39 sesiones")
```

---

## FONDOS

### Si el slide tiene foto base del usuario:
- Aplicar **darken filter ligero** (10-15%) para que el texto destaque
- Si la foto es muy clara/saturada, agregar gradiente sutil oscuro abajo (para dejar leer texto)
- Si la foto es muy oscura, no tocar — el texto blanco resalta solo

### Si el slide es F9 (fondo de color, urgencia):
Colores de fondo permitidos:
- Crema/nude `#F5E6D3` (el usuario lo usa para frases reflexivas)
- Negro puro `#000000` (urgencia + dramatismo)
- Rojo intenso `#DC2626` (alerta máxima)

---

## NIVEL DE "RUIDO VISUAL" DESEADO

El usuario NO usa diseño limpio minimalista. Usa diseño **denso intencional** (estilo collage):

- 2-4 cajas de texto por slide
- 1-2 elementos gráficos (flecha, X, ✓, emoji)
- 1 captura/mockup (cuando aplica)
- TOTAL: ~5-7 elementos por slide

**No exceder 8 elementos** (slide se vuelve ilegible).
**No bajar de 3 elementos** (slide se ve aburrido).

---

## NEGATIVE PROMPTS (qué NO incluir nunca)

Cuando construyas el prompt para Banana/Higgsfield, incluí estos negativos:

```
- NO blurry text
- NO text outside safe zone
- NO custom decorative fonts (only IG-native sans-serif)
- NO drop shadows on text boxes (IG doesn't apply them)
- NO gradient backgrounds on boxes (only solid colors)
- NO watermarks or generated AI artifacts
- NO over-saturated colors (use exact hex values)
- NO low-quality emoji renderings
- NO Hispanic stock-looking faces (use the photo of the creator)
- NO duplicated/morphed faces
```

---

## REFERENCIAS VISUALES PARA EL MOTOR

Si el motor lo permite (Higgsfield sí), pasa **siempre** estas referencias:

1. **1-2 fotos de stories pasadas del usuario** (de la carpeta de fotos, las que tienen ya el estilo aplicado) — como style reference
2. **La foto base elegida** del slide actual — como subject reference
3. **Captura/mockup** específico del slide (si aplica) — como composition reference

Higgsfield acepta hasta 3 reference assets por generación. Úsalos.

---

## TEST DE CALIDAD DEL OUTPUT

Antes de marcar el slide como "listo", verifica:

- [ ] La frase principal se lee desde 1 metro de distancia (en el preview de IG)
- [ ] La paleta es de las 5 cajas oficiales (no colores random)
- [ ] La cara del usuario se ve igual a la foto base (no morphed)
- [ ] No hay artefactos de IA (manos extras, texto basura)
- [ ] El emoji se ve nítido (no pixelado)
- [ ] El highlight amarillo/verde está SOLO sobre 1-3 palabras clave
- [ ] El border radius de las cajas es 12-16px (no perfectamente cuadrado, no super redondo)
- [ ] La captura/mockup tiene drop shadow sutil
- [ ] El slide se siente propio de la marca (no genérico de stock)
