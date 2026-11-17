"""LINK42 server-side SDK. Uses only the Python standard library."""
from .client import Link42, Link42Error, UploadError, TaskFailedError, PollTimeoutError, APIResponse

__all__ = ["Link42", "Link42Error", "UploadError", "TaskFailedError", "PollTimeoutError", "APIResponse"]
__version__ = "0.1.2"
