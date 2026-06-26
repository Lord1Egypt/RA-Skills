---
name: prd-generator
description: Generate structured Product Requirement Documents (PRD) in Markdown format, with optional Word (.docx) export. Activate when user mentions "写PRD", "产品需求文档", "需求文档", "PRD", "产品规格", "功能需求", or wants to design/document a software feature/module/product.
version: 2.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    install:
      - kind: node
        package: docx
        bins: []
---

# PRD Generator — 通用产品需求文档生成器

将模糊的产品想法转化为结构清晰、可直接交付研发的 PRD 文档。支持 Markdown 输出和 Word (.docx) 导出。

## 1. 触发条件

以下场景自动激活本 Skill：
- 用户要求「写 PRD」「写需求文档」「产品需求」「功能规格」
- 用户调用 `/prd-generator`
- 用户描述一个功能/模块/产品，需要结构化文档输出

## 2. 核心能力

- **通用化生成**：不绑定任何业务领域，自动适配用户指定的行业/产品类型
- **三级深度**：自动识别 PRD 层级（L0 产品总纲 / L1 大模块 / L2 具体功能），应用对应写作深度
- **Markdown 输出**：生成符合标准规范的 `.md` 文件
- **Word 导出**：通过内置脚本一键转换为专业排版的 `.docx` 文档
- **质量自检**：生成后自动对照检查清单校验完整性

## 3. 运行流程

```
1. 输入分析 → 识别产品领域、PRD 层级、目标用户
2. 规范应用 → 加载 references/prd_template.md 和 references/writing_spec.md
3. 内容生成 → 按模板结构逐章输出完整 PRD（Markdown）
4. 质量检查 → 对照检查清单验证
5. 可选导出 → 用户要求时，调用 scripts/md_to_docx.js 生成 Word 文档
```

## 4. PRD 层级识别

| 层级 | 范围 | 深度 | 典型编号 |
|------|------|------|----------|
| L0 | 整个产品/平台 | 行业背景、产品愿景、模块全景 | 无编号或 1.0 |
| L1 | 大功能域（含多个子模块） | 模块定位、子系统划分、接口契约 | 1.1 / 2.3 |
| L2 | 具体功能或页面集合 | 页面、字段、按钮、状态、异常 | 1.1.1 / 3.2.1 |

识别信号：
- 用户明确声明层级
- 文档名含三级编号 → L2；二级编号 → L1
- 描述整个行业趋势 → L0；描述具体页面交互 → L2

## 5. 输出格式

### 5.1 Markdown（默认）

保存为 `{topic}-PRD-v1.0.md`，包含完整章节：
1. 文档元信息
2. 修订记录
3. 项目背景与目标
4. 用户分析
5. 核心场景
6. 业务流程
7. 产品架构
8. 具体需求（编号、功能、交互、验收标准）
9. 数据埋点
10. 风险评估
11. 迭代计划
12. 附录（术语表、参考资料）

### 5.2 Word（可选）

执行转换脚本生成专业排版的 `.docx`：
```bash
node ~/.claude/skills/prd-generator/scripts/md_to_docx.js 输入.md 输出.docx
```

## 6. 写作规范约束

生成内容必须遵循 `references/writing_spec.md` 中的规范：
- 验收标准使用 Given-When-Then 格式
- 字段定义包含类型、必填、限制规则
- 边界异常覆盖网络超时、无权限、数据依赖、并发冲突
- 界面文案用「」标注
- 枚举值全部穷举

## 7. 关联资源

- **结构模板**：`references/prd_template.md` — PRD 完整章节模板
- **写作规范**：`references/writing_spec.md` — 字段表、验收标准、异常场景等专项规范
- **Word 转换**：`scripts/md_to_docx.js` — Markdown 转 Word 脚本
