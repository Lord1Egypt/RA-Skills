# 网络请求修改器

> 通过 Chrome DevTools Protocol 实时观察和修改浏览器网络请求/响应，无需安装浏览器插件。

一个 [Crush](https://crush.sh) skill。

## 功能

- **监控** HTTP 流量，JSONL 格式实时输出，支持 URL/类型过滤
- **拦截** 请求（分析统计、追踪脚本、广告），阻止发往服务器
- **Mock** API 响应，返回自定义 JSON
- **修改** 请求/响应 Header、URL、Cookie、Query 参数和 Body
- **注入** 脚本或 HTML 到页面
- 25 种匹配条件 + 17 种修改动作，覆盖请求和响应阶段

## 安装

```bash
npx skills add 241x/network-request-twister
```

## 使用

安装后，向 AI 助手说以下内容即可触发：

```
「帮我看看这个页面发了什么请求」
「把页面上所有发往 analytics 的请求屏蔽掉」
「把 /api/users 的返回值改成自定义 JSON」
「给所有 API 请求加上 Authorization Header」
「把 URL 里的 UTM 追踪参数去掉」
```

详细文档见 [SKILL.md](SKILL.md)，配置模板见 `examples/` 目录。
