---
_manifest:
  urn: "urn:fxsl:kb:opm-iso-19450"
  provenance:
    created_by: "kora/curator"
    created_at: "2026-03-22"
    source: "OPERATIONS/source/fxsl/opm-methodology/opm-iso.md"
version: "1.2.0"
status: published
tags: [opm, iso-19450, systems-engineering, conceptual-modeling, bimodal-representation, mbse, opcloud]
lang: en
extensions:
  kora:
    family: specification
---

# OPM ISO/PAS 19450 — Object-Process Methodology

Compact conceptual language and methodology for modelling automation systems and knowledge representation. Specifies formal syntax and semantics for system architects, designers and OPM-compliant tool vendors. Application ranges from simple assemblies to complex multidisciplinary dynamic systems.

OPM provides two semantically equivalent modalities: graphical (OPD set) and textual (OPL sentences in English subset). Domain experts understand OPL without technical training. OPM unifies function, structure and behaviour in a single model.

**Tool support:** OPCloud (cloud-based, primary implementation) generates OPL automatically from OPDs, supports simulation, MQTT/ROS integration, CSV import, AI requirements generation, templates, sub-models, and collaborative editing. Predecessor: OPCAT (desktop, freely available). **Applications:** next-generation appliance design, commercial aircraft modelling, business process knowledge management, automotive vehicle control, ISS robotic arms, insurance product design, and molecular biology research.

---

## Scope and Conformance

OPM is specified with sufficient detail for practitioners to produce conceptual models at various extents of detail and for tool vendors to create supporting software.

Three conformance levels:

| Level | Requirements |
|-------|-------------|
| Partial (symbolic) | Use only OPM symbols (§4) and elements (§7-12) with assigned semantics |
| Full | Partial + modelling approach per §6 and §14 |
| Toolmaker | Partial + provision for full + OPL support per EBNF (Annex A) |

No normative references.

---

## Glossary

76 formal definitions from ISO/PAS 19450 §3. Cross-references use definition numbers.

| # | Term | Definition |
|---|------|-----------|
| 3.1 | Abstraction | Decreasing detail and completeness to improve comprehension |
| 3.2 | Affectee | Transformee whose state changes via process; must be stateful object |
| 3.3 | Agent | Enabler that is a human or group of humans |
| 3.4 | Attribute | Object that characterizes a thing other than itself |
| 3.5 | Behaviour | Transformation of objects from model execution |
| 3.6 | Beneficiary | Stakeholder gaining functional value from system operation |
| 3.7 | Class | Collection of things with same perseverance, essence, affiliation, features and states |
| 3.8 | Completeness | Extent to which all system details are specified |
| 3.9 | Condition link | Procedural link from object/state to process denoting procedural constraint |
| 3.10 | Consumee | Transformee that a process consumes or eliminates |
| 3.11 | Context | Portion of OPM model represented by one OPD and corresponding OPL |
| 3.12 | Control link | Procedural link with additional control semantics |
| 3.13 | Control modifier | Symbol on link adding control semantics: "e" (event) or "c" (condition) |
| 3.14 | Discriminating attribute | Attribute whose values identify corresponding specializations |
| 3.15 | Effect | State change of object or attribute value; applies only to stateful objects |
| 3.16 | Element | Thing or link |
| 3.17 | Enabler | Object enabling a process without being transformed |
| 3.18 | Event | Point in time of object creation/appearance or entrance to state; may initiate precondition evaluation |
| 3.19 | Event link | Control link denoting event from object/state to process |
| 3.20 | Exhibitor | Thing characterized by a feature via exhibition-characterization |
| 3.21 | Feature | Attribute or operation |
| 3.22 | Folding | Abstraction by hiding refineables of unfolded refinee (4 kinds: part, feature, specialization, instance) |
| 3.23 | Function | Process providing functional value to a beneficiary |
| 3.24 | General | Refineable with specializations |
| 3.25 | Informatical | Of or pertaining to data, information, knowledge |
| 3.26 | Inheritance | Assignment of OPM elements from general to specializations |
| 3.27 | Input link | Link from object source state to transforming process |
| 3.28 | Instance (model) | Object/process that is refinee in classification-instantiation |
| 3.29 | Instance (operational) | Uniquely identifiable thing during runtime/simulation |
| 3.30 | Instrument | Non-human enabler |
| 3.31 | Invocation | Initiation of a process by a process |
| 3.32 | Involved object set | Union of preprocess and postprocess object sets |
| 3.33 | In-zoom context | Things and links within boundary of in-zoomed thing |
| 3.34 | In-zooming (object) | Part unfolding indicating spatial ordering of constituent objects |
| 3.35 | In-zooming (process) | Part unfolding indicating temporal partial ordering of constituent processes |
| 3.36 | Link | Graphical expression of structural or procedural relation |
| 3.37 | Metamodel | Model of a modelling language |
| 3.38 | Model fact | Relation between two OPM things or states |
| 3.39 | Object | Model element representing a thing with potential physical or informatical existence |
| 3.40 | Object class | Pattern for objects with same structure and transformation pattern |
| 3.41 | OPD | OPM graphic representation of model or part of model |
| 3.42 | OPL | English subset textual representation of OPM model |
| 3.43 | OPM | Formal bimodal graphic-text language for specifying complex multidisciplinary systems |
| 3.44 | OPD object tree | Tree graph depicting object elaboration through refinement |
| 3.45 | OPD process tree | Tree graph from SD through process in-zooming; primary navigation mechanism |
| 3.46 | Operation | Process characterizing a thing (what the thing does) |
| 3.47 | Output link | Link from transforming process to output state of object |
| 3.48 | Out-zooming (object) | Inverse of object in-zooming |
| 3.49 | Out-zooming (process) | Inverse of process in-zooming |
| 3.50 | Perseverance | Property: static (object) or dynamic (process) |
| 3.51 | Postcondition | Condition resulting from successful process completion |
| 3.52 | Postprocess object set | Objects remaining or resulting from process completion |
| 3.53 | Precondition | Condition for starting a process |
| 3.54 | Preprocess object set | Objects evaluated prior to starting a process |
| 3.55 | Primary essence | Majority essence (informatical or physical) of system things |
| 3.56 | Procedural link | Graphical notation of procedural relation |
| 3.57 | Procedural relation | Time-dependent or conditional connection between object/state and process |
| 3.58 | Process | Transformation of one or more objects |
| 3.59 | Process class | Pattern for processes with same transformation pattern |
| 3.60 | Property | Modelling annotation distinguishing elements (cardinalities, tags, labels) |
| 3.61 | Refineable | Thing amenable to refinement: whole, exhibitor, general, or class |
| 3.62 | Refinee | Thing refining a refineable: part, feature, specialization, or instance |
| 3.63 | Refinement | Elaboration increasing detail and completeness |
| 3.64 | Resultee | Transformee that a process creates |
| 3.65 | Stakeholder | Individual/organization with interest in the system |
| 3.66 | Stateful object | Object with specified states |
| 3.67 | Stateless object | Object lacking specified states |
| 3.68 | State (object) | Possible situation or position of an object |
| 3.69 | State (system) | Snapshot of system model at a point in time |
| 3.70 | State expression | Refinement revealing subset of object's states |
| 3.71 | State suppression | Abstraction hiding subset of object's states |
| 3.72 | Structural link | Graphical notation of structural relation |
| 3.73 | Structural relation | Operationally invariant connection between things |
| 3.74 | Structure | Objects and non-transient relations in model |
| 3.75 | System Diagram (SD) | Root OPD depicting system function and top-level context |
| 3.76 | Thing | Object or process |
| 3.77 | Transformation | Creation, consumption, or state change of an object |
| 3.78 | Transformee | Object affected by a process |
| 3.79 | Transforming link | A consumption, effect, or result link |
| 3.80 | Unfolding | Refinement adding detail to refinees |
| 3.81 | Value (attribute) | State of an attribute |
| 3.82 | Value (functional) | Benefit derived from a system's function |
| 3.83 | Whole | An aggregate |
| 3.84 | OPPL | Sentence classification layer over OPL used for model informativeness grading. Categories: Definition, Structural, Procedural, Meta, Unknown |

Key normative notes on glossary terms:

- **Property vs attribute (3.60)**: unlike an attribute, a property value **cannot change** during simulation or operational implementation. Cardinalities, tags and path labels are properties.
- **No process states (3.68)**: OPM has no concept of process state ("started", "in process", "finished"). Instead, model subprocesses such as Starting, Processing, Finishing.
- **Every thing implies instances (3.28/3.29)**: by creating a thing in the conceptual model, the modeller implies that at least one operational instance of that thing (or a specialization) can exist during system operation.

---

## Modelling Principles

Six principles govern OPM modelling:

1. **Purpose-serving activity** — System function and modelling purpose guide scope and detail. Different stakeholders require different views of the same system.
2. **Unification of function, structure and behaviour** — Structure (physical + informatical objects with structural relations) + behaviour (processes transforming objects over time) = function delivering value to stakeholders.
3. **Identifying functional value** — The value-providing process expresses the function as perceived by the main beneficiary. Identifying and labelling this primary process is the critical first step.
4. **Function vs behaviour** — Function is the value to the beneficiary; behaviour is how the system operates. Same function may have different structural/behavioural implementations (bridge vs ferry for river crossing).
5. **System boundary setting** — Environment is the collection of things outside the system that may interact with it. Systemic things have solid contour; environmental things have dashed contour.
6. **Clarity and completeness trade-off** — Real systems contain overwhelming detail. Understanding requires balancing clarity and completeness via OPD hierarchy.

