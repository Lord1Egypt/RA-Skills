---
name: ops-code-review
description: |
  Code Review 安全扫描工具，自动化代码审计，支持 Django/Python、React+TypeScript、PHP 多语言。
  自动识别代码仓库提交变更，调用安全扫描器进行规范检查和风险检测，报告推送飞书群。
  支持 post-commit hook 增量扫描和定时全量扫描。
  关键词：Code Review SVN security scan Django React PHP 代码审计 代码扫描 安全检测 CI/CD 自动化
metadata:
  openclaw:
    requires:
      bins: [svn, bandit, pylint, npx, phpcs]
      env:
        - CODE_REVIEW_SVN_USER
        - CODE_REVIEW_SVN_PASS
        - CODE_REVIEW_FEISHU_CHAT_ID
        - CODE_REVIEW_CONFIG
    install:
      - id: svn
        kind: system
        label: "Install SVN (subversion)"
        command: "apt-get install subversion"
      - id: bandit
        kind: pip
        label: "Install Bandit (Python security scanner) — ⚠️ uses --break-system-packages"
        note: "⚠️ pip --break-system-packages affects system-wide packages. Prefer a virtual environment."
        package: "bandit --break-system-packages"
      - id: pylint
        kind: pip
        label: "Install Pylint (Python linter) — ⚠️ uses --break-system-packages"
        note: "⚠️ pip --break-system-packages affects system-wide packages. Prefer a virtual environment."
        package: "pylint --break-system-packages"
      - id: node
        kind: node
        label: "Install Node.js (for npx/eslint)"
        package: node
      - id: composer
        kind: system
        label: "Install Composer (PHP package manager) — ⚠️ download then execute, not pipe"
        command: "curl -sS https://getcomposer.org/installer -o /tmp/composer-setup.php && php /tmp/composer-setup.php -- --install-dir=/usr/local/bin --filename=composer && rm -f /tmp/composer-setup.php"
        note: "⚠️ Downloads installer to /tmp first before executing. Review the command before running; prefer isolated environment."
      - id: phpcs
        kind: composer
        label: "Install PHP CodeSniffer"
        package: squizlabs/php_codesniffer
      - id: typescript-eslint
        kind: node_global
        label: "Install typescript-eslint (ESLint parser for TS/TSX) — ⚠️ global npm install"
        note: "⚠️ Global npm install modifies host environment. Review before running."
---

# Code Review Skill

## 首次使用前配置（必读）

### 1. 设置环境变量

**Linux/Mac**（加到 `~/.bashrc` 或 `~/.zshrc`）：
```bash
export CODE_REVIEW_SVN_USER="你的SVN用户名"
export CODE_REVIEW_SVN_PASS="你的SVN密码"
export CODE_REVIEW_FEISHU_CHAT_ID="飞书群机器人chat_id"
```

**OpenClaw 配置**（推荐，写入 OpenClaw 环境变量）：
在 OpenClaw 配置文件中添加：
```json
{
  "env": {
    "CODE_REVIEW_SVN_USER": "你的SVN用户名",
    "CODE_REVIEW_SVN_PASS": "你的SVN密码",
    "CODE_REVIEW_FEISHU_CHAT_ID": "飞书群机器人chat_id"
  }
}
```

### 2. 配置仓库信息

创建配置文件（完整示例包含所有支持的仓库）：
```bash
cat > config.json << 'EOF'
{
  "repos": {
    "ops_api": {
      "url": "http://your-svn/ops/dev/branches/branch_dev/ops_api",
      "lang": "django",
      "type": "incremental",
      "local": "/tmp/svn_repos/ops_api"
    },
    "ops_web": {
      "url": "http://your-svn/ops/dev/branches/branch_dev/ops_web",
      "lang": "react",
      "type": "incremental",
      "local": "/tmp/svn_repos/ops_web"
    },
    "ops_api_trunk": {
      "url": "http://your-svn/ops/dev/trunk/ops_api",
      "lang": "django",
      "type": "full",
      "local": "/tmp/svn_repos/ops_api_trunk"
    },
    "ops_web_trunk": {
      "url": "http://your-svn/ops/dev/trunk/ops_web",
      "lang": "react",
      "type": "full",
      "local": "/tmp/svn_repos/ops_web_trunk"
    },
    "gm": {
      "url": "http://your-svn/gm/trunk",
      "lang": "mixed",
      "type": "both",
      "local": "/tmp/svn_repos/gm"
    }
  }
}
EOF
```

