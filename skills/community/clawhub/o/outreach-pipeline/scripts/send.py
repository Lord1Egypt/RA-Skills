import csv
import os
import sys
import time
import argparse
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

try:
    import requests
except ImportError:
    requests = None

TEMPLATE_VARS = {}

def load_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if not r.get('email'):
                continue
            rows.append(r)
    return rows


def render(text, ctx):
    out = text
    for k, v in ctx.items():
        out = out.replace('{{'+k+'}}', str(v) if v is not None else '')
    # remove unreplaced vars
    # crude cleanup for patterns like {{var}}
    import re
    out = re.sub(r"\{\{[^}]+\}\}", '', out)
    return out


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def send_smtp(args, to_email, subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = formataddr((args.from_name, args.from_email))
    msg['To'] = to_email
    msg['Subject'] = subject

    with smtplib.SMTP(args.smtp_host, args.smtp_port) as server:
        server.starttls()
        server.login(args.smtp_user, args.smtp_pass)
        server.sendmail(args.from_email, [to_email], msg.as_string())


def send_sendgrid(args, to_email, subject, body):
    if requests is None:
        raise RuntimeError('requests not installed; run: uv pip install requests')
    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        raise RuntimeError('SENDGRID_API_KEY not set')
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": args.from_email, "name": args.from_name},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}]
    }
    r = requests.post('https://api.sendgrid.com/v3/mail/send', json=payload, headers={'Authorization': f'Bearer {api_key}'})
    if r.status_code >= 300:
        raise RuntimeError(f'SendGrid error: {r.status_code} {r.text}')


def send_mailgun(args, to_email, subject, body):
    if requests is None:
        raise RuntimeError('requests not installed; run: uv pip install requests')
    api_key = os.environ.get('MAILGUN_API_KEY')
    domain = os.environ.get('MAILGUN_DOMAIN')
    if not api_key or not domain:
        raise RuntimeError('MAILGUN_API_KEY/MAILGUN_DOMAIN not set')
    r = requests.post(f'https://api.mailgun.net/v3/{domain}/messages', auth=('api', api_key), data={
        'from': f"{args.from_name} <{args.from_email}>",
        'to': [to_email],
        'subject': subject,
        'text': body
    })
    if r.status_code >= 300:
        raise RuntimeError(f'Mailgun error: {r.status_code} {r.text}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--csv', required=True)
    p.add_argument('--template', required=True)
    p.add_argument('--subject', required=True)
    p.add_argument('--from-name', dest='from_name', required=True)
    p.add_argument('--from-email', dest='from_email', required=True)
    p.add_argument('--provider', choices=['smtp','sendgrid','mailgun'], required=True)
    p.add_argument('--smtp-host')
    p.add_argument('--smtp-port', type=int, default=587)
    p.add_argument('--smtp-user')
    p.add_argument('--smtp-pass')
    p.add_argument('--rate-limit', type=int, default=10, help='per minute')
    p.add_argument('--max-per-run', type=int, default=0, help='0 = no limit')
    p.add_argument('--out-log', default='send_results.csv')
    args = p.parse_args()

    rows = load_csv(args.csv)
    template = read_file(args.template)
    sent = 0

    with open(args.out_log, 'w', newline='', encoding='utf-8') as outf:
        writer = csv.writer(outf)
        writer.writerow(['email','status','error'])
        start = time.time()
        interval = 60 / max(1, args.rate_limit)

        for r in rows:
            ctx = dict(r)
            ctx.setdefault('from_name', args.from_name)
            ctx.setdefault('from_email', args.from_email)
            subj = render(args.subject, ctx)
            body = render(template, ctx)
            to_email = r['email']
            try:
                if args.provider == 'smtp':
                    if not all([args.smtp_host, args.smtp_user, args.smtp_pass]):
                        raise RuntimeError('Missing SMTP config')
                    send_smtp(args, to_email, subj, body)
                elif args.provider == 'sendgrid':
                    send_sendgrid(args, to_email, subj, body)
                elif args.provider == 'mailgun':
                    send_mailgun(args, to_email, subj, body)
                writer.writerow([to_email,'sent',''])
                sent += 1
            except Exception as e:
                writer.writerow([to_email,'error',str(e)])
            # rate limiting
            time.sleep(interval)
            if args.max_per_run and sent >= args.max_per_run:
                break

    print(f'Done. Sent: {sent}. Log: {args.out_log}')

if __name__ == '__main__':
    main()
