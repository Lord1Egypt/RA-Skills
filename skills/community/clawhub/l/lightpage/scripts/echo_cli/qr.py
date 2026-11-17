"""Generate a scan-ready PNG locally without third-party runtime packages."""

import os
import struct
import tempfile
import zlib
from pathlib import Path

from echo_cli.compat import unlink
from echo_cli.credentials import config_dir
from echo_cli.qrcodegen import QrCode


def png(uri):
    if len(uri.encode("utf-8")) > 2048:
        raise RuntimeError("URL exceeds the QR size limit")
    code = QrCode.encode_text(uri, QrCode.Ecc.MEDIUM)
    scale, border = 8, 4
    width = (code.get_size() + 2 * border) * scale
    rows = []
    for y in range(-border, code.get_size() + border):
        row = b"\x00" + bytes(
            0 if code.get_module(x, y) else 255
            for x in range(-border, code.get_size() + border)
            for _ in range(scale)
        )
        rows.extend([row] * scale)

    def chunk(kind, data):
        return (
            struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        )

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, width, 8, 0, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"".join(rows)))
        + chunk(b"IEND", b"")
    )


def create_login_qr(uri, *, directory=None):
    fd, filename = tempfile.mkstemp(prefix="login-", suffix=".png", dir=directory or config_dir())
    path = Path(filename)
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(png(uri))
    except BaseException:
        unlink(path)
        raise
    return path
