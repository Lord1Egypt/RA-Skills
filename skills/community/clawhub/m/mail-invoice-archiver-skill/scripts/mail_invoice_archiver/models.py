from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class InvoiceMetadata:
    invoice_number: str | None = None
    invoice_code: str | None = None
    amount_cents: int | None = None
    currency: str = "CNY"
    invoice_date: str | None = None
    vendor: str | None = None
    confidence: str = "low"
    extraction_sources: list[str] = field(default_factory=list)

    def merge(self, other: "InvoiceMetadata") -> "InvoiceMetadata":
        merged = InvoiceMetadata(
            invoice_number=other.invoice_number or self.invoice_number,
            invoice_code=other.invoice_code or self.invoice_code,
            amount_cents=other.amount_cents if other.amount_cents is not None else self.amount_cents,
            currency=other.currency or self.currency,
            invoice_date=other.invoice_date or self.invoice_date,
            vendor=other.vendor or self.vendor,
            confidence=other.confidence if other.confidence != "low" else self.confidence,
            extraction_sources=list(dict.fromkeys(self.extraction_sources + other.extraction_sources)),
        )
        return merged


@dataclass(slots=True)
class AttachmentPayload:
    part_ref: str
    filename: str
    content_type: str
    data: bytes
    source_kind: str = "attachment"
    source_ref: str | None = None

    @property
    def extension(self) -> str:
        if "." not in self.filename:
            return ""
        return self.filename.rsplit(".", 1)[-1].lower()


@dataclass(slots=True)
class ParsedMessage:
    uid: str
    account: str
    folder: str
    received_at: datetime | None
    sender: str
    subject: str
    preview: str
    body_text: str
    attachments: list[AttachmentPayload]


@dataclass(slots=True)
class SyncResult:
    month: str
    scanned_messages: int = 0
    canonical_saved: int = 0
    duplicates: int = 0
    conflicts: int = 0
    failures: int = 0
    link_failures: int = 0
    saved_paths: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DeliveryResult:
    month: str
    zip_path: str
    summary_path: str
    summary_json_path: str
