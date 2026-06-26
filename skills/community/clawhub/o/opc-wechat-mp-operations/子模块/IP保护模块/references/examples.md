# 水印示例

> 实际应用中的水印效果示例

---

## 一、文字水印示例

### 1.1 开头引导语

```
━━━━━━━━━━━━━━━━━━━━━━━━
📌 本文首发于【老胡说】
   专注技术成果转化与政策解读
━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.2 结尾声明

```
---
💡 原创文章，阅读全文请关注公众号【老胡说】
   后台回复【关键词】领取[资料名称]
```

---

## 二、图片水印示例

### 样式A：半透明背景（推荐）
```
┌────────────────────────────────┐
│                                │
│        [图片内容]              │
│                                │
│                                │
│                        ┌─────┐ │
│                        │老胡说│ │ ← 白色文字，黑色半透明背景
│                        └─────┘ │
└────────────────────────────────┘
```

### 样式B：角落小字
```
┌────────────────────────────────┐
│                                │
│        [图片内容]              │
│                                │
│                                │
│                    @老胡说    │ ← 小号字体，无背景
└────────────────────────────────┘
```

---

## 三、批量处理示例

```bash
# 批量处理图片水印
$ python scripts/image_watermark.py \
    --input ./images/ \
    --output ./images_output/ \
    --text "老胡说" \
    --opacity 0.5

# 处理完成：3张图片
```

---

## 四、HTML代码示例

### 公众号文章开头水印

```html
<div style="border-left: 4px solid #2D7D9A; padding: 12px 16px; background: #f8f9fa; margin: 20px 0;">
  <p style="margin: 0; color: #333;">
    📌 <strong>本文首发于【老胡说】</strong><br/>
    <span style="color: #666; font-size: 14px;">专注技术成果转化与政策解读</span>
  </p>
</div>
```

### 公众号文章结尾水印

```html
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="text-align: center; color: #666; font-size: 14px; padding: 20px;">
  <p>💡 原创文章，阅读全文请关注公众号【老胡说】</p>
  <p>📧 后台回复【报告】领取完整资料</p>
</div>
```

---

## 五、水印配置示例

```yaml
# config.yaml
wechat_name: "老胡说"

text_watermark:
  intro: "📌 本文首发于【老胡说】，专注技术成果转化..."
  outro: "💡 原创文章，未经授权禁止转载 | 老胡说"

image_watermark:
  position: "bottom_right"
  opacity: 0.5
  font_size: 24
  padding: 20
  background: true
```
