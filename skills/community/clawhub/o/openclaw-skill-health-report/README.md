# 🏥 健康报告生成系统

> **5 分钟上手 | 一键生成 | 多端推送**
> 
> 专业的个人健康管理工具，支持胆结石/糖尿病/高血压/健身减脂等多种场景

[![Version](https://img.shields.io/badge/version-1.0.9-blue.svg)](https://github.com/tankeito/openclaw-skill-health-report/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ⚠️ 隐私与数据外发警告 (Privacy & Data Export Warning)

**本技能运行时，需要读取您本地配置的 `MEMORY_DIR` 目录下的健康记录文件。根据您的配置，生成的健康报告将通过 Webhook 自动发送至外部平台（钉钉/飞书/Telegram）。**

**安全建议**：
- ✅ 请确保您完全信任所配置的 Webhook 接收端
- ✅ 建议在沙箱或隔离环境中使用
- ✅ 谨慎配置您的私有环境变量（Webhook Token、API Key 等）
- ✅ 定期检查 Webhook 访问日志，确保无异常调用

---

## 🚀 快速开始（3 步上手）

### 步骤 1：一键安装

```bash
# 进入 OpenClaw 工作区
cd ~/.openclaw/workspace/skills

# 克隆插件
git clone git@github.com:tankeito/openclaw-skill-health-report.git health_report

# 安装依赖
pip install reportlab pillow
```

### 步骤 2：初始化配置

```bash
# 进入插件目录
cd health_report

# 运行初始化脚本（交互式问答）
python3 scripts/init_config.py
```

**脚本会自动询问**：
```
👋 欢迎使用健康报告系统！

1️⃣  您的姓名或昵称？
   > 小明

2️⃣  性别和年龄？
   > 男，30 岁

3️⃣  身高（cm）和当前体重（kg）？
   > 175, 70

4️⃣  目标体重（kg）？
   > 65

5️⃣  健康状况？（胆结石/糖尿病/高血压/健身减脂）
   > 胆结石

6️⃣  有没有不吃/过敏的食物？
   > 海鲜

✅ 配置完成！配置文件已保存到 config/user_config.json
```

### 步骤 3：测试运行

```bash
# 生成今日报告
python3 scripts/health_report_pro.py /root/.openclaw/workspace/memory/2026-03-14.md 2026-03-14
```

---

## 📊 输出示例

### 文字报告（三端推送）

```
✅ 2026-03-14 健康报告已生成！

🎯 今日综合评分：90.0/100 ⭐⭐⭐⭐

📊 分项汇总
- 饮食合规性：86.7/100 ⭐⭐⭐⭐（脂肪 38.4g 略低）
- 饮水完成度：100/100 ⭐⭐⭐⭐⭐
- 体重管理：80/100 ⭐⭐⭐⭐
- 症状管理：100/100 ⭐⭐⭐⭐⭐
- 运动管理：0/100 ⭐

🤖 AI 专属健康点评
今天你在脂肪管理上表现非常出色！38.4g 的摄入量精准落在安全区间内。
饮水 2000ml 达标，充分稀释了胆汁浓度。

但必须严肃指出两个健康隐患：
第一，膳食纤维仅 14.1g，距离 25g 的最低要求差距较大。
第二，全天零运动，久坐不动会显著降低胆囊排空效率。

📝 今日详情汇总

🥗 进食情况
- 早餐 (08:06): 清汤牛肉面、脱脂纯牛奶 250ml、鸡蛋蛋白 1 个 - 257kcal
- 午餐 (12:49): 半碗米饭（约 75g）、凉拌土豆牛肉、煎蛋青菜汤 - 332kcal
- 加餐 (17:24): 苹果 1 个（约 200g） - 52kcal
- 晚餐 (19:27): 半碗米饭（约 75g）、豆腐青菜汤、凉拌鸡肉豆干 - 195kcal

💧 饮水情况
- 晨起：250ml
- 上午：250ml
- 中午：250ml
- 下午：250ml×2
- 晚上：250ml
→ 总计：2000ml/2000ml ✅

📈 基础健康数据
- 身高：175cm
- 体重：140 斤（70kg）
- BMI：22.9
- 基础代谢 (BMR)：1562 kcal
- 每日消耗 (TDEE)：1874 kcal

📋 次日优化方案

🥗 饮食计划
- 07:30-08:00 燕麦粥 50g、脱脂牛奶 250ml、水煮蛋蛋白 2 个 等 (450kcal)
- 12:00-12:30 糙米饭 150g、清蒸鸡胸肉 120g、蒜蓉西兰花 200g 等 (720kcal)
- 18:30-19:00 蒸红薯 200g、瘦牛肉 100g、清炒青菜 200g 等 (580kcal)

💧 饮水计划
- 07:00 250ml (晨起空腹温水)
- 09:30 250ml (工作间隙)
- ...共 8 次提醒

🏃 运动建议
- 午餐后 30 分钟 饭后散步 (20-30 分钟)
- 晚餐后 30 分钟 饭后散步 (20-30 分钟)
- 工作间隙 办公室拉伸 (5-10 分钟/次)

━━━━━━━━━━━━━━━━━━

📄 PDF 完整报告
https://your-domain.com/health_report_2026-03-14.pdf
```

### PDF 报告预览

PDF 报告共 3 页，包含以下内容：

**第 1 页 - 综合评分与健康数据**
- 📊 综合评分卡片（带星级和百分比）
- 📈 基础健康数据表格（身高/体重/BMI/BMR/TDEE）
- 🔥 热量与营养素环形图

**第 2 页 - 详细记录**
- 🥗 进食详情表（食物名称/份量/热量/蛋白质/脂肪/碳水）
- 💧 饮水时间轴（每次饮水时间和毫升数）
- 🏃 运动记录（类型/时长/消耗）
- 🤖 AI 专属健康点评（150-300 字深度分析）

**第 3 页 - 次日方案**
- 🥗 饮食计划（三餐详细菜单和营养信息）
- 💧 饮水计划（8 次定时提醒）
- 🏃 运动建议（具体活动和时长）
- ⚠️ 特别关注（7 条健康提示）

**PDF 下载链接格式**：
```
https://your-domain.com/health_report_YYYY-MM-DD.pdf
```

---

## 📝 数据录入（标准化格式）

### 方式一：对话式录入（推荐）

直接告诉机器人你今天的数据：

```
你：今天早上空腹体重 140 斤

机器人：✅ 体重已记录！2026-03-14 晨起空腹：140 斤

你：早上喝了 250ml 温水

机器人：✅ 饮水已记录！当前进度：250ml/2000ml（12.5%）

你：早餐吃了清汤牛肉面，喝了 250ml 脱脂牛奶，1 个鸡蛋蛋白

机器人：✅ 早餐已记录！估算热量：257kcal
- 清汤牛肉面：约 180kcal
- 安佳脱脂纯牛奶 250ml：约 87kcal
- 鸡蛋蛋白 1 个：约 17kcal
```

### 方式二：手动编辑 Markdown 文件

在 `~/.openclaw/workspace/memory/YYYY-MM-DD.md` 文件中记录：

```markdown
# 2026-03-14 健康记录

## 📊 体重记录
**晨起空腹**：140 斤

## 💧 饮水记录
### 晨起（约 07:30）
- 饮水量：250ml
- 累计：250ml/2000ml（12.5%）

### 上午（约 10:00）
- 饮水量：250ml
- 累计：500ml/2000ml（25%）

## 🥗 饮食记录
### 早餐（08:06）
- 清汤牛肉面 → 约 180kcal
- 安佳脱脂纯牛奶 250ml → 约 87kcal
- 鸡蛋蛋白 1 个 → 约 17kcal

### 午餐（12:49）
- 半碗米饭（约 75g）→ 约 87kcal
- 凉拌土豆牛肉 → 约 180kcal
- 煎蛋青菜汤 → 约 65kcal

### 加餐（17:24）
- 苹果 1 个（约 200g）→ 约 52kcal

### 晚餐（19:27）
- 半碗米饭（约 75g）→ 约 87kcal
- 豆腐青菜汤 → 约 50kcal
- 凉拌鸡肉豆干 → 约 58kcal

## 🏃 运动记录
（今日无运动）

## 📝 症状/不适
（无不适）
```

**格式说明**：
- 食物格式：`食物名称 → 约 XXXkcal`（热量可选，系统会自动估算）
- 饮水格式：记录单次饮水量和累计进度
- 运动格式：记录类型、时长、消耗热量

---

## ⚙️ 配置说明

### 个人健康档案（`config/user_config.json`）

```json
{
    "user_profile": {
        "name": "小明",
        "gender": "男",
        "age": 30,
        "height_cm": 175,
        "current_weight_kg": 70,
        "target_weight_kg": 65,
        "condition": "胆结石",
        "activity_level": 1.2,
        "dietary_preferences": {
            "dislike": ["鱼", "海鲜"],
            "allergies": ["海鲜"],
            "favorite_fruits": ["苹果", "香蕉"]
        }
    },
    "scoring_weights": {
        "diet": 0.45,
        "water": 0.35,
        "weight": 0.20,
        "exercise_bonus": 0.10
    }
}
```

### 消息推送配置（`config/.env`）

```bash
# 钉钉 Webhook
DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"

# 飞书 Webhook
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK"

# Telegram
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_CHAT_ID"

# 健康记录目录
MEMORY_DIR="/root/.openclaw/workspace/memory"

# PDF 报告目录
REPORT_WEB_DIR="/path/to/public/dir"
REPORT_BASE_URL="https://your-domain.com"
```

---

## 🤖 定时任务

### 设置每日自动推送

```bash
# 编辑 Crontab
crontab -e

# 添加每日 22:00 推送
0 22 * * * bash /root/.openclaw/workspace/skills/health_report/scripts/daily_health_report_pro.sh
```

---

## 🛠️ 故障排查

### 问题 1：配置文件不存在

```bash
# 运行初始化脚本
python3 scripts/init_config.py
```

### 问题 2：依赖库缺失

```bash
pip install reportlab pillow
```

### 问题 3：推送失败

```bash
# 测试 Webhook
curl -X POST "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"msgtype":"text","text":{"content":"测试"}}'
```

---

## 📦 项目结构

```
health_report/
├── scripts/                    # 核心代码
│   ├── health_report_pro.py    # 主脚本
│   ├── pdf_generator.py        # PDF 生成
│   ├── constants.py            # 食物常量
│   ├── init_config.py          # 初始化脚本（小白专用）
│   └── daily_health_report_pro.sh  # 定时任务脚本
├── config/                     # 配置文件
│   ├── user_config.json        # 个人健康档案
│   ├── .env                    # 推送配置
│   └── user_config.example.json # 配置模板
├── assets/                     # 资源文件
│   └── NotoSansSC-VF.ttf       # 中文字体
├── logs/                       # 日志目录
├── README.md                   # 使用说明（本文件）
├── SKILL.md                    # 机器人交互说明
└── requirements.txt            # Python 依赖
```

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/tankeito/openclaw-skill-health-report/issues
- **作者邮箱**: tqd354@gmail.com

---

## 📄 License

MIT License