---

## Fundamental Concepts

### Bimodal Representation

Every OPM model is expressed in semantically equivalent graphics (OPD) and text (OPL). Each OPD has a corresponding OPL paragraph. OPL uses colour coding: processes in blue, objects in green, states in golden brown. This redundancy leverages dual cognitive channels (visual + verbal).

### Modelling Elements

Two element kinds: **things** (objects and processes) and **links** (procedural and structural).

### Context Management

OPD is the fundamental unit depicting elements of a context. Mechanisms for managing contextual scope: state expression/suppression, unfolding/folding, in-zooming/out-zooming.

### Conceptual vs Runtime Models

Conceptual models describe structure and behaviour patterns. Runtime models represent operational instance occurrences during simulation. **A model expressing consistent detail is implementable as a simulation** capable of realizing resources and producing functional value — this is the formal criterion for model completeness.

---

## Visual Notation Specification

OPM's graphical layer uses a minimal set of shapes, contours, shadings and symbols. Every diagram element has a fixed visual specification that determines how to read and compose OPDs.

### Entity Symbols

Entities are closed shapes. Things (objects and processes) and their states are the building blocks.

| Entity | Shape | Contour variants | Shading variants | Label |
|--------|-------|-----------------|------------------|-------|
| Object | Rectangle | solid (systemic), dashed (environmental) | shaded (physical), flat/non-shaded (informatical) | object name, capitalized words |
| Process | Ellipse | solid (systemic), dashed (environmental) | shaded (physical), flat/non-shaded (informatical) | process name, capitalized gerund |
| State | Rounded-corner rectangle (rountangle) inside owning object | normal, thick (initial), double (final), with diagonal open arrow (default) | none | state name, non-capitalized |

The 8 thing symbol combinations result from the Cartesian product of Shape (rectangle/ellipse) × Depth (shaded/flat) × Contour (solid/dashed):

| Symbol | Description | Meaning |
|--------|-------------|---------|
| Shaded solid rectangle | Physical systemic object | Tangible object inside system boundary |
| Shaded dashed rectangle | Physical environmental object | Tangible object outside system boundary |
| Flat solid rectangle | Informatical systemic object | Data/information object inside system |
| Flat dashed rectangle | Informatical environmental object | Data/information object outside system |
| Shaded solid ellipse | Physical systemic process | Physical process inside system |
| Shaded dashed ellipse | Physical environmental process | Physical process outside system |
| Flat solid ellipse | Informatical systemic process | Information process inside system |
| Flat dashed ellipse | Informatical environmental process | Information process outside system |

### Procedural Link Symbols

Procedural links connect objects/states to processes. Each link type has a distinct arrowhead, terminal symbol, or annotation.

| Link | Source | Destination | Graphic specification |
|------|--------|-------------|----------------------|
| Consumption link | object | process | Arrow with **closed arrowhead** pointing from consumee to consuming process |
| Result link | process | object | Arrow with **closed arrowhead** pointing from creating process to resultee |
| Effect link | object ↔ process | bidirectional | **Bidirectional arrow with two closed arrowheads**, one in each direction between affectee and process |
| Input-output effect pair | state → process → state | directional pair | Arrow with closed arrowhead from **input state** to process + arrow from process to **output state** of same object |
| Agent link | agent | process | Line with **filled circle** ("black lollipop") at terminal end extending from agent to process |
| Instrument link | instrument | process | Line with **empty circle** ("white lollipop") at terminal end extending from instrument to process |
| Consumption event link | object | process | Consumption link with small letter **"e"** annotation near arrowhead |
| Effect event link | object ↔ process | bidirectional | Effect link with small letter **"e"** near process end of arrow |
| Agent event link | agent | process | Agent link with small letter **"e"** near process end |
| Instrument event link | instrument | process | Instrument link with small letter **"e"** near process end |
| Condition consumption link | object | process | Consumption link with small letter **"c"** near arrowhead |
| Condition effect link | object ↔ process | bidirectional | Effect link with small letter **"c"** near process end |
| Condition agent link | agent | process | Agent link with small letter **"c"** near process end |
| Condition instrument link | instrument | process | Instrument link with small letter **"c"** near process end |
| Invocation link | process | process | **Lightning-symbol jagged line** from invoking source to invoked destination, ending with closed arrowhead |
| Self-invocation link | process | same process | **Pair of invocation links** originating at process and joining head-to-tail before ending back at origin |
| Overtime exception link | process | handling process | **Single short oblique bar** crossing the line near destination process |
| Undertime exception link | process | handling process | **Two parallel short oblique bars** crossing the line near destination process |

State-specified variants of all procedural links originate from a **specific state** inside the object rather than from the object itself. The annotation ("e" or "c") placement remains near the arrowhead or process end.

### Structural Link Symbols

| Link | Graphic specification |
|------|----------------------|
| Aggregation-participation | **Filled black triangle** with apex connecting by line to whole; parts connect by lines to opposite horizontal base |
| Exhibition-characterization | **Small black triangle inside larger empty triangle**; larger triangle apex connects to exhibitor; features connect to opposite base |
| Generalization-specialization | **Empty triangle**; apex connects to general; specializations connect to opposite base |
| Classification-instantiation | **Small black circle inside empty triangle**; apex connects to class; instances connect to base |
| Incomplete collection indicator | **Short horizontal bar** crossing the vertical line below the triangle symbol |
| Unidirectional tagged | Arrow with **open arrowhead** and tag annotation near shaft |
| Bidirectional tagged | Line with **harpoon-shaped arrowheads** on opposite sides at both ends; each tag aligns on side of arrow with harpoon edge sticking out |
| Reciprocal tagged | Same as bidirectional but with single tag or no tag |

### Logical Operator Symbols

| Operator | Graphic specification |
|----------|----------------------|
| AND | Separate **non-touching** links of same kind on process contour |
| XOR | **Dashed arc** across links of the link fan, arc focal point at convergent endpoint |
| OR | **Two concentric dashed arcs** across links of the link fan, focal point at convergent endpoint |
| Probabilistic | **`Pr=p`** annotation along each fan link; probabilities sum to 1 |

### Context Management Symbols

| Mechanism | Graphic specification |
|-----------|----------------------|
| State suppression indicator | **Small rountangle with "..." label** in object's right bottom corner; signifies hidden states |
| In-diagram unfolding | Refineable and refinees in same OPD, connected by fundamental structural links |
| New-diagram unfolding/in-zooming | Refineable has **thick contour** in both parent OPD (folded) and child OPD (unfolded/in-zoomed) |
| Process in-zooming | Ellipse of refineable **enlarges** to accommodate subprocess symbols; execution timeline flows **top → bottom** within enlarged ellipse |
| Object in-zooming | Rectangle of refineable **enlarges** to accommodate constituent object symbols; arrangement indicates spatial/logical order |
| Implicit invocation | **No explicit symbol**; top-to-bottom vertical arrangement of subprocess ellipse top points within in-zoom context implies invocation sequence |
| Parallel implicit invocation | Subprocess ellipses with top points at **same height** (within tolerance) start simultaneously |
| Duplicate thing | **Small offset shape behind** the repeated thing symbol; indicates same logical element appearing multiple times in OPD |
| Path label | **Text annotation** along procedural link; matching labels on entry/exit links determine execution path |

### In-Zooming Visual Composition

Process in-zooming creates a visual hierarchy. In SD, a process P appears as a simple ellipse connected to objects via procedural links. In SD1, P's ellipse enlarges and contains its subprocesses (P1, P2, P3) as smaller ellipses arranged vertically. Objects from SD connect to the specific subprocesses they relate to. Links attached to the **outer contour** of an in-zoomed process distribute to all subprocesses (enabling links only — consumption and result links **must not** attach to outer contour, as this would violate temporal logic). The modeller migrates consumption/result links to specific subprocesses during in-zooming.

Object in-zooming analogously enlarges a rectangle to show constituent objects in spatial or logical order. Unlike process in-zooming, no transfer of execution control occurs.

---

## Things: Objects and Processes

### Objects

An object is a thing that exists or has potential physical or informatical existence. Persistence is default unless a process acts on it. Represented as a **rectangular box** with the object name.

### Processes

A process transforms one or more objects by generating, affecting (changing state), or consuming them. Has positive performance time duration. Represented as an **ellipse** with the process name.

### Object-Process Test

Three criteria distinguish process from object: time association (happens over time), verb association (ends in gerund "-ing"), and object transformation (must transform at least one object).

### Generic Properties

All things have three generic properties:

| Property | Values | Default |
|----------|--------|---------|
| Perseverance | static (object) / dynamic (process) | determined by type (Persistent default, Transient non-default) |
| Essence | physical / informatical | Informatical is default; Physical is non-default. System primary essence = majority of things |
| Affiliation | systemic / environmental | Systemic is default; Environmental is non-default |

**Affiliation inheritance**: attributes of environmental objects are automatically environmental. Processes performed by environmental entities are environmental processes.

---

## Object States

