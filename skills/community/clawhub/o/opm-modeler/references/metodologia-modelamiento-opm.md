---
_manifest:
  urn: "urn:fxsl:kb:metodologia-modelamiento-opm"
  provenance:
    created_by: "kora/curator"
    created_at: "2026-03-25"
    source: "synthesis:opm-iso-19450,opm-opl-es,opcloud-tutorial-videos,opm-applied-system-modeling,opm-canonical-example"
version: "3.5.1"
status: published
tags: [opm, methodology, system-modeling, sd-construction, refinement, complexity-management, modeling-protocol, patterns, antipatterns, control-flow, error-handling, quantitative, simulation, executable-modeling, opcloud]
lang: es
extensions:
  kora:
    family: specification
    depends_on:
      - "urn:fxsl:kb:opm-iso-19450"
      - "urn:fxsl:kb:opm-opl-es"
---

# Metodologia de Modelamiento OPM — Protocolo de Modelamiento Conceptual de Sistemas

## 1 Definicion

Esta especificacion define la metodologia para construir modelos conceptuales de sistemas usando Object-Process Methodology (OPM). Consolida reglas normativas desde [OPM ISO 19450](urn:fxsl:kb:opm-iso-19450) y [OPL-ES](urn:fxsl:kb:opm-opl-es), e incorpora directamente la guia operativa de tool usage previamente dispersa en artefactos hoy deprecados. Para la especificacion formal del lenguaje OPM, ver [OPM ISO 19450](urn:fxsl:kb:opm-iso-19450). Para la realizacion textual en espanol, ver [OPL-ES](urn:fxsl:kb:opm-opl-es).

### 1.1 Alcance y Precedencia del Corpus

Este artefacto es una **guia derivada**. No reemplaza la base normativa del corpus.

Orden de precedencia:

1. **ISO 19450** gobierna semantica OPM, notacion, relaciones y procedimiento base de construccion del SD.
2. **OPL-ES** gobierna la realizacion textual en espanol sin alterar la semantica OPM.
3. **Esta metodologia** integra las capas normativas anteriores y explicita reglas operativas para lifecycle, simulacion, gobernanza del modelo y uso de herramienta.

Regla de resolucion:

- Si una regla de **semantica OPM** entra en conflicto con una regla de herramienta, prevalece ISO 19450.
- Si un artefacto en `lang: es` define **realizacion OPL en espanol** como parte de su contrato, prevalece OPL-ES. Un artefacto expositivo en `lang: es` PUEDE mantener sentencias OPL canonicas en ingles para preservar roundtrip con ISO/OPCloud, siempre que lo declare explicitamente y no presente esas sentencias como OPL-ES.
- Las capacidades de OPCloud NO redefinen por si solas la semantica de OPM; solo operacionalizan su uso en la herramienta.
- Los artefactos deprecados del directorio NO participan en precedencia; solo sirven como routing historico.

## 2 Definiciones

| Termino | Definicion |
|---------|-----------|
| SD (System Diagram) | OPD de nivel 0 que define proposito, alcance y funcion principal del sistema |
| SD1 | OPD descendiente de SD donde el proceso principal se refina exponiendo subprocesos |
| OPD (Object-Process Diagram) | Diagrama unico de OPM que expresa estructura y comportamiento |
| OPL (Object-Process Language) | Modalidad textual de OPM, equivalente semantica del OPD |
| Beneficiario | Stakeholder que extrae valor y beneficio del sistema |
| Transformee | Objeto transformado por un proceso |
| Agente | Enabler humano exclusivamente; el termino esta reservado para personas o grupos de personas |
| Instrumento | Enabler no humano (fisico o informatical) |
| Funcion | Proceso de nivel superior que provee valor, percibido por el beneficiario |
| Arquitectura | Combinacion de estructura + comportamiento que habilita la funcion y produce emergencia |
| Emergencia | Capacidad del sistema completo que ninguna parte individual exhibe |
| Proceso state-preserving | Proceso que mantiene el status quo de un objeto sin transformarlo |
| Objeto transiente | Objeto de vida corta creado y consumido inmediatamente entre dos procesos |
| Semantic strength | Fuerza semantica de un link procedural que determina precedencia en conflictos |
| Singular Name Principle | Los nombres de things en OPM DEBEN ser singulares. En ingles, colecciones humanas usan "Group" y las inanimadas "Set". En espanol, los equivalentes son "Grupo" y "Conjunto" |

## 3 Fundamentos Ontologicos

### 3.1 Principio de Ontologia Minima

> Si un sistema puede especificarse al mismo nivel de precision y detalle con dos lenguajes de diferentes tamanos ontologicos, el lenguaje con ontologia menor es preferible, siempre que la comprensibilidad sea comparable.

OPM usa exactamente tres tipos de elementos: objetos, procesos, y relaciones.

### 3.2 Teorema Objeto-Proceso

> Objetos, procesos y relaciones entre ellos constituyen una ontologia universal minima.

Demostrado por necesidad (especificar estructura requiere objetos; especificar comportamiento requiere procesos) y suficiencia (las cosas existen o suceden; solo se asocian mediante relaciones). Los objetos pueden ser stateful (con estados explicitos, transformables via effect) o stateless (sin estados, solo creables/consumibles). La distincion stateful/stateless es posterior a la base ontologica.

### 3.3 Asercion Objeto-Proceso

> Usando objetos, procesos, relaciones, y mecanismos de refinamiento (in-zooming y unfolding), se puede modelar conceptualmente cualquier sistema en cualquier dominio y nivel de complejidad.

## 4 Principios de Modelamiento

Todo modelamiento OPM DEBE respetar estos principios. Constituyen restricciones invariantes que gobiernan cada decision.

### 4.1 Function-as-a-Seed

> El modelamiento de un sistema DEBE comenzar definiendo, nombrando y representando la funcion del sistema, que es su proceso de nivel superior.

La funcion es la semilla de la que evoluciona el modelo. Comenzar por la forma (objetos) en vez de la funcion (proceso) es un error comun.

### 4.2 Importancia de Thing

> La importancia de un thing T en un modelo OPM es directamente proporcional al OPD mas alto en la jerarquia donde T aparece.

Objetos y procesos tienen igual estatus; ninguno tiene supremacia sobre el otro.

### 4.3 Transformacion de Objeto por Proceso

> En un modelo OPM completo, cada proceso DEBE estar conectado a al menos un objeto que el proceso transforma o a un estado de ese objeto.

Un proceso sin transforming link no tiene significado. Un proceso PUEDE tener multiples transformees.

### 4.4 Unicidad de Link Procedural

> A cualquier nivel de detalle, un objeto y un proceso PUEDEN estar conectados con a lo sumo un link procedural, que determina univocamente el rol del objeto respecto al proceso.

**Resolucion de colision de roles:** Cuando un objeto es simultaneamente enabler (agent o instrument) y transformee (affectee) del mismo proceso, el transforming link DEBE prevalecer por mayor semantic strength. El modelador PUEDE agregar un stick-figure para preservar la identidad humana del agent desplazado. Alternativa: hacer in-zoom al proceso y asignar agent link a un subproceso y effect link a otro.

### 4.5 Representacion de Hechos del Modelo

> Todo hecho del modelo DEBE aparecer en al menos un OPD del set de OPDs del modelo.

No todo hecho necesita repetirse en cada OPD. Suficiente con que aparezca al menos una vez.

### 4.6 Jerarquia de Detalle

> Cuando un OPD se vuelve dificil de comprender por exceso de detalle, se DEBE crear un nuevo OPD descendiente.

Heuristica: un OPD NO DEBERIA exceder 20-25 entidades ni una pantalla/pagina.

### 4.7 Equivalencia Grafico-Texto

> Todo modelo OPM DEBE expresarse en modalidades graficas (OPD) y textuales (OPL) semanticamente equivalentes.

Cada OPD tiene un paragrafo OPL correspondiente. La redundancia aprovecha canales cognitivos duales (visual + verbal).

### 4.8 Trade-off Completitud-Claridad

> El detalle abrumador de sistemas reales DEBE balancearse distribuyendo la especificacion completa a traves del set de OPDs, manteniendo cada OPD individual claro y comprensible.

## 5 Clasificacion del Sistema

Antes de construir el SD, el modelador DEBE clasificar el sistema. La clasificacion determina que componentes del SD aplican.

Reglas prescriptivas por categoria:

