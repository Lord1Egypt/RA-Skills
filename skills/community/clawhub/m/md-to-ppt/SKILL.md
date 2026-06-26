---
name: md-to-ppt
description: "智能 Markdown 转 PPT。自动分析内容结构、智能分页、详细设计每页布局、自动生成/搜索配图。支持 Slidev/HTML/PPTX 多格式输出。| Intelligent Markdown to PPT with auto-layout and image generation."
version: "1.1.0"
license: MIT
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Message, WebSearch, WebFetch, Canvas
---

# 📊 智能 Markdown 转精美 PPT

**核心升级 v1.1.0**：
- 🤖 **智能内容分析** - 自动识别内容类型和优先级
- 📐 **自动布局设计** - 根据内容量智能分页和布局
- 🖼️ **自动配图** - 生成插图或从网络搜索下载
- 🎨 **布局模板** - 10+ 种专业布局模板

---

## 🎯 工作流程

```
用户输入 Markdown
      ↓
【阶段 1】内容分析
  - 识别主题和核心观点
  - 评估内容量和复杂度
  - 确定目标受众和场景
      ↓
【阶段 2】智能分页
  - 根据内容类型自动分组
  - 每页一个核心观点
  - 避免信息过载
      ↓
【阶段 3】布局设计
  - 为每页选择最佳布局
  - 安排标题/正文/图片位置
  - 设计视觉层次
      ↓
【阶段 4】自动配图
  - 生成 AI 插图 或
  - 从网络搜索相关图片
  - 优化图片尺寸和位置
      ↓
【阶段 5】生成 PPT
  - 应用主题模板
  - 渲染最终效果
  - 提供预览和导出
```

---

## 📐 智能分页规则

### 分页触发条件

| 条件 | 阈值 | 处理 |
|------|------|------|
| 列表项数量 | > 5 项 | 拆分为多页 |
| 文字数量 | > 100 字/页 | 拆分或精简 |
| 代码块 | > 15 行 | 单独一页 |
| 多个一级标题 | 每个标题新页 | 自动分页 |
| 表格 | > 5 行 | 单独一页 |

### 内容分组策略

```
输入内容分析
      ↓
识别内容块类型：
├─ 标题块 (# 标题 + 副标题)
├─ 列表块 (- 列表项)
├─ 引用块 (> 引用)
├─ 代码块 (```code```)
├─ 表格块 (|table|)
└─ 图片块 (![img](url))
      ↓
分组规则：
- 每个一级标题 = 独立章节
- 每 3-5 个列表项 = 一页
- 每个代码块 = 单独一页（如>15 行）
- 每个表格 = 单独一页
- 引用可与其他内容合并
```

---

## 🎨 布局模板库

### 模板 1：标题页 (Title)
```
┌─────────────────────────────┐
│                             │
│         主标题              │
│         副标题              │
│                             │
│      作者 | 日期            │
│                             │
└─────────────────────────────┘
适用：封面、章节起始页
```

### 模板 2：要点列表 (Bullet List)
```
┌─────────────────────────────┐
│  标题                       │
├─────────────────────────────┤
│  • 要点 1                   │
│  • 要点 2                   │
│  • 要点 3                   │
│  • 要点 4                   │
│           [配图]            │
└─────────────────────────────┘
适用：功能列表、优势说明
```

### 模板 3：左右对比 (Two Column)
```
┌─────────────────────────────┐
│  标题                       │
├──────────────┬──────────────┤
│   左侧内容   │   右侧内容   │
│   (Before)   │   (After)    │
│              │              │
└──────────────┴──────────────┘
适用：对比、前后变化、优劣分析
```

### 模板 4：数据表格 (Data Table)
```
┌─────────────────────────────┐
│  数据概览                   │
├─────────────────────────────┤
│  ┌─────┬─────┬─────┐       │
│  │ A   │ B   │ C   │       │
│  ├─────┼─────┼─────┤       │
│  │ 1   │ 2   │ 3   │       │
│  └─────┴─────┴─────┘       │
│        [图表可视化]         │
└─────────────────────────────┘
适用：数据展示、对比分析
```

