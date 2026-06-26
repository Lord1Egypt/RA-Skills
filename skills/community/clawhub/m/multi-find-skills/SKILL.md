---
name: multi-find-skills
description: |
  Multi Find Skills | 技能搜索全能版
  触发场景：用户询问"有什么技能可以帮我..."、"找一个能做X的技能"、"有没有技能可以..."、"帮我搜一下XXX相关的技能"、"search for skill"、"找技能"
  功能：当用户需要新能力、更好的工作流、更强大的工具或更安全的替代方案时，三生态(ClawHub+LobeHub+skills.sh)中搜索+质量核验比较+安装验证+记忆偏好+安全重跑+生命周期管理
  触发禁用：管理已安装用openclaw skills list、创建新skill用skill-creator
author: "wagnzairong (https://github.com/wangzairong)"
evolution:
  created_at: "2026-04-23"
  version: "2.8.0"
  domain: "#engineering"
  success_rate: 0
  parent_skill: ""
  last_used: ""
  use_count: 0
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: [clawhub]
      paths: [~/.openclaw/skills/multi-find-skills/memory.md]
---

# 🔍 Multi Find Skills | 技能搜索全能版

> 同步支持 **ClawHub**、**LobeHub**、**skills.sh** 三大生态的技能搜索工具，具备质量核验、安装验证与完整生命周期管理。

---

## 架构

**记忆文件**：`~/.openclaw/skills/multi-find-skills/memory.md`

**文件结构**：
```
~/.openclaw/skills/multi-find-skills/
├── SKILL.md          # 主文件
├── setup.md          # 首次设置与迁移
├── sources.md        # 三生态搜索命令
├── evaluation.md     # 质量核验与评分
├── troubleshooting.md
└── memory.md         # 用户偏好（运行时生成）
```

- 首次使用前检查： `ls memory.md || echo "NOT_FOUND"`
- **NOT_FOUND** → 执行 `setup.md` 首次设置流程
- **存在** → 读取并应用已有偏好

---

## 记忆系统

### 内存读取时机

每次激活技能时，搜索/推荐前必须：

1. 读取 `memory.md`
2. 获取 `Status.sources`（搜索来源偏好）
3. 获取 `Status.integration`（主动/被动模式）
4. 获取 `Passed` 列表（排除已拒绝的技能）
5. 获取 `Liked` 列表（倾向相似特质）
6. 获取 `Preferences`（过滤条件）

### 内存更新规则

| 触发条件 | 写入位置 |
|---|---|
| 用户说"两个都搜" / "只用 X" | `Status.sources` |
| 用户说"要活跃维护的" / "可以接受实验性的" | `Preferences` |
| 用户说"这个技能很好因为 X" | `Liked` |
| 用户说"不要这个，原因是 X" | `Passed` |
| 用户提到工作领域 | `Domains` |

> ⚠️ **规则：只记录用户明确说过的。不推断、不记录静默行为。**

---

## 触发词

**显式触发**："有什么技能可以帮我..."、"有没有技能可以..."、"找一个能做X的技能"、"帮我搜一下XXX相关的技能"、"search for skill"、"找技能"

**隐式触发**：用户问"怎么做一个X"、说"有没有更好的方式做X"、抱怨现有工具太弱/不稳定、提到重复性工作流、问"这个能做到吗"。

> 若 `memory.md` 中 `Status.integration: passive`，则只在显式触发词匹配时激活。

---

## 工作流程

### 快速流程

```
检测 → 加载记忆 → 理解需求 → 全源搜索 → 评估 → 比较 → 推荐 → 安装或降级 → 学习
```

### 详细流程（9步，整合自 skill-finder）

```
第1步：检测
  └─ 用户是否在描述能力缺口或可安装的需求？
      （见上方的"隐式触发"判断标准）

第2步：加载记忆
  ├─ 读取 memory.md
  ├─ 获取 Status.sources（搜索来源偏好）
  ├─ 获取 Passed 列表（排除已拒绝的技能）
  └─ 获取 Liked 列表（倾向相似特质）

第3步：理解需求
  ├─ 识别领域（React/测试/设计/部署）
  ├─ 识别具体任务（写测试/创建动画/PR审查）
  ├─ 按需求搜索而非按名称（见下方搜索策略表）
  └─ 判断是否适合搜索技能

第4步：搜索（详见 sources.md）
  ├─ 使用 memory.md 中的来源模式（默认 both）
  ├─ skills.sh：npx skills find "<关键词>"
  ├─ ClawHub：npx clawhub search "<关键词>"
  ├─ LobeHub：npx -y @lobehub/market-cli skills search --q "<关键词>"
  └─ 并行执行，汇总结果

第5步：评估（详见 evaluation.md）
  ├─ 四维评分（相关性/质量/维护/价值）≥ 3 才推荐
  ├─ 更新超过 6 个月 → ⚠️，超过 1 年 → ❌
  ├─ 安全扫描标记 → ❌ 不推荐
  └─ 检查 Passed/Liked 列表过滤结果

第6步：比较
  └─ 按匹配度 + 质量对所有来源的结果排名

第7步：推荐
  ├─ 最相关的 1-3 个并给出清晰理由和最优选择
  └─ 使用 evaluation.md 中的"推荐格式"输出

第8步：安装或降级
  ├─ 仅在用户明确同意后安装
  ├─ 安装命令详见 `sources.md`（含单个 skill vs 仓库安装说明）
  ├─ 用户拒绝 → 直接帮助完成任务
  └─ 安装后验证（ls ~/.openclaw/skills/<skill>/SKILL.md）

第9步：学习
  ├─ 将用户明确反馈写入 memory.md（收藏/跳过/偏好）
  ├─ 记录推荐结果到 adoption_log（adopted / rejected / timeout）
  └─ 更新 Metrics（total_recommendations++，采纳则 total_adoptions++）

第10步：追踪
  ├─ 安装成功 → skill_stats 中该技能推荐次数+1，采纳次数+1
  ├─ 用户拒绝 → skill_stats 中该技能拒绝次数+1
  └─ 无反馈超时 → adoption_log 标记 timeout，不更新 skill_stats
```

