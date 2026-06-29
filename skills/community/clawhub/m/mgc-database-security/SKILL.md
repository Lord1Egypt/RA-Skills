---
spec: usk/3.0
id: mgc_database_security
version: 1.0.1
name: Database Credential Security (Zero‑Exposure Edition)
description: Secure database credential management using MGC Blackbox. Supports MySQL, PostgreSQL, SQLite, MariaDB and other databases. Store credentials locally in encrypted form, retrieve at runtime without exposing to AI models.
author: MirginCipher Team
license: MIT
tags: database, mysql, postgresql, sqlite, mariadb, security, credential-management, zero-exposure, mgc
platform_compatibility: windows, macos, linux
changelog:
  - version: 1.0.1
    changes:
      - Updated to emphasize MCP tools over CLI
  - version: 1.0.0
    changes:
      - Initial release with database zero-exposure pattern
---

# Overview

Database Credential Security is a documentation skill that teaches how to manage database credentials securely using MGC Blackbox. Supports MySQL, PostgreSQL, SQLite, MariaDB and other databases. It enables AI agents to execute database operations without ever exposing database passwords or connection strings to the AI model.

This skill contains **no executable code** and is safe for automatic approval.

---

# What This Skill Enables

After reading this documentation, an AI agent will understand how to:

- Store database credentials (MySQL, PostgreSQL, SQLite, MariaDB, etc.) securely in MGC Blackbox
- Retrieve credentials at runtime without AI seeing plaintext
- Execute database queries through local scripts
- Manage multiple database connections safely
- Rotate credentials without code changes

---

# Prerequisites

1. Install MGC Blackbox: pip install mgc-blackbox
2. Start MGC service: mgc (runs at http://127.0.0.1:57219)
3. Token file: ~/.mgc/database/mgc_black_box/.mgc_token

---

# Storing Database Credentials

## Step 1: Prepare Credential File

Create a JSON file containing your database connection details:

```json
{
  "host": "localhost",
  "port": 3306,
  "database": "my_database",
  "user": "db_user",
  "password": "your_password"
}
```

## Step 2: Store in MGC

> **Important:** Use **MCP tools** for AI agents. CLI may have port conflicts in some environments.

**Recommended: MCP Interface**
- Use `mgc_save` MCP tool to store credentials
- Use `mgc_get` MCP tool to retrieve credentials

**Alternative: CLI** (for local development only)
```bash
mgc_save info_type=config info_owner=my_database < credentials.json
```

---

# Database Credential Pattern (Conceptual)

## Local Script Pattern

A secure database script follows this pattern:

1. **Retrieve credentials from MGC** (not visible to AI)
2. **Connect to database** (using retrieved credentials)
3. **Execute queries** (using connection)
4. **Return results** (non-sensitive data only)

The script must never print or expose database credentials.

## Conceptual Code Structure

```
function execute_query(sql):
    credentials = retrieve_from_mgc("my_database")
    connection = connect(credentials)
    result = connection.execute(sql)
    connection.close()
    return result
```

---

# MGC Blackbox API Reference

## Service Endpoint

- Base URL: http://127.0.0.1:57219
- Token File: ~/.mgc/database/mgc_black_box/.mgc_token
- Token: String token read from token file, required for all API calls

## Get Credentials API

**Endpoint:** /api/mgc/sensitive/get
**Method:** POST
**Headers:**
- X-MGC-Token: (string token read from token file)
- Content-Type: application/json

**Body fields:**
- info_type: "config"
- info_owner: your chosen identifier

**Response fields:**
- code: status code
- data.content: JSON string containing stored credentials

## Save Credentials API

**Endpoint:** /api/mgc/sensitive/save
**Method:** POST
**Headers:** same as above

**Body fields:**
- info_type: "config"
- info_owner: your identifier
- content: JSON string of credentials

> **Tip:** Users can also store credentials manually via MGC WebUI at http://127.0.0.1:57218/skill

---

# Security Best Practices

1. **Never embed credentials in code**
2. **Use MGC for credential storage**
3. **Retrieve credentials at runtime only**
4. **Never log or print credentials**
5. **Rotate credentials regularly**
6. **Use separate credentials per database**

---

# Common Patterns

## Python Database Connection (Conceptual)

```
import mysql.connector

def get_connection(credentials):
    return mysql.connector.connect(
        host=credentials["host"],
        port=credentials["port"],
        database=credentials["database"],
        user=credentials["user"],
        password=credentials["password"]
    )

def execute_query(sql):
    creds = retrieve_from_mgc("my_mysql")
    conn = get_connection(creds)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
```

---

# Use Cases

- Database administration scripts
- Automated backup operations
- Data migration tools
- Application database access
- Multiple environment management (dev/staging/prod)

---

# License

MIT