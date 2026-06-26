---
name: paper-summarize-pdf-to-feishu
version: 2.0.0
author: yy-fan
license: MIT
homepage: https://github.com/openclaw/openclaw
description: |
  总结论文 PDF 为飞书文档（含图表）。采用主控 - 子代理 (Orchestrator-Subagents) 架构处理长流程。
  支持学术论文、技术报告的自动去重、总结、配图、真实比对审核与人工确认。
  触发场景：发送 PDF 附件、"总结这个 PDF"、"把 PDF 写成飞书文档"、"论文总结"。
metadata:
  clawdbot:
    emoji: "📄"
    requires:
      bins:
        - pdftotext
        - pdfinfo
        - pdfimages
        - pdftoppm
        - tesseract
        - jq
    install:
      - id: apt-poppler
        kind: apt
        package: poppler-utils
        bins: ["pdftotext", "pdfinfo", "pdfimages", "pdftoppm"]
        label: "Install poppler-utils (PDF tools)"
      - id: apt-tesseract
        kind: apt
        package: tesseract-ocr
        bins: ["tesseract"]
        label: "Install tesseract-ocr (OCR)"
      - id: apt-jq
        kind: apt
        package: jq
        bins: ["jq"]
        label: "Install jq (JSON processor)"
---

# paper-summarize-pdf-to-feishu

**本技能采用多 Agent 协作模式**。作为主控 Agent，你的核心职责是：

- ✅ 调度流程
- ✅ 执行系统脚本
- ✅ 向子 Agent 分配具体任务并传递上下文
- ✅ 与用户沟通确认

**❌ 请不要试图自己在单次对话中完成所有长文本阅读和细节比对。**

---

## 🚨 执行前必读（30 秒）

**收到 PDF 后，第一步必须做**：
1. ✅ 完整阅读本 SKILL.md（不要跳过！）
2. ✅ 检查前置依赖（`which pdftotext pdfinfo ...`）
3. ✅ 创建日志目录（阶段零）

**❌ 禁止直接开始处理！**

---

## 📌 核心原则（违反=任务失败）

| 原则 | 说明 |
|------|------|
| **不要自己读长文本** | 必须派生 Reader 子 Agent |
| **不要自己上传图片** | 必须派生 Vision 子 Agent |
| **不要自我审核** | 必须派生 Reviewer + 真实数据注入 |
| **必须等用户确认** | 阶段四必须挂起 |
| **必须用占位符** | Reader 必须插入 `【FIGURE_X】` |

---

## 前置依赖检查 (主控 Agent 执行)

确保以下工具可用：`pdftotext`, `pdfinfo`, `pdfimages`, `pdftoppm`, `tesseract`, `jq`。

如果缺失，通过以下命令安装：

```bash
# PDF 处理工具
sudo apt-get install -y poppler-utils

# OCR 工具
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim

# JSON 处理工具（脚本中大量使用）
sudo apt-get install -y jq
```

**快速检查**：
```bash
which pdftotext pdfinfo pdfimages pdftoppm tesseract jq
# 所有命令都应该返回路径
```


## 日志管理规范（重要！）

### 日志目录结构

在**阶段零开始时**，主控 Agent 必须创建以下目录结构：

```bash
mkdir -p "$PAPER_DIR/logs/scripts"
mkdir -p "$PAPER_DIR/progress"
mkdir -p "$PAPER_DIR/errors"
```

**目录说明**：
| 目录 | 用途 | 内容 |
|------|------|------|
| `$PAPER_DIR/logs/` | 统一日志目录 | 所有 Agent 和脚本的日志 |
| `$PAPER_DIR/logs/scripts/` | 脚本日志 | `extract_metadata.log`, `locate_figures.log` 等 |
| `$PAPER_DIR/progress/` | 进度报告 | Markdown 格式的子 Agent 完成报告 |
| `$PAPER_DIR/errors/` | 错误报告 | 错误日志和堆栈跟踪 |

**优点**：
- ✅ 每篇论文独立，不会覆盖
- ✅ 多人使用不会冲突
- ✅ 清理论文时一起清理
- ✅ 符合"工作目录"的概念

---
---

## 完整工作流程（六阶段）

### 阶段零：去重检查 (主控 Agent 调度)

**日志目录创建**：
```bash
mkdir -p "$PAPER_DIR/logs/scripts"
mkdir -p "$PAPER_DIR/progress"
mkdir -p "$PAPER_DIR/errors"
log_master "✅ 日志目录已创建"
```


**目标**：检查论文是否已处理，避免重复工作。

1. **提取元数据**：
   ```bash
   scripts/extract_metadata.sh <input.pdf> "$PAPER_DIR/metadata.json" "$PAPER_DIR"
   ```

2. **检查去重**：
   ```bash
   scripts/check_duplicate.sh "$PAPER_DIR/metadata.json" "$PAPERS_DIR"
   result=$?  # 保存退出码
   
   # 检查脚本输出中的 RESULT 变量
   if echo "$output" | grep -q "RESULT=duplicate"; then
       echo "❌ 完全重复：该论文已处理过"
       echo "📋 飞书文档：$(cat $PAPER_DIR/feishu_doc_token.txt)"
       exit 1  # 停止任务
   elif echo "$output" | grep -q "RESULT=possible_duplicate"; then
       echo "⚠️  可能重复：已存在飞书文档，但 PDF 文件未找到"
       echo "📋 请用户确认是否继续"
       # 等待用户确认
   fi
   
   # 检查退出码
   if [[ $result -eq 1 ]]; then
       echo "❌ 去重检查失败，停止任务"
       exit 1
   fi
   ```

3. **根据返回结果判断**：
   - **退出码 0 + RESULT=new**：新论文，创建 `$PAPER_DIR`，复制 PDF，进入阶段一
   - **退出码 1 + RESULT=duplicate**：❌ **完全重复，立即停止任务**，告知用户已处理过
   - **退出码 0 + RESULT=possible_duplicate**：⚠️ 可能重复，等待用户确认
   - **退出码 2 + RESULT=supplement**：补充材料，执行合并流程

**⚠️ 重要**：主控 Agent 必须检查脚本的退出码和 RESULT 变量，如果检测到重复（`RESULT=duplicate` 或退出码 1），必须**立即停止任务**，不得继续执行后续阶段！

---

### 阶段一：提取与初稿生成 (Sub-agent: Reader)

