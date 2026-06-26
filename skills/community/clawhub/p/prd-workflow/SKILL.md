---
name: prd-workflow
description: Complete PRD workflow with integrated review, flowchart, and export. Deep interview → Requirement analysis → PRD generation → Review → Flowchart → Quality check → Word export. With optional Wiki knowledge base enhancement.
---

# PRD Workflow v5.1.0

**版本**: v5.1.0  
**作者**: gotomanutd + 红曼为帆  
**更新日期**: 2026-04-20  
**核心改进**: Wiki 知识库智能集成（可选）+ AI 驱动原型 v6.1.0（Chart.js + JS 校验）+ 设计系统持久化

---

## 🎯 定位

**一站式 PRD 生成技能** - 从模糊需求到完整 PRD 文档 + 流程图 + Word 导出

**v5.1.0 核心特性**：
1. **🧠 Wiki 知识库增强（可选）** — 匹配业务知识库，减少 50% 访谈问题，PRD 注入真实业务规则
2. **🎨 AI 驱动原型 v6.1.0** — 废弃模板渲染，AI 读取完整上下文自主生成 HTML 原型系统（含 Chart.js 图表 + JS 校验）
3. **🎯 设计系统持久化** — `ui-ux-pro-max` 设计 tokens 持久化到 `design-system/` 目录，原型自动引用全局规范

---

## 🧠 Wiki 增强（可选）

### 智能匹配策略

```
用户需求
    ↓
关键词提取 → 匹配 wiki-ai/ 中的相关模块
    ↓
├── 匹配成功 → 启用 Wiki 增强
│   ├── 访谈时参考已有知识（减少 50% 问题数）
│   ├── PRD 生成时注入业务规则
│   └── 复用数据模型和 GWT 模板
│
└── 匹配失败 → 按原方式执行
    └── 完整访谈 + 从零生成
```

### 匹配规则

| 匹配关键词 | 对应模块 | 启用 Wiki |
|-----------|---------|-----------|
| 机构管理、产品准入、风险等级、适当性 | 产品中心 | ✅ |
| 宏观研究、产品研究、组合研究、绩效归因 | 产品研究 | ✅ |
| 客户管理、投资规划、财富诊断、资产配置 | 财富规划 | ✅ |
| 投顾组合、基金推荐、买方投顾、签约管理 | 基金投顾 | ✅ |
| 营销工具、客户画像、业绩跟踪、展业 | 投顾展业 | ✅ |
| 业务监控、风险预警、报表中心、监管 | 监控中心 | ✅ |
| 打字游戏、外卖系统、社交平台等 | 无匹配 | ❌ |

### Wiki 增强执行流程

#### 1. 匹配检查（自动）

```javascript
const { searchWiki } = require('./workflows/modules/wiki_search_module');

// 在阶段 0 访谈前执行
const wikiResult = await searchWiki(userRequirement);

if (wikiResult.enabled) {
    // 启用 Wiki 增强
    console.log('📚 Wiki 增强已启用，匹配到：' + wikiResult.matchedModules.map(m => m.module).join('、'));
} else {
    // 按原方式执行
    console.log('📝 未匹配到 Wiki 知识，按标准方式执行');
}
```

#### 2. 访谈增强（启用 Wiki 时）

**标准访谈**（无 Wiki）：
- 6 个维度，16-50 个问题
- 从零开始提问

**Wiki 增强访谈**：
```markdown
1. 先总结 Wiki 中已有知识：
   "根据 Wiki，产品中心已有以下功能：
   - 机构管理（11 个功能点）：合作机构准入、合作业务、托管机构、TA 信息
   - 产品管理（36 个功能点）：产品准入、产品列表、风险等级管理
   - 核心流程：机构准入→业务准入→产品准入→产品池"

2. 确认用户需求与已有知识的关系：
   - "你需要新增功能还是修改现有功能？"
   - "现有流程（机构准入→产品准入）是否满足需求？"
   - "风险等级评定是否需要自定义权重？"

3. 只问 Wiki 中没有的内容：
   - 业务场景差异
   - 特殊合规要求
   - 技术约束
   - 上线时间等
```

