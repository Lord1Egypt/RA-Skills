# Google Serper Search

A Claude Code skill that enables web search and image search using Serper API.

## Installation

```bash
npx skills add shuliuzhenhua-sys/google-serper-search
```

## Configuration

Get a free API key from [serper.dev](https://serper.dev) and set it as an environment variable:

```bash
export SERPER_API_KEY="your_api_key"
```

To make it permanent, add it to your shell configuration file:

<thinking>
我需要提供不同 shell 的配置方法。让我列出常见的 shell 配置文件。
</thinking>

- **Zsh**: `echo 'export SERPER_API_KEY="your_api_key"' >> ~/.zshrc && source ~/.zshrc`
- **Bash**: `echo 'export SERPER_API_KEY="your_api_key"' >> ~/.bashrc && source ~/.bashrc`
- **Fish**: `echo 'set -Ux SERPER_API_KEY "your_api_key"' | fish`

## Usage

After installation, simply ask Claude to search for information in your conversation:

**Web Search Examples:**
- "Search for the latest AI news"
- "Find information about Claude Code"
- "What's the current weather in Tokyo?"

**Image Search Examples:**
- "Find pictures of mountains"
- "Search for images of the Eiffel Tower"
- "Show me photos of golden retrievers"

Claude will automatically use this skill when you request web or image searches.

### Advanced Parameters (optional)

The search script supports additional parameters for type, country, language, and time range:

```bash
python3 scripts/serper_search.py "latest AI news" --type news --gl us --hl en --tbs "past week"
```

Supported values:
- `--type`: search, images, videos, places, maps, reviews, news, shopping, lens, scholar, patents, autocomplete
- `--gl`: country code (ISO 3166-1 alpha-2), e.g. `us`, `cn`, `jp`, `gb`
- `--hl`: language code, e.g. `en`, `zh-cn`, `zh-tw`, `ja`, `ko`
- `--tbs`: `past hour`, `past 24 hours`, `past week`, `past month`, `past year`

## How It Works

When you ask Claude to search, it will:
1. Detect your search request
2. Call the Serper API via the included script
3. Parse and format the results
4. Present the information in a clear, organized way

## What You Get

**Web Search Results:**
- Knowledge graph with key facts
- Organic search results with links
- Related questions (People Also Ask)
- Related search suggestions

**Image Search Results:**
- Image URLs and thumbnails
- Image dimensions
- Source information

## License

MIT
