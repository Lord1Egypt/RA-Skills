# Design Review

Use this checklist before sharing a final STL or 3MF.

## Visual review

- Does the overall shape match the request?
- Are all requested holes, cutouts, slots, and bosses present?
- Is there a stable print surface on the bed-facing side?
- Are there obvious overhangs above roughly 45 degrees?
- Do thin sections look printable for the chosen nozzle and material?
- Are fillets and chamfers on the intended edges?
- Does the part look proportionally correct next to the stated dimensions?

## Dimensional review

Check the CadQuery bounding box before export:

```python
bb = result.val().BoundingBox()
print(bb.xlen, bb.ylen, bb.zlen)
```

Verify:
- outer dimensions
- hole spacing
- internal clearance
- lip and wall thickness
- screw boss diameter and pilot size

## Mesh review

Run strict validation when possible:

```bash
python3 scripts/run_cadquery_model.py model.py --preview --strict
```

Warnings to pay attention to:
- non-watertight mesh
- zero or tiny volume
- missing STL output
- preview render failure

## Printability heuristics

- Standard structural FDM wall thickness: at least 1.2 mm
- Snap fits usually need extra clearance and generous root fillets
- Long cantilevers may need thicker sections or a different print orientation
- Outdoor or warm-environment parts usually want PETG or ASA instead of PLA
- Tall narrow parts may need a brim

## Delivery reminder

Include:
- final file path
- preview path if available
- critical dimensions
- orientation recommendation
- support requirement or no-support confirmation
- one short slicer recipe
