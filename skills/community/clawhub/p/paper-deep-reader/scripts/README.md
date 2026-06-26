# Scripts

These scripts make the skill less prompt-only and more protocol-driven.

## Intended workflow

1. `scaffold_note.py`
   - create an Obsidian-compatible note from the base template
2. `build_paper_map.py`
   - extract a compact paper map
3. route the paper manually using `routing-rules.md`
   - choose one primary adapter
   - choose one to three evidence packs
   - add an optional secondary adapter only if independently load-bearing
4. `build_notation_table.py`
   - draft a notation table from equations and definitions
5. `build_claim_matrix.py`
   - draft a claim-evidence matrix
6. `build_limitation_ledger.py`
   - split paper-acknowledged limitations from likely reader-inferred caveats
7. `render_final_note.py`
   - inject the generated artifacts back into the final note scaffold

## Example

```bash
python scaffold_note.py \
  --title "Example Paper" \
  --authors "A. Author; B. Author" \
  --year 2026 \
  --venue "arXiv" \
  --url "https://arxiv.org/abs/xxxx.xxxxx" \
  --output example-note.md

python build_paper_map.py paper.md --output artifacts/paper-map.md

# route manually using paper-taxonomy.md + routing-rules.md
# then continue with artifact drafting

python build_notation_table.py paper.md --output artifacts/notation-table.md
python build_claim_matrix.py paper.md --output artifacts/claim-matrix.md
python build_limitation_ledger.py paper.md --output artifacts/limitation-ledger.md

python render_final_note.py \
  --input example-note.md \
  --paper-map-md artifacts/paper-map.md \
  --notation-table-md artifacts/notation-table.md \
  --claim-matrix-md artifacts/claim-matrix.md \
  --output example-note-filled.md
```

## Notes

- Routing is currently a deliberate reading step, not a separate script.
- All scripts are heuristic by design.
- They are intended to produce a strong first draft for the agent, not a final scholarly judgment.
- They use only the Python standard library.
