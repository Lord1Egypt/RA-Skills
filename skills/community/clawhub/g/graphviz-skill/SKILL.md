---
name: graphviz
description: "Generate architecture diagrams, flowcharts, dependency graphs, state machines, and other visualizations from natural language descriptions using Graphviz DOT. Use when: user asks to draw, visualize, or diagram something -- architecture, flow, schema, dependencies, states, ER diagram, block diagram. Returns a clickable GraphvizOnline link with rendered preview."
metadata: { "openclaw": { "emoji": "📐" } }
---

# Graphviz Diagram Generator

Generate diagrams from natural language descriptions and return a clickable link to GraphvizOnline with the rendered preview.

## When to Use

- "Draw the architecture of ..."
- "Make a diagram showing ..."
- "Visualize the data flow between ..."
- "Create a flowchart for ..."
- "Show dependencies between ..."
- "State machine diagram for ..."
- "ER diagram of ..."
- Any request involving diagrams, graphs, schemas, architecture visualization

## Workflow

1. If the user's description is vague, ask one clarifying question before generating
2. Generate valid DOT code following the conventions below
3. Show the DOT code in a fenced ```dot block
4. Construct the URL: `https://dreampuf.github.io/GraphvizOnline/#` + URL-encoded DOT code
5. Output the link on its own line so it's clickable

## DOT Code Conventions

### Graph type

- `digraph` for directed graphs (architecture, flows, dependencies, state machines)
- `graph` for undirected graphs (relationships, peer networks)

### Layout direction

- `rankdir=LR` for wide/horizontal layouts (architecture, pipelines)
- `rankdir=TB` for tall/vertical layouts (flowcharts, hierarchies)

### Node shapes by component type

- `box` or `component` -- services, applications, modules
- `cylinder` -- databases, storage
- `ellipse` -- users, actors, external systems
- `diamond` -- decision points (flowcharts)
- `folder` -- directories, namespaces, packages
- `note` -- annotations, comments
- `record` -- structured data, ER entities (use `<field>` syntax for fields)
- `doublecircle` -- start/end states (state machines)
- `circle` -- intermediate states

### Grouping

- Use `subgraph cluster_name { label="Group Name"; ... }` to group related components
- Give clusters a light fill: `style=filled; color=lightgrey;`

### Styling

- Use `fontname="Helvetica"` on the graph for clean rendering
- Color-code edges or nodes to distinguish component types when helpful
- Keep labels concise -- full names on nodes, short verbs on edges
- Use `style=dashed` for optional or async connections

### Edges

- Label edges with the relationship or protocol: `->` with `[label="HTTP"]`, `[label="gRPC"]`, `[label="publishes"]`
- Use `style=dashed` for async/optional connections
- Use `dir=both` for bidirectional relationships

## URL Construction

Construct the GraphvizOnline URL by URL-encoding the entire DOT source and appending it as a hash fragment:

```
https://dreampuf.github.io/GraphvizOnline/#<URL-encoded DOT code>
```

The DOT code must be encoded with standard percent-encoding (spaces -> `%20`, newlines -> `%0A`, etc.).

## Output Format

Always output in this order:

1. Brief description of what the diagram shows (1 sentence)
2. The DOT source in a fenced ```dot block
3. The clickable GraphvizOnline link on its own line

Example output structure:

> Architecture showing the API gateway routing to backend services:
>
> ```dot
> digraph { ... }
> ```
>
> [Open in GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/#digraph%20%7B%20...%20%7D)
