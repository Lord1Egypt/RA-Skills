#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='Render approval preview manifest for outreach-demo artifacts.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--subject', required=True)
    ap.add_argument('--email-text', required=True)
    ap.add_argument('--email-html', required=True)
    ap.add_argument('--brief', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    preview = {
        'recipient': data.get('contact_email', ''),
        'contact_name': data.get('contact_name', ''),
        'business_name': data.get('business_name', ''),
        'subject': args.subject,
        'plainTextEmailPath': args.email_text,
        'htmlEmailPath': args.email_html,
        'attachedBriefPath': args.brief,
        'attachedBriefFilename': Path(args.brief).name,
        'sendMode': 'html+brief',
    }
    Path(args.output).write_text(json.dumps(preview, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
