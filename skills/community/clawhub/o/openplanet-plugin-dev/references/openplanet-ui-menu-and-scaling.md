# Openplanet UI: Menu Hook & UI Scaling Patterns

## RenderMenu hook scope (PITFALL)
Openplanet only wires a **global** `void RenderMenu()` into the menu bar. If defined
inside a `class { }`, it is silently never called → the menu item never appears.
- OK global scope: `void RenderMenu() { ... }` at file top level.
- OK namespace scope: `namespace Foo { void RenderMenu() { ... } }` — still global, still hooked.
- BAD class scope: `class X { void RenderMenu() { ... } }` — NOT hooked.

When a window is drawn by a class method (e.g. `SocialUI.Render()`), add a **separate
global** `RenderMenu()` that toggles a global bool, then gate the class method's window
with that bool. From pursuit-suite: global `bool g_ShowSocialUI` + global `RenderMenu()`
toggling it; `SocialUI::Render()` early-returns on `!g_ShowSocialUI`. (Right shape whenever
a class owns the window — don't put RenderMenu inside the class.)

## UI Scale — resolution-preset dropdown (preferred over a 0–1 slider)
For "scale the UI" settings, use an **enum** + a value-mapping function so the user picks
a named preset tuned per aspect ratio / resolution instead of a raw multiplier:

```angelscript
enum EUiScale {
    Scale_4to3_Low = 0;  // ~800x600  -> 0.55
    Scale_4to3_Std = 1;  // ~1024x768 -> 0.70
    Scale_16to9_Sm = 2;  // ~1280x720 -> 0.80
    Scale_1080p    = 3;  // 1920x1080 -> 0.90
    Scale_1440p    = 4;  // 2560x1440 -> 1.00 (default)
    Scale_4K        = 5;  // 3840x2160 -> 1.20
}
[Setting category="UI" name="UI Scale" description="Scale the plugin UI. Pick a preset matching your resolution (smaller = 4:3 / low-res)."]
EUiScale S_UIScale = EUiScale::Scale_1440p;

float UiScaleValue(EUiScale s) {
    if      (s == EUiScale::Scale_4to3_Low) return 0.55f;
    else if (s == EUiScale::Scale_4to3_Std) return 0.70f;
    else if (s == EUiScale::Scale_16to9_Sm) return 0.80f;
    else if (s == EUiScale::Scale_1080p)    return 0.90f;
    else if (s == EUiScale::Scale_1440p)    return 1.00f;
    else if (s == EUiScale::Scale_4K)       return 1.20f;
    return 1.0f;
}
```

Apply in each render function:

```angelscript
void RenderWindow() {
    float uiScale = UiScaleValue(S_UIScale);   // declare at TOP, before any early-return branch
    UI::SetNextWindowSize(580 * uiScale, 450 * uiScale, UI::Cond::FirstUseEver);
    if (UI::Begin("Title", g_ShowWindow)) {
        UI::PushFontSize(16.0f * uiScale);
        // ... draw ...
        UI::PopFontSize();   // MUST match PushFontSize within the same window scope
    }
    UI::End();
}
```

### Pitfalls when scaling
- **Scale the MINIMUM window sizes too.** If a render fn locks a minimum
  (`if (ws.x < minWindowW) UI::SetWindowSize(...)`), multiply `minWindowW/minWindowH` by
  `uiScale`. Otherwise the window never actually shrinks on low-res / 4:3 and the setting
  feels broken (explicit user complaint: window too big on 4:3 low-res).
- **Declare `uiScale` at the very top of the function**, before any `if (...) { ...; return; }`
  branch that uses it. A function with an early-return modal branch
  (e.g. `if (S_BlockOutsideX) { ...; return; }`) will reference an undeclared `uiScale` in
  that branch if the declaration sat after it → compile error.
- **Balance PushFontSize/PopFontSize** per window. Count them; a mismatch corrupts the
  style stack and crashes the overlay.
- `UI::PushFontSize(float)` is the confirmed, repo-proven scaling primitive (used in
  event-calendar, apeiron-galaxy). Prefer it over uncertain APIs.
- Openplanet compiles **all** plugin `.as` files together — no `#include` is needed for
  cross-file globals/enum/functions. A helper like `UiScaleValue()` defined in Settings.as
  is visible everywhere in the plugin.

## Local docs caveat
`C:\Users\tomekdot\Openplanet4\docs` (lowercase `docs`) holds Openplanet tutorial / API
markdown but does **not** include the `UI::` namespace function reference. Don't assume
`UI::SetNextWindowContentScale` (or similar) exists — verify against openplanet.dev/docs/api,
and prefer functions already proven in-repo (`UI::PushFontSize`, `UI::SetNextWindowSize`,
`UI::Begin`, `UI::MenuItem`).
