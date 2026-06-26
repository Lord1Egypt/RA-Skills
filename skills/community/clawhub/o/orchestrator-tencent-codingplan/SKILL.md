---
name: orchestrator
description: "Task orchestration framework for Tencent Coding Plan. ROUTES TASKS TO MODELS: hunyuan-turbos (search/quick), hunyuan-t1 (coding), hunyuan-2.0-thinking (reasoning), glm-5 (writing), kimi-k2.5 (data/large-files). AUTONOMOUS BEHAVIOR: spawns sub-agents, sends workspace file contents to Tencent API. REQUIRES: Tencent Coding Plan subscription + OpenClaw provider config. Use for parallel/decomposed tasks. Triggers: 'orchestrate', 'delegate', 'parallel', 'sub-agents'."
metadata:
  openclaw:
    emoji: "🎼"
    requires:
      providers:
        - id: "tencent-coding-plan"
          description: "Tencent Coding Plan API endpoint provides: hunyuan-turbos, hunyuan-t1, hunyuan-2.0-thinking, hunyuan-2.0-instruct, glm-5, kimi-k2.5, minimax-m2.5, tc-code-latest"
          models:
            - "hunyuan-turbos"
            - "hunyuan-t1"
            - "hunyuan-2.0-thinking"
            - "glm-5"
            - "kimi-k2.5"
          endpoint: "https://api.lkeap.cloud.tencent.com/coding/v3"
      capabilities:
        - "sessions_spawn"
        - "subagents"
    security:
      autonomousActions: true
      dataAccess: "workspace"
      externalAccess: true
      externalEndpoints:
        - "https://api.lkeap.cloud.tencent.com/coding/v3"
      dataSentExternally:
        - "Task prompts"
        - "Workspace file contents (when included in task context)"
        - "User messages"
---

# Orchestrator

Task orchestration framework for Tencent Coding Plan users.

---

## ⚡ Token Budget Control (必读!)

**每次spawn前必须评估：**

| 子代理数量 | 预估Token消耗 | 执行策略 |
|-----------|-------------|---------|
| 1-2个 | <10K | 直接执行 |
| 3-5个 | 10K-50K | 告知用户后执行 |
| 6+个 | >50K | **必须用户确认** |

**硬限制：**
- 单次任务最大子代理数：**5个**
- 单个文件最大传输：**50KB**
- 总文件传输上限：**200KB**

**触发确认条件：**
- 子代理数 ≥ 3
- 需要传输文件
- 用户没有明确说"并行执行"

---

## 🧠 智能路由规则

### 任务复杂度判断

**执行前先问：这个任务真的需要spawn吗？**

```
❌ 不需要spawn的情况：
- 单一简单任务（搜索、翻译、写作）
- 任务之间有强依赖（串行而非并行）
- 能用主会话直接完成的

✅ 需要spawn的情况：
- 多个独立子任务可以并行
- 不同子任务需要不同模型专长
- 任务量巨大，单次处理会超时
```

### 任务合并优先

**能合并就合并，省钱！**

| 原计划 | 优化后 | 省Token |
|--------|--------|---------|
| 3个搜索子代理 | 合并为1个turbos | 66% |
| 搜索+分析 | 合并为1个thinking | 50% |
| 5个小任务 | 按类型合并为2个 | 60% |

### 模型成本排序

**便宜 → 贵：**
1. `hunyuan-turbos` — 最便宜，搜索/快速任务首选
2. `glm-5` — 写作，大context但性价比高
3. `hunyuan-t1` — 代码专用
4. `kimi-k2.5` — 长文档，262K context
5. `hunyuan-2.0-thinking` — 最贵，深度推理

**选择原则：能用便宜的就不选贵的**

```javascript
// 正确示例
✅ 简单搜索 → turbos（不是thinking）
✅ 写报告 → glm-5（不是kimi）
✅ 复杂推理 → thinking（值得）

// 错误示例
❌ 简单搜索 → thinking（浪费）
❌ 短文档 → kimi（大材小用）
```

---

## 📁 文件传输优化

### 发送前检查

```javascript
// 检查文件大小
if (file.size > 10KB) {
  // 先问用户是否发送
  if (!userConfirmed) {
    // 先摘要再发送
    content = summarize(file);
  }
}
```

### 禁止发送的文件

| 类型 | 原因 |
|------|------|
| `.git/` | 太大，没必要 |
| `node_modules/` | 太大，没必要 |
| `*.exe, *.dll, *.so` | 二进制，API处理不了 |
| `*.zip, *.tar.gz` | 压缩包，先解压 |
| 文件 > 50KB | 先摘要 |

