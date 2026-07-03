---
name: knowledge-engineering
description: "工业级RAG切片工具「可落地、可量化、可优化」,将RAG知识库长文档拆解为语义完整、检索就绪的原子化知识切片，内置多层质量门禁（校验→审计→检索可达性评估），确保切片可用性与RAG检索命中率。"
keywords: ["rag", "切片", "知识库", "语义分割", "检索增强生成", "chunking", "文档拆分", "质量门禁", "embedding-hint", "self-check", "PurePythonEmbedder", "retrieval-evaluation", "cross-refs"]
version: "5.19"
metadata:
  domain: "knowledge-engineering"
  author: "智慧半岛"
  platform:
    windows: full
    linux: full
    macos: full
  openclaw:
    requires:
      bins:
        - python
    emoji: "📚"
---

> 文档结构：SKILL.md = 核心运行时指令（Agent 执行必读），REFERENCE.md = 扩展参考与运维细节。非核心内容不得写入本文件。

# RAG知识库原子化切片控制器 (Auto-Archiving & Semantic-Preservation Edition)

> 🟢 **最小可用示例**：`python scripts/slice_generator.py input.md slices/`。完整工作流见 §0-§14，异常处理见 §11。

## 速查：标准工作流 (Quick Reference)

从源文件到检索就绪切片的完整路径，5 步闭环：

| 步骤 | 动作 | 工具/方式 | 输出 | 对应章节 |
|:---|:---|:---|:---|:---|
| ① 分析 | 结构扫描 + Token预算 + 熔断预演 + 目录决策 | `<analysis>` CoT | 切片计划清单 | §0 |
| ② 计划 | 自动生成分类路由与拆分方案 | `slice_generator.py --json` | JSON 切片计划 | §8.4 |
| ③ 生成 | 逐切片填充语义内容 + 写入磁盘 | Agent 按 §3 模板生成 | 带完整 YAML 的 .md 切片 | §3, §6-7 |
| ④ 校验 | 单切片完整性 + 跨切片审计 | `validate_slice.py --fix` → `batch_audit.py` | 致命项重生成 / 警告标记 | §4, §8.2-8.3 |
| ⑤ 终检 | 检索可达性评估（R@1/R@5/MRR） | `evaluate_retrieval.py --fix` | 检索报告 + 死片/弱片修复 | §8.5 |

## Goal
作为 RAG/知识库管线的核心 ETL 引擎，将长文档拆解为**语义完整、物理隔离、自包含、检索就绪**的 L0 级原子切片。
**核心使命**：在严格执行目录隔离的同时，确保切片既是独立的检索单元，又是原文语义的无损投影——保留事实精度、消除检索歧义、支持混合检索与自动化质量门禁。

## ⛔ 核心红线 (Critical Constraints)
1.  **目录绝对隔离**：每个源文件必须生成同名专属文件夹。严禁任何切片文件直接存在于输出根目录。
2.  **语义完整性优先于长度限制**：当字数熔断点位于代码块、表格、步骤列表或逻辑论证中间时，**必须**延后至当前语义单元结束处切分，禁止截断原子逻辑。
3.  **禁止破坏性改写**：自包含转换仅允许"补充"和"显式化"，严禁删除原文技术参数、修改代码逻辑或替换专业术语。
4.  **零指代原则**：切片内不得出现未定义的 `this`, `it`, `上述`, `如下` 等依赖外部上下文的指代词。
5.  **废弃内容显式标记**：检测以下任一形态的废弃声明——英文：`deprecated` `obsolete` `removed in` `no longer supported`；中文：`已弃用` `已废弃` `已移除` `不再支持` `替代方案`；表格中"废弃/移除"列的每一行。检测到后必须在正文首段前强制插入 `> [!CAUTION] ⚠️ {具体功能} 已在 {version} 中废弃，替代方案见 {related_slice}`，并在 YAML 中标记 `status: deprecated`。若版本号未知，写"某个版本"并标记 `human_review_required: true`。
6.  **多模态内容完整性**：图片、表格、图表等非文本内容必须保留完整语义，不得截断或丢失关键信息。
7.  **禁止脚本模板生成元数据**：`embedding_hint`、`qa_pairs`、`hybrid_keywords`、`tags` 等语义元数据必须由 Agent 自身推理生成，严禁使用 Python 脚本中的规则引擎、正则模板或字符串填充等方式替代。
8.  **禁止外部 LLM API**：禁止调用任何外部 LLM API（包括但不限于 Ollama、OpenAI API 等）来生成切片内容、摘要或元数据，所有生成工作必须由 Agent 自身完成。
9.  **网络驱动器路径约束（平台自适应）**：涉及网络驱动器（如 X: 盘、E:\Marvis_Data 等）上的文件读写操作时，Agent 应按以下优先级选择执行器：
    - **Windows 网络驱动器**：优先使用 `python_executor`，避免 `shell_executor`（PowerShell/cmd 可能因 WinError 2 找不到网络驱动器路径）
    - **Linux/macOS NFS/CIFS 挂载**：`shell_executor` 通常可用，但路径中含空格或特殊字符时回退到 `python_executor`
    - **自动检测**：脚本内部使用 `pathlib.Path` 处理路径，无需硬编码平台判断；`evaluate_retrieval.py` 等依赖外部模型的脚本需提供纯 Python 降级兜底
