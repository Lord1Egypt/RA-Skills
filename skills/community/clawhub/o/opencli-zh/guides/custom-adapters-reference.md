# Custom Adapters Reference

在需要进一步查自定义适配器细节、排障或阅读 opencli 内部实现时使用本文件。

使用本文件前，默认前提是：用户已经同意进入自定义适配器 / 定向排障流程。涉及 `evaluate`、`intercept`、`tap`、`record` 时，不把它们当作常规浏览手段滥用。

## Pipeline 扩展步骤

除主 guide 中的高频步骤外，还可按需使用：
- `filter`：过滤数据
- `sort`：排序
- `intercept`：网络拦截（installInterceptor / getInterceptedRequests）
- `tap`：Store Action Bridge（Pinia/Vuex 桥接）
- `download`：下载资源
- `wait`：等待固定时间或 DOM 元素

## tap 步骤详解

适用于 Vue + Pinia/Vuex 的网站（如小红书），自动完成：注入 fetch+XHR 双拦截 → 查找 store → 调用 action → 捕获匹配 URL 的响应 → 清理拦截。

| tap 参数 | 必填 | 说明 |
|---------|------|------|
| `store` | ✅ | Pinia store 名称 |
| `action` | ✅ | Store action 方法名 |
| `capture` | ✅ | URL 子串匹配 |
| `args` | ❌ | 传给 action 的参数数组 |
| `select` | ❌ | 从 captured JSON 中提取的路径 |
| `timeout` | ❌ | 超时秒数（默认 5s）|
| `framework` | ❌ | `pinia` 或 `vuex`（默认自动检测）|

## 认证策略

```
fetch(url) 直接能拿到？                     → Tier 1: public         (YAML, browser: false)
页面已登录后，携带站点会话能拿到？           → Tier 2: session        (YAML)
补充站点要求的请求头后能拿到？               → Tier 3: request-header (TS)
都不行，但 Store Action 能触发？              → Tier 4: intercept      (TS/YAML+tap)
无 API，纯 DOM 解析？                         → Tier 5: ui             (TS)
```

## 模板表达式

Pipeline 中可使用 `${{ expression }}` 语法，例如：

```text
${{ args.limit }}
${{ item.title }}
${{ index + 1 }}
${{ item.score > 10 }}
${{ item.active ? 'yes' : 'no' }}
${{ item.title | truncate(30) }}
https://api.com/${{ item.id }}.json
${{ item.subtitle || 'N/A' }}
${{ Math.min(args.limit, 50) }}
```

内置过滤器包括：
- `default`
- `join`
- `upper`
- `lower`
- `trim`
- `truncate`
- `replace`
- `keys`
- `length`
- `first`
- `last`
- `json`
- `slugify`
- `sanitize`
- `ext`
- `basename`

## 配置与路径

可选调试环境变量（非普通使用必需）：
- `OPENCLI_VERBOSE`：启用详细输出
- `OPENCLI_DAEMON_PORT`：Daemon 端口，默认 `19825`
- `OPENCLI_CDP_ENDPOINT`：CDP 直连端点
- `OPENCLI_BROWSER_COMMAND_TIMEOUT`：命令超时，默认 `45` 秒
- `OPENCLI_BROWSER_CONNECT_TIMEOUT`：浏览器连接超时，默认 `30` 秒
- `OPENCLI_BROWSER_EXPLORE_TIMEOUT`：Explore 超时，默认 `120` 秒

相关路径：
- `~/.opencli/clis/`：用户自定义适配器（YAML / TS），持久化写入前须先获用户许可
- `~/.opencli/explore/`：explore 输出产物
- `~/.opencli/record/`：record 捕获产物

## 架构速览

自定义适配器在 opencli 中的大致位置是：
- CLI 层：`opencli <site> <command>` 负责参数解析、命令发现与执行编排。
- 发现层：YAML / TS 适配器均被 discovery 层自动扫描并注册成动态子命令。
- 执行层：YAML 命令进入 pipeline 引擎，TS 命令直接执行 `func`。
- 浏览器层：若适配器依赖浏览器能力，则通过 BrowserBridge 接到 daemon / CDP / Chrome 扩展链路。
- 输出层：结果最终按 table / json / yaml / csv / markdown 等格式渲染。

可以把它理解成：
`YAML/TS adapter → discovery → execution/pipeline → browser bridge（如需）→ output`

## Workspace / 源码定位

若需要进一步读 opencli 源码，优先关注这些目录：
- `src/`：核心入口与编排逻辑
- `src/registry.js`：命令注册与 `cli()` API
- `clis/`：内置适配器定义（YAML / TS）
- `extension/`：Chrome Browser Bridge 扩展

## 常见陷阱

| 陷阱 | 表现 | 解决方案 |
|------|------|---------|
| 缺少 `navigate` | evaluate 报 `Target page context` 错误 | 在 evaluate 前加 `navigate:` 步骤 |
| evaluate 内模板字符串 | backticks 存为 JSON 时会被截断 | 改用字符串拼接或 function-style evaluate |
| 缺少 `strategy: public` | 公开 API 也启动浏览器 | 加上 `strategy: public` + `browser: false` |
| Cookie 过期 | 返回 401 / 空数据 | 在浏览器里重新登录目标站点 |
| YAML 内嵌大段 JS | 调试困难，转义问题 | 超过 10 行 JS 改用 TS adapter |
| 风控被拦截(伪200) | JSON 核心数据是 `""` 空串 | 添加断言，无核心数据升级鉴权 Tier |
| 页面异步加载 | evaluate 拿到空数据 | 增加 `wait` 或在 evaluate 内 polling |
