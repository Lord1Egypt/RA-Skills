# Worked example: a full-time match film (9:16, 13.5 s)

A club posts this after every game. Three scenes, one progress bar across the whole film, and a new beat every second or two. Use it as the bar for every post film: the layer stack, the timings and the pattern of something drawn, something counting and something looping carry over to every format.

Brand: Harbour City FC (sample). Navy `#0E2240`, mint `#8FD6C4`, white `#F4F7F6`. Fonts: Anton (shout and numbers), Barlow Condensed 700 to 800 (names and meta).

Field shapes and motion keys are in `orshot_get_design_spec` topics `film` and `template-json`. The snippets below are excerpts of the real template, trimmed to the keys that matter.

## The timeline

| Film time | Scene | What lands |
|---|---|---|
| 0.0 | Slam (3.4 s) | FULL and TIME at full width settle from 1.2x with an 8 px blur (0.4 s, `expo.out`). Behind them, 8 rows of `FULL TIME` at 9% opacity drift left and right on a radial mint gradient. The progress bar starts filling. |
| 0.7 | | A navy band wipes across (clip, 0.45 s). |
| 0.95 | | `Harbour City win` reveals by word in the band (mask). |
| 1.6 | | `League Two · Matchday 14` wakes from above. |
| 2.4 | Cut | `zoomThrough` the word TIME (1.0 s). |
| 2.4 + 0.75 | Score (5.6 s) | Stadium aerial footage, graded navy, scaling 1.15 to 1.0. The pitch draws itself part by part (0.5 to 2.5 s). `3` and `1` slam in at 700 px and count up. |
| + 1.5 to 1.9 | | Team names reveal by word; a mint bar wipes under the winner. |
| + 2.3 to 3.9 | | The match timeline line wipes from KO to FT. Each goal dot pops (`back.out(2)`) as the line passes its minute, and its minute and scorer wake beside it: home goals above in mint, away goals below in white. |
| 7.0 | Cut | `push` up (1.0 s). |
| 7.0 + 0.15 | Card (6.5 s) | Player photo (grayscale, raised so the player sits above the type), navy multiply grade, scrim. The rail word wipes up the mint edge (1.05 s); kit stripes on the rail. |
| + 0.3 to 1.7 | | The crest draws stroke by stroke; club and matchday wake; the score block lands row by row from the left; a mint glow grows behind the 3. |
| + 2.4 | | `Player of the match · Okafor` chip pops as a group (`back.out(1.7)`). |
| + 2.6 on | | The crest's star turns and pulses on a loop until the end. |
| + 3.6 | | `Full time at Dockside Park` reveals by word. |
| + 4.6 | | A light sweep crosses the score block. |
| 13.5 | End | The bar is full; the last frame is the club's static full-time post. |

## The layers that make it look designed

**Chrome: the progress bar, a `layers` track over the whole film.** Two shapes (a track at 22% opacity and the fill). The fill opens with a clip inset from `right: 100` to `0`, `ease: "none"`; its colour switches from navy to white while the first cut plays, so it reads on both grounds. Clip values at the colour-switch keyframes are the film fraction at those times.

```json
{ "id": "chrome", "kind": "layers", "clips": [{ "id": "progress",
  "anchor": { "page": "slam", "edge": "start", "offset": 0 }, "until": { "edge": "filmEnd" },
  "elements": [{ "id": "progress_fill", "type": "shape", "shapeType": "rectangle",
    "position": { "x": 64, "y": 118 }, "dimensions": { "width": 952, "height": 8 },
    "style": { "fill": "#0E2240", "borderRadius": "4px" },
    "motion": { "keyframes": [
      { "at": 0,    "clip": { "top": 0, "right": 100,   "bottom": 0, "left": 0 }, "fill": "#0E2240" },
      { "at": 2.6,  "clip": { "top": 0, "right": 80.74, "bottom": 0, "left": 0 }, "fill": "#0E2240", "ease": "none" },
      { "at": 3.0,  "clip": { "top": 0, "right": 77.78, "bottom": 0, "left": 0 }, "fill": "#F4F7F6", "ease": "none" },
      { "at": 13.5, "clip": { "top": 0, "right": 0,     "bottom": 0, "left": 0 }, "fill": "#F4F7F6", "ease": "none" } ] } }] }] }
```

