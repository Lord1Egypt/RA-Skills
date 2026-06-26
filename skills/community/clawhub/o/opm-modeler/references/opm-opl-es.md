---
_manifest:
  urn: "urn:fxsl:kb:opm-opl-es"
  provenance:
    created_by: "kora/curator"
    created_at: "2026-03-22"
    source: "OPERATIONS/source/fxsl/opm-methodology/opm-opl-es.md"
version: "1.3.1"
status: published
tags: [opm, opl, spanish, es, grammar, i18n, iso-19450, bimodal, localization]
lang: es
extensions:
  kora:
    family: specification
    depends_on:
      - "urn:fxsl:kb:opm-iso-19450"
---

# OPL-ES — Object-Process Language en Español

Especificación completa de la gramática OPL en español, complementaria a la gramática OPL en inglés definida en ISO/PAS 19450 Annex A. Diseñada para que herramientas de modelado OPM generen y parseen sentencias OPL indistintamente en inglés o español, manteniendo equivalencia semántica total.

Referencia normativa: `urn:fxsl:kb:opm-iso-19450`.

---

## 1. Decisiones de Diseño

### 1.1 Denominación de Procesos

En OPL-EN los procesos usan gerundio (-ing): "Cooking", "Driving", "Data Processing". En OPL-ES los procesos pueden usar **infinitivo** (-ar, -er, -ir): "Cocinar", "Conducir", "Procesar Datos", o una **nominalización verbal** encabezada por una primera palabra terminada en `-ción`: "Ampliación", "Verificación de Datos".

El infinitivo español es el equivalente funcional más directo del gerundio sustantivado inglés: funciona como sustantivo sujeto ("Cocinar consume..."). Sin embargo, en español técnico también es plenamente válida una forma nominal encabezada por `-ción`, cuando el dominio prefiera un nombre de acción en vez de un infinitivo.

**Validación de nombre**: un nombre de proceso OPL-ES válido cumple al menos una de estas condiciones:

1. La primera palabra está en infinitivo y termina en `-ar`, `-er` o `-ir`
2. La primera palabra termina en `-ción`
3. En dominios que lo justifiquen, la primera palabra termina en `-miento`

Ejemplos válidos: "Procesar Datos", "Preparar Empanadas", "Ampliación de Cobertura", "Verificación de Identidad", "Mantenimiento Preventivo".

**Patrones de nombre de proceso** (paralelos a EN):

| Patrón EN | Ejemplo EN | Patrón ES | Ejemplo ES |
|-----------|-----------|-----------|-----------|
| verb-ing | Making | Infinitivo o nominalización | Hacer / Fabricación |
| noun verb-ing | Cake Making | Infinitivo sustantivo o nominalización con complemento | Preparar Torta / Preparación de Torta |
| adj verb-ing | Automatic Responding | Infinitivo adverbio o nominalización | Responder Automáticamente / Respuesta Automática |
| adj noun verb-ing | Automatic Crash Responding | Infinitivo complejo o nominalización encabezada por `-ción` | Responder a Colisión Automática / Atención de Colisión Automática |

Máximo 4 palabras. Se capitalizan las palabras lexicas; articulos y preposiciones breves PUEDEN permanecer en minuscula cuando mejora la naturalidad del espanol.

### 1.2 Denominación de Objetos

Sin cambio respecto a OPL-EN: sustantivo singular, con capitalizacion en las palabras lexicas del nombre.

Plurales: sufijo "Conjunto" para inanimados (EN: "Set"), "Grupo" para humanos (EN: "Group").

Ejemplos: **Ingrediente**, **Conjunto de Ingredientes**, **Grupo de Comensales**, **Torta de Manzana**.

### 1.3 Denominación de Estados

Sin cambio respecto a OPL-EN: minúsculas, forma pasiva o descriptiva del objeto que los contiene.

Ejemplos: `pintado`, `inspeccionado`, `pre-cortado`, `vacío`, `cargado`, `satisfecho`.

### 1.4 Género Gramatical

Las plantillas usan masculino como género por defecto. El modelador ajusta al género natural del sustantivo en instancias concretas. El género afecta artículos y participios pero no la estructura de la sentencia.

Ejemplo: "es un **Sistema**" (masc.) → "es una **Máquina**" (fem.).

### 1.5 Ser vs Estar

- **estar** para estados de objetos (condición temporal, mutable): "**Objeto** está en `estado`"
- **ser** para propiedades invariantes (tipo, clasificación, esencia): "**Objeto** es de tipo X", "**X** es un **Y**"

Justificación: los estados OPM son situaciones temporales de un objeto (estar), mientras que tipo, clasificación y esencia son propiedades permanentes del modelo (ser). Esta distinción gramatical del español se alinea con la semántica OPM.

### 1.6 Artículos y Preposiciones

OPL-ES omite artículos en las sentencias, siguiendo la convención de OPL-EN, excepto donde la gramática española los requiere:

- "es un/una" en clasificación-instanciación y generalización-especialización individual
- "de lo contrario" en condiciones
- "al menos" en operadores lógicos y cardinalidades

