# Reglas Generales de Código

Estas reglas aplican a TODOS los lenguajes y archivos sin excepción.

---

## 🔴 BLOCKERS (Siempre rechazar)

### Dead Code
- Código comentado que se dejó "por si acaso"
- Funciones que nunca se llaman y no son exportadas
- Imports o requires no utilizados
- Variables declaradas pero nunca usadas
- Archivos enteros que no se referencian en ningún lado

### Errores Lógicos
- Condiciones que siempre son true o siempre son false
- Loops infinitos no intencionales
- Off-by-one errors en iteraciones
- Comparaciones incorrectas entre tipos
- Return statements inalcanzables (código después de return)
- Switch/case sin break que causa fall-through no intencional

### Manejo de Errores Inexistente
- Try/catch vacíos o que solo hacen console.log/print
- Promesas sin catch o sin try/catch en async/await
- No validar inputs de usuario antes de procesarlos
- No verificar null/undefined/nil antes de acceder a propiedades
- Funciones que pueden fallar sin ningún manejo de error

### Hardcoded Secrets
- Contraseñas en el código fuente
- API keys, tokens, secrets en el código fuente
- URLs de bases de datos con credenciales embebidas
- Cualquier string que parezca un secret o credencial
- Archivos .env commiteados al repositorio

---

## 🟡 WARNINGS (Debería corregirse)

### Complejidad Excesiva
- Funciones de más de 40 líneas: dividir en funciones más pequeñas
- Más de 3 niveles de anidamiento (if dentro de if dentro de if)
- Funciones con más de 4 parámetros: usar objeto de configuración
- Archivos de más de 300 líneas: considerar dividir en módulos
- Cyclomatic complexity alta: muchos caminos de ejecución posibles

### Naming Pobre
- Variables de una sola letra (excepto en loops cortos: i, j, k)
- Nombres genéricos que no dicen nada: data, info, temp, result, item, element, stuff
- Nombres que no describen qué contienen o qué hacen
- Booleanos que no empiezan con is, has, can, should, was, will
- Funciones que no empiezan con un verbo de acción
- Abreviaciones confusas: usr, mgr, btn (excepto las universalmente aceptadas)

### DRY (Don't Repeat Yourself)
- Bloques de código duplicados: 3 o más líneas iguales o casi iguales
- Lógica similar que podría abstraerse en una función reutilizable
- Strings mágicos repetidos: usar constantes con nombre descriptivo
- Configuraciones repetidas que deberían centralizarse

### Magic Numbers y Strings
- Números sin contexto: if (status === 3) debe ser if (status === STATUS.ACTIVE)
- Strings repetidos que representan estados o configuraciones
- Timeouts, límites, tamaños sin nombre descriptivo

### Comentarios Problemáticos
- Comentarios que describen QUÉ hace el código en lugar de POR QUÉ
- Comentarios desactualizados que no reflejan el código actual
- TODO, FIXME, HACK sin ticket o issue asociado

---

## 🔵 SUGGESTIONS (Mejoras opcionales)

### Legibilidad
- Usar early returns para reducir anidamiento
- Extraer condiciones complejas a variables con nombre descriptivo
- Preferir funciones puras cuando sea posible
- Separar lógica de negocio de lógica de infraestructura

### Performance General
- Operaciones costosas dentro de loops que podrían sacarse fuera
- Cálculos repetidos que podrían cachearse
- Concatenación de strings en loops: usar arrays y join
- Consultas a base de datos dentro de loops (N+1 problem)

### Testing
- Código nuevo sin tests correspondientes
- Tests que no cubren edge cases
- Tests que dependen del orden de ejecución
- Tests que dependen de datos externos o estado global

---

## 💡 NITS (Detalles menores)

### Formato
- Inconsistencia en uso de comillas simples vs dobles
- Inconsistencia en punto y coma al final de líneas
- Espaciado inconsistente entre bloques
- Líneas excesivamente largas (más de 120 caracteres)
- Archivo sin línea vacía al final