- **Artificial**: DEBE modelarse con los 5 componentes completos
- **Natural**: NO DEBE modelarse purpose (usar "outcome"). NO DEBE modelarse problem occurrence. NO hay agentes humanos — solo instrumentos. Componentes aplicables del SD: main function (si), process enablers (si, solo instrumentos), environment (si), purpose (no → outcome), problem occurrence (no)
- **Social**: DEBE modelarse con los 5 componentes completos. Se PUEDE usar state-specified enabling links para condiciones ambientales
- **Socio-tecnico**: DEBE modelarse con los 5 componentes completos. Se PUEDE usar tagged structural links para relaciones no fundamentales

### 5.1 Patrones de Referencia por Categoria

Los siguientes patrones sintetizan ejemplos pedagogicos recurrentes que conviene tener a mano al clasificar el sistema antes de construir el SD:

| Categoria | Patron de referencia | Leccion operativa |
|-----------|----------------------|-------------------|
| Artificial | `Airplane Flying`, `Battery Charging` | Hay purpose explicito, problem occurrence, agentes humanos y un benefit-providing object claramente identificable |
| Natural | `Fetus Developing`, `Rain Storm Forming` | Se modela outcome en vez de purpose; el outcome puede ser beneficial o detrimental; no hay agentes humanos |
| Social | `Conference Occurring` | Las condiciones ambientales PUEDE expresarse con state-specified enabling links, por ejemplo `good Weather` |
| Socio-tecnico | `Online Professional Identity Managing` | Tagged structural links suelen ser necesarios para relaciones no fundamentales, por ejemplo `Profile represents User` |
| Physical con partes informaticales | `Baggage Transporting` | Un sistema con tracking o software auxiliar SIGUE clasificandose como physical si la transformacion dominante es fisica |

## 6 Construccion del SD — Nivel 0

El SD DEBE ser simple y claro, con minimos detalles tecnicos. Todos los stakeholders DEBEN poder comprender el SD sin expertise tecnico.

### 6.0 Wizard Agnostico de Construccion del SD

El `wizard` del SD es un **protocolo de interaccion** agnostico de herramienta. No presupone OPCloud, formularios, UI grafica ni asistente LLM. Cualquier implementacion valida DEBE guiar al modelador por una secuencia ordenada de checkpoints y producir, al final, un SD semanticamente completo.

**Implementaciones validas:** entrevista guiada, formulario estructurado, checklist operativa, asistente conversacional, plugin de modelado o workflow humano moderado.

**Regla central:** cada etapa del wizard DEBE cerrar con un hecho del modelo explicitado y listo para representarse en OPD/OPL. El wizard NO termina cuando el usuario "entiende" el sistema; termina cuando los facts minimos del SD quedaron decididos.

**Pre-etapa obligatoria:** antes de iniciar el wizard, el modelador DEBE clasificar el sistema segun §5. La clasificacion determina si se habla de purpose u outcome y si `Problem Occurrence` aplica.

| Etapa | Objetivo | Output minimo obligatorio | Mapeo metodologico |
|-------|----------|---------------------------|--------------------|
| 0 | Clasificar sistema | Tipo: artificial / natural / social / socio-tecnico | §5 |
| 1 | Fijar proceso principal | Nombre canonico del main process | §6.1 |
| 2 | Identificar stakeholder primario | Beneficiary group o affectee equivalente | §6.2 |
| 3 | Fijar valor a transformar | Beneficiary/outcome attribute + input/output states | §6.3 |
| 4 | Fijar funcion principal | Benefit-providing object + atributo funcional, si aplica | §6.4 |
| 5 | Resolver agencia humana | Agent set valido o declaracion explicita de ausencia | §6.5 |
| 6 | Delimitar el sistema | Nombre del sistema + exhibition del proceso principal | §6.6 |
| 7 | Identificar enablers no humanos | Instrument set | §6.7 |
| 8 | Fijar transformees y resultados | Inputs, affectees y outputs | §6.8 |
| 9 | Delimitar contexto externo | Environment objects/processes | §6.9 |
| 10 | Modelar problema inicial, si aplica | Problem occurrence o decision explicita de no-aplicacion | §6.10 |
| 11 | Cerrar con gate de consistencia | Checklist SD `PASS/FAIL` | §6.11 |

**Semantica de cierre por etapa:**

- Si una etapa no puede cerrarse, el wizard DEBE retroceder a la etapa anterior que bloquea la decision.
- Si el sistema es **natural**, la etapa 10 DEBE cerrarse como `NO APLICA`, no como omision silenciosa.
- Si el sistema transforma multiples objetos, la etapa 4 DEBE dejar explicitado cual es el `Benefit-Providing Object`.
- Si no existen agentes humanos, la etapa 5 DEBE registrar `sin agentes humanos` en vez de forzar un placeholder.

**Contrato de salida del wizard:** un wizard agnostico correcto entrega, como minimo, un paquete de decisiones equivalente a:

1. tipo de sistema
2. proceso principal
3. beneficiary/affectee
4. atributo de valor + transicion de estados
5. funcion principal
6. agentes
7. sistema + exhibition
8. instrumentos
9. input/output set
10. environment
11. problem occurrence o no-aplicacion
12. verificacion SD

Una herramienta PUEDE dividir o fusionar etapas por conveniencia UX, pero NO DEBE perder ninguno de estos outputs semanticamente necesarios.

### 6.1 Paso 1: Identificacion del Proceso Principal

La forma del nombre depende del idioma de realizacion:

- En artefactos y modelos en **ingles**, el nombre del proceso DEBE terminar con verbo en forma gerundio (sufijo "-ing"), conforme a [OPM ISO 19450](urn:fxsl:kb:opm-iso-19450).
- En artefactos y modelos en **espanol**, el nombre del proceso DEBE encabezarse con infinitivo (-ar, -er, -ir) o con una nominalizacion verbal cuya primera palabra termine en `-ción`, conforme a [OPL-ES](urn:fxsl:kb:opm-opl-es) §1.1. La forma en `-miento` TAMBIEN PUEDE aceptarse cuando el dominio la exija.

**Correcto:** `Battery Charging`, `Airplane Flying`

**Incorrecto:** `Charge Battery`, `Fly Airplane`

En ingles, el nombre DEBERIA combinar el transformee seguido del verbo gerundio. En espanol, DEBERIA mantener la misma funcion nominal usando infinitivo o, cuando mejore la naturalidad terminologica del dominio, una forma encabezada por `-ción`.

### 6.2 Paso 2: Grupo Beneficiario

El nombre DEBE ser singular segun el Singular Name OPM Principle:

- En ingles: sufijo "Group" para humanos y "Set" para inanimados
- En espanol: sufijo "Grupo" para humanos y "Conjunto" para inanimados

El grupo beneficiario DEBE representarse como objeto fisico.

### 6.3 Paso 3: Atributo del Beneficiario y Estados

El modelador DEBE definir un atributo informatical del beneficiario con exactamente dos estados:
- **Estado input** (actual/problematico)
- **Estado output** (deseado/mejorado)

OPL: "[Main Process] changes [Beneficiary Attribute] of [Beneficiary Group] from [input] to [output]."

### 6.4 Paso 4: Funcion Principal

El modelador DEBE identificar el transformee principal (Benefit-Providing Object). DEBERIA agregar un Benefit-Providing Attribute cuyo valor cambia de problematico a satisfactorio.

Cuando el proceso transforma multiples transformees, solo el Benefit-Providing Object define la funcion. Otros transformees (consumidos/producidos) DEBEN modelarse pero NO son parte de la funcion.

### 6.5 Paso 5: Identificacion de Agentes

El termino "agent" y el agent link (black lollipop) DEBEN usarse exclusivamente para humanos o grupos humanos. Robots, software agents y sistemas IA DEBEN usar instrument link. Un robot PUEDE describirse como "embedded-software agent" en prosa, pero en el modelo DEBE usar instrument link.

Cuando el beneficiario es tambien agente del proceso, el modelador DEBE elegir el link segun la regla de colision de roles (§4.4): si el beneficiario es transformado, el effect link prevalece; el stick-figure preserva la identidad humana.

OPL: "[Agent] handles [Main Process]."

**Dual-role across different processes:** Un objeto PUEDE ser agent de un proceso y transformee de otro proceso distinto simultaneamente. Ejemplo: Learner es agent de MOOC Learning pero tambien transformee (Knowledge Level cambia). Esto es distinto de la colision agent-affectee del §4.4, que aplica al mismo proceso.

### 6.6 Paso 6: Naming del Sistema y Exhibition

