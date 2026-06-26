---
name: jike-wechat-writer
version: 1.0.1
license: MIT
description: "微信公众号文章创作技能，覆盖从选题挖掘到排版发布的全流程。当用户表达任何文章创作意图时都应激活——包括但不限于"写一篇文章"、"帮我写篇推文"、"公众号内容创作"、"帮我出一篇稿"、"这个选题怎么写"、"把这些素材整理成文章"、"写个公众号推送"、"帮我出个内容"、"围绕XX写点东西"等。即使用户只是给了一堆链接或素材然后说"帮我整理一下"，只要上下文暗示了创作需求，也应触发。当用户提到热点借势、选题挖掘、风格模仿、文章排版等公众号创作子环节时同样适用。未指定目标平台时，默认以微信公众号作为输出平台。此技能提供公众号创作各环节的核心指导模块，由 agent 根据上下文灵活编排。"
metadata: {"openclaw": {"emoji": "✍️", "requires": {"bins": ["python3"]}, "primaryEnv": "100CITY_API_KEY"}}
---

# 微信公众号文章创作技能

Script: `python3 {baseDir}/scripts/writer.py`

本技能为微信公众号文章创作提供全流程的核心指导。它不是一个必须从头走到尾的线性工作流，而是由多个独立模块组成的**创作指导集**——agent 应根据用户当前所处的创作阶段和实际需求，灵活调用对应模块。

## 核心规则

1. **API Key 未配置 = 技能不可用，必须停止一切创作动作**
- 技能激活后第一步必须执行 `python3 {baseDir}/scripts/writer.py check` 确认 Key 配置状态。
- 如果 check 失败：**立即停止，只做一件事——告诉用户需要配置 Key，给出配置方法，然后等待用户完成配置。** 不要读模块文档，不要搜索热点，不要分析选题，不要用网络搜索替代，不要做任何创作相关的事情。
- 没有 Key 就没有热点聚合搜索、没有风格拆解、没有图片生成——整个创作流程无法运行，用网络搜索凑出来的内容不符合本技能的质量标准。
2. **通过脚本调用 API** — skill内的能力通过 `writer.py`和 `render.py` 脚本调用，因为脚本封装了 API 认证、错误处理和格式化输出，直接 curl 会缺少这些保障。
3. **API 失败最多重试 1 次** — 同一个接口连续失败 2 次后停止重试，告知用户原因并给出替代方案，避免无意义的等待。

## API Key Setup

编辑 `{baseDir}/scripts/config.json`，填写 `api_key`。或设置环境变量 `100CITY_API_KEY`。

快速检查：`python3 {baseDir}/scripts/writer.py check`

## Script Quick Reference

```bash
# 检查连接
python3 {baseDir}/scripts/writer.py check

# 统一搜索（news/wechat_article/image）
python3 {baseDir}/scripts/writer.py search --query "关键词" --action news
python3 {baseDir}/scripts/writer.py search --query "关键词" --action wechat_article

# 获取最新热点新闻
python3 {baseDir}/scripts/writer.py trend

# 关键词热点总结
python3 {baseDir}/scripts/writer.py trend-summary --keyword "关键词"

# 按公众号名称拆解创作风格
python3 {baseDir}/scripts/writer.py style-by-name --name "公众号名称"

# 按文章链接拆解创作风格
python3 {baseDir}/scripts/writer.py style-by-url --url "文章链接"

# AI 生成图片
python3 {baseDir}/scripts/writer.py generate-image --prompt "图片描述"
python3 {baseDir}/scripts/writer.py generate-image --prompt "图片描述" --ratio 16:9
python3 {baseDir}/scripts/writer.py generate-image --prompt "图片描述" --ref-url "参考图URL"
```

所有命令支持 `--json` 获取原始 JSON 输出。

Script: `python3 {baseDir}/scripts/render.py`

