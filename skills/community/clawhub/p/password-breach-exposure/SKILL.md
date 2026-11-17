---
name: password-breach-exposure
description: Use after any major data-breach headline or when auditing which of your accounts are compromised — checks passwords against the Have I Been Pwned breach corpus using k-anonymity (only a 5-character SHA-1 prefix ever leaves the machine), maps each hit to what the breach actually leaked (passwords vs contact info vs payment), and produces a severity-ranked rotation queue with credential-stuffing blast-radius math instead of a vague "change everything."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [security, passwords, breach, haveibeenpwned, k-anonymity, rotation, hygiene]
---

# Password Breach Exposure

A breach drops. The advice is always "change your passwords" —
all of them? in what order? which ones actually matter? Most
people either panic-rotate one password or do nothing. Neither
survives contact with an attacker running credential stuffing,
where a LinkedIn-2012 password meets a Gmail login box within
hours.

This skill makes the exposure concrete and the response ordered:

1. **Check** — test specific passwords against the real breach
   corpus via Have I Been Pwned's Pwned Passwords API using
   **k-anonymity**: the script hashes locally (SHA-1), sends only
   the first 5 hex characters, and matches the suffix locally.
   The password itself never leaves the machine — not even in
   hashed-full form.
2. **Assess** — map each hit to what that breach class actually
   leaked (plaintext passwords vs bcrypt vs email-only vs payment
   data). A password in a bcrypt breach is urgent; the same
   password in a contact-scrape is cosmetic.
3. **Prioritize** — rotation queue ranked by (leaked credential
   type × reuse × account value), with a blast-radius estimate:
  `exposed uses = reuse count × stuffing hit-rate`.

## When to Use

- A breach is in the news and you had an account there
- Periodic hygiene audit ("which of my ~10 base passwords are
  burned?") — quarterly is reasonable
- After finding an old password written down / in a screenshot /
  in an email to yourself
- Building or rebuilding a password-manager vault: test base
  passwords BEFORE reusing them anywhere
- Helping a family member who "uses the same password everywhere"
  and wants to know how bad that actually is

Don't use for: choosing a NEW password's strength (different
problem — length/passphrase math), phishing/URL forensics
(different skill), or enterprise SIROM work. This is personal
triage.

## The Privacy Architecture (why this is safe)

The Pwned Passwords API is designed for exactly this flow:

```
SHA-1(password)        = 21BD1...  (computed locally)
prefix sent to API     = "21BD1"   (5 hex chars — that's ALL)
API returns            = every suffix in its corpus starting 21BD1
                             (typically 500-800 hash suffixes + counts)
local match            = compare your suffix against the list
```

- The API learns nothing usable: a 5-char prefix covers ~1M+
  possible hashes; your password is one of hundreds in the
  response
- No account, no email, no identifiers are sent — password check
  and email/breach check are SEPARATE queries (the script never
  combines them in one request)
- Offline fallback: if the network is unavailable, the script
  falls back to a bundled catalog of ~40 major breaches with
  leaked-field classes and dates, so assessment mode still runs

## The Rotation Queue Logic

Each exposed password gets a priority score:

```
severity  = leaked_type_weight   (plaintext 100 / bcrypt 65 /
                                  unsalted-hash 80 / contact-only 10)
priority  = severity × (1 + reuse_count) × account_weight
              (email/bank/phone = 3, shopping = 1.5, forums = 1)
```

Output is a numbered queue: rotate #1 first, with the reason
attached ("plaintext leak + 4 known reuses + guards an email
account"). Anything contact-only goes to the bottom as
"low-value rotation."

## Pitfalls

1. **Testing passwords by pasting them into random "breach
   checker" websites.** Unknown operators = you just handed over
   the credential. Only k-anonymity against a known endpoint, or
   fully local checks.
2. **Treating every breach as equal.** A 2012 leak of bcrypt
   hashes with no salts cracked by 2024 is still dangerous, but
   an email-only marketing leak is not a password event. The
   leaked-field class drives urgency.
3. **Rotating the exposed password everywhere EXCEPT the old
   forum it leaked from.** The stale copy re-burns the new one
   if you reuse. The queue includes the source account.
4. **Email-based panic.** "Your email appeared in a breach"
   emails describe the email appearing — often just contact
   data. Check WHAT leaked before spending a weekend on rotation.
5. **Forgetting the username side.** If the email itself leaked,
   credential stuffing also tries email+top-1000 passwords. A
   strong unique password survives that; 2FA on email/bank makes
   it moot — the report flags missing 2FA on high-value targets
   when you list them.
6. **One-and-done.** Old dumps keep circulating. Re-run the
   check quarterly and after every major headline.

## Verification Checklist

- [ ] Passwords tested only via k-anonymity (verify: request URL
      contains a 5-char prefix, nothing longer)
- [ ] Each hit mapped to leaked-field class + breach date
- [ ] Reuse count honestly estimated per password
- [ ] Rotation queue generated with priorities, #1 actionable now
- [ ] High-value accounts flagged for 2FA, not just rotation
- [ ] Breach sources dated — pre-2016 plaintext leaks are still
      fully live threats

## Quick Recipe

```
# interactive, password hidden on input
python3 scripts/breach_exposure.py check

# audit a set of base passwords non-interactively (careful: shells
# keep history — prefer the interactive mode)
python3 scripts/breach_exposure.py check --pw "old-base-1" --pw "old-base-2"

# map exposure to your accounts and build the rotation queue
python3 scripts/breach_exposure.py assess --email you@example.com \
    --inventory my_accounts.txt

# offline catalog of major breaches + what they leaked
python3 scripts/breach_exposure.py catalog
```

`my_accounts.txt`: one `account password-nickname weight` per
line (e.g. `gmail.com base-A 3`, `old-forum base-A 1`) — the
script cross-references nicknames against checked passwords and
emits the ranked queue.
