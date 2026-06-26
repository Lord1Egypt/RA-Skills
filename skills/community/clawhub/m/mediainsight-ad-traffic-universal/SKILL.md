---
name: 媒体广告流量市场分析
description: 查询广告投放流量分布与趋势的数据分析技能。支持按行业、地域、媒体（OTT/移动端）、目标受众等多维度分析广告曝光数据，适用于媒体策略评估、竞品投放监测、行业广告趋势研究等场景。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: MEDIAINSIGHT_MCP_TOKEN
    envVars:
      - name: MEDIAINSIGHT_MCP_TOKEN
        required: false
        description: 可选。未提供时脚本会使用公开共享的演示 token（权限较小、可能随时失效）；正式分析建议使用自己的 MediaInsight MCP token。
---

# 媒体广告流量市场分析

## 你会得到什么

- 一个可直接查询部分行业广告流量分布与趋势的分析技能
- 2 份免费 PDF 报告，可直接下载阅读
- 支持继续用你自己的 token 做更多行业更多媒体更细颗粒度分析

## 免费附赠报告

- [免费报告 1：2024全年媒体广告流量市场分析](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNP0jI9V9pRkKJrYtL?scode=ANEAJwfLAAokGeAoaDAGwAzwarAPE)
- [免费报告 2：2025全年媒体广告流量市场分析](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNaOYYZMA6R0ymjf1M?scode=ANEAJwfLAAoF9heh5bAGwAzwarAPE)

适合先看报告，再决定是否用自己的 token 做更细的行业、地域、媒体和 TA 分析。若浏览器中无法直接打开微信文档，请尝试在微信内访问对应链接。

## 快速体验

从 **skill 根目录** 执行以下命令可直接体验。
整个 skill 目录可单独打包分享，不依赖仓库其他 Python 模块。

脚本内置了一个公开共享、默认小权限的 MediaInsight MCP token，可直接体验。
也可通过 `--token`、`--token-file` 或环境变量 `MEDIAINSIGHT_MCP_TOKEN` 覆盖。

无需 `pip install`，仅需 Python 3.10+ 与可访问目标接口的网络环境。

新建任务默认值：

- 行业默认：`美妆个护类`
- 广告主默认：`明略集团`
- 品牌默认：`明略科技`
- 媒体默认：当前 Token 可见的全部**媒体大类**（即 `type=1` 顶层媒体类目），不是全部具体媒体

默认输出可以理解为：

- `美妆个护类` 行业
- 在当前默认 Token 可见的全部**媒介类型 / 媒体大类**上
- 查看广告流量分布

如果用户希望：

- 查看其他行业
- 细化到具体媒体而不是媒体大类
- 使用更完整的权限范围

则需要使用自己的 token。

```bash
python3 ./scripts/submit_ad_task.py \
  --task-name '演示：近1月广告流量分布' \
  --region-name 北京市 \
  --region-name 上海市 \
  --region-name 广州市 \
  --region-name 深圳市 \
  --months-back 1
```

> 默认会使用公开共享的小权限 demo token，可能随时失效或被限流。
> 如果需要更多维度数据或更稳定的结果，可显式传入 `--token` / `--token-file`，或设置环境变量 `MEDIAINSIGHT_MCP_TOKEN`。

## 适用场景

当用户需要分析**广告流量**分布或趋势，并提供以下信息时，使用此技能：

- **MediaInsight MCP token**：用于通过 MCP `get_ttc_token` 换取底层接口所需的 `ttc_token`。
- **业务约束条件**：包括行业、广告主、品牌、目标受众（TA）、地域范围、媒体范围等。
- 如果用户没有指定行业，默认使用 `美妆个护类`。
- 如果用户没有指定媒体，默认选择当前 Token 可见的全部**媒体大类**。这不是单个固定 ID，而是当前 Token 可见的 `type=1` 顶层媒体类目集合。
- 因此典型输出，不是“全行业、全媒体明细”，而是“指定行业在当前 Token 可见媒介类型上的广告流量”。

## 核心入口

调用本目录下的脚本：

```bash
./scripts/submit_ad_task.py
```

下载已完成任务结果时，调用：

```bash
./scripts/download_ad_task_report.py --biz-id 104433 --wait --extract-dir ./downloads/task-104433
```

注意：
任务创建成功后，报告文件生成通常还需要额外时间。
实际测试中，文件生成过程可能耗时约 10 分钟，建议优先使用 `--wait` 自动轮询后再下载。
如果不使用 `--wait` 且下载过早，脚本会返回 `report file is not ready for download`。

## 执行流程

1. 先对 MCP 执行 `initialize` 建立会话，再在同一会话中调用 `get_ttc_token` 获取 `ttc_token`，并写入 Cookie `_mz_ttc_tkt`。
2. 读取该用户权限范围内的实时字典：
   - 数据集、行业、广告主、品牌、地域、目标受众（TA）、媒体、投放类型、广告点位类型。
