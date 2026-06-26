# Logging: `log.py` Implementation

Dual-output logger: every agent writes to both stdout and a timestamped file under
`harness-logs/` in the project directory. One file per run. Never writes to `/tmp`.

---

## `harness/log.py` — Full Implementation

```python
from __future__ import annotations
import sys
import logging
from datetime import datetime
from pathlib import Path

_logger: logging.Logger | None = None


def setup(project_dir: Path, label: str = "run") -> None:
    """Call once at harness startup."""
    global _logger
    log_dir = project_dir / "harness-logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / f"{label}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    logger = logging.getLogger("harness")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fmt = logging.Formatter("%(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    _logger = logger
    logger.info(f"[Harness] Log → {log_path}")


def get() -> logging.Logger:
    """Return configured logger; falls back to stdout-only if setup() was never called."""
    if _logger is not None:
        return _logger
    logger = logging.getLogger("harness")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(ch)
    return logger
```

---

## Usage

```python
# harness.py — call setup() before any agent runs
import log
log.setup(PROJECT_DIR, label="run")

# Any agent file
import log
logger = log.get()
logger.info("  [Generator] Tool: Write")
```

`get()` is safe to call before `setup()` — it falls back to stdout only. This means
agents can call `log.get()` at module level without worrying about initialization order.
