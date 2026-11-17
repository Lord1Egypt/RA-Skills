<p align="center">
  <img alt="mu-self-evolve" src="assets/default-banner.png" width="100%">
</p>

# 🧬 mu-self-evolve · Agent自我反思与进化器

> AI Agent 持续进化系统 — 每日经验沉淀 + 每周错误反思，让 Agent 像人一样从经验中学习。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-self-evolve/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill%E9%9B%86%E5%90%88-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-self-evolve)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-self-evolve)](https://github.com/muippt/mu-self-evolve/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-self-evolve)](https://github.com/muippt/mu-self-evolve/stargazers)

### 💡 使用场景示例

🧠 **每日经验沉淀** — 自动从当天对话中提取纠正、错误、正向反馈，分类录入结构化文件。

🔗 **断链防护（v3.1）** — 触发信号当场写入日记，日记缺失时 cron 主动从当日真实痕迹兕底重建，进化闭环永不断流。

🔍 **VFM 确定性验算** — 经验提升为永久记忆前，必须通过脚本验证复现次数、跨任务数、解决率，而非仅靠 LLM 自评。

🪶 **评分+衰减淘汰** — 记忆条目按 30 天半衰期公式自动衰减，低价值条目自动归档，高复现条目豁免。

🏷️ **WHERE×WHY 病理归档** — 每条错误标注「出错环节×根因类型」，结构化分析模式而非模糊叙事。

🧪 **评委偏差审计** — 注入已知属性的合成测试条目，验证淘汰机制是否正常工作——给记忆系统做消防演习。

🔗 **断链防护（v3.1 新增）** — 最危险的失败不是出错，而是静默空转：cron 每天准时运行，但日记（唯一数据源）长期缺失，系统就在「每天准时地记录自己什么都没做」。v3.1 两端修复：①会话内触发信号（纠正/错误/新需求/正向反馈/关键决策）当场写入当日日记，禁止批末补写；②cron 发现日记缺失时，不再直接跳过，而是扫描当天三类真实痕迹（cron 留痕、长期记忆当日新增、工作区文件变更）重建日记再进入六步，严禁编造。

🛠️ **主动 Skill 合成** — 当同一领域≥3条经验聚类时，自动生成 Skill 草案（骨架+脚本框架），交人工确认。

⏰ **定时自动化** — 设置每日 cron 任务自动运行六步进化流程，周五额外执行周度反思。

📊 **跨环境支持** — 自动检测 OpenClaw、Claude Code 或其他 LLM Agent 环境，适配路径和调度方式。

---

### ✨ 核心亮点

#### 🔍 别光听 AI 自己说，拿数据验证

AI Agent 很擅长发现模式，但很难判断哪些模式值得永久记住。Agent 可能会说「我学到这条规则很重要！」——但你怎么知道它不是在幻觉式自信？

mu-self-evolve 把「提议」和「验证」分开。Agent 提议一条规则，然后 Python 脚本去查实际数据：这个错误复现了几次？跨了几个不同任务？提议的方案真的被确认有效吗？只有数据撑得住，规则才能写入永久记忆。

就像一个学生说自己掌握了某个知识点——你不能光听他说，得给他做套真题检验一下。

| 步骤 | 执行者 | 做什么 |
|------|--------|--------|
| 提议 | Agent | 「我发现这个模式反复出现」 |
| 验证 | 脚本 | 统计复现次数、跨任务数、解决率 → 置信度评分 0–100 |
| 提升 | 门控 | 置信度≥70 + 复现≥2 → 写入永久记忆 |

#### 🪶 记忆会像人脑一样遗忘

大多数记忆系统要么永远保留所有东西（直到你手动删除），要么按行数截断（文件太长就删最老的）。两种都不好：永远保留意味着噪声淹没信号；按行截断可能把一条关键规则删了，仅仅因为它比较老。

mu-self-evolve 用**时间衰减公式**——每条记忆的重要性分数会随时间自然下降，就像你忘了几个月前读过的书的细节，但对话中反复被提到的教训却记忆犹新。

被引用到的记忆会重置新鲜度。30 天没人碰的记忆分数减半。但在多个任务中被证明有用的记忆永久豁免——它们已经赢得了自己的位置。

```
effective_score = VFM × 0.5^(days_since_last_seen / 30)
```

#### 🏷️ 每个错误都有病历，不是只有描述

出错了，大多数系统记一条「Error: something failed」。这跟医生写「病人病了」一样——你知道出事了，但看不出规律。

mu-self-evolve 给每条错误打两个标签：**WHERE**（在哪一步出的？）和 **WHY**（根因是什么？）。这把一堆模糊的错误日志变成结构化矩阵，你可以一眼看出「哦，80% 的错误都发生在 MCP 调用阶段，根因都是 token 过期」。

**WHERE**（在哪出的）：`skill_load` · `mcp_call` · `file_write` · `api_call` · `browser_op` · `memory_op` · `agent_dispatch` · `prompt_parse` · `auth` · `other`

**WHY**（为什么出的）：`param_missing` · `token_expired` · `timing_race` · `perm_denied` · `knowledge_gap` · `format_mismatch` · `timeout` · `logic_error` · `config_drift` · `user_correction` · `other`

两组标签都可以自定义——随着 Agent 遇到新环境，你可以添加自己的标签。

#### 🧪 清道夫会给自己做体检

一个细思极恐的问题：如果记忆清理机制本身就坏了，在默默删除有价值的记忆，而表面上看一切正常呢？你永远不会知道——系统报告「已归档 5 条」，你信了，却没意识到其中 3 条本该保留。

mu-self-evolve 用**缺陷注入测试**来防御——**注入已知属性的假测试条目**——这些条目被设计成应该保留、应该归档、应该豁免的。跑完淘汰逻辑后，检查每条假条目是否被正确处理。任何一个不匹配都意味着淘汰逻辑有 bug。

就像质检员去检查质检员本身——如果检查机制自己就是坏的，一切看起来都正常但其实不正常。

---

### 📌 与同类工具对比

| 能力 | mu-self-evolve | 裸记忆文件 | 云端记忆 API | 向量数据库 |
|------|---------------|-----------|-------------|-----------|
| 每日自动沉淀 | ✅ 六步工作流 | ❌ 手动 | ❌ 仅 API | ❌ 需自行集成 |
| 断链防护 | ✅ 即时写入+兕底重建（v3.1） | ❌ | ❌ | ❌ |
| 确定性验算 | ✅ 脚本验证 | ❌ | ✌️ LLM 自评 | ❌ |
| 时间衰减淘汰 | ✅ 30天半衰期 | ❌ | ✌️ 有 | ✌️ 有 |
| 病理归档（WHERE×WHY） | ✅ 结构化标签 | ❌ | ❌ | ❌ |
| 评委偏差审计 | ✅ 缺陷注入 | ❌ | ❌ | ❌ |
| 主动 Skill 合成 | ✅ 聚类→草案 | ❌ | ❌ | ❌ |
| 跨环境支持 | ✅ OpenClaw + Claude Code | 不适用 | ❌ | ❌ |
| 无需外部 API | ✅ 完全本地 | ✅ | ❌ | ❌ |

---

### 🚀 六大工作流

| 工作流 | 场景 | 触发方式 |
|--------|------|---------|
| 每日进化（步骤1-6） | 提取今日经验、验算、提升、发摘要 | 定时 cron（每日） |
| 日记兕底补写（v3.1） | 日记缺失时扫描当日真实痕迹重建，防闭环空转 | 定时 cron 前置步骤 |
| 周度反思（步骤6a-6g） | 错误扫描、叙事生成、淘汰、Skill合成 | 周五（与每日合并） |
| 即时记录 | 用户纠正 Agent 或错误发生 | 触发检测（实时，当场写入日记） |
| 手动验算 | 检查某条规则的置信度 | `python3 vfm_verify.py <pattern-key>` |
| 淘汰审计 | 运行偏差测试+评分清理 | `python3 bias_audit.py && python3 eviction_score.py` |

---

### ⚙️ 技术规格

| 项目 | 说明 |
|------|------|
| 运行时 | Python 3.8+（仅脚本）；任意 LLM Agent（OpenClaw / Claude Code / Cursor） |
| 依赖 | 零外部依赖——仅用标准库 |
| 存储 | 本地 Markdown 文件（无数据库、无 API） |
| 脚本 | 4 个 Python 文件：`env_detect.py`、`vfm_verify.py`、`eviction_score.py`、`bias_audit.py` |
| 参考文档 | 4 个：`record-templates.md`、`weekly-reflection.md`、`file-structure.md`、`claude-code-compat.md` |
| 总体积 | ~45KB（不含 banner） |
| 调度 | `openclaw cron` 或系统 `crontab` |

---

### 🛠️ 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/muippt/mu-self-evolve.git

# 2. 初始化（自动检测环境）
cd mu-self-evolve
python3 scripts/env_detect.py --init

# 3. 设置定时进化
openclaw cron add --name "🧬 每日自我进化" --cron "30 19 * * *" --message "执行每日自我进化流程"
```

就这样。Agent 会开始每日沉淀经验、每周反思进化。

---

### 🔒 安全与隐私

- **100% 本地运行** — 所有数据留在工作区的 `.learnings/` 目录，无云端、无 API 调用、无遥测。
- **零外部依赖** — Python 脚本仅使用标准库。
- **不动模型参数** — 通过组织 Markdown 文本工作，不做微调或权重更新。
- **用户可控淘汰** — 每次归档决策都有日志；偏差审计确保透明度。

---

### ⭐ Star 趋势

如果 mu-self-evolve 帮助你的 Agent 变得更聪明，欢迎给个 Star ⭐

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-self-evolve&type=date)

> 一个会从自己的错误中学习的 AI Agent — 无需微调。

---

### 👤 作者简介

🎓 清华大学出版社签约作家 / 2026当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

---

### 📄 许可证与致谢

[MIT](LICENSE) © 2026 muippt

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 issue。
