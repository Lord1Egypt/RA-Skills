# Homarr styling and custom CSS

Use this reference for board appearance, custom CSS, Mantine selectors, and widget-specific styling.

## Prefer built-in board appearance

Use Homarr board settings before custom CSS when possible:

- background image URL, attachment, size, repeat;
- primary color;
- secondary color;
- opacity;
- icon color;
- item radius;
- layout columns and breakpoints.

Custom CSS is for focused changes, not redesigns or new features.

## Where custom CSS lives

Add custom CSS per board:

```text
Board settings -> Custom CSS
```

The CSS applies to that board page, not all Homarr boards globally.

## Scope to a widget

For one widget, add custom classes in Homarr:

```text
Edit mode -> widget three dots -> Edit item -> Advanced options -> Custom classes
```

Then scope CSS:

```css
.my-widget {
  border-radius: 16px !important;
}

.my-widget .mantine-Text-root {
  color: #f5f5f5;
}
```

Good selectors:

```css
.my-widget { ... }
.my-widget .mantine-Card-root { ... }
.my-widget .mantine-Text-root { ... }
```

Avoid generated Mantine classes with random suffixes:

```css
/* Bad: suffix changes after builds/updates */
.mantine-Card-x2fske { ... }
```

Avoid broad selectors unless intentionally changing the entire board:

```css
* { ... }
body { ... }
div { ... }
button { ... }
```

Use `!important` only when needed to override Mantine/Homarr styles.

## Mantine variables

Homarr uses Mantine. You can set Mantine CSS variables:

```css
:root {
  --mantine-primary-color-filled: #ffbb00;
}
```

Prefer small variable changes over broad DOM overrides when the goal is theme-level styling.

## Risks and limits

Custom CSS can:

- break after Homarr updates;
- make controls invisible or unclickable;
- harm accessibility/readability;
- conflict with responsive layouts and edit mode;
- hide UI without enforcing permissions.

CSS cannot:

- implement new widgets/features/integrations;
- securely hide elements from users;
- replace Homarr access control;
- safely revamp the whole UI.

`display: none` is not security.

## Styling workflow

1. Open the Homarr board.
2. Inspect with DevTools (`Ctrl+Shift+I` or right click -> Inspect).
3. Use element picker to find stable classes/structure.
4. Prototype CSS in DevTools.
5. Reload if experiments break the page.
6. Save minimal scoped CSS in board settings.
7. Verify desktop/mobile, light/dark theme, edit mode, and click/drag behavior.
8. Record fragile selectors or update-sensitive assumptions.
