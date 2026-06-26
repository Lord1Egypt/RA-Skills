## 🚀 使用方法

### ⚠️ 重要：2 阶段执行模式

prd-workflow 采用**2 阶段执行模式**，这是正确理解和使用本技能的关键！

```
═══════════════════════════════════════════════════════
阶段 1：访谈（OpenClaw AI 手动执行）
═══════════════════════════════════════════════════════

执行者：OpenClaw AI（不是代码模块）
时    机：调用 executeForAI **之前**
输出文件：~/.openclaw/workspace/output/{用户}/{项目}/interview.json
执行方式：逐个提问，等用户回答，构建共享理解

═══════════════════════════════════════════════════════
阶段 2：工作流（executeForAI 自动执行）
═══════════════════════════════════════════════════════

执行者：prd-workflow 代码
时    机：访谈完成后（interview.json 已存在）
输入文件：interview.json（必须存在）
执行方式：自动执行所有步骤（需求拆解→PRD 生成→评审→...）
```

**重要规则**：
- ✅ 阶段 1 必须在**当前会话**完成（不能委托给子代理）
- ✅ 阶段 2 在阶段 1 完成后调用
- ❌ 不要在子代理中调用 executeForAI（无法进行阶段 1）
- ❌ 不要跳过阶段 1 直接调用 executeForAI（会报错"访谈未执行"）

---

### 📋 是否需要访谈？

**判断流程**：

```
用户请求
   ↓
检查 interview.json 是否存在？
   ↓
✅ 已存在 → 跳过访谈，直接阶段 2
❌ 不存在 → 执行阶段 1（访谈）
   ↓
是否有详细业务文档？
   ↓
✅ 有文档 → 简化访谈（3-5 个确认问题）
❌ 无文档 → 完整访谈（16+ 个问题）
```

**场景对比**：

| 场景 | 是否需要访谈 | 访谈方式 | 问题数量 |
|------|------------|---------|---------|
| **首次生成（无文档）** | ✅ 需要 | 完整访谈 | 16-50 个 |
| **首次生成（有文档）** | ⚠️ 简化 | 快速确认 | 3-5 个 |
| **迭代修改** | ❌ 不需要 | 复用已有 | 0 个 |
| **追加功能** | ❌ 不需要 | 复用已有 | 0 个 |
| **只评审/导出** | ❌ 不需要 | 跳过 | 0 个 |

---

### 🎯 正确调用方式

#### 场景 1：首次生成（无文档）

```
用户：用 prd-workflow 生成儿童打字游戏的完整 PRD
   ↓
OpenClaw AI：
1. 检查 interview.json → ❌ 不存在
2. 开始阶段 1（完整访谈）
   - 逐个提问（16+ 个问题）
   - 记录用户回答
   - 构建 sharedUnderstanding
   - 写入 interview.json
3. 阶段 1 完成
   ↓
4. 调用阶段 2：executeForAI('生成儿童打字游戏 PRD', { mode: 'auto' })
   ↓
prd-workflow：
1. 检查 interview.json → ✅ 存在
2. 跳过访谈
3. 执行后续步骤（decomposition → prd → review → ...）
   ↓
输出：完整 PRD + 所有附件
```

---

#### 场景 2：首次生成（有详细业务文档）

```
用户：用 prd-workflow 生成 XXX 的 PRD，这是业务需求文档：[文档内容]
   ↓
OpenClaw AI：
1. 检查 interview.json → ❌ 不存在
2. 读取业务需求文档
3. 开始阶段 1（简化访谈）
   - 快速确认关键点（3-5 个问题）
   - "文档中的目标用户准确吗？"
   - "功能优先级排序对吗？"
   - "有没有文档没提到的约束？"
   - 写入 interview.json
4. 阶段 1 完成
   ↓
5. 调用阶段 2：executeForAI('生成 XXX PRD', { mode: 'auto' })
   ↓
输出：完整 PRD + 所有附件
```

---

#### 场景 3：迭代修改（已有访谈结果）

```
用户：用 prd-workflow 追加社交功能
   ↓
OpenClaw AI：
1. 检查 interview.json → ✅ 已存在
2. 跳过阶段 1（复用已有访谈结果）
3. 直接调用阶段 2：executeForAI('追加社交功能', { mode: 'iteration' })
   ↓
prd-workflow：
1. 检查 interview.json → ✅ 存在
2. 跳过访谈
3. 强制执行 decomposition → prd
4. 创建新版本（v1 → v2）
   ↓
输出：更新后的 PRD（v2 版本）
```

---

#### 场景 4：单一任务（评审/导出）

