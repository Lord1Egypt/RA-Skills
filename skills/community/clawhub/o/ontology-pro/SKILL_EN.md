# ontology-pro — Cognitive Ontology Engine

> A cognitive engine with "knowledge modeling + reasoning + decision output" — the cognitive cortex plugin for AI Agents.

---

## Triggers

This skill is automatically loaded when user requests involve:

1. **Knowledge Modeling**: Extract entities, concepts, and relationships from text to build knowledge graphs
2. **Deep Analysis**: Causal reasoning, variable identification, path exploration, and cognitive inference
3. **Decision Support**: Generate executable strategies based on analysis (optimal paths + risks + action items)
4. **Continuous Learning**: Accumulate knowledge across sessions, incrementally update cognitive models
5. **Domain Ontology**: Build specialized knowledge systems for specific domains (healthcare, energy, AI, etc.)
6. **Explicit Trigger**: User mentions "ontology", "knowledge graph", "cognitive modeling", "reasoning", "ontology"

---

## Four Core Features

| Feature | Description |
|---------|-------------|
| 🧠 Cognitive Graph | Extract entity-concept-relation triples from input, build dynamic knowledge graphs |
| 🔁 Dynamic Memory | Persistently store knowledge graphs, accumulate across sessions, gets smarter over time |
| 🔍 Reasoning Engine | Multi-step reasoning: causal analysis → variable identification → path exploration, output reasoning chains |
| 🎯 Strategy Output | Map reasoning results to executable strategies: optimal path + risk points + action suggestions |

---

## Workflow

### Command Mapping

Users can trigger the following capabilities via natural language, AI routes automatically by intent:

| User Intent | Command | Reference Doc |
|-------------|---------|---------------|
| "Analyze this content", "Extract key concepts", "Build knowledge graph" | `analyze` | `references/cognitive-graph.md` |
| "Think deeply", "Analyze causality", "Evaluate paths" | `think` | `references/reasoning-engine.md` |
| "Give me strategy", "What should I do", "Strategic analysis" | `strategy` | `references/strategy-output.md` |
| "Remember this", "Show learned knowledge", "Update memory" | `memory` | `references/memory-protocol.md` |

### Complete Flow

```
Input → analyze (knowledge extraction) → graph (graph build/update) → think (reasoning) → strategy (decision output) → memory (persistence)
```

#### Step 1: ANALYZE — Cognitive Modeling

1. Receive user input (text, document, conversation)
2. Use protocols in `references/cognitive-graph.md` for triple extraction
3. Extraction results: entity list + relation list + triple set
4. Output format: structured JSON

#### Step 2: GRAPH — Graph Build/Update

1. If first analysis: create new graph
2. If historical graph exists (load via memory protocol): incremental update
3. Dedup merge: merge attributes for same entities, append new relations
4. Save to memory layer
5. Optional: use `scripts/graph_visualize.py` to generate Mermaid visualization

#### Step 3: THINK — Reasoning

1. Load current knowledge graph as context
2. Use reasoning templates in `references/reasoning-engine.md`
3. Execute multi-step reasoning:
   - Causal relationship identification
   - Key variable extraction
   - Potential path exploration
4. Output reasoning chain (traceable reasoning process)

#### Step 4: STRATEGY — Decision Output

1. Based on reasoning results, use templates in `references/strategy-output.md`
2. Generate executable strategies:
   - Optimal path (recommended solution)
   - Risk points (potential issues)
   - Action items (specific steps)
3. Strategy priority: P0 urgent / P1 important / P2 optional

#### Step 5: MEMORY — Persistence

1. Use protocols in `references/memory-protocol.md`
2. Save incremental knowledge from this analysis to persistent storage
3. Update graph version and changelog
4. Next session can load historical knowledge to continue reasoning

---

## Knowledge Graph Data Format

Graphs are stored in JSON format with core structure:

```json
{
  "version": "1.0.0",
  "domain": "general",
  "updated_at": "2026-03-30T16:00:00+08:00",
  "entities": [
    {
      "id": "e001",
      "name": "Energy Storage System",
      "type": "concept",
      "attributes": { "category": "Energy", "aliases": ["ESS", "Storage"] }
    }
  ],
  "relations": [
    {
      "source": "e001",
      "target": "e002",
      "type": "includes",
      "weight": 0.8,
      "evidence": "Energy storage system includes battery management system"
    }
  ],
  "metadata": {
    "total_entities": 42,
    "total_relations": 67,
    "sessions_analyzed": 8
  }
}
```

---

## Reference Documents

| File | Purpose |
|------|---------|
| `references/cognitive-graph.md` | Cognitive graph construction protocol: triple extraction rules, entity type classification, relation type definitions |
| `references/reasoning-engine.md` | Reasoning engine prompt templates: causal analysis, variable identification, path exploration, reasoning chain output |
| `references/strategy-output.md` | Decision output templates: strategy generation, risk assessment, action item formatting |
| `references/memory-protocol.md` | Persistent memory protocol: storage format, incremental updates, context injection, version management |

## Script Tools

| File | Purpose |
|------|---------|
| `scripts/graph_visualize.py` | JSON graph → Mermaid diagram generation (can be rendered as visual graphs) |
| `scripts/memory_manager.py` | Knowledge persistence management: create/load/update/query graphs, session history management |

---

## Usage Examples

### Example 1: Domain Knowledge Modeling

```
User: Help me organize the knowledge structure of the energy storage industry chain

AI: OK, I'll perform cognitive modeling on the energy storage industry chain.

[analyze] Extracting entities and relationships...
  Entities: Energy storage batteries, BMS, PCS, EMS, Li-ion batteries, flow batteries, compressed air storage...
  Relations: Storage System-contains-BMS, Storage System-contains-PCS, Li-ion-belongs to-Storage Battery...

[graph] Knowledge graph built, containing 23 entities and 34 relations.

[think] Reasoning based on the graph...
  Causal chain: Policy subsidies → Market demand ↑ → Capacity expansion → Price decline → Penetration rate ↑
  Key variables: Battery cost, policy intensity, tech iteration speed

[strategy] Decision recommendations:
  P0: Focus on LiFePO4 cost curve, already in downward trajectory
  P1: Flow batteries have structural opportunities in long-duration storage
  P2: Compressed air storage suitable for large-scale grid-side applications
```

### Example 2: Continuous Learning

```
User: Remember, Zhejiang's electricity spot market rules use a two-stage design: day-ahead + real-time

AI: [memory] Knowledge graph updated:
  + Entity: Zhejiang Electricity Spot Market
  + Relation: Zhejiang-uses-two-stage spot(day-ahead + real-time)
  + Attributes: market_type=spot, region=Zhejiang, phases=[day-ahead, real-time]

  Current graph: 45 entities, 72 relations, 10 analysis records
```

---

## Design Philosophy

1. **Reasoning > Retrieval**: Not just searching existing knowledge, but performing multi-step reasoning to discover hidden relationships
2. **Memory > Forgetting**: Persistently accumulate knowledge from each interaction, avoiding repetitive analysis
3. **Decision > Analysis**: Ultimate goal is to provide executable strategies, not stop at analysis level
4. **Lightweight > Heavyweight**: JSON storage + Mermaid visualization, no external database dependencies
5. **Transparent > Blackbox**: Complete traceable reasoning chains, every conclusion supported by evidence
