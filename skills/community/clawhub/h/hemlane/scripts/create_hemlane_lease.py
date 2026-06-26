#!/usr/bin/env python3
"""Create a Hemlane lease agreement via GraphQL API."""
import argparse
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests required: pip install requests")
    sys.exit(1)

HEMLANE_API = "https://api.hemlane.com/graphql"

# GraphQL mutation for creating lease agreement
CREATE_LEASE_MUTATION = """
mutation ODCreateLeaseAgreement($input: LeaseAgreementCreateInput!) {
  leaseAgreementCreate(input: $input) {
    error
    leaseAgreement {
      createdAt
      createdByUser {
        id
        __typename
      }
      id
      status
      survey
      tenantGroup {
        id
        __typename
      }
      updatedAt
      __typename
    }
    __typename
  }
}
"""
from security_guard import require_earl_write
require_earl_write("create_hemlane_lease.py")

# GraphQL mutation for creating e-sign packet from lease
CREATE_ESIGN_MUTATION = """
mutation ODCreateLeaseAgreementTemplate($input: EsignDocumentCreateLeaseAgreementTemplateInput!) {
  esignDocumentCreateLeaseAgreementTemplate(input: $input) {
    error
    esignPacket {
      id
      sourceSignable {
        __typename
        ... on LeaseAgreement {
          id
          status
          __typename
        }
      }
      __typename
    }
    __typename
  }
}
"""


def load_auth(auth_file: str) -> dict:
    """Load auth headers from captured auth file."""
    with open(auth_file) as f:
        return json.load(f)


def create_lease_agreement(
    tenant_group_id: str,
    auth: dict,
    additional_disclosures: list = None,
    survey_data: dict = None
) -> dict:
    """Create a lease agreement for a tenant group."""
    headers = {
        "Content-Type": "application/json",
        "x-csrf-token": auth.get("x-csrf-token", ""),
        "cookie": auth.get("cookie", ""),
        "origin": auth.get("origin", "https://www.hemlane.com"),
        "referer": auth.get("referer", "https://www.hemlane.com/"),
        "user-agent": auth.get("user-agent", "Mozilla/5.0 OpenClaw Hemlane Skill"),
    }
    
    # Build survey input
    survey = {}
    if survey_data:
        survey.update(survey_data)
    if additional_disclosures:
        survey["additionalDisclosures"] = additional_disclosures
    
    variables = {
        "input": {
            "tenantGroupId": tenant_group_id,
        }
    }
    if survey:
        variables["input"]["survey"] = survey
    
    response = requests.post(
        HEMLANE_API,
        headers=headers,
        json={
            "operationName": "ODCreateLeaseAgreement",
            "query": CREATE_LEASE_MUTATION,
            "variables": variables,
        },
    )
    
    return response.json()


def create_esign_packet(
    lease_agreement_id: str,
    auth: dict
) -> dict:
    """Create an e-sign packet from a lease agreement."""
    headers = {
        "Content-Type": "application/json",
        "x-csrf-token": auth.get("x-csrf-token", ""),
        "cookie": auth.get("cookie", ""),
        "origin": auth.get("origin", "https://www.hemlane.com"),
        "referer": auth.get("referer", "https://www.hemlane.com/"),
        "user-agent": auth.get("user-agent", "Mozilla/5.0 OpenClaw Hemlane Skill"),
    }
    
    response = requests.post(
        HEMLANE_API,
        headers=headers,
        json={
            "operationName": "ODCreateLeaseAgreementTemplate",
            "query": CREATE_ESIGN_MUTATION,
            "variables": {
                "input": {
                    "leaseAgreementId": lease_agreement_id
                }
            },
        },
    )
    
    return response.json()


def main():
    ap = argparse.ArgumentParser(description="Create Hemlane lease agreement")
    ap.add_argument("--tenant-group-id", required=True, help="Tenant group ID")
    ap.add_argument("--auth-file", required=True, help="Path to auth JSON file")
    ap.add_argument("--disclosures", help="JSON file with additional disclosures")
    ap.add_argument("--survey", help="JSON file with survey data")
    ap.add_argument("--create-esign", action="store_true", help="Create e-sign packet after lease")
    ap.add_argument("--dry-run", action="store_true", help="Print mutation without executing")
    
    args = ap.parse_args()
    
    auth = load_auth(args.auth_file)
    
    # Load optional data
    additional_disclosures = None
    if args.disclosures:
        with open(args.disclosures) as f:
            additional_disclosures = json.load(f)
    
    survey_data = None
    if args.survey:
        with open(args.survey) as f:
            survey_data = json.load(f)
    
    if args.dry_run:
        print(f"Would create lease for tenant group: {args.tenant_group_id}")
        if additional_disclosures:
            print(f"With {len(additional_disclosures)} disclosures")
        print(json.dumps({
            "operationName": "ODCreateLeaseAgreement",
            "query": CREATE_LEASE_MUTATION[:200] + "...",
            "variables": {"input": {"tenantGroupId": args.tenant_group_id}}
        }, indent=2))
        return
    
    result = create_lease_agreement(
        args.tenant_group_id,
        auth,
        additional_disclosures,
        survey_data
    )
    
    if "errors" in result:
        print(f"Error: {result['errors']}")
        sys.exit(1)
    
    lease = result.get("data", {}).get("leaseAgreementCreate", {}).get("leaseAgreement", {})
    print(f"Created lease agreement: {lease.get('id')}")
    print(f"Status: {lease.get('status')}")
    
    if args.create_esign and lease.get("id"):
        esign_result = create_esign_packet(lease["id"], auth)
        if "errors" in esign_result:
            print(f"E-sign error: {esign_result['errors']}")
        else:
            packet = esign_result.get("data", {}).get("esignDocumentCreateLeaseAgreementTemplate", {}).get("esignPacket", {})
            print(f"Created e-sign packet: {packet.get('id')}")


if __name__ == "__main__":
    main()