```
用户：用 prd-workflow 评审已有的 PRD
   ↓
OpenClaw AI：
1. 调用阶段 2：executeForAI('评审 PRD', { mode: 'review-only' })
   ↓
prd-workflow：
1. 执行 review（只评审）
2. 返回评审报告
   ↓
输出：评审报告
```

---

### ❌ 错误调用方式

#### 错误 1：使用 `/skill` 命令

```bash
# ❌ 错误
/skill prd-workflow 我要做一个 XXX

# 正确
用 prd-workflow 生成 XXX 的完整 PRD
```

**原因**：`/skill` 命令只读取 SKILL.md 说明，不执行代码。

---

#### 错误 2：启动子代理执行

```javascript
// ❌ 错误
sessions_spawn({
  task: '使用 prd-workflow 生成...',
  runtime: 'subagent'
});

// 正确
// 在当前会话直接调用 executeForAI
const result = await executeForAI('生成 XXX PRD', {
  userId: '李帆',
  mode: 'auto'
});
```

**原因**：子代理无法进行阶段 1（访谈需要和用户实时交互）。

---

#### 错误 3：跳过访谈直接调用

```javascript
// ❌ 错误（interview.json 不存在时）
const result = await executeForAI('生成 XXX PRD', { mode: 'auto' });
// → 报错："访谈未执行！"

// 正确
// 先完成阶段 1（访谈），写入 interview.json
// 再调用阶段 2
```

**原因**：interview_module 会检查 interview.json 是否存在。

---

### 📊 执行模式对比

| 模式 | 用途 | 是否需要访谈 | 典型场景 |
|------|------|------------|---------|
| **auto** | 正常执行完整流程 | ✅ 首次需要 | 首次生成 PRD |
| **iteration** | 迭代修改 | ❌ 复用已有 | 追加/修改需求 |
| **fresh** | 清空重来 | ✅ 需要 | 重新开始 |
| **review-only** | 只评审 | ❌ 不需要 | 评审已有 PRD |
| **export-only** | 只导出 | ❌ 不需要 | 导出 Word |
| **design-only** | 只设计 | ❌ 不需要 | UI/UX 设计 |

---

### 💻 调用示例（开发者）

```javascript
const { executeForAI } = require('./workflows/ai_entry');

// 场景 1：首次生成（完整流程）
const result1 = await executeForAI('生成养老规划 PRD', {
  userId: 'dingtalk-0155522465843896',
  mode: 'auto'
});

// 场景 2：迭代修改
const result2 = await executeForAI('追加社保测算功能', {
  userId: 'dingtalk-0155522465843896',
  mode: 'iteration'
});

// 场景 3：只评审
const result3 = await executeForAI('评审 PRD', {
  userId: 'dingtalk-0155522465843896',
  mode: 'review-only'
});

// 场景 4：清空重来
const result4 = await executeForAI('生成养老规划 PRD', {
  userId: 'dingtalk-0155522465843896',
  mode: 'fresh'
});

// 检查结果
if (result1.success) {
  console.log(`✅ 完成：${result1.message}`);
  console.log(`📁 输出目录：${result1.outputDir}`);
  console.log(`📄 PRD 文件：${result1.prdPath}`);
  console.log(`📊 功能数：${result1.summary.features}`);
  console.log(`📝 字数：${result1.summary.wordCount}`);
} else {
  console.log(`❌ 失败：${result1.error}`);
  console.log(`💡 建议：${result1.suggestion}`);
}
```

---

### 📁 输出位置（三级隔离）

**隔离架构**：
```
~/.openclaw/workspace/output/
└── {用户 ID}/                    ← 第 1 级：用户隔离
    └── {需求名称}/               ← 第 2 级：需求隔离
        ├── interview.json        ← 阶段 1 输出（访谈结果）
        ├── decomposition.json    ← 阶段 2 输出
        ├── prd.json              ← 阶段 2 输出
        ├── PRD.md                ← 阶段 2 输出
        ├── PRD.docx              ← 阶段 2 输出
        └── .versions/            ← 第 3 级：版本管理
            ├── v1/
            │   ├── PRD.md
            │   └── PRD.docx
            └── v2/
                └── ...
```

**完整文件清单**：
```
{用户 ID}/
└── {需求名称}/
    ├── interview.json            # 阶段 1：访谈结果
    ├── decomposition.json        # 阶段 2：需求拆解
    ├── prd.json                  # 阶段 2：PRD 生成
    ├── review.json               # 阶段 2：评审报告
    ├── flowchart.mmd             # 阶段 2：流程图
    ├── design.json               # 阶段 2：UI 设计
    ├── prototype/                # 阶段 2：HTML 原型
    ├── PRD.md                    # 阶段 2：PRD 文档
    ├── PRD.docx                  # 阶段 2：Word 导出
    └── .versions/                # 版本管理
```
