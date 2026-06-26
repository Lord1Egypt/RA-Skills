#!/usr/bin/env python3
"""Minimal PowerLego API client mirroring the frontend integration."""

from __future__ import annotations

import json
import os
import uuid
from typing import Dict, Iterable, List, Tuple
from urllib.parse import quote
from urllib.request import Request, urlopen


API_TOKEN_ENV = "POWERLEGO_API_TOKEN"
DEFAULT_HEADERS = {
    "Accept": "*/*",
    "Origin": "https://www.personalized.energy",
    "Referer": "https://www.personalized.energy/",
}

ADDRESS_VALIDATOR_API = "https://www.powerlego.com/ApiGateway/v1/address_validator"
USAGE_ESTIMATOR_API = "https://www.powerlego.com/ApiGateway/v1/usage_estimator"
GET_UTILITY_API = "https://www.powerlego.com/ApiGateway/v1/get_utility"
PLAN_API = "https://www.powerlego.com/ApiGateway/v2/commission/get_plan"
PERSONALIZED_ENERGY_BASE = "https://www.personalized.energy/electricity-rates/texas"


def _load_api_token() -> str:
    token = os.environ.get(API_TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(
            f"Missing {API_TOKEN_ENV}. Set it in the environment before calling the PowerLego API."
        )
    if token.lower().startswith("bearer "):
        return token
    return f"Bearer {token}"


def _encode_multipart_formdata(fields: Iterable[Tuple[str, str]]) -> Tuple[bytes, str]:
    boundary = f"----CodexBoundary{uuid.uuid4().hex}"
    lines: List[bytes] = []

    for name, value in fields:
        lines.extend(
            [
                f"--{boundary}".encode(),
                f'Content-Disposition: form-data; name="{name}"'.encode(),
                b"",
                str(value).encode(),
            ]
        )

    lines.append(f"--{boundary}--".encode())
    body = b"\r\n".join(lines) + b"\r\n"
    return body, boundary


def _post_form(url: str, fields: Iterable[Tuple[str, str]]) -> object:
    body, boundary = _encode_multipart_formdata(fields)
    headers = dict(DEFAULT_HEADERS)
    headers["Authorization"] = _load_api_token()
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    headers["Content-Length"] = str(len(body))

    request = Request(url, data=body, headers=headers, method="POST")
    with urlopen(request) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def address_validator(term: str) -> object:
    return _post_form(ADDRESS_VALIDATOR_API, [("term", term)])


def usage_estimator(address1: str, city: str, state: str, zipcode: str) -> object:
    return _post_form(
        USAGE_ESTIMATOR_API,
        [
            ("address1", address1),
            ("city", city),
            ("state", state),
            ("zipcode", zipcode),
        ],
    )


def get_utility(zipcode: str) -> object:
    return _post_form(GET_UTILITY_API, [("zipcode", zipcode)])


def get_plan(zipcode: str, utility_code: str, usage_data: Dict[str, float | int]) -> object:
    fields: List[Tuple[str, str]] = [
        ("zipcode", zipcode),
        ("utility_code", utility_code),
    ]

    for month in range(1, 13):
        usage = usage_data.get(str(month), 0)
        fields.append((f"usage[monthly][{month}]", str(usage)))

    fields.append(("filter[type]", "normal"))
    return _post_form(PLAN_API, fields)


def build_personalized_energy_url(city: str, zipcode: str, address1: str) -> str:
    city_slug = city.strip().lower()
    encoded_address = quote(address1.strip(), safe="")
    return f"{PERSONALIZED_ENERGY_BASE}/{city_slug}/{zipcode}/{encoded_address}"
