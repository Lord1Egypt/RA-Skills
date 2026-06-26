# 简记账 (SimpleLedger) - 完整PRD示例

这是一个使用 PRD Skill 工作流生成的完整示例项目。

## 产品信息

- **产品名称**: 简记账 (SimpleLedger)
- **产品类型**: 工具类
- **目标平台**: iOS + Android (首版), Web后续
- **核心价值**: 让记账变得简单，帮助用户掌握财务状况

## 📁 示例输出

本示例包含完整的PRD输出文件，可直接查看效果：

| 文件 | 说明 |
|------|------|
| `output/prd-simple-ledger-v1.0.0.html` | 完整PRD文档（HTML格式，可直接浏览器打开） |

### 查看示例

1. **浏览器查看**: 直接用浏览器打开 `output/prd-simple-ledger-v1.0.0.html`
2. **打印成PDF**: 在浏览器中按 Ctrl+P / Cmd+P，选择"另存为PDF"

## 📋 PRD结构

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

## 🚀 使用说明

### 查看示例

```bash
# 进入示例目录
cd examples/ledger-app

# 浏览器打开HTML文件
# Windows
start output/prd-simple-ledger-v1.0.0.html

# macOS
open output/prd-simple-ledger-v1.0.0.html

# Linux
xdg-open output/prd-simple-ledger-v1.0.0.html
```

### 重新构建

如果你想修改后重新构建：

```bash
# 编辑 fragments/ 目录下的HTML片段

# 构建HTML
node build.js

# 生成PDF（需要安装Playwright）
node build-pdf.js

# 版本更新
node update.js patch "更新说明"
```

## 📚 学习要点

1. **文档结构**: 观察14个章节如何组织
2. **表格使用**: 学习用表格展示需求、用例、数据模型
3. **流程图**: 了解业务流程的描述方式
4. **样式规范**: 参考专业的PRD排版风格

## 📝 模仿创建

参考此示例创建你自己的PRD项目：

```bash
# 回到skill目录
cd ../..

# 初始化新项目
npm run init

# 按向导提示输入产品信息
```
