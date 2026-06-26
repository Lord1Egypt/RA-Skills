# HelloFresh Assistant

**Description:** Interact with your HelloFresh account — discover recipes, manage selections, convert instructions to audio, and get shipment alerts.

**Commands:**
- `/hello-fresh setup` — First-time setup (collects subscription info)
- `/hello-fresh status` — Show subscription status
- `/hello-fresh discover [week]` — Find recipes (this/next/last/2026-W11)
- `/hello-fresh history` — Past deliveries
- `/hello-fresh recommend` — AI recommendations
- `/hello-fresh convert <recipe>` — Text-to-speech cooking instructions
- `/hello-fresh track` — Delivery tracking
- `/hello-fresh notify` — Notification settings & check shipment
- `/hello-fresh notify check` — Manually check current shipment status
- `/hello-fresh notify enable` — Enable shipment alerts
- `/hello-fresh notify disable` — Disable shipment alerts
- `/hello-fresh reset` — Clear session

**Requires:** browser, tts

**Storage:** `~/.openclaw/hellofresh/session.json`

**Browser:** Uses profile="chrome" (Chrome Extension Relay) or Kernel.sh cloud

**Shipment Alerts:**
- Automatically detects when your box status changes (e.g., "Shipping soon" → "Out for delivery")
- Sends notifications via Telegram when enabled
- Tracks status history for change detection
