---
name: yunshi
description: |
  MingLi is your all-in-one Chinese astrology and fortune-telling companion. It combines six ancient divination systems — BaZi (Four Pillars of Destiny), ZiWei DouShu (Purple Star Astrology), QiMen DunJia, I Ching (Meihua Yishu & LiuYao), marriage compatibility analysis, and feng shui — into a single skill, with no external API required.

  Every morning MingLi delivers a personalized daily fortune reading covering career, wealth, relationships, and health. Every evening it previews tomorrow's energy and lucky elements. Ask for a full BaZi chart, a ZiWei life-map reading, an I Ching divination, a marriage compatibility report, or a feng shui layout recommendation — MingLi handles them all. Built-in calculation algorithms produce accurate traditional charts instantly.

  Supports Chinese and English output. Trigger: fortune telling, BaZi, daily horoscope, ZiWei, QiMen, I Ching, divination, feng shui, marriage compatibility, lucky color, yearly luck, 算命, 八字, 今日运势, 紫微斗数, 占卜, 合婚, 风水.
keywords: BaZi, Chinese astrology, daily horoscope, fortune telling, ZiWei DouShu, four pillars of destiny, I Ching, divination, feng shui, marriage compatibility, QiMen DunJia, daily fortune, horoscope push, lucky color, yearly luck, lucky elements, astrology, Chinese zodiac, fate analysis, life reading, 八字, 算命, 今日运势, 每日运程, 紫微斗数, 奇门遁甲, 梅花易数, 六爻, 占卜, 合婚, 风水, 流年, 大运, 命理, 四柱
metadata:
  openclaw:
    runtime:
      node: ">=18"
    install:
      - kind: node
        package: iztro
    env:
      - name: OPENCLAW_KNOWLEDGE_DIR
        required: false
        description: "Optional path to ZiWei pattern knowledge base (.md files). Defaults to ~/.openclaw/workspace/knowledge. Skill degrades gracefully if absent."
---

# 运势 (YunShi)

> 私人命理顾问 — 每日运程推送 · 八字紫微 · 占卜风水

## 何时使用

- 八字/四柱排盘、流年大运分析
- 今日/近期运势（事业/财运/感情/健康）
- 紫微斗数命盘
- 合婚、双方八字相配
- 占卦（梅花易数、六爻、奇门遁甲）
- 风水布局、财位、幸运颜色
- 用户说"算命""看运势""占卜""帮我占一卦"

---

## 🌐 多语言响应规则

1. **语言跟随**：用户语言 → 全程同语言回复
2. **专有术语保留中文**：柱名/星曜/卦名保持中文原字，括号内附译文
   - 英文示例：Your Day Pillar is **甲子** (Jiǎ Zǐ — Wood Rat), indicating...
3. **脚本输出翻译**：脚本返回的中文结构由 Agent 解读后以用户语言呈现
4. **注册格式**：非中文用户使用 `Name | Gender(M/F) | BirthDate | BirthTime | BirthPlace`
5. **推送语言**：跟随档案 `language` 字段（默认 `zh`）

---

## 📖 功能列表

### 排盘

| 功能 | 命令 |
|------|------|
| 八字排盘（四柱/日主/用神/神煞） | `八字 1990-05-15 14:30` |
| 紫微斗数（命宫/十二宫/四化） | `紫微 1990-05-15 男` |
| 奇门遁甲 | `奇门 2026-03-24 15:00` |
| 择吉选日 | `择吉 2026-04 开业` |

### 分析

| 功能 | 命令 |
|------|------|
| 流年/大运/事业/财运/婚姻/健康 | `2026年运势` / `未来十年运势` / `财运好不好` |
| 合婚分析 | `合婚 张三 李四` |
| 风水分析 | `风水分析` |

### 占卜

| 功能 | 命令 |
|------|------|
| 梅花易数 | `梅花易数 3 5 2`（数字起卦）或留空时间起卦 |
| 六爻预测 | `六爻占卜` |
| 奇门占卜 | `奇门选时 明天15:00` |

### 每日运程（自动推送）

