# PPT Master 版本历史

## v1.2.3 (2026-05-07) - XML 实体自动转义

**修复内容：**

### 1. 架构级 XML 容错设计
- ✅ 新增 `escape-xml` 处理步骤（finalize_svg.py Step 1.5）
- ✅ 自动转义 SVG 中孤立的 `&` 符号
- ✅ 使用负向前瞻正则，避免重复转义已转义实体

### 2. 技术实现
- 新增函数：`escape_xml_entities(svg_file)`
- 正则模式：`r'&(?!amp;|lt;|gt;|quot;|apos;|nbsp;|#\d+;|#x[0-9a-fA-F]+;)'`
- 处理流程：复制 svg_output → svg_final 后立即执行转义
- 默认启用：`escape_xml: True`

### 3. 测试验证
- 孤立 `&` → `&amp;` ✅
- 已转义实体不被修改 ✅
- `&&` → `&amp;&amp;` ✅
- XML 语法验证通过 ✅

**根本原因：**
- 批量生产的容错设计必须在架构层解决，不能靠事后修补
- 之前的 PPT 生成任务中，SVG 包含 `&` 符号导致 XML 解析失败

**预期收益：**
- 所有 PPT 生成的 SVG 自动转义，无需人工干预
- 避免导出 PPTX 时 XML 解析错误
- 架构级预防，而非事后修补

**文件变更：**
- `scripts/finalize_svg.py` - 新增 escape_xml_entities() 和 Step 1.5
- `.learnings/LEARNINGS.md` - 记录修复过程

---

## v1.2.2 (2026-04-25) - 技能选择机制优化

**优化内容：**

### 1. YAML Front Matter 重构
- ✅ 新增独立的 `read_when` 字段，明确触发词列表
- ✅ 新增 `metadata.openclaw` 配置：
  - `priority: high` - 高优先级，在多技能匹配时优先选择
  - `category: content-generation` - 分类标签
  - `tags` - 技能标签（ppt, presentation, slides, 演示文稿）
  - `conflicts_with` - 冲突技能列表（ppt-video, fireworks-tech-graph）

### 2. 触发词明确化
- 新增 10+ 个明确的中文触发词
- 区分不同场景：
  - 直接生成："生成 PPT"、"做 PPT"、"制作演示文稿"
  - 文件转换：PDF → PPT、DOCX → PPT、URL → PPT
  - 专业场景：财报、技术汇报、商业演示
  - 特定要求："原生可编辑"、"可修改"

### 3. 中文友好
- description 改为中文优先
- 触发词以中文为主，符合用户习惯

### 4. 冲突处理
- 明确标注与 `ppt-video`、`fireworks-tech-graph` 的冲突关系
- Agent 在选择时可避免误判

**预期收益：**
- 提高技能选择准确率
- 减少技能冲突
- 优先选择 pptx-master（priority: high）
- 中文场景更友好

**文件变更：**
- `SKILL.md` - YAML front matter 重构

---

## v1.2.1 (2026-04-19) - XML Validation Enhancement

**Fixed:**
- **SVG Content Checker** now validates XML syntax before content analysis
- Detects mismatched tags (e.g., `<tspan>...</text>`)
- Catches malformed SVG that would cause rendering failures

**Technical Details:**
- Added `xml.etree.ElementTree.fromstring()` validation in `_check_content_elements()`
- XML parse errors now block the workflow with clear error messages
- Prevents false-positive "passes" on malformed SVG files

**Issue Resolved:**
- Page 7 of AI Weekly Report PPT was blank due to XML tag mismatch
- Root cause: `<tspan>` closed with `</text>` instead of `</tspan>`
- Old checker missed it because it only counted string occurrences

---

## v1.2.0 (2026-04-18) - Content Review & Auto-Repair

**Added:**
- **SVG Content Checker** (`scripts/svg_content_checker.py`)
  - Blank page detection (text elements < 2 AND file size < 500 bytes)
  - Content density scoring (0-100%)
  - Design consistency checking (colors, fonts)
  - Structure completeness evaluation
- **SVG Repair Coordinator** (`scripts/svg_repair_coordinator.py`)
  - Automatic repair workflow
  - Regeneration prompt generation for blank pages
  - Fallback to placeholder pages when repair fails
- **Step 6.5** in workflow: Content Review & Auto-Repair
  - Automatic check after SVG generation
  - Non-blocking: warnings allow continuation
  - Blocking: blank pages trigger repair workflow

**Changed:**
- `SKILL.md`: Added Step 6.5 between SVG generation and post-processing
- Tool list: Added svg_content_checker.py and svg_repair_coordinator.py

**Use Case:**
- Automatically detect blank pages before PPTX export
- Generate repair prompts for manual regeneration
- Ensure presentation quality before delivery