El nombre default DEBERIA ser el nombre del proceso + "System" en ingles, o + "Sistema" cuando el modelo se realice completamente en espanol. El modelador PUEDE usar un nombre aceptado en su lugar.

El proceso principal DEBE modelarse como operacion del sistema via exhibition-characterization.

### 6.7 Paso 7: Identificacion de Instrumentos

El modelador DEBE identificar enablers no humanos requeridos durante toda la duracion del proceso. Cada instrumento DEBE conectarse via instrument link (white lollipop).

**Reclasificacion por desgaste:** Cuando el desgaste, degradacion o amortizacion de un instrumento es relevante al scope del sistema, el modelador DEBE reclasificarlo como affectee, agregando un atributo (ej: Amortization Level) que el proceso cambia. Se DEBE modelar un proceso de mantenimiento separado.

**Correcto:** Machine es affectee de Metal Cutting (Amortization Level cambia); Machine Maintaining es proceso separado.

**Incorrecto:** Machine es instrument de Metal Cutting cuando su desgaste es relevante al sistema (el mantenimiento queda oculto).

### 6.8 Paso 8: Objetos Input/Output

Cada objeto consumido DEBE conectarse via consumption link. Cada objeto creado DEBE conectarse via result link. Si un objeto es afectado (no consumido), DEBE conectarse via par input-output especificando la transicion de estados.

### 6.9 Paso 9: Objetos Environmentales

Los objetos environmentales DEBEN representarse con contorno dashed. Un mismo objeto PUEDE ser systemic en un modelo y environmental en otro.

### 6.10 Paso 10: Problem Occurrence

Para sistemas artificiales y sociales, el modelador DEBE modelar el problem occurrence — mirror image del purpose. Se DEBE agregar un proceso environmental que causa el estado problematico.

Para sistemas naturales, el problem occurrence NO DEBE modelarse.

### 6.11 Verificacion del SD

| Check | Condicion | Severidad |
|-------|-----------|----------|
| Purpose definido | Beneficiary + attribute + transicion estados | CRITICA |
| Funcion definida | Main process + main transformee | CRITICA |
| Enablers presentes | ≥1 agente o instrumento | ALTA |
| Environment identificado | ≥1 objeto environmental | MEDIA |
| Problem occurrence (si aplica) | Proceso environmental causa estado negativo | MEDIA |
| OPL legible | Sentencias OPL correctas | ALTA |
| Naming compliant | Gerundio + singular + Set/Group | ALTA |
| Exhibition | Sistema exhibe proceso como operacion | ALTA |
| Agents = humanos | Ningun instrument con agent link | ALTA |

## 7 Construccion de SD1 — Refinamiento Nivel 1

SD1 refina el SD exponiendo subprocesos y objetos asociados.

### 7.1 Refinamiento de Proceso Sincronico (In-Zooming)

Aplica cuando los subprocesos tienen un orden fijo y predefinido.

**Procedimiento:**
1. Crear nuevo OPD etiquetado SD1
2. Inflar el proceso principal en el centro
3. Agregar subprocesos verticalmente segun **Timeline OPM Principle** (primero arriba, ultimo abajo)
4. Cada subproceso DEBE estar conectado a al menos un transformee
5. Verificar aggregation-participation implicita por contencion grafica

**In-diagram vs new-diagram in-zooming:**

| Variante | Descripcion | Usar cuando |
|----------|-------------|-------------|
| In-diagram | Refineable aparece in-zoomed en el mismo OPD (no se crea OPD nuevo) | OPD tiene espacio suficiente; pocos subprocesos |
| New-diagram | Nuevo OPD descendiente; refineable con contour grueso en ambos OPDs | Caso prevalente; in-zooming requiere espacio sustancial |

**In-zooming semantics identity:** Cuando un proceso se in-zoomea, sus subprocesos = partes (aggregation-participation + orderability positiva), y los objetos que el proceso exhibe (via exhibition-characterization) = atributos del proceso. Objetos que ingresan al contexto por link migration mantienen su identidad independiente y NO son atributos del proceso. Simetricamente, cuando un objeto se in-zoomea: objetos internos = partes, procesos internos = operaciones del objeto.

**Paralelismo implicito:** Cuando dos o mas subprocesos tienen el borde superior de sus elipses a la misma altura, DEBEN interpretarse como ejecutandose en paralelo. El siguiente subproceso inicia cuando el ultimo de los paralelos termina. OPL usa la keyword `parallel` para expresar concurrencia.

**Correcto:** Subprocesos top-to-bottom; paralelos a la misma altura.

**Incorrecto:** Subprocesos fuera del proceso inflado; paralelos a alturas distintas sin intencion de secuencia.

### 7.2 Refinamiento de Proceso Asincronico (Unfolding)

Aplica cuando los subprocesos son independientes y PUEDEN ocurrir en cualquier orden.

**Four unfolding-folding pairs** (cada una corresponde a una relacion estructural fundamental):

| Relacion | Unfolding | Folding |
|----------|-----------|---------|
| Aggregation-participation | Expose parts of the whole | Hide parts |
| Exhibition-characterization | Expose features of the exhibitor | Hide features |
| Generalization-specialization | Expose specializations of the general | Hide specializations |
| Classification-instantiation | Expose instances of the class | Hide instances |

**Partial unfolding:** Cuando no todos los refinees se muestran, el non-comprehensiveness symbol indica que el unfolding es incompleto.

**Process unfolding use case:** Sistemas service-oriented y real-time con funciones paralelas o auxiliares independientes de la funcion core DEBERIAN usar unfolding en vez de in-zooming para process refinement.

**Decision rule — Aggregation vs Generalization:**

| Pregunta | Si → | No → |
|----------|------|------|
| ¿Cada subproceso es una variante/tipo del mismo patron de transformacion? | Generalization-specialization | Aggregation-participation |
| ¿El todo necesita todas las partes para funcionar? | Aggregation-participation | Generalization-specialization |

**Correcto:** Road Danger Warning → Vehicle Crash Alerting, Pedestrian Crash Alerting, Lane Deviation Alerting (son *tipos* de alerta → generalization).

**Incorrecto:** Usar aggregation para tipos/variantes (implica que el todo necesita todas las partes simultaneamente).

### 7.3 Refinamiento de Objetos

Los objetos se refinan via in-zooming (composicion espacial/estructural) y unfolding (taxonomias, features, instancias). In-zooming de objetos expone partes y operaciones (§7.1); unfolding expone refinees via las cuatro relaciones estructurales (§7.2). La posicion espacial de constituyentes en un object in-zooming PUEDE tener significado semantico (layout fisico, orden logico).

**Inner vs Outer Object Scoping:** Un objeto creado dentro de un proceso in-zoomed (inner object) existe solo en el scope de ese proceso y se elimina si el proceso padre se elimina. Un objeto creado a nivel SD (outer object) existe independientemente y es referenciable entre multiples OPDs. El modelador DEBE decidir el scope basandose en si la existencia del objeto depende del proceso (inner) o es independiente (outer). Mover un outer object dentro de un proceso inflado NO lo convierte en inner — el objeto retorna a su scope original al reposicionarlo (enveloping visual, no semantico).

### 7.4 Distribucion y Migracion de Links

| Tipo de link | Outer contour | Migracion default |
|-------------|---------------|-------------------|
| Agent link | PERMITIDO (distribuye a todos) | — |
| Instrument link | PERMITIDO (distribuye a todos) | — |
| Consumption link | PROHIBIDO | Migra al primer subproceso; reasignar |
| Result link | PROHIBIDO | Migra al primer subproceso; reasignar |
| Event link systemic | PROHIBIDO | — |

**Link migration procedure** (al hacer in-zooming):
1. Al dibujar el primer subproceso P1 dentro del proceso in-zoomed P, la herramienta DEBE mover automaticamente todos los procedural y control links de P a P1
2. Al agregar subprocesos subsiguientes, el modelador DEBE migrar transforming links de vuelta a P o al subproceso apropiado
3. Enabling links DEBEN migrarse a los subprocesos especificos donde el enabler es necesario
4. Links que aplican a todos los subprocesos DEBEN permanecer en el contour del proceso padre

**Implicit invocation links** (no visibles graficamente, implicitos por layout vertical):

| Tipo | Semantica |
|------|-----------|
| Process → first subprocess(es) | Control transferido al subproceso topmost al entrar al contexto in-zoomed |
| Subprocess → next subprocess(es) | Completion del source inicia el siguiente |
| Last subprocess → enclosing process | Control retorna al proceso in-zoomed tras completion del ultimo subproceso |

