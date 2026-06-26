---
name: openclaw-skill-manager
description: 管理 OpenClaw 技能安装、查询、更新和自定义空间。支持多空间架构，使用 CLI 查看技能。触发词：管理技能、安装skill、查询skill、更新skill、移动skill、添加skill空间、/skill
author: Claude
version: 3.1.0
tags: [skill, management, clawhub, installation, custom-space]
---

# Skill Manager

管理 OpenClaw 技能的多空间安装、查询、更新和自定义空间配置。

## 架构说明

### 技能空间层级

```
技能空间层级：
├── 系统内置: <openclaw>/skills              (bundled)
├── 全局:     ~/.openclaw/skills             (managed)
├── 主脑:     ~/.openclaw/workspace/skills   (workspace)
├── 专才:     ~/.openclaw/workspace-shared/skills (extra)
└── 自定义:   用户配置的路径                 (extra)
```

### Source 分类映射

| Source | 分类 | 路径 |
|--------|------|------|
| `openclaw-bundled` | 系统内置 | `~/openclaw/skills` |
| `openclaw-managed` | 全局 | `~/.openclaw/skills` |
| `openclaw-workspace` | 主脑 | `~/.openclaw/workspace/skills` |
| `openclaw-extra` | 扩展 | 专才 + 自定义空间 |

## 命令工作流

### Phase 1: 添加自定义技能空间

**输入**: 用户请求添加新的技能空间
**输出**: 配置更新结果

#### Step 1: 获取当前 Agent 配置
```bash
openclaw agents list
```

**解析 Workspace 路径：**
```bash
openclaw agents list | grep -A1 "Workspace:" | grep "Workspace:" | sed 's/.*Workspace: //' | sort | uniq
```

**向用户展示可选空间：**
```
检测到以下 Agent 工作空间：
1. 主脑空间: ~/.openclaw/workspace
2. 专才空间: ~/.openclaw/workspace-shared (code_expert, content_expert, stock_expert)

请输入要添加的技能空间路径：
（可直接输入序号 1/2，或输入自定义绝对路径）
```

#### Step 2: 用户输入处理
- **输入 1** → 路径=`~/.openclaw/workspace/skills`
- **输入 2** → 路径=`~/.openclaw/workspace-shared/skills`
- **输入其他路径** → 验证后添加
- **输入已存在路径** → 提示已存在，跳过

#### Step 3: 验证路径
```bash
# 检查路径是否存在
if [ ! -d "<用户输入路径>" ]; then
  echo "路径不存在，是否创建？(yes/no)"
  # 用户确认后创建
  mkdir -p "<用户输入路径>"
fi

# 检查是否已在配置中
openclaw config get skills.load.extraDirs | grep -q "<用户输入路径>" && echo "已存在，跳过"
```

#### Step 4: 用户确认
```
📝 即将添加技能空间：
   路径: /new/custom/path
   父目录: /new/custom

⚠️  确认添加？(yes/no):
```

#### Step 5: 更新配置
修改 `~/.openclaw/openclaw.json`：
```json
{
  "skills": {
    "load": {
      "extraDirs": [
        "/existing/path",
        "/new/custom/path"
      ],
      "watch": true,
      "watchDebounceMs": 250
    }
  }
}
```

#### Step 6: 重启 Gateway
```bash
openclaw gateway restart
```

#### Step 7: 验证
```bash
openclaw config get skills.load.extraDirs
openclaw skills list | grep -c "openclaw-extra"
```

#### Step 8: 返回结果
```
✅ 已添加自定义技能空间: /new/custom/path
🔄 Gateway 已重启
📦 该路径下的技能现在可通过 `openclaw skills list` 查看
```

---

### Phase 2: 安装技能

**输入**: 技能名称或地址、目标空间
**输出**: 安装结果报告

#### Step 1: 获取可用安装空间
```bash
openclaw config get skills.load.extraDirs
```

