# 🔒 presidio-pii

**Local PII protection for OpenClaw agents.**

Your AI agent talks to CRMs, cloud drives, and project management tools. That means customer names, phone numbers, emails, and addresses flow through AI models hosted on external servers. This skill makes sure none of that data ever leaves your machine unprotected.

## How It Works

1. Customer data comes in from CRM/Drive/etc: "John Smith, 954-555-1234, 123 Ocean Blvd"
2. Presidio (local Docker) detects PII and replaces with tokens
3. Clean data sent to AI model: "[PERSON_1], [PHONE_NUMBER_1], 123 [LOCATION_1]"
4. Model responds with tokens: "[PERSON_1] hasn't been followed up in 14 days."
5. Presidio restores real values locally
6. You see: "John Smith hasn't been followed up in 14 days."

The AI model (wherever it runs) only ever sees tokens. Real customer data stays on your Mac.

## What Gets Detected

Out of the box, Presidio catches:
- Person names (via NLP)
- Phone numbers (all formats)
- Email addresses
- Physical addresses
- Credit card numbers (with Luhn validation)
- US Social Security Numbers
- Bank account / routing numbers
- IP addresses
- Dates of birth

## Custom Recognizers

The skill includes a configs/recognizers.json where you can add patterns specific to your business. Examples included:
- City/region name boosting (for when spaCy misses local city names)
- Vessel/vehicle name patterns
- Project ID patterns that contain customer names
- **WhatsApp JID exclusion** (prevents @g.us and @s.whatsapp.net from being detected as emails)

Edit the JSON file, no container restart needed. Recognizers are passed with each API call.

### WhatsApp JID Protection

By default, Presidio's email recognizer detects `@g.us` in WhatsApp group IDs (e.g., `120363426280179487@g.us`) as email addresses. This skill includes a whitelist recognizer that prevents this false positive. The recognizer matches WhatsApp JIDs with a score of 0.0, effectively excluding them from PII detection.

## Prerequisites

- Docker running locally (Colima recommended for headless Mac Mini, Docker Desktop also works)
- Python 3 (included with macOS)
- curl (included with macOS)

## Quick Install

### 1. Start Presidio containers

Create a docker-compose.yml at ~/.openclaw/presidio/ with analyzer (port 5002:3000) and anonymizer (port 5001:3000). Then run: docker compose up -d

IMPORTANT: Presidio containers listen on port 3000 internally. Map 5002:3000 (analyzer) and 5001:3000 (anonymizer). If you map 5002:5002, you'll get empty replies.

### 2. Install the skill

    clawhub install presidio-pii

Or manually copy the skill folder to ~/.openclaw/workspace/skills/

### 3. Test it

    # Health check
    bash ~/.openclaw/workspace/skills/presidio-pii/scripts/presidio-health.sh

    # Scrub
    echo 'John Smith at 123 Ocean Blvd, Miami' | python3 ~/.openclaw/workspace/skills/presidio-pii/scripts/presidio-scrub.py test1

    # Restore
    echo '[PERSON_1] at 123 [LOCATION_1], [LOCATION_2]' | python3 ~/.openclaw/workspace/skills/presidio-pii/scripts/presidio-restore.py test1

## Security

- 100% local. Presidio containers run on localhost. No data leaves your machine.
- Fail-closed. If Presidio is down, the skill blocks data queries rather than sending unprotected PII.
- Ephemeral mappings. Token-to-real-value mapping files are created per request, stored with chmod 600, and auto-deleted after restore.
- Vanilla containers. Custom recognizers are passed via API calls, not baked into containers. Pull updated images anytime without losing your config.

## Why Colima over Docker Desktop?

If you're running OpenClaw on a headless Mac Mini, Colima saves ~1-2GB RAM compared to Docker Desktop. It runs entirely from the terminal with no GUI overhead.

    brew install docker docker-compose colima
    brew services start colima
    docker context use colima

## File Structure

    presidio-pii/
      SKILL.md              -- Agent instructions (what to scrub, when, how)
      skill.json            -- Metadata and tags
      README.md             -- You're reading it
      configs/
        recognizers.json    -- Custom PII patterns (edit for your business)
      scripts/
        presidio-health.sh  -- Health check (are containers up?)
        presidio-scrub.py   -- Analyze + anonymize + save mapping
        presidio-restore.py -- De-anonymize + delete mapping

## FAQ

Q: What if Presidio misses something?
A: No PII detection is 100%. Presidio + custom recognizers covers the vast majority of common patterns. You can always add more patterns to recognizers.json.

Q: Does this slow down responses?
A: Barely. The Presidio analysis (spaCy NER + regex) takes milliseconds. The Docker containers use about 500MB-1GB RAM combined and negligible CPU when idle.

Q: Can I use this with any AI model?
A: Yes. That's the point. Whether your model runs in the US, China, or anywhere else, it only sees tokens. The skill is model-agnostic.

Q: What about GDPR / CCPA compliance?
A: This skill helps you take "reasonable steps" to protect customer data. It's not a legal compliance solution on its own, but it significantly reduces your exposure. Consult a lawyer for formal compliance requirements.

## Why This Exists

I don't trust any AI provider with my customers' personal information. Not the American ones, not the Chinese ones, none of them. They're all logging whatever they want to train their models. If you're running a business and connecting your AI agent to customer data, you should assume that anything you send to an external model is being stored, analyzed, and used in ways you didn't agree to.

This skill keeps customer data on your machine where it belongs. The AI model gets tokens. Your customers get privacy. Everybody wins except the data harvesters.

Oh, and it's completely free and open source. Presidio is free (Microsoft open source). Colima is free. This skill is free. No subscriptions, no API keys, no usage fees. Just local software protecting your customers' data.

## License

MIT

## Author

Albert (@sebclawops - https://github.com/sebclawops)