Cuando dos+ subprocesos tienen tops a la misma altura, inician en paralelo; sincronizacion: el ultimo en terminar inicia el siguiente.

**Antipattern — Event a subproceso no-primero:** El modelador NO DEBERIA conectar un event link a un subproceso que no sea el primero (topmost) dentro de un in-zoom, excepto si ha verificado que todos los subprocesos anteriores pueden omitirse sin dejar precondiciones insatisfechas. Conectar a un subproceso intermedio salta los anteriores, potencialmente dejando el sistema en estado inconsistente.

**Split state-specified transforming links:** Cuando `P changes A from s1 to s2` se hace in-zoom con P1 y P2, el modelo queda underspecified. Resolucion:
1. `P1 changes A from s1` (split input — saca A de s1)
2. `P2 changes A to s2` (split output — pone A en s2)

Links control-modified de split NO estan permitidos (saltear un subproceso de un split distorsionaria la semantica del efecto).

### 7.5 Expresion y Supresion de Estados

Los estados DEBERIAN suprimirse en el SD cuando no estan conectados a ningun proceso. Los estados DEBERIAN expresarse en SD1 donde se conectan a subprocesos.

**Estado indeterminado durante proceso activo:** Mientras un proceso affecting esta activo, el affectee esta "en transicion" entre input state y output state. Su estado es indeterminado y NO disponible para uso por otros procesos. Si el proceso se detiene prematuramente, el affectee permanece en estado indeterminado a menos que un exception handler lo resuelva.

### 7.6 Verificacion de SD1

| Check | Condicion | Severidad |
|-------|-----------|----------|
| Subprocesos transforman | Cada subproceso ≥1 transformee | CRITICA |
| Refinamiento correcto | Sync → in-zooming; async → unfolding | ALTA |
| Links distribuidos | Consumption/result NO en outer contour | CRITICA |
| Sin event a no-primero | Event links solo al primer subproceso (o justificacion explicita) | ALTA |
| Split links resueltos | Ningun effect link underspecified en in-zoom con multiples subprocesos | ALTA |
| Estados expresados | Estados relevantes visibles y conectados | ALTA |
| Sin redundancia | Sin duplicacion innecesaria de hechos del SD | MEDIA |

## 8 Gestion de Complejidad — Niveles 2+

### 8.1 Cuatro Mecanismos de Refinamiento-Abstraccion

| Mecanismo | Refinamiento | Abstraccion | Uso principal |
|-----------|-------------|-------------|---------------|
| In-zooming / Out-zooming | Expone contenido interno | Oculta contenido interno | Procesos sincronicos; objetos con partes espaciales |
| Unfolding / Folding | Expone refinees via relacion estructural | Oculta refinees | Procesos asincronicos; taxonomias; features |
| State Expression / Suppression | Muestra estados | Oculta estados irrelevantes | Simplificacion contextual |
| View Creating / Deleting | Ensambla hechos de varios OPDs | Elimina un View | Vistas transversales |

**Decision in-zooming vs unfolding para procesos sincronicos:** In-zooming DEBERIA preferirse porque: (a) requiere menos simbolos, (b) genera OPL mas corto, (c) reemplaza event/invocation links explicitos con invocacion implicita del timeline. Unfolding de procesos sincronicos es semanticamente equivalente pero mas verboso.

**Port Folding:** Especializacion de folding donde la operacion (proceso feature) se desplaza al contour del exhibitor (objeto). Util cuando el modelador quiere que los rectangulos de objetos representen layout fisico y tamanos relativos. OPL: keyword "as ports" al final de la sentencia de exhibition. Port folding tambien aplica a atributos de procesos.

**Semi-Folding:** Tecnica intermedia entre fold completo y unfold completo. Muestra nombres de partes dentro del container del objeto sin crear un OPD hijo. Un indicador numerico ("2 more") senala partes ocultas. El modelador DEBERIA usar semi-folding para inspeccion rapida de estructura sin proliferacion de OPDs.

Reglas adicionales:
- Views NO DEBEN editarse; la edicion ocurre en OPDs no-view
- El set completo de estados de un objeto es la union de estados en todos los OPDs

### 8.2 Organizacion del OPD Tree y Forest

Convention de etiquetado: SD, SD1, SD1.1, SD1.2, SD2, etc. El **System Map** muestra todos los things sin links, sirviendo como indice navegable.

**Regla de integridad del arbol:** Solo OPDs leaf (hojas terminales) PUEDEN eliminarse. OPDs internos estan protegidos para mantener la integridad del arbol de refinamiento. Intentar eliminar un nodo interno DEBE generar error.

**System Map:** OPD tree elaborado donde cada nodo es un icono miniaturizado del OPD, con flechas gruesas indicando refinamiento. Esencial para navegacion en modelos complejos (>10 OPDs). El modelador DEBERIA generar el system map para cualquier modelo con mas de un nivel de detalle.

**Ultimate OPD:** Representacion flat obtenida por flattening recursivo del OPD tree de abajo hacia arriba. No apta para consumo humano excepto en modelos muy pequenos; util para machine use (knowledge management, querying).

**Whole System Specification** — tres constructos complementarios:

| Constructo | Contenido |
|-----------|-----------|
| OPD model specification | Coleccion de OPDs sucesivos en orden breadth-first |
| OPL model specification | Coleccion de paragrafos OPL correspondientes, con sentencias duplicadas eliminadas |
| OPM model specification | Presentacion side-by-side: cada OPD con su paragrafo OPL a la derecha |

**Sub-Models para trabajo concurrente:** Cuando multiples modeladores trabajan en subsistemas simultaneamente, el modelador DEBERIA separar subsistemas en sub-models. Las conexiones entre el modelo principal y los sub-models DEBEN mantenerse minimas para reducir acoplamiento y conflictos de edicion concurrente.

### 8.3 Creacion de Vistas

Tipos: process tree, object tree, allocation view, simulation-motivated view.

### 8.4 Precedencia de Links durante Out-Zooming

| B↔P1 \ B↔P2 | Effect | Result | Consumption |
|-------------|--------|--------|-------------|
| **Effect** | Effect | Result | Consumption |
| **Result** | Result | Invalido | Effect |
| **Consumption** | Consumption | Effect | Invalido |

**Orden de precedencia primario:** consumption = result > effect > agent > instrument.

**Orden completo (12 niveles, de mayor a menor semantic strength):**

1. consumption event
2. consumption = result (sin modifier)
3. result > consumption condition
4. consumption condition > effect event
5. effect event > effect (sin modifier)
6. effect > effect condition
7. effect condition > agent event
8. agent event > agent (sin modifier)
9. agent > agent condition
10. agent condition > instrument event
11. instrument event > instrument (sin modifier)
12. instrument > instrument condition

**Secondary precedence** (dentro de cada kind): event > non-control > condition. Event links llevan semantica del non-control link + process initiation. Condition modifiers debilitan criterios de satisfaccion de precondicion. State-specified links tienen precedencia sobre basic links del mismo tipo.

### 8.5 Practica Middle-Out y Simplificacion

**Middle-out**: el modelador comienza por el nivel que mejor entiende y refina/abstrae en ambas direcciones.

**Procedimiento de simplificacion de OPD sobrecargado:**
1. Identificar conjunto TO de things a extraer
2. Nombrar un nuevo proceso interino que los contenga
3. Ejecutar in-diagram out-zooming (link abstracting + content hiding)
4. Crear nuevo OPD descendiente con los hechos extraidos
5. Renumerar OPDs hijos afectados

Reduccion neta: procesos_removidos + objetos_removidos + links_removidos - 1 (el proceso interino agregado).

**Depth-first traversal para documentos complejos:** Al modelar estandares, regulaciones o documentos extensos, el modelador DEBERIA seguir una estrategia depth-first: profundizar completamente en una seccion/clausula antes de avanzar a la siguiente. Esto contrasta con breadth-first y permite descubrir inconsistencias locales mas rapidamente.

**Object-process disconnect bridging:** Documentos y estandares frecuentemente separan la descripcion de objetos (estructura) de la descripcion de procesos (comportamiento) en clausulas independientes sin integracion. El modelador DEBE conectar ambas vistas usando OPM, enlazando cada proceso con los objetos que transforma. Esta integracion revela gaps y objetos implicitos que el texto omite.

### 8.6 Emergencia como Criterio de Validacion Arquitectural

