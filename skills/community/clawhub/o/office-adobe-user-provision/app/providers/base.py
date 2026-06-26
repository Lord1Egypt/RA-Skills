from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ProviderBase(ABC):
    """Common interface for account providers."""

    name: str = ""

    @abstractmethod
    def init_metadata(self) -> Dict[str, Any]:
        """Run connectivity checks and return metadata, including products."""

    @abstractmethod
    def list_products(self) -> List[Dict[str, Any]]:
        """Return cached/queried product list."""

    @abstractmethod
    def create_user(self, identifier: str, product: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Create user and optionally assign product/license."""

    @abstractmethod
    def assign_product(self, identifier: str, product: str) -> Dict[str, Any]:
        """Assign additional product/license to existing user."""

    @abstractmethod
    def reset_password(self, identifier: str, **kwargs) -> Dict[str, Any]:
        """Reset password for user."""

    @abstractmethod
    def delete_user(self, identifier: str) -> Dict[str, Any]:
        """Delete user."""

    @abstractmethod
    def describe_user(self, identifier: str) -> Dict[str, Any]:
        """Return user summary/inventory."""

    def self_test(self, **kwargs) -> Dict[str, Any]:
        """Optional: run provider-specific diagnostics."""
        raise NotImplementedError("当前 provider 不支持自检")