将配置复制到运行时目录（必须）：
```bash
cp -f config.json /tmp/code_review_config.json
```

**注意**：`config.json` 不随 skill 上传，请根据实际 SVN 地址修改各仓库的 `url` 字段。

### 3. 检查工具依赖

```bash
python3 scripts/code_review.py check-deps
```

如有缺失工具，自动安装：
```bash
python3 scripts/code_review.py install-deps
```

## 能力概览

| 功能 | 说明 |
|------|------|
| 🔍 增量扫描 | post-commit 触发，只扫本次提交的文件 |
| 📋 全量扫描 | 每周定时，扫描整个仓库 |
| 🛠️ 多语言支持 | Django / React+TS / PHP |
| 🔴 问题分级 | ERROR / WARNING / INFO 三级 |
| 🛠️ 修复建议 | 具体代码修改方案，不只是说"有问题" |
| 📤 飞书推送 | 报告发送到配置的飞书群 |

## 环境变量说明

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CODE_REVIEW_SVN_USER` | ✅ | SVN 只读用户名 |
| `CODE_REVIEW_SVN_PASS` | ✅ | SVN 密码 |
| `CODE_REVIEW_FEISHU_CHAT_ID` | ✅ | 飞书群 chat_id（机器人 webhook 或群 ID）|
| `CODE_REVIEW_CONFIG` | ❌ | config.json 路径，默认为 `/tmp/code_review_config.json`（建议使用受保护目录如 `~/.config/code-review/config.json`）|

## 使用方式

### 手动触发扫描

```
审计代码 incremental ops_api    # 增量扫描（只扫变更）
审计代码 full gm                 # 全量扫描指定仓库
审计代码 fullall                 # 全量扫描所有仓库
审计代码 sync                   # 同步所有 SVN 仓库
审计代码 check-deps             # 检查工具依赖
```

### 增量扫描流程（post-commit hook）

```
用户提交代码
    ↓
SVN post-commit hook 触发
    ↓
code_review.py incremental <repo_name>
    ↓
SVN Manager 获取本次变更文件
    ↓
Analyzer 逐语言分析
    ↓
Report Generator 生成飞书格式报告
    ↓
推送到飞书群
```

### 全量扫描流程（定时任务）

```
每周定时触发
    ↓
code_review.py fullall
    ↓
遍历所有仓库，checkout 全量代码
    ↓
按语言全量扫描
    ↓