**Ground on a graphic scene: repeated type that drifts.** Each row is a 3300 px wide text layer at 9% opacity; even rows move `x` 0 to -520 over the scene, odd rows -520 to 0, `ease: "none"`. Under them a static SVG radial gradient from a lighter tint at the centre to a deeper one at the edges. The create checks flag these rows as off canvas and count their words as reading time; both warnings are wrong for a decorative ground.

**Slam: frame 0 already reads.** The word is opaque from the first frame and only settles:

```json
"motion": { "keyframes": [
  { "at": 0,    "scale": 1.2, "blur": 8, "opacity": 1 },
  { "at": 0.05, "scale": 1.2, "blur": 8, "opacity": 1, "ease": "none" },
  { "at": 0.4,  "scale": 1,   "blur": 0, "opacity": 1, "ease": "expo.out" } ] }
```

**Ground on a data scene: footage under a grade.** Horizontal stock footage cropped by `cover`, desaturated, under a brand-colour rectangle at 0.72 opacity, scaling down slowly so the ground is never still:

```json
{ "id": "aerial", "type": "video", "content": "stock://pixabay/video/208387",
  "position": { "x": 0, "y": 0 }, "dimensions": { "width": 1080, "height": 1920 },
  "style": { "objectFit": "cover", "filter": "grayscale(1) contrast(1.15)", "opacity": 0.55 },
  "videoOptions": { "loop": true, "muted": true },
  "parameterizable": true, "parameterId": "stadium_video", "parameterType": "videoUrl",
  "motion": { "keyframes": [{ "at": 0, "scale": 1.15 }, { "at": 5.6, "scale": 1.0, "ease": "none" }] } }
```

**The drawn subject: a pitch, part by part.** One SVG (`viewBox="0 0 1080 1920"`, mint strokes at 40% opacity) with `#outer`, `#half`, `#circle`, `#boxtop` and `#boxbot` groups, each with its own `drawIn` 0.2 to 0.4 s after the one before.

**A sequence that keeps building: the goal timeline.** A line wipes over `DUR` seconds from `A`. A goal at minute `m` sits at `x = L0 + LW * m / 90` and pops at `t = A + DUR * m / 90`, so each dot lands exactly as the line reaches it. Its minute (Anton 64 px) and scorer (Barlow Condensed 36 px) wake at `t` and `t + 0.1`.

**Photo placed for the layout.** The player sits low in the stock photo, and the score block sits low in the card. The image layer is 2800 px tall at `y: -900` so the player lands above the type; grayscale plus a navy multiply grade at 0.35 and a scrim that turns solid from 30% to 48% of the height.

**Static SVG for depth.** Kit stripes on the rail (a rotated `<pattern>` of navy bars at 8%), a radial mint glow behind the winning digit, and a diagonal light sweep (a white gradient band with `mixBlendMode: "screen"` moving `x` across in 1 s).

**A loop for the hold.** The crest's star sits in its own `<g id="startw">` and turns 72 degrees with a scale pulse, then repeats until the end:

```json
{ "selector": "#startw", "origin": "50% 50%", "repeat": -1, "repeatDelay": 1.2,
  "keyframes": [
    { "at": 2.6, "scale": 1,   "rotate": 0 },
    { "at": 3.0, "scale": 1.3, "rotate": 36, "ease": "power2.out" },
    { "at": 3.5, "scale": 1,   "rotate": 72, "ease": "power2.inOut" } ] }
```

## Fields

`result_line`, `matchday`, `home_team`, `away_team`, `home_score`, `away_score`, `stadium_video`, `photo`, `rail_word`, `club`, `potm`, `scorers`, `venue`, and per goal `gN_min` and `gN_name`. Keys carry their scene (`page2@home_score`, `page3@home_score`). A count layer counts to the score sent in its key.

The dots' positions and pop times are saved in the template, so a new minute per render changes the label, not where the dot sits. For a template reused every week, either space the goal slots evenly along the line (first goal, second goal, and so on, each label carrying its minute), or move each dot per render with its motion and position keys (Per-render motion control in https://orshot.com/docs/orshot-studio/motion.md). Make as many slots as the club's usual maximum.
