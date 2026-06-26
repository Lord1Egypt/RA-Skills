# 微信公众号IP水印技能

> 为公众号文章和图片添加IP水印，防止抄袭；通过个人观点模块建立独特IP辨识度

---

## 技能简介

本技能为公众号运营者提供完整的IP保护方案，包含：
1. **水印保护**：文字水印和图片水印双重机制
2. **观点IP**：通过专业观点输出建立不可复制的个人品牌

**核心价值**：个人经历 + 专业观点 = 不可复制的IP

---

## 参数配置

```yaml
# === 作者信息配置 ===
author:
  name: "老胡"                           # 作者简称
  full_name: "老胡说"                     # 公众号名称
  title: "技术成果转化咨询师"             # 身份标签
  background: |
    曾任央企投资公司常务副总、产权交易机构负责人
    专注技术成果转化和知识产权交易十余年
  expertise: ["技术成果转化", "知识产权交易", "投资咨询", "政策解读"]
  contact: "后台私信"                     # 联系方式提示

# === 水印配置 ===
watermark:
  # 文字水印配置
  text:
    intro: "📌 本文首发于【老胡说】，专注技术成果转化..."
    outro: "💡 原创文章，未经授权禁止转载 | 老胡说"
    style: "blockquote"                  # 普通/blockquote

  # 图片水印配置
  image:
    position: "bottom_right"              # 位置
    opacity: 0.5                          # 透明度
    font_size: 24                        # 字体大小
    padding: 20                           # 边距
    background: true                      # 是否背景

# === 观点模块配置 ===
opinion:
  # 观点类型定义
  types:
    comment:
      name: "老胡评论"
      emoji: "💬"
      color: "#2D7D9A"
      template: "【老胡评论】{content}"
      
    viewpoint:
      name: "老胡观点"
      emoji: "🎯"
      color: "#E67E22"
      template: "【老胡观点】{content}"
      
    reminder:
      name: "老胡提醒"
      emoji: "⚠️"
      color: "#27AE60"
      template: "【老胡提醒】{content}"

  # 插入规则
  rules:
    min_per_article: 1                    # 最少观点数
    max_per_article: 3                    # 最多观点数
    positions: ["关键论点后", "转折处", "总结前"]  # 插入位置
```

---

## 观点IP模块

### 核心价值

```
┌─────────────────────────────────────────────────────────┐
│                      IP = 不可复制的影响力               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   个人背景 ──┬── 真实经历（央企+产权交易十余年）         │
│              │    └── 别人无法冒充                      │
│              │                                         │
│   专业观点 ──┼── 行业洞察（政策解读+实操经验）          │
│              │    └── 独特视角                          │
│              │                                         │
│   风格特征 ──┴── 语言习惯（专业但有温度）               │
│                   └── 形成辨识度                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 观点类型说明

| 类型 | 用途 | 风格 | 示例 |
|------|------|------|------|
| 老胡评论 | 对政策/事件的解读 | 客观+洞察 | "这项政策的核心是..." |
| 老胡观点 | 基于经验的判断 | 主观+笃定 | "我认为企业应该..." |
| 老胡提醒 | 给读者的实用建议 | 关怀+实用 | "特别要注意的是..." |

### 观点插入原则

1. **适度原则**：每篇文章1-3处，不宜过多
2. **位置选择**：
   - 关键论点之后（强化观点）
   - 转折之处（引导思考）
   - 总结之前（升华主题）
3. **风格要求**：
   - 专业但不居高临下
   - 有人情味，接地气
   - 避免过于绝对

### 观点模板示例

```html
<!-- 老胡评论 -->
<div style="border-left: 4px solid #2D7D9A; padding: 12px 16px; margin: 16px 0; background: #f0f7fa;">
  <p style="margin: 0;"><strong>💬 老胡评论</strong></p>
  <p style="margin: 8px 0 0 0; color: #333;">{观点内容}</p>
</div>

<!-- 老胡观点 -->
<div style="border-left: 4px solid #E67E22; padding: 12px 16px; margin: 16px 0; background: #fef9f3;">
  <p style="margin: 0;"><strong>🎯 老胡观点</strong></p>
  <p style="margin: 8px 0 0 0; color: #333;">{观点内容}</p>
