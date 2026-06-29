# 常见PPT页面设计模式（v4）

> **核心原则：坐标是算出来的，不是写出来的。** 所有公式中的参数必须从参考页提取，禁止硬编码。

---

## 〇、设计哲学

借鉴guizang归藏的"极权式美学"和Mck麦肯锡的生产级护栏：

1. **约束即美感** — 给AI自由，它就还你一坨垃圾；给AI框架，它就能批量产出精品
2. **颜色锁死** — 只允许使用从原PPT提取的5个核心色值+2文字色，禁止自定义hex
3. **字体分级** — 标题/正文/注释三级分工，不混用
4. **布局公式化** — 所有坐标从公式计算，不允许凭感觉
5. **间距保护** — 分栏间距0.6-1.0cm，内容与装饰条间距≥0.15cm
6. **节奏感** — 深色/混合PPT: 连续3页以上同深浅=视觉疲劳; 浅色PPT: 用章节分隔页+布局变化控制节奏
7. **验证读回** — 生成完毕必须用python-pptx读回+validate_layout()检查
8. **色板角色** — PRIMARY=主色(最高频), SECONDARY=中性辅色(灰/深蓝), ACCENT=高饱和强调色(红/橙)

---

## 一、封面页模式

### 模式1：居中大标题
```
适用: 正式、简约风格
元素: 主标题(36pt居中) + 副标题(16pt) + 装饰线 + 背景色
坐标: 
  主标题_Y = SLIDE_H * 0.35
  副标题_Y = SLIDE_H * 0.55
  装饰线_Y = SLIDE_H * 0.50
  所有X居中 = (SLIDE_W - text_w) / 2
```

### 模式2：左文右图
```
适用: 商务、科技风格
元素: 主标题 + 副标题 + 说明文字 + 右侧色块区
坐标:
  文字区: X=MARGIN_L, W=(CONTENT_W-GAP)*0.6
  色块区: X=MARGIN_L+(CONTENT_W-GAP)*0.6+GAP, W=(CONTENT_W-GAP)*0.4
```

---

## 二、目录页模式

### 模式1：数字编号列表
```
适用: 专业咨询风格
元素: 01/02/03编号 + 章节标题 + 简短描述
坐标:
  编号_Y[i] = CONTENT_Y + i * (CARD_H + CARD_GAP)
  编号: X=MARGIN_L, W=1.5cm, H=1.0cm, 圆角矩形, C_PRIMARY填充
  标题: X=MARGIN_L+2.0, 同Y
  描述: X=MARGIN_L+2.0, Y=标题_Y+0.8cm, 浅灰12pt
```

### 模式2：图标卡片网格
```
适用: 活泼、现代风格
元素: 2x2或3x2网格卡片
坐标:
  ROW_GAP = 0.6, COL_GAP = 0.6
  CARD_W = (CONTENT_W - (COLS-1)*COL_GAP) / COLS
  CARD_H = (CONTENT_H - (ROWS-1)*ROW_GAP) / ROWS
  CARD_X[c] = CONTENT_X + c * (CARD_W + COL_GAP)
  CARD_Y[r] = CONTENT_Y + r * (CARD_H + ROW_GAP)
```

---

## 三、章节过渡页模式

### 模式1：大数字+标题
```
适用: 正式、大气风格
元素: 大号章节编号(72-96pt) + 章节标题(28pt) + 简短引言(14pt)
坐标:
  大编号: X=MARGIN_L, Y=SLIDE_H*0.25, 96pt, C_PRIMARY, alpha=0.2
  标题: X=MARGIN_L, Y=大编号bottom+0.5cm, 28pt加粗
  引言: X=MARGIN_L, Y=标题bottom+0.8cm, 14pt, C_TEXT_L
```

---

## 四、内容页模式（重点，含完整坐标公式）

