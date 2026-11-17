# Infoseek 网络边界受限清单（GA12）

> 生成时间：2026-09-16 15:16:53｜ 边界门控：OFF（默认，零行为变更）
> 定位：声明式网络边界台账 + host 实测证据；**不绕过网络边界，不把受限能力伪装为可用**。
> 用法：目标机重跑 `python scripts/boundary_gate.py --report --force` 刷新，形成「沙箱 vs 目标机」对照。

## 1. 能力边界声明

| 能力 | 边界 | 依赖 host |
|---|---|---|
| AccountTrustScorer | local | — |
| AgentKey | open | — |
| FakeDetect | local | — |
| L2Renderer | open | — |
| L4Transcribe | sandbox_restricted | storage.googleapis.com, r.jina.ai |
| Maigret | open | — |
| PatentLookup | sandbox_restricted | patents.google.com, github.com |
| PublicApisCatalog | local | — |
| QVeris | open | qveris.ai, qveris.cn |
| Sherlock | open | — |
| WikiVerify | sandbox_restricted | www.wikidata.org, query.wikidata.org, en.wikipedia.org, zh.wikipedia.org |
| manual_review | local | — |

## 2. Host 实测台账

| Host | 静态边界 | 实测 | 证据 | 消费能力 |
|---|---|---|---|---|
| api.wikimedia.org | sandbox_restricted | ❌ 不可达 | core/v1 REST 不可达（2026-09 实测） | — |
| commons.wikimedia.org | sandbox_restricted | ❌ 不可达 | Wikimedia 全系 https 黑洞（2026-09 实测） | — |
| en.wikipedia.org | sandbox_restricted | ❌ 不可达 | 解析到污染段（31.13.x FB 段），https 不可达（2026-09 实测） | WikiVerify |
| github.com | sandbox_restricted | ❌ 不可达 | git clone/大文件 release 资产传输不可达（~37KB/s 或超时）；API/Contents 另见 api.github.com | PatentLookup |
| patents.google.com | sandbox_restricted | ❌ 不可达 | SPA 需 JS，静态抓取返回 'Resource does not exist.'（2026-09 实测） | PatentLookup |
| query.wikidata.org | sandbox_restricted | ❌ 不可达 | SPARQL 端点 https 黑洞，20s 超时（2026-09 实测） | WikiVerify |
| qveris.ai | （未登记） | ❌ 不可达 |  | — |
| qveris.cn | （未登记） | ❌ 不可达 |  | — |
| r.jina.ai | sandbox_restricted | ❌ 不可达 | Errno 101 连接不可达（2026-09 L2 引擎实测） | L4Transcribe |
| storage.googleapis.com | sandbox_restricted | ❌ 不可达 | 大文件传输 ~37KB/s 或超时（2026-09 实测） | L4Transcribe |
| upload.wikimedia.org | sandbox_restricted | ❌ 不可达 | Wikimedia 全系 https 黑洞（2026-09 实测） | — |
| www.wikidata.org | sandbox_restricted | ❌ 不可达 | DNS 可解析但返回污染 IP（103.102.166.224）；http 301 / https SSL 握手失败（2026-09 实测） | WikiVerify |
| zh.wikipedia.org | sandbox_restricted | ❌ 不可达 | 同 en.wikipedia.org，污染段不可达（2026-09 实测） | WikiVerify |

**实测汇总**：不可达 13 个 ｜ 可达 0 个

## 3. 受限能力降级路径

门控开启后，受限能力的执行请求沿注册表 `degrade_to` 链显式降级（默认末端 `manual_review`），
并在代偿 trail 中以 `boundary_restricted` 留痕，绝不静默失败或长超时。

## 4. 边界原则

1. 不尝试绕过网络限制（无代理/VPN/反爬对抗）；
2. 不将受限项标记为「通过」（沙箱仅做负向验证，正向可达性由目标机补验）；
3. 不改动既有能力默认开关语义（仅新增声明与门控，门控默认 OFF）。