### Stateful and Stateless Objects

A stateful object has a set of permissible states. At any point in time, a stateful instance is at one state or in transition. A stateless object has no specified states and can only be created or consumed, not affected.

### Representation

A rounded-corner rectangle inside the owning object, labelled with the state name. In OPL: state names in bold without capitalization.

### Initial, Default and Final States

| Designation | Graphic | Meaning |
|-------------|---------|---------|
| Initial | thick border | state at object creation |
| Final | double border | state when consumed |
| Default | diagonal arrow indicator | most likely state on random inspection |

### Attribute Values

An attribute is an object characterizing a thing. Attribute values are states of attributes. May specify measurement units. OPL syntax: `Attribute of Object is value.` or `Attribute of Object ranges from X to Y.`

---

## Links Overview

### Procedural Links

Three kinds:

- **Transforming link** — connects process with transformee (consumption, result, or effect)
- **Enabling link** — connects enabler with process (agent or instrument)
- **Control link** — procedural link with control modifier ("e" for event, "c" for condition)

**Procedural link uniqueness principle**: an object or state has exactly one role (transformee or enabler) with respect to a linked process.

**State-specified procedural links**: connect process to a specific state of an object rather than the object itself.

### Structural Links

Two kinds: **tagged structural links** (user-defined semantics) and **fundamental structural links** (aggregation-participation, exhibition-characterization, generalization-specialization, classification-instantiation).

Structural links connect objects-to-objects or processes-to-processes, except exhibition-characterization which can connect objects to processes.

### Event-Condition-Action Control

Process performance begins when: (1) an initiating event occurs and (2) a precondition is satisfied. Events are lost after evaluation regardless of precondition outcome.

- **Preprocess object set** (precondition): consumees + affectees + enablers needed before process starts
- **Postprocess object set** (postcondition): resultees + affected objects after process completes

---

## Transforming Links

Three basic types:

| Link | Semantics | OPD | OPL Syntax | Direction |
|------|-----------|-----|-----------|-----------|
| Consumption | Process destroys/eliminates object | closed arrowhead → process | `Processing consumes Consumee.` | object → process |
| Result | Process creates/generates object | closed arrowhead → object | `Processing yields Resultee.` | process → object |
| Effect | Process changes object state | bidirectional closed arrowheads | `Processing affects Affectee.` | object ↔ process |

### State-Specified Transforming Links

| Link | OPL Syntax |
|------|-----------|
| State-specified consumption | `Process consumes specified-state Object.` |
| State-specified result | `Process yields specified-state Object.` |
| Input-output-specified effect | `Process changes Object from input-state to output-state.` |
| Input-specified effect | `Process changes Object from input-state.` |
| Output-specified effect | `Process changes Object to output-state.` |

Consumption rate and quantity may be modelled via link properties and object attributes when consumption occurs over time. The consumption link has a Rate property and the consumee has a Quantity attribute. Without these, consumption is immediate upon process activation.

**Result link to stateful object with initial state**: the result link should attach to the object rectangle or to a state other than the initial state — never to the initial state directly, to avoid ambiguity.

**Affectee transition semantics**: once an affecting process starts, the affectee exits its input state. The affectee reaches the output state only when the process completes. Between start and completion, the affectee is **in transition** between states. If the process stops prematurely (aborts), the affectee state remains **indeterminate** unless exception handling resolves it.

**Input-specified effect output resolution**: when no output state is specified, the destination is the object's default state. If no default state exists, the state probability distribution determines the output.

---

## Enabling Links

Enablers are necessary for process occurrence but are not transformed. Two kinds:

| Link | Enabler type | OPD symbol | OPL Syntax |
|------|-------------|------------|-----------|
| Agent link | Human/group with intelligent decision-making | filled circle ("black lollipop") | `Agent handles Processing.` |
| Instrument link | Inanimate non-decision-making object | empty circle ("white lollipop") | `Processing requires Instrument.` |

If an enabler ceases to exist during process execution, the process stops and the affectee state remains indeterminate.

### State-Specified Enabling Links

| Link | OPL Syntax |
|------|-----------|
| State-specified agent | `Specified-state Agent handles Processing.` |
| State-specified instrument | `Processing requires specified-state Instrument.` |

The process occurs if and only if the enabler is at the qualifying state.

---

## Control Links: Events

Event links annotate transforming or enabling links with "e". An event triggers precondition evaluation; the event is always lost afterward regardless of outcome.

### Transforming Event Links

| Link | OPL Syntax |
|------|-----------|
| Consumption event | `Object initiates Process, which consumes Object.` |
| Effect event | `Object initiates Process, which affects Object.` |

### Enabling Event Links

| Link | OPL Syntax |
|------|-----------|
| Agent event | `Agent initiates and handles Process.` |
| Instrument event | `Instrument initiates Process, which requires Instrument.` |

### State-Specified Transforming Event Links

| Link | OPL Syntax |
|------|-----------|
| State-specified consumption event | `Specified-state Object initiates Process, which consumes Object.` |
| Input-output-specified effect event | `Input-state Object initiates Process, which changes Object from input-state to output-state.` |
| Input-specified effect event | `Input-state Object initiates Process, which changes Object from input-state.` |
| Output-specified effect event | `Object in any state initiates Process, which changes Object to destination-state.` |

### State-Specified Enabling Event Links

| Link | OPL Syntax |
|------|-----------|
| State-specified agent event | `Specified-state Agent initiates and handles Processing.` |
| State-specified instrument event | `Specified-state Instrument initiates Processing, which requires specified-state Instrument.` |

---

## Control Links: Conditions and Exceptions

### Condition Links

Condition links annotate transforming or enabling links with "c". They provide a **bypass mechanism**: if the precondition fails, execution control skips the process instead of waiting.

### Condition Transforming Links

| Link | OPL Syntax |
|------|-----------|
| Condition consumption | `Process occurs if Object exists, in which case Object is consumed, otherwise Process is skipped.` |
| Condition effect | `Process occurs if Object exists, in which case Process affects Object, otherwise Process is skipped.` |

### Condition Enabling Links

| Link | OPL Syntax |
|------|-----------|
| Condition agent | `Agent handles Process if Agent exists, else Process is skipped.` |
| Condition instrument | `Process occurs if Instrument exists, else Process is skipped.` |

### Condition State-Specified Links

Six variants where the bypass checks whether the object is in a specified state:

| Link | OPL Syntax |
|------|-----------|
| Condition state-specified consumption | `Process occurs if Object is specified-state, in which case Object is consumed, otherwise Process is skipped.` |
| Condition input-output-specified effect | `Process occurs if Object is input-state, in which case Process changes Object from input-state to output-state, otherwise Process is skipped.` |
| Condition input-specified effect | `Process occurs if Object is input-state, in which case Process changes Object from input-state, otherwise Process is skipped.` |
| Condition output-specified effect | `Process occurs if Object exists, in which case Process changes Object to output-state, otherwise Process is skipped.` |
| Condition state-specified agent | `Agent handles Process if Agent is specified-state, else Process is skipped.` |
| Condition state-specified instrument | `Process occurs if Instrument is specified-state, otherwise Process is skipped.` |

Graphically, each uses its corresponding state-specified link symbol with the small letter **"c"** annotation near the process end.

### Exception Links

Connect a source process to exception-handling destination process based on duration.

| Link | Trigger | OPD symbol | OPL Syntax |
|------|---------|------------|-----------|
| Overtime | Source exceeds Maximal Duration | single oblique bar | `Handling occurs if duration of Source exceeds max-duration time-units.` |
| Undertime | Source falls short of Minimal Duration | two parallel oblique bars | `Handling occurs if duration of Source falls short of min-duration time-units.` |

Process Duration may specialize into Minimal, Expected and Maximal Duration. Duration Distribution (Normal, Uniform, Exponential) determines actual duration per process instance at runtime.

---

## Invocation Links

Process invocation: a process initiates another process. Semantically implies creation of a transient interim object immediately consumed by the destination.

| Link | OPD symbol | OPL Syntax |
|------|------------|-----------|
| Invocation | lightning jagged line with arrowhead | `Invoking-process invokes invoked-process.` |
| Self-invocation | pair of invocation links head-to-tail back to origin | `Invoking-process invokes itself.` |

**Implicit invocation** within in-zoomed process: sub-process termination invokes the one(s) immediately below it. No explicit link; relative height implies temporal order (top to bottom). When two or more subprocesses have top points at the same height, they start in parallel; the one completing last initiates the next subprocess.

**Cyclic invocation with conditional bypass**: use invocation links to model iterative/cyclical behaviour. After each cycle, a boolean decision node evaluates whether to loop back. Subprocesses whose entry conditions are already met can be skipped on re-entry. Example: in a refrigeration system, Evaporating invokes Vapor Compression Refrigerating, expressing the continuous refrigerant cycle. Identifying the refrigerant state at each stage helps determine which component fails.

---

## Structural Links

### Tagged Structural Links

User-defined semantics via textual tags along the link.

| Variant | OPD | OPL Syntax |
|---------|-----|-----------|
| Unidirectional tagged | open arrowhead + tag | `Source-thing tag Destination-thing.` |
| Unidirectional null-tagged | open arrowhead, no tag | `Source-thing relates to Destination-thing.` |
| Bidirectional tagged | harpoon arrowheads both ends + 2 tags | Two separate OPL sentences, one per direction |
| Reciprocal tagged | harpoon arrowheads + 1 tag | `Source and Destination are reciprocity-tag.` |
| Reciprocal null-tagged | harpoon arrowheads, no tag | `Source and Destination are related.` |

