---
name: github-to-clawhub
description: >
  将 GitHub 开源项目转化为 OpenClaw skill 并发布到 clawhub 的完整流程助手。
  当用户说"把这个 GitHub 项目做成 skill"、"把 XX 发布到 clawhub"、"把这个项目封装成 skill"、
  "把 GitHub 链接转成 skill 上传"、"GitHub 转 skill"等类似需求时触发。
  支持从 GitHub URL 出发，自动完成：README 分析 → clawhub 查重 → SKILL.md 撰写 → 目录创建 → clawhub 发布。
author: antonia-sz
version: 1.0.0
---

# GitHub → ClawHub 一键转化发布

把任意 GitHub 开源项目转化为 OpenClaw skill，发布到 clawhub.com。

---

## 前置要求

| 条件 | 说明 |
|------|------|
| **GitHub URL** | 目标项目的 GitHub 链接 |
| **clawhub token** | 格式：`clh_xxx`，在 clawhub.com → Profile → API Keys 获取 |
| **exec 权限** | OpenClaw 需要能执行 shell 命令（本地部署默认有） |

如果用户还没提供 token，**先询问 token，再继续**。

---

## 执行流程

### Step 1：读取原项目信息

```
web_fetch https://raw.githubusercontent.com/{owner}/{repo}/main/README.md
```

提取以下信息：
- 项目的核心功能（一句话）
- 技术路径（调 API / 本地计算 / 多 Agent / 纯提示词）
- 是否依赖外部服务、本地 GPU、特殊硬件
- License 类型（MIT / Apache / GPL 等）

**排除标准**（遇到这些直接告知用户不适合做 skill）：
- 需要本地 GPU / 大 VRAM
- 纯前端/移动端 UI 项目，无 API 可调
- 需要复杂本地服务部署才能运行
- 涉及敏感/违规内容

### Step 2：clawhub 查重

```
knot_skills search "{关键词1} {关键词2}"
```

搜索 2-3 次，覆盖不同角度的关键词。

判断标准：
- **完全重复**（功能完全相同）→ 告知用户，询问是否换 slug 继续，或放弃
- **部分重叠**（有相似但不完全相同）→ 说明差异，继续发布
- **空白地带**（无相似 skill）→ 直接继续

### Step 3：确定 skill 元信息

与用户确认（如果未提供）：
- `slug`：URL 友好名称，全小写 + 连字符，如 `opinion-analyzer`
- `displayName`：展示名称，如 `Opinion Analyzer — 多视角舆情分析助手`
- `tags`：逗号分隔，如 `analysis,sentiment,research`

**Slug 命名规则：**
- 全小写 + 连字符，无空格
- 不能和已有 slug 完全重复（Step 2 查重时会发现）
- 描述性词汇优先（`jd-interview-prep` 比 `interview` 好）

### Step 4：撰写 SKILL.md

这是核心步骤，决定 skill 质量。

**SKILL.md 结构：**

```markdown
---
name: {slug}
description: >
  {触发场景描述，包含5-10个触发词，这决定了 AI 什么时候加载这个 skill}
author: {作者}
version: 1.0.0
---

# {displayName}

灵感来源：[{原项目名}]({GitHub URL}) ⭐ {star 数}

{一句话核心价值}

---

## 使用方式
{2-3 个调用示例}

---

## 执行流程
{分步骤，具体到"做什么、怎么做"}

---

## 输出格式
{交付物的结构模板}

---

## 注意事项
{边界条件、限制}
```

**撰写原则：**
1. `description` 触发词要够多够准，这是 skill 被激活的唯一入口
2. 执行流程具体到操作层面，不能写"帮你分析"这种废话
3. 输出格式给出模板，AI 不会自己发明格式
4. **不是翻译 README**，是把原项目逻辑转化为 AI 行为规范

### Step 5：创建本地文件

```bash
SKILL_DIR="/root/.openclaw/workspace/skills/SKILL-{slug}"
mkdir -p "$SKILL_DIR"
# 写入 SKILL.md
```

如果原项目有实用脚本/配置文件需要随 skill 分发，也放入此目录。

### Step 6：发布到 clawhub

```bash
CLAWHUB_TOKEN={token} \
clawhub publish {SKILL_DIR} \
  --slug {slug} \
  --name "{displayName}" \
  --version 1.0.0 \
  --changelog "Initial release: {一句话描述}" \
  --tags "{tags}"
```

**常见错误处理：**

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Path must be a folder` | 传了文件路径 | 改为传目录路径 |
| `Slug is already taken` | slug 被占用 | 换更具体的 slug 重试 |
| `rate limit exceeded` | 每小时限 5 个新 skill | 用 qqbot-cron 创建 65 分钟后的重试任务 |
| `400` (acceptLicenseTerms) | CLI 版本 bug | patch publish.js，加 `acceptLicenseTerms: true` |
| `401 Unauthorized` | token 无效/过期 | 让用户在 clawhub.com 重新生成 token |

**频率限制时的 patch CLI 方法：**
```bash
PUBLISH_JS=$(find /usr/local/lib -name "publish.js" -path "*/clawhub/*" | head -1)
grep -q "acceptLicenseTerms" "$PUBLISH_JS" || \
  sed -i 's/skillName:/acceptLicenseTerms: true, skillName:/' "$PUBLISH_JS"
```

### Step 7：验证发布

```bash
knot_skills search "{slug}"
```

成功后回复：
```
✅ 已发布：{displayName}
📦 slug：{slug}
🌐 https://clawhub.com/skills/{slug}
```

---

## 快速模式

用户如果一句话提供了所有信息：
> "把 https://github.com/xxx/yyy 做成 skill，token 是 clh_xxx"

直接从 Step 1 执行到底，完成后汇报结果，**不需要逐步确认**。

缺少信息时，**只问缺少的那个**，不重复已知内容。

---

## 示例

**输入：** "把 https://github.com/666ghj/BettaFish 做成 skill，token clh_xxx"

**执行过程：**
1. fetch README → 多 Agent 舆情分析系统
2. knot_skills search → 无重复
3. slug: `opinion-analyzer`，name: `Opinion Analyzer — 多视角舆情分析助手`
4. 撰写 SKILL.md（多视角分析流程、报告模板）
5. 创建目录，写文件
6. `clawhub publish` → ✅ 成功