**日志要求**：
- 所有日志输出到 $PAPER_DIR/progress/reader.log
- 使用标准格式：[YYYY-MM-DD HH:MM:SS] [级别] 消息
- 关键步骤必须记录（开始、完成、错误）
- 完成后生成进度报告到 $PAPER_DIR/progress/reader_report.md

**目标**：提取 PDF 文本并生成结构化总结初稿。

1. **提取文本**（主控 Agent 执行）：
   ```bash
   scripts/extract_pdf_text.sh "$PAPER_DIR/paper.pdf" "$PAPER_DIR/paper.txt" "$PAPER_DIR"
   ```

2. **派生阅读子 Agent**（主控 Agent 调用 `sessions_spawn`）：

   ```bash
   sessions_spawn task="你是一个专业的学术阅读助手 (Reader)。
   
   **任务**：
   1. 分段读取 $PAPER_DIR/paper.txt 的完整内容（不要跳过任何部分）。
   2. 严格按照 summary_template.md 的结构要求，提取以下内容：
      - 研究背景与动机
      - 研究设计
      - 方法/系统架构
      - 核心结果（包含所有关键数据：百分比、p 值、置信区间、样本量）
      - 讨论与局限性
      - 结论
   3. 必须将最终生成的 Markdown 文本保存到 $PAPER_DIR/summary.md 中。
   
   **数据精度要求**：
   - 百分比：28.7%（不要四舍五入）
   - P 值：P < 0.001 或 P = 0.005
   - 样本量：n=691 或 2,069 人
   
   **图片占位符要求**（重要！）：
   - 在**相关章节内容后**插入占位符标记：`【FIGURE_X】`
   - 占位符单独一行，不要与正文混排
   - **必须用中文方括号** `【】`，因为飞书会过滤 HTML 注释 `<!-- -->`
   - **添加预期描述**（帮助 Vision Agent 匹配图片）：
     ```markdown
     ## 研究设计
     
     本研究采用随机对照试验设计...
     
     【FIGURE_1】
     <!-- 预期：流程图/试验设计，展示参与者分组和随访流程 -->
     
     ## 核心结果
     
     LLM 单独表现优异...
     
     【FIGURE_2】
     <!-- 预期：柱状图/数据对比，展示主要结局指标 -->
     ```
   - **占位符放置原则** ⭐：
     - Figure 应该放在**与其内容相关的章节后**，而不是按编号顺序
     - 例如：研究设计流程图 → 放在"研究设计"章节后，而不是"研究背景"后
     - 从 paper.txt 中提取 Figure 标题，根据内容判断应该放在哪个章节
   - **占位符数量** ⭐：
     - 占位符数量 ≠ PDF 中 Figure 总数
     - **只插入重要的、原文有描述的 Figure**（通常 3-5 个）
     - 判断标准：正文中明确提到"如图 X 所示"或有大段图片描述的
   
   **进度日志**（必须写入）：
   1. 开始任务时，立即写入 $PAPER_DIR/progress/reader.log：
      ```
      [YYYY-MM-DD HH:MM:SS] Reader 子 Agent 启动
      [YYYY-MM-DD HH:MM:SS] 开始读取 paper.txt (共 XXX 行)
      ```
   2. 每完成一个章节，追加进度：
      ```
      [YYYY-MM-DD HH:MM:SS] ✅ 完成：研究背景与动机
      [YYYY-MM-DD HH:MM:SS] ✅ 完成：研究设计
      ...
      ```
   3. 完成后写入最终报告：
      ```
      [YYYY-MM-DD HH:MM:SS] ✅ Reader 任务完成
      [YYYY-MM-DD HH:MM:SS] 输出文件：$PAPER_DIR/summary.md (XXX KB)
      [YYYY-MM-DD HH:MM:SS] 总耗时：X 分钟
      ```
   
   **完成后汇报**（向我报告）：
   ```markdown
   ## Reader 子 Agent 完成报告
   
   **开始时间**: YYYY-MM-DD HH:MM  
   **完成时间**: YYYY-MM-DD HH:MM  
   **耗时**: X 分钟  
   
   ### 执行结果
   - ✅ 成功生成 summary.md
   
   ### 输出文件
   - `$PAPER_DIR/summary.md` (XXX KB, XXX 行)
   - `$PAPER_DIR/progress/reader.log` (进度日志)
   
   ### 论文关键信息
   - **研究类型**: <如 RCT、队列研究等>
   - **样本量**: <如 2,069 人>
   - **主要结局**: <如 问诊时长减少 28.7%>
   
   ### 问题与备注
   <如有问题，在此说明；如无问题，填写"无">
   ```
   
   确认后向我（主控 Agent）报告。"
   ```

3. **等待子 Agent 完成**并确认 `$PAPER_DIR/summary.md` 已生成。

---

### 阶段二：文档创建与限流配图 (Sub-agent: Vision)

**目标**：创建飞书文档并插入图表。

1. **创建飞书文档**（主控 Agent 执行）：
   ```bash
   feishu_doc action=create title="总结：<论文标题>"
   ```
   获取 `doc_token` 并保存到 `$PAPER_DIR/feishu_doc_token.txt`。

2. **写入初稿**（主控 Agent 执行）：
   ```bash
   # ⚠️ 注意：必须使用 Reader 生成的完整 summary.md，不要手动修改或精简
   feishu_doc action=write doc_token="<token>" content="$(cat $PAPER_DIR/summary.md)"
   ```

3. **定位图表**（主控 Agent 执行）：
   ```bash
   scripts/locate_figures.sh "$PAPER_DIR/paper.pdf" "$PAPER_DIR/paper.txt" "$PAPER_DIR/images"
   ```
   
   **输出说明**：脚本使用 `pdfimages` 提取 PDF 中所有嵌入图片，生成 `fig_01.png`, `fig_02.png` 等文件。
   **注意**：提取的图片可能包含图标、线条等小文件（<10KB），Vision 子 Agent 需要筛选真正的 Figure（通常 >100KB）。

