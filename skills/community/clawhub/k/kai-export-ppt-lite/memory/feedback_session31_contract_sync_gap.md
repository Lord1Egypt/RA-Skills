# Session 31：slide-creator contract/reference 只落了 minimal path，必须升级为可同步 contract pipeline

日期：2026-04-23

## 这轮确认的事实

用户明确指出一个关键矛盾：

- `slide-creator` 和 `kai-export-ppt-lite` 属于同一套 skill 生态
- 既然上游 reference / preset / 中间层都掌握在自己手里，exporter 继续大量靠 heuristic 猜组件，效果差就说不过去

核查后的结论是：这个判断是对的。

## 已经落地的部分

Session 30 方案不是完全没做，以下基础设施已经进代码：

1. `ExportHints` schema
   - `contracts/export_hints.schema.json`

2. vendored preset contracts
   - `contracts/slide_creator/presets/blue-sky.json`
   - `contracts/slide_creator/presets/enterprise-dark.json`
   - `contracts/slide_creator/presets/swiss-modern.json`

3. producer-aware minimal path
   - `detect_producer()`
   - `validate_export_hints()`
   - `collect_export_context()`
   - contract resolve / validate

4. runtime 边界
   - 运行时不跨仓库读取 `slide-creator`
   - 运行时只消费当前 HTML / sidecar / vendored contracts

## 没有真正打通的部分

真正决定导出质量的主链路还没落地：

1. **没有 contract sync pipeline**
   - 当前 preset contracts 是手工/半手工落到 repo 的静态文件
   - 没有同步脚本
   - 没有 upstream version manifest
   - 没有“上游更新后自动重读并再生成 contract”的机制

2. **没有 contract -> component solver 的正式接线**
   - 当前 contract 更多只参与：
     - producer detection
     - runtime chrome filtering
     - decorative layer hints
     - 少量 semantic bias
   - 但没有真正驱动布局器去识别并排版：
     - `ds-kpi-card`
     - `ds-split-layout`
     - `feat-card`
     - `install-row`
     - `ds-insight`

3. **reference 优势没有被吃满**
   - exporter 现在更多只是“认得这是 `slide-creator` 产物”
   - 还做不到“按 `slide-creator` 的组件契约来排版”

## 为什么这会直接导致当前效果仍然偏差

以 `demo/data-story-zh.html` 为例：

- 当前低分并不只是文字重叠
- 更深层的问题是：
  - 卡片内部 slot 模型没有正式建模
  - split/grid 的轨道比例仍主要靠 generic 求解
  - install row 仍没有走 label rail + command rail 的组件布局器

所以即使：

- producer 被识别了
- contract 被加载了
- body pseudo grid 这类背景层能部分感知

最终导出仍会停留在：

- “知道它是谁”
- 但“不会按它的组件语义来排版”

这就是当前 `data-story` 还只有 `8.88/10` 的根因之一。

## 本轮正式决策

不再把 `slide-creator` reference 当作零散提示源，而是升级为一条正式的 **可同步、可追版本、可驱动布局器** 的 contract pipeline。

### 运行时原则不变

仍然坚持：

- 运行时不能跨仓库读 `slide-creator`
- 运行时只能消费本仓库 vendored contracts / manifests

### 开发期策略升级

开发期要新增：

1. `slide-creator` 上游同步脚本
2. 上游版本记录
3. contract/manifest 生成流程
4. component solver registry

## 下一步必须做的事

1. 新增 `scripts/sync-slide-creator-contracts.py`
   - 从 `slide-creator` 读取可复用 reference / preset / stable DOM 契约
   - 生成本仓库可消费的 versioned contracts

2. 新增 upstream manifest
   - 记录：
     - upstream repo
     - upstream commit
     - synced_at
     - preset sources
     - contract version

3. 把 contract 真正接到布局器
   - 第一批组件 solver：
     - `ds-kpi-card`
     - `feat-card`
     - `install-row`
     - `ds-split-layout`

4. 扩测试和 gate
   - 增加：
     - contract drift check
     - producer-aware fixture / corpus
     - contract-driven component regression tests

## 结论

Session 30 只完成了 **minimal path**，没有完成 **高保真主链路**。

当前 exporter 的 producer-aware 能力，更多还是：

- 识别 producer
- 读取 hints / contract
- 过滤 runtime chrome

而不是：

- 用 contract 直接驱动组件级布局器

后续必须按“上游同步 + 版本追踪 + component solver 接线”补全，否则 `slide-creator` 自家 HTML 的导出质量仍然会被 generic heuristic 上限卡住。