### 模板 5：代码展示 (Code)
```
┌─────────────────────────────┐
│  功能说明                   │
├─────────────────────────────┤
│  ```python                  │
│  def hello():              │
│      print("World")        │
│  ```                        │
│                             │
│  [代码说明/输出结果]        │
└─────────────────────────────┘
适用：技术分享、Demo 演示
```

### 模板 6：引用强调 (Quote)
```
┌─────────────────────────────┐
│                             │
│    "重要引用内容"           │
│                             │
│         — 作者              │
│                             │
│  [背景图/相关插图]          │
└─────────────────────────────┘
适用：金句、核心价值主张
```

### 模板 7：时间轴 (Timeline)
```
┌─────────────────────────────┐
│  发展历程                   │
├─────────────────────────────┤
│  2020 → 2021 → 2022 → 2023 │
│   ●      ●      ●      ●   │
│                             │
│  [各阶段说明]               │
└─────────────────────────────┘
适用：发展历程、项目进度
```

### 模板 8：图文混排 (Hero Image)
```
┌─────────────────────────────┐
│  标题                       │
├─────────────────────────────┤
│                             │
│      [大幅配图]             │
│                             │
│  简短说明文字               │
└─────────────────────────────┘
适用：产品展示、场景演示
```

### 模板 9：数据可视化 (Charts)
```
┌─────────────────────────────┐
│  数据洞察                   │
├─────────────────────────────┤
│     ┌───┐                   │
│  ┌──┼───┼──┐               │
│  │  │   │  │  [柱状图]     │
│  └──┴───┴──┘               │
│                             │
│  关键数据解读               │
└─────────────────────────────┘
适用：报表、数据分析
```

### 模板 10：结束页 (Ending)
```
┌─────────────────────────────┐
│                             │
│        谢谢观看             │
│                             │
│     Q&A / 联系方式          │
│                             │
└─────────────────────────────┘
适用：演示结束
```

---

## 🖼️ 自动配图策略

### 优先级 1：AI 生成插图
```
当内容包含：
- 抽象概念（如"效率"、"创新"）
- 未来场景（如"AI 时代"）
- 情感表达（如"成功"、"合作"）

调用 AI 绘画 API 生成：
- 风格：与主题匹配
- 尺寸：1920x1080
- 格式：PNG
```

### 优先级 2：网络搜索下载
```
当内容包含：
- 具体事物（如产品、人物）
- 数据图表
- 场景图片

搜索策略：
1. 提取页面关键词
2. 在 Unsplash/Pexels 搜索
3. 下载合适尺寸图片
4. 保存到 assets/目录
```

### 优先级 3：图标/Emoji
```
当内容包含：
- 列表项
- 分类标签
- 状态标识

使用：
- Emoji 表情
- FontAwesome 图标
- 自定义 SVG 图标
```

### 配图位置规则

| 布局模板 | 配图位置 | 尺寸建议 |
|----------|----------|----------|
| 要点列表 | 右侧 1/3 | 400x300 |
| 左右对比 | 每侧一半 | 各 500x400 |
| 引用强调 | 背景/底部 | 全屏/600x400 |
| 图文混排 | 中央大幅 | 800x600 |
| 数据可视化 | 中央 | 600x400 |

---

## 🔧 使用示例

### 示例 1：基础转换
```
用户：/md_to_ppt ./docs/report.md
助手：📊 正在分析文档结构...
     ✅ 检测到 3 个章节，12 个内容块
     📐 智能分页：预计生成 8 页幻灯片
     🎨 正在为每页设计布局...
     🖼️ 正在搜索/生成配图...
     ✅ 完成！生成 8 页精美 PPT
```

