---
name: poster-style-generator
description: 使用gpt-image-2生成海报，支持10种设计风格。每种风格精调了prompt，直接出图。
author: afeicn
---

# 海报风格生成器

用 `openai/gpt-image-2` 生成竖屏海报。

## 核心规则

使用本skill前，先确认以下参数：

- **模型**: `openai/gpt-image-2`
- **输出格式**: `jpeg`（quality: medium，控制文件大小）
- **尺寸**: `1536x2048`（**3:4比例**，不要用9:16。竖版正比，适合视频号/小红书封面）
- **设计原则**: 整个海报就是一个**标题**，标题文字占绝大部分版面。纯色底 + 粗体大字。不是插图，不是风景，是**大字标题海报**。
- **标题**: 由用户指定（示例：「我是怎么做出一款产品的」）

## 使用方式

1. 用户选择风格编号 1-10
2. 根据对应风格的prompt模板 + 用户提供的标题，替换 `{TITLE}` 占位符，生成完整prompt
3. 调用 `image_generate` 出图
4. 将图片发送给用户确认

## 风格库

### 1. 极简黑白印刷风
白底黑字，标题拆成三层排版：标题第一部分左上角超大黑体，第二部分小号宋体横排放中间，第三部分底部加粗无衬线字体压住画面。大量留白，像方法论书籍封面。克制、有知识感。

### 2. 毛笔书法冲击风
深米色宣纸背景，标题用毛笔大字处理，第一部分泼墨感最强占据上半部分；第二部分用小楷竖排穿插在中间；第三部分用黑色大字加红色印章式点缀。整体像"技术江湖秘籍"，有手作、开宗立派的感觉。

### 3. 赛博朋克霓虹风
深蓝黑背景，标题拆成霓虹灯牌：第一部分用紫蓝渐变发光字体，第三部分用电光蓝机械字体最大化处理，第二部分用小号像代码注释一样穿插。画面可加细微网格、故障线、扫描光效，但主体只有标题。科技发布会预告海报风格。

### 4. 手写便签风 ✅（已验证）
**已验证可用的prompt模板**（将 {TITLE} 替换为实际标题）：

> Vertical poster in hand-written sticky note style. Light yellow paper background with subtle lined grid. The title "{TITLE}" looks like it's handwritten on a task notebook page. The first part of the title in casual black hand-drawn font, slightly tilted. The key keyword in the title circled and underlined with blue marker (thick felt-tip pen style). Hand-drawn underline and small arrow decorations nearby. Looks like a real desk workspace inspiration note: personal, warm, process-oriented feel. Clean, minimal but with handcrafted texture. No people. 3:4 portrait format.

特点：浅黄纸张底+手写体+蓝色马克笔圈注+箭头划线。亲切、有过程感。

### 5. 复古铅字报纸风
泛黄纸张背景，标题采用多种复古印刷字体拼贴：第一部分像报纸大标题，第三部分用英文报刊式粗衬线体，第二部分用窄体小字嵌入中间。版面错落排布，带一点"独家揭秘"的传播感。

### 6. 产品发布会主视觉风
深灰到黑色渐变背景，标题居中但分层：第一部分用细长白色现代字体，第三部分用超大蓝白渐变字体压在画面中央。整体有玻璃拟态、柔光和轻微科技线条。产品发布会风，专业、干净。

### 7. 日式杂志排版风
浅灰白背景，标题竖排与横排混合。第一部分竖排放右侧，第三部分横向大号放中下部，第二部分小号字穿插在空白处。字体混用明朝体、圆体和英文无衬线，形成杂志封面式错落感。清爽、有设计腔调。

### 8. 手账涂鸦风
白色网格纸背景，标题被拆成不同贴纸：第一部分是手绘粗体，第二部分像黑色胶带标签，第三部分用彩色涂鸦泡泡字。整体有轻微歪斜、手画框线、划重点感。创作者复盘自己的作品的感觉。

### 9. 硬核工程师终端风
黑色终端背景，标题用命令行排版逻辑：第一部分像终端输出的小字，第三部分用大号等宽字体居中显示，带绿色或蓝色字符光效。版面有光标、扫描线和代码块感。从命令行里长出来的产品。

### 10. 国潮科技混搭风
深墨蓝或暗红渐变背景，标题结合毛笔与科技字体：第一部分用醒目的国潮书法字，第三部分用未来感金属字体，第二部分用小号宋体穿插。可加印章、折扇纹理、数字光线等细节。传统笔记美学×AI工具创造的反差感。

## 输出

调用后直接返回海报图片。用户确认后用于后续制作。
