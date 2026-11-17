# Amazon 已有 ASIN 上线准备度检查

用既有商品与评论证据识别改版和重新上线风险

固定工作流：`audit/launch`，输出 `ops_audit`。

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

- 没有 ASIN 或评论的全新品预测
- 广告预算与投放
- 供应链采购或库存执行