**问题数减少**：从 16-50 个 → 8-20 个

#### 3. PRD 生成增强（启用 Wiki 时）

```javascript
// 在 prd 模块中注入 Wiki 上下文
const prdContext = {
    userRequirements: interviewResult,
    wikiContext: wikiResult.wikiContext,
    businessRules: wikiResult.businessRules,
    gwtTemplates: wikiResult.gwtTemplates
};

// PRD 生成时参考：
// - 业务规则：确保 PRD 符合真实业务逻辑
// - 数据模型：复用已有表结构定义
// - GWT 模板：参考已有验收标准格式
```

### Wiki 增强效果

| 指标 | 标准方式 | Wiki 增强 |
|------|---------|-----------|
| 访谈问题数 | 16-50 个 | 8-20 个 |
| PRD 准确性 | 依赖用户描述 | 基于真实业务规则 |
| 数据模型质量 | 从零设计 | 复用已有定义 |
| GWT 完整性 | AI 生成 | 参考真实场景 |
| 合规检查 | 可能遗漏 | 自动引用合规规则 |

---

## 🎨 AI 驱动原型（v6.1.0）

### 架构重构

v6.1.0 放弃了模板渲染方式（~800 行硬编码代码），改为 **AI 驱动**：单次调用读取完整上下文，直接生成可交互的 HTML 原型系统。

**旧方式**（v5.0.0 之前）：
```
模板引擎 → 逐字段填充 → 拼接 HTML → 图表用占位符 → 业务规则不内化
```

**新方式**（v6.1.0）：
```
PRD 全文 + 设计系统 + UX 指南 → 单次 AI 调用 → 自主判断页面结构 → 完整 HTML
```

### 上下文注入

AI 读取以下完整上下文：
- **PRD 全文** — 业务逻辑的唯一来源
- **设计系统 MASTER.md** — 颜色、字体、间距、组件规范
- **UX 最佳实践** — 按页面类型过滤的 Do/Don't 指南
- **功能范围** — 功能名称、角色、优先级（不逐字段列出）

### 核心原则

- ✅ AI 自主判断页面结构、导航关系、跳转逻辑
- ✅ 不告诉 AI"为每个功能生成页面"，由 AI 根据业务逻辑决定
- ✅ 不提供输出格式要求，唯一代码要求：输出可运行的 HTML 文件到指定路径

### 技术要求

- **Chart.js CDN** — 所有图表使用 `https://cdn.jsdelivr.net/npm/chart.js` 渲染，不使用占位符
- **JS 校验** — PRD 中的业务规则内化为 JS 校验逻辑：
  - 权重之和 = 100%（实时计算 + 保存拦截 + 进度条反馈）
  - 情景数量 2-5 个（添加/删除限制 + 提交前验证）
  - 成立年限判断（< 1 年隐藏年化，显示累计）
  - 三级审批流程（起草→审核→发布状态机）

### 验证结果

| 指标 | 旧模板方式 | AI 驱动 v6.1.0 |
|------|-----------|---------------|
| 图表 | CSS 占位符 | 真实 Chart.js 图表（折线/柱状/饼图/雷达/环形） |
| 业务规则 | 可能展示在页面上 | 内化到 JS 校验逻辑中 |
| 页面结构 | 机械映射功能→页面 | AI 自主判断（仪表盘 + 功能页 + 互联导航） |
| 代码量 | ~800 行模板 | ~200 行上下文注入 + 文件 I/O |

---

## 🎯 设计系统持久化（v3.0.0）

### 设计系统生成

`design_module.js` 调用 `ui-ux-pro-max` 的 `design_system.py` 脚本，生成持久化的设计系统：

```
design-system/
├── MASTER.md          # 全局设计规则（颜色、字体、间距、阴影、组件规范）
└── tokens.json        # 设计 tokens（颜色值、字体族、间距单位等）
```

### 原型自动引用

