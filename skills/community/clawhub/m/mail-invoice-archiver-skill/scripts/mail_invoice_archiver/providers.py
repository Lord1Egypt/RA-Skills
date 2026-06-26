from __future__ import annotations

from dataclasses import dataclass


APPLE_MAIL_IMAP_ID = '("name" "Apple Mail" "version" "16.0" "vendor" "Apple Inc." "os" "macOS")'


@dataclass(frozen=True, slots=True)
class MailProvider:
    id: str
    display_name: str
    domains: tuple[str, ...]
    host_candidates: tuple[str, ...]
    folders: tuple[str, ...] = ("INBOX",)
    imap_port: int = 993
    imap_client_id: str = ""
    send_imap_id: bool = False
    secret_label: str = "authorization code"
    notes: str = ""
    support_level: str = "implemented"
    verification: str = "docs-verified"


MAIL_PROVIDERS: dict[str, MailProvider] = {
    "126": MailProvider(
        id="126",
        display_name="126 Mail",
        domains=("126.com",),
        host_candidates=("appleimap.126.com", "imap.126.com"),
        imap_client_id=APPLE_MAIL_IMAP_ID,
        send_imap_id=True,
        secret_label="authorization code",
        notes="Live-tested in this workspace. appleimap.126.com is preferred in practice.",
        support_level="implemented",
        verification="live-tested",
    ),
    "163": MailProvider(
        id="163",
        display_name="163 Mail",
        domains=("163.com",),
        host_candidates=("imap.163.com",),
        imap_client_id=APPLE_MAIL_IMAP_ID,
        send_imap_id=True,
        secret_label="authorization code",
        notes="Implemented with the same Netease IMAP and authorization-code flow as 126. Not live-tested here yet.",
        support_level="implemented",
        verification="docs-verified",
    ),
    "gmail": MailProvider(
        id="gmail",
        display_name="Gmail",
        domains=("gmail.com", "googlemail.com"),
        host_candidates=("imap.gmail.com",),
        send_imap_id=False,
        secret_label="app password",
        notes=(
            "Implemented with IMAP app-password login for personal Gmail accounts. "
            "Google Workspace deployments may require OAuth or admin-side IMAP controls; "
            "that path is not implemented in this runtime yet."
        ),
        support_level="implemented",
        verification="docs-verified",
    ),
    "custom": MailProvider(
        id="custom",
        display_name="Custom IMAP",
        domains=(),
        host_candidates=(),
        send_imap_id=False,
        secret_label="mail password or provider-specific secret",
        notes="Manual IMAP host_candidates configuration is required.",
        support_level="manual",
        verification="user-configured",
    ),
}


def known_mail_provider_ids(*, include_auto: bool = False) -> tuple[str, ...]:
    ordered = tuple(MAIL_PROVIDERS)
    if include_auto:
        return ("auto",) + ordered
    return ordered


def detect_mail_provider(email_address: str | None) -> str:
    if not email_address or "@" not in email_address:
        return "custom"
    domain = email_address.rsplit("@", 1)[1].strip().lower()
    for provider in MAIL_PROVIDERS.values():
        if domain in provider.domains:
            return provider.id
    return "custom"


def normalize_mail_provider(provider_id: str | None, email_address: str | None = None) -> str:
    value = (provider_id or "").strip().lower()
    if not value or value == "auto":
        return detect_mail_provider(email_address)
    if value not in MAIL_PROVIDERS:
        raise RuntimeError(f"Unknown mail provider: {value}")
    return value


def get_mail_provider(provider_id: str | None, email_address: str | None = None) -> MailProvider:
    normalized = normalize_mail_provider(provider_id, email_address)
    return MAIL_PROVIDERS[normalized]


def default_system_service_name(provider_id: str | None, email_address: str | None = None) -> str:
    normalized = normalize_mail_provider(provider_id, email_address)
    return f"mail-invoice-archiver/{normalized}-auth"


def list_mail_providers() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for provider in MAIL_PROVIDERS.values():
        rows.append(
            {
                "id": provider.id,
                "display_name": provider.display_name,
                "domains": list(provider.domains),
                "host_candidates": list(provider.host_candidates),
                "secret_label": provider.secret_label,
                "support_level": provider.support_level,
                "verification": provider.verification,
                "notes": provider.notes,
            }
        )
    return rows
