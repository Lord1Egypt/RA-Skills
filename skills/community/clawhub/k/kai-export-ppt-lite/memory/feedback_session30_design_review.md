# Session 30：通用 Exporter + Producer-Aware Hints + Vendored Contracts 设计收口

日期：2026-04-22

## 本轮完成

1. 新增 Session 30 主方案：
   - `docs/session30-exporter-hints-and-contracts-plan.md`
2. 完成自我对抗性评审：
   - `docs/session30-self-adversarial-review.md`
3. 完成 Claude 对抗性评审：
   - `docs/session30-claude-adversarial-review.md`

## 方案核心变化

这一轮的目标不是继续修单个 deck，而是把 exporter 的分层架构从“经验共识”收紧成可实施设计：

- `generic core` 继续负责通用 HTML 幻灯片导出
- `producer-aware` 只作为增益层，不得替代 generic core
- `slide-creator` reference 只作为开发期契约源，不得成为运行时依赖
- 运行时只允许读取：
  - 当前 HTML
  - 当前 HTML 内嵌 hints
  - 同目录 sidecar
  - 当前仓库 vendored contracts

## 自评后收紧的点

1. `ExportHints` 不能膨胀成第二套布局 IR
2. watermark 只能算 producer detection 信号，不能直接决定布局
3. vendored contracts 必须带来源和版本追踪
4. `slide-creator` 只是第一个 adapter，不是 exporter 的默认中心

## Claude 评审后采纳的修改

1. `ExportHints` 增加 schema 级结构约束
   - 不能只靠“禁止列表”防止 IR 漂移
2. producer detection 改成“跨机制独立信号”
   - `meta + data-producer` 只算一个元数据通道
   - watermark 单独算一个水印通道
3. `ProducerAdapter` 接口改为 Python `Protocol`
4. hints/contract 版本策略统一：
   - `contract_ref`
   - `contract_id`
   - `contract_version`
5. 新增原语从 producer-aware path 晋升到 generic core 的规则
6. success criteria 和 phase gate 全部补充数值化门槛

## 当前状态

- 代码未改，当前已验证导出基线仍是 `9.0/10`
- Session 30 完成的是设计与评审收口，不是实现
- 进入实现前，运行时边界、adapter 形式、contract 版本策略、对抗测试样本都已经明确

## 下一步

如果继续实现，应该严格按 Session 30 phase 顺序推进：

1. `Phase 2`
   - `ExportHints` schema
   - producer detection
   - `ProducerAdapter` 接口
   - `slide-creator adapter` minimal path
2. `Phase 3`
   - vendored contracts
   - drift/version checks
3. `Phase 4`
   - generic core 消费 hints
4. `Phase 5`
   - producer-aware corpus 和评估 gate
