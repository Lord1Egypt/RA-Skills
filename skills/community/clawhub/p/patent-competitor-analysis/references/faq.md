# 排查

## 免费试用

没设 `PATENTMAX_API_KEY` 时，脚本第一次运行自动领取一份免费试用（¥15、30 天有效，只开通本技能的功能），存在 `~/.patentmax/trial-key-*.json`。

- 报「免费试用额度已用完」或「免费试用只开通了领取它的那个功能」：注册 PatentMax 再送 ¥50 体验额度，创建正式密钥后设成环境变量
- 报「免费试用密钥已过期或失效」：本地缓存已自动清掉，重跑同一条命令会领新的
- 报「免费试用名额暂时发完了」或「今天这个网络已经领过」：当天领不到了，注册 PatentMax 用正式密钥

## 用自己的密钥

```bash
echo ${PATENTMAX_API_KEY:0:8}
```

应输出 `pm_live_` 或 `pm_test_`。要设置的话：

```bash
export PATENTMAX_API_KEY="pm_live_你的密钥"
```

Windows PowerShell 用 `$env:PATENTMAX_API_KEY="..."`，CMD 用 `set PATENTMAX_API_KEY=...`。`export` 只对当前终端有效，换窗口要重设。

密钥在 https://api.ip930.com/features/api-platform 自助创建。

## 400 参数不正确

必填只有两项，返回的 `detail` 里会逐项写缺了什么、怎么填：

| 字段 | 脚本参数 | 要求 |
| --- | --- | --- |
| `subject` 技术方向 | `--subject` | 3-255 字，只写技术名称 |
| `competitors` 目标企业 | `--company` | 至少 1 个，第一个是报告主体；写专利上登记的全称 |

可选字段：`materials` 背景素材（填了至少 5 字，上限 10 万字）、`objective` 分析目标（填了 3-2000 字）、`target_markets` 最多 20 个、`source_types` 最多 6 个、`excluded_directions` 最长 2000 字。

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
python scripts/patentmax_competitive.py status --operation-id <operation_id>
```

看 `status` 和 `progress`：

- `queued` 排队中
- `running` 正在跑，`stage` 字段有中文阶段描述
- `succeeded` 完成，可以取结果
- `failed` 失败，`error` 里有原因
- `cancelled` 已取消

**绝对不要因为等太久就重新提交**——会再扣一次费。真不想等了用 `cancel --operation-id`。

## 报错「没有找到名为 XX 的申请人」

目标企业名称和专利登记名对不上。常见原因：写了简称、错了一个字、填了「企业A」这类占位名。先用专利检索按申请人查一下登记全称，换成全称再提交。系统会自动尝试用字号回溯登记名，但回溯不到时会直接告诉你，不会扣费跑一份空报告。

## 报错「找到了申请人，但没有检索到与 XX 相关的公开专利」

企业对上了，但它在这个方向上没有公开专利。把 `--subject` 放宽一点（换成更常见的叫法或上位词）再试。

## 报告太泛，没有决策价值

典型症状与原因：

| 症状 | 原因 |
| --- | --- |
| 没有聚焦到你关心的分支 | `--subject` 太宽，换成更具体的技术名称 |
| 检索跑偏 | `--subject` 里混进了企业名或「专利布局」这类词，只写技术名称 |
| 主体企业的专利量明显偏少 | `--company` 写的是简称或集团名，实际申请人是子公司 |
| 数据偏旧 | 18 个月公开窗口，最新动作本来就查不到 |

**重跑要再花一次钱**，所以第一次就把企业全称和技术方向问清楚。

## quality_status 是什么意思

| 值 | 含义 | 怎么办 |
| --- | --- | --- |
| `qualified` | 通过质量校验 | 可作为分析依据 |
| `qualified_degraded` | 已生成但有数据短板 | 结论保守使用，交付时说明哪块不足 |
| `review_required` | 需人工复核 | 不要直接当结论交给决策层 |

后两档时看 `quality_details`，里面通常有具体原因（来源覆盖不足、某个维度数据缺失等）。

## 背景素材太长塞不进命令行

背景素材可不填。要带的话写到文件里用 `--materials-file`（UTF-8，上限 10 万字）。

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
    "report_type": "patent_intelligence",
    "input": {
      "subject": "钠离子电池",
      "competitors": ["宁德时代新能源科技股份有限公司"]
    }
  }'
```

返回 202 和 `operation_id`，然后轮询 `GET /api/v1/operations/{operation_id}`，完成后取 `GET /api/v1/reports/{report_id}`，下载 `GET /api/v1/reports/{report_id}/files/report.docx`。

**`Idempotency-Key` 是必填 header**，漏了会被拒。
