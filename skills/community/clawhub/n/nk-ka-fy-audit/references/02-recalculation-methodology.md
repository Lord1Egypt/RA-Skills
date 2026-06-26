# 审计重算方法论（参考）

## 总流程

1. 发现新月份 → 读取Excel, 解析所有Sheet
2. 按Sheet类型分类 → 计算表/汇总表/特殊表
3. 从计算表独立重算（按calc_method分类型）
4. 特殊表处理 → 按备注规则判定入账
5. 与汇总表逐品牌比对
6. 输出审计报告

## 各Sheet重算公式

### 1. 常规Sheet / 中快系列Sheet
```
支付宝返佣 = ROUND(支付宝交易金额 × 支付宝返佣比例, 2)
微信返佣 = ROUND(微信交易金额 × 微信返佣比例, 2)
总返佣 = 支付宝返佣 + 微信返佣
```
⚠️ 中快系列直接用 total_rebate（包含支付宝间连返佣，DB提取字段不包含此列）

### 2. 拓展Sheet（仅202307）
```
通道分润 = ROUND(交易金额 × (结算费率 - 商户返佣比例 - 成本费率) × 渠道分润比例, 2)
```
4通道：支付宝直联、微信直联、支付宝旗舰店、微信旗舰店。**必须从Excel读取重算**。

### 3. 志华/拓展人志华Sheet（202308~202406）
```
通道分润 = ROUND(交易金额 × 收益率 × 渠道分润比例, 2)
总返佣 = 分润(支付宝直连) + 分润(支付宝间连) + 分润(微信直连) + 分润(微信间连)
```
⚠️ DB只存收益率，缺渠道分润比例和间连数据 → **方案A：读Excel重算 | 方案B：直接用total_rebate**
⚠️ 志华数据**只通过calc_method计入**，不通过sheet_name重复计算

### 4. sql Sheet（仅202602）
用户明确指示不计入汇总，跳过 `calc_method='sql_recalc' for month='202602'`。

### 5. 历史差额调整
`audit_note='历史差额调整'` 的记录计入汇总，用原始total_rebate。

## 与汇总表比对逻辑

```
差额 = 汇总表总金额 - 审计重算总金额
|diff| ≤ 1元 → ✅ 通过
|diff| > 1元 → ❌ 差异（diff>1为超额发放，diff<0为少发视同无差异）
```

## 重算字段对应（按calc_method）

| calc_method | 重算方式 | 重算所需字段 |
|-------------|---------|-------------|
| regular | ROUND(txn×rate,2) | ali/wx_txn_amount, ali/wx_rebate_ratio |
| zhongkuai | 直接用total_rebate | total_rebate |
| expansion_307 | 读Excel完整公式 | 需Excel读取 |
| expansion_308 | 读Excel或用total_rebate | total_rebate（备用） |
| sql_recalc | total_rebate（202602跳过） | total_rebate |
| abnormal | 不计入（除非audit_note=历史差额调整） | — |