Preposición "a" personal: omitida para objetos directos, ya que las entidades OPM son típicamente inanimadas. Ejemplo: "*Cocinar* consume **Masa**" (no "consume a Masa").

### 1.7 Convenciones Tipográficas (Markdown OPL)

| Entidad | Convención | Ejemplo |
|---------|-----------|---------|
| Objeto | **negrita** | **Ingrediente** |
| Proceso | *cursiva* | *Cocinar* |
| Estado | `monoespaciado` | `crudo` |

Codificación de color OPD (rendering gráfico): objetos verde, procesos azul, estados marrón dorado. Sin cambio respecto a OPL-EN.

### 1.8 Orden Canónico

OPL-ES preserva el orden sujeto-verbo-complemento de cada plantilla OPL-EN. No se reordena la oración. Esto garantiza correspondencia 1:1 y simplifica el parsing bidireccional.

### 1.9 State-Specified: Posición del Estado

En OPL-EN el estado precede al objeto como modificador: "`specified-state` Object". En OPL-ES el estado sigue al objeto con la preposición "en": "**Objeto** en `estado`".

- EN: `active User handles Processing.`
- ES: **Usuario** en `activo` maneja *Procesar*.

### 1.10 Voz Pasiva

OPL-ES usa la pasiva refleja ("se consume", "se omite") en lugar de la pasiva perifrástica ("es consumido"), por naturalidad y concisión.

---

## 2. Vocabulario de Verbos OPL-ES

Verbos fijos de la gramática, conjugados en tercera persona singular del presente indicativo.

| Función | EN | ES | Infinitivo ES |
|---------|----|----|--------------|
| Consumo | consumes | consume | consumir |
| Resultado | yields | genera | generar |
| Efecto | affects | afecta | afectar |
| Cambio de estado | changes … from … to | cambia … de … a | cambiar |
| Agente | handles | maneja | manejar |
| Instrumento | requires | requiere | requerir |
| Iniciación | initiates | inicia | iniciar |
| Invocación | invokes | invoca | invocar |
| Ocurrencia | occurs | ocurre | ocurrir |
| Existencia | exists | existe | existir |
| Omisión (pasiva) | is skipped | se omite | omitir |
| Consumo (pasiva) | is consumed | se consume | consumir |
| Agregación | consists of | consta de | constar |
| Exhibición | exhibits | exhibe | exhibir |
| Especialización (pl.) | are | son | ser |
| Especialización (sg.) | is a | es un/una | ser |
| Instanciación | is an instance of | es una instancia de | ser |
| Relación | relates to | se relaciona con | relacionar |
| Variación de rango | ranges from … to | varía de … a | variar |
| Tipo | is of type | es de tipo | ser |
| Declaración de estados | can be | puede estar | poder + estar |
| Descomposición | zooms into … in that sequence | se descompone en … en esa secuencia | descomponerse |
| Despliegue | unfolds into | se despliega en | desplegarse |
| Refinamiento | is refined by in-zooming … in | se refina por descomposición de … en | refinarse |

### Palabras Clave Fijas

| EN | ES |
|----|----|
| if | si |
| in which case | en cuyo caso |
| otherwise / else | de lo contrario |
| from | de |
| to | a |
| and | y (e ante i-, hi-) |
| or | o (u ante o-, ho-) |
| as well as | así como |
| exactly one of | exactamente uno de |
| at least one of | al menos uno de |
| at least one other | al menos otro/a |
| an optional | un/una opcional |
| at least one | al menos un/una |
| following path | por ruta |
| duration of | duración de |
| exceeds | excede |
| falls short of | es menor que |
| in that sequence | en esa secuencia |
| can be | puede estar |
| is initial | es inicial |
| is final | es final |
| is default | es por defecto |
| is initial and final | es inicial y final |

---

## 3. Plantillas OPL-ES — Descripción de Entidades

### 3.1 Propiedades Genéricas

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| D1 | Thing is Physical. | **Cosa** es física. |
| D2 | Thing is Informatical. | **Cosa** es informática. |
| D3 | Thing is Environmental. | **Cosa** es ambiental. |
| D4 | Thing is Systemic. | **Cosa** es sistémica. |

### 3.2 Enumeración de Estados

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| D5 | Object can be state1, state2, or state3. | **Objeto** puede estar `estado1`, `estado2` o `estado3`. |
| D6 | Object can be state1, …, and other states. | **Objeto** puede estar `estado1`, …, y otros estados. |

### 3.3 Designación de Estados

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| D7 | State s of Object is initial. | Estado `s` de **Objeto** es inicial. |
| D8 | State s of Object is final. | Estado `s` de **Objeto** es final. |
| D9 | State s of Object is default. | Estado `s` de **Objeto** es por defecto. |
| D10 | State s of Object is initial and final. | Estado `s` de **Objeto** es inicial y final. |

---

## 4. Plantillas OPL-ES — Enlaces Transformadores

