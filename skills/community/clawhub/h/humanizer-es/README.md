# Humanizer-es: herramienta para humanizar textos generados por IA en español

> **Aviso**
>
> * Los archivos principales de este proyecto están adaptados a partir de [blader/humanizer](https://github.com/blader/humanizer/tree/main)
> * La parte de utilidades prácticas (reglas clave, lista rápida de verificación y puntuación de calidad) toma como referencia [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
> * El proyecto original se inspira en la guía de Wikipedia [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

---

## Descripción

**Humanizer-es** es una skill pensada para revisar y reescribir textos generados por IA en español, con el objetivo de que suenen más naturales, precisos y humanos.

No se limita a “cambiar palabras”: ayuda a detectar patrones típicos de escritura artificial y a sustituirlos por una redacción más creíble, concreta y fluida.

Este proyecto puede servirte para:

* editar y revisar contenido generado por IA
* mejorar la naturalidad de artículos, posts, emails o textos académicos
* aprender a identificar patrones frecuentes de escritura artificial
* entrenar un mejor criterio de edición en español

---

## Instalación

### Opción 1: instalación con `npx` (recomendada)

```bash
npx skills add https://github.com/mattc95/Humanizer-es.git
```

Es la forma más sencilla. La skill se instalará automáticamente en la ruta correcta.

### Opción 2: clonar con Git

```bash
# Clonar en el directorio de skills de Claude Code
git clone https://github.com/mattc95/Humanizer-es.git ~/.claude/skills/humanizer-es
```

### Opción 3: instalación manual

1. Descarga este proyecto en ZIP o clónalo en tu equipo

2. Copia la carpeta `Humanizer-es` en el directorio de skills de Claude Code:

   * **macOS/Linux**: `~/.claude/skills/`
   * **Windows**: `%USERPROFILE%\.claude\skills\`

3. Asegúrate de que la estructura quede así:

```text
~/.claude/skills/humanizer-es/
├── SKILL.md       # Definición de la skill
└── README.md      # Documentación
```

---

## Verificar la instalación

Reinicia Claude Code o vuelve a cargar las skills y escribe:

```text
/humanizer-es
```

Si la instalación se ha realizado correctamente, la skill quedará disponible.

---

## Uso

### Uso básico

Puedes usar Humanizer-es de varias formas dentro de Claude Code.

### 1. Invocar la skill directamente

```text
/humanizer-es Ayúdame a humanizar el siguiente texto:

[pega aquí tu texto]
```

### 2. Usarlo dentro de una conversación

```text
Usa humanizer para reescribir este párrafo y hacer que suene más natural:

Este proyecto representa nuestro firme compromiso con la innovación. Además, pone de manifiesto nuestro papel esencial dentro de un ecosistema tecnológico en constante evolución.
```

### 3. Aplicarlo a un archivo

```text
/humanizer-es Humaniza el contenido del archivo article.md
```

---

## Ejemplos de uso

### Caso 1: reescritura de copy de marketing

**Entrada**

```text
/humanizer-es
Ubicado en el corazón histórico de Madrid, este restaurante ofrece una experiencia gastronómica única, inmersiva y vibrante. Su propuesta se posiciona como un referente dentro del panorama culinario contemporáneo.
```

**Salida esperada**

> Este restaurante está en el centro de Madrid y se ha hecho conocido por su carta de temporada y su enfoque en cocina tradicional con un toque actual.

---

### Caso 2: reescritura de un resumen académico

**Entrada**

```text
/humanizer-es
Este estudio analiza en profundidad el papel transformador de la inteligencia artificial en el diagnóstico clínico, destacando su relevancia dentro del cambiante entorno sanitario actual. Asimismo, establece una base sólida para futuras investigaciones en este ámbito.
```

**Salida esperada**

> Este estudio examina el uso de modelos de IA en el diagnóstico clínico, con foco en la detección temprana de enfermedades respiratorias. El análisis se basa en datos hospitalarios recogidos entre 2020 y 2024.

---

### Caso 3: reescritura de una introducción para blog

**Entrada**

```text
/humanizer-es
La inteligencia artificial no es solo una herramienta tecnológica, sino una revolución que redefine la manera en que entendemos el futuro del trabajo. Expertos de la industria coinciden en que su impacto será profundo y duradero.
```

**Salida esperada**

> Cada vez es más evidente que la IA está cambiando la forma en que trabajamos. En algunos casos ahorra tiempo; en otros, obliga a replantear tareas que antes parecían intocables. El cambio ya está aquí, aunque todavía no siempre sepamos qué hacer con él.

---

## Qué detecta esta skill

Humanizer-es puede identificar y corregir **24 patrones frecuentes** de escritura generada por IA, agrupados en cuatro categorías.

### 📝 Patrones de contenido

1. Énfasis excesivo en la importancia, el legado o las grandes tendencias
2. Énfasis excesivo en la notoriedad o la cobertura mediática
3. Análisis superficiales con apariencia elaborada
4. Lenguaje promocional o publicitario
5. Atribuciones vagas y formulaciones imprecisas
6. Secciones típicas de “retos y perspectivas futuras”

### 🔤 Patrones lingüísticos y gramaticales

7. Uso excesivo de vocabulario típico de IA
8. Evasión innecesaria del verbo “ser”
9. Paralelismos negativos del tipo “no solo…, sino también…”
10. Uso excesivo de la regla de tres
11. Sustitución artificial de sinónimos
12. Generalizaciones o alcances falsos

### 🎨 Patrones de estilo

13. Uso excesivo de guiones largos
14. Uso excesivo de negritas
15. Listas con títulos incrustados en la línea
16. Encabezados en estilo Title Case
17. Emojis fuera de lugar
18. Comillas tipográficas innecesarias

### 💬 Patrones comunicativos y muletillas

19. Rastros de tono colaborativo artificial
20. Avisos innecesarios sobre la fecha límite de conocimiento
21. Tono adulador o servil
22. Frases de relleno
23. Exceso de matizaciones
24. Conclusiones genéricas y excesivamente optimistas

---

## Estructura del proyecto

* **`SKILL.md`** - definición de la skill
* **`README.md`** - documentación del proyecto

**Nota:** si quieres consultar la versión original en inglés, revisa [blader/humanizer](https://github.com/blader/humanizer)

---

## Uso manual

### Flujo recomendado

1. **Detectar patrones de IA** revisando el texto con apoyo de `SKILL.md`
2. **Reescribir los fragmentos problemáticos** con expresiones más naturales
3. **Conservar el sentido original** sin perder información importante
4. **Mantener el tono adecuado** según el tipo de texto
5. **Introducir una voz real** para que el resultado no suene mecánico

---

## Principios clave

### ✨ No basta con que el texto esté “limpio”; también debe sonar vivo

Eliminar patrones de IA es solo el primer paso. Un texto convincente necesita una voz humana real.

* **Ten criterio**: no te limites a repetir ideas; toma posición cuando haga falta
* **Varía el ritmo**: mezcla frases más cortas y más largas
* **Reconoce la complejidad**: no todo tiene que sonar cerrado o rotundo
* **Usa la primera persona cuando tenga sentido**: a veces hace el texto más honesto
* **Evita la perfección artificial**: una estructura demasiado impecable puede sonar falsa
* **Sé concreto**: los detalles específicos suelen funcionar mejor que las abstracciones

### Antes y después

**Antes (con tono artificial)**

> La nueva actualización del software representa una prueba clara del compromiso de la empresa con la innovación. Además, ofrece una experiencia fluida, intuitiva y potente que permite a los usuarios alcanzar sus objetivos con máxima eficiencia. No se trata solo de una mejora, sino de una revolución en la productividad digital.

**Después (más humano)**

> La actualización añade atajos de teclado, modo sin conexión y una mejor gestión de archivos. En las pruebas internas, la mayoría de los usuarios terminó las tareas en menos tiempo y con menos errores.

**Qué cambia**

* se elimina el simbolismo exagerado
* se reduce el vocabulario inflado
* se quita la regla de tres artificial
* se reemplaza la retórica grandilocuente por información concreta
* se añaden detalles verificables

---

## Vocabulario de alerta

Estas palabras y expresiones aparecen con demasiada frecuencia en textos generados por IA y conviene revisarlas con cuidado:

* además
* crucial
* profundizar en
* destacar
* duradero
* potenciar
* fomentar
* obtener
* poner de relieve
* interacción
* complejidad
* panorama
* clave
* demostrar
* prueba de
* subrayar
* valioso
* vibrante

No significa que siempre deban eliminarse, pero sí que conviene comprobar si realmente aportan algo.

---

## Contribuciones

Si encuentras errores, problemas de traducción o quieres mejorar esta documentación, puedes abrir un **Issue** o enviar un **Pull Request**.

### Adaptación al español

Durante la adaptación de este proyecto se tuvieron en cuenta varias cuestiones propias del español:

* algunos patrones del inglés no funcionan igual en español
* ciertos ejemplos se reescribieron para encajar mejor en contextos hispanohablantes
* se ajustó el tono para que la documentación sonara más natural en español

---

## Recursos de referencia

* [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) - guía original
* [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup) - proyecto de limpieza de IA en Wikipedia
* [blader/humanizer](https://github.com/blader/humanizer) - proyecto original en inglés
* [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) - referencia para la parte práctica

---

## Licencia

Este proyecto de traducción y adaptación sigue la licencia del proyecto original. Su contenido principal se basa en observaciones y síntesis desarrolladas por la comunidad de Wikipedia.

---

**Nota final:** esta herramienta no está pensada para “engañar” detectores de IA, sino para mejorar de verdad la calidad de los textos. La mejor forma de humanizar una redacción es aportar pensamiento real, criterio propio y una voz auténtica.
