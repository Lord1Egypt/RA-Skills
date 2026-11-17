"""First-run guide, shown wherever the API key turns out to be missing.

One source of truth for the three things a new user needs (where the key comes
from, how to store it, what a query costs). The Setup section of the SKILL.md
next to this package mirrors it — keep both in sync.
"""

from __future__ import annotations

KEY_URL = "https://www.kalodata.com/open-center/account"
SIGNUP_URL = "https://www.kalodata.com/open-center/home"
PRICING_URL = "https://www.kalodata.com/pricing"

SETUP_LINES = [
    f'1. Get a key: sign in at {KEY_URL} and click "generate key" '
    f"(no account yet? register at {SIGNUP_URL}). Already calling the KaloData API "
    "on credit-based billing? That same key works here — no new key needed.",
    "2. Save it: `kalo config set --key <API_KEY>`, or set KALODATA_API_KEY in the environment.",
    "3. Credits: every query spends KaloData credits — 0.2-0.4 for a basic lookup, "
    f"1-2 for an analysis/diagnosis. `kalo credit` shows the balance, {PRICING_URL} tops it up.",
]

NO_KEY_MESSAGE = "no KaloData API key configured yet"
