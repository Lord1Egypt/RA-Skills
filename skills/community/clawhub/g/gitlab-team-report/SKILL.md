---
name: gitlab-weekly-report
description: |
  生成 GitLab 团队周报，支持按产品功能分类 MR、按成员和仓库汇总贡献、输出 Markdown/HTML、生成图表和历史周报首页，并可选上传到飞书文档。用于用户提到“GitLab 周报”“团队周报”“统计本周 MR/commit”“按功能归类开发工作”“生成 HTML 周报”“上传周报到飞书”等场景。 Generate GitLab weekly team reports with MR categorization, contributor and repository summaries, Markdown/HTML output, charts, historical report index pages, and optional Feishu publishing. Use when users ask for “GitLab weekly report”, “team engineering summary”, “summarize merge requests and commits”, “group work by product area”, “generate an HTML report”, or “publish the report to Feishu”.
---

# GitLab Weekly Report Generator

生成适合团队复盘、周会同步和对外汇报的 GitLab 周报。

## 执行流程

1. 读取 `config/config.json`；如果不存在，先从 `config/config.example.json` 复制一份再填写。
2. 运行 `scripts/generate-report.sh` 生成周报主文件。
3. 如需图表，运行 `scripts/generate-charts.py`；如果环境缺少 `matplotlib`，接受 Mermaid 回退方案。
4. 如需发布到飞书，使用 `scripts/upload-to-feishu.sh` 或 `scripts/upload-to-feishu.js`。
5. 优先修改配置和分类规则，不要直接改业务脚本，除非需求本身变了。

## 主要能力

- 按 **一级分类 → 二级分类 → MR** 组织产品功能周报
- 按 **人 → repo** 汇总 MR、commit、贡献摘要
- 输出 `weekly_report.md` 与 `weekly_report.html`
- 生成 `stats.json`、图表和 `reports/index.html`
- 保持 Markdown 尽量兼容飞书文档
- 为 MR 和成员附上 GitLab 链接
- 支持“规则优先 + 启发式补全”的分类方式

## 关键文件

- `scripts/generate-report.sh`：命令入口
- `scripts/generate-report.py`：主逻辑
- `scripts/generate-charts.py`：图表生成
- `scripts/upload-to-feishu.sh` / `scripts/upload-to-feishu.js`：飞书上传
- `config/config.example.json`：配置示例
- `config/classification.rules.example.json`：分类规则示例
- `templates/report.template.md`：报告模板

## 配置方式

优先使用以下文件：

- `config/config.json`
- `config/classification.rules.json`

如果规则文件不存在，就从对应的 `*.example.json` 复制后再修改。

优先调整顺序：

1. `repo_rules`：适合仓库名、路径、项目归属明显的场景
2. `keyword_rules`：适合 title / label / branch 关键词补充判断
3. `default_category`：兜底分类

## 基本用法

```bash
cd /path/to/gitlab-weekly-report

cp config/config.example.json config/config.json
cp config/classification.rules.example.json config/classification.rules.json

./scripts/generate-report.sh \
  -c config/config.json \
  -s 2026-03-14 \
  -e 2026-03-19
```

可选参数：

| 参数 | 说明 |
|---|---|
| `-c, --config` | 配置文件 |
| `-s, --start-date` | 开始日期 |
| `-e, --end-date` | 结束日期 |
| `-o, --output` | 输出目录 |
| `--no-charts` | 跳过图表生成 |

## 典型输出

```text
reports/
├── index.html
├── latest -> 2026-03-14_to_2026-03-19/
└── 2026-03-14_to_2026-03-19/
    ├── weekly_report.md
    ├── weekly_report.html
    ├── stats.json
    └── charts/
```

## 依赖

必需：
- `python3`
- `jq`

推荐：
- `matplotlib`
- `pandas`
- `requests`

安装：

```bash
pip3 install -r requirements.txt
```

## 注意事项

- 保持 `SKILL.md` 聚焦流程和决策，不要把大段样例配置塞进来。
- 优先通过配置和规则文件调整分类结果。
- 接受图表回退到 Mermaid 的情况，不要因为缺少 `matplotlib` 阻塞周报生成。
- 飞书上传依赖本地配置和权限；发布 skill 时不要分发真实 token 或私有配置文件。