4. **自动识别支持图片的模型**（主控 Agent 执行）：
   ```bash
   # 从配置中自动查找支持图片输入的模型
   VISION_MODEL=$(jq -r '
     .models.providers | to_entries[] | 
     .value.models[] | 
     select(.input and (.input | index("image"))) | 
     .id | 
     first
   ' "~/.openclaw/openclaw.json" 2>/dev/null)
   
   # 如果找不到支持图片的模型，使用主模型
   if [[ -z "$VISION_MODEL" || "$VISION_MODEL" == "null" || "$VISION_MODEL" == "" ]]; then
       VISION_MODEL=$(jq -r '.agents.defaults.model.primary' "~/.openclaw/openclaw.json")
       echo "⚠️  未找到支持图片的模型，使用主模型：$VISION_MODEL"
   else
       echo "👁️ Vision 模型（自动识别）：$VISION_MODEL"
   fi
   ```

5. **派生配图子 Agent**（主控 Agent 调用 `sessions_spawn`）：

   ```bash
   sessions_spawn task="你是一个视觉处理专家 (Vision)。
   
   **任务**：
   1. 逐个读取 $PAPER_DIR/images 下的图片，确认图中包含正确的 Figure/Table 标题及内容。
   2. 使用 feishu_doc action=upload_image 上传图片到飞书文档 (token: $DOC_TOKEN)。
   3. **精确定位插入**：使用 parent_block_id + index 参数将图片插入到对应章节。
   
   🚨 **飞书操作关键规则**（必须遵守，否则失败）：
   
   **1. 防限流**：
   - 每次 `upload_image` 后必须 `sleep 3` 秒
   - 严重限流时等待 10 秒后重试
   
   **2. 智能匹配占位符（修正版流程）** ⭐：
   - **步骤 1**：`list_blocks` 获取所有 blocks，**从 root block 的 children 数组中查找占位符的位置**
   
     **关键**：占位符的 `index` 是它在 root block 的 `children` 数组中的位置（0-based）
     ```
     1. 获取 root block（第一个 block）
     2. 读取 root_block.children 数组
     3. 遍历 children 数组，找到占位符 block_id 的位置
     4. 该位置就是 index（0-based）
     ```
     
     **记录**：每个占位符的 `block_id` 和 `index`（在 children 数组中的位置）
   
   - **步骤 2**：对每张图片执行（必须按顺序执行，严格遵守）：
     
     **2a. OCR 提取文字**：
     ```bash
     tesseract image.png stdout --psm 6
     ```
     提取 Figure 编号和标题。
     
     **2b. 视觉模型理解**（重要！OCR 失败时必须执行）：
     ```
     使用 `read` 工具读取图片文件（路径：$PAPER_DIR/images/xxx.png）
     
     读取时附带问题（让模型分析图片）：
     "请分析这张图片：
     - 这是什么类型的图表？（流程图/柱状图/森林图/表格/其他）
     - 图中有什么关键词或标题？
     - 能否识别 Figure 编号或 Table 编号？
     
     请用简洁的格式回复，例如：
     类型：柱状图
     关键词：条件识别率，GPT-4o, Llama 3, 94.7%
     Figure 编号：Figure 2"
     ```
     
     **说明**：
     - 你的 `model` 参数已设置为支持图片的模型（如 qwen3.5-plus）
     - 使用 `read` 工具读取图片后，模型会自动"看到"并分析
     - 从模型回复中提取：图表类型、关键词、Figure 编号
     
     **2c. 匹配占位符**：
     - 根据 OCR 结果 + 视觉模型提取的关键词 + 占位符预期描述，匹配最合适的占位符
     - 记录占位符的 `block_id` 和 `index`
   
   - **步骤 3**：**先删除占位符，再上传图片** ⭐
     ```
     a. delete_block(block_id: 占位符的 block_id)
     b. 记录原 index = N
     c. sleep 1 秒（让飞书处理删除）
     d. upload_image(..., parent_block_id: 文档根 ID, index: N)
     e. 【关键验证】检查 file_token：
        - 如果 file_token 为空字符串 → 上传失败，等待 10 秒后重试
        - 如果 file_token 不为空 → 上传成功
     f. sleep 3 秒（防限流，必须执行！）
     g. 记录：图片上传成功，block_id = xxx
     ```
   
   - **匹配原则**：
     - Figure 编号优先（OCR 或视觉模型识别的"Figure 1"→匹配 `【FIGURE_1】`）
     - 关键词辅助（视觉模型提取的关键词与占位符预期描述重叠）
     - 如果 OCR 失败，必须使用视觉模型理解，不得直接退化
   
   - **步骤 4**：最终验证
     ```
     list_blocks 检查 Image block (block_type 27) 数量
     应该等于上传的图片数量
     ```
   
   **3. 精确定位参数**：
   - `parent_block_id`: 文档根 ID（和 `doc_token` 相同）
   - `index`: 占位符 block 的 index（在占位符位置插入）
   - 不填 `parent_block_id` 则追加到末尾
   
   **4. 上传后验证**：
   - 检查 `file_token` 不为空字符串
   - 执行 `read` 查看文档，确认图片数量正确
   - 打开飞书文档确认图片显示（不转圈）
   
   **5. 失败处理（重置法）**：
   - **触发条件**：
     - `delete_block` 返回 404（block 不存在）
     - 连续 2 次 `upload_image` 返回空 `file_token`
     - 文档结构混乱（block IDs 失效）
   - **操作步骤**：
     1. 向主控 Agent 报告需要重置
     2. 主控 Agent 执行：`feishu_doc action=write doc_token="$DOC_TOKEN" content="$(cat $PAPER_DIR/summary.md)"`（使用完整文件，不要精简）
     3. 重新从步骤 1 开始（`list_blocks` → 找占位符 → 上传图片）
   - **注意**：重置后所有占位符会恢复，需要重新上传所有图片
   
   **操作流程**：
   1. 用 `write` 写入 summary.md（含占位符 `【FIGURE_X】` 和预期描述）
   2. `list_blocks` 获取所有 blocks，读取占位符预期描述
   3. 对每张图片执行智能匹配（详细步骤）：
      ```
      a. OCR 提取：tesseract image.png stdout --psm 6
      
      b. 视觉模型理解（OCR 失败时必需）：
         调用 read 工具读取图片，附带问题：
         "请分析这张图片的类型、关键词、Figure 编号"
         
         示例模型回复：
         "类型：柱状图
          关键词：条件识别率，GPT-4o, 94.7%
          Figure 编号：Figure 2"
      
      c. 匹配占位符：
         - 如果 OCR 识别到"Figure 2"→匹配 `【FIGURE_2】`
         - 如果 OCR 失败，用关键词匹配：
           "柱状图" + "条件识别率" → 匹配预期描述为"柱状图，展示条件识别率"的占位符
      
      d. 获取占位符的 index（从 list_blocks 结果中）
      ```
   4. 在匹配到的占位符 `index` 位置 `upload_image`
   5. `delete_block` 删除占位符
   6. 重复步骤 3-5 直到所有图片上传完成
   
   **图片验证**：
   - 如果 pdfimages 提取的图片数量 < 文档中 Figure 数量，使用截图备选方案
   - 验证每张截图是否包含'Figure X'或'Table X'标题文字
   - 纯文字页面不要使用，检查相邻页面（±3 页范围）
   
   **进度日志**（必须写入）：
   1. 开始任务时，立即写入 $PAPER_DIR/progress/vision.log：
      ```
      [YYYY-MM-DD HH:MM:SS] Vision 子 Agent 启动
      [YYYY-MM-DD HH:MM:SS] 飞书文档 token: <token>
      [YYYY-MM-DD HH:MM:SS] 待上传图片：X 张
      ```
   2. 写入文本后：
      ```
      [YYYY-MM-DD HH:MM:SS] ✅ 写入 summary.md（含占位符和预期描述）
      [YYYY-MM-DD HH:MM:SS] ✅ list_blocks 获取 blocks 列表
      [YYYY-MM-DD HH:MM:SS] ✅ 找到占位符：【FIGURE_1】(index: X, 预期：流程图)
      ```
   3. 每上传一张图片，追加进度：
      ```
      [YYYY-MM-DD HH:MM:SS] 📸 处理图片：figure_1.png
      [YYYY-MM-DD HH:MM:SS] 🔍 OCR 结果：Figure 1, 流程图
      [YYYY-MM-DD HH:MM:SS] 👁️ 视觉模型分析：类型=流程图，关键词=研究设计，分组
      [YYYY-MM-DD HH:MM:SS] 🎯 匹配占位符：【FIGURE_1】(index: 4, 预期：流程图)
      [YYYY-MM-DD HH:MM:SS] ✅ Fig. 1 上传成功 (file_token: xxx, 527 KB, index: 4)
      [YYYY-MM-DD HH:MM:SS] ✅ 删除占位符【FIGURE_1】
      [YYYY-MM-DD HH:MM:SS] ⏳ 等待 3 秒（防限流）...
      [YYYY-MM-DD HH:MM:SS] 🔍 OCR 结果：失败（无文字）
      [YYYY-MM-DD HH:MM:SS] 👁️ 视觉模型分析：类型=柱状图，关键词=条件识别率，GPT-4o, 94.7%
      [YYYY-MM-DD HH:MM:SS] 🎯 匹配占位符：【FIGURE_2】(index: 13, 预期：柱状图，展示条件识别率)
      [YYYY-MM-DD HH:MM:SS] ✅ Fig. 2 上传成功 (file_token: xxx, 442 KB, index: 13)
      ...
      ```
   4. 完成后写入最终报告：
      ```
      [YYYY-MM-DD HH:MM:SS] ✅ Vision 任务完成
      [YYYY-MM-DD HH:MM:SS] 成功上传：X/ Y 张图片
      [YYYY-MM-DD HH:MM:SS] 智能匹配成功：X 张（命中率 XX%）
      [YYYY-MM-DD HH:MM:SS] 总耗时：X 分钟
      ```
   
   **完成后汇报**（向我报告）：
   ```markdown
   ## Vision 子 Agent 完成报告
   
   **开始时间**: YYYY-MM-DD HH:MM  
   **完成时间**: YYYY-MM-DD HH:MM  
   **耗时**: X 分钟  
   
   ### 执行结果
   - ✅ 成功创建飞书文档
   - ✅ 写入 summary.md（含占位符）
   - ✅ 上传 X 张图片（使用占位符定位）
   - ✅ 删除所有占位符
   
   ### 输出文件
   - 飞书文档链接：https://feishu.cn/docx/<doc_token>
   - `$PAPER_DIR/progress/vision.log` (进度日志)
   
   ### 图片上传详情
   | Figure | 大小 | 占位符 index | file_token | 匹配方式 | 状态 |
   |--------|------|-------------|------------|----------|------|
   | Fig. 1 | 527 KB | 4 | MsRLbdZbVo9... | OCR | ✅ |
   | Fig. 2 | 442 KB | 13 | NjuFbqaz8oT... | 视觉模型 | ✅ |
   
   ### 匹配统计
   - OCR 成功：X 张
   - 视觉模型辅助：Y 张
   - 匹配成功率：XX%
   
   ### 问题与备注
   <如有问题，在此说明；如无问题，填写"无">
   ```
   
   确认后向我（主控 Agent）报告。" model="$VISION_MODEL"
   ```

