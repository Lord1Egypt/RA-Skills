#!/bin/bash
# LeafEngines MCP Server installation script
# For OpenClaw skill installation

set -e

echo "🌱 Installing LeafEngines MCP Server skill..."

# Check for required tools
if ! command -v curl &> /dev/null; then
    echo "❌ curl is required but not installed"
    exit 1
fi

# Create configuration directory
CONFIG_DIR="$HOME/.openclaw/config"
mkdir -p "$CONFIG_DIR"

# Check if OpenClaw config exists
if [ ! -f "$CONFIG_DIR/config.yaml" ] && [ ! -f "$CONFIG_DIR/config.yml" ]; then
    echo "⚠️  OpenClaw config not found. Creating basic config..."
    cat > "$CONFIG_DIR/config.yaml" << EOF
# OpenClaw Configuration
# LeafEngines MCP Server added $(date)

mcpServers:
  leafengines:
    url: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server
    headers:
      x-api-key: YOUR_API_KEY_HERE
    description: Agricultural Intelligence API for soil analysis, weather forecasting, and crop recommendations

# Add your API key after getting it from:
# https://github.com/QWarranto/leafengines-claude-mcp/issues/new?template=get-api-key.md
EOF
    echo "✅ Created OpenClaw config at $CONFIG_DIR/config.yaml"
else
    echo "✅ OpenClaw config found"
fi

# Create API key instructions
cat > "API_KEY_INSTRUCTIONS.md" << 'EOF'
# 🌱 LeafEngines API Key Setup

## Get Your API Key

1. **Visit GitHub:** https://github.com/QWarranto/leafengines-claude-mcp
2. **Click "New Issue"**
3. **Select "🌱 Get Agricultural Intelligence API" template**
4. **Fill out the form** with your email and use case
5. **Submit** - You'll receive an API key via email

## Configure OpenClaw

Edit your OpenClaw config (`~/.openclaw/config/config.yaml`):

```yaml
mcpServers:
  leafengines:
    url: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server
    headers:
      x-api-key: YOUR_ACTUAL_API_KEY_HERE  # ← Replace with your key
```

## Configure Claude Desktop

1. Open Claude Desktop
2. Go to Settings → Developer → MCP Servers
3. Add new server:
   - URL: `https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server`
   - Headers: `x-api-key: YOUR_ACTUAL_API_KEY_HERE`

## Test Your Setup

```bash
# Test API key
curl -H "x-api-key: YOUR_API_KEY" \
  https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/api/health
```

## Support
- GitHub Issues: https://github.com/QWarranto/leafengines-claude-mcp/issues
- Discord: #mcp channel in Claude Discord
EOF

echo "✅ Created API key instructions: API_KEY_INSTRUCTIONS.md"

# Test connection to API
echo "🔧 Testing connection to LeafEngines API..."
if curl -s -o /dev/null -w "%{http_code}" "https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/api/health" | grep -q "200"; then
    echo "✅ LeafEngines API is reachable"
else
    echo "⚠️  Could not reach LeafEngines API (may require API key)"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get your API key from GitHub:"
echo "   https://github.com/QWarranto/leafengines-claude-mcp/issues/new?template=get-api-key.md"
echo "2. Configure OpenClaw with your API key"
echo "3. Restart OpenClaw to load the MCP server"
echo ""
echo "📚 Full instructions in: API_KEY_INSTRUCTIONS.md"
echo "🌐 Website: https://github.com/QWarranto/leafengines-claude-mcp"