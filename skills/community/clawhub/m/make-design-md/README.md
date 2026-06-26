# make-design-md

网站设计风格分析器 — 从网站 URL、HTML 文件或截图提取设计规范，生成符合 [Google design.md 规范](https://github.com/google-labs-code/design.md) 的结构化 DESIGN.md 文档。

## 功能

- **URL 分析** — 输入网站地址，自动抓取并提取设计令牌
- **HTML 文件分析** — 读取本地 HTML，解析 CSS 样式与结构
- **截图分析** — 从视觉截图中推断颜色、字体、间距等设计元素
- **规范输出** — 生成包含 YAML front matter 和 Markdown 正文的 DESIGN.md
- **预览生成** — 同时输出浅色/深色模式的 HTML 预览文件
- **验证导出** — 支持 Google 官方 CLI 验证格式、导出 Tailwind/DTCG 配置

## 快速开始

### 作为 Claude Code Skill 使用

在 Claude Code 中直接对话即可触发：

```
分析 https://linear.app 的设计风格，生成 DESIGN.md
```

```
分析 ./dist/index.html 的设计风格
```

```
分析 ./screenshots/homepage.png 的设计风格
```

### 使用 Google CLI 验证与导出

```bash
# 验证文档格式
npx @google/design.md lint DESIGN.md

# 导出为 Tailwind 配置
npx @google/design.md export --format tailwind DESIGN.md

# 导出为 DTCG 格式
npx @google/design.md export --format dtcg DESIGN.md
```

## 输出结构

生成的 DESIGN.md 包含：

| 部分 | 说明 |
|------|------|
| YAML Front Matter | 机器可读的设计令牌（colors, typography, spacing, rounded, components） |
| Markdown Body | 人类可读的设计原理说明 |

章节按规范顺序排列：Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts

## 字体 CDN 规则

生成网页/预览文件时，Google Fonts 必须使用国内镜像：

| 原始地址 | 替换为 |
|---------|--------|
| `fonts.googleapis.com` | `fonts.loli.net` |
| `fonts.gstatic.com` | `gstatic.loli.net` |

## 项目结构

```
├── SKILL.md                  # Skill 定义文件
├── references/
│   └── design-template.md    # DESIGN.md 文档模板
└── LICENSE                   # MIT 许可证
```

## 参考

- [Google design.md 规范](https://github.com/google-labs-code/design.md) — 官方规范仓库

## License

[MIT](LICENSE)