> ⚠️ **输出格式强制要求**：推荐结果必须使用 evaluation.md 的「推荐格式」输出（比较表 + 四维评分 + 综合分），不得使用原始 CLI 输出。

### 分类不明确时

提出澄清问题：
> "当你说'帮处理数据'，你是指：
> - 存储数据（数据库）？
> - 分析数据（pandas、可视化）？
> - 移动数据（ETL、流水线）？"

详细内容见各专项文件：
- 按需求搜索 → `sources.md ## 按需求搜索`
- 触发识别 → `sources.md ## 触发识别`
- 多结果策略 → `sources.md ## 多结果策略`

---

## 安装命令

详见 `sources.md`（含来源、安装命令语法）。

### 中国镜像（ClawHub 安装失败时）

```bash
clawhub config set registry https://cn.clawhub-mirror.com
clawhub install <skill-name> --registry https://cn.clawhub-mirror.com
```

---

## 安装验证

```bash
ls ~/.openclaw/skills/<skill-name>/SKILL.md
# 文件存在 = 安装成功
```

- 文件存在 → ✅ 安装成功
- 文件不存在 → ❌ 安装失败，尝试 `clawhub install <skill-name> --force`

---

## 安装确认（保守策略）

**安全规则**：不自动安装，不自动加 -y，不在用户未同意前选择安装范围。

1. 展示搜索结果 + 推荐
2. 提供安装命令（详见 `sources.md`）
3. **等待用户显式确认**后再执行安装

禁止：自动运行安装 / 自动加 -y / 静默选范围 / 跳过风险提示

## 输出格式

详见 `evaluation.md`（比较表 + 推荐格式 + 单结果/无结果格式）。

---

## 安全机制

### 输入验证

```bash
[[ ${#keyword} -gt 100 ]] && echo "关键词过长" && exit 1
[[ "$keyword" =~ [[:space:]]*[\;\|\`\"\'\\] ]] && echo "包含非法字符" && exit 1
[[ ${#keyword} -lt 2 ]] && echo "关键词至少2个字符" && exit 1
```

### 数据边界

- **离开机器**：搜索查询（ClawHub/skills.sh/LobeHub 公开搜索）
- **留在本地**：memory.md 中的偏好和搜索历史
- **本技能不会**：未经同意安装 / 跳过安全警告 / 收集隐藏数据 / 访问 skill 目录外的文件

---

## 故障排除

详见 `troubleshooting.md`


---
## 常见陷阱

- 等待"找个技能"的确切措辞 → 错失主动发现时机
- 搜索通用术语 → 得到噪音。要具体：`"react testing"` 而非 `"testing"`
- 保存模式为 `both` 时只搜索一个生态系统
- 仅按名称匹配推荐 → 错过有不同名称的更好替代方案
- 混淆 `ClawHub` 和 `Skills.sh` 之间的安装命令
- 忽略下载量 → 低下载量通常意味着被放弃
- 不检查最后更新时间 → 过时的技能会导致问题
- 混淆 LobeHub 安装命令 → 使用 `npx -y @lobehub/market-cli skills install`


## 安全与隐私

**离开你机器的数据：**
- 发送到 ClawHub 注册表的搜索查询（公开搜索）
- 通过 `skills` CLI / Skills.sh / LobeHub 生态系统发送的搜索查询

**留在本地数据：**
- `~/.openclaw/skills/multi-find-skills/memory.md` 中的所有偏好
- 搜索历史（如果启用）

**本技能不会：**
- 未经用户同意安装技能
- 使用强制安装标志跳过扫描器警告
- 用 `-y` 自动确认 `npx skills add`
- 静默切换到全局安装范围
- 收集隐藏行为数据
- 访问 `~/.openclaw/skills/multi-find-skills/` 外的文件


## 相关技能

- `clawhub` - ClawHub CLI 工具
- `skill-creator` - 创建新技能
- `healthcheck` - 系统健康检查
