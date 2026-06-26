---
name: imagen
description: Genera imágenes con calidad cheap, medium, good o top usando OpenRouter y la configuración activa de OpenClaw. Guarda los archivos en el workspace actual del agente, por defecto en ./skills/imagen/out.
user-invocable: true
metadata: {"openclaw":{"emoji":"🖼️","requires":{"bins":["python3"],"config":["agents.defaults.imageModel.primary"]},"primaryEnv":"OPENROUTER_API_KEY"}}
---

# Imagen

Usa esta skill cuando el usuario pida generar una imagen, ilustración, render, retrato, escena o composición visual.

## Regla principal

Cuando el usuario use `/imagen`, eso es una orden directa para generar una imagen.

No intentes:

- usar una tool llamada `imagen`
- usar `openclaw skills invoke`
- usar `openclaw imagen`
- ejecutar `SKILL.md`
- inspeccionar logs
- depurar
- usar `journalctl`
- inventar comandos CLI
- tratar esta skill como si fuera una tool
- responder con explicaciones sobre cómo invocarla

Tu trabajo es:

1. decidir la calidad correcta
2. extraer el prompt limpio
3. extraer tamaño y formato si el usuario los indica
4. inferir tamaño y formato si el usuario da una resolución exacta
5. ejecutar el script de generación
6. devolver el resultado final en la misma respuesta al usuario

## Ejecución directa (obligatoria)

- Si el usuario usa `/imagen` o pide generar una imagen, ejecuta directamente el comando base de esta skill.
- Ejecuta una sola llamada directa al script (sin `python3` delante):
  - `{baseDir}/scripts/gen_openrouter.py ...`
- No intentes leer, listar o buscar `SKILL.md` con `read`, `ls`, `find` o rutas tipo `~/.openclaw/...`.
- No hagas comandos previos de verificación (`ls`, `cat`, `find`, `test`, `stat`, `which`).
- No pidas confirmación para "usar la skill"; úsala directamente.
- Solo informa que la skill no está disponible si la ejecución devuelve un error real de script no encontrado (`ENOENT`).
- No intentes escribir ni mover archivos a `/workspace/media/outbound` ni usar adjuntos automáticos.

## Ejecución obligatoria

Esta skill debe usar siempre este script base:

    {baseDir}/scripts/gen_openrouter.py --quality <cheap|medium|good|top> --prompt "<prompt>" --workspace-dir . --timeout 300

Debes usar `--workspace-dir .` y `--timeout 300` de forma explícita.

`--workspace-dir .` hace que el script use el workspace actual del agente como raíz de salida.

Añade `--size` solo si el usuario especifica:

- `1K`
- `2K`
- `4K`
- o una resolución exacta tipo `1920x1080`

Añade `--aspect-ratio` solo si el usuario especifica:

- `1:1`
- `2:3`
- `3:2`
- `3:4`
- `4:3`
- `4:5`
- `5:4`
- `9:16`
- `16:9`
- `21:9`

Si el usuario no especifica tamaño, ratio ni resolución exacta, no envíes ninguno de esos parámetros. Deja que el modelo/proveedor use sus valores por defecto.

No uses otras rutas de salida.
No inventes otras herramientas.
No cambies el timeout salvo que el usuario lo pida expresamente.
No guardes la imagen dentro de la carpeta física compartida de la skill.
La salida debe quedar dentro del workspace actual del agente.
Ruta por defecto:

    ./skills/imagen/out

No uses la carpeta global compartida de skills fuera del workspace.

y `.` significa el workspace actual del agente.

## Cómo decidir la calidad

### Formatos aceptados

Acepta:

- `/imagen <prompt>`
- `/imagen cheap <prompt>`
- `/imagen medium <prompt>`
- `/imagen good <prompt>`
- `/imagen top <prompt>`

También acepta que el usuario combine calidad, tamaño y ratio en cualquier orden razonable, por ejemplo:

- `/imagen good 2K 16:9 un coche futurista en una autopista`
- `/imagen 4K 1:1 un retrato de un samurái`
- `/imagen top 1920x1080 una ciudad cyberpunk al amanecer`

### Reglas de extracción

1. Si aparece una calidad explícita (`cheap`, `medium`, `good`, `top`), úsala.
2. Si aparece un tamaño explícito (`1K`, `2K`, `4K`), úsalo.
3. Si aparece un ratio explícito (`1:1`, `16:9`, `4:3`, `3:2`, `9:16`, `21:9`, `2:3`, `3:4`, `4:5`, `5:4`), úsalo.
4. Si el usuario da una resolución exacta tipo `1920x1080`, `1024x1024`, `2048x2048` o similar:
   - deduce el ratio más cercano
   - deduce el tamaño aproximado
