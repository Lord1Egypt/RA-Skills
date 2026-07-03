# config.json example (mytonnages — routes A + C)

```json
{
  "hifleet_api_key": "from HiFleet website",
  "hifleet_charter_api_base": "https://api.hifleet.com/openclaw/vessel/charter",
  "hifleet_liner_api_base": "https://api.hifleet.com/openclaw/vessel/charter/liner",
  "charter_enrich_url": "https://api.hifleet.com/openclaw/vessel/charter/enrich-row",
  "mail_parse_interval_minutes": 10,
  "imap_host": "imap.example.com",
  "imap_port": 993,
  "imap_mailbox": "INBOX",
  "email": "user@example.com",
  "email_password": "app password (local only)",
  "smtp_host": "smtp.example.com",
  "smtp_port": 465,
  "mail_preview_host": "0.0.0.0",
  "mail_preview_port": 8765,
  "mail_preview_base_url": "http://localhost:8765",
  "mail_preview_token": ""
}
```

**Liner API base** (`hifleet_liner_api_base`): route C **port suggest** (`GET …/ports/suggest`) and **contact unlock** (`POST …/unlock`, `typeCode=product_will_arrive_charter` — **`CONTACT_API.md`**). Also used by **`hifleet-schedule`**.

| SMTP | 说明 |
|------|------|
| `smtp_host` / `smtp_port` | 回复邮件用；`email` / `email_password` 与 IMAP 相同。未填 `smtp_host` 时按 `imap_host` 推断（如 `imap.gmail.com` → `smtp.gmail.com`） |
| `smtp_use_ssl` | 可选；默认 port `465` 为 SSL，`587` 为 STARTTLS |

回复流程见 **`MAIL_REPLY.md`**。

Optional locale: environment **`HIFLEET_USER_LOCALE`** (`en`, `zh`, `zh-TW`, …).
