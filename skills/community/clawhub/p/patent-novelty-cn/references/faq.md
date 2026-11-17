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

`technical_solution` 必填。枚举字段只接受这些值：

| 字段 | 可选值 |
| --- | --- |
| `purpose` | `novelty` | `inventiveness` | `pre_filing` | `project_screening` | `competitor_scan` |
| `depth` | `quick` | `standard` | `deep` |
| `legal_status` | `all` | `active` | `pending` | `inactive` |
| `regions` | `global`，或 `CN`/`US`/`EP`/`JP`/`KR`/`WO` |

随时用 `python scripts/patentmax_novelty.py options` 打出这张表。

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
python scripts/patentmax_novelty.py status --operation-id <operation_id>
```

看 `status` 和 `progress`：

- `queued` 排队中
- `running` 正在跑，`stage` 字段有中文阶段描述
- `succeeded` 完成，可以取结果
- `failed` 失败，`error` 里有原因
- `cancelled` 已取消

**绝对不要因为等太久就重新提交**——会再扣一次费。真不想等了用 `cancel --operation-id`。

## 查新结果没有参考价值

九成是技术方案写得不够具体。见 `solution-guide.md`。

典型症状与原因：

| 症状 | 原因 |
| --- | --- |
| 对比文件一大堆但都不贴 | 方案只写了「通过……实现……」，没有具体手段 |
| 找不到任何相关文献 | 术语太生僻，换常见叫法重试；也可能方向确实空白 |
| 结论模棱两可 | 方案没写明和现有技术的区别在哪 |
| 漏掉了国外的在先公开 | `--regions` 缩到了 CN。国外公开同样破坏国内新颖性 |
| 漏掉了论文 | 加了 `--patents-only`。论文同样是现有技术 |
| 数据偏旧 | 18 个月公开窗口，最近一年半的申请本来就查不到 |

**改方案重跑要再花一次钱**，所以第一次就写细。不确定素材够不够，先问用户补三个问题。

## quality_status 是什么意思

| 值 | 含义 | 怎么办 |
| --- | --- | --- |
| `qualified` | 通过质量校验 | 可作为分析依据 |
| `qualified_degraded` | 已生成但有数据短板 | 结论保守使用，交付时说明哪块不足 |
| `review_required` | 需人工复核 | 不要直接当结论交给决策层 |

后两档时看 `quality_details`，里面通常有具体原因（来源覆盖不足、某个维度数据缺失等）。

## 素材太长塞不进命令行

写到文件里用 `--materials-file`：

```bash
python scripts/patentmax_novelty.py create --materials-file ./materials.md ...
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
    "report_type": "novelty",
    "input": {
      "title": "阀门卡滞诊断与清理装置",
      "technical_solution": "采集阀门转轴角度、启闭扭矩及前后水位……",
      "purpose": "pre_filing",
      "depth": "standard",
      "regions": ["global"],
      "legal_status": "all",
      "source_scope": {"patents": true, "papers": true, "web": true}
    }
  }'
```

返回 202 和 `operation_id`，然后轮询 `GET /api/v1/operations/{operation_id}`，完成后取 `GET /api/v1/reports/{report_id}`，下载 `GET /api/v1/reports/{report_id}/files/report.docx`。

**`Idempotency-Key` 是必填 header**，漏了会被拒。
