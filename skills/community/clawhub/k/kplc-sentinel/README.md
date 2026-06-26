# KPLC Sentinel

An OpenClaw skill that tracks prepaid electricity for Kenyan households. Parses KPLC token SMS messages, predicts when you'll run out of power, tracks spending, detects price trends, and warns you about planned outages in your area.

## Requirements

- OpenClaw installed and running (`npm install -g openclaw@latest`)
- A connected messaging channel (WhatsApp, Telegram, etc.)
- Python 3 with `pdfplumber` (`pip install -r requirements.txt`)
- An LLM API key (Anthropic, OpenAI, Google Gemini, etc.)

## Install

```
clawhub install kplc-sentinel
```

Or if you don't have the ClawHub CLI:

```
openclaw skills install kplc-sentinel
```

## Setup

If you don't have OpenClaw running yet:

```bash
# Install OpenClaw
npm install -g openclaw@latest

# Run the setup wizard (configures your LLM API key and daemon)
openclaw onboard

# Connect WhatsApp (scan QR code with your phone)
openclaw channels login --channel whatsapp

# Install the skill
openclaw skills install kplc-sentinel

# Install Python dependencies
pip install -r requirements.txt

# Start the gateway
openclaw gateway
```

Message your OpenClaw agent on WhatsApp and say "stima" to see the menu, or "stima setup" to start onboarding.

## Usage

The skill responds to the `stima` prefix, forwarded KPLC SMS messages, and natural language about electricity in English, Swahili, or Sheng.

**Menu:** Type "stima" to see a numbered menu of all commands. Reply with a number to select.

**Natural language:** You can also just ask naturally:
- "stima itaisha lini?" → checks your balance
- "nimetumia pesa ngapi kwa stima?" → monthly summary
- "kuna blackout lini?" → checks for outages
- "will my power last until Monday?" → checks your balance

The agent translates your intent into the right command automatically.

**Onboarding:** Say "stima setup". The skill asks for your household size, area/estate, and appliances. Your appliance list is used to estimate consumption even before you have any meter readings.

**Track a token purchase:** Forward your KPLC SMS to the chat. The skill parses the token, units, and amount automatically, and estimates how many days it will last.

Example SMS formats it recognizes:
```
Accept Token: 1234-5678-9012-3456-7890 Units: 34.5 Amount: 1000.00
Token: 9876-5432-1098 Units: 15.2 Amt: 500.0
```

**Record a meter reading:** Press 20# on your meter and type "stima 42.5".

**Check your balance:** "stima balance" or "nimebakisha units ngapi?"

**Budget:** "stima budget 3000" to set, "stima budget" to check.

**Usage insights:** "stima insights" for week-over-week comparison and day patterns.

**Spending dashboards:** "stima monthly", "stima yearly", or "stima spending".

**Price trends:** "stima price" or "bei ya stima imeongezeka?"

**Planned outages:** "stima outage" — the skill scrapes KPLC's maintenance schedule PDF and checks for your area. When an outage is found, the agent sets a reminder for the evening before so you can charge your devices.

**Low balance top-up:** When your power is running low, the agent includes M-Pesa top-up instructions (Paybill 888880).

**Profile:** "stima profile" to see household info and budget status.

**Reset:** "stima reset" to clear your profile and re-onboard (e.g. if you move house or change appliances).

**Help:** "stima help" or "stima menu" to see all commands.

## How it works

The skill returns structured JSON data from its Python scripts. The OpenClaw agent reads this data and composes natural, conversational responses using the Stima persona defined in SOUL.md. The scripts are the data layer; the agent is the brain.

Nothing leaves your machine except a single HTTPS request to `kplc.co.ke` to fetch the planned outage PDF (cached for 1 hour).

- **Burn rate:** Weighted average across all meter readings, with exponential decay so recent usage matters more
- **Appliance estimates:** When no meter readings exist yet, the skill estimates consumption from your appliance list (wattage × typical daily usage hours) scaled by household size — useful predictions from day one
- **Blackout prediction:** Current balance divided by burn rate (or appliance estimate)
- **Token-to-days:** Estimates how long a new purchase will last
- **Budget tracking:** Set a monthly KES limit, warns at 80% and 100%
- **Usage insights:** Week-over-week comparison and heaviest/lightest day detection
- **Household tips:** When balance is low, suggests turning off heavy appliances from your profile
- **Outage alerts:** Downloads and parses KPLC's two-column maintenance PDF, matches against your area
- **Price trends:** Tracks cost-per-unit across months, shows percentage changes
- **Multi-skill composability:** Returns structured data that other OpenClaw skills can act on (calendar events for outages, M-Pesa payments for top-ups)

## Security

- All SQL queries use parameterized statements (no injection)
- User input passed via stdin heredoc (no shell injection)
- Input length capped at 5000 characters
- Profile values sanitized before display (no chat injection)
- Database file created with owner-only permissions (0600)
- Outbound requests locked to `kplc.co.ke` HTTPS only
- No credentials stored in code
- Error messages don't leak internal details

## Heartbeat (proactive alerts)

The skill checks automatically via OpenClaw's heartbeat system:

- Every 6 hours: warns if you have less than 24 hours of power left, checks for planned outages
- Every 48 hours without a reading: asks for a spot check
- Weekly on Monday: sends a consumption and spending summary

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill metadata, agent routing, and JSON action reference |
| `SOUL.md` | Agent persona ("Stima") and response formatting guidance |
| `HEARTBEAT.md` | Scheduled proactive checks |
| `entrypoint.py` | Message handler — returns JSON data for the agent |
| `sentinel.py` | Heartbeat alerts and weekly summary |
| `logic.py` | Burn rate, predictions, appliance estimates, spending, outage parsing |
| `parser.py` | KPLC SMS regex parser |
| `init_db.py` | SQLite schema and connection management |
| `requirements.txt` | Python dependencies |