5. **等待子 Agent 完成**并确认图片已正确插入。

---

### 阶段三：真实数据比对审核 (Sub-agent: Reviewer)

**日志要求**：
- 所有日志输出到 $PAPER_DIR/progress/reviewer.log
- 使用标准格式：[YYYY-MM-DD HH:MM:SS] [级别] 消息
- 关键步骤必须记录（开始、完成、错误）
- 完成后生成进度报告到 $PAPER_DIR/progress/reviewer_report.md
- **审核报告保存到 $PAPER_DIR/progress/audit_report.md**

**目标**：通过注入真实数据防止审核幻觉。

**核心防幻觉机制**：必须将原始文本的切片直接喂给审核模型，不能让它空对空审核。

1. **读取 Fallback 模型**（主控 Agent 执行）：
   ```bash
   FALLBACK_MODEL=$(jq -r '.agents.defaults.model.fallbacks[0]' "~/.openclaw/openclaw.json")
   ```
   如果没有配置，则使用当前主模型。告知用户正在启动交叉审核。

2. **派生审核子 Agent（带真实数据注入）**（主控 Agent 调用 `sessions_spawn`）：

   ```bash
   sessions_spawn task="你是一个严苛的学术审核员 (Reviewer)。
   
   **【原始论文关键数据提取】**：
   $(cat $PAPER_DIR/paper.txt | grep -E '%|p<|p=|CI|n=' | head -n 30)
   
   **【生成的总结内容】**：
   $(cat $PAPER_DIR/summary.md)
   
   **请重点核查**：
   1. 飞书文档中的百分比、p 值、置信区间、样本量是否与原始数据存在偏差？
   2. 结论是否有无依据的夸大？
   3. 格式是否完全符合 summary_template.md 的精度要求？
   
   **进度日志**（必须写入）：
   1. 开始任务时，立即写入 $PAPER_DIR/progress/reviewer.log：
      ```
      [YYYY-MM-DD HH:MM:SS] Reviewer 子 Agent 启动
      [YYYY-MM-DD HH:MM:SS] 审核模型：<模型名称>
      [YYYY-MM-DD HH:MM:SS] 开始数据一致性核对
      ```
   2. 完成后写入最终报告：
      ```
      [YYYY-MM-DD HH:MM:SS] ✅ Reviewer 任务完成
      [YYYY-MM-DD HH:MM:SS] 审核结果：通过 / 需要修改
      [YYYY-MM-DD HH:MM:SS] 总耗时：X 分钟
      ```
   
   **输出要求**：
   请直接输出一份详尽的《审核报告及修改建议清单》，格式如下：
   
   ```markdown
   ## 审核报告
   
   ### 一致的内容
   - <列出哪些地方与原文一致>
   
   ### 需要修改的内容
   - <列出哪些地方需要修改，具体修改建议>
   
   ### 格式问题
   - <列出格式不符合要求的地方>
   
   ### 总体评价
   <通过/需要修改>
   ```
   
   **完成后汇报**（向我报告）：
   ```markdown
   ## Reviewer 子 Agent 完成报告
   
   **开始时间**: YYYY-MM-DD HH:MM  
   **完成时间**: YYYY-MM-DD HH:MM  
   **耗时**: X 分钟  
   **审核模型**: <模型名称>
   
   ### 执行结果
   - ✅ 审核通过 / ⚠️ 需要修改
   
   ### 审核统计
   - 一致的内容：X 处
   - 需要修改的内容：Y 处
   - 格式问题：Z 处
   
   ### 输出文件
   - `$PAPER_DIR/progress/reviewer.log` (进度日志)
   - `$PAPER_DIR/audit_report.md` (审核报告全文)
   
   ### 关键问题
   <如有严重问题（如数据错误、结论夸大），在此说明>
   
   ### 修改建议清单
   1. <具体修改建议 1>
   2. <具体修改建议 2>
   ...
   ```
   
   确认后向我（主控 Agent）报告。" model="$FALLBACK_MODEL"
   ```

