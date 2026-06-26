# PRD Workflow v5.1.0 - 技术文档

**架构设计 · 代码结构 · 开发指南**

> **v5.1.0 更新**: Wiki 增强（可选）+ AI 驱动原型 v6.1.0（Chart.js CDN + JS 校验）+ 设计系统持久化
> **v5.0.0 更新**: 分段确认模式 - 引入 Superpowers 分段确认 + 任务细化理念
> **v4.2.5 更新**: 验收标准 GWT 格式优化 - 需求拆解不再生成验收标准 + PRD 阶段按功能生成 GWT 格式

---

## 🏗️ 架构设计

### 三级隔离机制

```
output/
└── {用户 ID}/              ← 第 1 级:用户隔离
    └── {需求名称}/         ← 第 2 级:需求隔离
        └── .versions/     ← 第 3 级:版本管理
```

**设计原理**:
- **用户隔离**:多用户共享技能,数据互不干扰
- **需求隔离**:同一用户的不同需求独立存储
- **版本管理**:同一需求的迭代版本可追溯

**实现位置**:`workflows/data_bus.js`

```javascript
class DataBus {
  constructor(userInput, options = {}) {
    // 第 1 级:用户隔离
    const userId = options.userId || this.getDefaultUserId();

    // 第 2 级:需求隔离
    const projectName = this.extractProjectName(userInput);

    // ✅ v2.8.0 修复：使用 workspace 根目录作为输出目录基路径
    const workspaceRoot = path.resolve(__dirname, '../../..');
    this.outputDir = path.join(workspaceRoot, 'output', userId, projectName, '');

    // 第 3 级:版本管理
    this.versionsDir = path.join(this.outputDir, '.versions/');
  }
}
```

---

### 数据总线(DataBus)

**核心职责**:
- ✅ 技能间数据传递(JSON 文件)
- ✅ 并发控制(目录锁)
- ✅ 数据追溯(session ID)
- ✅ 输出目录管理

**数据结构**:
```json
{
  "schemaVersion": "1.0",
  "sessionId": "1774943921299-abc123",
  "skill": "interview",
  "data": { ... },
  "timestamp": "2026-04-04T00:00:00Z"
}
```

**实现位置**:`workflows/data_bus.js`

---

### 智能路由(SmartRouter)

**核心职责**:
- ✅ 解析用户需求(关键词匹配)
- ✅ 识别需要的技能
- ✅ 检查前置依赖
- ✅ 动态编排执行流程

**流程模板**:
```javascript
this.templates = {
  'full': ['precheck', 'interview', 'decomposition', 'prd', 'review',
           'flowchart', 'design', 'prototype', 'export', 'quality'],
  'lite': ['precheck', 'interview', 'decomposition', 'prd'],
  'review-only': ['review'],
  'export-only': ['export'],
  'design-only': ['design', 'prototype'],
  'check': ['precheck']  // 仅环境检查
};
```

**实现位置**:`workflows/smart_router.js`

---

### PRD 模板引擎(PRDTemplate)

**核心职责**:
- ✅ 强制约束 PRD 结构
- ✅ 基于功能模块化生成
- ✅ 输出标准化文档

**PRD 结构**:
```
## 1. 需求概述
## 2. 全局业务流程
## 3. 功能 1:[功能名称]
    ├── 3.1 功能概述
    ├── 3.2 用户场景
    ├── 3.3 业务流程
    ├── 3.4 业务规则
    ├── 3.5 输入输出定义
    ├── 3.6 用户故事
    ├── 3.7 验收标准
    ├── 3.8 原型设计
    └── 3.9 异常处理
## 4-N. 功能 2...N
## 非功能需求
## 附录
```

**实现位置**:`workflows/prd_template.js`

---

### 版本管理(VersionManager)

**核心职责**:
- ✅ 创建版本快照
- ✅ 恢复指定版本
- ✅ 版本对比
- ✅ 版本清理

**版本元数据**:
```json
{
  "version": "v2",
  "createdAt": "2026-04-04T00:10:00Z",
  "files": ["PRD.md", "PRD.docx", ...],
  "changeType": "追加需求",
  "changeSummary": "新增社保测算功能",
  "prdSummary": {
    "title": "养老规划 PRD",
    "featureCount": 5,
    "wordCount": 12000
  }
}
```

