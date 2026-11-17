# 历史开奖数据来源 (data_sources)

`scripts/fetch_history.py` 负责抓取历史开奖数据, 输出归一化 JSON 供 `analyze.py` / `generate.py` 使用。

## 一、归一化数据格式(所有脚本通用)

```json
{
  "game": "ssq",
  "source": "opencai",
  "records": [
    {"issue": "2024085", "date": "2024-07-28", "pools": {"red": [1,2,3,4,5,6], "blue": [9]}},
    {"issue": "2024084", "date": "2024-07-25", "pools": {"red": [...], "blue": [...]}}
  ]
}
```

- 多池彩种(双色球/大乐透/七乐彩): `pools` 含 `red`/`blue` 或 `front`/`back` 或 `main`/`special`。
- 单池彩种(3D/排列/七星/快乐8): `pools` 含 `main`。
- 字段顺序建议由旧到新或由新到旧均可, 脚本内部按数组顺序处理。

## 二、在线数据源(脚本内置尝试顺序)

> 公开彩票接口经常调整路径或增加反爬, 以下端点可能变动。脚本对每次请求做异常兜底,
> 任一可用即采用, 全部失败则提示改用 `--local` 导入已有文件。

### 1. 开彩网 opencai.net(推荐, 结构最规整)
- 地址: `https://www.opencai.net/api/lottery/?name=<api名>&num=<期数>`
- 返回(示例): `{"code":0,"data":[{"expect":"2024085","opencode":"01,02,03,04,05,06+07","opentime":"2024-07-28 21:15:00"}]}`
- 彩种名映射: ssq→ssq, dlt→dlt, qlc→qlc, kl8→kl8, fc3d→fc3d, pl3→pl3, pl5→pl5, qxc→qxc。
- `opencode` 用 `+` 分隔主池与副池; 双色球/大乐透/七乐彩按此拆分, 其余为单池。

### 2. 500 彩票 datachart.500.com(HTML 抓取, 脆弱)
- 地址: `https://datachart.500.com/<game>/history/newinc/history.php?start=...&end=...`
- 返回 HTML 表格, 需解析期号与开奖号; 页面结构变动时可能失效。

### 3. 官方站点(中彩网 / 体彩网)
- 中彩网 `https://www.cwl.gov.cn/`、体彩网 `https://www.lottery.gov.cn/`
- 官方数据最权威, 但多需配合具体 API 路径、Cookie / 请求头; 路径常随改版变化,
  脚本内置的兜底请求可能 404。若需稳定, 建议用浏览器/F12 抓取接口后写入本地文件。

## 三、本地文件导入(最稳妥)

当在线源不可达时, 直接把已有的开奖数据整理成上面的归一化 JSON(或 CSV)后:

```bash
python fetch_history.py --local mydata.json --out ssq_history.json   # 仅做格式校验/复制
python analyze.py --data ssq_history.json
python generate.py --game ssq --data ssq_history.json --strategy hot
```

CSV 字段约定: `issue,date,red,blue`(双色球) 或 `issue,date,main`(单池), 号码用逗号分隔。

## 四、获取足量样本的建议
- 分析统计建议至少 50–100 期; 概率/期望计算无需历史数据(纯组合数学)。
- 冷号、遗漏等指标依赖样本量, 样本过小会失真。
- 本 skill 自带 `assets/sample_ssq.json`(30 期示例)用于离线试用脚本。
