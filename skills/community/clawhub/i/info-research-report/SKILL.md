---
name: info-research-report
description: 信息调研报告自动化工作流。一键完成：多源搜索 → 深度挖掘 → 政府风格 DOCX 报告生成 → 邮件发送。
metadata:
  openclaw:
    command-dispatch: tool
    command-tool: exec
  requirements:
    python_packages:
      - python-docx
      - requests
    external_tools:
      - mcporter (browseros MCP) - 网页抓取
      - email-mail-master - 邮件发送
    environment_variables:
      - MINIMAX_API_KEY (可选/MiniMax API Key，用于生成摘要)
      - OPENAI_API_KEY (可选/OpenAI API Key，用于生成摘要)
  permissions:
    - read_files
    - execute_scripts
    - network_access
  warnings:
    - 本技能会将网页正文和生成的摘要发送到第三方 LLM 服务 (MiniMax/OpenAI) 进行处理
    - 请确保第三方服务的隐私和合规要求符合你的使用场景
    - 仅使用专用的 API Key，不要将与其他服务共享的密钥设置到环境变量中
---

# 信息调研报告自动化（政府标准版）

本 skill 用于自动生成"政府 / 机关单位风格"的调研报告：

- 封面（研究报告 + 主题 + 编制单位 + 编制时间）
- 报告说明 / 元信息
- 一、研究背景和目的
- 二、研究方法
- 三、主要发现和结论（Executive Summary）
- 四、详细来源分析（Source Details）
- 五、参考资料（All Search Results）

并自动将生成的 DOCX 报告通过邮件发送给指定收件人。

---

## 工作流程

### 步骤1：使用浏览器搜索

**推荐方案：使用 mcporter 调用 browseros**

```bash
# 1. 打开搜索页面
mcporter call browseros.new_page url="https://duckduckgo.com/html/?q=你的主题"

# 2. 获取页面内容
mcporter call browseros.get_page_content -- page=1
```

### 步骤2：提取搜索结果

从页面内容中解析搜索结果，保存为 `results.json`：

```json
[
  {
    "title": "结果标题",
    "url": "https://example.com/xxx",
    "content": "（可选）网页完整正文，用于生成更详细的摘要"
  }
]
```

### 步骤3：生成报告并发送邮件

```bash
python run.py "主题" "邮箱" "results.json" [--no-fetch]
```

- `--no-fetch`：跳过网页内容抓取，使用更快但摘要较简略

---

## 一键命令格式（需要先有 results.json）

```bash
python "C:\Users\Juxin\.openclaw\workspace\skills\info-research-report\run.py" "主题" "邮箱" "results.json"
```

- 若未提供 `results.json` 或文件不存在，脚本会使用一条预设提示数据，生成"示例报告"。

---

## 支持的参数

1. **主题**（必须）
   - 研究报告的主题关键词（例如："人工智能发展趋势"）
2. **邮箱**（必须）
   - 接收报告的邮箱地址
3. **results.json**（可选）
   - 搜索结果文件路径，推荐命名为 `results.json`
   - 若省略或文件不存在，将使用预置提示数据生成示例报告

---

## 报告输出结构（DOCX）

生成的 DOCX 报告为"政府/机关调研报告风格"，主要包含以下部分：

1. **封面**
   - 标题：`研究报告`
   - 副标题：`-- 主题`
   - 编制单位：可在代码中修改为实际部门名称
   - 编制时间：自动填入当前日期

2. **报告说明 / Report Information**
   - 报告主题 / Topic
   - 报告生成时间 / Generated
   - 信息来源数量 / Total Sources
   - 免责声明：如"本报告基于公开网络信息自动生成，仅供内部参考使用，不代表正式立场。"

3. **一、研究背景和目的**
   - 描述调研的背景、目的和使用范围（有模板文案，可按需修改）

4. **二、研究方法**
   - 说明使用 OpenClaw + browser 工具进行自动化检索
   - 描述信息筛选、整理与分析的方法

5. **三、主要发现和结论（Executive Summary）**
   - 对"主题"的主要结论进行概括性说明
   - 自动列出前若干个代表性信息点（基于前几条搜索结果标题）
   - 提示"需结合正文进一步研判"

6. **四、详细来源分析（Source Details）**
   - 对每条搜索结果输出一个小节，格式示例：
     - （1）标题
     - 来源 / Source：URL
     - 摘要 / Summary：snippet（如有）
   - 便于阅读者逐条查看来源信息

7. **五、参考资料（All Search Results）**
   - 列出所有搜索结果的标题与 URL，作为参考文献列表
   - 格式：
     - • 标题
       URL：...

---

## 报告输出示例（结构示意）

