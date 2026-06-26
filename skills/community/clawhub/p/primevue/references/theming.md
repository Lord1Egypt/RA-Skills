# PrimeVue Theming

## Architecture

**Styled mode** uses design tokens to separate styling from components.

Three token tiers:
1. **Primitive** — Raw values like `blue-50` to `blue-900` (no context)
2. **Semantic** — Meaningful names like `primary.color`, `surface.background`
3. **Component** — Per-component tokens like `button.background`, `inputtext.border`

A **preset** is a collection of design tokens (Aura, Material, Lara, Nora built-in).

## Setup

```vue
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',              // CSS variable prefix (default: 'p')
            darkModeSelector: '.dark', // or 'system', false
            cssLayer: false
        }
    }
});
```

## Built-in Presets

| Preset | Style | Notes |
|--------|-------|-------|
| Aura | PrimeTek's own | Default |
| Material | Google Material v2 | |
| Lara | Bootstrap-inspired | |
| Nora | Enterprise-focused | |

## Custom Preset

```vue
import { definePreset } from '@primeuix/themes';
import Aura from '@primeuix/themes/aura';

const MyPreset = definePreset(Aura, {
    // Override tokens here
});
```

## Change Primary Color

```vue
const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{indigo.50}',
            100: '{indigo.100}',
            200: '{indigo.200}',
            300: '{indigo.300}',
            400: '{indigo.400}',
            500: '{indigo.500}',  // Main color
            600: '{indigo.600}',
            700: '{indigo.700}',
            800: '{indigo.800}',
            900: '{indigo.900}',
            950: '{indigo.950}'
        }
    }
});
```

## Surface Colors

```vue
const MyPreset = definePreset(Aura, {
    semantic: {
        colorScheme: {
            light: {
                surface: {
                    0: '#ffffff',
                    50: '{zinc.50}',
                    // ... 100-950
                }
            },
            dark: {
                surface: {
                    0: '#ffffff',
                    50: '{slate.50}',
                    // ... 100-950
                }
            }
        }
    }
});
```

## Dark Mode

Default uses system preference. For toggleable dark mode:

```vue
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.dark-mode'  // Toggle this class on <html>
        }
    }
});
```

Toggle via JS:
```js
document.documentElement.classList.toggle('dark-mode');
```

## Focus Ring

```vue
const MyPreset = definePreset(Aura, {
    semantic: {
        focusRing: {
            width: '2px',
            style: 'dashed',  // or 'solid'
            color: '{primary.color}',
            offset: '1px'
        }
    }
});
```

## Form Input Styling

```vue
const MyPreset = definePreset(Aura, {
    semantic: {
        colorScheme: {
            light: {
                formField: {
                    hoverBorderColor: '{primary.color}'
                }
            },
            dark: {
                formField: {
                    hoverBorderColor: '{primary.color}'
                }
            }
        }
    }
});
```

## Component Tokens

Override specific component styles (not recommended — prefer custom preset):

```vue
const MyPreset = definePreset(Aura, {
    components: {
        card: {
            colorScheme: {
                light: {
                    root: { background: '{surface.0}', color: '{surface.700}' },
                    subtitle: { color: '{surface.500}' }
                },
                dark: {
                    root: { background: '{surface.900}', color: '{surface.0}' }
                }
            }
        }
    }
});
```

## Extend (Custom Tokens + CSS)

```vue
const MyPreset = definePreset(Aura, {
    components: {
        button: {
            extend: {
                accent: {
                    color: '#f59e0b',
                    inverseColor: '#ffffff'
                }
            },
            css: ({ dt }) => `
                .p-button-accent {
                    background: ${dt('button.accent.color')};
                    color: ${dt('button.accent.inverseColor')};
                }
            `
        }
    },
    extend: {
        my: {
            transition: { fast: '0.25s', normal: '0.5s' }
        }
    },
    css: ({ dt }) => `
        img { display: ${dt('my.imageDisplay')}; }
    `
});
```

## Noir Mode (Surface-based Primary)

```vue
const Noir = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{zinc.50}',
            // ... 50-950
        },
        colorScheme: {
            light: {
                primary: {
                    color: '{zinc.950}',
                    inverseColor: '#ffffff',
                    hoverColor: '{zinc.900}',
                    activeColor: '{zinc.800}'
                },
                highlight: {
                    background: '{zinc.950}',
                    color: '#ffffff'
                }
            },
            dark: {
                primary: {
                    color: '{zinc.50}',
                    inverseColor: '{zinc.950}',
                    hoverColor: '{zinc.100}',
                    activeColor: '{zinc.200}'
                },
                highlight: {
                    background: 'rgba(250,250,250,.16)',
                    color: 'rgba(255,255,255,.87)'
                }
            }
        }
    }
});
```

## Palette Utility

Generate color shades programmatically:

```vue
import { palette } from '@primeuix/themes';

const values = palette('#10b981');  // { 50: '#ecfdf5', ... 950: '#064e3b' }
const copyPrimary = palette('{blue}');
```

## $dt Utility

Access token values programmatically:

```vue
import { $dt } from '@primeuix/themes';

const primary = $dt('primary.color');
// { variable: 'var(--p-primary-color)', value: { light: '#10b981', dark: '#34d399' } }
```

## Runtime Updates

```vue
import { updatePreset, updatePrimaryPalette, updateSurfacePalette, usePreset } from '@primeuix/themes';

// Partial merge
updatePreset({ semantic: { primary: { 500: '#f59e0b' } } });

// Shorthand for primary
updatePrimaryPalette({ 500: '#f59e0b', /* ... */ });

// Shorthand for surface
updateSurfacePalette({ light: { 50: '#fafafa' }, dark: { 50: '#1a1a1a' } });

// Replace entirely
usePreset(MyPreset);
```

## Color Scheme Tokens

When customizing presets with `colorScheme`, you must match the structure — if the original uses `colorScheme`, your override must too, or it will be ignored.

```vue
// ❌ Wrong — ignored if preset uses colorScheme
const MyPreset = definePreset(Aura, {
    semantic: { primary: { color: '#f00' } }  // won't work if Aura uses colorScheme
});

// ✅ Correct — match original structure
const MyPreset = definePreset(Aura, {
    semantic: {
        colorScheme: {
            light: { primary: { color: '#f00' } },
            dark: { primary: { color: '#f00' } }
        }
    }
});
```

## CSS Layer

Enable for easier style overrides and CSS Modules compatibility:

```vue
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: { cssLayer: true }
    }
});
```

Layer order:
```css
@layer reset, primevue;  /* reset has higher specificity */
```

## Reserved Keys

Cannot use as token names: `primitive`, `semantic`, `components`, `directives`, `colorscheme`, `light`, `dark`, `common`, `root`, `states`, `extend`.

## Scale

Components use `rem` units. Adjust base font-size:

```css
html { font-size: 14px; }  /* default is 16px */
```
