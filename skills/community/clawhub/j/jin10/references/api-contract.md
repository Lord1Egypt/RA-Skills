# Jin10 API Contract

This skill uses the Jin10 MCP endpoint internally: `https://mcp.jin10.com/mcp`.

Do not send raw MCP protocol messages from the conversation. Use the bundled script in `scripts/jin10.py`.

## Command Map

### Quotes

```bash
python3 scripts/jin10.py --format json codes
python3 scripts/jin10.py --format json quote XAUUSD
python3 scripts/jin10.py --format text quote XAUUSD
python3 scripts/jin10.py --format json kline XAUUSD --time 1h --count 20
python3 scripts/jin10.py --format text kline XAUUSD --time 1d --count 5
```

Common symbols:
- `XAUUSD`: 现货黄金
- `XAGUSD`: 现货白银
- `USOIL`: WTI 原油
- `UKOIL`: 布伦特原油
- `COPPER`: 现货铜
- `USDJPY`: 美元/日元
- `EURUSD`: 欧元/美元
- `USDCNH`: 美元/人民币

### Flash

```bash
python3 scripts/jin10.py --format json flash list
python3 scripts/jin10.py --format json flash list --cursor "<next_cursor>"
python3 scripts/jin10.py --format json flash search "美联储"
```

### News

```bash
python3 scripts/jin10.py --format json news list
python3 scripts/jin10.py --format json news list --cursor "<next_cursor>"
python3 scripts/jin10.py --format json news search "原油"
python3 scripts/jin10.py --format json news search "非农" --cursor "<next_cursor>"
python3 scripts/jin10.py --format json news get 123456
```

### Calendar

```bash
python3 scripts/jin10.py --format json calendar
python3 scripts/jin10.py --format json calendar --keyword "非农"
python3 scripts/jin10.py --format json calendar --high-importance
python3 scripts/jin10.py --format text calendar --high-importance
```

## Output Contract

- `quote`:
  - `data.code`
  - `data.name`
  - `data.time`
  - `data.open`
  - `data.close`
  - `data.high`
  - `data.low`
  - `data.volume`
  - `data.ups_price`
  - `data.ups_percent`
- `kline`:
  - `data.code`
  - `data.name`
  - `data.klines[]`
  - `data.klines[].time`
  - `data.klines[].open`
  - `data.klines[].high`
  - `data.klines[].low`
  - `data.klines[].close`
  - `data.klines[].volume`
- `flash list/search`:
  - `data.items`
  - `data.next_cursor`
  - `data.has_more`
- `news list/search`:
  - `data.items`
  - `data.next_cursor`
  - `data.has_more`
- `news get`:
  - `data.id`
  - `data.title`
  - `data.introduction`
  - `data.time`
  - `data.url`
  - `data.content`
- `calendar`:
  - `data[]`
  - `pub_time`
  - `star`
  - `title`
  - `previous`
  - `consensus`
  - `actual`
  - `revised`
  - `affect_txt`

## Query Selection Rules

1. Quote or K-line request:
   - If the symbol is ambiguous, call `codes` first.
   - Then call `quote <CODE>` or `kline <CODE> [--time ...] [--count ...]`.
2. Latest flash by topic:
   - Use `flash search <keyword>`.
   - For chronological browsing, use `flash list` and paginate with `--cursor`.
3. News or long-form article:
   - Use `news search <keyword>` or `news list`.
   - Fetch details with `news get <id>`.
4. Calendar:
   - Use `calendar`.
   - Use `--high-importance` for major events only.
