# knowledge-engineering 运维参考手册

> 本文档为 SKILL.md 的补充内容，包含多模态处理细节、元数据精化规则、可用性契约详细表格、检索精度验证规则、脚本详细文档、用户指南、能力边界、FAQ、平台兼容性、更新记录等运维参考资料。Agent 运行时核心逻辑见 SKILL.md。

## 1. 多模态内容处理契约（详细）

| 内容类型 | 切分策略 | 自包含转换要求 |
| :--- | :--- | :--- |
| Markdown 表格 | 整体保留，禁止跨切片截断 | 若表格 > 30 行：在原切片中保留前 5 行 + 摘要段落；完整表格数据单独输出为 `.csv` 或 `.json` 结构化文件 |
| Mermaid/图表 | 作为独立原子单元，不与前后文合并 | 必须在代码块上方添加 `> [!NOTE] 图表说明：{自然语言描述核心逻辑}` |
| 图片引用 | 保留原始链接，必须补充 Alt Text | 结合上下文生成语义描述；低置信度时标记复核 |
| LaTeX公式 | 完整保留数学表达式，禁止截断 | 复杂公式组独立成切片，并提供自然语言解释 |
| PDF表格/图表 | 使用 Agent 自身视觉能力提取完整内容 | 生成包含原始图片和文本内容的复合切片 |

## 2. 内容自包含转换规则（详细）

1. **标题全路径补全**：`{一级标题} > {二级标题} - {当前标题}`
2. **指令→描述（保真模式）**：需保留文件路径和参数含义，避免简化
3. **术语锚定**：首次出现的缩略语必须展开为 `全称 (Abbreviation)` 格式
4. **约束显式化**：安全/限制条款包含 [触发条件] + [后果] + [规避方案] 三要素
5. **跨切片引用**：拆分切片尾部添加续接链接，下一切片头部添加承接链接
6. **多模态内容描述**：图片/图表包含完整语义描述
7. **代码示例可执行性**：补全 import/include；声明外部变量来源；标注输入/输出格式
8. **语义保真转换**：数值原样保留；单位缺失时推断并标注；隐含假设显式化；因果链完整性
9. **双重引用机制**：YAML `cross_refs` + 正文末尾"相关链接"段落

## 3. 元数据字段精化规则

### embedding_hint
- 保留至少 1 个原文具体实体（数值/参数名/类名/配置项名/错误码）
- 区分度约束：同一 Source-ID 下每个 hint 必须包含至少 1 个差异化特征词

### structural_context
- 格式固定为 `{根章节} → {二级章节} → {本切片标题} :: {关系类型}`
- 关系类型：前置/并列/分支/补充

### hybrid_keywords
- 至少 2 个关键词来自原文直接提取
- 泛化词排除：配置/方法/使用/设置/功能/参数/选项/说明/介绍
- 同名但不同模块的函数加模块前缀

### qa_pairs
- 每个 q 必须包含具体实体名
- 至少 2 个，覆盖检索意图类型
- 语义相似度 > 80% 追加实体限定词

## 4. 切片可用性契约（详细表格）

### 上下文自足性

| 要求 | 违反示例 | 合规示例 |
|:---|:---|:---|
| 模块/命名空间锚定 | "调用 create_session() 即可" | "调用 myapp.auth.create_session() 即可" |
| 隐式依赖显式化 | "需要先完成初始化" | "需要先完成 myapp.init() 初始化（见 xxx.md）" |
| 版本定位声明 | 仅 YAML 有 version | 正文首段明确版本适用声明 |
| 术语本地定义 | 直接使用未展开缩写 | 展开为全称 (Abbreviation) |

### 示例可执行性

| 要求 | 规则 |
|:---|:---|
| Import 补全 | 代码块前以注释形式补全缺失的 import |
| 上下文变量声明 | 引用外部变量需注释标明来源 |
| 输入/输出标注 | 代码块前后各加 `> **输入**` / `> **输出**` |
| 运行环境声明 | 依赖特定版本时正文中显式声明 |

### 知识层级完整性

概念定义 → 使用场景 → 核心内容 → 注意事项 → 相关链接。缺失段落标注 `> [!NOTE] 原文未明确说明...`。

