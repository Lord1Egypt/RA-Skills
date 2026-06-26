#!/usr/bin/env python3
"""
Groq-Bot v2 – KI-Assistent für Satin Trading System
- Fix 413: Token-Trimming + hartes Input-Limit
- Fix 429: Retry-After Header-Auswertung + Exponential Backoff
"""
import os
import json
import time
import logging
import yaml
import math
from pathlib import Path
from groq import Groq, RateLimitError, APIStatusError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/detailed.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
logger = logging.getLogger("groq-bot")

def load_config():
    config_path = Path('config.yaml')
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}

CONFIG = load_config()
MODEL = CONFIG.get('model', 'llama-3.1-8b-instant')
API_KEY = CONFIG.get('api_key', os.getenv('GROQ_API_KEY'))
MAX_TOKENS = CONFIG.get('max_tokens', 512)
MAX_INPUT_CHARS = CONFIG.get('max_input_chars', 3000)
TEMPERATURE = CONFIG.get('temperature', 0.5)
TIMEOUT = CONFIG.get('timeout_seconds', 30)

rl = CONFIG.get('rate_limit', {})
RPM_LIMIT = rl.get('requests_per_minute', 20)
TPM_LIMIT = rl.get('tokens_per_minute', 5000)
BACKOFF_MULTIPLIER = rl.get('backoff_multiplier', 2)
MAX_WAIT = rl.get('max_wait_seconds', 120)

client = Groq(api_key=API_KEY)

# ── Token-Budget-Tracker ──
TOKEN_BUDGET_FILE = Path('state/groq_token_budget.json')

def _load_budget():
    if TOKEN_BUDGET_FILE.exists():
        with open(TOKEN_BUDGET_FILE) as f:
            return json.load(f)
    return {"tokens_this_minute": 0, "minute_start": time.time()}

def _save_budget(b):
    TOKEN_BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_BUDGET_FILE, 'w') as f:
        json.dump(b, f)

def _estimate_chars(chars: int) -> int:
    """~4 chars per token für Deutsch"""
    return math.ceil(chars / 4)

def _check_token_budget(input_chars: int) -> float:
    """Returns seconds to wait, or 0 if OK."""
    b = _load_budget()
    now = time.time()
    elapsed = now - b["minute_start"]
    if elapsed >= 60:
        b = {"tokens_this_minute": 0, "minute_start": now}
        elapsed = 0
    estimated = _estimate_chars(input_chars)
    if b["tokens_this_minute"] + estimated > TPM_LIMIT:
        return 60 - elapsed + 1
    b["tokens_this_minute"] += estimated
    _save_budget(b)
    return 0

# ── Conversation History ──
CONVERSATION_FILE = Path('conversation.json')
MAX_HISTORY_MESSAGES = 6

