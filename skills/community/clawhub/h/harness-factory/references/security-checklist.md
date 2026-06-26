# Security Checklist for Harness Reviews

Use this during Phase 3 (Evaluate) for every code review.

## Authentication & Authorization
- [ ] All new endpoints require authentication (JWT/session token)
- [ ] Admin-only endpoints have admin role check
- [ ] No auth tokens exposed in logs or error messages

## Input Validation
- [ ] All user inputs validated (type, length, format)
- [ ] URL inputs checked for SSRF (block localhost, private IPs, link-local)
- [ ] File uploads: size limit enforced, content-type whitelist
- [ ] SQL/NoSQL injection prevention (parameterized queries only)

## CORS & Headers
- [ ] CORS origins restricted to production domains (not `*`)
- [ ] Security headers present (X-Content-Type-Options, etc.)

## Rate Limiting
- [ ] Abuse-prone endpoints have per-user rate limits
- [ ] Rate limit returns 429 with Retry-After header

## Data Protection
- [ ] No API keys or secrets in frontend code
- [ ] No secrets in git history
- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Error messages don't leak internal details to users

## Dependencies
- [ ] No new dependencies added without justification
- [ ] Existing dependencies not downgraded

## Common Vulnerabilities from Our Experience
- [ ] **CORS on image proxy** — CDN images need backend proxy (Brand Style Clone Round 4)
- [ ] **Stripe dispute handling** — webhook must auto-cancel subscription + zero credits
- [ ] **Frontend relative URLs** — must use full API base URL, not relative paths (TrendMuse Round 3)
- [ ] **OAuth token expiry** — tokens expire, need refresh mechanism
