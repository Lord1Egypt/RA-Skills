# 24 个内置模板

## 模板列表

| ID | 名称 | 风格描述 | 推荐场景 |
|----|------|----------|----------|
| `apple-notes` | Apple Notes | 简洁白色背景，类似苹果备忘录 | 知识笔记、读书笔记 |
| `xiaohongshu` | 小红书 | 经典小红书风格，温暖配色 | 生活方式、美妆、穿搭 |
| `instagram` | Instagram | 现代、简约、高对比度 | 时尚、旅行、摄影 |
| `dreamy` | 梦幻 | 柔和渐变，梦幻紫粉色调 | 情感、治愈、少女心 |
| `nature` | 自然 | 绿色系，自然清新 | 户外、健康、环保 |
| `minimalist` | 极简主义 | 黑白灰，极简设计 | 科技、商业、专业内容 |
| `minimal` | 简约 | 简洁现代，留白多 | 通用场景 |
| `notebook` | 笔记本 | 横线纸张效果 | 学习笔记、日记 |
| `coil-notebook` | 线圈笔记本 | 带装订线的笔记本效果 | 手账、学习记录 |
| `business` | 商务 | 专业商务风格 | 职场、商业分析 |
| `typewriter` | 打字机 | 复古打字机效果 | 文艺、复古、诗歌 |
| `watercolor` | 水彩 | 水彩晕染效果 | 艺术、创意、情感 |
| `fairytale` | 童话 | 可爱童话风格 | 亲子、童话故事 |
| `japanese-magazine` | 日系杂志 | 日系杂志排版 | 时尚、生活美学 |
| `traditional-chinese` | 国风 | 中国传统元素 | 传统文化、诗词 |
| `art-deco` | 装饰艺术 | Art Deco 几何风格 | 复古、奢华、设计 |
| `pop-art` | 波普艺术 | 波普艺术色彩 | 创意、潮流、年轻 |
| `cyberpunk` | 赛博朋克 | 霓虹灯、科技感 | 科技、游戏、未来 |
| `darktech` | 暗黑科技 | 深色科技风 | 技术、编程、极客 |
| `glassmorphism` | 玻璃拟态 | 毛玻璃效果 | 现代 UI、设计趋势 |
| `warm` | 温暖 | 暖色调温馨风格 | 家居、美食、亲情 |
| `meadow-dawn` | 草原黎明 | 柔和自然色调 | 自然、疗愈、清晨 |
| `bytedance` | 字节跳动 | 字节跳动品牌风格 | 互联网、科技 |
| `alibaba` | 阿里巴巴 | 阿里巴巴品牌风格 | 电商、商业 |

## 主题模式支持

大部分模板支持 `light` 和 `dark` 两种模式：

```bash
# 亮色模式
--mode light

# 暗色模式
--mode dark
```

**注意**：部分模板仅支持 `light` 模式，使用 `dark` 模式时会自动回退到 `light` 并输出告警。

## 模板预览

### 预览命令

使用预置文案快速预览模板效果：

```bash
node scripts/xhs-card.cjs render ./assets/preview-template.md \
  --theme <模板ID> \
  --mode light \
  --split none \
  --output ./output/preview-<模板ID>
```

### 批量预览所有模板

```bash
for theme in apple-notes xiaohongshu instagram dreamy nature minimalist; do
  node scripts/xhs-card.cjs render ./assets/preview-template.md \
    --theme $theme \
    --mode light \
    --split none \
    --output ./output/preview-$theme
done
```

## 模板选择建议

### 按内容类型选择

| 内容类型 | 推荐模板 |
|----------|----------|
| 知识笔记 | apple-notes, notebook, coil-notebook |
| 生活方式 | xiaohongshu, warm, meadow-dawn |
| 时尚穿搭 | instagram, japanese-magazine |
| 科技数码 | minimalist, cyberpunk, darktech |
| 文艺情感 | typewriter, watercolor, dreamy |
| 商业职场 | business, bytedance, alibaba |
| 传统文化 | traditional-chinese |
| 创意设计 | pop-art, art-deco, glassmorphism |

### 按目标受众选择

| 受众 | 推荐模板 |
|------|----------|
| 年轻女性 | xiaohongshu, dreamy, fairytale |
| 职场人士 | business, minimalist, apple-notes |
| 设计师 | pop-art, glassmorphism, art-deco |
| 程序员 | darktech, cyberpunk, minimalist |
| 学生群体 | notebook, coil-notebook, apple-notes |

## 自定义模板

如需自定义模板，可在 `assets/templates/` 目录下创建新的 HTML 文件：

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    :root {
      --bg-color: #ffffff;
      --text-color: #333333;
      --accent-color: #ff4f81;
    }
    .card {
      width: 440px;
      min-height: 586px;
      background: var(--bg-color);
      padding: 24px;
    }
    /* 更多样式... */
  </style>
</head>
<body>
  <div class="card">
    <div class="card-content">
      <!-- 内容区域 -->
    </div>
  </div>
</body>
</html>
```
