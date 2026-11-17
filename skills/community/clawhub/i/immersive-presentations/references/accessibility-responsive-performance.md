# Accessibility, Responsive Design, And Performance

An immersive presentation must remain legible, controllable, and understandable.

## Accessibility

Required by default:

- Keyboard navigation for all controls.
- Visible focus states.
- Semantic buttons and labels.
- Sufficient color contrast.
- Text alternatives or prose summaries for essential visual diagrams.
- Reduced-motion support.
- No essential information conveyed by color alone.
- Avoid rapid flashing, excessive strobing, or motion that can trigger discomfort.

For complex visuals, provide an accessible explanation near the scene or in a companion notes panel.

## Reduced Motion Behavior

Reduced motion is not "no content." It should:

- Preserve scene sequence.
- Preserve comparison and causality.
- Use immediate transforms, simple fades, or stepped states.
- Disable camera sweeps, parallax, and continuous looping effects.

## Responsive Design

Design for narrative integrity across screen sizes:

- Desktop can use wide spatial relationships.
- Mobile should reframe scenes, not just stack them.
- Keep labels attached to objects.
- Keep controls reachable.
- Avoid tiny diagrams and dense annotations.
- Use stable aspect ratios for diagrams, canvases, and stage areas.
- Test landscape and portrait when the experience is presentation-critical.

## Presenter Display Constraints

Assume projectors, low contrast rooms, and imperfect network conditions:

- Use large readable type.
- Keep key labels concise.
- Avoid hairline strokes for critical diagrams.
- Avoid essential details near screen edges.
- Provide a way to start from a known scene.

## Performance Bar

The experience should feel deliberate and responsive:

- Avoid layout thrashing.
- Animate transforms and opacity where possible.
- Use requestAnimationFrame or GSAP timelines responsibly.
- Keep background effects subordinate to foreground explanation.
- Lazy-load heavy media when possible.
- Provide fallbacks for missing assets.

## QA Checklist

Before final delivery:

- Navigate through every scene forward and backward.
- Test keyboard controls.
- Test reduced-motion mode.
- Test mobile width.
- Check that text does not overlap or spill out.
- Check that animations complete and reset cleanly.
- Verify that visual metaphors remain understandable without presenter narration when self-guided mode is required.

