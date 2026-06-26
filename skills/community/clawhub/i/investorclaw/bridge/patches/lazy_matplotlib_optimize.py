# SPDX-License-Identifier: Apache-2.0
"""Build-time patch: make matplotlib import lazy in ic_engine.commands.optimize.

ic_engine/commands/optimize.py has a module-level `from matplotlib import
pyplot as plt` that crashes at import time if matplotlib isn't installed.
For the v4.0 runtime image we strip matplotlib (only used for inline chart
rendering; the dashboard renders charts client-side). This patch makes the
import lazy so optimize.py imports cleanly.

Run as:  python3 lazy_matplotlib_optimize.py /path/to/site-packages
"""
from __future__ import annotations

import pathlib
import sys

OLD = "from matplotlib import pyplot as plt"
NEW = (
    "# matplotlib lazy-loaded; absent in mnemos-os/ic-engine runtime image\n"
    "try:\n"
    "    from matplotlib import pyplot as plt  # noqa: F401\n"
    "except ImportError:\n"
    "    plt = None  # type: ignore"
)


def main(site_packages: str) -> int:
    target = pathlib.Path(site_packages) / "ic_engine" / "commands" / "optimize.py"
    if not target.exists():
        print(f"FAIL: {target} not found", file=sys.stderr)
        return 1

    src = target.read_text()
    # Idempotency check FIRST — newer engine sources (commit 616b7a2+)
    # wrap the matplotlib import in try/except natively. If we detect the
    # signature ('try' + 'from matplotlib' + 'except ImportError' + 'plt
    # = None'), no-op. Doing this BEFORE the OLD-string check matters:
    # the OLD substring still matches inside the new try-block, so
    # blindly running .replace() would wrap a nested try with no body
    # and break Python parsing.
    already_lazy = (
        "try:" in src
        and "from matplotlib" in src
        and "except ImportError" in src
        and "plt = None" in src
    )
    if already_lazy:
        print(f"already lazy: {target} (no-op)")
        return 0
    if OLD not in src:
        print(f"FAIL: {target}: did not find expected import line", file=sys.stderr)
        return 1
    target.write_text(src.replace(OLD, NEW))
    print(f"patched: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
