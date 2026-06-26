"""
Apify REST API Client — shared by all data source modules.
Uses only stdlib (urllib/json) to avoid extra dependencies.
"""

import os
import json
import time
import urllib.request
import urllib.error
from typing import Any, Optional

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
APIFY_BASE = "https://api.apify.com/v2"
MAX_WAIT_SECONDS = 300  # 5 minutes max wait for actor run
POLL_INTERVAL = 5  # seconds between status checks


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {APIFY_TOKEN}",
        "Content-Type": "application/json",
    }


def _request(method: str, url: str, data: Optional[dict] = None) -> dict:
    """Make HTTP request to Apify API."""
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"[Apify] HTTP {e.code}: {error_body[:500]}")
        raise


def run_actor(actor_id: str, input_data: dict, wait_secs: int = MAX_WAIT_SECONDS) -> list:
    """
    Run an Apify actor and wait for results.
    
    Args:
        actor_id: Actor identifier (e.g., 'apify/facebook-ads-scraper')
        input_data: Actor input parameters
        wait_secs: Max seconds to wait for completion
    
    Returns:
        List of result items from the actor's dataset
    """
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN environment variable not set")

    # 1. Start the actor run
    print(f"[Apify] Starting actor: {actor_id}")
    url = f"{APIFY_BASE}/acts/{actor_id}/runs"
    result = _request("POST", url, input_data)
    
    run_id = result["data"]["id"]
    print(f"[Apify] Run started: {run_id}")

    # 2. Poll for completion
    start_time = time.time()
    while time.time() - start_time < wait_secs:
        time.sleep(POLL_INTERVAL)
        status_url = f"{APIFY_BASE}/actor-runs/{run_id}"
        status = _request("GET", status_url)
        run_status = status["data"]["status"]
        
        if run_status == "SUCCEEDED":
            dataset_id = status["data"]["defaultDatasetId"]
            print(f"[Apify] Run succeeded. Dataset: {dataset_id}")
            
            # 3. Fetch results
            items_url = f"{APIFY_BASE}/datasets/{dataset_id}/items?format=json"
            req = urllib.request.Request(items_url, headers=_headers())
            with urllib.request.urlopen(req, timeout=60) as resp:
                items = json.loads(resp.read().decode())
            
            print(f"[Apify] Got {len(items)} items")
            return items
        
        elif run_status in ("FAILED", "ABORTED", "TIMED-OUT"):
            print(f"[Apify] Run {run_status}")
            return []
        
        elapsed = int(time.time() - start_time)
        print(f"[Apify] Status: {run_status} ({elapsed}s elapsed)")

    print(f"[Apify] Timed out after {wait_secs}s")
    return []


def run_actor_sync(actor_id: str, input_data: dict, timeout_secs: int = 120) -> list:
    """
    Run actor using Apify's synchronous endpoint (waits for result in single call).
    Better for quick actors (< 2 min).
    """
    if not APIFY_TOKEN:
        raise ValueError("APIFY_TOKEN environment variable not set")

    print(f"[Apify] Running actor (sync): {actor_id}")
    url = f"{APIFY_BASE}/acts/{actor_id}/run-sync-get-dataset-items?token={APIFY_TOKEN}&timeout={timeout_secs}"
    
    body = json.dumps(input_data).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=timeout_secs + 30) as resp:
            items = json.loads(resp.read().decode())
            print(f"[Apify] Got {len(items)} items (sync)")
            return items
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"[Apify] Sync run failed: HTTP {e.code}: {error_body[:300]}")
        return []
    except Exception as e:
        print(f"[Apify] Sync run error: {e}")
        return []
