---
name: memory-system
description: 自动记忆维护与知识提炼流水线：WAL写前日志→MEMORY.md→每日日志→Obsidian同步，含Insight Miner数据分析和双链发现
---

# 自动记忆维护与知识提炼流水线

## 架构

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 协议层 — 四层记忆 (WAL → MEMORY.md → 日志 → Obsidian)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① WAL（写前日志）→ 会话中实时记录
   触发信号：
   | 你说…                   | 写入段      |
   |------------------------|-------------|
   | 金额/退费/支付方式      | 记账        |
   | "用X吧"/"就这样定了"    | 决策        |
   | "不是X，是Y"            | 决策        |
   | "我喜欢"/"不喜欢"       | 决策        |
   | cron/配置/脚本变更      | 系统        |
   | 跨天要做的              | 待办        |

② MEMORY.md ← 长期教训索引，≤3KB，自动修剪 >7天
③ memory/YYYY-MM-DD.md ← 每日原始档案
④ Obsidian ← 永久归档

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 执行层 — MemCore
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  05:00  MemCore 晨间整理
        读取昨日日志 → 提取新教训 → 去重写入 MEMORY.md
        文件：{{workspace}}/memory/scripts/memcore_evening.sh

  22:00  MemCore 晚间整理
        检查：MEMORY.md 大小 / 今日日志 / WAL / 任务板
        脚本：bash {{workspace}}/memory/scripts/memcore_evening.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 提炼层 — Insight Miner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  22:30  每日提炼 → 刷新 {{workspace}}/memory/money.md
          净值 / 消费趋势 / 资产变动 / 待办 / 关键信号 / 双链建议

  周日 20:00  周报
          周趋势 + 深度双链发现 + 系统异常汇总
```

## 晚间流水线（22:00-23:30）

```
22:00  MemCore 晚间整理     ← memcore_evening.sh
22:15  教训筛选→MEMORY.md   ← 去重+修剪
22:30  Insight Miner 跑     ← 合成 money.md + 双链
23:00  晚间快照归档         ← snapshot-evening
23:15  配置快照             ← config-snapshot
23:30  Obsidian 同步推      ← obsidian-sync
```

## 数据源路径

| 用途 | 路径 |
|:----|:-----|
| WAL | `{{workspace}}/memory/SESSION-STATE.md` |
| 长期记忆 | `{{workspace}}/MEMORY.md` |
| 每日日志 | `{{workspace}}/memory/YYYY-MM-DD.md` |
| 任务板 | `{{workspace}}/memory/taskboard.md` |
| 财务提炼 | `{{workspace}}/memory/money.md` |
| 账本 CSV | `{{accounting_dir}}/2026-*.csv`（用户自定义） |
| 资产快照 | `{{vault}}/资产/总览/资产快照/` |
| Obsidian vault | `{{vault}}`（用户自定义） |
| 同步脚本 | `{{sync_script}}`（用户自定义） |
| MemCore 脚本 | `{{workspace}}/memory/scripts/memcore_evening.sh` |

## 每日提炼输出（money.md）

`{{workspace}}/memory/money.md` 结构：

```
📊 资产净值      ← 从 current_state + 快照
💳 消费趋势      ← 从账本 CSV
📈 本周资产变动   ← 从快照对比
🔄 待办待处理    ← 从 WAL 待办段
📌 关键信号      ← 从数据提炼
🧩 日记关联      ← 双链建议
```

## 双链发现规则

| 类型 | 匹配 |
|:----|:-----|
| 时间线链接 | 同日期：日记↔快照↔账本 |
| 事件↔影响 | "T+0盈利"↔"现金变更" |
| 教训↔实例 | MEMORY.md教训↔日志实践 |
| 资产↔凭证 | 资产变动↔银行票据 |

## 散会归档（7步流程）

1. 汇总结论 → 每日日志
2. 新教训→MEMORY.md（先grep去重，不超3KB）
3. 关键结论→SESSION-STATE.md
4. 更新任务板
5. 完整日志追加
6. 写快照标记
7. 检查WAL未处理条目

## 约束

- LM Studio 调用必须串行
- 新增数据只用追加，不覆盖
- MEMORY.md >3KB 时修剪 >7天的旧教训
- 不存图片文件，OCR内容逐笔以文本登记