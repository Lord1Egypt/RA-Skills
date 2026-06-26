#!/usr/bin/env python3
"""HubSpot CRM CLI — contacts, deals, companies, activities, reports."""

import os
import sys
import json
import argparse
import requests
from datetime import datetime

BASE = "https://api.hubapi.com"


def get_headers():
    key = os.environ.get("HUBSPOT_API_KEY")
    if not key:
        print(json.dumps({
            "error": "HUBSPOT_API_KEY not set",
            "setup": "export HUBSPOT_API_KEY='pat-na1-xxxxxxxx-...'"
        }))
        sys.exit(1)
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def api(method, path, **kwargs):
    r = requests.request(method, BASE + path, headers=get_headers(), **kwargs)
    if r.status_code in (200, 201, 204):
        return r.json() if r.text else {"status": "ok"}
    print(json.dumps({"error": r.status_code, "detail": r.text}))
    sys.exit(1)


# ── CONTACTS ────────────────────────────────────────────

def contacts_list(args):
    r = api("GET", f"/crm/v3/objects/contacts?limit={args.limit}&properties=firstname,lastname,email,phone,company")
    out = [{"id": c["id"], **c["properties"]} for c in r.get("results", [])]
    print(json.dumps(out, indent=2))


def contacts_search(args):
    body = {"filterGroups": [{"filters": [
        {"propertyName": "email", "operator": "CONTAINS_TOKEN", "value": args.query}
    ]}], "properties": ["firstname", "lastname", "email", "phone", "company"]}
    r = api("POST", "/crm/v3/objects/contacts/search", json=body)
    out = [{"id": c["id"], **c["properties"]} for c in r.get("results", [])]
    print(json.dumps(out, indent=2))


def contacts_create(args):
    props = {}
    for k in ("email", "firstname", "lastname", "phone", "company"):
        v = getattr(args, k, None)
        if v:
            props[k] = v
    r = api("POST", "/crm/v3/objects/contacts", json={"properties": props})
    print(json.dumps({"id": r["id"], **r["properties"]}, indent=2))


def contacts_update(args):
    props = {}
    for k in ("phone", "jobtitle", "firstname", "lastname", "company", "email"):
        v = getattr(args, k, None)
        if v:
            props[k] = v
    r = api("PATCH", f"/crm/v3/objects/contacts/{args.id}", json={"properties": props})
    print(json.dumps({"id": r["id"], **r["properties"]}, indent=2))


def contacts_delete(args):
    api("DELETE", f"/crm/v3/objects/contacts/{args.id}")
    print(json.dumps({"deleted": args.id}))


# ── DEALS ───────────────────────────────────────────────

def deals_list(args):
    r = api("GET", f"/crm/v3/objects/deals?limit={args.limit}&properties=dealname,dealstage,amount,closedate,hubspot_owner_id")
    out = [{"id": d["id"], **d["properties"]} for d in r.get("results", [])]
    print(json.dumps(out, indent=2))


def deals_create(args):
    props = {"dealname": args.name, "dealstage": args.stage}
    if args.amount:
        props["amount"] = str(args.amount)
    r = api("POST", "/crm/v3/objects/deals", json={"properties": props})
    deal_id = r["id"]
    if args.contact_id:
        api("PUT", f"/crm/v3/associations/deals/contacts/batch/create",
            json={"inputs": [{"from": {"id": deal_id}, "to": {"id": args.contact_id},
                               "type": "deal_to_contact"}]})
    print(json.dumps({"id": deal_id, **r["properties"]}, indent=2))


def deals_update(args):
    props = {}
    if args.stage:
        props["dealstage"] = args.stage
    if args.amount:
        props["amount"] = str(args.amount)
    if args.name:
        props["dealname"] = args.name
    r = api("PATCH", f"/crm/v3/objects/deals/{args.id}", json={"properties": props})
    print(json.dumps({"id": r["id"], **r["properties"]}, indent=2))


def deals_move_stage(args):
    r = api("PATCH", f"/crm/v3/objects/deals/{args.id}", json={"properties": {"dealstage": args.stage}})
    print(json.dumps({"id": r["id"], "dealstage": r["properties"].get("dealstage")}, indent=2))


def pipeline_list(args):
    r = api("GET", "/crm/v3/pipelines/deals")
    for pipeline in r.get("results", []):
        stages = [{"id": s["id"], "label": s["label"], "probability": s.get("metadata", {}).get("probability")}
                  for s in pipeline.get("stages", [])]
        print(json.dumps({"pipeline": pipeline["label"], "id": pipeline["id"], "stages": stages}, indent=2))


