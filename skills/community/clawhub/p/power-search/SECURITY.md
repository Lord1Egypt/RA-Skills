# Power Search — Security & Transparency Report

## VirusTotal "Suspicious" Flag Explanation

Power Search may be flagged by VirusTotal Code Insight as potentially suspicious. **This is a false positive.** Here's why:

## Why The Flag Occurs

VirusTotal's heuristics flag code that:
1. **Makes HTTP requests** (via `node-fetch`)
2. **Calls external APIs** (Brave Search API)
3. **Spawns processes** (Docker container for Browserless)

All three of these are **intentional and legitimate** features of this tool.

## What Power Search Actually Does

### ✅ Legitimate Functionality

- Searches the web using Brave Search API (you provide the API key)
- Fetches full page content using a local Browserless container
- Parses HTML to extract text
- Formats and returns results to you

### ❌ What It Does NOT Do

- ✓ No `eval()` or dynamic code execution
- ✓ No hardcoded secrets or credentials
- ✓ No obfuscation or code hiding
- ✓ No cryptocurrency mining or exploits
- ✓ No malware, spyware, or backdoors
- ✓ No unauthorized external communications
- ✓ No data exfiltration or tracking

## Code Transparency

**Everything is open-source:**
- All source files are plain JavaScript (easy to audit)
- No compiled binaries or black boxes
- No minification or obfuscation
- Every dependency is a well-known, legitimate npm package

**Dependencies:**
- `node-fetch@^2.7.0` — HTTP requests (made by node.js maintainers)
- `commander@^11.1.0` — CLI parsing (used by thousands of projects)
- `cheerio@^1.0.0-rc.12` — HTML parsing (jQuery-like interface)

## API Key Security

### How Keys Are Handled

```javascript
// Correct: Required from environment
const BRAVE_API_KEY = process.env.BRAVE_API_KEY;
if (!BRAVE_API_KEY) {
  throw new Error('BRAVE_API_KEY environment variable not set');
}
```

**NOT:**
```javascript
// Never: Hardcoded in source
const BRAVE_API_KEY = 'BSA...'; // ← NOT IN THIS CODE
```

### Best Practices Implemented

1. **Environment variables only** — Keys never in code or `.env` files
2. **`.gitignore` protection** — `.env` files cannot be accidentally committed
3. **`.env.example`** — Template showing what variables are needed (no secrets)
4. **No logging** — Keys are never printed or cached
5. **No persistence** — Keys exist only in memory during execution

## Audit Checklist

For your review:

- [ ] Review `scripts/brave-search.js` — API calls only, no exploitation
- [ ] Review `scripts/browserless.js` — Container management, no code execution
- [ ] Review `scripts/search.js` — CLI parsing, no dynamic code
- [ ] Review `scripts/telegram-handler.js` — Message formatting, no backdoors
- [ ] Check `package.json` — All dependencies are legitimate npm packages
- [ ] Check for hardcoded secrets — `grep -r "BSAF\|clh_\|token" scripts/` (should be empty)
- [ ] Check `.gitignore` — Includes `*.env` to protect your keys

## Conclusion

Power Search is a **legitimate, auditable, and secure** tool. The VirusTotal flag is a false positive based on the tool's design (intentionally making API calls and spawning processes).

**You can safely use and share this skill.**

---

**Questions?** Review the source code directly at:
- `~/.npm-global/lib/node_modules/openclaw/skills/search/scripts/`
- https://clawhub.ai/churchtg7/power-search

---

*Report last updated: April 5, 2026*
*Skill version: 2.1.1*
