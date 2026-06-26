# Convenciones de Equipo

Aplica a todos los archivos. Estas reglas son personalizables por cada equipo
y deben adaptarse al proyecto específico.

---

## Instrucciones de Personalización

Este archivo es una PLANTILLA. Cada equipo debe:
1. Copiar este archivo
2. Ajustar las convenciones a su stack y acuerdos
3. Eliminar secciones que no apliquen
4. Agregar convenciones específicas del proyecto

---

## 🔴 BLOCKERS (Definidos por el equipo)

### Branch Protection
- No hacer push directo a main/master
- No hacer merge sin al menos 1 aprobación de code review
- No hacer merge si el CI/CD pipeline está fallando
- No hacer merge si hay conversaciones de review sin resolver

### Versionamiento
- Seguir Semantic Versioning (SemVer): MAJOR.MINOR.PATCH
  - MAJOR: cambios que rompen compatibilidad (breaking changes)
  - MINOR: nueva funcionalidad compatible hacia atrás
  - PATCH: correcciones de bugs compatibles hacia atrás
- Toda API pública deprecada debe marcarse con @deprecated y fecha de remoción
- Breaking changes deben documentarse en CHANGELOG.md

### Migraciones de Base de Datos
- Toda migración debe tener su rollback correspondiente
- No modificar migraciones que ya se ejecutaron en producción
- Crear nueva migración para corregir errores en migraciones previas
- Migraciones deben ser idempotentes cuando sea posible
- No incluir datos de seed en migraciones de estructura

---

## 🟡 WARNINGS (Definidos por el equipo)

### Estilo de Código

#### Naming Conventions por Lenguaje
Adaptar según el stack del proyecto:

  | Elemento          | JavaScript/TS   | Python         | PHP            |
  |-------------------|-----------------|----------------|----------------|
  | Variables         | camelCase       | snake_case     | camelCase      |
  | Funciones         | camelCase       | snake_case     | camelCase      |
  | Clases            | PascalCase      | PascalCase     | PascalCase     |
  | Constantes        | UPPER_SNAKE     | UPPER_SNAKE    | UPPER_SNAKE    |
  | Archivos          | kebab-case      | snake_case     | PascalCase     |
  | Componentes (UI)  | PascalCase      | N/A            | N/A            |
  | CSS classes       | kebab-case o BEM| kebab-case     | kebab-case     |

#### Idioma del Código
Definir y mantener consistencia:

  - Código (variables, funciones, clases): [Inglés / Español] → ELEGIR UNO
  - Comentarios: [Inglés / Español] → ELEGIR UNO
  - Commits: [Inglés / Español] → ELEGIR UNO
  - Documentación: [Inglés / Español] → ELEGIR UNO
  - UI/UX (textos al usuario): Según mercado objetivo

  Recomendación: Código siempre en inglés. Comentarios y commits en el idioma
  que todo el equipo domine. Documentación en el idioma del equipo.

### Estructura de Proyecto

#### Patrón de Arquitectura
Definir el patrón que sigue el proyecto y respetarlo:

  Opción A - Por capas (Layer-based):
    src/
    ├── controllers/    # Manejo de HTTP requests/responses
    ├── services/       # Lógica de negocio
    ├── repositories/   # Acceso a datos
    ├── models/         # Definición de entidades
    ├── middlewares/     # Middleware de la aplicación
    ├── utils/          # Funciones utilitarias
    ├── config/         # Configuración
    └── types/          # Tipos e interfaces (TS)

  Opción B - Por features/módulos (Feature-based):
    src/
    ├── users/
    │   ├── users.controller.ts
    │   ├── users.service.ts
    │   ├── users.repository.ts
    │   ├── users.model.ts
    │   ├── users.routes.ts
    │   ├── users.validation.ts
    │   └── users.test.ts
    ├── orders/
    │   ├── orders.controller.ts
    │   └── ...
    └── shared/
        ├── middlewares/
        ├── utils/
        └── types/

  Opción C - Hexagonal / Clean Architecture:
    src/
    ├── domain/           # Entidades y reglas de negocio (sin dependencias externas)
    │   ├── entities/
    │   ├── value-objects/
    │   └── ports/        # Interfaces/contratos
    ├── application/      # Casos de uso / servicios de aplicación
    │   └── use-cases/
    ├── infrastructure/   # Implementaciones concretas
    │   ├── persistence/
    │   ├── http/
    │   └── messaging/
    └── presentation/     # Controllers, resolvers, CLI
        ├── rest/
        └── graphql/

### Convenciones de Commits
Seguir Conventional Commits:

  Formato: <type>(<scope>): <description>

  Tipos permitidos:
    feat:     Nueva funcionalidad
    fix:      Corrección de bug
    docs:     Solo cambios en documentación
    style:    Cambios de formato (no afectan lógica)
    refactor: Cambio de código que no agrega feature ni corrige bug
    perf:     Mejora de performance
    test:     Agregar o corregir tests
    build:    Cambios en build system o dependencias
    ci:       Cambios en configuración de CI/CD
    chore:    Tareas de mantenimiento

  Reglas:
    - Descripción en imperativo: "add feature" no "added feature"
    - Primera línea máximo 72 caracteres
    - Body opcional para explicar el "por qué" (no el "qué")
    - Footer para referencias: "Closes #123", "BREAKING CHANGE: ..."

  Ejemplos:
    feat(auth): add JWT refresh token rotation
    fix(orders): prevent duplicate charge on retry
    refactor(users): extract validation to dedicated service
    docs(api): update authentication endpoints documentation

