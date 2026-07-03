# Knowledge Engineering — 使用说明

> 工业级 RAG 知识库原子化切片工具。将长文档拆解为语义完整、检索就绪的原子切片，内置多层质量门禁（校验 → 审计 → 检索可达性评估）。

---

## 1. 功能概览

将一份长文档（如技术手册、API 参考、项目文档）自动拆解为数十到数百个独立的 Markdown 切片文件，每个切片都是可被 RAG 系统独立检索的最小知识单元。

### 核心能力

- **语义拆分**：按概念、API、配置、指南自动分类，不截断代码块和表格
- **自包含转换**：每个切片可脱离原文独立理解，包含完整的定义、场景、示例、注意事项
- **检索优化**：自动生成 embedding_hint、hybrid_keywords、qa_pairs 等检索信号
- **多层质量门禁**：生成即校验（validate_slice）→ 批量审计（batch_audit）→ 检索评估（evaluate_retrieval）
- **版本管理**：自动检测版本差异，生成版本矩阵，标记废弃内容
- **断点续传**：中断后重试自动跳过已完成的切片

---

## 2. 环境要求

| 依赖 | 最低版本 | 安装命令 |
|:---|:---|:---|
| Python | 3.8 | 系统内置 |
| sentence-transformers | — | `pip install sentence-transformers` |
| numpy | — | `pip install numpy` |
| pyyaml | — | `pip install pyyaml` |

**一键安装**：`pip install sentence-transformers numpy pyyaml`

首次运行需下载约 90MB 的 sentence-transformers 默认模型。若网络受限，系统自动降级为 PurePythonEmbedder（TF-IDF，零外部依赖），不影响切片生成。

---

## 3. 快速开始

### 通过 AI Agent 使用（推荐）

在对话框中直接说：

```
把 C:\docs\redis-guide.md 切片，输出到 D:\kb\
```

Agent 自动完成分析 → 拆分 → 生成 → 校验全流程。10 片以内约 2 分钟完成。

### 常用指令

| 你要做什么 | 怎么说 |
|:---|:---|
| 切片一个文档 | `把 C:\docs\xxx.md 切片` |
| 指定输出位置 | `把 C:\docs\xxx.md 切片，输出到 D:\kb\` |
| 先看计划不生成 | `先看 C:\docs\xxx.md 的切片计划` |
| 大文档中断后继续 | 重新说原指令，Agent 自动跳过已有切片 |
| 修改分类 | `把 api_005 改成 config 分类` |
| 检索优化 | `检索死了，重新切片并优化 embedding_hint` |

---

## 4. 输出结构

切片完成后，输出目录下会生成以源文件名命名的文件夹，内部按内容类型分类：

```
输出目录/
└── redis-guide/
    ├── api/           # 函数签名、类定义、接口协议
    ├── config/        # 环境变量、配置文件字段、启动参数
    ├── guide/         # 安装部署、操作指南、故障排查
    ├── concepts/      # 架构原理、设计模式、术语定义
    ├── misc/          # Changelog、FAQ、附录
    ├── version_matrix.md   # 多版本差异对比
    └── evaluation_report.json  # 检索可达性评估
```

### 切片文件结构

每个 `.md` 切片包含固定五段内容：

```
─── YAML 头部（元数据：分类、标签、检索关键词）───
## 概念定义    ← 一句话说清"是什么"
## 使用场景    ← "什么时候用它"
## 核心内容    ← "怎么用"（代码/步骤/配置）
## 注意事项    ← "有什么坑"
## 相关链接    ← "还看什么"
```

---

## 5. 验收标准

切片完成后，Agent 会提供三项验收材料：

| 输出 | 说明 | 验收标准 |
|:---|:---|:---|
| 切片文件 | `.md` 文件 | 索引连续无遗漏、目录结构正确、内容可独立理解 |
| 审计报告 | 死链 / 缺失 / 异常 | 无死链、无孤儿切片、索引连续 |
| 检索报告 | R@1 / R@5 / MRR 评分 | R@1 ≥ 60%，死片数量 ≤ 5% |

---

## 6. 脚本速查

工具位于 `scripts/` 目录，通过 AI Agent 自动调用，也可手动执行：

| 脚本 | 用途 | 示例 |
|:---|:---|:---|
| `slice_generator.py` | 生成切片计划 | `python scripts/slice_generator.py input.md slices/ --json` |
| `validate_slice.py` | 单切片校验 | `python scripts/validate_slice.py slice.md --fix` |
| `batch_audit.py` | 批量审计 | `python scripts/batch_audit.py slices/ --fix` |
| `evaluate_retrieval.py` | 检索评估 | `python scripts/evaluate_retrieval.py slices/ --fix` |
| `platform_detect.py` | 平台检测 | `python scripts/platform_detect.py` |

---

## 7. 常见问题

**Q: 切片分类错了怎么办？**
A: 告诉 Agent `把 api_005 改成 config 分类`，Agent 会移动文件并更新索引。

**Q: 检索评分低（R@1 < 60%）？**
A: 告诉 Agent `检索死了，重新切片并优化 embedding_hint`。Agent 会重写检索信号，补充精确关键词。

**Q: 文档很大（> 10 万字）？**
A: Agent 会自动分批处理，每批 3~5 片。也可以先将文档拆成几个小文件分别切片。

**Q: 生成到一半中断了？**
A: 重新说一次原指令，Agent 会根据已有切片的 SELF_CHECK 标记自动跳过已完成部分。

**Q: 如何导入 RAG 知识库？**
A: 直接将生成的 `{Source-ID}/` 文件夹整体导入，各平台（Dify、FastGPT、AnythingLLM 等）均支持 `.md` 格式。

**Q: 支持哪些输入格式？**
A: 主要支持 `.md` `.txt` `.yaml` `.json`。PDF 建议先通过 Make-to-Markdown 转为 Markdown 再切片。

---

## 8. 版本记录

| 版本 | 日期 | 主要更新 |
|:---|:---|:---|
| v5.19 | 2026-06 | 文档精简：核心指令保留，运维参考移至 REFERENCE.md；HARB 安全红线 |
| v5.15 | 2026-04 | 多模态内容处理、消歧精度预检、版本差异摘要表 |
| v5.10 | 2026-02 | 分批协议增强、Token 预算估算公式、静默失败防护 |
| v5.0 | 2025-11 | 检索可达性评估（R@1/R@5/MRR）、PurePythonEmbedder 降级兜底 |
| v4.0 | 2025-08 | 二级目录智能分类、语义保真契约、自包含转换规则 |
| v3.0 | 2025-05 | 动态缓存、版本演进、元数据继承 |
| v2.0 | 2025-02 | 批量处理、错误恢复、进度跟踪 |
| v1.0 | 2024-11 | 初版，基础语义拆分与质量校验 |

完整更新记录和运维参考见 [REFERENCE.md](REFERENCE.md)。