### 4.1 Básicos

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| T1 | Consumo | Processing consumes Consumee. | *Procesar* consume **Consumido**. |
| T2 | Resultado | Processing yields Resultee. | *Procesar* genera **Resultado**. |
| T3 | Efecto | Processing affects Affectee. | *Procesar* afecta **Afectado**. |

### 4.2 State-Specified

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| TS1 | Consumo s-s | Process consumes specified-state Object. | *Proceso* consume **Objeto** en `estado`. |
| TS2 | Resultado s-s | Process yields specified-state Object. | *Proceso* genera **Objeto** en `estado`. |
| TS3 | Efecto entrada-salida | Process changes Object from input-state to output-state. | *Proceso* cambia **Objeto** de `estado-entrada` a `estado-salida`. |
| TS4 | Efecto solo entrada | Process changes Object from input-state. | *Proceso* cambia **Objeto** de `estado-entrada`. |
| TS5 | Efecto solo salida | Process changes Object to output-state. | *Proceso* cambia **Objeto** a `estado-salida`. |

---

## 5. Plantillas OPL-ES — Enlaces Habilitadores

### 5.1 Básicos

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| H1 | Agente | Agent handles Processing. | **Agente** maneja *Proceso*. |
| H2 | Instrumento | Processing requires Instrument. | *Proceso* requiere **Instrumento**. |

### 5.2 State-Specified

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| HS1 | Agente s-s | Specified-state Agent handles Processing. | **Agente** en `estado` maneja *Proceso*. |
| HS2 | Instrumento s-s | Processing requires specified-state Instrument. | *Proceso* requiere **Instrumento** en `estado`. |

---

## 6. Plantillas OPL-ES — Enlaces de Evento

### 6.1 Eventos Transformadores

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| ET1 | Consumo evento | Object initiates Process, which consumes Object. | **Objeto** inicia *Proceso*, que consume **Objeto**. |
| ET2 | Efecto evento | Object initiates Process, which affects Object. | **Objeto** inicia *Proceso*, que afecta **Objeto**. |

### 6.2 Eventos Habilitadores

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| EH1 | Agente evento | Agent initiates and handles Process. | **Agente** inicia y maneja *Proceso*. |
| EH2 | Instrumento evento | Instrument initiates Process, which requires Instrument. | **Instrumento** inicia *Proceso*, que requiere **Instrumento**. |

### 6.3 Eventos Transformadores State-Specified

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| ETS1 | Specified-state Object initiates Process, which consumes Object. | **Objeto** en `estado` inicia *Proceso*, que consume **Objeto**. |
| ETS2 | Input-state Object initiates Process, which changes Object from input-state to output-state. | **Objeto** en `estado-entrada` inicia *Proceso*, que cambia **Objeto** de `estado-entrada` a `estado-salida`. |
| ETS3 | Input-state Object initiates Process, which changes Object from input-state. | **Objeto** en `estado-entrada` inicia *Proceso*, que cambia **Objeto** de `estado-entrada`. |
| ETS4 | Object in any state initiates Process, which changes Object to destination-state. | **Objeto** en cualquier estado inicia *Proceso*, que cambia **Objeto** a `estado-destino`. |

### 6.4 Eventos Habilitadores State-Specified

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| EHS1 | Specified-state Agent initiates and handles Processing. | **Agente** en `estado` inicia y maneja *Proceso*. |
| EHS2 | Specified-state Instrument initiates Processing, which requires specified-state Instrument. | **Instrumento** en `estado` inicia *Proceso*, que requiere **Instrumento** en `estado`. |

---

## 7. Plantillas OPL-ES — Enlaces de Condición

### 7.1 Condición Transformadores

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| CT1 | Process occurs if Object exists, in which case Object is consumed, otherwise Process is skipped. | *Proceso* ocurre si **Objeto** existe, en cuyo caso **Objeto** se consume, de lo contrario *Proceso* se omite. |
| CT2 | Process occurs if Object exists, in which case Process affects Object, otherwise Process is skipped. | *Proceso* ocurre si **Objeto** existe, en cuyo caso *Proceso* afecta **Objeto**, de lo contrario *Proceso* se omite. |

### 7.2 Condición Habilitadores

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| CH1 | Agent handles Process if Agent exists, else Process is skipped. | **Agente** maneja *Proceso* si **Agente** existe, de lo contrario *Proceso* se omite. |
| CH2 | Process occurs if Instrument exists, else Process is skipped. | *Proceso* ocurre si **Instrumento** existe, de lo contrario *Proceso* se omite. |

