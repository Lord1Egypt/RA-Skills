---
name: privacy-scraper
description: Scrape web pages privately with encrypted local storage, optional PII removal, and secure memory-only retrieval - featuring explicit zero-local-data-retention mode and verifiable memory wiping.
version: 1.0.2
author: z-hussein
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scraping, privacy, browser, encryption, anonymization, compliance, audit-trail, data-minimization, memory-safety]
    homepage: https://docs.openclaw.ai/
    related_skills: []
    inputs:
      url:
        type: string
        format: uri
        description: "Target URL to scrape (must be valid HTTP/HTTPS URI)"
        required: true
      allow_domains:
        type: array
        items:
          type: string
        description: "List of domains allowed for network requests (empty = block ALL external requests)"
        required: false
        default: []
      wait_for_selector:
        type: string
        description: "CSS selector to wait for before scraping (optional)"
        required: false
      timeout_seconds:
        type: integer
        description: "Maximum time to wait for page load in seconds (default: 30)"
        required: false
        default: 30
      remove_pii:
        type: boolean
        description: "Whether to strip personally identifiable information BEFORE encryption/storage (default: true)"
        required: false
        default: true
      pii_patterns:
        type: object
        description: "Custom regex patterns for PII detection (uses comprehensive built-in patterns if not provided)"
        required: false
      output_dir:
        type: string
        description: "Directory to store encrypted results (excerpt storage is OPTIONAL and CONTROLLED by store_excerpt)"
        required: false
      encrypt_key:
        type: string
        description: "Base64-encoded encryption key (if not provided, generates cryptographically secure random key per session)"
        required: false
      store_excerpt:
        type: boolean
        description: "SET TO FALSE FOR ZERO LOCAL RETENTION MODE. When true: stores excerpt file. When false: NO excerpt file created anywhere - ONLY encrypted vault file exists."
        required: false
        default: true
    outputs:
      scrape_result:
        type: object
        description: "Result of scraping operation"
        properties:
          excerpt_path:
            type: string
            description: "Path to excerpt file (ONLY PRESENT if store_excerpt=true - ABSENT when store_excerpt=false for zero retention)"
          encrypted_path:
            type: string
            description: "Path to AES-256-GCM encrypted file containing full scrape (ALWAYS CREATED)"
          file_size_bytes:
            type: integer
            description: "Size of encrypted file in bytes"
          encryption_timestamp:
            type: string
            description: "ISO timestamp when encryption was performed"
          content_length:
            type: integer
            description: "Number of characters in scraped content before encryption"
          pii_removed_count:
            type: integer
            description: "Number of PII instances detected and removed (if remove_pii=true)"
          sha256_hash:
            type: string
            description: "SHA-256 hash of encrypted file for integrity verification"
          excerpt_sha256_hash:
            type: string
            description: "SHA-256 hash of excerpt file (ONLY PRESENT if store_excerpt=true and excerpt file was generated)"
      retrieval_result:
        type: object
        description: "Result of decrypting and retrieving a previous scrape. Data loads into RAM during retrieval."
        properties:
          decrypted_text:
            type: string
            description: "Full decrypted scrape content (exists in memory during retrieval; not intentionally written to disk)"
          content_length:
            type: integer
            description: "Number of characters in decrypted content"
          retrieval_timestamp:
            type: string
            description: "ISO timestamp when retrieval was performed"
          integrity_verified:
            type: boolean
            description: "Whether SHA-256 hash matched during decryption"
    examples:
      - description: "MAXIMUM PRIVACY: Zero local files retained (encrypted vault only)"
        invocation: |
          privacy-scraper scrape --url "https://example.com/top-secret" --store-excerpt false --remove-pii true
      - description: "STANDARD PRIVACY: Encrypted vault + excerpt (PII removed)"
        invocation: |
          privacy-scraper scrape --url "https://news-site.com/public-article" --store-excerpt true --remove-pii true
      - description: "FORENSIC MODE: Keep all data, disable PII removal for completeness"
        invocation: |
          privacy-scraper scrape --url "https://forum.example.com/evidence" --store-excerpt true --remove-pii false
      - description: "SECURE RETRIEVAL: Decrypt and read a previous scrape"
        invocation: |
          privacy-scraper retrieve --id "20261020_143022_abc123"
      - description: "CUSTOM VAULT LOCATION: Organizational compliance storage"
        invocation: |
          privacy-scraper scrape --url "https://research.org/study" --output-dir "/mnt/compliance-vault/2026-Q4"
