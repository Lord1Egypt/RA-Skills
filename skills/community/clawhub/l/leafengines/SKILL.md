---
name: leafengines
version: 1.2.0
description: LeafEngines - Agricultural Intelligence with Free Tier & Founder Pricing. 1,092+ downloads. 3 tools for soil analysis, crop recommendations, and TurboQuant capabilities. Free tier available with x-free-tier header.
homepage: https://app.soilsidekickpro.com/mcp
source: https://github.com/QWarranto/leafengines-claude-mcp
metadata: {"openclaw":{"emoji":"🌱","os":["darwin","linux"],"requires":{"bins":[]},"install":[{"id":"claude-desktop","kind":"manual","steps":["1. Open Claude Desktop settings","2. Navigate to Developer → MCP Servers","3. Add new server with URL: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server","4. Add header: x-free-tier: true (FREE) OR x-api-key: YOUR_PAID_KEY (Paid)"],"label":"Configure in Claude Desktop"},{"id":"openclaw-mcp","kind":"manual","steps":["1. Choose FREE tier (x-free-tier: true) or PAID tier (get API key from Stripe checkout)","2. Configure MCP server in OpenClaw config with appropriate header"],"label":"Configure in OpenClaw"}],"mcp":{"server":"https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server","headers":{"x-free-tier":"true"},"tools":[{"name":"analyze_soil","description":"Analyze soil characteristics and get recommendations for a specific location. Requires county_fips parameter (5-digit code).","inputSchema":{"type":"object","properties":{"county_fips":{"type":"string","description":"5-digit county FIPS code (e.g., '13067' for Fulton County, GA)"},"api_key":{"type":"string","description":"Optional API key for paid features (use x-api-key header instead)"}},"required":["county_fips"]}},{"name":"recommend_crop","description":"Get crop recommendations based on soil analysis.","inputSchema":{"type":"object","properties":{"county_fips":{"type":"string","description":"5-digit county FIPS code"},"api_key":{"type":"string","description":"Optional API key for paid features"}},"required":["county_fips"]}},{"name":"check_turboquant","description":"Check if TurboQuant capabilities are available for a location (FREE). No authentication required.","inputSchema":{"type":"object","properties":{"county_fips":{"type":"string","description":"5-digit county FIPS code"}},"required":["county_fips"]}}]}}}
---

# LeafEngines MCP Server v1.2.0

**Agricultural Intelligence with Free Tier & Founder Pricing** for Claude and OpenClaw. **1,092+ downloads** since March 29. Free tier available with `x-free-tier: true` header.

## Features

**Why 1,092+ Developers Choose Us:**
- ✅ **Free tier available** - No API key required for testing
- ✅ **Founder pricing** - $10→$49/month lifetime lock (first 100 customers)
- ✅ **Simple integration** - 3 focused tools with clear parameters
- ✅ **Proven adoption** - 1,092 organic downloads
- ✅ **Active development** - Regular updates and improvements

**3 Agricultural Intelligence Tools:**
1. **Analyze Soil** - Soil characteristics and recommendations (requires `county_fips`)
2. **Recommend Crop** - Crop suggestions based on soil analysis
3. **Check TurboQuant** - Verify optimization capabilities (FREE, no auth)

## Pricing Tiers

### Free Tier (No Payment Required)
- **Header:** `x-free-tier: true`
- **Tools:** `check_turboquant` (always free), limited `analyze_soil`
- **Rate Limit:** Reasonable usage for testing and evaluation
- **No API Key Needed** - Start immediately

### Founder Pricing (First 100 Customers - Lifetime Lock)
**Limited time offer:** First 100 customers get lifetime pricing locked at intro rates.

**Starter Plan:**
- **Intro:** $10/month → **Lifetime:** $49/month (normally $149)
- **Checkout:** https://buy.stripe.com/14A7sL30y8bR2F4fbgaMU02

**Pro Plan:**
- **Intro:** $49/month → **Lifetime:** $149/month (normally $499)
- **Checkout:** https://buy.stripe.com/cNi3cv1WuajZcfE7IOaMU03

**After 100 customers or 30 days:** Prices return to normal ($149/$499)

### Normal Pricing (After Founder Period)
- **Starter:** $149/month
- **Pro:** $499/month
- **Enterprise:** $1,999/month (custom volume)

## Quick Start

### Option A: Free Tier (Start Immediately)
**No API key required** - Use `x-free-tier: true` header

1. **Configure Claude Desktop:**
   - Open Claude Desktop settings
   - Navigate to Developer → MCP Servers
   - Add new server:
     - URL: `https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server`
     - Headers: `x-free-tier: true`

2. **Configure OpenClaw:**
```yaml
mcpServers:
  leafengines:
    url: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server
    headers:
      x-free-tier: true
```

### Option B: Paid Tier (Full Access)
**Get Founder pricing** - First 100 customers get lifetime lock

1. **Get API Key:**
   - **Starter:** https://buy.stripe.com/14A7sL30y8bR2F4fbgaMU02 ($10→$49/month lifetime)
   - **Pro:** https://buy.stripe.com/cNi3cv1WuajZcfE7IOaMU03 ($49→$149/month lifetime)

2. **Configure Claude Desktop:**
   - Same URL as above
   - Headers: `x-api-key: YOUR_PAID_API_KEY_HERE`

3. **Configure OpenClaw:**
```yaml
mcpServers:
  leafengines:
    url: https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server
    headers:
      x-api-key: YOUR_PAID_API_KEY_HERE
```