### 负面信息显式化

| 负面信息类型 | 呈现方式 |
|:---|:---|
| 硬限制 | 显式声明（如"最大支持 1000 条记录"） |
| 边界条件 | 标注临界值行为 |
| 常见陷阱 | `> [!CAUTION]` 或 `> [!WARNING]` |
| 版本废弃 | 正文顶部 `[!CAUTION]` + YAML `status: deprecated` |

### 检索信号完整性

| 信号类型 | 最低要求 | 关联字段 |
|:---|:---|:---|
| 语义信号 | embedding_hint 包含具体实体 | YAML embedding_hint |
| 精确匹配 | hybrid_keywords 至少 2 个原文提取 | YAML hybrid_keywords |
| 问答匹配 | qa_pairs 至少 2 个，覆盖意图类型 | YAML qa_pairs |
| 分类路由 | category 准确反映内容属性 | YAML category |
| 标签覆盖 | 领域+技术栈+动作三类标签 | YAML tags |

---

## 5. 语义保真与检索精度验证（详细）

### 事实保留验证

| 事实类型 | 检测方法 | 违规示例 | 合规示例 |
|:---|:---|:---|:---|
| 数值 | 原文具体数字是否在切片正文中保留 | YAML 有 version: "2.0"，正文写"新版本" | 正文写"从 v2.0 开始" |
| 参数名 | 原文配置键/参数名是否在正文中保留 | 原文 max_retry=3，切片写"设置重试次数" | 切片写"设置 max_retry=3" |
| 错误码 | 原文错误码/异常类型是否在正文中保留 | 原文 ERR_TIMEOUT，切片写"超时错误" | 切片写"抛出 ERR_TIMEOUT（超时错误）" |
| 路径/文件名 | 原文文件路径是否在正文中保留 | 原文 /etc/nginx/nginx.conf，切片写"配置文件" | 切片写"编辑 /etc/nginx/nginx.conf" |
| 命令 | 原文 CLI 命令是否完整保留 | 原文 kubectl apply -f deploy.yaml，切片写"执行部署" | 切片写"执行 kubectl apply -f deploy.yaml" |

### 隐含假设显式化

| 类型 | 标注格式 |
|:---|:---|
| 环境依赖 | `> [!IMPORTANT] 环境要求：{...}` |
| 权限要求 | `> [!IMPORTANT] 权限要求：需要管理员/root 权限` |
| 前置步骤 | `> [!NOTE] 前置步骤：需先完成 {...}` |
| 默认值 | 默认值为 8080（原文未说明变更方式） |
| 互斥条件 | `> [!WARNING] 限制：{...}` |

### 检索消歧机制

| 策略 | 实施方式 |
|:---|:---|
| 命名空间前缀 | hybrid_keywords 中用 `模块.实体名` |
| 参数特征标注 | embedding_hint 中标注参数差异 |
| 版本标记 | tags 中添加版本标签 |
| 场景限定 | embedding_hint 中标注场景 |
| 泛化词净化 | 排除黑名单：配置/方法/使用/设置/功能/参数/选项 |

### 检索精度自检项

- 同名冲突检测：是否存在两个切片 hybrid_keywords 包含相同精确关键词但指向不同内容
- 语义重叠检测：是否存在两个切片 embedding_hint 语义相似度 > 70%
- qa 唯一性检测：是否存在两个切片 qa_pairs 语义相似度 > 80%
- 泛化词残留检测：是否存在 hybrid_keywords 仅包含泛化词

---

## 6. 脚本详细文档

### validate_slice.py

```
用法: python validate_slice.py <slice_file> [--fix] [--json]
```
- 默认模式：检查 14 字段完整性 + 内容质量规则
- `--fix`：校验后将 SELF_CHECK 注释写入文件尾部
- `--json`：JSON 格式输出供 Agent 解析
- 必须调用时机：每个切片 write_file 写入后立即调用（带 --fix）

### batch_audit.py

```
用法: python batch_audit.py <slice_dir> [--fix] [--json]
```
审计项：索引连续性、死链检测、孤立切片、废弃命令、大小异常。
--fix 行为：生成 batch_audit_report.md + Jaccard Token Overlap 模糊匹配自动修正死链。
必须调用时机：每批/全部切片生成完毕后各调用一次。