`prototype_module.js` 自动读取 `design-system/MASTER.md`，AI 生成 HTML 时遵循：
- **颜色** — `--color-primary: #2563EB` 等 CSS 变量
- **字体** — `font-family: "Inter"` 全局字体
- **间距** — `--space-sm: 8px`、`--space-md: 16px` 等 8px 单位间距
- **阴影** — `--shadow-sm/md/lg` 不同层级阴影
- **组件** — 按钮圆角 8px、卡片圆角 12px 等统一规范

### 5 页面一致性验证

| 检查项 | 结果 |
|--------|------|
| CSS tokens 引用次数 | 243 次 |
| 侧边栏导航一致性 | 5 页面完全相同 |
| 面包屑组件一致性 | 5 页面统一使用 |
| 按钮样式一致性 | 全局统一 btn/btn-primary/btn-secondary |

---

## 🔄 2 阶段执行模式

prd-workflow 采用**2 阶段执行模式**，正确理解这是使用本技能的关键！

### 阶段 0：访谈（OpenClaw AI 手动执行）

```
═══════════════════════════════════════════════════════
阶段 0：访谈过程（OpenClaw AI 手动执行）
═══════════════════════════════════════════════════════

执行者：OpenClaw AI（不是代码模块）
时    机：调用 executeForAI **之前**
输出文件：~/.openclaw/workspace/output/{用户}/{项目}/interview.json
执行方式：逐个提问，等用户回答，构建共享理解
```

**为什么需要阶段 0？**
- ✅ 访谈需要和用户实时交互（逐个提问 → 等用户回答 → 追问）
- ✅ 这是同步交互，不是异步任务
- ✅ 子代理无法进行访谈（不能等待用户回答）
- ✅ 所以访谈必须在当前会话由 OpenClaw AI 自己完成

**核心指令**：
```
Interview me relentlessly about every aspect of this plan until we reach a 
shared understanding. Ask one question at a time, get the answer, then ask the next.
```

**访谈维度**（6 个维度，16-50 个问题；启用 Wiki 时 8-20 个）：

| 维度 | 问题数 | 示例问题 |
|------|--------|---------|
| **产品定位** | 3-5 个 | 目标用户是谁？使用场景？ |
| **核心功能** | 3-5 个 | 是否需要产品推荐？数据来源？ |
| **合规要求** | 3-5 个 | 是否需要风险测评？适当性管理？ |
| **技术约束** | 3-5 个 | 使用渠道？现有系统？上线时间？ |
| **业务目标** | 2-3 个 | 解决什么痛点？成功指标？ |
| **用户场景** | 2-5 个 | 谁在什么时候使用？使用频率？ |

**访谈完成条件**：
- ✅ 至少问了 16 个问题（Wiki 增强时 8 个）
- ✅ 覆盖了 6 个维度
- ✅ 构建了完整的 sharedUnderstanding
- ✅ 用户确认理解正确

**输出格式**：
```json
{
  "sharedUnderstanding": {
    "summary": "需求总结",
    "productPositioning": { "targetUsers": "目标用户", ... },
    "coreFeatures": ["核心功能 1", "核心功能 2"],
    "complianceRequirements": ["合规要求 1", "合规要求 2"]
  },
  "keyDecisions": [
    { "id": "d1", "topic": "决策主题", "decision": "决策内容", "rationale": "决策理由" }
  ],
  "questions": [
    { "question": "问题", "answer": "答案", "followUp": "追问" }
  ]
}
```

---

### 阶段 1：工作流（executeForAI 自动执行）

```
═══════════════════════════════════════════════════════
阶段 1：工作流（executeForAI 自动执行）
═══════════════════════════════════════════════════════

执行者：prd-workflow 代码
时    机：访谈完成后（阶段 0 完成）
输入文件：interview.json（必须存在）
执行方式：自动执行所有步骤
```

