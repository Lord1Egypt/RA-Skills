# Knowledge Card Factory - 使用示例

本文档提供 Knowledge Card Factory 的详细使用示例。

---

## 示例 1: AI 行业趋势卡片

### 用户指令
```
帮我制作一张关于「AI Agent 发展趋势」的知识卡片，发到小红书
```

### 执行过程

#### Stage 1: 热点发现
```bash
# brave-search 搜索热点
搜索关键词: "AI Agent 发展趋势 2026"
结果数量: 10 条

发现热点:
1. 多模态 Agent 成为主流
2. Agent 编排框架兴起
3. 企业级 Agent 平台爆发
4. Agent 安全与合规受关注
5. Agent 开发工具链成熟
```

#### Stage 2: 内容深挖
```bash
# agent-reach 跨平台抓取
平台: Twitter/X, 小红书, 公众号

核心观点:
- 多模态能力成为 Agent 标配
- Agent 间协作需要标准化协议
- 企业部署关注安全与可控性
- 低代码 Agent 开发平台兴起

数据点:
- 2026 年 Agent 市场规模预计 $150 亿
- 60% 企业已试点 AI Agent
- 平均 Agent 部署周期缩短至 2 周
```

#### Stage 3: 卡片创作
```bash
# nano-banana-pro 生成配图
风格: 赛博朋克
尺寸: 1024x1024

# card-renderer 渲染卡片
模板: 知识卡片模板
内容: 5 大趋势 + 数据可视化

生成文案:
标题: 2026 AI Agent 五大趋势，你准备好了吗？

正文:
🤖 AI Agent 正在重塑我们的工作方式...

标签: #AI #Agent #人工智能 #效率工具
```

#### Stage 4: 多端发布
```bash
# xiaohongshu-mcp 发布
平台: 小红书

发布结果:
✅ 发布成功
🔗 链接: https://xiaohongshu.com/note/xxx
📊 预估曝光: 5000+
```

---

## 示例 2: 天气出行指南

### 用户指令
```
帮我做一张北京周末出行天气指南卡片
```

### 执行过程

#### Stage 1: 数据获取
```bash
# weather 获取天气
城市: 北京
日期: 本周六、周日

天气数据:
周六: 晴，18-25°C，空气质量优
周日: 多云，16-22°C，有轻微雾霾

# brave-search 搜索景点
热门景点: 颐和园、故宫、798艺术区、三里屯
```

#### Stage 2: 内容整合
```bash
# 生成推荐
周六推荐:
- 户外活动: 颐和园踏青
- 适合: 拍照、散步、划船

周日推荐:
- 室内活动: 798艺术区看展
- 适合: 艺术、咖啡、打卡

穿搭建议:
- 春秋过渡季，建议薄外套
- 周日注意防护
```

#### Stage 3: 卡片生成
```bash
# card-renderer 渲染
风格: 清新简约
模板: 天气出行指南

输出: beijing-weekend-guide.png
```

---

## 示例 3: 技术知识卡片

### 用户指令
```
帮我做一张「Rust vs Go 性能对比」的技术卡片
```

### 执行过程

#### Stage 1: 技术调研
```bash
# brave-search 技术搜索
关键词: "Rust vs Go performance benchmark 2026"

发现对比点:
- 内存占用: Rust 更低
- 编译速度: Go 更快
- 运行性能: Rust 略胜
- 并发模型: 各有优势
- 学习曲线: Go 更平缓
```

#### Stage 2: 数据整理
```bash
# benchmark 数据
内存占用 (Web Server):
- Rust: 15MB
- Go: 45MB

编译时间 (100k lines):
- Rust: 120s
- Go: 8s

HTTP 吞吐量:
- Rust: 280k req/s
- Go: 250k req/s
```

#### Stage 3: 卡片创作
```bash
# nano-banana-pro 生成技术风格配图
风格: 简洁科技风
元素: 代码、性能图表

# 文案生成
标题: Rust vs Go: 2026 年度性能对决

关键结论:
✅ 追求极致性能 → 选 Rust
✅ 追求开发效率 → 选 Go
✅ 大型后端项目 → 看团队背景

标签: #Rust #Go #编程 #性能优化
```

---

## 示例 4: 产品发布海报

### 用户指令
```
帮我做一张「新产品上线」的宣传海报
```

### 执行过程

#### Stage 1: 产品信息收集
```bash
# 用户输入产品信息
产品名称: AI Assistant Pro
核心功能: 智能对话、文档处理、代码生成
目标用户: 开发者、内容创作者
价格: $9.9/月
```

#### Stage 2: 卖点提炼
```bash
# 核心卖点
1. 🚀 10倍效率提升
2. 📝 一键文档生成
3. 💻 智能代码补全
4. 🔒 端到端加密安全

# 竞品对比
vs ChatGPT: 更专注开发者场景
vs Claude: 更轻量、更快
vs Cursor: 不依赖 IDE
```

#### Stage 3: 海报生成
```bash
# nano-banana-pro 生成海报
风格: 现代科技
元素: 产品界面截图、功能图标

# 文案
标题: AI Assistant Pro 正式上线 🎉

副标题: 让 AI 成为你的超级搭档

CTA: 立即体验 → ai-assistant.pro

限时优惠: 首月 5 折
```

#### Stage 4: 多渠道发布
```bash
# 发布到多个平台
✅ 小红书: 已发布
✅ 公众号: 草稿已保存
✅ 微博: 已发布
✅ 飞书文档: 已归档
```

---

## 高级用法

### 自定义工作流

```json
{
  "custom_workflow": {
    "skip_stages": ["research"],
    "custom_content": "用户提供的原始内容",
    "style_override": "minimalist",
    "publish_later": true
  }
}
```

### 批量生产

```bash
# 批量生成多个主题卡片
topics = ["AI趋势", "Rust教程", "产品设计", "效率工具"]

for topic in topics:
    workflow.run(topic)
```

### 定时任务

```bash
# 每日热点卡片
cron: "0 9 * * *"
task: "生成昨日 AI 热点卡片并发布"
```

---

## 输出文件结构

```
output/
└── 2026-03-22/
    ├── ai-agent-trends/
    │   ├── card.png          # 知识卡片
    │   ├── caption.txt       # 配套文案
    │   ├── sources.json      # 内容来源
    │   └── publish_log.json  # 发布记录
    ├── beijing-weather/
    │   └── ...
    └── rust-vs-go/
        └── ...
```

---

## 常见问题

### Q: 生成的内容质量如何保证？
A: 系统默认开启 `require_confirmation`，所有内容需用户确认后才会发布。

### Q: 支持哪些发布平台？
A: 目前支持小红书，可通过扩展技能支持更多平台。

### Q: 图片版权如何处理？
A: AI 生成的图片可自由使用，但建议标注「AI 生成」。

### Q: 可以自定义卡片模板吗？
A: 可以，在 `templates/` 目录添加自定义模板即可。