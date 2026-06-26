# 信息调研报告自动化 (Automated Information Research Report)

一个用于自动生成政府风格调研报告的 OpenClaw Skill。

## 功能

- 一键生成政府/机关风格的 DOCX 调研报告
- 自动调用 LLM 生成摘要（背景/趋势/风险三部分）
- 支持网页内容抓取和分析
- 自动发送报告到指定邮箱

## 安装

### 依赖安装

```bash
pip install python-docx requests
```

### 环境变量（可选）

- `MINIMAX_API_KEY` - MiniMax API Key（用于生成摘要）
- `OPENAI_API_KEY` - OpenAI API Key（备用）
- `OPENCLAW_SKILLS_DIR` - 技能根目录

### 使用方式

1. **搜索主题**
```bash
mcporter call browseros.new_page url="https://duckduckgo.com/html/?q=你的主题"
mcporter call browseros.get_page_content -- page=1
```

2. **提取结果保存为 results.json**
```json
[
  {
    "title": "结果标题",
    "url": "https://example.com",
    "content": "（可选）网页正文"
  }
]
```

3. **生成报告**
```bash
python run.py "主题" "邮箱" "results.json" [--no-fetch]
```

## 参数

| 参数 | 说明 |
|------|------|
| 主题 | 研究报告的主题 |
| 邮箱 | 收件人邮箱 |
| results.json | 搜索结果文件（可选） |
| --no-fetch | 跳过网页抓取，使用更快 |

## 输出报告结构

1. 封面
2. 报告说明
3. 研究背景和目的
4. 研究方法
5. 主要发现和结论
6. 详细来源分析
7. 参考资料

## 依赖

- Python: python-docx, requests
- 外部工具: mcporter (browseros MCP), email-mail-master
- 权限: read_files, execute_scripts, network_access

## License

MIT-0