### Pull Requests
- Título descriptivo siguiendo el formato de commits
- Descripción con:
  - Qué cambia y por qué
  - Cómo probar los cambios
  - Screenshots si hay cambios visuales
  - Referencia al ticket/issue
- PRs pequeños y enfocados: idealmente < 400 líneas de cambio
- No mezclar refactoring con features en el mismo PR
- Resolver todos los comentarios de review antes de merge
- Squash merge para mantener historial limpio (o merge commit si se prefiere)

### Testing
Definir los requisitos mínimos del equipo:

  Cobertura mínima: [70% / 80% / 90%] → ELEGIR
  
  Qué debe tener tests:
    - Lógica de negocio (services): SIEMPRE
    - Endpoints/Controllers: SIEMPRE
    - Funciones utilitarias: SIEMPRE
    - Modelos/Entidades con lógica: SIEMPRE
    - Componentes UI con lógica: SIEMPRE
    - Integraciones con servicios externos: SIEMPRE (con mocks)
  
  Qué puede no tener tests:
    - Archivos de configuración
    - Tipos/Interfaces (TS)
    - Modelos sin lógica (solo definición de campos)
    - Código generado automáticamente

  Convención de nombres para archivos de test:
    Opción A: archivo.test.ts / archivo.spec.ts (junto al archivo)
    Opción B: __tests__/archivo.test.ts (en carpeta separada)
    → ELEGIR UNO y ser consistente

### Manejo de Dependencias
- Fijar versiones exactas en producción o usar lock files
- Revisar changelogs antes de actualizar dependencias mayores
- No agregar dependencias para funcionalidad trivial
- Evaluar tamaño, mantenimiento y seguridad antes de agregar una dependencia
- Documentar por qué se eligió una dependencia no obvia
- Actualizar dependencias regularmente (al menos mensualmente para patches de seguridad)

---

## 🔵 SUGGESTIONS (Definidos por el equipo)

### Code Review Checklist
Al hacer review, verificar:

  Funcionalidad:
    □ ¿El código hace lo que el ticket/issue describe?
    □ ¿Se manejan los edge cases?
    □ ¿Se manejan los errores apropiadamente?

  Calidad:
    □ ¿El código es legible y mantenible?
    □ ¿Los nombres son claros y descriptivos?
    □ ¿Hay duplicación que debería extraerse?
    □ ¿La complejidad es apropiada?

  Seguridad:
    □ ¿Se valida el input del usuario?
    □ ¿No hay secrets hardcodeados?
    □ ¿Se manejan permisos/autorización?

  Testing:
    □ ¿Hay tests para la nueva funcionalidad?
    □ ¿Los tests cubren casos edge?
    □ ¿Los tests existentes siguen pasando?

  Documentación:
    □ ¿Se actualizó la documentación si es necesario?
    □ ¿Los cambios de API están documentados?
    □ ¿Hay comentarios para lógica no obvia?

### Environments
Definir los ambientes del proyecto:

  | Ambiente    | Branch    | Propósito                        | Datos          |
  |-------------|-----------|----------------------------------|----------------|
  | Local       | cualquier | Desarrollo individual            | Seeds/Fixtures |
  | Development | develop   | Integración del equipo           | Datos de prueba|
  | Staging     | release/* | QA y validación pre-producción   | Copia de prod  |
  | Production  | main      | Usuarios finales                 | Datos reales   |

### Feature Flags
- Usar feature flags para funcionalidad que:
  - Se despliega incrementalmente
  - Necesita poder desactivarse rápidamente
  - Está en A/B testing
  - Es una migración gradual

### Monitoreo y Observabilidad
- Toda funcionalidad nueva debe incluir:
  - Logging apropiado (no excesivo)
  - Métricas relevantes (latencia, errores, throughput)
  - Alertas para condiciones anómalas
- Usar structured logging (JSON) en producción
- Incluir correlation IDs para trazar requests entre servicios

---

## 💡 NITS (Definidos por el equipo)

### Herramientas del Equipo
Documentar las herramientas acordadas:

  Formatter:       [Prettier / Black / gofmt / rustfmt]
  Linter:          [ESLint / Pylint+Flake8 / PHPStan / golangci-lint]
  Pre-commit:      [Husky + lint-staged / pre-commit framework]
  CI/CD:           [GitHub Actions / GitLab CI / Jenkins / CircleCI]
  Package Manager: [npm / yarn / pnpm / pip / composer]
  Node Version:    [Especificar versión, usar .nvmrc]
  
  Configuraciones deben estar commiteadas en el repo:
    .prettierrc / .eslintrc / .editorconfig / pyproject.toml / etc.

### Configuración del Editor
Incluir .editorconfig en el proyecto:

  # .editorconfig
  root = true

  [*]
  indent_style = space
  indent_size = 2
  end_of_line = lf
  charset = utf-8
  trim_trailing_whitespace = true
  insert_final_newline = true

  [*.{py,rs}]
  indent_size = 4

  [*.md]
  trim_trailing_whitespace = false

  [Makefile]
  indent_style = tab