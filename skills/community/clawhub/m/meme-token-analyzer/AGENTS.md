# Meme Token Analyzer Workflow

## Project Overview
- **Name**: Meme_Token_Analyzer
- **Function**: Analyze Meme Token sentiment, generate "Moonshot" prediction image, and output wealth gene detection report

## Node Inventory

| Node Name | File Location | Type | Description | Branch Logic | Config File |
|-------|---------|------|---------|---------|---------|
| search | `nodes/search_node.py` | task | Search token news and social media sentiment | - | - |
| image_gen | `nodes/image_gen_node.py` | task | Generate token moonshot prediction image | - | - |
| clean_data | `nodes/clean_data_node.py` | task | Clean search results into summary text | - | - |
| analysis | `nodes/analysis_node.py` | agent | Multimodal wealth gene detection analysis | - | `config/analysis_llm_cfg.json` |

**Type Legend**: task (task node) / agent (LLM) / condition (conditional branch) / looparray (list loop) / loopcond (conditional loop)

## Subgraph Inventory
No subgraphs

## Features ✨

- **🔍 Web Search**: Searches latest news, social media sentiment, and market trends with **time range filter (1 month)** for fresh data
- **🎨 Image Generation**: Creates "Moonshot" prediction images for tokens
- **🧹 Data Cleaning**: Condenses search results into LLM-friendly summaries with **date freshness validation**
- **🤖 AI Analysis**: Multimodal analysis combining sentiment data and visual elements
- **💎 Wealth Gene Rating**: Four-tier rating system (Diamond Hand, Moonshot, Paper Hand, Shitcoin)
- **🧠 Smart Detection**: Automatically detects major coins (BTC/ETH/SOL), handles missing data, and identifies irrelevant search results with appropriate warnings
- **📅 Data Freshness Check**: Validates search result dates and warns if data is outdated

## Skills Used
- Node `search` uses skill `web-search` for web search
- Node `image_gen` uses skill `image-generation` for image generation
- Node `analysis` uses skill `llm` for multimodal analysis (doubao-seed-1-6-vision-250815)

## Workflow Structure
```
START
  ├── search (Web Search) ──> clean_data (Data Cleaning) ──┐
  └── image_gen (Image Generation) ────────────────────────┤
                                                            ├─> analysis (Wealth Gene Detection) ──> END
```

## Input/Output
- **Input**: token_name (String) - Token name, e.g., "PEPE", "SHIB", "Dogecoin"
- **Output**: 
  - analysis_report (String) - Humorous and professional wealth gene detection report
  - generated_image_url (String) - Generated prediction image URL

## Analysis Framework
Report contains four dimensions:
1. 🎯 **Narrative Magic Analysis** - Whether name and concept are memorable
2. 📢 **Community Hype Ability Prediction** - Community activity and shilling intensity
3. 🎨 **Visual Gene Detection** - Meme image's viral potential
4. 🏆 **Wealth Gene Rating** - Final verdict
   - 🌟 Diamond Hand - 10000x potential
   - 🌙 Moonshot - 100x expected
   - 🗑️ Paper Hand - Likely a rug
   - 💩 Shitcoin - Stay away

## Intelligent Detection Rules

The workflow includes smart detection logic:

1. **Major Cryptocurrency Detection**: When analyzing BTC, ETH, SOL, etc., the report will humorously warn: "⚠️ Detected non-typical Meme, now performing cross-border scan with [Top Value Coin] perspective."

2. **No Data Handling**: If sentiment_data is empty or shows no results, the system will NOT fabricate prices, instead stating: "This token is so mysterious that even the shilling army online hasn't discovered it yet."

3. **Irrelevant News Detection**: If search results contain irrelevant information (e.g., AI Token consumption metrics), the report will add: "Note: Due to this token being too obscure on-chain, this report is primarily based on narrative potential and visual gene simulation analysis."
