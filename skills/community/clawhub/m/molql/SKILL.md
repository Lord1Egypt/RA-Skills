---
name: molql
description: This skill should be used when users need to translate natural language molecular structure queries into MolQL (Mol-Script) expressions. It handles basic atom/residue/chain selection, distance-based queries, property-based filtering, complex multi-part queries, and provides clarification for ambiguous requests.
---

# MolQL Translator Skill

## Purpose

This skill translates natural language molecular structure queries into valid MolQL (Mol-Script) expressions. It enables users to describe what they want to select or visualize in natural language, and returns the corresponding MolQL expression that can be used with Mol* or compatible molecular viewers.

## When to Use

Trigger this skill when users:
- Ask to select specific chains, residues, or atoms in natural language (e.g., "select chain A", "show residues 10-20")
- Request distance-based selections (e.g., "find atoms within 5Å of the ligand")
- Want property-based filtering (e.g., "show residues with B-factor greater than 30")
- Need complex combinatory queries (e.g., "select helices in chain A that are connected to heme")
- Make ambiguous molecular selection requests that need clarification

**Do NOT use** for:
- General molecular biology questions unrelated to structure selection

## How to Use

### Translation Workflow

1. **Parse the user's natural language request** to identify:
   - Selection target (chain, residue, atom, element, entity type)
   - Constraints (ranges, properties, distances)
   - Operations (union, intersection, exclusion, expansion)

2. **Map to MolQL patterns** using the reference syntax in `references/molql-syntax.md`:
   - Basic selections → `(sel.atom.chains ...)`, `(sel.atom.res ...)`, `(sel.atom.atoms ...)`
   - Distance queries → `(sel.atom.within ...)`, `(sel.atom.include-surroundings ...)`
   - Property filters → `(sel.atom.pick :test ...)`
   - Complex queries → Combine with `(sel.atom.merge ...)`, `(sel.atom.intersect ...)`

3. **Construct the MolQL expression** following S-expression syntax:
   - Use space-separated arguments
   - Named parameters use `:` prefix
   - Nested expressions for complex logic

4. **Return output** in this format:
   ```
   **MolQL Expression:**
   ```lisp
   (your-molql-expression-here)
   ```

   **Explanation:**
   [Brief description of what the expression selects]
   ```

### Query Categories and Patterns

#### Basic Selection

| Natural Language | MolQL Pattern |
|-----------------|---------------|
| "Select chain A" | `(sel.atom.chains (= atom.chain A))` |
| "Show residues 10-20" | `(sel.atom.res (in-range atom.resno 10 20))` |
| "Select alanine residues" | `(sel.atom.res (= atom.resname ALA))` |
| "Show carbon atoms" | `(sel.atom.atoms (= atom.el C))` |
| "Select CA atoms" | `(sel.atom.atoms (= atom.name CA))` |

#### Distance-Based Queries

| Natural Language | MolQL Pattern |
|-----------------|---------------|
| "Atoms within 5Å of iron" | `(sel.atom.include-surroundings (sel.atom.atoms (= atom.el _Fe)) :radius 5 :as-whole-residues true)` |
| "Residues near the ligand" | `(sel.atom.within (sel.atom.atom-groups :residue-test (= atom.entity-type non-polymer)) :target (sel.atom.atom-groups :entity-test (= atom.entity-type polymer)) :max-radius 5)` |

#### Property-Based Filtering

| Natural Language | MolQL Pattern |
|-----------------|---------------|
| "Residues with B-factor > 30" | `(sel.atom.pick (sel.atom.res (= atom.entity-type polymer)) :test (> atom.bfactor 30))` |
| "Show modified residues" | `(sel.atom.res atom.is-modified)` |

#### Complex Queries

| Natural Language | MolQL Pattern |
|-----------------|---------------|
| "Chain A and chain B" | `(sel.atom.merge (sel.atom.chains (= atom.chain A)) (sel.atom.chains (= atom.chain B)))` |
| "Helices in chain A" | `(sel.atom.pick (sel.atom.chains (= atom.chain A)) :test (core.flags.has-any atom.key.sec-struct (secondary-structure-flags helix)))` |
| "Everything except chain A" | `(sel.atom.except-by (sel.atom.all) :by (sel.atom.chains (= atom.chain A)))` |

### Ambiguous Query Handling

When the user's request is ambiguous, ask clarifying questions:

**Ambiguous**: "Select the active site"
**Clarification**: "Active site can be defined in different ways. Do you want to:
1. Select residues within a certain distance of a ligand/metal ion?
2. Select residues based on known catalytic residues?
3. Select based on secondary structure elements?
Please specify which approach, or provide more details."

