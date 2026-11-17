# Containment Order, Freeze Mechanics, Monitoring

## Why email first — the reset chain

Everything downstream of an email compromise is one "forgot password"
click away for the attacker. The containment order exists to cut attack
paths, not to soothe anxiety:

| Order | Target | Action | Why this slot |
|-------|--------|--------|---------------|
| 1 | Primary email | password + revoke sessions + check filters/forwarding + recovery options | it resets EVERYTHING below |
| 2 | Password manager | master password + re-pair 2FA | it IS all your other passwords |
| 3 | Banking / brokerage | password + alerts + fraud claims (clean device) | money moves fastest |
| 4 | 2FA anchors | re-enroll app-based; replace SMS where possible | codes route to attacker if SIM-swapped |
| 5 | Sibling reused accounts | rotate by importance: shopping, social, gaming | credential stuffing hits these within hours |
| 6 | Carrier | port-out PIN / Number Lock | closes the SIM-swap door |
| 7 | Recovery hygiene | strip attacker-known recovery emails/phones from OTHER accounts | he owns the reset path otherwise |

## Session theft: the part people miss

A logged-in attacker keeps his session token after you change the
password. On every service: **log out all other sessions / revoke
devices and apps**. Then inspect:

- Email **filters and forwarding rules** (exfiltration is silent)
- **Connected apps / OAuth grants** (a token-scraping app survives password changes)
- **Recovery email/phone** set on the account

Passkeys (device-bound) and "Apple/Google prompt" style 2FA block most
session-token replay — prefer them where offered.

## SIM swap: the 30-minute window

Signature: phone drops to SOS/No Service while Wi-Fi still works; texts
stop arriving; sometimes a "Hi, this is [carrier], reply YES to port"
sms preceded it.

1. Call the carrier's **fraud line** (not retail, not the porting
   department) — ask them to halt the port and reverse it.
2. From Wi-Fi, secure banking apps (SMS 2FA now routes to attacker).
3. Set a **port-out PIN / Number Lock** so future ports need it.
4. If cash moved: bank fraud claim + police report (banks ask for it).

## Freeze vs lock vs alert

| Tool | What it does | Cost | Verdict |
|------|--------------|------|---------|
| Freeze | blocks hard pulls almost outright; new credit can't open | free by law (US) | DEFAULT when SSN leaks |
| Lock | like freeze, faster toggle, bureau app | free-ish | fine, but freeze is the legal floor |
| Fraud alert | asks creditors to verify you | free, 1 yr renewable | weaker; use if you're about to apply for credit often |
| Credit monitoring | watches, doesn't block | $0-25/mo | take the breaching company's free offer; don't buy by default |

Freeze all **three** bureaus (Equifax, TransUnion, Experian) — creditors
pull different ones. Minors: request in writing/phone, they'll want
proof of guardianship — do it anyway; child SSNs are prime (clean files).
Keep the freeze **PINs in the password manager**, never in the email
account you just secured. Thaw temporarily (a day) when YOU apply for
credit — the lender tells you which bureau.

## Monitoring: the 90-day plan

- **Bank + cards:** push notifications on every transaction (not
  weekly digests). Issuer app settings, 5 minutes.
- **Bureaus:** each offers free account + alerts — set all three.
- **IRS IP PIN** (US, SSN leak): blocks e-file fraud with your number.
- **Virtual card numbers** for new online spending (issuer or
  privacy.com) — contain the next breach.
- **Monthly 10-minute ritual** (first of month): statements for charges
  you don't recognize; new accounts on bureau dashboards; any mail for
  accounts you never opened.
- **Escalate to `report`** when: new account appears, collections letter
  arrives, tax refund hijacked, or medical bill in your name (medical
  ID theft gets its own dispute lane — request the records).

## The report layer

IdentityTheft.gov builds the FTC affidavit — the document banks,
bureaus, and police treat as ground truth. Save the report number; it
goes into every dispute letter. Police report: non-emergency line or
  online portal, "identity theft" category; banks may ask for the
  report number, not the full report. Dispute letters to bureaus:
  certified mail, return receipt, attach FTC report, list each
  fraudulent item, demand blocking (FCRA §605B gives you the right).
