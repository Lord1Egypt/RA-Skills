# Table2Image API Reference

Complete API documentation for the Table2Image skill.

## Functions

### `renderTable(config)`

Main rendering function with full configuration options.

**Parameters:**
- `config` (Object):
  - `data` (Array): Array of row objects
  - `columns` (Array): Column definitions
  - `title` (String, optional): Table title
  - `subtitle` (String, optional): Table subtitle  
  - `theme` (String|Object, optional): Theme name or custom theme object. Built-in names: `discord-light`, `discord-dark`, `finance`, `minimal`, `sweet-pink`, `deep-sea`, `wisteria`, `pond-blue`, `camellia`
  - `maxWidth` (Number, optional): Max table width in pixels (default: 800)
  - `stripe` (Boolean, optional): Enable alternating row colors (default: true)

**Returns:** `Promise<{ buffer, width, height, format }>`

**Example:**
```typescript
const result = await renderTable({
  data: [{ name: 'AAPL', price: 150 }],
  columns: [
    { key: 'name', header: 'Stock', width: 100 },
    { key: 'price', header: 'Price', align: 'right' }
  ],
  title: 'Stocks',
  theme: 'discord-dark'
});
```

### `renderDiscordTable(data, columns, title?)`

Quick-render function optimized for Discord.

**Parameters:**
- `data` (Array): Row data
- `columns` (Array): Column definitions (simplified)
- `title` (String, optional): Table title

**Returns:** `Promise<{ buffer, width, height, format }>`

**Example:**
```typescript
const image = await renderDiscordTable(
  [{ name: 'BTC', price: 50000 }],
  [
    { key: 'name', header: 'Crypto' },
    { key: 'price', header: 'Price', align: 'right' }
  ],
  '💰 Crypto Prices'
);
```

### `renderFinanceTable(data, columns, title?)`

Quick-render function optimized for financial data.

Same API as `renderDiscordTable`, but uses 'finance' theme and includes:
- Automatic number formatting
- Conditional coloring for positive/negative values

### `autoConvertMarkdownTable(content, channel, options?)`

Automatically detect and convert markdown tables in content.

**Parameters:**
- `content` (String): Message content potentially containing markdown table
- `channel` (String): Target channel ('discord', 'telegram', 'whatsapp', etc.)
- `options` (Object, optional):
  - `theme` (String): Override default theme
  - `title` (String): Table title
  - `maxWidth` (Number): Max width

**Returns:** `Promise<{ converted: boolean, image?: Buffer, tableCount?: number }>`

**Example:**
```typescript
const result = await autoConvertMarkdownTable(
  '| Stock | Price |\n|-------|-------|\n| AAPL | $150 |',
  'discord'
);

if (result.converted) {
  await message.send({ attachment: result.image });
}
```

## Column Configuration

```typescript
{
  key: string,              // Data property name
  header: string,           // Display header
  width?: number | 'auto',  // Column width
  align?: 'left' | 'center' | 'right',  // Text alignment
  formatter?: (value, row) => string,   // Value formatter
  style?: CellStyle | ((value, row) => CellStyle),  // Styling
  wrap?: boolean,           // Enable text wrapping
  maxLines?: number         // Max lines when wrapping
}
```

## CellStyle

```typescript
{
  color?: string,           // Text color (hex)
  backgroundColor?: string, // Background color
  fontWeight?: 'normal' | 'bold' | number
}
```

## Themes

### discord-dark
- Background: #2f3136
- Header: #5865F2
- Text: #dcddde
- Best for: Discord dark mode

### finance
- Background: #1a1a2e
- Header: #16213e
- Text: #eaeaea
- Best for: Financial reports

### minimal
- Background: #ffffff
- Header: #333333
- Text: #333333
- Best for: Clean/simple presentations

### sweet-pink
- Background: #1A1A1D
- Header: #E6397C
- Text: #E6397C
- Best for: Stylish dark + pink accent

![sweet-pink](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-sweet-pink.png)

### deep-sea
- Background: #F5EFEA
- Header: #122E8A
- Text: #122E8A
- Best for: Classic blue + cream white

![deep-sea](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-deep-sea.png)

### wisteria
- Background: #5E55A2
- Header: #91C53A
- Text: #91C53A
- Best for: Retro purple + lime green

![wisteria](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-wisteria.png)

### pond-blue
- Background: #91CFD5
- Header: #113056
- Text: #113056
- Best for: Deep navy + soft cyan

![pond-blue](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-pond-blue.png)

### camellia
- Background: #F1DDDF
- Header: #E72D48
- Text: #E72D48
- Best for: Warm red + pale pink

![camellia](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-camellia.png)

## Custom Themes

You can pass a custom theme object directly to `renderTable()`.

### Shorthand: Primary + Secondary

For convenience, you only need to provide two colors. The engine will auto-generate the full theme:

```typescript
const image = await renderTable({
  data: stocks,
  columns: [...],
  theme: {
    primary: '#e6397c',    // accent → headerBg, text, border
    secondary: '#1a1a1d'   // base → background, rowBg, headerText
  }
});
```

Auto-generation rules:
- `headerBg` = `primary`
- `text` = `primary`
- `border` = `primary`
- `background` = `secondary`
- `rowBg` = `secondary`
- `headerText` = `secondary`
- `rowAltBg` = slightly lightened/darkened `secondary`

![custom-primary-secondary](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/custom-primary-secondary.png)

### Full Custom Theme

If you prefer full control, pass all 7 properties:

```typescript
const image = await renderTable({
  data: stocks,
  columns: [...],
  theme: {
    background: '#1a1a1d',
    headerBg: '#e6397c',
    headerText: '#1a1a1d',
    rowBg: '#1a1a1d',
    rowAltBg: '#2a2a2d',
    text: '#e6397c',
    border: '#e6397c'
  }
});
```

![custom-full](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/custom-full.png)

Required properties for a full custom theme:

| Property | Type | Description |
|----------|------|-------------|
| `background` | string | Table background color |
| `headerBg` | string | Header row background |
| `headerText` | string | Header text color |
| `rowBg` | string | Normal row background |
| `rowAltBg` | string | Alternating row background |
| `text` | string | Default text color |
| `border` | string | Border/line color |
