---
name: jiajiaoy-morning
description: |
  每日早晚全套推送 skill：
  - 08:00 早间简报（11个模块：早报/科技/财经/天气/运势/历史/菜谱/名言/正念/运动/英语）
  - 18:00 明日运势（结合八字个性化推算）
  支持任意 agent 执行，首次使用可向用户询问开关偏好后自动注册。
keywords: 早报, 简报, 晚间推送, 运势, morning, evening, 每日推送, 定时推送
metadata:
  openclaw:
    runtime:
      node: ">=18"
---

# jiajiaoy-morning — 每日早晚全套推送

## ⚠️ 首次使用：安装依赖 skill

本 skill 是**组合 skill**，依赖 11 个子 skill。首次使用前必须先安装依赖，否则脚本会报错。

**安装方法（在 skills 目录下执行）：**

```bash
# 进入 skills 目录（jiajiaoy-morning 的上级目录）
cd <skills目录>

# 一键安装所有依赖
clawhub install newstoady
clawhub install dailytech
clawhub install dailyfinance
clawhub install weather-daily
clawhub install yunshi
clawhub install daily-history
clawhub install daily-recipe
clawhub install daily-quote
clawhub install daily-mindful
clawhub install daily-fitness
clawhub install english-daily
```

> 所有依赖均已发布在 clawhub registry，可直接安装。
> 安装后目录结构应为：`skills/newstoady/`、`skills/dailytech/` ... 与 `skills/jiajiaoy-morning/` 并列。

如果缺少依赖，运行 `node scripts/build-prompts.js` 时会自动提示缺少哪些 skill 及安装命令。

---

## 触发场景

| 触发词 | 执行动作 |
|--------|---------|
| "发早报" / "今天早报" / cron 08:00 | 执行早间简报 |
| "发晚报" / "明日运势" / cron 18:00 | 执行晚间运势 |
| "设置早报" / "我想订阅" / 首次接入 | 执行安装向导 |
| "查看我的设置" | 显示当前配置 |

---

## 脚本速查

```
skills/jiajiaoy-morning/scripts/
├── setup.js         # 首次安装向导（输出问卷 / 保存配置）
├── build-prompts.js # 早间各模块 prompt 构建器
└── evening-push.js  # 晚间明日运势 prompt 生成器
```

---

## 场景一：首次安装（用户没有配置文件）

**Step 1** — 输出问卷，向用户提问：
```bash
node scripts/setup.js
```

**Step 2** — 用户回答后，将答案整理为 JSON，保存配置：
```bash
node scripts/setup.js --save '{"userId":"<id>","name":"<名字>","city":"上海","morningChannel":"telegram","morningTo":"<id>","eveningChannel":"telegram","eveningTo":"<id>","modules":{"news":true,"tech":true,"finance":true,"weather":true,"yunshi":true,"history":true,"recipe":true,"quote":true,"mindful":true,"fitness":true,"english":true,"yunshi_tomorrow":true}}'
```

**Step 3** — 脚本会输出 cron 注册指令，按指令在 openclaw 中添加两个定时任务。

---

## 场景二：早间简报执行（cron 08:00 / 手动触发）

**Step 1** — 构建所有模块 prompt：
```bash
node scripts/build-prompts.js <userId>
```

输出 JSON 数组，每项字段：
- `key` — 模块标识
- `module` — 模块名称
- `emoji` — 图标
- `group` — 分组（1/2/3）
- `prompt` — 待执行的指令（null 表示脚本出错，跳过）
- `searchRequired` — 是否需要 WebSearch
- `error` — 报错信息（仅在失败时）

**Step 2** — 按 group 依次执行每个模块的 prompt，收集结果。

**Step 3** — 按 group 分 3 条消息发送：

| 消息 | 模块 | 说明 |
|------|------|------|
| 消息1（group=1） | 📰早报 + 💻科技 + 💰财经 + 🌤️天气 | 需要 WebSearch |
| 消息2（group=2） | 🔮运势 + 📅历史 + 🍳菜谱 | 部分需搜索 |
| 消息3（group=3） | 💬名言 + 🧘正念 + 💪运动 + 📚英语 | 纯生成 |

每条消息头部格式：
```
🌅 早安 <name>！<年月日 星期X>
```

**错误处理**：某模块 prompt=null 时跳过，其余照常发送。

---

## 场景三：晚间明日运势执行（cron 18:00 / 手动触发）

**Step 1** — 生成明日运势 prompt：
```bash
node scripts/evening-push.js <userId>
```

**Step 2** — 执行输出的 prompt，结合八字推算明日运势。

**Step 3** — 发送结果。

---

## 已注册用户

| userId | 名字 | 城市 | 早间渠道 | 晚间渠道 | 开启模块 |
|--------|------|------|---------|---------|---------|
| 8603011439 | 方靖 | 上海 | Telegram | Telegram | 全部 11 项 + 明日运势 |

---

## 错误处理规则

| 错误 | 处理方式 |
|------|---------|
| 某模块脚本报错 | 跳过该模块，其余正常发送 |
| WebSearch 不可用 | 模块内标注 ⚠️，降级为知识库内容 |
| 消息超 4096 字符 | 按 group 分组已控制，单组不会超限 |
| 超时（>480s） | 已完成的 group 先发送，未完成标注缺失 |

---

## 模块开关说明

用户配置存储于：
```
skills/jiajiaoy-morning/data/users/<userId>.json
```

`modules.morning` 中各 key 设为 `false` 可关闭对应模块；
`modules.evening.yunshi_tomorrow` 设为 `false` 关闭晚间运势。

查看当前配置：
```bash
node scripts/setup.js --show <userId>
```