El modelador DEBE verificar que la arquitectura del sistema (structure + behavior) produce al menos una capacidad emergente — una funcionalidad que el sistema completo exhibe pero ninguna parte individual posee. Si no existe emergencia, la coleccion de partes no constituye un sistema en el sentido MBSE.

### 8.7 Gobernanza del Modelo

**Ontology Enforcement:** Para consistencia terminologica en equipos, el modelador DEBERIA configurar enforcement de ontologia organizacional en tres niveles:

| Nivel | Comportamiento |
|-------|---------------|
| None | Sin restriccion terminologica |
| Suggest | Sugiere termino estandar; el modelador puede ignorar |
| Enforce | Impide terminos no estandarizados |

**Model Informativeness Grading:** Las sentencias OPPL se clasifican en: Definition, Structural, Procedural, Meta, Unknown. Metricas: informative level, weighted score, INF average, total OPPL sentences. El modelador DEBERIA ejecutar grading periodicamente para identificar precedence links faltantes y procesos sin inputs/outputs.

**Version Comparison:** El modelador DEBERIA comparar versiones del modelo para tracking de mejoras y deteccion de regresiones. El diff entre versiones revela hechos agregados, modificados o eliminados.

**Name Coherency:** Ante nombres duplicados, el modelador DEBE resolver con una de tres opciones: (1) usar existing thing — crea visual instance (mismo thing, diferente vista en otro OPD), (2) renombrar con nombre unico, (3) descartar. La opcion "close" sin resolver NO DEBERIA usarse. Visual instances solo PUEDEN crearse entre elementos del mismo tipo (object→object, process→process).

### 8.8 Operaciones de Gestion del Modelo en OPCloud

Las siguientes capacidades son relevantes para el ciclo de vida del modelo, pero no alteran la semantica OPM:

- **Persistencia:** el modelador DEBERIA tratar Save/Load como operaciones regulares de checkpoint durante sesion. Share expone el modelo a otros usuarios con permisos read o edit.
- **Permisos:** el owner/admin PUEDE compartir con usuarios o grupos completos, pero NO entre organizaciones distintas. Read precede a write. El modelador DEBERIA verificar permisos antes de colaboracion concurrente.
- **Exportacion:** OPL puede exportarse con o sin numeracion. Los OPDs pueden exportarse como imagen o PDF, ya sea para el OPD actual, el arbol completo o solo el SD. Los exports DEBEN tratarse como snapshots publicables, no como SSOT del modelo.
- **Templates:** OPCloud soporta templates Private, Organizational y Global. Insertar un template crea una copia local; las actualizaciones posteriores del template fuente NO se propagan a las inserciones ya hechas.
- **Reubicacion del modelo:** mover modelos via cut/paste conserva auto-save e historial de versiones. El modelador DEBERIA revisar versiones antes y despues de mover o fusionar trabajo.
- **Busqueda y navegacion asistida:** operaciones como search, bring connected y filtered bring DEBERIAN usarse para inspeccion localizada de un subgrafo antes de editar, especialmente en modelos con alta densidad de links.

## 9 Heuristicas de Modelamiento Avanzado

### 9.1 State-Preserving Process → Tagged Structural Link

Cuando un proceso mantiene un objeto en su estado actual sin transformarlo (Supporting, Holding, Maintaining, Keeping, Storing, Containing, Connecting), el modelador DEBERIA reemplazarlo con un tagged structural link.

**Rationale:** Los procesos state-preserving violan la definicion fundamental de proceso como "thing que transforma un objeto". El tagged structural link es mas compacto y expresa la naturaleza time-invariant de la relacion.

**Correcto:** `Foundation supports House.` (tagged structural link, una sentencia OPL)

**Incorrecto:** Supporting como proceso explicito con Foundation como instrument y House como affectee (multiples links, OPL mas complejo, contradice definicion de proceso)

**Excepcion:** Si mantener el estado requiere esfuerzo no trivial (ej: helicopter hovering requiere propulsion activa), el modelador DEBE modelar el proceso explicitamente.

### 9.2 Transient Object → Invocation Link

Cuando un proceso crea un objeto que el siguiente proceso consume inmediatamente sin intervencion, el modelador DEBERIA suprimir el objeto transiente y reemplazar la creation-consumption pair con un invocation link (forma de rayo).

**Correcto:** `Object Detecting invokes Threat Assessing.` (invocation link, Spark suprimido)

**Incorrecto:** Mantener Detection Signal como objeto explicito cuando nunca es observado ni transformado por otro proceso.

### 9.3 Dualidad Estructural

Los patterns §9.1 y §9.2 son duales: tagged structural links suprimen procesos state-preserving innecesarios; invocation links suprimen objetos transientes innecesarios. El modelador DEBE aplicar ambos consistentemente.

### 9.4 Role Shift entre Niveles de Detalle

Un objeto PUEDE ser instrument en un nivel abstracto (ej: SD) y affectee en un nivel detallado (ej: SD1), siempre que el estado inicial y final sean iguales en el nivel abstracto (cambio neto = cero).

**Correcto:** Dishwasher es instrument de Dish Washing en SD. En SD1: Loading cambia Dishwasher de empty a loaded; Unloading cambia de loaded a empty (neto = sin cambio → instrument valido en SD).

**Incorrecto:** Declarar un objeto como instrument en SD cuando su estado neto cambia en SD1 (debe ser affectee en ambos niveles).

### 9.5 Arbol de Decision de Propiedades de Atributos

Al definir un atributo, el modelador DEBERIA clasificarlo en cuatro dimensiones binarias:

| Dimension | Valores | Criterio |
|-----------|---------|----------|
| Explicitness | explicit (default) / implicit | ¿Es un objeto separado? |
| Mode | qualitative (default) / quantitative | ¿Valores numericos? |
| Touch | hard (default) / soft | ¿Computable desde otros atributos? |
| Emergence | inherent (default) / emergent | ¿Al menos una parte lo exhibe? |

Atributos soft son derivables → PUEDEN no requerir tracking independiente. Atributos emergent existen solo a nivel del todo → definen la arquitectura del sistema.

### 9.6 Link Homogeneity

Structural links DEBEN ser homogeneos (object↔object o process↔process). Procedural links DEBEN ser non-homogeneous (object↔process). Unica excepcion: exhibition-characterization permite las 4 combinaciones de perseverance (object exhibe attribute-object, object exhibe operation-process, process exhibe attribute-object, process exhibe operation-process).

### 9.7 State-Specified Tagged Structural Links

Cuando un estado de un objeto corresponde o se asocia con otro objeto, el modelador DEBERIA usar un state-specified tagged structural link (conectando el estado al objeto asociado) en vez de crear procesos o objetos intermedios.

### 9.8 Discriminating Attributes y State-Specified Characterization

Cuando las especializaciones se distinguen por un valor de atributo, el modelador DEBERIA usar un discriminating attribute con state-specified characterization links. Esto produce un OPD significativamente mas compacto que repetir el atributo para cada especializacion.

### 9.9 Alcance de Herencia OPM

Cada especializacion DEBE heredar del general: (1) todas las partes (aggregation), (2) todos los features (exhibition), (3) todos los tagged structural links, (4) todos los procedural links. Los estados tambien se heredan. Una especializacion PUEDE override estados heredados especificando estados propios.

### 9.10 Relatividad de Instancia y Visual vs Logical Instances

"Instance" es relativo al sistema de discurso. Lo que es instancia en un sistema (ej: "Taurus 2015" en comparacion de autos) PUEDE ser clase con especializaciones en otro sistema (ej: autos individuales con VIN en un concesionario).

**Visual Instance vs Logical Instance:** Una visual instance es el mismo thing representado en diferentes OPDs (misma identidad, diferente vista). Una logical instance es una relacion classification-instantiation (clase → instancia). El modelador NO DEBE confundir ambas. Visual instances solo PUEDEN crearse entre elementos del mismo perseverance (object↔object, process↔process; object→process prohibido).

### 9.11 Clasificacion de Essence para Things Mixtos

Cuando un thing tiene partes physical e informatical, el modelador DEBE clasificarlo como **physical**. La esencia dominante del componente tangible prevalece. Ejemplo: Baggage Transporting system tiene componentes informaticales (location tracking) pero se clasifica como physical porque el proceso involucra transporte fisico.

### 9.12 Direct States vs Attribute + Values (Simplificacion)

Cuando un objeto tiene un solo atributo relevante, el modelador PUEDE simplificar el modelo asignando los valores del atributo como **estados directos del objeto**, eliminando el atributo intermedio.

