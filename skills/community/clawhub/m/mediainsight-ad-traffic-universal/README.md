# 媒体广告流量市场分析

用自然语言描述需求，自动查询广告投放流量的分布与趋势数据。支持按行业、地域、媒体（OTT/移动端）、目标受众等多维度组合分析。

---

## 你会得到什么

- 一个可直接查询部分行业广告流量分布与趋势的分析技能
- 2 份免费 PDF 报告，可直接下载阅读
- 支持继续用你自己的 token 做更多行业更多媒体更细颗粒度分析

## 免费附赠报告

- [免费报告 1：2024全年媒体广告流量市场分析](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNP0jI9V9pRkKJrYtL?scode=ANEAJwfLAAokGeAoaDAGwAzwarAPE)
- [免费报告 2：2025全年媒体广告流量市场分析](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNaOYYZMA6R0ymjf1M?scode=ANEAJwfLAAoF9heh5bAGwAzwarAPE)

适合先看报告，再决定是否用自己的 token 做更细的行业、地域、媒体和 TA 分析。若浏览器中无法直接打开微信文档，请尝试在微信内访问对应链接。

## 能做什么

- 查询指定行业在各媒体平台的广告曝光分布
- 对比不同地域、不同时段的投放流量趋势
- 按性别、年龄段等受众维度过滤数据
- 自动展开"全部媒体"为当前账号可见的完整媒体列表
- 下载已完成任务的结果 ZIP，并可解压查看 CSV

## 30 秒体验

脚本内置了一个公开共享、默认小权限的 MCP token，可直接体验真实提交流程；也可以通过 `--token`、`--token-file` 或环境变量 `MEDIAINSIGHT_MCP_TOKEN` 覆盖：

默认值说明：

- 行业默认：`美妆个护类`
- 广告主默认：`明略集团`
- 品牌默认：`明略科技`
- 媒体默认：当前 token 可见的全部**媒体大类**（即 `type=1` 顶层媒体类目），不是全部具体媒体

因此，这个公开默认体验更接近于：

- 查看 `美妆个护类`
- 在所有可见**媒介类型 / 媒体大类**上的
- 广告流量分布

```bash
python3 ./scripts/submit_ad_task.py \
  --task-name '演示：近1月广告流量分布' \
  --region-name 北京市 \
  --region-name 上海市 \
  --region-name 广州市 \
  --region-name 深圳市 \
  --months-back 1
```

> 默认会使用公开共享的小权限 demo token 先建立 MCP 会话，再调取 `get_ttc_token`，随后访问真实 MediaInsight 接口；该 token 可能随时失效或被限流。
> 如果省略 `--industry-name`，会默认使用 `美妆个护类`；如果省略媒体参数，会默认选择当前 token 可见的全部媒体大类。
> 如果你想看其他行业，或者想把媒体范围细化到具体媒体明细，通常需要切换成你自己的 token。
> 无需 `pip install`，仅需 Python 3.10+。

## 示例输出

```json
{
  "login": {
    "code": 0,
    "msg": "success"
  },
  "session_file": "/tmp/mediainsight-skill-xxxxx.json",
  "resolvedPayload": {
    "name": "演示：近1月广告流量分布",
    "advertiserStid": "000000080000000000000692",
    "brandStidList": ["000000100000000000010184"],
    "regionInfo": {
      "list": [
        "000000000000000000000012",
        "000000000000000000000020",
        "000000000000000000000124",
        "000000000000000000000126"
      ],
      "isPackage": false
    },
    "taInfoList": [
      [{"id": "gender-female-id", "type": 1}, {"id": "age-20-24-id", "type": 2}, {"id": "age-25-34-id", "type": 2}, {"id": "age-35-44-id", "type": 2}, {"id": "age-45-49-id", "type": 2}]
    ],
    "reportArgsAd": {
      "dataSet": "202504",
      "industryInfo": {
        "list": ["000000130000000000001960"],
        "isPackage": false
      },
      "campaignInfo": {
        "list": [],
        "isPackage": false
      },
      "deviceList": [0, 1],
      "mediaList": ["visible-root-media-type1-id-1", "visible-root-media-type1-id-2"],
      "adSpotTypeList": {
        "list": [],
        "isPackage": false
      },
      "indicators": ["impPassion"],
      "charts": [
        "freq-capping",
        "data",
        "total_metrics",
        "flow-distribution-media",
        "flow-distribution-platform",
        "flow-distribution-industry",
        "flow-distribution-ta",
        "flow-distribution-region",
        "frequency-saturation-freq-capping"
      ]
    }
  },
  "coin": {
    "code": 0,
    "msg": "OK",
    "data": {
      "coinCost": 20
    }
  },
  "create": {
    "code": 0,
    "msg": "OK",
    "data": 104422
  }
}
```

