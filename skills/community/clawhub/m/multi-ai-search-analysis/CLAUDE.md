# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-AI Search Analysis - A Python-based tool that queries multiple AI platforms (DeepSeek, Qwen, 豆包，Kimi, Gemini) in parallel to generate comparative analysis reports.

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt
playwright install msedge

# Login to AI platforms (first time setup)
python scripts/login.py

# Run analysis (parallel mode, recommended)
python scripts/run.py -t "分析主题" -d 维度 1 维度 2

# Run with specific platforms
python scripts/run.py -t "主题" -p DeepSeek Qwen Kimi

# Run in serial mode (for captcha scenarios)
python scripts/run.py -t "主题" --mode serial
```

## Architecture

### Core Components

- **scripts/run.py** - Main entry point with `MultiAISearch` class
  - Browser automation via Playwright async API
  - Parallel/serial execution modes
  - Login detection, session management, retry logic

- **scripts/reporter.py** - Report generation with `ReportGenerator` class
  - 4 templates: general, comparison, trend, evaluation
  - Markdown output with structured sections

- **scripts/login.py** - Login utility to authenticate all platforms

- **config/ai-platforms.json** - Platform configuration
  - URLs, selectors, timeouts, features per AI
  - Browser settings, output paths, retry config

### Execution Flow (Parallel Mode)

```
1. Initialize browser with persistent context (saves login state)
2. Open tabs for all selected platforms simultaneously
3. Check login status → prompt user if needed
4. Send identical question to all platforms
5. Wait for responses with progress tracking (tqdm)
6. Extract content using selector chains with fallbacks
7. Generate markdown report via reporter.py
```

### Key Patterns

- **Selector fallback chains**: Each platform has primary + fallback CSS selectors for robustness
- **Session management**: Auto-detects and creates new chat sessions to avoid context pollution
- **Retry logic**: 3 retries for sending, exponential backoff
- **Progress tracking**: tqdm for parallel, ASCII animation for serial

## Configuration

### Adding a new AI platform

Edit `config/ai-platforms.json`:
```json
{
  "name": "NewAI",
  "url": "https://...",
  "loginMethod": "email",
  "selectors": {
    "input": "textarea[placeholder*='输入']",
    "send": "button[aria-label*='发送']",
    "response": "article, div[class*='response']"
  }
}
```

### Response time tuning

Adjust `timeout` and `avgResponseTime` per platform in config.

## Output

Reports saved to `reports/{topic}-{timestamp}.md` with structure:
- Core summary
- Dimension-based analysis
- Data comparison tables
- AI platform特色 comparison

## Dependencies

- playwright (async browser automation)
- tqdm (progress bars)
- colorama (colored output)
- json5 (config parsing)
