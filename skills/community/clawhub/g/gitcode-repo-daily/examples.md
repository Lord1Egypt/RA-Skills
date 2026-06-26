# GitCode 仓库运营报表 — 使用示例

> 以下示例展示用户如何与Agent对话来触发此 skill，以及Agent在幕后执行的命令。

---

## Example 1: 生成今日日报

**用户**：帮我生成 owner/repo1 和 owner/repo2 的今日日报

**执行流程**：

```bash
# 1. 生成报表数据（自动写入 temp_dir/report.json）
python <SKILL_ROOT>/scripts/generate_daily_report.py

# 2. 读取 report.json，生成摘要，写入 temp_dir/summaries.json

# 3. 渲染日报 Markdown（自动保存摘要到 DB）
python <SKILL_ROOT>/scripts/generate_daily_report.py --render --output daily_2026-03-10.md
```

**输出效果**（固定格式，输出一致）：

```
📊 开源代码仓库运营日报
├── 一、仓库概览（指标总览表 + 全局摘要）
├── 二、分仓详情
│   ├── 📦 owner/repo
│   │   ├── Star/Fork/PR/Issue 指标
│   │   ├── 🔀 当日合并 PR（可点击链接）
│   │   ├── 🆕 当日新开 PR
│   │   ├── 📌 当日新增 Issue（可点击链接）
│   │   ├── ✅ 当日关闭 Issue
│   │   ├── 🔥 热门 Issue（评论较多）
│   │   └── 💬 该仓小结
│   └── 📦 owner/repo（同上结构）
└── 三、行动建议（自动识别陈旧 Issue/PR、热门 Issue、重大 PR）
```

---

## Example 2: 生成指定日期的日报

**用户**：生成 3 月 8 日的日报

```bash
python <SKILL_ROOT>/scripts/generate_daily_report.py --date 2026-03-08
# ... 后续摘要 + 渲染同上
python <SKILL_ROOT>/scripts/generate_daily_report.py --render --output daily_2026-03-08.md
```

---

## Example 3: 首次使用 — 配置仓库

**用户**：帮我生成 owner/repo 的日报

Agent会通过脚本将仓库写入 `config.json`：

```json
{
  "repos": ["owner/repo"],
  "timezone": "Asia/Shanghai"
}
```

后续生成报表时无需再次指定仓库。

---

## Example 4: 查看支持的所有参数

```bash
python <SKILL_ROOT>/scripts/generate_daily_report.py --help
```

主要参数：

| 参数 | 说明 |
|------|------|
| `--type day` | 报表类型，默认 day（日报） |
| `--date YYYY-MM-DD` | 报表日期，默认今日 |
| `--repos "owner/repo,..."` | 仓库列表（可选，传了会用于本次并写入 config） |
| `--render --output PATH` | 渲染报表到 Markdown 文件（同时自动保存摘要到 DB） |
| `--save-summaries` | 单独将摘要写入 DB（`--render` 已包含此操作，通常无需单独调用） |
| `--template PATH` | 自定义模板路径（留空自动选择 daily_report.md） |

---

## 前置条件

1. **Python 3.7+**（标准库即可，无需 pip install）
2. **GITCODE_TOKEN** 环境变量已配置（日报必须）
3. `config.json` 中配置了 `repos` 列表，或在对话中指定仓库
