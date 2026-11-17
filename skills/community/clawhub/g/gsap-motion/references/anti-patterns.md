# Anti-Patterns

Avoid motion that adds risk without improving understanding or feel.

## Overusing GSAP

Do not use GSAP for every transition. CSS is better for many basic UI states because it stays declarative, cheap, and easy to maintain.

## Animating Everything

Animating every card, section, icon, and number makes the page feel noisy. Pick focal moments and keep routine content calm.

## Blocking Interaction

Do not make users wait for decorative sequences before they can read, scroll, click, or type.

## Hidden Content Dependence

Do not leave important content invisible until JavaScript runs. Initial CSS and markup should produce a usable page.

## Global Selectors

Avoid selectors like `.card` or `h1` in reusable components. Use refs, scopes, or data attributes so animations do not leak across the app.

## Missing Cleanup

Duplicated animations, broken scroll triggers, and memory leaks often come from missing cleanup after remounts or route changes.

## Unsafe Scroll Effects

Avoid scroll hijacking, excessive pinning, parallax everywhere, and scrubbed motion that makes content hard to read.

## Ignoring Reduced Motion

Reduced-motion support is required for serious frontend work. Large spatial motion, parallax, zoom, and spinning should be reduced or removed.

## Layout-Heavy Animation

Animating layout properties in repeated or scroll-linked contexts can cause jank. Use transforms, opacity, or Flip.

## Text Effects That Hurt Reading

Letter-by-letter, word-by-word, or masked text reveals can be memorable in a hero, but they are poor defaults for body content, forms, labels, or instructions.

## Debug Leftovers

Remove ScrollTrigger markers, console logging, experimental CSS, and temporary delays before delivery.
