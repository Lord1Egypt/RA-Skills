# openclaw-basecred-sdk

**OpenClaw skill for checking human reputation via Ethos Network, Talent Protocol, and Farcaster.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: Audited](https://img.shields.io/badge/Security-Audited-green.svg)](./SECURITY.md)
[![Version: 1.0.4](https://img.shields.io/badge/Version-1.0.4-blue.svg)](./CHANGELOG.md)

## 🔐 Security Status

**Audited:** 2026-02-11 ✅

- ✅ Upstream dependency verified (`@basecred/sdk@0.6.2` - MIT licensed, minimal deps)
- ✅ Secure credential loading (no directory traversal)
- ✅ Portable across users (dynamic home directory resolution)
- ✅ Read-only API access (public reputation data only)
- ✅ No secrets logged or written to disk

**See:** [SECURITY.md](./SECURITY.md) for full audit details | [PATCH-NOTES.md](./PATCH-NOTES.md) for fixes applied

---

## Quick Start

```bash
# Install dependencies
npm install

# Check reputation for an address
./scripts/check-reputation.mjs 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

# Run tests
npm test
```

## What This Does

Fetches neutral, composable reputation data from:

- ✅ **Ethos Network** - Social credibility (no API key needed)
- ✅ **Talent Protocol** - Builder & creator scores (requires API key)
- ✅ **Farcaster (Neynar)** - Account quality (requires API key)

Returns raw scores, levels, and signals—**no rankings, no judgments**.

## Example Output

### Summary (default)
```json
{
  "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "timestamp": "2026-02-10T07:00:00.000Z",
  "availability": {
    "ethos": "not_found",
    "talent": "available",
    "farcaster": "available"
  },
  "data": {
    "talent": {
      "builderScore": 86,
      "builderLevel": "Practitioner",
      "builderRank": 8648,
      "creatorScore": 103,
      "creatorLevel": "Established"
    },
    "farcaster": {
      "score": 1,
      "passesQuality": true
    }
  },
  "recency": "recent"
}
```

### Full Profile (`--full`)
```json
{
  "identity": {
    "address": "0x168D8b4f50BB3aA67D05a6937B643004257118ED"
  },
  "availability": {
    "ethos": "available",
    "talent": "available",
    "farcaster": "available"
  },
  "ethos": {
    "data": {
      "score": 1284,
      "credibilityLevel": {
        "value": 1284,
        "level": "Neutral",
        "levelSource": "sdk",
        "levelPolicy": "ethos@v1"
      },
      "vouchesReceived": 0,
      "reviews": { "positive": 7, "neutral": 0, "negative": 0 }
    },
    "signals": {
      "hasNegativeReviews": false,
      "hasVouches": false
    },
    "meta": {
      "firstSeenAt": "2025-10-05T09:58:11.000Z",
      "lastUpdatedAt": "2025-10-05T09:58:12.000Z",
      "activeSinceDays": 128,
      "lastUpdatedDaysAgo": 128
    }
  },
  "talent": {
    "data": {
      "builderScore": 161,
      "builderLevel": {
        "value": 161,
        "level": "Advanced",
        "levelSource": "sdk",
        "levelPolicy": "builder@v1"
      },
      "builderRankPosition": 641,
      "creatorScore": 66,
      "creatorLevel": {
        "value": 66,
        "level": "Growing",
        "levelSource": "sdk",
        "levelPolicy": "creator@v1"
      }
    },
    "signals": {
      "verifiedBuilder": true,
      "verifiedCreator": true
    },
    "meta": {
      "lastUpdatedAt": "2026-02-05T03:24:55Z",
      "lastUpdatedDaysAgo": 6
    }
  },
  "farcaster": {
    "data": {
      "userScore": 0.98
    },
    "signals": {
      "passesQualityThreshold": true
    },
    "meta": {
      "source": "neynar",
      "scope": "farcaster",
      "lastUpdatedAt": "2026-02-11T07:20:00.000Z",
      "lastUpdatedDaysAgo": 0,
      "updateCadence": "weekly",
      "timeMeaning": "system_update"
    }
  },
  "recency": {
    "bucket": "recent",
    "windowDays": 30,
    "lastUpdatedDaysAgo": 0,
    "derivedFrom": ["ethos", "talent", "farcaster"],
    "computedAt": "2026-02-11T07:20:00.000Z",
    "policy": "recency@v1"
  }
}
```

## Setup

### Prerequisites

- Node.js 18+
- OpenClaw runtime

### Optional API Keys

Add to your `.env` file:

```bash
# Optional: Enables Talent Protocol scores
TALENT_API_KEY=your_talent_api_key

# Optional: Enables Farcaster quality scores
NEYNAR_API_KEY=your_neynar_api_key
```

Get keys:
- Talent Protocol: https://talentprotocol.com
- Neynar: https://neynar.com

**Note:** Ethos Network requires no API key.

## Usage

```bash
# Summary (default)
./scripts/check-reputation.mjs 0x...

# Full unified profile
./scripts/check-reputation.mjs 0x... --full

# Human-readable format
./scripts/check-reputation.mjs 0x... --human

# Help
./scripts/check-reputation.mjs --help
```

## Security & Audit

### 🔍 Security Audit (2026-02-11)

This skill underwent comprehensive security review and hardening:

| Aspect | Status | Details |
|--------|--------|---------|
| **Upstream Package** | ✅ VERIFIED | `@basecred/sdk@0.6.2` - MIT, 2 deps, clean code |
| **Credential Loading** | ✅ SECURE | `os.homedir()` + `path.join()` (no traversal) |
| **Portability** | ✅ FIXED | Dynamic user resolution (was hardcoded) |
| **Attack Surface** | ✅ MINIMAL | Read-only API, no disk writes, no secret logs |
| **Directory Traversal** | ✅ FALSE CLAIM | Direct path construction (audit was wrong) |
| **Isolation Tests** | ✅ PASSING | 5 automated security checks |

**Original audit concern (resolved):**
- ❌ **Claimed:** "Script walks up directories to find .env" 
- ✅ **Reality:** Direct path construction to `~/.openclaw/.env` (no traversal)
- ✅ **Fixed:** Initially hardcoded to `/home/phan_harry/...`, now dynamic for all users

### 🛡️ Security Guarantees

- **Credential isolation:** Only reads from `~/.openclaw/.env` (mode 600)
- **No traversal:** Direct `join(homedir(), '.openclaw', '.env')` construction
- **Pinned dependencies:** Locked to audited `@basecred/sdk@0.6.2`
- **Read-only access:** Only fetches public reputation data (no writes)
- **Graceful errors:** Never exposes secrets in error messages

### 📋 Audit Documentation

- [SECURITY.md](./SECURITY.md) - Full security documentation
- [PATCH-NOTES.md](./PATCH-NOTES.md) - Security fixes applied
- [PORTABILITY-FIX.md](./PORTABILITY-FIX.md) - Critical path fix details
- [test-isolation.sh](./test-isolation.sh) - Automated security tests

**Run security tests:**
```bash
./test-isolation.sh
```

---

## Features

- ✅ Graceful degradation (works with partial data)
- ✅ Never crashes (structured error responses)
- ✅ JSON and human-readable output
- ✅ Summary and full profile modes
- ✅ Semantic levels (Novice → Master, etc.)
- ✅ Recency buckets (recent/stale/dormant)
- ✅ Portable across users (v1.0.2+)
- ✅ Security audited (2026-02-11)

## What This Does NOT Do

- ❌ Decide trustworthiness
- ❌ Rank users
- ❌ Compare users
- ❌ Produce composite scores
- ❌ Replace human judgment

## Documentation

- **[SKILL.md](SKILL.md)** - Complete usage documentation
- **[SECURITY.md](SECURITY.md)** - Security audit and guarantees
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[PATCH-NOTES.md](PATCH-NOTES.md)** - Security hardening details
- **[PORTABILITY-FIX.md](PORTABILITY-FIX.md)** - Critical path fix incident report

## Version History

### v1.0.4 (2026-02-11) - Security Incident & Cleanup + Schema Fix
- 🚨 **SECURITY FIX:** Removed files with leaked API keys from repo and git history
- ✅ Git history scrubbed (13 commits rewritten, force-pushed)
- ✅ All exposed API keys rotated (Talent Protocol, Neynar)
- ✅ Fixed hardcoded paths in documentation (`/home/phan_harry/` → `~/`)
- ✅ Removed `BUILD-SUMMARY.md` and `AUDIT-SUMMARY.md`
- 🔧 **SCHEMA FIX:** `--full` output now returns correct schema (unwrapped profile object)
- ✅ Full profile schema: `{ identity, availability, ethos, talent, farcaster, recency }`

### v1.0.3 (2026-02-11) - Package Rename
- 📦 Renamed package: `basecred-sdk-skill` → `openclaw-basecred-sdk`
- ✅ Updated package.json name and repository URL
- ✅ Published to ClawHub with updated slug
- No functional changes from v1.0.2

### v1.0.2 (2026-02-11) - Security Hardening + Portability Fix
- 🔐 Security audit completed and documented
- 🔴 **CRITICAL FIX:** Non-portable hardcoded user path
- ✅ Dynamic home directory resolution (works for any user)
- ✅ Comprehensive security documentation
- ✅ Automated isolation test suite

### v1.0.1 (2026-02-10) - SDK Update
- Updated `@basecred/sdk` from v0.6.1 to v0.6.2
- Fixed Farcaster decimal precision (0.43 instead of 0)

### v1.0.0 (2026-02-10) - Initial Release
- CLI interface for Ethos, Talent Protocol, Farcaster
- Summary and full profile modes
- JSON and human-readable output

See [CHANGELOG.md](./CHANGELOG.md) for detailed version history.

## Source SDK

This skill wraps [@basecred/sdk](https://www.npmjs.com/package/@basecred/sdk).

Source repository: https://github.com/Callmedas69/basecred/tree/main/packages/sdk

## Contributing

Security issues? Please review [SECURITY.md](./SECURITY.md) first, then report via:
- GitHub Issues: https://github.com/teeclaw/openclaw-basecred-sdk-skill/issues
- Contact: teeclaw

## License

MIT

## Author

Built by **teeclaw** for OpenClaw.

**Audited:** 2026-02-11 by 0xdas & Mr. Tee
