---
name: primevue
description: "PrimeVue UI component library for Vue.js with 100+ components. Covers design token theming, unstyled mode, pass-through (pt) styling, forms with validation, and component usage."
metadata:
  author: yuexiaoliang
  version: "1.0.0"
---

# PrimeVue

PrimeVue is a next-generation Vue.js UI component suite by PrimeTek. Features 100+ components, design token-based theming, and unstyled mode for Tailwind/CSS integration.

## Quick Start

```bash
npm install primevue @primevue/themes
```

```vue
import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

const app = createApp(App);
app.use(PrimeVue, {
    theme: { preset: Aura, options: { darkModeSelector: '.dark' } },
    ripple: true
});
```

## Core Concepts

### Two Styling Modes

**Styled Mode** (default): Pre-skinned components with design token theming. Built-in presets: Aura, Material, Lara, Nora.

**Unstyled Mode**: Components render without styles, fully styled via Pass Through (pt) with Tailwind, Bootstrap, or custom CSS.

### Pass Through (pt)

Access internal DOM of any component to add arbitrary attributes, classes, aria, or events — no need to wait for component API updates.

```vue
<Button
    label="Search"
    icon="pi pi-search"
    :pt="{
        root: 'bg-teal-500 hover:bg-teal-700',
        label: 'text-white font-bold'
    }"
/>
```

### Design Tokens

Three-tier token system: **primitive** (raw values like colors) → **semantic** (meaningful names like primary.color) → **component** (per-component like button.background).

## Popular Components

| Component | Tag | Use Case |
|-----------|-----|----------|
| Button | `<Button>` | Actions, submit |
| DataTable | `<DataTable>` | Tabular data with sorting/filtering |
| Dialog | `<Dialog>` | Modal overlay |
| InputText | `<InputText>` | Text input |
| Dropdown | `<Select>` | Single selection |
| MultiSelect | `<MultiSelect>` | Multiple selection |
| Toast | `<Toast>` | Notifications |
| Menu | `<Menu>` | Navigation/list |
| Dialog | `<Dialog>` | Overlay content |
| Card | `<Card>` | Content container |
| Panel | `<Panel>` | Collapsible content |
| Toolbar | `<Toolbar>` | Button grouping |

## Forms

PrimeVue Forms library (`@primevue/forms`) provides state management with built-in validation.

```vue
<Form v-slot="$form" :initialValues :resolver @submit="onSubmit">
    <InputText name="username" />
    <Message v-if="$form.username?.invalid">{{ $form.username.error.message }}</Message>
    <Button type="submit" />
</Form>
```

Resolvers available for: Zod, Yup, Joi, Valibot, Superstruct.

## Configuration

```vue
app.use(PrimeVue, {
    ripple: true,              // Enable ripple effect
    inputVariant: 'filled',    // 'outlined' | 'filled'
    unstyled: false,           // Enable unstyled mode globally
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: '.dark',
            cssLayer: false
        }
    },
    pt: { /* global pass-through */ },
    zIndex: {
        modal: 1100,
        overlay: 1000,
        menu: 1000,
        tooltip: 1100
    }
});
```

## Theming

### Use Built-in Preset

```vue
import Aura from '@primeuix/themes/aura';
app.use(PrimeVue, { theme: { preset: Aura } });
```

### Customize Preset

```vue
import { definePreset } from '@primeuix/themes';
const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{indigo.50}',
            500: '{indigo.500}',
            // ... 50-950
        },
        colorScheme: {
            light: { surface: { 0: '#fff' } },
            dark: { surface: { 0: '#1a1a1a' } }
        }
    }
});
app.use(PrimeVue, { theme: { preset: MyPreset } });
```

### Runtime Updates

```vue
import { updatePreset, usePreset } from '@primeuix/themes';
updatePreset({ semantic: { primary: { 500: '#f59e0b' } } });
usePreset(MyPreset);  // Replace entirely
```

## Icons

```vue
<i class="pi pi-check"></i>
<span class="pi pi-spin pi-spinner"></span>

// Custom icon
<Select>
    <template #dropdownicon>
        <i class="fa-solid fa-chevron-down"></i>
    </template>
</Select>
```

## Installation Options

```bash
# Vite
npm create vite@latest my-app -- --template vue
npm install primevue @primevue/themes

# Nuxt
npm install @primeuix/nuxt

# Laravel
npm install primevue @primevue/themes
# Follow Laravel integration guide

# CDN
<script src="https://unpkg.com/primevue/umd/primevue.min.js"></script>
```

## Reference Docs

- [Theming & Design Tokens](references/theming.md)
- [Unstyled Mode & Pass Through](references/unstyled.md)
- [Forms Library](references/forms.md)
- [Components](references/components.md)
