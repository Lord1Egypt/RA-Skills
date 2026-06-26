# Jira Issue Fetcher (Skill 内置)

用于查询 Jira 问题与下载附件。该脚本已迁移到 Skill 目录，不再放在项目内。

## 目录

`~/.cursor/skills/jira-issue-analyzer/jira`

## 使用前准备（必须使用 venv）

```bash
cd ~/.cursor/skills/jira-issue-analyzer/jira
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env`：

```env
JIRA_BASE_URL=http://jira.banya.com.cn
JIRA_TOKEN=your_personal_access_token_here
```

## 命令示例

```bash
.venv/bin/python main.py --test
.venv/bin/python main.py get PI2506-150 -f json
.venv/bin/python main.py download PI2506-150 -d /tmp/jira_PI2506-150
```
