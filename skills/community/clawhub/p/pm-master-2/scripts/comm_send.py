#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master - Outbound Email Approval Gate (Communication Send Gate)
===================================================================

Formal email is an **external, irreversible, security-sensitive** action. This
script is a **hard approval gate + audit trail** in front of sending: it reads the
install-time policy (config.yaml at the skill root) and the project data
(project.yaml -> communication), and before delegating to a mail backend it
enforces:

  * whether email is enabled at all,
  * whether an approval is required and supplied by an authorized approver,
  * whether recipients are in the contact book,
  * whether external recipients require a sponsor co-signature.

Only after these pass does it invoke the selected backend (agent-mail / himalaya
/ gog / smtp) and write an audit entry to governance.communications[].

Security model (addresses ClawHub T09 / LP1):
  * Approval is NOT proven by the mere presence of a free-form string.
  * The approver identity must match an entry in the ADMIN-CONTROLLED allowlist
    only: `config.email.approvers` and `config.governance.approver_identities`.
    Authorization is NEVER derived from caller-modifiable project.yaml fields
    (project.pm / project.sponsor are data, not policy, and are explicitly
    excluded from the approver set).
  * The requester (who triggered the send) is recorded separately from the
    approver, and self-approval is forbidden by default.
  * There is no cryptographic token yet; the admin allowlist + separation of
    requester vs approver is the enforceable authorization boundary for a local
    CLI skill. Requester attribution may be supplied via `--requester` or, only
    when an administrator explicitly sets `config.email.trust_env_requester: true`,
    the `PM_MASTER_REQUESTER` environment variable. The requester identity is an
    UNTRUSTED audit label and never influences authorization.

Safe defaults:
  * requires_send_approval=true and no valid approver -> exit 1 (no send)
  * approval_override.require_sponsor_cosign=true with external recipients but
    approver not in sponsor_approvers -> exit 1
  * --dry-run: prints the would-be email + backend command, writes an audit
    record (status=dry-run), does NOT actually send.

Usage:
  # Resolve recipients by role (sponsor,pm -> looked up in communication.contacts[]),
  # then send after approval
  python3 comm_send.py --project <project>/project.yaml \
      --to "sponsor,pm" --subject "Milestone M2 achieved" --body-file draft.md \
      --approve "zhangsan(pm)" --requester "agent"

  # dry-run review (no real send)
  python3 comm_send.py --project <project>/project.yaml --to ops@example.com \
      --subject "Weekly report" --body-file draft.md --approve "zhangsan(pm)" --dry-run

  # external recipient + sponsor co-sign required
  python3 comm_send.py --project <project>/project.yaml --to client@external.example.com \
      --subject "Acceptance notice" --body-file draft.md --approve "lisi(sponsor)"
