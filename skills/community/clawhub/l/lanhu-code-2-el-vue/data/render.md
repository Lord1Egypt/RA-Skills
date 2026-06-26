# 2.3 循环渲染规范

## 2.3.1 何时使用v-for循环

**识别标准：**
- ✅ 3个或以上相似HTML结构
- ✅ class名称包含序号（如 `box_1`, `box_2`, `box_3`）
- ✅ 内容不同但结构相同的元素

## 2.3.2 实现要求

**必须满足的条件：**

| 要求项 | 说明 | 示例 |
|-------|------|------|
| ✅ 唯一key | 每个循环项必须有唯一key | `:key="item.id"` |
| ✅ 数据定义 | 数据必须在data()中定义 | `dataList: []` |
| ✅ 语义化变量 | 使用有意义的变量名 | `projectList` 而非 `list1` |
| ✅ 数据绑定 | 使用`:src`、`{{ }}`绑定数据 | `:src="item.imageUrl"` |

## 2.3.3 完整示例

**改造前（静态重复代码）：**
```vue
<template>
  <div class="list_container">
    <div class="box_1">
      <img src="img1.png" />
      <span>项目1</span>
    </div>
    <div class="box_2">
      <img src="img2.png" />
      <span>项目2</span>
    </div>
    <div class="box_3">
      <img src="img3.png" />
      <span>项目3</span>
    </div>
  </div>
</template>
```

**改造后（动态循环渲染）：**
```vue
<template>
  <div class="custom_list_container">
    <div 
      v-for="item in projectList" 
      :key="item.id"
      :class="['custom_list_item', { 'custom_list_item_selected': item.selected }]"
      @click="handleItemClick(item)"
    >
      <img :src="require(`./assets/img/${item.imageUrl}`)" class="custom_list_item_image" />
      <span class="custom_list_item_title">{{ item.title }}</span>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      projectList: [
        { id: 1, imageUrl: 'img1.png', title: '项目1', selected: false },
        { id: 2, imageUrl: 'img2.png', title: '项目2', selected: false },
        { id: 3, imageUrl: 'img3.png', title: '项目3', selected: false }
      ]
    }
  },
  methods: {
    handleItemClick(item) {
      this.projectList.forEach(p => p.selected = false)
      item.selected = true
    }
  }
}
</script>

<style scoped>
.custom_list_container {
  display: flex;
  flex-direction: row;
  gap: 16px;
}

.custom_list_item {
  padding: 12px;
  border: 1px solid #ddd;
  cursor: pointer;
}

.custom_list_item_selected {
  background-color: #e6f7ff;
  border-color: #1890ff;
}
</style>
```

## 2.3.4 图片路径处理

**⚠️ 重要：图片路径必须使用相对路径，动态绑定必须使用require**

根据项目结构，图片文件位于 `src/views/custom/assets/img/` 目录下，因此必须使用相对路径 `./assets/img/` 而不是绝对路径 `@/assets/img/`。

**关键规则：**

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| 静态图片（src写死） | `src="./assets/img/xxx.png"` | `src="@/assets/img/xxx.png"` |
| 动态绑定（:src） | `:src="require('./assets/img/' + item.img)"` | `:src="item.img"`（item.img是相对路径时） |
| data中定义图片路径 | `img: require('./assets/img/xxx.png')` | `img: './assets/img/xxx.png'` |

**静态图片引入方式：**
```vue
<!-- ✅ 正确方式1: 静态图片直接使用相对路径 -->
<img src="./assets/img/logo.png" />

<!-- ✅ 正确方式2: 动态绑定使用require（推荐） -->
<img :src="require(`./assets/img/${item.imageUrl}`)" />

<!-- ✅ 正确方式3: 在data中预处理require -->
<script>
export default {
  data() {
    return {
      projectList: [
        { id: 1, imageUrl: require('./assets/img/img1.png'), title: '项目1' }
      ]
    }
  }
}
</script>
<template>
  <img :src="item.imageUrl" />
</template>

<!-- ❌ 错误方式1: 使用@别名路径（会找不到文件） -->
<img src="@/assets/img/img1.png" />

<!-- ❌ 错误方式2: 动态绑定直接使用相对路径字符串 -->
<img :src="item.imageUrl" />
<!-- 如果item.imageUrl = './assets/img/xxx.png'，图片无法显示 -->
```

