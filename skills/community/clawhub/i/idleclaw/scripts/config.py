"""Shared configuration for IdleClaw skill scripts."""

import os
import re
import sys

DEFAULT_SERVER = "https://api.idleclaw.com"
MODEL_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9.:\-]*$")


def get_server_url() -> str:
    """Read and validate the server URL from environment."""
    url = os.environ.get("IDLECLAW_SERVER", DEFAULT_SERVER)
    if not re.match(r"^https?://", url):
        print(f"Warning: IDLECLAW_SERVER '{url}' is not an HTTP/HTTPS URL. Using default: {DEFAULT_SERVER}", file=sys.stderr)
        return DEFAULT_SERVER
    return url.rstrip("/")


def validate_model_name(model: str) -> str:
    """Validate a model name. Exits on invalid input."""
    if not model or not MODEL_PATTERN.match(model):
        print(f"Error: Invalid model name '{model}'. Only alphanumeric characters, colons, periods, and hyphens are allowed.", file=sys.stderr)
        sys.exit(1)
    return model