**Correcto (simplificado):** `Fetus can be embryo or baby.` (estados directos del objeto)

**Correcto (completo):** `Fetus exhibits Developmental Stage. Developmental Stage of Fetus can be embryo or baby.` (atributo + valores)

**Decision rule:** Usar la forma simplificada cuando el objeto tiene un solo atributo relevante al scope del modelo y la legibilidad mejora. Usar la forma completa cuando el objeto tiene multiples atributos o cuando el nombre del atributo agrega informacion semantica no obvia.

### 9.13 Generalizacion como Abstraccion del SD

Cuando multiples objetos especificos del SD1 compartirían el mismo tipo de relacion con el proceso principal en el SD, el modelador DEBERIA crear un objeto general que los englobe y agregar solo ese objeto al SD, manteniendo los especificos en SD1.

**Correcto:** Road Danger Representation (general) en SD; Vehicle-in-Front Representation, Pedestrian-in-Front Representation, Lane Set Representation (especificos) en SD1 conectados via generalization-specialization.

**Incorrecto:** Las tres representaciones especificas en SD (overcrowding del diagrama top-level).

### 9.14 Making Implicit Objects Explicit

Al modelar sistemas a partir de texto (standards, regulaciones, especificaciones), el modelador DEBE identificar y modelar explicitamente los objetos que el texto menciona implicitamente. En documentos process-oriented, los objetos transformados por los procesos frecuentemente no se nombran. El acto de forzar la pregunta "¿que objeto transforma este proceso?" revela entidades criticas omitidas por el autor del texto.

### 9.15 Synonym/Homonym Detection via Modelamiento Formal

OPM fuerza un mapping 1:1 entre things y nombres. El modelador DEBE usar este formalismo para detectar: (a) **sinonimos** — multiples palabras para el mismo concepto (ej: "purpose" vs "stated purpose" en ISO 15288), y (b) **homonimos** — misma palabra para conceptos distintos (ej: "environment" vs "operational environment"). Cada sinonimo detectado DEBE resolverse eligiendo un termino canonico. Cada homonimo DEBE resolverse creando things separados con nombres distintos.

### 9.16 Text-Diagram Inconsistency Detection

El modelamiento OPM de un documento existente produce como byproduct la deteccion de inconsistencias entre el texto principal y sus diagramas. El modelador DEBERIA documentar estas inconsistencias como hallazgos de calidad. Ejemplo: en ISO 15288, boxes representan "systems" en un diagrama y "processes" en otro, sin justificacion. El modelo OPM resuelve estas ambiguedades asignando perseverance correcto (object vs process) a cada thing.

### 9.17 Clause-Referenced OPD Naming

Al modelar documentos normativos, el modelador DEBERIA etiquetar los OPDs con las clausulas del documento fuente (ej: `[5.2.2] System`, `[6.1] Acquisition`). Esto permite trazabilidad directa entre el modelo y el texto fuente, facilita revision por pares, y soporta validacion de cobertura.

## 10 Control de Flujo Avanzado

### 10.1 Wait vs Skip — Condition vs Non-Condition Links

| Tipo de link | Si el objeto/estado esta ausente | Uso |
|-------------|----------------------------------|-----|
| Non-condition (sin `c`) | Proceso ESPERA indefinidamente | Proceso obligatorio — el sistema se detiene |
| Condition (con `c`) | Proceso se SALTA | Proceso opcional — la ejecucion avanza |

**Regla de decision:** Usar condition link cuando el proceso es opcional; usar non-condition link cuando es obligatorio. Error comun: usar non-condition link para un recurso que puede no aparecer → deadlock.

### 10.2 Precedencia de Skip sobre Wait

Cuando el preprocess object set contiene tanto condition links como non-condition links, skip DEBE tener precedencia sobre wait. Si cualquier condition-linked object/estado esta ausente, el proceso se salta independientemente de la satisfaccion de los non-condition links.

### 10.3 Semantica de Event Links (OR) vs Condition Links (AND/OR)

- **Multiples event links** al mismo proceso: semantica OR (cualquier evento individual basta para trigger)
- **Multiples condition links** al mismo proceso: semantica AND para ejecucion (todos deben cumplirse) pero semantica OR para skip (falla de cualquiera causa skip)

### 10.4 XOR vs OR Link Fans

| Fan | Simbolo | Semantica | Uso |
|-----|---------|-----------|-----|
| XOR | Arco dashed simple | Exactamente uno de los paths | Decisiones mutuamente excluyentes |
| OR | Arco dashed doble | Al menos uno de los paths | Concurrencia condicional |

Para fan size f=2: XOR usa "either...or"; para f>2: "exactly one of." OR siempre usa "at least one of."

### 10.5 XOR/OR Combinatorial (m-de-f)

Para f > 2, el modelador PUEDE generalizar: "exactly m of f" (XOR combinatorial) o "at least m of f" (OR combinatorial), donde m < f. El numero m se registra junto al arco en el OPD. Modela escenarios como "2 de 3 key holders deben estar presentes."

### 10.6 NOT via Existent/Non-Existent

OPM no tiene simbolo NOT dedicado. Para modelar "proceso P ejecuta solo cuando objeto S esta ausente," el modelador DEBERIA crear estados implicitos `existent` y `non-existent` para S, y conectar `non-existent` a P con instrument link o condition instrument link.

### 10.7 Path Labels para Disambiguation de Escenarios

Cuando un proceso tiene multiples links procedurales entrantes y salientes y se necesita especificar cual input mapea a cual output, el modelador DEBE usar path labels. El link seguido a la salida es el que tiene el mismo label que el link de entrada. Path labels proveen memoria entre input y output y eliminan el requisito AND para preprocess objects: solo objetos con el mismo label deben coexistir.

### 10.8 Patrones de Iteracion

**Patron Set-Member:** Adjuntar dos procedural links del mismo tipo a un proceso — uno a un set de n miembros y otro a un miembro — produce iteracion automatica n veces.

**Patron Loop:** Un invocation link desde el ultimo subproceso hacia el proceso padre in-zoomed crea un loop. Para intervalos entre iteraciones, insertar un proceso Waiting con time constraints.

**Patron Decision-Node:** Para iteracion con condicion de terminacion, usar un boolean decision node que evalua despues de cada ciclo; si "No," invocation link loopea; si "Yes," la ejecucion avanza al siguiente subproceso.

### 10.9 Semantica Temporal de Transforming Links

| Tipo | Timing de transformacion |
|------|-------------------------|
| Consumption | Inmediata al inicio del proceso. Consumee deja de existir tan pronto el proceso se activa. Si el consumee no existe, el proceso espera |
| Result | Creacion solo al termino del proceso. Durante la ejecucion, ni consumee (ya consumido) ni resultee (aun no creado) existen |
| Effect | Affectee sale del input state al inicio del subprocess que lo afecta; entra al output state al completion de ese subprocess. Entre ambos puntos, el objeto esta "en transicion" — estado indeterminado |

Esta semantica temporal es critica para simulacion y para entender la disponibilidad de objetos entre subprocesos.

### 10.10 Boolean Objects y Branching

Un **Boolean object** es un objeto informatical dual-state generado por un proceso de decision. Sus estados forman un par Boolean (yes/no, true/false, pass/fail, approved/denied, `geq-x`/`lt-x`). Cada estado se conecta via condition links a procesos alternativos subsiguientes, implementando control if-then-else.

**Generalizacion:** Cualquier objeto con n estados funciona como un case statement — cada estado PUEDE servir como source de condition o instrument link para un proceso subsiguiente distinto.

### 10.11 Scenarios y Behavioral Repertoire

Un **scenario** (thread of execution) es un path especifico a traves de la jerarquia de procesos del sistema, trazado siguiendo el estado de cada objeto. En cada branching point (Boolean object, condition links, XOR fan), exactamente un path se materializa. El conjunto completo de scenarios constituye el **behavioral repertoire** del sistema — la totalidad de comportamientos posibles.

### 10.12 Condition Transforming Links (Taxonomy Completa)

| Link | Semantica | OPL |
|------|-----------|-----|
| Condition consumption | Si consumee existe, proceso lo consume; si no, skip | `Process occurs if Object exists, in which case Process consumes Object, otherwise Process is skipped` |
| Condition effect | Si affectee existe, proceso lo afecta; si no, skip | `Process occurs if Object exists, in which case Process affects Object, otherwise Process is skipped` |
| Condition agent | Si agent existe, proceso opera con agent; si no, skip | `Agent handles Process if Agent exists, otherwise Process is skipped` |
| Condition instrument | Si instrument existe, proceso opera; si no, skip | `Process occurs if Instrument exists, else Process is skipped` |

