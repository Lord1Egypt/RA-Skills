# Other Diagram Types

State, git graph, gantt, pie, mind map, C4 context, and user journey.

## State Diagram

```mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Processing : payment_received
  Processing --> Shipped : packed
  Shipped --> Delivered : received
  Processing --> Cancelled : cancel
  Pending --> Cancelled : cancel
  Delivered --> [*]
  Cancelled --> [*]
```

### Composite States

```mermaid
stateDiagram-v2
  [*] --> Active

  state Active {
    [*] --> Idle
    Idle --> Running : start
    Running --> Idle : stop
  }

  Active --> Terminated : shutdown
  Terminated --> [*]
```

### Choice (Branching)

```mermaid
stateDiagram-v2
  state check <<choice>>
  [*] --> check
  check --> Approved : score > 700
  check --> Rejected : score <= 700
```

### Concurrency

Use `--` to split a composite state into concurrent regions:
```mermaid
stateDiagram-v2
  [*] --> Active
  state Active {
    [*] --> Process1
    --
    [*] --> Process2
  }
```

### Notes

```mermaid
stateDiagram-v2
  State1 --> State2
  note right of State1
    Important note here
  end note
```

Best practices: start from `[*]`, use clear transition labels, limit composite depth to ~2 levels.

---

## Git Graph

```mermaid
gitGraph
  commit id: "Initial commit"
  branch develop
  checkout develop
  commit id: "Add feature A"
  commit id: "Add feature B"
  checkout main
  merge develop id: "Release v1.0"
  branch hotfix
  checkout hotfix
  commit id: "Fix critical bug"
  checkout main
  merge hotfix id: "Hotfix v1.0.1"
```

Tag a commit or merge with `tag: "v1.0"`.

---

## Gantt Chart

```mermaid
gantt
  title Project Timeline
  dateFormat YYYY-MM-DD
  axisFormat %b %d

  section Planning
  Requirements     :done,   a1, 2024-01-01, 7d
  Design           :active, a2, after a1, 5d

  section Development
  Backend API      :        b1, after a2, 14d
  Frontend UI      :        b2, after a2, 14d

  section Testing
  Integration Test :        c1, after b1, 7d
  Go live          :milestone, m1, after c1, 0d
```

Task states: `done`, `active`, `crit`, or omit for upcoming. `milestone` marks a zero-duration point.

---

## Pie Chart

```mermaid
pie title Language Distribution
  "JavaScript" : 45
  "Python" : 30
  "Go" : 15
  "Other" : 10
```

---

## Mind Map

```mermaid
mindmap
  root((Project))
    Frontend
      React
      CSS
      TypeScript
    Backend
      Node.js
      PostgreSQL
      Redis
    DevOps
      Docker
      Kubernetes
      CI/CD
```

---

## C4 Context Diagram

```mermaid
C4Context
  title System Context Diagram

  Person(user, "User", "A user of the system")
  System(system, "Main System", "The core application")
  System_Ext(external, "External API", "Third-party service")

  Rel(user, system, "Uses")
  Rel(system, external, "Calls")
```

---

## User Journey

```mermaid
journey
  title Checkout Experience
  section Browse
    View product: 5: User
    Add to cart: 4: User
  section Pay
    Enter address: 3: User
    Confirm payment: 2: User, System
```

Each step scores satisfaction 1–5, followed by the actors involved.