</div>

<!-- 老胡提醒 -->
<div style="border-left: 4px solid #27AE60; padding: 12px 16px; margin: 16px 0; background: #f0faf4;">
  <p style="margin: 0;"><strong>⚠️ 老胡提醒</strong></p>
  <p style="margin: 8px 0 0 0; color: #333;">{观点内容}</p>
</div>
```

---

## 文字水印规则

### 开头引导语

```
━━━━━━━━━━━━━━━━━━━━━━━━
📌 本文首发于【老胡说】
   专注技术成果转化与政策解读
━━━━━━━━━━━━━━━━━━━━━━━━
```

### 结尾声明

```
---
💡 原创文章，阅读全文请关注公众号【老胡说】
   后台回复【关键词】领取[资料名称]
```

---

## 图片水印规则

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 位置 | 右下角 | bottom_right/bottom_left/top_right/top_left |
| 透明度 | 0.5 | 0.0-1.0 |
| 字体大小 | 24px | 根据图片尺寸调整 |
| 边距 | 20px | 与边缘的距离 |
| 背景 | 是 | 半透明黑色圆角矩形 |

---

## 作者背景卡片

### 样式一：简洁版

```html
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
  <p style="margin: 0 0 10px 0;"><strong>关于老胡</strong></p>
  <p style="margin: 0; color: #666; font-size: 14px; line-height: 1.8;">
    老胡，技术成果转化咨询师，曾任央企投资公司常务副总、产权交易机构负责人，
    专注技术成果转化和知识产权交易十余年。
  </p>
</div>
```

### 样式二：详细版

```html
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 12px; color: white;">
  <p style="margin: 0 0 12px 0; font-size: 18px;"><strong>👤 关于老胡</strong></p>
  <p style="margin: 0; font-size: 14px; line-height: 1.8;">
    技术成果转化咨询师，曾任央企投资公司常务副总、产权交易机构负责人。
    <br/>专注领域：技术成果转化、知识产权交易、投资咨询、政策解读。
    <br/>十余年实战经验，陪伴数百个项目完成转化落地。
  </p>
  <p style="margin: 12px 0 0 0; font-size: 13px; opacity: 0.9;">
    📧 深度交流，后台私信 | 🔄 转发请注明出处
  </p>
</div>
```

---

## 使用方法

### AI辅助处理

在创作公众号文章时，直接说：
- "帮我添加水印和观点模块"
- "生成带IP标识的文章"
- "在关键论点处插入老胡观点"

### 代码调用

```python
from scripts.watermark import add_text_watermark, add_image_watermark
from scripts.opinion import insert_opinions, AuthorCard

# 添加文字水印
marked_content = add_text_watermark(
    content=article_content,
    intro="📌 本文首发于【老胡说】",
    outro="💡 原创文章，未经授权禁止转载"
)

# 插入观点模块
marked_content = insert_opinions(
    content=marked_content,
    author="老胡",
    types=["comment", "viewpoint", "reminder"]
)

# 生成作者卡片
author_card = AuthorCard.generate(style="detailed")

# 添加图片水印
add_image_watermark(
    image_path="input.jpg",
    output_path="output.jpg",
    text="老胡说"
)
```

---

## 文件索引

| 文件 | 用途 |
|------|------|
| SKILL.md | 技能主文件（本文档） |
| [references/watermark-guide.md](references/watermark-guide.md) | 水印设计指南 |
| [references/examples.md](references/examples.md) | 水印示例 |
| [references/opinion_templates.md](references/opinion_templates.md) | 观点模板库 |
| [scripts/text_watermark.py](scripts/text_watermark.py) | 文字水印脚本 |
| [scripts/image_watermark.py](scripts/image_watermark.py) | 图片水印脚本 |
| [scripts/opinion.py](scripts/opinion.py) | 观点模块脚本 |

---

## 版本信息

- 创建时间：2026-04-25
- 版本：v2.0
- 适用平台：微信公众号
- 核心功能：水印保护 + 观点IP