Cada uno de estos TIENE version state-specified (proceso opera si objeto esta en estado especifico; si no, skip).

### 10.13 Value-Specified Procedural Links

| Link | Semantica |
|------|-----------|
| Value setting link | Unidirectional; establece valor de atributo independiente del valor previo |
| Value effect link | Bidirectional; cambia valor de atributo de uno no especificado a otro |
| In-out-specified value effect link pair | Cambia valor de atributo de input value especifico a output value especifico |

Estos links aplican a **values** (estados de atributos), no a estados de objetos no-atributo.

### 10.14 Probabilistic Fans

En un XOR diverging fan probabilistico, cada link DEBE anotarse con una probabilidad. La suma de todas las probabilidades DEBE ser exactamente 1. Default sin fan: si un proceso crea un objeto con n estados, cada estado tiene probabilidad 1/n.

## 11 Manejo de Errores Temporales

### 11.1 Overtime Exception Links

Cuando un proceso tiene Maximal Duration, el modelador DEBERIA adjuntar un overtime exception link a un proceso de manejo de overtime. Si el proceso excede su tiempo maximo, el exception handler se activa y resuelve los objetos en transicion a estados permisibles.

### 11.2 Undertime Exception Links

Cuando un proceso tiene Minimal Duration, el modelador DEBERIA adjuntar un undertime exception link. Si el proceso se completa antes del minimo (o es skipped, duracion = 0), el undertime handler se activa.

**Pattern — Undertime como detector de skip:** Un undertime exception link en un proceso con duracion minima detecta cuando el proceso no se ejecuto (duracion efectiva = 0 < minimo positivo), activando recovery logic. Esto provee un mecanismo formal para "proceso no ejecutado."

### 11.3 Resolucion de Estado Indeterminado

Todo affectee en transicion durante un proceso activo permanece en estado indeterminado si el proceso falla. Los exception handlers (overtime/undertime) DEBEN resolver el objeto a un estado permisible. Sin exception handling, el objeto queda indefinido y el modelo es incompleto para simulacion.

## 12 Modelamiento Cuantitativo y Simulacion

### 12.1 Transformation Rate

Cuando consumo, creacion, o cambio de estado ocurre como flujo continuo o operacion multi-unidad en el tiempo, el modelador DEBERIA asignar una propiedad Transformation Rate al procedural link relevante. Tres especializaciones: consumption rate, yield rate, effect rate.

### 12.2 Computing with OPM — Claridad de Roles de Operandos

Cuando se modelan operaciones aritmeticas no conmutativas (Dividing, Subtracting), el modelador DEBE designar explicitamente los roles de operandos (Dividend vs Divisor, Minuend vs Subtrahend). OPM embebe formulas en nombres de proceso (ej: `Residue Computing (residue=il-u)`) para compactness.

### 12.3 Duration Distribution para Simulacion Estocastica

El modelador PUEDE especificar una Duration Distribution en la propiedad Duration de un proceso, identificando una funcion de distribucion de probabilidad. En runtime, cada instancia del proceso muestrea su duracion independientemente. Sin Duration Distribution, todas las instancias ejecutan en exactamente la Expected Duration (irrealista para sistemas reales).

### 12.4 Workflow Computacional en OPCloud

Cuando se implemente el modelo en OPCloud, el modelador DEBE seguir este patron de 5 pasos:

1. **Definir objetos** con atributos computacionales (tipo: integer, float, string, character, boolean)
2. **Asignar alias** a cada atributo computacional (ej: "x1", "y1") para uso en formulas
3. **Crear proceso de calculo** — representado con braces `{}` en el OPD, indicando naturaleza computacional
4. **Definir formula** usando los aliases (ej: `slope = (y2-y1)/(x2-x1)`)
5. **Conectar proceso** a objetos via consumption/effect links para flujo de datos

**Stereotypes en OPCloud:** Templates de parametros reutilizables para patrones computacionales comunes. La herramienta distingue niveles Global y Organizational. Al remover un stereotype de un thing, el modelador DEBE elegir entre unlink (conservar componentes) o unlink-and-remove (eliminar componentes agregados).

### 12.5 Range Validation

El modelador DEBERIA asignar rangos a atributos computacionales para enforcement durante simulacion. Sintaxis: `[inclusive`, `(exclusive`. Multiples rangos: `[1,10][20,30]`. El sistema valida automaticamente que los valores permanezcan en rangos validos.

### 12.6 User Input Simulation Workflow

Para simulacion con entrada de usuario en OPCloud, el modelador DEBE seguir estos 6 pasos:

1. Crear usuario como objeto fisico
2. Conectar usuario al proceso via **agent link**
3. Marcar proceso para recibir user input durante simulacion
4. Crear objeto input computacional para recibir valores
5. Conectar proceso al objeto input via **effect link** (requerido para actualizar objetos computacionales con valores de usuario)
6. En la computacion, usar funcion **User Input** del API predefinido

Sin los pasos 5-6, el objeto input no recibira valores durante simulacion.

### 12.7 Operational Semantics en Contextos In-Zoomed

Ejecutar un proceso con contexto in-zoomed transfiere control recursivamente al subproceso topmost del nivel mas profundo. El control retorna al proceso in-zoomed tras completion del ultimo subproceso.

**Transformaciones del Involved Object Set por instancia:**

| Tipo de transformee | Timing de transformacion |
|---------------------|-------------------------|
| Consumee | Deja de existir al inicio del deepest subprocess que lo consume |
| Affectee | Sale del input state al inicio del deepest subprocess que lo cambia; entra al output state al completion de ese (o subsiguiente) subprocess |
| Resultee | Creado al completion del deepest subprocess que lo genera |

Un objeto stateful en transicion: ha dejado su input state pero aun no ha llegado al output state (duracion positiva). Durante este periodo, el objeto es indisponible para otros procesos.

### 12.8 Compound State Space y Precondiciones Compuestas

El state space de un objeto es el producto cartesiano de los sets de estados de todos sus atributos y partes stateful. El modelador DEBE reconocer que no todos los puntos del state space son factibles; los compound states infeasibles DEBERIAN identificarse mediante process modeling. Para precondiciones compuestas que abarcan multiples atributos, el modelador DEBE usar multiple condition clause OPL sentences con clausulas X-OR numeradas conectadas por AND logico.

### 12.9 Integracion Externa e Ingesta de Datos en OPCloud

Cuando el modelo deja de ser solo conceptual y debe intercambiar datos con entorno externo, el modelador PUEDE usar las siguientes capacidades:

- **MQTT:** adecuado para sensores/actuadores IoT con topicos publish/subscribe. Requiere configurar raw server y MQTT server. El modelador DEBERIA usarlo para acoplar variables computacionales a telemetria o comandos ligeros.
- **ROS:** adecuado para robots y sistemas con ROS master. El workflow minimo DEBE incluir definicion de mensaje, publicacion, suscripcion y manejo del feedback loop via condiciones/iteracion.
- **CSV Import para atributos:** util para carga masiva de instancias y valores de atributos. Restriccion: el objeto target NO DEBE ser una instancia conectada via classification-instantiation. El modelador DEBERIA previsualizar el import y decidir si ignora existentes o crea atributos faltantes.

## 13 Requirements Modeling en OPCloud

En este corpus, el modelamiento de requirements se trata como una capacidad de OPCloud, no como una extension normativa independiente de OPM. Por lo tanto, las siguientes reglas aplican solo cuando el modelo se implementa en OPCloud.

### 13.1 Operaciones Disponibles

OPCloud permite agregar, remover y visualizar requirements sobre elementos, links o diagramas completos. Las relaciones recuperables en el tutorial son:

- Exhibition
- Characterization
- Aggregation Participation

### 13.2 Convencion de Trazabilidad

Cuando se use trazabilidad de requirements en OPCloud, el tagged structural link con tag **"satisfies"** DEBERIA usarse como convencion de trazabilidad entre artefacto y requirement.

**Correcto:** `Seat satisfies RQ1 Driver Seat.`

**Incorrecto:** Conectar requirements a artifacts via procedural links (los requirements no transforman ni habilitan procesos; la relacion es estructural).

### 13.3 Ejemplo Minimo

Ejemplo recuperable desde el tutorial:

