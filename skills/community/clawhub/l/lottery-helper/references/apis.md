# 彩票数据接口（17500.cn）

## URL 总览

所有接口：`https://data.17500.cn/{code}_{asc|desc}.txt`
- `_desc.txt` = 最新在前
- `_asc.txt` = 历史升序

| 彩种 | 代码 | URL |
|------|------|-----|
| 双色球 | ssq | https://data.17500.cn/ssq_{asc\|desc}.txt |
| 大乐透 | dlt | https://data.17500.cn/dlt_{asc\|desc}.txt |
| 排列三 | pl3 | https://data.17500.cn/pl3_{asc\|desc}.txt |
| 排列五 | pl5 | https://data.17500.cn/pl5_{asc\|desc}.txt |
| 福彩3D | fc3d | https://data.17500.cn/3d_{asc\|desc}.txt |
| 北京快乐8 | kl8 | https://data.17500.cn/kl8_{asc\|desc}.txt |
| 七乐彩 | qlc | https://data.17500.cn/7lc_{asc\|desc}.txt |
| 七星彩 | qxc | https://data.17500.cn/7xc_{asc\|desc}.txt |

## 数据格式

### 双色球（ssq）
```
期号 日期 红1 红2 红3 红4 红5 红6 蓝球 出球顺序(6红+1蓝) 投注总额 奖池金额 [各奖级...]
```
示例：`2026039 2026-04-09 08 17 18 21 25 30 05 18 21 25 17 08 30 393444014 1934981238 ...`

### 大乐透（dlt）
```
期号 日期 前区1-5 后区1-2 前区出球顺序 后区出球顺序 投注总额 奖池金额 [各奖级...]
```
示例：`26038 2026-04-11 08 17 21 33 35 06 07 21 17 35 33 08 06 07 343632778 ...`

### 排列三/3D（pl3 / fc3d）
```
期号 日期 百 十 个 投注总额 直选注数 直选金额 组三注数 组三金额 组六注数 组六金额
```
### 排列五（pl5）
```
期号 日期 万 千 百 十 个 投注总额 直选注数 直选金额
```

### 北京快乐8（kl8）
```
期号 日期 号码1-20 投注总额 奖池金额 [各奖级...]
```
每期从 01-80 中开 20 个号码。

### 七乐彩（qlc）
```
期号 日期 基本号1-7 特别码 投注总额 [一等奖...各等奖]
```
从 01-30 中开 7 个基本号 + 1 个特别码。

### 七星彩（qxc）
```
期号 日期 位1-7 投注总额 奖池金额 [各等奖...]
```
从 0-9 中选 7 位。

## 查询示例

```python
import urllib.request

def fetch_latest(code, n=1):
    url = f"https://data.17500.cn/{code}_desc.txt"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8").strip().split("\n")[:n]
```

```python
def fetch_range(code, start_date, end_date):
    url = f"https://data.17500.cn/{code}_asc.txt"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        lines = r.read().decode("utf-8").strip().split("\n")
    return [l for l in lines if start_date <= l.split()[1] <= end_date]
```
