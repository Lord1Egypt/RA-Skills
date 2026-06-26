# MiniMax Coding Plan Tool

> Based on [yorch233/minimax-coding-plan-tool](https://clawhub.ai/yorch233/minimax-coding-plan-tool) by [@yorch233](https://github.com/yorch233)  
> This fork patches the API endpoint to use `api.minimax.io` for compatibility with standard Coding Plan keys (`sk-cp-*`).

Real-time web search and image understanding using MiniMax Coding Plan API.

## Setup

1. Install:
   ```bash
   clawhub install minimax-coding-plan-tool
   ```

2. Configure API key:
   ```bash
   openclaw config set skills.entries.minimax-coding-plan-tool.env.MINIMAX_API_KEY "sk-cp-xxx"
   ```

   Or in `openclaw.json`:
   ```json
   "skills": {
     "entries": {
       "minimax-coding-plan-tool": {
         "env": { "MINIMAX_API_KEY": "sk-cp-xxx" }
       }
     }
   }
   ```

3. Get your Coding Plan API key at: https://platform.minimaxi.com

## Usage

### Web Search

```bash
MINIMAX_API_KEY="sk-cp-xxx" node scripts/minimax_coding_plan_tool.js web_search "OpenAI latest news"
```

Returns structured results with title, URL, snippet, and date.

### Image Understanding

```bash
# From URL
MINIMAX_API_KEY="sk-cp-xxx" node scripts/minimax_coding_plan_tool.js understand_image "https://example.com/photo.jpg" "Describe this image"

# From local file
MINIMAX_API_KEY="sk-cp-xxx" node scripts/minimax_coding_plan_tool.js understand_image ./photo.png "What objects are visible?"
```

## License

MIT (same as original by @yorch233)
