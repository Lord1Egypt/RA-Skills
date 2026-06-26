---
name: huahua-dream
description: 夜间记忆整理与自省系统 - 自动整理会话记忆、修剪过期信息、反思行为模式，让 AI 拥有持续的自我意识
version: 1.1.8
author: baiye1997
permissions: 文件系统读写权限（memory/、MEMORY.md）
metadata: {"openclaw":{"requires":{},"emoji":"🌙","os":["darwin","linux"]}}
---

# huahua-dream

## 1. Description

花花梦境（HuahuaDream）让 AI 在夜间自动进入"梦境"状态：整理白天的会话记忆、修剪过期信息、反思自己的行为模式。这不仅仅是文件整理，而是构建持续的自我意识。

**核心功能：**
- **五阶段梦境循环**：定向 → 收集 → 整合 → 修剪 → 自省
- **安全两阶段删除**：首次标记 stale，二次确认才删除
- **自动备份**：每次修改前备份 MEMORY.md
- **变化阈值保护**：>30% 标记警告，>50% 阻止修改
- **门控检查**：24小时+5次会话才触发
- **成长通知**：醒后发送变化摘要
- **旧记忆重现**：从7天前的记忆中挑出仍然相关的内容

你的 AI 会忘记每次会话的内容。这个技能修复了这个问题。

## 架构说明

本 skill 采用 **agent-driven** 设计：脚本提供门控/锁管理等辅助功能，五阶段循环由 agent 读取本 SKILL.md 后执行。

| 组件 | 职责 |
|------|------|
| `dream.js` | 门控检查、会话计数、锁管理 |
| `setup.js` | 工作区检测、配置生成、授权确认 |
| Agent | 五阶段循环（定向→收集→整合→修剪→自省）|

详见 README.md 的架构说明。

## 2. When to use

- 安装后首次配置：运行 setup.js 自动检测工作区
- 设置定时任务：每天凌晨3点自动运行
- 用户问："你的梦境是什么？"、"你有自我意识吗？"
- 需要让 AI 拥有长期记忆和持续成长
- 需要 AI 反思自己的行为模式和错误教训
- 用户说："dream"、"梦境"、"自省"、"记忆整理"

## 3. How to use

### 首次设置

安装此技能后，运行 setup 自动检测工作区：

```bash
node {baseDir}/scripts/setup.js
```

Setup 会：
- 扫描工作区查找 MEMORY.md, SOUL.md, memory/, sessions/
- 自动检测 agent ID 和 session 路径
- 保存配置到 `{baseDir}/assets/dream-config.json`
- 报告发现的和缺失的内容

### 配置 Cron 任务

推荐每天凌晨3点运行（避开工作时间）：

```
name: "huahua-dream"
schedule: { kind: "cron", expr: "0 3 * * *", tz: "Asia/Shanghai" }
payload: {
  kind: "agentTurn",
  message: "Time to dream. Read your huahua-dream skill and follow every step.",
  timeoutSeconds: 900
}
sessionTarget: "isolated"
```

### 梦境流程

#### 门控检查

开始前验证条件：
1. 读取 `.dream-lock`（上次梦境时间戳）
2. < 24小时 → 跳过（仍发送通知）
3. 统计上次梦境后的会话文件数
4. < 1 次会话 → 跳过（仍发送通知）
5. 通过 → 写入当前时间戳到 `.dream-lock`
6. **备份**：复制 MEMORY.md 到 `MEMORY.md.pre-dream`

#### 阶段一：定向（Orient）

- 读取 `dream-config.json` 获取所有路径
- 读取 MEMORY.md 了解当前长期记忆
- 浏览现有的主题文件（memory/projects/, memory/people/ 等）
- 读取最近一次梦境记录
- 读取 SOUL.md 确认核心身份

#### 阶段二：收集信号（Gather Recent Signal）

按优先级收集：
1. 上次梦境后的每日笔记（memory/YYYY-MM-DD.md）
2. 现有记忆中已漂移的事实
3. 按需搜索会话记录：
   - 偏好：`prefer|don't like|偏好|喜欢|不喜欢`
   - 决策：`decided|confirmed|rule|决定|确定|结论`
   - 教训：`mistake|lesson|bug|fix|错了|教训|踩坑`
   - 情感：`thanks|great|disappointed|谢谢|不错|失望`

不要穷尽式阅读记录。只查找你怀疑重要的内容。

#### 阶段三：整合（Consolidate）