**实现位置**:`workflows/version_manager.js`

---

## 📁 代码结构

```
prd-workflow/
├── SKILL.md                    # ClawHub 技能说明(必需)
├── README.md                   # 本文档(技术说明)
├── clawhub.json                # ClawHub 发布配置
├── install.json                # 安装配置
│
├── workflows/                  # 核心工作流引擎
│   ├── main.js                 # 主入口(编排逻辑)
│   ├── ai_entry.js             # AI 调用入口
│   ├── utils.js                # 工具函数(v2.8.3 新增)
│   ├── data_bus.js             # 数据总线(隔离 + 传递)
│   ├── data_bus_schema.js      # 数据格式schema(v2.8.0 新增)
│   ├── smart_router.js         # 智能路由(技能编排)
│   ├── prd_template.js         # PRD 模板引擎(v2.8.8 重构)
│   ├── ai_diagram_extractor.js # AI 图表提取器(v2.8.8 新增)
│   ├── image_renderer.js       # 图片渲染服务(v4.0.0 新增)
│   ├── quality_gates.js        # 质量门禁(检查点)
│   ├── version_manager.js      # 版本管理(迭代支持)
│   ├── requirement_diff.js     # 需求对比(变更分析)
│   │
│   └── modules/                # 技能模块(12 个)
│       ├── precheck_module.js  # 环境检查(v2.8.0 新增)
│       ├── interview_module.js # 访谈检查
│       ├── decomposition_module.js # 需求拆解
│       ├── prd_module.js       # PRD 生成
│       ├── review_module.js    # 评审模块
│       ├── flowchart_module.js # 流程图模块
│       ├── design_module.js    # UI/UX 设计
│       ├── prototype_module.js # 原型生成
│       ├── export_module.js    # 导出模块
│       ├── quality_module.js   # 质量审核
│       └── optimize_module.js  # 优化模块
│
├── templates/                  # 模板文件
│   ├── PRD_TEMPLATE_v2.6.2.md  # PRD 模板
│   ├── PRD_TEMPLATE_v2.6.2_FUNCTION_BASED.md # 功能模板
│   └── questions-template.json # 访谈问题库
│
├── skills/                     # 内置技能(5 个)
│   ├── htmlPrototype/
│   ├── mermaid-flow/
│   ├── prd-export/
│   ├── requirement-reviewer/
│   └── ui-ux-pro-max/
│
├── templates/                  # 模板文件
│   ├── PRD_TEMPLATE_v2.6.2.md  # PRD 模板
│   ├── PRD_TEMPLATE_v2.6.2_FUNCTION_BASED.md # 功能模板
│   └── questions-template.json # 访谈问题库
│
├── tests/                      # 测试套件(v2.8.3 新增)
│   └── test.js                 # 单元测试 + 集成测试
│
└── examples/                   # 示例文件
    └── pension-example.md
```

---

## 🔧 开发指南

### 添加新技能

**Step 1:创建技能模块**
```javascript
// workflows/modules/new_skill_module.js
class NewSkillModule {
  async execute(options) {
    const { dataBus, qualityGate, outputDir } = options;

    console.log('\n📄 执行技能:新技能');

    // 1. 读取前置数据
    const prdData = dataBus.read('prd');

    // 2. 执行技能逻辑
    const result = await this.process(prdData);

    // 3. 质量检查
    const qualityCheck = qualityGate.check(result);

    // 4. 保存结果
    dataBus.write('new_skill', result);

    return {
      success: true,
      quality: qualityCheck
    };
  }
}

module.exports = { NewSkillModule };
```

**Step 2:注册到路由**
```javascript
// workflows/smart_router.js
this.skills = {
  // ... 现有技能
  'new_skill': { name: '新技能', keywords: ['新技能', 'new'] }
};

this.dependencies = {
  // ... 现有依赖
  'new_skill': ['prd']  // 依赖 PRD 生成
};

this.templates = {
  // ... 现有模板
  'with-new': ['interview', 'decomposition', 'prd', 'new_skill']
};
```

