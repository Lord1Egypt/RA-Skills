---
name: medical-scale-research
description: 医学量表信息检索与标准化报告生成。通过浏览器自动化检索量表背景、版权、CDISC 映射、统计方法等信息，生成飞书云文档并保存到量表知识库。
---

# 医学量表 Skill - medical-scale-research

## PURPOSE

通过浏览器自动化检索医学量表的完整信息（背景、版权、CDISC 映射、统计方法等），生成标准化的飞书云文档，并保存到量表知识库。支持版本追踪和增量更新。

## WHEN TO USE

### TRIGGERS
- "检索 [量表名] 量表的信息"
- "整理 [量表名] 量表的报告"
- "查询 [量表名] 的 CDISC domain"
- "更新 [量表名] 量表的版本信息"
- "[量表名] 量表的统计分析方法是什么"

### DO NOT USE WHEN
- 需要访问付费墙后的完整文献（只能获取摘要）
- 量表信息完全不存在于公开网络
- 用户需要即时版权授权（需联系版权方）

## INPUTS

### REQUIRED
- 量表名称（中文或英文，如 "SGRQ" / "圣乔治呼吸问卷"）

### OPTIONAL
- 指定版本（如 "最新版本" 或 "v2.0"）
- 指定检索重点（如 "重点检索 CDISC 映射"）
- 更新模式（如 "增量更新已有文档"）

### EXAMPLES
- "检索 SGRQ 量表的信息"
- "整理 EORTC QLQ-C30 量表的完整报告"
- "查询 PHQ-9 量表的 CDISC domain 和统计方法"
- "更新 EASI 量表的版本历史"

## OUTPUTS

### 默认输出
- 飞书云文档链接（标准化报告）
- 知识库归档确认

### 文档结构
```markdown
# [量表名称] 标准化研究报告

## 一、量表简介
### 1.1 背景及发展历程
### 1.2 应用领域
### 1.3 量表内容
### 1.4 版本历史（最新 + 更新摘要）
### 1.5 官方量表全文 ⚠️（必须有 PDF 链接或截图）

## 二、版权与授权信息
### 2.1 版权方信息
### 2.2 中文版信息

## 三、CDISC 编程
### 3.1 标准 aCRF 与受控术语（自动推荐 Domain）
### 3.2 SDTM 实现
### 3.3 ADaM 实现

## 四、统计分析
### 4.1 数据类型与分布特征
### 4.2 缺失值处理（条目级 + 访视级）
### 4.3 常规分析模型（含 SAS/R 程序）
### 4.4 探索性分析
### 4.5 结果呈现（Table/Figure 模板）

## 五、参考文献
```

### 1.5 官方量表全文章节模板
```markdown
### 1.5 官方量表全文

**获取状态**：✅ 已下载 PDF / ✅ 已截图

**PDF 下载**：
- 下载链接：[量表名称 Official PDF](URL)
- 本地路径：`/Users/wangyafei/Downloads/scales/[量表名]_official.pdf`
- 文件大小：XX KB

**量表条目预览**：
（如为截图，此处插入图片）

| 部分 | 条目示例 | 评分方式 |
|------|---------|---------|
| ... | ... | ... |

> **注意**：完整量表请下载上方 PDF 文件。量表版权归 [版权方] 所有，仅限学术研究使用。
```

## WORKFLOW

### 1. 解析量表名称
- 提取关键词（中英文全称、缩写）
- 识别同义词（如 "SGRQ" = "圣乔治呼吸问卷" = "St George's Respiratory Questionnaire"）

### 2. 并行检索 7 个维度 + 量表全文获取
使用 `browser` 工具打开多个 Tab 并行检索：

