# url-guard 钩子模板（0.25）

> **EN**: Host hook template: intercept web fetches at PreToolUse, route content pages through markitdown instead of raw fetch/search-snippet reliance.

## 用途
宿主在 PreToolUse（WebFetch / 网络抓取工具）触发时执行本检查：**内容页 URL 先转 Markdown 再分析**，杜绝"只引搜索摘要不抓源文"（基因 6d258d64 的机制化落地）。

## 规则
| 场景 | 动作 |
|---|---|
| URL 指向内容页（文章/文档/博客） | 提示：先 `python <markitdown-skill 安装目录>/scripts/url_to_markdown.py "<url>"`，对 Markdown 分析 |
| 已知 API/JSON 端点 | 直接取（非内容页） |
| 抓取失败（SPA/登录可见） | 允许降级用摘要，但**报告引用处必须标注「摘要级未核对」** |

## 参考实现（伪代码）
```js
// PreToolUse hook：tool==='WebFetch' 时
const url = toolInput.url;
if (isContentPage(url)) {
  return { decision: 'warn', message: `内容页请先转 Markdown：url_to_markdown.py "${url}"（pi-evox url-guard）` };
}
return { decision: 'allow' };
}
```

## 安装
按宿主钩子机制挂载（OpenClaw/Hermes 见 `docs/advanced.md` 接入契约；通用宿主用 PreToolUse 等效机制）。本模板不含自动抓取——**只提示路由**，抓取动作仍由 agent 显式执行（不静默自治原则）。
