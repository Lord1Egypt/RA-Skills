# 🐱🐶 Pet Emotion — AI宠物情绪识别

> WorkBuddy Skill | 拍照即得 | DashScope 多模态大模型驱动

上传猫或狗的照片，AI 自动分析宠物情绪。支持 6 种情绪分类，生成包含雷达图、置信度评分和 AI 解读的交互式 HTML 报告。

## 快速开始

### 1. 配置 API Key

编辑 `~/.workbuddy/config/dashscope.json`：
```json
{"api_key": "sk-xxxxxxxxxxxxxxxxxx"}
```

或在环境变量中设置：
```bash
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxxxx"
```

获取 Key：https://dashscope.console.aliyun.com/apiKey

### 2. 运行

```bash
python scripts/pet_emotion.py --image path/to/your_pet_photo.jpg
```

### 3. 触发词（WorkBuddy 中使用）

```
拍照识别宠物情绪  宠物情绪  宠物表情  猫咪心情  狗狗情绪
猫狗情绪  pet emotion  看看我家猫  看看我家狗  帮我看看宠物
```

## 功能

| 功能 | 说明 |
|------|------|
| 📸 拍照识别 | 上传照片，自动识别猫狗情绪 |
| 🎯 6情绪分类 | 快乐/悲伤/愤怒/恐惧/放松/警觉 |
| 📊 可视化报告 | Chart.js 雷达图 + 置信度条 + Emoji |
| 💬 AI解读 | 自然语言情绪解读和互动建议 |
| 🐱🐶 双物种 | 同时支持猫和狗 |

## 情绪分类

| 情绪 | Emoji | 典型特征 |
|------|-------|---------|
| 快乐 | 😊 | 放松姿势、尾巴摇摆、耳朵自然 |
| 悲伤 | 😢 | 耷拉耳朵、蜷缩、无精打采 |
| 愤怒 | 😠 | 龇牙、竖毛、身体僵硬 |
| 恐惧 | 😨 | 夹尾、躲藏、瞳孔放大 |
| 放松 | 😌 | 眯眼、打盹、肚皮朝上 |
| 警觉 | 🧐 | 竖耳、凝视、身体紧绷 |

## 技术栈

- **AI 模型**：DashScope qwen-vl-max（阿里通义千问多模态）
- **报告可视化**：Chart.js 雷达图 + 情绪刻度
- **图片处理**：Python Pillow + Base64 编码
- **API 协议**：OpenAI Compatible Chat Completions

## 项目结构

```
pet-emotion/
├── SKILL.md                    # WorkBuddy 技能定义
├── scripts/
│   └── pet_emotion.py          # 主脚本
├── assets/
│   └── report_template.html    # HTML 报告模板
└── references/
    └── emotion_guide.md        # 情绪解读知识库
```

## License

MIT
