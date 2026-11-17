# FORMATO EXACTO DEL ARCHIVO DE OUTPUT

La skill `guionizacion-historias-formula100k` debe guardar SIEMPRE el output en este formato exacto.
La skill `historias-a-imagenes-nanobanana` lo va a parsear, así que la estructura es contrato.

---

## NOMBRE DEL ARCHIVO

```
[YYYY-MM-DD]_[categoria-slug]_[tema-slug-3-palabras].md
```

- `categoria-slug`: uno de `urgencia`, `one-shot`, `lead-magnet`, `libre`, `encuestas`
- `tema-slug-3-palabras`: kebab-case, máximo 3 palabras descriptivas

Ejemplos válidos:
- `2026-05-06_lead-magnet_gpt-primer-segundo.md`
- `2026-05-07_one-shot_caso-brenda-39-sesiones.md`
- `2026-05-09_urgencia_ultimo-dia-banco-historias.md`

Ruta completa: `guiones/historias/[NOMBRE].md`

---

## ESTRUCTURA DEL ARCHIVO

````markdown
---
titulo: [Título descriptivo de la secuencia]
fecha: [YYYY-MM-DD]
categoria: [urgencia | one-shot | lead-magnet | libre | encuestas]
estructura: [#X — Nombre de la estructura]
objetivo: [vender X | captar leads para Y | etc.]
palabra_clave_cta: [PALABRA en mayúsculas]
slides: [3-6]
mood: [breve frase mood, ej: "viaje + autoridad + cercanía"]
---

# [Título de la secuencia]

> **Categoría:** [emoji + nombre]
> **Estructura usada:** #[X] — [Nombre]
> **Objetivo:** [una línea]
> **CTA:** Responde **[PALABRA]** y te [acción]

---

## 📋 Tabla slide-by-slide

| # | Frase principal | Capa visual | Formato | Qué grabar/buscar | Briefing de diseño |
|---|---|---|---|---|---|
| 1 | "[Frase del slide 1]" | [descripción de la capa 2] | 🎥 F[X] [Nombre formato] | [instrucción de grabación] | Fondo: [...]; Cajas: [...]; Elementos: [...]; Highlight: [...] |
| 2 | "[Frase del slide 2]" | [...] | 📸 F[X] | [...] | [...] |
| ... | ... | ... | ... | ... | ... |

---

## 🎨 Briefing visual general

**Mood:** [una frase]

**Paleta dominante:**
- Cajas principales: [blancas / negras / amarillas / verdes / rojas]
- Highlights: [amarillo + verde / rojo + verde / etc.]
- Elementos: [flechas amarillas / X rojas / ✓ verdes / globos / etc.]

**Capturas/mockups a preparar:**
1. [Captura de X — formato]
2. [Mockup del producto Y — donde conseguirlo]
3. [Screenshot de Z]

**Sesiones de grabación recomendadas:**
- Sesión A — [escenario]: graba [N] clips para slides [#, #, #]
- Sesión B — [escenario]: graba [N] clips para slides [#, #]

---

## 📝 Notas de producción

- [Nota 1: ej. "El slide 3 puede grabarse en el mismo escenario del slide 1 si haces un giro de cámara"]
- [Nota 2: ej. "Para slide 4 necesitas captura del dashboard del Banco de Historias — pídela a quien la tenga si no la tienes"]
- [Nota 3: ej. "Si no tienes mockup del GPT, abre el GPT en pantalla completa y graba un screen recording de 5s"]

---

## 🔁 Variantes opcionales (A/B test)

Si quieres testear, aquí hay 2 variantes del slide 1 (gancho):

- **Versión A (curiosidad):** "[frase A]"
- **Versión B (urgencia):** "[frase B]"

---

## ⚙️ Para la skill `historias-a-imagenes-nanobanana`

```yaml
slides_count: [N]
fotos_necesarias_de_carpeta:
  - slide_1: [descripción de la foto a buscar — ej: "la creadora caminando en escenario amplio, plano general"]
  - slide_2: [...]
  - slide_3: [...]
  - slide_4: [...]
  - slide_5: [...]
elementos_a_generar:
  - slide_2: "captura de calendario lleno de sesiones"
  - slide_4: "mockup de un GPT con interfaz de OpenAI"
estilo_textos: instagram-stories-native
```
````

---

## REGLAS PARA GENERAR EL OUTPUT

1. **Frontmatter YAML siempre presente** — la skill C lo usa para detectar metadatos.
2. **Tabla slide-by-slide siempre con 6 columnas** — no agregar ni quitar columnas.
3. **El bloque `## ⚙️ Para la skill historias-a-imagenes-nanobanana`** es OBLIGATORIO. Sin él, la skill C no puede procesar.
4. **Las frases entre comillas dobles** "..." (no comillas tipográficas) en la tabla — el parser las espera así.
5. **El emoji del formato** (🎥 / 📸) va al inicio de la celda Formato, antes de F[X].
6. **`palabra_clave_cta`** siempre en MAYÚSCULAS sin tildes.
7. **No usar tabs en la tabla**, solo espacios + pipes.
8. **Si la secuencia es de URGENCIA**, el bloque "Notas de producción" debe incluir explícitamente la consecuencia real (deadline, eliminación, cambio de precio).
