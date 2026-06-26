# ⚠️ 八、关键要求总结

### 8.0 唯一信息源（生成页面）

| 规则 | 说明 |
|------|------|
| ✅ **稿源范围** | 仅 `index.vue` + **index.vue 引用的**样式文件 + 上述文件中的图片等资源路径 |
| ❌ **禁止外扩** | 不得读取或参考其他工程文件生成页面内容（其他视图 `Custom.vue`/`index.vue`、`create.md`、路由、`package.json` 等） |

操作规范仍以本 Skill 与 `data/` 文档为准；`data/` 是规则书，不是页面设计稿。

### 8.1 文件操作规范（⭐核心约束）

| 规则 | 说明 | 违反后果 |
|------|------|---------|
| ❌ **禁止修改源文件** | `index.vue`及其引用的样式文件只能读取，绝对不能修改 | 破坏原始参考文件 |
| ✅ **只操作目标文件** | 所有代码只写入`Custom.vue` | 保证代码独立性 |
| ✅ **使用scoped样式** | 所有样式必须在`<style scoped>`中定义 | 避免样式污染 |
| ✅ **完整单文件组件** | Custom.vue必须包含template、script、style三部分 | 保证组件完整性 |

#### 8.1.1 执行前路径验证要求（⭐新增）

**⚠️ 开始改造前必须验证源文件存在性，否则会导致生成失败：**

**强制检查清单（执行前必须完成）：**
```javascript
// 步骤1: 验证源文件存在
必须存在: src/views/${folderName}/index.vue
// 样式：以 index.vue 实际引用为准逐项验证（常见为 assets/index.css）

// 步骤2: 验证目标路径
目标文件: src/views/${folderName}/Custom.vue

// 步骤3: 排除路径混淆
❌ 禁止读取: ${folderName}/index.vue  (根目录)
✅ 必须读取: src/views/${folderName}/index.vue

❌ 禁止输出: ${folderName}/Custom.vue  (根目录)
✅ 必须输出: src/views/${folderName}/Custom.vue
```

**路径验证失败处理：**
- 如果 `src/views/${folderName}/` 不存在 → 检查文件夹名称拼写
- 如果源文件不存在 → 确认项目结构是否符合规范
- 如果根目录存在 `${folderName}/` → 确认是否为之前错误创建，以 `src/views/` 下的为准

**验证示例（以 shushi 为例）：**
```bash
# 正确验证流程
ls src/views/shushi/index.vue          # 必须存在
# 再据 index.vue 引用确认各 css 存在
ls src/views/shushi/Custom.vue         # 生成目标

# 错误验证（会导致混淆）
ls shushi/index.vue                    # 可能是旧文件，不要以此为准
ls shushi/Custom.vue                   # 可能是错误位置生成的文件
```

### 8.2 执行原则（⭐必须遵守）

**1. 严格按顺序执行**
```
准备阶段 → 任务1 → 任务2 → 任务3 → 任务4 → 任务5 → 验证阶段
```
⚠️ 禁止跳跃执行，禁止同时执行多个任务

**2. 每个任务必须验证**
```javascript
完成任务 → 立即验证 → 确认通过 → 继续下一任务
                ↓
             发现问题 → 立即修复 → 再次验证
```

**3. 像素级匹配要求**
- 使用浏览器开发者工具对比验证
- 尺寸误差不超过1px
- 颜色必须完全一致（rgba值）
- 字体、间距必须完全一致

**4. 组件与方法同步生成**
```vue
<!-- ❌ 错误：分步执行 -->
步骤1: 写template
步骤2: 稍后写data
步骤3: 最后写methods

<!-- ✅ 正确：同步完成 -->
同时完成：
1. template中使用组件
2. data()中定义数据
3. methods中实现方法
```

