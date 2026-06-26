import json
import os
import sys
from datetime import datetime, timedelta
from dateutil import parser as dateparser, tz

CONFIG_DIR = os.path.expanduser("~/.openclaw/integrations/microsoft")
TOKENS_PATH = os.path.join(CONFIG_DIR, "tokens.json")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

REQUIRED_SCOPES = set([
    "User.Read",
    "Calendars.ReadWrite",
    "OnlineMeetings.ReadWrite",
])


def load_json(path, default=None):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception:
        return {} if default is None else default


def ensure_deps():
    try:
        import msal  # noqa: F401
        import requests  # noqa: F401
    except ImportError:
        os.system("python3 -m pip install --user msal requests python-dateutil tzlocal")


def build_msal_app():
    ensure_deps()
    import msal
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKENS_PATH) and os.path.getsize(TOKENS_PATH) > 0:
        try:
            cache.deserialize(open(TOKENS_PATH, 'r').read())
        except Exception:
            pass

    cfg = load_json(CONFIG_PATH, {})
    client_id = cfg.get('client_id')
    tenant = cfg.get('tenant', 'common')
    if not client_id:
        print("Error: Missing client_id in config. Run setup.py first.")
        sys.exit(1)
    app = msal.PublicClientApplication(
        client_id=client_id,
        authority=f"https://login.microsoftonline.com/{tenant}",
        token_cache=cache,
    )
    return app, cfg, cache


def acquire_token(scopes=None):
    import msal
    app, cfg, cache = build_msal_app()
    scopes = scopes or list(REQUIRED_SCOPES)
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])
    if not result:
        print("Interactive login required. Run setup.py first.")
        sys.exit(1)
    if 'access_token' not in result:
        print(f"Token acquisition failed: {result}")
        sys.exit(1)
    if cache.has_state_changed:
        with open(TOKENS_PATH, 'w') as f:
            f.write(cache.serialize())
        os.chmod(TOKENS_PATH, 0o600)
    return result['access_token'], cfg


def parse_time_with_tz(text, tzname=None):
    dt = dateparser.parse(text)
    if tzname:
        target_tz = tz.gettz(tzname)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=target_tz)
        else:
            dt = dt.astimezone(target_tz)
    elif not dt.tzinfo:
        dt = dt.replace(tzinfo=tz.tzlocal())
    return dt


def to_graph_datetime_timezoned(dt):
    return {
        "dateTime": dt.strftime('%Y-%m-%dT%H:%M:%S'),
        "timeZone": str(dt.tzinfo) if dt.tzinfo else 'UTC'
    }


def graph_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