**分类显示：**
```
可用的安装目标空间：

[1] 全局空间      ~/.openclaw/skills
[2] 主脑空间      ~/.openclaw/workspace/skills      (main)
[3] 专才空间      ~/.openclaw/workspace-shared/skills (code_expert, content_expert, stock_expert)
[4] 自定义空间    /Users/liber/custom-skills

请选择安装目标 (输入序号 1-4):
```

#### Step 2: 用户输入技能名称
```
请输入要安装的技能名称：
（或输入 URL/本地路径进行手动安装）
```

#### Step 3: 解析安装源类型
- **纯名称** (如 `stock-market-pro`) → clawhub 安装
- **URL** (如 `https://...`) → 手动安装
- **本地路径** (如 `/path/to/skill`) → 手动安装

#### Step 4: 用户确认
```
📝 即将安装技能：
   名称: stock-market-pro
   方式: clawhub 安装
   目标: 专才空间 (~/.openclaw/workspace-shared/skills)

⚠️  确认安装？(yes/no):
```

#### Step 5: 执行安装

**方式 A - clawhub：**
```bash
clawhub install <skill-name> --dir <parent-dir-of-skills>
```

**方式 B - 手动：**
```bash
# 下载/复制到目标路径
if [[ "<source>" =~ ^https?:// ]]; then
  curl -L "<source>" | tar -xz -C "<target-skills-dir>/"
else
  cp -r "<source>" "<target-skills-dir>/<skill-name>"
fi

# 标记为手动安装
touch "<target-skills-dir>/<skill-name>/.manual-install"
```

#### Step 6: 验证安装
```bash
# 检查技能是否出现在列表中
openclaw skills list | grep "<skill-name>"

# 检查 SKILL.md 完整性
cat "<target-skills-dir>/<skill-name>/SKILL.md" | grep -E "^(name|description):"
```

#### Step 7: 返回结果

**成功：**
```
✅ 技能 <skill-name> 已安装到 <space> 空间
📦 来源: clawhub / 手动安装
📍 路径: <full-path>
```

**失败：**
```
❌ 安装失败: <错误信息>
🔧 可能原因：
   1. 网络连接问题
   2. 技能名称拼写错误
   3. 目录权限不足
💡 尝试: clawhub search <keyword> 确认技能名称
```

---

### Phase 3: 查询技能列表

**输入**: 查询参数（可选过滤）
**输出**: 格式化的技能清单

#### Step 1: 获取 CLI 输出
```bash
openclaw skills list 2>&1
```

**CLI 失败时的 fallback：**
```bash
# 如果 CLI 失败，使用备用方法
if ! openclaw skills list >/dev/null 2>&1; then
  echo "⚠️ CLI 不可用，使用备用扫描..."
  # 扫描配置中的 extraDirs
  for dir in $(openclaw config get skills.load.extraDirs | jq -r '.[]'); do
    ls -1 "$dir" 2>/dev/null
  done
fi
```

#### Step 2: 解析 CLI 输出

**提取技能信息：**
```bash
# 提取技能名称、状态、描述、来源
openclaw skills list 2>&1 | awk -F'│' '
NR > 3 && NF >= 5 {
  status = $2
  name = $3
  desc = $4
  source = $5
  
  # 清理空格
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", status)
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", name)
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", desc)
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", source)
  
  # 提取状态
  if (status ~ /✓/) state = "ready"
  else if (status ~ /△/) state = "needs_setup"
  else state = "unknown"
  
  # 提取来源分类
  if (source ~ /bundled/) category = "系统内置"
  else if (source ~ /managed/) category = "全局"
  else if (source ~ /workspace/) category = "主脑"
  else if (source ~ /extra/) category = "扩展"
  else category = "其他"
  
  # 提取描述前50字符
  desc_short = substr(desc, 1, 50)
  if (length(desc) > 50) desc_short = desc_short "..."
  
  print category "|" name "|" state "|" desc_short "|" source
}'
```

