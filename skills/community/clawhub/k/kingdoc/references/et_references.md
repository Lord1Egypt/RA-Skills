# 电子表格 API 参考（kdoc.et.*）

> 金山文档电子表格基于 WPS 开放平台 et API，支持**单元格级精细编辑**，是本技能区别于「整文件替换」品类的核心能力。

## 基础约定

- Base URL：`https://developer.kdocs.cn/api/v1/openapi`
- 鉴权：`Authorization: Bearer <token>`（由 `engine/auth.py` 自动注入并刷新）
- 限流：429 自动指数退避（见 `references/rate_limit.md`）
- 连续 3 次及以上写入**必须**使用批量接口（铁律 #2）

## 工具清单

### kdoc.et.create
创建在线电子表格。

```json
POST /et/sheets
{ "name": "销售数据" }
```
返回：`{ "file_id": "...", "url": "https://docs.wps.cn/sheet/..." }`

### kdoc.et.range.write
批量写入单元格区域（**推荐，性能最佳**）。

```json
PUT /et/ranges/{sheet_id}
{
  "range": "A1:C10",
  "values": [["产品","销量","金额"],["A",100,2000], ...]
}
```

### kdoc.et.formula.set
设置单元格公式。

```json
POST /et/formula/set
{ "sheet_id": "<id>", "cell": "D1", "formula": "=SUM(C1:C10)" }
```

## 性能建议（硬件自适应）

批量写入大小由 `engine/hardware.py` 自动决定（见 `references/rate_limit.md`），
低端机默认 50 行/批，高端机 500 行/批，避免把内存撑爆。

## 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| KD004 | sheet_id 与品类不符 | 先用 `kdoc.file.info` 确认是 sheet |
| KD007 | 版本冲突 | 重新拉取最新版本后写入 |
| KD011 | range 格式错误 | 使用 `A1:C10` 标准格式 |
| KD006 | 限流 | 自动退避，无需人工干预 |

*最后更新：2026-07-12 | v3.0.0*
