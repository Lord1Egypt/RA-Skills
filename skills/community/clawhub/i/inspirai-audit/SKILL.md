---
name: inspirai-audit
description: "Skill 重叠分析工具 - 检测已安装 skills/commands 的功能重复，辅助精简配置。Triggers: 'skill 审计', '功能重叠', '重复检测', 'skill audit', 'skill scan', '精简配置'."
version: 1.0.0
license: MIT
---

# inspirai-audit - Skill 重叠分析工具

检测已安装 skills/commands 的功能重复，辅助精简配置。包含三个核心功能：扫描分析、状态查看、重叠处理。

---

## 一、扫描分析 (scan)

全量扫描已安装的 skills/commands，分析功能重叠并生成报告。

### 使用方式

```
audit scan
audit scan --quick        # 仅标签分析，跳过 AI 深度对比
audit scan --focus deploy  # 只分析与 deploy 相关的重叠
```

### 参数

- `--quick` — 仅执行标签分析，不做 AI 深度对比（速度快）
- `--focus <keyword>` — 聚焦分析某个功能领域的重叠
- `--include-project` — 同时扫描项目级 `.claude/commands/`（默认只扫描用户级）

### 执行步骤

#### Step 1: 收集所有已安装 Skill

扫描以下路径，收集所有 skill 的元信息：

```bash
# 1. 用户级 commands
COMMANDS_DIR="$HOME/.claude/commands"
find "$COMMANDS_DIR" -name "*.md" -not -path "*/.disabled/*" | while read f; do
    echo "command:$(basename "$f" .md):$f"
done

# 2. 子目录 commands (如 gh/fix-issue.md → /gh:fix-issue)
find "$COMMANDS_DIR" -mindepth 2 -name "*.md" | while read f; do
    DIR=$(basename "$(dirname "$f")")
    NAME=$(basename "$f" .md)
    echo "command:${DIR}:${NAME}:$f"
done

# 3. 已安装 plugins
PLUGINS_FILE="$HOME/.claude/plugins/installed_plugins.json"
# 解析 JSON 获取每个插件的 installPath
# 读取每个插件下 skills/*/SKILL.md
```

为每个 skill 建立信息记录：
```
{
  "id": "command:deploy" | "plugin:deploy:run",
  "type": "command" | "plugin-skill",
  "name": "deploy",
  "source": "~/.claude/commands/deploy.md" | "deploy@skill-market",
  "description": "...",
  "content_summary": "前200字摘要"
}
```

#### Step 2: 功能标签提取

对每个 skill 提取功能标签：

**标签维度：**

| 维度 | 标签示例 |
|------|---------|
| 领域 | deploy, review, test, format, refactor, scaffold, ui, docs, git, security, cloud, wechat, api |
| 动作 | generate, analyze, fix, create, monitor, scan, build, install, migrate |
| 技术栈 | frontend, backend, k8s, docker, node, python, react, aliyun |

**提取规则：**

1. **文件名/skill名** — 直接作为领域标签
2. **description 字段** — 提取关键词匹配标签库
3. **内容关键词** — 扫描正文，匹配预定义标签词典：

```
标签词典 = {
  "deploy": ["部署", "deploy", "release", "rollout", "发布"],
  "review": ["review", "审查", "code review", "PR"],
  "test": ["test", "测试", "spec", "assert", "coverage"],
  "format": ["format", "格式化", "lint", "prettier", "eslint"],
  "refactor": ["refactor", "重构", "restructure", "cleanup"],
  "ui": ["UI", "界面", "component", "组件", "frontend", "style", "CSS"],
  "generate": ["generate", "生成", "create", "scaffold", "template"],
  "security": ["security", "安全", "vulnerability", "漏洞", "scan"],
  "docs": ["documentation", "文档", "README", "注释", "comment"],
  "git": ["git", "commit", "branch", "merge", "PR", "pull request"],
  ...
}
```

4. 每个 skill 最终得到 3-8 个标签

#### Step 3: 重叠候选检测

对所有 skill 两两计算标签交集率：

```
overlap_score(A, B) = |tags(A) ∩ tags(B)| / min(|tags(A)|, |tags(B)|)
```

