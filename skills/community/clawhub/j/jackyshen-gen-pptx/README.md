# **AI驱动的演示文稿生成专家** — 将你的想法一键转化为商业级 PPT 格式幻灯片


## ✨ 核心优势

| 优势 | 说明 |
|------|------|
| 🎨 **多风格设计** | 支持手绘插画、商务简约、活力撞色等10+种配色方案 |
| 📐 **智能布局** | 基于16宫格网格的自动排版和关系图设计，告别杂乱排布 |
| 🤖 **AI全流程** | 从Story Line提炼到图片生成，全流程自动化 |
| ✅ **QA验证闭环** | 自动化内容检查 + 视觉审查，确保输出质量 |
| 📝 **演讲者注释** | 每页幻灯片自动附带口播稿和制作备注 |

---

## 🎯 与众不同

### 普通PPT工具 vs 我们的Skill

| 功能 | 普通工具 | pptx-gen Skill |
|------|----------|----------------|
| 内容提炼 | 手动复制粘贴 | AI自动分析素材提炼Story Line |
| 图片素材 | 手动搜索下载 | AI生图 + 版权图库双通道 |
| 配色方案 | 默认蓝色调 | 10+精选配色，按主题智能匹配 |
| 布局排版 | 手动拖拽对齐 | 16宫格网格自动布局 |
| 质量检查 | 人工肉眼检查 | 内容QA + 视觉QA双重验证 |
| 导出格式 | 仅PPTX | 一键生成可分享的PDF/图片 |

---

## 📖 快速开始

### 一键安装 Skill
`npx skills add https://github.com/mebusw/jackyshen-gen-pptx`


### 环境要求

- **Node.js 22+** (支持ES Module)
- **macOS/Linux/Windows** 均支持


### 安装依赖 （智能体会自行安装）
```bash
cd scripts/
pnpm i 2>&1 || npm i
```

## 工作流程

```
用户输入素材
     ↓
Task 0: 图片规划 (并行生成)
     ↓
Task 1: 提炼Story Line
     ↓
Task 2: 设计每页内容与布局
     ↓
Task 3: 生成PPT代码
     ↓
Task 4: QA验证
     ↓
输出: output.pptx +规范文档
```

---

## 🎨 设计风格

### 支持的主题配色

| 主题 | 配色 |
|------|------|
| **Midnight Executive** | 深蓝 + 冰蓝 + 白 |
| **Forest & Moss** | 森林绿 + 苔藓绿 + 米白 |
| **Coral Energy** | 珊瑚红 + 金色 + 藏青 |
| **Warm Terracotta** | 陶土红 + 沙色 + 灰绿 |
| **Ocean Gradient** | 深海蓝 + 青色 + 午夜蓝 |
| **Charcoal Minimal** | 炭灰 + 浅灰 + 黑 |
| **Sage Calm** | 鼠尾草绿 + 尤加利 + 板岩色 |
| **Cherry Bold** | 樱桃红 + 暖白 + 藏青 |
| **优普丰品牌** | 深海蓝 + 钢蓝 + 金色 / 橙粉 |

### 手绘插画风格 (默认)

```
背景色: #F9F7F2 (米白水彩纸纹理)
标题: 演示悠然小楷 (36-44pt)
正文: 圆润无衬线体 (14-16pt)
点缀: 珊瑚红 #FF7F7F / 鼠尾草绿 #8FA87A
```

---

## 📁 输出文件

```
pptx-gen-{TIMESTAMP}/
├── output.mjs          # PPT生成代码
├── output.pptx         # 最终幻灯片
├── output.mjson        # 布局规范文档
└── images/ # 生成图片素材
```

---

## 🔧 技术栈

- **PPT引擎**: [PptxGenJS 3.0+](https://gitbrent.github.io/PptxGenJS/)
- **AI生图**:  chatgpt-image / seedance / wanx-img / huny-img (任选)
- **图标库**: react-icons (Font Awesome, Material Design, etc.)
- **格式**: PPTX / PDF / PNG

---

## ⚠️ 常见问题

**Q: 生成的PPT打开报错？**
A: 检查颜色值是否使用6位hex格式（如 `FF0000`），不要带 `#` 前缀

**Q: 图片显示不出来？**
A: 确保使用 `path` 参数而非 `url`，图片路径使用相对路径

**Q: 文字被截断？**
A: 检查字号是否在合理范围，调整文本框宽度或字号大小

---
## References

[![PowerPoint Generation](https://img.shields.io/badge/PowerPoint-生成-FF7F7F?style=for-the-badge)](https://pptxgen.js.org/)
[![PptxGenJS](https://img.shields.io/badge/PptxGenJS-3.0+-1E2761?style=for-the-badge)](https://gitbrent.github.io/PptxGenJS/)



---

## 📄 License

MIT