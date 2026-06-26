# OpenClaw Key Management Skill - Test Plan

## Test Objectives
- Verify skill installation process works correctly
- Validate encryption/decryption functionality
- Test both convenience and high-security modes
- Ensure memory safety features work as expected
- Confirm skill-vetter security audit passes

## Test Environment
- **OS**: Ubuntu 24.04.1 LTS
- **OpenClaw**: 2026.3.13
- **Node.js**: v24.14.0
- **Workspace**: /home/jiutong/.openclaw/zhaining

## Test Cases

### TC01: Installation Process
**Description**: Verify the skill can be installed using the install.sh script
**Steps**:
1. Run `./install.sh` from skill directory
2. Verify files are copied to `skills/openclaw-key-management/`
3. Verify `.secrets/` directory is created
4. Verify vault initialization completes successfully
**Expected Result**: Installation completes without errors, all files present

### TC02: Basic Credential Operations
**Description**: Test adding, retrieving, and listing credentials
**Steps**:
1. Add a test credential: `./scripts/key_manager.sh add test_key`
2. Retrieve the credential: `./scripts/key_manager.sh get test_key`
3. List all credentials: `./scripts/key_manager.sh list`
4. Verify retrieved value matches original
**Expected Result**: All operations succeed, values match exactly

### TC03: Convenience Mode (System Key)
**Description**: Test automatic decryption using system key
**Steps**:
1. Ensure config has `"master_key_mode": "system_key"`
2. Add credential in one session
3. Restart shell/session
4. Retrieve credential without password prompt
**Expected Result**: Credential accessible without manual intervention

### TC04: High-Security Mode (Passphrase)
**Description**: Test passphrase-based decryption
**Steps**:
1. Run `./setup.sh` and choose high-security mode
2. Add credential
3. Attempt to retrieve credential
4. Verify passphrase prompt appears
5. Enter correct passphrase
**Expected Result**: Passphrase required, correct passphrase grants access

### TC05: Memory Safety
**Description**: Verify credentials are zeroed after timeout
**Steps**:
1. Add credential
2. Retrieve credential (starts 30-second timer)
3. Wait 35 seconds
4. Attempt to retrieve again
5. Check memory usage during operation
**Expected Result**: Second retrieval requires re-decryption, memory usage drops after timeout

### TC06: Migration Functionality
**Description**: Test automatic migration from existing memory files
**Steps**:
1. Add plaintext credential to MEMORY.md
2. Run `./scripts/key_manager.sh migrate`
3. Verify MEMORY.md contains `{SECRET:name}` reference
4. Verify credential is in encrypted vault
5. Test retrieval works
**Expected Result**: Migration completes, references updated, functionality preserved

### TC07: Backup and Restore
**Description**: Test backup creation and restoration
**Steps**:
1. Add multiple credentials
2. Run `./scripts/key_manager.sh backup`
3. Verify backup file created in `.secrets/backup/`
4. Delete current vault
5. Restore from backup
6. Verify all credentials accessible
**Expected Result**: Backup created successfully, restore preserves all data

### TC08: Error Handling
**Description**: Test error conditions and edge cases
**Steps**:
1. Attempt to get non-existent credential
2. Corrupt vault file
3. Remove permissions on .secrets directory
4. Test with invalid configuration
**Expected Result**: Graceful error handling, clear error messages

### TC09: Integration with OpenClaw
**Description**: Verify skill integrates with OpenClaw workflows
**Steps**:
1. Use credential reference in MEMORY.md
2. Create OpenClaw workflow that uses the credential
3. Verify workflow executes successfully
4. Check that no plaintext credentials appear in logs
**Expected Result**: Seamless integration, secure credential handling

### TC10: Security Audit
**Description**: Run skill-vetter security audit
**Steps**:
1. Install skill in clean environment
2. Run `skill-vetter` on the skill directory
3. Review audit report
4. Address any identified issues
**Expected Result**: Clean security audit, no red flags detected

## Test Data
- **Test Credentials**: 
  - `test_api_key`: "sk_test_123456789abcdef"
  - `test_password`: "SecureP@ssw0rd!2026"
  - `instreet_migration`: "sk_inst_65f59e5b26a662306c6e66b70c20d129"

## Success Criteria
- All test cases pass (TC01-TC10)
- No security vulnerabilities identified
- Performance acceptable for typical use cases
- Documentation accurate and complete
- Installation process smooth and intuitive

## Test Execution Log
*To be filled during test execution*