分级：
- `>= 0.6` → **高疑似重叠** → 进入 Step 4
- `0.3 ~ 0.6` → **中度疑似** → 标记在报告中但不深度分析
- `< 0.3` → 无关，跳过

将高疑似的 pair 聚合为**重叠组**（连通分量）：
- 如果 A-B 重叠且 B-C 重叠，合并为 {A, B, C} 一组

#### Step 4: AI 深度对比（非 --quick 模式）

对每个高疑似重叠组，将所有成员的 SKILL.md 内容一起分析：

**分析提示词：**

```
请分析以下 skills 的功能重叠情况：

[Skill A - {name}]
{SKILL.md 内容摘要，前500字}

[Skill B - {name}]
{SKILL.md 内容摘要，前500字}

请回答：
1. 功能重叠度（高/中/低/无）
2. 重叠的具体功能点
3. 各 skill 的独有能力
4. 推荐保留哪个（基于完整度和覆盖面）
5. 置信度（高/中/低）
```

#### Step 5: 生成报告

输出格式：

```
╔══════════════════════════════════════════════════╗
║  Skill Audit Report                             ║
╠══════════════════════════════════════════════════╣
║  扫描: {N} commands + {M} plugins ({T} skills)  ║
║  发现: {G} 组功能重叠                            ║
╚══════════════════════════════════════════════════╝

━━━ 重叠组 #1: {领域} (置信度: {高/中/低}) ━━━━━━
  A) {skill_id}  — {一句话描述}
  B) {skill_id}  — {一句话描述}

  重叠: {重叠功能点}
  A 独有: {独有能力}
  B 独有: {独有能力}

  → 建议: {保留/禁用建议}

━━━ 重叠组 #2: ... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ...
```

#### Step 6: 缓存结果

将扫描结果写入缓存文件：

```bash
CACHE_FILE="$HOME/.claude/audit-cache.json"
```

```json
{
  "lastScan": "2026-01-24T12:00:00Z",
  "skillCount": 42,
  "overlapGroups": [
    {
      "id": "group-1",
      "domain": "deploy",
      "confidence": "high",
      "members": ["command:deploy", "plugin:deploy:run"],
      "recommendation": "disable command:deploy",
      "resolved": false
    }
  ],
  "disabled": []
}
```

### 扫描输出示例

```
扫描完成: 28 commands + 11 plugins (42 skills)

发现 4 组功能重叠:

#1 部署 (高): /deploy vs /deploy:run → 建议禁用 command
#2 前端 (中): /make-it-pretty vs frontend-design vs ui-ux-pro-max
#3 代码审查 (中): /review vs superpowers:requesting-code-review
#4 规范设计 (低): /spec vs kiro:spec

运行 audit resolve 处理这些重叠。
```

### 扫描注意事项

- 标签提取基于关键词匹配，可能存在误判，以 AI 深度对比结果为准
- `--quick` 模式不消耗额外 token，适合快速预览
- 扫描不会修改任何文件，完全只读
- 缓存文件用于 status 和增量对比，可安全删除

---

## 二、状态查看 (status)

快速查看当前 skills 的安装状态、禁用列表和上次扫描结果。

### 使用方式

```
audit status
audit status --verbose    # 详细展示每个 skill 的状态
```

### 参数

- `--verbose` — 列出所有已安装 skill 及其状态（启用/禁用）

### 执行步骤

#### Step 1: 统计已安装数量

```bash
COMMANDS_DIR="$HOME/.claude/commands"
DISABLED_DIR="$COMMANDS_DIR/.disabled"
PLUGINS_FILE="$HOME/.claude/plugins/installed_plugins.json"
CACHE_FILE="$HOME/.claude/audit-cache.json"

# 统计 commands
ACTIVE_COMMANDS=$(find "$COMMANDS_DIR" -maxdepth 1 -name "*.md" | wc -l | tr -d ' ')
SUB_COMMANDS=$(find "$COMMANDS_DIR" -mindepth 2 -name "*.md" -not -path "*/.disabled/*" | wc -l | tr -d ' ')
DISABLED_COMMANDS=0
if [ -d "$DISABLED_DIR" ]; then
    DISABLED_COMMANDS=$(find "$DISABLED_DIR" -name "*.md" | wc -l | tr -d ' ')
fi

# 统计 plugins
ACTIVE_PLUGINS=$(jq '.plugins | keys | length' "$PLUGINS_FILE" 2>/dev/null || echo 0)
```

