# OpenClaw Key Management Skill - Usage Examples

## Basic Workflow

### 1. Installation
```bash
# From your OpenClaw workspace
git clone https://github.com/your-repo/openclaw-key-management-skill skills/openclaw-key-management
# OR
./skills/openclaw-key-management/install.sh
```

### 2. Initialize
```bash
./skills/openclaw-key-management/scripts/key_manager.sh init
```

### 3. Add Credentials
```bash
# Interactive prompt
./skills/openclaw-key-management/scripts/key_manager.sh add instreet_api_key

# Or pipe from secure source
echo "sk_inst_123456789" | ./skills/openclaw-key-management/scripts/key_manager.sh add instreet_api_key
```

### 4. Use in Memory Files
Replace plaintext credentials in `MEMORY.md`:
```markdown
### Before (INSECURE)
- **Instreet API Key**: sk_inst_123456789

### After (SECURE)  
- **Instreet API Key**: {SECRET:instreet_api_key}
```

### 5. Access in Scripts
```javascript
// In your OpenClaw workflows
const vault = require('./skills/openclaw-key-management/scripts/key_vault.js');
const secureVault = new vault('/path/to/workspace');

await secureVault.initialize();
const apiKey = await secureVault.getSecret('instreet_api_key');

// Use apiKey in your requests
// The credential will be automatically zeroed after 30 seconds
```

## Advanced Usage

### Migration from Existing Setup
```bash
# Automatically extract and secure existing credentials
./skills/openclaw-key-management/scripts/key_manager.sh migrate

# Verify migration
grep -r "{SECRET:" MEMORY.md
```

### Backup and Restore
```bash
# Create manual backup
./skills/openclaw-key-management/scripts/key_manager.sh backup

# List backups
ls .secrets/backup/

# Restore from backup (manual process)
cp .secrets/backup/vault_2026-03-14.json.enc .secrets/vault.json.enc
```

### High-Security Mode
```bash
# Switch to passphrase mode
./skills/openclaw-key-management/setup.sh
# Choose option 2

# Now all operations require passphrase
./skills/openclaw-key-management/scripts/key_manager.sh get my_secret
# Prompts for passphrase
```

## Integration Patterns

### With OpenClaw Memory System
The skill automatically integrates with OpenClaw's four-tier memory system:

- **Tier 1 (Ultra-short-term)**: Runtime credential cache
- **Tier 2 (Short-term)**: Never stores credentials in daily logs  
- **Tier 3 (Medium-term)**: Project-specific credentials in encrypted vault
- **Tier 4 (Long-term)**: Secure references only in MEMORY.md

### With Other Skills
Other skills can access credentials securely:
```javascript
// In another skill
const { getSecret } = require('../openclaw-key-management/scripts/key_vault.js');
const apiKey = await getSecret('required_api_key');
```

## Security Best Practices

### ✅ Recommended
- Run `./setup.sh` to configure security mode appropriately
- Regularly backup your `.secrets/` directory
- Use high-security mode for production deployments
- Monitor access logs if enabled

### ❌ Avoid
- Sharing your `.secrets/` directory without proper encryption
- Disabling memory safety features
- Storing master key backups in the same location as the vault
- Using weak system configurations

## Troubleshooting Common Issues

### "Credential not found"
- Verify the credential name matches exactly
- Check that the vault was initialized properly
- Ensure you're in the correct workspace directory

### "Decryption failed"  
- System changes (hostname, machine ID) may break convenience mode
- Restore from backup or re-migrate credentials
- Consider switching to high-security mode for better portability

### "Permission denied"
- Ensure proper file permissions on `.secrets/` directory
- Run with appropriate user privileges
- Check SELinux/AppArmor policies if applicable

## Performance Considerations

- **Memory usage**: Minimal overhead for typical credential counts (<100)
- **CPU usage**: Encryption/decryption is fast for small credentials
- **Disk I/O**: Vault is loaded once per session, then cached in memory
- **Network**: No external dependencies or network calls

For large-scale deployments with thousands of credentials, consider:
- Increasing Node.js memory limits
- Implementing credential rotation to reduce vault size
- Using separate vaults for different security domains