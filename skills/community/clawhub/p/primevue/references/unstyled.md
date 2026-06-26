# PrimeVue Unstyled Mode & Pass Through

## Setup

### Global Unstyled Mode

```vue
import { createApp } from 'vue';
import PrimeVue from 'primevue/config';

const app = createApp(App);
app.use(PrimeVue, { unstyled: true });
```

### Per-Component

```vue
<Button unstyled label="Styled with pt" />
<Button label="Default styled" />
```

## Pass Through (pt)

Each component exposes its internal DOM structure via the `pt` property. Access any element to add classes, styles, aria, data-*, or events.

### Basic Usage

```vue
<Panel
    header="Header"
    :pt="{
        root: 'border rounded p-4',
        header: { class: 'flex items-center justify-between' },
        title: 'text-xl font-bold',
        content: 'mt-4 text-gray-600',
        toggler: { class: 'hover:bg-gray-100 rounded p-2' }
    }"
>
    Content here
</Panel>
```

### Value Formats

pt values can be strings, objects, or functions:

```vue
:pt="{
    root: 'bg-primary',                              // string = class
    header: { class: 'text-lg', id: 'my-header' },  // object with properties
    content: (options) => ({                         // function returning object
        class: ['text-sm', { 'text-red': options.context.active }],
        style: { background: 'white' }
    })
}"
```

## Pass Through Properties

### Global Config

Apply pt to all instances of a component:

```vue
app.use(PrimeVue, {
    unstyled: true,
    pt: {
        button: {
            root: 'bg-blue-500 text-white px-4 py-2 rounded',
            label: 'font-medium'
        },
        panel: {
            header: 'bg-gray-100 p-4',
            content: 'p-4'
        }
    }
});
```

Component-level pt overrides global config.

### Component Override

```vue
<Button
    pt="{
        root: '!bg-red-500',  /* ! important */
        label: '!text-white'
    }"
/>
```

## PC Prefix

Components inside other components use `pc` prefix. E.g., Button's internal Badge is `pcBadge`:

```vue
<Button
    badge="2"
    :pt="{
        root: 'px-4 py-2',
        pcBadge: { root: '!bg-violet-500 !text-white' }
    }"
/>
```

## Tailwind Example

```vue
<Button
    label="Search"
    icon="pi pi-search"
    unstyled
    pt:root="bg-teal-500 hover:bg-teal-700 active:bg-teal-900 cursor-pointer py-2 px-4 rounded-full border-0 flex gap-2"
    pt:label="text-white font-bold text-lg"
    pt:icon="text-white text-xl"
/>
```

## Global Tailwind Config

```vue
app.use(PrimeVue, {
    unstyled: true,
    pt: {
        button: {
            root: 'cursor-pointer rounded-lg font-semibold transition-all duration-200',
            label: 'flex items-center gap-2'
        },
        inputtext: {
            root: 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
        },
        panel: {
            root: 'border border-gray-200 rounded-lg shadow-sm',
            header: 'flex items-center justify-between px-4 py-3 border-b',
            title: 'font-semibold text-gray-700',
            content: 'p-4'
        }
    }
});
```

## Volt (Tailwind v4 UI Library)

PrimeTek's official Tailwind v4 + PrimeVue library. Components live in your codebase (not node_modules):

```bash
npm install @volt-ui/vue
```

## Lifecycle Hooks

Access component lifecycle via `hooks` property:

```vue
<Panel
    :pt="{
        root: { class: 'my-panel' },
        hooks: {
            onMounted: () => console.log('mounted'),
            onUpdated: () => console.log('updated')
        }
    }"
>
    Content
</Panel>
```

Available hooks: `onBeforeCreate`, `onCreated`, `onBeforeUpdate`, `onUpdated`, `onBeforeMount`, `onMounted`, `onBeforeUnmount`, `onUnmounted`.

## usePassThrough Utility

Merge/extend existing pt configs:

```vue
import { usePassThrough } from '@primevue/core';

const customButton = usePassThrough(
    defaultButtonPT,    // base config
    { root: 'custom-class' },
    { mergeSections: true, mergeProps: false }
);
```

## CSS Custom Properties

Combine pt with CSS custom properties:

```vue
<Button
    :pt="{
        root: 'transition-colors duration-200',
        label: 'text-sm'
    }"
    style="--my-brand: #10b981"
>
```

## Declarative Syntax (pt:*)

Alternative to `:pt` object — use `pt:` prefix in template:

```vue
<Panel
    pt:root="border rounded p-4"
    pt:header="bg-gray-50 px-4 py-2"
    pt:content="mt-2"
>
    Content
</Panel>
```

## Custom CSS in pt

```vue
app.use(PrimeVue, {
    pt: {
        global: {
            css: `
                .my-button { border: 2px solid currentColor; }
                @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
                .fade-in { animation: fadeIn 0.3s ease; }
            `
        }
    }
});
```

## Common Use Cases

### Add aria attributes

```vue
<DataTable
    :pt="{
        root: { 'aria-label': 'User list' },
        table: { 'aria-rowcount': totalRows }
    }"
/>
```

### Add data-testid

```vue
<Button
    label="Submit"
    :pt="{
        root: { 'data-testid': 'submit-btn' },
        label: { 'data-cy': 'submit-label' }
    }"
/>
```

### Dynamic styling based on state

```vue
<Button
    :pt="(options) => ({
        root: {
            class: [
                'px-4 py-2 rounded',
                options.context.active ? 'bg-blue-700' : 'bg-blue-500',
                { 'opacity-50': options.context.disabled }
            ]
        }
    })"
/>
```

## CSS Layer with Pass Through

When using `cssLayer: true`, PrimeVue styles are wrapped in the `primevue` layer:

```css
@layer reset, primevue;

/* Your reset */
@layer reset { button { margin: 0; } }

/* PrimeVue in primevue layer */
@layer primevue { .p-button { margin: 0; } }
```

This makes your CSS (no layer) highest priority, so overrides work without `!important`.