#### Step 2: 读取扫描缓存

```bash
if [ -f "$CACHE_FILE" ]; then
    LAST_SCAN=$(jq -r '.lastScan' "$CACHE_FILE")
    TOTAL_GROUPS=$(jq '.overlapGroups | length' "$CACHE_FILE")
    RESOLVED=$(jq '[.overlapGroups[] | select(.resolved == true)] | length' "$CACHE_FILE")
    PENDING=$((TOTAL_GROUPS - RESOLVED))
    DISABLED_LIST=$(jq -r '.disabled[]' "$CACHE_FILE" 2>/dev/null)
else
    LAST_SCAN="从未扫描"
    TOTAL_GROUPS=0
    RESOLVED=0
    PENDING=0
fi
```

#### Step 3: 输出状态

**基础模式：**

```
Skill Audit Status
──────────────────────────────────
已安装:  {ACTIVE_COMMANDS} commands + {SUB_COMMANDS} sub-commands + {ACTIVE_PLUGINS} plugins
已禁用:  {DISABLED_COMMANDS} commands
上次扫描: {LAST_SCAN}
重叠组:  {TOTAL_GROUPS} 组 (已处理 {RESOLVED}, 待处理 {PENDING})

禁用列表:
  - deploy.md (重叠: /deploy:run 完全覆盖)
  - make-it-pretty.md (重叠: frontend-design 覆盖)
```

**--verbose 模式（额外展示）：**

```
所有 Skills:
  Commands:
    [启用] /commit — Smart Git Commit
    [启用] /review — Code Review
    [禁用] /deploy — 基础部署 (被 /deploy:run 替代)
    [启用] /test — Smart Test Runner
    ...

  Plugins:
    [启用] superpowers@claude-plugins-official (15 skills)
    [启用] frontend-design@claude-plugins-official (1 skill)
    [启用] feature-dev@claude-plugins-official (3 skills)
    ...

  待处理重叠:
    #3 代码审查: /review vs superpowers:requesting-code-review
```

### 自动提醒逻辑

当用户执行 `plugin install` 后，如果检测到新安装的 plugin 在缓存中有潜在重叠记录，输出提醒：

```
[audit] 新安装的 {plugin_name} 可能与已有 skill 功能重叠
[audit] 运行 audit scan 查看详细分析
```

此提醒逻辑在 scan 的描述中声明为 agent 行为建议（非强制执行）。

### 状态查看注意事项

- 无缓存文件时提示先运行 `audit scan`
- 状态信息完全来自文件系统和缓存，不消耗 token
- `--verbose` 模式可能输出较长，适合排查具体 skill 状态

---

## 三、处理功能重叠 (resolve)

基于扫描分析的结果，交互式引导用户处理每组重叠。

### 使用方式

```
audit resolve              # 处理所有未解决的重叠组
audit resolve --group 2    # 只处理第 2 组
audit resolve --undo       # 恢复上次禁用的 skills
```

### 参数

- `--group <n>` — 只处理指定编号的重叠组
- `--undo` — 恢复所有被禁用的 skills
- `--dry-run` — 预览将要执行的操作，不实际执行

### 前置检查

```bash
CACHE_FILE="$HOME/.claude/audit-cache.json"
if [ ! -f "$CACHE_FILE" ]; then
    echo "[INFO] 未找到扫描结果，请先运行 audit scan"
    exit 0
fi

# 检查是否有未解决的重叠组
UNRESOLVED=$(jq '[.overlapGroups[] | select(.resolved == false)] | length' "$CACHE_FILE")
if [ "$UNRESOLVED" -eq 0 ]; then
    echo "[INFO] 所有重叠组已处理完毕，无需操作"
    exit 0
fi
```

### 执行步骤

#### Step 1: 加载扫描结果

从 `~/.claude/audit-cache.json` 读取未处理的重叠组。

#### Step 2: 逐组展示并等待决策

对每个未解决的重叠组，展示详情并让用户选择：