### 示例 2：指定主题
```
用户：/md_to_ppt ./pitch.md --theme business-gold --auto-images
助手：🎨 应用主题：黑金风格
     🖼️ 自动配图模式：启用
     📐 布局设计：
        - 第 1 页：标题页
        - 第 2 页：痛点（左右对比）
        - 第 3 页：解决方案（图文混排）
        - 第 4 页：市场规模（数据可视化）
        - 第 5 页：团队（列表 + 头像）
        - 第 6 页：结束页
     ✅ 完成！
```

### 示例 3：交互式创建
```
用户：帮我做个融资路演 PPT
助手：👋 好的！我来帮您创建融资路演 PPT。

请提供以下内容（或提供 Markdown 文件）：
1. 项目名称和一句话介绍
2. 目标解决的痛点
3. 解决方案/产品
4. 市场规模数据
5. 商业模式
6. 团队介绍
7. 融资需求

我将自动：
- 设计专业布局
- 生成/搜索配图
- 应用商务主题
- 生成演讲备注
```

---

## 📋 布局设计算法

### 步骤 1：内容分析
```python
def analyze_content(markdown):
    sections = parse_markdown(markdown)
    
    for section in sections:
        # 识别内容类型
        section.type = detect_type(section)  # title/list/code/table/quote
        
        # 评估内容量
        section.complexity = calculate_complexity(section)
        
        # 确定优先级
        section.priority = determine_priority(section)
    
    return sections
```

### 步骤 2：智能分页
```python
def smart_paginate(sections):
    pages = []
    current_page = []
    current_load = 0
    
    for section in sections:
        # 计算本节占用空间
        load = calculate_load(section)
        
        # 超过阈值则新开一页
        if current_load + load > PAGE_THRESHOLD:
            pages.append(current_page)
            current_page = []
            current_load = 0
        
        current_page.append(section)
        current_load += load
    
    return pages
```

### 步骤 3：布局匹配
```python
def match_layout(page):
    # 根据内容类型选择布局
    if page.has_title() and not page.has_content():
        return "title"
    
    elif page.has_list() and len(page.list) <= 5:
        return "bullet_list"
    
    elif page.has_comparison():
        return "two_column"
    
    elif page.has_table():
        return "data_table"
    
    elif page.has_code() and len(page.code) > 15:
        return "code_full"
    
    elif page.has_quote():
        return "quote"
    
    else:
        return "mixed"
```

### 步骤 4：配图决策
```python
def decide_images(page):
    keywords = extract_keywords(page)
    
    # 尝试 AI 生成
    if is_abstract_concept(keywords):
        return generate_ai_image(keywords)
    
    # 尝试网络搜索
    elif is_concrete_object(keywords):
        return search_and_download(keywords)
    
    # 使用图标
    else:
        return generate_icons(keywords)
```

---

## 🎯 内容 - 布局映射表

| 内容类型 | 推荐布局 | 配图策略 |
|----------|----------|----------|
| 单一级标题 | 标题页 | 背景图/渐变 |
| 3-5 个列表项 | 要点列表 | 右侧配图 |
| 对比内容 | 左右对比 | 每侧配图 |
| 数据表格 | 数据可视化 | 图表 + 图标 |
| 长代码块 | 代码展示 | 无图/架构图 |
| 重要引用 | 引用强调 | 背景图 |
| 时间序列 | 时间轴 | 节点图标 |
| 产品展示 | 图文混排 | 大幅产品图 |
| 团队介绍 | 列表 + 头像 | 成员照片 |
| 结束页 | 结束页 | 背景图/Logo |

---

## 🛠️ 技术实现

### 核心脚本
```bash
# 完整转换流程
python3 scripts/md_to_ppt.py \
  --input ./docs/presentation.md \
  --output ./slides/output/ \
  --theme business-blue \
  --format slidev \
  --auto-images \
  --smart-layout
```

### 依赖安装
```bash
# Slidev
npm install -g @slidev/cli

# 图片处理
pip3 install pillow requests

# AI 绘图（可选）
pip3 install diffusers transformers

# 网络搜索（可选）
pip3 install google-search-results
```

