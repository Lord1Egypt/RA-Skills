---
name: git-daily-report
description: 发送 image-tool (所有 remote 分支) 和 voc 项目 (dev 分支) 的每日 Git 变化报告 + 代码审查（安全 + 通用）（前一天）。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["git","curl","rg"]}}}
---

# Git 日报技能

每天自动发送 image-tool 和 voc 项目前一天的 Git 提交记录。
- image-tool: 所有 remote 分支
- voc-frontend / voc-backend: 仅 dev 分支

---

## 📋 项目路径

| 项目 | 路径 | 分支 |
|------|------|------|
| image-tool | `/home/admin/ua-image/code/UA-EC-Image-Tool` | 所有 remote 分支 |
| voc-frontend | `/home/admin/voc/code/UA-VOC-Frontend` | dev |
| voc-backend | `/home/admin/voc/code/UA-VOC-Backend` | dev |

---

## 🔧 获取 Git 变化

```bash
# 获取指定日期的提交（前一天）
TARGET_DATE="2026-03-22"
START_DATE="${TARGET_DATE} 00:00:00"
END_DATE="${TARGET_DATE} 23:59:59"

cd /path/to/repo

# image-tool: 获取所有 remote 分支
REMOTE_BRANCHES=$(git branch -r | grep -v '\->' | sed 's/^[[:space:]]*//')
for branch in $REMOTE_BRANCHES; do
    echo "📍 $branch:"
    git log --since="$START_DATE" --until="$END_DATE" --oneline --no-decorate "$branch"
done

# voc 项目：仅获取 dev 分支
echo "📍 origin/dev:"
git log --since="$START_DATE" --until="$END_DATE" --oneline --no-decorate "origin/dev"
```

---

## 🔍 代码审查

### 1️⃣ 安全审查

```bash
# 获取变更的文件列表
CHANGED_FILES=$(git diff --name-only "origin/main~1" "origin/main")

for file in $CHANGED_FILES; do
    # 1. 检查硬编码密码/密钥
    rg -n "(password|passwd|pwd|secret|api_key|apikey|token|credential)\s*[=:]\s*[\"'][^\"']+[\"']" "$file"
    
    # 2. 检查硬编码 IP/URL
    rg -n "(https?://|ftp://)[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" "$file"
    
    # 3. 检查 SQL 拼接风险
    rg -n "(execute|query|cursor\.execute)\s*\(\s*[\"'].*\+.*[\"']" "$file"
    
    # 4. 检查 eval/exec 危险函数
    rg -n "\b(eval|exec|system|os\.system|subprocess\.call)\s*\(" "$file"
    
    # 5. 检查调试代码残留
    rg -n "(console\.log|debugger|print\s*\(|logging\.debug)" "$file"
    
    # 6. 检查 TODO/FIXME 标记
    rg -n "(TODO|FIXME|XXX|HACK):" "$file"
done
```

**安全检查项：**

| 风险类型 | 检查内容 | 严重程度 |
|---------|---------|---------|
| 🔴 高危 | 硬编码密码/API 密钥/Token | 严重 |
| 🔴 高危 | SQL 注入风险（字符串拼接） | 严重 |
| 🟡 中危 | eval/exec/system 危险函数 | 中等 |
| 🟡 中危 | 硬编码内网 IP/URL | 中等 |
| 🟢 低危 | console.log/debugger 调试代码 | 轻微 |
| 🟢 低危 | TODO/FIXME 技术债务 | 轻微 |

---

### 2️⃣ 通用 Code Review

```bash
for file in $CHANGED_FILES; do
    # 1. 检查长函数 (>50 行)
    # 2. 检查大文件 (>500 行)
    # 3. 检查重复代码模式
    # 4. 检查命名规范 (驼峰/下划线)
    # 5. 检查注释完整性
    # 6. 检查错误处理
    # 7. 检查边界条件
    
    # 示例：检查空 catch 块
    rg -n "catch\s*\(\s*\w+\s*\)\s*\{\s*\}" "$file"
    
    # 示例：检查魔法数字
    rg -n "[^0-9][0-9]{4,}[^0-9]" "$file" | grep -v "//"
    
    # 示例：检查 var 使用 (JS)
    rg -n "\bvar\s+\w+\s*=" "$file"
    
    # 示例：检查缺少默认值
    rg -n "process\.env\.[A-Z_]+\s*[^|]" "$file"
done
```

