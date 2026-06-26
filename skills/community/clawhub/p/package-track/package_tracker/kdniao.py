"""
快递鸟 (Kdniao) tracking provider.
即时查询 API, RequestType 1002.
"""

import base64
import hashlib
import json
import urllib.parse
import urllib.request
from typing import Any

from package_tracker.base import BaseTracker

# 即时查询
KDNIAO_REQUEST_TYPE_TRACK = "1002"
KDNIAO_API_URL = "https://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx"
KDNIAO_SANDBOX_URL = "http://sandboxapi.kdniao.com:8080/kdniaosandbox/gateway/exterfaceInvoke.json"


def _make_data_sign(request_data_json: str, api_key: str) -> str:
    """DataSign = urlencode(base64_encode(md5(RequestData + ApiKey))). RequestData has no spaces."""
    raw = request_data_json + api_key
    md5_hex = hashlib.md5(raw.encode("utf-8")).hexdigest()
    b64 = base64.b64encode(md5_hex.encode("utf-8")).decode("utf-8")
    return urllib.parse.quote(b64)


def _request_body(
    ebusiness_id: str,
    api_key: str,
    shipper_code: str,
    logistic_code: str,
    request_type: str,
    order_code: str = "",
    customer_name: str = "",
) -> bytes:
    req_data = {
        "OrderCode": order_code or "",
        "ShipperCode": shipper_code,
        "LogisticCode": logistic_code,
    }
    if customer_name:
        req_data["CustomerName"] = customer_name
    # 无空格 JSON，与快递鸟签名规则一致
    request_data_json = json.dumps(req_data, separators=(",", ":"), ensure_ascii=False)
    data_sign = _make_data_sign(request_data_json, api_key)
    request_data_encoded = urllib.parse.quote(request_data_json)
    form = {
        "EBusinessID": ebusiness_id,
        "RequestType": request_type,
        "RequestData": request_data_encoded,
        "DataSign": data_sign,
        "DataType": "2",
    }
    return urllib.parse.urlencode(form).encode("utf-8")


class KdniaoTracker(BaseTracker):
    """快递鸟即时查询."""

    def __init__(
        self,
        ebusiness_id: str | None = None,
        api_key: str | None = None,
        sandbox: bool = False,
        request_type: str | None = None,
        api_url: str | None = None,
        sandbox_url: str | None = None,
    ):
        self.ebusiness_id = ebusiness_id or ""
        self.api_key = api_key or ""
        self.request_type = request_type or KDNIAO_REQUEST_TYPE_TRACK
        resolved_api_url = api_url or KDNIAO_API_URL
        resolved_sandbox_url = sandbox_url or KDNIAO_SANDBOX_URL
        self.base_url = resolved_sandbox_url if sandbox else resolved_api_url
        if not self.ebusiness_id or not self.api_key:
            raise ValueError(
                "Kdniao requires EBusinessID and ApiKey. "
                "Provide them via JSON config (providers.kdniao) or pass to constructor."
            )

    def track(
        self,
        shipper_code: str,
        logistic_code: str,
        order_code: str = "",
        customer_name: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        body = _request_body(
            self.ebusiness_id,
            self.api_key,
            shipper_code,
            logistic_code,
            request_type=self.request_type,
            order_code=order_code,
            customer_name=customer_name,
        )
        req = urllib.request.Request(
            self.base_url,
            data=body,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
        return json.loads(raw)

