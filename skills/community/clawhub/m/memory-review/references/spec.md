# Memory Review 详细规范

## 扫描范围

- 默认扫描最近 5 天的日记
- 可通过参数自定义天数

## 知识识别规则

### 识别 5 类知识

| 类型 | 特征 | 存放位置 |
|------|------|----------|
| 设计决策 | "选择了 X 而不是 Y，因为 Z" | memory/knowledge/fw-*.md |
| 可复用经验 | "这个模式对 XXX 效果很好" | memory/knowledge/fw-*.md |
| 新术语 | 首次使用的内部术语 | memory/glossary.md |
| 实体变更 | 项目状态变更、新人物等 | memory/projects/*/ |
| 重复模式 | 同一个操作做了 3+ 次 | memory/knowledge/fw-*.md |

### 优先级判断

```
错误类 → 高优先级（立即沉淀）
新技能/工具 → 高优先级
配置优化 → 中优先级
经验总结 → 中优先级
待办/想法 → 低优先级（可延后）
```

## 增量扫描逻辑

使用 md5 比对判断是否有新内容需要扫描：

### 1. 读取上次状态

- 读取上次执行日志 `data/exec-logs/memory-review/` 目录下最新的文件
- 提取 `lastScanned` 字段：格式 `{ "date": "2026-03-16", "md5": "abc123" }`

### 2. 判断是否需要扫描

- 检查 memory/daily/ 目录下是否有比 lastScanned.date 更新的文件
- 如果有，需要扫描
- 如果没有，检查 lastScanned.date 对应文件的当前 md5 是否变化
- 如果 md5 变了，需要扫描
- 否则，跳过（没有新内容）

### 3. 计算 md5

```bash
md5sum memory/daily/YYYY-MM-DD.md
```

## 执行步骤

1. 读取上次的 lastScanned 状态
2. 按上述增量逻辑判断是否需要扫描
3. 如果需要扫描：
   - 扫描相关日记文件
   - 识别 5 类信号
   - 自动写入知识库
   - 生成报告
4. 如果不需要扫描：输出"无新内容"
5. 写入执行日志，包含新的 lastScanned 状态
6. 投递报告（读取 AGENTS.md/MEMORY.md 获取配置）

## 执行规则

1. 所有 shell 命令必须同步执行（不使用 background 参数）
2. 原子化写入输出文件：先写 .tmp 文件，然后 mv 到最终路径
3. 在生成进程退出前不要读取输出文件

## 报告格式

```markdown
# Memory Review 报告

**生成时间**: YYYY-MM-DD HH:MM
**扫描范围**: YYYY-MM-DD ~ YYYY-MM-DD

---

## 扫描结果

- 扫描了 X 天的日记
- 识别到 N 条知识

## 已自动沉淀

| 知识条目 | 位置 | 状态 |
|----------|------|------|
| xxx | memory/knowledge/fw-xxx.md | ✅ 已写入 |

## lastScanned 状态

```json
{
  "lastScanned": {
    "date": "YYYY-MM-DD",
    "md5": "abc123"
  }
}
```
```

## 投递规则

从 AGENTS.md 或 MEMORY.md 读取投递配置：

```markdown
## 报告投递

- 渠道：feishu
- 目标：<飞书群ID或用户ID>
```

如果配置中无投递信息，可以跳过投递或询问用户。
