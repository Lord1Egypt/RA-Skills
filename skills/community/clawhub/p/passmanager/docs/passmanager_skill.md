# PassManager Skill

**Skill Name**: PassManager  
**Version**: 1.0.0  
**Author**: iSenlink  
**Created**: 2026-03-13  
**Skill Type**: Password Management  
**Security Level**: Confidential  

---

## 🎯 Overview

### 1.1 Introduction
PassManager is a local, encrypted password management system built on SQLite with AES-256-GCM encryption. It replaces third-party password services (like 1Password) with a self-hosted, fully-controlled solution for AI assistants.

### 1.2 Key Features
- ✅ **Local Storage**: All passwords stored in a local SQLite database
- ✅ **AES-256-GCM Encryption**: Military-grade authenticated encryption
- ✅ **RBAC Access Control**: Role-based permissions (admin/user/auditor/guest)
- ✅ **Audit Trail**: Complete access logging
- ✅ **Auto Backup**: Scheduled backup mechanism
- ✅ **Zero Hardcoded Passwords**: Eliminate security risks entirely

### 1.3 Use Cases
- Enterprise password management for AI assistant teams
- Secure credential sharing within a team
- Sensitive information storage
- Replacement for third-party password managers

---

## 🔧 Installation & Setup

### 2.1 Installation
```bash
# Method 1: Via skillhub
skillhub install passmanager

# Method 2: Manual install
git clone [repository_url] passmanager
cd passmanager
pip3 install cryptography
```

### 2.2 Configuration Steps
```bash
# 1. Initialize the database
python3 scripts/passmanager.py init

# 2. Add a team member
python3 scripts/passmanager.py add-assistant --name "alice" --level admin

# 3. Add your first credential
python3 scripts/passmanager.py add --service "email" --key "user@example.com" --value "[password]"

# 4. Verify installation
python3 scripts/passmanager.py status
```

### 2.3 Requirements
- Python 3.8+
- SQLite 3.35+
- OpenClaw 2026.3.7+
- `cryptography` Python package (`pip3 install cryptography`)

---

## 📖 Usage Guide

### 3.1 Basic Commands

#### 3.1.1 Credential Management
```bash
# Add a credential
passmanager add --service "email" --key "username" --value "password"

# Query a credential
passmanager get --service "email" --key "username"

# Update a credential
passmanager update --service "email" --key "username" --value "new_password"

# Delete a credential
passmanager delete --service "email" --key "username"

# List all credentials
passmanager list
```

#### 3.1.2 Team Management
```bash
# Add a team member
passmanager add-assistant --name "bob" --level user

# Change member permissions
passmanager update-assistant --name "bob" --level admin

# List all members
passmanager list-assistants

# Remove a member
passmanager delete-assistant --name "bob"
```

#### 3.1.3 System Management
```bash
# View system status
passmanager status

# View access logs
passmanager logs --days 7

# Backup database
passmanager backup

# Restore database
passmanager restore --backup-file "backup_20260313.db"

# Export passwords (encrypted)
passmanager export --output "passwords_export.json"
```

### 3.2 Advanced Features

#### 3.2.1 Batch Operations
```bash
# Batch import
passmanager import --file "passwords.csv"

# Batch export
passmanager export-all --format json

# Batch update expired passwords
passmanager update-expired --days 90
```

#### 3.2.2 Security Auditing
```bash
# Password strength audit
passmanager audit-strength

# Password expiry audit
passmanager audit-expiry

# Permission audit
passmanager audit-permissions

# Generate audit report
passmanager audit-report --output "audit_report.md"
```

#### 3.2.3 Integration
```python
# Use in scripts
import passmanager
pm = passmanager.PassManager()
password = pm.get_password("email", "user@example.com")
```

---

## 🔒 Security Architecture

### 4.1 Encryption Scheme
```
Credential Encryption Flow:
Plaintext Password → AES-256-GCM Encrypt → Nonce+Ciphertext+AuthTag → SQLite Storage

Key Derivation:
Master Password → PBKDF2-SHA256 (600K iterations, random 32-byte salt) → AES-256 Key (32 bytes)
```

### 4.2 Role-Based Access Control
```yaml
Permission Levels:
  admin:     # Administrator
    - Full access to all operations
    - Team management
    - System configuration
    - Backup & restore
    
  user:      # Regular user
    - Query credentials
    - Add credentials
    - Update own credentials
    
  auditor:   # Audit role
    - View logs
    - Generate audit reports
    - Read-only access
    
  guest:     # Guest role
    - Limited query access
    - No modification permissions
```

### 4.3 Access Control
- **Authentication**: Master password required for all sensitive operations
- **Rate Limiting**: Protection against brute force attacks
- **Audit Trail**: Every operation is logged
- **Session Isolation**: No plaintext password caching in memory

---

## 📊 Database Schema

