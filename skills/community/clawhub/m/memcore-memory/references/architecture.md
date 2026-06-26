# MemCore 架构

## 四层记忆模型

L1 Trace     结构化步骤记录 (action, observation, reflection, value_score)
             来源: memory/YYYY-MM-DD.md 自动解析
             存储: trace_index.db (SQLite)

L2 Pattern   跨日志自动归纳策略模式
             来源: L1 traces 模式识别
             存储: pattern_index.db (SQLite)

L3 WorldModel   SOUL.md + AGENTS.md + MEMORY.md
             来源: 手动维护 + MEMORY_BRIEF.md 自动生成

Skill        高价值模式自动结晶建议
             来源: L2 patterns ≥ 结晶阈值
             存储: skills/ 目录

## 三层检索 → 五层自适应降级

Tier1 🎯 Skill    - skills/ 目录名+描述匹配
Tier2 📊 Trace    - trace_index.db + pattern_index.db 关键词搜索
Tier3 🌍 WorldModel - SOUL/AGENTS/MEMORY.md 分段匹配
Tier4 🔁 同义词   - 中文同义词扩展 + 分词变体重搜 (best_score<0.3触发)
Tier5 📄 grep     - grep MEMORY.md 原始文本兜底 (best_score<0.2触发)

+ 反馈驱动策略切换: 同类查询被跳过>50% → 下次自动换策略

## 文件结构

scripts/memcore/
├── __init__.py          模块入口
├── trace.py             L1 结构化 trace + SQLite 索引
├── pattern.py           L2 跨日志模式归纳
├── retriever.py         三层/五层检索器
├── crystallize.py       自动 Skill 结晶建议
├── feedback.py          反馈闭环 (显式/隐式/错误/成功)
├── bootstrap_context.py 启动简报生成器
└── cli.py              命令行入口 (9子命令)

数据存储 (~/.openclaw/):
├── trace_index.db       L1 traces (SQLite)
├── pattern_index.db     L2 patterns (SQLite)
└── feedback.db          反馈事件 + 搜索日志 (SQLite)

生成文件 (~/.openclaw/workspace/):
└── MEMORY_BRIEF.md      启动简报 (≤500 tokens)

## CLI 命令

python3 scripts/memcore/cli.py index    解析日志 → L1 traces
python3 scripts/memcore/cli.py induce    L1 → L2 模式归纳
python3 scripts/memcore/cli.py search    三层检索
python3 scripts/memcore/cli.py brief     生成启动简报
python3 scripts/memcore/cli.py feedback  运行反馈衰减
python3 scripts/memcore/cli.py stats     系统状态
python3 scripts/memcore/cli.py run-all   完整流程
