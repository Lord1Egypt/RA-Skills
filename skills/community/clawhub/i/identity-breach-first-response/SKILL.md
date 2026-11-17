---
name: identity-breach-first-response
description: Use the hour you learn your email/password/SSN or a company holding your data was breached — runs the damage-scoping triage (what does the attacker ACTUALLY have: password reuse blast radius, session-hijack vs credential-stuffing, SIM-swap window), orders the first-60-minutes containment sequence (which account to secure FIRST and why — email before banking, because email resets everything), breach math (1-in-4 reuse means N sibling accounts), and generates the FTC identity-theft report + bureau letters when SSN is in scope.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [security, data-breach, identity-theft, credentials, incident-response, sim-swap]
---

# Identity Breach First Response

A breach notice or a suspicious-login alert starts a clock. The first
hour decides whether this is a password change or a six-month identity
theft case: email compromise means the attacker can reset everything
downstream; a SIM swap means your 2FA codes are HIS codes; SSN in the
dataset means new accounts you won't see for months. This skill is the
triage instrument: scope what the attacker actually holds, contain in
the order that cuts attack paths, then monitor for the parts that got
through.

## When to Use

- "We were breached and your data was included" email arrived
- A security alert: new login, password-changed-without-you, missing 2FA prompt
- Phone drops to SOS / "No Service" out of nowhere (SIM-swap signature — minutes matter)
- Bank/credit-card fraud alerts, or a collections letter for an account you never opened
- You found your password in a leak dump / HIBP notification
- Deciding whether to freeze credit (yes if SSN leaked) and with whom

**Don't use for:** an actively spreading enterprise compromise you're
responsible for (your IR team / CERT); stalking or targeted threats
(police); child CSAM or extortion demands involving money transfers —
stop and escalate to law enforcement.

## The Method

1. **`scope`** — what leaked (password hash vs plaintext, email, phone,
   SSN, card, DOB, security answers) → what each unlocks → breach reuse
   math (if you reuse 1-in-4 passwords, a 120-account person has ~30
   sibling accounts at risk) → the blast-radius verdict.
2. **`contain --min 60`** — the ordered containment checklist with the
   WHY per slot: email FIRST (it resets everything), bank passwords but
   from a CLEAN device, then the password manager itself, then 2FA
   rotate; SIM-swap branch with the carrier codes; "don't click the
   breach email's links — type them" rule.
3. **`freeze`** — SSN in scope → the exact bureau freeze sequence (all
   three, free by law), freeze-vs-lock decision, fraud-alert
   alternative, minor-children quirk, and the PIN handling rules.
4. **`monitor`** — the 90-day watch plan: what alerts to set where
   (bank push, bureau alerts, IRS IP PIN, credit-card virtual numbers),
   first-of-month 10-minute check ritual, and the red flags that
   escalate to `report`.
5. **`report`** — generates the FTC IdentityTheft.gov report (the
   document banks and bureaus actually want), the police-report
   request, and the dispute letter template with your FTC report
   number slot.

Run `python3 scripts/breach_response.py <cmd> --help` for all flags.

## Judgment Rules

- **Email is the master key.** Attacker with email access resets bank
  passwords at will. Secure email (password + review filters/forwarding
  rules + revoke sessions) before anything else including banking.
- **Session hijacking beats password stealing.** Changing the password
  does NOT kick out a logged-in attacker — "log out all sessions /
  revoke tokens" on every service that offers it, in the same sitting.
  Then check mail forwarding rules and connected-app authorizations.
  (Passkey/service-specific prompts block most session theft.)
- **SIM swap signature:** phone shows SOS/No Service, calls fail, but
  Wi-Fi works. Response order: carrier fraud line (not the store),
  banking app via Wi-Fi, then set a carrier port-out PIN.
- **Plaintext password + reuse = assume every reused sibling account is
  burned.** Rotate them by importance, not alphabetically.
- **Freeze > lock > alert.** A freeze blocks hard-pull new accounts
  nearly outright; alerts rely on a creditor bothering to check. All
  three bureaus, free, keep the PINs in the password manager (not email).
- **Don't trust the breach email itself.** Breach notices are a favored
  phishing skin. Never click through — type the company's URL yourself.

## Common Pitfalls

1. Rotating the breached password but leaving identical passwords on
   sibling accounts (attacker's credential-stuffing list has those too).
2. Changing passwords FROM the possibly-infected machine — use a
   different, clean device for the first resets.
3. Skipping "revoke sessions" — the attacker stays logged in for days
   on the token while you admire your new password.
4. Only freezing one bureau — creditors pull different ones.
5. Setting the bureau freeze PIN to something stored in the same email
   account that just got breached.
6. Forgetting recovery-email/phone on the breached account itself is
   attacker-controlled — check the recovery settings of your OTHER
   accounts, not just the breached one.
7. Ignoring the "security answers" leak: mother's maiden name doesn't
   rotate — move every account that uses leaked answers to a fake
   generated answer stored in the manager.
8. Paying for credit monitoring when freezes + free bureau alerts do
   the job a la carte (fine to take the company's free offer, though).

## Verification Checklist

- [ ] Email account: new password, sessions revoked, forwarding/filter
      rules inspected, recovery phone/email verified yours
- [ ] Password manager password rotated + its 2FA re-paired
- [ ] All reused sibling passwords rotated (importance-first)
- [ ] 2FA re-enrolled where seeds might have been seen; app-based > SMS
- [ ] Bank/card: password + alerts on, from a clean device; fraud
      claims filed for bad charges within the issuer's window
- [ ] SIM-swap cleared (or port-out PIN set with carrier)
- [ ] Bureau freezes at all three + PINs stored in the manager
- [ ] IRS IP PIN requested if SSN leaked (US)
- [ ] FTC report filed if accounts were opened; number recorded
- [ ] 30/60/90-day calendar checks created

## One-Shot Recipe

Breach notice says plaintext passwords + phone numbers leaked; you
reuse passwords "a lot":

```bash
python3 scripts/breach_response.py scope --leaked password,email,phone \
    --accounts 120 --reuse 0.25
python3 scripts/breach_response.py contain --min 60
python3 scripts/breach_response.py freeze --ssn no
python3 scripts/breach_response.py monitor
```

Then work the contain list top to bottom, on a clean device, starting
with email.