**路径说明：**
- ✅ **正确路径**: `./assets/img/` - 相对于当前Vue文件的路径
- ❌ **错误路径**: `@/assets/img/` - 项目根目录别名路径（在此项目中不适用）
- ✅ **文件结构**: `src/views/custom/assets/img/图片文件.png`

## 2.3.6 CSS 背景图片路径处理（⭐新增重要规则）

**⚠️ 问题背景：**
当从 `assets/index.css` 复制样式到 `Custom.vue` 时，CSS 中的背景图片路径必须保持原样，不得修改。

**原始文件结构：**
```
src/views/${folderName}/
├── assets/
│   ├── index.css          # 原始样式文件，路径：url(./img/xxx.png)
│   └── img/               # 图片文件夹
│       └── xxx.png
└── Custom.vue             # 生成的目标文件
```

**关键规则：**

| 场景 | 正确做法 | 错误做法 |
|------|---------|---------|
| **Template 中的 &lt;img&gt; 标签** | `:src="require('./assets/img/xxx.png')"` | `:src="require('./img/xxx.png')"` |
| **CSS 中的 background-image** | `url(./img/xxx.png)`（保持原样） | `url(./assets/img/xxx.png)`（错误修改） |
| **data() 中定义的图片路径** | `img: require('./assets/img/xxx.png')` | `img: require('./img/xxx.png')` |

**为什么 CSS 路径必须保持原样？**
- 原始 `index.css` 在 `assets/` 目录下，所以它使用 `url(./img/...)` 是正确的
- 当把 CSS 内联到 `Custom.vue` 中时，webpack 会根据原始 CSS 文件的上下文正确解析路径
- 如果修改路径为 `url(./assets/img/...)`，会导致图片找不到

**完整示例：**

**原始 index.css 中的样式：**
```css
/* ✅ 原始路径，保持不变 */
.main_group {
  background: url(./img/background.png) 100% no-repeat;
  background-size: 100% 100%;
}
```

**Custom.vue 中的样式（正确）：**
```vue
<style scoped>
/* ✅ 保持原始路径不变 */
.shushi_main_group {
  background: url(./img/background.png) 100% no-repeat;
  background-size: 100% 100%;
}
</style>

<template>
  <!-- ✅ Template 中的 img 标签使用 ./assets/img/ -->
  <img :src="require('./assets/img/logo.png')" />
</template>
```

**Custom.vue 中的样式（错误）：**
```vue
<style scoped>
/* ❌ 错误：修改了路径 */
.shushi_main_group {
  background: url(./assets/img/background.png) 100% no-repeat;
  background-size: 100% 100%;
}
</style>
```

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

**为什么动态绑定必须使用require？**

Vue CLI使用webpack打包，只有使用 `require()` 或 `import` 引入的图片，webpack才能：正确解析图片路径、将图片复制到dist目录、返回打包后的最终URL。直接使用字符串路径，webpack无法识别，图片不会被打包，导致404错误。

## 2.3.5 常见错误避免

❌ **错误示例：**
```vue
<!-- 错误1: 缺少key -->
<div v-for="item in list">

<!-- 错误2: 使用index作为key（数据有增删操作时） -->
<div v-for="(item, index) in list" :key="index">

<!-- 错误3: 数据未定义 -->
<div v-for="item in projectList" :key="item.id">
<!-- 但data()中没有projectList -->

<!-- 错误4: 动态绑定图片路径错误 -->
<img :src="item.imageUrl" />
<!-- 但imageUrl是相对路径字符串，应使用require -->

<!-- 错误5: data中图片路径未使用require -->
data() {
  return {
    imageUrl: './assets/img/xxx.png'  // ❌ 错误
    imageUrl: require('./assets/img/xxx.png')  // ✅ 正确
  }
}
```

✅ **正确示例：**
```vue
<div 
  v-for="item in projectList" 
  :key="item.id"
  class="custom_list_item"
>
  <img :src="require(`./assets/img/${item.imageUrl}`)" />
  <span>{{ item.title }}</span>
</div>
```
