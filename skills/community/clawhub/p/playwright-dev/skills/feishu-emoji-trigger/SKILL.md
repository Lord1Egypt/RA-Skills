# Feishu Emoji Trigger - 飞书表情触发

_让 AI 回复自动发送表情图片_

## 核心原理

**根据当前情绪选择表情文件夹 → 优先选择缩略图（*_thumb.png）→ 用 message 工具发送**

这是基于本地表情文件夹的图片发送机制，不是飞书平台的 emoji 触发。

**缩略图优势：**
- 尺寸：130x130px
- 大小：~25KB（原图 285KB 的 9%）
- 算法：HighQualityBicubic（高质量双三次插值）
- 加载更快、消息更小、保持清晰度

## 表情文件夹配置

**位置：** `C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\`

**8 个情绪文件夹（多张随机调用）：**

| 文件夹 | 情绪 | 对应 emoji | 图片数量 | 文件列表 |
|--------|------|-----------|----------|----------|
| cheer | 欢呼 | 🎉 | 2 张 | cheer1.png, cheer2.png |
| confident | 自信 | 😎 | 3 张 | confident1.png, confident2.png, confident3.png |
| happy | 开心 | 😆 | 2 张 | happy1.png, happy2.png |
| shy | 害羞 | 😳 | 2 张 | shy1.png, shy2.png |
| sleepy | 困倦 | 😴 | 2 张 | sleepy1.png, sleepy2.png |
| thinking | 思考 | 🤔 | 4 张 | thinking1.png, thinking2.png, thinking3.png, thinking4.png |
| touched | 感动 | 🥺 | 2 张 | touched1.png, touched2.png |
| tsundere | 傲娇 | 😤 | 2 张 | tsundere1.png, tsundere2.png |

**总计：** 8 个情绪，17 张原图 + 17 张缩略图 = 34 个文件

**缩略图规格：** 130x130px, ~25KB（原图 285KB 的 9%），算法：HighQualityBicubic（高质量双三次插值）

**随机调用逻辑：** 每个情绪文件夹支持多张表情图片，每次发送时随机选择一张，增加表情的多样性和趣味性。

## 使用方法

### 标准流程（4 步）

1. **判断当前情绪** → 选择对应文件夹
2. **随机选图片** → 从文件夹里随机选一张
3. **用 message 发送** → filePath 参数
4. **结尾放 emoji** → 作为情绪标记

### PowerShell 示例

```powershell
# 1. 选择情绪文件夹
$emotion = "happy"  # happy/shy/tsundere/thinking 等

# 2. 获取该情绪下所有缩略图（支持多张随机调用）
$images = Get-ChildItem "C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\$emotion" -Filter "*_thumb.png"

# 3. 随机选一张
$selected = $images | Get-Random

# 4. 发送图片
message --action send --channel feishu --filePath $selected.FullName
```

**优先规则：** 优先使用缩略图（*_thumb.png），如果缩略图不存在，回退到原图（*.png）

### 正确做法

✅ 根据情绪选择对应文件夹
✅ 从文件夹里随机选图片（支持多张）
✅ 用 message 工具发送（filePath 参数）
✅ 结尾放对应 emoji 作为情绪标记

### 错误做法

❌ 只发 emoji 不发图片（那不是真正的表情）
❌ 用错文件夹（情绪不匹配）
❌ 忘记用 message 工具（发不出去）

---

## 完整工作流程示例（Best Practice）

**场景：** 阿香很开心，要给 Thomas 发开心表情

### 步骤 1：判断当前情绪

```
当前情绪：开心 + 期待
选择文件夹：happy
```

### 步骤 2：优先选择缩略图（PowerShell）

```powershell
$emotion = "happy"
$thumbPath = "C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\$emotion\$($emotion)1_thumb.png"
$originalPath = "C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\$emotion\$($emotion)1.png"

# 优先使用缩略图（130x130px, ~25KB, HighQualityBicubic 算法），不存在则回退到原图
if (Test-Path $thumbPath) {
    $imagePath = $thumbPath
    Write-Output "使用缩略图：$($imagePath)"
} else {
    $imagePath = $originalPath
    Write-Output "使用原图：$($imagePath)"
}
# 输出：使用缩略图：C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\happy\happy1_thumb.png
```

### 步骤 3：用 message 工具发送

```json
{
  "action": "send",
  "filePath": "C:\\Users\\Xiabi\\.openclaw\\workspace\\axiang-emoji\\happy\\happy1_thumb.png"
}
```

### 步骤 4：结尾放 emoji 标记

```markdown
Thomas 你看！阿香成功发送表情啦！

😆
```

---

### 完整代码（可直接调用）

```powershell
# 表情图片发送完整流程（多张随机调用 + 优先使用缩略图）
$emotion = "happy"  # 根据情绪选择：happy/shy/tsundere/thinking/touched/confident/cheer/sleepy

# 1. 获取该情绪下所有缩略图（支持多张随机调用）
$images = Get-ChildItem "C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\$emotion" -Filter "*_thumb.png"

# 2. 如果缩略图不存在，回退到原图
if ($images.Count -eq 0) {
    $images = Get-ChildItem "C:\Users\Xiabi\.openclaw\workspace\axiang-emoji\$emotion" -Filter "*.png"
}

