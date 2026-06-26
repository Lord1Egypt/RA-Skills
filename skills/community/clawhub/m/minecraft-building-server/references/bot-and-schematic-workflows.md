# Bot, Schematic, and Assisted Building Workflows

## 1. Main Approaches

| Approach | Best use | Notes |
|----------|----------|-------|
| FAWE + schematic | Fast deployment of static builds | Lowest operational complexity |
| Mineflayer bot | Parametric / scripted building | More flexible, more setup cost |
| Litematica | Precise client-guided building | Useful where server-side editing is limited |

## 2. FAWE + Schematic Route

Best for:
- repeatable structure deployment
- modular scenes
- reusable build workflows with reusable assets

Typical flow:
1. build prototype
2. export schematic
3. transfer to target environment
4. paste and align
5. blend and finalize

## 3. Mineflayer Route

Best for:
- scripted placement
- integration with external planning/data
- experimental AI-driven build systems

Typical concerns:
- navigation/pathfinding
- chunk loading
- placement order
- material supply
- rate limiting
- recovery from failure

## 4. Litematica Route

Best for:
- precision manual reproduction
- survival-compatible workflows
- teams that want visual guidance rather than full automation

Important note:
- printer-style automation may violate public server rules; always require explicit authorization

## 5. Large Project Management

For team-scale building:
1. clarify requirements
2. prototype key sections
3. divide work by zone or specialty
4. standardize palette/style
5. assemble and review
6. deliver schematic/world/render bundle

## 6. Boundary Note

This reference focuses on construction methods and build execution workflows, not server infrastructure operations.
