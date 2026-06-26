---
name: hot-content-writer
description: "✍️ 热点文案一键生成！输入热点话题，AI自动生成小红书/抖音/公众号/微博多平台文案。支持DeepSeek API，成本极低！自媒体运营必备！免费使用，定制开发请联系作者。"
homepage: https://github.com/openclaw/hot-content-writer
metadata:
  {
    "openclaw":
      {
        "emoji": "✍️",
        "requires": { "bins": ["python3"] },
      },
  }
---

# ✍️ 热点文案生成器 v1.1

输入热点话题，AI 自动生成多平台爆款文案。支持 DeepSeek API，每次生成成本不到1分钱！

## ✨ v1.1 新功能

- 🤖 **DeepSeek API 集成** — 填入API Key即可AI智能生成
- 💰 **成本极低** — DeepSeek约1元/100万token，单次生成不到1分钱
- 📁 **config.json 配置** — 统一管理API密钥和参数
- 🔧 **更好的错误提示** — API问题一目了然

## ✨ 功能亮点

- 🎯 **多平台适配** — 小红书、抖音、公众号、微博
- 🎨 **多种风格** — 专业干货、轻松种草、幽默搞笑、情感共鸣
- 🔥 **热点联动** — 可配合热榜技能，从热点直接生成文案
- 📋 **批量生成** — 一次生成多个平台的文案
- 💡 **标题推荐** — 自动生成多个爆款标题备选

## 📦 安装

```bash
npx clawhub@latest install hot-content-writer
```

## 🔑 AI API 配置（推荐）

默认使用模板生成，配置API后效果质的飞跃！

### 方式一：config.json（推荐）

编辑 `config.json`，填入你的 DeepSeek API Key：

```json
{
  "api_provider": "deepseek",
  "api_key": "sk-你的API密钥",
  "api_base": "https://api.deepseek.com",
  "model": "deepseek-chat"
}
```

### 方式二：环境变量

```bash
export DEEPSEEK_API_KEY="sk-你的API密钥"
```

### 获取 DeepSeek API Key

1. 访问 https://platform.deepseek.com
2. 注册/登录
3. 创建API Key
4. 充值（最低10元，够用很久）

**成本参考：** DeepSeek约1元/100万token，一次文案生成约消耗500-1000 token，成本不到1分钱。

## 🚀 使用

### 单平台生成

```bash
# 小红书种草文案
python3 generate.py --topic "春天穿搭灵感" --platform xiaohongshu

# 抖音口播脚本
python3 generate.py --topic "AI工具推荐" --platform douyin

# 公众号深度文章
python3 generate.py --topic "2026年自媒体趋势" --platform gongzhonghao

# 微博短文案
python3 generate.py --topic "今日热点话题" --platform weibo
```

### 指定风格

```bash
# 干货型
python3 generate.py --topic "ChatGPT使用技巧" --platform xiaohongshu --style professional

# 种草型
python3 generate.py --topic "平价好物推荐" --platform xiaohongshu --style casual

# 搞笑型
python3 generate.py --topic "打工人日常" --platform douyin --style funny

# 情感型
python3 generate.py --topic "异地恋故事" --platform weibo --style emotional
```

### 批量生成（全平台）

```bash
# 一个话题生成所有平台文案
python3 generate.py --topic "AI取代人类工作" --all

# 指定输出文件
python3 generate.py --topic "减肥方法" --all --output content.json
```

### 联动热榜技能

```bash
# 从热榜自动取话题生成
python3 generate.py --from-hot --platform xiaohonghao --top 3

# 指定平台热榜
python3 generate.py --from-hot --source weibo --top 5 --all
```

### 其他选项

```bash
# 生成标题备选
python3 generate.py --topic "职场干货" --platform xiaohongshu --titles-only

# 指定字数
python3 generate.py --topic "读书推荐" --platform gongzhonghao --words 800

# 指定目标人群
python3 generate.py --topic "护肤" --platform xiaohongshu --audience "20-30岁女性"

# 生成多个版本
python3 generate.py --topic "科技资讯" --platform douyin --versions 3
```

### 每日自动生成（新功能 ✨）

```bash
# 获取热榜话题 → 自动生成文案 → 企微推送格式
python3 daily_content.py --top 3 --wechat-format

# 指定平台和风格
python3 daily_content.py --top 5 --platform douyin --style funny

# 输出JSON格式
python3 daily_content.py --top 3 --output daily.json

# 指定热榜来源
python3 daily_content.py --source bilibili --top 3
```

## 📊 输出示例

```json
{
  "topic": "AI工具推荐",
  "platform": "xiaohongshu",
  "style": "casual",
  "titles": [
    "🔥 5个AI神器！打工人效率翻倍的秘密",
    "后悔没早发现！这些AI工具太香了",
    "同事问我为什么准时下班，我偷偷用了这些AI工具"
  ],
  "content": "姐妹们！！！今天必须给你们安利几个我用了就离不开的AI神器...\n\n[正文内容]\n\n#AI工具 #效率提升 #打工人必备",
  "hashtags": ["#AI工具", "#效率提升", "#打工人必备"],
  "word_count": 456,
  "generated_at": "2026-03-29T21:38:00"
}
```

## 💰 版本说明

| 功能 | 免费版 | Pro版 |
|------|--------|-------|
| 单平台生成 | ✅ 每天3次 | ✅ 无限次 |
| 多平台批量 | ❌ | ✅ |
| 热榜联动 | ❌ | ✅ |
| 标题优化 | 基础 | 高级(10个备选) |
| 风格选择 | 2种 | 全部 |
| 字数控制 | ❌ | ✅ |
| 目标人群 | ❌ | ✅ |

## 🔧 自定义开发

需要更多平台支持、专属模板、或批量自动化？
- QQ: 2595075878
- 邮箱: 2595075878@qq.com

定价：
- 简单定制: 500-1000元
- 中等项目: 2000-5000元
- 大型项目: 10000元+