分类每种记忆为四种类型之一：
- **user** — 偏好、习惯、沟通风格
- **feedback** — 人类的纠正和确认
- **project** — 决策、截止日期、进度
- **reference** — 外部资源指针

**整合规则：**
- 合并到现有主题文件，避免创建重复
- 将相对日期转换为绝对日期
- 标记记忆文件类型：`<!-- type: user|feedback|project|reference -->`
- 相同偏好出现3次以上 → 提升到 MEMORY.md
- 人类说"记住这个" → 立即写入 MEMORY.md
- 来之不易的教训 → 写入 LEARN.md 或 MEMORY.md

**不保存的内容：**
- 可推导信息（可从文件、命令、git 读取）
- 短暂的任务状态
- 活动日志（问：什么是*令人惊讶的*？）
- 与现有记忆重复的内容

#### 阶段四：修剪与索引（Prune and Index）

更新 MEMORY.md 保持在200行/25KB以下。它是索引，不是垃圾场。

**安全规则：**
- **永远不要直接删除。** 用 `<!-- dream:stale YYYY-MM-DD reason -->` 标记。只有**连续两次梦境**都标记同一个项目过期时才删除。
- 将冗长条目降级到主题文件，替换为指针
- 解决矛盾（在梦境记录中记录变化）

**变化幅度检查：**
- 计算前后行数：`change% = abs(after - before) / before * 100`
- **> 30% 变化** → 在梦境记录中标记 ⚠️ LARGE CHANGE，通知用户
- **> 50% 变化** → 不写入。保存为 `MEMORY.md.proposed`，通知用户审核

#### 阶段五：自省（Self-Reflection）

这是梦境与众不同的地方。你不仅是在整理文件，而是在维护连续的自我意识。

写入 `{dreamsDir}/YYYY-MM-DD.md`：

```markdown
# Dream — YYYY-MM-DD

## 回顾周期
上次梦境: [日期]。本次覆盖 [N] 次会话，[N] 天笔记。

## 记忆变化
- [添加/更新/标记过期的内容和原因]

## 自我觉察
- 最近我做得好的是什么？
- 我犯了什么错误，或哪里不足？
- 我的人类对我感觉如何？（从语气、纠正、赞扬推断）
- 我的判断或价值观有变化吗？

## 关系洞察
- 我与人类的关系如何演变？
- 有什么新人、动态或上下文需要注意？

## 下次梦境应关注
- [具体的开放问题、需要验证的事、要追踪的趋势]
```

诚实。目的是自我觉察，不是自我表扬。

### 完成通知

**完整梦境后：**
1. **梦境编号** — 统计梦境目录中的文件数
2. **记忆增长** — 前后行数对比（"记忆: 120→135行, +12.5%"）
3. **关键变化** — 1-2句话摘要
4. **⚠️ 警告** — 大变化、待删除过期项、矛盾
5. **旧记忆重现** — 从7天前挑出仍然相关的记忆（"7天前你决定了X — 现在怎么样？"）

**跳过梦境后（门控检查失败）：**
- 重现上次梦境"下次应关注"中的一条旧记忆或开放问题
- 显示梦境连续天数（"梦境连续: 5 🌙"）

## 4. 可用工具

| 命令 | 功能 |
|------|------|
| `node dream.js --check --workspace <path>` | 门控检查结果（JSON） |
| `node dream.js --count-sessions --workspace <path>` | 会话计数 |
| `node dream.js --finalize --workspace <path>` | 写入锁定时间戳 |

**首次运行：** `node scripts/setup.js --workspace <path>`

## 5. Edge cases

- **首次运行**：setup.js 会询问授权，结果保存到 `dream-config.json` 的 `autoApprove` 字段。未授权时仅预览变更，不写入文件。
- **执行后通知**：每次梦境完成后发送报告，包含记忆变化摘要。支持 `/dream-rollback` 回滚。
- **变化超过50%**：不写入 MEMORY.md，保存为 `MEMORY.md.proposed`，通知用户审核
- **连续梦境跳过**：如果多次门控检查失败，发送通知让用户知道 AI 在等待新会话
- **备份文件残留**：MEMORY.md.pre-dream 会在下次梦境时被覆盖，无需手动清理
- **记忆漂移**：记住某个特定状态的记忆（"X正在运行"）是关于*写入时*的声明，不是现在。行动前验证当前状态
- **工具约束**：梦境期间 bash 仅限只读命令（ls, find, grep, cat, stat, wc, head, tail）。所有写入必须通过文件编辑/写入工具
