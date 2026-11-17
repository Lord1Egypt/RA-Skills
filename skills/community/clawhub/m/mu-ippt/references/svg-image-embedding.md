> 通用技术约束请参阅 shared-standards.md。

# SVG 图片嵌入指南

SVG 文件中添加图片的技术规范和推荐工作流。

---

## 图片资源清单格式

在设计规范与内容大纲中定义；每张图片都有状态标注。如果图片方案包含"B) 用户自备"，必须在 Strategist 完成八项确认后立即运行 `analyze_images.py`，并在输出设计规范之前完成清单。

```markdown
| Filename | Dimensions | Purpose | Status | Generation Description |
|----------|-----------|---------|--------|----------------------|
| cover_bg.png | 1280x720 | 封面背景 | Pending | 现代科技感抽象背景，深蓝渐变 |
| product.png | 600x400 | 第 3 页 | Existing | - |
| team.png | 600x400 | 第 5 页 | Placeholder | 团队协作场景（后续补充） |
```

### 三种状态类型

| 状态 | 含义 | Executor 处理方式 |
|------|------|------------------|
| **Pending** | 需要 AI 生成，有描述 | 先将图片生成到 `images/`，再用 `<image>` 引用 |
| **Existing** | 用户已有图片 | 放入 `images/`，用 `<image>` 引用 |
| **Placeholder** | 尚未处理 | 使用虚线边框占位符；后续替换 |

---

## 工作流

```
1. Strategist 确定图片需求 → 添加图片资源清单，标注每项状态
2. 图片准备（pending/existing） → 放入 project/images/
3. Executor 生成 SVG（svg_output/）
   ├── Existing/Pending → <image href="../images/xxx.png" .../>
   └── Placeholder → 虚线边框 + 描述文字
4. 预览：python3 -m http.server -d <project_path> 8000 → /svg_output/<filename>.svg
5. 后处理与导出
   ├── python3 scripts/finalize_svg.py <project_path>
   └── python3 scripts/svg_to_pptx.py <project_path> -s final
```

> 建议：生成阶段在 `svg_output/` 中保持外部引用。后处理时 `finalize_svg.py` 会自动将图片嵌入到 `svg_final/`，然后从 `svg_final/` 导出 PPTX。

---

## 外部引用 vs Base64 嵌入

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **外部引用** | 文件体积小、迭代快、易于替换 | 预览需要从项目根目录启动 HTTP 服务 | `svg_output/` 开发阶段 |
| **Base64 嵌入** | 单文件自包含、导出稳定 | 文件体积大 | `svg_final/` 交付阶段 |

---

## 方法一：外部引用（推荐用于生成阶段）

### 语法

```xml
<image href="../images/image.png" x="0" y="0" width="1280" height="720"
       preserveAspectRatio="xMidYMid slice"/>
```

### 关键属性

| 属性 | 说明 | 示例 |
|------|------|------|
| `href` | 图片路径（相对或绝对） | `"../images/cover.png"` |
| `x`、`y` | 图片左上角位置 | `x="0" y="0"` |
| `width`、`height` | 图片显示尺寸 | `width="1280" height="720"` |
| `preserveAspectRatio` | 缩放模式 | `"xMidYMid slice"` |

### preserveAspectRatio 常用值

| 值 | 效果 |
|----|------|
| `xMidYMid slice` | 居中裁切（类似 CSS `cover`） |
| `xMidYMid meet` | 完整显示（类似 CSS `contain`） |
| `none` | 拉伸填充，不保持宽高比 |

### 预览方式

浏览器安全策略会阻止直接打开的 SVG 加载外部图片。需要从项目根目录启动 HTTP 服务：

```bash
python3 -m http.server -d <project_path> 8000
# 访问 http://localhost:8000/svg_output/your_file.svg
```

---

## 方法二：Base64 嵌入（推荐用于交付阶段）

### 语法

```xml
<image href="data:image/png;base64,iVBORw0KGgo..." x="0" y="0" width="1280" height="720"/>
```

### MIME 类型

| MIME 类型 | 文件格式 |
|----------|---------|
| `image/png` | PNG |
| `image/jpeg` | JPG/JPEG |
| `image/gif` | GIF |
| `image/webp` | WebP |
| `image/svg+xml` | SVG |

---

## 转换流程

### 推荐：使用 finalize_svg.py（统一流水线）

```bash
python3 scripts/finalize_svg.py <project_path>         # 图标、图片、文字、圆角矩形——一步搞定
python3 scripts/svg_to_pptx.py <project_path> -s final  # 从最终版本导出 PPTX
```

### 单独使用：embed_images.py（高级用法）

处理特定 SVG 文件而不运行完整流水线：

```bash
python3 scripts/svg_finalize/embed_images.py <svg_file>                         # 单个文件
python3 scripts/svg_finalize/embed_images.py <project_path>/svg_output/*.svg    # 批量处理
python3 scripts/svg_finalize/embed_images.py --dry-run <project_path>/svg_output/*.svg  # 预览模式
```

---

## 最佳实践

### 图片优化

嵌入前压缩图片以减小文件体积：

```bash
convert input.png -quality 85 -resize 1920x1080\> output.png  # ImageMagick
pngquant --quality=65-80 input.png -o output.png               # pngquant（推荐）
```

### 文件组织

```
project/
├── images/            # 图片素材
├── sources/           # 源文件及其附带的图片
│   └── article_files/
├── svg_output/        # 原始版本（外部引用）
└── svg_final/         # 最终版本（图片已嵌入）
```

### 圆角处理（禁止使用 clipPath）

由于 `clipPath` 与 PPT 不兼容，**禁止**使用裁切路径实现图片圆角。替代方案：
- 在图片生成时直接处理圆角（导出带圆角的 PNG）
- 或在图片上方叠加同尺寸的圆角矩形遮挡边缘（视觉模拟）

---

## 常见问题

**Q：直接打开 SVG 看不到图片？**
浏览器安全策略阻止了跨目录请求。请从项目根目录启动 HTTP 服务，或先运行 `finalize_svg.py` 然后查看 `svg_final/` 中的文件。

**Q：Base64 文件太大？**
压缩原始图片、使用 JPEG 格式、降低分辨率（匹配实际显示尺寸即可）。

**Q：如何将 Base64 反向提取为图片？**
```bash
base64 -d image.b64 > image.png
```