"""
import os
import re
import sys
import argparse
import subprocess
import datetime
import uuid
import tempfile

try:
    import yaml
except ImportError:
    yaml = None

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG = os.path.join(os.path.dirname(SCRIPT_DIR), 'config.yaml')


def load(path):
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def has(path):
    return os.path.exists(path)


def die(msg, code=1):
    print(f"x {msg}", file=sys.stderr)
    sys.exit(code)


# ---------- Recipient resolution ----------
def resolve_recipients(tokens, contacts):
    """tokens: comma-separated role names / names / emails.
    Returns (emails[], external_flags[])."""
    emails = []
    external = []
    known = {(str(c.get('role', '')).strip().lower(),
              str(c.get('name', '')).strip().lower(),
              str(c.get('email', '')).strip().lower())
             for c in (contacts or [])}
    known_emails = {e for (_, _, e) in known}
    for tok in [t.strip() for t in tokens.split(',') if t.strip()]:
        low = tok.lower()
        if '@' in tok:                      # explicit email
            emails.append(tok)
            external.append(tok.strip().lower() not in known_emails)
            continue
        hit = None
        for c in (contacts or []):
            if (str(c.get('role', '')).strip().lower() == low
                    or str(c.get('name', '')).strip().lower() == low):
                hit = c.get('email')
                break
        if hit:
            emails.append(hit)
            external.append(str(hit).strip().lower() not in known_emails)
        else:
            die(f"Unknown recipient (not in communication.contacts[] and not an email): {tok}")
    if not emails:
        die("Recipient list is empty")
    return emails, external


# ---------- Backend command construction ----------
def build_backend_cmd(backend, frm, to_csv, subject, body_file, smtp_cfg):
    """Return the backend CLI command list, or None for smtp (draft only)."""
    if backend == 'agent-mail':
        return ['agentmail', 'send', '--to', to_csv, '--subject', subject, '--body-file', body_file]
    if backend == 'himalaya':
        return ['himalaya', 'mail', 'send', '--from', frm, '--to', to_csv,
                '--subject', subject, '--body-file', body_file]
    if backend == 'gog':
        return ['gog', 'mail', 'send', '--to', to_csv, '--subject', subject, '--body-file', body_file]
    if backend == 'smtp':
        if not (smtp_cfg or {}).get('host'):
            die("backend=smtp but config.yaml has no smtp.host")
        # Generic SMTP has no inline CLI; produce an EML draft for the user's client
        return None
    die(f"Unknown mail backend: {backend} (use agent-mail/himalaya/gog/smtp)")


def _base_identity(value):
    """Normalize a stakeholder identity: drop a trailing (ROLE) qualifier and lowercase.

    'ZhangSan(PM)' -> 'zhangsan'  |  'LiSi(sponsor)' -> 'lisi'  |  'PM' -> 'pm'
    """
    text = re.sub(r'\(.*?\)', '', (value or '')).strip()
    return text.lower()


def resolve_approver(approve_arg, email_cfg, requester, data=None):
    """Enforce the allowlist-based authorization boundary (ClawHub T09-1 / AIG).

    Returns the normalized approver string, or None when no approval was given
    (the caller treats that as a dry-run / denied state).

    The authorized approver set is taken SOLELY from admin-controlled policy:
      * config.email.approvers, and
      * config.governance.approver_identities.

    Authorization is deliberately NOT derived from project.yaml (project.pm /
    project.sponsor). Those fields are caller-modifiable project data, not
    security policy; deriving approval authority from them would let anyone who
    can edit project.yaml self-authorize. Self-approval is forbidden by default.
    If the allowlist is empty (no admin has configured an approver) the send is
    rejected (fail-closed) rather than accepting any string.
    """
    approver = (approve_arg or '').strip()
    if not approver:
        return None
    allowlist = [_base_identity(x) for x in (email_cfg.get('approvers') or [])]
    allowlist += [_base_identity(x) for x in ((email_cfg.get('governance') or {}).get('approver_identities') or [])]
    # NOTE: project.pm / project.sponsor are intentionally excluded (caller data).
    allowlist = [x for x in allowlist if x]
    if not allowlist:
        die("No authorized approver configured (set config.email.approvers and/or "
            "config.governance.approver_identities). Refusing an unverifiable approval.")
    if _base_identity(approver) not in allowlist:
        die(f"Approver '{approver}' is not in the admin allowlist "
            f"(config.email.approvers / config.governance.approver_identities)")
    if (email_cfg.get('forbid_self_approval', True) and requester
            and _base_identity(approver) == (requester or '').strip().lower()):
        die("Self-approval forbidden: approver must differ from requester")
    return approver


def main():
    ap = argparse.ArgumentParser(
        description="PM Master outbound email approval gate (Communication Send Gate)")
    ap.add_argument('--project', required=True)
    ap.add_argument('--to', required=True,
                    help='Recipients: role name / person name (resolved from communication.contacts[]) or email, comma-separated')
    ap.add_argument('--subject', required=True)
    ap.add_argument('--body', help='Body (inline string)')
    ap.add_argument('--body-file', help='Body (file path, recommended for multi-line)')
    ap.add_argument('--cc', default='', help='Cc, same rules as --to')
    ap.add_argument('--approve', metavar='APPROVER', default=None,
                    help='Approver identity (must be in config.email.approvers / config.governance.approver_identities), e.g. "zhangsan"')
    ap.add_argument('--requester', default=None,
                    help='Identity that requested the send (recorded as an untrusted audit label); defaults to "agent"')
    ap.add_argument('--dry-run', action='store_true', help='Print + audit only, do not really send')
    ap.add_argument('--config', default=DEFAULT_CONFIG, help='Install-time policy file (skill root config.yaml)')
    a = ap.parse_args()

    # ---- Load policy and data ----
    if not has(a.project):
        die(f"project.yaml not found: {a.project}")
    if not has(a.config):
        die(f"Install-time config not found: {a.config} (create config.yaml at skill root defining email.*)")
    data = load(a.project)
    cfg = load(a.config) or {}
    email_cfg = cfg.get('email') or {}
    comm = data.get('communication') or {}

    # ---- Body content ----
    body = a.body
    if a.body_file:
        if not has(a.body_file):
            die(f"Body file not found: {a.body_file}")
        with open(a.body_file, 'r', encoding='utf-8') as f:
            body = f.read()
    if not body or not body.strip():
        die("Email body is empty (provide --body or --body-file)")

    # ---- Guardrail 1: capability switch ----
    if not email_cfg.get('enabled', False):
        die("Email is disabled (config.email.enabled=false, disabled at install time)")

    # ---- Recipient resolution ----
    contacts = comm.get('contacts') or []
    to_emails, to_ext = resolve_recipients(a.to, contacts)
    cc_emails, cc_ext = ([], []) if not a.cc else resolve_recipients(a.cc, contacts)
    external_any = any(to_ext) or any(cc_ext)

    # ---- Guardrail 2 & 3: approval + sponsor co-sign (allowlist-bound) ----
    # Requester attribution: only trust the environment if an admin explicitly
    # opts in (LP1 hardening). The requester is an UNTRUSTED audit label and is
    # never used for authorization.
    if email_cfg.get('trust_env_requester', False):
        requester = (a.requester or os.environ.get('PM_MASTER_REQUESTER') or 'agent').strip().lower()
    else:
        requester = (a.requester or 'agent').strip().lower()
    if email_cfg.get('requires_send_approval', True):
        if not a.approve:
            die("Approval required but not provided (config.email.requires_send_approval=true; pass --approve <approver>)")
    ov = comm.get('approval_override') or {}
    if ov.get('require_sponsor_cosign') and external_any:
        # Sponsor co-sign authority is admin policy only (config.email.sponsor_approvers);
        # project.yaml's declared sponsor is NOT trusted here (caller-modifiable).
        sponsor_allow = [_base_identity(x) for x in (email_cfg.get('sponsor_approvers') or [])]
        sponsor_allow = [x for x in sponsor_allow if x]
        if not (a.approve and _base_identity(a.approve) in sponsor_allow):
            die("External recipient(s) present and require_sponsor_cosign=true; "
                "approver must be in config.email.sponsor_approvers (admin-configured)")
    approver = resolve_approver(a.approve, email_cfg, requester, data)

    frm = comm.get('from') or email_cfg.get('default_from') or ''
    backend = email_cfg.get('backend', 'agent-mail')
    to_csv = ','.join(to_emails)
    cc_csv = ','.join(cc_emails)

    # ---- Show draft (for review) ----
    print("=== Email Draft (Communication Send Gate) ===")
    print(f"From    : {frm or '(unset, use backend default)'}")
    print(f"To      : {to_csv}")
    if cc_csv:
        print(f"Cc      : {cc_csv}")
    print(f"Subject : {a.subject}")
    print(f"Backend : {backend}  | Approver: {approver or '(none)'}")
    print("---- Body ----")
    print(body.strip())
    print("--------------")

    # ---- Audit record ----
    gov = data.setdefault('governance', {})
    log = gov.setdefault('communications', [])
    record = {
        'to': to_emails,
        'cc': cc_emails,
        'subject': a.subject,
        'on': datetime.date.today().isoformat(),
        'approved_by': approver,
        'requested_by': requester,
        'backend': backend,
        'status': 'dry-run' if a.dry_run else 'pending',
    }

    # ---- dry-run: audit only, no send ----
    if a.dry_run:
        record['status'] = 'dry-run'
        log.append(record)
        save(a.project, data)
        print("\n! --dry-run: not actually sent; audit record written (governance.communications).")
        sys.exit(0)

    if approver is None:
        die("Approval required before sending (no authorized approver supplied)")

    # ---- Real send: delegate to backend ----
    body_file = None
    try:
        tmp = tempfile.NamedTemporaryFile('w', suffix='.eml', delete=False, encoding='utf-8')
        tmp.write(body)
        tmp.close()
        body_file = tmp.name
        cmd = build_backend_cmd(backend, frm, to_csv, a.subject, body_file,
                                email_cfg.get('smtp'))
        if cmd is None:   # smtp has no CLI: write an EML draft, confined to artifacts/
            artifact_dir = os.path.realpath(os.path.join(
                os.path.dirname(os.path.abspath(a.project)), 'artifacts'))
            os.makedirs(artifact_dir, exist_ok=True)
            # T05 fix: never derive a filesystem path from the subject; sanitize + confine.
            safe = re.sub(r'[^A-Za-z0-9_\-]', '_', (a.subject or 'draft'))[:40]
            candidate = os.path.realpath(os.path.join(artifact_dir, f"draft_{safe}_{uuid.uuid4().hex[:8]}.eml"))
            if os.path.commonpath([artifact_dir, candidate]) != artifact_dir:
                die("Draft path escapes the artifact directory (path-traversal defense)")
            draft = candidate
            with open(draft, 'w', encoding='utf-8') as f:
                f.write(f"From: {frm}\nTo: {to_csv}\nCc: {cc_csv}\nSubject: {a.subject}\n\n{body}")
            record['status'] = 'draft-saved'
            record['draft'] = os.path.relpath(draft, os.path.dirname(os.path.abspath(a.project)))
            log.append(record)
            save(a.project, data)
            print(f"\n> EML draft generated (backend=smtp has no CLI): {record['draft']}; send via your mail client.")
            sys.exit(0)
        # Execute backend command
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if p.returncode == 0:
            record['status'] = 'sent'
            log.append(record)
            save(a.project, data)
            print(f"\nEmail sent (backend={backend}); audit written to governance.communications.")
            sys.exit(0)
        else:
            record['status'] = 'failed'
            record['error'] = (p.stdout + p.stderr).strip()[:500]
            log.append(record)
            save(a.project, data)
            die(f"Backend send failed ({backend} exit={p.returncode}): {record['error']}")
    except FileNotFoundError:
        record['status'] = 'failed'
        record['error'] = f'Backend CLI not found: {backend} (confirm the mail skill is installed/connected)'
        log.append(record)
        save(a.project, data)
        die(record['error'])
    finally:
        if body_file and os.path.exists(body_file):
            try:
                os.remove(body_file)
            except OSError:
                pass


if __name__ == '__main__':
    main()