#### Step 3: 按分类统计
```bash
# 统计各分类数量
openclaw skills list 2>&1 | awk -F'│' '
NR > 3 && $5 ~ /bundled/ {bundled++}
NR > 3 && $5 ~ /managed/ {managed++}
NR > 3 && $5 ~ /workspace/ {workspace++}
NR > 3 && $5 ~ /extra/ {extra++}
END {
  print "系统内置:", bundled
  print "全局:", managed
  print "主脑:", workspace
  print "扩展:", extra
}'
```

#### Step 4: 格式化输出

**完整列表格式：**
```
## 技能清单

### 系统内置技能 (X个)

| 技能 | 状态 | 用途 |
|------|------|------|
| 🔐 1password | ✅ ready | 1Password CLI 设置使用 |
| 📝 apple-notes | ✅ ready | Apple Notes 管理 |
| ... | ... | ... |

### 全局技能 (X个)

| 技能 | 状态 | 用途 |
|------|------|------|
| 📦 ragflow | ✅ ready | RAG 操作客户端 |
| ... | ... | ... |

### 主脑技能 (X个) - main

| 技能 | 状态 | 用途 |
|------|------|------|
| 📦 darwin-skill | ✅ ready | Skill 自动优化 |
| ... | ... | ... |

### 扩展技能 (X个)

| 技能 | 状态 | 来源 | 用途 |
|------|------|------|------|
| 📦 stock-market-pro | ✅ ready | workspace-shared | 股票市场分析 |
| ... | ... | ... | ... |

**总计：X 个技能（Y 个就绪可用）**
```

**中文用途提取规则：**
1. 从 CLI 输出的 `Description` 列提取
2. 截取前 50 个字符或第一个句号/逗号前的内容
3. 转换为简洁中文描述（不超过 10 字）

---

### Phase 4: 更新技能

**输入**: 技能名称 或 `--all` 标志
**输出**: 更新结果报告

#### Step 1: 定位技能
```bash
openclaw skills list | grep "<skill-name>"
```

#### Step 2: 检查安装类型
```bash
# 查找技能路径
skill_path=$(openclaw skills list 2>&1 | awk -F'│' -v name="<skill-name>" '
$3 ~ name {print $5}' | head -1)

# 检查是否为手动安装
if [ -f "$skill_path/<skill-name>/.manual-install" ]; then
  echo "手动安装"
else
  echo "clawhub 安装"
fi
```

#### Step 3: 用户确认
```
📝 即将更新技能：
   名称: <skill-name>
   当前版本: <version>
   来源: clawhub / 手动安装

⚠️  确认更新？(yes/no):
```

#### Step 4: 执行更新

**clawhub：**
```bash
# 备份当前版本
cp -r "<skill-path>" "<skill-path>.backup.$(date +%Y%m%d%H%M%S)"

# 执行更新
clawhub update <skill-name> --dir <parent-dir-of-skill>
```

**手动安装：**
```
⚠️ 技能 <skill-name> 为手动安装，无法自动更新
💡 更新选项：
   1. 使用 `/skill update <name> --force` 强制重新下载
   2. 使用 `/skill install <new-url> --manual` 重新安装
   3. 手动删除后重新安装
```

#### Step 5: 返回结果
```
✅ 技能 <name> 已更新至最新版本
📦 来源: clawhub
📍 路径: <full-path>
```

---


### Phase 5: 移动技能

**输入**: 技能名称、目标空间
**输出**: 移动确认和结果

#### Step 1: 定位技能
```bash
# 获取技能当前路径
source_path=$(openclaw skills list 2>&1 | awk -F'│' -v name="<skill-name>" '
$3 ~ name {
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", $5)
  print $5
}' | head -1)
```

#### Step 2: 验证目标空间
```bash
# 检查目标空间是否在配置中
openclaw config get skills.load.extraDirs | grep -q "<target-path>" || echo "❌ 目标空间未配置"

# 检查是否有同名技能
ls "<target-path>/<skill-name>" 2>/dev/null && echo "⚠️  目标空间已存在同名技能"
```

