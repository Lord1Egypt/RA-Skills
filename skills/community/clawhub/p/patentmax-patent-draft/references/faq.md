# 常见问题

## 报错

| 现象 | 处理 |
| --- | --- |
| `未设置 API 密钥` | `export PATENTMAX_API_KEY=pm_live_xxx`，密钥在 https://api.ip930.com/features/api-platform 创建 |
| `HTTP 401` | 密钥无效或已撤销，到控制台重新创建 |
| `HTTP 402` | 余额不足，到控制台充值 |
| `HTTP 400` | 材料少于 20 字或超过 10 万字；`ideas` 的方向数只能是 1 到 5 |
| `HTTP 409` | 任务还没跑完就来下载，或同一个幂等键正在处理中。等一会儿用 `status` 查 |
| `HTTP 429` | 触发限流，稍后再试 |
| 下载创新升级的 Word 报 404 | **正常**，创新升级只出方向清单，没有 Word。结果用 `status` 取，挑一个方向再写初稿 |
| `读不了这个 Word 文件` | 只支持 `.docx`。老的 `.doc` 先另存为 `.docx` |
| `不是 UTF-8 文本` | 文件编码不对。另存为 UTF-8，或读完后写进 `--supplement` |

## 等待

**等了十几分钟还没完成，是不是卡了？**

大概率没有。通常 6～15 分钟，排队或材料多时可能到 30 分钟。只要没有报错，就继续 `wait`。**不要重新提交。**

**命令断了、对话重开了？**

任务还在服务端跑。用 `wait --operation-id <id>` 接着看，不要重新提交。

**不想要了？**

`cancel --operation-id <id>`，预扣的钱全额退回，后台任务同时停掉。

## 结果

**核对说明里推断条目太多？**

材料太薄了。把核对说明里「待补充」的问题拿去问用户，答案写进 `--supplement`，连同原材料重新提交一次。这是新任务，会重新计费。

**附图有的没画出来？**

`figures` 里 `auto: false` 的图只给了绘图说明，需要另外画。系统画不出的通常是需要精确尺寸的结构图，或材料里对连接关系描述不够的图。

**发明点全都撞上了？**

说明这个方向在专利库里已经有人做过。建议：

1. 看 `alternatives`，换一种实现方式
2. 回头用 `ideas` 换个方向
3. 用专利查新做一次正式判断

**初稿能直接递交吗？**

不能。初稿是给专利代理人的起点，正式的申请文件由代理人定稿并递交。

## 没有 Python 怎么办

直接用 curl：

```bash
# 提交初稿
curl -s -X POST "https://api.ip930.com/api/v1/reports" \
  -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 任取一个唯一串" \
  -d '{"report_type":"technical_disclosure","input":{"supplement":"材料正文……","title_hint":"案件名称"}}'

# 出方向
curl -s -X POST "https://api.ip930.com/api/v1/reports" \
  -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 任取一个唯一串" \
  -d '{"report_type":"idea_upgrade","input":{"idea_text":"想法……","direction_count":3}}'

# 查状态
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  "https://api.ip930.com/api/v1/operations/<operation_id>"

# 取结果
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  "https://api.ip930.com/api/v1/reports/<report_id>"

# 下载初稿 / 核对说明
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" -o 专利初稿.docx \
  "https://api.ip930.com/api/v1/reports/<report_id>/files/report.docx"
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" -o 核对说明.docx \
  "https://api.ip930.com/api/v1/reports/<report_id>/files/report.docx?kind=notes"
```

**`Idempotency-Key` 必填。** 同一个键重试不会重复扣费，但同一个键配不同的材料会被拒绝。