10. **语义保真原则**：切片必须保留原文的关键事实信息，不得遗漏或弱化——
    - **事实保留**：关键数值（超时 30s / 阈值 80% / 限制 1000 条）、参数名（max_retry / api_key）、错误码（ERR_TIMEOUT / 403）、配置项（config.yaml 字段）等事实数据必须原样出现在切片正文中，禁止仅靠 YAML 元数据间接引用
    - **隐含假设显式化**：原文中未明说但影响正确性的假设（如"需要管理员权限""默认端口 8080""依赖 systemd"）必须提取为显式声明
    - **因果链锚定**：若切片内容是一个因果链中的一环（A 导致 B，B 导致 C），必须在正文中显式标注其前置因果 `> [!IMPORTANT] 前置条件：{A 的发生机制}`，防止孤立切片产生误导
11. **系统破坏操作禁令 (HARB)**：以下高风险行动黑名单中的命令，Agent 在任何阶段均不得自动执行，必须输出完整命令预览并等待用户显式确认：
    - **文件系统破坏**：`rm -rf` / `del /f /s` / `Remove-Item -Recurse -Force` 等递归强制删除 | 格式化（`format` / `mkfs`） | 对工作目录外任意路径的批量写操作
    - **数据不可逆丢失**：`git reset --hard` / `git clean -fdx` | 数据库 `DROP TABLE` / `TRUNCATE` / `DROP DATABASE` | 清空回收站 | `shred` / `wipe` 等安全擦除
    - **系统级破坏**：`diskpart clean` | 注册表 `reg delete` 批量删除 | `sc delete` 删除系统服务 | `bcdedit` 修改引导配置
    - **批量不可逆操作**：对 >50 个文件或目录的单次删除/覆盖 | 对 >10 个 Git 仓库的单次 `push --force` / `reset --hard`
    违反本禁令的脚本或流水线必须被拒绝执行并告知用户原因

## Prerequisites (环境依赖)

使用本 skill 前请确认以下环境已就绪：

| 依赖项 | 最低版本 | 安装命令 | 说明 |
|:---|:---|:---|:---|
| Python | 3.8 | — | 全平台通用，Windows/Linux/macOS 均可 |
| sentence-transformers | — | `pip install sentence-transformers` | 检索评估（§8.5），首次运行自动下载默认模型 ~90MB |
| numpy | — | `pip install numpy` | 数值计算支撑 |
| pyyaml | — | `pip install pyyaml` | YAML 切片元数据解析 |

**一键安装**：`pip install sentence-transformers numpy pyyaml`

**磁盘空间**：首次运行需额外 ~90MB（模型下载）。若网络受限，sentence-transformers 缺失时系统自动降级为 PurePythonEmbedder（TF-IDF，零外部依赖，评估精度约 SBERT 的 75-85%），不影响切片生成流程。

> 💡 **平台差异提示**：网络驱动器路径在 Windows 下建议通过 `python_executor` 而非 `shell_executor` 访问（详见红线 #9）。

## 0. 预处理思维链 (Pre-computation CoT) [强制执行]
在生成任何切片文件之前，**必须**先在 `<analysis>` XML标签内完成以下推理（此标签内容不计入最终切片输出）：
1.  **结构扫描**：列出所有 H1-H3 标题，识别并列/递进关系。
2.  **原子单元标记**：识别所有不可分割的代码块、表格、Mermaid图、LaTeX公式，标记其起止字符位置。对于超长代码块（>50行），判断是否可按方法/分支/逻辑段做语义再拆分，显式声明"此代码块不可再拆分"或"已拆分为 N 个子切片"。
3.  **Token 预算估算**：中文按 1 字 ≈ 1.5 Token、代码按 1 字符 ≈ 0.3 Token、英文按 1 词 ≈ 1.3 Token 估算全文总 Token。若回溯后切片 Token 数 > 模型容量上限的 60%，强制采用"移至下一切片"策略。
4.  **熔断点预演**：按差异化软上限（见 §2）模拟切分，检查是否命中原子单元。若命中，计算回溯/延后成本。
5.  **多模态盘点**：统计各类非文本元素数量及分布密度。创建 `multimodal/` 子目录的条件：多模态元素 ≥ 5 个 **且** 占全文总内容比例 ≥ 25%。若单个切片中多模态元素 < 2 个，不创建 `multimodal/` 子目录，保持原有分类路由。
6.  **版本/废弃检测**：扫描 deprecated/version 关键词，规划警告标记位置及版本矩阵生成需求。
7.  **目录决策**：基于上述分析，确定最终的二级目录结构、降级策略应用结果及完整文件名列表。
8.  **可用性预检**：逐切片预判独立检索场景下的可用性——
    - 检索到此切片后，用户是否需要额外上下文才能理解？（是 → 必须在正文中补充模块/命名空间/前置概念锚定）
    - 代码示例能否脱离原文独立理解？（否 → 补全必要的 import 语句与上下文变量声明）
    - 是否遗漏了该知识点的限制条件、边界情况和常见陷阱？
    - qa_pairs 是否覆盖了该切片最可能被检索到的 3 类意图（how-to / what-is / troubleshooting）？
