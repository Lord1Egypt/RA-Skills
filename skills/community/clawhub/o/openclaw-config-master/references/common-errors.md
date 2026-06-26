# 常见配置错误模式字典

本文档详细列出了 OpenClaw 配置系统中最常见的错误模式，帮助快速诊断和解决配置问题。

---

## 📋 目录

1. [Unknown key（未知键名）](#1-unknown-key未知键名)
2. [Type mismatch（类型不匹配）](#2-type-mismatch类型不匹配)
3. [Missing required field（缺少必需字段）](#3-missing-required-field缺少必需字段)
4. [Cross-field constraint failure（跨字段约束失败）](#4-cross-field-constraint-failure跨字段约束失败)
5. [Circular $include（循环引用）](#5-circular-include循环引用)
6. [Array concatenation surprise（数组拼接意外）](#6-array-concatenation-surprise数组拼接意外)
7. [Version mismatch（版本不一致）](#7-version-mismatch版本不一致)

---

## 1. Unknown key（未知键名）

### 🔍 错误类型识别

配置文件中使用了不被系统识别的键名。

### 📤 openclaw doctor 输出示例

```bash
$ openclaw doctor

🔍 Configuration Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: /path/to/config/base.yaml
Error: Unknown key 'environmet' in section 'server'

Valid keys for 'server':
  • environment
  • host
  • port
  • workers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Did you mean: 'environment'?
```

### 🎯 根本原因分析

**常见原因：**
1. **拼写错误** - 键名拼写不正确（如 `environmet` → `environment`）
2. **版本不匹配** - 使用了已废弃的键名或使用了新版本的键名
3. **配置迁移** - 从旧版本迁移时键名发生变化
4. **自定义扩展** - 使用了未注册的自定义键名

### ✅ 解决步骤

1. **验证拼写**
   ```bash
   # 使用 doctor 命令检查拼写建议
   openclaw doctor --check-spelling

   # 查看所有可用键
   openclaw schema list-keys
   ```

2. **检查版本兼容性**
   ```bash
   # 查看当前版本
   openclaw version

   # 检查配置文件版本要求
   openclaw schema version-check
   ```

3. **修正键名**
   ```yaml
   # 错误示例
   server:
     environmet: production
     host: 0.0.0.0

   # 正确示例
   server:
     environment: production
     host: 0.0.0.0
   ```

4. **验证修复**
   ```bash
   openclaw validate
   ```

### 🛡️ 预防措施

**开发阶段：**
```yaml
# 1. 使用 IDE 自动补全
# 安装 OpenClaw YAML Schema
# vscode: ext install openclaw.schema-support

# 2. 启用严格模式
openclaw init --strict-mode

# 3. 添加预提交钩子
#!/bin/bash
# .git/hooks/pre-commit
openclaw validate || exit 1
```

**CI/CD 集成：**
```yaml
# .github/workflows/config-check.yml
name: Config Validation
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Config
        run: |
          openclaw doctor
          openclaw validate --strict
```

---

## 2. Type mismatch（类型不匹配）

### 🔍 错误类型识别

配置值的类型与预期不符（如字符串代替数字、列表代替对象等）。

### 📤 openclaw doctor 输出示例

```bash
$ openclaw doctor

🔍 Configuration Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: /path/to/config/database.yaml
Path: database.postgresql.port
Error: Type mismatch

Expected: integer (port number)
Received: string "5432"

Schema definition:
  port:
    type: integer
    range: [1, 65535]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Quick fix: Remove quotes around the number
```

### 🎯 根本原因分析

**常见原因：**
1. **YAML 引号滥用** - 将数字或布尔值用引号包裹
2. **类型混淆** - 列表、对象、字符串混用
3. **环境变量注入** - 环境变量始终是字符串类型
4. **动态类型转换失败** - 表达式计算结果类型错误

### ✅ 解决步骤

1. **识别类型要求**
   ```bash
   # 查看字段类型定义
   openclaw schema inspect database.postgresql.port

   # 输出示例
   Type: integer
   Range: 1-65535
   Required: true
   Default: 5432
   ```

2. **修正类型错误**

   **场景 A：数字被引号包裹**
   ```yaml
   # 错误
   database:
     port: "5432"    # 字符串

   # 正确
   database:
     port: 5432      # 整数
   ```

   **场景 B：布尔值拼写错误**
   ```yaml
   # 错误
   debug: "true"     # 字符串
   debug: yes        # 不明确
   debug: on         # 不明确

   # 正确
   debug: true       # 布尔值
   debug: false
   ```

   **场景 C：列表 vs 对象**
   ```yaml
   # 错误：应该是对象但用了列表
   servers:
     - host: localhost
       port: 8080

   # 正确：对象格式
   servers:
     primary:
       host: localhost
       port: 8080
   ```

   **场景 D：环境变量类型转换**
   ```yaml
   # 错误：环境变量是字符串
   database:
     port: $DB_PORT  # 结果: "5432" (字符串)

   # 方案 1: 使用类型转换函数
   database:
     port: !int $DB_PORT

   # 方案 2: 使用环境文件
   # .env
   DB_PORT=5432
   ```

3. **验证修复**
   ```bash
   # 详细类型检查
   openclaw validate --type-check

   # 预览类型转换
   openclaw render --dry-run
   ```

### 🛡️ 预防措施

**配置模板：**
```yaml
# 使用模板明确类型
# templates/database.yaml.template
database:
  postgresql:
    host: !required string
    port: !required integer
    ssl: !required boolean
    pools:
      size: !optional integer
      timeout: !optional integer
```

**类型注解：**
```yaml
# 使用 YAML 注释标注类型
server:
  environment: string    # "development" | "production" | "staging"
  host: string           # hostname or IP
  port: integer          # 1-65535
  workers: integer       # >= 1
  debug: boolean         # true | false
  features: string[]     # array of feature names
```

**验证脚本：**
```python
#!/usr/bin/env python3
# scripts/validate-types.py
import yaml
import sys
from pathlib import Path

def validate_types(config_file):
    """验证配置文件类型"""
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # 类型检查逻辑
    checks = [
        (config.get('server', {}).get('port'), int, 'server.port'),
        (config.get('server', {}).get('debug'), bool, 'server.debug'),
        # ... 更多检查
    ]

    for value, expected_type, path in checks:
        if not isinstance(value, expected_type):
            print(f"❌ Type error at {path}: expected {expected_type.__name__}, got {type(value).__name__}")
            sys.exit(1)

    print("✅ All types are correct")

if __name__ == '__main__':
    validate_types(sys.argv[1])
```

---

## 3. Missing required field（缺少必需字段）

### 🔍 错误类型识别

配置文件中缺少系统运行所必需的字段。

### 📤 openclaw doctor 输出示例

```bash
$ openclaw doctor

🔍 Configuration Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: /path/to/config/app.yaml
Section: server
Error: Missing required fields

Required fields not found:
  • host (required)
  • port (required)

Optional fields found:
  • environment (optional)
  • workers (optional, has default)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Run 'openclaw scaffold server' to generate a template
```

### 🎯 根本原因分析

**常见原因：**
1. **配置不完整** - 手动创建配置时遗漏字段
2. **版本升级** - 新版本增加了必需字段
3. **条件分支** - 某些配置组合下才需要的字段
4. **模板误用** - 使用了不完整的模板

### ✅ 解决步骤

1. **识别缺失字段**
   ```bash
   # 查看必需字段列表
   openclaw schema required-fields server

   # 输出
   Required fields for 'server':
     - host (string, required)
     - port (integer, 1-65535, required)
     - environment (string, optional, default="development")
   ```

2. **补充缺失字段**
   ```yaml
   # 错误：缺少必需字段
   server:
     environment: production

   # 正确：包含所有必需字段
   server:
     host: 0.0.0.0        # 必需
     port: 8080           # 必需
     environment: production  # 可选，但有值
   ```

3. **使用脚手架生成**
   ```bash
   # 生成完整模板
   openclaw scaffold server --output config/server.yaml

   # 编辑模板
   nano config/server.yaml

   # 验证
   openclaw validate
   ```

4. **处理条件性必需字段**
   ```yaml
   # 某些字段在其他字段特定值时才必需
   database:
     type: postgresql  # 当此值为 postgresql 时
     postgresql:       # 此对象变为必需
       host: localhost
       port: 5432
     mysql:            # 此对象可选
       host: localhost
       port: 3306
   ```

### 🛡️ 预防措施

**完整配置模板：**
```yaml
# config/schema/full-config.template.yaml
# 完整配置模板（包含所有字段和注释）

server:
  # 必需字段
  host: !required
  port: !required

  # 可选字段（带默认值）
  environment: !optional "development"
  workers: !optional 4

  # 条件性字段
  ssl:
    enabled: false
    # 当 enabled: true 时，以下字段必需
    certificate: !conditional
    private_key: !conditional

database:
  type: !required "postgresql"

  # 根据 type 值选择配置
  postgresql: !when_type_postgresql
    host: !required
    port: !required
    database: !required

  mysql: !when_type_mysql
    host: !required
    port: !required
    database: !required
```

**自动化检查：**
```bash
#!/bin/bash
# scripts/check-required-fields.sh

# 检查所有配置文件
for config in config/*.yaml; do
    echo "Checking $config..."

    # 提取所有必需字段
    required_fields=$(openclaw schema required-fields --all)

    # 检查每个字段是否存在
    while read -r field; do
        if ! openclaw get "$field" --config "$config" >/dev/null 2>&1; then
            echo "❌ Missing required field: $field"
        fi
    done <<< "$required_fields"
done
```

**CI/CD 集成：**
```yaml
# .github/workflows/required-check.yml
name: Required Fields Check
on: [pull_request]

jobs:
  check-required:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install OpenClaw
        run: |
          curl -fsSL https://get.openclaw.dev | sh
      - name: Check Required Fields
        run: |
          openclaw doctor --check-required
          openclaw validate --strict
```

---

## 4. Cross-field constraint failure（跨字段约束失败）

### 🔍 错误类型识别

多个字段之间的约束关系不满足（如端口范围、URL 协议匹配等）。

### 📤 openclaw doctor 输出示例

```bash
$ openclaw doctor

🔍 Configuration Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: /path/to/config/ssl.yaml
Error: Cross-field constraint failure

Constraint: SSL port must be 443 when protocol is HTTPS
Violation:
  • server.protocol: "https"
  • server.port: 8443

Expected:
  • server.port should be 443
  • OR server.protocol should be "http"

Related constraints:
  • Port 443 requires protocol "https"
  • Port 80 requires protocol "http"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Use 'openclaw explain ssl-constraint' for details
```

### 🎯 根本原因分析

**常见原因：**
1. **逻辑冲突** - 两个或多个字段的值存在逻辑矛盾
2. **依赖关系** - 一个字段的值决定了另一个字段的合法范围
3. **互斥约束** - 某些字段不能同时出现或必须同时出现
4. **业务规则** - 配置违反了业务逻辑规则

### ✅ 解决步骤

1. **识别约束规则**
   ```bash
   # 查看跨字段约束
   openclaw schema constraints server

   # 输出
   Constraints for 'server':
     1. protocol=https ⟹ port=443
     2. protocol=http ⟹ port∈{80,8080}
     3. ssl.enabled=true ⟹ protocol=https
     4. workers > 0
   ```

2. **修复约束违反**

   **场景 A：协议与端口不匹配**
   ```yaml
   # 错误：HTTPS 协议但端口不是 443
   server:
     protocol: https
     port: 8443

   # 修复方案 1：修改端口
   server:
     protocol: https
     port: 443

   # 修复方案 2：使用自定义 HTTPS 端口（需要额外配置）
   server:
     protocol: https
     port: 8443
     custom_port: true
   ```

   **场景 B：SSL 配置冲突**
   ```yaml
   # 错误：SSL 启用但协议不是 HTTPS
   server:
     protocol: http
     ssl:
       enabled: true
       certificate: /path/to/cert.pem

   # 正确：SSL 启用时必须使用 HTTPS
   server:
     protocol: https
     ssl:
       enabled: true
       certificate: /path/to/cert.pem
   ```

   **场景 C：端口范围冲突**
   ```yaml
   # 错误：多个服务使用相同端口
   services:
     api:
       port: 8080
     web:
       port: 8080

   # 正确：使用不同端口
   services:
     api:
       port: 8080
     web:
       port: 8081
   ```

   **场景 D：环境特定约束**
   ```yaml
   # 错误：生产环境但 debug=true
   server:
     environment: production
     debug: true

   # 正确：生产环境必须关闭 debug
   server:
     environment: production
     debug: false
   ```

3. **验证修复**
   ```bash
   # 检查所有约束
   openclaw validate --constraints

   # 详细约束报告
   openclaw doctor --constraint-report
   ```

### 🛡️ 预防措施

**约束定义文件：**
```yaml
# config/constraints/schema-constraints.yaml
# 跨字段约束定义

constraints:
  - name: ssl-protocol-match
    description: "SSL enabled requires HTTPS protocol"
    condition:
      - field: server.ssl.enabled
        value: true
    requires:
      - field: server.protocol
        value: https
    error_message: "When SSL is enabled, protocol must be HTTPS"

  - name: https-default-port
    description: "HTTPS should use port 443 unless custom_port is set"
    condition:
      - field: server.protocol
        value: https
      - field: server.custom_port
        value: false
    requires:
      - field: server.port
        value: 443
    error_message: "HTTPS protocol requires port 443 (unless custom_port is true)"

  - name: production-no-debug
    description: "Production environment must not have debug enabled"
    condition:
      - field: server.environment
        value: production
    forbids:
      - field: server.debug
        value: true
    error_message: "Debug mode must be disabled in production"

  - name: unique-ports
    description: "All services must use unique ports"
    validator: python:validate_unique_ports
    error_message: "Multiple services cannot use the same port"
```

**自定义约束验证器：**
```python
# validators/constraints.py
from typing import Dict, Any

def validate_unique_ports(config: Dict[str, Any]) -> bool:
    """验证所有服务使用唯一端口"""
    ports = set()
    services = config.get('services', {})

    for service_name, service_config in services.items():
        port = service_config.get('port')
        if port in ports:
            raise ValueError(
                f"Port {port} is used by multiple services. "
                f"Duplicate found in {service_name}"
            )
        ports.add(port)

    return True

def validate_worker_count(config: Dict[str, Any]) -> bool:
    """验证 worker 数量不超过 CPU 核心数"""
    import os
    cpu_count = os.cpu_count()
    workers = config.get('server', {}).get('workers', 1)

    if workers > cpu_count:
        raise ValueError(
            f"Worker count ({workers}) exceeds CPU cores ({cpu_count})"
        )

    return True
```

**约束测试用例：**
```yaml
# tests/constraints/test-ssl-constraint.yaml
test_cases:
  - name: valid-https-443
    config:
      server:
        protocol: https
        port: 443
    expected: pass

  - name: invalid-https-not-443
    config:
      server:
        protocol: https
        port: 8443
    expected: fail
    error: "HTTPS protocol requires port 443"

  - name: valid-https-custom-port
    config:
      server:
        protocol: https
        port: 8443
        custom_port: true
    expected: pass
```

---

## 5. Circular $include（循环引用）

### 🔍 错误类型识别

配置文件之间形成循环引用，导致无法解析。

### 📤 openclaw doctor 输出示例

```bash
$ openclaw doctor

🔍 Configuration Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Error: Circular dependency detected in $include directives

Dependency chain:
  config/base.yaml
    → config/database.yaml
      → config/base.yaml  ⚠️ CIRCULAR

Break the cycle by:
  1. Removing one of the $include directives
  2. Refactoring shared config into a separate file
  3. Using !merge instead of $include

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Run 'openclaw graph --includes' to visualize dependencies
```

### 🎯 根本原因分析

**常见原因：**
1. **双向引用** - A 包含 B，B 又包含 A
2. **间接循环** - A → B → C → A
3. **公共配置依赖** - 多个文件相互依赖共享配置
4. **重构不当** - 重构时引入了循环引用

### ✅ 解决步骤

1. **可视化依赖关系**
   ```bash
   # 生成依赖图
   openclaw graph --includes > deps.dot
   dot -Tpng deps.dot -o deps.png

   # 查看依赖树
   openclaw tree --includes

   # 输出
   config/base.yaml
   ├── config/database.yaml
   │   └── config/base.yaml  ⚠️ CIRCULAR
   └── config/server.yaml
   ```

2. **识别循环引用**

   **场景 A：直接循环**
   ```yaml
   # config/base.yaml
   server:
     $include: config/server.yaml

   # config/server.yaml
     base:
       $include: config/base.yaml  # ❌ 循环
   ```

   **场景 B：间接循环**
   ```yaml
   # config/base.yaml
   database:
     $include: config/database.yaml

   # config/database.yaml
   backup:
     $include: config/backup.yaml

   # config/backup.yaml
   storage:
     $include: config/base.yaml  # ❌ 循环
   ```

3. **打破循环引用**

   **方案 1：提取共享配置**
   ```yaml
   # 创建新的共享配置文件
   # config/common/defaults.yaml

   # 修改原文件，只包含共享配置
   # config/base.yaml
   defaults:
     $include: config/common/defaults.yaml

   # config/database.yaml
   defaults:
     $include: config/common/defaults.yaml
   ```

   **方案 2：使用合并标签**
   ```yaml
   # config/base.yaml
   server:
     host: localhost
     port: 8080

   # config/server.yaml
   server:
     $merge:  # 合并而不是包含
       workers: 4
       environment: production
   ```

   **方案 3：使用变量**
   ```yaml
   # config/base.yaml
   defaults:
     database_port: 5432

   # config/database.yaml
   database:
     port: ${defaults.database_port}
   ```

4. **验证修复**
   ```bash
   # 检查依赖关系
   openclaw validate --check-circular

   # 生成新的依赖图
   openclaw graph --includes --no-circular > fixed-deps.dot
   ```

### 🛡️ 预防措施

**依赖关系规范：**
```yaml
# config/DEPENDENCIES.md
# 依赖关系规范文档

## 配置文件层次结构

```
config/
├── base.yaml          # 基础配置（不包含任何其他配置）
├── common/            # 公共配置（不包含任何其他配置）
│   ├── defaults.yaml
│   └── constants.yaml
├── services/          # 服务配置（只包含 common/）
│   ├── api.yaml
│   └── web.yaml
└── environments/      # 环境配置（只包含 common/ 和 services/）
    ├── development.yaml
    └── production.yaml
```

## 依赖规则

1. **基础层**：base.yaml, common/*.yaml - 不包含任何文件
2. **服务层**：services/*.yaml - 只包含 common/
3. **环境层**：environments/*.yaml - 只包含 common/ 和 services/
4. **禁止**：向下包含或同层相互包含
```

**自动化检查：**
```bash
#!/bin/bash
# scripts/check-circular-includes.sh

# 检查循环引用
openclaw validate --check-circular || {
    echo "❌ Circular dependency detected!"
    openclaw graph --includes > /tmp/cycle.dot
    echo "Dependency graph saved to /tmp/cycle.dot"
    exit 1
}

echo "✅ No circular dependencies found"
```

**预提交钩子：**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# 检查循环引用
echo "Checking for circular dependencies..."
if ! openclaw validate --check-circular; then
    echo "❌ Circular dependency detected. Please fix before committing."
    exit 1
fi

echo "✅ Dependency check passed"
```

---

## 6. Array concatenation surprise（数组拼接意外）

### 🔍 错误类型识别

`$include` 指令在处理数组时产生意外的拼接结果。

### 📤 openclaw doctor 输出示例

```bash
$ openclaw doctor

🔍 Configuration Warning
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File: /path/to/config/app.yaml
Warning: Unexpected array concatenation

Field: server.middleware
Issue: $include concatenates arrays by default

Current behavior:
  Base file defines: [logger, auth]
  $include adds: [logger, auth, cache]

Expected behavior:
  • Use !replace to replace the entire array
  • Use !merge to intelligently merge (deduplicate)
  • Or split into different array names

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Use 'openclaw explain array-strategies' for details
```

### 🎯 根本原因分析

**常见原因：**
1. **默认拼接行为** - `$include` 默认会拼接数组而不是替换
2. **重复元素** - 拼接导致数组中出现重复元素
3. **顺序依赖** - 拼接顺序影响执行逻辑
4. **意图不清** - 不清楚是替换还是拼接

### ✅ 解决步骤

1. **理解数组拼接行为**
   ```bash
   # 查看当前数组内容
   openclaw get server.middleware --trace

   # 输出
   server.middleware:
     - config/base.yaml: [logger, auth]
     - config/middleware.yaml: [cache, rate-limit]
     - Result (concatenated): [logger, auth, cache, rate-limit]
   ```

2. **选择正确的数组策略**

   **场景 A：完全替换**
   ```yaml
   # 错误：意外的拼接
   server:
     middleware:
       $include: config/middleware.yaml
   # 结果: [logger, auth, cache] (包含重复的 logger)

   # 正确：使用替换
   server:
     middleware:
       !replace: !include config/middleware.yaml
   # 结果: [cache] (完全替换)
   ```

   **场景 B：智能合并（去重）**
   ```yaml
   # 错误：重复元素
   server:
     middleware:
       $include: config/base.yaml    # [logger, auth]
       $include: config/custom.yaml  # [logger, cache]
   # 结果: [logger, auth, logger, cache] (重复)

   # 正确：使用合并
   server:
     middleware:
       !merge: !include config/base.yaml
       !merge: !include config/custom.yaml
   # 结果: [logger, auth, cache] (去重)
   ```

   **场景 C：顺序敏感**
   ```yaml
   # 错误：顺序错误
   server:
     middleware:
       - cache
       - auth
       - logger
   # 结果: 缓存中间件在认证之前执行（不安全）

   # 正确：调整顺序
   server:
     middleware:
       - logger    # 先记录
       - auth      # 再认证
       - cache     # 最后缓存
   ```

   **场景 D：条件性包含**
   ```yaml
   # 根据环境包含不同的中间件
   server:
     middleware:
       $include: config/middleware/common.yaml
       $include: config/middleware/${environment}.yaml
   # development: [logger, debug-panel]
   # production: [logger, compression, rate-limit]
   ```

3. **验证数组内容**
   ```bash
   # 查看最终数组
   openclaw get server.middleware --json | jq .

   # 检查重复
   openclaw get server.middleware --check-duplicates

   # 验证顺序
   openclaw validate --middleware-order
   ```

### 🛡️ 预防措施

**数组策略定义：**
```yaml
# config/strategies/arrays.yaml
# 数组处理策略文档

strategies:
  - name: replace
    description: "完全替换数组（不去重）"
    use_when: "需要完全替换现有内容"
    example: |
      array:
        !replace: !include config/new-array.yaml

  - name: merge
    description: "智能合并（去重）"
    use_when: "需要组合多个数组但避免重复"
    example: |
      array:
        !merge: !include config/first.yaml
        !merge: !include config/second.yaml

  - name: concatenate
    description: "简单拼接（允许重复）"
    use_when: "需要保留重复项或顺序很重要"
    example: |
      array:
        $include: config/first.yaml
        $include: config/second.yaml

  - name: prepend
    description: "在数组开头添加"
    use_when: "新元素需要优先执行"
    example: |
      array:
        !prepend: [new-item]
        $include: config/rest.yaml

  - name: append
    description: "在数组末尾添加"
    use_when: "新元素需要最后执行"
    example: |
      array:
        $include: config/base.yaml
        !append: [new-item]
```

**命名规范：**
```yaml
# 使用明确的命名区分不同的数组
server:
  # 基础中间件（始终启用）
  middleware_core:
    - logger
    - error-handler

  # 环境特定中间件
  middleware_env:
    $include: config/middleware/${environment}.yaml

  # 最终组合
  middleware:
    !merge: !ref server.middleware_core
    !merge: !ref server.middleware_env
```

**验证脚本：**
```python
#!/usr/bin/env python3
# scripts/validate-arrays.py

import yaml
import sys
from collections import Counter

def validate_arrays(config_file):
    """验证数组配置"""
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # 检查中间件顺序
    middleware = config.get('server', {}).get('middleware', [])

    # 检查重复
    counter = Counter(middleware)
    duplicates = [item for item, count in counter.items() if count > 1]

    if duplicates:
        print(f"❌ Duplicate middleware found: {duplicates}")
        return False

    # 检查顺序
    if 'auth' in middleware and 'cache' in middleware:
        auth_idx = middleware.index('auth')
        cache_idx = middleware.index('cache')

        if cache_idx < auth_idx:
            print("❌ Cache middleware must come after auth middleware")
            return False

    print("✅ Array validation passed")
    return True

if __name__ == '__main__':
    validate_arrays(sys.argv[1])
```

---

## 7. Version mismatch（版本不一致）

### 错误类型识别

OpenClaw 本地版本与最新版本不一致，或配置使用了当前版本不支持的字段。

### openclaw doctor 输出示例

```bash
$ openclaw doctor

Configuration Error
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Warning: Config uses fields not available in current version

Current version: 2026.3.28
Field 'acp.stream.coalesceIdleMs' requires version >= 2026.4.0

Suggestion: Update openclaw to use this field
  openclaw update

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run 'openclaw update status --json' for version details
```

### 根本原因分析

**常见原因：**
1. **本地版本落后** — 未及时更新 openclaw，配置文件引用了新版本才有的字段
2. **配置文件迁移** — 从新版本环境复制配置到旧版本环境
3. **技能版本不匹配** — 技能文档引用了新版本字段，但本地 openclaw 版本较旧
4. **破坏性变更** — 版本升级后某些字段被废弃或重命名

### 解决步骤

1. **检查当前版本**
   ```bash
   # 检查本地版本
   openclaw --version

   # 检查最新版本和更新状态
   openclaw update status --json
   # 关键字段: availability.latestVersion, availability.hasRegistryUpdate
   ```

2. **更新到最新版本**
   ```bash
   # 预览更新（不实际执行）
   openclaw update --dry-run

   # 执行更新
   openclaw update

   # 非交互式更新
   openclaw update --yes
   ```

3. **更新技能**
   ```bash
   # 确保配置技能是最新版
   openclaw skills update openclaw-config-master

   # 更新所有技能
   openclaw skills update
   ```

4. **查阅最新文档**
   ```bash
   # 内置文档搜索
   openclaw docs "configuration"

   # 查看完整配置参考
   openclaw config schema

   # 在线文档
   # https://docs.openclaw.ai/gateway/configuration-reference
   ```

5. **验证版本一致**
   ```bash
   openclaw --version
   openclaw doctor
   ```

### 预防措施

**版本检查脚本（可加入 cron 或 CI）：**
```bash
#!/bin/bash
# check-version.sh — 版本一致性检查

CURRENT=$(openclaw --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
LATEST=$(openclaw update status --json | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('availability', {}).get('latestVersion', 'unknown'))
")

if [ "$CURRENT" != "$LATEST" ]; then
    echo "版本不一致: 当前=$CURRENT, 最新=$LATEST"
    echo "请运行: openclaw update"
    exit 1
else
    echo "版本一致: $CURRENT"
fi
```

**版本相关的配置错误速查**：

| 错误现象 | 版本原因 | 解决方法 |
|---------|---------|---------|
| `Unknown key 'acp'` | 本地版本 < 2026.3.28 | 更新 openclaw |
| `Unknown key 'stream' in acp` | 本地版本 < 2026.4.0 | 更新 openclaw |
| `tools.web.enabled not found` | 旧版字段，2026.3.x 已重构 | 改用 `tools.web.search.enabled` |
| `bindings is not an array` | 旧版格式（对象），新版要求数组 | 参考 `version-migration.md` |
| `commands.bash should be boolean` | 类型错误（字符串 `"true"`） | 改为布尔值 `true` |

---

## 🔧 快速参考

### 常用诊断命令

```bash
# 版本检查
openclaw --version
openclaw update status --json

# 全面检查
openclaw doctor

# 验证配置
openclaw config validate

# 配置文件路径
openclaw config file

# 查看 Schema
openclaw config schema

# 安全审计
openclaw security audit

# 网关状态
openclaw gateway status

# 查看必需字段
openclaw config schema

# 技能版本
openclaw skills list
```

### 错误模式速查表

| 错误类型 | 快速诊断命令 | 常见解决方案 |
|---------|-------------|-------------|
| Version mismatch | `openclaw --version && openclaw update status --json` | 更新 openclaw：`openclaw update` |
| Unknown key | `openclaw doctor` | 检查拼写、使用 `openclaw config schema` |
| Type mismatch | `openclaw doctor` | 移除引号、使用正确类型 |
| Missing required field | `openclaw doctor` | 补充必需字段 |
| Cross-field constraint | `openclaw doctor` | 查看约束定义、调整字段值 |
| Circular $include | `openclaw doctor` | 提取共享配置、重构依赖 |
| Array concatenation | `openclaw doctor` | 理解 $include 的数组拼接行为 |

---

## 📚 相关资源

- [配置验证完整指南](/mnt/c/Users/aqbjq/Downloads/2/openclaw-config/guides/validation.md)
- [配置模式参考](/mnt/c/Users/aqbjq/Downloads/2/openclaw-config/references/schemas.md)
- [诊断工具使用手册](/mnt/c/Users/aqbjq/Downloads/2/openclaw-config/guides/diagnostics.md)
- [最佳实践指南](/mnt/c/Users/aqbjq/Downloads/2/openclaw-config/guides/best-practices.md)

---

## 🤝 贡献

发现新的错误模式？欢迎提交 PR 扩展此文档！

---

**文档版本**：1.0.0
**最后更新**：2026-03-27
**维护者**：OpenClaw 配置团队