```
━━━ 重叠组 #{n}: {领域} (置信度: {level}) ━━━━━━
  A) {skill_id}  — {描述}
  B) {skill_id}  — {描述}

  重叠: {重叠点}
  建议: {recommendation}
```

用户选项：
1. **保留 A，禁用 B** — 按建议操作
2. **保留 B，禁用 A** — 反向选择
3. **全部保留** — 标记为已处理但不禁用
4. **跳过** — 暂不处理

#### Step 3: 收集所有决策后确认

所有组处理完毕后，汇总展示即将执行的操作：

```
即将执行以下操作：

  禁用: /deploy (command) → 移至 .disabled/
  禁用: /make-it-pretty (command) → 移至 .disabled/
  保留: frontend-design, ui-ux-pro-max, /review, ...

确认执行？(Y/n)
```

#### Step 4: 执行禁用操作

**禁用 command：**
```bash
DISABLED_DIR="$HOME/.claude/commands/.disabled"
mkdir -p "$DISABLED_DIR"

# 移动文件到 .disabled 目录
mv "$HOME/.claude/commands/deploy.md" "$DISABLED_DIR/deploy.md"
echo "[OK] 已禁用 /deploy → .disabled/deploy.md"
```

**禁用 plugin skill：**
```bash
# 在 installed_plugins.json 中添加 disabled 标记
# 或者更简单：在 audit-cache.json 中记录禁用状态
# Claude Code 加载时检查此标记
PLUGINS_FILE="$HOME/.claude/plugins/installed_plugins.json"

# 方案：通过移除 installed_plugins.json 中的条目实现
# 但保留在 audit-cache.json 中以便恢复
jq ".plugins.\"${PLUGIN_KEY}\" += [{\"disabled\": true}]" "$PLUGINS_FILE" > tmp && mv tmp "$PLUGINS_FILE"
```

**注意：** 对于 plugin 的禁用，优先使用 `claude plugin uninstall` 命令（如果可用），并在 audit-cache.json 中记录以便恢复。

#### Step 5: 更新缓存

```bash
# 标记已处理的组
jq ".overlapGroups[$GROUP_INDEX].resolved = true" "$CACHE_FILE" > tmp && mv tmp "$CACHE_FILE"

# 记录禁用的 skills（用于 undo）
jq ".disabled += [\"$SKILL_ID\"]" "$CACHE_FILE" > tmp && mv tmp "$CACHE_FILE"
```

### --undo 恢复流程

```bash
if [ "$MODE" = "undo" ]; then
    DISABLED_DIR="$HOME/.claude/commands/.disabled"

    # 恢复所有 .disabled 目录中的 commands
    if [ -d "$DISABLED_DIR" ]; then
        for f in "$DISABLED_DIR"/*.md; do
            [ -f "$f" ] || continue
            mv "$f" "$HOME/.claude/commands/$(basename "$f")"
            echo "[OK] 已恢复 /$(basename "$f" .md)"
        done
    fi

    # 恢复 plugins（从 cache 记录中重新安装）
    DISABLED_PLUGINS=$(jq -r '.disabled[] | select(startswith("plugin:"))' "$CACHE_FILE")
    for p in $DISABLED_PLUGINS; do
        echo "[INFO] 请手动运行: claude plugin install ${p#plugin:}"
    done

    # 清空禁用记录
    jq '.disabled = [] | .overlapGroups[].resolved = false' "$CACHE_FILE" > tmp && mv tmp "$CACHE_FILE"
    echo "[OK] 所有禁用已恢复"
fi
```

### 安全规则

- **确认前不执行** — 所有操作在用户最终确认后才批量执行
- **可恢复** — command 只是移动到 .disabled/，随时可用 --undo 恢复
- **不删除** — 永远不 rm 任何文件，只做移动
- **不碰项目级** — 只处理 `~/.claude/commands/`，不碰项目 `.claude/commands/`
- **plugin 谨慎处理** — plugin 禁用记录在 cache 中，不直接修改 installed_plugins.json 结构

### 处理重叠注意事项

- 首次使用前必须先运行 `audit scan`
- `--dry-run` 可预览操作效果
- 禁用的 command 在 `.disabled/` 目录，不会被 Claude Code 加载
- 恢复 plugin 可能需要手动 `claude plugin install`
