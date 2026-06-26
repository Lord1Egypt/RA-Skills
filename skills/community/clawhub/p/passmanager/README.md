# PassManager 🔐

> Enterprise-grade password management system for AI assistants

**Version 1.1.0** — True AES-256-GCM encryption, RBAC, audit logging, backup/restore.

> ⚠️ v1.1.0 Security Fix: Older v1.0.0 used base64 encoding masquerading as encryption. v1.1.0 replaces it with true AES-256-GCM authenticated encryption.

## Quick Start

```bash
# 1. Install dependency
pip3 install cryptography

# 2. Initialize (first use)
passmanager init "YourMasterPassword" --admin admin

# 3. Add a credential
passmanager add admin "YourMasterPassword" email Gmail user@example.com "password123"

# 4. Get a credential
passmanager get admin "YourMasterPassword" email Gmail user@example.com --show-password
```

## Features

- 🔐 **True AES-256-GCM** encryption with random nonces
- 🔑 **PBKDF2-SHA256** key derivation (600K iterations)
- 👥 **RBAC**: admin / user / auditor / guest
- 📝 **Full audit trail** (DB + file dual write)
- 💾 **Backup & restore** with key preservation
- 🚫 **Zero network** — fully local SQLite storage

## Documentation

| File | Content |
|------|---------|
| [SKILL.md](SKILL.md) | Full skill reference |
| [scripts/passmanager.py](scripts/passmanager.py) | Main program source |
| [docs/passmanager_skill.md](docs/passmanager_skill.md) | Detailed skill documentation |
| [docs/passmanager_training.md](docs/passmanager_training.md) | Training manual |

## Security Notice

**PassManager v1.1.0 uses real AES-256-GCM encryption** via the `cryptography` library.
Previous versions (v1.0.0) used only base64 encoding — do not use v1.0.0 for sensitive data.

## License

MIT

---

**Author**: iSenlink  
**Version**: 1.1.0  
**Last Updated**: 2026-05-29
