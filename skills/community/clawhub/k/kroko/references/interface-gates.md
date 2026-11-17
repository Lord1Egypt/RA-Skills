# Interface gates: the UI/UX half, measured

Code discipline produces no interface. These are the gates, and they are numbers,
which is why an agent can satisfy them and a reviewer can verify them.

## The measurable gates

| Gate | Target | Instrument |
|---|---|---|
| Largest Contentful Paint | <= 2.5 s at p75 | Lighthouse, web-vitals |
| Interaction to Next Paint | <= 200 ms at p75 | Lighthouse |
| Cumulative Layout Shift | <= 0.1 at p75 | Lighthouse |
| Contrast ratio | >= 4.5:1 body, >= 3:1 large text | axe-core |
| Keyboard | every action reachable, focus always visible | axe-core + manual |
| Screen reader | correct role, name, state, and order | ARIA APG audit |
| Touch target | >= 44x44 pt (iOS), >= 48x48 dp (Android) | manual |
| Frame budget | <= 16.7 ms at 60 Hz, <= 8.3 ms at 120 Hz | DevTools, Flutter DevTools |
| Text scaling | layout holds at 200% text size | manual |
| Reduced motion | honoured, no essential information in motion | manual |

The Core Web Vitals thresholds are the published ones: LCP *"should occur within
2.5 seconds"*, INP *"of 200 milliseconds or less"*, CLS *"of 0.1 or less"*, all
measured *"at the 75th percentile of page loads, segmented across mobile and desktop
devices."*

## The agent design rules

1. **Obtain tokens before drawing.** Spacing scale, type scale, palette, radii,
   elevation. An agent that hard-codes `padding: 13px` invents an inconsistent
   system one line at a time. Use a 4/8 pt grid and a modular type scale.
2. **Never hand-roll a platform primitive.** Native pickers, sheets, menus, share
   dialogs and gestures exist. Reimplementing them loses accessibility for free.
3. **One primary action per screen.** Two primaries means none.
4. **Hierarchy through weight and space, not colour.** Colour is the last resort and
   the first thing to break in dark mode, in bright sunlight, and for colour-blind
   users.
5. **Design every state.** Empty, loading, error, partial, offline, over-long
   content. Agents ship the happy path and a spinner; the other five are the product.
6. **Motion explains a state change or it does not exist.** No decorative motion on
   a loading path.
7. **Respect user settings.** Reduced motion, larger text, dark mode, high contrast.
8. **Semantic colours, never raw hex, in a component.** Pure black on pure white is
   a choice, and usually a wrong one; let the system adapt.
9. **Test with real content.** The longest plausible string, the empty collection,
   the missing image, the slow network.
10. **The platform pattern beats your new idea** for navigation, back gestures,
    permissions and settings. Users transfer expectations; do not spend them.

## Reference documents

- Apple Human Interface Guidelines, for platform conventions and hierarchy.
- Material Design 3, for Android and cross-platform tokens.
- WCAG 2.2 and the WAI-ARIA Authoring Practices, for the accessibility contract.
- web.dev Web Vitals, for the performance numbers and how to measure them.
- Flutter performance best practices, for frame budget and rebuild discipline.
