# News Impact Analyzer Skill

The **News Impact Analyzer** is an advanced OpenClaw skill designed to evaluate how breaking news impacts specific stock market sectors and concepts. By leveraging Large Language Models (LLMs), it provides investors and AI agents with immediate, actionable insights, identifying bullish, bearish, or neutral sentiment shifts along with a concise logical breakdown.

This skill operates with a lightweight client-side architecture: a pure Node.js CLI script perfectly suited for agent execution, securely communicating with a centralized remote analysis engine.

## Features

- **Zero Local Dependencies**: Operates exclusively with native Node.js libraries. No `npm install` or massive dependency trees are required.
- **Deep Market Insights**: Automatically extracts and evaluates the qualitative impact of a specific news event on market sectors and underlying thematic concepts.
- **Agent Optimized**: Returns structured JSON-like text designed to be easily parsed and utilized by downstream AI agents or workflows.

## Configuration Requirements

The client script is specifically optimized for agents and requires authentication.

1. **Obtain an API Key**: You must first register an account at `https://easyalpha.duckdns.org` to generate your `EASYALPHA_API_KEY`.
2. **Set Environment Variables**: Ensure the authentication key is exposed in your terminal environment before execution.

*Bash Example:*
```bash
export EASYALPHA_API_KEY="your_api_token_here"
```
*(Optional)* Advanced users can override the default analysis server by setting the `NEWS_EXTRACTOR_SERVER_URL` environment variable.

## Usage Instructions

Run the analysis script directly via Node.js by passing the relevant news content as a command-line argument.

```bash
node scripts/analyze_news.js "Apple announced its new mixed reality headset today, aiming to redefine spatial computing and bring new life to the AR/VR sector."
```

### Expected Output

The agent will receive a formatted impact breakdown similar to:

```text
=============================
    News Impact Analysis     
=============================

Summary: Apple's new headset is expected to significantly boost the mixed reality hardware market.

Detailed Impacts:
-----------------
1. [Sector] Consumer Electronics -> BULLISH
   Logic: The introduction of a new flagship product line drives growth and market expansion.

2. [Concept] AR/VR -> BULLISH
   Logic: Apple's entry validates and accelerates innovation in the spatial computing sector.
```