9.  **命令有效性预检**：对代码块中的每个 CLI 命令/API 调用进行时效性校验——
    - 对照版本差异速查表中的"废弃/移除"清单，标记已废弃命令
    - 标注命令首次引入版本和（如有）废弃版本
    - 已废弃命令必须在代码块上方添加 `> [!CAUTION] ⚠️ 此命令已在 {工具名} {版本} 中废弃，替代命令：{正确命令}`
    - 已废弃命令不应作为核心示例，除非切片主题本身就是版本迁移指南
10. **消歧与精度预检**：逐切片识别检索冲突风险——
    - **同名冲突**：是否存在多个切片包含同名函数/配置项/类名？（是 → 在 hybrid_keywords 中添加消歧前缀，如 `auth.create_session` vs `db.create_session`）
    - **语义重叠**：是否存在多个切片描述相似但细节不同的内容？（是 → 在 embedding_hint 中强调差异化特征，如"异步版本""仅限 Windows""v2.0 新增"）
    - **泛化词陷阱**：hybrid_keywords 是否包含无区分度的通用词（"配置""方法""使用""设置"等）？（是 → 替换为具体实体名）
    - **检索噪声预估**：该切片的 embedding_hint 是否可能匹配到无关查询？（是 → 增加限定词缩小语义范围）
> ⚠️ 未完成 `<analysis>` 直接输出切片视为严重违规。
> 
> 🛑 **STOP CHECKPOINT**：`<analysis>` 完成后，**必须暂停**，将分析结果（结构扫描 / 原子单元标记 / 熔断预演 / 目录决策）以摘要形式输出给用户确认。确认后开始生成切片文件。禁止跳过确认直接进入批量切片生成。

## 1. 动态目录与路由契约 (Directory & Routing Contract)

### 1.1 源文件指纹与元数据继承
-   **Source-ID**：取文件名（不含后缀）作为唯一标识。
-   **元数据继承**：从源文件 Frontmatter 或首段提取 `version`, `author`, `last_updated`，注入到每个切片的 YAML 头中。若原文缺失，标记为 `unknown`。
-   **强制动作**：创建 `{Source-ID}/` 文件夹作为所有输出的根容器。

### 1.2 二级目录智能分类
在 `{Source-ID}/` 内部按内容属性路由：
-   `api/`: 函数签名、类定义、接口协议。
-   `config/`: 环境变量、配置文件字段说明、启动参数、部署配置项。与 `api/`（接口签名）互斥，`api/` 不再接收配置项说明。
-   `guide/`: 安装部署、操作指南、故障排查步骤。
-   `concepts/`: 架构原理、设计模式、术语定义。
-   `misc/`: Changelog、FAQ、附录、许可证。
-   `multimodal/`: 包含图片、表格、图表等多模态内容的特殊处理区域（当且仅当多模态元素 ≥ 5 且占比 ≥ 25% 时创建）。

> 💡 **动态降级与防抖动策略**：
> -   若某分类下切片数 ≤ 2 **且** 总字数 < 1500字 → 合并至 `{Source-ID}/` 根目录，文件名保留分类前缀（如 `concept_001-xxx.md`）。
> -   若某分类下切片数 ≤ 2 **但** 总字数 ≥ 1500字 → **仍创建子目录**，避免单文件过大影响检索粒度。
> -   **缓冲区防抖**：字数在 1300~1700 之间时，额外考虑切片数：
>     - 若切片数为 2 且各切片字数均 ≥ 600，仍创建子目录；
>     - 若切片数为 2 但某一切片 < 600 字，合并至根目录（避免单切片过小而目录碎片化）；
>     - 若切片数为 1，不建子目录。
>     避免阈值临界点（1499 vs 1501）导致目录结构震荡。
> -   **多模态降级**：若多模态内容过于分散（单个切片中多模态元素 < 2个），则不创建 `multimodal/` 子目录，保持原有分类。
> -   **结构稳定性**：除非内容变更超过 30%，否则增量更新时应保持原有目录结构不变，避免索引频繁失效。

