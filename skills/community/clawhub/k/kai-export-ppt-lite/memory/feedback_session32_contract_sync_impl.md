# Session 32：slide-creator contract sync pipeline 首次落地

本轮把“多引用 slide-creator 上游信息”从讨论变成了代码和产物：

## 已落地

1. 新增开发期同步脚本
   - `scripts/sync-slide-creator-contracts.py`
   - 从本地 `slide-creator` checkout 读取 preset reference / demo HTML
   - 生成本仓库自包含的 contract 文件，不依赖运行时跨仓库读取

2. 新增 versioned manifest
   - `contracts/slide_creator/manifest.json`
   - 记录：
     - `upstream_commit`
     - `generated_at`
     - 每个 preset 的 `contract_id / contract_version / family / producer_version_tested`

3. contract 面扩充
   - 现有 preset：
     - `blue-sky`
     - `enterprise-dark`
     - `swiss-modern`
   - 新增 preset：
     - `data-story`

4. contract 内容不再只有 producer 识别提示
   - 现在每个 preset contract 都包含：
     - `component_selectors`
     - `component_slot_models`
     - `layout_variations`
     - `decorative_layers`
     - `producer_detection`
     - `observed_component_classes`

5. 修正了一处真实 drift
   - `data-story` reference 写的是 `body::before`
   - 但实际 demo 使用的是 `.slide::before`
   - contract 现在同时记录 `.slide::before` 和 `body::before`
   - exporter 也补上了 `var(--grid-line)` + `opacity` 的网格背景解析

## 这轮对质量的实际意义

这轮不是直接把 `data-story` 拉到 `9.5+`，而是把最关键的基础设施补齐：

- exporter 终于有了可同步、可追版本的上游 contract 面
- `data-story` 不再是“最需要提质却完全没有 contract”的 preset
- decorative background 不再只支持 `rgba(...)`，现在 `data-story` 的变量色网格也能进入导出

## 当前验证

1. `python3 -m py_compile scripts/sync-slide-creator-contracts.py scripts/test-export.py scripts/export-sandbox-pptx.py`
2. `python3 scripts/test-export.py`
3. `python3 scripts/export-sandbox-pptx.py demo/data-story-zh.html demo/data-story-output.pptx`
4. `python3 scripts/compare-html-ppt-visual.py demo/data-story-zh.html demo/data-story-output.pptx --outdir demo/data-story-visual-compare`

结果：

- 测试全通过
- `data-story` 当前逐页分数仍是：
  - Slide 1 `9.2`
  - Slide 2 `8.3`
  - Slide 3 `9.0`
  - Slide 4 `8.5`
  - Slide 5 `9.1`
  - Slide 6 `8.7`
  - Slide 7 `8.9`
  - Slide 8 `9.3`
- 总体仍是 `8.88/10`

## 结论

Session 32 证明了一点：

- “多引用一些”是对的
- 但只有当这些 contract 真正进入 component solver，质量才会继续明显上升

当前最正确的下一步不是再补更多 manifest 字段，而是开始消费它们：

1. `ds-kpi-card` solver
2. `feat-card` solver
3. `install-row` solver
4. `ds-split-layout` solver

否则 exporter 仍然只是：

- 认得 `slide-creator`
- 认得 `Data Story`
- 但还不会按照它的组件槽位稳定排版
