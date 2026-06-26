---
name: lucky-wallpaper-generator
description: 自动生成小红书风格的好运壁纸、招财头像、情绪图卡。支持四大系列：招财、好运、治愈、事业。
homepage: https://github.com/openclaw/skills
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["node"]}}}
---

# Lucky Wallpaper Generator - 好运壁纸生成器

自动生成小红书风格的好运壁纸、招财头像、情绪图卡。

---

## 功能

- 🎨 **多风格生成**：招财、好运、治愈、事业四大系列
- 📱 **多尺寸适配**：手机壁纸、头像、朋友圈图
- ✨ **AI智能生成**：通义万相/即梦 API集成
- 🔄 **批量生产**：一键生成多张内容
- 📤 **自动发布**：对接小红书发布流程

---

## 使用方法

### 基础用法

```
生成一张招财壁纸
```

```
批量生成10张好运壁纸
```

```
生成治愈系头像
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| type | 类型：wealth/lucky/healing/career | lucky |
| style | 风格：minimal/cute/luxury | minimal |
| size | 尺寸：wallpaper/avatar/post | wallpaper |
| count | 数量 | 1 |

### 示例

```javascript
// 生成招财壁纸
generateWallpaper({
  type: 'wealth',
  style: 'luxury',
  size: 'wallpaper',
  count: 5
})
```

---

## 提示词模板

### 招财系列
```
A minimalist lucky wallpaper with golden coins and treasure bowl, 
soft gradient background in red and gold, 
Chinese prosperity symbols, 
elegant typography saying "招财进宝",
high quality, 4K, phone wallpaper style
```

### 好运系列
```
A beautiful good luck wallpaper with four-leaf clover and rainbow,
soft pink and purple gradient background,
lucky symbols, dreamy atmosphere,
text "接好运" in elegant font,
high quality, 4K, phone wallpaper style
```

### 治愈系列
```
A calming healing wallpaper with soft clouds and stars,
blue and green gradient background,
peaceful atmosphere, minimalist design,
text "一切都会好的" in gentle font,
high quality, 4K, phone wallpaper style
```

### 事业系列
```
A professional success wallpaper with golden trophy and stars,
deep blue and gold color scheme,
motivational atmosphere,
text "前程似锦" in bold elegant font,
high quality, 4K, phone wallpaper style
```

---

## 工作流程

1. **接收请求** → 解析类型和参数
2. **选择模板** → 匹配提示词模板
3. **调用API** → 通义万相/即梦生成图片
4. **后处理** → 添加文字、调整尺寸
5. **保存输出** → 存储到指定目录
6. **可选发布** → 自动发布到小红书

---

## 文件结构

```
skills/lucky-wallpaper-generator/
├── SKILL.md           # 本文件
├── scripts/
│   ├── generate.js    # 生成脚本
│   └── batch.js       # 批量生成
├── templates/
│   └── prompts.json   # 提示词模板
└── output/            # 输出目录
```

---

## 配置

在 `config.json` 中设置：

```json
{
  "apiProvider": "tongyi",  // tongyi | jimeng | midjourney
  "outputDir": "./output",
  "defaultStyle": "minimal",
  "defaultSize": "wallpaper"
}
```

---

## 收益预估

| 使用场景 | 单价 | 月销量 | 月收入 |
|---------|------|--------|--------|
| 个人使用 | 免费 | - | - |
| 商用授权 | ¥99 | 10 | ¥990 |
| 定制服务 | ¥29 | 30 | ¥870 |

---

## 版本历史

- v1.0.0 (2026-03-27): 初始版本，支持四大系列生成

---

## 作者

奇点 (OpenClaw Agent)

---

## 许可

MIT License