**通用审查项：**

| 类别 | 检查内容 | 建议 |
|-----|---------|------|
| 📐 代码结构 | 函数过长 (>50 行) | 拆分函数 |
| 📐 代码结构 | 文件过大 (>500 行) | 模块化拆分 |
| 📐 代码结构 | 嵌套过深 (>4 层) | 提前返回/卫语句 |
| 🏷️ 命名规范 | 变量/函数命名不清晰 | 使用语义化命名 |
| 🏷️ 命名规范 | 魔法数字 | 提取为常量 |
| 📝 注释 | 缺少函数/类注释 | 添加文档注释 |
| 📝 注释 | 注释与代码不一致 | 更新或删除注释 |
| ⚠️ 错误处理 | 空 catch 块 | 添加日志或处理 |
| ⚠️ 错误处理 | 缺少边界检查 | 添加验证 |
| ♻️ 代码复用 | 重复代码 | 提取公共函数 |
| 🔧 最佳实践 | 使用 var 而非 let/const | 使用块级作用域 |
| 🔧 最佳实践 | 硬编码配置 | 使用环境变量/配置 |

---

## 📤 发送 DingTalk 消息

使用 `message` 工具发送：

```json
{
  "action": "send",
  "channel": "dingtalk",
  "target": "1923216025-1426160278",
  "message": "📊 **Git 日报 - 2026-03-22**\n\n📁 **image-tool**:\n  📍 origin/main:\n    - abc123 修复登录问题\n\n📁 **voc-frontend**:\n  📍 origin/main:\n    - 无更新\n\n📁 **voc-backend**:\n  📍 origin/main:\n    - ghi789 优化查询性能"
}
```

---

## ⏰ 定时任务配置

使用 cron 工具设置每天 10:00 执行：

```json
{
  "action": "add",
  "job": {
    "name": "git-daily-report",
    "schedule": {
      "kind": "cron",
      "expr": "0 10 * * *",
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "你是一个 Git 日报助手。请执行以下任务：\n1. 获取昨天的日期（格式：YYYY-MM-DD）\n2. 检查以下仓库的 Git 提交记录：\n   - /home/admin/ua-image/code/UA-EC-Image-Tool (所有 remote 分支)\n   - /home/admin/voc/code/UA-VOC-Frontend (仅 dev 分支)\n   - /home/admin/voc/code/UA-VOC-Backend (仅 dev 分支)\n3. 对 image-tool，先获取所有 remote 分支列表 (git branch -r)，然后遍历每个分支获取提交；对 voc 项目，直接获取 origin/dev 分支的提交\n4. 获取每个项目的变更文件列表及改动统计 (git diff --stat, git diff --numstat)\n5. 对有代码变更的项目，进行代码审查：\n   - 安全审查：硬编码密码、SQL 注入、危险函数、调试代码等\n   - 通用 Code Review：代码结构、命名规范、注释、错误处理、最佳实践等\n6. 生成格式化的报告并通过 DingTalk 发送给用户 (target: 1923216025-1426160278)\n\n报告格式要求：\n- 每个项目列出提交信息和变更文件 (+x -y)\n- 代码审查分【安全审查】和【Code Review】两部分\n- 风险等级标注 (🔴🟡🟢)\n- 汇总风险和改进建议",
      "deliver": true,
      "channel": "dingtalk",
      "to": "1923216025-1426160278"
    }
  }
}
```

---

## 💬 用户交互

### 设置 Git 日报

**用户**: 每天早上 10 点发送 git 日报

**AI 操作**:
1. 确认当前时间和时区
2. 调用 cron 工具创建定时任务
3. 回复确认信息

**AI 回复**: `✅ 已设置 Git 日报，每天 10:00 发送 image-tool 和 voc 项目所有 remote 分支的昨日提交记录~`

### 查询 Git 日报状态

**用户**: git 日报设置了吗？

**AI 操作**:
1. 调用 cron 工具 `action: "list"` 查询任务

**AI 回复**:
```
📋 Git 日报状态：

🔄 git-daily-report - 每天 10:00

说"取消 git 日报"可删除~
```

### 取消 Git 日报

**用户**: 取消 git 日报

