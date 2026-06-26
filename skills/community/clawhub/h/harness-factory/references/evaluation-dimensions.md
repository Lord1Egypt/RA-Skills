# Evaluation Dimensions

## 1. Functionality (30%)
- Does the feature work as specified in SPRINT.md?
- Are all success criteria met?
- Does the full user flow work end-to-end?
- Do error states produce clear user messages?

## 2. Code Quality (25%)
- Follows existing code patterns and conventions?
- No duplicate code (DRY)?
- Functions have docstrings?
- No dead imports or unused variables?
- Clean separation of concerns?

## 3. Security (25%)
- CORS properly configured?
- All endpoints require appropriate auth?
- Rate limiting on abuse-prone endpoints?
- No SSRF vulnerabilities in URL handling?
- No secrets in code or logs?
- Input validation on all user inputs?

## 4. UX / Edge Cases (20%)
- What happens with empty/null input?
- What happens on network timeout?
- What happens with concurrent requests?
- Loading states and error messages user-friendly?
- Mobile responsive (if frontend)?
