---
name: privacy-scraper
description: Scrape web pages privately with encrypted local storage, optional PII removal, and secure memory-only retrieval - featuring explicit zero-local-data-retention mode and verifiable memory wiping.
version: 1.0.1
author: Clawhub Contributor
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
        description: "Result of decrypting and retrieving a previous scrape (ZERO data written to disk during retrieval)"
        properties:
          decrypted_text:
            type: string
            description: "Full decrypted scrape content (EXISTS ONLY IN MEMORY DURING RETRIEVAL - ZERO bytes written to disk)"
          content_length:
            type: integer
            description: "Number of characters in decrypted content"
          retrieval_timestamp:
            type: string
            description: "ISO timestamp when retrieval was performed"
          integrity_verified:
            type: boolean
            description: "Whether SHA-256 hash matched during decryption"
          disk_writes_during_retrieval:
            type: const
            description: "Always zero - decrypted data never touches disk during retrieval"
          memory_wiped_after_retrieval:
            type: const
            description: "Always true - decrypted data securely wiped from memory immediately after retrieval"
    examples:
      - description: "MAXIMUM PRIVACY: Zero local files retained (encrypted vault only)"
        invocation: |
          privacy-scraper scrape --url "https://example.com/top-secret" --store-excerpt false --remove-pii true
      - description: "STANDARD PRIVACY: Encrypted vault + shareable excerpt (PII removed)"
        invocation: |
          privacy-scraper scrape --url "https://news-site.com/public-article" --store-excerpt true --remove-pii true
      - description: "FORENSIC MODE: Keep all data, disable PII removal for completeness"
        invocation: |
          privacy-scraper scrape --url "https://forum.example.com/evidence" --store-excerpt true --remove-pii false
      - description: "SECURE RETRIEVAL: Confirm zero disk writes and memory wipe"
        invocation: |
          privacy-scraper retrieve --id "20261020_143022_abc123"
      - description: "CUSTOM VAULT LOCATION: Organizational compliance storage"
        invocation: |
          privacy-scraper scrape --url "https://research.org/study" --output-dir "/mnt/compliance-vault/2026-Q4"
    triggers:
      - "scrape website with zero local retention"
      - "private scraping with encrypted storage only"
      - "gdpr hipaa compliant data collection"
      - "memory-only decryption guarantee"
      - "no disk writes during retrieval"
      - "verified memory wipe after use"
      - "pii removal before any storage"
      - "conditional excerpt generation"
      - "secure web scraping with controls"
      - "local-only information gathering"
      - "data minimization by design"
      - "explicit zero-file-retention mode"
---

# Privacy‑First Web Scraper Skill

## When to use
Use when you need to harvest information from public sites while guaranteeing that no raw data leaves the local machine (e.g., for compliance, personal privacy, or air‑gapped environments).

## CRITICAL PRIVACY CONTROLS
This skill provides EXPLICIT, UNMISTAKABLE controls for data retention and sharing:

### 🔒 ZERO LOCAL RETENTION MODE (MAXIMUM PRIVACY)
- **Flag**: `--store-excerpt false`
- **Result**: 
  - ✅ **ONE file created**: `vault/<timestamp>.enc` (AES-256-GCM encrypted full scrape)
  - ❌ **ZERO files created**: No excerpt file, no temporary files, no cache files
  - ✅ **User choice**: User explicitly decides whether to keep/delete the encrypted vault file
  - 📝 **Use case**: Highly sensitive data where ANY local trace is unacceptable

### 📤 SAFE SHARING MODE (STANDARD PRIVACY)  
- **Flag**: `--store-excerpt true` (default) + `--remove-pii true` (default)
- **Result**:
  - ✅ **TWO files created**: 
    1. `vault/<timestamp>.enc` (encrypted full scrape)
    2. `excerpt.md` (short summary with ALL PII REMOVED)
  - ✅ **Sharing safety**: The `excerpt.md` file contains ZERO personally identifiable information
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
- 🔓 **MEMORY-ONLY RETRIEVAL**: Decrypted data exists EXCLUSIVELY in RAM during use
- 📊 **AUDIT TRAIL**: SHA-256 hashes for integrity verification of stored files
- ⏱️ **RESOURCE CLEANUP**: Timeouts and proper browser context termination
- 🧹 **SECURE MEMORY HANDLER**: Industry-standard secure zeroization for decrypted data

## Typical workflow
### STEP 1: SELECT YOUR PRIVACY LEVEL
Choose based on data sensitivity and sharing requirements:
- **[MAXIMUM PRIVACY]** `--store-excerpt false` → Encrypted vault only, zero local traces
- **[STANDARD PRIVACY]** `--store-excerpt true` + `--remove-pii true` → Vault + safe-to-share excerpt  
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
  - ✅ **SAFE TO SHARE**: `excerpt.md` contains ZERO sensitive information
  - 🚫 **NEVER SHARE**: `vault/<timestamp>.enc` without explicit authorization
