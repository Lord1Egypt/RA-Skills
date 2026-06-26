# GOG Weekly Sales Analytics Workflow

Automated workflow that:
1. Scrapes weekly discounted game data from GOG store
2. Analyzes deals using Google Gemini to find best value offers
3. Generates markdown report with insights and recommendations
4. Syncs report to shared Feishu Drive folder for team access
5. Publishes the workflow as a reusable skill on ClawHub

## Usage
```
cp .env.example .env
# Fill in API keys in .env
pip install -r requirements.txt
python main.py
```

## Skills Used
- web-scraper: GOG store data extraction
- gemini: AI-powered sales analysis and report generation
- feishu-drive: Cloud storage sync and permission management
- gog: Game metadata and platform integration
- clawhub: Skill publishing and distribution
