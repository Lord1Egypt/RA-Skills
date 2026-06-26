# Mermaid Syntax Detailed Reference

> Official Documentation: https://mermaid.js.org/intro/syntax-reference.html

## Complete List of Flowchart Node Shapes

```
A["Rectangle — Default"]        A[/"Parallelogram — I/O"/]
A(["Rounded Rectangle"])          A(("Circle"))
A{"Diamond — Decision"}         A[["Subroutine"]]
A[("Database — Cylinder")]     A>"Tag — Flag"]
A((("Double Circle — Start/End"))) A{{"Hexagon"}}
A[/"Trapezoid 1"\]            A[\"Trapezoid 2"/]
```

## Complete List of Sequence Diagram Arrow Types

```
->>     Solid arrow (synchronous call)
-->>    Dashed arrow (return)
->      Solid, no arrowhead
-->     Dashed, no arrowhead
-x      Solid, cross tail (async loss)
--)     Solid, circle tail (async message)
-x      Solid, cross tail
```

## Flowchart Subgraphs (Grouping)

```
flowchart LR
    subgraph Frontend
        A["React App"]
        B["State Management"]
    end
    subgraph Backend
        C["API Server"]
        D["Database"]
    end
    A --> C
    B --> C
    C --> D
```

## Sequence Diagram Advanced Features

### Auto Numbering
```
sequenceDiagram
    autonumber
    A->>B: Message 1
    B->>C: Message 2
```

### Create/Destroy Participants
```
sequenceDiagram
    create participant C
    A->>C: Create
    destroy C
    A-xC: Destroy
```

### Critical Section
```
sequenceDiagram
    critical Critical Operation
        A->>B: Non-interruptible
    option Timeout Handling
        A->>B: Retry
    end
```

### Parallel Blocks
```
sequenceDiagram
    par Parallel Task 1
        A->>B: Execute simultaneously
    and Parallel Task 2
        A->>C: Execute simultaneously
    end
```

## Class Diagram Annotations and Generics

```
classDiagram
    class Box~T~ {
        +T value
        +get() T
        +set(T val) void
    }
    Box : <<Generic Class>>

    class Animal {
        <<abstract>>
        +makeSound()*
    }

    note "This is an example class" as N1
    Animal .. N1
```

## Gantt Chart Additional Options

```
gantt
    title Project Plan
    dateFormat YYYY-MM-DD
    axisFormat %m/%d
    tickInterval 7d
    excludes weekends

    section Phase 1
    Task A    :a1, 2026-01-01, 30d
    Task B    :a2, after a1, 20d
```

## State Diagram Concurrent States

```
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> TaskA
        TaskA --> TaskB
        TaskB --> [*]
        --
        [*] --> TaskC
        TaskC --> TaskD
        TaskD --> [*]
    }

    Active --> [*]
```

Use `--` to separate concurrent sub-states.

## ER Diagram Key Types

```
erDiagram
    USER {
        int id PK "Primary Key"
        string name
        string email UK "Unique Key"
    }
    ORDER {
        int id PK
        int userId FK "Foreign Key → USER"
    }
```

## Mind Map More Shapes

```
mindmap
  root
    (Circle)
      [Rounded Rectangle]
        Cloud))
          ))Bang))
            Hexagon))
```

Available icons:
- Font Awesome icons: `::icon(fa fa-book)`
- Custom icons only supported by certain renderers

## Sankey Diagram

```
sankey-beta
    Source,A,Target,B,100
    Source,A,Target,C,50
    Source,B,Target,D,80
    Source,C,Target,D,20
```

## Quadrant Chart

```
quadrantChart
    title Tech Radar
    x-axis "Low Value" --> "High Value"
    y-axis "Hard to Implement" --> "Easy to Implement"
    quadrant-1 "Key Investment"
    quadrant-2 "Sustain Advantage"
    quadrant-3 "Phase Out"
    quadrant-4 "Observe and Assess"
    "React": [0.8, 0.7]
    "jQuery": [0.1, 0.9]
    "WebAssembly": [0.6, 0.2]
    "Svelte": [0.5, 0.5]
```

## Configuration Directives

Use on the first line inside the code block:

```
%%{init: { ... }}%%
```

Common configurations:

```json
{
  "theme": "default",
  "themeVariables": {
    "primaryColor": "#bb2528",
    "primaryTextColor": "#fff",
    "primaryBorderColor": "#7C0000",
    "lineColor": "#F8B229",
    "secondaryColor": "#006100",
    "tertiaryColor": "#fff"
  },
  "flowchart": {
    "htmlLabels": true,
    "curve": "basis"
  },
  "sequence": {
    "mirrorActors": false,
    "actorMargin": 50
  },
  "gantt": {
    "titleTopMargin": 25,
    "barHeight": 20
  }
}
```

## Common Error Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Diagram does not render | Syntax error | Check if quotes are paired and arrow syntax is correct |
| Chinese characters garbled | Encoding issue | Use UTF-8; wrap Chinese nodes in quotes |
| Poor layout | Incorrect direction | Try switching between `TD`/`LR` |
| Lines too cluttered | Too many nodes | Use `subgraph` for grouping |
| `graph` warning | Deprecated | Switch to `flowchart` |