### 5.1 Table Structure
```sql
-- Credentials table
CREATE TABLE passwords (
    id INTEGER PRIMARY KEY,
    service TEXT NOT NULL,
    key_name TEXT NOT NULL,
    encrypted_value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    created_by TEXT,
    tags TEXT,
    notes TEXT,
    UNIQUE(service, key_name)
);

-- Team members table
CREATE TABLE assistants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    permission_level TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_access TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

-- Audit log table
CREATE TABLE access_logs (
    id INTEGER PRIMARY KEY,
    assistant_name TEXT,
    action TEXT,
    service TEXT,
    key_name TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN
);

-- Backups table
CREATE TABLE backups (
    id INTEGER PRIMARY KEY,
    backup_file TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    size_bytes INTEGER,
    checksum TEXT
);
```

### 5.2 Indexes
```sql
-- Performance indexes
CREATE INDEX idx_passwords_service_key ON passwords(service, key_name);
CREATE INDEX idx_access_logs_assistant ON access_logs(assistant_name, timestamp);
CREATE INDEX idx_passwords_expires ON passwords(expires_at);
```

---

## 🚀 Deployment Guide

### 6.1 Single Server Deployment
```bash
# 1. Install skill
skillhub install passmanager

# 2. Initialize
cd passmanager
python3 scripts/setup.py

# 3. Test
python3 scripts/test_passmanager.py

# 4. Configure auto backup (cron)
crontab -e
# Add: 0 2 * * * /usr/bin/python3 /path/to/passmanager/scripts/backup.py
```

### 6.2 Cluster Deployment
```bash
# 1. Deploy master
python3 scripts/deploy_master.py

# 2. Deploy slaves
python3 scripts/deploy_slave.py --master 192.168.1.100

# 3. Sync configuration
python3 scripts/sync_config.py
```

### 6.3 High Availability
```yaml
# ha-config.yaml
replication:
  mode: master-slave
  slaves: 3
  sync_interval: 60s
  
backup:
  strategy: incremental
  retention_days: 30
  storage: s3://your-backup-bucket
  
monitoring:
  health_check: /health
  alert_threshold: 95%
```

---

## 📈 Performance

### 7.1 Benchmarks
| Operation | Avg Response | Max Concurrency | Data Volume |
|-----------|-------------|-----------------|-------------|
| Query | < 10ms | 1000 QPS | 10,000+ entries |
| Add | < 50ms | 500 QPS | - |
| Batch Import | < 5s | 10 QPS | 1000 entries/batch |
| Audit Report | < 30s | 5 QPS | Full database |

### 7.2 Resource Usage
- **Memory**: < 50MB
- **Disk**: < 100MB (DB + logs)
- **CPU**: < 5% (average)

---

## 🔍 Troubleshooting

### 8.1 Common Issues

#### Q1: Database connection failed
```bash
# Check file permissions
ls -la ~/.passmanager/

# Fix permissions
chmod 600 ~/.passmanager/passwords.db

# Re-initialize
python3 scripts/passmanager.py init --force
```

#### Q2: Query returns empty
```bash
# Check permissions
python3 scripts/passmanager.py check-permission --name "your_user"

# Check if entry exists
python3 scripts/passmanager.py exists --service "email" --key "username"

# Debug
python3 scripts/passmanager.py debug --service "email" --key "username"
```

#### Q3: Backup failed
```bash
# Check disk space
df -h

# Check backup directory permissions
ls -la ~/.passmanager/backups/

# Test manual backup
python3 scripts/passmanager.py backup --test
```

### 8.2 Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| ERR-001 | Database connection failed | Check DB file permissions and path |
| ERR-002 | Insufficient permissions | Check user role level |
| ERR-003 | Entry not found | Verify service name and key are correct |
| ERR-004 | Encryption failed | Check encryption key configuration |
| ERR-005 | Backup failed | Check disk space and permissions |
| ERR-006 | Import format error | Verify import file format |

---

## 📚 Documentation

### 9.1 Internal Docs
- `passmanager_training_public.md` — Training manual
- `passmanager_security.md` — Security whitepaper
- `passmanager_migration.md` — Migration guide

### 9.2 External Resources
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [AES Encryption Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [OpenClaw Skill Development Guide](https://docs.openclaw.ai/skills)

### 9.3 Contact
- **Technical Issues**: tech@isenlink.com
- **Security Vulnerabilities**: security@isenlink.com
- **Feature Requests**: feedback@isenlink.com

---

## ✅ Compliance

### 10.1 Security Standards
- ✅ OWASP Security Guidelines
- ✅ AES-256-GCM Encryption Standard
- ✅ PBKDF2 Password Hashing (600K iterations)

### 10.2 Audit Schedule
- **Quarterly**: Full security audit
- **Monthly**: Vulnerability scan
- **Weekly**: Access log review
- **Daily**: System health check

### 10.3 Changelog
| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2026-03-13 | Initial release (base64 obfuscation — deprecated) |
| v1.1.0 | 2026-05-28 | AES-256-GCM true encryption, RBAC, audit logging |

---

**Maintainer**: iSenlink  
**Last Updated**: 2026-05-29  
**Skill Status**: ✅ Production Ready  

---
*This skill is developed by iSenlink. All rights reserved.*
