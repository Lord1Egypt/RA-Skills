# OpenCard 数据流

## 卡片字段总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OpenCard 名片                                │
│                                                                     │
│  ┌─ 左侧 ─────────────────────┐  ┌─ 右侧 ──────────────────────┐  │
│  │                             │  │                              │  │
│  │  display_name               │  │  default_model    (stat卡)   │  │
│  │  role_title                 │  │  token_30d_short  (stat卡)   │  │
│  │  recent_focus          [AI] │  │                              │  │
│  │  openclaw_review       [AI] │  │  skill_names      (chips区)  │  │
│  │                             │  │  platform_chips   (chips区)  │  │
│  │                             │  │                              │  │
│  │                             │  │  timezone              [AI]  │  │
│  │                             │  │  generated_at                │  │
│  └─────────────────────────────┘  └──────────────────────────────┘  │
│                                                                     │
│  [AI] = 由大模型生成      无标记 = 由脚本直接提取                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 脚本直接提取的字段（确定性数据）

```
字段              源文件                                    提取方式
─────────────────────────────────────────────────────────────────────

display_name      ~/.openclaw/workspace/USER.md             读取 **Name:** 字段
                                                            fallback → "Unknown"

role_title        ~/.openclaw/workspace/USER.md             读取 **Notes:** 字段
                                                            按 ；; 分割取前 2 段
                                                            用 · 连接，截断到 20 字符
                                                            fallback → ""

timezone_raw      ~/.openclaw/workspace/USER.md             读取 **Timezone:** 字段
                                                            fallback → "Asia/Shanghai"

default_model     ~/.openclaw/openclaw.json                 读取 agents.defaults.model.primary
                                                            去掉 provider 前缀，保留模型名
                                                            fallback → "Unknown"

token_30d         ~/.openclaw/agents/main/sessions/*.jsonl  遍历所有 .jsonl 文件
                                                            只读 type=message 的记录
                                                            累加 usage.totalTokens
                                                            仅统计最近 30 天内的记录

skill_names       ~/.openclaw/skills/                       遍历目录，收集非隐藏子文件夹名
                  ~/.openclaw/workspace/skills/             两个路径去重合并，返回排序列表

skills_count      （由 skill_names 计算）                   len(skill_names)

platforms         ~/.openclaw/agents/main/sessions/         读取 sessions.json
                  sessions.json                             从 session key 第 3 段提取平台
                                                            + deliveryContext.channel
                                                            + origin.provider / origin.surface
                                                            通过 PLATFORM_LABELS 映射显示名
                                                            （feishu→飞书, discord→Discord,
                                                             webchat→Web, tui→终端）

platform_count    （由 render 脚本计算）                     len(platforms)

token_30d_short   （由 render 脚本格式化）                   去掉 " tokens" 后缀
                                                            如 "6.2M tokens" → "6.2M"

generated_at      （运行时生成）                             当天日期 YYYY-MM-DD
```

## AI 生成的字段

```
字段              输入素材                                   生成规则
─────────────────────────────────────────────────────────────────────

timezone          timezone_raw (来自 USER.md)               IANA 时区 → 城市名
                                                            如 Asia/Shanghai → 上海
                                                            fallback → 渲染为空

recent_focus      copy_inputs.user_md_excerpt               1-2 句话描述用户近况
                  copy_inputs.memory_md_excerpt              ≤ 25 个中文字
                  copy_inputs.memory_bullets                 fallback → USER.md Notes 正则提取

openclaw_review   copy_inputs.user_md_excerpt               犀利点评，有观点有论据
                  copy_inputs.identity_md_excerpt            ≤ 35 个中文字
                  copy_inputs.memory_md_excerpt              fallback → "一个对 AI 有自己想法的人。"
                  copy_inputs.memory_bullets
                  copy_inputs.stats_summary
```

## 完整执行流程

```
用户说"帮我生成名片"
        │
        ▼
┌──────────────────────┐
│  collect-data.py     │  读取本地文件，输出 JSON
│                      │  包含确定性字段 + copy_inputs 素材
└──────────┬───────────┘
           │ JSON 输出
           ▼
┌──────────────────────┐
│  AI 阅读 JSON        │  基于 copy_inputs 中的素材
│  + SKILL.md 指令     │  生成 4 个字段：
│                      │  timezone / recent_focus /
│                      │  openclaw_review
│                      │  写回 JSON
└──────────┬───────────┘
           │ 补全后的 JSON
           ▼
┌──────────────────────────────┐
│  render-background-card.py   │  读取 JSON + HTML 模板
│                              │  填充占位符，输出 HTML 预览
│                              │  （如果 AI 字段为空，自动用 fallback）
└──────────┬───────────────────┘
           │ HTML 文件
           ▼
┌──────────────────────────────┐
│  用户在浏览器预览 + 迭代      │
└──────────┬───────────────────┘
           │ 确认 OK
           ▼
┌──────────────────────────────┐
│  export-background-card.sh   │  Playwright + Chrome
│                              │  HTML → PNG (1200×800 @2x)
└──────────────────────────────┘
```

## 本地文件依赖汇总

```
~/.openclaw/
├── openclaw.json                          → default_model
├── workspace/
│   ├── USER.md                            → display_name, role_title, timezone_raw
│   │                                        + AI 素材 (user_md_excerpt)
│   ├── IDENTITY.md                        → AI 素材 (identity_md_excerpt)
│   ├── MEMORY.md                          → AI 素材 (memory_md_excerpt, memory_bullets)
│   └── memory/*.md                        → AI 素材 (memory_bullets 补充)
├── skills/                                → skill_names, skills_count
└── agents/main/sessions/
    ├── sessions.json                      → platforms
    └── *.jsonl                            → token_30d
```
