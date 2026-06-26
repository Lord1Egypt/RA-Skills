"""Detection providers for local and remote anonymization."""

from modeio_redact.providers.local_regex_provider import LocalRegexProvider
from modeio_redact.providers.remote_api_provider import RemoteApiProvider

__all__ = ["LocalRegexProvider", "RemoteApiProvider"]
