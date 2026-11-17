# lottery-bark-check

> 守号交给它，开奖后一条推送：中没中、中几等奖、多少钱。

中国彩票（双色球 / 大乐透）开奖自动核对 + Bark 推送。抓官方数据、比对守号、算奖级金额、按固定版式推送，全程零依赖。

## 前提：推送依赖 Bark

**本技能的推送只走 Bark 一个通道**，不接微信、不接 Server酱。使用前你需要：

1. 装 Bark App —— iPhone 在 App Store 搜「Bark」；安卓可用 Bark 官方安卓版或兼容服务；
2. 拿到自己的 device_key —— 打开 Bark 首页，推送地址形如 `https://api.day.app/AbCdEf12/`，中间那段就是；
3. 把它放进环境变量 `BARK_DEVICE_KEY`，或写进 `~/.lottery/config.json`。

没有 Bark 也能用：`--dry-run` 只在本机打印核对结果，不推送。要收到手机通知则必须配置 key，缺 key 时脚本会直接报错退出。

## 安装（二选一）

```bash
# A. 作为 Agent 技能
unzip lottery-bark-check.skill -d ~/.codebuddy/skills/        # CodeBuddy
unzip lottery-bark-check.skill -d ~/.workbuddy/skills/        # WorkBuddy

# B. 当普通脚本用
python3 scripts/lottery_check.py --init
```

## 30 秒上手

```bash
export BARK_DEVICE_KEY='你的BarkKey'
python3 scripts/lottery_check.py --ssq "03 04 11 12 13 28 + 01" --dry-run
python3 scripts/lottery_check.py            # 去掉 --dry-run 即推送
```

## 每天自动跑

```bash
# crontab -e
30 22 * * * BARK_DEVICE_KEY=你的Key /usr/bin/python3 /path/to/lottery_check.py >> ~/.lottery/run.log 2>&1
```

## 特性

- 双色球取中彩网官方接口，大乐透取 500 网历史页，全部真实数据
- 开奖日 21:15 / 21:25 后数据未更新会自动重试 3 轮（间隔 90 秒）
- 周五只发「周五不开奖」，非开奖日静默
- 版式锁定：结构不符拒绝推送；号码间插 U+2060 防止 iOS 误染蓝
- device_key 只从环境变量或配置文件读取，日志与预览一律脱敏

## 文件结构

```
lottery-bark-check/
├── SKILL.md                    # 技能说明（Agent 读取）
├── scripts/lottery_check.py    # 主脚本，零依赖
├── examples/config.example.json
└── references/bark-markdown.md # Bark 配色/字体源码级考证
```

## 免责声明

仅供个人核对，数据以官方公告为准。理性购彩，未满 18 周岁禁止购买彩票。

MIT License
