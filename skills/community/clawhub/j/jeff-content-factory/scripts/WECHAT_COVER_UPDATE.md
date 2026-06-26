# 微信封面图生成功能更新说明

## 更新日期：2026-01-19

## 关键变更

### 1. 微信封面图尺寸规范
- **标准尺寸**：900 x 383 像素
- **宽高比**：约 21:9（横版）
- **格式**：PNG（推荐，支持透明度）

### 2. 设计风格规范
- **风格**：平面矢量插画风格（Flat Vector Illustration）
- **特点**：
  - 扁平化设计
  - 几何图形
  - 简洁现代
  - 商务专业

### 3. 脚本功能增强

#### 新增功能
- **自动裁剪调整**：生成图片后自动裁剪并调整到 900x386 尺寸
- **智能比例保持**：根据原图比例智能裁剪，保持主体内容
- **高质量输出**：使用 LANCZOS 算法确保缩放质量
- **可选跳过调整**：添加 `--no-resize` 参数保留原始尺寸

#### 依赖要求
- **必需**：`requests` 库（API 调用）
- **可选**：`Pillow` 库（图片调整）
  ```bash
  pip install Pillow
  ```
  如未安装 Pillow，脚本会跳过调整步骤并提示用户

### 4. Prompt 模板更新

#### 新的默认 Prompt 模板
```
平面矢量插画风格的微信公众号封面图，主题：{theme}。
扁平化设计，几何图形，简洁现代。
{color_scheme}背景，{style}风格。
文章标题：{title}。
900x386像素横版构图，高质量输出。
专业商务风格，适合企业内容传播，吸引眼球。
```

#### 风格示例

**1. 科技/AI 主题**
```
平面矢量插画风格，科技感微信封面图，主题：AI企业自动化。
扁平化设计，几何图形，蓝色光效元素。
简约现代，数字化图标，专业且吸引眼球。
900x386横版构图，适合公众号文章。
```

**2. 商务/企业主题**
```
平面矢量插画风格，企业级微信公众号封面，主题：企业数字化转型。
扁平化商务设计，深蓝色调，几何图形组合。
简洁大气，突出核心信息，传递专业感。
900x386像素高清横版。
```

**3. 极简风格**
```
极简平面矢量插画风格，微信封面图，主题：效率提升工具。
扁平化设计，留白艺术，蓝白配色。
几何图形，简约现代，专业商务风格。
900x386横版构图，高质量输出。
```

## 使用方法

### 基础用法（自动调整到 900x386）
```bash
python scripts/generate_cover_photo.py \
  --title "Claude Cowork企业部署完全指南" \
  --theme "AI企业自动化与协作" \
  --output "output/2026-01-19-article-cover.png"
```

### 自定义风格
```bash
python scripts/generate_cover_photo.py \
  --title "AI代理如何改变企业工作流" \
  --theme "AI工作流自动化" \
  --style "futuristic flat design" \
  --color-scheme "blue and purple gradient" \
  --output "output/cover.png"
```

### 保留原始尺寸（不调整）
```bash
python scripts/generate_cover_photo.py \
  --title "文章标题" \
  --theme "文章主题" \
  --output "output/cover.png" \
  --no-resize
```

### 高质量生成
```bash
python scripts/generate_cover_photo.py \
  --title "文章标题" \
  --theme "文章主题" \
  --model "cogview-4" \
  --quality "high" \
  --output "output/cover.png"
```

## 技术实现

### 图片生成流程
1. **API 调用**：使用 GLM-Image API 生成 1280x720 或 1024x1024 图片
2. **下载图片**：从临时 URL 下载到本地
3. **智能裁剪**：
   - 计算目标宽高比（900/383 ≈ 2.35）
   - 根据原图比例决定裁剪方向
   - 居中裁剪保持主体内容
4. **高质量缩放**：使用 LANCZOS 算法调整到 900x386
5. **优化保存**：质量 95，启用优化

### 裁剪算法
```python
target_ratio = 900 / 383  # ≈ 2.35
img_ratio = img.width / img.height

if img_ratio > target_ratio:
    # 图片更宽，裁剪宽度
    new_width = int(img.height * target_ratio)
    left = (img.width - new_width) // 2
    crop_box = (left, 0, left + new_width, img.height)
else:
    # 图片更高，裁剪高度
    new_height = int(img.width / target_ratio)
    top = (img.height - new_height) // 2
    crop_box = (0, top, img.width, top + new_height)
```