3. 仅在该 Token 可见的选项范围内解析用户输入的名称为 ID。
4. 将"全部媒体"展开为该 Token 可见的**全量**媒体 ID 集合（而非部分子集）。
   如果用户未指定媒体，也未要求 all media，则默认使用当前 Token 可见的全部**媒体大类**（type=1）。
5. 计算本次任务消耗的积分数。
6. 提交任务。
7. 任务完成后，如需取回结果文件，按 `bizId` 或内部 `taskId` 下载报告 ZIP，并可解压得到 CSV。
   报告文件生成可能耗时约 10 分钟，建议使用 `--wait` 自动轮询直到文件就绪后再下载。

说明：

- MCP 返回的 `_mz_ttc_tkt` 以当次会话、当次调用结果为准，测试或联调时应立刻拿当前返回值去访问 `api_v2`。
- 不要混用历史轮次换取到的 `_mz_ttc_tkt`，否则容易误判为 token 或权限异常。

## 操作规则

1. **禁止硬编码**：不得跨用户硬编码广告主、品牌、媒体、地域或行业 ID，所有 ID 必须从当前 Token 的字典中动态解析。
2. **权限边界**：若请求的名称在当前 Token 的字典中不存在，立即停止，向用户说明该项超出当前账号权限范围。
3. **媒体展开规则**："全部媒体"必须展开为该 Token 可见的完整具体媒体列表，不得只取少量精选子集。
4. **名称匹配策略**：优先精确匹配；仅当精确匹配无结果且存在唯一部分匹配时，才使用模糊匹配。
5. **可审计性**：如需保留审计记录或保证任务可复现，将解析后的 Payload 写入文件（使用 `--payload-out` 参数）。

## 标准调用示例

```bash
python3 ./scripts/submit_ad_task.py \
  --task-name '近2月美妆个护媒体大类流量分布' \
  --industry-name '美妆个护类' \
  --gender female \
  --age-range 20-49 \
  --region-name 北京市 \
  --region-name 上海市 \
  --region-name 广州市 \
  --region-name 深圳市 \
  --months-back 2 \
  --payload-out /tmp/mediainsight-task.json
```

## 常用参数变体

| 场景 | 参数 |
|------|------|
| 使用默认行业 | 可省略 `--industry-name`，默认 `美妆个护类` |
| 使用默认媒体大类 | 可省略 `--media-name` 和 `--all-media`，脚本会自动选择当前 Token 可见的全部 `type=1` 媒体大类 |
| 展开全部叶级媒体 | `--all-media`，会展开为当前 Token 可见的全部 `type=3` 叶级媒体，数量取决于权限 |
| 包含 OTT | 默认设备仅 `pc` + `mobile`；如需 OTT，显式添加 `--device ott` |
| 仅查询单月数据 | `--months-back 1` |
| 指定特定数据集 | `--dataset 202603` |
| 指定具体媒体（替代全媒体） | `--media-name 爱奇艺 --media-name 腾讯新闻` |
| 指定开放年龄段 | `--age-range 20+` 或 `--age-range 20岁及以上` |
| 查询全部人群 | `--gender all --age-range all` |
| 仅解析不提交（调试模式） | `--dry-run` |

## 年龄参数规则

`--age-range` 不要使用 `20-99` 这类近似写法。
请直接使用产品语义对应的年龄表达，脚本会自动映射到真实 TA 年龄桶。

- `20-49`：表示 20-24、25-29、30-34、35-39、40-44、45-49
- `20+`：表示 20 岁及以上，会覆盖到 `60岁及以上`
- `20岁及以上`：等价于 `20+`
- `all`：表示全部年龄段

如果用户说“男 20+”，应使用：

```bash
--gender male --age-range 20+
```

不要改写成：

```bash
--gender male --age-range 20-99
```

## 预期输出

脚本输出一个 JSON 对象，包含以下字段：

| 字段 | 说明 |
|------|------|
| `login` | 登录状态 |
| `session_file` | 会话文件路径 |
| `resolvedPayload` | 解析后的完整任务参数 |
| `coin` | 本次任务消耗的积分数 |
| `create` | 任务创建结果（`--dry-run` 模式下不包含此字段） |

注意：
`resolvedPayload.reportArgsAd.mediaList` 在三种情况下含义不同：

- 省略媒体参数：默认写入当前 Token 可见的全部**媒体大类** ID（type=1）
- `--all-media`：写入当前 Token 可见的全部叶级具体媒体 ID（type=3），数量取决于权限
- `--media-name ...`：写入用户指定名称解析出的媒体/媒体类目 ID

结果下载提醒：

- 任务创建成功不等于结果文件立刻可下载
- 报告文件生成过程可能耗时约 10 分钟
- 建议直接使用 `download_ad_task_report.py --wait` 自动轮询后再下载

## 异常处理

| 异常现象 | 原因判断 |
|----------|----------|
| 认证失败 | 先确认是否已执行 MCP `initialize`，并使用当次 `get_ttc_token` 返回的最新 `_mz_ttc_tkt` 访问目标接口 |
| 名称解析失败 | 该名称超出当前账号的权限范围 |
| 积分计算成功但任务提交失败 | 提交链路本身有效，失败原因在任务侧，非技能问题 |
