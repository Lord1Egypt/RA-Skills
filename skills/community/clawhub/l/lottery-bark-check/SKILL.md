---
name: lottery-bark-check
description: 中国彩票开奖核对与 Bark 推送技能。必须配合 Bark App 使用：抓取中彩网（双色球）与 500 网（大乐透）官方最新开奖，与用户守号比对，判定奖级与金额，按定稿蓝黑版式生成报告，并通过 Bark 推送（group 固定「彩票」，需自备 Bark device_key）到手机，每天定时核对不漏期。关键词：彩票、双色球、大乐透、开奖号码、守号核对、中奖查询、Bark 推送、Bark device_key、开奖提醒、定时提醒。
version: 1.0.0
license: MIT
---

# 彩票开奖核对与 Bark 推送（lottery-bark-check）

把你守的那注号码交给它，每天开奖后自动核对，中没中、中几等奖、多少钱，一条推送到手机。

- **真实数据**：双色球取自中彩网官方接口，大乐透取自 500 网历史开奖页，不猜不编。
- **零依赖**：只用 Python 3 标准库 + `curl`，不需要装任何包。
- **零配置起步**：一条 `--init` 生成配置模板，填上 Bark device_key 和守号即可。
- **版式固定**：内置排版校验，版式走样直接拒绝推送，不会被随意改动。

## 前提：推送必须有 Bark

这个技能只负责「核对 + 生成内容」，**把内容送到你手机上这一步，只走 Bark 一个通道**（不接微信、不接 Server酱、不发邮件）。

| 你需要准备 | 说明 |
|---|---|
| Bark App | iPhone 在 App Store 搜「Bark」安装；安卓可用 Bark 官方安卓版或自建兼容服务。装好打开首页即可看到推送地址 |
| device_key | 推送地址形如 `https://api.day.app/AbCdEf12/`，中间的 `AbCdEf12` 就是你的 device_key。每人一个，互不影响 |
| 网络 | 只往 `api.day.app` 发一条 HTTPS 请求，结果不经过任何第三方服务器 |

没有 Bark 也能跑：加 `--dry-run` 只在本机打印核对结果，不推送。**但要收到手机通知，必须先有 Bark 和自己的 device_key。** 缺少 key 时脚本直接报错退出，不会静默失败。

## 安装

```bash
# 方式一：把技能目录放进技能库
cp -r lottery-bark-check ~/.codebuddy/skills/          # CodeBuddy
cp -r lottery-bark-check ~/.workbuddy/skills/          # WorkBuddy

# 方式二：直接单文件运行（不装技能也能用）
python3 lottery-bark-check/scripts/lottery_check.py --help
```

## 三步用起来

```bash
# 1. 生成配置（默认写到 ~/.lottery/config.json）
python3 scripts/lottery_check.py --init

# 2. 填 Bark device_key 与守号（或走环境变量）
export BARK_DEVICE_KEY='你的BarkKey'
python3 scripts/lottery_check.py --ssq "03 04 11 12 13 28 + 01" \
                                 --dlt "03 04 11 13 28 + 01 12" --dry-run   # 只预览

# 3. 去掉 --dry-run 即真实推送
python3 scripts/lottery_check.py
```

`device_key` 在 Bark App 首页的推送地址里（`https://api.day.app/XXXXXXXX/`）。多注守号用 `;` 分隔，如 `"03 04 11 12 13 28 + 01; 01 02 03 04 05 06 + 07"`。

## 参数

| 参数 | 说明 |
|---|---|
| `--ssq "6红 + 1蓝"` | 双色球守号，多注用 `;` 分隔，覆盖配置文件 |
| `--dlt "5前 + 2后"` | 大乐透守号，多注用 `;` 分隔，覆盖配置文件 |
| `--config PATH` | 指定配置文件（默认 `~/.lottery/config.json`） |
| `--dry-run` | 只渲染并打印 payload（密钥脱敏），不推送 |
| `--date YYYY-MM-DD` | 复测指定日期，用于回溯核对 |
| `--init` | 生成示例配置文件 |

## 配置文件

```json
{
  "bark_device_key": "你的BarkKey",
  "group": "彩票",
  "level": "timeSensitive",
  "sound": "bell",
  "notes": {
    "ssq": [{"red": [3, 4, 11, 12, 13, 28], "blue": [1]}],
    "dlt": [{"front": [3, 4, 11, 13, 28], "back": [1, 12]}]
  }
}
```

优先级：命令行参数 > 环境变量 `BARK_DEVICE_KEY` > 配置文件。

## 推送长什么样

```text
彩票 11/14 周六 · 大乐透        ← 标题（只写当日开奖彩种）
未中奖                          ← 副标题
开奖 01 07 11 27 29 + 02 06    ← 开奖号全部蓝色
我的 03 04 11 13 28 + 01 12    ← 只有命中的号蓝色，其余黑色
合计 1+0 → 未中奖
本期总计 ¥0
```

中奖时「合计」行变为 `合计 6+1 → 中奖 一等奖 ¥10,000,000`（中奖与金额蓝色加粗），副标题变为「中奖」。多注守号时每注前加 ①②③ 序号。

## 开奖日与推送策略

| 彩种 | 开奖日 |
|---|---|
| 双色球 | 周二、周四、周日 21:15 |
| 大乐透 | 周一、周三、周六 21:25 |

- 周五两彩种均不开奖 → 只发一条「周五不开奖」纯文字。
- 开奖日但官方数据尚未发布 → 自动重试（最多 3 轮，间隔 90 秒），仍无数据则发「开奖数据暂未更新」，不编造。
- 其它非开奖日不推送，不打扰。

## 定时运行

```bash
# crontab：每天 22:30
30 22 * * * BARK_DEVICE_KEY=你的Key /usr/bin/python3 /path/to/scripts/lottery_check.py >> ~/.lottery/run.log 2>&1
```

在 WorkBuddy / CodeBuddy 里也可以直接建一个「每天 22:30」的自动化任务，让 Agent 运行本技能。

## 排版与配色（为什么是这个样子）

Bark 的 markdown 没有任何自定义颜色参数，唯一能出现的彩色是「链接蓝」。所以：

- **开奖行全部蓝色**：每个号码写成 `[NN](https://bark.day.app)`。
- **我的行只有命中的号蓝色**，其余纯文本（黑色）。
- 蓝字用链接实现，字体与黑字一致，代价是自带下划线——这是刻意取舍，换来两行字体统一。
- 号码之间插入不可见词连接符 `U+2060`，否则 iOS 会把「连续多组两位数」识别成电话号码而**整行误染蓝**。这是本技能最容易踩的坑。
- 详细源码级考证见 `references/bark-markdown.md`。

推送前会跑 `validate_layout()`：正文必须是「开奖 →（我的 → 合计）× N → 本期总计」结构，不符就报错拒发。

## 免责声明

本项目仅用于个人核对自己购买的彩票，数据来自公开页面，可能存在延迟或解析偏差，**一切以中国福利彩票 / 中国体育彩票官方公告为准**。请理性购彩，未满 18 周岁禁止购买彩票。

## 许可

MIT