3. **收集审核报告**，准备提交用户确认。

4. **应用审核修改**（主控 Agent 执行） ⭐：
   
   **步骤 4a**：读取审核报告
   ```bash
   # 读取审核报告
   AUDIT_REPORT="$PAPER_DIR/progress/audit_report.md"
   
   # 提取修改建议清单
   MODIFY_LIST=$(grep -A 20 "修改建议清单" "$AUDIT_REPORT")
   ```
   
   **步骤 4b**：逐项应用修改
   ```bash
   # 对每个修改建议：
   # 1. 使用 list_blocks 找到需要修改的 block_id
   # 2. 使用 update_block 修改文本块
   # 3. 使用 insert/append 添加缺失内容
   # 4. 记录修改日志
   ```
   
   **修改原则**：
   - 数据错误 → 使用 `update_block` 修改对应文本块
   - 缺失数据 → 使用 `insert` 在相应位置添加
   - 格式问题 → 使用 `update_block` 调整格式
   - 每次修改后验证 `success: true`
   
   **步骤 4c**：验证修改
   ```bash
   # 使用 read 查看飞书文档
   # 确认所有修改已应用
   # 记录验证结果到 progress/audit_apply.log
   ```

---

### 阶段四：人工确认 (主控 Agent 执行)

**目标**：让用户确认审核报告并决定是否修改。

1. **主控 Agent 收集 Reviewer 的《审核报告及修改建议清单》**。

2. **向用户发送以下内容**：

   ```
   📄 飞书初稿链接：<doc_link>
   
   ## 审核报告摘要
   
   <审核报告内容>
   
   ## 修改建议清单
   
   <具体修改建议>
   
   ---
   
   ⏳ 请确认是否采纳以上修改建议：
   
   | 回复 | 操作 |
   |------|------|
   | 【确认】 | 自动应用修改，输出最终版 |
   | 【修改 xxx】 | 进行微调（告诉我具体修改内容） |
   | 【跳过】 | 保留现状，输出最终版 |
   ```

3. **挂起等待用户回复**。

---

### 阶段五：定稿完善 (主控 Agent 执行)

**目标**：应用修改并输出最终版。

1. **应用修改**（根据用户确认） ⭐：
   
   **如果用户回复【确认】**：
   ```bash
   # 1. 读取审核报告中的修改建议清单
   AUDIT_REPORT="$PAPER_DIR/progress/audit_report.md"
   
   # 2. 对每个修改建议执行：
   #    a. 使用 list_blocks 找到目标 block_id
   #    b. 使用 update_block 修改内容
   #    c. 验证修改成功 (success: true)
   #    d. 记录修改日志
   
   # 3. 使用 read 验证所有修改已应用
   # 4. 记录验证结果到 progress/audit_apply.log
   ```
   
   **修改方法**：
   | 修改类型 | 使用工具 | 说明 |
   |----------|---------|------|
   | 修改文本 | `update_block` | 需要提供正确的 block_id |
   | 添加内容 | `insert` / `append` | insert 在指定位置，append 追加到末尾 |
   | 修改表格 | `write_table_cells` | 修改表格单元格内容 |
   | 添加表格行 | `insert_table_row` | 在表格中添加新行 |
   
   **验证流程**：
   ```bash
   # 1. 使用 read 查看飞书文档
   # 2. 确认所有修改已应用
   # 3. 如果有遗漏，重新执行修改
   # 4. 记录最终验证结果
   ```
   
   **如果用户回复【修改 xxx】**：根据用户具体要求修改。
   
   **如果用户回复【跳过】**：保持现状，记录"用户选择跳过修改"。

2. **强制署名**（主控 Agent 必须执行）：
   在文档末尾追加署名块（严格按照 `summary_template.md` 的表格要求）：
   
   ```markdown
   ## 📝 文档信息
   
   | 项目 | 信息 |
   |------|------|
   | 撰写人 | Lux（qwencode/qwen3.5-plus） |
   | 审核状态 | ✅ 已审核 / ⏭️ 已跳过 |
   | 审核模型 | <审核模型名称> |
   | 生成时间 | <YYYY-MM-DD HH:MM> |
   | 文档版本 | v1.0（最终版） |
   
   **审核修改记录**：
   - ✅ 核实接受日期：已确认
   - ✅ 关键数据已核对（X 处一致，Y 处已补充）
   - ✅ 图片已上传（X 张）
   ```

