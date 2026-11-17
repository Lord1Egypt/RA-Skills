"""twist — Observe and modify browser network requests/responses via CDP.

Usage:
    python -m twist --observe
    python -m twist --launch -c rules.json -u https://example.com
    python twist.py --list-targets

Or programmatically:
    from twist import TwistApp, Options, ObserveOptions
    app = TwistApp(Options(observe=ObserveOptions(enabled=True)))
    await app.run()
"""

from __future__ import annotations

from .app import Options, TwistApp  # noqa: F401
from .observe import ObserveOptions, ObserveFilter, parse_filter  # noqa: F401

__version__ = "1.1.0"
