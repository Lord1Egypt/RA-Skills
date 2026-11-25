# 版本口径标准（单一数据源）

> 本文件是 Pi × EvoX 对上游依赖的**唯一版本口径表**（0.43 O02 建立，C77 判据锚点）。
> 所有文档引用上游版本号时以本表为准；**历史发布记录**（README 逐版发布记录、旧版 changelog、
> 已发布版本的 changelog/Release body）中的版本号为当时快照，按「已发布只读冻结」纪律不回改。
> 判据：C77（跨文档版本口径对靶，读取 `_docs_meta_0430.json`；数据源见下表）。

## 一、三轴定义与当前值

| 轴 | 含义 | 当前值 | 数据源 |
|---|---|---|---|
| **锁定依赖版本** | `package.json` `optionalDependencies` 固定值；仅主动安装可选集成时生效；A/B 主流程零 npm 依赖 | pi `0.74.2` / evolver `2.0.30` | `package.json`（生成器直读） |
| **上游实测版本** | 每版开发前 C42 双源核对（dist-tags.latest + versions.time）实测的最新版；仅用于兼容性评估与最低运行说明，**不是本项目安装的版本** | pi `1.5.2`（2026-11-10 发布）/ evolver `2.0.51`（2026-11-12 发布）；0.42 检查时点 2026-11-15 | `docs/overview.md` 的 `upstream=pi@…` meta 注释（生成器 L15 提取）+ `_upstream_check_04XX.md` 留痕 |
| **最低运行版本** | 上游各自 `engines` 声明（C42 tarball 契约探针实测，不凭版本号推断） | pi 1.5.2 → Node `>=22.19.0`；evolver 2.0.51 → Node `^22.13.0 \|\| >=23.4.0`；默认 light 后端 → Node `>=22` | 上游 npm `engines` 字段 |

## 二、引用规则

1. 文档陈述「锁定依赖 / optionalDependencies」→ 用**锁定轴**值，不得混入实测值
2. 文档陈述「上游最新 / C42 实测」→ 用**实测轴**值（必要时附时点）
3. 文档陈述「最低运行要求 / engines」→ 用**最低运行轴**值
4. 三轴值变更顺序：先改数据源（package.json / overview meta / 本表），生成器对靶随动；**禁止只改文档不改数据源**
5. 跨文档版本号出现处对靶：中文行与 EN 行**逐一成对校验**（0.42 实证：EN 行可单独滞后）

## 二a、国内镜像检查等价写法（0.43 O05）

- **用户侧版本检查**（国内网络）：
  `npm view @earendil-works/pi-coding-agent version --registry=https://registry.npmmirror.com`
  `npm view @evomap/evolver version --registry=https://registry.npmmirror.com`
- **可选集成安装**（国内网络）：先 `npm config set registry https://registry.npmmirror.com` 再 `npm install`，装完可还原 registry
- **同步延迟**：npmmirror 与官方 registry 通常分钟级同步；**C42 双源核对以官方 registry 为准**（`dist-tags.latest` + `versions.time`），npmmirror 结果仅作国内可达性参考，不作为实测轴数据源

## 三、语义不可混用的背景

- 锁定轴是「本项目实际安装基线」；实测轴是「上游演进观察」——两者语义不同、互不覆盖（详见 `docs/faq.md` Q16）。
- 历史漏采教训（0.42 upstream check §2）：0.40 时点实测记为 pi 1.5.1 / evolver 2.0.50，实为漏采
  （pi 1.5.2 发布于该检查前 20 分钟）；0.42 起强制双源交叉核对（C60）。
- **本表当前值与 0.42 发布口径一致（pi 1.5.2 / evolver 2.0.51）**；0.43 开发启动时 C42 须重跑，
  若上游有新版，更新本表实测轴 + overview meta，再同步全部引用处。

> **EN — Version Standards (single source of truth)**: This file is the only version reference for upstream dependencies. Three axes must never be conflated — (1) **Locked dependency versions** are the exact `optionalDependencies` pins in `package.json` (pi `0.74.2` / evolver `2.0.30`); they are the optional-integration compatibility baseline, and the A/B main flows run with zero npm dependencies. (2) **Upstream-checked versions** are the latest releases measured at each version's C42 dual-source check (pi `1.5.2` / evolver `2.0.51`); these are for compatibility assessment and minimum-runtime notes only, NOT what this project installs. (3) **Minimum runtime** comes from each upstream's `engines` field (pi 1.5.2 -> Node >=22.19.0; evolver 2.0.51 -> Node ^22.13.0 or >=23.4.0; the default light backend only needs Node >=22). Every cross-document version statement must point to the matching axis; historical release records stay frozen at their point-in-time snapshots. Domestic mirror hints (`npmmirror`) are reachability aids only — C42 dual-source checks always use the official registry.
