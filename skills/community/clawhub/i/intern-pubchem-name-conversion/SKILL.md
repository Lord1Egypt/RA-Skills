---
name: intern_pubchem_name_conversion
description: Convert molecules between IUPAC, SMILES, and molecular formula using PubChem as the source of truth. Use this whenever the user asks to convert, normalize, or cross-check molecular representations in chemistry/science workflows (including Intern research tasks). Prefer API lookup over memory; do not guess.
homepage: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
metadata: { "openclaw": { "emoji": "🧪", "requires": { "bins": ["curl", "python3"] } } }
---

# Intern PubChem Name Conversion

Convert one molecular representation into all three fields:
- `smiles`
- `iupac`
- `formula`

## When to use

Use this skill when the user asks to:
- convert IUPAC <-> SMILES
- fetch molecular formula from IUPAC/SMILES
- validate molecule identity against PubChem

Do not use this skill for:
- reaction mechanism explanation
- quantum chemistry simulation
- docking or property prediction beyond PubChem identifiers

## Input contract

Expect one input value and one type:
- `input_type`: `iupac` or `smiles`
- `input_value`: raw string

If the user gives only one string without type:
- treat strings with many bond symbols (`=`, `#`, `[`, `]`, `@`) as `smiles`
- otherwise treat as `iupac`/name query

## Required behavior

Always query PubChem first. Do not answer from memory when tools are available.

1) URL-encode the full input string:

```bash
ENCODED=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$INPUT_VALUE")
```

2) Build the primary endpoint:
- If `input_type == iupac`:
  - `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{ENCODED}/property/SMILES,IUPACName,MolecularFormula/JSON`
- If `input_type == smiles`:
  - `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{ENCODED}/property/SMILES,IUPACName,MolecularFormula/JSON`

3) If `smiles` primary endpoint is non-200, retry once with:
- `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity/smiles/{ENCODED}/property/SMILES,IUPACName,MolecularFormula/JSON`

4) If still non-200, do CID fallback:
- Resolve CID:
  - iupac: `.../compound/name/{ENCODED}/cids/JSON`
  - smiles: `.../compound/smiles/{ENCODED}/cids/JSON`
- Then fetch properties by CID:
  - `.../compound/cid/{CID}/property/SMILES,IUPACName,MolecularFormula/JSON`

5) Parse `PropertyTable.Properties[0]` and map:
- `smiles <- SMILES` (fallback `ConnectivitySMILES`)
- `iupac <- IUPACName`
- `formula <- MolecularFormula`

## Output format

Return JSON only (no markdown fences, no extra prose):

```json
{
  "smiles": "...",
  "iupac": "...",
  "formula": "..."
}
```

If all attempts fail, still return the same schema with empty strings:

```json
{
  "smiles": "",
  "iupac": "",
  "formula": ""
}
```

## Quality rules

- Keep PubChem values verbatim; do not rewrite or normalize names.
- If multiple records are returned, use the first record consistently.
- Do not silently swap stereochemistry markers.
