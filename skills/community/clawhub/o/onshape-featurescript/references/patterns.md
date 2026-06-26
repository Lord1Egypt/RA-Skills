# Proven FS Patterns & Pitfalls

## Enum/Cond
if/else blocks for params.

## Shell Caps
qFacesParallelToDirection(qOwnedByBody(finalBody, FACE), vector(0,1,0))

## Union
Primary body first in qUnion.

## Label Wrap
skText flat → opWrap cylinder → opThicken 0.5mm.

## Fonts
AllertaStencil-Regular.ttf (stencil OD).

## Common Fixes
| Pitfall | Fix |
|---------|-----|
| Ternary ValueWithUnits | if/else |
| Shell entities fail | qOwnedByBody |
| cylinder args | coordSystem + r |
| Multi-instance | qOwnedByBody not qEverything |