早晨 07:00 推送今日运势，晚间 20:00 推送明日预告。内容：综合指数、幸运颜色/方位/数字、今日宜忌、风险预警、吉时、每日一言。

| 推送命令 | 说明 |
|---------|------|
| `每日运势开` / `开启运势推送` | 开启 |
| `每日运势关` / `关闭运势推送` | 关闭 |
| `推送状态` | 查看当前状态 |

---

## 📦 环境依赖

- **Node.js >=18**（必须）
- `npm install` 安装 `iztro`（紫微斗数）和 `lunar-typescript`（农历转换）
- `OPENCLAW_KNOWLEDGE_DIR`：可选，紫微格局知识库，不存在时自动降级
- **推送渠道**：`telegram`/`feishu` 由 openclaw 运行时投递，skill 不调用任何渠道 API
- **新闻联动**：由 Agent 的 WebSearch 工具完成，无搜索能力时跳过
- **个人数据**：存储在 `data/profiles/<userId>.json`，含敏感信息，请确认访问权限

---

## 🛠️ 工具脚本

```bash
# 注册 / 档案
node scripts/register.js <userId> <姓名> <性别> <出生日期> <出生时间> [地点]
node scripts/profile.js show <userId>
node scripts/profile.js add <userId> spouse|child <姓名> <出生日期> <性别>

# 排盘
node scripts/ziwei.js <出生日期> <性别> [时辰]
node scripts/qimen.js [日期] [时辰]
node scripts/zhuanshi.js <YYYY-MM> <活动类型> [用户八字]
node scripts/fengshui.js [八字] [年份]

# 运程 / 合婚 / 占卜
node scripts/daily-fortune.js [日期]
node scripts/marriage.js <userId1> <userId2>
node scripts/meihua.js [数字1-3]
node scripts/liuyao.js [010203] [问题]

# 推送管理
node scripts/daily-push.js --dry-run          # 模拟推送
node scripts/daily-push.js --test <userId>    # 测试推送
node scripts/daily-push.js --list             # 查看已开启用户
node scripts/push-toggle.js on|off|status <userId>

# 偏好追踪（每次提问后调用）
node scripts/preference-tracker.js record <userId> <topic> explicit_query|topic_drill
node scripts/preference-tracker.js weights|top <userId> [N]
# topic: 财运|事业|感情|健康|婚姻|子女|官司|出行|风水
```

---

## ⏰ Cron 推送配置

```bash
openclaw cron add "0 7 * * *" "cd ~/.openclaw/workspace/skills/yunshi && node scripts/daily-push.js"
openclaw cron list
openclaw cron delete <任务ID>
```

**子时算法**：`1` = 23:00-23:59 算次日（倪海厦派）；`2` = 算当日（传统派）

---

## 📊 交叉验证权重

| 问题类型 | 八字 | 紫微 | 奇门 | 梅花 | 六爻 |
|----------|------|------|------|------|------|
| 终身命格 | 40% | 30% | - | - | - |
| 年度运势 | 40% | 30% | 20% | 10% | - |
| 事业决策 | 30% | 20% | 30% | - | 20% |
| 婚姻感情 | 40% | 30% | - | 10% | 20% |
| 当下问事 | - | - | 30% | 40% | 30% |

---

## ⚠️ 风险预警等级

🔴 严重（立即处理）· 🟡 注意（谨慎处理）· 🟢 提示（一般提醒）

类型：🚨 健康 · 💰 财务 · 💕 感情 · 💼 事业 · ⚖️ 法律

---

## 📁 数据文件

```
data/profiles/{userId}.json   # 用户档案（姓名/出生/家庭成员八字）
scripts/                      # register, ziwei, qimen, fengshui, profile,
                              # daily-fortune, marriage, meihua, liuyao,
                              # zhuanshi, daily-push, push-toggle, preference-tracker
```

---

## ⚠️ 注意事项

1. 用户数据与AI计算冲突时，以用户提供信息为准
2. 命理是参考，不是定数
3. 用户档案仅供个人使用，注意数据隐私

---

*Version: 1.1.0 · Updated: 2026-03-30*
