# PRD Generator

通用产品需求文档（PRD）生成器。将产品想法转化为结构化的 Markdown PRD，支持导出为专业排版的 Word 文档。

## 特性

- **通用化**：不绑定任何业务领域，自动适配你描述的产品类型
- **三级深度**：自动识别 L0（产品总纲）/ L1（大模块）/ L2（具体功能）
- **规范输出**：遵循标准 PRD 写作规范（验收标准、字段定义、边界异常）
- **双格式支持**：Markdown + Word (.docx)

## 快速开始

### 1. 生成 PRD（Markdown）

```
/prd-generator 我要做一个在线预约系统，用户可以预约医生的门诊时间
```

### 2. 导出为 Word

```bash
# 先生成 PRD 后，执行转换
node ~/.claude/skills/prd-generator/scripts/md_to_docx.js 你的PRD.md 输出.docx
```

## 命令

| 命令 | 说明 |
|------|------|
| `/prd-generator <需求描述>` | 根据描述生成 PRD |
| `/prd-generator --level L2 <描述>` | 指定层级生成 |

## 依赖

Word 导出需要 Node.js 和 `docx` 包：

```bash
npm install -g docx
```

## PRD 标准结构

1. 文档元信息
2. 修订记录
3. 项目背景与目标
4. 用户分析
5. 核心场景
6. 业务流程
7. 产品架构
8. 具体需求（编号 / 功能 / 交互 / 验收标准）
9. 数据埋点
10. 风险评估
11. 迭代计划
12. 附录
