# 版本迁移指南

本文档提供 OpenClaw 配置的版本升级和配置迁移完整指南，确保平滑过渡到新版本。

## 目录

- [升级前准备](#升级前准备)
- [版本兼容性矩阵](#版本兼容性矩阵)
- [v1.0.0 → 2026.3.28 关键变更](#v100--2026328-关键变更)
- [迁移步骤](#迁移步骤)
- [破坏性变更](#破坏性变更)
- [验证与测试](#验证与测试)
- [回滚方案](#回滚方案)
- [实用脚本](#实用脚本)

---

## 升级前准备

### 0. 版本检查（必做）

在执行任何迁移操作之前，必须先检查当前版本和最新版本：

```bash
# 检查本地版本
openclaw --version
# 输出示例: OpenClaw 2026.4.1 (da64a97)

# 检查最新可用版本（JSON 格式，便于脚本解析）
openclaw update status --json
# 关键字段:
#   availability.latestVersion      — 最新版本号
#   availability.hasRegistryUpdate  — 是否有更新可用

# 预览更新内容（不实际更新）
openclaw update --dry-run
openclaw update --dry-run --json
```

**版本不一致时的处理**：
```bash
# 如果有更新可用，先更新 openclaw 本身
openclaw update          # 交互式更新
openclaw update --yes    # 非交互式更新

# 更新完成后验证版本
openclaw --version
```

**技能版本检查**：
```bash
# 确保配置技能是最新版本
openclaw skills update openclaw-config-master

# 查看已安装技能列表
openclaw skills list
```

**查阅最新文档**：
```bash
# 内置文档搜索
openclaw docs "configuration"
openclaw docs "migration"

# 在线文档
# 配置参考: https://docs.openclaw.ai/gateway/configuration-reference
# Update CLI: https://docs.openclaw.ai/cli/update
```

### 1. 备份配置

```bash
# 创建备份目录
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=".clawhub/backup_$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

# 备份所有配置
cp -r .clawhub/* "$BACKUP_DIR/"

# 备份特定文件
cp _meta.json "$BACKUP_DIR/"
cp SKILL.md "$BACKUP_DIR/"
```

### 2. 检查清单

在升级前，请确认：

- [ ] 当前版本已记录（查看 `_meta.json`）
- [ ] 所有配置文件已备份
- [ ] 环境变量已记录（如果有）
- [ ] 自定义脚本已备份
- [ ] 测试环境可用（建议先在测试环境验证）

### 3. 版本信息查看

```bash
# 查看当前配置版本
cat _meta.json | grep -E '"version"|"schemaVersion"'

# 查看配置结构
python3 << 'EOF'
import json
with open('_meta.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f"当前版本: {data.get('version', 'unknown')}")
    print(f"Schema版本: {data.get('schemaVersion', 'unknown')}")
EOF
```

---

## 版本兼容性矩阵

| 当前版本 | 目标版本 | 兼容性 | 需要迁移 | 风险等级 |
|---------|---------|-------|---------|---------|
| 1.0.x | 1.1.x | ✅ 完全兼容 | 否 | 低 |
| 1.0.x | 2.0.x | ⚠️ 需要迁移 | 是 | 中 |
| 1.x | 3.0.x | ❌ 破坏性变更 | 是 | 高 |
| 2.x | 3.0.x | ⚠️ 需要迁移 | 是 | 中 |
| **1.0.x** | **2026.3.28** | **⚠️ 需要迁移** | **是** | **高** |

---

## v1.0.0 → 2026.3.28 关键变更

> **参考来源**：`openclaw/openclaw@v2026.3.28`（schema 生成于 2026-03-22）
> 
> **背景**：原 skill 编写时参考的是 `openclaw/openclaw@875324e`（2026-02-07），之间相隔约 7 周，OpenClaw 有大量新增功能和 schema 变更。

### 1. `agents.defaults` — 从 2 个字段扩展到 40+ 个

**旧版（v1.0.0）** 仅记录：
```json
"agents": {
  "defaults": {
    "model": "provider/model",
    "models": { ... }
  }
}
```

**新版（2026.3.28）** 包含 40+ 字段：

| 字段类别 | 新增/变更字段 |
|---------|-------------|
| 模型 | `model`、`imageModel`、`imageGenerationModel`、`pdfModel`、`pdfMaxBytesMb`、`pdfMaxPages`、`models` |
| 工作区 | `workspace`、`repoRoot`、`skipBootstrap`、`bootstrapMaxChars`、`bootstrapTotalMaxChars`、`bootstrapPromptTruncationWarning` |
| 上下文 | `contextTokens`、`contextPruning`、`cliBackends`、`memorySearch`、`userTimezone`、`timeFormat`、`envelopeTimezone`、`envelopeTimestamp`、`envelopeElapsed` |
| 代理行为 | `thinkingDefault`、`verboseDefault`、`elevatedDefault`、`blockStreamingDefault`、`blockStreamingBreak`、`blockStreamingChunk`、`blockStreamingCoalesce` |
| 计时/交互 | `humanDelay`、`timeoutSeconds`、`typingIntervalSeconds`、`typingMode`、`heartbeat`、`maxConcurrent` |
| 媒体 | `mediaMaxMb`、`imageMaxDimensionPx` |
| 子代理/沙箱 | **`subagents`**（`maxConcurrent`、`maxChildrenPerAgent`）、**`sandbox`** |
| 压缩 | **`compaction`**（`mode: "safeguard" \| "aggressive"`） |
| 嵌入式 PI | `embeddedPi` |

**迁移建议**：检查现有配置中 `agents.defaults` 是否只使用了 `model`/`models`。如果使用了 v1.0.0 的简化配置，建议逐步补充新字段以利用新功能。

### 2. `tools.web.search` — 整体结构重构（破坏性变更）

**旧版结构（v1.0.0，已失效）**：
```json
"web": {
  "enabled": true,
  "allowUserUrls": true,
  "allowedDomains": ["github.com", "gitlab.com"]
}
```

**新版结构（2026.3.28）** — 改为 Provider-Specific 架构：

```json
"tools": {
  "web": {
    "search": {
      "enabled": true,
      "provider": "brave",
      "maxResults": 10,
      "timeoutSeconds": 30,
      "cacheTtlMinutes": 60,
      "apiKey": "your-key",

      "brave": { "apiKey": "...", "baseUrl": "...", "model": "...", "mode": "default" },
      "firecrawl": { "apiKey": "...", "baseUrl": "...", "model": "..." },
      "gemini": { "apiKey": "...", "baseUrl": "...", "model": "..." },
      "grok": { "apiKey": "...", "baseUrl": "...", "model": "...", "inlineCitations": true },
      "kimi": { "apiKey": "...", "baseUrl": "...", "model": "..." },
      "perplexity": { "apiKey": "...", "baseUrl": "...", "model": "..." }
    }
  }
}
```

**主要变化**：
- `web` 移到 `tools.web` 下
- `allowUserUrls` 和 `allowedDomains` 被移除，改为每个 provider 的独立配置
- 新增 Provider：`firecrawl`、`gemini`、`grok`、`kimi`、`perplexity`
- 新增 `x_search`（X/Twitter 搜索）和 `fetch`（页面抓取）子模块

### 3. 新增顶级配置根键

以下根键在 v1.0.0 中不存在：

| 新键 | 说明 |
|-----|------|
| **`acp`** | ACP 运行时配置（调度、后端、流转设置等） |
| **`mcp`** | MCP（Model Context Protocol）服务器配置 |
| **`cli`** | CLI 特定配置 |
| **`secrets`** | 密钥管理（providers、resolution、defaults） |

### 4. `approvals` — 新系统（exec/plugin 模式）

```json
"approvals": {
  "exec": {
    "enabled": true,
    "mode": "session",
    "agentFilter": ["agent-id", ...],
    "sessionFilter": ["session-pattern", ...],
    "targets": [{ "channel": "telegram", "accountId": "123", "threadId": "456" }]
  },
  "plugin": {
    "enabled": true,
    "mode": "session",
    "agentFilter": [...],
    "sessionFilter": [...],
    "targets": [...]
  }
}
```

- `mode` 可选：`"session"` | `"targets"` | `"both"`
- `targets` 支持按 `channel`、`to`、`accountId`、`threadId` 细粒度控制

### 5. `bindings` — 从对象变为路由对象数组

**旧版（v1.0.0）**：
```json
"bindings": {
  "channel-name": { ... }
}
```

**新版（2026.3.28）**：
```json
"bindings": [
  {
    "type": "route",
    "agentId": "agent-id",
    "comment": "optional note",
    "match": { "channel": "telegram", "accountId": "123456", "peer": "user@domain" }
  }
]
```

### 6. `hooks` — 扩展了大量新字段

新增字段：`defaultSessionKey`、`allowRequestSessionKey`、`allowedSessionKeyPrefixes`、`allowedAgentIds`、`maxBodyBytes`、`presets`、`transformsDir`、`mappings`

### 7. `tools.profile` — 新增 `"messaging"` 值

有效值：`"minimal"` | `"coding"` | `"messaging"` | `"full"`

### 8. `tools.exec` — 新增多个字段

新增：`host`（`"sandbox"` | `"gateway"` | `"node"`）、`safeBins`、`strictInlineEval`、`safeBinProfiles`、`backgroundMs`、`timeoutSec`、`cleanupMs`、`notifyOnExit`、`applyPatch`

### 9. `gateway` — 新增多个子系统

| 子系统 | 新增内容 |
|-------|---------|
| `gateway.http` | 全新子系统：`endpoints.chatCompletions`、`endpoints.responses`、`securityHeaders` |
| `gateway.push` | APNS relay 配置 |
| `gateway.allowRealIpFallback` | 新布尔字段 |
| `gateway.channelHealthCheckMinutes` | 健康检查间隔 |
| `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback` | 新字段 |
| `gateway.reload.deferralTimeoutMs` | 热重载延迟超时 |
| `gateway.remote` 新增 | `tlsFingerprint`、`sshTarget`、`sshIdentity` |

### 10. `memory.qmd` — 扩展子结构

新增：`mcporter`（MCP Porter 配置）、`limits`、`sessions`、`update`、`scope`、`searchMode`、`includeDefaultMemory`

---

## 迁移步骤

### 标准迁移流程

#### Step 1: 环境准备

```bash
# 1. 确认备份完整性
ls -lh .clawhub/backup_*/

# 2. 创建工作分支（如果使用 Git）
git checkout -b migrate-to-v2026.3.28

# 3. 记录当前状态
echo "迁移前状态:" > migration-log.txt
date >> migration-log.txt
cat _meta.json >> migration-log.txt
```

#### Step 2: 版本分析

```bash
# 分析配置变更
python3 << 'EOF'
import json
import sys

def analyze_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

print("=== 配置分析 ===")
print("1. 检查必需字段:")
# 根据具体版本要求添加检查逻辑

print("\n2. 检查废弃字段:")
# 根据具体版本要求添加检查逻辑

print("\n3. 检查类型兼容性:")
# 根据具体版本要求添加检查逻辑
EOF
```

#### Step 3: 执行迁移

```bash
# 根据目标版本执行相应的迁移脚本
# 示例：迁移到 2026.3.28 版本
./scripts/migrate-to-2026.3.28.sh

# 或使用 Python 脚本
python3 scripts/migrate-to-2026.3.28.py
```

#### Step 4: 验证结果

```bash
# 验证 JSON 格式
for file in .clawhub/**/*.json; do
    python3 -m json.tool "$file" > /dev/null && echo "✅ $file" || echo "❌ $file"
done

# 验证配置完整性
./scripts/validate-config.sh
```

---

## 破坏性变更

### ⚠️ v1.0.0 → 2026.3.28 主要破坏性变更

#### 1. `tools.web.search` 结构完全重构

**旧格式在 2026.3.28 中不再有效。**

| 旧字段 | 状态 | 替代方案 |
|-------|------|---------|
| `web.enabled` | ❌ 移除 | 使用 `tools.web.search.enabled` |
| `web.allowUserUrls` | ❌ 移除 | 每个 Provider 独立配置 |
| `web.allowedDomains` | ❌ 移除 | Provider 配置中管理 |

**迁移步骤**：
1. 将原 `web` 配置迁移到 `tools.web.search`
2. 选择 Provider（`brave`/`firecrawl`/`gemini`/`grok`/`kimi`/`perplexity`）
3. 将 API Key 移到对应 Provider 的 `apiKey` 字段或顶层 `apiKey`

#### 2. `bindings` 从对象变为数组

旧配置 `bindings.{channel}` 需要转换为 `bindings[{ type: "route", match: {...} }]` 格式。

#### 3. `agents.defaults` 字段大幅扩展

旧配置只有 `model`/`models`，新版有 40+ 字段。向后兼容，但仍建议补全缺失字段。

### v1.0 → v2.0 其他变更（参考）

1. **字段重命名**
   ```json
   // 旧版本
   {
     "agentName": "my-agent",
     "agentType": "general"
   }

   // 新版本
   {
     "name": "my-agent",
     "type": "general-purpose"
   }
   ```

2. **结构调整**
   ```json
   // 旧版本
   {
     "config": {
       "timeout": 30,
       "retries": 3
     }
   }

   // 新版本
   {
     "execution": {
       "timeout": 30,
       "retryPolicy": {
         "maxAttempts": 3
       }
     }
   }
   ```

3. **废弃字段**
   - `legacyField` → 已移除
   - `deprecatedOption` → 使用 `newOption` 替代

### v2.0 → v3.0 主要变更（示例）

1. **新架构引入**
2. **配置文件位置变更**
3. **环境变量命名规范更新**

---

## 验证与测试

### 自动化验证

```bash
#!/bin/bash
# validate-migration.sh - 验证迁移结果

echo "=== 迁移验证报告 ==="

# 1. JSON 语法检查
echo "1. JSON 语法检查:"
find .clawhub -name "*.json" -exec python3 -m json.tool {} \; > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ 所有 JSON 文件格式正确"
else
    echo "   ❌ 存在 JSON 格式错误"
    exit 1
fi

# 2. 必需字段检查
echo "2. 必需字段检查:"
python3 << 'EOF'
import json
import sys

required_fields = ['version', 'schemaVersion', 'name']
with open('_meta.json', 'r') as f:
    data = json.load(f)
    missing = [field for field in required_fields if field not in data]
    if missing:
        print(f"   ❌ 缺少必需字段: {missing}")
        sys.exit(1)
    else:
        print("   ✅ 所有必需字段存在")
EOF

# 3. 版本一致性检查
echo "3. 版本一致性检查:"
# 添加具体检查逻辑

echo "   ✅ 验证完成"
```

### 手动测试清单

- [ ] 配置文件加载正常
- [ ] 所有功能可正常使用
- [ ] 日志输出无异常
- [ ] 性能无明显下降
- [ ] 向后兼容性测试通过

---

## 回滚方案

### 快速回滚

```bash
#!/bin/bash
# rollback.sh - 快速回滚到备份版本

BACKUP_DIR=$1

if [ -z "$BACKUP_DIR" ]; then
    echo "用法: ./rollback.sh <备份目录>"
    echo "示例: ./rollback.sh .clawhub/backup_20240101_120000"
    exit 1
fi

echo "=== 开始回滚 ==="
echo "目标备份: $BACKUP_DIR"

# 1. 停止服务（如果运行中）
# systemctl stop openclaw-service

# 2. 备份当前版本（以防万一）
CURRENT_BACKUP=".clawhub/before_rollback_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$CURRENT_BACKUP"
cp -r .clawhub/* "$CURRENT_BACKUP/"

# 3. 恢复备份
echo "恢复配置文件..."
cp -r "$BACKUP_DIR"/* .clawhub/

# 4. 验证恢复
echo "验证恢复结果..."
python3 -m json.tool _meta.json > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ 回滚成功"
else
    echo "❌ 回滚失败，配置文件损坏"
    echo "正在恢复到回滚前状态..."
    cp -r "$CURRENT_BACKUP"/* .clawhub/
    exit 1
fi

# 5. 重启服务
# systemctl start openclaw-service

echo "=== 回滚完成 ==="
```

### 回滚决策树

```
发现问题
    ↓
问题严重吗？
    ├─ 否 → 记录问题，继续监控
    └─ 是 → 可以快速修复？
             ├─ 是 → 修复并验证
             └─ 否 → 执行回滚
                      ↓
                   备份可用？
                      ├─ 是 → 恢复备份
                      └─ 否 → 使用应急方案
```

---

## 实用脚本

### 1. 版本比较工具

```python
#!/usr/bin/env python3
# compare_versions.py - 比较两个配置版本

import json
import sys
from pathlib import Path

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_configs(old_config, new_config):
    """比较两个配置的差异"""
    changes = {
        'added': [],
        'removed': [],
        'modified': [],
        'unchanged': []
    }

    old_keys = set(old_config.keys())
    new_keys = set(new_config.keys())

    # 新增字段
    changes['added'] = list(new_keys - old_keys)

    # 删除字段
    changes['removed'] = list(old_keys - new_keys)

    # 修改字段
    common_keys = old_keys & new_keys
    for key in common_keys:
        if old_config[key] != new_config[key]:
            changes['modified'].append({
                'field': key,
                'old': old_config[key],
                'new': new_config[key]
            })
        else:
            changes['unchanged'].append(key)

    return changes

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python3 compare_versions.py <旧版本> <新版本>")
        sys.exit(1)

    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])

    old_config = load_config(old_path)
    new_config = load_config(new_path)

    changes = compare_configs(old_config, new_config)

    print("=== 配置变更报告 ===")
    print(f"\n新增字段 ({len(changes['added'])}):")
    for field in changes['added']:
        print(f"  + {field}: {new_config[field]}")

    print(f"\n删除字段 ({len(changes['removed'])}):")
    for field in changes['removed']:
        print(f"  - {field}: {old_config[field]}")

    print(f"\n修改字段 ({len(changes['modified'])}):")
    for change in changes['modified']:
        print(f"  ~ {change['field']}:")
        print(f"      旧值: {change['old']}")
        print(f"      新值: {change['new']}")

    print(f"\n未变更字段 ({len(changes['unchanged'])}):")
    for field in changes['unchanged']:
        print(f"  = {field}")
```

### 2. 自动迁移脚本模板

```bash
#!/bin/bash
# migrate-template.sh - 迁移脚本模板

set -e  # 遇到错误立即退出

# 配置
SOURCE_VERSION="1.0.0"
TARGET_VERSION="2026.3.28"
BACKUP_DIR=".clawhub/backup_$(date +%Y%m%d_%H%M%S)"

echo "=== OpenClaw 配置迁移工具 ==="
echo "源版本: $SOURCE_VERSION"
echo "目标版本: $TARGET_VERSION"
echo ""

# Step 1: 备份
echo "[1/5] 创建备份..."
mkdir -p "$BACKUP_DIR"
cp -r .clawhub/* "$BACKUP_DIR/"
echo "✅ 备份完成: $BACKUP_DIR"

# Step 2: 验证环境
echo "[2/5] 验证环境..."
if [ ! -f "_meta.json" ]; then
    echo "❌ 错误: 未找到 _meta.json"
    exit 1
fi
echo "✅ 环境验证通过"

# Step 3: 执行迁移
echo "[3/5] 执行迁移..."
# 在这里添加具体的迁移逻辑
# 示例：更新 _meta.json
python3 << 'EOF'
import json
from pathlib import Path

# 读取配置
meta_path = Path("_meta.json")
with open(meta_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 执行迁移转换
# data['version'] = '2026.3.28'
# data['schemaVersion'] = '2026.3.28'

# 保存配置
with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("配置迁移完成")
EOF

echo "✅ 迁移完成"

# Step 4: 验证结果
echo "[4/5] 验证结果..."
python3 -m json.tool _meta.json > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ JSON 格式验证通过"
else
    echo "❌ JSON 格式验证失败，正在回滚..."
    cp -r "$BACKUP_DIR"/* .clawhub/
    exit 1
fi

# Step 5: 清理
echo "[5/5] 清理..."
echo "备份保留在: $BACKUP_DIR"
echo "如无问题，可手动删除"

echo ""
echo "=== 迁移成功完成 ==="
echo "建议运行: ./scripts/validate-config.sh"
```

### 3. 健康检查脚本

```bash
#!/bin/bash
# health-check.sh - 配置健康检查

echo "=== OpenClaw 配置健康检查 ==="

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查计数
PASS=0
FAIL=0
WARN=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✅${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}❌${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
    ((WARN++))
}

# 1. 文件存在性检查
echo -e "\n### 1. 文件存在性检查"
[ -f "_meta.json" ] && check_pass "_meta.json 存在" || check_fail "_meta.json 缺失"
[ -f "SKILL.md" ] && check_pass "SKILL.md 存在" || check_fail "SKILL.md 缺失"
[ -d ".clawhub" ] && check_pass ".clawhub 目录存在" || check_fail ".clawhub 目录缺失"

# 2. JSON 格式检查
echo -e "\n### 2. JSON 格式检查"
for file in _meta.json .clawhub/**/*.json; do
    if [ -f "$file" ]; then
        python3 -m json.tool "$file" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            check_pass "$file 格式正确"
        else
            check_fail "$file 格式错误"
        fi
    fi
done

# 3. 必需字段检查
echo -e "\n### 3. 必需字段检查"
python3 << 'EOF'
import json
import sys

try:
    with open('_meta.json', 'r') as f:
        data = json.load(f)

    required = ['name', 'version']
    missing = [field for field in required if field not in data]

    if missing:
        print(f"❌ 缺少必需字段: {missing}")
        sys.exit(1)
    else:
        print(f"✅ 必需字段完整")
        sys.exit(0)
except Exception as e:
    print(f"❌ 检查失败: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    ((PASS++))
else
    ((FAIL++))
fi

# 4. 版本一致性检查
echo -e "\n### 4. 版本一致性"
# 添加具体检查逻辑
check_warn "版本一致性检查未实现"

# 5. 权限检查
echo -e "\n### 5. 文件权限"
[ -r "_meta.json" ] && check_pass "_meta.json 可读" || check_fail "_meta.json 不可读"
[ -w "_meta.json" ] && check_pass "_meta.json 可写" || check_warn "_meta.json 不可写"

# 汇总
echo -e "\n=== 检查汇总 ==="
echo -e "通过: ${GREEN}$PASS${NC}"
echo -e "警告: ${YELLOW}$WARN${NC}"
echo -e "失败: ${RED}$FAIL${NC}"

if [ $FAIL -gt 0 ]; then
    echo -e "\n${RED}❌ 健康检查失败${NC}"
    exit 1
else
    echo -e "\n${GREEN}✅ 健康检查通过${NC}"
    exit 0
fi
```

---

## 最佳实践

### 1. 版本管理建议

- **使用语义化版本**（Semantic Versioning）：主版本.次版本.补丁
- **记录所有变更**：维护 CHANGELOG.md
- **渐进式升级**：避免跨多个主版本直接升级
- **测试先行**：先在测试环境验证

### 2. 备份策略

```bash
# 保留最近 5 个备份
ls -t .clawhub/backup_* | tail -n +6 | xargs rm -rf

# 自动备份脚本（添加到 crontab）
# 每天凌晨 2 点自动备份
# 0 2 * * * /path/to/backup-script.sh
```

### 3. 监控建议

- 迁移后监控系统日志
- 关注性能指标
- 设置告警阈值
- 定期验证配置完整性

---

## 故障排查

### 常见问题

#### 问题1：JSON 格式错误

```bash
# 错误信息
Error: Expecting property name enclosed in double quotes

# 解决方案
python3 -m json.tool _meta.json > _meta_fixed.json
mv _meta_fixed.json _meta.json
```

#### 问题2：字段类型不匹配

```bash
# 检查字段类型
python3 << 'EOF'
import json
with open('_meta.json', 'r') as f:
    data = json.load(f)
    print(f"version 类型: {type(data.get('version'))}")
    print(f"version 值: {data.get('version')}")
EOF
```

#### 问题3：权限问题

```bash
# 修复权限
chmod 644 _meta.json
chmod 755 .clawhub
```

---

## 获取帮助

- **文档**：查看项目 SKILL.md
- **问题反馈**：提交 Issue 到项目仓库
- **社区支持**：加入 OpenClaw 社区讨论

---

**最后更新**: 2026-03-31
**维护者**: OpenClaw 配置团队
**参考版本**: `openclaw/openclaw@v2026.3.28`
