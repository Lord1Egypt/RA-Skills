# Running as a systemd service

## 1. Create env file

```bash
cat > /etc/imap-mail.env <<EOF
MAIL_IMAP_HOST=mail.example.com
MAIL_IMAP_PORT=993
MAIL_SMTP_HOST=mail.example.com
MAIL_SMTP_PORT=465
MAIL_USER=agent@example.com
MAIL_PASS=yourpassword
MAIL_FROM_NAME=MyAgent
EOF
chmod 600 /etc/imap-mail.env
```

## 2. Create systemd unit

```bash
cat > /etc/systemd/system/imap-mail-api.service <<EOF
[Unit]
Description=IMAP Mail API bridge
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/skills/imap-mail/scripts/mail-api.py
Restart=on-failure
RestartSec=5
EnvironmentFile=/etc/imap-mail.env

[Install]
WantedBy=multi-user.target
EOF
```

## 3. Enable and start

```bash
systemctl daemon-reload
systemctl enable --now imap-mail-api.service
systemctl status imap-mail-api.service
```

## 4. Verify

```bash
curl http://127.0.0.1:8025/health
```