### 7.3 Condición State-Specified

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| CS1 | Process occurs if Object is specified-state, in which case Object is consumed, otherwise Process is skipped. | *Proceso* ocurre si **Objeto** está en `estado`, en cuyo caso **Objeto** se consume, de lo contrario *Proceso* se omite. |
| CS2 | Process occurs if Object is input-state, in which case Process changes Object from input-state to output-state, otherwise Process is skipped. | *Proceso* ocurre si **Objeto** está en `estado-entrada`, en cuyo caso *Proceso* cambia **Objeto** de `estado-entrada` a `estado-salida`, de lo contrario *Proceso* se omite. |
| CS3 | Process occurs if Object is input-state, in which case Process changes Object from input-state, otherwise Process is skipped. | *Proceso* ocurre si **Objeto** está en `estado-entrada`, en cuyo caso *Proceso* cambia **Objeto** de `estado-entrada`, de lo contrario *Proceso* se omite. |
| CS4 | Process occurs if Object exists, in which case Process changes Object to output-state, otherwise Process is skipped. | *Proceso* ocurre si **Objeto** existe, en cuyo caso *Proceso* cambia **Objeto** a `estado-salida`, de lo contrario *Proceso* se omite. |
| CS5 | Agent handles Process if Agent is specified-state, else Process is skipped. | **Agente** maneja *Proceso* si **Agente** está en `estado`, de lo contrario *Proceso* se omite. |
| CS6 | Process occurs if Instrument is specified-state, otherwise Process is skipped. | *Proceso* ocurre si **Instrumento** está en `estado`, de lo contrario *Proceso* se omite. |

---

## 8. Plantillas OPL-ES — Excepción e Invocación

### 8.1 Enlaces de Excepción

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| EX1 | Overtime | Handling occurs if duration of Source exceeds max-duration time-units. | *Manejo* ocurre si duración de *Fuente* excede máx-duración unidades-tiempo. |
| EX2 | Undertime | Handling occurs if duration of Source falls short of min-duration time-units. | *Manejo* ocurre si duración de *Fuente* es menor que mín-duración unidades-tiempo. |

### 8.2 Enlaces de Invocación

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| IV1 | Invocación | Invoking invokes Invoked. | *Invocador* invoca *Invocado*. |
| IV2 | Auto-invocación | Invoking invokes itself. | *Invocador* se invoca a sí mismo. |

---

## 9. Plantillas OPL-ES — Enlaces Estructurales

### 9.1 Etiquetados

| ID | Tipo | OPL-EN | OPL-ES |
|----|------|--------|--------|
| SE1 | Unidireccional etiquetado | Source tag Destination. | **Origen** etiqueta **Destino**. |
| SE2 | Unidireccional sin etiqueta | Source relates to Destination. | **Origen** se relaciona con **Destino**. |
| SE3 | Bidireccional etiquetado | Source f-tag Dest. / Dest b-tag Source. | **Origen** etiqueta-f **Destino**. / **Destino** etiqueta-b **Origen**. |
| SE4 | Recíproco etiquetado | Source and Destination are tag. | **Origen** y **Destino** son etiqueta. |
| SE5 | Recíproco sin etiqueta | Source and Destination are related. | **Origen** y **Destino** se relacionan. |

Nota: en SE1, SE3 y SE4, "etiqueta" es el tag definido por el modelador en español (ej. "emplea", "pertenece a", "supervisa"). El tag actúa como verbo o predicado nominal de la oración.

### 9.2 Relaciones Estructurales Fundamentales

| ID | Relación | OPL-EN | OPL-ES |
|----|----------|--------|--------|
| RF1 | Agregación-participación | Whole consists of Part1, Part2 and Part3. | **Todo** consta de **Parte1**, **Parte2** y **Parte3**. |
| RF2 | Exhibición-caracterización (solo atributos) | Exhibitor exhibits Attribute1 and Attribute2. | **Exhibidor** exhibe **Atributo1** y **Atributo2**. |
| RF2b | Exhibición-caracterización (atributos + operaciones) | Exhibitor exhibits Attribute1 as well as Operation1. | **Exhibidor** exhibe **Atributo1** así como *Operación1*. |
| RF3 | Generalización-especialización (compuesto) | Specialization1 and Specialization2 are General. | **Especialización1** y **Especialización2** son **General**. |
| RF3b | Generalización-especialización (individual) | Specialization is a General. | **Especialización** es un **General**. |
| RF4 | Clasificación-instanciación | Instance is an instance of Class. | **Instancia** es una instancia de **Clase**. |

### 9.3 Colecciones Incompletas

| OPL-EN | OPL-ES |
|--------|--------|
| …and at least one other part. | …y al menos otra parte. |
| …and at least one other feature. | …y al menos otro rasgo. |
| …and at least one other specialization. | …y al menos otra especialización. |

### 9.4 State-Specified Estructurales

| Grupo | OPL-EN | OPL-ES |
|-------|--------|--------|
| Estado en origen (uni) | Specified-state Source tag Destination. | **Origen** en `estado` etiqueta **Destino**. |
| Estado en destino (uni) | Source tag specified-state Destination. | **Origen** etiqueta **Destino** en `estado`. |
| Estado en ambos (uni) | Sa Source tag Sb Destination. | **Origen** en `sa` etiqueta **Destino** en `sb`. |
| Estado en origen (bidi, f-tag) | Sa Source f-tag Destination. | **Origen** en `sa` etiqueta-f **Destino**. |
| Estado en origen (bidi, b-tag) | Destination b-tag Sa Source. | **Destino** etiqueta-b **Origen** en `sa`. |
| Estado en ambos (recíproco) | Sa Source and Sb Dest are tag. | **Origen** en `sa` y **Destino** en `sb` son etiqueta. |
| Estado en origen (recíproco) | Dest and Sa Source are tag. | **Destino** y **Origen** en `sa` son etiqueta. |

