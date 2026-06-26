# English Visual Vocabulary Skill

通过视觉化图片帮助记忆英语单词的智能学习工具。

## 📁 目录结构

```
english-visual-vocabulary/
├── SKILL.md                      # Skill主文档
├── README.md                     # 本文件
├── scripts/                      # 辅助脚本
│   ├── generate_card.py          # 单个单词卡片生成
│   ├── generate_cards_batch.py   # 批量卡片生成
│   ├── create_plan.py            # 学习计划创建
│   └── ebbinghaus_reminder.py    # 艾宾浩斯复习提醒
└── references/                   # 参考资源
    ├── common_roots.md           # 词根词缀手册
    ├── ebbinghaus_schedule.md    # 艾宾浩斯时间表
    └── vocabulary_lists/         # 词库
        ├── beginner.json         # 初级词汇
        ├── intermediate.json     # 中级词汇
        └── advanced.json         # 高级词汇
```

## 🚀 快速开始

### 方式一：对话式学习（推荐）

直接在对话中使用触发词：
- "帮我背单词"
- "制定一个30天英语学习计划"
- "学习单词 'serendipity'"

### 方式二：脚本工具

```bash
# 生成单个单词卡片
python scripts/generate_card.py --word "happy" --style "artistic"

# 批量生成
python scripts/generate_cards_batch.py --words "apple,banana,orange"

# 创建学习计划
python scripts/create_plan.py --days 30 --words-per-day 20

# 查看今日复习
python scripts/ebbinghaus_reminder.py --action today
```

## 🎨 图片风格

支持多种图片风格：
- `cartoon` - 卡通风格
- `realistic` - 写实风格
- `artistic` - 艺术风格
- `minimalist` - 极简风格

## 📊 核心功能

### 1. 视觉记忆
- 为每个单词生成配图
- 支持多种风格
- 通过图片建立情境关联

### 2. 词根词缀分析
- 自动拆解单词结构
- 提供词源信息
- 帮助举一反三

### 3. 艾宾浩斯复习
- 科学复习时间表
- 自动提醒
- 记忆效果追踪

### 4. 学习计划
- 个性化定制
- 每日任务管理
- 进度追踪

## 📚 词库说明

### Beginner（初级）
- 基础词汇
- 日常生活用语
- 适合英语初学者

### Intermediate（中级）
- 常见学术词汇
- 工作场景用语
- 适合有一定基础的学习者

### Advanced（高级）
- 高级学术词汇
- 文学用词
- 适合高水平英语学习者

## 💡 使用建议

1. **每日学习量**：建议20-30个新单词
2. **固定时间**：选择早晨或睡前学习
3. **主动回忆**：先看图片猜单词，再看答案
4. **及时复习**：严格按照艾宾浩斯时间表
5. **造句练习**：用新单词造3个句子

## 🔗 相关工具

- `image_generate` - 生成单词配图
- `search_images` - 搜索网络图片
- `echart` - 生成学习进度图表

## 📝 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持基础单词卡片生成
- 实现艾宾浩斯复习系统
- 提供三级词库

## 🤝 贡献

欢迎贡献：
- 添加更多词库
- 改进词根分析算法
- 优化图片生成逻辑

## 📄 许可证

MIT License

---

**开始你的视觉化词汇学习之旅！** 🎯
