# Breach Exposure — Reference Playbook

## What actually leaks in a breach (classes)

| Class | Example breaches | What attackers have | Urgency |
|---|---|---|---|
| Plaintext passwords | RockYou, Collection #1-5, many forum dumps | Direct credential | CRITICAL if reused |
| Unsalted/fast-hash (MD5/SHA-1) | older vBulletin/PhpBB dumps | Crackable in minutes-hours | CRITICAL |
| Bcrypt/scrypt/argon2, salted | LinkedIn 2012 (SHA-1 unsalted, later cracked), bcrypt-era dumps | Slow to crack; GPU farms still get weak ones | HIGH |
| Email + personal data, no creds | marketing DBs, scrapes | Phishing/enumeration, stuffing lists | LOW (credential-wise) |
| Payment/token data | some e-commerce breaches | Fraud, card replacement | Card issue, not password issue |

Date matters: a "cracked-by-now" weak bcrypt from 2013 behaves
like plaintext today. Treat anything pre-2016 with weak hashing
as exposed.

## K-anonymity flow (exact)

1. `h = SHA1(password.encode('utf-8')).hexdigest().upper()`
2. `GET https://api.pwnedpasswords.com/range/{h[:5]}`
   - No email, no identifiers, no full hash in the URL
   - Optional header `Add-Padding: true` makes even request
     timing/volume less fingerprintable
3. Response body: lines of `HASH_SUFFIX:COUNT`
4. If `h[5:]` appears → the password is in the corpus, seen
   `COUNT` times. COUNT is exposure breadth, not direct risk —
   but count > 0 means it's in attacker wordlists. Count in the
   millions = it's in every basic wordlist.

Rate limits: the API is generous but not infinite; the script
sleeps briefly between requests and caches results locally so
re-runs don't re-query.

## Interpreting results

- **0 hits** on a base password: good — it's not in the known
  corpus. Strength against offline cracking is a SEPARATE
  question (length still rules).
- **1-100 hits**: in the corpus, niche. Rotate where reused.
- **1,000+ hits**: in active wordlists. Any account using it is
  subject to automated stuffing. Rotate everywhere, enable 2FA
  on anything valuable.
- Password found in a breach WITH your email (via the separate
  breach-list check): that exact pair is likely circulating.
  Treat every shared-use sibling as burned.

## Blast-radius math

```
exposed_login_attempts = reuse_count × hit_rate
hit_rate ≈ 0.1% - 2% for large-scale stuffing campaigns
```
With 12 reuses and 1%: ~0.12 expected account compromises per
campaign — repeated across many campaigns per year, plus
targeted attempts where the attacker knows your email from the
same dump. Reuse is the multiplier; that's why the queue sorts
by reuse × severity, not severity alone.

## Rotation order doctrine

1. Email account (it resets everything else — guard it first)
2. Financial / payment accounts
3. Phone-carrier (SIM-swap surface; set a port-out PIN)
4. Password manager master password if any exposed base
   resembles it
5. Accounts where the exposed pair (email+password) leaked
   together — those pairs trade openly
6. Everything else reusing the base, forum-tier last

For each: NEW unique password (passphrase length beats symbol
soup), then 2FA where offered, then log out other sessions.

## Offline catalog (bundled with the script)

The script ships `data/breach_catalog.json` — ~40 landmark
breaches with name, year, scale, and leaked-field class. When
the network is unavailable (or for skittish users), `assess`
runs against this catalog: you tell it which breaches your
emails appeared in (from HIBP emails or news), it produces the
same severity mapping and queue. The classes and doctrine are
what matter; the live API only answers "is THIS exact password
in the corpus."

## Family/less-technical users

Run the interactive check WITH them; never ask them to send
passwords to you in chat. The 5-char-prefix property means the
check is safe even on their laptop at the kitchen table — that's
the whole point of k-anonymity. Print the rotation queue and
tape it to the monitor; humans finish visible queues.

## What this skill is NOT

- Not a password generator/strength advisor (length + uniqueness
  is the whole doctrine here)
- Not an email-breach monitoring service (HIBP's email alerts do
  that; this skill consumes such news, replaces panic with order)
- Not forensics on a compromised account (that's incident
  response: sessions, recovery email/phone, forwarding rules,
  connected apps — do that BEFORE rotating if an account is
  actively owned)
