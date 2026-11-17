# Integrate PIP in a product

Read this when implementing or updating a product that has chosen PIP. The
[UI README](https://github.com/WhiteKiwi/kiwi-design-system/blob/main/packages/ui/README.md)
and [token README](https://github.com/WhiteKiwi/kiwi-design-system/blob/main/packages/tokens/README.md)
own exact APIs and compatibility. Check their revision against installed packages.

## Establish the integration

Inspect the app's framework, dependencies, CSS entry point, theme handling, and
existing wrappers before editing. Use the app's package manager and lockfile.
React applications use `@whitekiwi/ui` with `@whitekiwi/tokens`; non-React
applications can use the token stylesheet alone. Keep the two PIP packages on
matching releases. Check the current peer ranges rather than assuming that an
older React app can consume the UI package.

Load styles once through the framework's global CSS entry, in this order:

```tsx
import "@whitekiwi/tokens/theme.css";
import "@whitekiwi/ui/styles.css";
import "./app.css";
```

Omit the UI stylesheet for a token-only app. Use public package exports, not
internal source paths. The current UI entry preserves `"use client"`; event
handlers and calls to its `cn` helper belong in a client module in RSC frameworks.
Read the package documentation before changing those boundaries.

## Preserve responsibilities

- Use semantic token roles and keep foreground/background pairs together.
- Choose light or dark with `data-theme` on the root element. System mode removes the attribute; `data-theme="auto"` does not enable it.
- The app owns theme persistence, fonts, resets, layout, routing, data, and form submission.
- Use the component's actual contract. For example, Button defaults to `type="button"`; form submission requires an explicit submit type. TextField connects labels and descriptions but does not validate input for the app.
- Intentional app theming and layout can stay local. When an internal-selector override or copied component is needed to repair a shared defect, propose an upstream fix rather than leaving an unexplained fork.

The installed version remains the implementation boundary. If the necessary API
exists only on `main`, identify it as unreleased. Use the contribution reference's
tarball workflow to test it; do not describe a source merge as a registry release.

## Return local improvements

Before closing the task, compare new local controls and styles with PIP exports.
Carry authorized shared improvements through the contribution workflow and link
the PIP PR from the consumer. If work remains, preserve a tracked next action and
removal condition; a design-document suggestion alone is not completion.
For non-React apps, inspect the native-pattern examples and CSS contract before
reimplementing shared visual states. Product data and theme persistence stay local.

## Adopt and verify

Review release notes and API/token changes, update matching dependencies and the
lockfile, and run the app's type checks, production build, and relevant tests.
Inspect affected pages in light/dark, narrow and desktop layouts, keyboard flow,
focus, errors, and reduced motion as relevant to the change. Remove tracked
workarounds after the published fix is verified. Do not commit machine-specific
tarball paths as the final app dependency.

If a review only asks for findings, report the gap and proposed change without
performing integration. If implementation or an upgrade was already requested,
continue within that scope without another approval loop.
