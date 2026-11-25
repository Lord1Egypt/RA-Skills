---
name: email-deliverability-check
description: >
  Check and fix email deliverability: sending domain setup, SPF, DKIM and
  DMARC records, sending readiness, bounces and spam complaints, so emails
  reach the inbox instead of spam in Gmail and Outlook. Use for
  deliverability, DNS records or why emails go to spam.
---

# Email deliverability check

Find out why email isn't reaching the inbox and fix it.

Guide: [Email deliverability](https://nitrosend.com/email-deliverability)

1. Read sender and delivery state from `nitro_get_status`: `delivery.reason_code`,
   `issues` and `retry_at`. Report pauses exactly as returned.
2. For a customer-owned domain, add it with `nitro_manage_domains` (`operation: "add"`) and show
   the DNS records (SPF, DKIM, DMARC) to create; check with
   `nitro_manage_domains` (`operation: "verify"`). The Nitrosend brand address needs no DNS.
3. Use `nitro_get_insights` for bounce and complaint trends and
   `nitro_review_delivery` for a specific campaign or flow.
4. Never bypass a sending pause, content review or ownership check.
