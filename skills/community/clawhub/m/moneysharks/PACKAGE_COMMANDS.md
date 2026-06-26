# Packaging Commands

## One-shot packaging script

From the skill folder:

```bash
./package_moneysharks.sh
```

This creates a `moneysharks.skill` archive in the parent directory of the skill folder.

## Direct zip command

From the parent directory containing `moneysharks-skill/`:

```bash
zip -r moneysharks.skill moneysharks-skill \
  -x "*/.DS_Store" \
  -x "*/__pycache__/*" \
  -x "*/.git/*" \
  -x "*/logs/*.log"
```

## Notes
- The archive keeps the `moneysharks-skill/` folder structure intact.
- Runtime log files are excluded.
- Example configs, references, scripts, and templates are included.
