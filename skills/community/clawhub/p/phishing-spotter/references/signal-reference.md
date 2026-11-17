# Signal Reference — Phishing Detection

## Why Textual Analysis Works

Phishing must, by definition, persuade you to act through the message itself.
That forces attackers into reusable rhetorical patterns (urgency, fear,
authority) and URL tricks (spoofed domains, harvest paths). AI-generated
phishing fixed the grammar but cannot avoid the *structure* of persuasion —
the pattern library here targets structure, not spelling mistakes.

## URL Attacks, Ranked by Effectiveness

### 1. Brand-in-subdomain (`paypal.com.evil.io`) — weight 25
The most effective trick on mobile, where URLs truncate. The eye finds
"paypal.com" and stops. Defense: read domains **right-to-left** — only the
last two labels (the registrable domain) identify the site. Everything left
of it is attacker-controlled subdomain space.

### 2. Homograph/IDN (`pаypal.com` with Cyrillic а) — weight 25
Internationalized Domain Names allow non-ASCII lookalikes. Many fonts render
Cyrillic а, е, о, р, с identically to Latin. Raw-unicode hosts and punycode
(`xn--`) forms are both flagged.

### 3. `@` authority trick (`http://paypal.com@evil.io/`) — weight 20
Everything before `@` is a *username*; browsers go to the host after it.

### 4. Punycode (`xn--ppyl-4nd.com`) — weight 22
Encoded homograph. Appears in the raw URL when the mail client doesn't
decode IDN.

### 5. IP host, encoded hosts, shorteners — weights 10–15
Obfuscation layers. Shorteners alone are neutral (marketing uses them too) —
weight 10 — but they hide everything else, so treat any shortened link in a
pressure-message as hostile until expanded safely.

### 6. Credential-bait paths — weight 12
`/login`, `/verify`, `/wallet`, `/unlock` on a spoofed domain = credential
harvester. On a real domain, meaningless (real sites have login pages too);
the score combines URL + context signals for this reason.

## The Pressure Ladder

Attacks escalate pressure to compress your thinking time:

| Rung | Pattern | Weight |
|---|---|---|
| Fear | account suspension, breach alerts, legal action | 12 |
| Clock | 24/48-hour deadlines, "immediately", "right now" | 15/10 |
| Authority | CEO/CFO/agency impersonation | 8 |
| Reward | lottery, refund, "you won", % off | 12–15 |
| Secrecy | "don't tell anyone", "confidential" | 12 |
| Isolation | move to phone/WhatsApp (away from auditable channels) | 8 |

**Gift cards, crypto, wire = automatic scam signal** (weights 12–15). No
legitimate business, court, utility, or tax agency bills in gift cards.

## Structural Tells

- **Reply-To ≠ From domain** (+12): replies route to the attacker while the
  visible From looks official.
- **Display-name impersonation** (+12): `"PayPal Support" <x@random.io>` —
  mail clients show the display name prominently, the domain small.
- **Free-mail domains for corporate claims** (+10): `ceo@somedomain@gmail.com`
  style BEC.
- **Generic greeting** (+6): "Dear Customer" — your bank knows your name.
- **Risky attachments** (+15): `.exe .scr .js .vbs .hta .jar .iso .zip .docm`
  — delivery vehicles for malware.

## Score Bands

| Score | Band | Action |
|---|---|---|
| 0–24 | LOW RISK | Still verify credential requests independently |
| 25–49 | SUSPICIOUS | Verify via app/known number before any click |
| 50–74 | LIKELY PHISHING | Do not interact; report and delete |
| 75–100 | ALMOST CERTAINLY PHISHING | Report, delete, alert family/team |

Calibration: a real GitHub "new device sign-in" email scores ~24 (LOW); a
classic PayPal spoof scores ~100. Tailored low-noise lures (spear phishing)
can score LOW — **the score is evidence-weighting, not proof**. That's why
every report ends with independent-verification steps.

## What This Tool Deliberately Never Does

- **Never fetches URLs.** Visiting is the attack working. All analysis is
  textual.
- **Never trusts TLS/padlock.** Free certificates mean HTTPS proves nothing
  about who runs a site.
- **Never renders remote images.** Real mail clients loading remote images
  leak your IP + read-time to the attacker ("this address is live"). This
  tool doesn't render anything.

## If You Already Clicked (damage-control order)

1. **Disconnect** the device from network (limits beaconing/exfil).
2. **Change the password** for the phished site *from a different device*;
   use the official app, not any link.
3. **Revoke sessions and app tokens** (most major sites have a "log out all
   devices" control).
4. **Enable/verify 2FA** — preferably an app or key, NOT SMS.
5. If a card/bank: **notify the bank, freeze the card**, watch statements.
6. **Check for forward rules** created in your mail settings (attackers
   backdoor accounts here).
7. Report: FTC reportfraud.ftc.gov, IC3, phishing@<brand>, reportphishing@apwg.org.