# ── COMPANIES ───────────────────────────────────────────

def companies_create(args):
    props = {"name": args.name}
    if args.domain:
        props["domain"] = args.domain
    if args.industry:
        props["industry"] = args.industry
    r = api("POST", "/crm/v3/objects/companies", json={"properties": props})
    print(json.dumps({"id": r["id"], **r["properties"]}, indent=2))


def companies_search(args):
    body = {"filterGroups": [{"filters": [
        {"propertyName": "name", "operator": "CONTAINS_TOKEN", "value": args.query}
    ]}], "properties": ["name", "domain", "industry", "numberofemployees"]}
    r = api("POST", "/crm/v3/objects/companies/search", json=body)
    out = [{"id": c["id"], **c["properties"]} for c in r.get("results", [])]
    print(json.dumps(out, indent=2))


def companies_associate(args):
    body = {"inputs": [{"from": {"id": args.company_id}, "to": {"id": args.contact_id},
                        "type": "company_to_contact"}]}
    api("PUT", "/crm/v3/associations/companies/contacts/batch/create", json=body)
    print(json.dumps({"associated": {"company": args.company_id, "contact": args.contact_id}}))


# ── ACTIVITIES ──────────────────────────────────────────

def log_email(args):
    props = {
        "hs_timestamp": str(int(datetime.utcnow().timestamp() * 1000)),
        "hs_email_subject": args.subject,
        "hs_email_text": args.body,
        "hs_email_direction": "EMAIL",
        "hs_email_status": "SENT"
    }
    r = api("POST", "/crm/v3/objects/emails", json={"properties": props})
    aid = r["id"]
    api("PUT", "/crm/v3/associations/emails/contacts/batch/create",
        json={"inputs": [{"from": {"id": aid}, "to": {"id": args.contact_id}, "type": "email_to_contact"}]})
    print(json.dumps({"activity_id": aid, "type": "email", "subject": args.subject}))


def log_call(args):
    props = {
        "hs_timestamp": str(int(datetime.utcnow().timestamp() * 1000)),
        "hs_call_duration": str(args.duration * 1000),
        "hs_call_body": args.notes or "",
        "hs_call_status": "COMPLETED",
        "hs_call_direction": "OUTBOUND"
    }
    r = api("POST", "/crm/v3/objects/calls", json={"properties": props})
    aid = r["id"]
    api("PUT", "/crm/v3/associations/calls/contacts/batch/create",
        json={"inputs": [{"from": {"id": aid}, "to": {"id": args.contact_id}, "type": "call_to_contact"}]})
    print(json.dumps({"activity_id": aid, "type": "call", "duration_sec": args.duration}))


def log_meeting(args):
    props = {
        "hs_timestamp": str(int(datetime.utcnow().timestamp() * 1000)),
        "hs_meeting_title": args.title,
        "hs_meeting_body": args.notes or "",
        "hs_internal_meeting_notes": args.notes or ""
    }
    r = api("POST", "/crm/v3/objects/meetings", json={"properties": props})
    aid = r["id"]
    api("PUT", "/crm/v3/associations/meetings/contacts/batch/create",
        json={"inputs": [{"from": {"id": aid}, "to": {"id": args.contact_id}, "type": "meeting_to_contact"}]})
    print(json.dumps({"activity_id": aid, "type": "meeting", "title": args.title}))


def log_note(args):
    props = {
        "hs_timestamp": str(int(datetime.utcnow().timestamp() * 1000)),
        "hs_note_body": args.body
    }
    r = api("POST", "/crm/v3/objects/notes", json={"properties": props})
    aid = r["id"]
    api("PUT", "/crm/v3/associations/notes/contacts/batch/create",
        json={"inputs": [{"from": {"id": aid}, "to": {"id": args.contact_id}, "type": "note_to_contact"}]})
    print(json.dumps({"activity_id": aid, "type": "note"}))


# ── REPORTS ─────────────────────────────────────────────

def report_pipeline(args):
    deals = api("GET", "/crm/v3/objects/deals?limit=100&properties=dealname,dealstage,amount")
    stage_totals = {}
    for d in deals.get("results", []):
        stage = d["properties"].get("dealstage", "unknown")
        amount = float(d["properties"].get("amount") or 0)
        if stage not in stage_totals:
            stage_totals[stage] = {"count": 0, "total_value": 0}
        stage_totals[stage]["count"] += 1
        stage_totals[stage]["total_value"] += amount
    print(json.dumps(stage_totals, indent=2))


