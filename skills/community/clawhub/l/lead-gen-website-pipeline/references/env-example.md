# Environment Variables Reference

Copy this to your project's `.env` file and fill in your keys.

```bash
# Google (required)
GOOGLE_PLACES_API_KEY=your_places_api_key
GOOGLE_API_KEY=your_gemini_api_key
GOOGLE_SHEET_ID=your_google_sheet_id

# AI Models (at least one required)
ANTHROPIC_API_KEY=your_anthropic_key        # Claude for spec generation
OPENAI_API_KEY=your_openai_key              # GPT for HTML building
CLAUDE_BIN=/path/to/claude                  # Claude Code CLI (Max plan, optional)

# Deployment (required)
VERCEL_TOKEN=your_vercel_token
VERCEL_PROJECT_NAME=ai-website-specs        # Optional, defaults to ai-website-specs

# Outreach (required for email automation)
AGENTMAIL_API_KEY=your_agentmail_key
AGENTMAIL_INBOX=your-name@agentmail.to

# Branding
FORM_EMAIL=demo@yourdomain.com              # Contact form submissions go here
BRAND_DOMAIN=YourDomain.com                 # Footer attribution

# Optional
OLLAMA_BASE_URL=http://127.0.0.1:11434     # Local model fallback
OLLAMA_MODEL=qwen2.5-coder:3b
TZ=America/Chicago
```
