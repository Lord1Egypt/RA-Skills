# Motion Design

Motion should feel like part of the product's interaction language, not a layer added at the end.

## Purposes

Use motion to support:

- Orientation: where something came from or where it went.
- Feedback: whether an action worked.
- Hierarchy: what matters most now.
- Continuity: how layout or route changes relate.
- Personality: a small amount of brand character.
- Storytelling: guided reveals when the page is built around a narrative.

## Hierarchy

Important elements can move first, move less, or settle with more visual weight. Secondary items can follow with shorter, subtler animation.

For ranked or social UI:

- Give top-ranked items slightly stronger presence.
- Use rank numbers as motion anchors.
- Let reordering show continuity rather than snapping.
- Keep repeated cards scannable.

## Timing

Typical product UI ranges:

- Press/tap feedback: `0.08s` to `0.18s`.
- Hover/focus feedback: `0.12s` to `0.25s`.
- Small entrances: `0.25s` to `0.45s`.
- Section reveals: `0.35s` to `0.7s`.
- Layout transitions: `0.25s` to `0.6s`.

Use longer durations only for deliberate hero or storytelling moments.

## Stagger

Stagger can reveal structure, but too much stagger delays the interface.

Use:

- `0.03s` to `0.06s` for dense cards.
- `0.06s` to `0.1s` for sparse hero elements.
- Small groups instead of whole-page cascades.

## Personality

Choose motion personality from the product domain:

- Utility apps: quiet and efficient.
- Social/lifestyle apps: expressive but still quick.
- Games: playful and more animated.
- Editorial/story pages: cinematic when content supports it.

Do not copy the visual language of reference products; translate the intent into a distinct system.

## Motion Tokens

For larger projects, define shared values:

```ts
export const motion = {
  duration: {
    fast: 0.16,
    base: 0.32,
    slow: 0.56,
  },
  ease: {
    standard: "power2.out",
    emphasized: "power3.out",
    inOut: "power2.inOut",
  },
};
```

Use tokens to keep motion consistent, not to force every interaction into the same pattern.
