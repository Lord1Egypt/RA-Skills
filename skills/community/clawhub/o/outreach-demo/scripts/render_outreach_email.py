#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from load_sender_config import load_sender_config


def main():
    ap = argparse.ArgumentParser(description='Render outreach email draft from structured JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    sender = load_sender_config()
    top = ''
    fits = data.get('openclaw_fits', [])
    if fits:
        top = fits[0].get('use_case', '')
    contact = data.get('contact_name') or 'there'
    business = data.get('business_name', '')
    business_line = business if str(business).rstrip().endswith(('.', '!', '?')) else f"{business}."
    observations = data.get('website_observations', [])
    observation = observations[0] if observations else 'I found a few concrete workflow opportunities worth testing.'

    body = (
        f"Hi {contact},\n\n"
        f"I pulled together a short OpenClaw Opportunity Brief for {business_line}\n\n"
        f"One thing that stood out: {observation}\n\n"
        "Inside:\n"
        "- 3 concrete OpenClaw opportunities\n"
        f"- the priority move I would test first: {top}\n"
        "- a simple live-demo angle\n\n"
        "Attached if you want to skim it. If useful, I can walk through it live in 10 minutes.\n\n"
        "Best,\n"
        f"{sender['senderName']}\n"
        f"{sender['senderBrandLine']}\n"
        f"{sender['senderAccount']}\n"
    )
    Path(args.output).write_text(body, encoding='utf-8')


if __name__ == '__main__':
    main()
