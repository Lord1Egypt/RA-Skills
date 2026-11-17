# Mol-Script Expression Syntax Reference Manual

Mol-Script (also known as MolQL) is a declarative language for describing molecular structure selection and queries. This document details the **pure syntax** of mol-script expressions, without involving the Mol* library usage.

---

## Table of Contents

1. [Syntax Basics](#syntax-basics)
2. [Literals](#literals)
3. [Symbols](#symbols)
4. [Expression Structure](#expression-structure)
5. [Bracket Types](#bracket-types)
6. [Comments](#comments)
7. [Core Operators](#core-operators)
8. [Structure Selectors](#structure-selectors)
9. [Atom Properties](#atom-properties)
10. [Bond Properties](#bond-properties)
11. [Atom Set Operations](#atom-set-operations)
12. [Complete Examples](#complete-examples)
13. [Quick Reference](#quick-reference)

---

## Syntax Basics

### Expression Format

Mol-script uses **S-expression** (Lisp-style) syntax:

```lisp
(function-name arg1 arg2 ...)
```

### Basic Rules

- **Space-separated**: Arguments are separated by spaces or newlines
- **Named parameters**: Use `:` prefix, e.g., `:name value`
- **Nested expressions**: Expressions can serve as arguments to other expressions
- **Case-sensitive**: Symbol names are case-sensitive

---

## Literals

### Boolean Values

```lisp
true
false
```

### Numbers

```lisp
42          ; Integer
3.14        ; Float
-10         ; Negative number
1.5e-10     ; Scientific notation
```

### Strings

```lisp
ALA         ; String without spaces
`A B C`     ; String with spaces (using backtick)
```

### Lists

```lisp
[1 2 3]                    ; Number list
[A B C]                    ; Symbol list
[ALA GLY VAL]              ; Residue name list
```

### Sets

```lisp
{CA CB CG}                 ; Atom name set
{C N O S}                  ; Element set
```

---

## Symbols

### Ordinary Symbols

```lisp
atom.resno                 ; Atom property
sel.atom.all              ; Selector
in-range                  ; Operator
```

### Shorthand Symbols

```lisp
.CA        ; Atom name: equivalent to (atom-name CA)
._C        ; Element symbol: equivalent to (element-symbol C)
```

### Named Parameters

```lisp
:radius 5.0               ; Named parameter
:test condition           ; Test condition
:target selection         ; Target selection
```

---

## Expression Structure

### Basic Expression

```lisp
(operator arg1 arg2 ...)
```

### Positional Parameters

```lisp
(+ 1 2)                    ; Addition
(= atom.resno 10)          ; Equality check
(in-range atom.resno 10 100)  ; Range check
```

### Named Parameters

```lisp
(sel.atom.atom-groups
  :chain-test (= atom.chain A)
  :residue-test (= atom.resname ALA))
```

### Mixed Parameters

```lisp
(func positional1 positional2
  :named1 value1
  :named2 value2)
```

---

## Bracket Types

### Parentheses `()` - Function Call

```lisp
(= atom.resno 10)          ; Function call/expression
```

### Square Brackets `[]` - List Construction

```lisp
[list 1 2 3]               ; Create list
```

### Curly Braces `{}` - Set Construction

```lisp
{set CA CB CG}             ; Create set
```

---

## Comments

```lisp
; Single-line comment (to end of line)
(sel.atom.all)  ; Inline comment

; Select all atoms
(sel.atom.all)
```

---

## Core Operators

### Logical Operators

```lisp
; Not
(not condition)

; And
(and condition1 condition2 ...)

; Or
(or condition1 condition2 ...)
```

### Relational Operators

```lisp
; Equal
(= value1 value2)

; Not equal
(!= value1 value2)

; Less than
(< a b)

; Less than or equal
(<= a b)

; Greater than
(> a b)

; Greater than or equal
(>= a b)

; Range check (min <= value <= max)
(in-range value min max)
```

### Mathematical Operators

```lisp
; Basic operations
(+ a b)                    ; Addition
(- a b)                    ; Subtraction
(* a b)                    ; Multiplication
(/ a b)                    ; Division
(** a b)                   ; Power
(mod a b)                  ; Modulo

; Aggregation
(min values...)            ; Minimum
(max values...)            ; Maximum

; Mathematical functions
(floor x)                  ; Floor
(ceil x)                   ; Ceiling
(round x)                  ; Round
(trunc x)                  ; Truncate
(abs x)                    ; Absolute value
(sign x)                   ; Sign function
(sqrt x)                   ; Square root
(cbrt x)                   ; Cube root

; Trigonometric functions
(sin x) (cos x) (tan x)
(asin x) (acos x) (atan x)
(sinh x) (cosh x) (tanh x)

; Exponential and logarithmic
(exp x) (log x) (log10 x)
(atan2 y x)
```

### String Operators

```lisp
; Concatenation
(concat str1 str2 ...)

; Regex matching
(regex.match regex string)
```

### Set Operators

```lisp
; Check if element is in set
(set.has set element)

; Check subset
(set.subset set1 set2)

; Get list element
(list.get list index)
```

### Type Conversion

```lisp
(bool value)               ; Convert to boolean
(num value)                ; Convert to number
(str value)                ; Convert to string
```

### Type Construction

```lisp
; List
(list item1 item2 ...)

; Set
(set item1 item2 ...)

; Regular expression
(regex pattern)
(regex pattern flags)      ; flags: i(case-insensitive), g(global), etc.

; Bit flags
(bitflags number)
```

---

## Structure Selectors

### Generators

Generators create sequences of atom sets.

#### Select All Atoms

```lisp
(sel.atom.all)
```

#### Atom Group Selection

```lisp
(sel.atom.atom-groups
  :entity-test test        ; Entity test (optional)
  :chain-test test         ; Chain test (optional)
  :residue-test test       ; Residue test (optional)
  :atom-test test          ; Atom test (optional)
  :group-by property)      ; Grouping property (optional)
```

**Example: Select Chain A**

```lisp
(sel.atom.atom-groups
  :chain-test (= atom.chain A))
```

**Example: Select ALA Residues**

```lisp
(sel.atom.atom-groups
  :residue-test (= atom.resname ALA))
```

**Example: Select Grouped by Residue**

```lisp
(sel.atom.atom-groups
  :residue-test (= atom.resname ALA)
  :group-by atom.key.res)
```

#### Simplified Atom Selection

```lisp
; Select atoms matching condition (each atom independently)
(sel.atom.atoms test)

; Select residues matching condition (grouped by residue)
(sel.atom.res test)

; Select chains matching condition (grouped by chain)
(sel.atom.chains test)
```

**Example:**

```lisp
(sel.atom.atoms (= atom.el C))           ; Select carbon atoms
(sel.atom.res (= atom.resno 10))         ; Select residue 10
(sel.atom.chains (= atom.chain A))       ; Select chain A
```

#### Bonded Atom Pairs

```lisp
(sel.atom.bonded-pairs
  :test bond-test)        ; Bond test (default: covalent)
```

#### Ring Selection

```lisp
(sel.atom.rings
  :fingerprint (ringfp _C _N _C _C)   ; Ring fingerprint (optional)
  :only-aromatic true)                ; Aromatic rings only (optional)
```

#### Empty Selection

```lisp
(sel.atom.empty)
```

### Modifiers

Modifiers modify and extend existing selections.

#### Union

```lisp
(sel.atom.union selection1 selection2 ...)
```

#### Include Surroundings

```lisp
(sel.atom.include-surroundings selection
  :radius distance               ; Radius (Angstrom)
  :atom-radius value             ; Atom radius increment (optional)
  :as-whole-residues true/false) ; Whether to include whole residues
```

#### Include Connected

```lisp
(sel.atom.include-connected selection
  :bond-test test                ; Bond type test (optional)
  :layer-count n                 ; Connection layers (optional, default 1)
  :fixed-point true/false        ; Continue adding until no new connections (optional)
  :as-whole-residues true/false) ; Whole residues (optional)
```

#### Cluster

```lisp
(sel.atom.cluster selection
  :min-distance min              ; Minimum distance
  :max-distance max              ; Maximum distance
  :min-size n                    ; Minimum merge size (optional, default 2)
  :max-size n)                   ; Maximum merge size (optional)
```

#### Except

```lisp
(sel.atom.except-by selection
  :by other-selection)
```

#### Intersect

```lisp
(sel.atom.intersect-by selection
  :by other-selection)
```

#### Union Extension

```lisp
(sel.atom.union-by selection
  :by other-selection)
```

#### Surrounding Ligands

```lisp
(sel.atom.surrounding-ligands selection
  :radius distance
  :include-water true/false)
```

#### Whole Residue Expansion

```lisp
(sel.atom.expand-property selection
  :property property)
```

### Filters

Filters select atom sets based on conditions.

#### Conditional Filter

```lisp
(sel.atom.pick selection
  :test condition)
```

#### Distance Filter

```lisp
(sel.atom.within selection
  :target target-selection
  :min-radius min              ; Minimum radius (optional, default 0)
  :max-radius max              ; Maximum radius
  :atom-radius value           ; Atom radius increment (optional)
  :invert true/false)          ; Whether to invert (optional)
```

#### Connectivity Filter

```lisp
(sel.atom.is-connected-to selection
  :target target-selection
  :bond-test test              ; Bond test (optional)
  :disjunct true/false         ; Whether must have external connection (optional)
  :invert true/false)          ; Whether to invert (optional)
```

#### First Element

```lisp
(sel.atom.first selection)
```

#### Same Property Filter

```lisp
(sel.atom.with-same-atom-properties selection
  :source source-selection
  :property property)
```

#### Intersected Filter

```lisp
(sel.atom.intersected-by selection
  :by other-selection)
```

### Combinators

#### Merge

```lisp
(sel.atom.merge selection1 selection2 ...)
```

#### Intersect

```lisp
(sel.atom.intersect selection1 selection2 ...)
```

#### Distance Clustering

```lisp
(sel.atom.dist-cluster
  :matrix [[0 5] [2 0]]        ; Distance matrix
  :selections [sel1 sel2])     ; Selection list
```

---

## Atom Properties

### Core Properties

```lisp
atom.el                      ; Element symbol (C, N, O, ...)
atom.vdw                     ; Van der Waals radius
atom.mass                    ; Atomic mass
atom.atomic-number           ; Atomic number

atom.x                       ; X coordinate
atom.y                       ; Y coordinate
atom.z                       ; Z coordinate

atom.key                     ; Atom unique key
atom.bond-count              ; Bond count
atom.src-index               ; Source file index

atom.op-name                 ; Symmetry operation name
atom.instance-id             ; Symmetry operation instance ID
atom.op-key                  ; Symmetry operation key

atom.model-index             ; Model index
atom.model-label             ; Model label
atom.model-entry-id          ; Model entry ID (e.g., PDB ID)
```

### Macromolecule Properties (Auth Naming - PDB Original)

```lisp
atom.name                    ; Atom name (auth_atom_id)
atom.resname                 ; Residue name (auth_comp_id)
atom.chain                   ; Chain ID (auth_asym_id)
atom.resno                   ; Residue sequence number (auth_seq_id)
atom.inscode                 ; Insertion code (pdbx_PDB_ins_code)
```

### Macromolecule Properties (Label Naming - mmCIF Standard)

```lisp
atom.label_atom_id           ; Atom ID
atom.label_comp_id           ; Residue name
atom.label_asym_id           ; Chain ID
atom.label_entity_id         ; Entity ID
atom.label_seq_id            ; Sequence ID
atom.label_alt_id            ; Alternate location ID
```

### Grouping Keys

```lisp
atom.key.res                 ; Residue unique key
atom.key.chain               ; Chain unique key
atom.key.entity              ; Entity unique key
atom.key.molecule            ; Connected component key
atom.key.sec-struct          ; Secondary structure key
```

### Entity Properties

```lisp
atom.entity-type             ; Entity type (polymer/non-polymer/water/branched)
atom.entity-subtype          ; Entity subtype
atom.entity-prd-id           ; PRD ID
atom.entity-description      ; Entity description
```

### Chemical Properties

```lisp
atom.is-het                  ; Whether HETATM
atom.is-modified             ; Whether modified residue
atom.modified-parent         ; Modified parent name
atom.chem-comp-type          ; Chemical component type
atom.object-primitive        ; Object primitive type
```

### Physical Properties

```lisp
atom.occupancy               ; Occupancy
atom.bfactor                 ; B factor
atom.pdbx_formal_charge      ; Formal charge
```

### Secondary Structure

```lisp
atom.secondaryStructureFlags ; Secondary structure flags
```

### IHM Specific Properties

```lisp
atom.ihm.has-seq-id          ; Whether has sequence ID
atom.ihm.overlaps-seq-id-range  ; Whether overlaps with sequence ID range
```

---

## Bond Properties

```lisp
bond.flags                   ; Bond flags
bond.order                   ; Bond order
bond.length                  ; Bond length
bond.key                     ; Bond unique identifier
bond.atom-a                  ; Bond atom A
bond.atom-b                  ; Bond atom B
```

### Bond Type Judgment

```lisp
(bond.is flag1 flag2 ...)
```

**Allowed Bond Flags:**

```lisp
covalent                     ; Covalent bond
metallic                     ; Metallic bond
ion                          ; Ionic bond
hydrogen                     ; Hydrogen bond
sulfide                      ; Sulfide bond
computed                     ; Computed bond
aromatic                     ; Aromatic bond
```

**Example:**

```lisp
(bond.is metallic covalent)  ; Metallic or covalent bond
```

---

## Atom Set Operations

### Atom Count

```lisp
(atom.set.atom-count)
```

### Query Count

```lisp
(atom.set.count-query query)
```

### Reduce Operation

```lisp
(atom.set.reduce
  :initial initial-value
  :value value-expression)
```

**Usage Example:**

```lisp
(atom.set.reduce
  :initial 9999
  :value atom.set.reduce.value)  ; Current reduce value
```

### Property Set

```lisp
(atom.set.property property)
```

**Example:**

```lisp
(atom.set.property atom.label_atom_id)  ; Get all atom names
```

---

## Type Constructors

### Element Symbol

```lisp
(element-symbol C)           ; Single element
(element-symbol C N O)       ; Multiple elements
```

### Atom Name

```lisp
(atom-name CA)
(atom-name CA CB CG)
```

### Residue ID

```lisp
; Auth naming
(auth-resid chain seq_id)
(auth-resid chain seq_id ins_code)

; Label naming
(label-resid entity_id asym_id seq_id)
(label-resid entity_id asym_id seq_id ins_code)
```

**Example:**

```lisp
(auth-resid A 10)            ; Chain A residue 10
(auth-resid A 10 i)          ; Chain A residue 10, insertion code i
```

### Entity Type

```lisp
(ent-type polymer)           ; Polymer
(ent-type non-polymer)       ; Non-polymer
(ent-type water)             ; Water
(ent-type branched)          ; Branched
```

### Bond Flags

```lisp
(bond-flags covalent metallic)
```

### Secondary Structure Flags

```lisp
(secondary-structure-flags helix)
(secondary-structure-flags alpha beta)
```

**Allowed Flags:**

```lisp
alpha, beta, 3-10, pi, sheet, strand, helix, turn, none
```

### Ring Fingerprint

```lisp
(ringfp _C _N _C _C _C)      ; Five-membered ring fingerprint
```

---

## Complete Examples

### Select All Atoms

```lisp
(sel.atom.all)
```

### Select Specific Chain

```lisp
(sel.atom.chains (= atom.chain A))
```

### Select Residue Range

```lisp
(sel.atom.res (in-range atom.resno 130 180))
```

### Select Specific Residue Name

```lisp
(sel.atom.res (= atom.resname ALA))
```

### Select Specific Element

```lisp
(sel.atom.atoms (= atom.el _Fe))
```

### Select Cα Atoms

```lisp
(sel.atom.atoms (= atom.name CA))
```

### Select Protein

```lisp
(sel.atom.atom-groups
  :entity-test (and
    (= atom.entity-type polymer)
    (regex.match (regex "(polypeptide|cyclic-pseudo-peptide|peptide-like)" "i")
      atom.entity-subtype)))
```

### Select Backbone Atoms

```lisp
(sel.atom.atom-groups
  :entity-test (= atom.entity-type polymer)
  :atom-test (set.has {CA C O N P} atom.label_atom_id))
```

### Select Side Chain Atoms

```lisp
(sel.atom.atom-groups
  :entity-test (= atom.entity-type polymer)
  :atom-test (not (set.has {CA C O N} atom.label_atom_id)))
```

### Select Helices

```lisp
(sel.atom.atom-groups
  :residue-test (core.flags.has-any
    atom.key.sec-struct
    (secondary-structure-flags helix))
  :group-by atom.key.sec-struct)
```

### Select β-Sheets

```lisp
(sel.atom.atom-groups
  :residue-test (core.flags.has-any
    atom.key.sec-struct
    (secondary-structure-flags beta))
  :group-by atom.key.sec-struct)
```

### Select Water Molecules

```lisp
(sel.atom.atom-groups
  :entity-test (= atom.entity-type water))
```

### Select Ligands

```lisp
(sel.atom.atom-groups
  :entity-test (and
    (or
      (= atom.entity-type non-polymer)
      (!= atom.entity-prd-id ""))
    (not (regex.match (regex "(oligosaccharide|lipid|ion)" "i")
      atom.entity-subtype))))
```

### Select Surrounding Residues

```lisp
(sel.atom.include-surroundings
  (sel.atom.atoms (= atom.el _Fe))
  :radius 5
  :as-whole-residues true)
```

### Select Connected Residues

```lisp
(sel.atom.include-connected
  (sel.atom.res (= atom.resname HEM))
  :layer-count 2
  :bond-test (bond.is metallic covalent)
  :as-whole-residues true)
```

### Select Disulfide Bridge Residues

```lisp
(sel.atom.pick
  (sel.atom.res
    (set.has {CYS} atom.resname))
  :test (sel.atom.is-connected-to
    (sel.atom.atom-groups
      :residue-test (set.has {CYS} atom.resname)
      :atom-test (set.has {SG} atom.label_atom_id))
    :target (sel.atom.atom-groups
      :residue-test (set.has {CYS} atom.resname)
      :atom-test (set.has {SG} atom.label_atom_id))
    :bond-test true))
```

### Select Residues Within 5Å of Ligand

```lisp
(sel.atom.within
  (sel.atom.atom-groups
    :residue-test (= atom.entity-type non-polymer))
  :target (sel.atom.atom-groups
    :entity-test (= atom.entity-type polymer))
  :max-radius 5
  :as-whole-residues true)
```

### Cluster LYS Residues

```lisp
(sel.atom.cluster
  (sel.atom.res (= atom.resname LYS))
  :max-distance 5)
```

### Select All Rings

```lisp
(sel.atom.rings)
```

### Select Aromatic Rings

```lisp
(sel.atom.rings
  :only-aromatic true)
```

### Select Rings with Specific Fingerprint

```lisp
(sel.atom.rings
  :fingerprint (ringfp _C _N _C _C))
```

### Select Modified Residues

```lisp
(sel.atom.res atom.is-modified)
```

### Select Metal Coordination Atoms

```lisp
(sel.atom.atoms
  (> (atom.bond-count
       :flags (bond-flags metallic))
     0))
```

### Distance Clustering

```lisp
(sel.atom.dist-cluster
  :matrix [[0 5] [2 0]]
  :selections [
    (sel.atom.res (= atom.resname LYS))
    (sel.atom.res (= atom.resname ALA))])
```

### Select Residues with B-Factor < 30

```lisp
(sel.atom.pick
  (sel.atom.res
    (= atom.entity-type polymer))
  :test (< atom.bfactor 30))
```

### Select Chain A and Chain B

```lisp
(sel.atom.merge
  (sel.atom.chains (= atom.chain A))
  (sel.atom.chains (= atom.chain B)))
```

### Select Residues 10-100 in Chain A

```lisp
(sel.atom.pick
  (sel.atom.chains (= atom.chain A))
  :test (in-range atom.resno 10 100))
```

### Complement of Selection

```lisp
(sel.atom.except-by
  (sel.atom.all)
  :by (sel.atom.chains (= atom.chain A)))
```

### Select Residues Connected to Current Selection

```lisp
(sel.atom.include-connected
  (sel.atom.current)  ; or other selection
  :layer-count 1
  :as-whole-residues true)
```

---

## Quick Reference

### Common Aliases

| Symbol | Meaning |
|--------|---------|
| `atom.el` | Element symbol |
| `atom.name` | Atom name (auth) |
| `atom.resname` | Residue name (auth) |
| `atom.chain` | Chain ID (auth) |
| `atom.resno` | Residue sequence number (auth) |
| `atom.bfactor` | B factor |
| `atom.key.res` | Residue key |
| `atom.key.chain` | Chain key |

### Common Operators

| Operator | Syntax | Example |
|----------|--------|---------|
| Equal | `(= a b)` | `(= atom.resno 10)` |
| Not Equal | `(!= a b)` | `(!= atom.el C)` |
| Range | `(in-range v min max)` | `(in-range atom.resno 10 100)` |
| Set Contains | `(set.has set val)` | `(set.has {ALA GLY} atom.resname)` |
| Logical And | `(and c1 c2)` | `(and (> x 0) (< x 10))` |
| Logical Or | `(or c1 c2)` | `(or (= el C) (= el N))` |
| Logical Not | `(not c)` | `(not (= el H))` |

### Selector Patterns

```lisp
; Select by chain
(sel.atom.chains (= atom.chain A))

; Select by residue
(sel.atom.res (= atom.resname ALA))

; Select by residue range
(sel.atom.res (in-range atom.resno 10 100))

; Select by atom
(sel.atom.atoms (= atom.name CA))

; Select by element
(sel.atom.atoms (= atom.el C))
```

### Modifier Patterns

```lisp
; Expand surroundings
(sel.atom.include-surroundings sel :radius 5 :as-whole-residues true)

; Expand connections
(sel.atom.include-connected sel :layer-count 2 :as-whole-residues true)

; Except
(sel.atom.except-by sel :by other)

; Merge
(sel.atom.merge sel1 sel2 ...)

; Cluster
(sel.atom.cluster sel :max-distance 5)
```

### Filter Patterns

```lisp
; Conditional filter
(sel.atom.pick sel :test condition)

; Distance filter
(sel.atom.within sel :target other :max-radius 5)

; Connectivity filter
(sel.atom.is-connected-to sel :target other)
```

---

## Syntax Summary

### Expression Hierarchy

```
Expression
├── Literal (true/false, number, string)
├── Symbol (atom.resno, sel.atom.all, =, ...)
└── Apply (function call)
    └── (head arg1 arg2 :name value ...)
```

### Parameter Types

- **Positional parameters**: Passed in order
- **Named parameters**: In `:name value` form
- **Optional parameters**: Parameters with default values

### Evaluation Rules

- Literals evaluate to themselves
- Symbols look up corresponding values/functions
- Apply expressions call functions with arguments

---

This document covers the complete syntax rules of mol-script expressions. All examples can be used directly with the mol-script parser.
