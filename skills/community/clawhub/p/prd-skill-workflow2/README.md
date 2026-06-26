# PRD FullStack - 全栈PRD协作工作流

与用户共同探讨，产出可供开发、设计、测试、运营、项目经理使用的完整PRD文档。

## 快速开始

```bash
# 1. 安装依赖
npm install

# 2. 安装 Playwright 浏览器（仅首次需要）
npx playwright install chromium

# 3. 初始化PRD项目
npm run init
# 或：npm run init <项目目录> <产品名称>

# 4. 在Claude对话中描述产品想法，AI将自动生成完整PRD
```

## 目录结构

```
prd-skill-workflow/
├── SKILL.md                    # Skill定义文件（核心入口）
├── COLLABORATION.md            # 协作流程快速参考
├── FULLSTACK_PRD.md            # 全栈PRD工作流设计文档
├── README.md                   # 本文件
├── package.json                # Node.js项目配置
├── prompts/                    # 10步协作Prompts
│   ├── step1-explorer.md       # 需求探索
│   ├── step2-positioning.md    # 产品定位
│   ├── step3-blueprint.md      # 功能蓝图
│   ├── step4-analysis.md       # 市场分析与核心流程
│   ├── step5-architecture.md   # 信息架构
│   ├── step6-prototype.md      # 原型+UI
│   ├── step7-functional.md     # 功能+数据
│   ├── step8-tech.md           # 技术方案
│   ├── step9-testing.md        # 测试+埋点
│   └── step10-operation.md     # 运营+计划
├── templates/                  # 输出模板
│   ├── build.js                # HTML构建脚本
│   ├── build-pdf.js            # PDF生成脚本
│   ├── update.js               # 版本更新脚本
│   ├── styles.css              # PRD样式表
│   └── fragments/              # HTML章节模板
├── templates-config/           # 6种产品类型配置
│   ├── saas.json               # SaaS/B端
│   ├── ecommerce.json          # 电商
│   ├── education.json          # 教育
│   ├── social.json             # 社交
│   ├── content.json            # 内容
│   └── tool.json               # 工具
│   └── [支持自定义配置]        # 用户可在项目中创建自定义配置
├── scripts/                    # 工具脚本
│   ├── init-prd.js             # PRD项目初始化脚本（交互式）
│   ├── status.js               # 查看协作进度
│   ├── score.js                # PRD质量评分系统
│   └── validate.js             # PRD验证脚本
├── shortcuts/                  # 快捷模板
│   └── quick-templates.md      # 常用功能模板
└── checklists/                 # 检查清单
    └── prd-review-checklist.md # PRD审查清单
```

## 10步协作流程

```
Step 1: 需求探索      → 理清产品想法
Step 2: 产品定位      → 确定类型、名称、平台
Step 3: 功能蓝图      → 梳理功能清单和优先级
Step 4: 市场分析      → 竞品分析、差异化定位
Step 5: 信息架构      → 产品结构、页面层级
Step 6: 原型+UI       → 线框图、设计规范
Step 7: 功能+数据     → 功能规格、数据模型
Step 8: 技术方案      → 架构、接口、部署
Step 9: 测试+埋点     → 测试用例、数据埋点
Step 10: 运营+计划    → 运营策略、项目排期
```

## 依赖说明

- **Node.js**: >= 16.0.0
- **Playwright**: 用于PDF生成（首次运行需下载浏览器）

```bash
npm install
# Playwright首次使用需安装浏览器
npx playwright install chromium
```

## 使用方式

### 启动PRD协作

在Claude中输入：
```
我想做一个[产品类型]，主要解决[核心问题]
```

Claude将引导你完成10步协作流程，最终生成完整PRD。

### 输出规格

最终PRD约 **150-200页**，包含：
- 30+ 张表格（需求清单、竞品对比、测试用例等）
- 20+ 张流程图（Mermaid语法）
- 15+ 个页面原型描述
- 完整的UI设计规范
- 详细的技术架构说明
- 可执行的测试方案
- 运营推广策略
- 项目里程碑规划

输出格式：
- 📄 `prd-<产品名>-v1.0.0.pdf`
- 🌐 `prd-<产品名>-v1.0.0.html`

## 快捷指令（20+模板）

在 Step 7（功能规格）时，可以使用快捷模板：

**功能规格：**
| 指令 | 效果 |
|------|------|
| `/login` | 生成标准登录功能规格 |
| `/logout` | 生成退出登录功能规格 |
| `/forgot-password` | 生成忘记密码功能规格 |
| `/register` | 生成注册功能规格 |
| `/profile` | 生成个人中心功能规格 |
| `/search` | 生成搜索功能规格 |
| `/notification` | 生成消息通知功能规格 |

