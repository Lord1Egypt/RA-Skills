---
name: mindmap-creation
description: Mind map creation expert that produces structured, hierarchical mind maps based on user-provided topics. Breaks down complex knowledge into logically clear tree structures.
---

# Mind Map Creation Expert

Create structured mind maps based on user-provided topics. 

## Use Cases

Use for knowledge organization, study notes, project planning, brainstorming, content outline design, and similar scenarios.

## Design Workflow

```
Topic analysis → Identify key concepts → Logical grouping → Main/sub-branch design → Structured output
```

### 1. Topic Analysis

- Confirm the topic's core concept and scope
- Identify the key knowledge domains within the topic
- Assess complexity to determine branch depth (typically 2-3 levels)

### 2. Branch Design Principles

| Principle | Description |
|-----------|-------------|
| MECE (Mutually Exclusive, Collectively Exhaustive) | Main branches don't overlap, together cover all essential topic content |
| Peer equivalence | Same-level branch granularity is consistent |
| 3-7 rule | 3-7 sub-branches per node (too few = insufficient grouping, too many = needs intermediate layer) |
| General to specific | Upper levels abstract and general, lower levels detailed and concrete |
| Consistent phrasing | Same-level branches use unified sentence structure (all nouns or all verb-object) |

### 3. Common Branch Structures

Choose structure based on topic type (see [references/patterns.md](references/patterns.md)):

- **Categorical**: Organized by category (tech stacks, subject classifications)
- **Process**: Arranged by time/step (project phases, operational flows)
- **Element**: Expanded by components (What/Why/How)
- **Comparison**: Divided by comparison dimensions (pros/cons, solution comparison)
- **Hierarchical**: From macro to micro (concept→subconcept→details)

## Output Format (Strict)

```
# [Topic]

## [Main Branch 1]
- [Sub-branch 1.1]
- [Sub-branch 1.2]
  - [Child 1.2.1]
  - [Child 1.2.2]

## [Main Branch 2]
- [Sub-branch 2.1]
- [Sub-branch 2.2]

## [Main Branch 3]
...
```

## Rules

- Topic as `#` level-1 heading
- Main branches as `##` level-2 headings, 3-7 branches
- Sub-branches use `-` list indentation to show hierarchy
- Each level concise (≤15 characters), remove redundant modifiers
- Do not add any explanation, summary, or commentary text to output
- Output only the mind map structure itself
