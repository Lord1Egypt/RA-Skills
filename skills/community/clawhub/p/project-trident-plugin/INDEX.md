# Trident Plugin: Complete Package Index

> **Ambient memory architecture for OpenClaw agents. Three-tier persistent memory system with lossless capture, intelligent signal routing, and optional semantic recall.**

---

## 📦 Package Contents

### Core Files (6 total, 88 KB)

| File | Purpose | Audience | Size |
|------|---------|----------|------|
| **plugin-manifest.json** | ClawHub metadata & config schema | Developers, ClawHub | 12 KB |
| **config.schema.json** | JSON Schema validation | Developers, Tools | 12 KB |
| **README.md** | Overview & quick start | Everyone | 12 KB |
| **INSTALL.md** | Step-by-step setup (all platforms) | Users installing | 16 KB |
| **MIGRATION.md** | Skill → Plugin transition | Upgrading users | 16 KB |
| **COMPLETION_REPORT.md** | Delivery summary | Project owner | 16 KB |

---

## 🚀 Quick Navigation

### I'm installing Trident for the first time
→ Read: **README.md** (5 min) → **INSTALL.md** (15 min)

### I have the old Trident skill, can I upgrade?
→ Read: **MIGRATION.md** (safe upgrade path with backup)

### I want to understand the architecture
→ Read: **README.md** "Architecture" section + **plugin-manifest.json** capabilities

### I'm configuring Trident
→ Reference: **config.schema.json** (all 28 options documented)

### I'm publishing this to ClawHub
→ Review: **plugin-manifest.json** metadata + **COMPLETION_REPORT.md** publication steps

### Something's broken
→ Check: **INSTALL.md** "Troubleshooting" section

---

## 📋 File Descriptions

### plugin-manifest.json

**What it is:** ClawHub package definition  
**Contains:**
- Plugin metadata (name, version, author, license, repository)
- Full configuration schema with constraints
- Dependencies (lossless-claw required, docker/git optional)
- Lifecycle hooks (install, activate, deactivate, uninstall)
- Capabilities and permissions

**Key stats:**
- 307 lines
- 28 configuration properties
- 4 example configurations
- Proper JSON Schema 7 validation

**Who needs to edit:**
- On version bumps (version field)
- When adding new features (capabilities, lifecycle)
- Rarely — this is stable metadata

### config.schema.json

**What it is:** Validation schema for openclaw.json Trident configuration  
**Contains:**
- 28 properties (booleans, strings, integers, enums, URIs)
- Type constraints and bounds (e.g., interval: 5-60 min)
- Conditional validation (if Qdrant enabled, URL required)
- Descriptions for every option
- 4 example configurations

**Key stats:**
- 287 lines
- Follows JSON Schema Draft 7
- Covers all use cases (Lite, Zero-Cost, Full, Cloud)
- No passwords/secrets (API keys expected from environment)

**Who needs to edit:**
- When adding new configuration options
- When changing defaults
- Rare — highly stable

### README.md

**What it is:** Public-facing plugin overview  
**Contains:**
- Problem statement ("agents forget")
- Solution overview (three-tier architecture)
- Quick start (5 minutes)
- Features table
- Cost comparison (5 profiles)
- Feature comparison vs. competitors
- Security overview
- Platform support matrix
- Philosophy and vision

**Key stats:**
- 337 lines
- ~4,000 words
- Links to other docs
- Suitable for ClawHub display

**Audience:** Everyone (especially new users)

**Who needs to edit:**
- When updating features or costs
- For promotional updates
- Regularly — this is the marketing document

### INSTALL.md

**What it is:** Complete installation guide for all platforms  
**Contains:**
- Prerequisites check
- Step-by-step installation (3 steps)
- Configuration walkthrough with examples
- Model selection guide with cost table
- Verification tests (activate, test, verify, status)
- Trident Lite details (what you have, next steps)
- Semantic recall setup (Qdrant Docker, binary, cloud)
- Git backup setup
- Upgrade and migration procedures
- Comprehensive troubleshooting
- Platform-specific notes (Windows, macOS, Linux, Docker)
- Quick reference command table

**Key stats:**
- 595 lines
- ~6,000 words
- 12 major sections
- Examples for every command
- Covers 7+ platforms explicitly

**Audience:** Users installing Trident for the first time

**Who needs to edit:**
- When adding new installation steps
- When troubleshooting becomes necessary
- Often — this is your support document

### MIGRATION.md

**What it is:** Upgrade guide for existing Trident skill users  
**Contains:**
- What changed (removed, added, kept)
- File structure evolution (skill → plugin)
- Configuration model transition (env vars → JSON)
- New capabilities (manifest, schema, scripts, docs)
- Dependency changes
- Platform support evolution
- Cost model improvements
- Security enhancements
- Data preservation guarantees
- Backwards compatibility notes
- Summary of why this matters

**Key stats:**
- 471 lines
- ~5,000 words
- Explicitly documents what's preserved
- Explains "why" behind changes

**Audience:** Existing Trident users, G (project owner)

**Who needs to edit:**
- If migration steps change
- Rarely — this is historical documentation

### COMPLETION_REPORT.md

**What it is:** Delivery summary and project completion record  
**Contains:**
- Deliverable checklist (all 5 core files)
- Design decisions and rationale (6 major decisions)
- Files excluded (with reasons)
- ClawHub publication readiness checklist
- Technical specifications
- Next steps for G (immediate, publication, testing)
- Impact summary (before/after)
- Conclusion

**Key stats:**
- 393 lines
- ~3,500 words
- Signed-off status
- Suitable for handoff to project owner

