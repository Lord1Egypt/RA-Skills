# luma-events-query

按 **Luma App 搜索框**的方式查 [lu.ma](https://lu.ma) 公开活动。支持杭州、重庆、上海、北京等中国大陆城市，以及东京等地。不需要 API Key。

## 安装

ClawHub（OpenClaw）：

```bash
openclaw skills install luma-events-query
```

skills.sh / 任意 Agent：

```bash
npx skills add diaoxiaoniu/luma-events-query
```

手动：把本仓库拷到你的 skills 目录。

## 用法

```bash
python3 scripts/luma-events.py search 杭州 --limit 10
python3 scripts/luma-events.py search Hangzhou --limit 10
python3 scripts/luma-events.py search 重庆 --limit 10
python3 scripts/luma-events.py search 东京 --topic AI --limit 10
```

没有 Python 时：

```bash
curl -sS "https://api.lu.ma/discover/get-paginated-events?pagination_limit=20&query=Hangzhou"
```

## 许可

MIT-0。免费使用、修改、再分发。