## 输出示例

### 成功输出
```
🎨 Generating cover photo with GLM-Image API...
   Model: glm-image
   Size: 1280x720
   Quality: standard
   Prompt: 平面矢量插画风格的微信公众号封面图...
✅ Image generated successfully!
   URL: https://temporary-url.com/image.png
📥 Downloading image to: output/2026-01-19-article-cover.png
✅ Image downloaded successfully!
   Size: 245.3 KB
   Path: output/2026-01-19-article-cover.png
📐 Resizing image to WeChat size (900x386)...
   Original size: 1280x720
✅ Image resized successfully!
   New size: 900x386
   File size: 198.7 KB
   Path: output/2026-01-19-article-cover.png

============================================================
✅ Cover photo generation completed!
   Output: output/2026-01-19-article-cover.png
   Size: 900x386 (WeChat standard)
============================================================
```

### 无 Pillow 库时的输出
```
⚠️  Warning: PIL/Pillow not installed. Image resizing will be skipped.
   Install with: pip install Pillow
🎨 Generating cover photo with GLM-Image API...
...
✅ Image downloaded successfully!
⚠️  Skipping resize: PIL/Pillow not installed

============================================================
✅ Cover photo generation completed!
   Output: output/2026-01-19-article-cover.png
============================================================
```

## 集成到 Content Factory 工作流

### 更新后的发布流程
1. 生成文章内容（MD、HTML、小红书、Tweet）
2. **生成微信封面图**（新增步骤）
   ```bash
   python scripts/generate_cover_photo.py \
     --title "$(extract_title)" \
     --theme "$(extract_theme)" \
     --output "output/YYYY-MM-DD-article-slug-cover.png"
   ```
3. 发布到微信公众号（包含封面图）
   ```bash
   python scripts/wechat_publish.py \
     --html "output/YYYY-MM-DD-article-slug.html" \
     --cover "output/YYYY-MM-DD-article-slug-cover.png"
   ```

## 最佳实践

### 1. Prompt 优化建议
- **明确主题**：清晰描述文章核心主题
- **强调风格**：始终包含"平面矢量插画风格"
- **指定元素**：列出关键视觉元素（图标、图形等）
- **色彩方案**：明确主色调和配色方案
- **尺寸说明**：提及 900x386 横版构图

### 2. 质量控制
- **标准质量**：用于草稿和快速预览
- **高质量**：用于最终发布版本
- **模型选择**：
  - `glm-image`：最新模型，推荐使用
  - `cogview-4`：高质量，适合重要文章
  - `cogview-3-flash`：快速生成，适合批量

### 3. 成本优化
- 使用 `standard` 质量节省成本
- 批量生成时考虑复用相似主题封面
- 监控 API 使用量

### 4. 文件管理
- 统一命名：`YYYY-MM-DD-article-slug-cover.png`
- 集中存储：`D:\AI\contents\CCoutput\`
- 定期清理临时文件

## 故障排除

### 问题：PIL/Pillow 未安装
**解决方案**：
```bash
pip install Pillow
```

### 问题：图片裁剪后主体内容丢失
**解决方案**：
- 使用 `--no-resize` 保留原图
- 手动调整 prompt 强调主体居中
- 尝试不同的生成尺寸（1280x720 vs 1024x1024）

### 问题：生成的图片不符合平面矢量风格
**解决方案**：
- 在 prompt 中多次强调"平面矢量插画风格"、"扁平化设计"
- 添加"几何图形"、"简约现代"等关键词
- 尝试使用 `cogview-4` 模型

### 问题：API 调用失败
**解决方案**：
- 检查 API key 是否正确
- 验证网络连接
- 查看 API 配额是否用尽

## 更新文件清单

- ✅ `SKILL.md` - 更新第 8 节封面图生成说明
- ✅ `scripts/generate_cover_photo.py` - 添加图片调整功能
- ✅ `scripts/WECHAT_COVER_UPDATE.md` - 本更新说明文档

## 后续计划

- [ ] 添加批量生成支持
- [ ] 集成模板库（预设风格）
- [ ] A/B 测试功能（生成多个变体）
- [ ] 自动化风格学习（基于成功案例）
- [ ] 封面效果分析（点击率追踪）

---

**更新版本**：2.0.0
**更新日期**：2026-01-19
**状态**：已完成，可投入使用