| 维度 | 数据源 | 检索策略 |
|------|--------|---------|
| 背景信息 | PubMed, Google Scholar, 量表官网 | `"[量表名] development validation history"` |
| **官方量表全文** | 官网 PDF 下载链接 | `"[量表名] official instrument PDF download"` |
| 版本历史 | 官网，GitHub, 修订记录 | `"[量表名] version history revision changelog"` |
| 版权信息 | Mapi Research Trust, 版权方官网 | `"[量表名] copyright license permission"` |
| 中文版信息 | CNKI, 万方，中文论文 | `"[量表名] 中文版 信效度 验证"` |
| CDISC 映射 | CDISC 官网，TAUGs, SDTMIG | `"[量表名/概念] CDISC SDTM ADaM domain"` |
| 统计方法 | 高引文献，系统评价 | `"[量表名] scoring algorithm missing data analysis"` |

### 2.1 ⚠️ 量表全文获取（强制要求）

**必须完成以下任一操作，否则停止执行并告知用户**：

#### 选项 A：下载官方 PDF（优先）
```
1. 在官网/权威来源查找 PDF 下载链接
2. 使用 exec 下载：curl -L -o "/Users/wangyafei/Downloads/scales/[量表名]_official.pdf" "[PDF_URL]"
3. 验证文件：ls -lh 确认文件存在且>1KB
4. 在文档 1.4 章节后插入"官方量表全文"章节，包含：
   - PDF 下载链接（可点击）
   - 本地保存路径
   - 文件大小
   - 版权说明
```

#### 选项 B：屏幕截图（无法下载时）
```
1. 打开量表官方页面（browser.open）
2. 使用 browser.snapshot 捕获页面（aria refs）
3. 如页面较长 → 滚动分多次截图（至少覆盖完整量表条目）
4. 使用 feishu_doc.upload_image 上传图片到飞书云盘
5. 在文档 1.4 章节后插入"官方量表全文"章节，包含：
   - 量表条目截图（至少 1 张）
   - 来源网址链接
   - 版权说明
```

#### ❌ 无法获取时的处理
```
如无法找到 PDF 且无法截图：
1. 停止执行
2. 告知用户："未找到 [量表名] 的官方量表全文（PDF 或截图）"
3. 提供版权方联系方式
4. 询问用户是否继续生成报告（不含量表全文）
```

### 2.2 量表全文检索策略

**检索关键词**（按顺序尝试）：
```
1. "[量表名] official PDF download"
2. "[量表名] full instrument PDF"
3. "[量表名] questionnaire PDF"
4. "[量表名] 官网" → 查找下载链接
5. "[量表名] Mapi Research Trust" → 版权方官网
```

**权威来源优先级**：
```
1. 量表官方网站（.edu/.org 域名）
2. 版权方官网（如 Mapi Research Trust）
3. 原作者机构网站
4. 指南/共识文件（如 EPOS2020）
5. 学术论文补充材料（Supplementary Materials）
```

### 3. 信息提取与结构化
- 使用 `web_fetch` 提取页面内容
- 过滤噪声，提取关键字段
- 验证信息一致性（多源交叉验证）

### 4. CDISC 自动推荐
基于规则引擎推荐 Domain：

```json
{
  "生活质量/HRQoL": {"sdtm": "QS", "adam": "ADQS"},
  "症状评估": {"sdtm": "QS", "adam": "ADQS"},
  "病史": {"sdtm": "MH", "adam": "ADMH"},
  "合并用药": {"sdtm": "CM", "adam": "ADCM"},
  "不良事件": {"sdtm": "AE", "adam": "ADAE"},
  "生命体征": {"sdtm": "VS", "adam": "ADVS"},
  "实验室检查": {"sdtm": "LB", "adam": "ADLB"}
}
```

### 5. 生成飞书文档（重要！）

**⚠️ 内容长度限制**：飞书 API 对单次写入内容长度有限制（约 5KB）

**推荐方法**：
```
IF 内容 > 5KB:
  1. 先 create 创建空文档
  2. 将内容按章节分割（每段<4KB）
  3. 使用 insert 操作逐段插入（after_block_id）
  4. 每插入一段后获取新的 block_id
ELSE:
  直接使用 write 操作一次性写入
```

**操作步骤**：
1. **创建文档**：`feishu_doc create` → 获取 doc_token
2. **写入第一章**：`feishu_doc write` → 写入完整第一章
3. **获取最后 block_id**：`feishu_doc list_blocks` → 获取最后一个 block_id
4. **插入后续章节**：`feishu_doc insert` + after_block_id → 逐章插入
5. **验证内容**：`feishu_doc read` → 确认内容完整

