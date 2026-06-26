# /novel fail-log - 失败记录与优化

## 触发方式

```
/novel fail-log add <问题描述>
/novel fail-log list
/novel fail-log review
```

或对话式：
```
记录这次问题
查看失败记录
```

---

## 功能

记录写作过程中出现的穿帮、矛盾、崩塌等问题，持续优化后续创作质量。

---

## 核心文件

```
<项目名>/
└── .fail-log/
    ├── yyyy-MM-dd.md   # 按日期分文件
    └── summary.md      # 问题汇总索引
```

---

## 问题分类

| 类型 | 说明 |
|------|------|
| `contradiction` | 前后矛盾（角色设定、时间线等） |
| `foreshadow-broken` | 伏笔提前揭晓/未揭晓 |
| `character-inconsistent` | 角色性格/行为不一致 |
| `timeline-error` | 时间线错误 |
| `plot-hole` | 情节漏洞 |
| `pacing-issue` | 节奏问题 |
| `ai-detection` | 被AI检测出的表达 |

---

## fail-log add

当追踪验证失败或质量分析失败时，自动追加到当日记录：

```
## [contradiction] 角色性格前后不一致

**章节**：第3章
**发现时间**：2026-04-14
**问题描述**：
- 第2章设定女主"性格内向"
- 第3章却写她"主动搭话陌生人"

**影响范围**：第3章
**修复建议**：修改第3章女主行为，改为"在朋友介绍下才开口"

**后续预防**：后续章节注意内向性格的表现方式
```

---

## fail-log review

**每次 `/novel write` 前必读**（预防同类问题）

```
📖 失败记录复习

最近失败记录（共3条）：
1. [contradiction] 第2章：角色性格内向→外向突变
   → 预防：性格转变需要过渡场景
2. [timeline-error] 第3章：出现了第5年才发生的事
   → 预防：写作前对照 timeline.md
3. [ai-detection] 第4章：使用了"唯一的""直到"等词
   → 预防：对照 anti-ai 禁用词表

✅ 检查完成，未发现当前章节相关问题
```

---

## 输出格式

### fail-log list

```
📋 失败记录汇总

总计：8条

contradiction     : 2条
foreshadow-broken : 1条
character-inconsistent : 1条
timeline-error    : 1条
pacing-issue      : 2条
ai-detection      : 1条

最新记录（2026-04-14）：
  - [contradiction] 第3章角色性格问题
```

---

## 自动化规则

- **每次 track --check 失败**：自动追加一条到 fail-log
- **每次 analyze 失败**：自动追加一条到 fail-log
- **每次 write 前**：自动读取 .fail-log/recent 预防
