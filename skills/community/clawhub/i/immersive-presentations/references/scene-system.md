# Scene System

A scene is a staged explanation with visual state, continuity, interaction, and a narrative beat.

## Scene Contract

Each scene should specify:

- `id`: stable scene identifier.
- `role`: what the scene does in the story.
- `question`: the audience question it answers.
- `visual metaphor`: the object/system that carries the concept.
- `persistent objects`: what continues from previous scenes.
- `camera`: frame, movement, zoom, pan, orbit, or focus.
- `motion intent`: why objects move.
- `interaction`: what the user/presenter can manipulate.
- `transition in/out`: how continuity is preserved.
- `accessibility`: text alternatives, keyboard behavior, reduced motion.
- `presenter notes`: speaker intent.

## Scene Archetypes

### World Build

Build the system layer by layer. Use for context and orientation.

Example: a blank workspace fills with documents, people, queues, constraints, and decisions.

### Pressure Cooker

Increase visual pressure until the problem is obvious.

Example: requests accelerate until a manual review queue bends, overflows, or fragments.

### Mechanism Reveal

Show how a hidden process works.

Example: a query travels through embedding, retrieval, ranking, context assembly, and answer generation.

### Side-By-Side Transformation

Compare two approaches with synchronized motion.

Example: one path retrieves evidence while another plans tool calls; the audience sees where each succeeds and fails.

### Lens Change

Use camera movement or layer toggles to change perspective.

Example: zoom from business process to system architecture to token-level trace.

### Tradeoff Field

Let the audience adjust variables and see consequences.

Example: sliders for latency, accuracy, autonomy, cost, risk, and human control.

### Failure Mode

Demonstrate what breaks and why.

Example: an agent loops, a retrieval system returns stale evidence, or a dashboard hides uncertainty.

### Decision Map

Resolve complexity into a usable framework.

Example: a matrix where scenarios move into recommended architecture zones.

### Memory Image

End with a simple, memorable visual that carries the thesis.

Example: a control tower where search, tools, humans, and agents coordinate in visible layers.

## Visual Metaphors

Choose metaphors that preserve structure:

- Networks for relationships, dependencies, graph reasoning, contagion, supply chains.
- Maps for geography, markets, territories, risk surfaces, operating environments.
- Machines for workflows, pipelines, transformations, operations.
- Lenses for perspective, focus, abstraction, model interpretation.
- Theaters/stages for competing actors, roles, coordination.
- Ecosystems only when feedback loops and adaptation are central.
- Physical fields for forces, gradients, optimization, uncertainty.

Avoid metaphors that look good but distort the concept. If the metaphor cannot explain the mechanism, replace it.

## Object Permanence

Objects that represent the same concept should persist across scenes. Avoid destroying and recreating them visually.

Useful techniques:

- Stable IDs for entities.
- Shared layout coordinates across scenes.
- Morphing between representations.
- Persistent labels that change position but keep identity.
- Ghost trails or dimmed previous states for comparison.
- Camera movement over hard scene replacement.

## Anti-Deck Composition

Instead of:

```text
Title
- Bullet
- Bullet
- Bullet
```

Use:

```text
One strong visual system
Short spoken/narrative caption
Labels attached to objects
Motion that reveals sequence, causality, or contrast
```

A scene can contain text, but the text should serve the visual explanation.