**AI 操作**:
1. 调用 cron 工具 `action: "list"` 找到任务 ID
2. 调用 cron 工具 `action: "remove"` 删除任务

**AI 回复**: `✅ 已取消 Git 日报任务`

---

## 📝 报告格式模板

```
📊 **Git 日报 - {日期}**

📁 **image-tool** (origin/main):
  📝 提交：abc123 修复登录问题
  📄 变更文件 (2):
    - src/login.js (+15 -3)
    - src/api.js (+8 -1)

📁 **voc-frontend** (origin/dev):
  📝 提交：def456 新增用户组件
  📄 变更文件 (5):
    - src/components/UserForm.vue (新增)
    - src/views/UserView.vue (+120 -45)
    - src/router/index.ts (+25 -2)
    - src/types/user.ts (+10 -0)
    - src/api/user.js (+30 -5)

📁 **voc-backend** (origin/dev):
  📝 提交：ghi789 优化查询性能
  📄 变更文件 (3):
    - routes/user.js (+45 -12)
    - services/db.js (+20 -8)
    - utils/validator.js (+15 -3)

🔍 **代码审查**:

📁 **image-tool**:
变更文件：src/login.js, src/api.js

【安全审查】
- ✅ 未发现硬编码密码/密钥
- ✅ 未发现 SQL 注入风险
- ⚠️ src/login.js:15 发现 console.log 调试代码

【Code Review】
- ✅ 函数长度合理
- ✅ 命名规范清晰
- 💡 建议：提取魔法数字为常量

---

📁 **voc-frontend**:
变更文件：UserForm.vue, TestView.vue, router/index.ts, comment.ts, CommentView.vue

【安全审查】
- ✅ 未发现硬编码密码/密钥
- ✅ 未发现 SQL 注入风险
- ⚠️ TestView.vue:22 发现 console.log 调试代码

【Code Review】
- ⚠️ TestView.vue: 函数过长 (176 行)，建议拆分
- ⚠️ TestForm.vue: 硬编码测试数据，建议移至 mock 文件
- 💡 建议：添加类型定义和注释

---

📁 **voc-backend**:
变更文件：11 个 Java 文件

【安全审查】
- ✅ 已清理多处 System.out.println 调试代码 👍
- ✅ 未发现硬编码密码/密钥
- ✅ 未发现 SQL 注入风险
- ✅ 未发现危险函数调用

【Code Review】
- ✅ 代码结构清晰
- ✅ 命名规范良好
- 💡 建议：添加单元测试

---

🚨 **风险汇总**:
- 🔴 高危：0 处
- 🟡 中危：2 处 (函数过长、测试数据硬编码)
- 🟢 低危：1 处 (console.log)

📈 **改动统计**:
- 总文件数：18
- 新增行数：+253
- 删除行数：-59

💡 **改进建议**:
1. 移除 TestView.vue 中的 console.log
2. 拆分 TestView.vue 中的长函数
3. 将测试数据移至 mock 文件

_Generated at {时间}_
```

---

## ⚠️ 注意事项

1. **时区**: 使用 `Asia/Shanghai` (GMT+8)
2. **日期计算**: 报告的是**前一天**的提交（例如 23 号早上发 22 号的）
3. **分支覆盖**: 
   - image-tool: 所有 remote 分支 (origin/*)
   - voc-frontend / voc-backend: 仅 dev 分支 (origin/dev)
4. **无更新处理**: 如果项目/分支没有提交，显示「无更新」
5. **错误处理**: 如果仓库不存在或 git 命令失败，在报告中注明
6. **代码审查**:
   - 分【安全审查】和【Code Review】两部分
   - 仅对有代码变更的项目进行审查
   - 使用 `git diff --name-only` 获取变更文件列表
   - 优先报告🔴高危问题（密码泄露、SQL 注入等）
   - 发现高危问题时，在报告开头添加🚨警告提示
7. **通用 Code Review 重点**:
   - 代码结构：函数长度、文件大小、嵌套深度
   - 命名规范：语义化命名、避免魔法数字
   - 注释文档：函数/类注释、注释与代码一致性
   - 错误处理：空 catch 块、边界检查
   - 最佳实践：var vs let/const、环境变量配置
8. **依赖工具**: 需要安装 `ripgrep (rg)` 进行代码搜索
