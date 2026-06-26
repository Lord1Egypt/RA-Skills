# PlantUML Syntax Quick Reference

## Themes

Built-in themes (set near the top of the file, after `@startuml`):

```plantuml
!theme plain               ' minimal black/white
!theme cerulean-outline    ' clean blue/white
!theme materia             ' material design
!theme spacelab            ' light, professional
!theme sketchy             ' hand-drawn look
!theme cyborg              ' dark mode
```

Full list: https://the-lum.github.io/puml-themes-gallery/

## Common Skinparam

```plantuml
skinparam classAttributeIconSize 0   ' hide visibility icons in class diagrams
skinparam packageStyle rectangle     ' rectangle-style packages
skinparam actorStyle awesome         ' stick-figure actors
skinparam defaultFontSize 12
skinparam dpi 150                    ' resolution control
skinparam shadowing false            ' disable shadows
skinparam monochrome true            ' grayscale output
skinparam backgroundColor #FFFFFF
```

For consistency, prefer the shared include:

```plantuml
!include /home/guoxh/.openclaw/skills/plantuml/references/default-style.iuml
```

## Use Case Diagram

### Actors & Use Cases
```plantuml
actor "Regular User" as User
actor Admin
usecase "Login" as UC1
usecase "Manage Users" as UC2
```

### Relationships
```plantuml
User --> UC1
UC2 .> UC1 : <<include>>     ' dashed arrow, FROM base TO included
UC3 .> UC1 : <<extend>>      ' dashed arrow, FROM extension TO base
Admin <|-- User              ' generalization (Admin inherits User)
```

### System Boundary
```plantuml
rectangle "System Name" {
  usecase "UC1" as UC1
  usecase "UC2" as UC2
}
```

## Class Diagram

### Visibility
- `+` public, `-` private, `#` protected, `~` package

### Relationships
```plantuml
ClassA <|-- ClassB              ' generalization (inheritance)
ClassA *-- ClassB               ' composition (filled diamond on A)
ClassA o-- ClassB               ' aggregation (hollow diamond on A)
ClassA --> ClassB               ' association
ClassA ..> ClassB               ' dependency (dashed)
ClassA ..|> InterfaceB          ' realization (dashed, hollow triangle)
```

### Multiplicity & Labels
```plantuml
ClassA "1" --> "0..*" ClassB : label >
```

### Abstract & Interfaces
```plantuml
abstract class Shape { }        ' name in italics
interface Drawable { }          ' <<interface>> stereotype
```

### Notes
```plantuml
note left of ClassA : Some note
note right of ClassB
  Multi-line note
end note
```

## Sequence Diagram

### Messages
```plantuml
A -> B  : synchronous call
A ->> B : asynchronous call
A --> B : return (dashed)
A -> A  : self-call
```

### Activation Bars
```plantuml
A -> B : msg
activate B
B --> A : reply
deactivate B
```

### Fragments
```plantuml
alt condition 1
  A -> B : msg1
else condition 2
  A -> B : msg2
end

opt optional condition
  A -> B : msg3
end

loop for each item
  A -> B : msg4
end

par parallel
  A -> B : msg5
else
  A -> C : msg6
end
```

### Grouping & Notes
```plantuml
group Description
  A -> B : msg
end

note left of A : note text
note over A, B : note spanning lifelines
```

### Delay & Separators
```plantuml
... 5 minutes later ...
== Section Title ==
```

## Activity Diagram

### Basic Flow
```plantuml
start
:Action 1;
:Action 2;
stop
```

### Branching
```plantuml
if (condition?) then (yes)
  :action A;
else (no)
  :action B;
endif
```

### Loops
```plantuml
repeat
  :action;
repeat while (more?)
```

```plantuml
while (condition?) is (yes)
  :action;
endwhile (no)
```

### Parallel & Swimlanes
```plantuml
|Swimlane 1|
start
:action A;
|Swimlane 2|
:action B;
|Swimlane 1|
:action C;
stop
```

### Fork/Join
```plantuml
start
fork
  :branch 1;
fork again
  :branch 2;
end fork
stop
```

## State Diagram

```plantuml
[*] --> State1
State1 --> State2 : event1 [guard] / action
State2 --> State3 : event2
State3 --> [*]

' Composite state
state "Active" as Active {
  [*] --> Running
  Running --> Paused : pause
  Paused --> Running : resume
}
State1 --> Active : activate
Active --> [*] : deactivate
```

## Component Diagram

```plantuml
component [Component A] as CA
component [Component B] as CB
interface "API" as API

CA -right- API
API -right- CB
```

## Deployment Diagram

```plantuml
node "Web Server" as WS {
  component [Web App] as WA
}
node "DB Server" as DB {
  database [Database] as D
}
WA ..> D : JDBC
```

## ER Diagram

```plantuml
entity "Customer" as customer {
  * customer_id : BIGINT <<PK>>
  --
  * name : VARCHAR
  * email : VARCHAR
}
entity "Order" as order {
  * order_id : BIGINT <<PK>>
  --
  * customer_id : BIGINT <<FK>>
  * order_date : DATE
}
customer ||--o{ order
```

## Timing Diagram

```plantuml
@startuml TimingExample
robust "Browser" as B
concise "Network" as N

@0
B is Idle
N is Down

@+100
B is Connecting
N is Up

@+200
B is Active

@+500
B is Idle
N is Down
@enduml
```

## Mindmap

```plantuml
@startmindmap
* Project
** Backend
*** API
*** DB
** Frontend
*** Web
*** Mobile
** Ops
*** CI/CD
*** Monitoring
@endmindmap
```

## WBS (Work Breakdown Structure)

```plantuml
@startwbs
* Release 1.0
** Design
*** Use cases
*** Data model
** Implementation
*** Backend
*** Frontend
** Testing
*** Unit
*** Integration
@endwbs
```

## Gantt

```plantuml
@startgantt
Project starts 2026-06-01
[Design] lasts 10 days
[Implementation] lasts 20 days
[Implementation] starts at [Design]'s end
[Testing] lasts 7 days
[Testing] starts at [Implementation]'s end
@endgantt
```

## JSON / YAML Visualization

```plantuml
@startjson
{
  "name": "Order",
  "id": 42,
  "items": [
    { "sku": "A1", "qty": 2 },
    { "sku": "B2", "qty": 1 }
  ]
}
@endjson
```

## Common Pitfalls

1. **Reserved words:** Avoid using `end`, `subgraph`, `graph`, `flowchart` as node/participant IDs.
2. **Quotes required:** Use double quotes around labels containing `()`, `,`, `:`, or `/`.
3. **Include vs Extend direction:**
   - `<<include>>`: arrow FROM base use case TO included use case
   - `<<extend>>`: arrow FROM extending use case TO base use case
4. **Composition diamond:** Filled diamond (`*--`) is on the **whole/owner** side, not the part side.
5. **Sequence alt/else:** Always close with `end`.
6. **C4 stdlib + custom theme:** Don't combine `!theme` with `<C4/...>` unless tested — C4 brings its own colors.
7. **`!include` paths:** Use absolute paths or paths relative to the `.puml` file's directory.
