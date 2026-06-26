---
name: opm-modeler
description: Model systems using Object-Process Methodology (OPM/ISO 19450). Use when the user asks to model a system, create an SD, build OPDs, write OPL sentences, refine processes, validate an OPM model, or anything related to OPM conceptual modeling. Triggers on words like OPM, OPD, OPL, system diagram, SD, SD1, in-zooming, unfolding, transformee, beneficiary, enabler, agent, instrument, or any reference to OPM modeling methodology.
---

# OPM Modeler

Construir modelos conceptuales de sistemas usando Object-Process Methodology (OPM) conforme a ISO 19450.

## Corpus normativo

Tres documentos SSOT en `references/`. Orden de precedencia:

1. **opm-iso-19450.md** — semantica OPM, notacion, relaciones, procedimiento SD. Autoridad maxima.
2. **opm-opl-es.md** — realizacion textual OPL en español. Gobierna superficie linguistica ES sin alterar semantica.
3. **metodologia-modelamiento-opm.md** — guia operativa: wizard SD, refinamiento, complejidad, simulacion, validacion.

Regla de conflicto: ISO 19450 > OPL-ES > metodologia. Consultar siempre antes de emitir sentencias OPL o tomar decisiones de modelado.

## Cuando cargar referencias

- **Construir SD o SD1**: leer metodologia (§6, §7) + ISO (SD procedure, links).
- **Escribir OPL en español**: leer opm-opl-es.md (plantillas §3-§13).
- **Escribir OPL en ingles**: leer ISO (EBNF, link syntax tables).
- **Validar modelo**: leer metodologia (§15 invariantes, §16 checklist).
- **Refinamiento nivel 2+**: leer metodologia (§8 complejidad, §9 heuristicas).
- **Control de flujo**: leer metodologia (§10) + ISO (conditions, events, XOR/OR).
- **Simulacion/cuantitativo**: leer metodologia (§12, §14) + ISO (duration, execution).

Cargar solo las secciones relevantes — no inyectar los 3 documentos completos a la vez.

## Procedimiento de modelado

### Fase 0 — Clasificar sistema

Determinar tipo: artificial / natural / social / socio-tecnico. Esto gobierna que componentes del SD aplican (§5 metodologia).

### Fase 1 — Construir SD via wizard

Seguir las 12 etapas del wizard agnostico (§6.0 metodologia):

0. Clasificar sistema
1. Fijar proceso principal (gerundio EN / infinitivo o -cion ES)
2. Identificar beneficiario
3. Fijar atributo de valor + estados input/output
4. Fijar funcion principal (benefit-providing object)
5. Resolver agencia humana (agent = solo humanos)
6. Delimitar sistema + exhibition
7. Identificar instrumentos
8. Fijar inputs/outputs
9. Delimitar contexto externo
10. Problem occurrence (si aplica)
11. Gate de consistencia (checklist §6.11)

Cada etapa DEBE cerrar con un hecho del modelo explicito. Si una etapa no puede cerrarse, retroceder.

### Fase 2 — Emitir OPL

Generar sentencias OPL usando plantillas del corpus:
- ES: usar plantillas de opm-opl-es.md con convenciones tipograficas (**objeto**, *proceso*, `estado`)
- EN: usar sintaxis EBNF de ISO 19450

### Fase 3 — Refinar (SD1+)

- Sync (orden fijo) → in-zooming (§7.1)
- Async (orden variable) → unfolding (§7.2)
- Verificar distribucion de links (§7.4): consumption/result NUNCA en outer contour
- Resolver split links si hay efecto underspecified
- Expresar estados suprimidos en SD

### Fase 4 — Validar

Ejecutar checklist §16 de metodologia. Reportar como tabla con severidad CRIT/ALTA/MEDIA/BAJA.

## Reglas duras

1. Agent link (black lollipop) = solo humanos. Robots, software, IA → instrument link.
2. Todo proceso DEBE transformar al menos un objeto.
3. Nombres singulares. Plurales: Grupo (humanos), Conjunto (inanimados).
4. Proceso EN: gerundio (-ing). Proceso ES: infinitivo o nominalizacion en -cion/-miento.
5. Consumption/result links NO en outer contour de proceso in-zoomed.
6. Colision agent+affectee en mismo proceso: transforming link prevalece (§4.4 metodologia).
7. Todo OPD ≤ 20-25 entidades.
8. Structural links homogeneos (excepcion: exhibition-characterization).

## Formato de salida

Para cada nivel del modelo entregar:

1. **Tabla de elementos** — nombre, tipo (objeto/proceso), esencia, afiliacion, estados
2. **Tabla de enlaces** — tipo, origen, destino, ID plantilla
3. **Parrafo OPL** — sentencias completas en el idioma elegido
4. **Resultado de validacion** — checklist con PASS/FAIL por item
