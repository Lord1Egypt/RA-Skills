# News Content Extractor Skill

This is a high-performance news content extraction tool specifically built for [OpenClaw](https://openclaw.ai). It accurately identifies news titles, authors, publication dates, and body content while filtering out advertisements and irrelevant sidebars.

## 🌟 Features

- **Fast Installation**: The client is based on Node.js, requiring no Python dependencies—plug and play.
- **High Accuracy**: The core parsing logic is driven by the cloud-based `trafilatura` engine, optimized specifically for news.
- **Privacy Protection**: Remote parsing is performed using only an API Key.

## 🚀 Installation Steps

1. **Install from ClawHub**:
   Run the following command in your OpenClaw project directory:
   ```bash
   npx clawhub@latest install news-content-extractor
   ```

2. **Configure Environment Variables**:
   To use this Skill, you need to set up an API Key. Add the following items to your `.env` file or system environment variables:
   ```bash
   # Your authentication token, obtainable from: https://easyalpha.duckdns.org
   EASYALPHA_API_KEY=YOUR_API_KEY
   
   # Backend URL (Optional, uses the default address otherwise)
   NEWS_EXTRACTOR_SERVER_URL=https://easyalpha.duckdns.org/api/v1/extract
   ```

## 📝 Usage

Once installed and configured, you can send news URLs directly in the chat:

**User**: "Extract the content of this news: https://www.bbc.com/news/world-67890"

**Agent**: (Automatically calls this Skill and returns results like below)
> **Title**: xxxx  
> **Date**: 2024-xx-xx  
> **Body**: ......

---

## 🛠️ Technical Support
If you encounter any issues during installation or usage, please contact [ClawHub.ai](https://clawhub.ai) or check the project homepage for troubleshooting.
