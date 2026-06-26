# llm-daily-digest · 大模型每日简报 skill

一个 **OpenClaw skill**，让你的 OpenClaw agent 每天自动采集、筛选、汇总 LLM / 大模型领域的关键动态，产出一份中文 Markdown 简报——**标题叫 "🗣️ 今天 AI 圈发生了啥"**。设计目标是"一份能让我在地铁上 5 分钟读完、又不漏掉当天真正重要的事"的日报。

## 📡 覆盖的 14 个抓取入口

- **🏢 头部厂商官方博客（最高优先级一手源，8 家）**：
  - 🌐 **海外**：OpenAI、Anthropic、Google DeepMind / Google AI、Meta AI（Llama）、xAI（Grok）、Mistral AI
  - 🇨🇳 **国内**：DeepSeek、通义千问 Qwen（阿里）
- **📦 GitHub Trending**（daily，多语言）
- **📄 arXiv**(cs.CL / cs.AI / cs.LG / cs.CV)
- **🤗 Hugging Face**（models trending + daily papers）
- **📊 Papers With Code**
- **💬 Hacker News**
- **𝕏 Twitter/X**（带降级策略）
- **🇨🇳 机器之心** + **量子位**

覆盖四类内容：**厂商官方发布 / 新开源项目 / 新论文 / 行业资讯**。

## 📦 安装

把整个 `llm-daily-digest/` 目录放到 OpenClaw workspace 的 skills 目录下：

```bash
# 假设你已经把这个 skill 解压到了本地
cp -r llm-daily-digest ~/.openclaw/workspace/skills/

# 验证
ls ~/.openclaw/workspace/skills/llm-daily-digest/
# 应该能看到 SKILL.md 和 README.md
```

然后重启 OpenClaw Gateway 让它扫描到新 skill：

```bash
openclaw gateway stop && openclaw gateway --port 18789
# 或如果装了 daemon，用对应的 launchctl / systemctl restart
```

> OpenClaw 启动时会自动扫描 `~/.openclaw/workspace/skills/` 下所有 skill，不需要额外注册。参考 https://docs.openclaw.ai/tools/skills

## 🧪 手动跑一次（先验证通不通）

在 OpenClaw 的任一会话/频道里发消息：

```
今天 AI 圈发生了啥
```

或者任一等价说法：`跑一下今天的大模型日报` / `总结一下今天 AI 动态` / `给我一份 LLM 快报` 都行。

agent 应该：
1. 识别并加载本 skill
2. 并行抓取 14 个入口
3. 去重、筛选、归类、打分
4. 生成 `~/.openclaw/workspace/digests/YYYY-MM-DD.md`
5. 回消息告诉你文件路径 + 今日 3 条精选 + 采集统计

如果某些源失败（比如 X/Twitter 登录墙），skill 会自动跳过并在简报末尾注明，这是正常的。

## ⏰ 配置每日定时任务

详见 OpenClaw cron 文档：https://docs.openclaw.ai/automation/cron-jobs

核心思路是配置一条 cron，让它每天早上给 agent 发 `今天 AI 圈发生了啥` 这条消息。推荐时间：**北京时间早上 8-10 点**（避开 UTC 日期切换的时间）。

## 📂 产出文件

简报保存在：`~/.openclaw/workspace/digests/YYYY-MM-DD.md`

结构（空分区会智能省略）：

- 🔥 今日要闻（3-5 条，跨来源去重精选）
- 🏢 厂商官方发布（8 家每天必查，无发布也留白证明"查过了"）
  - 🌐 海外：OpenAI / Anthropic / Google / Meta / xAI / Mistral
  - 🇨🇳 国内：DeepSeek / Qwen
- 📦 GitHub 新项目 / 趋势
- 📄 arXiv 新论文
- 🤗 Hugging Face
- 📊 Papers With Code
- 💬 社区热议（HN + X，X 传言会 ⚠️ 隔离）
- 🇨🇳 中文媒体精选
- 📝 编者按（可选）

## 🔧 自定义

如果要改关注的关键词、信息源、或者输出格式，直接编辑 `SKILL.md`：

- **加来源** → 在"来源清单"章节加一节
- **改关键词** → 修改每个来源下的"筛选关键词"
- **改输出格式** → 改"输出结构"里的模板
- **改时间窗** → 改"核心工作流"第 1 步

## 🐛 调试

- agent 说它采不到内容？检查 OpenClaw 的 `browser` 工具是否启用，以及网络是否可达。
- 简报内容重复度高？"筛选与质量标准"里的去重规则可能需要收紧。
- 某个源总是抓不到？把它从 `SKILL.md` 的"来源清单"里暂时删掉，或加强"降级策略"。
- agent 没触发 skill？在消息里更明确地说"使用 llm-daily-digest skill 生成今日简报"。
