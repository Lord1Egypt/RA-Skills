# Configuración NanoBanana para Miniaturas YouTube

## Configuración base siempre aplicar

```
Aspect ratio: 16:9        → set_aspect_ratio ANTES de generar
Resolution: 2K            → imageSize: "2K"  
Model: gemini-3.1-flash-image-preview
```

YouTube requiere exactamente **1280x720 píxeles**. NanoBanana en 16:9 + 2K se acerca.
Post-procesamiento con ImageMagick para dimensiones exactas si es necesario.

---

## Flujo según si hay foto del usuario o no

### CON foto propia (recomendado — convierte más)

Usar `gemini_edit_image` con la foto como input.

**Prompt de edición para foto propia:**
```
Place this person centered on a pure solid black background (#000000).
Preserve all edge detail and hair strands precisely.
Add a bold yellow (#FFD700) text banner "[PALABRAS]" in thick sans-serif font
[at the top / at the bottom] of the image.
[Optional: add small Instagram logo top-right corner]
Maintain the person's original expression and pose.
Result should look like a professional YouTube thumbnail.
Keep composition clean with significant negative space.
```

**Si la foto tiene fondo blanco y necesitas removerlo primero:**
```bash
magick foto_original.jpg -fuzz 15% -transparent white foto_sin_fondo.png
```
Luego usar esa PNG como input de `gemini_edit_image`.

---

### SIN foto propia (generación completa)

Usar `gemini_generate_image` con descripción detallada.

**Descripción física estándar para el usuario (adaptar para otros):**
```
Latin American woman in her late 20s, long dark hair, warm skin tone,
confident radiant smile, professional but approachable style,
wearing [blusa/blazer] in [color que contraste con fondo negro].
```

**Prompt completo de generación:**
```
[Descripción física] centered on pure solid black background,
direct eye contact with camera, confident [smile/determined] expression.
Bold yellow (#FFD700) sans-serif text "[PALABRAS EN MAYÚSCULAS]" 
prominently placed [above/below] the person, thick font weight.
[Opcional: small platform icons - Instagram, TikTok]
Professional studio photography, dramatic front lighting with subtle rim light.
Clean minimal composition, heavy negative space around subject.
YouTube thumbnail format, 16:9 aspect ratio, high contrast.
IMPORTANT: solid black background only, NO gradients or textures.
```

---

## Tres variaciones — cómo diferenciarlas

Para las 3 variaciones obligatorias, cambiar UN elemento cada vez:

| Variación | Cambio |
|-----------|--------|
| **A** | Texto arriba, persona centrada, expresión sonriendo |
| **B** | Texto abajo, persona ligeramente a la izquierda, expresión de sorpresa o señalando |
| **C** | Texto lateral derecho, persona izquierda mirando al texto, + 1 ícono adicional |

---

## Post-procesamiento final

Recortar a dimensiones exactas YouTube:
```bash
# Verificar herramienta disponible
which magick && echo "ImageMagick 7 OK" || which convert && echo "ImageMagick 6 OK"

# Recortar a 1280x720 exactos
magick variacion_a.png -resize 1280x720^ -gravity center -extent 1280x720 thumbnail_a_final.png
magick variacion_b.png -resize 1280x720^ -gravity center -extent 1280x720 thumbnail_b_final.png
magick variacion_c.png -resize 1280x720^ -gravity center -extent 1280x720 thumbnail_c_final.png
```

---

## Errores frecuentes y soluciones

| Error | Causa | Solución |
|-------|-------|---------|
| Fondo no completamente negro | Prompt no explícito | Agregar "MUST be pure #000000 solid black, NO gradients" |
| Texto ilegible o distorsionado | Texto muy largo | Reducir a máx 4 palabras, font más bold |
| Persona mal recortada | Fondo original complejo | Usar `magick -fuzz 20%` para mejor remoción |
| `IMAGE_SAFETY` bloqueado | Expresión o elemento sensible | Simplificar descripción, usar "professional" y "family-friendly" |
| Composición muy cargada | Demasiados elementos en prompt | Quitar 1-2 elementos, mantener solo persona + texto |