**内容分割策略**：
```
章节 1：一、量表简介（约 3KB）
章节 2：二、版权与授权信息（约 2KB）
章节 3：三、CDISC 编程（约 3KB）
章节 4：四、统计分析（约 4KB）
章节 5：五、参考文献 + 附录（约 2KB）
```

### 6. 保存到知识库
- 使用 `feishu_wiki` 创建/更新节点
- 按疾病领域/量表类型分类
- 记录版本历史

### 7. 增量更新（可选）
- 对比新旧版本
- 高亮变更内容
- 更新版本历史

## SAFETY & EDGE CASES

- **版权信息**：明确标注信息来源，不提供法律建议
- **版本准确性**：优先使用最新版本，标注检索日期
- **CDISC 推荐**：标注为"推荐"，需人工确认
- **付费内容**：只能获取摘要，标注"需订阅"
- **多版本并存**：明确标注各版本差异
- **信息冲突**：多源交叉验证，标注不确定性
- **⚠️ 飞书文档长度限制**：
  - 单次写入内容 < 5KB
  - 长文档需分章节插入
  - 使用 insert + after_block_id 逐段写入
- **⚠️ 量表全文获取（强制）**：
  - 必须下载 PDF 或截图，否则停止执行
  - PDF 文件需验证存在且>1KB
  - 截图需覆盖完整量表条目

## STOP AND ASK THE USER IF

- 量表名称模糊/有多个同名量表
- 版权信息无法确认（需用户核实）
- CDISC 推荐置信度低（需人工判断）
- 检索结果为空（需调整策略）
- 知识库权限不足（需用户授权）
- **⚠️ 无法获取量表全文（PDF/截图）**：
  - 停止执行并告知用户
  - 提供已尝试的检索来源
  - 提供版权方联系方式
  - 询问是否继续生成报告（不含量表全文）

## EXAMPLES

### Example 1: 首次检索
**Input**: "检索 SGRQ 量表的信息"

**Process**:
1. 解析 → SGRQ = St George's Respiratory Questionnaire = 圣乔治呼吸问卷
2. 并行检索 7 个维度
3. 提取结构化数据
4. CDISC 推荐 → QS (生活质量)
5. 生成飞书文档
6. 保存到知识库

**Output**:
```
✅ 已完成 SGRQ 量表信息检索

📄 文档链接：https://xxx.feishu.cn/docx/xxxxx
📚 已归档至：医学量表库 > 呼吸系统 > SGRQ

检索维度：
✓ 背景信息（5 篇文献）
✓ 官方量表（✅ 已下载 PDF - 7.0KB）
✓ 版本历史（v2.1 最新版，2023 更新）
✓ 版权信息（Mapi Research Trust）
✓ 中文版（3 篇验证文献）
✓ CDISC 映射（QS/ADQS 推荐）
✓ 统计方法（4 种模型）

📎 量表全文：
- PDF 路径：/Users/wangyafei/Downloads/scales/SGRQ_official.pdf
- 下载链接：[SGRQ Official PDF](https://xxx.xxx.ac.uk/xxx.pdf)
```

### Example 2: 增量更新
**Input**: "更新 EASI 量表的版本信息"

**Process**:
1. 读取已有文档
2. 检索最新版本信息
3. 对比变更内容
4. 更新版本历史章节
5. 标注变更日期

**Output**:
```
✅ 已更新 EASI 量表版本信息

📝 新增内容：
- v2024 版本（2024-01 发布）
- 儿童权重系数调整
- 新增深色皮肤红斑评估指南

📄 更新链接：https://xxx.feishu.cn/docx/xxxxx
```

## FILES

- `templates/scale-report.md` - 文档模板
- `rules/cdisc-mapping.json` - CDISC 推荐规则
- `examples/SGRQ-example.md` - 示例输出

## RELATED SKILLS

- `lark-doc` - 飞书文档操作
- `lark-wiki` - 飞书知识库管理
- `agent-browser` - 浏览器自动化
