"""Shared skip marker: the runtime permission model (0600/0700, fcntl,
O_NOFOLLOW) is POSIX-only. The project targets Linux; on Windows these
tests would fail on NTFS semantics rather than on real defects."""
from __future__ import annotations

import os
import unittest

requires_posix = unittest.skipUnless(
    os.name == "posix", "POSIX permission model required (Linux/macOS)"
)

requires_fcntl = unittest.skipUnless(
    os.name == "posix", "inter-process meter locking requires fcntl (POSIX)"
)

