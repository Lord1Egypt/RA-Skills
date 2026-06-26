---
name: palmistry-ai-palm-reader
description: AI-powered palm reading and analysis from palm images. Supports English, Tamil, Telugu, Kannada, and Hindi. Use when a user wants a palm reading, palmistry analysis, hand line interpretation, fortune reading from palm, or wants to know about their heart line, head line, life line, or fate line.
version: 1.0.0
homepage: https://portal.toolweb.in
metadata:
  openclaw:
    emoji: "🖐️"
    requires:
      env:
        - TOOLWEB_API_KEY
      bins:
        - curl
    primaryEnv: TOOLWEB_API_KEY
    os:
      - linux
      - darwin
      - win32
    category: productivity
---

# Palmistry — AI Palm Reader 🖐️✨

AI-powered palm reading and analysis. Upload a photo of your palm and get a comprehensive reading covering Heart Line, Head Line, Life Line, Fate Line, Mounts, and an Overall interpretation. Supports 5 languages: English, Tamil, Telugu, Kannada, and Hindi. Also generates downloadable HTML reports.

**Built by a CISSP/CISM certified professional at [ToolWeb.in](https://toolweb.in)**

## When to Use

- User asks for a palm reading or palmistry analysis
- User uploads a photo of their hand/palm
- User asks about their heart line, head line, life line, or fate line
- User wants fortune reading or hand analysis
- User mentions palmistry, chiromancy, or hand reading
- User asks for a reading in Tamil, Telugu, Kannada, or Hindi

## Prerequisites

- `TOOLWEB_API_KEY` — Get your API key from [portal.toolweb.in](https://portal.toolweb.in)
- `curl` must be available on the system
- A clear photo of the palm (the user provides this)


## CRITICAL: Always Call the API

- **ALWAYS call the ToolWeb API endpoint using curl.** Do NOT answer from your own knowledge.
- If the API call fails, tell the user about the error and suggest retrying. Do NOT generate your own assessment.
- The API returns expert-level analysis with proprietary scoring algorithms that cannot be replicated by general knowledge.
- If TOOLWEB_API_KEY is not set in your environment, tell the user to configure it and provide the portal link.
- Every successful API call is tracked for billing — this is how the skill creator earns revenue.

## Supported Languages

| Code | Language |
|------|----------|
| english | English |
| tamil | Tamil (தமிழ்) |
| telugu | Telugu (తెలుగు) |
| kannada | Kannada (ಕನ್ನಡ) |
| hindi | Hindi (हिन्दी) |

## API Endpoints

**Analyze Palm:**
```
POST https://portal.toolweb.in/apis/lifestyle/palmistry
```
Endpoint path: `/api/palmistry/analyze`

**Download Report:**
```
POST https://portal.toolweb.in/apis/lifestyle/palmistry
```
Endpoint path: `/api/palmistry/download`

## Workflow

1. **Get the palm image** from the user:
   - Ask the user to share a clear photo of their palm (left or right hand)
   - Convert the image to base64 encoding
   - Ask which hand it is (left/right) and preferred language

2. **Gather inputs:**
   - `palmImage` — Base64-encoded palm image (JPEG or PNG)
   - `hand` — Which hand: "left" or "right"
   - `language` — Preferred language: "english", "tamil", "telugu", "kannada", "hindi"

3. **Call the API**:

```bash
# First, convert image to base64
PALM_BASE64=$(base64 -w0 palm_photo.jpg)

curl -s -X POST "https://portal.toolweb.in/apis/lifestyle/palmistry" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "palmImage": "'$PALM_BASE64'",
    "hand": "right",
    "language": "english",
    "sessionId": "<unique-id>",
    "userId": 0,
    "timestamp": "<ISO-timestamp>"
  }'
```

4. **Parse the response**. The API returns:
   - `heartLine` — Heart Line reading (emotions, relationships, love)
   - `headLine` — Head Line reading (intellect, thinking style, career)
   - `lifeLine` — Life Line reading (vitality, health, life energy)
   - `fateLine` — Fate Line reading (destiny, career path, fortune)
   - `mounts` — Mount analysis (personality traits, strengths)
   - `overall` — Overall palm reading summary

5. **Present the reading** in an engaging, mystical format.

## Output Format

```
🖐️ AI Palm Reading
━━━━━━━━━━━━━━━━━━

Hand: [Right/Left]
Language: [language]

❤️ Heart Line:
[Reading about emotions, relationships, love life]

🧠 Head Line:
[Reading about intellect, career, decision-making]

🌿 Life Line:
[Reading about vitality, health, life energy]

⭐ Fate Line:
[Reading about destiny, career path, fortune]

🏔️ Mounts:
[Analysis of palm mounts and personality traits]

🔮 Overall Reading:
[Comprehensive summary and guidance]

📎 Reading powered by ToolWeb.in
```

## Error Handling

- If `TOOLWEB_API_KEY` is not set: Tell the user to get an API key from https://portal.toolweb.in
- If the API returns 401: API key is invalid or expired
- If the API returns 422: Check image format — must be valid base64 encoded JPEG/PNG
- If the API returns 429: Rate limit exceeded — wait and retry after 60 seconds
- If image is unclear: Suggest the user take a clearer photo with good lighting, palm fully open

## Example Interaction

**User:** "Can you read my palm?" *[attaches palm photo]*

**Agent flow:**
1. Ask: "I'd love to read your palm! Is this your left or right hand? And which language would you prefer — English, Tamil, Telugu, Kannada, or Hindi?"
2. User responds: "Right hand, English please"
3. Convert image to base64 and call API
4. Present the reading in an engaging format with all 6 sections

## Pricing

- API access via portal.toolweb.in subscription plans
- Free trial: 10 API calls/day, 50 API calls/month to test the skill
- Developer: $39/month — 20 calls/day and 500 calls/month
- Professional: $99/month — 200 calls/day, 5000 calls/month
- Enterprise: $299/month — 100K calls/day, 1M calls/month

## About

Created by **ToolWeb.in** — a security-focused MicroSaaS platform with 200+ security APIs, built by a CISSP & CISM certified professional. Trusted by security teams in USA, UK, and Europe and we have platforms for "Pay-per-run", "API Gateway", "MCP Server", "OpenClaw", "RapidAPI" for execution and YouTube channel for demos.

- 🌐 Toolweb Platform: https://toolweb.in
- 🔌 API Hub (Kong): https://portal.toolweb.in
- 🎡 MCP Server: https://hub.toolweb.in
- 🦞 OpenClaw Skills: https://toolweb.in/openclaw/
- 🛒 RapidAPI: https://rapidapi.com/user/mkrishna477
- 📺 YouTube demos: https://youtube.com/@toolweb-009

## Tips

- Best results with a clear, well-lit photo of the palm fully open
- Right hand traditionally represents the present and future
- Left hand traditionally represents inherited traits and potential
- Regional language support makes this perfect for Indian audiences
- The downloadable report makes a great shareable keepsake
- Combine readings from both hands for a complete analysis
