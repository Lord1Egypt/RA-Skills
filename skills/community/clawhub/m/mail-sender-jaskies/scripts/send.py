import smtplib
from email.mime.text import MIMEText
import argparse
import os

def send_email(smtp_server, smtp_port, smtp_user, smtp_pass, from_email, to_email, subject, body):
    try:
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email via SMTP.")
    parser.add_argument("--smtp-server", default=os.getenv("SMTP_SERVER"), help="SMTP server address")
    parser.add_argument("--smtp-port", default=os.getenv("SMTP_PORT", 587), type=int, help="SMTP port")
    parser.add_argument("--smtp-user", default=os.getenv("SMTP_USER"), help="SMTP username")
    parser.add_argument("--smtp-pass", default=os.getenv("SMTP_PASS"), help="SMTP password")
    parser.add_argument("--from-email", default=os.getenv("FROM_EMAIL"), help="Sender email address")
    parser.add_argument("--to-email", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body content")

    args = parser.parse_args()

    # Check for required args if env vars aren't set
    if not args.smtp_server or not args.smtp_user or not args.smtp_pass:
        print("Error: Missing SMTP configuration (server, user, or pass). Use environment variables or arguments.")
        exit(1)

    send_email(
        args.smtp_server,
        args.smtp_port,
        args.smtp_user,
        args.smtp_pass,
        args.from_email or args.smtp_user,
        args.to_email,
        args.subject,
        args.body
    )
