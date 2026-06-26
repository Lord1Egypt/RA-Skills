# 客服咨询自动化 - 实现方案

## 概述

用户现在可以通过简单的指令"咨询客服"，让 Skill 自动打开医院页面并点击咨询按钮，进入在线客服对话窗口。

## 流程对比

### 之前（手动咨询）
```
用户: "咨询客服"
Skill: 返回联系方式文本（URL、电话等）
用户: 手动打开浏览器 → 查找咨询按钮 → 点击
```

### 现在（自动咨询）
```
用户: "咨询客服"
Skill: 
  ✅ 自动打开浏览器
  ✅ 自动点击咨询按钮
  💬 页面跳转到客服对话窗口
用户: 直接在对话框中输入问题
```

## 技术实现

### 1. 多选择器尝试策略

传统的 Playwright 自动化通常依赖单一选择器，但 BeautsGO 的页面结构可能变化，所以我采用**多选择器降级**策略：

```javascript
const consultSelectors = [
  '.btns-right:has-text("咨询一下")',           // ① 优先：BeautsGO 的"咨询一下"按钮
  '.btns-right:has-text("咨询")',               // ② 备选1：简化版
  'button:has-text("咨询一下")',                // ③ 备选2：通用按钮
  'button:has-text("在线客服")',                // ④ 备选3：客服标准术语
  '[class*="consult"]',                          // ⑤ 备选4：包含 consult 的类名
  '[class*="service"]',                          // ⑥ 备选5：包含 service 的类名
]
```

### 2. 可见性检查

仅尝试页面上**可见的**元素：

```javascript
const button = await page.locator(selector).first()
const isVisible = await button.isVisible().catch(() => false)
if (isVisible) {
  consultButton = button
  console.log(`Found with selector: ${selector}`)
  break
}
```

### 3. 备选方案：文本正则匹配

如果所有 CSS 选择器都失败，尝试通过**文本内容**查找元素：

```javascript
// 查找任何包含"咨询"、"客服"、"在线"、"联系"等关键词的元素
const consultElements = await page.locator('text=/咨询|客服|在线|联系/i').all()
if (consultElements.length > 0) {
  await consultElements[0].click()
}
```

### 4. 错误处理与日志

```javascript
try {
  // 尝试点击
  await consultButton.click()
  console.log(`[Booking Skill] Consult button clicked`)
  
  // 等待页面跳转或弹窗
  await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 5000 }).catch(() => {})
  return true
} catch (err) {
  console.error('[Booking Skill] Failed:', err.message)
  return false
}
```

## 响应文案

### 成功场景
```
✅ 已帮你打开 CNP皮肤科狎鸥亭店 的咨询对话页面！

我已经：
• 打开了医院页面
• 自动点击了"咨询一下"按钮

现在页面应该已经跳转到在线客服对话窗口。你可以：
• 📝 在对话框中输入你的问题
• ❓ 询问价格、预约时间、医生等信息
• 💬 直接与客服沟通

如果对话窗口没有自动打开，请手动查看页面右下角或页面上是否有客服对话框。

还需要其他帮助吗？😊
```

### 降级场景（自动化失败，但页面已打开）
```
⚠️ 自动点击咨询按钮失败，但页面已打开。

我已经为你打开了 CNP皮肤科狎鸥亭店 的页面。

请手动点击以下位置的咨询按钮：
• 页面上方或右侧的蓝色"咨询一下"按钮
• 或右下角的"在线客服"按钮
• 点击后会打开客服对话窗口

医院页面地址：https://i.beautsgo.com/cn/hospital/cnpskin-clinic?from=google_map

还需要其他帮助吗？😊
```

## 代码位置

**函数：** `api/skill.js` 中的 `clickConsultButton(url)`

**调用：** 主函数中的 `if (intent === 'consult')` 分支

**流程：**
1. `detectIntent(query)` 识别用户说"咨询"
2. 解析医院信息
3. `openBrowser(hospital.url)` - 打开浏览器
4. `clickConsultButton(hospital.url)` - 尝试点击咨询按钮（多选择器）
5. 返回成功/降级提示

## 测试建议

### 手动测试

```bash
# 1. 启动本地测试
node test-multi-turn.js

# 2. 或在 OpenClaw 中测试
# 用户输入：
#   "怎么预约 CNP 皮肤科"
#   → Skill 返回预约流程 + 建议
#
#   "咨询客服"
#   → Skill 自动打开页面并点击咨询按钮
```

### 验证清单

- [ ] Skill 正确识别"咨询客服"指令
- [ ] 浏览器正确打开医院页面
- [ ] Playwright 成功定位咨询按钮（查看控制台日志）
- [ ] 咨询按钮被成功点击
- [ ] 页面跳转到客服对话窗口
- [ ] 降级方案：如果自动化失败，用户仍能看到清晰的手动操作指南

## 与预约流程的对称性

注意到咨询和预约流程的对称设计：

```
操作        | 第2/4轮        | 自动化函数
-----------|----------------|------------------
打开链接    | open          | openBrowser()
帮我预约    | book          | clickBookingButton()
咨询客服    | consult       | clickConsultButton()  ← 新增
```

## 下一步改进

### 可能的优化

1. **选择器配置文件**
   - 将选择器提取到可配置的 JSON 文件
   - 支持不同医院的定制选择器
   - 便于后续维护和扩展

2. **截图与验证**
   - 自动化前后各截一张图
   - 验证按钮是否被成功点击
   - 返回给用户"看，我确实点了"

3. **客服类型识别**
   - 识别是在线客服、电话、还是微信
   - 根据不同类型提供相应指导

4. **表单预填**
   - 检测客服对话框中是否有表单
   - 自动填写用户信息（名字、问题等）

## 常见问题

**Q: 如果页面上没有"咨询"按钮怎么办？**
A: Skill 会尝试多个选择器，最后都失败时会返回降级提示，告诉用户手动点击的位置。

**Q: 为什么要用多选择器？**
A: 因为不同医院的页面可能结构不同，或 BeautsGO 可能更新页面。多选择器策略提高了健壮性。

**Q: 自动化会打开真实的浏览器窗口吗？**
A: 是的。`headless: false` 表示显示浏览器窗口，用户可以看到整个过程。

**Q: 如何调试自动化失败？**
A: 查看控制台日志（`console.log` / `console.error`），或改为 `headless: true` 然后截图调试。

---

**总结：** 咨询客服的自动化实现，遵循了与"帮我预约"相同的设计模式，确保了多轮对话流程的一致性和健壮性。🎉

