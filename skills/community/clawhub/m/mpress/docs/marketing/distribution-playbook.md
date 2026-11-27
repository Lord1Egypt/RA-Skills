# 分发工作流：把一个 Agent Skill 铺到「能被找到」的地方

> 适用：`mpress` 这类「开源 Skill + 可选 CLI」。
> 目标不是"到处发一遍"，而是让三类入口同时成立：**AI 助手能装、技能目录能搜到、人类能看到别人在用**。
> 配套：`docs/marketing/README.template.md`。
> 本文只写"怎么做"，不含任何已执行的发布动作。

---

## 0. 先想清楚：一个 Skill 被用起来要过三关

```text
被发现 ──→ 被安装 ──→ 被留下
（目录/搜索/AI 回答）  （一条命令）   （跑通 + 有反馈）
```

绝大多数 Skill 死在第一关：仓库有了，但没有任何目录收录，用户搜不到，AI 也不知道它存在。

三关各自的关键动作：

| 关卡 | 决定因素 | 你要做的事 | 主要在哪个文件上做 |
|---|---|---|---|
| 被发现 | SKILL.md 的 `description`、目录站收录、GitHub topics | 重写 description + 铺渠道 | `SKILL.md` / GitHub About |
| 被安装 | 一条能复制的命令、无密钥也能跑通 | README 首屏给命令 + 提供 demo 模式 | `README.md` |
| 被留下 | 一次成功体验、失败有明确提示 | 退出码/错误提示 + 示例文章 + FAQ | `scripts/` / `docs/` |

**优先级判断**：现在 stars=0，说明第一关完全没打通。渠道开通 > README 美化 > 功能新增。

---

## 1. 渠道矩阵（按投入产出排序）

