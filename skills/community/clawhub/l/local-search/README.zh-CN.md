# local-search

> **语言**：[English](./README.md) · [简体中文](./README.zh-CN.md)

[![ClawHub](https://img.shields.io/badge/ClawHub-%40Sakurakilove%2Flocal--search-red?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6eiIvPjwvc3ZnPg==)](https://clawhub.ai/@Sakurakilove/local-search)
[![Version](https://img.shields.io/badge/version-1.6.2-blue)](https://github.com/Sakurakilove/local-search/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Node](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-blue.svg?logo=typescript)](https://www.typescriptlang.org/)
[![GitHub stars](https://img.shields.io/github/stars/Sakurakilove/local-search?style=social)](https://github.com/Sakurakilove/local-search)
[![GitHub last commit](https://img.shields.io/github/last-commit/Sakurakilove/local-search)](https://github.com/Sakurakilove/local-search/commits/main)

完全在用户本机运行的网页搜索 skill。直接通过 HTTP 抓取 **DuckDuckGo / Bing / Google** 的公开搜索结果页（SERP），并在某个引擎被限流或不可达时自动切换到下一个。

每条结果是一个 `SearchFunctionResultItem`，包含 `url`、`name`、`snippet`、`host_name`、`rank`、`date`、`favicon` 七个标准字段，外加三个扩展字段：`source_engine`、`raw_html`、`score`。

## 快速开始

**一键安装**（ClawHub CLI）：

```bash
npx clawhub install @Sakurakilove/local-search
```

**手动安装**（clone 本仓库）：

```bash
# 1. 安装唯一的运行时依赖
cd local-search
npm install           # 或：bun install

# 2. 跑示例
tsx scripts/web_search.ts

# 3. 或直接用 CLI
tsx bin/web-search.ts "人工智能" --num 5
tsx bin/web-search.ts "AI 新闻" --recency-days 1 --json -o ai_news.json
```

## 为什么用它？

- **无需 API Key** —— 直接调用公开搜索引擎。
- **没有中间跳板** —— 你的机器 → 搜索引擎，之间没有任何云服务。
- **完全透明** —— 每条结果都带 `source_engine` 字段，你能看到是哪个引擎回答的。
- **健壮容错** —— DDG 限流时，编排器自动切到 Bing。Google 已从 auto 链路移除（数据中心 IP 几乎都返回 enablejs 墙）；如需 Google，请显式传 `--engine google`。
- **Locale 自动识别** —— 根据查询文本自动选择 locale（CJK → zh-CN，假名 → ja-JP，韩文 → ko-KR，西里尔 → ru-RU 等；拉丁/默认 → en-US）。可用 `--locale <BCP-47>` 覆盖。对非英文查询至关重要 —— Bing 的 `ensearch=1`（强制英文 SERP）对 CJK 查询会返回垃圾结果，所以只在英文 locale 下才设。

## 文件结构

```
local-search/
├── SKILL.md             # 完整文档（先读这个）
├── package.json         # 声明 cheerio 为唯一运行时依赖
├── tsconfig.json
├── LICENSE.txt
├── bin/
│   └── web-search.ts    # CLI 入口：tsx bin/web-search.ts <query> [opts]
├── src/
│   ├── index.ts         # SDK 导出
│   ├── search.ts        # 带 auto-fallback 的编排器
│   ├── types.ts         # SearchFunctionResultItem + 选项
│   └── engines/
│       ├── _shared.ts   # fetch / 解析辅助
│       ├── duckduckgo.ts
│       ├── bing.ts
│       ├── google.ts
│       └── index.ts     # 引擎注册表 + AUTO_ENGINE_ORDER
└── scripts/
    └── web_search.ts    # 快速开始示例
```

## 编程式调用

```typescript
import { search } from "local-search";

const outcome = await search("法国的首都是哪里？", { num: 5 });
if (outcome.success) {
  console.log(`引擎：${outcome.engine}（耗时 ${outcome.elapsedMs}ms）`);
  for (const item of outcome.results) {
    console.log(`- ${item.name}\n  ${item.url}\n  ${item.snippet}\n`);
  }
} else {
  console.error(outcome.error);
}
```

## CLI 用法

```bash
tsx bin/web-search.ts <query> [options]

Options:
  --num, -n <N>          结果数量（默认 10）
  --engine, -e <id>      duckduckgo | bing | google | auto（默认 auto）
  --recency-days, -r <N> 限制为最近 N 天内的结果
  --locale <BCP-47>      结果语言/地区，如 en-US（默认）、zh-CN、ja-JP
  --timeout <ms>         单引擎超时（默认 8000ms）
  --json                  输出 JSON
  --output, -o <path>    将 JSON 写入文件
  --quiet, -q            隐藏 banner
  --help, -h             显示帮助
```

## 引擎对比

| 引擎 | 端点 | 需要 Key | 住宅 IP | 数据中心 IP | 时间过滤 |
|---|---|---|---|---|---|
| DuckDuckGo | `https://html.duckduckgo.com/html/`（GET） | 否 | 高 | 中（负载高时限流） | `df=d<N>`（精确天数） |
| Bing | `https://www.bing.com/search` | 否 | 高 | 高 | `freshness=d1\|w1\|m1`（分桶） |
| Google | `https://www.google.com/search` | 否 | 中 | 低（enablejs 墙） | `tbs=qdr:d\|w\|m\|y`（分桶） |

`engine: "auto"`（默认）会按 **DuckDuckGo → Bing → Google** 的顺序尝试，返回第一个非空结果集。数据中心 IP 的实际链路通常是 DDG → Bing（Google 通常被墙）；住宅 IP 三个引擎都能用。

引擎顺序可在 `src/engines/index.ts` 的 `AUTO_ENGINE_ORDER` 中调整。

## 验证安装

`npm install` 之后跑一遍端到端测试，确认你的网络下一切正常：

```bash
tsx scripts/test.ts
```

预期输出：8 个测试全部通过。即使你的 IP 被 DDG 限流，测试也会通过 —— auto 模式会自动切到 Bing，测试套件里的 Test 6 专门验证了这条 fallback 路径。

## 致谢

结果 schema 与 skill 结构受 [`z-ai-web-dev-sdk`](https://www.npmjs.com/package/z-ai-web-dev-sdk) 的 `web-search` skill 启发。该项目的 MIT 设计塑造了本仓库使用的 `SearchFunctionResultItem` 结构；所有引擎后端代码均为原创。

## 许可证

MIT。详见 [`LICENSE.txt`](./LICENSE.txt)。
