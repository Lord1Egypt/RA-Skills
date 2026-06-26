---
name: huo15-openclaw-ppt
displayName: 火一五演示稿技能
description: 乔布斯极简风格 PPT 生成技能，支持深蓝底色 + 苹方字体 + 白/灰双色调。支持内容规划、单页生成、合并版导出。触发词：做PPT、生成PPT、PPT、第X页、写PPT、制作PPT。
version: 1.1.0
aliases:
  - 火一五PPT技能
  - 火一五演示稿技能
  - PPT生成
  - 乔布斯风格PPT
  - 极简PPT
dependencies:
  python-packages:
    - python-pptx
    - Pillow
---

# 火一五 PPT 技能 v1.1

> 乔布斯极简风格 PPT 生成 — 青岛火一五信息科技有限公司

---

## 一、设计风格

### 配色系统（纯白/灰双色系）
| 常量 | RGB | 用途 |
|------|-----|------|
| C_BG | (0x06, 0x0D, 0x1A) | 高级感暗蓝背景（Photoshop图标风格） |
| C_CARD | (0x0D, 0x18, 0x2A) | 卡片背景 |
| C_TEXT | (0xFF, 0xFF, 0xFF) | 主文字白色 |
| C_SUBTEXT | (0x88, 0x88, 0x88) | 副文字灰色 |
| C_LIGHT | (0xCC, 0xCC, 0xCC) | 浅灰强调色 |
| C_DIVIDER | (0x33, 0x33, 0x44) | 分隔线暗灰 |

### 字体
- Mac：`PingFang SC`（苹方）
- Windows：`Microsoft YaHei`
- **字号层级**：标题64pt / 副标题26pt / 页面标题28pt / 卡片标题14pt / 正文10–11pt / 页脚9pt

### 布局
- 页面尺寸：13.33 × 7.5 寸（16:9）
- 左侧边距：0.6 寸
- 卡片宽度：12.13 寸
- 卡片间距：0.1 寸

---

## 二、组件规范

### 通用函数模板
```python
def text_box(slide, text, left, top, width, height,
             font_size=14, bold=False, color=None, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    run = p.add_run(); run.text = text
    run.font.size = Pt(font_size); run.font.bold = bold
    run.font.name = FONT; run.font.color.rgb = color or C_TEXT
    return tb

def add_card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid(); shape.fill.fore_color.rgb = C_CARD
    shape.line.color.rgb = RGBColor(0x33, 0x33, 0x44); shape.line.width = Pt(0.5)
    return shape

def add_divider(slide, left, top, width, color=None):
    ln = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(0.008))
    ln.fill.solid(); ln.fill.fore_color.rgb = color or RGBColor(0x33, 0x33, 0x44)
    ln.line.fill.background()
```

---

## 三、页面类型规范

### 3.1 封面页
- 纯色背景，无任何装饰元素（无线条、无渐变、无图形）
- 主标题：居中，64pt 加粗白色
- 副标题：主标题下方，26pt 白色不加粗
- 底部信息：底部居中，14pt 灰色
- **无**分隔线、无页码、无页脚

### 3.2 内容页（左上角标准标题）
```
text_box(slide, "页面标题", 0.6, 0.35, 8, 0.55, font_size=28, bold=True, color=C_TEXT)
text_box(slide, "ENGLISH SUBTITLE", 0.6, 0.82, 10, 0.35, font_size=10, color=C_SUBTEXT)
add_divider(slide, 0.6, 1.18, 12.13)
```

### 3.3 卡片列表页（五阶段、四杠杆等）
- 编号圆点：白色小圆形（0.28 寸），白底白字居中，序号用11pt粗体
- 卡片高度：0.88 寸/张，间距0.1 寸
- 内容字数控制在能完整显示的范围内

### 3.4 双栏对比页
- 左右各宽 5.9 寸，间距 0.23 寸
- 卡片高度统一

### 3.5 时间轴页
- 轴线：0.025 寸高暗灰矩形条
- 节点：白色/灰色圆形（0.42 寸）
- 时间标签在节点上方，正文在节点下方

### 3.6 引言页（人物照片 + 引言卡片）
- 人物图片：横版（800×400）→ 全宽12.13寸；竖版/方版保持比例
- 引言卡片在图片下方，高度容纳引言文字
- 人名、职位、来源分三行

### 3.7 封底页
- 大字标题：居中，52pt 加粗
- 副标题：28pt 灰色
- 二维码：左右对称放置，保持比例

---

## 四、图片处理规范（必看）

**必须保持原始比例，不得拉伸变形。**

| 原图尺寸 | 类型 | 放置尺寸 |
|---------|------|---------|
| 800×400 | 横版 | 宽12.13寸，高按比例 |
| 1292×1070 | 竖方 | 宽5.5寸，高4.55寸 |
| 1080×1542 | 竖版 | 宽2.6寸，高3.71寸 |
| 1000×1000 | 正方 | 宽3.0寸，高3.0寸 |
| 192×204 | 小二维码 | 宽1.5寸，高1.59寸 |
| 568×564 | 二维码 | 宽1.5寸，高1.5寸 |