### slice_generator.py

```
用法: python slice_generator.py <source.md> <output_dir> [--stubs] [--json] [--report] [--resume]
      python slice_generator.py --renumber <output_dir> [--dry-run]
```
模式：--json 输出切片计划、--stubs 创建 YAML 骨架桩文件、--report 打印拆分摘要、--resume 断点续传、--renumber 全局索引重排。

### evaluate_retrieval.py

```
用法: python evaluate_retrieval.py <slice_dir> [--fix] [--model MODEL_NAME]
```
评估指标：Recall@1（核心）、Recall@3、Recall@5、MRR。
阈值：死片 R@1=0.0 → 重构 hint；弱片 R@1<0.3 → 优化 hint 或增加 qa_pairs；正常 R@1≥0.3。
依赖：sentence-transformers，三层降级策略：SBERT → 自动安装 → PurePythonEmbedder（TF-IDF 加权多粒度 n-gram 哈希,512维）。

### platform_detect.py

平台检测模块（v5.12）：OS/架构/能力检测，含 sentence-transformers 可用性检测。

---

## 7. 用户指南

### 快速启动

说"把 xxx.md 切片"即可。可用的说法：`"把 xxx.md 切片"` / `"帮我把 xxx 拆成 RAG 切片"` / `"为 RAG 准备 xxx.md"` / `"看一下 xxx.md 的切片计划"`（只出计划）。

### 工作流

Agent 分析 10~30s → 确认计划（>10 片暂停确认）→ 逐批生成（每批 3~5 个）→ 验收结果。

| 输出 | 用途 |
|:---|:---|
| 切片文件 | 直接导入知识库 |
| 审计报告 | 确认索引连续性、死链、废弃命令 |
| 检索报告 | R@1/R@5/MRR 评分 |

### 常见操作

| 操作 | 指令 |
|:---|:---|
| 指定输出位置 | "把 C:\a.md 切片，输出到 D:\kb\" |
| 先看计划 | "先帮我看看 C:\a.md 的切片计划" |
| 增量追加 | "v2.1 新增的 API 追加切片到 D:\kb\api\" |
| 检索死了重切 | "重构 embedding_hint，重新切片 C:\a.md" |
| 从 docx 开始 | "把 D:\spec.docx 转成 md 然后切片" |

---

## 8. 反模式（完整）与 FAQ

### 完整反模式清单

| # | 反模式 | 正确做法 |
|:---|:---|:---|
| 1 | 跳过 analysis 直接切片 | 强制执行 analysis |
| 2 | 用脚本模板生成 embedding_hint/qa_pairs | Agent 推理生成 |
| 3 | 调用外部 API 生成内容 | Agent 自身完成 |
| 4 | 将大表格截断为多个切片 | >30 行保留前5行+摘要+输出为 .csv |
| 5 | 用泛化词做 keyword | 排除泛化词黑名单 |
| 6 | 未完成 analysis 前就写文件 | 分批协议强制 |
| 7 | 全部内容塞进一个切片 | 字数上限+语义拆分 |
| 8 | 忘记调用 validate_slice.py | 标准工作流强制 |
| 9 | 用 shell_executor 操作网络驱动器 | python_executor |
| 10 | 依赖"用户会先读到前置切片"假设 | 上下文自足性 |
| 11 | q 写成泛化提问 | q 必须包含实体名 |
| 12 | 不同切片用相同的 embedding_hint | 区分度约束 |
| 13 | 大文档中断后从头再来 | 断点续传 |

### FAQ

| 问题 | 解答 |
|:---|:---|
| 源文件是 .docx/.pptx | 先用 markitdown 提取为 .md 再切片 |
| 同步和异步版本 API 怎么切 | 各切一片，hint 标注差异化，keywords 加消歧前缀 |
| 大段注释代码要不要切片 | 不切。注释中说明性文字提取为废弃标记 |
| 切片内容高度重叠 | 合并语义重叠切片，保留信息更完整者 |
| 检索大量死片 | 检查 hint 是否包含精确实体名，--fix 验证 |
| 追加切片到已有知识库 | 传新内容源文件，输出到已有目录，自动延续索引 |
| 源文件编码非 UTF-8 | python_executor 先转 UTF-8 |
| 中断后恢复 | 重新说原指令，自动跳过已校验切片 |
| validate_slice.py 报 FAIL | 加 --json 获取详细原因 |
| batch_audit.py 报告死链 | 运行 --fix 自动模糊匹配修正 |