> 上面是贴近真实结构的示例输出，具体字段值会随当前 token 的权限范围、可见媒体数和当月数据集变化而变化。

## 查看更多行业数据

如果你要扩展到其他行业，或进一步细化到具体媒体明细，通常需要换用你自己的 token。

**[申请正式账号](https://jsj.top/f/OO3GKM)**

正式账号每月赠送固定金币额度，额度不足时可充值。

申请后使用自己的 MCP token 运行：

```bash
python3 ./scripts/submit_ad_task.py \
  --token '<YOUR_MCP_TOKEN>' \
  --task-name '近2月美妆个护媒体大类流量分布' \
  --industry-name '美妆个护类' \
  --gender female \
  --age-range 25-44 \
  --region-name 上海市 \
  --months-back 2
```

> 可见的行业、广告主、品牌、媒体、地域、TA 和数据集，都会根据当前 token 的实际权限动态解析。
> 如果未显式指定媒体，脚本默认会选择当前 token 可见的全部媒体大类；只有使用 `--all-media` 时，才会展开为全部叶级具体媒体，数量取决于当前 token 权限。
> 默认设备是 `pc` 和 `mobile`；如果需要包含 OTT，请显式加上 `--device ott`。

## 下载任务结果

任务完成后，可按创建接口返回的 `bizId` 下载结果：

```bash
python3 ./scripts/download_ad_task_report.py \
  --biz-id 104433 \
  --wait \
  --extract-dir ./downloads/task-104433
```

也支持直接传内部 `taskId`：

```bash
python3 ./scripts/download_ad_task_report.py \
  --task-id 4433 \
  --wait \
  --extract-dir ./downloads/task-4433
```

注意：

- 任务创建成功后，报告文件通常不会立刻生成完成
- 实测文件生成过程可能耗时约 10 分钟
- 可使用 `--wait` 自动轮询直到文件可下载
- 如果不使用 `--wait` 且下载过早，脚本会返回 `report file is not ready for download`
- 下载的 CSV 文件为 GBK 编码，读取时请指定 `encoding='gbk'`（如 pandas：`pd.read_csv(path, encoding='gbk')`）

## 认证说明

- 这套 skill 访问 `api_v2` 时，不是直接拿 MCP token 调业务接口。
- 正确链路是：`MCP token -> initialize -> get_ttc_token -> Cookie _mz_ttc_tkt -> api_v2`
- `_mz_ttc_tkt` 以当次 MCP 会话返回值为准，联调时应直接使用当前返回值，不要混用历史轮次换出的 cookie。

## 安装要求

- Python 3.10+
- 网络需可访问 `https://mediainsight.cn.miaozhen.com`

## 年龄参数怎么写

`--age-range` 请尽量按产品语义直接填写，不要自己发明近似区间。

- `20-49`
  适用于明确的闭区间年龄段。
- `20+`
  表示 20 岁及以上，会自动覆盖到 `60岁及以上`。
- `20岁及以上`
  与 `20+` 等价。
- `all`
  表示全部年龄段。

推荐示例：

```bash
python3 ./scripts/submit_ad_task.py \
  --task-name '男20plus京津深' \
  --industry-name '美妆个护类' \
  --region-name 北京市 \
  --region-name 天津市 \
  --region-name 深圳市 \
  --gender male \
  --age-range '20+' \
  --months-back 2
```

不推荐写法：

```bash
--age-range 20-99
```

因为产品里的高龄段实际是 `60岁及以上`，不是无限细分到 99 岁。

## 常见问题

**为什么我查的行业或媒体不存在？**
数据权限由账号决定。演示账号仅开放部分维度，申请正式账号后可查询完整范围。

**提交成功后在哪里看结果？**
脚本会输出创建接口的原始响应；其中任务标识通常在 `create.data`。数据处理完成后，可用 `download_ad_task_report.py` 按 `bizId` 或内部 `taskId` 下载结果文件，也可到对应平台查看分析报告。报告文件生成可能耗时约 10 分钟，建议直接使用 `--wait` 自动轮询下载。

**金币怎么算？**
每次提交前脚本会输出本次预计消耗的金币信息（通常在 `coin.data`），可提前确认再决定是否继续。
