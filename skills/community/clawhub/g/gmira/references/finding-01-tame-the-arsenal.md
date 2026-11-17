# Finding 01: registry components ship with the gallery demo's taste welded in

Date: 2026-07-25. Verified by build, not by reading. Screenshots in `proofs/finding-01/`.

## What happened

First install from the wired arsenal: `@componentry/dither-prism-hero`, used with a deliberate
palette (near-black `#0a0a0a`, deep green `#1f5f4a`, gold `#d6a419`) for a restrained dark hero.

What rendered was a rainbow smear with a blown-out white disc welded to the middle of the
viewport. Not the palette. Not close to the palette. See `01-defaults-slop.png`.

Zero console errors. The component "worked". The output was slop.

## Root cause

`dither-prism-hero.tsx` is a 9-layer fragment shader. The palette is applied once, at layer 2:

```glsl
col = mix(uColor1, uColor2, t1);
col = mix(col, uColor3, t2);
```

Then six further layers **add** to `col` without renormalizing, and only the final line clamps:

| Layer | Operation | Palette-aware? |
|---|---|---|
| 3 prismatic refraction | `col += prismColor * edgeMask * 0.4` | No. Rainbow from a hue sweep. |
| 4 iridescence | `col = mix(col, iris, irisMask)` | No. Rainbow. |
| 6 mouse ripple | `col += ripple * prismColor * 1.2` | No. |
| 6 mouse tint | `col += ripple * vec3(0.3, 0.2, 0.4)` | No. Hardcoded violet. |
| 6 mouse glow | `col += mouseGlow(..., vec3(1.0, 0.8, 1.0))` | No. Near-white. |
| 6 proximity boost | `col = mix(col, col * 1.5 + prismColor * 0.3, ...)` | Partly. |
| final | `col = clamp(col, 0.0, 1.0)` | Too late. |

The worst offender is the glow. Its own function:

```glsl
float core  = exp(-dist * 15.0) * 1.5;
float outer = exp(-dist *  5.0) * 0.8;
vec3  glow  = glowColor * (core + outer) * pulse * intensity;
```

At the glow's center that is `(1.5 + 0.8) * ~0.9 * intensity` added to RGB. With the shipped
intensity of `0.8` that is roughly **+1.84 added to every channel before clamp**: guaranteed
pure white, whatever the palette says.

And it is not even interactive. Both the position and the intensity are hardcoded, in the
initial uniforms **and re-set every single frame**:

```js
uniforms.uMouse.value.set(0.5, 0.5);      // never reads the pointer
uniforms.uMouseIntensity.value = 0.8;     // not exposed as a prop
```

So the component labels a feature "VISIBLE Mouse interaction" in its own source comments, never
wires it to a mouse, and the dead feature's fallback state destroys the one thing the component's
public API claims to control.

## The fix

Expose the welded constant, default it to off. Four-line patch, kept in-repo:

```diff
-  uMouseIntensity: { value: 0.8 },
+  uMouseIntensity: { value: mouseIntensity },   // prop, defaults to 0
```

Same component, same brief, same palette props, after the patch: `02-tamed.png`. Dark green
field, gold at the edges, visible dither grain, legible type, palette honored.

## The general law this proves

> **A registry component is an engine, not a design. Its defaults are tuned to win a five-second
> gallery GIF, and the gallery GIF is the new generic.**

Installing more impressive components does not make a site less generic. In 2026 the rainbow
WebGL blob occupies exactly the cultural position the purple CSS gradient did in 2021. The
arsenal raises the ceiling; it does nothing about the floor.

Three practices follow, and they belong in every build skill in the library:

1. **Install then tame, in the same breath.** The shadcn model copies source into your repo
   precisely so you can edit it. Editing it is not a workaround, it is the intended workflow.
   Treat an unedited registry component as an unfinished one.
2. **Audit for welded constants before use.** Grep the installed file for numeric literals
   assigned inside `useFrame`, `useMemo` uniform blocks, or render loops. Anything the props
   cannot reach is a decision the component author made for your client. The specific smell:
   a prop exists for a thing, and a hardcoded value elsewhere overrides it.
3. **Additive effect stacks cannot honor a dark palette.** Any shader that does `col += ...`
   more than twice without renormalizing will trend to white. If the brief needs restraint,
   either zero the additive coefficients or pick a different engine. Check by rendering the
   palette and comparing against the source hexes, not by trusting the prop names.

## Second-order note: the components also ship banned patterns

The same file's default headline class is:

```
text-transparent bg-clip-text bg-gradient-to-b from-zinc-900 via-zinc-500 to-zinc-800
```

Gradient text, which impeccable's craft floor bans outright (`skill-ban-gradient-text`, emphasis
comes from weight or size). The component's `children` slot is the escape hatch and the library
should always use it rather than the `title1` / `title2` props.

Conclusion: the arsenal is worth having, and every component in it needs a taming pass before it
touches a client surface. That pass is a skill.
