# 排查

## 报「未设置 API 密钥」

```bash
echo ${PATENTMAX_API_KEY:0:8}
```

应输出 `pm_live_` 或 `pm_test_`。空的话：

```bash
export PATENTMAX_API_KEY="pm_live_你的密钥"
```

Windows PowerShell 用 `$env:PATENTMAX_API_KEY="..."`，CMD 用 `set PATENTMAX_API_KEY=...`。`export` 只对当前终端有效，换窗口要重设。

密钥在 https://api.ip930.com/features/api-platform 自助创建。

## 400 参数不正确

必填只有 `subject`（技术主题，3-255 字），返回的 `detail` 里会逐项写缺了什么、怎么填。

可选字段：`materials`（填了至少 5 字，上限 10 万字）、`objective`（填了 3-2000 字）。

另外 `target_markets` 最多 20 个、`competitors` 最多 50 个。`roadmap_context` 每项最长 2000 字，其中 `disclosure_timing`、`filing_preference`、`budget_and_volume`、`confidentiality_limits` 为 500 字。

**注意这个接口不接受 `source_types` 和 `time_range`**——那两个是企业情报分析的参数，传进来会被拒。

## 401 / 402 / 403

- **401** 密钥无效或已撤销——检查是否复制完整、有没有多余空格
- **402** 余额不足——到控制台充值
- **403** 该密钥没有此接口权限

## 409 任务冲突

两种情况：

- **报告还没跑完就来取结果** —— 先用 `wait --operation-id <operation_id>` 确认状态是 `succeeded` 再取
- **同一个 Idempotency-Key 正在处理中** —— 这是幂等保护在起作用，说明同样的请求已经在跑了，**不要改 key 重试**，用返回的 operation_id 去查状态

## 429 限流

已有同类任务在排队，或触发频率限制。等一会儿再试，不要死循环重试。

## 任务卡住 / 等超时了

**跑得久不代表失败。** 这类报告要跑几十分钟是正常的，只要没有报错就继续 `wait`，不要重新提交。

```bash
python scripts/patentmax_roadmap.py status --operation-id <operation_id>
```

看 `status` 和 `progress`：

- `queued` 排队中
- `running` 正在跑，`stage` 字段有中文阶段描述
- `succeeded` 完成，可以取结果
- `failed` 失败，`error` 里有原因
- `cancelled` 已取消

**绝对不要因为等太久就重新提交**——会再扣一次费。真不想等了用 `cancel --operation-id`。

## 报告太泛，没有决策价值

典型症状与原因：

| 症状 | 原因 |
| --- | --- |
| 报告很散，没有聚焦 | `--subject` 太宽，换成更具体的技术名称 |
| 检索跑偏 | `--subject` 写成了句子（「XX 的技术路线与专利布局」），只写技术名称 |
| 数据偏旧 | 18 个月公开窗口，最新动作本来就查不到 |

**重跑要再花一次钱**，所以第一次就把技术主题问清楚。

## quality_status 是什么意思

| 值 | 含义 | 怎么办 |
| --- | --- | --- |
| `qualified` | 通过质量校验 | 可作为分析依据 |
| `qualified_degraded` | 已生成但有数据短板 | 结论保守使用，交付时说明哪块不足 |
| `review_required` | 需人工复核 | 不要直接当结论交给决策层 |

后两档时看 `quality_details`，里面通常有具体原因（来源覆盖不足、某个维度数据缺失等）。

## 素材太长塞不进命令行

素材可不填。要带的话写到文件里用 `--materials-file`：

```bash
python scripts/patentmax_roadmap.py create --materials-file ./materials.md ...
```

文件要 UTF-8 编码。上限 10 万字。

## 中文乱码

脚本已强制 UTF-8 输出。还乱码是终端编码问题：

- Windows CMD：先跑 `chcp 65001`
- PowerShell：`$OutputEncoding = [System.Text.Encoding]::UTF8`
- Git Bash：一般没问题

## 想先验证参数，不想扣费

把密钥换成 `pm_test_` 开头的沙箱密钥，会立即返回模拟结果、不调用外部服务、不计费。

**它跑不出真实分析结果**，只能用来确认参数拼得对、响应结构长什么样。正式使用走 `pm_live_`。

## 没有 Python

脚本只用标准库，Python 3.7+ 都能跑，不需要 `pip install`。

实在没有就直接发 HTTP 请求：

```bash
curl -s -X POST "https://api.ip930.com/api/v1/reports" \
  -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 自定义唯一串" \
  -d '{
    "report_type": "roadmap_layout",
    "input": {
      "subject": "钠离子电池正极材料",
      "roadmap_context": {
        "future_plan": "明年 Q2 量产，Q4 进两家车企供应链",
        "budget_and_volume": "今年 15 件，预算 60 万",
        "disclosure_timing": "9 月车展首发"
      }
    }
  }'
```

返回 202 和 `operation_id`，然后轮询 `GET /api/v1/operations/{operation_id}`，完成后取 `GET /api/v1/reports/{report_id}`，下载 `GET /api/v1/reports/{report_id}/files/report.docx`。

**`Idempotency-Key` 是必填 header**，漏了会被拒。
