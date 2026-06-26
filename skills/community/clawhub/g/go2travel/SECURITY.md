# Security Documentation

## External Dependencies

### flyai CLI

- **Package**: `@fly-ai/flyai-cli` (npm)
- **Source**: https://github.com/alibaba-flyai/flyai-skill
- **Install**: `npm i -g @fly-ai/flyai-cli`
- **Purpose**: Command-line interface to Fliggy (飞猪) MCP for real-time travel data
- **Permissions**: Reads local flyai config for API access; makes HTTPS requests to Fliggy API
- **No local secret access**: flyai CLI does not access filesystem beyond its own config directory
- **No network secrets**: All API calls use pre-configured tokens; skill does not handle credentials

### What flyai commands do

| Command | Network | Local Access |
|---------|---------|-------------|
| `flyai keyword-search` | HTTPS to Fliggy API | None |
| `flyai search-flight` | HTTPS to Fliggy API | None |
| `flyai search-hotel` | HTTPS to Fliggy API | None |
| `flyai search-poi` | HTTPS to Fliggy API | None |

### Security Boundaries

- This skill only invokes flyai CLI with user-provided search queries
- No credentials, tokens, or secrets are embedded in the skill
- All data returned by flyai is public travel information (prices, images, booking links)
- The skill does not modify any local files or system configuration
