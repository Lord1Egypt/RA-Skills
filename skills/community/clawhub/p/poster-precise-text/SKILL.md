---
name: poster-precise-text
description: 精准文字海报生成技能（两步法）。当用户需要生成中文海报且文字必须100%精准时触发。核心方法：Step1 用 image_synthesize 以参考图生成插画，Step2 用 HTML 精确渲染文字，两者互补。适用场景：健康科普、教育宣传、活动海报、运营素材。
---

# poster-precise-text · 精准文字海报两步法

## 核心原则

> **文字精准 > 插画还原**
> 当两者冲突时，优先保文字。AI 图像生成对中文精准度有限，用 HTML 控制文字是唯一可靠解法。

---

## 触发判断

用户说这些词时激活：
- "海报" + "文字要准"
- "中文海报" "排版复刻"
- "生成海报" "文字清晰"
- 直接发一张图片要求"复刻"

---

## 标准工作流

### Step 1 · 提取内容（images_understand）

分析原图，提取：
- 所有文字内容（逐字）
- 排版结构（标题区/内容区/页脚）
- 视觉风格（配色/字体风格/图标数量）

### Step 2 · 生成插画（image_synthesize）

**有原图参考时：**
- `input_files`: 原图路径
- `prompt`: 明确要求"保留原图排版风格，重生成插画，文字区域留空"
- 注意：文字留白成功率约40%，做好重试准备

**无原图时（纯文字海报）：**
- `prompt`: 详细描述排版结构（不用"参考图生成"）
- 文字内容直接写在 prompt 里（用于评估插画匹配度）

### Step 3 · HTML 精准文字版

使用预设模板，填入精准文字内容，输出 HTML 文件。

**发布 HTML：**
```
deploy(project_name="poster-xxx", dist_dir=临时目录)
```

**导出 PNG（如需要）：**
当前环境 Playwright 不可用，可选方案：
- 截图工具手动导出
- 告知用户"在浏览器打开 HTML → 截图"

---

## 模板用法

```html
<!-- 参考：/workspace/skills/poster-precise-text/references/bone_health_template.html -->
```

关键替换字段：

| 字段 | 说明 |
|------|------|
| `{{title}}` | 主标题 |
| `{{subtitle}}` | 副标题 |
| `{{section1_title}}` | 板块1标题 |
| `{{section1_cards}}` | 板块1内容（卡片JSON） |
| `{{section2_items}}` | 板块2内容（列表JSON） |
| `{{section3_items}}` | 板块3内容 |
| `{{footer_left}}` | 左下内容 |
| `{{footer_right}}` | 右下内容 |
| `{{bg_color}}` | 主色调 |
| `{{accent_color}}` | 强调色 |

---

## 配色规范

**医疗健康类（推荐）：**
- 主色：`#00857C`（青绿色）
- 背景：`#F7F7F7`
- 强调：`#F5A623`（橙色）
- 正文：`#1A1A1A`

**政务宣传类：**
- 主色：`#C41E3A`（中国红）
- 辅助：`#FFD700`（金色）

**教育科普类：**
- 主色：`#2563EB`（蓝色）
- 辅助：`#10B981`（绿色）

---

## Prompt 模板（image_synthesize）

### 有原图参考
```
Recreate this poster layout. Keep the exact structure, illustrations, icons, color scheme. 
Only change text to: [精准文字内容]
Keep all other elements identical.
```

### 无参考，纯文字海报
```
[见 references/poster_prompt_guide.md]
```

---

## 常见问题

**Q: 文字变形严重怎么办？**
→ 跳过参考图，用纯 prompt 生成海报，HTML 文字做精准层

**Q: 图像生成报错了？**
→ 检查 input_files 数量是否超限（max 10）
→ 尝试去掉 input_files，只用纯 prompt

**Q: HTML 发布后需要 PNG 格式？**
→ 用户在浏览器打开 → Ctrl+P 打印为 PDF
→ 或截图工具处理

---

## 版权说明

- 插画风格仅作参考，不可抄袭原图商业素材
- 生成的 HTML 版权归发布方所有