### 1.3 版本演进处理
-   **版本冲突检测与差异摘要**：同一 `Source-ID` + `category` + 相似标题下存在多个 `version` 时，自动生成 `version_matrix.md` 索引切片。该文件 **必须强制包含版本差异摘要表**，表结构固定为：

    | 版本 | 新增 | 修改 | 废弃/移除 | 备注 |
    |:---|:---|:---|:---|:---|
    | {version} | {新增内容简述} | {修改内容简述} | {废弃/移除项} | {补充说明} |

    "废弃/移除"列不可省略，即使某版本无废弃项也必须填入 `-`。
-   **废弃标记**：严格执行核心红线第5条。
-   **多版本内容处理**：当同一语义单元包含多个版本信息时，创建独立的版本切片并建立关联引用。

### 1.4 源文件缺失或不可读处理
若在 `<analysis>` 阶段发现源文件路径不存在、无法访问或无读取权限：
-   **立即终止**：不生成任何切片文件，不创建空目录。
-   **明确报错**：输出源文件路径及具体失败原因（不存在 / 权限不足 / 格式不支持），提示用户检查路径是否正确。
-   **禁止凭空生成**：严禁基于文件名猜测内容或创建空白切片占位。

> 🔴 **CHECKPOINT**：命中此条件时，必须立即向用户报告并等待用户提供正确路径，禁止跳过继续执行。

## 2. 智能拆分触发器 (Smart Splitting Triggers)

采用 **"语义优先，字数兜底，回溯保护"** 的三重判定机制。字数软上限按内容类型差异化：

| 内容类型 | 字数软上限 | 代码行数软上限 | 说明 |
|:---|:---|:---|:---|
| 纯文本为主 | 700 字 | - | 适用于教程、概念说明、纯文档 |
| 代码为主 | 500 字 | 40 行 | 适用于 API 参考、配置示例、代码清单 |
| 混合内容 | 加权计算 | 40 行 | `(文本字数 × 1.0 + 代码字数 × 1.4 + 表格单元格数 × 0.3) / 内容段数`，结果 > 700 时触发。内容段数 = 按 H2/H3 标题分段的段落数，最少计为 1 |

| 优先级 | 触发条件 | 执行动作 | 例外/回溯保护 |
| :--- | :--- | :--- | :--- |
| P0 | 独立 API/类/配置项 | 立即切分为独立文件 | 若含超长示例代码（>40行），主体描述为一个切片（标注示例引用），示例代码独立为 `{prefix}_examples.md` 切片，两者通过 `cross_refs` 互链 |
| P1 | 并列结构 (Step/List) | 每个顶层步骤/条目独立成切片 | 子步骤嵌套过深时，父步骤+子步骤合并 |
| P2 | 语义段落自然边界 | 在段落/章节交界处切分 | 禁止在句子中间切分 |
| P3 | 字数软上限触发 | 寻找最近的语义边界切分 | **回溯保护**：若最近边界在代码块/表格内，必须回溯至该块起始处；若回溯后切片 > 1500 字，则将整个块移至下一切片，当前切片末尾添加 `[!NOTE] 完整{代码/表格}见 {next_slice}` |

### 2.5 多模态内容处理

表格/Mermaid/图片/LaTeX/PDF 图表的切分策略、自包含转换要求见 [REFERENCE.md §1](REFERENCE.md)。核心原则：表格 > 30 行保留前 5 行 + 输出 .csv；图表独立原子单元不合并；图片必须补 Alt Text。

### 2.6 内容自包含转换规则 (Non-Destructive Transformation)

8 条核心规则：标题全路径补全、指令→描述保真模式、术语锚定、约束显式化（条件+后果+规避三要素）、跨切片 `📎` 引用、代码可执行性（补 import/I/O/环境声明）、语义保真（数值+单位+隐含假设+因果链）、双重引用（YAML cross_refs + 正文相关链接）。完整条款见 [REFERENCE.md §2](REFERENCE.md)。

## 3. 标准化输出格式 (Standard Output Format)

