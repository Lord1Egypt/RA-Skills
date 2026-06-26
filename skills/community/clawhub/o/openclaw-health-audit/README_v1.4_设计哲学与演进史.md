# OpenClaw Health Audit — 一个关于"不知道钱烧哪去了"的故事

> 🔷 Powered by halfmoon82 🔷  
> © 2026 halfmoon82. All rights reserved.

---

## 安装命令

```bash
clawhub install halfmoon82/openclaw-health-audit
```

安装完成后，运行向导完成初始配置：

```bash
bash ~/.openclaw/workspace/skills/openclaw-health-audit/scripts/install.sh
```

---

## 写在前面

你有没有遇到过这种情况：

月底看账单，token 消耗比上个月多了三倍。翻遍所有对话记录，找不到哪里"用力过猛"。感觉每天也没做什么特别的事，但那些 token 就像水一样，从某个看不见的地方漏掉了。

我们遇到过。不止一次。

这个技能，就是为了把那个"漏水的地方"找出来。

---

## 第一次意识到问题的存在

最初，我们根本没有意识到需要一个"系统健康监控"这样的东西。

AI 代理跑着，就跑着呗。偶尔出个问题，排查一下，修了继续跑。这是大多数人的默认状态。

直到有一天，我们开始认真地看 token 消耗曲线。

曲线是这样的：在某个特定的日期，消耗量开始爬坡，然后持续维持在高位，再也没有回落。没有任何明显的"大任务"可以解释这个增量。

**第一个坑：System Prompt 在悄悄变胖**

`AGENTS.md` 是代理的核心指令文件。我们在里面记录了很多东西——规则、流程、注意事项。每次学到什么新东西，就往里面加一段。

问题是，我们只管加，从来不管它有多大。

在某个时间点，`AGENTS.md` 悄悄超过了 14KB。这意味着每一轮对话，光是 system prompt 就要消耗接近 4000 tokens。一天二十次交互，就是 80,000 tokens——全部来自那些"已经写在文件里，但这次对话根本用不上"的内容。

**我们连这个文件有多大都不知道。**

这就是 Health Audit 诞生的第一个理由：你需要有人定期告诉你，你的 system prompt 又胖了。

---

## 第二个坑：Cron Job 在后台悄悄烧钱

Cron Job 是个好东西。让代理定时检查邮件、定时备份、定时做各种自动化任务。设置好就不用管了。

正是"不用管了"这四个字，埋下了隐患。

我们有一个 `cloudflared-watchdog`，每五分钟检查一次 cloudflared 进程。这个任务本身很轻量，应该几乎不消耗 token。

但有一段时间，它开始消耗大量 token——因为有人（是我们自己）不小心把它配置到了用户直连的 Discord 会话上，并且没有设置 `timeoutSeconds`。

每次执行，都会触发语义路由检查，产生一次完整的 agent turn，带着整个对话历史。每五分钟一次，每天 288 次，每次 2000-5000 tokens。

**一个"几乎不消耗 token"的 Cron Job，每天悄悄烧掉 60-150 万 tokens。**

Health Audit 的第二个功能：检查所有 Cron Job 是否合规——是否使用了隔离会话，是否设置了超时，是否使用了高速模型而不是高价模型。

---

## 第三个坑：孤儿 Session 无限积累

每次你说"新话题"，或者触发了 C-auto 分支，系统就会创建一个新的 Session。旧的 Session 按理说应该被清理——但实际上，它们只是被"遗弃"了，文件还在磁盘上，状态还在 `session_model_state.json` 里。

这本身不直接消耗 token。但当系统需要遍历 Session 状态、或者检索历史上下文的时候，大量孤儿 Session 会拖慢响应，也会让 session 状态文件越来越臃肿，增加每次加载的开销。

我们某次检查，发现累积了 47 个孤儿 Session，其中有些已经超过 30 天没有活动了。

Health Audit 第三个功能：检测超过 N 天（默认 7 天）无活动的孤儿 Session，提供一键清理。

---

## 第四个坑：LLM 缓存从未真正命中（Category E）

这个坑我们在 semantic-router 的文档里也提到了，但它值得在这里再说一遍。

OpenClaw 的 message-injector 插件有一个 prefix cache 机制：如果每轮对话的 `prependContext`（注入到 system prompt 开头的内容）保持不变，LLM provider 就可以复用缓存，cache_read 的价格大约是 input 的 1/10。

但有一段时间，每轮 `prependContext` 里都包含了当轮的 `declarationPrepend`——而 declaration 里有 `ctx_score`（一个每次都不同的浮点数）。

结果：**每轮对话 prefix cache 100% miss，input tokens 全部按原价计算。**

`PATCH_CACHE_TTL` 的正确配置是 30 分钟（1,800,000ms），而不是系统默认的 5 分钟。`extractDeclKey` 也需要更名为 `extractSkillKey`，只关心 skill 激活状态而不是声明文本本身。

Health Audit 会检查这些配置是否正确——`message-injector/index.ts` 里的 TTL 值、函数命名、`declarationPrepend` 是否仍然混入 `prependContext`。

---

