# Finance & Accounting

## Capabilities
- Financial data analysis and reporting
- Budget tracking and expense categorization
- Invoice generation and management
- Stock/crypto price checking
- Currency conversion
- Financial calculations (compound interest, amortization, etc.)

## Tools
- **Python**: pandas for analysis, matplotlib for charts
- **APIs**: Yahoo Finance (yfinance), CoinGecko, exchangerate APIs
- **Spreadsheets**: Google Sheets via `gog`, Excel via openpyxl
- **Web search**: Real-time financial data lookup

## Common Tasks

### Budget Analysis
1. Import transactions (CSV, API, manual)
2. Categorize expenses
3. Calculate totals by category/month
4. Visualize with charts
5. Identify trends and anomalies

### Stock Analysis
```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")
info = ticker.info
```

### Currency Conversion
- Use web search for live rates
- Or API: `https://api.exchangerate-api.com/v1/latest/USD`

### Invoice Generation
- Create HTML/PDF invoices with templates
- Track payment status
- Calculate taxes and totals

## Financial Formulas
- Compound Interest: A = P(1 + r/n)^(nt)
- ROI: (Gain - Cost) / Cost × 100
- CAGR: (Ending/Beginning)^(1/n) - 1
- Monthly Payment: P * [r(1+r)^n] / [(1+r)^n - 1]

## Data Sources
- Google Finance, Yahoo Finance
- CoinGecko, CoinMarketCap
- Bank CSV exports
- Google Sheets financial tracking
