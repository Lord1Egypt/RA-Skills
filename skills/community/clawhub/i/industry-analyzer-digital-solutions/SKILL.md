---
name: digital-solutions-analyzer
description: "Analyze digital transformation solutions for a given industry from major vendors (Huawei, Alibaba, Baidu, Tencent) + vertical industry digital solution providers. Find specific products/solutions or document each company's positioning and differentiation. Use when user asks for '数字化方案', '数字化转型', '行业数字化', 'digital transformation', '行业云方案', '行业 AI 方案'. Part of the industry-analyzer plugin (6-Skill 流水线第 3 环)."
---

# 数字化方案分析器 (Digital Solutions Analyzer)

Analyze digital transformation solutions for a given industry from major vendors (Huawei / Alibaba / Baidu / Tencent) + vertical industry digital solution providers.

## When to Use

- 用户明确要求"分析 {行业} 数字化方案 / 数字化转型方案"
- 行业分析流水线第 3 环（由 行业分析成章官 调度）
- 独立召唤

## Input

- **必填**：`output/{industry-slug}/session.json`
- **可选**：用户可指定重点厂商（如"重点看华为"）

## Output

- **文件**：`output/{industry-slug}/03-digital-solutions.md`
- **格式**：Markdown，含 4 大厂各 1 节 + 垂直厂商合并 1 节

### 必含覆盖

| 类别 | 数量要求 | 内容要求 |
|---|---|---|
| **4 大厂** | 华为 / 阿里 / 百度 / 腾讯 **全部覆盖** | 每家 4 要素（见下） |
| **垂直厂商** | ≥3 家 | 同 4 要素 |

### 必含要素（每家厂商 / 方案）

| 要素 | 说明 |
|---|---|
| **核心方案名** | 产品 / 解决方案名 |
| **目标场景** | 解决客户的什么场景 / 痛点 |
| **差异化策略** | 与同类方案比，独特在哪 |
| **客户案例** | ≥1 个具体客户 / 案例（可写行业） |
| **行业定位** | 该方案在行业中的位置（领先/跟随/差异） |

### 找不到具体方案时的退路

整理"核心解决方案定位 + 差异化策略"：
- 不强求具体产品名
- 必须有定位（解决什么问题）
- 必须有差异化（凭什么能做）
- 案例可用行业级（如"已服务 50+ 三甲医院"）

## Workflow

1. **读 session.json**
2. **4 大厂方案搜索**（并行）：
   - `"华为 {行业} 解决方案"`
   - `"阿里云 {行业} 行业方案"`
   - `"百度 {行业} AI 方案"`
   - `"腾讯云 {行业} 行业方案"`
   - `"Huawei/Alibaba/Baidu/Tencent {industry} digital solution"`
3. **垂直厂商搜索**：
   - `"{行业} 数字化 厂商"`
   - `"{行业} 行业 SaaS"`
   - `"{行业} 信息化 系统"`
   - `"{industry} vertical software vendors"`
4. **每方案整理 4 要素**（找具体产品/案例/官网资料）
5. **找不到具体方案时**：整理定位 + 差异化
6. **写 `03-digital-solutions.md`**
7. **更新 session.json**

### 厂商检索清单参考

参见 `references/major-vendors-list.md`

## stop_condition

- `03-digital-solutions.md` 存在
- 4 大厂全覆盖（华为/阿里/百度/腾讯）
- 垂直厂商 ≥3 家
- 每家 4 要素齐
- session.json `status.solutions` = `done`

## style

- 具体、对比明确、定位清晰
- 不用"赋能""引领"等空话
- 找不到 → 标"具体方案未公开，整理定位与差异化：..."
- 厂商对比：可加 1 张对比表（4 大厂 / 垂直厂商）

## 更新 session.json

- 改 `status.solutions` = `done` / `failed`
- 改 `updated_at`
- 在 `data_sources` 追加

## Standalone Mode

同 Skill 1，未提供 session.json 时自动生成最小版本。

## 错误处理

- 4 大厂某家在 {行业} 无明显方案 → 标"该大厂在 {行业} 暂无公开方案，可参考其在 {相关行业} 的布局"
- 垂直厂商资料稀少 → 至少给 3 家，明确说明行业集中度
- 找不到具体客户案例 → 用行业案例或公开宣传

## 参考

- 行业分析器总 spec：`~/Downloads/周报生成器/行业分析器/docs/superpowers/specs/2026-06-07-industry-analyzer-design.md` §5.3
- 厂商清单：`references/major-vendors-list.md`