### Fundamental Structural Relations

| Relation | Refineable → Refinee | OPD symbol | OPL Syntax |
|----------|---------------------|------------|-----------|
| Aggregation-participation | whole → parts | filled black triangle | `Whole consists of Part1, Part2 and Part3.` |
| Exhibition-characterization | exhibitor → features | small black triangle inside larger empty triangle | `Exhibitor exhibits Attribute1 as well as Operation1.` |
| Generalization-specialization | general → specializations | empty triangle | `Specialization1 and Specialization2 are General.` |
| Classification-instantiation | class → instances | small black circle inside empty triangle | `Instance is an instance of Class.` |

Incomplete collections use a horizontal bar crossing the vertical line below the triangle, with OPL phrase "and at least one other part/feature/specialization".

**Perseverance constraint**: with the exception of exhibition-characterization, all refinee destination things must have the **same Perseverance** as the refineable source thing (all objects or all processes).

Exhibition-characterization is the only structural link connecting objects to processes (feature = attribute if object, operation if process). The "of" relation identifies the exhibitor: `Feature of Exhibitor ...`

**Classification-instantiation**: unlike the other 3 fundamental relations, there is **no distinction between complete and incomplete collections** — the number of instances may not be known a priori and varies during operation.

### Inheritance

Specializations inherit from the general: all parts, all features, all tagged structural links, all procedural links. Multiple inheritance allowed. Discriminating attribute constrains specialization values. Maximum specializations with multiple discriminating attributes = Cartesian product of possible values.

**Override mechanism**: the modeller may override any inherited participant by specifying a specialization of that participant with a different name and different set of states.

**Runtime existence rule**: a specialized thing instance does not exist in the absence of the more general thing instance from which it inherits.

**Procedure to create a general from existing specializations**:

1. Identify common features and participants across candidate specializations
2. Create a new general thing with those common elements
3. Connect general to specializations via generalization-specialization link
4. Remove common elements from specializations (now inherited)
5. Migrate common tagged structural links and procedural links from specializations to the general

### State-Specified Structural Links

State-specified characterization links associate specialized objects with specific attribute values.

Seven kinds of state-specified tagged structural links decompose into 3 groups:

| Group | Unidirectional | Bidirectional | Reciprocal |
|-------|---------------|---------------|------------|
| **Source** state-specified | `Specified-state Source tag Destination.` | `Specified-state Source f-tag Dest.` / `Dest b-tag Specified-state Source.` | `Dest and Specified-state Source are reciprocal-tag.` |
| **Destination** state-specified | `Source tag Specified-state Dest.` | — | — |
| **Source-and-destination** state-specified | `Sa Source tag Sb Dest.` | `Sa Source f-tag Sb Dest.` / `Sb Dest b-tag Sa Source.` | `Sa Source and Sb Dest are reciprocal-tag.` |

Bidirectional and reciprocal variants do not exist for destination-only specification (hence 7 kinds, not 9).

---

## Relationship Cardinalities

### Object Multiplicity

Constraint on count of object instances associated with a link. Default: one instance per link end. Applies to tagged structural, aggregation-participation and procedural links.

| Symbol | Bounds | OPL phrase |
|--------|--------|-----------|
| ? | 0..1 | an optional |
| * | 0..* | optional (none to many) |
| (none) | 1..1 | (default) |
| + | 1..* | at least one |

Range syntax: `qmin..qmax` (closed). Multiple ranges separated by comma. Arithmetic expressions use +, -, *, /, (, ). Constraints use =, ≠, <, ≤, ≥, curly braces for set members, and "in" (∈) membership operator — all after semicolon. If a parameter has multiple constraints, they appear as a semicolon-separated list. **Parameter names must be unique across the entire system model.**

**Participation constraints do NOT apply to processes.** Sequential repetition of a process uses a recurrent process with an iteration counter. Parallel repetition uses synchronous/asynchronous subprocesses within an in-zoomed process.

**Type declaration**: objects may declare a computational type. OPL: `Object is of type type-identifier.` Types: boolean, string, integer, float, double, short, long, enumerated.

**Optionality examples** (visual reference):

- `Car has an optional Sunroof.` — question mark (?) near Sunroof link
- `Car is equipped with optional Airbags.` — asterisk (*) near Airbag link
- `Car is steered by Steering Wheel.` — no annotation (1..1 default)
- `Car carries at least one Spare Tire.` — plus (+) near Spare Tire link

**Parametric multiplicity example** (Blade Replacing system): Jet Engine consists of **b Installed Blades**. **k** (k=2..4) Aviation Engine Mechanics handle Blade Replacing, using **k Blade Fastening Tools**. 1..2 Aerospace Engineers handle Blade Replacing. Blade Replacing consumes **i inspected Blades** and **(b−i) new Blades**, yields **b Dismantled Blades**. Blade Inspecting yields **a (a≤b) inspected Blades**.

**Multi-constraint example** (Airplane): `Airplane consists of Body, 2 Wings, and e Engines, where e≥1, e=b+2*w.` Each Wing has **w Engines** (0≤w≤3). Body has **b Engines** (b∈{0,1}).

---

## Logical Operators: AND, XOR, OR

### AND

Separate non-touching links of same kind = logical AND. OPL uses "and" conjunction in single sentence.

### XOR

Link fan with dashed arc, focal point at convergent end. Exactly one of the things at divergent end exists/occurs. OPL: `...exactly one of Thing1, Thing2 and Thing3...`

### OR

Link fan with two concentric dashed arcs. At least one of the things at divergent end exists/occurs. OPL: `...at least one of Thing1, Thing2 and Thing3...`

### Link Fan Combinatorics

XOR and OR apply to all procedural link families. The convergent end is the common endpoint; the divergent end is not common.

**Consumption and result link fans:**

| Fan type | OPD visual | XOR OPL | OR OPL |
|----------|-----------|---------|--------|
| Converging consumption (objects → process) | Objects A, B, C each with closed arrowhead to process P; dashed arc at P end | `P consumes exactly one of A, B, or C.` | `P consumes at least one of A, B, or C.` |
| Diverging consumption (object → processes) | Object B with closed arrowheads diverging to P, Q, R; dashed arc at B end | `Exactly one of P, Q, or R consumes B.` | `At least one of P, Q, or R consumes B.` |
| Converging result (processes → object) | Processes P, Q, R with closed arrowheads converging to object B; dashed arc at B end | `Exactly one of P, Q, or R yields B.` | `At least one of P, Q, or R yields B.` |
| Diverging result (process → objects) | Process P with closed arrowheads diverging to A, B, C; dashed arc at P end | `P yields exactly one of A, B, or C.` | `P yields at least one of A, B, or C.` |

**Effect link fans** (bidirectional — no converging/diverging distinction):

| Fan type | XOR OPL | OR OPL |
|----------|---------|--------|
| Multiple objects | `P affects exactly one of A, B, or C.` | `P affects at least one of A, B, or C.` |
| Multiple processes | `Exactly one of P, Q, or R affects B.` | `At least one of P, Q, or R affects B.` |

**Enabling link fans** (enabler is object → diverging to processes):

| Fan type | XOR OPL | OR OPL |
|----------|---------|--------|
| Agent fan | `B handles exactly one of P, Q, or R.` | `B handles at least one of P, Q, or R.` |
| Instrument fan | `Exactly one of P, Q, or R requires B.` | `At least one of P, Q, or R requires B.` |

**Invocation link fans:**

| Fan type | XOR OPL | OR OPL |
|----------|---------|--------|
| Diverging | `P invokes exactly one of Q or R.` | `P invokes at least one of Q or R.` |
| Converging | `Exactly one of P or Q invokes R.` | `At least one of P or Q invokes R.` |

### AND Visual Examples

AND requires **non-touching links** on process contour. Three canonical examples:

- **Agent AND**: Safe Owner A and Safe Owner B handle Safe Opening — two separate agent links (black lollipops) from each owner to the process, links not touching on ellipse contour. Both must be present.
- **Instrument AND**: Safe Opening requires Key A, Key B, and Key C — three separate instrument links (white lollipops), non-touching. All three keys needed.
- **Result AND**: Meal Preparing yields Starter, Entree and Dessert — three separate result links from process to each object. All three created.
- **Effect AND with input-output pairs**: Interest Rate Raising changes Exchange Rate from low to high, Price Index from low to high, and Interest Rate from low to high — three pairs of input-output-specified effect links.

### Control-Modified Link Fans

Each XOR fan has event and condition variants:

