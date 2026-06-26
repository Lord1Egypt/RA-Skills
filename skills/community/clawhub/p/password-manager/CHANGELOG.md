# Changelog

All notable changes to password-manager will be documented in this file.

## [1.0.4] - 2026-03-03

### ✨ Added
- **CLI Command: `update`** - Update existing entries without re-adding
  - `password-manager update --name <name> --password <new-pwd>`
  - `password-manager update --name <name> --username <user> --tags <tags> --notes <notes>`
  
- **CLI Command: `change-password`** - Change master password without reinitializing
  - `password-manager change-password --old <old-password> --new <new-password>`
  - Vault is automatically re-encrypted with new password
  - Cache is updated automatically

- **Environment Variable Support** - `PASSWORD_MANAGER_MASTER_PASSWORD` for automation

- **Help Documentation** - Updated with new commands and options

### 🔧 Fixed
- **Cache Reuse Logic** - Fixed issue where cache was rebuilt on every operation
  - Now properly reuses existing cache within 48-hour window
  - Only rebuilds when cache is missing or expired
  
- **Password Generation Parameters** - Fixed `--include-symbols false` parameter parsing
  - Now supports both `--no-symbols` and `--include-symbols false`
  
- **saveVault Return Value** - Added return value with write verification
  - Returns `{ success: boolean, entries?: number, error?: string }`
  - Verifies write by attempting to decrypt after save

### 📝 Updated
- **SKILL.md** - Added documentation for new CLI commands
- **MEMORY.md** - Added bug fix records and test results
- **password-manager-requirements.md** - Created comprehensive requirements specification

### 🧪 Testing
- **Three independent model tests** - All passed
  - qwen3-coder-plus: 13/13 tests passed
  - qwen3-max-2026-01-23: 16/16 acceptance criteria met
  - MiniMax-M2.5: 7/7 tests passed

- **Test Coverage**
  - Core functionality: ✅ init, add, get, update, delete, search, list
  - New features: ✅ update command, change-password command
  - Bug fixes: ✅ cache reuse, parameter parsing, saveVault return value

### 📊 Acceptance Status (AT1-AT16)
- ✅ 16/16 acceptance criteria met
- ✅ All core CRUD operations working
- ✅ Security requirements verified
- ✅ Performance requirements met

---

## [1.0.3] - 2026-03-02

### ✨ Added
- Published to ClawHub (v1.0.3)
- Full English translation (13 files)
- Installed on all 5 Agent workspaces

### 🔧 Fixed
- PTY interactive input support
- Write verification mechanism
- deriveCacheKey with fixed salt

---

## [1.0.0] - 2026-02-28

### ✨ Added
- Initial release
- F1-F16 all features implemented
- 10 OpenClaw tools
- 45 unit tests
- Security score: 5.5/10 → 9.0/10

---

**Version Format**: [MAJOR.MINOR.PATCH]
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)