5. Todo lo que no sea calidad, tamaño o ratio debe considerarse parte del prompt.
6. Si no hay pista de calidad, usa las reglas automáticas.
7. Si no hay pista de tamaño, no envíes `--size`.
8. Si no hay pista de ratio, no envíes `--aspect-ratio`.

### Normalización de niveles

Interpreta también estas variantes:

- barato, low, baja → cheap
- medio, balanced, normal, intermedio → medium
- bueno, mejor, pro, quality, good → good
- premium, máxima calidad, max, top, ultra → top

## Reglas automáticas de calidad cuando no se especifica

Estas reglas se aplican tanto a `/imagen <prompt>` sin nivel explícito como a peticiones en lenguaje natural.

### Usa `cheap` cuando:

- el usuario solo pide una imagen sin pedir mejora especial
- la petición es casual, rápida o genérica
- no hay señales de que quiera gran realismo, mucho detalle o máxima calidad

Ejemplos:
- `/imagen un gato samurái`
- `genérame una imagen de una cabaña en el bosque`
- `hazme una imagen de un perro astronauta`

### Usa `medium` cuando:

- el usuario pide una mejora moderada pero no alta
- menciona “un poco mejor”, “algo mejor”, “más detalle”, “más cuidado”
- parece querer algo mejor que cheap sin pedir calidad claramente alta

Ejemplos:
- `/imagen una ciudad futurista con más detalle`
- `hazme una imagen un poco mejor de una casa junto al lago`
- `genera una imagen más cuidada de una moto retro`

### Usa `good` cuando:

- el usuario pide claramente una mejora visible
- menciona “mejor”, “más realista”, “hazlo mejor”, “mejóralo”, “más pro”
- quiere un resultado claramente superior, pero no necesariamente el más caro

Ejemplos:
- `/imagen un retrato más realista de una violinista bajo lluvia neón`
- `genérame una imagen mejor de un castillo flotante`
- `hazme una imagen más pro de un dragón sobre una montaña`

### Usa `top` cuando:

- el usuario pide explícitamente la máxima calidad
- menciona “top”, “premium”, “máxima calidad”, “la mejor calidad”, “ultra”
- quiere un resultado premium, cinematográfico o lo mejor posible

Ejemplos:
- `/imagen top un dragón cinematográfico sobre una ciudad futurista al amanecer`
- `quiero una imagen con máxima calidad de una nave espacial orgánica`
- `hazme la mejor versión posible de un retrato hiperrealista`

## Cómo decidir tamaño y formato

OpenRouter usa estos parámetros:

- `image_size`: `1K`, `2K`, `4K`
- `aspect_ratio`: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### Si el usuario especifica tamaño

Respétalo.

Ejemplos:
- `1K`
- `2K`
- `4K`

### Si el usuario especifica ratio

Respétalo.

Ejemplos:
- `1:1`
- `16:9`
- `4:3`
- `3:2`
- `9:16`
- `21:9`

### Si el usuario especifica resolución exacta

Si el usuario da una resolución exacta tipo `ancho x alto`, por ejemplo:

- `1024x1024`
- `1920x1080`
- `2048x2048`
- `1536x1024`
- `768x1344`

haz lo siguiente:

1. Calcula el ratio más cercano entre los ratios soportados.
2. Calcula el tamaño aproximado:
   - si la resolución es cercana a una base de 1K, usa `1K`
   - si es claramente mayor y encaja mejor con 2K, usa `2K`
   - si es claramente muy alta y encaja mejor con 4K, usa `4K`
3. Si el ratio exacto no está soportado, usa el ratio soportado más cercano.
4. Si el usuario da una resolución exacta pero también da un ratio explícito, el ratio explícito manda.
5. Si el usuario da una resolución exacta pero también da un tamaño explícito, el tamaño explícito manda.

### Valores por defecto

Si el usuario no especifica nada:

- no envíes `image_size`
- no envíes `aspect_ratio`

Deja que el modelo/proveedor use sus valores por defecto.

## Uso en lenguaje natural

Si el usuario pide una imagen sin slash command, aplica estas reglas:

- sin pista de calidad → cheap
- “un poco mejor”, “algo mejor”, “más detalle”, “más cuidado” → medium
- “mejor”, “más realista”, “hazlo mejor”, “mejóralo”, “más pro” → good
- “máxima calidad”, “premium”, “top”, “la mejor calidad”, “ultra”, “cinematográfico” → top

Además:

- si menciona `1K`, `2K` o `4K`, usa ese tamaño
- si menciona `1:1`, `16:9`, `4:3`, `3:2`, `9:16`, `21:9`, usa ese ratio
- si menciona una resolución exacta, infiere ratio y tamaño automáticamente
- si no dice nada sobre tamaño o formato, no envíes esos parámetros y deja que el modelo/proveedor use el comportamiento por defecto

## Qué hace el script

El script:

