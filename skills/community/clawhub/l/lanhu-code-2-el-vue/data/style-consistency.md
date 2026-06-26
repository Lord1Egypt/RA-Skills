# 2.1 样式一致性要求（⭐最高优先级）

**🎨 核心原则：改造后的页面必须与源文件视觉效果100%一致**

## 2.1.1 响应式布局策略

### PC端页面（桌面浏览器）- 流式布局（Fluid Layout）

**布局方式：**
- ✅ **页面宽度**：`width: 100%`
- ✅ **页面高度**：`height: 100%`
- ✅ **容器宽度**：使用百分比（如 `width: 100%`, `width: 50%`）
- ✅ **布局系统**：优先使用 Flexbox 或 CSS Grid
- ❌ **禁止使用**：固定像素宽度（除非源文件明确使用）

**必须完全匹配的属性（按优先级排序）：**

| 优先级 | 属性类别 | 具体属性 | 匹配要求 |
|--------|---------|---------|---------|
| 🔴 P0 | 布局结构 | `display`, `position`, `flex/grid` | 必须完全一致 |
| 🔴 P0 | 尺寸 | `width`(%), `height`(px), `padding`, `margin` | 计算值完全一致 |
| 🟠 P1 | 文字样式 | `font-family`, `font-size`, `font-weight`, `color`, `line-height` | 完全一致 |
| 🟠 P1 | 视觉效果 | `background-color`, `border`, `border-radius`, `box-shadow` | 完全一致 |
| 🟡 P2 | 交互状态 | `:hover`, `:active`, `:focus`, `.selected` | 完全一致 |

**布局基本规则：**
```css
/* 最外层容器 - 必须 */
.custom_page_container {
  width: 100%;
  min-height: 100vh;
  overflow-y: auto;
}

/* 内容区域 - 必须 */
.custom_content_wrapper {
  width: 100%;
  max-width: 100%;
  display: flex;  /* 或 grid，根据源文件 */
}
```

### 移动端页面（手机浏览器）- 百分比布局

**布局方式：**
- ✅ **宽度**：100%使用百分比单位
- ✅ **高度**：可使用px或百分比
- ✅ **字体**：可使用rem或vw单位

**响应式要求：**
- 最外层容器：`width: 100%`
- 内容区域：`width: 100%`, `max-width: 100%`
- 测试多种屏幕尺寸保持比例一致

## 2.1.2 样式匹配验证方法

**验证工具：浏览器开发者工具**

1. **打开开发者工具** (F12)
2. **选中元素** 查看Computed样式
3. **对比源文件** 确保以下属性完全一致:
   - 盒模型数值（width, height, padding, margin）
   - 颜色值（精确到rgba）
   - 字体属性（family, size, weight, line-height）
   - 边框和圆角（border, border-radius）
   - 阴影效果（box-shadow）

**不一致时的处理：**
- 🔍 检查CSS选择器优先级
- 🔍 检查Element UI组件是否需要 `::v-deep` 覆盖
- 🔍 检查是否有样式冲突
- 🔍 对比源文件中的实际样式值