---

## 10. Plantillas OPL-ES — Gestión de Contexto

### 10.1 Descomposición (In-Zooming)

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| CX1 | Process zooms into P1, P2 and P3, in that sequence. | *Proceso* se descompone en *P1*, *P2* y *P3*, en esa secuencia. |
| CX2 | Process zooms into parallel P1 and P2. | *Proceso* se descompone en paralelo *P1* y *P2*. |

### 10.2 Despliegue (Unfolding)

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| CX3 | Thing unfolds in SD1 into T1, T2 and T3. | **Cosa** se despliega en SD1 en **T1**, **T2** y **T3**. |

### 10.3 Refinamiento entre OPDs

| ID | OPL-EN | OPL-ES |
|----|--------|--------|
| CX4 | SD is refined by in-zooming Process in SD1. | SD se refina por descomposición de *Proceso* en SD1. |

---

## 11. Operadores Lógicos

### 11.1 AND

AND se expresa implícitamente mediante sentencias OPL separadas para cada enlace. No hay operador explícito — cada enlace genera su propia oración. Gráficamente: enlaces separados (no se tocan) en el contorno del proceso.

Ejemplo AND de agentes:

- EN: `Safe Owner A handles Safe Opening.` / `Safe Owner B handles Safe Opening.`
- ES: **Dueño de Caja Fuerte A** maneja *Abrir Caja Fuerte*. / **Dueño de Caja Fuerte B** maneja *Abrir Caja Fuerte*.

### 11.2 XOR

Gráficamente: arco discontinuo simple. EN: "exactly one of". ES: "exactamente uno de".

| Familia | OPL-EN | OPL-ES |
|---------|--------|--------|
| Consumo conv. | P consumes exactly one of A, B, or C. | *P* consume exactamente uno de **A**, **B** o **C**. |
| Consumo div. | Exactly one of P, Q, or R consumes B. | Exactamente uno de *P*, *Q* o *R* consume **B**. |
| Resultado conv. | Exactly one of P, Q, or R yields B. | Exactamente uno de *P*, *Q* o *R* genera **B**. |
| Resultado div. | P yields exactly one of A, B, or C. | *P* genera exactamente uno de **A**, **B** o **C**. |
| Efecto (objetos) | P affects exactly one of A, B, or C. | *P* afecta exactamente uno de **A**, **B** o **C**. |
| Efecto (procesos) | Exactly one of P, Q, or R affects B. | Exactamente uno de *P*, *Q* o *R* afecta **B**. |
| Agente | B handles exactly one of P, Q, or R. | **B** maneja exactamente uno de *P*, *Q* o *R*. |
| Instrumento | Exactly one of P, Q, or R requires B. | Exactamente uno de *P*, *Q* o *R* requiere **B**. |
| Invocación div. | P invokes exactly one of Q or R. | *P* invoca exactamente uno de *Q* o *R*. |
| Invocación conv. | Exactly one of P or Q invokes R. | Exactamente uno de *P* o *Q* invoca *R*. |

### 11.3 OR

Misma estructura que XOR, reemplazando:

- EN: "exactly one of" → "at least one of"
- ES: "exactamente uno de" → "al menos uno de"

Gráficamente: arco doble (dos arcos concéntricos discontinuos).

### 11.4 XOR/OR con Modificadores de Control

Los abanicos XOR y OR se combinan con modificadores evento ("e") y condición ("c"). Regla de composición:

**Evento + XOR** — insertar "inicia" antes del verbo principal:

- EN: `B initiates exactly one of P, Q, or R, which affects B.`
- ES: **B** inicia exactamente uno de *P*, *Q* o *R*, que afecta **B**.

**Condición + XOR** — insertar "si … existe/está en estado … de lo contrario … se omite":

- EN: `Exactly one of P, Q, R occurs if B exists, otherwise skipped.`
- ES: Exactamente uno de *P*, *Q* o *R* ocurre si **B** existe, de lo contrario se omite.

Reemplazar "exactamente" por "al menos" para obtener la variante OR.

### 11.5 Probabilístico

Anotación `Pr=p` en cada enlace del abanico. Suma de probabilidades = 1. Notación numérica universal, sin cambio entre EN y ES.

---

## 12. Cardinalidad y Multiplicidad

| Símbolo | Rango | OPL-EN | OPL-ES |
|---------|-------|--------|--------|
| ? | 0..1 | an optional | un/una opcional |
| * | 0..* | optional (none to many) | opcional (cero o más) |
| (ninguno) | 1..1 | (default) | (por defecto) |
| + | 1..* | at least one | al menos un/una |

Rango parametrizado: `qmín..qmáx`. Restricciones con =, ≠, <, ≤, ≥, ∈. Sin cambio sintáctico entre EN y ES (notación matemática universal).