```bash
# 渲染 MD 为带样式的 HTML（微信公众号排版）
python3 {baseDir}/scripts/render.py render article.md --theme blue-minimal -o article.html

# 查看可用主题
python3 {baseDir}/scripts/render.py list-themes

# 从公众号文章链接拆解排版样式
python3 {baseDir}/scripts/render.py extract-style "https://mp.weixin.qq.com/s/xxxxx" --name "主题名" --id theme-id
```

## 模块总览

| 模块 | 职责 | 何时激活 | 详细文档 |
| --- | --- | --- | --- |
| A. 选题与方向确认 | 从上下文中提炼创作方向 | 创作起点，每次必经 | `{baseDir}/references/module-a-topic.md` |
| B. 记忆适配 | 读取用户行业背景、品牌资产与创作历史 | MEMORY.md 或 MEMORY/ 目录存在时 | `{baseDir}/references/module-b-memory.md` |
| C. 风格遵循 | 获取并遵循目标公众号的创作风格 | 选题确认后、正文创作前 | `{baseDir}/references/module-c-style.md` |
| D. 正文创作与迭代 | 产出 MD 文件并与用户迭代 | 核心创作环节 | `{baseDir}/references/module-d-writing.md` |
| E. 配图策略 | 将占位标记替换为真实图片 | 文案确认后、渲染排版前 | `{baseDir}/references/module-e-image.md` |
| F. 公众号样式应用 | 通过 render.py 生成带排版样式的 HTML，支持从公众号文章拆解自定义样式 | 用户要求公众号排版样式时 | `{baseDir}/references/module-f-styling.md` |

进入某个模块的详细执行时，读取对应的 reference 文件获取完整指导。

## 模块间协作关系

```
用户发起创作请求
    │
    ▼
[模块 A] 选题与方向确认 ← 创作入口
    │
    ├── 存在 MEMORY.md / MEMORY/ ？──→ [模块 B] 记忆适配（隐式融入创作）
    │
    ▼
[模块 C] 风格确认 ← 选题确认后、正文创作前
    │   检查 MEMORY.md 是否有风格偏好
    │   ├── 有 → 读取风格报告，遵循创作
    │   ├── 无 → 询问用户是否模仿某公众号
    │   │       ├── 用户提供名称/链接 → 拆解风格 → 保存到 MEMORY.md
    │   │       └── 用户不需要 → 使用公众号爆文默认风格
    │
    ▼
[模块 D] 正文创作与迭代 ← 核心环节（在风格框架确定后开始）
    │   D2 撰写时在配图位置插入 <!-- IMG: 描述 --> 占位
    │
    ├── 用户确认文案 ──→ 可选：进入配图
    │
    ├── 用户要求公众号样式？──→ [模块 F] 公众号样式应用（render.py，占位图自动填充）
    │
    ▼
[模块 E] 配图策略（read .md → 扫描占位 → search/generate → 替换为真实图片）
    │   ⚠️ 消耗算力，仅在用户明确要求时执行
    │
    ├── 配图完成后可重新执行模块 F 渲染最终版
    │
    └── 创作完成
```

## 模块执行说明

- 模块 A 和模块 C 是正文创作前的两个关键环节，因为选题方向和风格框架直接决定了正文质量
- 模块 C 的三种结果（已有风格 / 拆解新风格 / 爆文默认风格）都会产出一套明确的写作框架，模块 D 在此框架下创作
- 模块 B 不产出独立交付物，隐式融入创作过程
- 模块 C 的配图习惯会传递给模块 D（占位描述）和模块 E（图片风格选择）
- 模块 D 专注文案质量，配图以占位标记形式预留位置；模块 E 在用户明确要求时执行配图替换（消耗算力，不擅自执行）
- 模块 F 不要求配图完成——`.md` 中的 `<!-- IMG: -->` 占位标记会被渲染为占位图片并保留描述文字，后续可随时配图后重新渲染
- 整个流程中，用户随时可以要求回到任意模块进行调整