# Changelog

## 1.3.0

Release theme: 从“第一次能顺手用”升级为“安装可信、重复导入干净、中文问题能命中”的稳定版本。

What changed:
- 新增 `kc doctor`，检查数据目录、JSON 存储、CLI 入口和 PATH 可用性；依赖缺失时也可用 `node bin/cli.js doctor` 做基础诊断
- 修复重复导入同一文件会重复创建来源记录的问题，来源现在按 canonical path 去重
- 强化中文自然语言查询，`kc answer "哪些文档把规划和强化学习连起来了？"` 这类问题会按关键词命中概念和来源
- HTML 答案页、HTML 图谱和 DOT 输出会转义用户输入、概念名和来源路径
- 修复 npm 包入口，`main` 现在指向 `src/index.js`
- 修正包元数据里的 GitHub owner，避免继续指向不可达的 `openclaw/knowledge-connector`
- 新增回归测试覆盖来源去重、中文问答命中、HTML/DOT 转义、doctor 自检和 CLI fallback

Suggested one-line changelog:
- Added install diagnostics, source de-duplication, safer HTML/DOT output, and better Chinese cross-document answering.

## 1.2.0

Release theme: 从“能导入和能搜索”继续升级为“第一次就能顺手用”的知识产品体验。

What changed:
- 新增 `kc import-wizard`，支持预览可导入文件和向导式导入
- 新增 `kc answer`，把跨文档搜索整理成更像答案页的结果
- 强化导入 onboarding 和结果表达，降低第一次使用门槛
- 更新文案，明确产品线继续往深度体验而不是更多相似 skill 发展

Suggested one-line changelog:
- Added an import wizard and answer-style cross-document results to make Knowledge Connector easier to onboard and more actionable.

## 1.1.0

Release theme: 从概念提取工具升级为更完整的知识产品线入口。

What changed:
- 把产品定位收敛到四个核心价值：导入体验、跨文档搜索、关系可视化、可操作结果
- 新增 `kc import-docs`，支持批量导入文件和目录
- 新增 `kc search`，返回跨文档概念、来源文档和下一步建议
- 新增 `kc map`，生成围绕单个概念的可操作子图
- 升级 HTML 可视化，加入下一步建议和常用后续命令
- 为知识库补充来源文档存储，让搜索和图谱更有上下文
- 重写 SKILL、README、package 文案，明确它是一条产品线而不是相似 skill 的拆分

Suggested one-line changelog:
- Upgraded Knowledge Connector into an action-oriented knowledge graph product with document import, cross-document search, relationship maps, and next-step guidance.
