# scrapers/ — 国内房源平台扫描模板

参考 [career-ops](https://github.com/career-ops-hq/career-ops) 的 `providers/` 模式：**一个平台一个模块**，文件系统即注册表，零依赖、零 token。

## 职责边界

每个非 `_` 前缀的 `*.mjs` 模块回答三个问题（也是它能可靠回答的全部）：

1. **这个 URL 是不是我的平台？**（`detect()`：域名与路径语法 → 页面类型/城市码/房源 ID）
2. **AI 在这个平台的页面上该提取什么？**（`fields`：字段清单，scan 模式逐项抓取）
3. **这个平台的成交价去哪找、可信到什么档位？**（`transaction` + `notes`）

**页面抓取本身不在这里做**——house-ops 的抓取由 AI 通过 WebFetch 按字段清单完成，模块只负责 URL 语法与清单，不写会过时的 DOM 选择器。确定性归一化与交叉验证在 [`../scripts/scan.mjs`](../scripts/scan.mjs)。

## 加载与路由（`_registry.mjs`）

1. 每个非 `_` 前缀的 `*.mjs` 按文件名字母序动态加载（detect 优先级因此确定）；
2. `detect()` 首个命中即胜出；坏模块（形状不对、id 重复、import 报错）打警告跳过，绝不 fatal；
3. `_` 前缀是共享工具，永远不被当作平台加载：`_registry.mjs`（加载/路由）、`_fields.mjs`（字段契约与价格归一化）、`_ke-group.mjs`（链家/贝壳共用工厂）。

## 当前平台

| 模块 | 平台 | 成交明细 |
|---|---|---|
| `beike.mjs` | 贝壳找房（ke.com） | ✅ `/chengjiao/`（成交数据档） |
| `lianjia.mjs` | 链家（lianjia.com） | ✅ `/chengjiao/`（成交数据档） |
| `anjuke.mjs` | 安居客（anjuke.com） | ❌ 仅估算行情（挂牌数据档封顶） |
| `5i5j.mjs` | 我爱我家（5i5j.com） | ❌（挂牌数据档封顶） |
| `fang.mjs` | 房天下（fang.com） | ❌（挂牌数据档封顶） |

未识别平台走 `generic` 兜底清单（`scripts/scan.mjs` 内置）。

## 新增平台

读 [**ADDING_A_PLATFORM.md**](ADDING_A_PLATFORM.md)——模块契约、`detect()` 容错要求、字段清单纪律、测试清单。政务公开数据源（交叉验证用）不在这里加，去 [`templates/official-sources.cn.yml`](../templates/official-sources.cn.yml)。
