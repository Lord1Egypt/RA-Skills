from __future__ import annotations

import random
import string
from datetime import datetime


def generate_ref_code(length: int = 10) -> str:
    prefix = datetime.utcnow().strftime("%y%m")
    suffix_length = max(4, length - len(prefix))
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=suffix_length))
    return f"{prefix}{suffix}"