def report_conversions(args):
    pipelines = api("GET", "/crm/v3/pipelines/deals")
    deals = api("GET", "/crm/v3/objects/deals?limit=100&properties=dealstage")
    counts = {}
    for d in deals.get("results", []):
        s = d["properties"].get("dealstage", "unknown")
        counts[s] = counts.get(s, 0) + 1
    total = sum(counts.values()) or 1
    result = {stage: {"count": cnt, "pct": round(cnt / total * 100, 1)} for stage, cnt in counts.items()}
    print(json.dumps(result, indent=2))


# ── CLI ─────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="HubSpot CRM CLI")
    sub = p.add_subparsers(dest="cmd")

    # contacts-list
    cl = sub.add_parser("contacts-list")
    cl.add_argument("--limit", type=int, default=20)

    # contacts-search
    cs = sub.add_parser("contacts-search")
    cs.add_argument("--query", required=True)

    # contacts-create
    cc = sub.add_parser("contacts-create")
    cc.add_argument("--email", required=True)
    cc.add_argument("--firstname"); cc.add_argument("--lastname")
    cc.add_argument("--phone"); cc.add_argument("--company")

    # contacts-update
    cu = sub.add_parser("contacts-update")
    cu.add_argument("--id", required=True)
    cu.add_argument("--phone"); cu.add_argument("--jobtitle")
    cu.add_argument("--firstname"); cu.add_argument("--lastname")
    cu.add_argument("--company"); cu.add_argument("--email")

    # contacts-delete
    cd = sub.add_parser("contacts-delete")
    cd.add_argument("--id", required=True)

    # deals-list
    dl = sub.add_parser("deals-list")
    dl.add_argument("--limit", type=int, default=20)

    # deals-create
    dc = sub.add_parser("deals-create")
    dc.add_argument("--name", required=True)
    dc.add_argument("--stage", required=True)
    dc.add_argument("--amount", type=float)
    dc.add_argument("--contact-id")

    # deals-update
    du = sub.add_parser("deals-update")
    du.add_argument("--id", required=True)
    du.add_argument("--stage"); du.add_argument("--amount", type=float); du.add_argument("--name")

    # deals-move-stage
    dms = sub.add_parser("deals-move-stage")
    dms.add_argument("--id", required=True)
    dms.add_argument("--stage", required=True)

    # pipeline-list
    sub.add_parser("pipeline-list")

    # companies-create
    comc = sub.add_parser("companies-create")
    comc.add_argument("--name", required=True)
    comc.add_argument("--domain"); comc.add_argument("--industry")

    # companies-search
    coms = sub.add_parser("companies-search")
    coms.add_argument("--query", required=True)

    # companies-associate
    coma = sub.add_parser("companies-associate")
    coma.add_argument("--company-id", required=True, dest="company_id")
    coma.add_argument("--contact-id", required=True, dest="contact_id")

    # log-email
    le = sub.add_parser("log-email")
    le.add_argument("--contact-id", required=True, dest="contact_id")
    le.add_argument("--subject", required=True); le.add_argument("--body", default="")

    # log-call
    lc = sub.add_parser("log-call")
    lc.add_argument("--contact-id", required=True, dest="contact_id")
    lc.add_argument("--duration", type=int, default=0)
    lc.add_argument("--notes", default="")

    # log-meeting
    lm = sub.add_parser("log-meeting")
    lm.add_argument("--contact-id", required=True, dest="contact_id")
    lm.add_argument("--title", required=True); lm.add_argument("--notes", default="")

    # log-note
    ln = sub.add_parser("log-note")
    ln.add_argument("--contact-id", required=True, dest="contact_id")
    ln.add_argument("--body", required=True)

    # reports
    sub.add_parser("report-pipeline")
    sub.add_parser("report-conversions")

    args = p.parse_args()
    dispatch = {
        "contacts-list": contacts_list, "contacts-search": contacts_search,
        "contacts-create": contacts_create, "contacts-update": contacts_update,
        "contacts-delete": contacts_delete,
        "deals-list": deals_list, "deals-create": deals_create,
        "deals-update": deals_update, "deals-move-stage": deals_move_stage,
        "pipeline-list": pipeline_list,
        "companies-create": companies_create, "companies-search": companies_search,
        "companies-associate": companies_associate,
        "log-email": log_email, "log-call": log_call,
        "log-meeting": log_meeting, "log-note": log_note,
        "report-pipeline": report_pipeline, "report-conversions": report_conversions,
    }
    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