每个切片必须严格遵循以下模板（注意：YAML 中的输出格式示例仅为字段说明，实际生成时请替换为真实内容）：

    ---
    title: "{全路径标题}"
    source_id: "{Source-ID}"
    category: "{api|config|guide|concepts|misc|multimodal}"
    index: {三位数序号，如 001}
    version: "{继承自原文或 unknown}"
    status: "{active|deprecated|beta}"
    tags: [{自动提取的3-5个关键词}]
    embedding_hint: "{去除代码/表格后的纯语义摘要，≤200字。必须包含至少1个具体数值/参数名/类名/配置项名，确保精确关键词匹配}"
    structural_context: "{根章节} → {二级章节} → {本切片标题} :: {与前序切片的关系：前置/并列/分支/补充}"
    hybrid_keywords: ["精确匹配词1", "精确匹配词2", "精确匹配词3", "..."]  # 3~7个，至少2个为原文直接提取
    cross_refs:
      depends_on: ["{前置依赖切片ID}"]
      related_to: ["{相关概念切片ID}"]
    qa_pairs:  # 至少1个，推荐2~3个
      - q: "{具体问题，必须包含实体名：API名/配置项/错误码，禁止泛化提问如'如何设置？'}"
        a: "{自包含答案，必须包含关键参数/步骤/结论}"
        type: "{how-to|what-is|troubleshooting|comparison}"
      - q: "{另一个具体问题}"
        a: "{自包含答案}"
        type: "{how-to|what-is|troubleshooting|comparison}"
    multimodal_refs:
      - type: "{image|table|chart|formula}"
        id: "{content_id}"
        path: "{relative_path_to_multimodal_content}"
    human_review_required: {true|false}
    ---

    # {全路径标题}

    > [!INFO] 📄 来源：{Source-ID}.md | 🏷️ 分类：{category} | 📅 更新：{last_updated}

    ## 概念定义
    {该知识点的简明定义，1~3 句话回答"是什么"。若术语在原文其他位置首次定义，此处必须重新定义或以 `> [!NOTE]` 引用定义切片}

    ## 使用场景
    {该知识点适用于什么问题/场景，回答"什么时候用"}

    ## 核心内容
    {已完成自包含转换的正文——方法、步骤、配置、代码等具体内容}

    ## 注意事项
    {限制条件、边界情况、常见陷阱、版本兼容性约束。若原文未提及，标注 `[!WARNING] 原文未明确说明限制条件，需人工补充`}

    ## 相关链接
    {通过 cross_refs 链接到前置依赖和相关概念切片}

    > 📎 续接切片：{下一切片文件名}

### 3.1 元数据字段精化规则

`embedding_hint` 包含具体实体名 + 区分度约束；`structural_context` 固定格式；术语本地定义 + hybrid_keywords 实体提取 + 泛化词排除；qa_pairs 含实体名 + 唯一性验证。完整规则见 [REFERENCE.md §3](REFERENCE.md)。

## 4. 输出后自检协议 (Post-Generation Self-Correction)

每个切片写入磁盘后，**必须立即**执行以下校验并在文件尾部追加自检注释。若命中任何 🔴 致命项，**立即重生成该切片**直至通过，**不允许进入下一批**。

### 4.1 YAML Frontmatter 完整性强制校验 [最高优先级]

切片写入后立即执行，不可推迟到下一批次：

1. 重新读取刚写入的文件
2. 检查第一个 `---` 块是否包含全部 14 个必填字段：`title`, `source_id`, `category`, `index`, `version`, `status`, `tags`, `embedding_hint`, `structural_context`, `hybrid_keywords`, `cross_refs`, `qa_pairs`, `multimodal_refs`, `human_review_required`
3. 若检测到 `AIGC:` 等外部水印覆盖了标准 YAML 块，**必须在文件头部追加第二个 `---` 块**，将完整标准元数据写入
4. 校验失败立即重写该切片，不做"下一批统一修复"的延迟处理

### 4.2 阻断式分级自检

| 级别 | 含义 | 处理方式 |
|:---|:---|:---|
| 🔴 致命 | 检索或语义完整性被破坏 | 立即重生成该切片 |
| 🟡 警告 | 影响质量但不致命 | 标记 `human_review_required: true`，允许继续 |
| 🟢 建议 | 规范合规性 | 记录但允许通过 |

#### 🔴 致命（必须重生成）

> 🛑 **STOP**：任何致命项命中后，**必须立即停止当前批次**，输出已发现的致命问题清单，重新生成该切片。重新生成后再次执行全部自检。禁止忽略致命项继续下一批。

- [ ] **目录隔离**：文件路径是否符合 `{Source-ID}/{category}/` 规范？
- [ ] **语义完整**：代码块/表格/列表是否被截断？回溯保护是否生效？
- [ ] **零指代**：正文是否存在未定义的 this/it/上述/如下？
- [ ] **事实保真**：原文关键数值/参数名/错误码/配置项是否原样保留在切片正文中？是否出现数值替换或模糊化？
- [ ] **YAML 完整性**：全部 14 个必填字段是否存在？（见 §4.1）

