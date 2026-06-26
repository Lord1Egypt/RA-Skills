from __future__ import annotations

import json
import sys
from typing import Any


def dump_json(data: Any) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
