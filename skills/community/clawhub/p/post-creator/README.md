# Post Creator - OpenClaw 海报生成器 Skill

> 为 OpenClaw AI Agent 提供精美海报生成能力，支持中英文，多种风格

## 功能特点

- 🎨 **8种设计风格**：现代、极简、复古、中国风、科技、奢华、自然、活泼
- 🌍 **中英文支持**：无缝支持中文、英文及双语海报
- 📱 **响应式设计**：适配各种屏幕尺寸
- 🖨️ **打印就绪**：支持打印优化
- ⚡ **即开即用**：生成独立 HTML 文件，浏览器直接打开

## 安装

```bash
clawhub install post-creator
```

## 使用示例

### 基础使用

```
用户: 帮我生成一个科技风格的产品发布会海报
AI: [生成完整的HTML海报代码]
```

### 风格选择

```
用户: 我需要一张中国风的新年贺卡
用户: Create a minimalist poster for design exhibition
用户: 做一张奢华风格的品牌发布海报
```

### 自定义内容

```
用户: 生成海报：
- 标题：AI创新峰会
- 日期：2026年6月15日
- 地点：北京国家会议中心
- 风格：科技感
```

## 支持的风格

| 风格 | 适用场景 | 关键词 |
|------|----------|--------|
| 现代 | 活动、发布会 | modern, 现代, 简洁 |
| 极简 | 设计展、艺术展 | minimalist, 极简, 留白 |
| 复古 | 文化活动、怀旧 | retro, vintage, 复古, 怀旧 |
| 中国风 | 传统文化、节日 | chinese, 中国风, 传统, 中式 |
| 科技 | 科技会议、AI活动 | tech, 科技, 未来, 数字 |
| 奢华 | 品牌发布、高端活动 | luxury, 奢华, 高端, 精致 |
| 自然 | 环保、健康、户外 | nature, 自然, 绿色, 环保 |
| 活泼 | 创意活动、派对 | playful, 活泼, 创意, 趣味 |

## 输出格式

生成的海报是一个完整的 HTML 文件：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>海报标题</title>
  <style>
    /* 所有样式内联 */
  </style>
</head>
<body>
  <!-- 海报内容 -->
</body>
</html>
```

## 使用方式

1. **生成**：让 AI 生成海报代码
2. **保存**：将代码保存为 `.html` 文件
3. **打开**：在浏览器中打开文件
4. **截图**：使用截图工具保存为图片

## 文件结构

```
post-creator/
├── SKILL.md                    # 主技能定义
├── README.md                   # 本文件
├── references/
│   └── styles.md              # 风格模板参考
├── assets/
│   └── templates/             # 预设模板
└── scripts/                   # 辅助脚本
```

## 设计原则

- **自包含**：所有代码在一个文件中
- **美观**：遵循专业设计原则
- **可读**：清晰的视觉层次
- **无障碍**：确保文字可读性

## 常见用途

- 🎫 活动海报（会议、演唱会、展览）
- 🚀 产品发布（新品上市、功能更新）
- 🏷️ 促销海报（折扣、限时优惠）
- 📢 公告通知（新闻、更新、通知）
- 📱 社交媒体（Instagram、微信分享）
- 🏢 企业宣传（公司介绍、服务推广）
- 📚 教育培训（课程、工作坊）
- 🎊 节日祝福（新年、中秋、圣诞）

## 许可证

MIT License

## 贡献

欢迎贡献！请提交 PR 或 Issue 到 ClawHub 仓库。

## 相关链接

- [ClawHub](https://clawhub.ai)
- [OpenClaw 文档](https://docs.openclaw.ai)
