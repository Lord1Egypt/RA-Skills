import os
import sys
import json
import requests
from dotenv import load_dotenv


def get_client():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(env_path)

    api_key = os.environ.get("MSS_API_KEY")
    endpoint = os.environ.get("MSS_API_ENDPOINT")

    if not api_key or not endpoint:
        print("ERROR: MSS not configured. Please provide your API key to initialize.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    return endpoint, headers


def api_get(path, params=None):
    endpoint, headers = get_client()
    resp = requests.get(f"{endpoint}{path}", headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_post(path, payload):
    endpoint, headers = get_client()
    resp = requests.post(f"{endpoint}{path}", headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def api_patch(path, payload):
    endpoint, headers = get_client()
    resp = requests.patch(f"{endpoint}{path}", headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fmt_json(data):
    return json.dumps(data, indent=2, ensure_ascii=False)