def load_conversation():
    if CONVERSATION_FILE.exists():
        try:
            with open(CONVERSATION_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('messages', [])
        except Exception as e:
            logger.warning(f"Fehler beim Laden: {e}")
    return []

def save_conversation(messages):
    try:
        CONVERSATION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONVERSATION_FILE, 'w', encoding='utf-8') as f:
            json.dump({"messages": messages[-MAX_HISTORY_MESSAGES*2:]}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Speicherfehler: {e}")

def _trim_messages(messages: list, max_chars: int = 6000) -> list:
    """Trim history to stay within budget."""
    total = sum(len(m.get('content', '')) for m in messages)
    while total > max_chars and len(messages) > 1:
        removed = messages.pop(0)
        total -= len(removed.get('content', ''))
    return messages

def _extract_retry_after(error) -> int:
    """Extract Retry-After header value in seconds."""
    try:
        retry_after = getattr(error, 'headers', {}).get('retry-after', None)
        if retry_after is None and hasattr(error, 'response'):
            retry_after = error.response.headers.get('retry-after', None)
        if retry_after:
            return min(int(retry_after) + 1, MAX_WAIT)
    except (ValueError, TypeError, AttributeError):
        pass
    return -1

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=BACKOFF_MULTIPLIER, min=4, max=60),
    retry=retry_if_exception_type((RateLimitError, ConnectionError)),
    retry_error_callback=lambda retry_state: None
)
def run_query(prompt: str, conversation_history: list = None) -> str:
    """Send request to Groq with full 413/429 protection."""
    # 413-Fix: Trim input
    prompt = prompt[:MAX_INPUT_CHARS]

    messages = []
    system_prompt = CONFIG.get('system_prompt', '')
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    if conversation_history:
        hist = conversation_history[-MAX_HISTORY_MESSAGES:]
        messages.extend(hist)
    messages.append({"role": "user", "content": prompt})

    # 413-Fix: Trim total message chars
    messages = _trim_messages(messages)

    # 429-Fix: Pre-flight token budget check
    total_chars = sum(len(m.get('content', '')) for m in messages)
    wait_secs = _check_token_budget(total_chars)
    if wait_secs > 0:
        logger.info(f"Token-Budget-Wartezeit: {wait_secs:.0f}s")
        time.sleep(wait_secs)

    logger.info(f"API-Anfrage: model={MODEL}, msgs={len(messages)}, chars={total_chars}")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            timeout=TIMEOUT
        )
        answer = response.choices[0].message.content
        logger.info(f"Antwort: {len(answer)} Zeichen")
        return answer

    except RateLimitError as e:
        retry_after = _extract_retry_after(e)
        if retry_after > 0:
            logger.warning(f"429 Rate-Limit — warte {retry_after}s (Retry-After Header)")
            time.sleep(retry_after)
        else:
            wait = min(BACKOFF_MULTIPLIER ** min(5, 10), MAX_WAIT)
            logger.warning(f"429 Rate-Limit — warte {wait}s (Backoff)")
            time.sleep(wait)
        raise  # tenancy retry

    except APIStatusError as e:
        status = e.status_code if hasattr(e, 'status_code') else 0
        if status == 413:
            logger.error("413 Payload Too Large — reduziere Historie")
            # Aggressives Trimmen und Retry
            messages = messages[-2:] if len(messages) > 2 else messages
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=min(MAX_TOKENS, 256),
                    temperature=TEMPERATURE,
                    timeout=TIMEOUT
                )
                return response.choices[0].message.content
            except Exception:
                return "Fehler: Request auch nach Reduktion zu groß. Bitte kürzere Anfrage."
        elif status == 400 and "decommissioned" in str(e).lower():
            logger.error(f"Modell {MODEL} decommissioned — bitte config.yaml aktualisieren")
            return f"Fehler: Modell {MODEL} nicht mehr verfügbar. Bitte config updaten."
        return f"Fehler (HTTP {status}): {str(e)}"

    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {str(e)}")
        return f"Fehler: {str(e)}"

def process_user_input(prompt: str) -> str:
    """Verarbeitete eine Benutzeranfrage mit Token-Awareness."""
    try:
        prompt = prompt[:MAX_INPUT_CHARS]
        conversation = load_conversation()
        answer = run_query(prompt, conversation)
        conversation.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer}
        ])
        save_conversation(conversation)
        return answer
    except Exception as e:
        logger.error(f"Verarbeitungsfehler: {str(e)}")
        return f"Verarbeitungsfehler: {str(e)}"

def main():
    print(f"Groq-Bot v2 gestartet (Modell: {MODEL})")
    print("'exit' zum Beenden")
    while True:
        try:
            user_input = input("\nAnfrage: ").strip()
            if user_input.lower() in ('exit', 'quit', 'ende'):
                break
            if not user_input:
                continue
            print(f"\nAntwort: {process_user_input(user_input)}")
        except (KeyboardInterrupt, EOFError):
            print("\nBeendet.")
            break

if __name__ == "__main__":
    main()