**Join 1,092+ developers** using agricultural intelligence tools.

## Use Cases

### For Farmers & Agriculturists
- **Crop planning** based on soil and climate
- **Irrigation optimization** using weather forecasts
- **Pest management** with detection tools
- **Yield prediction** for harvest planning

### For Researchers & Students
- **Environmental analysis** for studies
- **Climate impact assessment**
- **Agricultural data** for research projects
- **Sustainability scoring**

### For Developers & AI Agents
- **Agricultural intelligence** in applications
- **Environmental data** for AI models
- **Real-time weather** and soil data
- **Integration** with farming IoT systems
- **TurboQuant optimization** testing and deployment

### For TurboQuant Users
- **Test optimization** on your hardware
- **Verify performance** improvements (6x memory, 8x speed)
- **Check compatibility** for Gemma 7B on 4GB devices
- **Optimize deployment** for edge/offline scenarios

## Security & Privacy

### Data Handling & Security
- **SSL/TLS Encryption:** All API calls use HTTPS with valid SSL certificates from Supabase
- **Endpoint Security:** `https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server`
- **Data Retention:** API request logs retained for 30 days for usage monitoring and abuse prevention
- **No Personal Data Collection:** API does not collect or store personal information beyond necessary request data
- **Supabase Infrastructure:** Enterprise-grade cloud platform with SOC 2 compliance

### Free Tier Privacy
- **No Authentication Required:** Free-tier endpoints (`turbo_quant_capabilities`) require no API key
- **Anonymous Usage Tracking:** Basic metrics collected for service improvement (request count, endpoint usage)
- **No Cross-Site Tracking:** No third-party analytics or tracking scripts
- **Data Minimization:** Only necessary agricultural parameters collected (latitude, longitude, soil type, etc.)

### API Key Privacy
- **GitHub Issue Process:** Email and use case only requested for API key issuance
- **No Sensitive Data:** Never request passwords, personal identifiers, or financial information
- **Key Rotation:** API keys can be regenerated upon request
- **Usage Limits:** Clear rate limits documented per pricing tier

## API Key Options

### 1. Free Tier (Recommended for Testing)
- **Header:** `x-free-tier: true`
- **Tools:** `check_turboquant` (always free), limited `analyze_soil`
- **No Signup Required** - Start immediately
- **Privacy:** No email collection, anonymous usage

### 2. Founder Pricing (Limited Time)
**First 100 customers get lifetime pricing lock:**
- **Starter:** $10/month → $49/month lifetime (normally $149)
  - Checkout: https://buy.stripe.com/14A7sL30y8bR2F4fbgaMU02
- **Pro:** $49/month → $149/month lifetime (normally $499)
  - Checkout: https://buy.stripe.com/cNi3cv1WuajZcfE7IOaMU03

### 3. Normal Pricing (After Founder Period)
- **Starter:** $149/month
- **Pro:** $499/month
- **Enterprise:** $1,999/month (custom)

**No more GitHub issue requests** - All API keys via Stripe checkout for instant access.

## API Documentation

**MCP Server URL:** `https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server`

**Authentication Options:**
1. **Free Tier:** `x-free-tier: true` header
2. **Paid Tier:** `x-api-key: YOUR_PAID_KEY_HERE` header

**Emergency API (Direct Calls):**
- **Base URL:** `https://leafengines-emergency-api-1.onrender.com/v1/`
- **Free Tier:** Same `x-free-tier: true` header
- **Parameter:** `county_fips` (5-digit code required)

**MCP Tools:**
1. **`analyze_soil`** - Soil analysis with recommendations
   - **Parameter:** `county_fips` (5-digit code)
   - **Free Tier:** Limited access with `x-free-tier: true`

2. **`recommend_crop`** - Crop recommendations
   - **Parameter:** `county_fips` (5-digit code)
   - **Paid Tier:** Full access with `x-api-key`

3. **`check_turboquant`** - TurboQuant capabilities check
   - **Parameter:** `county_fips` (5-digit code)
   - **Always FREE** - No authentication required

## Support & Community

- **GitHub Repository:** https://github.com/QWarranto/leafengines-claude-mcp
- **Documentation:** https://github.com/QWarranto/soil-sidekick-pro-guide
- **Early Adopters:** 1,092+ MCP downloads, 476+ n8n downloads, 54+ QGIS downloads
- **Support:** GitHub issues or email

**Platform Downloads (as of April 20, 2026):**
- **MCP Server:** 1,092+ downloads (since March 29)
- **n8n Node:** 476+ downloads (since April 9)
- **Node-RED:** 124+ downloads (since April 6)
- **QGIS Plugin:** 54+ downloads (since April 14)
- **Total:** ~1,746+ downloads across platforms

## License & Intellectual Property

Proprietary - Commercial API service. Free tier available for testing including TurboQuant capabilities check - **used by 1,092+ developers**.

## TurboQuant Technology

**Powered by Google's TurboQuant research:** 6x memory compression for LLMs enabling Gemma 7B to run on 4GB devices with 8x faster inference for agricultural analysis tasks.

---

**Updated:** April 20, 2026
**Version:** 1.2.0
**Key Changes:**
- Corrected tool list (3 tools, not 10)
- Added Free Tier instructions (`x-free-tier: true`)
- Updated pricing to Founder model (first 100 customers)
- Removed outdated GitHub issue API key process
- Added accurate download statistics (1,092+ MCP downloads)
- Fixed Quick Start with dual paths (Free vs Paid)