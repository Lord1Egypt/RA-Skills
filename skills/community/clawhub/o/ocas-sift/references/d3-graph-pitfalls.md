# D3 Force Graph: Interaction & Layout Pitfalls

## simulation.on('end') Locking Viewport

**Problem:** Calling `d3.zoomIdentity.translate(tx, ty).scale(scale)` inside `simulation.on('end')` overwrites the user's current zoom/pan transform, locking the viewport and preventing pan/zoom/drag.

**Fix:** Do an initial fit ONCE using a `setTimeout` flag (`initialFitDoneRef`), and use `alphaTarget(0)` (not `0.005`) on drag end to fully release the simulation.

```ts
// WRONG: locks viewport after animation
simulation.on('end', () => {
  d3.select(canvas).transition().call(zoom.transform,
    d3.zoomIdentity.translate(tx, ty).scale(scale));
});

// CORRECT: one-time gentle fit
if (!initialFitDoneRef.current) {
  initialFitDoneRef.current = true;
  setTimeout(() => {
    d3.select(canvas).call(zoom.transform,
      d3.zoomIdentity.translate(tx, ty).scale(scale));
  }, 100);
}

// CORRECT: fully release simulation on drag end
.on('end', (event) => {
  if (!event.active) simulation.alphaTarget(0); // not 0.005
  if (event.subject) { event.subject.fx = null; event.subject.fy = null; }
})
```

## Resize Breaking Aspect Ratio

**Problem:** On window resize, the canvas drawing buffer gets stretched non-uniformly because the DPR-scaled buffer dimensions aren't updated, or the zoom transform is rescaled.

**Fix:** Only resize the drawing buffer and recenter the simulation force. NEVER touch the zoom transform on resize.

```ts
const handleResize = () => {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  dimRef.current = { w: rect.width, h: rect.height, dpr };
  simulationRef.current?.force('center', d3.forceCenter(rect.width/2, rect.height/2));
  simulationRef.current?.alpha(0.05).restart();
};
```

## Arbitrary Node Positions (No Grouping)

**Problem:** Pure force simulation with `forceCenter` produces a circular blob with no meaningful organization.

**Fix:** Add a custom force that pulls nodes toward group centers based on a shared attribute (company, location, role). Arrange group centers in a grid layout.

```ts
const computeGroupCenters = (nodes, mode, w, h) => {
  const groups = new Map();
  nodes.forEach(n => {
    const key = getGroupKey(n, mode);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(n);
  });
  const centers = new Map();
  const names = Array.from(groups.keys()).sort();
  const cols = Math.ceil(Math.sqrt(names.length));
  const rows = Math.ceil(names.length / cols);
  names.forEach((name, i) => {
    centers.set(name, {
      x: w / (cols + 1) * ((i % cols) + 1),
      y: h / (rows + 1) * (Math.floor(i / cols) + 1),
    });
  });
  return centers;
};
```

## Dynamic Color System (3-Cue Model)

When building design systems, derive ALL colors from 3 cue values via HSL luminance shifts. Change one hue variable → entire palette updates.

```css
:root {
  --hue-accent: 221;
  --sat-accent: 71%;
  --lit-accent: 53%;
  --color-primary: hsl(var(--hue-accent), var(--sat-accent), var(--lit-accente));
  --color-primary-hover: hsl(var(--hue-accent), var(--sat-accent), calc(var(--lit-accent) - 4%));
  --color-primary-soft: hsl(calc(var(--hue-accent) + 10), calc(var(--sat-accent) + 15%), 90%);
}
```
