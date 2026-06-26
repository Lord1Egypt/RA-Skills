# AI Code Reviewer Skill

Skill para que un agente de IA realice code reviews profesionales, consistentes
y accionables. Diseñado para integrarse con flujos de trabajo de Pull Requests
en cualquier plataforma (GitHub, GitLab, Bitbucket, Azure DevOps).

---

## ¿Qué es esto?

Es un conjunto de reglas, templates y ejemplos que le enseñan a una IA a hacer
code reviews como lo haría un senior developer experimentado. La IA analiza
código y genera comentarios categorizados por severidad, con explicaciones
claras y sugerencias de solución.

---

## Estructura del Proyecto

  ai-code-reviewer/
  ├── SKILL.md                         # Instrucciones principales para la IA
  ├── README.md                        # Este archivo
  ├── references/                           # Reglas de revisión por categoría
  │   ├── general.md                   # Buenas prácticas generales
  │   ├── security.md                  # Seguridad y vulnerabilidades
  │   ├── javascript-typescript.md     # Reglas específicas JS/TS
  │   ├── nodejs.md                    # Reglas específicas Node.js
  │   ├── php.md                       # Reglas específicas PHP
  │   ├── python.md                    # Reglas específicas Python
  │   ├── css-html.md                  # Reglas específicas CSS/HTML
  │   └── team-conventions.md          # Convenciones de equipo (personalizable)
  └── assets/                       # Templates para los comentarios
      ├── review-comment.md            # Formato de comentarios individuales
      └── review-summary.md           # Formato del resumen del review

---

## Niveles de Severidad

Los hallazgos se clasifican en 4 niveles:

  BLOCKER  🔴  Bugs, vulnerabilidades, pérdida de datos    → Debe fijarse antes del merge
  WARNING  🟡  Code smells, complejidad, malas prácticas   → Debería fijarse
  SUGGEST  🔵  Mejoras de legibilidad, estructura          → Considerar
  NIT      💡  Estilo, preferencias, detalles menores      → Opcional

---

## Cómo Usar

### 1. Configuración Inicial

Clonar o copiar esta estructura en tu proyecto o en la configuración
de tu agente de IA.

### 2. Personalizar Convenciones de Equipo

Editar rules/team-conventions.md para ajustarlo a tu equipo:

  - Elegir el patrón de arquitectura (por capas, por features, hexagonal)
  - Definir el idioma del código y comentarios
  - Establecer la cobertura mínima de tests
  - Configurar las convenciones de commits
  - Definir los ambientes del proyecto
  - Listar las herramientas del equipo (linter, formatter, CI/CD)

### 3. Integrar con tu Flujo de Trabajo

#### Opción A: Prompt Directo

Pasar el contenido de SKILL.md como system prompt y el diff del PR
como user prompt:

  System: [contenido de SKILL.md]
  User: Revisa el siguiente Pull Request:
        Título: feat(auth): add JWT refresh token
        Descripción: Implementa rotación de refresh tokens
        Diff:
        [diff del PR]

#### Opción B: GitHub Action

Crear un workflow que se ejecute en cada PR:

  # .github/workflows/ai-code-review.yml
  name: AI Code Review
  on:
    pull_request:
      types: [opened, synchronize]

  jobs:
    review:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Run AI Review
          # Configurar según tu agente/proveedor de IA
          # El agente debe recibir SKILL.md + rules/ + diff del PR

#### Opción C: GitLab CI

  # .gitlab-ci.yml
  ai-review:
    stage: review
    only:
      - merge_requests
    script:
      # Configurar según tu agente/proveedor de IA

#### Opción D: Hook de Pre-push

Para revisión local antes de subir cambios:

  # .husky/pre-push
  # Ejecutar el agente de IA con los cambios staged
  # Útil para catch temprano de blockers

---

## Qué Revisa

