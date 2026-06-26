# Ink Component API Reference

## `<Box>`

A Flexbox layout container. Renders children according to Yoga layout rules.

```tsx
import { Box, Text } from 'ink';

<Box flexDirection="column" gap={1} padding={1} borderStyle="round">
  <Text bold>Card Title</Text>
  <Text>Body content goes here</Text>
</Box>
```

### Full Prop Table

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `width` | number | — | Fixed width in characters |
| `minWidth` | number | — | Minimum width |
| `height` | number | — | Fixed height in lines |
| `minHeight` | number | — | Minimum height |
| `flexGrow` | number | 0 | Flex grow factor |
| `flexShrink` | number | 1 | Flex shrink factor |
| `flexBasis` | number/string | auto | Flex basis |
| `flexDirection` | `"row"`/`"column"`/`"row-reverse"`/`"column-reverse"` | `"row"` | Main axis direction |
| `justifyContent` | `"flex-start"`/`"center"`/`"flex-end"`/`"space-between"`/`"space-around"` | `"flex-start"` | Main axis alignment |
| `alignItems` | `"flex-start"`/`"center"`/`"flex-end"`/`"stretch"` | `"stretch"` | Cross axis alignment |
| `alignSelf` | `"flex-start"`/`"center"`/`"flex-end"`/`"stretch"` | — | Override parent alignItems |
| `gap` | number | 0 | Spacing between children |
| `padding` | number | 0 | Padding all sides |
| `paddingX` | number | 0 | Horizontal padding |
| `paddingY` | number | 0 | Vertical padding |
| `paddingTop` | number | 0 | Top padding |
| `paddingBottom` | number | 0 | Bottom padding |
| `paddingLeft` | number | 0 | Left padding |
| `paddingRight` | number | 0 | Right padding |
| `margin` | number | 0 | Margin all sides |
| `marginX` | number | 0 | Horizontal margin |
| `marginY` | number | 0 | Vertical margin |
| `marginTop` | number | 0 | Top margin |
| `marginBottom` | number | 0 | Bottom margin |
| `marginLeft` | number | 0 | Left margin |
| `marginRight` | number | 0 | Right margin |
| `borderStyle` | string | — | Border style (see below) |
| `borderColor` | string | — | Border color name |
| `borderDimColor` | boolean | false | Dim the border color |
| `textWrap` | `"wrap"`/`"word-break"`/`"truncate"`/`"truncate-start"`/`"truncate-middle"`/`"truncate-end"` | `"wrap"` | Text wrap mode |
| `display` | `"flex"`/`"none"` | `"flex"` | Display mode |
| `overflow` | string | — | Overflow behavior |

### Border Styles

- `"single"` — ┌─┐│└ ┘  
- `"double"` — ╔═╗║╚ ╝  
- `"round"` — ╭─╮│╰ ╯  
- `"classic"` — +-+|+ +  
- `"bold"` — ┏━┓┃┗ ┛  
- `"singleDouble"` — ╓─╖║╙ ╜  
- `"doubleSingle"` — ╒═╕│└ ╛  

### Layout Shortcuts

```tsx
<Box width="50%" />       // percentage of parent
<Box width={40} />        // fixed 40 chars
<Box column />            // same as flexDirection="column"
<Box row />               // same as flexDirection="row"
```

---

## `<Text>`

Renders styled text to the terminal. Supports nesting for mixed styles.

```tsx
<Text color="green" bold>Success!</Text>

// Nesting
<Text>
  Hello <Text color="cyan" bold>World</Text>!
</Text>

// Truncation
<Text wrap="truncate-end">A very long text that will be cut off...</Text>
```

### Text Props

| Prop | Type | Description |
|------|------|-------------|
| `color` | string | Text color (name, hex, or rgb) |
| `backgroundColor` | string | Background color |
| `bold` | boolean | Bold text |
| `dim` | boolean | Dim/faint |
| `italic` | boolean | Italic |
| `underline` | boolean | Underline |
| `overline` | boolean | Overline |
| `strikethrough` | boolean | Strikethrough |
| `inverse` | boolean | Swap foreground/background |
| `hidden` | boolean | Invisible text |
| `wrap` | string | Text wrap mode |

### Color Names

**Standard:** black, red, green, yellow, blue, magenta, cyan, white, gray, grey

**Bright:** redBright, greenBright, yellowBright, blueBright, magentaBright, cyanBright, whiteBright

**Background:** prefix with `bg` (bgGreen, bgRed, bgCyanBright)

**CSS-style:** `"#ff0000"`, `"rgb(255,0,0)"`, `"hsl(0,100%,50%)"`

---

## `<Newline>`

```tsx
<Newline />       // one blank line
<Newline count={3} />  // three blank lines
```

---

## `<Spacer>`

```tsx
<Spacer />             // fills available space (flex: 1)
<Spacer height={2} />  // fixed 2-line spacer
```

---

## `<Stdin>`

Low-level stdin access. Use `useInput` for most cases.

```tsx
<Stdin onData={data => handle(data.toString())} />
```

---

## `<Stdout>`, `<Stderr>`

Stream capture for testing output.

```tsx
<Stdout onData={data => { /* capture stdout */ }} />
<Stderr onData={data => { /* capture stderr */ }} />
```

---

## `<Transform>`

Applies a transform function to children content before rendering. Useful for custom formatting.

```tsx
import { Transform } from 'ink';

<Transform transform={text => text.toUpperCase()}>
  Make me shout
</Transform>
```