3. **更新本地元数据**：
   保存最终状态到 `$PAPER_DIR/final_metadata.json`。

4. **向用户交付最终版链接**，流程结束。

5. **记录修改日志** ⭐：
   ```bash
   # 保存修改记录到 progress/audit_apply.log
   # 包含：修改项、修改前、修改后、修改时间、验证结果
   ```

---

## 附加流程：补充材料处理

如果在【阶段零】判定传入的 PDF 为补充材料：

1. **主控 Agent 读取已有的飞书文档 token**：
   ```bash
   DOC_TOKEN=$(cat "$PAPER_DIR/feishu_doc_token.txt")
   ```

2. **执行合并脚本**：
   ```bash
   scripts/merge_supplement.sh "$PAPER_DIR" "<supplement.pdf>" "$DOC_TOKEN"
   ```

3. **主控 Agent 调用** `feishu_doc action=append` **将补充摘要追加到主文档**的"📎 补充材料"章节中。

4. **无需走完整生成和审核流程**。

---

## 主控 Agent 注意事项

### 子 Agent 清理机制（重要！）

**原则**：每个阶段完成后，立即清理已完成的子 Agent，只保留主控 Agent

**实现**：
1. 派生子 Agent 时记录 session_key
2. 等待子 Agent 完成（`sessions_yield`）
3. 获取子 Agent 结果
4. 立即清理：`subagents action=kill target="$session_key"`

**示例**：
```bash
# 阶段一：Reader Agent
reader_session=$(sessions_spawn task="Reader..." label="Reader-Agent")
sessions_yield  # 等待完成
summary_md=$(cat "$PAPER_DIR/summary.md")  # 获取结果
subagents action=kill target="$reader_session"  # ← 清理 Reader

# 阶段二：Vision Agent
vision_session=$(sessions_spawn task="Vision..." label="Vision-Agent")
sessions_yield
doc_token=$(cat "$PAPER_DIR/feishu_doc_token.txt")
subagents action=kill target="$vision_session"  # ← 清理 Vision

# 阶段三：Reviewer Agent
reviewer_session=$(sessions_spawn task="Reviewer..." label="Reviewer-Agent")
sessions_yield
audit_report=$(cat "$PAPER_DIR/audit_report.md")
subagents action=kill target="$reviewer_session"  # ← 清理 Reviewer

# 最终：只保留主控 Agent
```

**好处**：
- ✅ 只保留主控 Agent，降低内存占用（节省 ~300-400MB/每个阶段）
- ✅ 避免子 Agent 堆积
- ✅ 明确的资源管理

---

### 职责边界

- ✅ **应该做的**：
  - 调度流程
  - 执行系统脚本
  - 调用 `sessions_spawn` 派生子 Agent
  - 整合子 Agent 的结果
  - 与用户沟通确认

- ❌ **不应该做的**：
  - 亲自阅读长文本（交给 Reader）
  - 亲自处理图片上传（交给 Vision）
  - 自我审核（交给 Reviewer + 真实数据注入）

---

### 🚨 飞书操作关键原则（本业务特有）

**核心原则**：
> 📌 **通用工具用法参考 `feishu-doc` 技能文档**
> 📌 **本节只记录本业务特有的纠偏规则和易错点**

---

#### 1. 图片上传防限流（高优先级）

**规则**：任何涉及 `upload_image` 的循环操作，必须：
```bash
feishu_doc action=upload_image ...
sleep 3  # 必须间隔 3 秒
feishu_doc action=upload_image ...
sleep 3  # 必须间隔 3 秒
```

**违反后果**：
- `file_token` 为空字符串
- 图片 block 创建但图片转圈不显示
- 需要删除所有空 token block 重新上传

**严重限流时**：
- 等待 10 秒后重试
- 增加间隔到 5 秒

---

#### 2. 删除失败 → 重置法（兜底方案）

**适用场景**：
- `delete_block` 返回 404（block 不存在）
- 文档结构混乱，需要清理
- Block IDs 失效，无法定位
- 连续 2 次 `upload_image` 返回空 `file_token`

**操作步骤**：
```bash
# 1. 使用 Reader 生成的完整 summary.md（不要精简）
# 2. 全量覆盖（清除所有旧 blocks）
feishu_doc action=write doc_token="$DOC_TOKEN" content="$(cat $PAPER_DIR/summary.md)"
# 3. 重新 upload_image 上传图片
# 4. read 查看文档确认结果
```

**效果**：清除所有旧 blocks，恢复到干净状态。

**方案对比**：
| 场景 | 方案 | 地位 |
|------|------|------|
| 文档结构混乱、block IDs 失效 | 重置法（`write` 全量覆盖） | **兜底方案** |
| 图片精确定位 | 占位符法（`【FIGURE_X】`） | **首选方案** |

**历史经验**：
- 2026-03-26/27：遇到 `delete_block` 404 错误，使用重置法成功
- 2026-03-28：占位符方案验证成功，成为首选方案

---

#### 3. 操作前确认流程

**任何飞书文档修改操作前**，必须：
1. `list_blocks` 获取最新 blocks 列表
2. 确认目标 blocks 存在（检查 block IDs）
3. 逐个调用工具（不批量）
4. 操作后再次 `list_blocks` + `read` 验证

---

#### 4. 图片精确定位技巧

**参数说明**：
- `parent_block_id`: 文档根 ID（和 `doc_token` 相同）
- `index`: 从 `list_blocks` 的 `children` 数组获取（0-based）
- 不填 `parent_block_id` 则自动追加到末尾

**定位方法**：
```bash
# 从 list_blocks 返回中找到章节标题的 block_id
# 计算其 index（在 children 数组中的位置）
# 上传图片时 index = 章节 index + 1
```

**插入策略**：
- 从文档末尾往前插（倒序），避免索引偏移
- Fig. 1 插入到 4.1 章节后，Fig. 2 插入到 4.2 章节后

---

#### 5. 上传后验证清单

