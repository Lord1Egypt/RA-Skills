#!/usr/bin/env python3
from security_guard import require_earl_write
require_earl_write("submit_hemlane_referral.py")
import argparse, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERY = ROOT / 'references' / 'example-hubspot-submit.graphql'
VARS = ROOT / 'references' / 'example-hubspot-submit.variables.json'
REPLAY = ROOT / 'scripts' / 'replay_hemlane_graphql.py'

ap = argparse.ArgumentParser(description='Submit a Hemlane referral using the HAR-derived HubspotFormSubmit mutation.')
ap.add_argument('--first-name', required=True)
ap.add_argument('--last-name', required=True)
ap.add_argument('--phone', required=True)
ap.add_argument('--email', required=True)
ap.add_argument('--referrer-name', default=os.environ.get('HEMLANE_REFERRER_NAME', 'Earl Co (ECO Systems)'))
ap.add_argument('--referrer-email', default=os.environ.get('HEMLANE_REFERRER_EMAIL', 'ecosystemspm@gmail.com'))
ap.add_argument('--form-id', default=os.environ.get('HEMLANE_FORM_ID', '5e905969-3188-4c3a-ba74-519d43a39761'))
ap.add_argument('--page-uri', default='https://www.hemlane.com/dashboards/owner/')
ap.add_argument('--dry-run', action='store_true')
ap.add_argument('--pretty', action='store_true')
args = ap.parse_args()

payload = json.loads(VARS.read_text())
fields = payload['input']['fields']
mapv = {
    'firstname': args.first_name,
    'lastname': args.last_name,
    'phone': args.phone,
    'email': args.email,
    'referrername': args.referrer_name,
    'referreremail': args.referrer_email,
}
for f in fields:
    if f['name'] in mapv:
        f['value'] = mapv[f['name']]
payload['input']['formId'] = args.form_id
payload['input']['context']['pageUri'] = args.page_uri

tmp = Path('/tmp/hemlane_referral_variables.json')
tmp.write_text(json.dumps(payload))
cmd = [sys.executable, str(REPLAY), '--query', str(QUERY), '--variables', str(tmp), '--operation-name', 'HubspotFormSubmit']
if args.dry_run:
    cmd.append('--dry-run')
if args.pretty:
    cmd.append('--pretty')
raise SystemExit(subprocess.call(cmd))
