# Password Breach Exposure

"My email was in another breach." The standard advice — change
your passwords — is directionally right and operationally
useless: which ones, in what order, and how bad is it really?

## The Problem

- People reuse a handful of base passwords across dozens of
  sites. One plaintext leak burns all of them at once, and
  credential-stuffing bots test those pairs against email,
  banks, and carriers within hours.
- "Breach" news conflates wildly different events: a contact
  scrape (Facebook 2021: no passwords) vs a plaintext dump
  (Collection #1: 773M credentials). Response effort should
  match the leak class — it almost never does.
- Checking "is my password leaked?" on random websites means
  **handing the password to a stranger**.

## What This Skill Does

1. **Safe corpus check (k-anonymity).** Passwords are SHA-1
   hashed locally; only the first 5 hex characters are sent to
   the Have I Been Pwned range API. The full hash — much less
   the password — never leaves the machine. The API's response
   covers hundreds of hashes; it can't know which is yours.
2. **Exposure banding.** CLEAN / NICHE / KNOWN / WORDLIST /
   UBIQUITOUS from corpus hit counts — "known" directly maps to
   attacker wordlists, so the verdict is about real attack
   surface, not shame.
3. **Ranked rotation queue.** Cross-reference a simple account
   inventory (`account base-nickname weight`) to sort rotations
   by severity × reuse × account value — email and financial
   accounts first, forum accounts last, each with the reason
   attached.
4. **Offline catalog.** 23 landmark breaches with leaked-field
   classes, so the "what did THIS breach actually leak" question
   answers itself even without network.

## Example

```
$ python3 scripts/breach_exposure.py check
password: ********
  #  EXPOSURE     SEEN   VERDICT
  1  WORDLIST     48,213   in active wordlists - rotate EVERYWHERE + 2FA
  2  CLEAN             0   not in known corpus - keep, but check strength

$ python3 scripts/breach_exposure.py assess --inventory accounts.txt
  1. gmail.com              ROTATE NOW + enable 2FA
     WORDLIST (48,213 hits), reused on 5 accounts, weight 3.0
  2. old-forum.example      low-value rotation
     ...
```

## Who Needs This

Anyone with more than three accounts and at least one reused
password — which is most people sharing a password manager with
family, or maintaining an inherited "I use two passwords"
system. Also the right 30-minute project the evening a breach
headline names a service you actually use.

MIT License. Everything runs locally except the 5-character-prefix
API calls; results cache in `scripts/data/`.
