# patent-disclosure · 技术交底书

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://clawhub.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-Publish-orange.svg)](https://clawhub.ai)

[English](#english) · [中文](#中文)

---

## 中文

引导撰写**专利技术交底书**：模板、检查清单、结合 **patent-search** 做现有技术对比，并 **导出 Word（.docx）** 供下载。

### 主要能力

| 命令 | 说明 |
|------|------|
| `template` | 空白交底书 Markdown 模板 |
| `checklist` | 撰写检查清单 |
| `export` | 传入完整 Markdown `content` → 生成 `.docx` |

**无需** 9235 API Token；导出依赖 `python-docx`（见 `requirements.txt`）。

### 工作流

1. 收集发明点 → `checklist` 补全信息  
2. `patent-search` 检索现有技术 → 填入对比表  
3. 按 `template.md` 撰写正文  
4. `export` 生成 Word  

### 依赖

```bash
pip install -r requirements.txt
```

### 免责声明

可专利性初评仅供参考，不构成法律意见；正式申请须由专利代理人审核。

---

## English

Guides **invention disclosure** drafting: template, checklist, prior-art workflow with **patent-search**, and **Word (.docx) export**.

### Commands

| Command | Purpose |
|---------|---------|
| `template` | Blank disclosure Markdown template |
| `checklist` | Writing checklist |
| `export` | Full Markdown `content` → downloadable `.docx` |

No third-party API token required. Install: `pip install -r requirements.txt`.

### Workflow

1. Gather invention facts → `checklist`  
2. Prior art via **patent-search**  
3. Fill sections from `template.md`  
4. `export` to Word  

Disclaimer: not legal advice; have a patent attorney review before filing.