---

## 📁 输出结构

```
slides/output/
├── slides.md           # Slidev 主文件
├── style.css           # 自定义样式
├── README.md           # 使用说明
├── assets/             # 图片资源
│   ├── page-1-bg.png   # 第 1 页背景
│   ├── page-2-img.jpg  # 第 2 页配图
│   └── icons/          # 图标目录
│       ├── check.svg
│       └── star.svg
└── layout-plan.json    # 布局设计方案（可选）
```

---

## 💡 最佳实践

### 1. Markdown 编写建议
```markdown
# 清晰的一级标题（每章自动分页）

## 明确的二级标题（内容分组）

- 列表项控制在 5 个以内
- 每行文字不超过 30 字
- 代码块添加语言标识

> 引用用于强调重点

![描述](图片 URL 或留空由 AI 生成)
```

### 2. 配图建议
- 商务场景：使用真实照片
- 技术分享：使用架构图/流程图
- 创意提案：使用插画风格
- 数据报告：使用图表可视化

### 3. 布局选择
- 内容少 → 大图 + 少字
- 内容多 → 分多页，避免拥挤
- 重要信息 → 引用布局强调
- 对比内容 → 左右布局

---

## ⚙️ 配置选项

### 命令行参数
```bash
--input, -i          # 输入 Markdown 文件
--output, -o         # 输出目录
--theme, -t          # 主题名称
--format, -f         # 输出格式 (slidev/html/pptx)
--title              # PPT 标题
--author             # 作者名
--auto-images        # 启用自动配图
--smart-layout       # 启用智能布局
--image-source       # 图片源 (ai/search/mixed)
--layout-plan        # 输出布局设计方案
```

### 配置文件
```yaml
# .md-to-ppt.yml
default:
  theme: business-blue
  format: slidev
  auto-images: true
  smart-layout: true
  image-source: mixed

layouts:
  max_items_per_page: 5
  max_words_per_slide: 100
  code_threshold: 15
```

---

## 🚀 进阶功能

### 1. 布局预览
```
用户：/md_to_ppt ./doc.md --preview-layout
助手：📐 布局设计方案：

第 1 页 [标题页]
├─ 主标题：产品介绍
├─ 副标题：让 PPT 制作更简单
└─ 背景：渐变

第 2 页 [要点列表]
├─ 标题：市场痛点
├─ 列表：4 项
├─ 配图：右侧（待生成）
└─ 布局：80% 文字 + 20% 图片

...

确认布局方案后开始生成？(是/修改)
```

### 2. 配图预览
```
用户：/md_to_ppt ./doc.md --preview-images
助手：🖼️ 配图方案：

第 2 页 - 市场痛点
  关键词：效率、协作、学习
  推荐图片：办公场景/团队协作
  来源：Unsplash（3 个选项）
  [预览图 1] [预览图 2] [预览图 3]
  
选择或输入"生成"使用 AI 创作？
```

### 3. 批量转换
```bash
# 转换整个目录
python3 scripts/md_to_ppt.py \
  --batch ./docs/ \
  --output ./slides/ \
  --theme business-blue
```

---

## 🛠️ 故障排除

### 问题 1：配图失败
**解决**：检查网络连接，或改用本地图标

### 问题 2：布局拥挤
**解决**：启用 `--smart-layout` 自动分页，或手动添加 `---` 分页符

### 问题 3：图片尺寸不对
**解决**：检查 `assets/` 目录，图片应调整为 1920x1080 或按比例缩放

### 问题 4：中文乱码
**解决**：确保 UTF-8 编码，使用支持中文的字体

---

## 📞 支持

- GitHub Issues: [待创建]
- 文档：`./docs/usage.md`
- 示例：`./templates/`
- 布局模板：`./layouts/`

---

**版本**: 1.1.0  
**作者**: 太子 @neutronstar238  
**许可**: MIT  
**更新**: 新增智能布局设计和自动配图功能
