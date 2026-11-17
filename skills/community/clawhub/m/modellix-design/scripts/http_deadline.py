"""Bound authenticated REST socket I/O by one absolute monotonic deadline."""

from __future__ import annotations

import http.client
import math
import socket
from threading import Event, Lock, Thread
import time
import urllib.request


class HttpDeadline:
    def __init__(self, timeout_seconds):
        if not isinstance(timeout_seconds, (int, float)) or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("A positive finite HTTP deadline is required.")
        self.end = time.monotonic() + timeout_seconds
        self._stop = Event()
        self._lock = Lock()
        self._socket = None
        self._expired = False
        self._watcher = Thread(target=self._watch, name="modellix-rest-deadline", daemon=True)

    def __enter__(self):
        self._watcher.start()
        return self

    def __exit__(self, exc_type, exc, traceback):
        self._stop.set()
        self._watcher.join(timeout=0.2)
        with self._lock:
            self._socket = None
        self.remaining()
        return False

    def remaining(self):
        remaining = self.end - time.monotonic()
        if self._expired or remaining <= 0:
            raise TimeoutError("REST request exceeded its absolute deadline.")
        return remaining

    def bind(self, current_socket):
        # A timeout during TCP -> TLS replacement must also stop the new socket.
        with self._lock:
            self._socket = current_socket
            expired = self._expired
        if expired:
            self._shutdown(current_socket)
        self.remaining()

    def _watch(self):
        if self._stop.wait(max(0, self.end - time.monotonic())):
            return
        with self._lock:
            self._expired = True
            current_socket = self._socket
        self._shutdown(current_socket)

    @staticmethod
    def _shutdown(current_socket):
        if current_socket is not None:
            try:
                # close() on a buffered response can wait for the reader's lock.
                current_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

    def create_connection(self, address, timeout=None, source_address=None):
        host, port = address
        last_error = None
        # DNS uses the platform resolver. Recheck before connecting/sending if it
        # returns after the deadline; never start a late paid request.
        for family, kind, protocol, _, destination in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
            self.remaining()
            candidate = socket.socket(family, kind, protocol)
            try:
                candidate.settimeout(self.remaining())
                if source_address:
                    candidate.bind(source_address)
                self.bind(candidate)
                candidate.connect(destination)
                self.remaining()
                return candidate
            except OSError as error:
                candidate.close()
                last_error = error
        self.remaining()
        if last_error is not None:
            raise last_error
        raise OSError("REST host resolved to no usable addresses.")


class DeadlineHTTPConnection(http.client.HTTPConnection):
    def __init__(self, host, deadline, **kwargs):
        super().__init__(host, **kwargs)
        self._create_connection = deadline.create_connection


class DeadlineHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, deadline, **kwargs):
        super().__init__(host, **kwargs)
        self.deadline = deadline
        self._create_connection = deadline.create_connection

    def connect(self):
        # Keep HTTPConnection's proxy CONNECT handling, with its socket already
        # watched. Bind TLS before handshaking so a trickle cannot reset the cap.
        http.client.HTTPConnection.connect(self)
        server_hostname = self._tunnel_host or self.host
        self.sock = self._context.wrap_socket(self.sock, server_hostname=server_hostname, do_handshake_on_connect=False)
        self.deadline.bind(self.sock)
        self.sock.settimeout(self.deadline.remaining())
        self.sock.do_handshake()


class DeadlineHTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, deadline):
        super().__init__()
        self.deadline = deadline

    def http_open(self, request):
        return self.do_open(lambda host, **kwargs: DeadlineHTTPConnection(host, self.deadline, **kwargs), request)


class DeadlineHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, deadline, context=None):
        super().__init__(context=context)
        self.deadline = deadline

    def https_open(self, request):
        return self.do_open(lambda host, **kwargs: DeadlineHTTPSConnection(host, self.deadline, **kwargs), request, context=self._context)
