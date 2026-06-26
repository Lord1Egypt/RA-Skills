# Changelog

## v2.9.3 (2026-06-04)

### 核心能力模块截图移除

- **融资诊断模块**: 移除 `assets/screenshot-diagnosis.png` 截图引用
- **TS条款分析模块**: 移除 `assets/screenshot-termsheet.png` 截图引用
- **Capital EQ模块**: 移除 `assets/screenshot-capitaleq.png` 截图引用
- **assets 目录说明更新**: 移除 `SKILL.md` 资源部分对3张截图的引用
- **版本号**: 2.8.6 → 2.9.3

---

## v2.8.1 (2026-05-24)

### 文案与资产更新

- **description 优化**: 去除"被拒后情绪急救。已帮852+创始人少走弯路"文案，替换为"模拟投资人谈判"
- **视觉资产更新**: 替换 3 张功能截图（融资诊断 / TS条款分析 / Capital EQ）为最新版本

---

## v2.8.0 (2026-05-24)

### 页面与品牌全面升级

- **品牌焕新**: Slogan 升级为「OPC创业者专属的AI融资顾问」/ "The AI Financing Advisor for OPC Entrepreneurs"
- **价值主张**: 新增「节奏不跑偏 · 条款不踩坑 · 情绪不崩溃」核心主张
- **视觉资产**: 新增 4 张品牌资产（Logo + 3 张功能截图）
- **SKILL.md 全面重构**: 优化页面结构，提升 ClawHub 转化率
  - 顶部新增 Security & Privacy 安全声明区块
  - 新增 Free vs Pro 功能对比表（页面上部展示）
  - 新增 Why This Skill 竞品对比表（¥299/月 vs 竞品订阅制）
  - 3 张功能截图直接嵌入（融资诊断 / TS条款分析 / Capital EQ）
  - 精简响应示例，突出「结论→依据→行动建议」结构
  - 优化 description 为转化导向文案

### SEO 与发现优化

- **skill.json tags 扩充**: 从 10 个增加到 23 个，覆盖更多搜索场景
  - 新增: `term-sheet`, `ts-analysis`, `capital-eq`, `emotional-intelligence`, `bp`, `pre-a`, `series-a`, `chinese`, `china-startup`
- **description 优化**: 更简洁、更有转化力，突出 Capital EQ 差异化

### 数据与版本

- **版本号统一**: skill.json / SKILL.md / 页面统一为 `v2.8.0`
- **displayName 统一**: 焕智FA Pro — AI专属融资顾问
- **下载数据**: 已帮 852+ 创始人少走弯路

---

## v2.7.5 (2026-05-22)

- 微调交互规则
- 优化升级提示触发频率

## v2.7.0 (2026-05-15)

- 新增 Capital EQ 深度干预模式
- 扩充情绪识别关键词库

## v2.6.0 (2026-05-01)

- 优化 TS 条款分析准确度
- 新增 Liquidation Preference 2x 红旗规则

## v2.5.0 (2026-04-15)

- 融资诊断脚本优化，评分逻辑更精准
- 新增 2 个测试用例

## v2.4.0 (2026-04-01)

- 首次发布 Pro 版付费功能
- 新增融资进度追踪模块
- 新增 edge-tts 语音回复支持
