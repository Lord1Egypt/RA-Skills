---
name: module-tsx
description: >
  Use this skill whenever a user wants to run TypeScript, TSX, or React in the
  browser without a build step, or asks about module-tsx. Triggers on: "run
  TypeScript in the browser", "no build step", "inline TSX", "module-tsx",
  "script type module-tsx", "React without bundler", "write a page that uses
  React with TypeScript", "browser TypeScript", "build-free React", or any
  request to write an HTML page that imports or renders TypeScript/TSX code.
  Always use this skill when writing HTML that needs to execute TypeScript or
  JSX in the browser.
---

# module-tsx skill

module-tsx runs TypeScript and TSX directly in the browser — no build step, no
bundler. It transpiles code on the fly and rewrites bare specifiers (like
`"react"`) to `https://esm.sh/<pkg>` automatically.

## How to load it

```html
<script type="module" src="https://esm.sh/module-tsx"></script>
```

Load this **before** any `<script type="module-tsx">` tags.

## Writing code

Use `<script type="module-tsx">` like `<script type="module">` but with full
TypeScript and JSX support:

```html
<script type="module-tsx">
  const greet = (name: string) => `Hello, ${name}!`
  console.log(greet("world"))
</script>
```

Or load an external file:

```html
<script type="module-tsx" src="./main.tsx"></script>
```

## React / TSX — zero config

Bare specifiers resolve to esm.sh automatically, so React just works with no
import map needed. JSX without an explicit `import React` is fine too — it's
auto-injected:

```html
<div id="root"></div>
<script type="module-tsx">
  import { createRoot } from "react-dom/client";

  function App() {
    return <h1>Hello!</h1>;   // React auto-injected, no import needed
  }

  createRoot(document.getElementById("root")!).render(<App />)
</script>
```

## Example complete page

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My App</title>
    <script type="module" src="https://esm.sh/module-tsx"></script>
  </head>
  <body>
    <div id="root"></div>
    <script type="module-tsx">
      import { createRoot } from "react-dom/client";
      import "@tailwindcss/browser";

      interface Props { name: string }

      function Greeting({ name }: Props) {
        return <h1 class="text-2xl font-bold">Hello, {name}!</h1>;
      }

      createRoot(document.getElementById("root")!).render(<Greeting name="world" />);
    </script>
  </body>
</html>
```

## Import maps — only when you need them

An import map is optional. Use one only when you need to:

- **Pin a specific version** (e.g. `react@18` instead of latest)
- **Deduplicate peer dependencies** across packages

The import map must be declared **before** the module-tsx script tag, because
module-tsx reads it at startup:

```html
<script type="importmap">
  {
    "imports": {
      "react": "https://esm.sh/react@18",
      "react-dom/client": "https://esm.sh/react-dom@18/client"
    }
  }
</script>
<script type="module" src="https://esm.sh/module-tsx"></script>
```

### Peer dependency deduplication

When a UI library (like `@radix-ui/themes`) depends on the same React as your
app, both must resolve to the exact same URL or you get "Invalid hook call"
crashes. Use `?deps=` to tell the CDN which React to bundle against:

```html
<script type="importmap">
  {
    "imports": {
      "react": "https://esm.sh/react@18",
      "react-dom": "https://esm.sh/react-dom@18",
      "react-dom/": "https://esm.sh/react-dom@18/",
      "@radix-ui/themes": "https://esm.sh/@radix-ui/themes?deps=react@18,react-dom@18",
      "@radix-ui/themes/": "https://esm.sh/@radix-ui/themes/"
    }
  }
</script>
<script type="module" src="https://esm.sh/module-tsx"></script>
<script type="module-tsx">
  import '@radix-ui/themes/styles.css' // .css files will be injected as <style> tags
</script>
```

## Relative imports

`.ts` and `.tsx` files can be imported relatively — fetched and transpiled on the fly:

```tsx
import { Button } from "./components/Button.tsx";
```

## CSS imports

```tsx
import "./style.css"; // injects a <style> tag into <head>
import styles from "./button.module.css"; // returns { root: "abc123_root", ... }
```

## Dev vs Production

Use the **dev** build during development for a rich error overlay (runtime errors,
failed imports, source-mapped stack traces with code frames):

```html
<script type="module" src="https://esm.sh/module-tsx/dev"></script>
```

Use the **production** build for deployment (no error overlay, smaller footprint):

```html
<script type="module" src="https://esm.sh/module-tsx"></script>
```

## Common mistakes

- **`defer` attribute**: not supported. Use `async` or no attribute.
- **Dual React**: if a package depends on React as a peer, use `?deps=react@18`
  so it shares the same instance — otherwise you'll get hook errors.
- **Import map ordering**: if you use an import map, it must come before the
  module-tsx `<script>` tag.
