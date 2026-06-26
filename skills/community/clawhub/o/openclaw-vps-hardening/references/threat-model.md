# Threat Model & Attack Surface

Documents what this hardening strategy defends against and residual risks.

## Attack Surface: Before Hardening

```
Internet → port 22   (SSH — root, password auth enabled)
         → port 18789 (OpenClaw — token auth, HTTP, public)

Risks:
- SSH brute force / credential stuffing
- OpenClaw token interception (HTTP, no TLS)
- Direct WebSocket abuse (no rate limiting)
- Anyone who guesses/steals the token has full agent access
- Port scan reveals agent infrastructure
```

## Attack Surface: After Hardening

```
Internet → port 2222  (SSH — key-only, non-root, fail2ban)
         → (nothing else — 18789 closed, served via Cloudflare Tunnel)

Cloudflare Edge → Access policy check (identity required)
                → Cloudflare Tunnel → localhost:18789
                                    → OpenClaw token auth (2nd factor)
```

A full internet port scan shows: one SSH port. Nothing else.

---

## What Each Layer Defends

| Threat | Defended by |
|---|---|
| SSH brute force | Fail2Ban (3 strikes, 24hr ban) + non-default port |
| SSH credential theft | Key-only auth (no passwords accepted) |
| Direct port 18789 access | UFW deny + loopback binding |
| Unauthorized agent access | Cloudflare Access (identity gate) |
| Token interception | Cloudflare TLS termination (HTTPS only) |
| Distributed brute force | Cloudflare Access blocks before VPS |
| Agent infrastructure exposure | Port scan shows nothing except SSH |
| Root escalation via OpenClaw | Non-root service user (koda) |
| Config/key exfiltration | File permissions 600/700 |
| Unpatched CVEs | Unattended security upgrades |

---

## Residual Risks (Not Covered)

| Risk | Mitigation outside this strategy |
|---|---|
| SSH key compromise | Rotate keys periodically, use hardware key (YubiKey) |
| Cloudflare account compromise | Strong password + MFA on Cloudflare account |
| Anthropic API key exfiltration | Key rotation, Anthropic spend limits |
| Insider threat (team member) | Per-user Cloudflare Access policies, audit logs |
| Supply chain attack on openclaw npm | Pin to specific version, review changelogs |
| DDoS against Cloudflare endpoint | Cloudflare DDoS protection (included free) |
| Zero-day in cloudflared | Keep cloudflared updated, monitor advisories |

---

## Security Posture Summary

**Before hardening:** C- (open port, no TLS, no rate limiting, no brute-force protection)
**After hardening:** A- (closed ports, HTTPS, identity gate, brute-force protection, least-privilege)

The remaining gap to A: hardware SSH keys, Anthropic API spend limits, key rotation policy.
