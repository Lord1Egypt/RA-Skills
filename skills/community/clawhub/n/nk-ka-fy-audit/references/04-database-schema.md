# 数据库结构与增量入库流程（参考）

## 数据库位置
`/workspace/业务数据/集团客户部FY数据.db`

## 核心表结构

### raw_records（逐行原始数据）
```sql
CREATE TABLE raw_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    sheet_name TEXT NOT NULL,
    merchant_sn TEXT, merchant_name TEXT, brand TEXT,
    level1_name TEXT, level2_name TEXT, level3_name TEXT,
    alipay_txn_amount REAL, alipay_indirect_txn_amt REAL,
    wechat_txn_amount REAL, wechat_indirect_txn_amt REAL,
    alipay_rebate_ratio REAL, wechat_rebate_ratio REAL,
    settlement_rate REAL, cost_rate REAL, merchant_rebate_ratio REAL,
    alipay_direct_yield REAL, alipay_direct_ch_ratio REAL,
    alipay_indirect_yield REAL, alipay_indirect_ch_ratio REAL,
    wechat_direct_yield REAL, wechat_direct_ch_ratio REAL,
    wechat_indirect_yield REAL, wechat_indirect_ch_ratio REAL,
    alipay_rebate REAL, wechat_rebate REAL,
    alipay_direct_rebate REAL, alipay_indirect_rebate REAL,
    wechat_direct_rebate REAL, wechat_indirect_rebate REAL,
    total_rebate REAL, original_note TEXT, audit_note TEXT,
    rebate_method TEXT, settlement_date TEXT, occurrence_date TEXT,
    source_row INTEGER, calc_method TEXT
);
```

Also: `monthly_audit`, `brand_audit`, `raw_lines`, `file_structure` tables.

## 增量入库流程（新增单个月份）

1. 检查数据库是否已有该月数据（已存在则跳过）
2. 查找 `DATA_DIR/month/` 目录下的xlsx文件
3. 用openpyxl打开，探测所有Sheet
4. 自动分类Sheet（汇总/常规/中快/拓展/异常/sql）
5. 按类型解析，批量INSERT到raw_records
6. 保存file_structure元数据

**强制约束：**
- 不修改历史数据（除非用户明确要求）
- 新月份只INSERT，不UPDATE/DELETE
- 遇到未知Sheet先问用户，不自作主张
- 中快：LIKE '中快%' 匹配
- 志华：只通过calc_method计入，不重复
- SQL：默认排除（202602）
- 异常表：按备注规则判定，默认排除