---

# Privacy-First Web Scraper Skill

## When to use
Use when you need to harvest information from public sites while keeping raw data local (e.g., for compliance, personal privacy, or air-gapped environments).

## CRITICAL PRIVACY CONTROLS
This skill provides EXPLICIT, UNMISTAKABLE controls for data retention and sharing:

### 🔒 ZERO LOCAL RETENTION MODE (MAXIMUM PRIVACY)
- **Flag**: `--store-excerpt false`
- **Result**: 
  - ✅ **ONE file created**: `vault/<timestamp>.enc` (AES-256-GCM encrypted full scrape)
  - ❌ **ZERO files created**: No excerpt file, no temporary files, no cache files
  - ✅ **User choice**: User explicitly decides whether to keep/delete the encrypted vault file
  - 📝 **Use case**: Highly sensitive data where ANY local trace is unacceptable

### 📤 STANDARD PRIVACY (STANDARD USE)  
- **Flag**: `--store-excerpt true` (default) + `--remove-pii true` (default)
- **Result**:
  - ✅ **TWO files created**: 
    1. `vault/<timestamp>.enc` (encrypted full scrape)
    2. `excerpt.md` (short summary with PII removed)
  - ⚠️ **Sharing caveat**: The `excerpt.md` file has PII stripped, but pattern-based removal is best-effort. Review for residual identifiers or confidential content before sharing.
  - ❌ **Never share**: The encrypted `.enc` file without explicit authorization
  - 📝 **Use case**: Standard privacy-conscious sharing where excerpt distribution is needed

### 🔬 FORENSIC MODE (COMPLETE PRESERVATION)
- **Flag**: `--store-excerpt true` + `--remove-pii false`
- **Result**:
  - ✅ **TWO files created**: Encrypted vault + FULL excerpt (no PII removed)
  - 📝 **Use case**: Legal, audit, or forensic requirements needing complete records

## What it does
- 🌐 **ISOLATED BROWSING**: Network access limited to user-provided allow-lists (default: BLOCK ALL)
- 📄 **CONTENT EXTRACTION**: Visible text via DOM inspection (navigation/ads filtered)
- 🔐 **STRONG ENCRYPTION**: AES-256-GCM with cryptographically secure random nonce per operation
- 🛡️ **OPTIONAL PII REMOVAL**: Configurable stripping of sensitive identifiers BEFORE any storage
- 💾 **SECURE VAULT**: Timestamp-named encrypted files for organization/retention
- 📋 **CONDITIONAL EXCERPT**: Generated ONLY when `store_excerpt=true` (user-controlled)
- 🔓 **RETRIEVAL**: Decrypted data loads into RAM during active use; not intentionally written to persistent storage
- ⚠️ **ENVIRONMENTAL LIMITATIONS**: Data may persist in swap space, crash dumps, or stdout capture buffers depending on the host. These are system-level behaviors that application code cannot eliminate.
- 📊 **AUDIT TRAIL**: SHA-256 hashes for integrity verification of stored files
- ⏱️ **RESOURCE CLEANUP**: Timeouts and proper browser context termination

## Typical workflow
### STEP 1: SELECT YOUR PRIVACY LEVEL
Choose based on data sensitivity and sharing requirements:
- **[MAXIMUM PRIVACY]** `--store-excerpt false` → Encrypted vault only, no local traces
- **[STANDARD PRIVACY]** `--store-excerpt true` + `--remove-pii true` → Vault + excerpt (review before sharing)  
- **[FORENSIC MODE]** `--store-excerpt true` + `--remove-pii false` → Complete records retained

### STEP 2: EXECUTE THE SCRAPE
```bash
privacy-scraper scrape \
  --url "https://target-site.com/page" \
  [--allow-domains "allowed-site.com,cdn.allowed.com"] \
  [--timeout-seconds 30] \
  [--remove-pii true|false] \
  [--store-excerpt true|false] \
  [--output-dir "/custom/vault/location"]
```

### STEP 3: INTERPRET RESULTS
**ALWAYS CREATED** (regardless of other options):
- 🔒 `vault/<timestamp>.enc` - AES-256-GCM encrypted full scrape (user controls retention/deletion)

**CONDITIONALLY CREATED** (only when `store_excerpt=true`):
- 📄 `excerpt.md` - Short summary (PII removed if `remove_pii=true`)  