**流程图：**
| 指令 | 效果 |
|------|------|
| `/flow-login` | 生成登录流程图 |
| `/flow-register` | 生成注册流程图 |
| `/flow-payment` | 生成支付流程图 |
| `/flow-refund` | 生成退款流程图 |
| `/flow-order` | 生成订单流程图 |

**数据表：**
| 指令 | 效果 |
|------|------|
| `/table-user` | 生成用户表结构 |
| `/table-order` | 生成订单表结构 |
| `/table-product` | 生成商品表结构 |
| `/table-message` | 生成消息表结构 |

**测试用例：**
| 指令 | 效果 |
|------|------|
| `/tc-login` | 生成登录测试用例 |
| `/tc-register` | 生成注册测试用例 |
| `/tc-payment` | 生成支付测试用例 |

**其他：**
| 指令 | 效果 |
|------|------|
| `/api-response` | 生成标准API响应格式 |
| `/permission` | 生成RBAC权限设计 |
| `/track-user` | 生成用户埋点事件 |
| `/track-business` | 生成业务埋点事件 |

AI 也可以主动推荐：
"这个功能很常见，我有标准模板，需要我按模板生成吗？"

## 自定义产品类型配置

如果默认的6种产品类型不满足需求，可以创建自定义配置：

```bash
# 在项目目录中运行
node scripts/init-custom-config.js
```

向导会引导你创建新的产品类型配置，包括：
- 产品类型名称和ID
- 识别关键词（用于自动匹配）
- 关注焦点
- 常用功能列表
- 典型用户角色
- 特殊埋点事件
- 常见流程图

创建的配置保存在项目 `templates-config/` 目录下，会覆盖或扩展默认配置。

### 配置示例

```json
{
  "id": "health",
  "name": "健康医疗",
  "keywords": ["健康", "医疗", "医生", "挂号", "问诊"],
  "focusAreas": ["用户隐私保护", "医疗数据安全", "合规性"],
  "commonFeatures": ["预约挂号", "在线问诊", "健康档案", "报告查询"],
  "userRoles": ["患者", "医生", "护士", "管理员"],
  "specialEvents": ["预约成功", "问诊开始", "处方开具"],
  "commonFlows": ["预约挂号流程", "在线问诊流程", "缴费流程"]
}
```

## 迭代与版本管理

### 交互式迭代向导（推荐）

```bash
npm run iterate
```

向导会引导你：
1. 选择变更类型（新增/修复/优化等）
2. 输入变更描述
3. 列出详细变更清单
4. 自动建议版本升级类型
5. 自动更新 CHANGELOG 和 ITERATION.json

### 标准版本更新

```bash
# 补丁版本（修复问题）
npm run update patch "修复登录bug"

# 次要版本（新增功能）
npm run update minor "新增搜索功能"

# 主要版本（重大重构）
npm run update major "重构用户体系"

# 仅增加构建号
npm run update build
```

### 查看变更历史

```bash
npm run history
```

输出示例：
```
1. v1.2.0 (build #15) - 2024-03-20
   ✨ 新增搜索功能
   • 添加全文搜索接口
   • 实现搜索结果排序
   • 添加搜索历史记录
```

### 版本对比

```bash
# 对比最近两个版本
npm run diff

# 对比指定版本
npm run diff v1.0.0 v1.1.0
```

### 版本回滚

```bash
# 查看可回滚的版本
npm run rollback

# 回滚到指定版本
npm run rollback v1.0.0
```

## 项目命令

```bash
# 初始化新项目（交互式）
npm run init

# 构建HTML
npm run build

# 生成PDF
npm run build:pdf

# 构建HTML+PDF
npm run build:all

# PRD质量评分
npm run score
npm run score:html  # 生成HTML报告

# 验证PRD完整性
npm run validate

# 查看协作进度（在项目目录中）
node status.js

# 版本更新与迭代
npm run iterate           # 交互式迭代向导
npm run update            # 标准版本更新
npm run history           # 查看变更历史
npm run diff              # 对比版本差异
npm run rollback          # 回滚到指定版本

# 自定义配置
node scripts/init-custom-config.js  # 创建自定义产品类型配置
```

## 适用对象

- **产品经理**：系统梳理需求
- **开发团队**：技术方案、接口设计
- **设计师**：UI规范、交互原型
- **测试团队**：测试策略、验收标准
- **运营团队**：数据指标、运营策略
- **项目经理**：排期计划、风险管理
