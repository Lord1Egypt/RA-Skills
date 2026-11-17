"""Bounded HTTP transport using only the Python standard library."""

import json
import socket
import ssl
from contextlib import contextmanager
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_RESPONSE = 5 * 1024 * 1024


class TransportError(OSError):
    pass


class Headers(dict):
    def __init__(self, values=()):
        super().__init__()
        self.update(values)

    def __setitem__(self, name, value):
        super().__setitem__(name.lower(), value)

    def __getitem__(self, name):
        return super().__getitem__(name.lower())

    def __contains__(self, name):
        return super().__contains__(name.lower())

    def get(self, name, default=None):
        return super().get(name.lower(), default)

    def update(self, values=(), **kwargs):
        for name, value in dict(values, **kwargs).items():
            self[name] = value


class Response:
    def __init__(self, status_code, headers=(), content=b"", request=None):
        self.status_code = status_code
        self.headers = Headers(headers)
        self.content = content
        self.request = request

    def json(self):
        return json.loads(self.content.decode("utf-8"))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Stream(Response):
    def __init__(self, response, request):
        super().__init__(response.code, response.headers.items(), request=request)
        self.response = response
        length = self.headers.get("content-length")
        self.expected_size = int(length) if length and length.isdigit() else None
        if request.get_method() == "HEAD" or self.status_code in {204, 304}:
            self.expected_size = None

    def iter_bytes(self, chunk_size=65536):
        size = 0
        try:
            while True:
                chunk = self.response.read(chunk_size)
                if not chunk:
                    if self.expected_size is not None and size != self.expected_size:
                        raise TransportError("Incomplete network response")
                    return
                size += len(chunk)
                yield chunk
        except (OSError, ValueError, HTTPException) as exc:
            raise TransportError("Network response failed") from exc


class Client:
    def __init__(self, base_url="", timeout=20, follow_redirects=False):
        if follow_redirects:
            raise ValueError("Redirects are not supported")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = Headers()
        self.opener = build_opener(NoRedirect())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        pass

    @contextmanager
    def stream(self, method, path, timeout=None, headers=(), params=None, **kwargs):
        url = self.base_url + path if path.startswith("/") else path
        if params:
            # Match existing clients: omit absent query parameters.
            query = [(key, value) for key, value in params.items() if value is not None]
            url += ("&" if "?" in url else "?") + urlencode(query, doseq=True)
        merged = Headers(self.headers)
        merged.update(headers)
        body = kwargs.pop("content", None)
        if "json" in kwargs:
            body = json.dumps(kwargs.pop("json"), ensure_ascii=False).encode("utf-8")
            merged["Content-Type"] = "application/json"
        elif "data" in kwargs:
            body = urlencode(kwargs.pop("data")).encode("ascii")
            merged["Content-Type"] = "application/x-www-form-urlencoded"
        if kwargs:
            raise TypeError("Unsupported HTTP options: " + ", ".join(kwargs))
        merged["Accept-Encoding"] = "identity"
        request = Request(url, data=body, headers=dict(merged), method=method)
        response = None
        try:
            try:
                response = self.opener.open(request, timeout=timeout or self.timeout)
            except HTTPError as exc:
                # HTTP errors are responses; API owns retry and error translation.
                response = exc
            yield Stream(response, request)
        except (URLError, socket.timeout, ssl.SSLError, OSError, HTTPException) as exc:
            raise TransportError("Network request failed") from exc
        finally:
            if response is not None:
                response.close()

    def request(self, method, path, **kwargs):
        with self.stream(method, path, **kwargs) as streamed:
            chunks, size = [], 0
            for chunk in streamed.iter_bytes():
                size += len(chunk)
                if size > MAX_RESPONSE:
                    raise RuntimeError("Response exceeds 5 MiB")
                chunks.append(chunk)
            return Response(
                streamed.status_code, streamed.headers, b"".join(chunks), streamed.request
            )

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def head(self, path, **kwargs):
        return self.request("HEAD", path, **kwargs)
