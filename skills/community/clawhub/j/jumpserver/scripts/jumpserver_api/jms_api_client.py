from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import json
import warnings
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

warnings.filterwarnings(
    "ignore",
    message=r"urllib3 v2 only supports OpenSSL 1\.1\.1\+",
    module=r"urllib3(\..*)?",
)

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .jms_types import JumpServerAPIError


DEFAULT_TIMEOUT = 30
DEFAULT_PAGE_SIZE = 100
AUTHENTICATION_TOKEN_PATH = "/api/v1/authentication/auth/"


class JumpServerClient(object):
    def __init__(self, config, session=None, timeout=DEFAULT_TIMEOUT):
        self.config = config.validate(require_org_id=False)
        self.base_url = self.config.base_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout
        self._password_token = None
        if not self.config.verify_tls:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def health_check(self):
        return self.get("/api/health/")

    def list_paginated(self, path, params=None):
        results = []
        next_ref = path
        next_params = dict(params or {})
        follow_all = not any(key in next_params for key in ("limit", "offset"))
        if follow_all:
            next_params["limit"] = int(next_params.get("limit") or DEFAULT_PAGE_SIZE)

        while next_ref:
            payload = self.get(next_ref, params=next_params)
            next_params = None

            if isinstance(payload, list):
                results.extend(payload)
                break
            if isinstance(payload, dict) and isinstance(payload.get("results"), list):
                page_records = payload.get("results") or []
                results.extend(page_records)
                if not follow_all:
                    break
                next_ref = payload.get("next") or self._next_offset_ref(next_ref, len(page_records))
                if len(page_records) < int((payload.get("limit") or DEFAULT_PAGE_SIZE)):
                    break
                continue
            return payload

        return results

    def _next_offset_ref(self, path, page_size):
        raw = urlparse(self._absolute_url(path))
        query = dict(parse_qsl(raw.query, keep_blank_values=True))
        current_offset = int(query.get("offset") or 0)
        limit_value = int(query.get("limit") or page_size or DEFAULT_PAGE_SIZE)
        query["offset"] = str(current_offset + page_size)
        query["limit"] = str(limit_value)
        next_query = urlencode(query)
        return urlunparse(raw._replace(query=next_query))

    def options(self, path, params=None):
        return self._request("OPTIONS", path, params=params)

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, params=None, json_body=None):
        return self._request("POST", path, params=params, json_body=json_body)

    def put(self, path, params=None, json_body=None):
        return self._request("PUT", path, params=params, json_body=json_body)

    def patch(self, path, params=None, json_body=None):
        return self._request("PATCH", path, params=params, json_body=json_body)

    def delete(self, path, params=None, json_body=None):
        return self._request("DELETE", path, params=params, json_body=json_body)

    def _request(self, method, path, params=None, json_body=None):
        url = self._absolute_url(path)
        prepared = self._prepare_request(method, url, params=params, json_body=json_body)
        signed_path = self._signed_path(prepared.url)
        prepared.headers["Authorization"] = self._build_authorization_header(
            method=method,
            signed_path=signed_path,
            headers=prepared.headers,
        )
        response = self._send_prepared(prepared, method=method, signed_path=signed_path)
        return self._decode_response(response, method, signed_path)

    def _prepare_request(self, method, url, params=None, json_body=None):
        headers = {
            "Accept": "application/json",
            "Date": self._date_header(),
        }
        if self.config.org_id:
            headers["X-JMS-ORG"] = self.config.org_id
        request = requests.Request(
            method=method.upper(),
            url=url,
            params=params,
            json=json_body,
            headers=headers,
        )
        return self.session.prepare_request(request)

    def _send_prepared(self, prepared, *, method, signed_path):
        try:
            return self.session.send(
                prepared,
                verify=self.config.verify_tls,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise JumpServerAPIError(
                "Request failed: %s" % exc,
                method=method,
                path=signed_path,
            )

    def _build_authorization_header(self, method, signed_path, headers):
        if self.config.uses_access_key_auth():
            return self._authorization_header_hmac(
                method=method,
                signed_path=signed_path,
                headers=headers,
            )
        if self.config.uses_password_auth():
            return "Bearer %s" % self._password_bearer_token()
        raise JumpServerAPIError("No supported authentication credentials are configured.")

    def _password_bearer_token(self):
        if self._password_token:
            return self._password_token

        url = self._absolute_url(AUTHENTICATION_TOKEN_PATH)
        request = requests.Request(
            method="POST",
            url=url,
            data={
                "username": self.config.username,
                "password": self.config.password,
            },
            headers={"Accept": "application/json"},
        )
        prepared = self.session.prepare_request(request)
        response = self._send_prepared(
            prepared,
            method="POST",
            signed_path=self._signed_path(prepared.url),
        )
        payload = self._response_payload(response)
        if not response.ok:
            message = "JumpServer authentication failed"
            if isinstance(payload, dict):
                message = (
                    payload.get("detail")
                    or payload.get("msg")
                    or payload.get("error")
                    or payload.get("message")
                    or message
                )
            elif isinstance(payload, str) and payload.strip():
                message = payload.strip()
            raise JumpServerAPIError(
                message,
                status_code=response.status_code,
                method="POST",
                path=self._signed_path(prepared.url),
                details=payload,
            )
        if not isinstance(payload, dict) or not payload.get("token"):
            raise JumpServerAPIError(
                "JumpServer authentication response did not include a token.",
                status_code=response.status_code,
                method="POST",
                path=self._signed_path(prepared.url),
                details=payload,
            )
        self._password_token = str(payload.get("token"))
        return self._password_token

    def _absolute_url(self, path):
        if str(path).startswith("http://") or str(path).startswith("https://"):
            raw = urlparse(str(path))
            expected = urlparse(self.base_url)
            if raw.scheme != expected.scheme or raw.netloc != expected.netloc:
                raw = raw._replace(scheme=expected.scheme, netloc=expected.netloc)
                return urlunparse(raw)
            return str(path)
        return urljoin(self.base_url + "/", str(path).lstrip("/"))

    def _signed_path(self, url):
        parsed = urlparse(url)
        path = parsed.path or "/"
        if parsed.query:
            return "%s?%s" % (path, parsed.query)
        return path

    def _authorization_header_hmac(self, method, signed_path, headers):
        signed_headers = ["(request-target)", "accept", "date"]
        lines = ["(request-target): %s %s" % (method.lower(), signed_path)]
        for header in signed_headers[1:]:
            lines.append("%s: %s" % (header, headers[header.title()]))
        payload = "\n".join(lines)
        digest = hmac.new(
            self.config.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature = base64.b64encode(digest).decode("utf-8")
        return (
            'Signature keyId="%s",algorithm="hmac-sha256",headers="%s",signature="%s"'
            % (
                self.config.access_key,
                " ".join(signed_headers),
                signature,
            )
        )

    def _decode_response(self, response, method, signed_path):
        if response.status_code == 204 or not response.content:
            return None

        parsed = self._response_payload(response)
        if response.ok:
            return parsed

        message = "JumpServer API request failed"
        if isinstance(parsed, dict):
            message = (
                parsed.get("detail")
                or parsed.get("msg")
                or parsed.get("error")
                or parsed.get("message")
                or message
            )
        elif isinstance(parsed, str) and parsed.strip():
            message = parsed.strip()

        if response.status_code == 429:
            hint = "The request was throttled. Try a smaller time window, split the query into batches, or choose the correct command_storage_id before retrying."
            if message and hint not in message:
                message = "%s %s" % (message, hint)

        raise JumpServerAPIError(
            message,
            status_code=response.status_code,
            method=method,
            path=signed_path,
            details=parsed,
        )

    def _response_payload(self, response):
        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type.lower():
            try:
                return response.json()
            except ValueError:
                pass
        text = response.text
        if not text:
            return None
        try:
            return json.loads(text)
        except ValueError:
            return text

    def _date_header(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        return now.strftime("%a, %d %b %Y %H:%M:%S GMT")
