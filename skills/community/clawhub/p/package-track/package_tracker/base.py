"""Base interface for tracking providers."""

from abc import ABC, abstractmethod
from typing import Any


class BaseTracker(ABC):
    """Abstract base for all tracking providers."""

    @abstractmethod
    def track(
        self,
        shipper_code: str,
        logistic_code: str,
        order_code: str = "",
        customer_name: str = "",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Query tracking info for a single shipment.

        :param shipper_code: Courier code (e.g. SF, ZTO, YTO).
        :param logistic_code: Tracking number.
        :param order_code: Optional order reference.
        :param customer_name: Optional; for SF (顺丰), last 4 digits of phone.
        :return: Provider-specific dict with at least state and traces.
        """
        pass

