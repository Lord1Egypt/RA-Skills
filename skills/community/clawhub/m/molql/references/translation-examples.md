# MolQL Translation Examples

This file provides comprehensive examples of natural language to MolQL translations for common molecular structure queries.

---

## Basic Selection Queries

### Chain Selection

**User**: "Select chain A"
```lisp
(sel.atom.chains (= atom.chain A))
```
**Explanation**: Selects all atoms in chain A.

**User**: "Show me chains A and B"
```lisp
(sel.atom.merge
  (sel.atom.chains (= atom.chain A))
  (sel.atom.chains (= atom.chain B)))
```
**Explanation**: Merges selections from chain A and chain B.

**User**: "Everything except chain A"
```lisp
(sel.atom.except-by
  (sel.atom.all)
  :by (sel.atom.chains (= atom.chain A)))
```
**Explanation**: Takes all atoms and excludes those in chain A.

### Residue Selection

**User**: "Select residue 10"
```lisp
(sel.atom.res (= atom.resno 10))
```
**Explanation**: Selects residue number 10.

**User**: "Show residues 10 to 20"
```lisp
(sel.atom.res (in-range atom.resno 10 20))
```
**Explanation**: Selects all residues with sequence numbers 10 through 20.

**User**: "Select all alanine residues"
```lisp
(sel.atom.res (= atom.resname ALA))
```
**Explanation**: Selects all residues named ALA (alanine).

**User**: "Show glycine and serine residues"
```lisp
(sel.atom.res (set.has {GLY SER} atom.resname))
```
**Explanation**: Selects residues whose name is either GLY or SER.

**User**: "Select residues from chain A, positions 50 to 100"
```lisp
(sel.atom.pick
  (sel.atom.chains (= atom.chain A))
  :test (in-range atom.resno 50 100))
```
**Explanation**: First selects chain A, then filters to residues 50-100.

### Atom Selection

**User**: "Select all carbon atoms"
```lisp
(sel.atom.atoms (= atom.el C))
```
**Explanation**: Selects all atoms with element carbon.

**User**: "Show CA atoms only"
```lisp
(sel.atom.atoms (= atom.name CA))
```
**Explanation**: Selects only alpha carbon atoms.

**User**: "Select backbone atoms"
```lisp
(sel.atom.atoms (set.has {CA C O N} atom.name))
```
**Explanation**: Selects atoms with names CA, C, O, or N.

**User**: "Show sidechain atoms"
```lisp
(sel.atom.atoms (not (set.has {CA C O N P} atom.name)))
```
**Explanation**: Selects all atoms except backbone atoms.

**User**: "Select all iron atoms"
```lisp
(sel.atom.atoms (= atom.el _Fe))
```
**Explanation**: Selects atoms with element Fe (note underscore prefix for elements).

---

## Distance-Based Queries

**User**: "Find atoms within 5 angstroms of the iron"
```lisp
(sel.atom.include-surroundings
  (sel.atom.atoms (= atom.el _Fe))
  :radius 5
  :as-whole-residues true)
```
**Explanation**: Selects iron atoms, then expands to include all atoms within 5Å, grouped by whole residues.

**User**: "Show residues near the ligand"
```lisp
(sel.atom.within
  (sel.atom.atom-groups :entity-test (= atom.entity-type polymer))
  :target (sel.atom.atom-groups :residue-test (= atom.entity-type non-polymer))
  :max-radius 5)
```
**Explanation**: Selects polymer residues that are within 5Å of non-polymer entities (ligands).

**User**: "What's within 8Å of the heme?"
```lisp
(sel.atom.include-surroundings
  (sel.atom.res (= atom.resname HEM))
  :radius 8
  :as-whole-residues true)
```
**Explanation**: Expands from HEM residues to include surroundings within 8Å.

**User**: "Select water molecules near the protein"
```lisp
(sel.atom.within
  (sel.atom.atom-groups :entity-test (= atom.entity-type water))
  :target (sel.atom.atom-groups :entity-test (= atom.entity-type polymer))
  :max-radius 4)
```
**Explanation**: Selects water molecules within 4Å of the protein.

---

## Property-Based Queries

### B-Factor Filtering

**User**: "Show residues with B-factor greater than 30"
```lisp
(sel.atom.pick
  (sel.atom.res (= atom.entity-type polymer))
  :test (> atom.bfactor 30))
```
**Explanation**: Filters polymer residues to those with B-factor above 30.

**User**: "Find highly flexible regions with B-factor above 50"
```lisp
(sel.atom.pick
  (sel.atom.res (= atom.entity-type polymer))
  :test (> atom.bfactor 50))
```
**Explanation**: Selects residues with high B-factors (>50), indicating high flexibility.

### Element and Type Filtering

**User**: "Select only water molecules"
```lisp
(sel.atom.atom-groups
  :entity-test (= atom.entity-type water))
```
**Explanation**: Selects all water molecules.

**User**: "Show the protein only"
```lisp
(sel.atom.atom-groups
  :entity-test (and
    (= atom.entity-type polymer)
    (regex.match (regex "(polypeptide|peptide)" "i")
      atom.entity-subtype)))
```
**Explanation**: Selects polymer entities that are polypeptides/peptides.

