# Mapulse 使用教程 🇰🇷

## 安装

```bash
clawhub install mapulse
```

## 配置（只需 1 步）

```bash
mapulse setup
```

它会问你一个问题：**Telegram Bot Token**

没有 Token？3 步拿到：
1. Telegram 搜 **@BotFather**
2. 发 `/newbot`，起个名字
3. 复制 Token，粘贴到 setup

就这样。Bot 自动跑起来了。

## 验证

打开 Telegram → 找到你的 Bot → 发 `/start`

## 日常管理

```bash
mapulse status          # 看状态
mapulse logs            # 看日志
mapulse stop            # 停
mapulse start           # 启动
mapulse restart         # 重启
```

## 想要 AI 深度分析？（可选）

```bash
mapulse config ai sk-or-你的openrouter_key
mapulse restart
```

没有也行，只是少了"为什么涨/跌"的原因分析功能。

## 想要 DART 公示？（可选）

```bash
mapulse config dart 你的dart_key
mapulse restart
```

免费申请：https://opendart.fss.or.kr/

## 群组里用

```bash
mapulse config groups -100你的群组ID
mapulse restart
```

群里 @你的bot 就能触发查询。

---

完整命令列表：`mapulse help`
