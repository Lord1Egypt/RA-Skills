#!/usr/bin/env python3
from security_guard import require_earl_write
require_earl_write("post_hemlane_maintenance_request_comment.py")
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = ROOT / 'references' / 'maintenance-request-comment.graphql'
REPLAY = ROOT / 'scripts' / 'replay_hemlane_graphql.py'

ap = argparse.ArgumentParser(description='Post a Hemlane maintenance request comment.')
ap.add_argument('--request-id', required=True)
ap.add_argument('--body', required=True)
ap.add_argument('--hide-from-tenants', action='store_true')
ap.add_argument('--hide-from-owners', action='store_true')
ap.add_argument('--dry-run', action='store_true')
ap.add_argument('--pretty', action='store_true')
args = ap.parse_args()

payload = {
    'input': {
        'maintenanceRequestId': args.request_id,
        'body': args.body,
        'isHiddenFromTenants': bool(args.hide_from_tenants),
        'isHiddenFromOwners': bool(args.hide_from_owners)
    }
}
tmp = Path('/tmp/hemlane_request_comment_variables.json')
tmp.write_text(json.dumps(payload))
cmd = [sys.executable, str(REPLAY), '--query', str(QUERY), '--variables', str(tmp), '--operation-name', 'OwnerDashboardMaintenanceMaintenanceRequestCommentCreate']
if args.dry_run:
    cmd.append('--dry-run')
if args.pretty:
    cmd.append('--pretty')
raise SystemExit(subprocess.call(cmd))
