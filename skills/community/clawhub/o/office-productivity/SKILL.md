---
name: office-productivity
description: 办公自动化技能套件，涵盖文档处理（Word/Excel/PPT/PDF）、邮件管理、日程规划、报表生成、会议纪要等办公场景。触发场景：创建文档、编辑表格、制作PPT、处理邮件、生成报表、日程管理、整理会议记录、批量文件处理等任何办公效率提升需求。
---

# Office Productivity - 办公自动化

## 核心能力

### 文档处理
- **Word (.docx)**：创建、编辑、格式化；支持模板填充、批注处理、页眉页脚
- **Excel (.xlsx)**：数据整理、公式计算、图表生成、批量数据处理
- **PPT (.pptx)**：幻灯片创建、模板应用、批量排版
- **PDF**：合并、拆分、提取文字/图片、加水印、签名

### 邮件 & 日历
- 邮件读取 / 发送（IMAP/SMTP）
- 邮件批量处理（分类、归档、回复）
- 日程读取与事件创建（ ICS / Google Calendar API）

### 报告 & 文档生成
- 根据模板自动填充数据生成报告
- 多文件汇总（会议记录、项目文档合并）
- 格式化输出（Markdown → Word/PDF）

### 关键脚本
- `scripts/create_docx.py` - Python-docx 创建 Word 文档
- `scripts/create_xlsx.py` - openpyxl 创建 Excel（含图表）
- `scripts/create_pptx.py` - python-pptx 创建 PPT
- `scripts/pdf_tools.py` - PDF 处理（合并/拆分/提取）
- `scripts/mail_client.py` - IMAP/SMTP 邮件收发

### 参考资源
- `references/office-templates/` - 常用办公模板
- `references/api-docs.md` - 邮件/日历 API 说明

## 工作流程

1. **明确需求**：用户需要处理什么办公任务？
2. **选择工具**：根据文件类型和任务性质选择对应脚本
3. **执行生成**：调用对应脚本，传入参数
4. **输出交付**：文件路径或直接发送

## 注意事项
- Office 文件优先使用 python-docx / openpyxl / python-pptx 库
- PDF 处理推荐 PyPDF2 / pdfplumber
- 邮件操作需要用户提供 IMAP/SMTP 配置
- 批量处理先在小样本上测试再全量执行