---

## 9. 能力边界

### 支持

| 输入格式 | 限制 |
|:---|:---|
| Markdown (.md) | 单文件 ≤ 50MB |
| 纯文本 (.txt) | 单文件 ≤ 10MB |
| YAML (.yaml/.yml) | 嵌套深度 ≤ 8 层 |
| JSON (.json) | 单文件 ≤ 20MB |

### 不支持

| 场景 | 替代方案 |
|:---|:---|
| 图片/音视频直接切片 | 先提取描述再切片 |
| 动态网页内容 | web_fetch → .md 再切片 |
| 跨文件关联切片 | 分别切片后手工关联 cross_refs |
| 英文 > 5 万词 / 中文 > 10 万字 | 拆分为多个源文件 |

### 边界情况

| 边界 | 行为 |
|:---|:---|
| 源文件不存在 | 立即终止，报错 |
| 源文件为空 | 终止，提示无内容 |
| 源文件无任何标题 | 按段落切分，标题兜底 |
| 单段落超 3000 字 | 按句号强制切分，标记语义不完整 |
| 全文件只有一个语义单元 | 输出 1 个切片，标记人工评估 |
| 输出目录已存在同名切片 | 覆盖写入 |

---

## 10. 平台兼容性

| 平台 | 状态 | 说明 |
|------|------|------|
| Windows | 完全支持 | pathlib.Path；网络驱动器需 python_executor |
| Linux | 完全支持 | pathlib.Path 原生适配 |
| macOS | 完全支持 | Homebrew Python 需确保 pip 包在 PATH |

关键约束：
- evaluate_retrieval.py 三层降级策略（SBERT → 自动安装 → PurePythonEmbedder）
- 所有脚本使用 pathlib.Path 自动适配路径分隔符
- 首次运行自动下载 BGE 模型（约 90MB），需网络连接

---

## 11. 更新记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v5.19 | 2026-06-09 | 综合审查修复：死引用修正、版本对齐 |
| v5.18 | 2026-06-08 | HARB 红线#11 系统破坏操作禁令；异常处理三段式规范化 |
| v5.17 | 2026-06-08 | evaluate_retrieval.py 查询感知文档向量混合增强；auto_fix_hints 占位符/非占位符双路径修复 |
| v5.16 | 2026-06-07 | platform_detect.py v1.0 零外部依赖；evaluate_retrieval.py 启动时平台检测路由 |
| v5.15 | 2026-06-07 | darwin-skill 优化：新增速查工作流表格；非核心章节拆分至 README.md |
| v5.13 | 2026-06-07 | 新增 4 个显式 CHECKPOINT/STOP 标记 |
| v5.12 | 2026-06-07 | 新增 platform_detect.py；evaluate_retrieval.py 三层降级路由 |
| v5.11 | 2026-06-07 | evaluate_retrieval.py 新增 PurePythonEmbedder |
| v5.10 | 2026-06-06 | batch_audit.py --fix 自动修正死链 |
| v5.9 | 2026-06-06 | 语义保真与检索精度双层强化；红线#10 |
| v5.8 | 2026-06-05 | validate_slice.py 存活校验增强 |
| v5.7 | 2026-06-05 | slice_generator.py 分类路由优化 |
| v5.6 | 2026-06-05 | 语义保真与检索精度强化；消歧预检 |

---

## 12. 异常处理（详细）

> 本章节为 SKILL.md §11 的详细补充，包含错误分类与精确处理命令、静默失败防护清单、错误信息格式规范。

### 12.1 错误分类与处理