### 模式A：左文右数据 ⭐ 最常用
```
适用: 行业趋势、公司概况、背景介绍
结构: 左栏2-3个竖向卡片 + 右栏3-5个数据框

分栏比例（由内容量决定）:
  文字密集(每卡>50字) → ratio_left = 7/12 ≈ 0.58
  文字适中(每卡30-50字) → ratio_left = 0.6
  文字精简(每卡<30字) → ratio_left = 0.5

坐标公式:
  LEFT_W  = (CONTENT_W - GAP) * ratio_left
  RIGHT_W = (CONTENT_W - GAP) * (1 - ratio_left)
  LEFT_X  = CONTENT_X
  RIGHT_X = CONTENT_X + LEFT_W + GAP

  验证: LEFT_X + LEFT_W + GAP + RIGHT_W = CONTENT_X + CONTENT_W ± 0.1cm

左栏卡片:
  CARD_GAP = 0.4cm
  CARD_H = (CONTENT_H - (N-1)*CARD_GAP) / N
  CARD_Y[i] = CONTENT_Y + i*(CARD_H + CARD_GAP)
  每张卡片: X=LEFT_X, W=LEFT_W, H=CARD_H
  卡片内部: 左装饰条0.2cm(C_SECONDARY) + 标题14pt + 描述12pt

右栏数据框:
  DATA_GAP = 0.4cm
  DATA_H = (CONTENT_H - (M-1)*DATA_GAP) / M
  DATA_Y[i] = CONTENT_Y + i*(DATA_H + DATA_GAP)
  每个数据框: X=RIGHT_X, W=RIGHT_W, H=DATA_H
  数据框内部: 浅灰背景(C_BG_GRAY) + 左侧0.1cm强调色竖条 + 大数字28pt + 说明12pt

⛔ 禁止: LEFT_W < 12cm 且 RIGHT_W < 10cm 且 GAP > 2cm（会产生中间空白）
```

### 模式B：三栏卡片并列
```
适用: 三大优势、三个特点、三大价值

坐标公式:
  COL3_GAP = 0.6cm
  COL3_W = (CONTENT_W - 2*COL3_GAP) / 3
  COL3_X[0] = CONTENT_X
  COL3_X[1] = CONTENT_X + COL3_W + COL3_GAP
  COL3_X[2] = CONTENT_X + 2*(COL3_W + COL3_GAP)

  验证: COL3_X[2] + COL3_W = CONTENT_X + CONTENT_W ± 0.1cm

卡片内部结构:
  顶部: 编号徽章(0.8×0.6cm, C_SECONDARY背景, 白色10pt)
  中部: 标题(16pt加粗)
  底部: 描述(12pt, C_TEXT_L)
  左侧: 装饰竖条(0.2cm宽, 与卡片等高, C_SECONDARY或C_ACCENT)
```

### 模式C：上文下图
```
适用: 产品展示、案例介绍

坐标公式:
  TEXT_H = CONTENT_H * 0.35
  IMAGE_H = CONTENT_H * 0.60
  IMAGE_GAP = 0.5cm
  TEXT_Y = CONTENT_Y
  IMAGE_Y = CONTENT_Y + TEXT_H + IMAGE_GAP

  图片区用浅灰色块占位: X=CONTENT_X, W=CONTENT_W, H=IMAGE_H, C_BG_GRAY填充
  色块内居中文字: "示意图区域" 12pt 浅灰
```

### 模式D：左文右图（经典）
```
适用: 背景叙述、项目缘起

坐标公式:
  TEXT_W = (CONTENT_W - GAP) * 0.6
  IMAGE_W = (CONTENT_W - GAP) * 0.4
  TEXT_X = CONTENT_X
  IMAGE_X = CONTENT_X + TEXT_W + GAP

  验证: TEXT_W + GAP + IMAGE_W = CONTENT_W ± 0.1cm

文字区: 小标题(18pt) + 段落(14pt) + 装饰竖条(0.2cm, C_PRIMARY)
图片区: 色块占位(C_BG_GRAY) + 装饰元素
```

### 模式E：时间轴
```
适用: 发展历程、里程碑

纵向时间轴公式:
  N = 时间节点数
  NODE_GAP = (CONTENT_H - 1.0) / (N-1) if N>1 else 0
  NODE_Y[i] = CONTENT_Y + i * NODE_GAP

  时间线: X=CONTENT_X+1.5, Y=CONTENT_Y, W=0.05cm, H=CONTENT_H, C_PRIMARY
  节点圆点: X=CONTENT_X+1.3, Y=NODE_Y[i]-0.15, D=0.5cm, C_PRIMARY
  年份: X=CONTENT_X, Y=NODE_Y[i], 14pt加粗, C_PRIMARY
  事件标题: X=CONTENT_X+2.5, Y=NODE_Y[i], 14pt
  事件描述: X=CONTENT_X+2.5, Y=NODE_Y[i]+0.6, 12pt, C_TEXT_L
```

### 模式F：左右对比
```
适用: 对比分析、方案对比

坐标公式:
  HALF_W = (CONTENT_W - 1.5) / 2  # 中间1.5cm给VS分隔
  LEFT_X = CONTENT_X
  RIGHT_X = CONTENT_X + HALF_W + 1.5

  VS标记: X=CONTENT_X+HALF_W+0.25, Y=CONTENT_Y+CONTENT_H/2-0.3, 0.8×0.6圆角矩形
```

