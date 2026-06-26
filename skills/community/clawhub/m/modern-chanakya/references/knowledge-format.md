# Modern Chanakya Knowledge Format

## Suggested record shape

For each principle or verse-derived idea, store:

- **title**
- **sourceType** (`classical` | `scholarly-summary` | `wiki-orientation` | `modern-commentary`)
- **sourceNote**
- **originalIdea**
- **historicalMeaning**
- **modernInterpretation**
- **example**
- **tags**
- **relatedIdeas**
- **confidence** (`high` | `medium` | `low`)

## Example

### Title
A system fails when the wrong layer owns the wrong responsibility.

### Source type
modern-commentary

### Original idea
Chanakya repeatedly emphasizes proper placement, role clarity, and disciplined structure.

### Historical meaning
Order and effectiveness depend on correct assignment of people and functions.

### Modern interpretation
UI should not own backend truth. Presentation and authority should stay in the correct layers.

### Example
If a frontend hardcodes business truth, the product becomes fragile and confused.

### Tags
- structure
- placement
- systems
- software-architecture

### Confidence
medium

## Growth rule

Prefer fewer high-quality principles over many weakly sourced fragments.
Merge duplicates and improve retrieval instead of letting the vault become noisy.