## 第五个坑：Session 状态里的"僵尸模型"（Category F）

`session_model_state.json` 记录了每个 Session 当前使用的模型和 fallback 链。

我们发现过这样的记录：某个 Session 的 `fallbackChain` 只有一个元素，没有任何备用；另一个 Session 的 primary 模型前缀是 `lovbrowser/`——这是一个已经废弃的旧格式，正确格式应该是 `custom-llmapi-lovbrowser-com/`。

这些"僵尸状态"的危害是隐性的：当 primary 模型不可用时，fallback 链太短意味着更容易全线失败；错误的 provider 前缀意味着模型实际上调不通，但系统不会主动报错。

Health Audit 的 Category F：检查所有 Session 的 fallbackChain 长度和 provider 前缀格式。

---

## 第六个坑：修复了但没有验证（Category G）

随着系统越来越复杂，我们积累了一套"已知修复"——FIX-0 到 FIX-4，分别对应 declarationPrepend 污染、haiku 模型失效、gemini-3 不可用、lockModel 毒化等问题。

每次修复完，感觉很好，打了 commit，继续前进。

但几周后，偶尔会有人不小心触碰了相关代码，或者配置更新把某个修复覆盖掉了——然后同样的问题再次出现，要重新排查，重新修复，重新烧一遍 token。

Category G 就是为了解决"已知修复被悄悄撤销"的问题。它会定期检查 `message-injector/index.ts` 代码里那些关键特征是否还在：

- `declarationPrepend` 是否还混在 `prependContext` 里（G1）
- `extractSkillKey` 函数是否存在（G2）
- 模型池配置是否和 pools.json 一致（G3）
- fallback 链是否包含已失效的模型（G4/G5）
- `lockModel` 是否还在返回 `modelOverride`（G6）
- `extractStableRoutingParts` 是否存在（G7，路由标签功能）
- `isChannelSession` 是否正确排除了 `:subagent:` 会话（G8）

---

## 当前版本（v1.4.0）的监控全景

```
Layer 1 — 可见成本
  A. System Prompt 体积漂移
     每次超过 warn/alert 阈值时告警

Layer 2 — 配置合规
  B. Cron Job 合规性
     - sessionTarget 必须为 isolated
     - sessionKey 必须为 null
     - timeoutSeconds 必须设置
     - model 不得使用高价模型
  C. 孤儿 Session 检测
     超过 7 天无活动的 Session
  E. 缓存配置完整性
     PATCH_CACHE_TTL / extractSkillKey / declarationPrepend
  F. Session 状态完整性
     fallbackChain 长度 / provider 前缀格式
  G. 代码完整性（FIX-0~4 合规）
     G1-G8 逐项检查，附带修复命令

Layer 3 — 趋势参考
  D. Token 消耗趋势
     warn: 30M/48h  alert: 60M/48h
```

---

## 设计哲学

### 1. 可观测性是第一生产力

问题存在不可怕，看不见才可怕。Health Audit 的核心价值不是修复，而是**让隐性问题变得可见**。每 48 小时一份报告，每份报告包含具体的数值和可执行的修复命令。

### 2. 修复要带着验证

Category G 的存在，是因为我们吃过"修了又被撤销"的亏。每次修复之后的检查，和修复本身同样重要。

### 3. 基线要从实测来

每个系统的 System Prompt 大小都不一样。安装向导会在你的实际环境里测量当前基线，然后以基线 ×1.1 作为 warn，×1.4 作为 alert——而不是用一个对所有人都一样的魔法数字。

### 4. 自动修复要保守

Health Audit 提供修复命令，但不自动执行（除非你明确传 `--fix all`）。每一个修复操作都会先在 dry-run 模式下展示给你看，确认后再执行。"看不见的自动修复"和"看不见的问题"一样危险。

---

## 快速开始

```bash
# 安装
clawhub install halfmoon82/openclaw-health-audit

# 首次配置（测量基线，生成 config.json）
bash ~/.openclaw/workspace/skills/openclaw-health-audit/scripts/install.sh

# 生成报告
python3 ~/.openclaw/workspace/skills/openclaw-health-audit/scripts/health_monitor.py --report

# 查看可修复项
python3 ~/.openclaw/workspace/skills/openclaw-health-audit/scripts/health_monitor.py --list-fixes

# 执行修复（先 dry-run 确认）
python3 ~/.openclaw/workspace/skills/openclaw-health-audit/scripts/health_monitor.py --fix all --dry-run
python3 ~/.openclaw/workspace/skills/openclaw-health-audit/scripts/health_monitor.py --fix all
```

注册 48 小时定时检查（推荐）：

```bash
# 使用模板注册 Cron Job
cat ~/.openclaw/workspace/skills/openclaw-health-audit/templates/cron_health_job.json
# 按模板配置后执行 cron add
```

---

> **作者**: halfmoon82  
> **版本**: openclaw-health-audit v1.4.0  
> **最后更新**: 2026-03-06  
> **状态**: 生产级，持续迭代中
>
> 🔷 Powered by halfmoon82 🔷  
> © 2026 halfmoon82. All rights reserved.  
> MIT License — 自由使用，保留署名。
