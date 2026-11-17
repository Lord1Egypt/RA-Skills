# Brandkit — Reglas de paleta, tipografía, copy

Reglas universales que se aplican a TODOS los arquetipos y se inyectan en los prompts.

---

## PALETA POR MOOD

### `clinico_dramatico` (default para A1, A2)
- Fondo: `dark navy #0A1A2F` o `dark teal #0D2B36` o `near-black #0A0A0A`
- Texto principal: blanco puro `#FFFFFF`
- Acento positivo: verde clínico `#3DD68C`
- Acento negativo: rojo sangre `#E63946`
- Detalles: dorado/ámbar `#F4B860`

### `calido_lifestyle` (default para A4)
- Fondo: crema `#F4EBD0` o papel `#F1E9D2`
- Texto principal: charcoal `#2B2B2B` o serif marrón `#5C3A21`
- Acento positivo: verde oliva `#5B7553`
- Acento negativo: terracota `#A8431E`
- Detalles: dorado mate `#C8A24B`

### `tech_cyber` (default para A6)
- Fondo: gradiente oscuro `#0A0A0A → #1A1A2E`
- Texto principal: blanco neón `#FFFFFF`
- Acento A: cian eléctrico `#00D9FF`
- Acento B: magenta neón `#FF006E`
- Detalles: verde matrix `#00FF41`

### `scrapbook` (alternativa para A4 lifestyle)
- Fondo: blanco roto `#FAF7F0` con textura papel
- Acentos: tape washi crema, post-it amarillo limón, sombras suaves
- Texto: serif clásico negro

### `editorial` (default para A3, A7)
- Fondo: gradiente neutro suave (warm-to-cool si A3, sólido si A7)
- Texto principal: blanco o charcoal
- Acentos: 1 color por lado (warm vs cool)

---

## TIPOGRAFÍA

| Rol | Fuente sugerida | Características |
|---|---|---|
| Hook principal | Bold sans-serif (Inter, Helvetica Now, Anton) | UPPERCASE, tracking ajustado, peso 700-900 |
| Sub-hook | Misma familia, peso 500-600 | Mixed case, tamaño 60% del hook |
| Etiquetas en pills | Sans-serif limpia (Inter, SF Pro) | Sentence case, peso 500 |
| Caption serif (lifestyle) | Display serif (Playfair, Cormorant) | Para A4 lifestyle / scrapbook |
| Bullets sidebars (A3) | Sans-serif fina (Inter Light) | 12-14pt, espaciado generoso |

**REGLA**: nunca mezclar más de 2 familias tipográficas en la misma imagen.

---

## REGLAS DE COPY

### Idioma
- **El usuario escribe en español NEUTRO** (de la memoria del sistema).
- Reemplazos obligatorios si el input es argentino:
  - `vos` → `tú`
  - `tenés` → `tienes`
  - `acá` → `aquí`
  - `mirá` → `mira`
  - `copiá` → `copia`
  - `dale` → `está bien` / "vamos"
- Si el input es en inglés, mantener inglés.
- NUNCA mezclar idiomas en la misma imagen.

### Longitud de textos en imagen
- **Hook**: 1-3 palabras UPPERCASE. Ej: "KIDNEY CARE", "BLOOD CLEANING", "HÁBITOS QUE DAÑAN".
- **Sub-hook**: 2-4 palabras. Ej: "Foods to limit", "Lo que cuida".
- **Etiqueta de item**: 1-3 palabras. Ej: "Coconut water", "Cebada", "Granada".
- **Atributo/verdict**: 3-5 palabras. Ej: "Removes toxins", "Limpia toxinas", "Avoid late evening".
- **Total de palabras en la imagen**: 30-80 ideal. >100 ilegible.

### Tono de copy
- **Directo**: imperativo, sin rodeos, sin filler.
- **Específico**: nombres concretos, verbos de acción.
- **Sin promesas medicas falsas**: si menciona "limpia", "elimina", "cura" → debe estar respaldado
  por research. Cuando no se pueda verificar, usar verbos suaves ("apoya", "favorece", "ayuda a").
- **Sin emojis dentro del texto literal de la imagen** (salvo 👍/👎 en pills de A4).
- **Watermark**: opcional. Si se usa, formato `@handle` en serif fina, semi-transparente, top center.

---

## REGLAS DE LAYOUT 9:16

- **Resolución target**: 1080×1920 px.
- **Safe area**: 60px de margen inferior (Instagram UI), 100px de margen superior (Stories UI / IG handle).
- **Densidad visual**: 60-75% del frame ocupado, 25-40% respiración (nunca >80%, nunca <40%).
- **Punto focal**: siempre en el TERCIO SUPERIOR-MEDIO (regla de los tercios). Es donde el ojo del
  scroller cae primero.
- **Hook arriba**: el texto principal SIEMPRE en los primeros 200px desde el top.

---

## DOS Y DON'TS GLOBALES

✅ **Sí:**
- Render hiperrealista 3D / Octane / fotorrealista
- Profundidad de campo cerrada (sujeto aislado)
- Iluminación cinematográfica
- Mini-figuras 3D estilo Playmobil cuando aplica (A2)
- Texto en pills blancas con bordes redondeados
- Watermark sutil opcional

❌ **No:**
- Estilos cartoon o flat illustration (rompe el código viral)
- Más de 10 items en la imagen
- Más de 100 palabras totales
- Mezcla de 2 idiomas
- Emojis aleatorios fuera de pills 👍👎
- Logos/branding de terceros sin contexto del brief
- Cualquier elemento que reste densidad informativa al sujeto principal
