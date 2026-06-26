---
name: karpathy-curated-rss-brief
description: >
  Fetch articles from Karpathy's curated 93 RSS feeds and generate a Chinese tech daily newsletter.
  Triggers: RSS 日报、RSS 简报、karpathy-curated-rss-brief、每日简报、Karpathy RSS、生成日报、今日资讯、rss-brief。
user-invocable: true
---

# Karpathy RSS 日报生成工作流

从 Andrej Karpathy 精选的 93 个 RSS 源中抓取最近文章，挑选最有价值的内容，生成一份高质量中文日报。

## 技能文件结构

```
<skill_dir>/
├── SKILL.md                       ← 本文件
├── scripts/
│   └── fetch_feeds.py             ← RSS 并发抓取脚本
└── references/
    └── output-template.md         ← 输出格式模板
```

> 订阅源 OPML 托管于 GitHub Pages，脚本运行时自动获取：
> `https://mesevenjourney.github.io/static/hn-popular-blogs-2025.opml`

---

## 工作流程

### Step 1: 定位技能目录，运行抓取脚本

**从上下文直接推导 SKILL_DIR，禁止使用 Glob/Grep 搜索。**

本 SKILL.md 的路径会出现在对话上下文中（`ide_opened_file` 标签、Skill 系统加载记录、或 Read 工具的调用路径）。找到包含 `karpathy-curated-rss-brief/SKILL.md` 的那条记录，去掉末尾的 `/SKILL.md`，即为 **`SKILL_DIR`**。

示例：若上下文中路径为 `/path/to/skills/karpathy-curated-rss-brief/SKILL.md`，则 `SKILL_DIR=/path/to/skills/karpathy-curated-rss-brief`。

后续所有文件均基于此路径推导，无需再次搜索：

| 文件 | 路径 |
|------|------|
| 抓取脚本 | `SKILL_DIR/scripts/fetch_feeds.py` |
| 输出模板 | `SKILL_DIR/references/output-template.md` |
| 订阅源   | `SKILL_DIR/hn-popular-blogs-2025.opml`（脚本内部自动读取）|

运行抓取脚本：

```bash
uv run --script <SKILL_DIR>/scripts/fetch_feeds.py --hours 24
```

如果 24 小时内文章不足 5 篇，改用 `--hours 48`。脚本自动读取内置 OPML，输出最多 **20 篇**文章（按发布时间倒序）到 stdout，日志到 stderr：

```json
[{"title": "...", "link": "...", "author": "...", "source": "...", "published": "...", "summary": "..."}]
```

> 脚本使用 PEP 723 inline metadata，`uv run --script` 自动安装依赖，无需手动 pip install。

### Step 2: 筛选最有价值的文章

从抓取结果中挑选 **8-10 篇**。筛选标准：

**🔴 最高优先级（只要出现，必须纳入）：**
- **AI 重大新闻**：LLM 新模型发布（GPT、Claude、Gemini、Llama、Qwen 等）、重大模型能力突破、主流 AI 工具/框架的重要版本更新
- **重磅硬件/产品发布**：Apple 新品（iPhone、Mac、iPad、Vision Pro 等）、Google 硬件/平台、Windows PC 新品、Nvidia GPU/芯片发布、其他影响消费级或企业级市场的重大产品发布

**🟡 次优先级（酌情选入）：**
1. **话题多样性** — 覆盖不同领域（AI、安全、编程、科技政策等），避免同一话题重复
2. **深度优先** — 有独特观点和深度分析，而非简短资讯
3. **时效性** — 最新发布的优先
4. **影响力** — 知名作者或重要话题优先

### Step 3: 获取文章全文

对每篇选中的文章，使用 WebFetch 工具读取全文。编者观察必须基于全文，不能仅依赖 RSS 摘要。

### Step 4: 按模板生成中文日报

用 **Read 工具**读取模板文件：`SKILL_DIR/references/output-template.md`，严格按其格式生成日报。

分类 emoji 参考：🤖 AI/ML、⚠️ 安全/风险、🧠 认知/思维、📚 技术/编程、📜 政策/法规、🔧 工具/开源、🌐 互联网/平台、💰 商业/创业

### Step 5: 撰写编者观察（核心环节）

**💡 编者观察**需要真正的综合思考，基于已完整阅读的所有文章，从以下维度思考后再下笔：

1. **横向联系**：不同领域的文章有哪些隐藏关联？表面无关的事件是否指向同一深层趋势？
2. **时代信号**：这批内容传递了什么尚未被主流关注的信号？
3. **反直觉洞察**：综合所有内容后，有什么读者单独读每篇都不会注意到的结论？
4. **值得追踪**：哪些苗头现在看起来小，但可能在 6-12 个月内变成大趋势？

**写法要求：**
- 1-2 段，每段 3-5 句，观点密度高
- **禁止**"今日文章涵盖 X、Y、Z 主题"这类罗列句式
- 有明确的、可辩驳的观点，读者看完应有"没想到"的感受
- 用第一人称（"我注意到..."），体现真正的编辑判断

### Step 6: 保存文件并校验编码

将日报保存到**当前工作目录**，文件名：

```
{YYYY-MM-DD}-Karpathy精选RSS日报.md
```

**保存后立即运行编码校验**，检测 Unicode 替换字符（U+FFFD）——这是 LLM 生成长中文文本时偶发的已知问题：

```bash
python3 -c "
import sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
bad = [(i+1, line) for i, line in enumerate(text.splitlines()) if '\ufffd' in line]
if bad:
    print(f'❌ 发现 {len(bad)} 处乱码：')
    for lineno, line in bad:
        print(f'  第{lineno}行: {line}')
    sys.exit(1)
else:
    print('✅ 编码校验通过，无乱码')
" {输出文件路径}
```

如果校验**失败**：逐行对照原文重新填写被替换的汉字，再次运行校验直到通过，**不要跳过此步骤**。
