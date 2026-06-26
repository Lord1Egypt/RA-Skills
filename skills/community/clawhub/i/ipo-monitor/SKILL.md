# IPO监控技能

自动监控七大交易所IPO动态，只推送昨日更新数据到飞书表格。

## 功能

- ✅ 监控上交所、深交所、北交所、港股、纳斯达克、纽交所
- ✅ 浏览器+snapshot抓取方式，稳定可靠
- ✅ 差异计算，只推送新增/更新的IPO
- ✅ 告警冷却机制，避免重复告警
- ✅ 本地SQLite备份，数据不丢失
- ✅ 支持定时任务

## 适用场景

- 金融从业者跟踪IPO动态
- 投资机构监控潜在标的
- 个人投资者关注新股上市

## 使用方法

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 修改配置文件
# 编辑 config.yaml 设置飞书webhook等

# 3. 运行
python main.py --browser
```

## 配置说明

| 参数 | 说明 |
|------|------|
| feishu_webhook | 飞书机器人Webhook地址 |
| alert_cooldown_seconds | 告警冷却时间(秒) |
| exchanges | 要监控的交易所列表 |

## 定时任务

支持三种方式：
- OpenClaw cron
- 守护进程模式
- crontab

详见 SCHEDULER.md

## 技术栈

- Python 3.x
- BeautifulSoup4 (解析)
- SQLite (本地存储)
- OpenClaw Browser (网页抓取)

## 版本

1.0.0 - 初始版本