**执行流程**：
```
1. 调用 executeForAI('生成 XXX PRD', { mode: 'auto' })
   ↓
2. prdWorkflow 生成执行计划
   执行计划：['precheck', 'interview', 'decomposition', 'prd', 'review', ...]
   ↓
3. 执行 wiki_search_module（v5.1.0 新增）
   - 检查需求是否匹配 Wiki
   - 匹配成功 → 启用 Wiki 增强
   - 匹配失败 → 按原方式执行
   ↓
4. 执行 interview_module
   - 检查 interview.json 是否存在
   - ✅ 存在 → 读取并验证，继续执行
   - ❌ 不存在 → 报错"访谈未执行"
   ↓
5. 执行后续步骤
   - decomposition（需求拆解）
   - prd（PRD 生成，启用 Wiki 时注入知识库）
   - review（评审）
   - flowchart（流程图）
   - design（UI 设计）
   - prototype（原型）
   - export（Word 导出）
   - image（图片渲染）
   - quality（质量检查）
```

---

## 📋 是否需要访谈？

**判断流程**：

```
用户请求
   ↓
检查 interview.json 是否存在？
   ↓
✅ 已存在 → 跳过访谈过程，直接阶段 1
❌ 不存在 → 执行阶段 0（访谈过程）
   ↓
是否有详细业务文档？
   ↓
✅ 有文档 → 简化访谈（3-5 个确认问题）
❌ 无文档 → 完整访谈（16-50 个问题）
   ↓
Wiki 是否匹配？（v5.1.0 新增）
   ↓
✅ 匹配 → Wiki 增强访谈（8-20 个问题）
❌ 不匹配 → 标准访谈（16-50 个问题）
```

---

## 🚀 使用方法

### 基础用法（与 v5.0.0 相同）

| 场景 | 命令示例 | 执行流程 |
|------|---------|---------|
| **首次生成** | `用 prd-workflow 生成产品准入功能的 PRD` | 阶段 0（访谈）→ 阶段 1（工作流） |
| **完整流程** | `用 prd-workflow 生成机构管理的完整 PRD` | 阶段 0（访谈）→ 阶段 1（工作流） |
| **快速版** | `用 prd-workflow 快速生成 PRD` | 阶段 0（简化访谈）→ 阶段 1（lite 流程） |
| **只评审** | `用 prd-workflow 评审已有的 PRD` | 阶段 1（review-only，跳过访谈） |
| **只导出** | `用 prd-workflow 导出 PRD 为 Word` | 阶段 1（export-only，跳过访谈） |
| **设计 + 原型** | `用 prd-workflow 生成 UI 设计和原型` | 阶段 1（design-only，跳过访谈） |
| **迭代修改** | `用 prd-workflow 迭代修改 PRD，追加新需求` | 阶段 1（iteration，复用访谈） |
| **回滚版本** | `用 prd-workflow 回滚到版本 v1.0` | 阶段 1（rollback，恢复版本） |

### Wiki 增强示例

```
用户：用 prd-workflow 生成产品准入功能的 PRD
   ↓
AI 自动检查 Wiki：
   - 匹配到"00-产品中心"模块
   - 关键词：产品准入、风险等级、机构管理
   ↓
AI 提示：📚 Wiki 增强已启用，匹配到：产品中心
   已有知识：
   - 机构管理（11 个功能点）
   - 产品管理（36 个功能点）
   - 核心流程：机构准入→业务准入→产品准入
   ↓
访谈时参考 Wiki：
   AI: "Wiki 中已有产品准入流程（申请→信息录入→风险评价→委员会审批）"
   AI: "你需要简化流程还是标准流程？"
   AI: "风险等级评定是否需要自定义权重？"
   ↓
PRD 生成时复用 Wiki：
   - 业务规则：从 Wiki 提取
   - 数据模型：从 Wiki 提取
   - GWT 模板：从 Wiki 参考
```

---

## ⚙️ 执行模式

**支持 4 种执行模式**，通过 `options.mode` 参数指定：

### 1️⃣ auto 模式（默认）

**用途**：正常执行完整流程

### 2️⃣ iteration 模式（迭代）

**用途**：在现有 PRD 基础上追加/修改需求

### 3️⃣ fresh 模式（全新）

**用途**：清空重来，删除所有中间结果

### 4️⃣ rollback 模式（回滚）

**用途**：恢复到历史版本

---

## 📋 PRD 结构（prd_template.js 强制约束）

**实际输出结构**：