生成报告推送飞书
```

## 工具依赖

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `svn` | SVN 客户端 | `apt-get install subversion` |
| `bandit` | Python 安全扫描 | `pip install --break-system-packages bandit` |
| `pylint` | Python 代码检查 | `pip install --break-system-packages pylint` |
| `npx` | 执行 ESLint | `npm install -g npx` |
| `composer` | PHP 包管理器 | 下载安装脚本到 `/tmp` 后执行（不通过管道），最后清理安装文件 |
| `phpcs` | PHP 代码规范 | `composer global require squizlabs/php_codesniffer` |
| `@typescript-eslint/*` | ESLint 的 TypeScript 解析器 | `npm install -g @typescript-eslint/parser @typescript-eslint/eslint-plugin typescript-eslint` |

**首次使用前必须运行工具检查**，确保所有依赖就绪。

## SVN Hook 部署

### 生成 hook 脚本
```
code_review.py setup-hooks
```

### 部署步骤
1. 在 SVN 服务器上找到仓库路径
2. 将生成的 `post-commit` 脚本放到 `hooks/` 目录
3. 赋予执行权限：`chmod +x hooks/post-commit`
4. 确保 SVN 服务器能访问本 skill 的 scripts 目录

## 定时任务配置（OpenClaw Cron）

推荐使用 OpenClaw 内置 cron，比服务器 crontab 更方便管理：

```json
{
  "schedule": { "kind": "cron", "expr": "0 3 * * 1", "tz": "Asia/Shanghai" },
  "payload": { "kind": "agentTurn", "message": "执行全量代码审计：\ncd /root/.openclaw/workspace/skills/code-review && python3 scripts/code_review.py fullall" },
  "sessionTarget": "isolated"
}
```

创建方式：告诉 OpenClaw "帮我创建一个每周一凌晨3点执行全量代码审计的定时任务"

## 报告示例

```
📊 代码审计报告
━━━━━━━━━━━━━━━━━━
🏷️ 仓库：运维后台后端 (Django)
📅 时间：2026-04-14 10:00
🔍 方式：🔄 增量扫描
📁 扫描文件：5
🐛 问题总数：3
  🔴 严重/错误：1
  🟡 警告：1
  🟢 提示：1
━━━━━━━━━━━━━━━━━━

🔴 严重 | models/user.py:45
   └ [CUST-105] 敏感信息明文存储
   └ 🛠️ 修复：使用环境变量或密钥管理服务，不要明文存储

🟡 警告 | views/order.py:88
   └ [CUST-311] 潜在 SQL 拼接风险
   └ 🛠️ 修复：使用参数化查询，避免字符串拼接查询语句

🟢 提示 | utils/helper.py:12
   └ [CUST-324] 弱随机数生成
   └ 🛠️ 修复：使用 os.urandom 或 secrets 模块替代 random

━━━━━━━━━━━━━━━━━━
⚙️ 由 OpenClaw 代码审计 Skill 自动生成
```

## 注意事项

1. **敏感信息**：SVN 账密和飞书群 ID 通过环境变量注入，不随 skill 上传
2. **首次使用**：先配置环境变量 → 创建 config.json → 复制到 `/tmp/code_review_config.json` → 运行 `check-deps` → 运行 `install-deps` → 运行 `sync`
3. **工具缺失**：记录在 `/tmp/code_review_missing_tools.json`，运行 `install-deps` 自动安装
4. **扫描效率**：全量扫描较慢，建议放在低峰时段
5. **误报处理**：如果某类问题确认为可接受的惯用写法，可以在报告中注明

## ClawScan 安全自检清单

发布前用以下命令扫描所有脚本和引用文档：

```bash
grep -rE "(oc_[a-f0-9]+|http://[a-z]+\.[a-z]+|:[0-9]{4,5})" \
  scripts/ references/ --include="*.py" --include="*.md" --include="*.yml"
```

**触发 ClawScan flag 的模式（立即修复）：**
- `oc_` 开头的真实飞书 ID → 改为 `os.environ.get("CODE_REVIEW_FEISHU_CHAT_ID", "")`
- 内网 hostname（如 `zabbix.ops.qiyujoy.com`）→ 改为 `os.environ.get("ZABBIX_URL", "")`
- 真实用户名默认值 → 改为 `os.environ.get("XXX_USER", "")` 空默认值
- 任何 Base64 编码或明显凭据格式的字符串

**不触发 flag 的安全模式：**
- `{{ MYSQL_PASSWORD }}`（Ansible Jinja2 变量注入）
- `<your_mysql_password>`、`<your_token>`（尖括号包裹的占位符）
- `os.environ.get("XXX", "")` 空默认值
- 示例 URL 如 `https://zabbix.example.com`、`http://your-svn/ops/dev/branches/`

**元数据声明要求：**
所有运行时需要的环境变量必须在 frontmatter 的 `metadata.openclaw.requires.env` 中声明，包括非敏感的 `CODE_REVIEW_CONFIG`。敏感凭据变量（`CODE_REVIEW_SVN_PASS` 等）必须声明，但不赋值。