**Ejemplo de multiplicidad parametrizada**:

- EN: `Jet Engine consists of b Installed Blades.`
- ES: **Motor a Reacción** consta de b **Paletas Instaladas**.

### 12.1 Tipo

| OPL-EN | OPL-ES |
|--------|--------|
| Object is of type type-id. | **Objeto** es de tipo tipo-id. |

Tipos: boolean, string, integer, float, double, short, long, enumerated. Sin traducción (identificadores de tipo universales).

---

## 13. Etiquetas de Camino

| OPL-EN | OPL-ES |
|--------|--------|
| Following path label, Process consumes Object. | Por ruta etiqueta, *Proceso* consume **Objeto**. |
| Following path label, Process yields Object. | Por ruta etiqueta, *Proceso* genera **Objeto**. |

"Por ruta" es la expresión fija. "etiqueta" es el nombre de la ruta definido por el modelador.

**Ejemplo (Preparar Alimento)**:

- EN: `Following path carnivore, Food Preparing consumes Meat, yields Stew and Steak.`
- ES: Por ruta carnívoro, *Preparar Alimento* consume **Carne**, genera **Estofado** y **Bistec**.

- EN: `Following path herbivore, Food Preparing consumes Cucumber and Tomato, yields Salad.`
- ES: Por ruta herbívoro, *Preparar Alimento* consume **Pepino** y **Tomate**, genera **Ensalada**.

---

## 14. Atributos y Valores

| OPL-EN | OPL-ES |
|--------|--------|
| Attribute of Object is value. | **Atributo** de **Objeto** es valor. |
| Attribute of Object ranges from X to Y. | **Atributo** de **Objeto** varía de X a Y. |
| Attribute of Object can be value1, value2, or value3. | **Atributo** de **Objeto** puede estar `valor1`, `valor2` o `valor3`. |

**Ejemplo**:

- EN: `Cleanliness of Dish Set can be dirty or clean.`
- ES: **Limpieza** de **Conjunto de Platos** puede estar `sucio` o `limpio`.

- EN: `State dirty of Cleanliness of Dish Set is initial.`
- ES: Estado `sucio` de **Limpieza** de **Conjunto de Platos** es inicial.

---

## 15. Reglas de Transformación Sistemática EN → ES

Para implementadores de herramientas. Reglas aplicadas en secuencia sobre una sentencia OPL-EN para producir OPL-ES:

| # | Regla | EN | ES |
|---|-------|----|----|
| R1 | Verbo principal | consumes, yields, affects, handles, requires, initiates, invokes, occurs, exists | consume, genera, afecta, maneja, requiere, inicia, invoca, ocurre, existe |
| R2 | State-specified: posición | `state Object` (estado antes del objeto) | **Objeto** en `estado` (estado después del objeto con "en") |
| R3 | Estado condicional | Object is state | **Objeto** está en `estado` |
| R4 | Declaración de estados | can be | puede estar |
| R5 | Conjunción copulativa | and | y (e ante i-/hi-) |
| R6 | Conjunción disyuntiva | or | o (u ante o-/ho-) |
| R7 | Preposición de origen | from | de |
| R8 | Preposición de destino | to | a |
| R9 | Preposición posesiva | of | de |
| R10 | Cuantificador XOR | exactly one of | exactamente uno de |
| R11 | Cuantificador OR | at least one of | al menos uno de |
| R12 | Condicional | if … exists | si … existe |
| R13 | Consecuencia | in which case | en cuyo caso |
| R14 | Alternativa | otherwise / else | de lo contrario |
| R15 | Pasiva refleja | is consumed / is skipped | se consume / se omite |
| R16 | Camino | Following path | Por ruta |
| R17 | Artículo en instanciación | is an instance of | es una instancia de |
| R18 | Artículo en especialización (sg.) | is a | es un/una |
| R19 | Secuencia | in that sequence | en esa secuencia |
| R20 | Designación de estado | is initial / is final / is default | es inicial / es final / es por defecto |
| R21 | Nombres de entidad | (sin cambio — definidos por el modelador) | (sin cambio) |

**Nota para parsers**: el verbo principal (R1) es el ancla léxica para detectar el idioma de la sentencia. Un parser puede determinar EN vs ES verificando si el primer verbo conjugado pertenece al set EN o ES.

---

## 16. Ejemplo Completo: Sistema de Preparación de Empanadas

### Contexto

Sistema doméstico de preparación de empanadas de pino (tradicionales chilenas). Modela el SD completo con los 5 componentes de un sistema artificial.

### Componentes del SD

| Componente | Elemento |
|-----------|---------|
| 1. Propósito | Cambiar **Nivel de Satisfacción** de **Grupo de Comensales** de `insatisfecho` a `satisfecho` |
| 2. Función principal | *Preparar Empanadas* (proceso principal) + **Grupo de Comensales** (operando) |
| 3. Habilitadores | **Cocinero** (agente), **Sistema de Preparación de Empanadas** (instrumento principal), **Horno**, **Utensilios de Cocina** (instrumentos) |
| 4. Entorno | **Receta** (informático, ambiental) |
| 5. Ocurrencia del problema | *Cocinar sin Sistema* (proceso ambiental) causa estado `insatisfecho` |

