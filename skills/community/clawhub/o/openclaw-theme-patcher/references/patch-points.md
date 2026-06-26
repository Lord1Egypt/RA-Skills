# Bundle Patch Points

Use this file to patch the installed OpenClaw Control UI bundle with the smallest possible change set.

For upgrade migrations, use this file to compare the old saved bundle structures to the new live bundle before editing. Do not assume old patch locations survive a version bump.

## Active files

Patch the active install only:
- `dist/control-ui/assets/index-*.js`
- `dist/control-ui/assets/index-*.css`

Resolve the live install first with:

```bash
which openclaw
readlink -f "$(which openclaw)"
openclaw status
```

## JS patch points

In the minified JS bundle, locate these structures.

Migration rule: confirm each structure in the current live bundle before patching it. A previous version may have used a different variable name, list shape, or resolver branch layout.

### 1. Allowed theme id set

Typical shape:

```js
var Za=new Set([`claw`,`knot`,`dash`, ...])
```

Add the new theme id here.

### 2. Theme alias/default map

Typical shape:

```js
$a={...,tokyoNight:{theme:`tokyo-night`,mode:`dark`}}
```

Add an alias entry if the bundle uses one.

### 3. Theme card list in Appearance

Typical shape:

```js
var Wb=[
  {id:`claw`,label:`Claw`,...},
  ...
]
```

Add a new card:
- `id`: theme id
- `label`: user-facing label
- `description`: short description
- `icon`: reuse an existing icon token

### 4. Resolver function

Typical shape:

```js
function ro(e,t){...}
```

Required behavior:
- dark mode -> `<theme-id>`
- light mode -> `<theme-id>-light`

Critical warning:
- do not patch the resolver by broad heuristics such as replacing the first `return e`
- only edit the resolver after confirming the exact theme-switch branch in the current bundle
- if you cannot identify the resolver confidently, stop and inspect more context instead of guessing

## CSS patch points

Append or insert two theme selectors:

```css
:root[data-theme=<theme-id>]{...}
:root[data-theme=<theme-id>-light]{...}
```

Use an existing theme block as the structure template.

## Minimal verification

After patching, verify all of these:

1. Theme appears in `Settings -> Appearance -> Theme`
2. Selecting it changes the UI immediately or after hard refresh
3. Top-right light/dark toggle switches variants when both selectors exist
4. Existing themes still look unchanged

For migrations also verify:
5. The migrated theme visually matches the saved old CSS intent
6. No unrelated UI text/layout regressions appear after the JS patch

## Failure mapping

### Theme missing from list
- JS card list not patched
- theme id missing from allowed set
- stale cached JS
- wrong install path edited

### Theme visible but no visual change
- CSS selectors missing
- resolver targets wrong selector id
- wrong CSS file edited

### Light/dark toggle does nothing for new theme
- resolver missing new branch
- `<theme-id>-light` selector missing or misspelled

## Editing style

- prefer exact-text edits
- keep each edit surgical
- do not refactor minified bundle code
- patch the smallest number of strings needed
- when migrating, save the pre-edit live bundle or ensure you already have a stock recovery path
- if a migration patch breaks unrelated UI, remove the broken theme registration first, restore stock behavior, then retry from structural comparison