**PNG带透明通道**：用 `Image.save()` 转换后嵌入，避免 PIL 无法识别问题。

---

## 五、合并版输出流程

1. 先做 Slide 1 确认风格
2. 每新增一页叠加到同一 `prs` 对象
3. 输出：`/Users/jobzhao/.openclaw/media/outbound/合并版_{主题}.pptx`
4. **每次更新必须保留前面所有已确认的页面**

### 脚本命名规范
- 单页测试脚本：`create_pptx_slide{N}.py`
- 合并版脚本：`create_pptx_combined.py`
- 输出路径：`/Users/jobzhao/.openclaw/media/outbound/`

---

## 六、微信图片获取（易踩坑总结）

### 坑1：COS URL 签名过期
- 微信发的图片 COS URL 有签名时效，过期返回 403
- **解决**：优先用微信接收后的本地附件路径

### 坑2：Odoo base64 解码后文件损坏
- `ir.attachment.datas` 是 base64 字符串，必须 `base64.b64decode()`
- 解码后可能 PIL 无法识别（Magic header 被截断）
- **解决**：用微信本地附件路径（`~/.openclaw/media/inbound/`）

### 坑3：本地附件路径识别
- 微信接收的文件命名：`E4_BC_81_E4_B8_9A...---uuid.png`（`---` 是分隔符）
- 用 `PIL.Image.open()` 直接打开测试是否可用
- RGBA 模式图片需 `.convert('RGB')` 或 `.save()` 后再使用

### 坑4：PIL 报 `UnidentifiedImageError`
- 原因：文件不是标准图片格式（如 WebP 或 COS 返回的错误页）
- **解决**：检查 `magic = data[:8].hex()`，确认是有效图片头
- **最佳方案**：始终通过微信本地路径获取图片

### 本地附件目录
```
~/.openclaw/media/inbound/
├── book_5000days.jpg        # 历史文件（可能已损坏）
├── book_yuce_1000.jpg       # 历史文件（可能已损坏）
├── book_yuce_1000---UUID.jpg  # 微信接收的原始文件 ✅
└── E4_BC_81...---UUID.png   # 微信接收的其他图片 ✅
```

---

## 七、常用代码片段

### 创建带编号的列表行
```python
dot = slide.shapes.add_shape(9, Inches(0.75), Inches(y+0.3), Inches(0.28), Inches(0.28))
dot.fill.solid(); dot.fill.fore_color.rgb = C_TEXT; dot.line.fill.background()
ntb = slide.shapes.add_textbox(Inches(0.75), Inches(y+0.3), Inches(0.28), Inches(0.28))
ntf = ntb.text_frame; np_ = ntf.paragraphs[0]; np_.alignment = PP_ALIGN.CENTER
nr = np_.add_run(); nr.text = num; nr.font.size = Pt(11); nr.font.bold = True
nr.font.name = FONT; nr.font.color.rgb = C_BG
```

### 繁荣度进度条（灰度渐变）
```python
for i in range(10):
    alpha = 0.3 + i * 0.07
    v = int(255 * alpha)
    bar = slide.shapes.add_shape(1, Inches(0.85 + i*0.56), Inches(y), Inches(0.5), Inches(0.18))
    bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor(v, v, v); bar.line.fill.background()
```

### 底部四引用横排
```python
quotes = [("乔布斯：", "..."), ("Naval：", "...")]
for i, (author, quote) in enumerate(quotes):
    x = 0.8 + i * 3.0
    text_box(slide, author, x, y, 0.8, 0.3, font_size=9, bold=True, color=C_TEXT)
    text_box(slide, quote, x, y+0.28, 2.8, 0.3, font_size=9, color=C_SUBTEXT)
```

---

## 八、触发词

- 做PPT、生成PPT、制作PPT
- 第X页、第X张、继续
- 乔布斯风格、极简PPT、深蓝PPT
- 添加 Slide X、把XXX放上、统一风格

---

## 九、参考案例

「走向具身智能」龙虾生态战略 PPT（11页）：
- Slide 1：封面
- Slide 2：人工智能五个阶段（五行卡片列表）
- Slide 3：战略参考读物（两本书封面）
- Slide 4：乔布斯引言（人物照片 + 引言卡片）
- Slide 5：Naval Ravikant 引言（人物照片 + 引言卡片）
- Slide 6：为什么押宝龙虾（双栏对比）
- Slide 7：我们的公司（双公司卡片）
- Slide 8：可行性分析（四卡片2×2）
- Slide 9：未来业态预判（时间轴）
- Slide 10：落地点（双栏核心产品 + 四引用）
- Slide 11：封底（标题 + 二维码）

---

**技术支持：** 青岛火一五信息科技有限公司
