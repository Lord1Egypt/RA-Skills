"""Huawei Cloud APM 2.0 OpenAPI helpers."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.sdk_request import SdkRequest
from huaweicloudsdkcore.signer.signer import Signer

from .common import get_credentials_with_region


def _master_address(payload: Any) -> Optional[str]:
    if not isinstance(payload, dict):
        return None
    for key in ("master_address", "masterAddress"):
        if payload.get(key):
            return str(payload[key])
    for key in ("data", "result"):
        nested = _master_address(payload.get(key))
        if nested:
            return nested
    return None


def get_apm_master_address(
    region: str,
    auth_token: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve the APM 2.0 master PodLB address.

    The documented API accepts X-Auth-Token. When a token is unavailable, use
    standard Huawei Cloud AK/SK signing so the shared dispatcher remains useful
    in an AK/SK-only session.
    """
    token = auth_token or os.environ.get("HUAWEI_AUTH_TOKEN")
    host = f"apm.{region}.myhuaweicloud.com"
    resource_path = "/v1/apm2/openapi/systemmng/get-master-address"
    query_params = [("region_name", region)]
    headers: Dict[str, str] = {"Content-Type": "application/json"}
    url = f"https://{host}{resource_path}?region_name={region}"
    auth_mode = "x-auth-token"

    if token:
        headers["X-Auth-Token"] = token
    else:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        if not access_key or not secret_key:
            return {
                "success": False,
                "error": "HUAWEI_AUTH_TOKEN or Huawei Cloud AK/SK credentials are required",
            }
        request = SdkRequest(
            method="GET",
            schema="https",
            host=host,
            resource_path=resource_path,
            query_params=query_params,
            header_params={"Content-Type": "application/json", "X-Project-Id": proj_id or ""},
        )
        signed = Signer(BasicCredentials(access_key, secret_key, proj_id)).sign(request)
        url = f"{signed.schema}://{signed.host}{signed.uri}"
        headers = signed.header_params
        auth_mode = "ak-sk-signature"

    try:
        response = requests.get(url, headers=headers, verify=True, timeout=30)
        payload = response.json() if response.text else {}
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text[:500]}",
                "auth_mode": auth_mode,
            }
        address = _master_address(payload)
        if not address:
            return {
                "success": False,
                "error": "master_address was not present in the APM response",
                "auth_mode": auth_mode,
                "response": payload,
            }
        return {
            "success": True,
            "action": "get_apm_master_address",
            "region": region,
            "master_address": address,
            "auth_mode": auth_mode,
        }
    except requests.RequestException as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    except json.JSONDecodeError as exc:
        return {"success": False, "error": f"Invalid APM response JSON: {exc}"}
