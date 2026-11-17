# Evidence - ui-language-fix

## Build Summary

The language switcher now writes the selected locale to the existing user preference key and the navigation renderer reads labels from the locale dictionary on every render.

## AC1 - PASS

Verified with a German-locale browser session after saving language preference.

Observed labels:
- Home -> Startseite
- Settings -> Einstellungen
- Billing -> Abrechnung

## AC2 - PASS

Reloaded the page after saving German. The stored locale remained  and the German navigation labels were still visible.

## AC3 - PASS

Switched back to English. The navigation returned to:
- Home
- Settings
- Billing

No route names or preference keys changed.
