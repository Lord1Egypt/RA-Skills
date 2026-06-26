from __future__ import annotations

import requests

from ima_runtime.shared.seedance_capabilities import requires_seedance_compliance
from ima_runtime.shared.types import PreparedMediaAsset


class AssetVerificationError(RuntimeError):
    """Raised when compliance verification fails."""


def verify_asset(base_url: str, api_key: str, asset_url: str, asset_name: str | None = None) -> dict:
    url = f"{base_url}/open/v1/assets/verify"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "IMA-OpenAPI-Client/ima-video-ai",
        "x-app-source": "ima_skills",
        "x_app_language": "en",
    }
    payload = {"url": asset_url}
    if asset_name:
        payload["name"] = asset_name[:64]

    response = requests.post(url, json=payload, headers=headers, timeout=300)
    try:
        data = response.json()
    except ValueError as exc:
        raise AssetVerificationError(f"Verification API returned non-JSON response (HTTP {response.status_code})") from exc

    code = data.get("code")
    if code not in (0, 200):
        message = data.get("message") or "Unknown error"
        raise AssetVerificationError(f"Verification API error: code={code}, msg={message}")

    return (data.get("data") or {}).get("result", {})


def check_verification_result(result: dict, asset_name: str) -> None:
    status = str(result.get("status") or "").lower()
    if status in {"active", "success"}:
        return
    if status == "failed":
        error_info = result.get("error") or {}
        error_msg = error_info.get("message") or "Unknown error"
        raise AssetVerificationError(f"Asset verification failed for {asset_name}: {error_msg}")
    if status in {"processing", "pending"}:
        raise AssetVerificationError(f"Asset verification still processing for {asset_name}.")
    raise AssetVerificationError(f"Unknown verification status for {asset_name}: {status or '<empty>'}")


def ensure_assets_verified(base_url: str, api_key: str, task_type: str, model_id: str | None, media_assets: tuple[PreparedMediaAsset, ...]) -> None:
    if not requires_seedance_compliance(task_type, model_id):
        return
    for asset in media_assets:
        result = verify_asset(base_url, api_key, asset.url, asset.source)
        check_verification_result(result, asset.source)