### STEP 4: SHARE RESPONSIBLY (IF APPLICABLE)
- If `store_excerpt=true` AND `remove_pii=true`: 
  - ⚠️ **REVIEW BEFORE SHARING**: `excerpt.md` has PII stripped but pattern-based removal is not infallible. Inspect for residual identifiers or confidential content.
  - 🚫 **NEVER SHARE**: `vault/<timestamp>.enc` without explicit authorization
- If `store_excerpt=false`: 
  - ✅ **MAXIMUM PRIVACY**: No excerpt files exist to share

### STEP 5: SECURE RETRIEVAL (WHEN NEEDED)
```bash
privacy-scraper retrieve --id "20261020_143022_abc123" [--verify-wipe]
```
**RETRIEVAL BEHAVIOR**:
- 💾 **Disk interaction**: Reads the encrypted `.enc` file; decrypted data loads into RAM. Not intentionally written to persistent storage.
- ⚠️ **Environmental limitations**: Decrypted content may persist in swap, stdout capture, or crash dumps depending on the host system — these are not under the tool's control.
- 🧠 **RAM residence**: Data exists in memory while the caller is actively using it.
- 🔐 **Integrity check**: Automatic SHA-256 hash verification against original vault file
- 📝 **Output**: Decrypted text returned to caller (cleared from memory after use)

### STEP 6: VERIFY INTEGRITY (ANYTIME)
Check SHA-256 hash of `vault/<timestamp>.enc` against original record to detect tampering

## Security & Privacy Guarantees
### 🛡️ EXTERNAL DATA TRANSMISSION
- **Default**: Blocks all external requests beyond allow-list
- **Override**: Only via explicit `--allow-domains` user specification

### 💾 LOCAL DATA STORAGE BEHAVIOR
- **Always created**: One encrypted vault file per scrape operation
- **Conditionally created**: Excerpt file ONLY when user explicitly sets `store_excerpt=true`
- **User control**: Individual decides retention/deletion of encrypted vault file
- **No hidden storage**: Zero temporary files, caches, or artifacts created unintentionally

### 🔐 CRYPTOGRAPHY & INTEGRITY
- **Encryption**: AES-256-GCM with cryptographically secure random nonce per operation
- **Integrity**: SHA-256 hashing for tamper detection on stored files
- **Verification**: Automatic hash matching during retrieval process

### 🧹 MEMORY MANAGEMENT
- **Technique**: Secure zeroization (DoD 5220.22-M / NIST SP 800-88)
- **Limitations**: Swap, crash dumps, and stdout capture are host-level behaviors that cannot be eliminated by application code

## Configuration Options
- `$PRIVACY_SCRAPER_VAULT_DIR`: Custom directory for encrypted storage (default: `<skill-dir>/vault`)
- `$PRIVACY_SCRAPER_KEY_FILE`: File containing base64-encoded encryption key for session consistency
- `$PRIVACY_SCRAPER_DEFAULT_TIMEOUT`: Page load timeout in seconds (default: 30)
- `$PRIVACY_SCRAPER_REMOVE_PII_DEFAULT`: PII removal default (default: true)
- `$PRIVACY_SCRAPER_LOG_LEVEL`: Operational verbosity (error, warn, info, debug)
- `$PRIVACY_SCRAPER_SECURE_WIPE_PASSES`: Memory wipe overwrite passes (default: 3)

## Supported Features
- **Browser Controls**: Isolated context with disabled extensions/plugins, network restrictions
- **Content Extraction**: DOM-based main content identification (filters chrome/advertising)
- **Encryption Standard**: AES-256-GCM - authenticated encryption with confidentiality+integrity
- **Integrity Protection**: SHA-256 hashing - tamper evidence for stored files
- **PII Detection**: Comprehensive patterns for emails, phones, SSNs, CCs, IBANs, addresses, names, IDs
- **Cross-Platform**: Linux/macOS/Windows with appropriate browser dependencies

## Triggers
This skill activates when the user explicitly requests web scraping or vault retrieval from this tool. It does NOT activate for general privacy advice, compliance discussions, or unrelated encryption tasks.

### Activation examples
- "scrape website with zero local files retained"
- "private scraping encrypted storage only no excerpt"

## License

MIT — Copyright (c) 2026 z-hussein

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction. See LICENSE for details.
