# 快速开始（QUICKSTART）

5 分钟跑通「**做任务 → 自动记账 → 看提效报告**」闭环。

本文件是 hands-on 实操指南（本地 CLI）。更完整的架构与能力清单见 [README.md](README.md)。

---

## 一、环境要求

- **Python ≥ 3.10**（纯标准库即可跑通核心闭环，**零第三方依赖**）
- **可选**：`python-docx` / `openpyxl` —— 仅当要用 `--format docx/xlsx` 富格式导出时才需要；缺失时自动降级为 `.md` / `.csv`，不影响主流程
- **无需联网、无需密钥、无需 LLM**

---

## 二、五分钟闭环（4 步）

从项目**根目录**运行。Windows / PowerShell 用户用 `.venv\Scripts\python`；mac / Linux 用 `python3`（或先 `source .venv/bin/activate`）。

### 1) 初始化账本（仅首次）

```bash
python scripts/executor.py --init-ledger ledger.json
```

→ 生成 `{"tasks":[]}` 的空账本。之后所有记账都进这个文件。

### 2) 执行一个办公任务（先把活干完，拿到交付物）

```bash
python scripts/executor.py --type 周报生成 --input 本周事件.txt --output 周报.md
```

- 交付物写入 `周报.md`（Markdown）。
- **不写账本、不联网** —— 这一步只负责把任务做成可交付物。

### 3) 确认写回（执行 + 自动记账闭环）

先**预览**（dry-run，安全，不落盘）：

```bash
python scripts/executor.py --type 周报生成 --input 本周事件.txt \
  --apply-ledger ledger.json \
  --skill-tokens 1800 --baseline-tokens 12000 --baseline-minutes 25
```

确认无误后，**真正写回**（加 `--confirm-ledger`）：

```bash
python scripts/executor.py --type 周报生成 --input 本周事件.txt \
  --apply-ledger ledger.json \
  --skill-tokens 1800 --baseline-tokens 12000 --baseline-minutes 25 \
  --confirm-ledger
```

参数说明：

- `--skill-tokens` / `--skill-minutes`：本次用 AI 实际消耗的 Token / 分钟（也可由宿主完成事件自动注入，见步骤 4 之外的 host 钩子）。
- `--baseline-tokens` / `--baseline-minutes`：**你不用本技能、自己手搓 / 反复试错的估计成本**——这就是「省了多少」的基准。**必须提供 baseline 才能写回**（护栏会拦截缺省 baseline，防止空账本出现负节省、污染数据）。
- 不加 `--confirm-ledger` 永远是**预览**；只有显式确认才落盘。

### 4) 看提效报告

```bash
python scripts/report_engine.py ledger.json --format html --output 提效报告.html
```

浏览器打开 `提效报告.html`，即可看到节省 Token / 率 / 趋势等可视化。

> 一句话摘要版：加 `--summary`；Markdown 版：`--format markdown`。

---

## 三、常见任务示例

| 你想做的事 | `--type` | `--input` 给什么 |
|-----------|----------|------------------|
| 写周报 | `周报生成` | 本周要点（每行一条，可带「风险：」「下周计划：」等前缀） |
| 整理会议纪要 | `会议纪要` | 会议转录文本（自动抽结论 / 待办 / 负责人 / 截止） |
| 分析 CSV 数据 | `数据分析` | CSV 文件路径，或直接贴 CSV 文本 |
| 提炼文档要点 | `文档整理` | 一篇长文 |
| 出 PPT 大纲 | `PPT大纲` | 首行写主题，其余每行一个要点 |

每个 `--type` 支持的中英文别名（如 `weekly` / `minutes` / `slides` 等）见 `scripts/executor.py` 的 `_EXEC_ALIASES`。

---

## 四、在对话里直接说（自然语言触发）

如果你是天禧 / OpenClaw 宿主用户，不用碰命令行，直接说：

- 「帮我写一份周报」（贴入本周要点）
- 「整理一下会议纪要」
- 「分析这个 CSV 算关键指标」
- 「把这篇文章提炼成要点」 / 「给这个主题出个 PPT 大纲」
- 「生成我的提效报告」

技能会调 `executor` 生成交付物，并默认走 **dry-run 预览 + 确认写回**，不污染账本。

---

## 五、PowerShell / Windows 注意事项

- **venv 解释器**：`.venv\Scripts\python`（cmd 与 PowerShell 通用）。想先激活环境：
  - PowerShell：`.\.venv\Scripts\Activate.ps1`
  - cmd：`.venv\Scripts\activate`
- **路径分隔符**：反斜杠 `scripts\executor.py` 或正斜杠 `scripts/executor.py` 都行。
- **中文文件名 / 路径**：全部按 utf-8 处理，正常支持。
- **富格式导出**：`--format docx` / `--format xlsx` 需要 `pip install python-docx openpyxl`；缺失时自动降级为同路径 `.md` / `.csv`，不会报错中断。

---

## 六、安全红线（执行层）

- 纯标准库，**不联网、不读密钥、不调 LLM**。
- 内容智能来自你提供的原始内容（模板渲染），数据智能来自本地 stdlib 计算。
- CI 跑**四红线预检**（`scripts/security_preflight.py`）：无危险执行 / 无网络外发 / 无硬编码密钥 / 用户字段转义。
- 写账本**默认 dry-run**，需显式确认才落盘；**绝不**自动删文件 / 发邮件 / 改外部数据。

---

## 七、下一步

- 完整能力清单、目录结构、测试与 CI：见 [README.md](README.md)
