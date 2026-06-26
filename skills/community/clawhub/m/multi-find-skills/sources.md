# 搜索来源详细说明

## 搜索来源总览

| 来源 | 搜索命令 | 审查命令 | 安装命令 | 说明 |
|------|---------|---------|---------|------|
| **ClawHub** | `clawhub search "<关键词>"` | `clawhub inspect <slug>` | `clawhub install <slug>` | 精选注册表，内置元数据 |
| **skills.sh** | `npx skills find <关键词>` | 审查返回的仓库/页面 | `npx skills add <owner/repo@skill>` | 开放生态，广泛发现 |
| **LobeHub** | `npx -y @lobehub/market-cli skills search --q "<关键词>"` | — | `npx -y @lobehub/market-cli skills install <skill> --agent open-claw` | 社区市场，AI 相关较多 |
| **GitHub** | 网页搜索 | — | `npx skills add <owner/repo>` | 补充来源 |

---

## 搜索命令速查

### ClawHub

```bash
npx clawhub search "<关键词>"                # 向量搜索
npx clawhub explore --sort installs --limit 20   # 按安装量浏览热门
npx clawhub explore --sort rating --limit 20     # 按评分浏览
npx clawhub explore --sort trending --limit 20   # 按趋势浏览
npx clawhub inspect <slug>                       # 查看详情
npx clawhub inspect <slug> --files              # 查看所有文件
npx clawhub list                                # 查看已安装
```

> **注意**：`clawhub` 命令通常全局安装；如遇问题可使用 `npx clawhub` 调用。

### skills.sh

```bash
npx skills find "<关键词>"                   # 搜索 skills
npx skills add owner/repo --list            # 预览可用技能（不安装）
npx skills list                             # 查看已安装
npx skills list -g                          # 查看全局安装
npx skills find "popular"                    # 浏览热门技能
npx skills check                            # 检查已安装技能的更新
npx skills update                           # 更新已安装的技能
```

### LobeHub

```bash
npx -y @lobehub/market-cli skills search --q "<关键词>"
npx -y @lobehub/market-cli skills install <skill-name> --agent open-claw
```

---

## 多来源搜索流程

对于每个新查询：

1. 读取 `memory.md`，获取 `Status.sources`（both / clawhub / skills.sh / lobehub）
2. 如果模式为 `both`，用相同的关键词**并行**搜索 ClawHub、skills.sh 和 LobeHub
3. 在推荐前一起比较所有来源的最强匹配
4. 为每个结果附加来源和确切安装命令

---

## 触发识别（隐式激活）

即使用户没有明确说"技能"也搜索：

| 用户信号 | 通常意味着 | 动作 |
|---|---|---|
| "我怎么做 X？" | 技能可能已经解决了这个问题 | 搜索相关技能 |
| "你能做这个吗？" | 可能存在能力缺口 | 搜索并推荐 |
| "一定有更好的方法" | 专业化工作流 | 搜索相关技能 |
| "我应该安装什么？" | 直接的技能发现请求 | 搜索 + 推荐 |
| "当前这个技能太弱了" | 替换搜索 | 搜索替代方案 |

---

## 按需求搜索，而非按名称

用户说"我需要处理 PDF"——不要只搜索"pdf"。思考他们实际需要什么：

| 用户需求 | 更好的搜索 |
|---|---|
| 编辑 PDF | `clawhub search "pdf edit"` + `skills find pdf edit` |
| 创建 PDF | `clawhub search "pdf create"` + `skills find pdf generate` |
| 从 PDF 提取 | `clawhub search "pdf extract"` + `skills find pdf parse` |
| 填写 PDF 表单 | `clawhub search "pdf form"` + `skills find pdf form` |

---

## 查询优化

| 情况 | 行动 |
|---|---|
| 结果太多 | 增加具体性："python" → "python async" |
| 无结果 | 扩大："fastapi oauth2" → "api auth" |
| 领域错误 | 澄清："testing" → "unit testing" vs "e2e testing" |
| 工具特定 | 直接试工具名："stripe"、"twilio" |
| 一个来源为空 | 保留另一个来源，但说明只有一个生态系统产生了匹配 |

---

## 扩展搜索词

如果首次搜索结果不佳：

1. **同义词** — edit → modify，create → generate，check → validate
2. **相关工具** — pdf → document，docx → word
3. **底层任务** — "pdf form" → "form filling"
4. **领域名称** — "stripe payments" → 只要 "stripe"

---

## 解读结果

将每个结果规范化为相同的决策形态：
- 来源（ClawHub / skills.sh / LobeHub）
- 名称 / 标识符
- 功能
- 安装命令
- 质量信号（下载量、更新时间、四维评分）

**快速质量信号：**
- 高下载量 + 最近更新 = 维护良好
- 清晰的描述 = 结构可能良好
- 同一作者的多个技能 = 成熟的创建者
- 可识别的仓库或维护者 = Skills.sh 中更安全的选择
- 模糊的描述 = 可能质量低

---

## 多结果策略

当多个技能匹配时：

1. **过滤** — 应用四维评分标准（evaluation.md）
2. **排名** — 按特定需求的匹配度，不只是下载量
3. **呈现前 3 名** — 每个都附理由
4. **选出赢家** — 给出建议，而不只是选项
5. **让用户选择** — 或提出澄清问题

示例回复：
> 为 React 测试找到 3 个选项：
> 1. `react-testing`（ClawHub）— 专注于组件测试，5k 下载量
> 2. `vercel-labs/agent-skills@frontend-design`（Skills.sh）— 更广泛的 frontend 工作流
> 3. `testing`（ClawHub）— 通用测试，包含 React 部分
>
> 哪个更适合你的项目？

---

## 搜索是语义的

搜索基于含义，不是关键词精确匹配：
- `"react hooks"` 找到关于 React 模式的技能
- `"api testing"` 找到 REST、GraphQL 测试技能
- `"deploy docker"` 找到容器化 + 部署

不需要特殊运算符——用自然语言描述你想要什么。

---

## skills.sh 排行榜分类

| 分类 | 说明 | 适用场景 |
|------|------|---------|
| **All Time** | 总安装量排名 | 发现经过时间验证的成熟技能 |
| **Trending (24h)** | 24小时内安装量 | 发现最新热门趋势 |
| **Hot** | 实时热度 | 追逐最新潮流 |

访问 https://skills.sh 查看完整排行榜

---

## 安装命令语法

```bash
# ClawHub
clawhub install <slug>

# skills.sh：安装特定 skill
npx skills add owner/repo@skill-name -g -y

# skills.sh：安装整个仓库
npx skills add owner/repo -g -y

# 参数：-g=全局安装，-y=跳过确认，@skill-name=指定特定 skill

# LobeHub
npx -y @lobehub/market-cli skills install <skill-name> --agent open-claw
```

---

## 补充来源

- **OpenClaw Directory**：https://www.openclawdirectory.dev/skills（网页分类浏览）
- **GitHub**：`site:github.com "openclaw skill"` / `site:github.com "SKILL.md"`
- **推荐 GitHub 来源**：
  - `vercel-labs/agent-skills` — Vercel 官方技能库
  - `anthropics/anthropic-cookbook` — Anthropic 相关
  - `microsoft/semantic-kernel` — Microsoft 相关
  - `openclaw/openclaw` — OpenClaw 官方
- **社区论坛**：
  - SitePoint：https://www.sitepoint.com/community/
  - Discord：https://discord.com/invite/clawd