### Tabla de Elementos

| Tipo | Nombre | Esencia | Afiliación | Estados |
|------|--------|---------|------------|---------|
| Proceso | *Preparar Empanadas* | Físico | Sistémico | — |
| Objeto | **Grupo de Comensales** | Físico | Sistémico | — |
| Objeto | **Nivel de Satisfacción** | Informático | Sistémico | `insatisfecho`, `satisfecho` |
| Objeto | **Cocinero** | Físico | Sistémico | — |
| Objeto | **Sistema de Prep. de Empanadas** | Físico | Sistémico | — |
| Objeto | **Horno** | Físico | Sistémico | — |
| Objeto | **Utensilios de Cocina** | Físico | Sistémico | — |
| Objeto | **Masa Cruda** | Físico | Sistémico | — |
| Objeto | **Relleno de Pino** | Físico | Sistémico | — |
| Objeto | **Empanada** | Físico | Sistémico | — |
| Objeto | **Receta** | Informático | Ambiental | — |

### Tabla de Enlaces

| Tipo | Origen | Destino | ID |
|------|--------|---------|-----|
| Efecto (entrada-salida) | *Preparar Empanadas* | **Nivel de Satisfacción** | TS3 |
| Exhibición-caracterización | **Grupo de Comensales** | **Nivel de Satisfacción** | RF2 |
| Agente | **Cocinero** | *Preparar Empanadas* | H1 |
| Instrumento | **Sistema de Prep. de Empanadas** | *Preparar Empanadas* | H2 |
| Instrumento | **Horno** | *Preparar Empanadas* | H2 |
| Instrumento | **Utensilios de Cocina** | *Preparar Empanadas* | H2 |
| Consumo | **Masa Cruda** | *Preparar Empanadas* | T1 |
| Consumo | **Relleno de Pino** | *Preparar Empanadas* | T1 |
| Resultado | *Preparar Empanadas* | **Empanada** | T2 |
| Etiquetado (nulo) | **Receta** | *Preparar Empanadas* | SE2 |

### OPL-ES del SD

```
*Preparar Empanadas* afecta **Grupo de Comensales**.
**Grupo de Comensales** exhibe **Nivel de Satisfacción**.
**Nivel de Satisfacción** puede estar `insatisfecho` o `satisfecho`.
Estado `insatisfecho` de **Nivel de Satisfacción** es inicial.
Estado `satisfecho` de **Nivel de Satisfacción** es final.
*Preparar Empanadas* cambia **Nivel de Satisfacción** de `insatisfecho` a `satisfecho`.
**Cocinero** maneja *Preparar Empanadas*.
*Preparar Empanadas* requiere **Sistema de Preparación de Empanadas**.
*Preparar Empanadas* requiere **Horno**.
*Preparar Empanadas* requiere **Utensilios de Cocina**.
*Preparar Empanadas* consume **Masa Cruda**.
*Preparar Empanadas* consume **Relleno de Pino**.
*Preparar Empanadas* genera **Empanada**.
**Receta** es ambiental.
**Receta** se relaciona con *Preparar Empanadas*.
```

### OPL-EN Equivalente

```
Preparing Empanadas affects Diner Group.
Diner Group exhibits Satisfaction Level.
Satisfaction Level can be unsatisfied or satisfied.
State unsatisfied of Satisfaction Level is initial.
State satisfied of Satisfaction Level is final.
Preparing Empanadas changes Satisfaction Level from unsatisfied to satisfied.
Cook handles Preparing Empanadas.
Preparing Empanadas requires Empanada Preparation System.
Preparing Empanadas requires Oven.
Preparing Empanadas requires Kitchen Utensils.
Preparing Empanadas consumes Raw Dough.
Preparing Empanadas consumes Pino Filling.
Preparing Empanadas yields Empanada.
Recipe is Environmental.
Recipe relates to Preparing Empanadas.
```

### SD1: Descomposición de Preparar Empanadas

```
SD se refina por descomposición de *Preparar Empanadas* en SD1.
*Preparar Empanadas* se descompone en *Preparar Masa*, *Preparar Relleno*,
  *Armar Empanadas* y *Hornear Empanadas*, en esa secuencia.
*Preparar Masa* consume **Masa Cruda**.
*Preparar Masa* genera **Masa Estirada**.
*Preparar Relleno* consume **Relleno de Pino**.
*Preparar Relleno* genera **Relleno Cocido**.
*Armar Empanadas* consume **Masa Estirada**.
*Armar Empanadas* consume **Relleno Cocido**.
*Armar Empanadas* genera **Empanada** en `cruda`.
**Horno** puede estar `frío` o `precalentado`.
*Hornear Empanadas* requiere **Horno** en `precalentado`.
*Hornear Empanadas* cambia **Empanada** de `cruda` a `horneada`.
```

---