**5. Element 替换：先删后写、样式一次覆盖**
- **多选/单选/按钮**：替换时必须**先删除**该区域原有表现同一交互的 DOM（如 div+img+span、div+@click），**再**写入 el-checkbox、el-radio-group+el-radio、el-button；禁止保留原 DOM 又加组件导致两套 UI 并存。单选用 el-radio 替换，样式与源页一致、选中/悬停为主题色；**开关不替换**，保留源页面原生 DOM（不使用 el-switch）。
- **样式**：替换后须在 `<style scoped>` 中用 `::v-deep` **一次写完**该组件的覆盖样式（隐藏默认方框、label 布局与源稿一致、选中态与源稿一致、按钮宽高圆角背景与源稿一致），使视觉效果与 index/设计稿一致。识别与修复方法见 **`data/element-ui-style.md`** 第 2.7～2.9 节。

### 8.3 代码规范（⭐严格要求）

**1. 命名规范**
- Class 名**仅使用下划线 `_` 连接**，**不得包含任何数字**（0-9）。序位、顺序用英文词表示（如 `first`、`second`、`left`、`right`、`main`、`sub`）。
```javascript
✅ 正确示例：
custom_header_container
custom_list_item
custom_button_primary
custom_math_cell_first
custom_theme_option_second

❌ 错误示例：
group_1              // 含数字
custom_cell_2        // 含数字
custom_option_3      // 含数字
box-1                // 使用连字符
headerBox            // 使用驼峰
hc                   // 无意义缩写
```

**⚠️ Class 重命名必须完整执行**：Custom.vue 中所有来自源文件的 class 须按 `[sourceName]_[功能]_[内容]_[特征]` 重命名，**仅用下划线连接、且不得含数字**，样式须复制到 Custom.vue 的 `<style scoped>` 并更新选择器，不得仅引用 `index.css`。命名规范与识别、修复流程见 **`data/class-naming.md`**。

**⚠️ Element UI 替换必须执行**：凡有按钮、多选、单选、输入、分页、弹窗等，须用 el-button、el-checkbox、el-radio-group+el-radio、el-input、el-pagination、el-dialog 等替换，并用 ::v-deep 保持视觉一致；禁止整页无任何 Element 组件。单选用 el-radio 替换（样式与源页一致、选中/悬停主题色）；**开关不替换**，保留原生 DOM。替换规范与识别、修复流程见 **`data/element-ui-style.md`**、**`data/recognition-and-fix.md`**。

**2. 结构完整性**
```vue
<template>
  <!-- 必须有根元素 -->
  <div class="custom_page_container">
    <!-- 页面内容 -->
  </div>
</template>

<script>
// 必须导出对象
export default {
  name: 'BB',          // 必须有name
  data() {             // 必须有data
    return {}
  },
  methods: {}          // 必须有methods
}
</script>

<style scoped>      
/* 必须使用scoped */
/* 必须定义所有样式 */
</style>
```

**3. 代码质量要求**
- ✅ 所有变量和方法必须有意义的命名
- ✅ 代码缩进统一（2空格或4空格）
- ✅ 没有未使用的变量和方法
- ✅ 没有console.log（除非是必要的日志）
- ✅ 没有TODO注释（必须完成所有功能）

### 8.4 数据和方法完整性（⭐关键检查）

**检查清单：**

```javascript
// 1. 所有Element UI组件都有对应的data
<el-pagination :current-page="currentPage" />
↓ 必须在data()中定义
data() {
  return {
    currentPage: 1  // ✅ 已定义
  }
}

// 2. 所有事件绑定都有对应的methods
<el-input v-model="keyword" @change="handleSearch" />
↓ 必须在methods中实现
methods: {
  handleSearch() {   // ✅ 已实现
    // ...
  }
}

// 3. 所有methods中使用的数据都已定义
methods: {
  handleSearch() {
    this.isLoading = true  // 使用了isLoading
  }
}
↓ 必须在data()中定义
data() {
  return {
    isLoading: false  // ✅ 已定义
  }
}
```

### 8.5 循环渲染样式处理规范（⭐新增重要规则）

**⚠️ 问题背景：**
在使用 `v-for` 循环渲染列表元素时，如果源 CSS 中各元素的 margin 值不一致（如第一个无 margin、中间有 margin、组间有大 margin），直接使用 `:class` 动态绑定会导致样式与源稿不一致。