| Base fan | Event variant OPD | Event OPL | Condition variant OPD | Condition OPL |
|----------|------------------|-----------|----------------------|---------------|
| Effect (multiple processes) | Bidirectional arrows B↔P,Q,R with "e" near each process | `B initiates exactly one of P, Q, or R, which affects B.` | Same with "c" | `Exactly one of P, Q, R occurs if B exists, otherwise skipped.` |
| Consumption | Arrowheads B→P,Q,R with "e" | `s2 B initiates exactly one of P, Q, R, which consumes B.` | Same with "c" | `Exactly one of P, Q, R occurs if B is s2, otherwise skipped.` |
| Agent | Black lollipops B→P,Q,R with "e" | `s2 B initiates and handles exactly one of P, Q, R.` | Same with "c" | `B handles exactly one of P, Q, R if B is s2, otherwise skipped.` |
| Instrument | White lollipops B→P,Q,R with "e" | `s2 B initiates exactly one of P, Q, R, which requires s2 B.` | Same with "c" | `Exactly one of P, Q, R requires B is s2, otherwise skipped.` |

Every XOR fan in the table has an **OR counterpart** where "exactly" is replaced by "at least" and the single dashed arc becomes a double dashed arc.

### Probabilistic Link Fans

Annotate each fan link with `Pr=p` where probabilities sum to 1.

**Numeric example**: Process P can create object B in three states — s1 (Pr=0.32), s2 (Pr=0.24), s3 (Pr=0.44). Graphically, three result links from P to each state of B, each annotated with its probability. Without annotation, default probability = 1/n (here 1/3 each). If the object has m initial states, creation probability per initial state = 1/m.

**Mixed example**: P yields one of objects A, B, or C at state sc1, with probabilities annotated per link. Source objects may have or lack state specifications within the same fan.

### Execution Path and Path Labels

Path labels along procedural links resolve ambiguity when multiple output options exist. On process exit, the link with the same label as the entry link is followed. OPL: `Following path label, Process consumes/yields Object.`

A **scenario** is a set of one or more path labels that define a specific collection of procedural links to follow through the model. Scenarios are a compact alternative to creating additional OPDs for each execution variant. Their utility grows with system complexity.

**Example** (Food Preparing): Two scenarios — "herbivore" and "carnivore". Following path **carnivore**: Food Preparing consumes Meat, yields Stew and Steak. Following path **herbivore**: Food Preparing consumes Cucumber and Tomato, yields Salad.

---

## Context Management and Refinement

### Completing the SD

The System Diagram models: stakeholders (especially beneficiaries), the value-providing process, and environmental/systemic things creating a succinct OPL paragraph. SD should contain only central, indispensable things. Functional value may be explicit (source-destination states of beneficiary attribute) or implicit (beneficiary is affected).

### Refinement-Abstraction Mechanisms

Three pairs:

| Mechanism | Refinement | Abstraction |
|-----------|-----------|-------------|
| State expression / suppression | Reveal object states in OPD | Hide states (pseudo-state symbol with "..." appears) |
| Unfolding / folding | Reveal refineables via fundamental structural links | Hide refineables, leaving root |
| In-zooming / out-zooming | For aggregation-participation only; reveals subprocesses with temporal order or constituent objects with spatial order | Inverse; requires link precedence resolution |

Four unfolding-folding pairs correspond to four fundamental relations: aggregation, exhibition, generalization, classification.

**In-diagram** unfolding: refineable and refinees in same OPD. **New-diagram** unfolding: creates child OPD (refineable shown with thick contour in both parent and child OPDs).

**View Diagrams**: an OPD that collects model facts from multiple OPDs to explain a specific phenomenon or emphasize a particular aspect. Created by selecting any element and adding connected elements from any OPD. View diagrams are distinct from process tree and object tree OPDs.

## OPD Trees and Implicit Control

**OPD process tree**: root = SD, each node = OPD from process in-zooming. Primary navigation mechanism. Labels: `SD`, `SD1`, `SD1.1`, `SD1.1.1`, etc.

**OPD object tree**: root = object, depicting elaboration through refinement.

Timeline within in-zoomed process flows top → bottom. Sub-process reference points at same height execute in parallel.

### Implicit Invocation Links Summary

Two implicit invocation forms govern synchronous in-zoomed execution:

| Form | Semantics | Structural cue |
|------|-----------|----------------|
| Implicit invocation link | A subprocess invokes the subprocess immediately below it as soon as it completes | successive ellipse top points arranged vertically |
| Parallel implicit invocation link set | Multiple subprocesses start together when their ellipse top points are aligned at the same height | equal-height ellipse top points within the same in-zoom context |

This captures the substance of ISO Table 24: invocation order can be encoded without explicit invocation arrows when the in-zoom layout already fixes temporal order.

---

## Link Distribution Across Context

Links attached to the **outer contour** of an in-zoomed process have **distributive semantics** — they distribute to all subprocesses (analogous to algebraic parentheses).

**Critical restrictions:**

- **Consumption and result links MUST NOT attach to the outer contour** of an in-zoomed process. A distributed consumption link would consume an already-consumed object; a distributed result link would create an already-existing instance. Both violate temporal logic.
- When a process is in-zoomed, all consumption and result links initially migrate **to the first subprocess by default**. The modeller then reassigns to the correct subprocess.
- **Event links from systemic objects/states MUST NOT cross the boundary** of an in-zoomed process to initiate subprocesses — this would interfere with the prescribed temporal order. Environmental event links that cross require explicit contingency modelling.
- If a condition link causes a subprocess to be skipped and there is a next subprocess in the in-zoom context, execution control initiates that next subprocess.

**Valid vs invalid distribution example**: Process P zooms into P1, P2, P3. Agent A handles P (valid: distributes to all subprocesses). Instrument D required by P (valid: distributes). But `P consumes C` — **NOT VALID** because P1 consumes C first; C doesn't exist when P2/P3 perform. And `P yields B` — **NOT VALID** because B can only be created once. Correct: P1 consumes C, P2 yields B, P3 affects B (assign to specific subprocesses). ISO illustrates the equivalence and restriction pattern explicitly in Figure 50 and Figure 51.

---

## Split State-Specified Transforming Links

When an input-output-specified effect link (Process changes Object from s1 to s2) is in-zoomed and contains multiple subprocesses, the model becomes **underspecified** — it's unclear which subprocess takes Object out of s1 and which puts it into s2.

Resolution procedure (3 steps):

1. **Original**: `P changes A from s1 to s2` (single process, unambiguous)
2. **In-zoomed, UNDERSPECIFIED**: P zooms into P1 and P2. `P changes A from s1 to s2` — could mean P1 or P2 or split
3. **Resolved with split links**: `P1 changes A from s1.` (split input link) + `P2 changes A to s2.` (split output link)

The split input link connects from the input state of the affectee to the early subprocess. The split output link connects from the late subprocess to the output state. This is the only mechanism to resolve underspecification in in-zoomed effect links.

Summary of the split pair:

| Pair | Meaning | Source | Destination |
|------|---------|--------|-------------|
| Split input-output specified effect link pair | Early subprocess takes the object out of its input state; later subprocess places it in the output state | input state + late subprocess | early subprocess + output state |

This is the recoverable core of ISO Table 25. ISO Figure 52 provides the canonical underspecified middle case and the repaired split-link case.

**Abstraction role shift**: an object may be an instrument at an abstract level (e.g., Dishwasher as instrument of Dish Washing in SD) and become an affectee at a detailed level (Dish Loading changes Dishwasher from empty to loaded, Dish Unloading changes back to empty in SD1). This is valid because the initial and final states are the same at the abstract level.

---

## Link Precedence During Out-Zooming

When out-zooming, procedural links from sub-processes migrate to the parent process. **Semantic strength** determines which link prevails:

**Transforming link precedence matrix** (when two links of different kinds compete for B↔P after out-zooming):

| B↔P1 \ B↔P2 | Effect | Result | Consumption |
|-------------|--------|--------|-------------|
| **Effect** | Effect | Result | Consumption |
| **Result** | Result | Invalid | Effect |
| **Consumption** | Consumption | Effect | Invalid |

