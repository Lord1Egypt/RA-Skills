# Multi-Search-CN 参考

## 设计取舍

| 方式 | 说明 |
|------|------|
| **DuckDuckGo HTML** | 无 API Key、纯 Python3 标准库可解析 `result__a`，对中文设 `kl=cn-zh` |
| **必应/百度/搜狗/360 直达链接** | 仅生成搜索 URL；**不保证**用 curl 能解析正文（风控/JS/验证码） |

## 依赖

- Python 3.8+（无第三方包）

## 与 OpenClaw / 小爪

在 Ubuntu 上（`openclaw` 所在机器）可直接：

```bash
python3 /path/to/multi-search-cn/scripts/search_cn.py "你的关键词"
```

若需飞书/定时任务里调用，注意频率，避免对搜索引擎造成过高请求。

## 故障排查

1. **DDG 无结果**：升级脚本；检查网络；换 `--urls-only` 用浏览器打开各引擎。
2. **企业网络拦截**：代理环境下再试。
3. **合规**：遵守各搜索引擎 robots/服务条款；本 Skill 面向个人研究与自动化辅助，非批量抓取。