| 优先级 | 渠道 | 类型 | 要不要审核 | 门槛 | 预期收益 | 首轮耗时 |
|---|---|---|---|---|---|---|
| **P0** | GitHub 仓库资产（About / topics / release / social preview） | 基础设施 | 否 | 无 | 所有下游抓取的数据源 | 30 min |
| **P0** | [skills.sh](https://skills.sh) | 目录 + 榜单 | 否（自动） | Node ≥ 22 | 英文圈最大安装入口，`npx skills add` 直接可用 | 20 min |
| **P0** | [ClawHub](https://clawhub.ai) | 官方 registry | 自动安全审核 | GitHub 账号 | OpenClaw 生态内可被语义检索到 | 30 min |
| **P1** | [SkillHub](https://www.skillhub.cn) | 中文市场 | 自动审核（关键词 + AI 语义） | 实名认证（腾讯云人脸） | 腾讯 WorkBuddy / 中文 AI 用户 | 60 min |
| **P1** | [虾评](https://xiaping.coze.com) | 中文技能交易平台 | 试用版免审，转正需评测 | 注册拿 API Key | Coze 生态曝光 + 评测带来口碑 | 60 min |
| **P1** | `llms.txt` + `SKILL.md` description | 机器可读 | 否 | 无 | 被 LLM/目录正确理解 | 30 min |
| **P2** | [SkillsMP](https://skillsmp.com) | 自动索引 | 否（爬虫） | 无需操作 | 长尾搜索流量 | 0 |
| **P2** | [FindSkills](https://findskills.org) | 自动索引 + CLI | 否（爬虫） | 无需操作 | 长尾；**注意其条款不向中国大陆居民提供服务** | 0 |
| **P2** | [ClawShip](https://clawship.dev/skills/submit) / [Swarmnest](https://swarmnest.ai/agent-skills/submit) / [AgentHub](https://agentskillsmarket.space/submit) | 提交表单 | 人工 | 表单 | 小站，聊胜于无 | 20 min |
| **P2** | awesome-* 列表 PR | 社区 | 人工 review | GitHub PR | 长期 SEO + 可信度 | 30 min |
| **P2** | npm（scoped） | 包管理 | 无 | 改名/加 scope | `npx` 入口、npm 站内搜索 | 30 min |
| **P3** | 公众号 / V2EX / 即刻 / 小红书 / X | 内容 | 平台规则 | 无 | 冷启动第一批真实用户 | 2 h |

> 判断标准：**能不能被「一条命令」装走**。不能的渠道，优先级降一级。

---

## 2. 发布前必修：把「可被抓取」的资产补齐

这一节不完成，后面所有渠道都是把半成品递出去。

### 2.1 重写 `SKILL.md` 的 description（最高杠杆）

目录站（skills.sh / ClawHub / SkillHub / 虾评）**只读 SKILL.md，不读 README**。ClawHub 是向量检索，description 就是召回的唯一依据。

现状（过长、以任务罗列为主）：

```yaml
description: 当用户要把 Markdown 文章排成微信公众号格式、生成本地排版预览，或自动上传图片与封面并推送到微信公众号草稿箱时使用；不用于改写文章内容。
```

建议改成「品类 + 触发原话 + 产出 + 边界 + 同义词」：

```yaml
name: mpress
description: 把 Markdown 或纯文本排成微信公众号图文并推进草稿箱的 Skill。当用户说"公众号排版/微信图文/推文排版/排成公众号格式/生成封面图/推到草稿箱/一键发布到公众号"时使用；产出内联 HTML、layout.json、1800×766 封面，可只本地生成（不联网）或直连公众号草稿箱。不用于改写文章内容，不自动群发。
metadata:
  version: 6.1.0
```

改写原则：
- **把用户会说的原话写进去**（"推文""草稿箱""封面图"），不要只写内部术语。
- **写清"能不能不联网"**——这是安装决策的关键信息。
- **边界写进同一句**，减少误触发。
- 长度控制在 300 字内（目录站展示会截断）。
- 改完顺手把 `metadata.version` 提到 `6.1.0`：多数目录站只在版本变化时重抓，否则旧描述会挂很久。
- 改完 `README` 的「给 AI Agent 的速览」和 `llms.txt` 必须同步同义。

### 2.2 加 `llms.txt`（仓库根目录）

```markdown
# mpress

> 把 Markdown / 纯文本排版成微信公众号图文，并可推送到公众号草稿箱的开源 Agent Skill + CLI。Node ≥ 18，仅 2 个依赖，MIT。

## 是什么
- 类型：Agent Skill（SKILL.md）+ 命令行工具（scripts/wechat.mjs）
- 入口：`npx skills add shxuk/mpress`
- 离线生成：`node scripts/wechat.mjs gen 文章.md`（不联网、不需要密钥）
- 推送草稿箱：`node scripts/wechat.mjs push 文章.md`（需 WECHAT_APP_ID / WECHAT_APP_SECRET + IP 白名单）

## 何时使用
- 用户要把 Markdown 文章排成微信公众号格式
- 用户要生成公众号封面图（1800×766）
- 用户要把文章推送到公众号草稿箱
- 用户要统一的杂志风版式（kicker / lead / metrics / dossier / versus / steps / verdict / qa / checklist / follow）

## 何时不用
- 用户要改写文章内容
- 用户要自动群发（本工具只到草稿箱）
- 用户没有公众号或没有开发者权限

## 关键事实
- 版本：6.0.0（Skill）/ 1.1.0（npm）
- 许可：MIT
- 运行时：Node ≥ 18
- 依赖：markdown-it、juice
- 退出码：2 凭证 / 3 白名单 / 4 图片 / 5 结构 / 6 网络
- 已知限制：无微信支付权限时正文 `<a>` 链接会被微信剥离

## 链接
- 仓库：https://github.com/shxuk/mpress
- 规范：docs/规范/VISUAL-SYSTEM.md, docs/规范/SVG-FOLD.md
- 样例：docs/样例/style-overview.md
```

### 2.3 GitHub 仓库资产

| 位置 | 现在 | 改成 |
|---|---|---|
| About description | 英文长句 | `把 Markdown 排成微信公众号图文并推进草稿箱 · Agent Skill + CLI · 离线生成 / 一键 push · MIT` |
| Topics | `ai-skill, markdown, publisher, svg-fold, wechat` | 追加 `wechat-mp`、`wechat-official-account`、`typesetting`、`agent-skill`、`claude-skill`、`cover-generator`、`markdown-to-html` |
| Homepage | 空 | 先指博客案例页；`skills.sh` 收录后再改指 `https://skills.sh/shxuk/mpress` |
| Social preview | 默认 | 上传 `assets/preview-components.png` 裁切版（1280×640） |
| Release | 无 | 打 `v1.2.0` tag，release notes 写「更名 mpress + 安装命令 + 实测数据」 |
| 仓库名 | `mpress` | **已改名 `mpress`**（2026-11）。GitHub 改名会保留 star、issue 与 301 重定向；改名窗口只有开源头几天，越早越便宜 |

> topics 是 GitHub 搜索和第三方爬虫的主要分类信号，加到 10–12 个上限为止。

### 2.4 npm 发布（改名后已解锁）

旧名 `mpress` 在 npm 上被 `panda_neo` 占用，所以当时的方案只能是 scoped 包或干脆不发。**改名 `mpress` 后这个冲突消失了**：`mpress` 在 npm 上仍未注册，直接发布就能拿到裸包名，`npx mpress gen 文章.md` 立刻可用——这是把「只能 clone」变成「一条命令」的关键一步。

```bash
npm login
npm publish --access public
npm view mpress version        # 确认发布成功
npx mpress gen templates/editorial.md
```

> 发布前检查两点：一是 `package.json` 的 `files` 白名单不能漏 `assets/`（主题和底图在里面，漏了装完会缺样式）；二是别把 `.env`、`credentials` 带进包里。

### 2.5 安装路径实测（三条，全部要亲手跑通）

```bash
# A. 技能目录安装（主力路径）
npx skills add shxuk/mpress

# B. 克隆后直接跑（离线可用，验证零密钥体验）
git clone https://github.com/shxuk/mpress.git
cd mpress && npm i
node scripts/wechat.mjs gen docs/样例/style-overview.md

# C. 从 GitHub 直接跑（npx 拉取仓库，需网络）
npx github:shxuk/mpress gen docs/样例/style-overview.md
```

验收：B 必须在**没有 `.env`、没有网络**的机器上跑通；C 若不稳定就不要写进 README。

### 2.6 体积检查（SkillHub 有硬限制）

SkillHub GitHub 导入要求：归档 ≤ 20 MiB、候选目录 ≤ 10 MiB、文件数 ≤ 200。

```bash
git archive --format=zip -o /tmp/skill.zip HEAD
ls -lh /tmp/skill.zip
unzip -l /tmp/skill.zip | tail -3
```

超限时：把 `assets/components/*.png`、`docs/样例` 里的大图压缩或移出，只保留 README 用到的 3–4 张。

---

## 3. 逐渠道 Runbook

### 3.1 skills.sh（P0，最先做）

**它是什么**：Vercel 维护的 Agent Skills 目录 + 排行榜，`npx skills add owner/repo` 是当前英文圈最通用的安装方式。

**收录机制**：没有提交表单。榜单按 `skills` CLI 的**匿名安装遥测**排名，仓库页 `skills.sh/owner/repo` 由安装数据生成。

**动作**：
1. 确认 `npx skills add shxuk/mpress` 能装成功（SKILL.md 在根目录即可）。
2. README 顶部加 badge：
   ```markdown
   [![skills.sh](https://skills.sh/b/shxuk/mpress)](https://skills.sh/shxuk/mpress)
   ```
3. 把这条命令作为**所有渠道文案的统一 CTA**（公众号、V2EX、X 都一样）。
4. 发布后 24h 检查 `skills.sh/shxuk/mpress` 是否出现；没出现就再装两次并等 48h。

**坑**：Node 需 ≥ 22.20；安装量少时榜单不显示，属正常，看仓库页而不是榜单。

---

### 3.2 ClawHub（P0）

**它是什么**：OpenClaw 官方技能 registry，语义检索（向量），有安全审核和版本历史。

**动作**：

```bash
npm i -g clawhub
clawhub login                 # GitHub OAuth device flow
clawhub whoami

# 先 dry-run，看会传哪些文件、版本号怎么算
clawhub skill publish . \
  --slug mpress \
  --name "WeChat Article Publisher" \
  --categories communication,creative \
  --topics "wechat,markdown,publishing,typesetting,cover" \
  --dry-run

# 正式发布
clawhub skill publish . \
  --slug mpress \
  --name "WeChat Article Publisher" \
  --categories communication,creative \
  --topics "wechat,markdown,publishing,typesetting,cover"
```

**要点**：
- `--slug` 一旦定下就是安装标识，选短且语义准的（`wechat-article` 优于 `mpress`）。
- 合法 category 只有固定集合，本 skill 用 `communication` + `creative`（最多 3 个）；`topics` 最多 5 个、≤48 字符。
- 发布后进入 pending，等自动安全审核通过才可被搜索/安装。
- **ClawHub 上的 Skill 以 MIT-0 释出**（比 MIT 更宽松，无署名要求）。这是平台规则，不是你能选的；如果你在意署名，考虑只发试用/文档而不发 ClawHub。
- 首次发布默认 `1.0.0`，之后按 patch 递增；用 `--version` 显式指定大版本。

**验证**：
```bash
clawhub search "wechat 公众号 排版"
clawhub inspect @<your-handle>/mpress
```

---

### 3.3 SkillHub（P1，中文主力）

**它是什么**：腾讯 WorkBuddy 生态的中文 Skill 市场，支持 ZIP 上传和 GitHub 直连导入。

**硬门槛**：发布个人 Skill 需**实名认证**（腾讯云人脸核身）。这一步只能你本人做。

**动作**：
1. 登录 [skillhub.cn](https://www.skillhub.cn)，完成实名认证。
2. 控制台 → 发布 Skill → 选「GitHub 导入」，填 `https://github.com/shxuk/mpress`。
3. 平台自动校验：仓库非 fork / 非归档、根目录含 `SKILL.md`、归档 ≤ 20 MiB、候选目录 ≤ 10 MiB、文件数 ≤ 200。
4. 填写展示信息（见 §4 文案包）：名称、一句话简介、详细描述、分类、标签、封面图。
5. 提交 → 自动审核（关键词 + AI 语义）→ 通过后上架。

**坑**：
- 超大图片会导致导入失败，先按 §2.6 瘦身。
- 分类选"内容创作 / 办公效率"这类，别选"开发工具"。
- 描述里必须出现"公众号""排版""草稿箱"，否则语义审核容易判成"通用 Markdown 工具"。

---

### 3.4 虾评 xiaping.coze.com（P1，中文评测驱动）

**它是什么**：Agent 技能交易/评测平台，技能有"试用版 → 转正"机制，靠真实评测积累可信度。

**机制要点**（来自官方 `https://xiaping.coze.com/skill.md`，务必以线上最新版为准）：
- 注册：`POST /api/auth/register {"name": "..."}` → 返回 `sk_` 开头的 key。
- 发布：`POST /api/skills`，表单字段 `name / description(50–300 字) / trigger(JSON 数组) / category / tags / version / file(ZIP ≤ 10MB) / requires_api_key`。
- 新技能默认**试用版**，+10 虾米。
- 转正：不依赖外部 API Key 的走 SBI（≥ 2.0 或 ≥ 50 篇评测）；**依赖 API Key 的需 ≥ 40 篇评测且加权分 ≥ 4**。
- 评测：`POST /api/skills/{id}/comments`（1–5 星 + 20–2000 字 + 维度），评测者需先下载、等级 ≥ A2-1。
- 更新：`POST /api/upload`（file + skill_id + changelog）。
- 域名必须是 `xiaping.coze.com`（旧 `.site` 域会丢 Authorization）。

**关键决策：`requires_api_key` 怎么填**

本 skill 的 `gen` 模式零密钥可跑，但核心价值"推进草稿箱"需要公众号 AppID/Secret。**建议如实填 `true`**——虚假申报会在审核/评测阶段被拆穿，且 40 篇评测的门槛是可以用运营补上的，信誉补不上。

对应的运营动作：把"帮它转正"写进 README / 公众号文末，邀请真实用户评测（不要刷，平台会看下载+评测比）。

**打包**：

```bash
git archive --format=zip -o mpress-v1.2.0.zip HEAD
# 检查 ≤ 10MB
```

**发布脚本（示例，执行前先看懂字段）**：

```bash
export XP_KEY=sk_xxx
curl -X POST https://xiaping.coze.com/api/skills \
  -H "Authorization: Bearer $XP_KEY" \
  -F "name=公众号排版发布器" \
  -F "description=<50–300 字，见 §4>" \
  -F 'trigger=["公众号排版","微信图文","推到草稿箱","生成封面图"]' \
  -F "category=内容创作" \
  -F "tags=微信,公众号,排版,markdown" \
  -F "version=6.0.0" \
  -F "requires_api_key=true" \
  -F "file=@mpress-v1.2.0.zip"
```

**验证**：`GET /api/skills/{id}` 看状态；用另一个账号下载 + 评测走一遍完整链路。

---

### 3.5 自动收录类（P2，零动作但要"喂养"）

| 站点 | 机制 | 你能做的 |
|---|---|---|
| SkillsMP | 爬 GitHub 上所有公开 `SKILL.md`（自称 430 万+） | 保证根目录 `SKILL.md` + description 关键词准确；等抓取 |
| FindSkills | 聚合 GitHub / ClawHub 等 | 同上；**其服务条款注明不向中国大陆居民提供服务**，不要作为主渠道运营 |

这两家不认证、不担保、也不代安装，价值是长尾搜索命中。**不要为它们改仓库结构**。

---

### 3.6 表单提交类（P2，20 分钟批量做）

| 站点 | 入口 | 提交内容 |
|---|---|---|
| ClawShip | `clawship.dev/skills/submit` | 仓库 URL + 一句话 + 分类 |
| Swarmnest | `swarmnest.ai/agent-skills/submit` | 仓库 URL + 描述 + 演示 |
| AgentHub | `agentskillsmarket.space/submit` | GitHub 导入或表单 |

统一用 §4 的「50 字版 + 120 字版」，不要现写。

---

### 3.7 awesome 列表 PR（P2）

目标仓库（先搜再提，避免重复）：
- `awesome-claude-skills` / `awesome-agent-skills` / `awesome-ai-agents`
- 中文：`awesome-wechat`（若有公众号开发相关分区）

PR 格式照抄邻居条目的写法，一行一条：

```markdown
- [mpress](https://github.com/shxuk/mpress) - 把 Markdown 排成微信公众号图文并推送草稿箱的 Skill；离线生成，MIT。
```

注意：多数 awesome 列表要求"有实际使用价值 + 有 README + 有 License"，提交前先满足。一次提 2 个，别群发。

---

### 3.8 内容渠道（P3，前 50 个真实用户来自这里）

**公众号（你自己的号，最强案例场）**

结构固定，别写产品说明书：

1. 开头 3 行：我原来排一篇要 40 分钟，现在 3 分钟。
2. 一张 before/after 截图。
3. 三条命令。
4. 一个真实失败案例（比如 IP 白名单踩坑）+ 怎么解决。
5. 文末：仓库链接 + "装完回来告诉我哪里排版不对"。

**V2EX**：发 `/go/create`，标题带痛点（"写了个把 Markdown 直接推进公众号草稿箱的 Skill"），正文给命令和截图，**不要**一上来贴 star 求关注。

**即刻 / 小红书**：只发结果图 + 一句"AI 一句话，排版+封面+草稿箱全做完"，评论区放链接。

**X / 英文**：一条 thread，首推给 GIF，第二条给 `npx skills add`，第三条给边界（不群发、需 IP 白名单）。

---

## 4. 文案包（复制即用）

### 4.1 一句话（中 / 英）

- 中：**把 Markdown 一句话排成微信公众号图文，连同封面一起推进草稿箱。**
- 英：**Turn Markdown into a WeChat Official Account article — typeset, covered, and pushed to your drafts folder.**

### 4.2 三档长度

**50 字（列表/目录副标题）**
> 把 Markdown 排成微信公众号图文并推进草稿箱的 Agent Skill。离线可生成，联网可直推，MIT。

**120 字（README 首段 / SkillHub 简介）**
> mpress 是一个开源的 Agent Skill + CLI：把 Markdown 或纯文本排版成微信公众号可用的内联 HTML，生成 1800×766 封面，需要时连图片一起推进公众号草稿箱。内置 10 个杂志风卡片组件与原生 SVG 折叠，样式由一套 CSS 统一控制。零密钥可离线生成，推送只需 AppID/AppSecret 与 IP 白名单。

**300 字（虾评 / 商店详情）**
> 写公众号最烦的不是写，是排版和上传：图片要一张张另存再传，样式每次都要重调，AI 写好的稿子还得手工搬进后台。
>
> mpress 把这段流程做成一条命令：给 AI 一篇 Markdown，它按固定版式渲染成微信能吃的内联 HTML（table 布局、内联样式、无外链 CSS），自动上传正文图片与封面（1800×766），新建或更新公众号草稿，你在后台确认后自己点群发。
>
> 它提供 10 个卡片组件（刊头、结论条、指标卡、双轨对照、步骤阶梯、档案卡、判词、问答、清单、关注卡）和原生 SVG 折叠，全部由 `assets/theme.css` 一处控制，换品牌色只改一份 CSS。也支持只本地生成（`gen`，不联网、不需要密钥），先看效果再接公众号。
>
> 边界：不改写正文，不自动群发，不做数据统计。适合有固定品牌规范的企业运营、做个人 IP 的自媒体、以及批量产出图文的内容团队。

### 4.3 虾评 `trigger` 数组

```json
["公众号排版","微信图文排版","推到公众号草稿箱","生成公众号封面","markdown 转公众号","微信推文排版","一键发布公众号"]
```

### 4.4 tags / topics

- 中文：`微信` `公众号` `排版` `Markdown` `封面图` `内容运营`
- 英文：`wechat` `markdown` `publishing` `typesetting` `cover` `agent-skill`

### 4.5 固定 FAQ（所有渠道复用）

**Q：需要公众号的什么权限？**
A：需要已认证公众号开发者权限，拿到 AppID 与 AppSecret，并把运行机器的出口 IP 加进 IP 白名单。已认证的订阅号、服务号都行；个人主体未认证订阅号没有草稿接口权限。

**Q：会不会自动群发？**
A：不会。工具只写草稿箱，群发必须你在公众号后台手动点。

**Q：AppSecret 会不会泄露？**
A：凭证只从环境变量或本地 `credentials` 文件读取，`.gitignore` 已忽略；仓库不含任何用户凭据。

**Q：没有微信支付权限，正文链接怎么办？**
A：微信会剥离未授权域名的 `<a>`，工具会提前提示受影响的链接，改为纯文本展示。

**Q：必须联网吗？**
A：不必须。`gen` 模式纯本地渲染，不联网、不需要密钥，可以先看排版效果。

---

## 5. 节奏：90 分钟开荒 + 30 天跟进

| 时间 | 动作 | 完成标志 |
|---|---|---|
| D0 · 90 min | §2 全部资产（description / llms.txt / About / topics / release / 体积检查） | 三条安装命令自测通过 |
| D0 · 30 min | §3.1 skills.sh + §3.2 ClawHub | `clawhub inspect` 可见，skills.sh 仓库页出现 |
| D1 | §3.3 SkillHub（实名 + 导入）、§3.4 虾评（试用版上架） | 两个后台都有条目 |
| D3 | §3.8 公众号案例文 + V2EX | 首批真实反馈进 issue |
| D7 | 复盘：哪个渠道带来 clone/install；改 description 关键词 | 有数据表 |
| D14 | §3.6 表单类 + §3.7 一个 awesome PR | 至少 1 个 PR 合入 |
| D30 | 发 `v6.1`（修掉前 30 天 issue），同步所有渠道 changelog | 二次曝光 |

---

## 6. 度量：只看四个数

| 指标 | 从哪看 | 目标（30 天） |
|---|---|---|
| **安装数**（北极星） | skills.sh 仓库页 / clawhub downloads / SkillHub 浏览-下载 | ≥ 50 |
| 仓库访问 → clone 转化 | GitHub Insights → Traffic | ≥ 15% |
| 真实反馈 | issue + 评测数 + 私信 | ≥ 10 |
| 目录收录数 | 手动巡检表 | ≥ 4 个平台 |

渠道归因：每个渠道用不同的入口链接（README 里同一个命令，但各渠道文末用 `?utm_source=` 的仓库链接），GitHub Traffic 能看到来源。

**别看的数**：stars（滞后且不可控）、曝光量（无转化意义）。

---

## 7. 风险与合规清单

| 风险 | 说明 | 处置 |
|---|---|---|
| **npm 包名混淆** | `mpress` 已被他人占用 | 只用 scoped 包或 `npx skills add`，README 禁止裸 `npx` |
| **凭证泄露** | AppSecret 是高敏凭证 | 只走环境变量/本地文件；README 显式声明不收集；PR 前检查 diff |
| **ClawHub MIT-0** | 上架即以 MIT-0 释出，无署名要求 | 接受再发；不接受就只发文档/试用 |
| **虾评 API-key 判定** | 申报 `true` 会走 40 篇评测转正 | 如实申报 + 用真实用户评测；不要刷评 |
| **SkillHub 实名** | 人脸核身不可代做 | 本人操作，一次性 |
| **FindSkills 地域条款** | 明确不向中国大陆居民提供服务 | 只依赖自动抓取，不主动运营、不引导用户 |
| **目录抓取延迟** | 自动索引站可能数周不更新 | 以 SKILL.md 为唯一事实源，等即可 |
| **"即将上线"文案** | 发布前写死未上线渠道会失信 | README 只写已可用路径 |

---

## 8. 验收标准（做完怎么算完成）

- [ ] `SKILL.md` description 含触发原话 + 边界，且与 README 速览、`llms.txt` 三处同义
- [ ] 三条安装命令在干净环境跑通（含一条零密钥离线）
- [ ] GitHub About / topics / release / social preview 全部更新
- [ ] 至少 3 个目录站可搜到，且搜索词是"公众号排版"这类用户词而非仓库名
- [ ] 所有渠道使用同一句 50 字简介，一个 CTA
- [ ] 有 1 篇真实案例（含 before/after 与失败复盘）
- [ ] 30 天复盘表有数据

---

## 9. 把项目包装成「个人案例」

渠道铺完只是"有人用"，案例是"别人记住你是谁"。同一套素材，三种写法。

### 9.1 案例页只讲三件事

| 段 | 写什么 | 反面写法 |
|---|---|---|
| 问题 | 你自己遇到的、能量化的痛（"一篇 3000 字，排版 40 分钟，图片 12 张"） | "公众号排版行业存在效率问题" |
| 做法 | 你做的**关键取舍**（为什么用内联样式、为什么只到草稿箱、为什么坚持 2 个依赖） | 功能罗列 |
| 结果 | 数字 + 一句别人给的反馈 | "广受好评" |

### 9.2 必备素材（各 1 份，所有场景复用）

1. **一张 before/after**：微信后台里手排 vs 工具产出，同屏对比。
2. **一个数字**：单篇耗时从 X → Y（自己掐表，注明样本量）。
3. **一个失败**：IP 白名单 / 外链被剥离 / 图片顺序错乱中最真实的一个，以及怎么定位的。
4. **一个外部信号**：第一个陌生 issue、第一条评测、第一次被目录收录（截图存档）。

### 9.3 三种对外话术

**作品集条目（3 行）**
> mpress · 开源 Agent Skill（MIT）
> 把 Markdown 一键排成微信公众号图文并推进草稿箱；10 个版式组件 + 原生 SVG 折叠，2 个依赖，零密钥可离线出稿。
> 已收录于 {渠道名}，累计安装 {N} 次。

**自我介绍 30 秒**
> 我做了一个公众号排版的开源 Skill：AI 写完稿，一条命令就排好版、做好封面、进草稿箱。现在有 {N} 个人在用，也上了 {渠道}。做的过程中最大的坑是微信会剥离外链样式，所以整套 CSS 必须内联——这也是它和 135、秀米那类编辑器不一样的地方。

**面试/合作问答**
- 为什么做这个？→ 自己的重复劳动 + 现有工具不可编程。
- 最难的部分？→ 微信的样式沙箱（只能内联、不能外链 CSS、不能 JS），以及"只到草稿箱"的产品边界。
- 怎么验证有人需要？→ 渠道数据 + issue 内容分布，而不是 star 数。

### 9.4 一条纪律

**所有数字必须能指向一个链接或截图。** 案例最贵的不是排版，是可信度；一个编的数字会让整篇失效。

