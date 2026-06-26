# 安全框架部署指南

**版本**: 1.0.2
**日期**: 2026-03-19

---

## 目录

1. [环境准备](#环境准备)
2. [安装 Python 依赖](#安装-python-依赖)
3. [部署安全模块](#部署安全模块)
4. [配置审计日志](#配置审计日志)
5. [集成到技能脚本](#集成到技能脚本)
6. [验证部署](#验证部署)
7. [故障排除](#故障排除)

---

## 环境准备

### 1.1 系统要求

- **操作系统**: Windows 10+/Server 2019+ (或 Linux/macOS)
- **Python**: 3.9+ (已安装 3.11.9 ✅)
- **权限**: 标准用户权限即可（无需 Administrator/root）。只需对 `SKILLs/` 目录有读写权限。

### 1.2 检查现有安装

```bash
# 检查 Python
python --version  # 应 >= 3.9

# 检查 SKILLs 根目录
echo $SKILLS_ROOT
# 或
find /c/Users/Administrator -type d -name "SKILLs" | head -2
```

---

## 安装 Python 依赖

### 2.1 依赖说明

**Security Skill 使用 Python 标准库，无外部依赖**。它是 LobsterAI 的一个独立安全模块。

如果需要运行完整的 LobsterAI 系统，其他核心技能（如 docx, xlsx, pdf 等）可能需要额外包。请参考各技能的 `requirements.txt`。

### 2.2 安装命令

```bash
# Security Skill 本身无需安装任何包
# 如果使用 LobsterAI，请确保其环境已正确配置

# 验证
python -c "import security; print('Security module ready')"
```

### 2.3 可选工具（仅开发/扫描用）

以下工具不是运行 Security Skill 所必需的，仅用于额外的安全分析：

```bash
# 依赖漏洞扫描（独立工具）
pip install pip-audit

# 代码质量检查（独立工具）
pip install bandit safety

# 测试覆盖率
pip install coverage
```

**注意**: 这些工具用于扫描其他技能的依赖，不是 Security Skill 的运行时依赖。

---

## 部署安全模块

### 3.1 定位 SKILLs 根目录

```bash
# 通常位置
SKILLS_LOCAL="C:\Users\Administrator\AppData\Local\Programs\LobsterAI\resources\SKILLs"
SKILLS_ROAMING="C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs"

# 选择部署位置（建议 Local，因为它是程序自带位置）
export SKILLS_ROOT="$SKILLS_LOCAL"
```

### 3.2 创建 security 目录

```bash
cd "$SKILLS_ROOT"
mkdir -p security
```

### 3.3 复制安全模块

如果安全模块已在 `security/` 目录：

```bash
# 从项目目录复制
cp -r /path/to/project/security/* "$SKILLS_ROOT/security/"
```

**应包含的文件**:
```
security/
├── __init__.py           # 包标识
├── audit_logger.py       # 审计日志记录器（直接调用，无需 Shell 包装器）
├── input_validator.py    # 输入验证
├── output_sanitizer.py   # 输出清理
├── authorizer.py         # RBAC 授权器
├── code_scanner.py       # 恶意代码扫描器
├── dependency_scanner.py # 依赖漏洞扫描器
├── tests.py              # 单元测试套件（可选，开发用）
├── rbac_config.example.json  # RBAC 配置示例
└── DEPLOYMENT.md         # 本文件
```

### 3.4 设置目录权限（可选安全强化）

默认情况下，security 目录使用标准权限即可工作。如果环境对安全性要求极高，可参考以下步骤进行权限加固。

**Windows**（可选）:
```powershell
# 限制仅 Administrators 可写（生产环境建议）
# icacls "$SKILLS_ROOT\security" /inheritance:r
# icacls "$SKILLS_ROOT\security" /grant "Administrators:(OI)(CI)F"
# icacls "$SKILLS_ROOT\security" /remove "Users"
# icacls "$SKILLS_ROOT\security" /remove "Authenticated Users"
```

**Linux/macOS**（可选）:
```bash
# 设置严格权限
# chmod 755 security
# chmod 644 security/*.py
# chown -R root:root security  # 需要 sudo（不推荐）
```
**注意**: 严格权限可能需要管理员/root 权限，仅建议在生产环境且符合安全策略时启用。开发环境通常不需要。

---

## 配置审计日志

### 4.1 创建日志目录

```bash
# 确定 LOBSTERAI_HOME
export LOBSTERAI_HOME="${LOBSTERAI_HOME:-${APPDATA:-$HOME/.config}/LobsterAI}"

# Windows (PowerShell)
$LOBSTERAI_HOME = "$env:APPDATA\LobsterAI"

# 创建日志目录
mkdir -p "$LOBSTERAI_HOME/logs/security"
```

### 4.2 设置日志权限（可选）

默认情况下，日志目录使用标准权限即可。如果环境对日志完整性有严格要求，可进行以下权限加固。

**Windows**（可选）:
```powershell
$logDir = "$LOBSTERAI_HOME\logs\security"
New-Item -ItemType Directory -Force -Path $logDir
# 如需限制仅 Administrators 可读写，可启用以下命令（需要管理员权限）
# icacls $logDir /inheritance:r
# icacls $logDir /grant "Administrators:(OI)(CI)F"
# icacls $logDir /remove "Users"
# icacls $logDir /remove "Authenticated Users"
```

**Linux/macOS**（可选）:
```bash
mkdir -p "$LOBSTERAI_HOME/logs/security"
# chmod 700 限制仅所有者访问（生产环境建议）
# chmod 700 "$LOBSTERAI_HOME/logs/security"
# chown root:root "$LOBSTERAI_HOME/logs/security"  # 需要 sudo，不推荐以 root 运行 LobsterAI
```
**注意**: 严格日志权限可能需要管理员权限，仅建议在合规性要求严格的场景使用。

### 4.3 测试日志写入

```bash
# 测试 Python 审计日志器
python "$SKILLS_ROOT/security/audit_logger.py" \
  --event start \
  --skill test-skill \
  --data '{"test": "data"}'

# 检查日志文件
tail -1 "$LOBSTERAI_HOME/logs/security/audit.log" | jq .
```

### 4.4 配置 RBAC 授权

1. 复制 RBAC 配置模板：
   ```bash
   cp "$SKILLS_ROOT/security/rbac_config.example.json" "$LOBSTERAI_HOME/security/rbac_config.json"
   ```

2. 编辑 `rbac_config.json`，根据实际需求调整：
   - 为用户分配角色（admin, operator, auditor, user）
   - 配置技能白名单/公开列表
   - 设置技能级别的角色限制

3. 配置文件权限（可选）:
   ```bash
   # 生产环境建议限制为仅管理员可读写
   # icacls "$LOBSTERAI_HOME/security/rbac_config.json" /inheritance:r
   # icacls "$LOBSTERAI_HOME/security/rbac_config.json" /grant "Administrators:R"
   # 或使用 chmod 设置适当权限（Linux/macOS）
   # chmod 600 "$LOBSTERAI_HOME/security/rbac_config.json"
   ```
   **注意**: 配置文件包含敏感权限策略，建议在生产环境中限制访问权限。开发环境可跳过此步骤。

### 4.5 配置安全扫描

安全扫描器（code_scanner, dependency_scanner）无需额外配置，使用内置数据库。

**定期扫描建议**:
- 每日自动扫描所有技能代码
- 每次依赖更新后运行依赖漏洞扫描
- 技能上线前必须通过代码扫描

**扫描命令示例**:
```bash
# 代码扫描
python -m security.code_scanner --skill all --output markdown > code-scan-report.md

# 依赖扫描
python -m security.dependency_scanner --skill all --output json > dep-scan-report.json
```

---

## 集成到技能脚本

### 5.1 Python 技能

在技能脚本开头添加：

```python
#!/usr/bin/env python3
import os
import sys
import time
import json

# 添加 security 到路径
SKILLS_ROOT = os.environ.get('SKILLS_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(SKILLS_ROOT, 'security'))

from security.audit_logger import audit_logger
from security.authorizer import can_execute_skill
from security.input_validator import InputValidator, validate_input
from security.output_sanitizer import OutputSanitizer

def main():
    skill_name = "my-skill"
    user_id = os.environ.get('LOBSTERAI_USER_ID', 'anonymous')

    # 1. 解析输入
    input_data = json.loads(sys.stdin.read())

    # 2. 输入验证（基本）
    errors = []
    if 'prompt' in input_data:
        validator = InputValidator()
        valid, validation_errors = validator.validate_skill_prompt(skill_name, input_data['prompt'])
        if not valid:
            errors.extend(validation_errors)

    if errors:
        error_resp = {'error': 'Validation failed', 'details': errors}
        print(json.dumps(error_resp))
        audit_logger.log_event('validation_failed', {'errors': errors}, user_id, skill_name, level='error')
        sys.exit(1)

    # 3. 授权检查（RBAC）
    if not can_execute_skill(user_id, skill_name, context={'input': input_data}):
        error_resp = {'error': 'Unauthorized: insufficient permissions'}
        print(json.dumps(error_resp))
        audit_logger.log_event('authorization_denied', {}, user_id, skill_name, level='warning')
        sys.exit(403)

    # 4. 审计：开始
    audit_logger.log_event('skill_execution_start', input_data, user_id, skill_name)
    start_time = time.time()

    try:
        # 5. 执行业务逻辑（敏感数据应在输出前清理）
        result = do_work(input_data)

        # 6. 输出清理（脱敏）
        safe_result = OutputSanitizer.sanitize_dict(result)

        # 7. 审计：成功结束
        duration = (time.time() - start_time) * 1000
        audit_logger.log_event('skill_execution_end', {
            'result': safe_result,
            'duration_ms': duration
        }, user_id, skill_name)

        # 8. 输出结果
        print(json.dumps(safe_result))

    except Exception as e:
        # 9. 审计：错误（错误信息自动脱敏）
        duration = (time.time() - start_time) * 1000
        error_msg = OutputSanitizer.sanitize(str(e))
        audit_logger.log_event('skill_execution_error', {
            'error': error_msg,
            'duration_ms': duration
        }, user_id, skill_name, level='error')
        error_resp = {'error': 'Execution failed', 'details': error_msg}
        print(json.dumps(error_resp))
        sys.exit(1)

def do_work(input_data):
    # 技能具体逻辑
    return {'status': 'ok'}

if __name__ == "__main__":
    main()
```

### 5.2 Bash/Shell 技能

在脚本中添加审计调用（直接调用 Python 审计日志器）：

```bash
#!/usr/bin/env bash
set -euo pipefail

# 路径设置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="${SKILLS_ROOT:-$(dirname "$SCRIPT_DIR")}"
PYTHON_AUDIT_LOGGER="$SKILLS_ROOT/security/audit_logger.py"

# 审计日志函数
audit_start() {
    local skill_name="$1"
    local input_file="$2"

    if [[ -f "$PYTHON_AUDIT_LOGGER" ]]; then
        local data
        data=$(jq -c '.' "$input_file" 2>/dev/null || echo '{}')
        python "$PYTHON_AUDIT_LOGGER" --event start --skill "$skill_name" --data "$data" &
        echo $! > /tmp/audit_pid_$$  # 保存 PID 以便后续
    fi
}

audit_end() {
    local skill_name="$1"
    local duration="$2"
    local result_file="$3"

    if [[ -f "$PYTHON_AUDIT_LOGGER" ]]; then
        local data
        data=$(jq -c '.' "$result_file" 2>/dev/null || echo '{}')
        python "$PYTHON_AUDIT_LOGGER" --event end --skill "$skill_name" --data "$data" --duration "$duration" &
    fi
}

audit_error() {
    local skill_name="$1"
    local error_msg="$2"

    if [[ -f "$PYTHON_AUDIT_LOGGER" ]]; then
        python "$PYTHON_AUDIT_LOGGER" --event error --skill "$skill_name" --error "$error_msg" &
    fi
}

# 使用示例
input_file="/tmp/input.json"
output_file="/tmp/output.json"

audit_start "my-skill" "$input_file"
start_time=$(date +%s%3N)

try {
    # 执行业务逻辑
    python myscript.py "$input_file" > "$output_file"
    status=0
} || {
    status=$?
    audit_error "my-skill" "Exit code: $status"
    exit $status
}

end_time=$(date +%s%3N)
duration=$((end_time - start_time))
audit_end "my-skill" "$duration" "$output_file"
```

### 5.3 Node.js 技能

```javascript
const { execFile } = require('child_process');
const path = require('path');

const SKILLS_ROOT = process.env.SKILLS_ROOT || path.join(__dirname, '..');
const AUDIT_LOGGER = path.join(SKILLS_ROOT, 'security', 'audit_logger.py');

function auditStart(skillName, inputData) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify(inputData);
        execFile('python', [AUDIT_LOGGER, '--event', 'start', '--skill', skillName, '--data', data], (err) => {
            if (err) console.warn('Audit log failed:', err);
            resolve();
        });
    });
}

function auditEnd(skillName, result, durationMs) {
    const data = JSON.stringify(result);
    execFile('python', [AUDIT_LOGGER, '--event', 'end', '--skill', skillName, '--data', data, '--duration', durationMs.toString()]);
}

function auditError(skillName, error) {
    execFile('python', [AUDIT_LOGGER, '--event', 'error', '--skill', skillName, '--error', error.message]);
}

// 使用
async function main() {
    const input = getInput();
    await auditStart('my-skill', input);
    const start = Date.now();

    try {
        const result = await doWork(input);
        await auditEnd('my-skill', result, Date.now() - start);
        output(result);
    } catch (error) {
        await auditError('my-skill', error);
        throw error;
    }
}
```

---

## 验证部署

### 6.1 检查文件

```bash
# 安全模块存在
ls -la "$SKILLS_ROOT/security/"

# 应显示：
# audit_logger.py
# input_validator.py
# output_sanitizer.py
# ...

# 日志目录存在
ls -la "$LOBSTERAI_HOME/logs/security/"
```

### 6.2 测试审计日志

```bash
# 测试记录
python "$SKILLS_ROOT/security/audit_logger.py" \
  --event start \
  --skill validation-test \
  --data '{"test": "audit"}'

# 验证日志
tail -1 "$LOBSTERAI_HOME/logs/security/audit.log" | python -m json.tool
```

### 6.3 测试输入验证

```bash
# 正常输入
echo '{"prompt": "search for news"}' | \
  python "$SKILLS_ROOT/security/input_validator.py" --skill scheduled-task --input -

# 危险输入（应失败）
echo '{"prompt": "rm -rf /"}' | \
  python "$SKILLS_ROOT/security/input_validator.py" --skill scheduled-task --input -
```

### 6.4 测试输出清理

```bash
# 测试清理
echo '{"error": "Failed with password=secret123"}' | \
  python "$SKILLS_ROOT/security/output_sanitizer.py" --json -
# 输出: {"error": "Failed with password=[REDACTED]"}
```

### 6.5 测试 RBAC 授权

```bash
# 使用测试配置（见 rbac_config.example.json）
# 创建测试用户
export LOBSTERAI_USER_ID="test_operator"

# 测试白名单技能（应允许）
python -c "from security.authorizer import can_execute_skill; print(can_execute_skill('test_operator', 'web-search'))"
# 期望输出: True

# 测试非白名单技能（应拒绝）
python -c "from security.authorizer import can_execute_skill; print(can_execute_skill('test_operator', 'scheduled-task'))"
# 期望输出: False
```

### 6.6 测试代码扫描

```bash
# 扫描单个技能
python -m security.code_scanner --skill web-search --output markdown > web-scan.md

# 查看报告
cat web-scan.md | grep -E "威胁等级|问题数"
# 期望：web-search 应无 critical/high 问题
```

### 6.7 测试依赖扫描

```bash
# 扫描所有技能的依赖
python -m security.dependency_scanner --skill all --output json > dep-scan.json

# 检查报告
python -c "import json; data=json.load(open('dep-scan.json')); print('Total:', data['total_skills'], 'Vulns:', sum(data['summary'].values()))"
```

### 6.8 运行完整测试套件

```bash
cd "$SKILLS_ROOT/security"
python tests.py

# 期望输出: Ran 25 tests in ... OK
```

### 6.9 测试技能集成

选择 3 个技能进行集成测试：

1. **scheduled-task**（高风险）- 测试授权拒绝
2. **imap-smtp-email**（敏感数据）- 测试输出脱敏
3. **web-search**（浏览器）- 测试完整流程

执行典型任务，检查：
- 审计日志是否记录
- 错误信息是否脱敏
- 输入验证是否生效
- 授权检查是否正常

---

## 故障排除

### 7.1 审计日志不写入

**症状**: 执行技能后，`audit.log` 无新条目

**排查**:
1. 检查 `LOBSTERAI_HOME` 环境变量是否设置
   ```bash
   echo $LOBSTERAI_HOME
   ```
2. 检查日志目录权限
   ```bash
   ls -ld "$LOBSTERAI_HOME/logs/security"
   ```
3. 检查 Python 模块导入
   ```bash
   python -c "from security.audit_logger import get_audit_logger; print('OK')"
   ```
4. 查看技能脚本是否调用审计函数

**修复**:
- 设置 `LOBSTERAI_HOME` 环境变量
- 确保目录可写
- 确保 `security/` 在 `sys.path` 中

### 7.2 输入验证误阻断

**症状**: 正常 prompt 被 ValidationError 拒绝

**排查**:
1. 查看错误信息
2. 检查 prompt 是否包含被黑名单的词（如 "delete" 在 "delete old records" 中）

**修复**:
- 调整 `input_validator.py` 中的 `allowed_commands` 或 `dangerous_commands`
- 使用更精确的单词边界检测：`\brm\b` 而非包含匹配

### 7.3 输出清理过度

**症状**: 正常信息被误判为敏感

**排查**: 检查 `output_sanitizer.py` 的正则模式是否过于宽泛

**修复**: 细化正则表达式，使用更严格的边界

### 7.4 web-search 启动失败

**症状**: 以 root 运行时立即失败

**原因**: 已修复的 root 防护（安全增强）

**解决**:
- **推荐**: 使用非 root 用户运行 LobsterAI
- **临时绕过（不推荐）**: 修复 `browser.js` 回退到 `--no-sandbox`（会降低安全性）

### 7.5 依赖包冲突

**症状**: `pip install` 失败或技能导入错误

**解决**:
```bash
# 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 7.6 RBAC 授权失败

**症状**: 技能执行返回 "Unauthorized" 但用户应有权限

**排查**:
1. 检查用户角色分配：`cat "$LOBSTERAI_HOME/security/rbac_config.json" | jq '.role_assignments["<user_id>"]'`
2. 检查技能权限配置：`jq '.skill_permissions["<skill_id>"]'`
3. 检查白名单/公开列表

**修复**:
- 更新 `rbac_config.json` 为用户添加正确角色
- 将技能加入白名单或公开列表
- 重新加载配置：`python -c "from security.authorizer import get_authorizer; get_authorizer().reload_config()"`

### 7.7 代码扫描误报/漏报

**症状**: 安全代码被标记为危险，或危险代码未检测到

**排查**:
1. 查看扫描报告详细信息：`python -m security.code_scanner --skill <skill> --output markdown`
2. 检查 `DANGEROUS_FUNCTIONS` 和 `DANGEROUS_MODULES` 定义

**修复**:
- 调整 `code_scanner.py` 中的检测规则
- 对于误报，添加例外逻辑（需评估风险）

### 7.8 依赖漏洞扫描无结果

**症状**: 已知漏洞未检测到

**排查**:
1. 检查内置数据库是否包含该包：`grep -A2 "requests" security/dependency_scanner.py`
2. 检查版本范围匹配逻辑

**修复**:
- 扩展 `KNOWN_VULNERABILITIES` 数据库
- 安装 `safety` 或 `pip-audit` 以获得更全面的检测
- 确保依赖文件格式正确（版本号明确）

---

## 维护与监控

### 8.1 日志轮转

审计日志每天自动轮转（由 `audit_logger.py` 的 `_rotate_if_needed()` 实现）。如需手动触发：

```bash
# 手动轮转（重命名当前日志）
mv "$LOBSTERAI_HOME/logs/security/audit.log" "$LOBSTERAI_HOME/logs/security/audit.log.$(date +%Y%m%d_%H%M%S)"
# 下次写入会自动创建新文件
```

### 8.2 日志分析

**实时监控**:
```bash
tail -f "$LOBSTERAI_HOME/logs/security/audit.log" | jq .
```

**统计调用次数**:
```bash
jq -r '.skill_name' "$LOBSTERAI_HOME/logs/security/audit.log" | sort | uniq -c | sort -nr
```

**查找失败**:
```bash
jq 'select(.event_type=="skill_execution_end" and .status=="failed")' "$LOBSTERAI_HOME/logs/security/audit.log"
```

### 8.3 更新安全模块

当安全模块更新时：

1. 替换 `security/` 目录下的文件
2. 无需重启 LobsterAI（模块按需加载）
3. 建议通知所有技能脚本重新加载（或重启 LobsterAI）

### 8.4 定期安全扫描

**代码扫描**（每日）:
```bash
python -m security.code_scanner --skill all --output markdown > daily-code-scan-$(date +%Y%m%d).md
# 检查是否有新的 critical/high 问题
```

**依赖漏洞扫描**（每次依赖更新后）:
```bash
python -m security.dependency_scanner --skill all --output json > dep-scan-$(date +%Y%m%d).json
# 对比历史报告，关注新出现的漏洞
```

**授权审计**（每周）:
```bash
# 列出所有用户的权限
python -c "from security.authorizer import get_authorizer; a=get_authorizer(); print(a.list_user_permissions('all'))"
```

---

## 进阶配置

### 9.1 SKILL 拓扑图自动更新

SKILL 拓扑关系图 (`skill-topology-interactive.html`) 支持自动更新，在安装或学习新 SKILL 后运行：

```bash
# 生成拓扑数据（自动检测 SKILLs 位置）
python update_topology.py

# 指定 SKILLs 位置
python update_topology.py --skills-dir "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs"

# 使用自定义配置（调整 category/tier/desc）
python update_topology.py --config topology-config.json
```

生成的 `skill-topology-data.json` 会被 `skill-topology-interactive.html` 自动加载。

**自定义元数据**：
复制 `topology-config.example.json` 为 `topology-config.json`，编辑后使用 `--config` 参数。

**建议工作流**：
1. 安装新 SKILL（复制到 SKILLs 目录）
2. 如需自定义元数据，编辑 topology-config.json
3. 运行 `python update_topology.py`
4. 刷新 `skill-topology-interactive.html` 查看新 SKILL

### 9.2 审计日志签名（防篡改）

审计日志支持 HMAC 签名，确保日志完整性。

**配置**:
```bash
# 设置签名密钥（仅管理员可访问）
export LOBSTERAI_AUDIT_SECRET="your-32-byte-or-longer-secret-key"
# Windows (PowerShell)
$env:LOBSTERAI_AUDIT_SECRET = "your-secret-key"
```

密钥要求：
- 长度至少 32 字符
- 使用高熵随机字符串
- 存储在安全位置（如 Windows Credential Manager 或 Azure Key Vault）

**验证签名**（示例）:
```python
from security.audit_logger import get_audit_logger
logger = get_audit_logger()
logs = logger.get_recent_logs(hours=1)
for entry in logs:
    # 验证 entry['signature']
    pass
```

### 9.2 RBAC 动态配置

**热重载配置** 无需重启：
```python
from security.authorizer import get_authorizer
get_authorizer().reload_config()
```

**多租户支持**（规划中）:
可为不同租户使用不同的 RBAC 配置文件，通过 `LOBSTERAI_TENANT_ID` 环境变量区分。

### 9.3 自定义扫描规则

扩展 `PythonCodeScanner` 类：

```python
class MyScanner(PythonCodeScanner):
    DANGEROUS_FUNCTIONS = {
        **PythonCodeScanner.DANGEROUS_FUNCTIONS,
        'my_custom_danger': 'critical'
    }
    DANGEROUS_MODULES = {
        **PythonCodeScanner.DANGEROUS_MODULES,
        'suspicious_lib': 'high'
    }

scanner = MyScanner()
```

### 9.4 加密审计日志

（可选）使用 `cryptography` 库加密日志文件：

```bash
pip install cryptography
```

配置 `audit_logger.py` 使用 Fernet 加密：
```python
from cryptography.fernet import Fernet
cipher = Fernet(KEY)
encrypted = cipher.encrypt(json.dumps(entry).encode())
```

### 9.5 远程日志收集

（可选）配置 `audit_logger.py` 将日志发送到 SIEM 系统：

```python
import requests
def send_to_siem(entry):
    try:
        requests.post('https://siem.company.com/audit', json=entry, timeout=5)
    except Exception as e:
        # 本地降级存储
        pass
```

**推荐方案**: 使用 Fluentd / Logstash 收集日志文件，而非直接集成。

### 9.6 自定义验证规则

扩展 `InputValidator` 类：

```python
class CustomValidator(InputValidator):
    def validate_my_skill(self, data):
        # 自定义规则
        if data.get('user_id') not in ALLOWED_USERS:
            raise ValidationError("User not allowed")
        super().validate_all('my-skill', data)
```

---

## 联系与支持

- **安全事件**: security@lobsterai.com
- **漏洞报告**: 通过内部漏洞赏金平台
- **文档更新**: 修改 `SECURITY.md` 并提交 PR

---

**部署完成检查清单**:

- [ ] Python 依赖全部安装
- [ ] security/ 目录部署到 SKILLs 根目录
- [ ] LOBSTERAI_HOME/logs/security/ 目录存在且权限正确
- [ ] 测试审计日志写入成功
- [ ] 测试输入验证和输出清理
- [ ] 至少 3 个高风险技能已集成审计
- [ ] 管理员已阅读本指南

**恭喜！安全框架已成功部署。**

- **安全事件**: security@lobsterai.com
- **漏洞报告**: 通过内部漏洞赏金平台
- **文档更新**: 修改 `SECURITY.md` 并提交 PR

---

**部署完成检查清单**:

- [ ] Python 依赖全部安装
- [ ] security/ 目录部署到 SKILLs 根目录
- [ ] LOBSTERAI_HOME/logs/security/ 目录存在且权限正确
- [ ] 测试审计日志写入成功
- [ ] 测试输入验证和输出清理
- [ ] 至少 3 个高风险技能已集成审计
- [ ] 管理员已阅读本指南

**恭喜！安全框架已成功部署。**