**User**: "Select ligands only"
```lisp
(sel.atom.atom-groups
  :entity-test (and
    (or
      (= atom.entity-type non-polymer)
      (!= atom.entity-prd-id ""))
    (not (regex.match (regex "(oligosaccharide|lipid|ion)" "i")
      atom.entity-subtype))))
```
**Explanation**: Selects non-polymer entities excluding sugars, lipids, and ions.

### Modified Residues

**User**: "Show modified residues"
```lisp
(sel.atom.res atom.is-modified)
```
**Explanation**: Selects all modified amino acid residues.

**User**: "Find phosphorylated residues"
```lisp
(sel.atom.res (and atom.is-modified (set.has {SEP TPO PTR} atom.resname)))
```
**Explanation**: Selects modified residues that are common phosphorylated forms.

---

## Secondary Structure Queries

**User**: "Select all helices"
```lisp
(sel.atom.atom-groups
  :residue-test (core.flags.has-any
    atom.key.sec-struct
    (secondary-structure-flags helix))
  :group-by atom.key.sec-struct)
```
**Explanation**: Selects residues with helical secondary structure.

**User**: "Show beta sheets"
```lisp
(sel.atom.atom-groups
  :residue-test (core.flags.has-any
    atom.key.sec-struct
    (secondary-structure-flags beta))
  :group-by atom.key.sec-struct)
```
**Explanation**: Selects residues forming beta sheets.

**User**: "Select helices in chain A"
```lisp
(sel.atom.pick
  (sel.atom.chains (= atom.chain A))
  :test (core.flags.has-any
    atom.key.sec-struct
    (secondary-structure-flags helix)))
```
**Explanation**: Selects helical residues within chain A.

---

## Complex Multi-Part Queries

**User**: "Select chain A and chain C, but only residues 10-50"
```lisp
(sel.atom.pick
  (sel.atom.merge
    (sel.atom.chains (= atom.chain A))
    (sel.atom.chains (= atom.chain C)))
  :test (in-range atom.resno 10 50))
```
**Explanation**: Merges chains A and C, then filters to residues 10-50.

**User**: "Show CA atoms in residues 100-150 of chain B"
```lisp
(sel.atom.pick
  (sel.atom.res (in-range atom.resno 100 150))
  :test (= atom.name CA))
```
**Explanation**: Selects residues 100-150, then filters to CA atoms only.

**User**: "Select the active site: residues within 6Å of the zinc ion that are also part of helices"
```lisp
(sel.atom.intersect
  (sel.atom.include-surroundings
    (sel.atom.atoms (= atom.el _Zn))
    :radius 6
    :as-whole-residues true)
  (sel.atom.atom-groups
    :residue-test (core.flags.has-any
      atom.key.sec-struct
      (secondary-structure-flags helix))))
```
**Explanation**: Intersects residues near zinc with helical residues.

**User**: "Show disulfide bonded cysteines"
```lisp
(sel.atom.pick
  (sel.atom.res (set.has {CYS} atom.resname))
  :test (sel.atom.is-connected-to
    (sel.atom.atom-groups
      :residue-test (set.has {CYS} atom.resname)
      :atom-test (set.has {SG} atom.label_atom_id))
    :target (sel.atom.atom-groups
      :residue-test (set.has {CYS} atom.resname)
      :atom-test (set.has {SG} atom.label_atom_id))
    :bond-test true))
```
**Explanation**: Selects CYS residues that are connected via their SG atoms (disulfide bonds).

---

## Ambiguous Query Clarifications

### Example 1: "Select the active site"

**Skill Response**:
"Active site can be defined in different ways. Could you clarify:
1. Should I select residues within a certain distance of a ligand or metal ion? If so, which one?
2. Do you have specific catalytic residue numbers in mind?
3. Should I base it on secondary structure elements?

For example, you could say: 'Select residues within 5Å of the zinc ion' or 'Select the catalytic triad residues 45, 78, and 102'."

### Example 2: "Show the binding pocket"

**Skill Response**:
"To select the binding pocket, I need more information:
1. Which ligand, cofactor, or metal defines the binding site? (e.g., heme, ATP, magnesium)
2. What radius should I use? (typically 5-8Å from the ligand)
3. Should I include whole residues or just atoms within the radius?

For example: 'Show residues within 6Å of the heme group, including whole residues'."

### Example 3: "Select the interface"

**Skill Response**:
"Interface between which chains or entities? For example:
- 'Select the interface between chain A and chain B'
- 'Show residues at the protein-ligand interface'
- 'Select the dimer interface'

A typical interface selection might be: 'Select residues in chain A within 5Å of chain B'."

---

## Quick Reference Card

| User Says | MolQL Pattern |
|-----------|---------------|
| "Select chain X" | `(sel.atom.chains (= atom.chain X))` |
| "Residues N to M" | `(sel.atom.res (in-range atom.resno N M))` |
| "ALA residues" | `(sel.atom.res (= atom.resname ALA))` |
| "CA atoms" | `(sel.atom.atoms (= atom.name CA))` |
| "Within N Å of X" | `(sel.atom.include-surroundings X :radius N :as-whole-residues true)` |
| "B-factor > N" | `(sel.atom.pick sel :test (> atom.bfactor N))` |
| "X and Y" | `(sel.atom.merge X Y)` |
| "X except Y" | `(sel.atom.except-by X :by Y)` |
| "X near Y" | `(sel.atom.within X :target Y :max-radius N)` |
