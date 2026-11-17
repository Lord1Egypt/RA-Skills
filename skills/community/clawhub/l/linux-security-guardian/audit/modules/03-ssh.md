# Module 03 — SSH Configuration

## Commands
```bash
sshd -T 2>/dev/null          # full effective SSH config (best method)
cat /etc/ssh/sshd_config     # raw config file
grep -v "^#\|^$" /etc/ssh/sshd_config
```

## Checks — 20+ SSH Security Parameters

| Parameter | Secure Value | Finding if Wrong |
|---|---|---|
| PermitRootLogin | no | HIGH → confirm to set no |
| PasswordAuthentication | no | HIGH → confirm to set no |
| PubkeyAuthentication | yes | HIGH |
| PermitEmptyPasswords | no | CRITICAL → auto-fix |
| X11Forwarding | no | MEDIUM |
| MaxAuthTries | ≤ 4 | MEDIUM |
| LoginGraceTime | ≤ 60 | LOW |
| AllowAgentForwarding | no | LOW |
| AllowTcpForwarding | no | MEDIUM |
| ClientAliveInterval | 300 | LOW |
| ClientAliveCountMax | 2 | LOW |
| Protocol | 2 (implicit modern) | CRITICAL if 1 |
| Port | not 22 | INFO (advisory) |
| UsePAM | yes | MEDIUM if no |
| IgnoreRhosts | yes | HIGH if no |
| HostbasedAuthentication | no | HIGH |
| PermitUserEnvironment | no | MEDIUM |
| StrictModes | yes | HIGH if no |
| MaxSessions | ≤ 4 | LOW |
| Banner | set | INFO |
| LogLevel | VERBOSE or INFO | MEDIUM if silent |
| AllowUsers/AllowGroups | set | INFO (advisory) |

## Auto-Fix Eligible (from whitelist only)
- PermitEmptyPasswords no → AUTO-FIX (sed in place)

## Confirm Required
- PermitRootLogin no → confirm (could lock out if no key auth)
- PasswordAuthentication no → confirm (MUST have key auth working first)
- All others → queue confirm

## Checks — SSH Ciphers, MACs, and Key Exchange Algorithms (CIS)

### Commands
```bash
# Check configured ciphers
sshd -T 2>/dev/null | grep -i ciphers

# Check configured MACs
sshd -T 2>/dev/null | grep -i macs

# Check configured KexAlgorithms
sshd -T 2>/dev/null | grep -i kexalgorithms

# Check for weak ciphers in current config
grep -i ciphers /etc/ssh/sshd_config 2>/dev/null
```

### Weak Ciphers (CBC mode — vulnerable to padding oracle attacks)
| Cipher | Status | Severity |
|--------|--------|----------|
| 3des-cbc | WEAK | HIGH |
| aes128-cbc | WEAK | MEDIUM |
| aes192-cbc | WEAK | MEDIUM |
| aes256-cbc | WEAK | MEDIUM |
| blowfish-cbc | WEAK | HIGH |
| cast128-cbc | WEAK | MEDIUM |
| arcfour/arcfour128/arcfour256 | WEAK (RC4) | CRITICAL |
| rijndael-cbc@lysator.liu.se | WEAK | MEDIUM |

### Weak MACs (vulnerable to hash collision)
| MAC | Status | Severity |
|-----|--------|----------|
| hmac-md5 | WEAK | HIGH |
| hmac-md5-96 | WEAK | HIGH |
| hmac-ripemd160 | WEAK | MEDIUM |
| hmac-sha1 | WEAK | MEDIUM |
| hmac-sha1-96 | WEAK | MEDIUM |
| umac-64@openssh.com | WEAK | MEDIUM |
| hmac-sha2-256-96 | WEAK | MEDIUM |
| hmac-sha2-512-96 | WEAK | MEDIUM |

### Weak Kex Algorithms (vulnerable to man-in-the-middle)
| Algorithm | Status | Severity |
|-----------|--------|----------|
| diffie-hellman-group1-sha1 | WEAK | HIGH |
| diffie-hellman-group14-sha1 | WEAK | MEDIUM |
| diffie-hellman-group-exchange-sha1 | WEAK | HIGH |
| diffie-hellman-group-exchange-sha256 (small moduli) | WEAK | MEDIUM |
| ecdh-sha2-nistp256/384/521 | WEAK (NIST curves) | LOW |
| curve25519-sha256 | STRONG | PASS |
| curve25519-sha256@libssh.org | STRONG | PASS |
| diffie-hellman-group16-sha512 | STRONG | PASS |
| diffie-hellman-group18-sha512 | STRONG | PASS |
| sntrup761x25519-sha512@openssh.com | STRONG (post-quantum) | PASS |

### Recommended Secure Config
```
# /etc/ssh/sshd_config.d/99-hardening.conf
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
```

### Auto-Fix Eligible
- Weak ciphers/MACs/Kex detected → write hardening config to /etc/ssh/sshd_config.d/99-hardening.conf (confirm required — could break legacy clients)

### Output Format (Ciphers/MACs/Kex)
```
[HIGH] 03-ssh: weak_cipher | cipher: 3des-cbc | in use: yes | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 03-ssh: weak_mac | mac: hmac-sha1 | in use: yes | action_id: ACT-YYYYMMDD-XXX
[PASS] 03-ssh: kex_algorithm | kex: curve25519-sha256 | strong ✓
```

## Output Format
```
[HIGH] 03-ssh: PermitRootLogin | value: yes | expected: no | action_id: ACT-YYYYMMDD-001
[PASS] 03-ssh: MaxAuthTries | value: 3 ≤ 4
```
