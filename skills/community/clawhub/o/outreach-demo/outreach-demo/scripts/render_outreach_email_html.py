#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path
from load_sender_config import load_sender_config


def main():
    ap = argparse.ArgumentParser(description='Render lightweight HTML outreach email from structured JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    sender = load_sender_config()
    contact = html.escape(data.get('contact_name') or 'there')
    business = html.escape(data.get('business_name', ''))
    top = ''
    fits = data.get('openclaw_fits', [])
    if fits:
        top = html.escape(fits[0].get('use_case', ''))
    observations = data.get('website_observations', [])
    observation = html.escape(observations[0] if observations else 'I found a few concrete workflow opportunities worth testing.')
    body = f'''<!doctype html>
<html>
<body style="margin:0;padding:24px;background:#F8FAFC;font-family:Arial,Helvetica,sans-serif;color:#111827;">
  <div style="max-width:640px;margin:0 auto;background:#FFFFFF;border:1px solid #E5E7EB;border-radius:14px;overflow:hidden;box-shadow:0 8px 24px rgba(15,23,42,0.06);">
    <div style="padding:22px 24px;background:#0F172A;color:#FFFFFF;">
      <div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#DBEAFE;font-weight:700;">OpenClaw Opportunity Brief</div>
      <div style="font-size:24px;font-weight:700;margin-top:6px;">{business}</div>
    </div>
    <div style="padding:24px;">
      <p style="margin:0 0 14px 0;">Hi {contact},</p>
      <p style="margin:0 0 14px 0;line-height:1.55;">I pulled together a short <strong>OpenClaw Opportunity Brief</strong> for <strong>{business}</strong>.</p>
      <div style="margin:0 0 16px 0;padding:14px 16px;background:#F8FAFC;border:1px solid #E5E7EB;border-radius:10px;line-height:1.55;">
        <strong>One thing that stood out:</strong><br>{observation}
      </div>
      <div style="margin:0 0 16px 0;padding:16px;background:#DBEAFE;border:1px solid #93C5FD;border-radius:12px;">
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#2563EB;margin-bottom:10px;">Inside the brief</div>
        <ul style="margin:0;padding-left:18px;line-height:1.6;">
          <li>3 concrete OpenClaw opportunities</li>
          <li><strong>Priority move:</strong> {top}</li>
          <li>a simple live-demo angle</li>
        </ul>
      </div>
      <p style="margin:0 0 18px 0;line-height:1.55;">Attached if you want to skim it. If useful, I can walk through it live in 10 minutes.</p>
      <p style="margin:0;line-height:1.6;">Best,<br>{html.escape(sender['senderName'])}<br><span style="color:#6B7280;">{html.escape(sender['senderBrandLine'])}</span><br><span style="color:#6B7280;">{html.escape(sender['senderAccount'])}</span></p>
    </div>
  </div>
</body>
</html>
'''
    Path(args.output).write_text(body, encoding='utf-8')


if __name__ == '__main__':
    main()
