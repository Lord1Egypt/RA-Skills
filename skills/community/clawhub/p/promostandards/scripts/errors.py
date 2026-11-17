"""Error types for the PromoStandards client.

The distinction that matters to a calling agent is *why* a call did not
produce data:

- `NotSupportedError` — this supplier does not publish this service (or
  this version of it). Structural, known before the call, never a retry.
- `ServiceMessageError` — the supplier answered, and said no. Carries the
  supplier's own code/description so the agent can decide.
- `TransportError` — the network or the endpoint failed. May be transient.
- `ConfigError` — our configuration is wrong or incomplete.

Nothing here is ever swallowed into an empty result: callers distinguish
"supplier returned zero rows" from "we could not ask".
"""

from __future__ import annotations


class PromoStandardsError(Exception):
    """Base for every error this package raises."""

    kind = "error"

    def as_dict(self) -> dict:
        return {"type": self.kind, "message": str(self)}


class ConfigError(PromoStandardsError):
    """Supplier config is missing, malformed, or lacks credentials."""

    kind = "config_error"


class NotSupportedError(PromoStandardsError):
    """The supplier does not offer this service/version/operation.

    Raised from configuration and registry data *before* a call goes out,
    so an agent never learns this by faulting mid-transaction.
    """

    kind = "not_supported"

    def __init__(
        self,
        message: str,
        *,
        supplier: str | None = None,
        service: str | None = None,
        version: str | None = None,
        available: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.supplier = supplier
        self.service = service
        self.version = version
        self.available = available or []

    def as_dict(self) -> dict:
        return {
            "type": self.kind,
            "message": str(self),
            "supplier": self.supplier,
            "service": self.service,
            "version": self.version,
            "available": self.available,
        }


class TransportError(PromoStandardsError):
    """HTTP/network failure, or a non-XML body where XML was promised."""

    kind = "transport_error"

    def __init__(self, message: str, *, status: int | None = None,
                 url: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.url = url

    def as_dict(self) -> dict:
        return {"type": self.kind, "message": str(self),
                "status": self.status, "url": self.url}


class SoapFaultError(PromoStandardsError):
    """The endpoint returned a SOAP Fault."""

    kind = "soap_fault"

    def __init__(self, message: str, *, code: str | None = None,
                 detail: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.detail = detail

    def as_dict(self) -> dict:
        return {"type": self.kind, "message": str(self),
                "code": self.code, "detail": self.detail}


class ServiceMessageError(PromoStandardsError):
    """The service answered with an error-severity ServiceMessage.

    Inventory 2.0.0 and Product Data 2.0.0 return a ServiceMessageArray;
    Inventory 1.2.1 returns a bare `errorMessage`. Both land here.
    """

    kind = "service_message"

    def __init__(self, message: str, *, code: str | None = None,
                 severity: str | None = None,
                 messages: list[dict] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.severity = severity
        self.messages = messages or []

    def as_dict(self) -> dict:
        return {"type": self.kind, "message": str(self), "code": self.code,
                "severity": self.severity, "messages": self.messages}


class EscalationRequired(PromoStandardsError):
    """A write failed in a state a human must resolve.

    Raised when `sendPO` fails in a way that leaves the order's fate
    ambiguous — submitted-but-unacknowledged, or rejected mid-transaction.
    Never retried automatically: a duplicate purchase order is worse than
    a late one.
    """

    kind = "escalation_required"

    def __init__(self, message: str, *, supplier: str | None = None,
                 po_number: str | None = None,
                 context: dict | None = None) -> None:
        super().__init__(message)
        self.supplier = supplier
        self.po_number = po_number
        self.context = context or {}

    def as_dict(self) -> dict:
        return {"type": self.kind, "message": str(self),
                "supplier": self.supplier, "po_number": self.po_number,
                "context": self.context, "action": "escalate_to_human"}
