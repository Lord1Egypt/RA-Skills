# IKEA Instruction Reader

## The Problem

Flat-pack furniture from IKEA, Wayfair, Amazon, and others ships with **wordless instruction manuals** — only numbered line drawings, no text. This creates universal pain points:

- **48% of people** admit to making at least one assembly error (IKEA customer survey)
- **Parts confusion:** Without labels, it's easy to use the wrong screw or insert a cam lock backwards
- **Step identification:** After a break, it's hard to tell which step you're on
- **No progress tracking:** There's no record of which parts you've used, leading to "did I already put this in?" moments
- **Common mistakes are undocumented:** The manual never says "don't do X" — only what TO do

The result: millions of wasted hours, broken furniture, and the universal experience of leftover hardware at the end.

## Who Needs This

- **Anyone buying flat-pack furniture** — IKEA alone sells to 4.5 billion customers yearly, and the average person assembles 3-5 flat-pack items per year
- **First-time furniture buyers** (college students, new apartment renters)
- **People with visual processing difficulties** who struggle with diagram-only instructions
- **Non-native speakers** in countries where IKEA manuals have no text to translate
- **Moving services** that assemble furniture for clients

## How It Works

### Assembly Tracker (`scripts/assembly_tracker.py`)
A parts and progress management system:

```bash
# Initialize a project from a manifest
python scripts/assembly_tracker.py init --name "KALLAX 4x4" --manifest manifests/kallax.json

# Check off parts used in a step
python scripts/assembly_tracker.py use --step 3 --parts "dowel:8,cam_lock:8,side_panel:2,top_panel:1"

# Get current status
python scripts/assembly_tracker.py status

# Verify no missing parts for remaining steps
python scripts/assembly_tracker.py verify
```

### Step Guide (`scripts/step_guide.py`)
Text guidance generator for common assembly step types:

```bash
# Get guidance for a step type
python scripts/step_guide.py --type cam_lock --panels 2

# Get full tool checklist
python scripts/step_guide.py --tools --project shelf
```

### Sample Output

```
$ python scripts/assembly_tracker.py status
╔══════════════════════════════════════════╗
║  KALLAX 4x4 — Assembly Progress         ║
╠══════════════════════════════════════════╣
║  Steps completed: 3 / 12 (25%)          ║
║  Parts used:     28 / 87  (32%)          ║
║                                          ║
║  ✓ Step 1: Frame assembly               ║
║  ✓ Step 2: Shelf insertion              ║
║  ✓ Step 3: Side panel connection        ║
║  → Step 4: Back panel attachment (NEXT)  ║
║    Step 5: Drawer slide install          ║
║    ...                                   ║
║                                          ║
║  ⚠ Missing for step 4: back_panel (0/1) ║
╚══════════════════════════════════════════╝
```

## Real-World Example

Alex is assembling a 6-drawer dresser alone. He's reached step 7 out of 14, has been at it for 2 hours, and isn't sure if he installed the drawer slides correctly. He uses the tracker to check his parts inventory:

```bash
$ python scripts/assembly_tracker.py status
Steps completed: 6 / 14 (43%)
Parts used: 42 / 95 (44%)

✓ Step 1-3: Frame assembled
✓ Step 4-5: Back panel and dividers installed
✓ Step 6: Drawer slide tracks (frame side) installed
→ Step 7: Drawer slide tracks (drawer side) (NEXT)
⚠ WARNING: You have 6 drawer slide tracks remaining but step 7
  needs 12 (6 drawers × 2 tracks). Did you install them on the
  wrong side in step 6?

Recommended: Check step 6 — frame-side tracks use the wide bracket,
drawer-side tracks use the narrow bracket.
```

The tracker catches the error before Alex proceeds further, saving him from having to disassemble later.

## License

MIT — see [LICENSE](LICENSE)