Result + consumption to same object = invalid (can't both create and destroy). When both compete, effect prevails (implicit existence cycle).

Primary precedence order: consumption = result > effect > agent > instrument. State-specified links have higher precedence than basic links. Secondary: event > non-control > condition within each kind.

## OPD Labels and Navigation

**SD contains exactly one systemic process** (the system function). It may contain one or more environmental processes. OPD labels: `SD` (tier 0), `SD1` (tier 1), etc.

**OPD tree edge labels**: each edge in the OPD process tree uses a unidirectional tagged structural link with tag `"is refined by in-zooming ProcessName in"` or `"is refined by unfolding ProcessName in"`. OPL refinement sentence: `Tierₙ OPD label is refined by in-zooming Refineable Process Name in Tierₙ₊₁ OPD Label.`

**OPL specification ordering**: the sequence of OPL paragraphs generally follows **breadth-first order** starting from SD.

### Whole-System OPL

Whole-system OPL is the concatenated textual specification obtained by traversing the OPD tree and composing the OPL paragraphs in model order. Its purpose is to provide a complete textual rendering of the entire model, not just the current context. The canonical ISO example is the Dish Washing System whole-system OPL table: local OPD paragraphs remain context-specific, while whole-system OPL restores end-to-end textual continuity across SD, descendants, states and refinements.

Recoverable core of Table 26 for Dish Washing System:

- `Household User handles Dish Washing.`
- `Dish Washing requires Dishwasher.`
- `Dish Washing consumes Soap.`
- `Dish Washing affects Dish Set.`
- `SD is refined by in-zooming Dish Washing in SD1.`
- `Dishwasher consists of Soap Compartment and other parts.`
- `Dishwasher can be empty or loaded.`
- `State empty of Dishwasher is initial and final.`
- `Soap Compartment can be empty or loaded.`
- `State empty of Soap Compartment is initial.`
- `Dish Set exhibits Cleanliness.`
- `Cleanliness of Dish Set can be dirty or clean.`
- `State dirty of Cleanliness of Dish Set is initial.`
- `State clean of Cleanliness of Dish Set is final.`
- `Dish Washing zooms into Dish Loading, Detergent Inserting, Dish Cleaning & Drying, and Dish Unloading, in that sequence.`
- `Dish Loading changes Dishwasher from empty to loaded.`
- `Detergent Inserting requires Soap.`
- `Detergent Inserting changes Soap Compartment from empty to loaded.`
- `Dish Cleaning & Drying requires Dishwasher.`
- `Dish Cleaning & Drying consumes Soap.`
- `Dish Cleaning & Drying changes Cleanliness of Dish Set from dirty to clean.`
- `Dish Unloading changes Dishwasher from loaded to empty.`

**OPD simplification**: in-diagram out-zooming + new-diagram in-zooming can simplify an overloaded OPD. Restriction: an object cannot become part of the abstracted set if its links would create direct process-to-process procedural links (which OPM does not define semantics for, except invocation and exception links).

### OPM Fact Consistency Principle

A model fact appearing in one OPD and contradicting a fact in another OPD creates inconsistency. Tools should detect and report such conflicts. A fact in one OPD may be a refinement or abstraction of a fact in another OPD within the same model — this is not a contradiction.

---

## System Diagram: Procedure and Components

The SD is the top-level OPD (level 0) providing a high-level view comprehensible to all stakeholders regardless of technical expertise. Five components for artificial/socio-technical systems (three for natural systems):

### 1. Purpose

Who benefits and what value they receive. Expressed as state change in beneficiary attribute from problematic to satisfactory. Natural systems: "outcome" rather than "purpose".

### 2. Main Function

Combination of main process + main object (operand). Function name = object name + process name (e.g. "Car Painting"). The main process transforms the operand via a transforming link.

### 3. Enablers

Objects required for the process but not transformed by it.

- **Agents**: humans/groups (black lollipop). Natural systems without humans have no agents.
- **Instruments**: non-human objects (white lollipop). The system itself is typically the primary instrument. Default system name = function name + "System".

### 4. Environment

Things outside the system that affect its operation. Systemic (solid contour) vs environmental (dashed contour) determined by affiliation attribute.

### 5. Problem Occurrence

Mirror image of purpose + function. An environmental process causes the beneficiary attribute to be in the problematic state. Not applicable for natural systems.

### SD Construction Procedure

Guided 9-stage procedure. Each stage has a guiding question.

1. **Main process** — "What is the main process of the system?" Name must end in gerund ("-ing").
2. **Beneficiary group** — "Who is the beneficiary?" Singular names; use "Set" for inanimate plurals, "Group" for human plurals.
3. **Beneficiary attribute** — "What is the beneficiary attribute?" Define input state (current, problematic) and output state (desired, satisfactory).
4. **Agent** — "Is the beneficiary also the agent?" Additional enablers: maximum 3, singular names.
5. **System name** — "What is the name of the system?" Default: main process name + "System".
6. **Instruments** — "What instruments are required?" Maximum 3 tools, singular names. Physical instruments can be selected.
7. **Inputs** — "What are the inputs?" Maximum 3, singular names. If an input is affected by the main process, it must also be defined as an output.
8. **Outputs** — "What is the output?" Select whether output is also an input.
9. **Environmental objects** — "What environmental objects are associated?" Select from previously defined objects.

### Detail Hierarchy (SD1)

When an OPD becomes too complex, create a descendant OPD. SD1 refines SD:

- **Process refinement**: synchronous (in-zooming, fixed temporal order) or asynchronous (unfolding, no fixed order)
- **Object refinement**: unfolding into parts and attributes
- **State expression**: states suppressed in SD become visible in SD1 linked to sub-processes

---

## System Types and SD Variations

### Artificial (Man-Made) Systems

Full 5-component SD: purpose, main function, enablers, environment, problem occurrence. Purpose expresses the value the system provides to beneficiaries. Problem occurrence is the mirror image of purpose — an environmental process causes the problematic state.

### Natural Systems

Only 3 components apply: main function, enablers (instruments only — no human agents), environment. "Purpose" is replaced by "outcome" (beneficial or detrimental to affected groups). "Problem occurrence" does not apply — no intentional design. Example: storm system — ocean and atmosphere are environmental objects; warm ocean water is instrument.

### Social Systems

Full 5-component SD applies. Agents are the core — organizers, ushers, participants. Instruments include facilities and equipment. Environment includes weather (may affect attendance). Example: conference system — purpose is to increase business cooperation; problem occurrence is business decline.

### Socio-Technical Systems

Complex systems where many components interact in multiple ways and diverse specialists must collaborate. Example: a smartphone was developed by tens of thousands of people across hundreds of companies. OPM is fundamental for guiding development and ensuring a good product — if a model is disordered, incomplete or unclear, the final product will have many problems.

---

## Decision Nodes and Conditional Behaviour

### Decision Nodes

A **decision node** is an informatical object representing a choice point. Best practice: name decision nodes as questions. A **boolean object** is a decision node with two opposing states: "Yes"/"No".

### Condition vs Non-Condition Instrument Link

Critical distinction:

- **Condition instrument link** (with "c"): if the instrument does not exist or is not in the required state, the process is **skipped** and execution continues to the next process
- **Non-condition instrument link** (without "c"): if the instrument is missing, execution **stops and waits** until the instrument exists or transitions to the required state

This difference determines whether the system fails gracefully (skip) or blocks (wait).

### Iterative Subprocesses

Model iteration using decision nodes + invocation links: a boolean decision node evaluates a condition after each subprocess cycle. If "No" → invocation link loops back. If "Yes" → execution proceeds. The invocation link must not violate the top-to-bottom timeline within in-zoomed processes.

### Spatial Ordering in Object In-Zooming

In object in-zooming, spatial position of constituent objects has semantic meaning — unlike process in-zooming where only the vertical timeline matters. Spatial ordering applies to both physical objects (arrangement in a room, layout of components) and informatical objects (order of sections in an article, sequence of fields in a record).

---

## Model-Based Systems Engineering with OPM

### MBSE Overview

Model-Based Systems Engineering (MBSE) uses conceptual models to design and develop complex systems. Traditional approaches are text-based, lack standardized language, and have no formal verification/validation. OPM addresses these limitations with bimodal formal specification.

### Alternative Solution Concepts

Procedure for generating alternative solutions:

1. Create at least 3 distinct conceptual models
2. Apply holistic creative thinking
3. Distill the central concept of each — the underlying physical or logical principle of the architecture
4. Make implicit assumptions explicit

A **concept** is the core principle underlying a system architecture. **Alternative solution concepts** are distinct architectural approaches to the same problem.

### Preliminary Design Review (PDR)

Structured review with 8 sections:

1. Cover page
2. Problem statement
3. Purpose and motivation
4. Assumptions and constraints
5. Alternative solutions (≥3 conceptual models)
6. Selected solution with justification
7. Full lifecycle cost estimates and schedule
8. Risks and mitigation mechanisms (failure modes, prevention, recovery modelled with OPM)

### OPM as Common Blueprint

OPM serves as a discipline-neutral specification for detailed design of complex systems where diverse disciplines have their own languages. Detailed models typically span **5 to 10 levels of detail** in the OPD process tree.

### Virtual Integration

Advanced technique: integration of conceptual hardware models with actual executable software modules. The software controls the hardware models virtually through simulation, enabling early validation before physical prototyping.

---

## OPL Formal Syntax: Core EBNF

OPL conforms to ISO/IEC 14977:1996 EBNF. The formal syntax is necessarily incomplete for probability (§12.7), execution paths (§13), and complex participation constraints.

### Document Structure

```ebnf
OPL paragraph = OPL sentence, { new line, OPL sentence } ;
OPL sentence = OPL formal sentence, "." ;
OPL formal sentence = thing description sentence
    | procedural sentence
    | structural sentence
    | context management sentence ;
```

### Base Declarations

```ebnf
non zero digit = '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;
decimal digit = '0' | non zero digit ;
positive integer = non zero digit, {decimal digit} ;
name = letter, {string character} ;
capitalized word = upper case letter, {string character} ;
non capitalized word = lower case letter, {string character} ;
type identifier = "boolean" | "string" | number type | "enumerated" ;
number type = [prefix], "integer" | "float" | "double" | "short" | "long" ;
participation constraint = lower single | upper single | lower plural | upper plural
    | ( "0" | participation limit, [ " to ", participation limit ] ) ;
lower single = "a" | "an" | "an optional" | "at least one" ;
range clause = " is ", value name | " ranges from ", value name, " to ", value name ;
```

### Identifiers

```ebnf
object identifier = singular object name, [ " in ", measurement unit ], [ range clause ] ;
process identifier = singular process name | singular process name, " process" ;
thing identifier = object identifier | process identifier ;
state identifier = non capitalized word ;
tag expression = non capitalized phrase ;
```

Object names: capitalized singular/plural noun phrases. Process names: capitalized gerund phrases. State names: non-capitalized. Tags: non-capitalized phrases.

## OPL Formal Syntax: Sentence Families

### Thing Description Sentences

```ebnf
generic property sentence = thing identifier, " is ", [essence], [affiliation], [perseverance] ;
state enum sentence = object identifier, " can be ", state list | "..., and other states" ;
initial states sentence = "State ", state identifier, " of ", object identifier, " is initial" ;
final states sentence = "State ", state identifier, " of ", object identifier, " is final" ;
default state sentence = "State ", state identifier, " of ", object identifier, " is default" ;
```

Essence: Physical | Informatical. Affiliation: Systemic | Environmental. Perseverance: Persistent | Transient.

### Procedural Sentences

```ebnf
procedural sentence = transforming sentence | enabling sentence | control sentence ;
transforming sentence = consumption sentence | result sentence | effect sentence | change sentence ;

consumption sentence = process identifier, " consumes ", object with optional state list ;
result sentence = process identifier, " yields ", object with optional state list ;
effect sentence = process identifier, " affects ", object list ;
change sentence = in out specified change sentence | input specified change sentence
    | output specified change sentence ;

in out object change phrase = object identifier, " from ", input state, " to ", output state ;
input object change phrase = object identifier, " from ", input state ;
output object change phrase = object identifier, " to ", output state ;

enabling sentence = agent sentence | instrument sentence ;
agent sentence = object with optional state list, " handle ", process identifier ;
instrument sentence = process identifier, " requires ", object with optional state list ;

control sentence = event sentence | condition sentence | invocation sentence | exception sentence ;
consumption event sentence = object with optional state, " initiates ", process identifier,
    ", which consumes ", object identifier ;
effect event sentence = object identifier, " initiates ", process identifier,
    ", which affects ", object identifier ;
agent event sentence = object with optional state, " initiates and handles ", process identifier ;
instrument event sentence = object with optional state, " initiates ", process identifier,
    ", which requires ", object with optional state ;

invocation sentence = process identifier, " invokes ", process list
    | process identifier, " invokes itself " ;
overtime exception sentence = active process identifier,
    " occurs if duration of ", process identifier, " exceeds ", max duration time units ;
undertime exception sentence = active process identifier,
    " occurs if duration of ", process identifier, " falls short of ", min duration time units ;
```

XOR/OR variants use "exactly one of" / "at least one of" phrases for link fans. Condition sentences use "occurs if ... exists/is state, in which case ... otherwise ... is skipped" pattern.

### Structural Sentences

```ebnf
structural sentence = tagged structural sentence | aggregation sentence
    | characterization sentence | exhibition sentence
    | specialization sentence | instantiation sentence ;

aggregation sentence = object identifier, " consists of ", object list ;
exhibition sentence = thing identifier, " exhibits ", thing list ;
specialization sentence = thing list, " are ", thing identifier ;
instantiation sentence = thing identifier, " is an instance of ", thing identifier ;
tagged structural sentence = source thing, " ", tag expression, " ", destination thing ;
```

### Context Management Sentences

```ebnf
context management sentence = unfolding sentence | in zoom sentence ;
unfolding sentence = thing identifier, " unfolds in ", child OPD, " into ", thing list ;
in zoom sentence = process identifier, " zooms in ", child OPD, " into ",
    process list, ", in that sequence" ;
```

OPL for parallel subprocesses: `Process zooms into parallel A and B.`

---

## OPM Metamodel

The OPM model structure has parallel graphical and textual hierarchies:

- OPM Model → OPD Set (graphical) + OPL Spec (textual)
- OPD Set → OPDs → OPD Constructs → Thing Sets + Link Sets
- OPL Spec → OPL Paragraphs → OPL Sentences → Phrases (Reserved Phrases + Names)

A Basic Construct = exactly 2 things + 1 link. Compound constructs include link fans or more than 2 refinees.

### Link Model

Link consists of Source, Destination, and Connector (Line + Symbol + optional Tag + optional Path Label). Multiplicity has Lower&Upper Bounds: 0..1 (?), 0..* (*), 1..1 (none), 1..* (+).

### Thing Model

Thing = Object | Process. Objects may be Stateless (no states) or Stateful (with State Set). Stateful objects generate State-Specific Objects, each referring to a particular state.

### Structural Construct Model

Basic Structural Construct = Refineable + Refinee + Structural Link. Five variants: Aggregation-Participation, Exhibition-Characterization, Generalization-Specialization, Classification-Instantiation, Tagged Structural.

### Procedural Construct Model

Basic Procedural Construct = Object + Process + Procedural Link. Semantics: transformation, enablement, transformation & control, enablement & control. Transformation constructs decompose into Consumption, Effect and Result constructs. Enablement constructs decompose into Agent and Instrument constructs.

### New-Diagram In-Zooming and Out-Zooming Models

Annex C models in-zooming and out-zooming as first-class OPM processes:

- **New-Diagram In-Zooming**: requires `SDn`, performs Content Showing then Link Refining, yields `SDn+1`
- **New-Diagram Out-Zooming**: requires `SDn+1`, performs Link Abstracting then Content Hiding, yields `SDn`
- **Semi-Zoomed OPD**: transient intermediate object that exists only inside these transformations

Figure C.19 establishes the symmetric pair. Figure C.20 elaborates the migration of links from a refined process `P` toward subprocesses `P1`, `P2`, `P3` with consumee, agent, instrument and resultee links reassigned at the detailed level.

### Simplifying an OPD

Figure C.21 formalizes OPD simplification: an overloaded OPD can be reduced by abstracting a bounded set of processes and objects into a higher-level construct, provided the abstraction does not create illegal direct procedural links between peer processes. Simplification is therefore constrained by semantics, not just by layout.

### Process Performance Controlling Model (Annex C.6)

Canonical self-referential OPM model demonstrating a complete in-zoomed process hierarchy (SD → SD1 → SD1.1 → SD1.1.1 → SD1.1.1.1 → SD1.2 → SD1.2.1 → SD1.2.2 → SD1.2.3). Models how OPM controls process execution at runtime.

**SD: Process Performance Controlling** — An Executable Process invokes Process Performance Controlling, which affects the Involved Object Set (union of Preprocess Object Set, size r≥0, and Postprocess Object Set, size s≥0) and yields either a Success Message or a Failure Message (Abort Message or Cancel Message).

**SD1: In-zoomed** — Process Performance Controlling decomposes into Process Initiating → Process Performing, in sequence. Process Status tracks states: idle → started(t=0) → operating(time less than n) → completing(t=n) → completed(t=n) or aborted. Postcondition object: false → true.

**SD1.1: Process Initiating** — Decomposes into Precondition Evaluating → (Cancelling | Starting). If Precondition is false → Cancelling yields Cancel Message, Process Status returns to idle. If Precondition is true → Starting consumes Precondition, yields false Postcondition, changes Process Status to started(t=0).

**SD1.1.1: Precondition Evaluating** — Decomposes into Enabler Set Checking → Consumee & Affectee Set Checking → (Precondition Refuting | Precondition Confirming). Each check produces positive/negative results. If any negative → Precondition Refuting resets Status to idle. If all positive → Precondition Confirming sets Precondition to true.

**SD1.2: Process Performing** — Decomposes into Initial Process Performing → Main Process Performing → Final Process Performing.

- Initial: parallel Input State Exiting + Consumee Set Consuming. Status changes from started(t=0) to operating(time less than n).
- Main: loop of Elapsed Time & Duration Comparing → Enabler & Affectee Set Checking → Process Executing & Time Incrementing (invokes back to comparing). If Set Approval denied → Aborting & Notifying. If elapsed time equals duration → Finalizing. If elapsed time exceeds duration → Overtime Exception Handling.
- Final: parallel Resultee Set Generating + Output State Entering + Success Notifying. Status → completed(t=n), Postcondition → true.

This model demonstrates: multi-level in-zooming, state transitions across hierarchy levels, condition links for bypass, exception handling, parallel subprocesses, and the instrument-to-affectee role shift across abstraction levels.

---

## Dynamics and Simulation

### Executability

An OPM model provides executability — the ability to simulate a system by executing its model via animation in a software environment.

### Transformation Modes

| Mode | Meaning |
|------|---------|
| Construction | Object created/generated/yielded — radical transformation into existence |
| Effect | Object state changes — identity maintained |
| Consumption | Object eliminated/destroyed — ceases to exist |

Construction and consumption are more profound than effect (change existence vs change state).

### Timeline Principle

Default execution timeline within in-zoomed process: top → bottom. Sub-processes at same height execute in parallel. Exception Exiting process causes unconditional prompt exit regardless of graphical position.

### Timed Events

State events can represent time events. System Clock objects with specific values trigger processes at defined times.

### Lifespan Diagram

Shows for any point in time: which objects exist, what state each is at, and which processes are active. Useful for tracking state transitions over system lifetime.

### Process Duration Properties

| Property | Description |
|----------|-------------|
| Duration | Actual elapsed time (runtime) |
| Minimal Duration | Minimum allowable time |
| Expected Duration | Statistical mean |
| Maximal Duration | Maximum allowable time |
| Duration Distribution | Probability function (Normal, Uniform, Exponential) with parameters |

System time unit is default for all processes unless explicitly overridden.

**Graphical placement**: duration values display **inside the process ellipse**, below the process name and time unit. Minimal duration appears to the **left**, expected duration in the **center**, maximal duration to the **right**. Example: `Processing [min] (30.0, 45.6, 60.0)` with distribution `normal, mean=45.6, sd=7.3`.

### Duration Examples

Annex D adds four recoverable example patterns:

1. **Figure D.5 / Processing Duration metamodel**: compact process notation can encode minimal, expected and maximal duration together with distribution parameters; actual `Duration` remains a runtime property. Canonical values: `Duration [min] = 63.3`, `Expected Duration = 45.6`, `Maximal Duration = 60.0`, distribution `normal, mean=45.6, sd=7.3`.
2. **Figure D.6 / Distribution variants**: exponential, normal and uniform distributions can parameterize the same process depending on domain assumptions and time units. Canonical examples: `exponential, lambda=5.6`, `normal, mean=1.63, sd=0.16`, `uniform, a=3, b=5`.
3. **Figure D.7 / Overtime exception**: if actual duration exceeds maximal duration, Overtime Exception Handling occurs and may affect the same affectee as the main process. Canonical case: `Processing [min] (30.0, 45.6, 60.0)`, `uniform, a=5.0, b=70.0`, runtime duration `63.3`, instance id `1`.
4. **Figure D.8 / Undertime exception**: if actual duration falls short of the minimal threshold, Undertime Exception Handling occurs under the symmetric rule. Canonical case: the same duration envelope and distribution, runtime duration `23.4`, instance id `2`.

---

## Guidance and Naming Conventions

### OPD Best Practices

- No more than one page/screen per OPD
- Maximum 20-25 things per OPD
- No occlusion between things
- Roughly same number of links as things
- Minimize link crossings
- Links should not cross thing areas

### Element Representation Principle

Any model element may appear in any number of OPDs. Include only elements necessary for grasping a certain aspect.

### Multiple Thing Copies

To avoid long crossing links, duplicate thing symbols (small offset behind the repeated thing) may appear in the same OPD. Use sparingly.

### Naming Rules

| Element | Convention | Examples |
|---------|-----------|----------|
| Object | Singular noun, capitalized. Plural → add "Set" (inanimate) or "Group" (humans). Max multi-word phrase. | `Ingredient Set`, `Customer Group`, `Apple Cake` |
| Process | Gerund (verb+ing), capitalized. Patterns: verb, noun-verb, adjective-verb, adjective-noun-verb. Max 4 words. | `Making`, `Cake Making`, `Automatic Crash Responding` |
| State | Non-capitalized passive form of owning object. | `painted`, `inspected`, `pre-cut` |
| Link tag | Non-capitalized phrase | `serves`, `relates to` |

**Capitalization convention**: first letter of each word in thing names capitalized; state names and link tags not capitalized. In OPL text, object and process names appear in **bold face**. State names appear in bold without capitalization. By default, a noun identifies an object.

**A state cannot exist without its owning object** — it has meaning only in the context of the object to which it belongs.

**Consumed object disappears at process start** — by assumption, the consumee ceases to exist as soon as the process begins execution, not at completion.

**Procedural link uniqueness — dual control roles**: an object may additionally be a trigger (event modifier "e") and/or a conditioning object (condition modifier "c") simultaneously, beyond its single transformee or enabler role.

### Thing Importance Principle

Relative importance of a thing is generally proportional to the highest OPD in the hierarchy where it appears.

---

## Applied Examples

Canonical examples from ISO/PAS 19450 and complementary sources demonstrating OPM notation in practice.

### Steel Rod Machining (State-Specified Links)

Objects: Raw Metal Bar (states: pre-cut, cut), Part (states: pre-tested, tested). Processes: Cutting (environmental), Machining (physical), Testing (environmental). Enablers: Machine Operator (agent), Coolant (instrument).

OPD composition: Cutting changes Raw Metal Bar from pre-cut to cut (input-output-specified effect). Machining consumes cut Raw Metal Bar (state-specified consumption) and yields pre-tested Part (state-specified result). Machine Operator handles Machining (agent link with black lollipop). Machining requires Coolant (instrument link with white lollipop). Testing changes Part from pre-tested to tested (input-output-specified effect).

Key visual: state-specified links originate from/terminate at specific rounded-corner rectangles inside their owning objects, not from the object rectangle itself.

### Check-Based Paying (In-Zooming with State Transitions)

Object: Check (states: blank → signed → endorsed → cashed & cancelled). Attribute: Keeper (states: payer → payee → financial institution). Agents: Payer, Payee, Bank.

SD1 shows Check-Based Paying in-zoomed into 4 sequential subprocesses:

1. Writing & Signing — changes Check blank→signed (Payer handles)
2. Delivering & Accepting — changes Keeper payer→payee (Payer and Payee handle)
3. Endorsing & Submitting — changes Check signed→endorsed and Keeper payee→financial institution (Payee handles)
4. Cashing & Cancelling — changes Check endorsed→cashed & cancelled and Keeper financial institution→payer (Bank handles)

Key visual: large enclosing ellipse for Check-Based Paying contains 4 smaller ellipses arranged top-to-bottom. Objects outside the ellipse connect via state-specified links to specific subprocesses. Keeper values connect to corresponding agent objects via unidirectional null-tagged structural links.

### Dish Washing (Role Shift Across Abstraction)

SD: Household User handles Dish Washing. Dish Washing requires Dishwasher (instrument link — white lollipop). Dish Washing consumes Soap. Dish Washing affects Dish Set.

SD1 (in-zoomed): Dish Washing decomposes into Dish Loading → Detergent Inserting → Dish Cleaning & Drying → Dish Unloading. Dishwasher (states: empty, loaded) becomes an affectee at this level — Dish Loading changes it from empty to loaded, Dish Unloading changes it back to empty. At SD level, Dishwasher appears as instrument because its initial and final states are the same (empty).

Key visual: demonstrates that an object can be an instrument at one abstraction level and an affectee at a more detailed level. Split state-specified transforming links resolve the underspecification when in-zooming.

### Safe Opening (Logical Operators)

XOR example: exactly one of Safe Owner A and Safe Owner B handles Safe Opening (dashed arc across two agent link fans). OR example: at least one of Safe Owner A and Safe Owner B handles Safe Opening (two concentric dashed arcs). AND example: Safe Opening requires Key A, Key B, and Key C (three separate non-touching instrument links).

Key visual: AND = links don't touch on process contour. XOR = single dashed arc at convergent point. OR = double dashed arc at convergent point.

### Vehicle Specialization (Discriminating Attribute)

Vehicle exhibits Travelling Medium. Travelling Medium can be ground, air, water surface. Car, Aircraft, and Ship are Vehicles (generalization-specialization with empty triangle). Car exhibits ground Travelling Medium. Aircraft exhibits air Travelling Medium. Ship exhibits water surface Travelling Medium (state-specified characterization links — exhibition-characterization triangle from specialization to specific attribute value).

Key visual: discriminating attribute appears once with all values; each specialization connects to its corresponding value via state-specified characterization link, avoiding redundancy.

### Home Safety (Asynchronous Process)

Home Safety Maintaining consists of Burglary Handling, Fire Protecting, and Earthquake Alarming (aggregation-participation link — filled black triangle — not in-zooming). Since subprocess order is unknown, unfolding is used instead of in-zooming. Detection Module exhibits Detected Threat (states: burglary, fire, earthquake). Each state-specified instrument event link initiates the corresponding subprocess.

Key visual: asynchronous = aggregation-participation triangle from process to subprocesses (unordered). Synchronous = in-zoomed enlarged ellipse with vertical subprocess ordering.

### Coffee Making (Structure-Behaviour-Function)

Structure: Coffee Machine consists of Water Tank, Milk Frother, Water Heater, Capsule Compartment, Cup Holder, Operation Button. Behaviour: Making Coffee (main process) decomposes into Water Heating, Milk Frothing, Coffee Preparing, Milk Adding. Making Coffee consumes Water, Milk, and intact Capsule; yields Coffee Beverage in Cup. Function: beneficiary is Coffee Drinker; function changes Satisfaction from unsatisfied to satisfied.

### Electric Car Operation (SD Components)

Purpose: change Business Success of Company Stakeholder Group from current to improved. Function: Electric Car Operating (main process) changes Electric Car from stopped to moving. Agents: Driver. Instruments: Electric Car Operating System. Environment: Terrain Type, Regulations. Problem: traditional human-centered manufacturing → partial automation level.

### Auxiliary Social and Socio-Technical Examples

- **Air Traffic Control**: Pilot and Air Traffic Controller are agents; Control Tower is an instrument. Used to contrast agent vs instrument semantics.
- **MOOC Learning**: Student Group acts as agent; MOOC platform acts as instrument. Useful for non-physical socio-technical systems.
- **Online Professional Identity Management**: online profile can represent the user through a tagged structural link; the identity-management system and internet connection act as instruments/environment.
- **Baggage Transportation**: main function changes baggage location from origin airport to destination airport; useful for state change and SD function framing.
- **Conference System**: organizer and ushers are agents; facilities/equipment are instruments; weather can be environmental despite the system being social.

For OPCloud tool procedures, UI workflows and feature details, see `urn:fxsl:kb:opcloud-tutorial-videos`.
