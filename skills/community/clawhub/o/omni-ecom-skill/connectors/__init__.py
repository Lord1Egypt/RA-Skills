"""Port-and-adapter connector contracts for omni-ecom v1.5."""

from .contract import ConnectorError, ConnectorProtocol, canonical_hash
from .mock_platform import MockPlatformConnector

__all__ = ["ConnectorError", "ConnectorProtocol", "MockPlatformConnector", "canonical_hash"]
