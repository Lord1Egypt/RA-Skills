# Writing a job type

A job type is one JavaScript file, `<jobType>.js`, saved beside the project file. `build.py` inlines
it after `kit.js` and `layout.js`, so it runs in the browser as a plain script: no imports, no
modules, no Node APIs. It must define one global, `const JOB`.

Start by copying `assets/views/deck.js`. It is the unit-safe pattern and it is short.
`assets/views/sunroom.js` shows existing-plus-new work, a sloped roof and a side elevation.

Contents: [the contract](#the-contract) · [coordinates and units](#coordinates-and-units) ·
[View](#view-the-2d-drawing-api) · [styles](#line-and-fill-styles) · [Iso](#iso-the-picture) ·
[open items in a drawing](#open-items-in-a-drawing) · [fitting the boxes](#fitting-the-boxes) ·
[checklist](#checklist)

## The contract

```js
const JOB = {
  type: 'deck',
  derive(P) { ... return G; },              // geometry worked out once: member positions, levels
  picture(P, G, o) { ... return iso; },     // an Iso for the main picture. o = { den, id }
  labels(P, G, iso) { ... },                // optional: iso.label(...) calls for the field-sheet picture
  stepPicture(P, G, step, k) { ... return svgString; },   // optional: small picture for step k (step.pic names it)
  field: {
    pictureNote: 'Decking shown cut away',  // optional small caption
    pictureDen: 60, coverDen: 48,           // optional: number or (P, G) => number
    planHeight: 10,                         // optional: inches of the middle column given to the plan
    plan:    { title: 'Framing plan', den: 24, draw: viewPlan },
    section: { title: 'Section', den: 16, draw: viewSection },
    side:    { title: 'Front elevation', den: 48, draw: viewElevation, note: '...' },   // optional
    details: [ { title: 'Post base and footing', den: 4, draw: detailBase, note: (P, G) => 'Typical of ' + G.posts.length }, ... ],
  },
};
```

Each `draw` is `(P, G, den) => svgString`: make `new View(den, 'uniqueId')`, draw, `return v.svg()`.
Use the `den` you are handed, not a hard-coded one, so `scales` in the project file works.
`P` is the project file; `P.geometry` holds the numbers. Keep every job number in the project file
and every drawing decision in the view.

View numbers are assigned by the layout: plan 1, section 2, side 3 if present, then details.
Read them from the global `REF`: `REF.plan`, `REF.section`, `REF.side`, `REF.d1`, `REF.d2`..., and
`REF.sheet` (the field sheet number). Write cross-references as `` `SEE ${REF.d1}/${REF.sheet}` ``.

The field sheet has fixed boxes: picture 8.6 in wide (left), plan and section 14.4 in wide (middle),
steps (right), and a row of details 5.8 in tall across the bottom, split evenly. Two or three details
fit well; four is tight.

## Coordinates and units

- Model units are the project's (`P.geometry.units`): inches or millimetres. y is up.
- Draw at real size. A 16 ft deck is 192 units wide in inches. Scale is applied by the View.
- `den` is the scale ratio: 24 means 1:24 (½" = 1'-0").
- Sizes you type in the view (an offset for a dimension line, a break line, a plate thickness)
  should go through `const I = v => v * UPI;` so the view also works in millimetres.
- Write dimensions with `FMT(length, approx)`: feet-inches or millimetres to suit. `approx` adds ±.
- Text and line weights are in sheet points and print the same size at every scale. `v.pt(n)` gives
  n points in model units when you need a gap that should not scale.

## View: the 2D drawing API

```js
const v = new View(den, 'plan');           // id must be unique in the set
v.line(x1, y1, x2, y2, cls)
v.rect(x0, y0, x1, y1, cls, { fill })      // fill: v.pat('conc') | v.pat('wall') | a colour
v.poly([[x, y], ...], cls, close = true)
v.circle(x, y, r, cls)
v.arc(cx, cy, r, a0, a1, cls)              // degrees, counter-clockwise
v.lumber(x0, y0, x1, y1, cls)              // a member cut in section: rectangle with an X
v.text(s, x, y, { cls, anchor: 'start'|'middle'|'end', rot, size })   // '\n' makes lines
v.arrow(tipX, tipY, fromX, fromY)
v.dimH(x1, x2, y, yo, { text, approx })    // dimension line at y; extension lines start at yo
v.dimV(y1, y2, x, xo, { text, approx })
v.note(s, tx, ty, ex, ey, { side: 'r'|'l', kind })   // leader from target (tx,ty) to elbow (ex,ey); text runs to `side`
v.datum(s, x, y, toX)                      // level symbol with a line to toX and a two-line label
v.bubble(x, y, num, sheet)                 // section or detail reference bubble
return v.svg();
```

`note` kinds: none = ink (existing or neutral), `'N'` = blue (new work), `'R'` = red with a warning
triangle (the engineer still owes this). Notes are UPPER CASE, two or three short lines. `wrap(s, n)`
breaks a long string at about n characters.

The drawing's extents are measured from what you draw, then every view is fitted to its real bounding
box in the browser, so you never set a canvas size. Anything you draw makes the view bigger.

## Line and fill styles

| Class | Use |
|---|---|
| `new` | New member: blue outline, light blue fill |
| `newF` | Light blue fill only (pair with an open `poly(..., 'new', false)` for a member cut by a break line) |
| `newS` | New member cut in plan: solid blue (posts, columns) |
| `newH` | New work hidden below: dashed blue (beams under joists, footings in plan) |
| `ex` | Existing member: grey outline, light grey fill |
| `exh` | Existing, hidden below: dashed grey |
| `exw` | Existing wall or slab outline; give it `{ fill: v.pat('wall') }` or `v.pat('conc')` |
| `exb` | Existing beyond, faint (the house behind an elevation) |
| `steel` | Connector or plate, solid dark. `steelo` = outlined |
| `o` / `o2` | Ink line, medium / thin (grade, break lines, door swings) |
| `anch` / `anchOk` | Anchor or fastener centreline: red dashed while open / blue dashed once answered |
| `cutl` / `cutl2` | Section cut line / its heavy end marks |
| `dm`, `ld` | Dimension and leader lines (used by dimH, dimV, note) |

Text classes: `t` normal, `ts` small, `tb` bold, `tN` blue bold, `tR` red bold, `td` dimension grey.
Colours for the picture come from `PAL` (`PAL.newSolid`, `PAL.existSolid`, `PAL.slab`, `PAL.wall`,
`PAL.steel`, `PAL.shore`, `PAL.check`); `shade(hex, f)` lightens (f > 0) or darkens.

Colour is meaning: blue is new, grey is existing, red is the engineer's, orange is a hold or temporary
work. Do not use colour for decoration.

## Iso: the picture

```js
const iso = new Iso(den, id);
iso.solid(x0, x1, y0, y1, zBottom, zTop, colour, { order, stroke, op })   // a box; zBottom / zTop may be functions of y for a slope
iso.quad([[x, y, z], ...4], colour, { order })                             // a flat face (glass, a panel)
iso.line3([x, y, z], [x, y, z], cls)    iso.poly3([[x, y, z], ...], cls)
iso.label(s, [x, y, z], ex, ey, { side, kind })
return iso;                             // picture() returns the Iso; stepPicture() returns iso.svg()
```

x runs to the lower right, y to the lower left, z is up; the viewer looks from +x, +y, +z. So put
the side people should see at large x and large y, and the house or back wall at y = 0.
`order` is the paint layer (ground 0, then up); within a layer, far things paint first.

The picture is not to scale. Give `pictureDen` and `coverDen` so it roughly fills its box (8.3 in wide on the
field sheet, 7.2 in on the cover): the scene is about `(length + depth + 4 × ground margin) × 0.866` wide, so
`den = that width in inches / 8.3`. If it is still too big the layout shrinks it to fit, and the audit
complains only when the labels would get small.

Screen position of a 3D point is `[(y - x) * 0.866, (x + y) / 2 - z]`. Label elbows `(ex, ey)` are in
those screen units. Compute them from the geometry (see `labels` in deck.js), and place labels above
and below the object rather than beside it, so the picture can use the full width of its box.

Step pictures: draw the same scene with a mode per group, so each step shows what is built in that
step in blue, what was built earlier in grey, and nothing else. Give each a unique id (`'st' + k`).

## Open items in a drawing

```js
const anc = answer(P, 'anchor');                       // '' while the item is open
v.line(0, 2, 0, -4, anc ? 'anchOk' : 'anch');
v.note(anc ? 'ANCHOR TO (E) CONCRETE:\n' + wrap(anc.toUpperCase(), 36)
           : 'ANCHOR TO (E) CONCRETE:\nTYPE, SIZE, EMBEDMENT, EDGE DISTANCE',
       0, -2, 5, 3, { kind: anc ? 'N' : 'R' });
```

Every engineering value that is not in the project file gets this treatment: a red note that says
exactly what is owed, which turns into the engineer's own words once answered. Draw the thing
schematically (a footing of nominal size, a generic connector) and never label it with a size the
user did not give.

## Fitting the boxes

Run `print.py`. The audit names each view that is too wide or tall for its box, by how much.
In order of preference: wrap or shorten notes; move note elbows closer; put notes on the side with
room; shorten a member stub in a detail (use a break line); change `planHeight`; lower the scale
(`den` up one step). Keep the plan the largest view.

Then look at the preview PNGs for what the audit cannot see: overlapping notes, a leader crossing a
dimension, text on top of linework, a label pointing at nothing.

## Job-specific drawing code

Keep job-specific drawing code beside the project file, and keep it small:

- A job keeps its own drawing file only for what is particular to that job.
- When the same change is needed on a second job, it moves into the kit view (`assets/views/`), with a
  project-file option if it is not always wanted, and both jobs drop their copy of it.
- A job-local file starts with a short comment listing what it changes from the kit view, so the next
  person can see what is a candidate to move.

Otherwise every job carries its own copy of a view, the copies drift apart and the kit never improves.

## Checklist

- [ ] `const JOB` defined; every `draw` uses the `den` argument and a unique View id.
- [ ] No job number typed in the view that belongs in `P.geometry`.
- [ ] Every size in the view goes through `I()`, every printed dimension through `FMT()`.
- [ ] New work blue, existing grey; hidden members dashed.
- [ ] Each engineering unknown is a red note tied to an open item with `answer(P, key)`.
- [ ] Notes cross-reference details with `REF`, and each detail is referenced from the plan or section.
- [ ] `print.py` audit is clean and the previews were looked at.
