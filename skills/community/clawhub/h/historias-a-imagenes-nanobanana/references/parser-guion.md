# PARSER DEL GUION (.md)

Cómo leer y validar el archivo .md generado por `guionizacion-historias-formula100k`.

---

## ESTRUCTURA ESPERADA

El archivo tiene 4 bloques en este orden estricto:

1. **Frontmatter YAML** (entre `---` y `---`)
2. **Encabezado y metadata** (heading + cita)
3. **Tabla slide-by-slide** (header `## 📋 Tabla slide-by-slide`)
4. **Briefing visual general** + **Notas de producción** + **Bloque ⚙️ YAML**

---

## EXTRACCIÓN

### 1. Frontmatter YAML

Captura todo lo que está entre la primera y la segunda línea `---`. Parsear como YAML:

```yaml
titulo: ...
fecha: 2026-05-06
categoria: lead-magnet
estructura: "#9 — Algo me ha sorprendido"
objetivo: ...
palabra_clave_cta: GPT
slides: 5
mood: ...
```

Validar campos requeridos: `titulo`, `categoria`, `estructura`, `palabra_clave_cta`, `slides`.

### 2. Tabla slide-by-slide

Buscar la línea `## 📋 Tabla slide-by-slide` y la primera tabla markdown debajo.

Columnas esperadas (en orden):
- `#` — número de slide
- `Frase principal` — entre comillas dobles "..."
- `Capa visual` — descripción libre
- `Formato` — empieza con 🎥 o 📸 + F[1-15] + nombre
- `Qué grabar/buscar` — instrucción
- `Briefing de diseño` — descripción visual completa

Parsear cada fila a un objeto:

```json
{
  "n": 1,
  "frase": "Algo me sorprendió hoy...",
  "capa_visual": "captura de DM con 8.7K reacciones",
  "formato_emoji": "🎥",
  "formato_codigo": "F1",
  "formato_nombre": "Video Selfie",
  "que_grabar": "Selfie hablando a cámara en el escritorio",
  "briefing": "Fondo: ...; Cajas: ...; Elementos: ...; Highlight: ..."
}
```

### 3. Bloque ⚙️ (CRÍTICO para Skill C)

Buscar el bloque:

````
## ⚙️ Para la skill `historias-a-imagenes-nanobanana`

```yaml
slides_count: 5
fotos_necesarias_de_carpeta:
  - slide_1: "la creadora caminando en escenario amplio, plano general"
  - slide_2: "la creadora en escritorio con laptop"
  ...
elementos_a_generar:
  - slide_2: "captura de calendario lleno de sesiones"
  - slide_4: "mockup de un GPT con interfaz de OpenAI"
estilo_textos: instagram-stories-native
```
````

Parsear el bloque YAML interno. Resultado:

```json
{
  "slides_count": 5,
  "fotos_necesarias_de_carpeta": {
    "slide_1": "la creadora caminando en escenario amplio, plano general",
    "slide_2": "la creadora en escritorio con laptop",
    ...
  },
  "elementos_a_generar": {
    "slide_2": "captura de calendario lleno de sesiones",
    "slide_4": "mockup de un GPT con interfaz de OpenAI"
  },
  "estilo_textos": "instagram-stories-native"
}
```

### 4. Briefing visual general (paleta + capturas)

Bajo `## 🎨 Briefing visual general`. Capturar:
- `mood` (línea bajo `**Mood:**`)
- `paleta_dominante` (lista bajo `**Paleta dominante:**`)
- `capturas_a_preparar` (lista bajo `**Capturas/mockups a preparar:**`)
- `sesiones_grabacion` (lista bajo `**Sesiones de grabación recomendadas:**`)

---

## SI EL .MD ESTÁ MALFORMED

Si falta algún bloque crítico (`Frontmatter`, `Tabla`, `Bloque ⚙️`):

1. Mostrar al usuario qué bloque falta
2. Sugerir regenerar con `guionizacion-historias-formula100k`
3. Abortar (no intentar inferir — riesgo de output basura)

Si falta solo el bloque ⚙️ (guion legacy):

1. Inferir `fotos_necesarias_de_carpeta` del campo "Qué grabar/buscar" de cada slide
2. Inferir `elementos_a_generar` del campo "Capa visual" cuando mencione "mockup", "captura", "dashboard"
3. Notificar al usuario: "El guion no tiene bloque ⚙️ explícito, lo inferí del contenido. Verifica antes de generar."

---

## CACHE

Guardar el guion parseado en memoria de la sesión actual con clave:
```
hash(file_path + last_modified)
```

Para que si el usuario pide "regenera solo el slide 3", no haya que parsear todo de nuevo.

---

## EJEMPLO REAL DE PARSER

Input: `guiones/historias/2026-05-06_lead-magnet_gpt-primer-segundo.md`

Output esperado:

```json
{
  "metadata": {
    "titulo": "GPT del Primer Segundo — Lead Magnet",
    "categoria": "lead-magnet",
    "estructura": "#9 — Algo me ha sorprendido",
    "palabra_clave_cta": "GPT",
    "slides_count": 5,
    "mood": "viaje + autoridad + cercanía"
  },
  "slides": [
    { "n": 1, "frase": "Yo en la mañana", "formato_emoji": "🎥", "formato_codigo": "F2", ...},
    { "n": 2, "frase": "Yo en la noche", "formato_emoji": "📸", "formato_codigo": "F4", ...},
    ...
  ],
  "para_skill_c": {
    "fotos_necesarias_de_carpeta": {...},
    "elementos_a_generar": {...}
  }
}
```