| 错误类型 | 典型症状 | 原因 | 精确处理命令 |
|:---|:---|:---|:---|
| `源文件不可读` | 切片计划为空，报"文件不存在或无权限" | 路径拼写错误 / 网络驱动器断连 / 权限不足 | ① `python -c "from pathlib import Path; print(Path('<源文件路径>').exists(), Path('<源文件路径>').stat())"` 验证路径可达性 ② 网络驱动器走 `python_executor` |
| `切片数异常` | 实际生成数与计划不符，或全部切片为空 | `<analysis>` CoT 估算偏差 / 源文件格式异常 | ① `python scripts/slice_generator.py "<源文件>" <output_dir> --json` 获取修正计划 ② 对比 `<analysis>` 节的标题统计与脚本输出数量 |
| `校验失败 (致命)` | validate_slice.py 返回 FAIL，文件被重生成 | YAML 字段缺失 / 内容截断 / 指代词泄漏 | ① `python scripts/validate_slice.py "<切片路径>" --fix --json` 输出完整校验日志 ② 搜索 SELF_CHECK 注释中 `fatal_failed: true` 定位失败字段 |
| `索引不连续` | batch_audit.py 报告 index 有跳跃 | 某批切片写入失败未被察觉 | ① `python scripts/batch_audit.py "<切片目录>"` 列出缺失索引 ② 用 python_executor 解析审计报告定位缺口，进入断点续传：`python scripts/slice_generator.py "<源文件>" <output_dir> --resume` |
| `死链` | cross_refs 引用的切片文件不存在 | 被引用切片被重命名或未生成 | `python scripts/batch_audit.py "<切片目录>" --fix` 自动检测死链并修复 |
| `依赖缺失` | `ModuleNotFoundError: sentence-transformers` | Python 依赖未安装 | `pip install sentence-transformers numpy pyyaml` 后重新运行评估 |
| `检索死片` | evaluate_retrieval.py 报告 R@1=0 | embedding_hint 与切片内容语义偏离 | ① `python scripts/evaluate_retrieval.py "<切片目录>"` 输出死片清单（含评分明细） ② 逐一打开死片文件，重写 embedding_hint 加入正文精确关键词 |
| `Token 溢出` | 生成中断，报上下文超限 | 源文件过大，估算偏差 | 使用 §9.2 的分批确认机制，手动控制每批 ≤2 片；或 `python scripts/slice_generator.py "<源文件>" <output_dir> --json` 查看完整计划后分阶段执行 |
| `编码错误` | 切片中文变乱码 | write_file 未使用 UTF-8 | ① `python -c "import chardet; print(chardet.detect(open('<文件>','rb').read()))"` 检测实际编码 ② 若非 UTF-8，用 `python -c "open('<文件>','r',encoding='gbk').read()"` 另存为 UTF-8 |
| `目录冲突` | 分类降级后文件路径重复 | 同名分类前缀 + 相同 index | `python scripts/batch_audit.py "<切片目录>"` 检测冲突；用 python_executor 扫描冲突文件后手动重编号 |

### 12.2 静默失败防护

以下错误在历史版本中容易无声失败，当前版本已加入显式检查：

| 静默失败形态 | 检测机制 | 对应条款 |
|:---|:---|:---|
| 切片写入成功但 YAML 被 AIGC 水印覆盖 | §4.1 强制校验 — 检测到立即重写 | §4.1 |
| 代码块被截断但未触发回溯保护 | §4.2 语义完整性检查项 | §2 P3 回溯保护 |
| cross_refs 引用不存在切片 | batch_audit.py 死链检测 | §8.3 |
| embedding_hint 泛化导致检索不到 | evaluate_retrieval.py R@1 检测 | §8.5 |
| qa_pairs 过于泛化可匹配多个切片 | §5 检索精度自检（qa 唯一性检测） | — |
| 废弃命令仍在代码块中无标记 | §4.2 致命项 + batch_audit.py 终结审计 | §2.6.9 |

### 12.3 错误信息格式

所有脚本和 Agent 错误信息必须遵循三段式：

```
[类型]: 发生了什么
原因: 为什么发生
操作: 如何修复
```

示例：
```
[校验失败] 切片 D:\kb\api\api_003-auth.md YAML 缺少 embedding_hint 字段
原因: Agent 生成切片时跳过了 embedding_hint 的填充
操作: 重新生成该切片，确保 YAML 中包含 embedding_hint（≤200字，包含至少1个实体名）
```
