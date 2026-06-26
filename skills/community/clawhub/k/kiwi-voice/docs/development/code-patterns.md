# Code Patterns

Conventions and patterns used throughout the Kiwi Voice codebase.

## Logging

Always use `kiwi_log()` — never bare `print()`:

```python
from kiwi.utils import kiwi_log

kiwi_log("TAG", "message", level="INFO")
# → [14:08:25.342] [INFO] [TAG] message
```

## Project Root Paths

Use `PROJECT_ROOT` for paths to project-level assets:

```python
from kiwi import PROJECT_ROOT
import os

path = os.path.join(PROJECT_ROOT, 'sounds', 'startup.mp3')
```

## i18n Strings

User-facing strings always go through `t()`. Developer-facing log messages do not:

```python
from kiwi.i18n import t

# User-facing — use t()
self._speak(t("responses.greeting"))
self._speak(t("responses.heard", command=cmd))

# Developer-facing — plain string
kiwi_log("TAG", "Internal log message", level="INFO")
```

Module-level constants are kept as fallback defaults. Instance attributes override them from i18n at init time:

```python
self.wake_word = t("wake_word.keyword") or WAKE_WORD
self.hallucination_phrases = set(t("hallucinations.phrases") or HALLUCINATION_PHRASES)
```

## Optional Module Loading

Modules with optional dependencies use try/except with availability flags:

```python
try:
    from kiwi.speaker_manager import SpeakerManager
    SPEAKER_MANAGER_AVAILABLE = True
except ImportError:
    SPEAKER_MANAGER_AVAILABLE = False
```

Then check the flag before using:

```python
if SPEAKER_MANAGER_AVAILABLE:
    self.speaker_manager = SpeakerManager()
```

## GPU Auto-Detection

CUDA is used when available, with automatic CPU fallback:

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

## Threading

All background work uses daemon threads with crash protection:

```python
import threading

thread = threading.Thread(target=self._worker, daemon=True)
thread.start()

def _worker(self):
    while self._running:
        try:
            # work
            pass
        except Exception as e:
            kiwi_log("WORKER", f"Error: {e}", level="ERROR")
            time.sleep(1)
            continue
```

Shared resources are guarded by `threading.Lock`:

```python
self._lock = threading.Lock()

with self._lock:
    self._cache[key] = value
```

## Windows UTF-8

Console codepage is set for Unicode output:

```python
import ctypes
ctypes.windll.kernel32.SetConsoleCP(65001)
```

## Tests

Run tests:

```bash
pytest tests/ -v
```

Smoke tests verify module imports and basic config loading:

```bash
pytest tests/test_smoke.py
```
