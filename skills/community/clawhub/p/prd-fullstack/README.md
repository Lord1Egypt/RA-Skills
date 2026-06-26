# PRD FullStack Skill - 全栈PRD协作工作流

## 概述

这是一个专业的PRD（产品需求文档）协作工作流Skill，帮助产品经理、开发团队、设计师、测试团队等共同创建完整、专业的PRD文档。

## 核心特性

### 🎯 完整覆盖
- **14个专业章节**：从产品概述到项目计划的全覆盖
- **6大产品类型**：SaaS、电商、教育、社交、内容、工具
- **10步协作流程**：从需求探索到运营计划的完整流程

### 🤝 智能协作
- **对话式引导**：自然对话，不是机械问答
- **可视化输出**：图表、表格、流程图丰富展示
- **可回退机制**：随时修改，灵活调整
- **专业级标准**：企业级PRD文档质量

### 🛠️ 强大工具
- **HTML/PDF输出**：一键生成专业文档
- **版本管理**：自动版本控制和更新
- **模板系统**：6种产品类型配置模板
- **检查清单**：PRD质量审查清单

## 快速开始

### 触发方式
当用户说以下关键词时触发：
- "帮我写PRD"
- "做完整需求文档"
- "产品需求文档"
- "需要PRD模板"

### 使用流程
```
用户：我想做一个在线教育平台

AI：好的！我们一起来做这份完整的PRD。
      首先，能详细说说你的想法吗？

[经过10步协作...]

AI：✅ PRD全栈文档完成！

      📄 prd-edu-platform-v1.0.0.pdf (180页)
      🌐 prd-edu-platform-v1.0.0.html
      📝 prd-edu-platform-v1.0.0.md

      章节覆盖：
      ✅ 产品篇：项目背景、市场分析、需求列表
      ✅ 体验篇：信息架构、流程图、原型、UI规范
      ✅ 功能篇：功能规格、数据模型
      ✅ 技术篇：架构设计、接口文档
      ✅ 质量篇：测试方案、数据埋点
      ✅ 运营篇：运营策略
      ✅ 管理篇：项目计划
```

## 文件结构

```
prd-skill-workflow/
├── SKILL.md                    # Skill配置文件
├── README.md                   # 本文件
├── COLLABORATION.md            # 协作流程快速参考
├── FULLSTACK_PRD.md            # 完整PRD结构说明
├── package.json                # 项目配置
├── prompts/                    # 10步协作Prompts
│   ├── step1-explorer.md      # 需求探索
│   ├── step2-positioning.md   # 产品定位
│   ├── step3-blueprint.md     # 功能蓝图
│   ├── step4-market.md        # 市场分析
│   ├── step5-architecture.md  # 信息架构
│   ├── step6-prototype.md     # 原型+UI
│   ├── step7-functional.md    # 功能+数据
│   ├── step8-tech.md          # 技术方案
│   ├── step9-testing.md       # 测试+数据
│   ├── step10-operation.md    # 运营+计划
│   └── iteration.md           # 版本迭代管理
├── templates/                  # 输出模板
│   ├── build.js               # HTML构建脚本
│   ├── build-pdf.js           # PDF生成脚本
│   ├── update.sh              # 版本更新脚本
│   ├── styles.css             # PRD样式表
│   └── fragments/             # 14个章节模板
├── templates-config/          # 6种产品类型配置
│   ├── saas.json              # SaaS/B端
│   ├── ecommerce.json         # 电商
│   ├── education.json         # 教育
│   ├── social.json            # 社交
│   ├── content.json           # 内容
│   └── tool.json              # 工具
├── checklists/                # 检查清单
│   └── prd-review-checklist.md # PRD审查清单
├── shortcuts/                 # 快捷模板
│   └── quick-templates.md     # 常用功能模板
├── examples/                  # 示例项目
│   └── ledger-app/            # 简记账完整示例
├── scripts/                   # 工具脚本
│   └── validate.js            # PRD验证脚本
└── references/                # 参考资料
    └── design-system.md       # 设计规范
```

## 10步协作流程

| 步骤 | 名称 | 目标 | 核心产出 |
|-----|------|------|----------|
| 1 | 需求探索 | 理清产品想法 | 需求摘要卡片 |
| 2 | 产品定位 | 确定类型、名称、平台 | 产品定位卡片 |
| 3 | 功能蓝图 | 功能清单和优先级 | 功能清单表格 |
| 4 | 市场分析 | 竞品分析、差异化 | 市场分析章节 |
| 5 | 信息架构 | 产品结构、页面层级 | 产品结构图 |
| 6 | 原型+UI | 线框图、设计规范 | 设计规范文档 |
| 7 | 功能+数据 | 功能规格、数据模型 | 功能规格+数据模型 |
| 8 | 技术方案 | 架构、接口、部署 | 技术架构文档 |
| 9 | 测试+埋点 | 测试用例、数据埋点 | 测试方案+埋点清单 |
| 10 | 运营+计划 | 运营策略、项目排期 | 运营策略+项目计划 |

## 输出规格

最终PRD约 **150-200页**，包含：
- 30+ 张表格（需求清单、竞品对比、测试用例等）
- 20+ 张流程图（Mermaid语法）
- 15+ 个页面原型描述
- 完整的UI设计规范
- 详细的技术架构说明
- 可执行的测试方案
- 运营推广策略
- 项目里程碑规划

## 适用对象

- **产品经理**：系统梳理需求，产出专业PRD
- **开发团队**：清晰的技术方案和接口设计
- **设计师**：完整的UI规范和交互原型
- **测试团队**：详细的测试策略和用例
- **运营团队**：数据指标和运营策略
- **项目经理**：排期计划和风险管理

## 安装使用

1. **安装Skill**：
   ```bash
   # 从ClawHub安装
   openclaw skill install prd-fullstack
   ```

2. **触发使用**：
   - 在对话中说"帮我写PRD"
   - 或"需要PRD模板"

3. **自定义配置**：
   - 修改 `templates-config/` 中的配置文件
   - 调整 `prompts/` 中的对话流程
   - 自定义 `templates/styles.css` 样式

## 示例项目

包含完整示例：`examples/ledger-app/`
- 简记账App的完整PRD
- 包含所有章节的示例内容
- 可直接运行的构建脚本

## 技术依赖

- Node.js >= 16.0.0
- Playwright (用于PDF生成)
- 支持Mermaid图表的Markdown渲染器

## 许可证

MIT License

## 作者

蒲公英 (Dandelion) - AI编程助手

## 更新日志

### v1.0.0 (2026-03-21)
- 初始版本发布
- 完整的10步协作流程
- 6种产品类型配置
- HTML/PDF输出支持
- 示例项目包含

## 贡献指南

欢迎提交Issue和Pull Request：
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 支持

如有问题，请：
1. 查看 `examples/` 目录中的示例
2. 阅读 `COLLABORATION.md` 协作指南
3. 提交Issue到项目仓库