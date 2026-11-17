# 优先级教练 · Priority Coach

优先级教练是一个温和、克制、不压迫的个人成长教练 skill。它不帮用户把一天排满，而是帮用户在混乱里看清 **现在最值得先顾的事**，并落到一个今天就能开始的最小动作。

当前版本 **v0.3.1**（基于 v0.3.0）。

## 0.3.1（2026-09-03 · staged 草案）

- **脚本说明补齐**：SKILL.md「资源 / scripts/」补充 `release_monitor.py` / `weekly_report.py` 用途说明——它们是仓库级维护者工具（发布 / 下载量监控、周报），不随 ClawHub 发布包分发，日常对话不触发，消除"悬空脚本"疑问
- **新增案例示意**：SKILL.md 末尾新增"案例示意"小节，用一个抽象化的多重身份（主业 + 内容副业 + 育儿）"忙但空"场景演示 cold_start → priority_select → today_plan 全流程，标注可替换为 Bonnie 真实记录
- 版本由 0.3.0 → 0.3.1（说明：GitHub 发布版尚为 0.2.3，本地 live 已是 0.3.0；本轮以本地 live 为基准递增）

## 0.3.0 新增：主线回顾与断更承接

- **断更承接**：用户停了一阵回来，不再从零冷启动——先读上次结果卡，问一句"还成立吗"，接上就走
- **主线重检**：对比多次记录，输出"稳住 / 漂走 / 建议下车"三栏主线重检卡，回答"我定的优先级还对不对"
- 不审判中断、不做打卡羞辱；回顾更新需用户同意，旧记录保留形成主线轨迹
- 详见 `references/review.md`

## 0.2.x 安全加固（相对 0.2.1）

- **全量 opt-in**：所有本地写入（会话摘要 + 完整结果卡）都必须先获得用户明确同意，未同意不落盘
- **能力边界声明**：SKILL.md 新增"能力与信任边界"一节，明确声明本 skill 不联网、不执行 shell、不读写自身数据目录之外的文件
- **发布包瘦身**：维护者用的迭代监控工具不再随发布包分发（见仓库内 `MAINTAINING.md`）
- **states.md 同步加固**：所有状态脚本的"记录动作"统一为同意后写入（0.2.3）
- ClawHub 安全扫描已通过（staticScan / SkillSpector / VirusTotal 均 clean）

`0.2.1` 相对 `0.1.2` 的主要变化：
- 从“默认先做 5 问”升级为“先路由、再进入状态”
- 新增 `overwhelmed_mode`，处理太乱、太累、选不动的场景
- 统一 OpenClaw 语境与本地记录路径
- 补齐完整状态脚本、最小记忆 schema 与发布文档

## 它能做什么

### 1. 收拢重点
帮助用户从“很多事缠在一起”里，收成当前最该优先的 1–3 件事。

### 2. 定一个今天可开始的动作
把重点落成一个 10–30 分钟可开始的最小动作，而不是一整份完美计划。

### 3. 陪用户过完整天，也接得住长周期
支持：
- `cold_start`
- `priority_select`
- `today_plan`
- `morning_start`
- `evening_wrap`
- `habit_checkin`
- `mainline_review`（主线回顾 / 断更承接）
- `overwhelmed_mode`

### 4. 本地保存结果
仅在用户同意时，保存结果卡到本地，方便下次续上。

## 与 0.1.2 相比的关键变化

- **入口改造**：不再默认所有会话都走完整冷启动，而是先判断用户当下最需要哪种帮助
- **过载降级**：新增低负担模式，不再强迫用户继续选 3 件事
- **脚本更完整**：每个状态都有标准脚本和 next step
- **文档更一致**：统一到 OpenClaw，而不是混用 WorkBuddy 文案
- **记录更稳**：优先写入 `~/.openclaw/data/priority-coach/records.json`，兼容旧版 `~/.workbuddy` 路径

## 目录结构

```text
priority-coach/
├── SKILL.md
├── README.md
├── skill-card.md
├── LICENSE
├── references/
│   ├── router.md
│   ├── states.md
│   ├── cold-start.md
│   ├── daily-flows.md
│   ├── review.md
│   ├── memory-schema.md
│   └── copy-tone.md
└── scripts/
    └── record.py
```

> 注：GitHub 开发仓库的 `scripts/` 下另有维护者工具 `release_monitor.py` / `weekly_report.py`，不随发布包分发，未列入上表；详见 SKILL.md「资源 / scripts/」与仓库 `MAINTAINING.md`。

## 在 OpenClaw 中使用

### 安装公开版
```bash
~/.openclaw/bin/openclaw skills install @bonniegeng-max/priority-coach
```

### 查看当前 skill 信息
```bash
~/.openclaw/bin/openclaw skills info priority-coach --json
```

### 本地覆盖 / 调试
如果要让本地版本优先生效，可把本目录内容回写到：

```text
~/.openclaw/workspace/skills/priority-coach
```

## 本地记录

本地记录脚本：
```bash
python3 scripts/record.py list
python3 scripts/record.py latest
python3 scripts/record.py path
```

默认数据路径：
```text
~/.openclaw/data/priority-coach/records.json
```

兼容旧路径：
```text
~/.workbuddy/priority-coach/records.json
```

> 规则：只有在用户明确同意“保存 / 记下来”的情况下，才调用保存。

## 隐私边界

- 默认不分享、不自动上传
- 默认只保存结果卡，不保存完整原始回答
- 分享给他人时，只暴露：3 个重点 + 今天最小行动 +（可选）我需要的支持
- 不暴露：原始回答、完整焦虑来源、敏感情绪细节

## 发布前检查建议

- 跑一遍 `cold_start -> priority_select -> today_plan`
- 跑一遍 `overwhelmed_mode`
- 跑一遍 `morning_start`
- 跑一遍 `evening_wrap`
- 试一次 `record.py add/list/latest/delete`
- 检查 README / skill-card / LICENSE / _meta.json 版本一致性

## License

MIT（见 `LICENSE`）。

> 注：ClawHub 的 skill 页会把许可证显示成 **MIT-0**——那是平台元数据的默认值，
> `clawhub publish` 没有提供指定许可证的参数，改不了。**本仓库的 `LICENSE` 文件才是准的。**