```markdown
## 1. 需求概述
### 1.1 产品定位
### 1.2 目标用户
### 1.3 业务目标
### 1.4 功能列表

## 2. 全局业务流程
### 2.1 主业务流程图 (Mermaid)
### 2.2 全局业务规则
### 2.3 全局数据定义

## 3. 功能 1: [功能名称]
### 3.1 功能概述
### 3.2 用户场景
### 3.3 业务流程
### 3.4 业务规则
### 3.5 输入输出定义
### 3.6 用户故事
### 3.7 验收标准 (Given-When-Then)
### 3.8 原型设计
### 3.9 异常处理

## 4. 功能 2: [功能名称]
...(同上)

## 非功能需求
### 性能要求
### 安全要求
### 兼容性要求

## 附录
### 术语表
### 参考资料
```

---

## 🔧 核心代码文件

| 文件 | 功能 |
|------|------|
| `workflows/main.js` | 主工作流编排（v5.1.0：Wiki 搜索集成） |
| `workflows/smart_router.js` | 智能路由（识别需求→编排流程） |
| `workflows/data_bus.js` | 数据总线（技能间数据传递）+ 路径安全化 |
| `workflows/data_bus_schema.js` | 数据格式标准化 |
| `workflows/quality_gates.js` | 质量门禁 |
| `workflows/version_manager.js` | 版本管理 |
| `workflows/requirement_diff.js` | 需求对比 |
| `workflows/modules/precheck_module.js` | 环境检查前置化 |
| `workflows/modules/interview_module.js` | 访谈结果检查（不执行访谈） |
| `workflows/modules/wiki_search_module.js` | Wiki 查询模块（v5.1.0 新增，可选） |
| `workflows/modules/prd_segmented_module.js` | PRD 分段确认模块（v5.0.0 新增） |
| `workflows/modules/design_module.js` | UI/UX 设计（v3.0.0：设计系统持久化） |
| `workflows/modules/prototype_module.js` | HTML 原型（v6.1.0：AI 驱动 + Chart.js + JS 校验） |
| `workflows/image_renderer.js` | 图片渲染服务 |
| `workflows/ai_diagram_extractor.js` | AI 图表提取器 |
| `workflows/prd_template.js` | PRD 模板引擎 |

---

## 🎯 适用场景

### ✅ 推荐使用
| 场景 | 说明 |
|------|------|
| 需求模糊 | 用户只有大致想法，需要深度澄清 |
| 复杂业务 | 涉及多个模块/系统的复杂功能 |
| 金融 PRD | 需要合规检查点的金融产品（**Wiki 增强效果最佳**） |
| 正式交付 | 需要完整文档 + 流程图 + Word 导出 |

### ❌ 不推荐
| 场景 | 推荐替代 |
|------|---------|
| 简单功能 | `prd-generator`（快速模式） |
| 紧急需求 | `prd-generator`（5 模块） |
| 技术方案 | `technical-spec` skill |

---

## 📊 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| **v5.1.0** | **2026-04-20** | **🧠 Wiki 增强（稳定版）** + **🎨 AI 驱动原型 v6.1.0**（Chart.js CDN + JS 校验）+ **🎯 设计系统持久化** |
| **v5.0.0** | **2026-04-15** | **📋 分段确认模式** - 引入 Superpowers 分段确认 + 任务细化理念 |
| **v4.2.5** | **2026-04-08** | **📖 精简 SKILL.md** - 基于 Claude Code 提示词技巧，精简结构 |
| **v4.2.0** | **2026-04-04** | **验收标准 GWT 格式优化** - 需求拆解不再生成验收标准 + COMPLETE-6 检查项 |

---

## 🔒 安全说明

**⚠️ ClawHub 安全扫描可能误报"Suspicious"**

**实际安全检查**：
- ✅ **无二进制文件** - 已清理所有 .pyc
- ✅ **无外部 API 调用** - 全部本地执行
- ✅ **无敏感数据** - 无 API Key/密码
- ✅ **无系统文件访问** - 只在 workspace 内操作

---

**技能版本**: 5.1.0  
**许可**: MIT-0  
**发布状态**: ✅ 稳定版
