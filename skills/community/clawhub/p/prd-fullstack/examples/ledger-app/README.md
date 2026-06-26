# 记账App - 完整PRD示例

这是一个使用 PRD Skill 工作流生成的完整示例项目。

## 产品信息

- **产品名称**: 简记账 (SimpleLedger)
- **产品类型**: 工具类
- **目标平台**: iOS + Android (首版), Web后续
- **核心价值**: 让记账变得简单，帮助用户掌握财务状况

## PRD结构

本示例包含完整的14章PRD：

| 章节 | 内容 | 文件名 |
|-----|------|--------|
| 01 | 项目概述 | 01-overview.md |
| 02 | 市场分析 | 02-market.md |
| 03 | 需求列表 | 03-requirements.md |
| 04 | 信息架构 | 04-architecture.md |
| 05 | 用户流程 | 05-user-flows.md |
| 06 | 原型设计 | 06-prototype.md |
| 07 | UI设计规范 | 07-ui-design.md |
| 08 | 功能规格 | 08-functional.md |
| 09 | 数据模型 | 09-data-model.md |
| 10 | 技术方案 | 10-tech.md |
| 11 | 非功能需求 | 11-nonfunctional.md |
| 12 | 测试方案 | 12-testing.md |
| 13 | 数据埋点 | 13-tracking.md |
| 14 | 运营方案 | 14-operation.md |
| 15 | 项目计划 | 15-project-plan.md |

## 使用说明

1. 阅读各章节了解完整PRD的写法
2. 参考 build.js 和 build-pdf.js 构建输出
3. 模仿此结构创建你自己的PRD项目

## 生成文档

```bash
# 构建HTML
node build.js

# 生成PDF
node build-pdf.js

# 版本更新
./update.sh patch "更新说明"
```