**必须检查**：
- [ ] `upload_image` 返回的 `file_token` 不为空字符串
- [ ] `read` 查看文档，确认图片数量正确
- [ ] 打开飞书文档确认图片显示（不转圈）

**验证命令**：
```bash
feishu_doc action=read doc_token="$DOC_TOKEN"
# 检查 "Image" 数量是否正确
# 如果 "Image": 7，说明 7 张图片都已成功上传
```

---

#### 6. 区分两种"delete"

**不要混淆**：
| 操作 | 用途 | 常见错误 | 解决方案 |
|------|------|----------|----------|
| `feishu_doc delete_block` | 删除文档块 | 404（block 不存在） | 用重置法（write 全量覆盖） |
| `feishu_drive delete` | 删除云空间文件 | 400（权限问题） | 检查文件权限 |

---

### 错误处理

**子 Agent 错误报告机制**：

### 错误处理

**子 Agent 错误报告机制**：

如果子 Agent 执行失败，必须写入错误报告：

```bash
# 错误报告格式 ($PAPER_DIR/errors/<agent>.log)
## 错误报告

**子 Agent**: Reader/Vision/Reviewer  
**错误类型**: 脚本执行失败 / API 限流 / 文件不存在 / 超时 / ...  
**错误信息**: <具体错误内容>  
**发生时间**: YYYY-MM-DD HH:MM:SS  
**重试次数**: X/3  

### 建议操作
<主控 Agent 应该采取的行动，如：重试、跳过、人工介入等>
```

**主控 Agent 响应流程**：

1. **检查错误日志**：读取 `$PAPER_DIR/errors/<agent>.log`
2. **判断错误类型**：
   - **可重试错误**（如 API 限流、网络超时）：重试最多 3 次
   - **致命错误**（如文件不存在、权限不足）：停止任务，告知用户
3. **用户沟通**：如重试失败，向用户说明情况并提供建议

**常见错误处理**：

| 错误类型 | 错误代码 | 处理方案 |
|----------|----------|----------|
| 飞书 API 限流 | 429 | 等待 10 秒后重试，增加 sleep 时间到 5 秒 |
| Block 不存在 | 404 | 重新获取 blocks 列表，或使用重置法 |
| PDF 无法提取文本 | - | 检查是否为扫描版，建议使用 OCR |
| 子 Agent 超时 | - | 增加 `timeoutSeconds`，或拆分任务 |
| 文件不存在 | - | 检查路径，重新运行前置脚本 |
| jq 解析失败 | - | 检查 JSON 格式，手动修复 metadata.json |
| OCR 识别失败 | - | 检查 tesseract 是否安装，语言包是否存在 |
| 图片上传失败 | - | 检查图片文件是否存在，大小是否超过限制 |

**重试机制示例**：

```bash
# 飞书 API 调用重试
max_retries=3
retry_count=0

while [[ $retry_count -lt $max_retries ]]; do
    result=$(feishu_doc action=upload_image ...)
    
    if echo "$result" | grep -q '"success": true'; then
        echo "✅ 上传成功"
        break
    elif echo "$result" | grep -q "429"; then
        retry_count=$((retry_count + 1))
        echo "⚠️  API 限流，等待 10 秒后重试 ($retry_count/$max_retries)"
        sleep 10
    else
        echo "❌ 上传失败：$result"
        break
    fi
done

if [[ $retry_count -eq $max_retries ]]; then
    echo "❌ 达到最大重试次数，任务失败"
    # 写入错误日志
    echo "错误类型：API 限流" >> "$PAPER_DIR/errors/vision.log"
    echo "重试次数：$max_retries" >> "$PAPER_DIR/errors/vision.log"
    echo "建议操作：等待 5 分钟后重试，或联系用户" >> "$PAPER_DIR/errors/vision.log"
fi
```

---

## 子 Agent 职责说明

| 子 Agent | 职责 | 关键技能 | 进度日志 |
|----------|------|----------|----------|
| **Reader** | 长文本阅读、总结生成 | 分段读取、信息提取、结构化输出 | `progress_reader.log` |
| **Vision** | 图片审核、飞书上传 | 图片识别、`upload_image`、限流规避 | `progress_vision.log` |
| **Reviewer** | 数据一致性核对 | 数据比对、格式检查、报告生成 | `progress/reviewer.log` |

---

## 进度日志文件说明

每个子 Agent 执行时都会生成进度日志文件，便于调试和审计：

### 进度日志位置

| 文件 | 说明 | 生成时机 |
|------|------|----------|
| `$PAPER_DIR/progress/reader.log` | Reader 子 Agent 进度 | 阅读论文时 |
| `$PAPER_DIR/progress/vision.log` | Vision 子 Agent 进度 | 上传图片时 |
| `$PAPER_DIR/progress/reviewer.log` | Reviewer 子 Agent 进度 | 审核数据时 |
| `$PAPER_DIR/errors/<agent>.log` | 错误报告 | 发生错误时 |

### 进度日志格式

```log
[YYYY-MM-DD HH:MM:SS] <Agent> 子 Agent 启动
[YYYY-MM-DD HH:MM:SS] 开始 <任务描述>
[YYYY-MM-DD HH:MM:SS] ✅ 完成：<步骤 1>
[YYYY-MM-DD HH:MM:SS] ✅ 完成：<步骤 2>
[YYYY-MM-DD HH:MM:SS] ✅ <Agent> 任务完成
[YYYY-MM-DD HH:MM:SS] 输出文件：<文件路径>
[YYYY-MM-DD HH:MM:SS] 总耗时：X 分钟
```

### 错误报告格式

```markdown
## 错误报告

**子 Agent**: <Agent 名称>  
**错误类型**: <错误类型>  
**错误信息**: <具体错误>  
**发生时间**: YYYY-MM-DD HH:MM:SS  
**重试次数**: X/3  

### 建议操作
<主控 Agent 应该采取的行动>
```

---

## 版本历史

- **v2.0.0** (2026-03-28)：重构为多 Agent 协作架构，新增防幻觉机制 + 飞书操作知识精简
- **v1.x**：单 Agent 全流程（已废弃）

---

## 附录：改进的汇报模板

### Reader 子 Agent 完成报告（详细版）

