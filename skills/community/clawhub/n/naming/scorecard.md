# CLASH Scorecard

Use this to evaluate finalists before recommending a winner.

CLASH stands for:
- **Clarity**
- **Load**
- **Adjacency**
- **Search collision**
- **Harm**

Score each dimension from 1 to 5, then weight by lane.

## Dimensions

### Clarity
- 5: audience can infer the object or role quickly
- 3: understandable with light context
- 1: needs explanation or sounds misleading

### Load
- 5: easy to say, spell, remember, and transcribe
- 3: minor friction but manageable
- 1: repeated pronunciation or spelling errors likely

### Adjacency
- 5: fits the current product, taxonomy, or API family cleanly
- 3: workable but slightly off-pattern
- 1: breaks the system or creates naming debt

### Search collision
- 5: low ambiguity inside the intended namespace
- 3: some overlap but survivable with context
- 1: collides hard with existing concepts, packages, endpoints, or generic terms

### Harm
- 5: no obvious negative meaning, joke risk, or cultural friction
- 3: mild risk that needs contextual handling
- 1: invites confusion, bad connotations, or reputational problems

## Weighting By Lane

| Lane | Highest weights |
|------|-----------------|
| Product or brand | Clarity, Load, Harm |
| Feature or workflow | Clarity, Adjacency |
| API or schema | Clarity, Adjacency, Search collision |
| Package, repo, command, file | Clarity, Search collision |
| Rename | Adjacency, Search collision, Harm |

## Shortlist Table

```markdown
| Candidate | C | L | A | S | H | Notes |
|-----------|---|---|---|---|---|-------|
| [name]    | 4 | 5 | 3 | 4 | 5 | Clean but slightly narrow |
```

## Tie-Breakers

When scores are close:
1. Pick the name that reduces explanation debt
2. Pick the one that keeps the larger system more coherent
3. Pick the one that survives spoken conversation better
4. Pick the one with the safer migration path

## Do Not Fake Clearance

This scorecard is not legal clearance, trademark clearance, or guaranteed namespace availability.

If live verification matters, call it out explicitly in the recommendation:
- trademark search still needed
- package registry still needed
- repo or org namespace still needed
- domain or handle availability still needed