**Step 3:更新主工作流**
```javascript
// workflows/main.js
const { NewSkillModule } = require('./modules/new_skill_module');

// 在技能执行循环中处理
```

---

### 修改 PRD 模板

**Step 1:修改模板引擎**
```javascript
// workflows/prd_template.js
buildFunctionChapter(feature, index) {
  let content = '';

  // 添加新的小节
  content += `### ${index}.10 数据埋点\n\n`;
  content += '| 事件名称 | 触发时机 | 上报参数 |\n';
  content += '|---------|---------|---------|\n';

  return content;
}
```

**Step 2:更新 SKILL.md 文档**
```markdown
## 📋 PRD 结构

## 3. 功能 1:[功能名称]
### 3.10 数据埋点  ← 新增
```

---

### 调试技巧

**启用详细日志**:
```javascript
// workflows/main.js
const DEBUG = true;

if (DEBUG) {
  console.log('🔍 调试模式已启用');
  console.log('📁 输出目录:', dataBus.outputDir);
  console.log('📝 执行计划:', plan.skillsToExecute);
}
```

**查看数据总线内容**:
```bash
cd output/{用户 ID}/{需求名称}/
cat interview.json | jq .
cat decomposition.json | jq .
cat prd.json | jq .
```

**检查版本历史**:
```bash
cd output/{用户 ID}/{需求名称}/.versions/
ls -la
cat v1/.version.json | jq .
```

---

## 🧪 测试

### 单元测试

**运行测试**:
```bash
cd /Users/lifan/.openclaw/workspace/skills/prd-workflow
node tests/unit-tests.js
```

**测试覆盖**:
- ✅ DataBus 类(目录隔离、锁机制)
- ✅ SmartRouter 类(需求解析、流程编排)
- ✅ VersionManager 类(版本创建、恢复)
- ✅ PRDTemplate 类(模板生成)

---

### 集成测试

**完整流程测试**:
```bash
cd workflows/
node main.js "生成养老规划 PRD"
```

**检查输出**:
```bash
ls -la output/default/养老规划/
cat output/default/养老规划/PRD.md | head -50
```

---

### 并发测试

**测试目录锁**:
```bash
# 终端 1
node main.js "生成养老规划 PRD"

# 终端 2(同时执行)
node main.js "生成养老规划 PRD"
# 预期:检测到并发,报错退出
```

---

## 🤝 贡献指南

### 提交 PR

1. **Fork 仓库**
2. **创建分支**:`git checkout -b feature/new-skill`
3. **实现功能**:遵循现有代码风格
4. **编写测试**:确保测试通过
5. **更新文档**:SKILL.md + README.md
6. **提交 PR**:描述清晰的变更说明

---

### 代码规范

**JavaScript 风格**:
- ✅ 使用 ES6+ 语法
- ✅ 异步用 async/await
- ✅ 错误用 try-catch
- ✅ 日志用 console.log + emoji

**文件命名**:
- ✅ 小写 + 下划线:`data_bus.js`
- ✅ 类名大写:`class DataBus`
- ✅ 模块导出:`module.exports = { DataBus }`

---

### 版本发布

**Step 1:更新版本号**
```javascript
// workflows/main.js
console.log(`🚀 启动 PRD Workflow v2.7.1...`);
```

**Step 2:更新 SKILL.md**
```yaml
---
version: 2.6.5
更新日期:2026-04-04
---
```

**Step 3:更新变更历史**
```markdown
## 📊 版本历史
| 版本 | 日期 | 变更内容 |
|------|------|---------|  
| **v2.7.1** | **2026-04-04** | **🚀 准备发布** - 统一版本号 |
| **v2.7.0** | **2026-04-04** | **🤖 AI 集成优化** - ai_entry.js + 错误处理 + 测试 |
| v2.6.5 | 2026-04-03 | 📝 文档更新 |
```

**Step 4:发布到 ClawHub**
```bash
clawhub publish ./prd-workflow
```

---

## 📚 参考资料

- **OpenClaw Skills**: https://docs.openclaw.ai
- **ClawHub**: https://clawhub.ai
- **Matt Pocock Skills**: github.com/mattpocock/skills

---

**文档版本**: 4.2.5
**最后更新**: 2026-04-08
**维护者**: gotomanutd
