---
name: knowledge-graph-memory
description: Builds and maintains a knowledge graph for long-term memory with concept drift detection and temporal reasoning. Use when storing structured knowledge, detecting concept changes over time, or performing temporal queries.
---

# Knowledge Graph Memory

Long-term memory system with knowledge graph, concept drift detection, and temporal reasoning.

## When to Use

- Building knowledge graphs from concepts and relationships
- Detecting concept drift over time
- Temporal reasoning and time-based queries
- Long-term memory storage with consolidation

## Usage

```javascript
const { KnowledgeGraph, Memory } = require('./skills/knowledge-graph-memory');

// Create a knowledge graph
const kg = new KnowledgeGraph();

// Add concepts
kg.addConcept('AI', { category: 'technology', importance: 0.9 });
kg.addConcept('Machine Learning', { category: 'technology' });

// Link concepts
kg.link('AI', 'Machine Learning', 'includes');

// Find related concepts
const related = kg.getRelated('AI');

// Detect concept drift
const drift = kg.detectDrift('AI');

// Search concepts
const results = kg.search({ name: 'AI' });
```

## Features

- **Knowledge Graph**: Nodes (concepts) and edges (relationships)
- **Concept Drift Detection**: ADWIN, DDM, statistical methods
- **Temporal Reasoning**: Time-based queries and event tracking
- **Memory Consolidation**: Promote important memories, forget unused ones

## API

### KnowledgeGraph

```javascript
const kg = new KnowledgeGraph({
  maxNodes: 10000,
  consolidationThreshold: 0.1,
  driftDetection: { method: 'statistical', threshold: 2.0 }
});

// Add and get concepts
kg.addConcept(name, properties);
kg.getConcept(idOrName);

// Create relationships
kg.link(sourceId, targetId, edgeType, properties);

// Query
kg.getRelated(conceptId, edgeType);
kg.findPath(startId, endId, maxDepth);
kg.search({ name: 'pattern', type: 'concept' });

// Drift detection
kg.detectDrift(conceptId);

// Memory management
kg.consolidate();
kg.removeConcept(id);

// Serialization
kg.toJSON();
KnowledgeGraph.fromJSON(data);
```

### Concept

```javascript
const concept = new Concept({
  name: 'AI',
  type: 'concept',
  properties: { category: 'technology' },
  importance: 0.8
});

concept.access();  // Increment access count
concept.update({ newProperty: 'value' });  // Update with history
```

### DriftDetector

```javascript
const detector = new DriftDetector({
  method: 'statistical',
  windowSize: 100,
  threshold: 2.0
});

const result = detector.addSample(value);
// { drift: boolean, warning: boolean, mean, stdDev }
```

### TemporalReasoner

```javascript
const reasoner = new TemporalReasoner();

reasoner.addEvent({ type: 'concept_added', conceptId: 'AI' });
reasoner.getEventsInRange(start, end);
reasoner.getEventsBefore(time);
reasoner.getEventsAfter(time);
reasoner.getRecentEvents(10);
```

### Memory

```javascript
const memory = new Memory({
  shortTermMaxSize: 100,
  consolidationInterval: 3600000
});

memory.remember('key', { data: 'value' }, { importance: 0.8 });
memory.recall('key');
memory.forget('key');
memory.consolidate();
```

## Node Types

- `CONCEPT`: Abstract concept
- `ENTITY`: Concrete entity
- `EVENT`: Time-based event
- `FACT`: Verified fact
- `RELATION`: Relationship node

## Edge Types

- `IS_A`: Inheritance relationship
- `HAS_A`: Composition relationship
- `RELATED_TO`: Generic relationship
- `CAUSES`: Causal relationship
- `PRECEDES`: Temporal ordering
- `INCLUDES`: Set membership
- `SIMILAR_TO`: Similarity relationship
- `DERIVED_FROM`: Derivation relationship

## Example: Building a Knowledge Base

```javascript
const { KnowledgeGraph, EdgeType } = require('./skills/knowledge-graph-memory');

const kg = new KnowledgeGraph();

// Build knowledge structure
kg.addConcept('Technology', { category: 'domain' });
kg.addConcept('AI', { category: 'field' });
kg.addConcept('Machine Learning', { category: 'subfield' });
kg.addConcept('Neural Networks', { category: 'technique' });
kg.addConcept('Deep Learning', { category: 'technique' });

// Create relationships
kg.link('AI', 'Technology', EdgeType.IS_A);
kg.link('Machine Learning', 'AI', EdgeType.IS_A);
kg.link('Neural Networks', 'Machine Learning', EdgeType.IS_A);
kg.link('Deep Learning', 'Neural Networks', EdgeType.IS_A);
kg.link('Deep Learning', 'Machine Learning', EdgeType.RELATED_TO);

// Query the graph
const mlRelated = kg.getRelated('Machine Learning');
const path = kg.findPath('Deep Learning', 'Technology');

console.log('ML related concepts:', mlRelated.map(r => r.concept.name));
console.log('Path:', path?.map(c => c.name));
```

## Example: Concept Drift Detection

```javascript
const { KnowledgeGraph } = require('./skills/knowledge-graph-memory');

const kg = new KnowledgeGraph();
kg.addConcept('User Behavior', { pattern: 'initial' });

// Simulate concept evolution
for (let i = 0; i < 50; i++) {
  const concept = kg.getConcept('User Behavior');
  concept.update({ pattern: `evolved_${i}` });
  
  const drift = kg.detectDrift('User Behavior');
  if (drift.drift) {
    console.log('Drift detected at iteration', i);
  }
}
```

## Example: Memory Consolidation

```javascript
const { Memory } = require('./skills/knowledge-graph-memory');

const memory = new Memory();

// Store memories
memory.remember('important_fact', { value: 'critical data' }, { importance: 0.9 });
memory.remember('temporary_note', { value: 'temp data' }, { importance: 0.3 });

// Access important memory multiple times
for (let i = 0; i < 5; i++) {
  memory.recall('important_fact');
}

// Consolidate - promotes frequently accessed to long-term
const result = memory.consolidate();
console.log('Promoted:', result.promoted, 'Removed:', result.removed);
```
