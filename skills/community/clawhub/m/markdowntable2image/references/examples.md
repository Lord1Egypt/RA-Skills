# Table2Image Examples

Common use cases and code patterns.

## Example 1: Discord Stock Report

```typescript
import { renderDiscordTable } from '../scripts/index.js';

const stocks = [
  { symbol: 'AAPL', price: 173.50, change: 2.5 },
  { symbol: 'GOOGL', price: 142.30, change: -1.2 },
  { symbol: 'MSFT', price: 378.90, change: 0.8 }
];

const image = await renderDiscordTable(
  stocks,
  [
    { key: 'symbol', header: 'Symbol', width: 80 },
    { 
      key: 'price', 
      header: 'Price', 
      align: 'right',
      formatter: (v) => `$${v.toFixed(2)}`
    },
    { 
      key: 'change', 
      header: 'Change %', 
      align: 'right',
      formatter: (v) => `${v > 0 ? '+' : ''}${v}%`,
      style: (v) => ({ color: v > 0 ? '#43b581' : '#f04747' })
    }
  ],
  '📊 Stock Market Update'
);

// Send to Discord
await message.send({ attachment: image.buffer });
```

## Example 2: Fund Portfolio

```typescript
import { renderFinanceTable } from '../scripts/index.js';

const portfolio = [
  { name: '天弘人工智能C', nav: 1.2345, change: -0.54, value: 12345 },
  { name: '诺德新生活A', nav: 2.1567, change: -0.66, value: 10783 }
];

const image = await renderFinanceTable(
  portfolio,
  [
    { key: 'name', header: '基金', width: 160 },
    { 
      key: 'nav', 
      header: '净值', 
      align: 'right',
      formatter: (v) => v.toFixed(4)
    },
    { 
      key: 'change', 
      header: '涨跌', 
      align: 'right',
      formatter: (v) => `${v > 0 ? '+' : ''}${v}%`,
      style: (v) => ({ color: v >= 0 ? '#43b581' : '#f04747' })
    },
    { 
      key: 'value', 
      header: '市值', 
      align: 'right',
      formatter: (v) => `¥${v.toLocaleString()}`
    }
  ],
  '💰 基金持仓'
);
```

## Example 3: Leaderboard with Medals

```typescript
import { renderTable } from '../scripts/index.js';

const players = [
  { rank: 1, name: 'Player1', score: 9500 },
  { rank: 2, name: 'Player2', score: 8200 },
  { rank: 3, name: 'Player3', score: 7800 }
];

const image = await renderTable({
  data: players,
  columns: [
    { 
      key: 'rank', 
      header: '', 
      width: 40,
      align: 'center',
      formatter: (v) => ['🥇', '🥈', '🥉'][v-1] || v
    },
    { key: 'name', header: 'Player' },
    { 
      key: 'score', 
      header: 'Score', 
      align: 'right',
      formatter: (v) => v.toLocaleString()
    }
  ],
  title: '🏆 Leaderboard',
  theme: 'discord-dark'
});
```

## Example 4: Auto-detect from Message

```typescript
import { autoConvertMarkdownTable } from '../scripts/index.js';

// User message contains markdown table
const userMessage = `
Check out today's prices:

| Crypto | Price | 24h |
|--------|-------|-----|
| BTC | $50,000 | +5% |
| ETH | $3,000 | +3% |
`;

// Auto-convert if needed
const result = await autoConvertMarkdownTable(userMessage, 'discord');

if (result.converted) {
  await message.send({ attachment: result.image });
} else {
  await message.send({ content: userMessage });
}
```

## Example 5: CLI Usage

```bash
# Create JSON data file
cat > stocks.json << 'EOF'
[
  {"symbol": "AAPL", "price": 150, "change": 2.5},
  {"symbol": "GOOGL", "price": 2800, "change": -1.2}
]
EOF

# Generate table image
node scripts/table-cli.mjs \
  --data-file stocks.json \
  --columns "symbol,price,change" \
  --headers "Symbol,Price,Change" \
  --align "l,r,r" \
  --dark \
  --title "Stock Prices" \
  --output stocks.png
```

## Example 6: Multi-line Text

```typescript
const products = [
  { 
    name: 'Pro Plan', 
    description: 'Full access to all features including premium support and API access',
    price: 99 
  }
];

const image = await renderTable({
  data: products,
  columns: [
    { key: 'name', header: 'Plan', width: 100 },
    { 
      key: 'description', 
      header: 'Features', 
      width: 300,
      wrap: true,
      maxLines: 3
    },
    { 
      key: 'price', 
      header: 'Price', 
      align: 'right',
      formatter: (v) => `$${v}/mo`
    }
  ]
});
```
