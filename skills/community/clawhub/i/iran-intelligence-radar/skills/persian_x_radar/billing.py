from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error, parse, request

import yaml


SKILLPAY_API = "https://skillpay.me/api/v1"


def _config_path() -> Path:
    return Path(__file__).resolve().with_name("config.yaml")


def load_config() -> Dict[str, Any]:
    with _config_path().open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _billing_config() -> Dict[str, Any]:
    return load_config().get("billing", {})


def _logs_dir() -> Path:
    root = Path(__file__).resolve().parents[2]
    path = root / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_billing_logger() -> logging.Logger:
    logger = logging.getLogger("persian_x_radar.billing")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(_logs_dir() / "billing.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def _skillpay_base_url() -> str:
    return os.getenv("SKILLPAY_BASE_URL", SKILLPAY_API).rstrip("/")


def _request_json(
    method: str,
    endpoint: str,
    skill_id: str,
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 10,
) -> Dict[str, Any]:
    base = _skillpay_base_url()
    url = f"{base}{endpoint}"

    data = None
    headers = {
        "Content-Type": "application/json",
        "X-Skill-ID": skill_id,
    }

    if method.upper() == "GET" and payload:
        url = f"{url}?{parse.urlencode(payload)}"
    elif payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = request.Request(url=url, data=data, headers=headers, method=method.upper())

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {}
        return {
            "success": False,
            "error": f"http_{exc.code}",
            **parsed,
        }
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "success": False,
            "error": str(exc),
        }


def charge_user(user_id: str) -> Dict[str, Any]:
    billing = _billing_config()
    skill_id = str(billing.get("skill_id", ""))
    price = float(billing.get("price_per_call", 0.0))

    payload = {
        "user_id": user_id,
        "skill_id": skill_id,
        "amount": price,
    }
    response = _request_json("POST", "/billing/charge", skill_id=skill_id, payload=payload)

    if response.get("success") is True and response.get("charged") is True:
        return {
            "success": True,
            "charged": True,
            "price": price,
        }

    return {
        "success": False,
        "charged": False,
        "price": price,
        "payment_url": response.get("payment_url"),
        "error": response.get("error", "charge_failed"),
    }


def check_balance(user_id: str) -> Dict[str, Any]:
    skill_id = str(_billing_config().get("skill_id", ""))
    response = _request_json(
        "GET",
        "/billing/balance",
        skill_id=skill_id,
        payload={"user_id": user_id},
    )

    if response.get("success") is True:
        return response

    return {
        "success": False,
        "error": response.get("error", "balance_check_failed"),
        "payment_url": response.get("payment_url"),
    }