**❌ 错误示例：**
```vue
<!-- 源CSS中：第一个无margin，中间margin-left:12px，第4个margin-left:171px -->
<div v-for="(digit, index) in digits" :key="index" class="custom_digit_box">
  {{ digit }}
</div>

<style>
.custom_digit_box {
  margin-left: 12px;  /* 所有元素都有12px margin，与源稿不符 */
}
.custom_digit_box:first-child {
  margin-left: 0;  /* 只能处理第一个，无法处理中间的大间距 */
}
</style>
```

**✅ 正确做法：**
```vue
<!-- 明确展开每个元素，使用特定class控制margin -->
<div class="custom_digit_box custom_digit_first">{{ digits[0] }}</div>
<div class="custom_digit_box custom_digit_middle">{{ digits[1] }}</div>
<div class="custom_digit_box custom_digit_middle">{{ digits[2] }}</div>
<div class="custom_digit_box custom_digit_gap">{{ digits[3] }}</div>  <!-- 组间大间距 -->
<div class="custom_digit_box custom_digit_middle">{{ digits[4] }}</div>

<style>
.custom_digit_first { margin-left: 0; }
.custom_digit_middle { margin-left: 12px; }
.custom_digit_gap { margin-left: 171px; }  /* 组间大间距 */
</style>
```

**识别步骤：**
1. 检查源 CSS 中各元素的 margin 值是否一致
2. 如果发现不一致（如 `margin-left: 0`、`margin-left: 12px`、`margin-left: 171px` 混合使用）
3. 说明存在**组内小间距 + 组间大间距**的布局模式
4. 必须放弃 `v-for` 循环，改为显式展开每个元素

**常见场景：**
- 竖式运算中的数字分组显示
- 表格中的列分组
- 任何需要视觉分组的列表布局

**修复自检清单：**
- [ ] 检查源 CSS 中所有同类元素的 margin 值
- [ ] 识别 margin 值的变化规律（0 → 12px → 171px）
- [ ] 为每种 margin 值创建独立的 class
- [ ] 在 template 中显式展开元素，不使用 v-for
- [ ] 验证每个元素的 margin 与源稿像素级一致

### 8.6 CSS 背景图片路径处理规范（⭐新增重要规则）

**⚠️ 问题背景：**
当从 `assets/index.css` 复制样式到 `Custom.vue` 时，CSS 中的背景图片路径必须保持原样，不得修改，否则会导致图片找不到。

**关键规则（必须遵守）：

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| **Template 中的 &lt;img&gt; 标签** | `:src="require('./assets/img/xxx.png')"` | `:src="require('./img/xxx.png')"` |
| **CSS 中的 background-image** | `url(./img/xxx.png)`（保持原样） | `url(./assets/img/xxx.png)`（错误修改） |
| **data() 中定义的图片路径** | `img: require('./assets/img/xxx.png')"` | `img: require('./img/xxx.png')"` |

**为什么 CSS 路径必须保持原样：**
- 原始 `index.css` 在 `assets/` 目录下，所以它使用 `url(./img/...)` 是正确的
- 当把 CSS 内联到 `Custom.vue` 中时，webpack 会根据原始 CSS 文件的上下文正确解析路径
- 如果修改路径为 `url(./assets/img/...)`，会导致图片找不到

**识别与修复步骤：**
1. 从 `assets/index.css` 读取样式时，记录所有 `url(./img/...)` 路径
2. 将样式复制到 `Custom.vue` 时，**保持路径完全不变**
3. 验证 CSS 中的背景图片路径都是 `url(./img/...)`
4. 验证 Template 中的 `&lt;img&gt;` 标签路径都是 `require('./assets/img/...')`

**修复自检清单：**
- [ ] 检查所有 CSS background-image 路径都是 `url(./img/...)`
- [ ] 检查所有 Template 中的 &lt;img&gt; 标签路径都是 `require('./assets/img/...')`
- [ ] 确认没有将 CSS 路径错误修改为 `url(./assets/img/...)`
- [ ] 确认没有将 Template 路径错误修改为 `require('./img/...')`

