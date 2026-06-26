#!/usr/bin/env python3
from security_guard import require_earl_write
require_earl_write("send_hemlane_tenant_reply.py")
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = ROOT / 'references' / 'tenant-reply.graphql'
REPLAY = ROOT / 'scripts' / 'replay_hemlane_graphql.py'

ap = argparse.ArgumentParser(description='Send a Hemlane tenant reply using the HAR-derived tenantGroupMessageAdd2 mutation.')
ap.add_argument('--tenant-group-id', required=True)
ap.add_argument('--body', required=True)
ap.add_argument('--notify-immediately', action='store_true', default=True)
ap.add_argument('--owner-private', action='store_true', default=False)
ap.add_argument('--attachment-url', default=None)
ap.add_argument('--dry-run', action='store_true')
ap.add_argument('--pretty', action='store_true')
args = ap.parse_args()

payload = {
    'input': {
        'tenantGroupId': args.tenant_group_id,
        'body': args.body,
        'notifyImmediately': bool(args.notify_immediately),
        'isOwnerPrivate': bool(args.owner_private),
        'attachmentUrl': args.attachment_url,
    }
}

tmp = Path('/tmp/hemlane_tenant_reply_variables.json')
tmp.write_text(json.dumps(payload))
cmd = [sys.executable, str(REPLAY), '--query', str(QUERY), '--variables', str(tmp), '--operation-name', 'ODProspectiveTenantGroupMessageCreate']
if args.dry_run:
    cmd.append('--dry-run')
if args.pretty:
    cmd.append('--pretty')
raise SystemExit(subprocess.call(cmd))
