# 数据契约（data.json schema）

> 本文档定义 one-paper-company 周期复盘形态的 data.json 完整 schema。

## 完整 TypeScript 定义

```typescript
interface CycleData {
  // —— 行情层 ——
  pre:        [string, number, string][];   // 稀疏史前点
  closes:     [string, number][];            // 早期月线收盘
  candles:    [string, number, number, number, number][];  // 月K
  events:     [string, number, string, string][];          // K线事件

  // —— 财务层 ——
  fin:        [string, number, number, number][];          // [季, 营收, 净利, 毛利率%]
  seg:        { years: string[]; dc:number[]; gaming:number[];
                proviz:number[]; auto:number[]; oem:number[] };
  hf:         { years: string[]; capex:number[]; dcrev:number[]; rent:number[] };
  inv:        [string, number, number][];

  // —— 研究层 ——
  wall:       { w1: WallRow[]; w2: WallRow[] };
  fateClass:  Record<string, string>;
  scores:     ScoreItem[];
  excluded:   { per:string; why:string }[];
  radar:      { ind:string[]; now:number[]; cisco:number[]; mine:number[] };
  stages:     string[];
  clock:      ClockItem[];
  signals:    SignalItem[];

  // —— 文案层 ——
  hero:       { kicker:string; h1Prefix:string; h1Em:string; thesis:string;
                metaRow: MetaItem[] };
  steps:      StepItem[];
  outro:      { h2:string; p:string; verdict:string;
                footgrid: {title:string; body:string}[] };
  footer:     string;

  // —— 品牌层 ——
  brand:      { green:string; greenD:string; pixelTextTop:string; pixelTextBottom:string };
  quarter:    string;
  asOf:       string;

  // —— 模板层（可选，有默认值）——
  title:      string;
  kline:      { yMin?; yMax?; focusYMin?; focusYMax?; focusRange?; markArea?; footHtml? };
  vizNote:    string;
  vpFoots:    { fin; seg; wall; hf; inv; score; signal };
  stepMeta:   Record<string, {vp; tag; state?}>;
  wallLabels: { w1: string; w2: string };
  wallEmptyFallback: string;
  clockCenterText: string;
  radarLabels: { now; cisco; mine };
  finMarkpoints: Markpoint[];
  invMarkpoints: Markpoint[];
}
```

**完整示例**：见 `references/nvidia_data.json` 和 `references/amd_data.json`。

## 时钟 8 扇区阶段名（固定，勿改）

```javascript
var STAGES = ["底部观察","早期上行","重新扩张","过热或反转",
              "交付洪峰消化","供需再平衡","利润压力","脆弱复苏"];
```

## 信号卡 8 项结构（固定）

每张信号卡四要素固定，内容按公司填充：
- `now`：现值
- `th`：阈值（触发警报）
- `lag`：时滞（领先/滞后什么指标几个季度）
- `fp`：证伪（什么情况说明这个信号失灵）
- `src`：信源
- `st`：状态（st-ok/st-part/st-watch）

## 数据获取链路

| 数据字段 | 抓取工具 | 兜底策略 |
|---|---|---|
| 股票代码 | `mx-xuangu` / `mx-zixuan` | AskUserQuestion 让用户填 |
| `pre`（稀疏史前点） | WebSearch "公司 IPO 价格 拆股复权" | 留空数组 + 标注"史前数据不可机读" |
| `closes`（早期月线） | `mx-xuangu` qfq 前复权 | WebSearch "公司 月K 历史数据" |
| `candles`（月K） | `mx-xuangu` qfq 前复权 | WebSearch |
| `events`（K线事件） | WebSearch 公司大事记 | 用户提供 |
| `fin`（财务季） | WebSearch 公司 IR / SEC 10-K | 缺失季用 null 占位 |
| `seg`（分部财年） | WebSearch 公司 10-K 分部披露 | 简化为单分部 |
| `hf`（高频需求） | WebSearch 四大客户 capex / TrendForce | 标注"近似"并跳过 |
| `inv`（库存） | WebSearch 公司财报库存天数 | 留空 + vp-foot 标注 |
| `wall`（格局墙） | WebSearch 行业出清史 | 内置行业模板（半导体/软件/能源/金融） |
| `scores`/`excluded`/`radar`/`clock`/`signals` | industry-cycle-research 方法论框架（内置） | Phase B 让用户修改 |
| 图片 | Wikimedia Commons / 公司官网 | 占位灰底 + alt + figcaption |
