# OpenClaw 记忆问题排查指南

## 常见问题诊断流程

### 问题 1：龙虾失忆了

**症状**：Agent 忘记之前的对话、决策、约束

**诊断步骤**：

```
1. 检查 Memory Flush 是否启用
   └─ 查看配置: agents.defaults.compaction.memoryFlush.enabled
   
2. 检查 MEMORY.md 内容
   └─ 是否存在关键信息？
   └─ 关键信息是否在开头/结尾？
   
3. 检查 daily logs
   └─ 是否有当天的日志？
   └─ 日志是否过于臃肿？
   
4. 检查上下文长度
   └─ 是否触发过 compaction？
   └─ 是否超出模型窗口限制？
```

**解决方案**：

```bash
# 一键修复
bash scripts/install.sh

# 或手动配置
# 在 openclaw.json 中启用 memoryFlush
```

---

### 问题 2：Token 消耗过高

**症状**：API 费用快速增长，对话成本高

**诊断步骤**：

```
1. 检查 MEMORY.md 行数
   └─ 超过 500 行需要精简
   
2. 检查 daily logs 数量
   └─ 超过 30 天的日志需要归档
   
3. 检查上下文配置
   └─ reserveTokensFloor 是否合理？
   
4. 检查会话模式
   └─ 是否频繁开启新会话？
```

**解决方案**：

```bash
# 优化记忆文件
bash scripts/optimize_memory.sh

# 安装搜索增强，按需检索
clawhub install qmd
```

---

### 问题 3：记忆搜不到

**症状**：Agent 找不到之前存储的信息

**诊断步骤**：

```
1. 检查文件是否存在
   └─ MEMORY.md 是否存在？
   └─ memory/ 目录是否有日志？
   
2. 检查搜索能力
   └─ 原生 SQLite 搜索能力有限
   └─ 是否需要语义搜索？
```

**解决方案**：

```bash
# 安装 qmd 搜索增强
clawhub install qmd
```

---

### 问题 4：Compaction 丢失信息

**症状**：压缩后关键约束丢失

**原因**：
- Memory Flush 未启用
- 关键信息未写入 durable memory
- 压缩策略过于激进

**解决方案**：

```json
// 配置 openclaw.json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

---

## 一键诊断命令

```bash
# 运行诊断脚本
bash scripts/diagnose.sh
```

输出示例：
```
🏥 OpenClaw 记忆系统诊断
═══════════════════════════════════════════════════════

🔍 检查 Memory Flush 配置...
   ✅ Memory Flush 已启用

🔍 检查 MEMORY.md...
   ✅ MEMORY.md 行数正常: 120 行 (3.2K)

📋 发现 2 个优化建议：
   1. 将关键决策、重要规则放在 MEMORY.md 开头
   2. (可选) 安装 qmd: clawhub install qmd
```

---

## 预防措施

### 每日检查

- [ ] Memory Flush 是否正常工作
- [ ] 今日日志是否正常追加

### 每周维护

- [ ] 精炼 MEMORY.md
- [ ] 归档旧日志
- [ ] 运行诊断脚本

### 每月检查

- [ ] 备份记忆文件
- [ ] 检查 Token 消耗趋势
- [ ] 更新关键决策记录

---

## 紧急恢复

如果记忆完全丢失：

```bash
# 1. 检查备份
ls ~/.openclaw/memory-backups/

# 2. 恢复最近的备份
bash scripts/restore_memory.sh

# 3. 如果没有备份，检查 Git
cd ~/.openclaw/workspace
git log --oneline
git checkout HEAD~1 -- MEMORY.md
```