#### Step 3: 用户确认
```
📝 即将移动技能：
   技能: <skill-name>
   从: <source-path>
   到: <target-path>

⚠️  移动后原位置将备份，确认移动？(yes/no):
```

#### Step 4: 执行移动
```bash
# 备份原位置
mv "<source-path>" "<source-path>.backup.$(date +%Y%m%d%H%M%S)"

# 复制到新位置
cp -r "<source-path>.backup.*" "<target-path>/<skill-name>"

# 验证
ls "<target-path>/<skill-name>/SKILL.md"
```

#### Step 5: 返回结果
```
✅ 技能 <name> 已移动到 <space> 空间
📍 新路径: <target-path>
🗂️  备份: <source-path>.backup.<timestamp>
```

---

## 安装路径映射

| 空间类型 | 配置路径 | 安装命令 |
|----------|----------|----------|
| 全局 | `~/.openclaw/skills` | `clawhub install X --dir ~/.openclaw/skills` |
| 主脑 | `~/.openclaw/workspace/skills` | `clawhub install X --dir ~/.openclaw/workspace/skills` |
| 专才 | `~/.openclaw/workspace-shared/skills` | `clawhub install X --dir ~/.openclaw/workspace-shared/skills` |
| 自定义 | 用户配置的路径 | `clawhub install X --dir <parent-dir-of-skills>` |

---

## 异常处理

### CLI 命令失败
**触发**: `openclaw skills list` 执行失败或超时
**检测**: 命令返回非零退出码
**处理**:
```bash
# Fallback 到配置扫描
for dir in $(openclaw config get skills.load.extraDirs 2>/dev/null | jq -r '.[]' 2>/dev/null); do
  if [ -d "$dir" ]; then
    ls -1 "$dir" 2>/dev/null | while read skill; do
      echo "│ unknown │ $skill │ (fallback scan) │ openclaw-extra │"
    done
  fi
done
```

### 空间未配置
**触发**: 用户尝试安装到未配置的空间
**处理**:
```
❌ 空间 <path> 未在配置中
💡 请先添加该空间：/skill add-space
   或选择已配置的空间安装
```

### 手动安装技能更新
**触发**: 用户尝试更新手动安装的技能
**处理**:
```
⚠️ 技能 <name> 为手动安装，无法自动更新
📦 原始来源: <url-or-path>
💡 更新选项：
   1. 使用 `/skill update <name> --force` 强制重新下载
   2. 使用 `/skill install <new-url> --manual` 重新安装
   3. 手动删除后重新安装
```

### 路径不存在
**触发**: 添加空间时路径不存在
**处理**:
```
⚠️ 路径 <path> 不存在
💡 是否创建该目录？(yes/no)
```

---

## 注意事项

- 添加自定义空间后需要重启 Gateway 生效
- 手动安装的技能不会自动更新（创建 `.manual-install` 标记）
- 移动技能前会自动备份原位置
- 关键操作前均有用户确认提示
- CLI 失败时有 fallback 扫描机制

---

## 测试验证

### 测试 Prompt 1: 添加自定义空间
```
添加一个新的技能空间 /Users/liber/custom-skills
```
**期望**: 提示确认 → 更新配置 → 重启 Gateway → 验证

### 测试 Prompt 2: 安装技能到指定空间
```
安装 stock-market-pro 到专才空间
```
**期望**: 显示可用空间 → 用户选择 → 确认 → clawhub 安装 → 验证

### 测试 Prompt 3: 查看技能列表
```
/skill list
```
**期望**: 按分类显示所有技能，包含状态、来源、用途

### 测试 Prompt 4: CLI 失败 fallback
```
当 openclaw skills list 失败时，使用备用扫描
```
**期望**: 检测到 CLI 失败 → 扫描 extraDirs → 显示结果