```text
研究报告
-- 人工智能发展趋势
编制单位：某某研究部门 / Research Department
编制时间：2026年04月03日

（分页）

报告说明 / Report Information
报告主题 / Topic：人工智能发展趋势
报告生成时间 / Generated：2026-04-03 11:34:00
信息来源数量 / Total Sources：5
说明：本报告基于公开网络信息自动生成，仅供内部参考使用，不代表正式立场。
------------------------------------------------------------

一、研究背景和目的
为系统掌握"人工智能发展趋势"相关情况，本报告通过自动化工具收集和整理了互联网上的公开信息……

------------------------------------------------------------

二、研究方法
1. 通过 OpenClaw browser 自动化工具，在 DuckDuckGo 等搜索引擎中检索"人工智能发展趋势"相关信息；
2. 对检索结果中较为权威、信息量较大的来源进行筛选……

------------------------------------------------------------

三、主要发现和结论（Executive Summary）
综合各类公开信息，围绕"人工智能发展趋势"，本报告整理了以下若干主要结论和要点：

（示例）
（1）AI 行业整体保持高速发展，相关应用场景持续扩大……
（2）多国政府陆续发布人工智能发展规划与监管政策……
（3）大模型技术成为当前热点方向……

（以上要点根据来源标题和摘要自动提取，实际使用时建议结合正文内容进一步研判。）

------------------------------------------------------------

四、详细来源分析（Source Details）

（1）某权威机构发布的人工智能发展白皮书
来源 / Source：https://example.com/ai-whitepaper
摘要 / Summary：该白皮书系统分析了当前 AI 发展现状……

（2）某主流媒体关于人工智能监管政策的报道
来源 / Source：https://example.com/ai-policy
摘要 / Summary：文章梳理了近期多国出台的 AI 监管政策……

……

------------------------------------------------------------

五、参考资料（All Search Results）
• 某权威机构发布的人工智能发展白皮书
  URL：https://example.com/ai-whitepaper
• 某主流媒体关于人工智能监管政策的报道
  URL：https://example.com/ai-policy
• ……
```

---

## 依赖与环境要求

### Python 包
- `python-docx` - 生成 DOCX 报告
- `requests` - 调用 LLM API（可选）
- 标准库：`os`, `sys`, `json`, `subprocess`, `datetime`, `re` 等

### 环境变量（可选）
- `MINIMAX_API_KEY` - MiniMax API Key（用于生成摘要）
- `OPENAI_API_KEY` - OpenAI API Key（备用）
- `OPENCLAW_SKILLS_DIR` - 技能根目录（默认：`C:\Users\Juxin\.openclaw\workspace\skills`）

> ⚠️ **配置方法**：
> 1. 复制 `.env.template` 为 `.env`
> 2. 填入你的 API Key
> 3. 运行脚本时会自动加载

### 快速配置命令
```bash
# 复制模板
copy "C:\Users\Juxin\.openclaw\workspace\skills\info-research-report\.env.template" "C:\Users\Juxin\.openclaw\workspace\skills\info-research-report\.env"

# 编辑 .env 文件，填入你的 API Key
notepad "C:\Users\Juxin\.openclaw\workspace\skills\info-research-report\.env"
```

### 外部工具
- `mcporter` + `browseros MCP` - 网页内容抓取
- `email-mail-master` - 邮件发送（需要邮箱配置）

### 安装依赖
```bash
pip install python-docx requests
```

---

## Browser 工具集成说明

本 skill 默认假设：

- 搜索阶段由 OpenClaw 的 `browser` 工具完成：
  - `browser action=navigate ...`
  - `browser action=snapshot`
- 解析阶段可在上游 skill 或外部脚本中完成，将结果写入 `results.json`
- 本 skill 专注于：
  - 使用已有的 `results.json` 生成"政府风格" DOCX 报告
  - 将报告通过 email skill（`email-mail-master`）发送至指定邮箱

如果 browser 工具不可用，也可以手工构造 `results.json`，直接调用 `run.py` 生成报告。

---

## 邮件发送

本 skill 调用 `email-mail-master` skill 的 `mail.py` 脚本发送邮件。

> ⚠️ **路径说明**：默认使用环境变量 `OPENCLAW_SKILLS_DIR` 指定的技能目录查找邮件脚本。请确保：
> - 环境变量 `OPENCLAW_SKILLS_DIR` 已正确配置
> - `email-mail-master` skill 已安装
> - 邮件服务（QQ/163/阿里云）已配置完成

邮件内容包含：
- 主题：`研究报告 / Research Report: 主题`
- 正文简要说明：
  - 主题 / Topic
  - 来源数量 / Sources
  - 提示"附带自动生成的研究报告（DOCX），仅供内部参考使用"
- 附件：生成的 DOCX 报告文件

---

## 示例命令

```bash
# 前提：已通过 browser 工具完成搜索并生成 results.json
python "C:\Users\Juxin\.openclaw\workspace\skills\info-research-report\run.py" "人工智能发展趋势" "2507541738@qq.com" "results.json"
```

运行后效果：
- 当前目录生成：`Report_人工智能发展趋势_YYYYMMDDHHMM.docx`
- 收件邮箱收到一封带 DOCX 报告附件的邮件
```