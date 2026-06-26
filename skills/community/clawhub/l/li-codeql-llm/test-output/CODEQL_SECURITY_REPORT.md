# CodeQL 安全扫描报告

**扫描时间**: 2026-03-19 07:03:41
**总漏洞数**: 38

## 📊 漏洞统计

| 漏洞类型 | 数量 | 严重程度 |
|----------|------|----------|
| py/stack-trace-exposure | 14 | ⚪ 提示 |
| py/sql-injection | 5 | ⚪ 提示 |
| py/weak-sensitive-data-hashing | 4 | ⚪ 提示 |
| py/code-injection | 3 | ⚪ 提示 |
| py/unsafe-deserialization | 3 | ⚪ 提示 |
| py/full-ssrf | 2 | ⚪ 提示 |
| py/flask-debug | 2 | ⚪ 提示 |
| py/command-line-injection | 2 | ⚪ 提示 |
| py/weak-cryptographic-algorithm | 1 | ⚪ 提示 |
| py/path-injection | 1 | ⚪ 提示 |
| py/clear-text-logging-sensitive-data | 1 | ⚪ 提示 |

## 🔍 详细发现

### ⚪ 提示 py/stack-trace-exposure

**发现数量**: 14

**1. 位置**: `unknown:51`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**2. 位置**: `unknown:89`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**3. 位置**: `unknown:110`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**4. 位置**: `unknown:133`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**5. 位置**: `unknown:158`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**6. 位置**: `unknown:182`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**7. 位置**: `unknown:205`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**8. 位置**: `unknown:88`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**9. 位置**: `unknown:160`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**10. 位置**: `unknown:239`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**11. 位置**: `unknown:51`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**12. 位置**: `unknown:145`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**13. 位置**: `unknown:167`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....

**14. 位置**: `unknown:188`
**描述**: [Stack trace information](1) flows to this location and may be exposed to an external user....


---

### ⚪ 提示 py/sql-injection

**发现数量**: 5

**1. 位置**: `unknown:37`
**描述**: This SQL query depends on a [user-provided value](1)....

**2. 位置**: `unknown:64`
**描述**: This SQL query depends on a [user-provided value](1)....

**3. 位置**: `unknown:108`
**描述**: This SQL query depends on a [user-provided value](1)....

**4. 位置**: `unknown:232`
**描述**: This SQL query depends on a [user-provided value](1)....

**5. 位置**: `unknown:44`
**描述**: This SQL query depends on a [user-provided value](1)....


---

### ⚪ 提示 py/weak-sensitive-data-hashing

**发现数量**: 4

**1. 位置**: `unknown:28`
**描述**: [Sensitive data (password)](1) is used in a hashing algorithm (MD5) that is insecure for password ha...

**2. 位置**: `unknown:36`
**描述**: [Sensitive data (password)](1) is used in a hashing algorithm (SHA1) that is insecure for password h...

**3. 位置**: `unknown:101`
**描述**: [Sensitive data (password)](1) is used in a hashing algorithm (SHA256) that is insecure for password...

**4. 位置**: `unknown:176`
**描述**: [Sensitive data (password)](1) is used in a hashing algorithm (SHA256) that is insecure for password...


---

### ⚪ 提示 py/code-injection

**发现数量**: 3

**1. 位置**: `unknown:197`
**描述**: This code execution depends on a [user-provided value](1)....

**2. 位置**: `unknown:138`
**描述**: This code execution depends on a [user-provided value](1)....

**3. 位置**: `unknown:160`
**描述**: This code execution depends on a [user-provided value](1)....


---

### ⚪ 提示 py/unsafe-deserialization

**发现数量**: 3

**1. 位置**: `unknown:43`
**描述**: Unsafe deserialization depends on a [user-provided value](1)....

**2. 位置**: `unknown:81`
**描述**: Unsafe deserialization depends on a [user-provided value](1)....

**3. 位置**: `unknown:125`
**描述**: Unsafe deserialization depends on a [user-provided value](1)....


---

### ⚪ 提示 py/full-ssrf

**发现数量**: 2

**1. 位置**: `unknown:149`
**描述**: The full URL of this request depends on a [user-provided value](1)....

**2. 位置**: `unknown:173`
**描述**: The full URL of this request depends on a [user-provided value](1)....


---

### ⚪ 提示 py/flask-debug

**发现数量**: 2

**1. 位置**: `unknown:139`
**描述**: A Flask app appears to be run in debug mode. This may allow an attacker to run arbitrary code throug...

**2. 位置**: `unknown:171`
**描述**: A Flask app appears to be run in debug mode. This may allow an attacker to run arbitrary code throug...


---

### ⚪ 提示 py/command-line-injection

**发现数量**: 2

**1. 位置**: `unknown:88`
**描述**: This command line depends on a [user-provided value](1)....

**2. 位置**: `unknown:182`
**描述**: This command line depends on a [user-provided value](1)....


---

### ⚪ 提示 py/weak-cryptographic-algorithm

**发现数量**: 1

**1. 位置**: `unknown:56`
**描述**: [The block mode ECB](1) is broken or weak, and should not be used.
[The cryptographic algorithm DES]...


---

### ⚪ 提示 py/path-injection

**发现数量**: 1

**1. 位置**: `unknown:154`
**描述**: This path depends on a [user-provided value](1)....


---

### ⚪ 提示 py/clear-text-logging-sensitive-data

**发现数量**: 1

**1. 位置**: `unknown:209`
**描述**: This expression logs [sensitive data (password)](1) as clear text....


---

