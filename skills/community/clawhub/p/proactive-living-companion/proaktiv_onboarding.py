#!/usr/bin/env python3
"""
Proactive v1.0.18 — Onboarding Script (International / English)
Sends a system trigger to kick off the onboarding interview via Telegram.
"""

import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_message_via_openclaw(message_text, question_type="setup"):
    full_prompt = f"""
[SYSTEM-ONBOARDING: {question_type}]
This is the Proactive v1.0.18 setup interview running via Telegram.

YOUR TASK:
{message_text}

RULES FOR YOUR TELEGRAM REPLY:
1. Act as a friendly, warm companion. Welcome the user to Proactive v1.0.18.
2. Ask the questions below naturally and clearly (e.g. with bullet points).
3. Be transparent -- tell the user this is Proactive, your automated companion, introducing itself for the first time.
4. Let the user know you'll write their answers directly into your memory files.
"""
    try:
        command = ['openclaw', 'send', full_prompt, '--session', 'isolated']
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info("Onboarding message sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send onboarding message: {e}")

def main():
    intro_text = """
Please ask the user the following setup questions in ONE well-formatted Telegram message:

1. **Interests** — What topics are you most interested in right now? (e.g. AI tools, home automation, fitness, F1, music production)

2. **Sports & Events** — Should Proactive track any sports or events for you? (e.g. F1, Champions League, wrestling)

3. **No-Go Topics** — Any topics you absolutely do NOT want to be pinged about? (e.g. politics, crypto, religion)

4. **Quiet Hours** — When should Proactive stop pinging and go silent? (e.g. 22:00–07:30)

5. **Chill Mode** — After what time in the evening should work/tech topics stop, and only entertainment/lifestyle pings come through? (e.g. from 20:00)

Ask all five questions at once. Keep it friendly and concise.
"""
    send_message_via_openclaw(intro_text, "onboarding_questions")

if __name__ == "__main__":
    main()