### 模式G：上下分区（策略+缺口）
```
适用: 上半展示策略方向，下半展示人才缺口

坐标公式:
  GROUP_GAP = 0.7cm
  SECTION_TITLE_H = 0.8cm
  TOP_H = (CONTENT_H - GROUP_GAP - SECTION_TITLE_H) * 0.4
  BOT_H = (CONTENT_H - GROUP_GAP - SECTION_TITLE_H) * 0.6
  TOP_Y = CONTENT_Y + SECTION_TITLE_H
  BOT_Y = TOP_Y + TOP_H + GROUP_GAP
```

---

## 五、数据页模式

### 模式1：大数字突出
```
适用: 核心数据、业绩成果、关键指标

坐标公式:
  N = 数据个数
  DATA_GAP = 0.4cm
  DATA_W = (CONTENT_W - (N-1)*DATA_GAP) / N
  DATA_X[i] = CONTENT_X + i*(DATA_W + DATA_GAP)

  数据框: 浅灰背景(C_BG_GRAY) + 左侧0.1cm强调色竖条
  大数字: 28-32pt加粗, C_PRIMARY, 居中于框
  说明: 12pt, C_TEXT_L, 居中于框底部
```

### 模式2：图表+说明
```
适用: 数据分析、趋势展示

坐标公式:
  CHART_W = (CONTENT_W - GAP) * 0.55
  TEXT_W = (CONTENT_W - GAP) * 0.45
  CHART_X = CONTENT_X
  TEXT_X = CONTENT_X + CHART_W + GAP

  图表区: 用add_rect()手绘柱状/条形图
  说明区: 标题(16pt) + 要点列表(14pt)
```

---

## 六、总结页模式

### 模式1：金句+要点
```
适用: 价值主张、核心理念、总结升华

坐标公式:
  上方要点区: Y=CONTENT_Y, H=CONTENT_H*0.55
  底部金句框: Y=SLIDE_H-FOOTER_H, H=FOOTER_H, W=CONTENT_W
  金句框: C_PRIMARY背景 + C_ACCENT左竖条0.3cm + 白色文字18pt
```

---

## 七、通用设计元素参数

### 装饰元素（坐标公式化）
| 元素 | 尺寸 | 位置 | 颜色 |
|------|------|------|------|
| 顶部装饰条 | H=0.2cm, W=SLIDE_W | X=0, Y=0 | C_PRIMARY |
| 左侧竖条 | W=0.2cm, H=容器高 | X=容器左, Y=容器顶 | C_SECONDARY或C_ACCENT |
| 底部装饰框 | H=1.9cm, W=CONTENT_W | X=MARGIN_L, Y=SLIDE_H-2.1 | C_PRIMARY背景+C_ACCENT左竖条0.3cm |
| 编号徽章 | W=0.8cm H=0.6cm | X=卡片左+0.3, Y=卡片顶+0.3 | C_SECONDARY背景+白色10pt |
| 分隔线 | H=0cm, W=CONTENT_W | X=MARGIN_L, Y=标题区底 | C_LINE_GRAY |
| 数据框 | W=RIGHT_W, H=DATA_H | X=RIGHT_X, Y=DATA_Y[i] | C_BG_GRAY背景+左0.1cm强调色竖条 |

### 卡片样式
| 样式 | 描述 |
|------|------|
| 浅色背景卡 | 白色或#F5F5F5背景，无边框，用于内容区 |
| 数据框 | 浅灰背景+左侧0.1cm强调色竖条，大数字28-32pt+说明12pt |
| 强调色卡片 | C_PRIMARY浅色背景(10%透明度)+左侧0.2cm竖条+加粗标题 |

### 文字层级
| 级别 | 字号 | 粗细 | 颜色 |
|------|------|------|------|
| 一级标题 | 28-36pt | 加粗 | C_PRIMARY |
| 二级标题 | 20-24pt | 加粗 | C_TEXT |
| 三级标题 | 16-18pt | 加粗 | C_PRIMARY |
| 正文 | 14-16pt | 常规 | C_TEXT |
| 注释/来源 | 9-12pt | 常规 | C_TEXT_L |
| 数据大字 | 28-32pt | 加粗 | C_PRIMARY或C_ACCENT |

---

## 八、python-pptx 踩坑速查

### PP_PARAGRAPH_ALIGNMENT 枚举（必看！）

