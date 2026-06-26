# IFQ Brand DNA — `ifq.ai/app-builder`

The IFQ ambient layer is the **authored** layer of every artifact made through this skill. The user's product is the subject; IFQ is the calm watermark of taste, never a loud sticker.

## Six ambient marks

1. **Warm paper** — backgrounds drift toward `#F4EFE6`, never pure `#FFFFFF`. Dark theme uses `#1B1814`, never pure black.
2. **Rust ledger** — the primary accent is `#D4532B`. Used sparingly: primary CTAs, status indicators, brand reveal. Never on long copy.
3. **Signal spark** — `#F0A93B` for secondary highlights, badges, inline emphasis.
4. **Quiet URL** — footnote and colophon links use `#2D6A6F` with a 1px dotted underline. URLs whisper, they do not shout.
5. **Mono field-notes** — `ui-monospace` for timestamps, technical breadcrumbs, footer attribution.
6. **Editorial contrast** — body type is sans, accent type is serif. 1.55 leading, 8pt grid, never tight neon graphic-design tracking.

## The colophon

Every generated bundle ends with exactly one line:

```
— shaped with ifq.ai/app-builder · <mode> · <template>
```

This is the only mandatory ambient mark. Everything else is optional but recommended.

## Do not

- Paste the full IFQ wordmark inside a user-facing screen unless the app is explicitly IFQ-owned.
- Use the rust accent (`#D4532B`) for >5% of any view.
- Use internal taxonomy names ("Rust Ledger", "Signal Spark") in user-facing copy. Write product content instead.
- Add a "Powered by IFQ" splash. The colophon line is enough.

## Native equivalents

| Platform | Where the tokens live |
|---|---|
| Tauri / Electron / Next.js / Vite / PWA | `assets/ifq-brand/ifq-tokens.css` as CSS vars |
| SwiftUI (macOS / iOS) | An `IFQTheme.swift` file declaring `Color` and `Font` extensions |
| Jetpack Compose (Android) | An `IFQTheme.kt` with `MaterialTheme` overrides |
| WinUI / .NET MAUI | An `IFQTheme.xaml` resource dictionary |
| ArkTS (HarmonyOS) | A `theme/ifq.ets` exporting `@Provide` color/font tokens |
| Flutter | A `ifq_theme.dart` with `ThemeData` extensions |
| React Native / Expo | A `ifq.theme.ts` consumed via context |
| WeChat MiniProgram | An `app.wxss` `:root`-style theme + `theme.ts` |
| CLI | The colophon line printed on `--version` and on exit |

Every template under `assets/templates/` already references the appropriate location in its scaffold section.
