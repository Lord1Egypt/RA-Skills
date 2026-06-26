#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=1.27.0",
#   "docusign-esign>=6.1.0",
# ]
# ///
"""Local DocuSign MCP server exposed over stdio."""

from __future__ import annotations

import os

import docusign_esign as ds
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("docusign")

_BASE_URI = os.environ.get("MAVERICK_DOCUSIGN_MCP_BASE_URI", "https://demo.docusign.net/restapi")
_ACCOUNT_ID = os.environ.get("MAVERICK_DOCUSIGN_MCP_ACCOUNT_ID", "")
_ACCESS_TOKEN_ENV = "MAVERICK_DOCUSIGN_MCP_ACCESS_TOKEN"


def _bearer_token(ctx: Context) -> str:
    _ = ctx
    token = os.environ.get(_ACCESS_TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(f"{_ACCESS_TOKEN_ENV} is required")
    return token


def _api_client(access_token: str) -> ds.ApiClient:
    client = ds.ApiClient(host=_BASE_URI)
    client.set_default_header("Authorization", f"Bearer {access_token}")
    return client


def _account_id(client: ds.ApiClient, access_token: str) -> str:
    if _ACCOUNT_ID:
        return _ACCOUNT_ID
    info = client.get_user_info(access_token)
    for account in info.accounts or []:
        if getattr(account, "is_default", False):
            return account.account_id
    if info.accounts:
        return info.accounts[0].account_id
    raise RuntimeError("No DocuSign accounts found for this token")


@mcp.tool()
def list_envelopes(ctx: Context, from_date: str = "", status: str = "") -> dict:
    """List DocuSign envelopes. Optionally filter by from_date and status."""
    access_token = _bearer_token(ctx)
    client = _api_client(access_token)
    account_id = _account_id(client, access_token)
    api = ds.EnvelopesApi(client)
    kwargs: dict = {"from_date": from_date or "2020-01-01"}
    if status:
        kwargs["status"] = status
    result = api.list_status_changes(account_id, **kwargs)
    envelopes = []
    for envelope in result.envelopes or []:
        envelopes.append(
            {
                "envelope_id": envelope.envelope_id,
                "status": envelope.status,
                "subject": envelope.email_subject,
                "created": envelope.created_date_time,
                "sent": envelope.sent_date_time,
                "completed": envelope.completed_date_time,
            }
        )
    return {"envelopes": envelopes, "total": len(envelopes)}


@mcp.tool()
def get_envelope(ctx: Context, envelope_id: str) -> dict:
    """Get detailed status and metadata for a specific DocuSign envelope."""
    access_token = _bearer_token(ctx)
    client = _api_client(access_token)
    account_id = _account_id(client, access_token)
    api = ds.EnvelopesApi(client)
    envelope = api.get_envelope(account_id, envelope_id)
    return {
        "envelope_id": envelope.envelope_id,
        "status": envelope.status,
        "subject": envelope.email_subject,
        "created": envelope.created_date_time,
        "sent": envelope.sent_date_time,
        "delivered": envelope.delivered_date_time,
        "signed": envelope.signing_location,
        "completed": envelope.completed_date_time,
        "declined": envelope.declined_date_time,
        "voided": envelope.voided_date_time,
        "voided_reason": envelope.voided_reason,
    }


@mcp.tool()
def list_templates(ctx: Context, search_text: str = "") -> dict:
    """List available DocuSign templates."""
    access_token = _bearer_token(ctx)
    client = _api_client(access_token)
    account_id = _account_id(client, access_token)
    api = ds.TemplatesApi(client)
    kwargs: dict = {}
    if search_text:
        kwargs["search_text"] = search_text
    result = api.list_templates(account_id, **kwargs)
    templates = []
    for template in result.envelope_templates or []:
        templates.append(
            {
                "template_id": template.template_id,
                "name": template.name,
                "description": template.description,
                "created": template.created,
                "last_modified": template.last_modified,
            }
        )
    return {"templates": templates, "total": len(templates)}


@mcp.tool()
def get_template(ctx: Context, template_id: str) -> dict:
    """Get a DocuSign template definition including roles and documents."""
    access_token = _bearer_token(ctx)
    client = _api_client(access_token)
    account_id = _account_id(client, access_token)
    api = ds.TemplatesApi(client)
    template = api.get(account_id, template_id)
    roles = []
    for signer in (template.recipients.signers if template.recipients else []) or []:
        roles.append(
            {
                "role_name": signer.role_name,
                "name": signer.name,
                "email": signer.email,
                "routing_order": signer.routing_order,
            }
        )
    docs = []
    for document in template.documents or []:
        docs.append(
            {
                "document_id": document.document_id,
                "name": document.name,
                "file_extension": document.file_extension,
                "order": document.order,
            }
        )
    return {
        "template_id": template.template_id,
        "name": template.name,
        "description": template.description,
        "email_subject": template.email_subject,
        "roles": roles,
        "documents": docs,
    }


@mcp.tool()
def send_envelope_from_template(
    ctx: Context,
    template_id: str,
    email_subject: str,
    signers: list[dict[str, str]],
    email_blurb: str = "",
) -> dict:
    """Send a DocuSign envelope from a template."""
    access_token = _bearer_token(ctx)
    client = _api_client(access_token)
    account_id = _account_id(client, access_token)
    api = ds.EnvelopesApi(client)

    signer_objs = [
        ds.TemplateRole(
            role_name=signer["role_name"],
            name=signer["name"],
            email=signer["email"],
        )
        for signer in signers
    ]
    envelope_def = ds.EnvelopeDefinition(
        template_id=template_id,
        email_subject=email_subject,
        email_blurb=email_blurb,
        template_roles=signer_objs,
        status="sent",
    )
    result = api.create_envelope(account_id, envelope_definition=envelope_def)
    return {"envelope_id": result.envelope_id, "status": result.status, "uri": result.uri}


@mcp.tool()
def list_envelope_recipients(ctx: Context, envelope_id: str) -> dict:
    """List all recipients and their signing status for an envelope."""
    access_token = _bearer_token(ctx)
    client = _api_client(access_token)
    account_id = _account_id(client, access_token)
    api = ds.EnvelopesApi(client)
    result = api.list_recipients(account_id, envelope_id)
    signers = []
    for signer in result.signers or []:
        signers.append(
            {
                "name": signer.name,
                "email": signer.email,
                "status": signer.status,
                "signed": signer.signed_date_time,
                "delivered": signer.delivered_date_time,
                "routing_order": signer.routing_order,
            }
        )
    return {"signers": signers}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
