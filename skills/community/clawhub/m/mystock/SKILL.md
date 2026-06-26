***

name: my-stock
description: MyStock - 我的股票智能助手。Use when user asks about stock quotes, market analysis, limit-up tracking, shareholder dynamics, investment research, or portfolio management. Handles real-time prices, technical analysis, and financial data queries.
metadata:
version: 1.1.6
author: wangz
license: MIT
category: finance
-----------------

# MyStock - 我的股票智能助手

🎨 MyStock is a **full-featured stock analysis assistant** with a **beautiful Web UI**, providing real-time quotes, limit-up tracking, shareholder dynamics monitoring, and more!

!\[MyStock Demo]\(assets/mystock-demo.png null)

## ✨ Capabilities

1. **Real-time Quotes** - Query stock prices and percentage changes
2. **Limit-up Analysis** - Track daily limit-up boards and first-board opportunities
3. **Shareholder Dynamics** - Monitor shareholder increases, buybacks, and executive transactions
4. **Portfolio Management** - Manage watchlists and investment notes
5. **AI Assistant** - Get AI-powered investment insights
6. **🎨 Beautiful Web UI** - Modern Vue 3 + Element Plus interface

## 🎨 Web UI Features

The skill includes a complete **web interface** that users can interact with:

- **Watchlist Management** - Add/remove stocks with one click
- **Real-time Data Display** - Live price updates with color-coded changes
- **Limit-up Analysis** - Visual tracking of daily limit-up stocks
- **Shareholder Activity** - Detailed tabs for different activity types
- **AI Chat Assistant** - Built-in AI assistant for stock questions
- **Responsive Design** - Works on desktop and mobile

## When to Use

Invoke this skill when the user:

- Asks about stock prices, quotes, or market data
- Mentions specific stock codes or names
- Asks about limit-up (涨停) stocks or trading opportunities
- Needs shareholder/investor activity information
- Wants to track investment portfolio
- Asks for stock analysis or research
- Wants to see a **visual interface** for stock analysis
- Mentions terms like: 打板, 涨停, 股东增持, 回购, 高管增持

## Architecture

```
./
├── start.sh           # ⭐ One-click startup (UI + Backend)
├── backend/           # FastAPI backend server
│   ├── main.py       # Main API server
│   ├── ai_service.py # AI service integration
│   └── requirements.txt
├── frontend/         # Web interface
│   └── index.html    # Vue 3 single-page app ⭐
├── scripts/          # Helper scripts
│   ├── install.sh    # One-click installation script
│   ├── check_api.py  # API health check
│   └── test_skill.py # Skill trigger test
└── references/       # Documentation
    └── usage_examples.md
```

## Quick Start

### 1. One-Click Installation (Recommended)

```bash
bash scripts/install.sh
```

This will automatically:

- ✅ Install Node.js dependencies (jsdom for pywencai)
- ✅ Install Python dependencies
- ✅ Configure environment variables
- ✅ Prepare data directories

### 2. ⚡ Start Everything (Recommended)

```bash
./start.sh
```

This one script starts:

- ✅ Backend API server (port 8000)
- ✅ Frontend web interface (port 5000)
- ✅ Automatically opens browser with UI

**Or start separately:**

### 3. Start Backend Server

```bash
cd backend
pip install -r requirements.txt
./start.sh
```

The backend server runs on `http://localhost:8000`

**Important**: The `start.sh` script automatically sets `NODE_PATH` for pywencai jsdom dependency.

### 4. Start Frontend UI

```bash
cd frontend
python -m http.server 5000
```

Access the web interface at `http://localhost:5001`

**The UI will open automatically when using** **`./start.sh`**

### ⚠️ Important Dependencies

#### Node.js (Required for pywencai)

pywencai uses jsdom for web scraping, which requires Node.js:

```bash
# Install Node.js (if not installed)
# Download from: https://nodejs.org/

# Install jsdom globally
npm install -g jsdom

# Verify installation
node -e "require('jsdom')"
```

The startup script automatically sets `NODE_PATH` to find jsdom.

### 4. API Endpoints

| Endpoint                    | Method   | Description                 |
| --------------------------- | -------- | --------------------------- |
| `/api/stocks`               | GET      | Get stock quotes            |
| `/api/limit-up-analysis`    | GET      | Get limit-up board analysis |
| `/api/shareholder-activity` | GET      | Get shareholder dynamics    |
| `/api/portfolio`            | GET/POST | Manage portfolio            |
| `/api/chat`                 | POST     | AI chat assistant           |

## Usage Examples

### Example 1: Query Stock Price

User says: "查询贵州茅台的股价"

The assistant should:

1. Call API: `GET /api/stocks?code=600519.SH`
2. Return formatted response with price, change %, etc.

### Example 2: Limit-up Analysis

User says: "查看今天的打板分析"

The assistant should:

1. Call API: `GET /api/limit-up-analysis`
2. Analyze and present limit-up candidates
3. Highlight first-board opportunities

### Example 3: Shareholder Dynamics

User says: "最近有哪些股东增持"

The assistant should:

1. Call API: `GET /api/shareholder-activity`
2. Present shareholder increase data
3. Include buyback and executive transaction info

## Data Sources

- Real-time quotes: Via `pywencai` library (同花顺问财)
- Shareholder data: Via `pywencai` queries
- Historical data: Stored in local JSON files

## Important Notes

### Investment Disclaimer

⚠️ **DISCLAIMER**: This tool is for educational and research purposes only. All investment decisions should be made at your own risk. Past performance does not guarantee future results.

### Rate Limiting

- API calls should be throttled to avoid overwhelming the data source
- Cache frequently accessed data locally
- Maximum 1 request per second recommended

### Data Accuracy

- Real-time data may have slight delays
- Historical data is cached locally
- Verify critical information through official sources

## Troubleshooting

### API Server Won't Start

1. Check if port 8000 is in use:
   ```bash
   lsof -i:8000
   ```
2. Verify Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys if needed
   ```

### Data Not Loading

1. Verify API server is running:
   ```bash
   curl http://localhost:8000/
   ```
2. Check network connectivity
3. Review server logs for errors

### Frontend Not Displaying

1. Ensure backend API is accessible
2. Check browser console for errors
3. Verify CORS settings in backend

## Development

### Project Structure

```
./
├── backend/
│   ├── main.py          # FastAPI application
│   ├── ai_service.py    # AI integration
│   ├── ai_config.py     # AI configuration
│   ├── sync_all_stocks.py # Stock data sync
│   └── requirements.txt  # Python dependencies
├── frontend/
│   └── index.html       # Single-file Vue 3 app
├── scripts/
│   ├── install.sh       # One-click installation script
│   ├── check_api.py     # API health check
│   └── test_skill.py    # Skill trigger test
├── references/
│   └── usage_examples.md # Detailed usage examples
└── README.md            # Project documentation
```

### Adding New Features

1. Backend changes: Add new endpoints in `main.py`
2. Frontend changes: Edit `frontend/index.html`
3. Test thoroughly before committing

## Integration with Claude Code

This skill can be used alongside Claude Code for:

- Automated stock research
- Portfolio analysis workflows
- Investment strategy discussions
- Market trend analysis

When Claude Code detects stock-related queries, it can:

1. Invoke this skill automatically
2. Use backend APIs for data
3. Provide AI-powered insights
4. Generate analysis reports

## License

MIT License - See LICENSE file for details

## Support

For issues or feature requests, please open an issue on the GitHub repository.
