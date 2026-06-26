# PassManager 🔐

**Enterprise-grade password management system for AI assistants.**

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](LICENSE)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)

> **⚠️ Security Advisory (v1.1.0)**  
> Older versions (v1.0.0) used base64 encoding masquerading as encryption. v1.1.0 replaces it with proper **AES-256-GCM** authenticated encryption.

---

## 📋 Overview

PassManager is an enterprise-grade credential management system for AI assistant teams. It provides **AES-256-GCM** authenticated encryption, RBAC (Role-Based Access Control), full audit logging, and backup/restore capabilities—all in a zero-network-dependency SQLite database.

### Key Features
- 🔐 **AES-256-GCM** — Random nonce per encryption, key derived via PBKDF2 (600K iterations)
- 👥 **RBAC** — admin / user / auditor / guest roles
- 📝 **Full Audit Trail** — Every operation logged (DB + file dual write)
- 💾 **Backup & Restore** — Automated & manual backup with safe restoration
- 🚫 **Zero Network** — Fully local SQLite storage, no external services

---

## 🔧 Quick Start

### Prerequisites
```bash
pip3 install cryptography
```

### 1. Initialize
```bash
passmanager init "YourMasterPassword" --admin admin
```

### 2. Add a Credential
```bash
passmanager add admin "YourMasterPassword" email Gmail user@example.com "MyPassword123" --notes "My email account"
```

### 3. Retrieve a Credential
```bash
passmanager get admin "YourMasterPassword" email Gmail user@example.com --show-password
```

### 4. List Credentials
```bash
passmanager list admin --type email
```

---

## 📖 Command Reference

### Credential Management

| Command | Usage |
|---------|-------|
| `add` | `passmanager add <user> <master_pwd> <type> <service> <username> <password> [--notes]` |
| `get` | `passmanager get <user> <master_pwd> <type> <service> [username] [--show-password]` |
| `list` | `passmanager list <user> [--type TYPE]` |
| `update` | `passmanager update <user> <master_pwd> <type> <service> <username> [--password] [--notes]` |
| `delete` | `passmanager delete <user> <type> <service> [username]` |

### System Management

| Command | Usage |
|---------|-------|
| `init` | `passmanager init <master_password> [--admin NAME]` |
| `status` | `passmanager status` |
| `backup` | `passmanager backup [--output PATH]` |
| `restore` | `passmanager restore <backup_file>` |
| `audit` | `passmanager audit [--limit N] [--user NAME] [--action ACTION]` |

### Team Management

| Command | Usage |
|---------|-------|
| `team add` | `passmanager team add <admin> <name> [--role admin/user/auditor/guest]` |
| `team list` | `passmanager team list` |
| `team remove` | `passmanager team remove <admin> <name>` |
| `team update` | `passmanager team update <admin> <name> <role>` |

---

## 🔒 Security Architecture

### Encryption Scheme (AES-256-GCM)
```
Master Password (user input)
    │
    ▼
PBKDF2-SHA256 (600,000 iterations + random 32-byte salt)
    │
    ▼
AES-256 Key (32 bytes)
    │
    ▼
AES-GCM Encryption (random 12-byte nonce per operation)
    │
    ▼
Ciphertext stored in SQLite (nonce + ciphertext + auth tag)
```

### Permission Matrix

| Operation | admin | user | auditor | guest |
|-----------|-------|------|---------|-------|
| Add credential | ✅ | ✅ | ❌ | ❌ |
| View credential | ✅ | ✅ | ✅ | ✅ |
| List credentials | ✅ | ✅ | ✅ | ❌ |
| Update credential | ✅ | ✅ | ❌ | ❌ |
| Delete credential | ✅ | ❌ | ❌ | ❌ |
| View audit log | ✅ | ❌ | ✅ | ❌ |
| Backup/restore | ✅ | ❌ | ❌ | ❌ |
| Team management | ✅ | ❌ | ❌ | ❌ |

---

## 📁 Directory Structure

```
passmanager/
├── SKILL.md                  # This file
├── config.json               # Skill configuration
├── README.md                 # Project readme
├── scripts/
│   ├── passmanager.py        # ⭐ Main program v1.1.0
│   └── backup.py             # Backup utility
├── docs/
│   ├── passmanager_skill.md         # Detailed skill docs
│   └── passmanager_training.md      # Training manual
└── examples/                 # Usage examples (TBD)
```

---

## 📊 Status

- ✅ **v1.0.0** Initial release (base64 obfuscation ❌ — deprecated)
- ✅ **v1.1.0** Current: AES-256-GCM ✅, RBAC ✅, Audit Logging ✅, Backup/Restore ✅

---

**Author**: iSenlink  
**Version**: 1.1.0  
**Last Updated**: 2026-05-29  
**Status**: ✅ Production Ready
