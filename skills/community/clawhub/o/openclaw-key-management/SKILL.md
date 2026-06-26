---
name: openclaw-key-management
version: 1.0.0
description: Secure credential storage system for OpenClaw that encrypts and protects API keys, tokens, and sensitive credentials from memory file compromise.
---

# OpenClaw Key Management Skill 🔐

A comprehensive security key management system that protects your AI assistant's credentials even if memory files are compromised.

## When to Use

- **Before storing any API keys, passwords, or tokens** in your OpenClaw memory files
- **When you need to secure existing credentials** already stored in MEMORY.md or daily logs
- **For any OpenClaw deployment** that handles sensitive authentication data
- **When sharing your workspace** with others or backing up to cloud storage

## Core Features

### 🔒 Strong Encryption
- **AES-256-GCM** authenticated encryption
- **PBKDF2-HMAC-SHA256** key derivation (100,000 iterations)
- Per-credential random salts and initialization vectors
- Tamper detection with authentication tags

### 🧠 Memory Safety
- Credentials exist in memory for only **30 seconds** during active use
- Automatic secure zeroing of plaintext credentials
- Memory locking to prevent swapping to disk
- Runtime credential cache with automatic cleanup

### 📁 Separation of Concerns
- Credentials never stored in `MEMORY.md` or daily log files
- Dedicated encrypted vault in `.secrets/vault.json.enc`
- Automatic detection and blocking of credential logging attempts
- Secure references like `{SECRET:api_key_name}` in memory files

### ⚙️ Dual Security Modes
- **Convenience Mode**: System key derived from machine ID + hostname (automatic decryption)
- **High-Security Mode**: User passphrase required at each session start
- Configurable via `config/key_management.json`

### 🛠️ Easy Management
- CLI tool for adding, retrieving, and managing credentials
- Automatic backup system with versioned encrypted backups
- Migration tool to extract existing credentials from memory files
- Integration with OpenClaw's existing memory architecture

## Installation

### Prerequisites
- OpenClaw 2026.3.13 or later
- Node.js 18+ (for encryption module)
- Standard Unix-like system (Linux/macOS)

### Setup Steps
```bash
# 1. Clone or copy this skill to your skills directory
cp -r openclaw-key-management-skill ~/.openclaw/your-workspace/skills/

# 2. Initialize the key vault
cd ~/.openclaw/your-workspace
./skills/openclaw-key-management/scripts/key_manager.sh init

# 3. Configure security mode (optional)
# Edit skills/openclaw-key-management/config/key_management.json
# Set "master_key_mode" to "system_key" (default) or "passphrase"

# 4. Migrate existing credentials (if any)
./skills/openclaw-key-management/scripts/key_manager.sh migrate
```

## Usage

### Adding Credentials
```bash
# Add a new credential
./skills/openclaw-key-management/scripts/key_manager.sh add my_api_key

# Add with metadata
./skills/openclaw-key-management/scripts/key_manager.sh add instreet_api_key
```

### Retrieving Credentials
```bash
# Get credential value (automatically decrypted)
./skills/openclaw-key-management/scripts/key_manager.sh get my_api_key

# List all stored credentials
./skills/openclaw-key-management/scripts/key_manager.sh list
```

### Integration with OpenClaw
In your OpenClaw workflows, reference credentials using the secure placeholder format:
```markdown
### External Service
- **API Key**: {SECRET:my_api_key}
```

The system automatically intercepts these references and provides the decrypted value at runtime.

## Security Architecture

### File Structure
```
workspace/
├── .secrets/                    # Encrypted secrets directory
│   ├── master.key               # Encrypted master key
│   ├── vault.json.enc           # Main encrypted credential vault
│   ├── backup/                  # Versioned encrypted backups
│   └── temp/                    # Ephemeral runtime files
├── skills/openclaw-key-management/
│   ├── scripts/key_vault.js     # Node.js encryption module
│   ├── scripts/key_manager.sh   # CLI management tool
│   └── config/key_management.json # Configuration template
└── MEMORY.md                    # Safe references only: {SECRET:name}
```

### Threat Model & Mitigations

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Memory file compromise | High | Credentials never stored in plaintext |
| Runtime memory dump | Medium | Short credential lifespan + secure zeroing |
| Master key theft | Critical | Optional passphrase protection |
| Backup exposure | Medium | Backups encrypted with same strong crypto |
| Malicious skill/plugin | High | Credential access requires explicit permission |

## Configuration Options

### `config/key_management.json`
```json
{
  "version": "1.0",
  "master_key_mode": "system_key", // "system_key" or "passphrase"
  "encryption": {
    "algorithm": "aes-256-gcm",
    "pbkdf2_iterations": 100000,
    "salt_length": 16,
    "iv_length": 12
  },
  "runtime": {
    "credential_timeout_seconds": 30,
    "enable_memory_locking": true,
    "auto_cleanup_on_exit": true
  },
  "backup": {
    "enabled": true,
    "max_backups": 10,
    "backup_interval_hours": 24
  }
}
```

## Migration Guide

### From Existing OpenClaw Deployments
1. **Backup your current workspace**
2. **Install this skill** following the installation steps
3. **Run migration tool**: `./scripts/key_manager.sh migrate`
4. **Verify**: Check that `MEMORY.md` now contains `{SECRET:name}` references
5. **Test**: Ensure your workflows still function correctly

### Manual Migration
If automatic migration fails, manually:
1. Extract credentials from your memory files
2. Add them using: `./scripts/key_manager.sh add credential_name`
3. Replace plaintext values in memory files with `{SECRET:credential_name}`

## Best Practices

### ✅ Do
- Always use this skill for any sensitive credentials
- Regularly backup your encrypted vault
- Use high-security mode for production deployments
- Review and update your configuration periodically

### ❌ Don't
- Store plaintext credentials in memory files
- Share your `.secrets/` directory without encryption
- Disable memory safety features without understanding risks
- Use weak system configurations (outdated Node.js, etc.)

## API Reference

### Node.js Module
```javascript
const SecureKeyVault = require('./skills/openclaw-key-management/scripts/key_vault.js');
const vault = new SecureKeyVault('/path/to/workspace');

await vault.initialize();
await vault.setSecret('api_key', 'your-secret-value');
const secret = await vault.getSecret('api_key');
```

### CLI Commands
- `init` - Initialize key vault
- `add NAME` - Add new secret
- `get NAME` - Get secret value
- `list` - List all secrets
- `backup` - Create backup
- `migrate` - Migrate existing credentials

## Troubleshooting

### Common Issues
- **"No vault file found"**: Run `init` command first
- **Decryption failures**: Verify system hasn't changed (machine ID, hostname)
- **Permission errors**: Ensure proper file permissions on `.secrets/` directory
- **Memory issues**: Increase Node.js memory limit if handling many credentials

### Recovery Procedures
- **Lost master key (convenience mode)**: Restore from backup or re-migrate credentials
- **Forgotten passphrase (high-security mode)**: No recovery possible (by design)
- **Corrupted vault**: Restore from latest backup in `.secrets/backup/`

## Contributing

This skill follows OpenClaw AgentSkills specification. Contributions welcome:
- Security improvements
- Additional encryption algorithms
- Better integration with OpenClaw core
- Documentation enhancements

## License

MIT License - Free to use, modify, and distribute.

---

**Remember**: Security is a process, not a product. This skill provides strong protection, but always follow security best practices in your overall OpenClaw deployment.