"""Browser driver implementations."""

from ..config import Config
from .base import BrowserDriver
from .webbridge import WebBridgeDriver

# Registry of available driver backends. Backend name -> driver class.
# This is the authoritative list of what is actually implemented: the CLI
# derives its --backend choices from it, so adding an entry here is all that is
# needed to expose a new backend. Do not advertise a backend anywhere else
# before it appears here.
DRIVER_REGISTRY = {
    "webbridge": WebBridgeDriver,
}


def create_driver(config: Config, suffix: str = "") -> BrowserDriver:
    """Create a driver instance for the configured backend.

    Unknown backend names fail closed. Falling back to WebBridge would let a
    caller believe it selected a backend that does not exist — for example via
    PERPLEXITY_DRIVER, which bypasses the CLI's choices check.
    """
    backend = config.driver_backend
    if backend not in DRIVER_REGISTRY:
        raise ValueError(
            "Unknown driver backend "
            f"{backend!r}; implemented backends: "
            f"{', '.join(sorted(DRIVER_REGISTRY))}"
        )
    cls = DRIVER_REGISTRY[backend]
    return cls(
        url=config.webbridge_url,
        session=config.make_session(suffix),
    )


__all__ = ["BrowserDriver", "WebBridgeDriver", "DRIVER_REGISTRY", "create_driver"]