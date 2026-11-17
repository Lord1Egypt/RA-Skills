# Amazon 市场进入对照简报 专属运营工作流

固定契约：`page_compare/entry` → `ops_page_compare`。不得改成任意 prompt 或其他 focus。

1. `operations capabilities` 验证服务端能力。
2. `operations profile --asin <ASIN> --site <站点>` 检查商品字段。
3. `operations quote --asin <ASIN> --site <站点>` 返回报价与 requestId。
4. 用户明确确认后，以同一 requestId 执行 `operations run ... --confirm`。
5. 流中断后只运行 `operations status --request-id <原值>`，不得直接重跑。

## 不适用

- 市场规模或销量预测
- 广告预算、库存或采购执行
- 订单、利润或真实退货率判断
