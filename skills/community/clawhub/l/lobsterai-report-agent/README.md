# lobsterai-report-agent

超长可行性研究报告多 Agent 协作撰写系统。

多子 Agent 并行创作 + 自动编排流程 + 精美 docx 输出，适合 10+ 章节的超长篇报告。

---

## 功能特性

- **多 Agent 并行**：最多 5 个子 Agent 并发撰写，效率翻倍
- **增量更新**：内容未变化的章节跳过重写
- **精美排版**：封面、表格式目录、彩色章节标题、重点标注盒、美化表格
- **飞书 RAG**：自动检索飞书知识库补充参考资料
- **6 种封面风格**：经典政务 / 现代简约 / 商务典雅 / 科技数字 / 中式传统 / 全屏沉浸
- **跨章一致性审查**：自动检查数量指标冲突和术语不统一

---

## 目录结构

```
lobsterai-report-agent/
├── SKILL.md                 # OpenClaw Skill 说明文档
├── README.md                # 本文件
├── LICENSE                  # MIT License
├── requirements.txt         # Python 依赖
├── integrate_report.py      # facade（兼容旧接口）+ CLI 入口
├── parallel_tracker.py      # 并行进度追踪
├── notify.py                # 可配置通知渠道
├── src/
│   ├── __init__.py         # 包入口，导出公共 API
│   ├── config.py            # 路径配置 + 文件 I/O
│   ├── engine.py             # 核心业务逻辑（markdown → docx、术语表、审查等）
│   └── cli.py               # CLI 入口
└── references/              # 子流程参考文档
    ├── phase0_guide.md      # Phase 0 需求确认流程
    ├── phase1_guide.md      # 规划师 prompt 模板
    ├── phase2_guide.md      # 子 Agent prompt 模板
    ├── table_format_guide.md # Markdown 表格格式规范
    └── bug_fix_guide.md     # Bug 排查与强制重建
```

---

## 快速开始

### 安装依赖

```bash
pip install python-docx
```

（可选，Mermaid 图表渲染需要）：

```bash
npm install -g @mermaid-js/mermaid-cli
```

### 配置工作目录

默认工作目录：`~/.config/lobsterai-report-agent/`

可通过环境变量覆盖：

```bash
# Linux / macOS
export LOBAI_CHAPTERS_DIR=/path/to/your/chapters
export LOBAI_OUTPUT_DIR=/path/to/output

# Windows
set LOBAI_CHAPTERS_DIR=D:\my_reports\chapters
set LOBAI_OUTPUT_DIR=D:\my_reports\output
```

或在工作目录放置 `config.json`：

```json
{
  "project_name": "XX市医疗资产精细化管理方案",
  "doc_type": "可行性研究报告",
  "notification_channel": "log"
}
```

### CLI 用法

```bash
# 生成整合报告（全部章节 → docx）
python integrate_report.py

# 批量转换章节 txt → docx
python integrate_report.py convert-batch

# 单章转换
python integrate_report.py --convert-one 01-概述.txt 01-概述.docx

# 生成/更新术语表
python integrate_report.py glossary

# 跨章一致性审查
python integrate_report.py check

# 查看/清空参考资料
python integrate_report.py ref show
python integrate_report.py ref clear
```

### Python API 用法

```python
import integrate_report as ir

# 读取配置
plan = ir.load_plan()
chapters_dir = ir.get_chapters_dir()

# 生成整合报告
result = ir.generate_with_accurate_toc()

# 批量转换
ir.batch_convert_txt_to_docx()

# 一致性审查
issues = ir.check_cross_chapter_consistency(chapters_data)
```

---

## Pipeline 流程

```
Phase 0：需求确认（4 步）
    ↓
Phase 1：规划师生成大纲（plan.json）
    ↓
Phase 2：并行子 Agent 撰写（最多 5 并发）
    ↓
Phase 2.5：跨章一致性审查
    ↓
Phase 3：整合师汇总 → docx
```

详见 [SKILL.md](SKILL.md)

---

## 通知渠道配置

`notify.py` 支持可配置的推送渠道：

| 渠道 | 配置值 | 说明 |
|------|--------|------|
| 控制台（默认） | `log` | 打印到 stdout |
| 飞书 | `feishu` | 通过 OpenClaw 飞书插件推送 |
| OpenClaw 微信 | `openclaw-weixin` | 通过 OpenClaw 微信插件推送 |

配置方式（三选一）：

1. `config.json` 中添加：`"notification_channel": "feishu"`
2. 环境变量：`set LOBAI_NOTIFY_CHANNEL=feishu`
3. 代码中调用：`notify.set_channel('feishu')`

---

## License

MIT License - 详见 [LICENSE](LICENSE) 文件
