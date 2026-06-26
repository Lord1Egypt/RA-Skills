# Quick Publishing Guide

## Ready to Publish to ClawHub ✅

This skill package is **production-ready** and can be uploaded to ClawHub immediately.

---

## 📦 What's Inside

This folder contains a complete, self-contained OpenClaw skill:

- **1 Action**: `proxy` — transparent gateway to ZhenInsure Skill Chat V2 APIs (conversations, messages, handoff)
- **Zero Dependencies**: Pure native `fetch`, no external packages
- **~5KB**: Skill definition + action handler + documentation
- **Production Code**: API key validation, endpoint whitelist, cost table, error handling

---

## 🚀 Publish to ClawHub (2 commands)

```bash
# 1. Login (server without browser: use --token)
clawhub login --token <YOUR_TOKEN> --no-browser

# 2. Publish
cd /www/wwwroot/www.zhenins.com
clawhub publish insurance-broker \
  --slug insurance-broker \
  --name "ZhenInsure 真机保险 | Insurance Broker" \
  --version 2.0.2
```

**Repository**: https://clawhub.ai/zhenstaff/insurance-broker

---

## 📋 What Happens Next

After publishing:

1. **Users can install**:
   ```bash
   clawhub install zhenstaff/insurance-broker
   ```

2. **Users configure API key**:
   ```bash
   claw config set ZHENINSURE_API_KEY sk_live_abc123...
   ```

3. **Users run actions**:
   ```bash
   claw run insurance-broker proxy \
     '{"endpoint": "/api/v1/billing/balance", "method": "GET"}'
   ```

---

## ✅ Pre-Upload Checklist

Everything is complete:

- [x] Package name: `insurance-broker`
- [x] Version: `2.0.2`
- [x] Single `proxy` action implemented
- [x] Zero external dependencies (native `fetch`)
- [x] README.md updated
- [x] SKILL.md updated
- [x] LICENSE file present (MIT)
- [x] .gitignore configured
- [x] package-lock.json preserved for reproducible installs
- [x] No sensitive data in code
- [x] Tests passing

---

## 🔧 Folder Structure

```
insurance-broker/           # This folder
├── LICENSE                # MIT
├── README.md              # User documentation
├── SKILL.md               # Extended docs
├── package.json           # Metadata
├── package-lock.json      # Reproducible install
├── skill.json             # Action definitions
├── actions/
│   ├── index.js           # Export barrel
│   └── proxy.js           # Core proxy handler
└── test/
    └── test-all.js        # Smoke tests
```

---

## 📝 Metadata Summary

```json
{
  "org": "zhenstaff",
  "slug": "insurance-broker",
  "name": "ZhenInsure 真机保险 | Chat & Handoff",
  "version": "2.0.2",
  "category": "finance",
  "license": "MIT",
  "actions": 1,
  "size": "~6KB"
}
```

---

## 🎯 After Publishing

Verify it worked:

```bash
# Search for your skill
clawhub search insurance-broker

# Inspect metadata
clawhub inspect zhenstaff/insurance-broker

# Install locally
clawhub install zhenstaff/insurance-broker
```

---

## 📞 Need Help?

- Documentation: `README.md` in this folder
- Support: support@zhenins.com

---

**Status**: PUBLISHED ✅ (2026-05-11)

Published to ClawHub as `insurance-broker@2.0.2`
**Last Updated**: 2026-05-11
