#!/usr/bin/env python3
"""Send an audio file as a Telegram voice message."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from kiwi.utils import kiwi_log

TOKEN = os.getenv("KIWI_TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("KIWI_TELEGRAM_CHAT_ID", "")

if not TOKEN or not CHAT_ID:
    print("Error: set KIWI_TELEGRAM_BOT_TOKEN and KIWI_TELEGRAM_CHAT_ID env vars")
    sys.exit(1)

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <audio_file>")
    sys.exit(1)

AUDIO_FILE = sys.argv[1]

url = f"https://api.telegram.org/bot{TOKEN}/sendVoice"

with open(AUDIO_FILE, 'rb') as f:
    files = {'voice': f}
    data = {'chat_id': CHAT_ID, 'caption': 'Kiwi Voice TTS test'}
    resp = requests.post(url, files=files, data=data)

kiwi_log("VOICE-SEND", f"Status: {resp.status_code}")
kiwi_log("VOICE-SEND", f"Response: {resp.text[:500]}")