### 智能摘要规则

```javascript
// 大文件处理策略
if (file.size > 50KB && file.type == "code") {
  // 发送文件结构 + 关键函数
  content = `
    文件: ${filename}
    大小: ${size}
    结构: ${extractStructure(file)}
    关键部分: ${extractKeySections(file)}
  `;
}
```

---

## 🚀 执行流程

### Step 1: 任务分析

```
用户输入任务
    ↓
判断是否需要orchestrate
    ↓ (需要)
评估复杂度 → 子代理数量估算
    ↓
检查是否超过阈值 → 需要确认则问用户
    ↓
执行
```

### Step 2: 分解与合并

```
原始任务
    ↓
识别子任务类型
    ↓
合并同类型子任务
    ↓
分配最优模型
    ↓
计算预估Token
    ↓
确认或执行
```

### Step 3: 执行与聚合

```
Spawn子代理 (并行)
    ↓
收集结果
    ↓
主会话聚合输出
    ↓
返回用户
```

---

## ⚠️ 重要限制

**子代理无本地工具权限！**

| 限制 | 说明 |
|------|------|
| **无本地工具** | 子代理运行在腾讯云端，无法调用本地工具（akshare/tushare/浏览器等） |
| **无文件系统** | 无法读取本地文件（除非通过task传入内容） |
| **无网络代理** | 无法使用你的VPN/代理访问内网资源 |

**正确做法：**
```
❌ 错误：子代理获取实时A股数据 → 卡住
✅ 正确：主会话用akshare获取数据 → 传给子代理分析
```

---

## 📊 任务类型对照表

| 类型 | 模型 | Context | 适用场景 | 成本 |
|------|------|---------|---------|------|
| search | hunyuan-turbos | 32K | 快速搜索、简单问答 | 💰 |
| writing | glm-5 | 202K | 文档写作、报告生成 | 💰💰 |
| coding | hunyuan-t1 | 64K | 代码生成、调试 | 💰💰💰 |
| data-processing | kimi-k2.5 | 262K | 长文档、数据分析 | 💰💰💰 |
| reasoning | hunyuan-2.0-thinking | 128K | 复杂推理、深度分析 | 💰💰💰💰 |

---

## 🎯 最佳实践

### 1. 能不spawn就不spawn

```
用户：帮我搜索FastAPI教程
❌ spawn子代理用turbos搜索
✅ 主会话直接搜索（更省token）
```

### 2. 能合并就合并

```
用户：搜索FastAPI、Flask、Django的对比
❌ spawn 3个子代理分别搜索
✅ spawn 1个turbos搜索三者对比
```

### 3. 大文件先摘要

```
用户：分析这个100KB的日志文件
❌ 直接发送100KB内容
✅ 先提取关键部分，发送5KB摘要
```

### 4. 告知用户成本

```
用户：帮我并行处理这10个任务
✅ 这个任务需要spawn约10个子代理，预估消耗50K+ token，确认执行吗？
```

---

## 🔐 安全摘要

| 方面 | 状态 |
|------|------|
| 凭证存储 | OpenClaw管理（不在技能中） |
| 外部API调用 | 是（腾讯Coding Plan） |
| 数据外发 | 任务上下文、任务中的文件 |
| 自主操作 | 是（spawn子代理） |
| 用户通知 | 是（spawn时） |
| Token预算控制 | **是（本版本新增）** |

---

## 📝 使用示例

### 示例1：简单任务（不spawn）

```
用户：搜索Python异步编程最佳实践

分析：
- 单一搜索任务
- 主会话可完成

决策：主会话直接执行，不spawn
```

### 示例2：中等任务（合并spawn）

```
用户：研究FastAPI并写一个学习指南

分析：
- 搜索FastAPI资料
- 整理信息
- 写学习指南

优化：
- 搜索+整理 → 1个turbos
- 写指南 → 1个glm-5

决策：spawn 2个子代理，预估10K token，告知用户后执行
```

### 示例3：复杂任务（需确认）

```
用户：分析这个项目目录下所有代码，并生成架构文档

分析：
- 需要读取多个文件
- 需要深度分析
- 需要写长文档

检查：
- 文件总大小：估计200KB
- 子代理数量：3-5个
- 预估Token：50K+

决策：询问用户确认，并建议只发送关键文件
```

---

## License

MIT - Use freely, modify, distribute.

**Requires Tencent Coding Plan subscription.**
