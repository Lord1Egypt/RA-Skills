# Motion And GSAP

Motion must teach. It should reveal structure, causality, transformation, attention, or time.

## Delegation To `gsap-motion`

If the user's `gsap-motion` skill is installed or available, use it after the narrative plan is defined.

This skill owns:

- Narrative architecture.
- Acts and scene list.
- Visual metaphors.
- Persistent objects.
- Presentation camera.
- Interaction model.
- Accessibility and reduced-motion requirements.
- Motion intent per scene.

Delegate to `gsap-motion` for:

- GSAP timelines.
- ScrollTrigger scenes.
- Flip transitions.
- SplitText or text choreography.
- SVG/canvas/WebGL animation coordination.
- Responsive animation behavior.
- Performance optimization.
- Reduced-motion variants.

## Motion Intent Vocabulary

Use precise motion verbs:

- `reveal`: expose hidden structure.
- `trace`: follow a path or causality chain.
- `compress`: summarize complexity.
- `expand`: unpack a concept.
- `morph`: preserve identity across representation changes.
- `compare`: synchronize alternatives.
- `focus`: direct attention.
- `interrupt`: show failure or discontinuity.
- `accumulate`: show scale or pressure.
- `resolve`: converge to a decision or model.

Avoid vague directives like "make it dynamic" or "add cool transitions."

## Timeline Pattern

Each scene should have:

```text
enter timeline
main beat timeline
interactive state timeline
exit timeline
reduced-motion equivalent
```

Transitions should preserve spatial and conceptual continuity whenever possible.

## Camera Pattern

The presentation camera can:

- Push in to inspect detail.
- Pull out to show system context.
- Pan across a process.
- Track an object through stages.
- Reframe around a newly important relationship.
- Snap only when a conceptual discontinuity is intentional.

Camera movement is part of explanation. It is not a background flourish.

## Scroll, Step, And Time

Choose the control model based on delivery:

- Step-based: best for live presentation with keyboard control.
- Scroll-based: best for self-guided scrollytelling.
- Hybrid: best when a speaker presents but the audience may later explore.
- Timeline autoplay: use sparingly, with pause and navigation controls.

## Reduced Motion

Reduced-motion mode should preserve meaning:

- Replace travel with staged visibility, simple opacity, or instant layout changes.
- Preserve sequence.
- Preserve labels and relationships.
- Avoid removing the explanation.

## Performance

Prefer transform and opacity for DOM motion. Use SVG for diagrams, canvas/WebGL for many particles or large simulations, and DOM for accessible labels and controls.

For many moving items:

- Avoid animating thousands of DOM nodes.
- Use canvas/WebGL or aggregate marks.
- Keep labels sparse and contextual.
- Profile before adding decorative complexity.

