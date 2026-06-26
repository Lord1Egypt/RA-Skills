---
name: kimi-web-search
description: 通过 Kimi API 的 builtin_function $web_search 联网检索。用于新闻、实时信息、股价、公司动态等时效性内容；支持中英检索。先判断用户要「原始搜索结果条目」还是「综合总结」（默认总结），再调用脚本或相应参数。
---

# Kimi 联网搜索

用 Kimi 内置工具 `$web_search` 检索互联网最新信息。

## 前置准备

在调用脚本前，您需要在 Moonshot 开放平台申请 **API Key**。
https://platform.moonshot.cn/

请将 API Key 配置在系统的环境变量中。脚本会自动读取该变量（亦支持 `KIMI_API_KEY`）：

```bash
# Linux / macOS
export MOONSHOT_API_KEY="your_api_key_here"

# Windows (CMD)
set MOONSHOT_API_KEY="your_api_key_here"
```

## 意图识别（先做这个）

| 用户意图 | 表现 | 调用方式 |
|---------|------|----------|
| **总结**（默认） | 要结论、分析、简报、「帮我查一下并说明」 | `search(query)` 或 `python3 scripts/kimi_search.py -q "..."`，**不要**加 `--raw` |
| **原始结果** | 要来源列表、逐条链接、摘录、引用、材料汇总、不要一句话概括 | `search(query, raw_output=True)` 或 `python3 scripts/kimi_search.py -q "..." --raw` |

未明确说「要原文/链接/逐条」时，按 **总结** 处理。

## 前置条件

依赖：

```bash
pip install openai httpx
```

密钥（任选其一）：

- 环境变量：`MOONSHOT_API_KEY` 或 `KIMI_API_KEY`
- 文件：`~/.config/moonshot/api_key` 或 `~/.openclaw/credentials/moonshot-api-key`

申请地址：https://platform.moonshot.cn/

## 用法

在 skill 根目录下执行（`scripts/kimi_search.py` 相对该目录）：

**总结（默认）**

```bash
python3 scripts/kimi_search.py -q "你的检索问题"
```

**原始搜索结果条目**

```bash
python3 scripts/kimi_search.py -q "你的检索问题" --raw
```

**Python**（当前工作目录为 `scripts` 时）

```python
from kimi_search import search

print(search("快手 最新财报"))
print(search("某主题", raw_output=True))
```

## 行为说明

- **总结**：系统提示为总结，模型在联网后给出综合回答与引用。
- **原始**：工具往返后会把系统提示换为中文严格格式，要求逐条输出 Title / Date / URL / Summary，禁止一句话概括；`temperature=0.3`。
- 模型默认 `kimi-k2-turbo-preview`，`max_tokens=8192`，`thinking` 关闭。

## 故障排查

连接或 SSL：检查网络；可用 `curl https://api.moonshot.cn/v1/models -H "Authorization: Bearer $MOONSHOT_API_KEY"` 测通。

鉴权失败：在控制台核对密钥是否有效。

限流：间隔重试或缓存重复查询。

## 许可

MIT