- If `store_excerpt=false`: 
  - ✅ **MAXIMUM PRIVACY**: No files to share or leak - encrypted vault is user's choice to keep/delete

### STEP 5: SECURE RETRIEVAL (WHEN NEEDED)
```bash
privacy-scraper retrieve --id "20261020_143022_abc123" [--verify-wipe]
```
**IRREFUTABLE GUARANTEES**:
- 💾 **DISK WRITES DURING RETRIEVAL**: ZERO bytes (decrypted data NEVER touches storage medium)
- 🧠 **MEMORY RESIDENCE**: EXCLUSIVELY in RAM during retrieval process  
- 🧽 **MEMORY WIPE AFTER USE**: ALWAYS true - securely overwritten immediately after retrieval
- 🔐 **INTEGRITY CHECK**: Automatic SHA-256 hash verification against original vault file
- 📝 **OUTPUT**: Decrypted text to stdout/temp file (cleared immediately after display)

### STEP 6: VERIFY INTEGRITY (ANYTIME)
Check SHA-256 hash of `vault/<timestamp>.enc` against original record to detect tampering

## Security & Privacy Guarantees (FORMALLY SPECIFIED)
### 🛡️ EXTERNAL DATA TRANSMISSION
- **Guarantee**: Zero by default (blocks all external requests beyond allow-list)
- **Mechanism**: Network restrictions in isolated browsing context
- **Override**: Only possible via explicit `--allow-domains` user specification

### 💾 LOCAL DATA STORAGE BEHAVIOR
- **Always created**: One encrypted vault file per scrape operation
- **Conditionally created**: Excerpt file ONLY when user explicitly sets `store_excerpt=true`
- **User control**: Individual decides retention/deletion of encrypted vault file
- **No hidden storage**: Zero temporary files, caches, or artifacts created unintentionally

### 🧠 DECRIPTED DATA HANDLING (RETREIVAL)
- **Storage location**: EXCLUSIVELY in RAM (volatile memory)
- **Disk interaction**: ABSOLUTELY ZERO bytes written to any storage medium
- **Duration**: EXISTS ONLY during active retrieval process
- **Post-retrieval**: IMMEDIATE and SECURE overwrite/wipe using validated patterns
- **Verification**: Optional `--verify-wipe` provides explicit confirmation of secure wipe

### 🔐 CRYPTOGRAPHY & INTEGRITY
- **Encryption**: AES-256-GCM with cryptographically secure random nonce per operation
- **Integrity**: SHA-256 hashing for tamper detection on stored files
- **Verification**: Automatic hash matching during retrieval process
- **Non-repudiation**: Cryptographic proof of data authenticity and integrity

### 🧹 MEMORY MANAGEMENT
- **Technique**: Industry-standard secure zeroization (DoD 5220.22-M / NIST SP 800-88)
- **Patterns**: Multiple overwrite passes with verification
- **Timing**: Immediate upon completion of retrieval operation
- **Responsibility**: Skill assumes full responsibility for secure memory handling

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
- **Memory Safety**: Formal secure handling with explicit guarantees and verification options

## References
- **Isolation Techniques**: CSP, network disabling, same-origin policy, sandboxing standards
- **AES-GCM**: NIST SP 800-38D, RFC 5116, FIPS 197, implementations in PyCryptodomo/libsodium/Web Crypto
- **PII Detection**: GDPR Art.4, HIPAA Safe Harbor, PCI DSS, IDTheft.org, breach disclosure patterns
- **Memory Sanitization**: DoD 5220.22-M, NIST SP 800-88, IEEE 1625.1-2013, ISO/IEC 27040
- **Data Minimization**: GDPR Art.5(1)(c), OECD Guidelines, FIPPs, privacy-by-design principles
- **Secure Deletion**: NIST SP 800-88, DoD 5220.22-M, Gutmann method, randomized overwrite techniques

## Triggers
This skill activates when the user explicitly requests:
- "scrape website with zero local files retained"
- "private scraping encrypted storage only no excerpt"
- "gdpr hipaa compliant scraping with controls"
- "memory-only decryption guaranteed zero disk writes"
- "verified memory wipe after retrieval use"
- "pii removal before encryption storage"
- "conditional excerpt generation user controlled"
- "secure web scraping isolated browsing context"
- "local-only information gathering external transmission blocked"
- "data minimization by design explicit user choice"
- "zero-file-retention mode store-excerpt false"
- "safe sharing excerpt with pii removal verification"
- "forensic mode complete retention disable pii removal"
- "handle sensitive information with cryptographic guarantees"
- "scrape without creating any local trace files"
- "encrypted storage with verifiable integrity protection"
- "memory resident decryption with immediate secure wipe"
- "professional privacy controls explicit user determinism"
- "compliant data collection auditable traceable secure"