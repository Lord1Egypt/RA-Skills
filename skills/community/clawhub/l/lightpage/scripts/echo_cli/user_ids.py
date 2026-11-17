"""Public user references, independent of device and content UUIDs."""

import argparse
import re
import uuid


def user_reference(value):
    if re.fullmatch(r"[a-z0-9]{10}", value):
        return value
    try:
        return str(uuid.UUID(value))
    except ValueError:
        raise argparse.ArgumentTypeError("Use a 10-character UID or legacy user UUID") from None