## 17. Diferencias con EBNF ISO 19450 Annex A

La EBNF de OPL-EN (ISO/PAS 19450 Annex A) define los terminales léxicos en inglés. Para OPL-ES se requiere una EBNF paralela con los siguientes cambios:

### 17.1 Terminales Léxicos

Sustituir cada terminal reservado EN por su equivalente ES según la tabla de la sección 2.

### 17.2 Identificadores

```ebnf
(* EN *)
process identifier = singular process name | singular process name, " process" ;
(* ES *)
identificador de proceso = nombre singular de proceso | nombre singular de proceso, " proceso" ;
```

Nombre de proceso EN: frase en gerundio capitalizada (-ing). Nombre de proceso ES: frase capitalizada encabezada por infinitivo (`-ar`, `-er`, `-ir`) o por nominalización en `-ción`; `-miento` también se acepta cuando el dominio lo requiere.

```ebnf
(* EN *)
state identifier = non capitalized word ;
(* ES — sin cambio *)
identificador de estado = palabra no capitalizada ;
```

### 17.3 Participación

```ebnf
(* EN *)
lower single = "a" | "an" | "an optional" | "at least one" ;
(* ES *)
singular inferior = "un" | "una" | "un opcional" | "una opcional" | "al menos un" | "al menos una" ;
```

### 17.4 Sentencias de Cambio de Estado

```ebnf
(* EN *)
in out object change phrase = object identifier, " from ", input state, " to ", output state ;
(* ES *)
frase de cambio entrada-salida = identificador de objeto, " de ", estado entrada, " a ", estado salida ;
```

### 17.5 Estructura de Producción

Las reglas de producción (no terminales) no cambian. Solo se sustituyen los terminales léxicos. Esto garantiza que ambas gramáticas generan sentencias semánticamente equivalentes.

---

## 18. Notas de Implementación

### 18.1 Parsing Bidireccional

Una herramienta OPM bilingüe debería:

1. Detectar idioma de la sentencia OPL por verbo principal (consume/consumes, genera/yields, etc.)
2. Permitir cambio de idioma global del modelo (re-generar todas las sentencias OPL)
3. Mantener el modelo semántico (OPD) independiente del idioma OPL
4. Permitir modelos mixtos solo si el usuario lo habilita explícitamente (no recomendado)

### 18.2 OPCloud

OPCloud ya soporta múltiples idiomas OPL (chino, francés, alemán, coreano). OPL-ES seguiría el mismo mecanismo de localización, agregando español como idioma disponible en: User Settings > OPL Language.

A nivel de superficie textual, una implementación operativa DEBERIA además permitir:

1. Elegir idioma OPL a nivel de usuario/modelo sin alterar el OPD subyacente
2. Mostrar todas las sentencias o solo las de esencia no-default
3. Alternar numeración, aliases y units display sin afectar la semántica
4. Re-generar el párrafo OPL completo al cambiar idioma, manteniendo invariantes de roundtrip

### 18.3 Compatibilidad Semántica

OPL-ES no modifica la semántica OPM. Un modelo creado con OPL-ES es semánticamente idéntico a su equivalente OPL-EN. La traducción es puramente léxica y sintáctica, no semántica. El modelo interno (OPD constructs, link sets, thing sets) permanece invariante.

### 18.4 Roundtrip

Toda sentencia OPL-EN en forma canonica tiene al menos una sentencia OPL-ES semánticamente equivalente y viceversa. El roundtrip EN→ES→EN DEBE preservar la semántica original, aunque la superficie española pueda realizarse con infinitivo o con nominalización encabezada por `-ción` (y, cuando aplique, `-miento`). La herramienta DEBERIA respetar la forma elegida por el modelo o normalizarla al registro configurado, pero NO forzar exclusivamente infinitivo.

**Nota normativa sobre roundtrip y superficie:** preservar roundtrip NO significa imponer una unica forma superficial en espanol. Significa preservar el mismo hecho del modelo. Por lo tanto, si dos nombres de proceso en OPL-ES son semanticamente equivalentes y validos en el dominio, ambos PUEDEN mapear al mismo proceso interno. Ejemplo: `Verificar Identidad` y `Verificación de Identidad` PUEDEN representar el mismo proceso. Al volver de ES a EN, la herramienta DEBE recuperar un nombre ingles semanticamente equivalente, aunque la superficie espanola original no haya sido la unica posible. La normalizacion de superficie, si existe, DEBERIA ser configurable por politica editorial del modelo, no una imposicion semantica fija del lenguaje.

### 18.5 Politica de Modelos Mixtos

Un modelo con prosa de apoyo en español y OPL canónica en inglés es aceptable como artefacto editorial, pero una herramienta bilingüe NO DEBERIA mezclar OPL-EN y OPL-ES dentro del mismo párrafo generado salvo habilitación explícita del usuario. La política recomendada es:

1. Un idioma OPL canónico por modelo activo
2. Cambio de idioma mediante re-generación completa, no edición parcial
3. Mezcla EN/ES solo para revisión o migración, nunca como estado estable por defecto
