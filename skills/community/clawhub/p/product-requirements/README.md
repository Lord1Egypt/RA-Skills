# Amazon 产品需求整理

将评论痛点整理为可验证产品需求

固定工作流：`product/requirements`，输出 `ops_product`。

## 使用

```bash
python scripts/ari.py operations capabilities
python scripts/ari.py operations profile --asin <ASIN> --site amz_us
python scripts/ari.py operations quote --asin <ASIN> --site amz_us
# 用户明确确认后，复用报价返回的 requestId：
python scripts/ari.py operations run --asin <ASIN> --site amz_us --request-id <requestId> --confirm
```

评论不足时先单独使用 `collect`；本 Skill 不会隐式采集。流中断时使用
`operations status --request-id <原requestId>`，不要直接重跑。

需要 ARI API Key（`ari_live_*`）。首次使用运行 `python scripts/ari.py setup`。

## 不适用

- 研发排期或交付承诺
- 供应商采购与下单执行
- 销量或利润预测