1. lee `~/.openclaw/openclaw.json`
2. toma `agents.defaults.imageModel.primary` y `fallbacks`
3. resuelve los niveles así:
   - cheap → primary
   - medium → fallback 1 si existe, si no primary
   - good → fallback 2 si existe, si no fallback 1, si no primary
   - top → fallback 3 si existe, si no fallback 2, si no fallback 1, si no primary
4. lee la API key de OpenRouter
5. genera la imagen con OpenRouter
6. guarda el resultado dentro del workspace actual del agente
7. por defecto guarda en:
   - `skills/imagen/out`
8. devuelve por stdout:
   - quality
   - model
   - output_file
   - image_size si se usó
   - aspect_ratio si se usó
   - workspace_dir
   - output_dir

## Uso obligatorio del script

Debes invocar el script con `exec`, con `--workspace-dir .` y con `--timeout 300`.

Ejemplo válido:

    {baseDir}/scripts/gen_openrouter.py --quality good --prompt "un perro astronauta tomando café" --workspace-dir . --timeout 300

Ejemplo válido:

    {baseDir}/scripts/gen_openrouter.py --quality medium --prompt "una ciudad futurista con más detalle" --workspace-dir . --size 2K --aspect-ratio 16:9 --timeout 300

Ejemplo válido:

    {baseDir}/scripts/gen_openrouter.py --quality top --prompt "un dragón cinematográfico sobre una ciudad futurista al amanecer" --workspace-dir . --size 4K --aspect-ratio 16:9 --timeout 300

## Reglas obligatorias

1. Si el usuario da una calidad explícita, respétala.
2. Si el usuario no da calidad explícita, usa las reglas automáticas anteriores.
3. No inventes más niveles aparte de `cheap`, `medium`, `good` y `top`.
4. Si el usuario da un tamaño explícito, respétalo.
5. Si el usuario da un ratio explícito, respétalo.
6. Si el usuario da una resolución exacta, infiere ratio y tamaño automáticamente.
7. Si el usuario no da tamaño, no envíes `--size`.
8. Si el usuario no da ratio, no envíes `--aspect-ratio`.
9. No cambies el modelo principal de chat.
10. No invoques otras skills.
11. No intentes usar una tool llamada `imagen`.
12. No uses CLI ni shell distintos del script indicado.
13. No digas que la skill no funciona salvo que el script falle realmente.
14. No respondas con explicaciones técnicas salvo que el usuario las pida.
15. No sustituyas el script por razonamiento o suposiciones.
16. No guardes la salida en `{baseDir}/out`.
17. La salida debe quedar en el workspace actual del agente.
18. Si necesitas una ruta explícita, usa siempre `--workspace-dir .`.
19. No derives la ruta de salida desde la carpeta física compartida de la skill.

## Respuesta al usuario

Si la generación funciona:

- no adjuntes ni muevas el archivo a `media/outbound`
- deja la imagen en `./skills/imagen/out/`
- devuelve una respuesta textual con la ruta final (`OUTPUT_FILE`) y un resumen breve
- la línea breve debe incluir:
  - calidad usada
  - modelo usado
  - tamaño usado si se usó
  - ratio usado si se usó

Formato recomendado:

- `Imagen generada (cheap · black-forest-labs/flux.2-klein-4b)`
- `Imagen generada (medium · sourceful/riverflow-v2-fast · 2K · 16:9)`
- `Imagen generada (good · black-forest-labs/flux.2-pro)`
- `Imagen generada (top · openai/gpt-5-image-mini · 4K · 16:9)`

Si la petición de imagen venía dentro de un mensaje con más cosas, la imagen debe ir con la respuesta normal en el mismo mensaje final, no como una respuesta separada sin contexto.

Ejemplo:
- si el usuario pide una imagen y además hace una pregunta, responde a la pregunta en esa misma respuesta final.

## Persistencia del archivo

- No borres la imagen generada automáticamente.
- Debe permanecer en `skills/imagen/out` del workspace actual del agente.

## Si falla

Si falla:

- responde breve
- no des trazas largas salvo que el usuario las pida
- formato recomendado:
  - `No he podido generar la imagen con ese nivel. Prueba otra vez o cambia de calidad.`

## Importante

- La selección de modelos debe salir siempre del config activo, no de valores hardcodeados.
- Si el usuario cambia los modelos en `openclaw.json`, esta skill debe seguir funcionando sin editarse.
- Esta skill no asume ninguna tool built-in de text-to-image.
- Esta skill no debe intentar descubrir cómo funciona OpenClaw.
- Esta skill debe limitarse a enrutar la petición al script correcto con la calidad, tamaño y ratio correctos.
- Si el usuario da una resolución exacta, conviértela a ratio y tamaño compatibles antes de llamar al script.
- La carpeta de salida no es la carpeta compartida de la skill.
- La carpeta de salida es el workspace actual del agente, por defecto en `skills/imagen/out`.