```markdown
## Reader 子 Agent 完成报告

**开始时间**: YYYY-MM-DD HH:MM  
**完成时间**: YYYY-MM-DD HH:MM  
**耗时**: X 分钟  

### 执行结果
- ✅ 成功生成 summary.md

### 输出文件
- `$PAPER_DIR/summary.md` (XXX KB, XXX 行)
- `$PAPER_DIR/progress/reader.log` (进度日志)

### 论文关键信息
- **研究类型**: <如 RCT、队列研究等>
- **样本量**: <如 2,069 人>
- **主要结局**: <如 问诊时长减少 28.7%>

### 问题与备注
<如有问题，在此说明；如无问题，填写"无">

### 详细进度
| 步骤 | 状态 | 耗时 |
|------|------|------|
| 读取 paper.txt | ✅ 完成 | X 秒 |
| 提取研究背景 | ✅ 完成 | X 秒 |
| 提取研究设计 | ✅ 完成 | X 秒 |
| 提取核心结果 | ✅ 完成 | X 秒 |
| 生成 summary.md | ✅ 完成 | X 秒 |
```

### Vision 子 Agent 完成报告（详细版）

```markdown
## Vision 子 Agent 完成报告

**开始时间**: YYYY-MM-DD HH:MM  
**完成时间**: YYYY-MM-DD HH:MM  
**耗时**: X 分钟  

### 执行结果
- ✅ 成功上传 X/Y 张图片

### 图片上传清单
| Figure | file_token | 大小 | 插入位置 | 状态 |
|--------|------------|------|----------|------|
| Fig. 1 | `xxx...` | XXX KB | 4.1 章节后 | ✅ |

### 输出文件
- `$PAPER_DIR/progress/vision.log` (进度日志)

### 问题与备注
<如有问题，在此说明>

### 详细进度
| 步骤 | 状态 | 耗时 |
|------|------|------|
| 获取 blocks 列表 | ✅ 完成 | X 秒 |
| 上传 Fig. 1 | ✅ 完成 | X 秒 |
| 上传 Fig. 2 | ✅ 完成 | X 秒 |
| 上传 Fig. 3 | ✅ 完成 | X 秒 |
| 验证图片数量 | ✅ 完成 | X 秒 |
```

### Reviewer 子 Agent 完成报告（详细版）

```markdown
## Reviewer 子 Agent 完成报告

**开始时间**: YYYY-MM-DD HH:MM  
**完成时间**: YYYY-MM-DD HH:MM  
**耗时**: X 分钟  
**审核模型**: <模型名称>

### 执行结果
- ✅ 审核通过 / ⚠️ 需要修改

### 审核统计
- 一致的内容：X 处
- 需要修改的内容：Y 处
- 格式问题：Z 处

### 输出文件
- `$PAPER_DIR/progress/reviewer.log` (进度日志)
- `$PAPER_DIR/audit_report.md` (审核报告全文)

### 关键问题
<如有严重问题，在此说明>

### 修改建议清单
1. <具体修改建议 1>
2. <具体修改建议 2>
...

### 详细进度
| 步骤 | 状态 | 耗时 |
|------|------|------|
| 读取原始数据 | ✅ 完成 | X 秒 |
| 读取总结内容 | ✅ 完成 | X 秒 |
| 数据一致性核对 | ✅ 完成 | X 秒 |
| 格式检查 | ✅ 完成 | X 秒 |
| 生成审核报告 | ✅ 完成 | X 秒 |
```

---

## 附录：关键步骤确认函数

```bash
# 关键步骤确认函数
confirm_step() {
    local step_name=$1
    local log_file=$2
    
    log_master "🔍 确认步骤：$step_name"
    
    if [[ ! -f "$log_file" ]]; then
        log_master "❌ 日志文件不存在：$log_file"
        return 1
    fi
    
    # 检查是否有 ERROR
    if grep -q "\[ERROR\]" "$log_file"; then
        log_master "❌ 检测到错误，查看错误日志"
        cat "$log_file" | grep "\[ERROR\]"
        return 1
    fi
    
    # 检查是否完成
    if grep -q "✅ 完成\|\[SUCCESS\]" "$log_file"; then
        log_master "✅ 步骤确认成功：$step_name"
        return 0
    else
        log_master "⚠️ 步骤未完成：$step_name"
        return 1
    fi
}

# 使用示例（在每个阶段完成后调用）
# confirm_step "Reader 完成" "$PAPER_DIR/logs/reader.log" || exit 1
# confirm_step "Vision 完成" "$PAPER_DIR/logs/vision.log" || exit 1
# confirm_step "Reviewer 完成" "$PAPER_DIR/logs/reviewer.log" || exit 1
```

---

## 附录：Vision 模型自动识别

### 工作原理

技能会自动从 `~/.openclaw/openclaw.json` 中查找支持图片输入的模型：

```bash
# 自动识别逻辑
VISION_MODEL=$(jq -r '
  .models.providers | to_entries[] | 
  .value.models[] | 
  select(.input and (.input | index("image"))) | 
  .id | 
  first
' "~/.openclaw/openclaw.json")
```

**识别逻辑**：
1. 遍历所有 provider 的 models
2. 查找 `input` 字段包含 `"image"` 的模型
3. 使用找到的第一个模型
4. 如果找不到，回退到 `model.primary`

**如何判断模型是否支持图片**：
查看 `models.providers[].models[]` 中的 `input` 字段：
```json
{
  "models": {
    "providers": {
      "qwencode": {
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5 Plus",
            "input": ["text", "image"]  ← 支持图片
          }
        ]
      }
    }
  }
}
```

**优点**：
- ✅ 无需手动配置
- ✅ 自动选择支持图片的模型
- ✅ 向后兼容（无配置也能用）
- ✅ 符合"约定优于配置"原则

---

## 版本历史

- **v2.0.0** (2026-03-28)：重构为多 Agent 协作架构，新增防幻觉机制 + 飞书操作知识精简
  - 完全重写 SKILL.md，从单 Agent 改为多 Agent 协作（Reader/Vision/Reviewer）
  - 新增 5 个核心脚本（extract_metadata.sh, check_duplicate.sh, extract_pdf_text.sh, locate_figures.sh, merge_supplement.sh）
  - 新增防幻觉机制：强制注入原始数据到 Reviewer 子 Agent
  - 新增标准化汇报机制（进度日志 + 完成报告 + 错误报告）
  - 精简飞书操作知识：删除通用内容，保留本业务特有的 6 大核心原则
- **v1.x**：单 Agent 全流程（已废弃）