**Ambiguous**: "Show the binding pocket"
**Clarification**: "To select the binding pocket, I need to know:
1. Which ligand or cofactor defines the binding site?
2. What radius should I use (typically 5-8Å)?
3. Should I include whole residues or just atoms within the radius?"

### Bundled Resources

- **`references/molql-syntax.md`**: Complete MolQL syntax reference manual (1150 lines) covering all operators, selectors, atom properties, and examples. Load this reference when you need to look up specific syntax patterns or verify expression structure.

### Key MolQL Concepts

#### Selection Levels
- **Atoms**: Individual atoms - use `(sel.atom.atoms test)`
- **Residues**: Grouped by residue - use `(sel.atom.res test)`
- **Chains**: Grouped by chain - use `(sel.atom.chains test)`

#### Common Properties
- `atom.chain` - Chain ID (A, B, C...)
- `atom.resno` - Residue sequence number
- `atom.resname` - Residue name (ALA, GLY, etc.)
- `atom.name` - Atom name (CA, CB, N, C, O...)
- `atom.el` - Element symbol (C, N, O, Fe...)
- `atom.bfactor` - B-factor (temperature factor)
- `atom.entity-type` - Entity type (polymer, non-polymer, water)

#### Logical Operators
- `(= a b)` - Equal
- `(!= a b)` - Not equal
- `(< a b)`, `(> a b)` - Less/greater than
- `(in-range v min max)` - Range check
- `(and c1 c2)` - Logical AND
- `(or c1 c2)` - Logical OR
- `(not c)` - Logical NOT
- `(set.has {A B C} value)` - Set membership

#### Common Modifiers
- `(sel.atom.merge s1 s2 ...)` - Union of selections
- `(sel.atom.intersect s1 s2 ...)` - Intersection
- `(sel.atom.except-by s :by other)` - Exclusion
- `(sel.atom.include-surroundings s :radius 5)` - Expand by distance
- `(sel.atom.include-connected s :layer-count 2)` - Expand by connectivity

## Examples

### Example 1: Simple Chain Selection
**User**: "Select chain A"

**Response**:
```lisp
(sel.atom.chains (= atom.chain A))
```
**Explanation**: Selects all atoms in chain A, grouped by chain.

### Example 2: Residue Range
**User**: "Show me residues 130 to 180"

**Response**:
```lisp
(sel.atom.res (in-range atom.resno 130 180))
```
**Explanation**: Selects all residues with sequence numbers between 130 and 180 (inclusive), grouped by residue.

### Example 3: Distance Query
**User**: "Find residues within 5 angstroms of the iron atom"

**Response**:
```lisp
(sel.atom.include-surroundings
  (sel.atom.atoms (= atom.el _Fe))
  :radius 5
  :as-whole-residues true)
```
**Explanation**: First selects iron atoms, then expands the selection to include all residues with any atom within 5Å of the iron.

### Example 4: Property Filter
**User**: "Which residues have high B-factors, say above 50?"

**Response**:
```lisp
(sel.atom.pick
  (sel.atom.res (= atom.entity-type polymer))
  :test (> atom.bfactor 50))
```
**Explanation**: Selects polymer residues where the B-factor is greater than 50.

### Example 5: Complex Query
**User**: "Select all helices in chain A that are near the heme group"

**Response**:
```lisp
(sel.atom.within
  (sel.atom.pick
    (sel.atom.chains (= atom.chain A))
    :test (core.flags.has-any
      atom.key.sec-struct
      (secondary-structure-flags helix)))
  :target (sel.atom.res (= atom.resname HEM))
  :max-radius 5)
```
**Explanation**: First selects helical secondary structure elements in chain A, then filters to only those within 5Å of HEM residues.

## Troubleshooting

### Common Mistakes

1. **Wrong selector level**: Using `sel.atom.atoms` when you want residue-level selection. Remember:
   - Use `sel.atom.atoms` for individual atom selection
   - Use `sel.atom.res` for residue-level grouping
   - Use `sel.atom.chains` for chain-level grouping

2. **Missing named parameter colon**: Named parameters must have `:` prefix
   - ❌ `(sel.atom.include-surroundings sel radius 5)`
   - ✅ `(sel.atom.include-surroundings sel :radius 5)`

3. **Wrong element symbol format**: Element symbols in comparisons use underscore prefix
   - ❌ `(= atom.el Fe)`
   - ✅ `(= atom.el _Fe)`

4. **String vs symbol**: Chain IDs and residue names are symbols, not strings
   - ❌ `(= atom.chain "A")`
   - ✅ `(= atom.chain A)`

### When Translation Fails

If you cannot confidently translate a query:
1. Explain which part is ambiguous
2. Ask for clarification
3. Suggest possible interpretations
4. Provide MolQL for the most likely interpretation as a starting point
