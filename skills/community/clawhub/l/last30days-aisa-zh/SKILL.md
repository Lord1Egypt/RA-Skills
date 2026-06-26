---
name: last30days-zh
version: "1.0.4"
description: "聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket、GitHub 和 web search 结果。触发条件：当用户需要 recent social research、人物近况、公司动态、竞品对比、发布反应、趋势扫描时使用。支持 AISA 规划、聚类、重排和 JSON 输出。"
argument-hint: "last30days OpenAI Agents SDK, last30days Peter Steinberger, last30days OpenClaw vs Codex"
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
homepage: https://github.com/AIsa-team/agent-skills
repository: https://github.com/AIsa-team/agent-skills
author: mvanhorn
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "📰"
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
        - bash
    primaryEnv: AISA_API_KEY
    files:
      - "scripts/*"
---

# last30days 中文版

聚合最近 30 天的社交平台、社区论坛、预测市场、GitHub 和 grounded web 结果，再合成为一份研究简报。

## 触发条件

- 当用户需要最近 30 天的人物、公司、产品、市场、工具或趋势研究时使用。
- 当用户需要竞品对比、发布反应、社区情绪、近期动态总结时使用。
- 当用户需要结构化 JSON 输出，例如 `query_plan`、`ranked_candidates`、`clusters`、`items_by_source` 时使用。

## 不适用场景

- 不适合纯百科类、没有时效要求的问题。
- 不适合只想看单一官方来源、完全不需要社区和社交信号的场景。

## 能力

- 通过 AISA 提供规划、重排、综合、grounded web search、X/Twitter、YouTube 和 Polymarket。
- Reddit 和 Hacker News 走公开路径。
- GitHub 走官方 GitHub API，按需使用 `GH_TOKEN` 或 `GITHUB_TOKEN`。
- TikTok、Instagram、Threads、Pinterest 在启用时走托管发现路径。

## 环境要求

- 主凭证：`AISA_API_KEY`
- 可选 GitHub：`GH_TOKEN` 或 `GITHUB_TOKEN`
- Python `3.12+`

```bash
for py in /usr/local/python3.12/bin/python3.12 python3.14 python3.13 python3.12 python3; do
  command -v "$py" >/dev/null 2>&1 || continue
  "$py" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' || continue
  LAST30DAYS_PYTHON="$py"
  break
done
```

## 快速命令

```bash
bash "${SKILL_ROOT}/scripts/run-last30days.sh" "$ARGUMENTS" --emit=compact
"${LAST30DAYS_PYTHON}" "${SKILL_ROOT}/scripts/last30days.py" "$ARGUMENTS" --emit=json
"${LAST30DAYS_PYTHON}" "${SKILL_ROOT}/scripts/last30days.py" "$ARGUMENTS" --quick
"${LAST30DAYS_PYTHON}" "${SKILL_ROOT}/scripts/last30days.py" "$ARGUMENTS" --deep
"${LAST30DAYS_PYTHON}" "${SKILL_ROOT}/scripts/last30days.py" --diagnose
```

## 示例

- `last30days OpenAI Agents SDK`
- `last30days Peter Steinberger`
- `last30days OpenClaw vs Codex`
- `last30days Kanye West --quick`