```python
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT

# ✅ 正确写法
p.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
p.alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
p.alignment = PP_PARAGRAPH_ALIGNMENT.RIGHT
p.alignment = PP_PARAGRAPH_ALIGNMENT.JUSTIFY

# ❌ 错误写法（会报 AttributeError）
p.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT  # 如果从 pptx.enum 导入方式错误
p.alignment = 'left'  # 字符串不行
p.alignment = 0  # 整数不行
```

### shape 位置可能为 None

某些占位符shape的 `left/top/width/height` 可能为 `None`，必须先判断：

```python
for shape in slide.shapes:
    if shape.left is None or shape.top is None:
        continue  # 跳过无位置信息的shape
    left_cm = Emu(shape.left).cm
```

### 全屏背景色块识别

PPT的第一个shape经常是全屏白色/浅色背景色块（宽度≈幻灯片宽度，高度≈幻灯片高度）。
检测装饰条时必须排除这种色块，否则会误报"顶部装饰条=19.05cm"。

```python
def is_fullscreen(shape, slide_w, slide_h):
    w = Emu(shape.width).cm
    h = Emu(shape.height).cm
    return w >= slide_w * 0.95 and h >= slide_h * 0.95
```

### set_ea_font 必须调用

python-pptx 默认只设置西文字体（`a:latin`），不设置东亚字体（`a:ea`）。
中文内容如果不调用 `set_ea_font()`，在 PowerPoint 中可能显示为宋体。

```python
from scripts.analyze_style import set_ea_font
run.font.name = "Noto Sans SC"  # 西文
set_ea_font(run, "Noto Sans SC")  # 东亚（必做！）
```

---

## 九、布局合理性检查清单

> 分级检查（借鉴Mck P0-P3 + guizang防幻觉机制）

### P0 阻断级（不通过不交付）
- [ ] 左右分栏紧密排列，间距0.6-1.0cm
- [ ] 左右分栏之间无超过2cm的空白
- [ ] 所有shape左边缘 ≥ MARGIN_L - 0.5cm
- [ ] 所有shape右边缘 ≤ SLIDE_W - MARGIN_R + 0.5cm
- [ ] 无图片shape(shape_type==13)
- [ ] 每页≥20个shape
- [ ] 无模板残留关键词

### P1 功能级
- [ ] 颜色值均在色板列表中
- [ ] 字体与提取结果一致
- [ ] 内容不溢出底部装饰条
- [ ] 标题区与内容区之间有分隔线

### P2 品质级
- [ ] 纵向卡片间距均匀（偏差<0.3cm）
- [ ] 同行元素顶部对齐（偏差<0.2cm）
- [ ] 标题风格同类页面统一

### P3 润色级
- [ ] 节奏感：连续3页以上有无深浅交替
- [ ] 信息密度与原PPT匹配
- [ ] 底部金句框与参考页风格一致

---

## 十、sldIdLst操作唯一可靠方法：清空+按序重建

> **⚠️ 这是最多踩坑的地方！不要用 addprevious/addnext/insert，只重建！**

`python-pptx` 对 `sldIdLst` 的操作（`addprevious`, `addnext`, `insert`）在多页插入时**必然导致顺序错乱**。唯一可靠的方法：

```python
def rebuild_sldIdLst(prs, new_slide_order):
    """
    清空sldIdLst并按新顺序重建
    new_slide_order: [(slide_obj, rId_str, slide_id_int), ...]
    """
    sldIdLst = prs.presentation.sldIdLst
    # 1. 记住原来的映射
    old_entries = []
    for sldId in sldIdLst:
        rId = sldId.get(qn('r:id'))
        sid = sldId.get('id')
        old_entries.append((rId, int(sid)))
    
    # 2. 清空
    for child in list(sldIdLst):
        sldIdLst.remove(child)
    
    # 3. 按新顺序插入
    for slide, rId, slide_id in new_slide_order:
        sldId = etree.SubElement(sldIdLst, qn('p:sldId'))
        sldId.set('id', str(slide_id))
        sldId.set(qn('r:id'), rId)
```

**操作步骤（替换第2-5页为例）：**
1. 提取原sldIdLst所有条目（rId + slide id）
2. 找到原第2-5页对应的slide对象
3. 创建新页面并添加到slides集合
4. 构建新的顺序列表：[原第1页, 新页A, 新页B, 新页C, 新页D, 原第6页...]
5. 清空sldIdLst + 按序重建
6. 删除原第2-5页的slide part引用

**关键：slide_id不能重复！** 新页面的slide_id必须从max+1开始递增。
