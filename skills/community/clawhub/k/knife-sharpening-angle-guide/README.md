# Knife Sharpening Angle Guide

**Stop sharpening every knife at the angle your uncle taught you.**

A 15° edge on a German chef's knife folds on the first squash; 25° on a
gyuto turns a laser into a wedge. Sharpening fails for three specific
reasons — wrong angle for the class, skipped grits, and never raising a
burr — and all three are fixable with lookup tables and trigonometry, not
talent.

## What It Does

`scripts/edge_guide.py`:

```bash
python3 scripts/edge_guide.py --knife german-chefs --condition very-dull
python3 scripts/edge_guide.py --drawer            # every knife in the drawer
python3 scripts/edge_guide.py --heights --blade-mm 45   # hand-angle height table
python3 scripts/edge_guide.py --stones-owned 1000 6000  # gap analysis
python3 scripts/edge_guide.py --steel vg10 --burr
```

- **Angle-per-class table**: Japanese 12–15°, German 20°, boning 18–22°,
  cleaver 25°+, pocket 20–25°, with asymmetric 70/30 pass-count warnings
  for Japanese blades.
- **Grit ladder from your edge's actual state**: chipped → 220-400 start;
  very dull → 400-800; refresh → 1000. Max 3× jumps enforced.
- **Pass-height math**: spine height = blade width × sin(angle) with
  finger-width references, plus the Sharpie calibration trick.
- **Burr protocol narration**: the step sequence most people skip, which is
  why their knives look sharp and cut nothing.
- **Steel decoder**: X50CrMoV15 vs VG-10 vs SG2 vs carbon — what to expect
  at the stone so you don't misread steel behavior as bad technique.
- **Stone-gap analysis**: which single stone to buy next given what you own.

## Who Needs This

- Home cooks with a mixed drawer (German + Japanese + beater) and one
  stubborn habit
- New whetstone owners intimidated by angle-holding
- EDC/pocket-knife people chasing edge stability over razor bragging
- Anyone restoring thrift-store or inherited knives

## Example

A 45 mm German chef's knife, very dull: `--knife german-chefs
--condition very-dull` → 20°/side, ladder 400-800 → 1000 → 3000 (6000
optional), spine height 15.4 mm (two thumb widths). The same session on a
70/30 santoku warns you to count 3:2 passes per side or you'll center the
bevel and change how the knife steers.

## License

MIT — see LICENSE.