### Reglas Generales (rules/general.md)
  - Naming y legibilidad
  - Complejidad ciclomática y nesting
  - DRY (Don't Repeat Yourself)
  - Error handling
  - Funciones puras y side effects
  - Código muerto e imports no utilizados
  - Documentación y comentarios

### Seguridad (rules/security.md)
  - SQL Injection
  - XSS (Cross-Site Scripting)
  - CSRF (Cross-Site Request Forgery)
  - Secrets y credenciales hardcodeadas
  - Autenticación y autorización
  - Validación de input
  - Manejo de datos sensibles
  - Configuración de CORS y headers
  - Dependencias con vulnerabilidades conocidas

### JavaScript / TypeScript (rules/javascript-typescript.md)
  - Uso correcto de tipos en TypeScript
  - Manejo de async/await y promesas
  - Inmutabilidad y manejo de estado
  - Comparaciones estrictas
  - Closures y memory leaks
  - Patrones específicos del lenguaje

### Node.js (rules/nodejs.md)
  - Seguridad del servidor
  - Manejo de variables de entorno
  - Streaming y manejo de archivos
  - Graceful shutdown
  - Event loop y operaciones bloqueantes
  - Manejo de dependencias

### PHP (rules/php.md)
  - Tipado estricto y type hints
  - Seguridad específica de PHP
  - Uso moderno del lenguaje (8.x+)
  - Manejo de errores y excepciones
  - Patrones y convenciones PSR

### Python (rules/python.md)
  - Tipado con type hints
  - Patrones pythónicos
  - Manejo de recursos y context managers
  - Seguridad y validación
  - Estructura y convenciones PEP

### CSS / HTML (rules/css-html.md)
  - Accesibilidad (a11y)
  - Semántica HTML
  - Performance de CSS
  - Responsive design
  - Seguridad en HTML

---

## Formato de Salida

### Comentarios Individuales

Cada hallazgo sigue el formato definido en assets/review-comment.md:

  🔴 Seguridad: SQL Injection en búsqueda de usuarios

  Archivo: src/repositories/user.repository.ts líneas 45-48

  Hallazgo:
  Descripción del problema encontrado.

  Por qué importa:
  Impacto y riesgo del problema.

  Sugerencia:
  Código o pasos para resolverlo.

  Referencia:
  Regla o estándar que respalda el comentario.

### Resumen del Review

Al final se genera un resumen siguiendo assets/review-summary.md:

  - Veredicto general (🔴 / 🟡 / 🟢)
  - Tabla de estadísticas por severidad
  - Lista de hallazgos críticos
  - Resumen de warnings, suggestions y nits
  - Lo positivo del PR
  - Tabla de archivos revisados

---

## Personalización

### Agregar Reglas para Otro Lenguaje

  1. Crear un nuevo archivo en rules/, por ejemplo rules/go.md
  2. Seguir la misma estructura de severidades:
     - 🔴 BLOCKERS
     - 🟡 WARNINGS
     - 🔵 SUGGESTIONS
     - 💡 NITS
  3. Referenciar el archivo en SKILL.md

### Modificar Severidades

Si tu equipo considera que algo clasificado como WARNING debería ser
BLOCKER (o viceversa), editar el archivo de reglas correspondiente
y mover la regla a la sección apropiada.

### Agregar Reglas de Negocio

Para reglas específicas de tu dominio, agregarlas en
rules/team-conventions.md o crear un archivo dedicado como
rules/business-rules.md.

Ejemplos:
  - "Todo endpoint que modifique datos financieros debe tener audit log"
  - "Los precios siempre se manejan en centavos (integer), nunca en decimales"
  - "Los emails transaccionales deben pasar por el servicio de templates"

---

## Principios de Diseño

### Consistencia
  Todos los reviews siguen el mismo formato y criterios, sin importar
  quién (o qué) haga el review.

### Accionabilidad
  Cada comentario incluye una sugerencia concreta de cómo resolver el
  problema. No se señalan problemas sin ofrecer solución.

### Proporcionalidad
  La severidad es proporcional al impacto real. No todo es un blocker.
  Los nits se marcan como nits.

### Respeto
  El tono es constructivo y profesional. Se critica el código, no a la
  persona. Se reconoce lo que está bien hecho.

### Educación
  Cada comentario explica el "por qué" detrás de la regla, no solo el
  "qué". El objetivo es que el equipo aprenda y mejore.

---

## Limitaciones

  - La IA no ejecuta el código, analiza estáticamente
  - No reemplaza tests automatizados, linters ni SAST tools
  - No tiene contexto completo del proyecto (solo ve el diff y archivos
    proporcionados)
  - Puede generar falsos positivos; el criterio humano es la decisión final
  - No verifica que el código compile o pase tests
  - Las reglas de negocio específicas deben configurarse manualmente

---

## Complementar Con

Esta skill funciona mejor cuando se combina con:

  ESLint / Pylint / PHPStan     Linting automático
  Prettier / Black              Formateo automático
  SonarQube / CodeClimate       Análisis estático profundo
  Snyk / Dependabot             Vulnerabilidades en dependencias
  Jest / Pytest / PHPUnit       Tests automatizados
  Husky / pre-commit            Hooks de pre-commit

La IA se enfoca en lo que las herramientas automáticas NO cubren bien:
lógica de negocio, arquitectura, naming, legibilidad, patrones y
contexto semántico del código.

---

## Contribuir

Para mejorar esta skill:

  1. Agregar nuevos patrones a examples/good-code.md o examples/bad-code.md
  2. Refinar reglas existentes en rules/
  3. Agregar reglas para nuevos lenguajes
  4. Mejorar los templates de comentarios
  5. Reportar falsos positivos o reglas faltantes

---

## Licencia

Uso interno del equipo. Adaptar según las necesidades del proyecto.