- Door-Peephole: peephole como parte de door
- Restricciones dimensionales: 56-64 inches
- Componentes: lens + sleeves
- Componente opcional: peephole cover
- Funcion: one-way view for seeing visitors

### 13.4 Analisis de Gaps y Generacion Asistida

OPCloud ofrece capacidades auxiliares que el modelador PUEDE usar para detectar vacios y acelerar derivacion de requirements:

- **Identification of Missing Knowledge:** DEBERIA usarse como heuristica de deteccion de gaps, no como verdad del modelo. `Pistol` sirve para filtrado rapido; `RGCN`, cuando este disponible, ofrece mayor precision. El umbral de confianza DEBERIA ajustarse explicitamente antes de aceptar sugerencias.
- **AI Requirements Generation:** toma OPPL como insumo y genera texto de requirement, verification type, acceptance criteria y model triplets. La salida DEBE revisarse manualmente antes de integrarla al corpus o al modelo.
- **Version comparison:** el modelador DEBERIA comparar resultados del analisis entre versiones sucesivas para distinguir mejoras reales de ruido introducido por cambios de layout o renaming.

## 14 Simulacion y Ejecucion del Modelo

### 14.1 Depth-First OPD Tree Traversal para Ejecucion

La ejecucion animada del modelo OPM sigue un recorrido **depth-first** del OPD tree. Los tokens fluyen a lo largo de los links: al llegar a un proceso in-zoomed, el control se transfiere recursivamente al subproceso mas profundo (topmost del nivel mas bajo). El control retorna al nivel padre tras completar el ultimo subproceso.

Los tokens se visualizan como valores que se pasan entre objetos y procesos: consumed (eliminado del source), instrument (read-only, permanece), resultee (creado en destination). Tokens computacionales llevan valores numericos.

### 14.2 Transition Conceptual → Computational

El modelador DEBE reconocer el punto en el OPD tree donde la transicion de modelamiento conceptual puro a modelamiento computacional es necesaria. Indicadores:

- Los valores numericos especificos se vuelven necesarios para decision de diseno
- Trade-off studies requieren parametros cuantitativos
- El proceso fisico tiene una formula matematica subyacente (ej: V = V0 - (F/m)*t)

En este punto, el modelador DEBE convertir procesos conceptuales a procesos computacionales y usar la realizacion soportada por la herramienta. En OPCloud, la senal visual recuperable es el uso de `{}` en el OPD.

### 14.3 Simulacion Conceptual vs Ejecucion Computacional en OPCloud

El modelador DEBE distinguir entre:

- **Simulacion conceptual:** animacion visual del flujo de tokens para validar orden, precondiciones y cobertura del comportamiento
- **Ejecucion computacional:** corrida efectiva de formulas, atributos computacionales y actualizacion de valores

Reglas operativas:

- La velocidad de animacion DEBERIA ajustarse para hacer visibles procesos rapidos o loops
- Si el orden observado no coincide con el esperado, el modelador DEBE revisar altura relativa de subprocesos, links de control y condiciones
- Los tokens computacionales transportan valores; los conceptuales solo evidencian disponibilidad, consumo, creacion o cambio de estado

## 15 Invariantes

Los invariantes se verifican operativamente en §16, donde se organizan por nivel con severidad asignada.

| Invariante | Enforcement |
|-----------|-------------|
| Nombre del proceso principal termina en gerundio (EN) o se encabeza por infinitivo / `-ción` / `-miento` valido (ES) | lint |
| Todos los nombres de things son singulares | lint |
| Grupo beneficiario es objeto fisico | lint |
| Atributo del beneficiario es objeto informatical | lint |
| Exactamente un proceso principal por SD | schema |
| Agent links solo conectan a humanos (exclusividad) | manual |
| Instrument links solo conectan a no humanos | manual |
| Todo enabler persiste sin cambio neto tras el proceso | manual |
| Objetos environmentales tienen contorno dashed | lint |
| Sistema exhibe proceso principal via exhibition-characterization | manual |
| Consumption/result links NO en outer contour de proceso in-zoomed | lint |
| Todo subproceso conectado a al menos un transformee | lint |
| Modelo bimodal: todo OPD tiene paragrafo OPL equivalente | schema |
| Un hecho del modelo aparece en al menos un OPD | schema |
| Structural links son homogeneos (excepcion: exhibition-characterization) | lint |
| Enablers y affectees pertenecen a Pre(P) ∩ Post(P); consumees solo a Pre(P); resultees solo a Post(P) | manual |
| Probabilidades en fan XOR suman exactamente 1 | lint |
| Subprocesos paralelos tienen borde superior de elipse a la misma altura | manual |
| Split links control-modified NO estan permitidos | lint |
| Arquitectura del sistema produce al menos una capacidad emergente | manual |
| Links NO DEBEN cruzar areas ocupadas por things | manual |
| Things NO DEBEN ocultarse mutuamente (excepcion: port folding) | manual |
| Minimizar numero de links y cruces de links en cada OPD | manual |
| Si se usan requirements en OPCloud, la trazabilidad usa links estructurales y la convencion "satisfies" | manual |
| En OPCloud, procesos computacionales se distinguen visualmente con `{}` en el OPD | lint |
| Sinonimos resueltos: un thing = un nombre canonico | manual |

## 16 Checklist de Validacion

Todos los invariantes de §15 DEBEN verificarse en el nivel aplicable. Esta tabla lista checks operativos adicionales organizados por nivel.

| Nivel | Check | Condicion | Severidad |
|-------|-------|-----------|----------|
| SD | Sistema clasificado | Tipo determinado (artificial/natural/social/socio-tecnico) | CRITICA |
| SD | Purpose/outcome definido | Beneficiary + attribute + transicion estados | CRITICA |
| SD | Funcion definida | Main process + main transformee | CRITICA |
| SD | Enablers presentes | ≥1 agente o instrumento | ALTA |
| SD | Environment identificado | ≥1 objeto environmental | MEDIA |
| SD | Problem occurrence (si aplica) | Proceso environmental causa estado negativo | MEDIA |
| SD | Instrument reclassification | Instrumentos con desgaste relevante reclasificados a affectee | MEDIA |
| SD1 | Refinamiento correcto | Sync → in-zooming; async → unfolding | ALTA |
| SD1 | Sin event a no-primero | Event links no a subprocesos intermedios (o justificacion) | ALTA |
| SD1 | Split links resueltos | Ningun effect link underspecified en in-zoom multi-subprocess | ALTA |
| SD1 | Estados expresados | Estados relevantes visibles y conectados | ALTA |
| SD1 | Tipo async correcto | Aggregation para partes; generalization para tipos | ALTA |
| SD1 | Sin redundancia | Sin duplicacion innecesaria de hechos del SD | MEDIA |
| SD2+ | Precedencia links | Out-zooming aplica matriz de precedencia | ALTA |
| SD2+ | OPD tree valido | Etiquetado secuencial correcto | MEDIA |
| SD2+ | Role shift coherente | Instrument en abstract = affectee en detail solo si cambio neto = 0 | ALTA |
| Quant | Operandos explicitos | Operaciones no conmutativas con roles designados | MEDIA |
| Quant | Computational workflow | Atributos computacionales con tipo, alias y formula | MEDIA |
| Quant | Range validation | Rangos definidos para atributos con dominio acotado | MEDIA |
| Error | Exception handlers | Procesos con time bounds tienen overtime/undertime links | MEDIA |
| Error | Indeterminate resolution | Affectees en transicion resueltos por exception handler | MEDIA |
| Global | Claridad | Ningun OPD excede 20-25 entidades | MEDIA |
| Global | Inner/outer scoping | Objetos inner solo existen en scope de su proceso padre | MEDIA |
| Global | Name coherency | Sin nombres duplicados no resueltos | ALTA |
| Global | Ontology enforcement | Nivel configurado para organizacion (Suggest o Enforce) | MEDIA |
| Global | Model informativeness | Grading ejecutado; sin precedence links faltantes criticos | MEDIA |
| Global | System map | Generado para modelos con >10 OPDs | MEDIA |
| Global | Specification constructs | OPD + OPL + OPM spec completos en breadth-first order | MEDIA |
| Global | Port folding | Usado donde layout fisico de componentes es relevante | BAJA |
| Global | Implicit objects | Objetos implicitos en texto fuente identificados y modelados explicitamente | ALTA |
| Req | Trazabilidad estructural | Si se usan requirements en OPCloud, se ocupan links estructurales y convencion "satisfies" | MEDIA |