#### 🟡 警告（标记 human_review_required: true，允许继续）
- [ ] **标题全路径**：标题是否严格遵循 `一级>二级>当前` 格式？
- [ ] **元数据质量**：embedding_hint ≤200字 且 包含至少 1 个原文实体（数值/参数名/类名/配置项名）？ structural_context 非空且符合 `{根章节} → {二级章节} → {本切片标题} :: {关系类型}` 格式？ qa_pairs 至少 2 个且覆盖必要意图类型？ hybrid_keywords 至少 2 个为原文直接提取且总量 3~7 个？ tags 是否包含领域+技术栈+动作三类标签？
- [ ] **多模态契约**：图片是否有 Alt Text？大表格是否已输出结构化数据文件？
- [ ] **可用性五维**（§6）：上下文自足性（模块锚定/术语本地定义）？示例可执行性（import补全/I/O标注）？知识层级（五段完整）？负面信息（限制/边界/陷阱）？检索信号（qa_pairs意图覆盖/tags三类）？
- [ ] **检索精度**（§7）：embedding_hint 是否含差异化特征词？hybrid_keywords 是否排除了泛化词？是否存在同名冲突需消歧前缀？qa_pairs 是否通过跨切片唯一性验证？

#### 🟢 建议（记录但允许通过）
- [ ] **废弃标记**：deprecated 内容是否有 `[!CAUTION]` 警告及 YAML 标记？
- [ ] **人机协作**：不确定内容是否已标记 `human_review_required: true`？
- [ ] **跨切片引用**：拆分切片是否包含承接/续接链接？

### 4.3 自检注释写入 [强制执行]

每个切片文件尾部必须追加以下格式的自检注释：

```
<!-- SELF_CHECK:
  fatal_passed=[true|false]
  fatal_failed=[失败项列表，全部通过写 none]
  warning_items=[警告项列表，全部通过写 none]
  action=[pass|regenerate|mark_review]
-->
```

若 `fatal_passed=false`，立即重生成该切片。若 `action=mark_review`，YAML 中 `human_review_required` 必须设为 `true`。

## 5. 分批处理协议 (Token Budget Awareness)
当源文档预估切片数 > 10 或总 Token 接近上下文窗口 70% 时：

> 🔴 **CHECKPOINT**：触发分批条件后，**必须暂停**，先输出 `<analysis>` 摘要和切片清单预览。等待用户明确确认后再进入分批生成。禁止自动跳过确认直接全量生成。

1.  先输出完整的 `<analysis>` 及 **切片清单预览**（仅文件名+标题+分类）。
2.  等待用户确认或自动继续后，再逐批（每批 3~5 个切片）生成完整内容。
3.  每批结束时输出进度标记：`<!-- BATCH_COMPLETE: {current}/{total} -->`。

**每批结束后强制追加批审计注释**：

```
<!-- BATCH_AUDIT:
  batch: {current}/{total}
  files: [本批文件名列表]
  index_start: {本批第一个index}  index_end: {本批最后一个index}
  index_gap: [若与上批末尾index间隔≠1，记录缺失的index]
  orphans: [本批中未被前批任何切片"续接链接"引用的切片，无则写 none]
  size_anomalies: [本批中大小偏离全部已生成切片均值 > 50% 的切片及原因，无则写 none]
-->
```

**全部批次完成后，强制执行终结校验**（在最后一批的批审计注释中追加）：

```
<!-- FINAL_AUDIT:
  total_files: {N}
  index_continuity: [1..{N} 是否有遗漏，列出缺失索引号]
  cross_ref_validity: [所有 YAML cross_refs 中的引用切片是否真实存在，列出死链]
  orphan_slices: [未被任何其他切片 cross_refs 引用的切片，列出文件名]
  deprecated_commands: [所有代码块中检测到的已废弃命令及所在切片]
-->
```

若终结校验发现索引不连续或死链，必须修复后重新输出受影响的切片。终结校验不通过不得声称任务完成。

**Token 估算公式**（在 `<analysis>` 阶段显式计算）：
- 中文文本：1 字 ≈ 1.5 Token
- 代码：1 字符 ≈ 0.3 Token
- 英文文本：1 词 ≈ 1.3 Token
- 公式/表格：按单元格数 × 2 Token 估算


## 6. 切片完整可用性契约 (Slice Completeness & Usability Contract)

每片生成后逐项自检以下五维（必须全部 ✅）：

**上下文自足性**：`description` 是否包含模块名？`cross_refs` 是否声明所有前置依赖切片？正文首段是否有术语本地定义？

**示例可执行性**：代码块是否补全了 import 语句？输入/输出是否有明确标注（路径/类型/预期值）？是否声明了运行环境（OS/Python 版本）？