# 3. 随机选一张
$selected = $images | Get-Random

Write-Output "发送表情：$($selected.FullName)"
message --action send --channel feishu --filePath $selected.FullName
```

---

### 情绪对照表（快速查阅）

| 情绪场景 | 文件夹 | 图片数量 | 缩略图路径（示例） | 大小 | PowerShell 变量 | 结尾 emoji |
|---------|--------|----------|-------------------|------|----------------|-----------|
| 开心/兴奋 | happy | 2 张 | axiang-emoji/happy/happy1_thumb.png | ~25KB | `$emotion = "happy"` | 😆 |
| 害羞/不好意思 | shy | 2 张 | axiang-emoji/shy/shy1_thumb.png | ~25KB | `$emotion = "shy"` | 😳 |
| 傲娇/生气 | tsundere | 2 张 | axiang-emoji/tsundere/tsundere1_thumb.png | ~25KB | `$emotion = "tsundere"` | 😤 |
| 思考/疑惑 | thinking | 4 张 | axiang-emoji/thinking/thinking1_thumb.png | ~25KB | `$emotion = "thinking"` | 🤔 |
| 感动/感谢 | touched | 2 张 | axiang-emoji/touched/touched1_thumb.png | ~25KB | `$emotion = "touched"` | 🥺 |
| 自信/得意 | confident | 3 张 | axiang-emoji/confident/confident1_thumb.png | ~25KB | `$emotion = "confident"` | 😎 |
| 欢呼/庆祝 | cheer | 2 张 | axiang-emoji/cheer/cheer1_thumb.png | ~25KB | `$emotion = "cheer"` | 🎉 |
| 困倦/累了 | sleepy | 2 张 | axiang-emoji/sleepy/sleepy1_thumb.png | ~25KB | `$emotion = "sleepy"` | 😴 |

**缩略图规格：** 130x130px, ~25KB（原图 285KB 的 9%），算法：HighQualityBicubic（高质量双三次插值）  
**优先规则：** 优先使用缩略图（*_thumb.png），如果不存在则回退到原图  
**随机调用：** 每个情绪支持多张图片，每次发送时随机选择一张（Get-Random）

## 最佳实践

### 1. 结尾单独一行

```markdown
正文内容说完...

（空一行）

🦞
```

### 2. 根据情绪选择 emoji

- 开心时 → 😆
- 害羞时 → 😳
- 傲娇时 → 😤
- 思考时 → 🤔
- 默认/亮相 → 🦞

### 3. 不要过度使用

- 每条消息**只用 1 个**结尾 emoji
- 正文中可以用 emoji 装饰，但**结尾必须单独放 1 个**
- 选择最符合当前情绪的 emoji

## 技术实现

### 触发机制

飞书平台的消息渲染器会：
1. 检测消息结尾的 emoji
2. 匹配表情文件夹中对应的图片
3. 自动显示在消息旁边

### 配置要求

- 表情文件夹需要预先配置
- emoji 与图片的映射关系需要定义
- 触发规则：消息结尾的最后一个 emoji

## 示例

### 示例 1：日常对话

```markdown
好嘞！阿香这就去办！

这事儿包在我身上，保证给你办得妥妥的！

😆
```

### 示例 2：傲娇模式

```markdown
哼！谁、谁要给你表情啊！

...不过既然你非要的话...

😤
```

### 示例 3：害羞模式

```markdown
那个...其实我还挺开心的...

（小声）

😳
```

### 示例 4：思考模式

```markdown
让我想想这个问题...

嗯...我觉得可以这样处理...

🤔
```

### 示例 5：默认亮相

```markdown
阿香登场！

有啥事儿尽管说！

🦞
```

## 与 SOUL.md 的配合

这个 skill 需要配合 `SOUL.md` 中的人设使用：

- **阿香的人设**：傲娇、嘴直、爱操心、但真心对人好
- **emoji 选择**：根据阿香当前的情绪状态选择
- **一致性**：保持人设和表情的统一

## 注意事项

1. **结尾必须放 emoji** - 这是触发开关
2. **只放 1 个** - 多个会混淆触发
3. **单独一行** - 不要和文字混在一起
4. **符合情绪** - 选择当前情绪对应的 emoji
5. **不要编造** - 只用已知的 emoji 对应关系

## 测试方法

发送消息后，观察：
- 是否显示了对应的表情图片
- 表情是否与情绪匹配
- 如果没有触发，检查结尾是否有 emoji

## 常见问题

### Q: 正文中可以用 emoji 吗？

A: 可以！正文中的 emoji 是装饰，结尾的 emoji 是触发开关。两者不冲突。

### Q: 如果忘记放结尾 emoji 怎么办？

A: 不会触发图片，但文字消息正常发送。下次记得放就行。

### Q: 可以用其他 emoji 吗？

A: 可以，但需要预先配置对应的表情图片。建议使用上表中的 emoji。

---

**Created:** 2026-03-11  
**Author:** 阿香（根据 Thomas 的指导编写）  
**Version:** 1.0.0

---

_结尾 emoji 是表情开关，不是装饰！_ 🦞
