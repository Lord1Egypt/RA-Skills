# Dust Collection Fittings Lib Spec

## Coordinate Convention
- Z-axis build.
- Inlet Z=0 (-Z extrude).
- Outlet Z=transitionLength (+Z).
- Branch +X (XZ plane).

## Completed
- Symmetrical Smooth Wye
- Reducing Elbow
- Straight/Offset Adapter
- Hard Wye (branch angle/pos/OD)

## Future
- **Cross (Double Wye)**: Mirror branches +X/-X. Explicit sketches (no array).
  - qCapEntity per spigot END.
- Brush Head: Bristles/ferrule.
- Dusty Mascot: Fittings robot.

## Branch Geo
```
var branchDir = vector(sinA, 0, cosA);
var origin = vector(mainR, 0, branchPos + mainR * cosA / sinA);
var plane = plane(origin, branchDir, cross(vector(0,1,0), branchDir));
```
Extrude UP_TO_BODY.

## Pitfalls
- No ternary lengths.
- qOwnedByBody(finalBody).
- cylinder(coordSystem(...), r).
