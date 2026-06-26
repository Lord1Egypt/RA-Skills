---
name: kimi-websearch
description: "联网搜索工具。Use When (1)用户需要通过联网获取信息; (2)如果你无法直接回答用户的问题，或者需要更多信息来回答用户的问题。"
metadata:
  openclaw:
    emoji: 🔍
    requires:
      env:
        - KIMI_API_KEY
        - MOONSHOT_API_KEY
    primaryEnv: MOONSHOT_API_KEY
    dependencies:
      - name: openai
        type: pip
        version: ">=1.0.0"
---

# Kimi Web Search / Kimi 联网搜索工具

## Requirements

通过设置环境变量 `KIMI_API_KEY` 或 `MOONSHOT_API_KEY` 来提供 Kimi/Moonshot API 密钥。

如果没有设置，请登录 [Moonshot API Keys](https://platform.moonshot.cn/console/api-keys) 获取 API Key，并将其设置为环境变量。

## 执行流程

1. 先把用户请求整理成适合搜索的单条问题，尽量具体，避免模糊描述。
2. 按照 [联网搜索脚本](#联网搜索脚本) 的说明调用脚本进行联网搜索，获取最新的网络信息来回答用户的问题。
3. 把结果按照[输出要求](#输出要求)进行整理后输出给用户。

## 脚本说明

> ⚠️ 注意: 如果当前环境使用 uv ，则优先使用 `uv run xxx.py` 来执行脚本；如果没有 uv ，则使用 `python3 xxx.py` 来执行脚本。

### 联网搜索脚本

```bash
# 通过 Kimi API 进行联网搜索，获取最新的网络信息来回答用户的问题。
python3 {baseDir}/scripts/web_search.py "<the question you want to ask>"

# 当遇到错误的时候，可以获取帮助
python3 {baseDir}/scripts/web_search.py --help
```

## 输出要求

- **必须**提供给用户消息来源的url，确保信息的准确性，例如

  ```markdown
  1. 新闻内容xxxx
     消息来源：[xxx](https://www.example.com)
  ```

- 如果没有明确的搜索主题，例如“今天的新闻”，可以参考以下分类整理后输出给用户：

```markdown
📰 今日要闻
🇨🇳 国内
🌍 国际焦点
📈 财经资讯
💻 科技动态
```

- 优先输出整理后的结论，不要把整段原始脚本输出原封不动贴给用户。
- 如果搜索结果明显不完整、存在时效风险，直接说明不足。
- 如果用户要求继续追问同一主题，直接换一个搜索参数重新运行。