**知识层级**：正文是否覆盖五段——是什么（定义）→ 何时用（场景判断）→ 怎么做（步骤/代码）→ 注意什么（边界/限制）→ 还看什么（cross_refs 链接）？

**负面信息**：硬限制是否显式列出？废弃 API 是否标注替代方案？已知陷阱是否在正文中标记？

**检索信号**：keyword 是否覆盖语义+精确+问答+分类+标签五类信号？`embedding_hint` 是否包含正文核心关键词的精确拼写？

> 完整检查项（含 qa_pairs 意图覆盖规则）见 [REFERENCE.md §4](REFERENCE.md)。



## 7. 语义保真与检索精度契约 (Semantic Fidelity & Retrieval Precision)

每批切片生成后逐项自检以下五维：

| 维度 | 检查项 | 失败特征 |
|:---|:---|:---|
| 事实保留 | 数值/参数/错误码/路径/命令逐项与源文件核对 | YAML `fact_ violations` 非空 |
| 隐含假设 | 环境/权限/前置依赖/默认值/互斥关系五类均已显式声明 | 正文含模糊限定词（"一般"/"通常"）但未标注条件 |
| 因果链 | 标注规则：起点（触发条件）→ 中间（转换逻辑）→ 终点（预期结果） | 缺少任一环节导致步骤断链 |
| 检索消歧 | 命名空间前缀/参数特征/版本标记/场景限定均已嵌入 | 同名概念跨切片 `keyword` 相同 |
| 精度自检 | `batch_audit.py` 报告同名冲突=0、语义重叠=0、泛化词残留=0 | 冲突数 > 0 或泛化词未净化 |

> 完整规则见 [REFERENCE.md §5](REFERENCE.md)。

## 8. 复用脚本体系 (Reusable Scripts)

> 🩺 **症状→脚本速查**：以下映射表覆盖常见问题与对应脚本，无需通读 §8 全文。

| 症状 | 运行 | 章节 |
|:---|:---|:---:|
| 单切片 YAML 缺字段 / 内容不规范 | `python scripts/validate_slice.py <file> --fix --json` | §8.2 |
| 批量切片索引不连续 / 死链 | `python scripts/batch_audit.py <dir> --fix` | §8.3 |
| 需要生成切片计划 JSON / stub | `python scripts/slice_generator.py <src> <out> --stubs --json` | §8.4 |
| 检索评估：想知道 R@1/R@5/MRR | `python scripts/evaluate_retrieval.py <dir> --fix` | §8.5 |
| 全局索引重排（插入/删除切片后） | `python scripts/slice_generator.py --renumber <dir>` | §8.4 |
| 不确定当前环境平台/模型能力 | `python scripts/platform_detect.py` | §8.6 |
| 计划中断，需要恢复 | `python scripts/slice_generator.py <src> <out> --resume` | §8.4 |

skill 的 `scripts/` 目录内置五个复用脚本。Agent 不得手动重写同类逻辑，必须通过 `python_executor` 调用脚本。

### 8.1 脚本清单

`validate_slice.py` / `batch_audit.py` / `slice_generator.py` / `evaluate_retrieval.py` / `platform_detect.py`。存在性自检 oneliner 及各脚本详细用法见 [REFERENCE.md §6](REFERENCE.md)。

### 8.6 标准工作流

```
1. slice_generator.py --json    → 获取切片计划
2. Agent 逐切片填充语义内容 + write_file
3. validate_slice.py --fix      → 每片写入后立即校验
4. batch_audit.py               → 每批/全部完成后审计
5. evaluate_retrieval.py --fix  → 检索可达性终检
```

## 9. 使用指南与能力边界 (User Guide & Scope)

**用户操作**（启动→确认计划→等待生成→验收结果→常见操作速查→FAQ）见 [REFERENCE.md §7](REFERENCE.md)。**能力边界**：支持输入 md/txt/yaml/json/PDF，不支持图片原始数据/数据库/流式；边界情况说明见 [REFERENCE.md §9](REFERENCE.md)。

## 10. 异常处理 (Error Handling)

所有错误信息必须遵循三段式格式：`[类型]: 发生了什么 → 原因: 为什么发生 → 操作: 如何修复`。

