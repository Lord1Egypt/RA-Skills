# API Sources for Gold Prices

## Official Sources

### 1. Antam (Logam Mulia)
- **URL:** https://www.logammulia.com/id/harga-emas-hari-ini
- **Update:** Daily, 09:00 WIB
- **Data:** Buy, Sell, Buyback prices
- **Method:** Web scraping (no public API)

### 2. Hartadinata
- **URL:** https://harga-emas.org/
- **Update:** Real-time
- **Data:** Multiple sizes (0.1g - 1000g)
- **Method:** Web scraping

### 3. UBS
- **URL:** https://harga-emas.org/ubs
- **Update:** Daily
- **Data:** Buy, Sell, Buyback
- **Method:** Web scraping

### 4. Pegadaian (Galeri 24)
- **URL:** https://www.pegadaian.co.id/harga-emas
- **Update:** Daily
- **Data:** Antam, UBS, Retro
- **Method:** Web scraping

## Alternative Sources

### API (Paid)
- **GoldAPI.io** - Real-time gold prices
- **Metals-API.com** - Precious metals API
- **CurrencyLayer** - Currency + metals

### Scraping Strategy
1. Primary: Antam official site
2. Backup: harga-emas.org
3. Fallback: Pegadaian

## Rate Limiting
- Respect robots.txt
- Cache results (30 min)
- Use exponential backoff on failure

## Data Format
```json
{
  "brand": "antam",
  "buyPrice": 2950000,
  "sellPrice": 2850000,
  "buybackPrice": 2669000,
  "unit": "gram",
  "lastUpdate": "2026-03-27T09:00:00+07:00"
}
```