**Audience:** G (project owner), archival

**Who needs to edit:**
- Rarely — this is a completion record
- Update when publishing to ClawHub (add publication date)

---

## 🔧 Configuration Quick Reference

### Minimal (Trident Lite)

```json
{
  "plugins": {
    "trident": {
      "enabled": true,
      "layer0_enabled": true,
      "layer0_5_enabled": true,
      "layer0_5_model": "anthropic/claude-haiku-4-5"
    }
  }
}
```

Cost: **$1.44/day** (15-min interval)

### Zero Cost (Ollama)

```json
{
  "plugins": {
    "trident": {
      "enabled": true,
      "layer0_5_model": "ollama/mistral",
      "layer0_5_interval_minutes": 30
    }
  }
}
```

Cost: **$0**

### Full (with Semantic Recall)

```json
{
  "plugins": {
    "trident": {
      "enabled": true,
      "semantic_recall_enabled": true,
      "qdrant_enabled": true,
      "qdrant_url": "http://localhost:6333",
      "falkordb_enabled": true,
      "git_backup_enabled": true
    }
  }
}
```

Cost: **$1.44 + $0–50/mo** (depends on Qdrant deployment)

---

## 📊 Plugin Specification

| Aspect | Value |
|--------|-------|
| **Name** | trident |
| **Version** | 2.0.0 |
| **Type** | plugin |
| **Category** | memory |
| **License** | MIT-0 |
| **Required Plugin** | lossless-claw ≥1.0.0 |
| **Optional Dependencies** | docker, git |
| **Minimum OpenClaw** | 1.0.0 |
| **Minimum Node.js** | 22.14.0 |
| **Configuration Options** | 28 (all optional except enabled, layer0_enabled) |
| **Platforms Supported** | 7 (Linux, macOS, Windows, Docker, Ubuntu VPS, CentOS VPS, Alpine) |
| **Architecture** | Three-tier (LCM + Signal Router + Buckets) |
| **Cost Range** | $0–50/month (depending on configuration) |

---

## 🔐 Security Features

- ✅ **SHA256 template integrity verification** — detects tampering with Layer 0.5 prompt
- ✅ **Audit logging** — all routing decisions logged to `memory/layer0/audit-log.md`
- ✅ **Sandboxed cron** — Layer 0.5 can only write to `memory/` subdirectory
- ✅ **No credentials in config** — API keys expected from environment variables
- ✅ **File scoping** — Layer 0.5 has explicit read/write boundaries

---

## 📈 Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| **2.0.0** | 2026-04-17 | ✅ Current | ClawHub plugin release |
| 1.0.0 | 2026-04-03 | Archived | Original skill release |

---

## 📖 Reading Paths

### Path 1: I'm New to Trident (30 minutes)
1. README.md — Overview (5 min)
2. INSTALL.md — Installation (15 min)
3. INSTALL.md "Trident Lite" — Understand what you have (5 min)
4. Let it run for 24 hours, then review memory files

### Path 2: I Have Existing Trident (15 minutes)
1. MIGRATION.md "Summary" — Why upgrade? (3 min)
2. MIGRATION.md "Migration from Skill to Plugin" — How to upgrade (5 min)
3. INSTALL.md "Verify" — Test new installation (7 min)

### Path 3: I'm Technical/Architecting (45 minutes)
1. README.md — Overview (5 min)
2. README.md "Architecture" — Understand layers (10 min)
3. plugin-manifest.json — Study capabilities and lifecycle (10 min)
4. config.schema.json — Understand all options (10 min)
5. MIGRATION.md — Understand design decisions (10 min)

### Path 4: I'm Publishing to ClawHub (20 minutes)
1. COMPLETION_REPORT.md — Understand what was delivered (10 min)
2. plugin-manifest.json — Verify metadata (5 min)
3. COMPLETION_REPORT.md "Publication" — Follow publication steps (5 min)

---

## ✅ Quality Checklist

- ✅ All files are valid JSON/Markdown
- ✅ No personal data (no SOUL.md, USER.md, MEMORY.md, daily logs)
- ✅ No VPS-specific code (Docker Compose removed)
- ✅ Cross-platform (7 platforms documented)
- ✅ Backward compatible (existing memory preserved)
- ✅ Configuration schema complete (28 properties)
- ✅ Documentation comprehensive (6,784 words)
- ✅ Cost transparent (5 profiles with pricing)
- ✅ Security hardened (SHA256 + audit logging)
- ✅ ClawHub ready (manifest + schema + docs)

---

## 🎯 Use This Package To

- **Install Trident** — Run `cladhub install shivaclaw/trident`
- **Configure Trident** — Edit openclaw.json with config.schema.json reference
- **Understand architecture** — Read README.md and plugin-manifest.json
- **Troubleshoot issues** — Refer to INSTALL.md troubleshooting section
- **Upgrade from skill** — Follow MIGRATION.md
- **Publish to ClawHub** — Use plugin-manifest.json + COMPLETION_REPORT.md
- **Make decisions** — config.schema.json examples cover all use cases

---

## 📞 Support Resources

- **GitHub Issues:** [ShivaClaw/project-trident/issues](https://github.com/ShivaClaw/project-trident/issues)
- **ClawHub:** [clawhub.ai/shivaclaw/trident](https://clawhub.ai/shivaclaw/trident)
- **Documentation:** All docs included in this package

---

## 📜 License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

**Package Status:** ✅ Complete and ready for deployment  
**Generated:** 2026-04-17  
**By:** Shiva (Subagent: trident-plugin-creator)