| 错误类型 | 症状 | 处理方式 | 仍失败兜底 |
|:---|:---|:---|:---|
| 源文件不可读 | 切片计划为空、文件不存在或无权限 | `python -c "from pathlib import Path; print(Path('<路径>').exists())"` 验证路径可达性；网络驱动器走 `python_executor` | 终止当前任务，等待用户提供正确路径 |
| 切片数异常 | 实际生成数与计划不符、全部切片为空 | `python scripts/slice_generator.py "<源文件>" <output_dir> --json` 获取修正计划 | 对比 `<analysis>` 标题统计与脚本输出数量，排查遗漏 |
| 校验致命失败 | `validate_slice.py` 返回 FAIL，YAML 缺字段/内容截断 | `python scripts/validate_slice.py "<切片路径>" --fix --json` 输出完整日志 | 搜索 `SELF_CHECK` 注释中 `fatal_failed: true` 定位失败字段后重生成 |
| 索引不连续 | `batch_audit.py` 报告 index 跳跃 | `python scripts/batch_audit.py "<切片目录>"` 列出缺失索引 | 断点续传：`python scripts/slice_generator.py "<源文件>" <output_dir> --resume` |
| 死链 | `cross_refs` 引用的切片文件不存在 | `python scripts/batch_audit.py "<切片目录>" --fix` 自动检测死链并修复 | 手动打开死链来源切片，更新 `cross_refs` 为实际存在的切片 ID |
| 依赖缺失 | `ModuleNotFoundError: sentence-transformers` | `pip install sentence-transformers numpy pyyaml` 后重新运行评估 | 系统自动降级 PurePythonEmbedder（TF-IDF），零外部依赖 |
| 检索死片 | `evaluate_retrieval.py` 报告 R@1=0 | `python scripts/evaluate_retrieval.py "<切片目录>"` 输出死片清单 | 逐一打开死片文件，重写 `embedding_hint` 加入正文精确关键词 |
| Token 溢出 | 生成中断、上下文超限 | 使用 §5 分批确认机制，手动控制每批 ≤2 片 | `python scripts/slice_generator.py "<源文件>" <output_dir> --json` 查看完整计划后分阶段执行 |
| 编码错误 | 切片中文变乱码 | `python -c "import chardet; print(chardet.detect(open('<文件>','rb').read()))"` 检测实际编码 | 若非 UTF-8，重新以正确编码读取后另存为 UTF-8 |

> 完整异常处理（含静默失败防护清单、错误信息格式示例）见 [REFERENCE.md §12](REFERENCE.md)。

---

## 11. 反模式与 FAQ (Anti-Patterns & FAQ)

| # | 禁止行为 | 正确做法 |
|:--|:---|:---|
| 1 | 跳过 `<analysis>` 直接生成切片 — 无计划切片质量不可控 | 必须完成 §0 CoT 的 10 步分析并通过 CHECKPOINT 确认 |
| 2 | 用脚本模板生成元数据 — 语义空洞导致检索命中率低 | Agent 逐片手工填充 `description/keyword/embedding_hint` |
| 3 | 调用外部 API（如 OpenAI Embedding）— 泄露敏感文档内容 | 仅用 skill 内置脚本（SBERT 本地 → PurePythonEmbedder 降级） |
| 4 | 大表格截断保留 — 丢失关键数据列 | 被截断表格标注 `[TRUNCATED]` 并记录截断位置 |
| 5 | 泛化词做 keyword — 检索消歧失效 | keyword 必须包含命名空间前缀、参数特征或版本标记 |
| 6 | 未完成 analysis 就写文件 — 切片计划未定就产出垃圾 | analysis 阶段仅写 JSON stub，确认后逐片写入 |
| 7 | 单切片塞全部内容 — 上下文超限且检索精度归零 | 严格遵守 §2 拆分阈值（700 字软上限 / 500 字硬上限） |
| 8 | 忘记校验 — 低质量切片流入下游 | 每片写入后立即 `validate_slice.py --fix`，每批结束后 `batch_audit.py` |
| 9 | shell_executor 操作网络驱动器 — WinError 2 | 网络驱动器走 python_executor（pathlib.Path） |
| 10 | 假设阅读顺序 — 切片被跨顺序检索时上下文断裂 | 每片自包含：内含术语定义 + 前置依赖声明 + 版本号 |
| 11 | 泛化提问导致检索混淆 — 同名概念选择错误 | 切片正文显式标注命名空间和适用范围 |
| 12 | 相同 embedding_hint — 检索同质化导致死片 | embedding_hint 必须唯一化：加入路径/章节/索引号区分 |
| 13 | 中断后从头再来 — 重复片段造成索引混乱 | 使用 `slice_generator.py --resume` 从断点续传 |

> 完整反模式清单（含症状诊断、危害说明与案例分析）及 FAQ 见 [REFERENCE.md §8](REFERENCE.md)。

## 12. 平台兼容性与更新记录 (Platform & Changelog)

Windows / Linux / macOS 三平台完全支持。关键约束：网络驱动器用 python_executor；evaluate_retrieval.py 三层嵌入降级路由（SBERT → 自动安装 → PurePythonEmbedder）；所有脚本使用 pathlib.Path。详见 [REFERENCE.md §10](REFERENCE.md)。更新记录见 [REFERENCE.md §11](REFERENCE.md)。
