# Lead Guardian — Real Estate Lead Response Skill

AI-powered lead response and qualification for real estate agents.

## Description

Lead Guardian helps real estate agents respond to leads instantly, qualify them automatically, and route hot leads for immediate follow-up. Works via SMS, email, or CRM webhook integration.

## Capabilities

- **Instant Response** — Reply to new leads within 60 seconds
- **AI Qualification** — Extract buying/selling intent, timeline, pre-approval status, price range
- **Hot Lead Detection** — Identify ready-to-buy leads and alert agents immediately
- **Conversation Tracking** — Full history of lead interactions
- **CRM Integration** — Connect with Follow Up Boss, KW Command, and others

## Use Cases

1. **After-Hours Coverage** — Respond to leads when you're unavailable
2. **Lead Qualification** — Filter tire-kickers from serious buyers
3. **Speed to Lead** — Beat competitors with instant response
4. **Consistent Follow-Up** — Never miss a lead

## Requirements

- Twilio account (for SMS)
- OpenRouter API key (for AI)
- Optional: CRM webhook URL

## Quick Start

```bash
# Install dependencies
pip install flask twilio requests python-dotenv

# Configure
export TWILIO_ACCOUNT_SID="your_sid"
export TWILIO_AUTH_TOKEN="your_token"
export TWILIO_PHONE_NUMBER="+1xxxxxxxxxx"
export OPENROUTER_API_KEY="your_key"
export AGENT_PHONE="+1xxxxxxxxxx"

# Run
python app.py
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| TWILIO_ACCOUNT_SID | Yes | Twilio account SID |
| TWILIO_AUTH_TOKEN | Yes | Twilio auth token |
| TWILIO_PHONE_NUMBER | Yes | Your Twilio phone number |
| OPENROUTER_API_KEY | Yes | For AI responses |
| AGENT_PHONE | No | Phone to alert for hot leads |

### Hot Lead Criteria

A lead is flagged as "hot" when:
- Timeline is "immediate" or "1-3 months"
- Pre-approved for mortgage
- Explicitly requests an agent

### Qualification Questions

The AI naturally extracts:
1. **Direction** — Buying, selling, or both
2. **Timeline** — When they want to move
3. **Pre-approval** — Mortgage status (if buying)
4. **Price Range** — Budget (if buying)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sms` | POST | Twilio webhook for incoming SMS |
| `/api/leads` | GET | List all leads |
| `/api/leads/:id/messages` | GET | Get conversation history |
| `/api/leads/:id/handoff` | POST | Mark lead as handed off |
| `/` | GET | Admin dashboard |

## Cost

~$30/month for 500 leads
- Twilio number: $1/month
- SMS (1,000 messages): $10
- Claude Haiku API: $15-20

## Files

```
lead-guardian/
├── SKILL.md          # This file
├── app.py            # Main Flask application
├── leads.db          # SQLite database (created on run)
└── .env.example      # Environment template
```

## Credits

Built by KW Sacramento Metro AI Team.

## License

MIT
