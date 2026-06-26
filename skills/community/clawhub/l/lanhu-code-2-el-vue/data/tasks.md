# 四、任务清单（严格按顺序执行）

### 🎯 任务执行总览

| 任务编号 | 任务名称 | 是否必须 | 预计耗时 | 输出产物 |
|---------|---------|---------|---------|---------|
| 任务1 | 页面结构分析 | ✅ 必须 | 5-10分钟 | 分析报告 |
| 任务2 | 筛选项组件开发 | ⭕ 可选 | 10-15分钟 | 筛选组件代码 |
| 任务3 | 列表组件开发 | ✅ 必须 | 15-20分钟 | 列表组件代码 |
| 任务4 | Element UI替换 | ✅ 必须 | 20-30分钟 | 组件替换代码 |
| 任务5 | 其他部分渲染 | ✅ 必须 | 10-15分钟 | 完整页面代码 |

---

### 任务1: 页面结构分析 ⭐（必须第一步执行）

**🎯 目标：** 全面分析源文件，输出详细的改造计划

**📋 执行步骤：**

#### 步骤1: 读取并理解源文件

**只允许读取：** 当前 `src/views/${folderName}/index.vue` 与 **index.vue 所引用**的样式文件（及链式 `@import`）。**禁止**打开其他视图、其他 `Custom.vue`、`create.md`、路由等作为分析或生成依据。

```javascript
需要分析的内容：
1. HTML结构层次
   - 页面整体布局（单栏/双栏/多栏）
   - 主要区块划分
   - 元素嵌套关系
   
2. CSS样式特征
   - 关键颜色值
   - 字体和尺寸
   - 间距和对齐方式
   
3. 交互逻辑
   - 点击事件
   - 状态切换
   - 数据绑定点
```

#### 步骤2: 识别重复结构

**识别方法：**
```javascript
1. 相似class名称（序号模式）
   示例: box_1, box_2, box_3
        text_91, text_94, text_96
        
2. 相同HTML结构
   <div class="item">...</div>
   <div class="item">...</div>
   <div class="item">...</div>
   
3. 列表容器特征
   - class包含: list, group, container
   - 包含3个或以上相似子元素
```

**输出格式：**
```javascript
{
  loopStructures: [
    {
      // 容器信息
      container: {
        class: 'group_4',
        htmlTag: 'div'
      },
      // 列表项信息
      items: [
        { class: 'box_91', index: 0 },
        { class: 'box_94', index: 1 },
        { class: 'box_96', index: 2 }
      ],
      // 数据定义
      dataName: 'coursePageList',  // 在data()中的变量名
      description: '课件列表项',
      itemCount: 3,
      // 动态字段
      dynamicFields: [
        { name: 'pageNum', type: 'string', sample: '第1页' },
        { name: 'thumbnail', type: 'string', sample: 'img/thumb1.png' },
        { name: 'selected', type: 'boolean', sample: false }
      ]
    }
  ]
}
```

#### 步骤3: 识别Element UI替换点

**替换映射表：**

| 源HTML元素 | Element UI组件 | 识别特征 | 优先级 |
|-----------|---------------|---------|-------|
| `<input type="text">` | `el-input` | 输入框 | 🔴 高 |
| `<input type="textarea">` | `el-input type="textarea"` | 多行文本 | 🔴 高 |
| `<select>` | `el-select` + `el-option` | 下拉选择 | 🔴 高 |
| 分页HTML结构 | `el-pagination` | 页码按钮组 | 🟠 中 |
| 弹窗HTML结构 | `el-dialog` | 固定定位+遮罩 | 🟠 中 |
| `<input type="radio">` | `el-radio-group` + `el-radio` | 单选按钮组 | 🟡 低 |
| `<input type="checkbox">` | `el-checkbox` | 复选框 | 🟡 低 |
| 日期输入 | `el-date-picker` | 日期格式输入 | 🟡 低 |

**⚠️ 易遗漏的识别（必须检查）：**
- **输入框**：若页面存在「可由用户编辑的文本」（如公式栏、搜索框、关键词输入），即使用户可见为 `<span>{{ value }}</span>` 或静态稿未出现 `<input>`，也须识别为 `el-input` 并列入 elementComponents。详见 `data/element-ui-style.md` 第四部分 4.3.1 节。
- **多选框**：若存在「布尔开关/勾选」语义（如「隐藏 xxx」「显示 xxx」「是否 xxx」、图标+文字可点击切换），即使源实现为多个 `<div @click>`，也须识别为 `el-checkbox` 或 `el-checkbox-group` 并列入 elementComponents。详见同上。

**输出格式：**
```javascript
{
  elementComponents: [
    {
      location: '页面底部',
      original: {
        type: 'pagination',
        html: '<div class="pagination">...',
        class: 'pagination_wrapper'
      },
      replace: {
        component: 'el-pagination',
        props: ['current-page', 'page-size', 'total'],
        events: ['size-change', 'current-change']
      },
      priority: 'high'
    }
  ]
}
```

#### 步骤4: 输出完整分析报告

**报告模板：**
```javascript
{
  // 1. 页面概况
  overview: {
    pageType: 'PC端管理页面',
    layout: '双栏布局',
    complexity: 'medium',
    estimatedTime: '60分钟'
  },
  
  // 2. 需要循环渲染的结构
  loopStructures: [...],
  
  // 3. 需要替换的组件
  elementComponents: [...],
  
  // 4. 静态部分
  staticParts: [
    { description: '页面头部', class: 'header_container' },
    { description: '侧边栏', class: 'sidebar_menu' },
    { description: '页面底部', class: 'footer_copyright' }
  ],
  
  // 5. 数据结构定义
  dataStructure: {
    // data()中需要定义的数据
    coursePageList: [],
    currentPage: 1,
    pageSize: 10,
    total: 0,
    searchKeyword: '',
    selectedId: null
  },
  
  // 6. 方法列表
  methods: [
    'handlePageChange',
    'handleSizeChange',
    'handleSearch',
    'handleItemClick',
    'handleDelete'
  ]
}
```

**✅ 验证标准：**
- [ ] 已识别所有重复结构（容器和item）
- [ ] 已标记每个结构的动态数据字段
- [ ] 已列出所有可替换的Element UI组件
- [ ] 已输出完整分析结果
- [ ] 分析结果清晰易懂，可直接指导后续开发

---

### 任务2: 筛选项组件开发（如存在）

**目标：** 将筛选按钮改为循环渲染，视觉效果一致

**识别方法：**
- 查找3个或以上的相似筛选按钮/标签
- class通常包含 `filter`, `tag`, `tab` 关键词
- 有激活/选中状态的样式

**执行步骤：**
1. 提取筛选项HTML结构
2. 定义数据结构（在 `data()` 中）
3. 使用v-for循环渲染，绑定动态class和事件
4. 复制并重命名样式（按标准2匹配）
5. 实现点击切换激活状态的方法

**代码示例：**
```vue
<template>
  <div class="mount_filter_container">
    <div 
      v-for="item in filterList" 
      :key="item.id"
      :class="['mount_filter_item', { 'mount_filter_item_active': item.active }]"
      @click="handleFilterClick(item)"
    >
      {{ item.label }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filterList: [
        { id: 1, label: '全部', active: true },
        { id: 2, label: '已评', active: false },
        { id: 3, label: '未评', active: false }
      ]
    }
  },
  methods: {
    handleFilterClick(item) {
      this.filterList.forEach(i => i.active = false)
      item.active = true
    }
  }
}
</script>
```

**验证标准：**
- ✅ 通过v-for循环渲染，数量一致
- ✅ 三种状态样式（默认/hover/激活）完全一致
- ✅ 点击切换功能正常
- ✅ class已重命名为规范格式

---

### 任务3: 列表组件开发（Grid/Flex布局）⭐（必须）

**目标：** 将列表改为循环渲染，使用Grid或Flex布局，视觉效果一致

**识别方法：**
- 查找包含3个或以上相似项的容器
- 列表项有相似的class名称
- 容器class包含 `list`, `group`, `container` 关键词

**执行步骤：**
1. 识别列表容器和列表项结构
2. 提取单个列表项的完整HTML
3. 定义数据结构（在 `data()` 中）
4. 使用v-for循环，替换静态内容为数据绑定
5. 确定布局方式，计算高度，设置溢出
6. 复制并重命名样式（按标准1完整匹配）
7. 实现交互逻辑（点击选中等）

**代码示例：**
```vue
<template>
  <div class="mount_list_container">
    <div 
      v-for="item in listData" 
      :key="item.id"
      :class="['mount_list_item', { 'mount_list_item_selected': item.selected }]"
      @click="handleItemClick(item)"
    >
      <img :src="require(`@/assets/img/${item.imageUrl}`)" class="mount_list_item_image" />
      <div class="mount_list_item_title">{{ item.title }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      listData: [
        { id: 1, imageUrl: 'img1.png', title: '项目1', selected: false },
        { id: 2, imageUrl: 'img2.png', title: '项目2', selected: false }
      ]
    }
  },
  methods: {
    handleItemClick(item) {
      item.selected = !item.selected
    }
  }
}
</script>
```

**验证标准：**
- ✅ 通过v-for循环渲染，数量一致
- ✅ 列表项样式完全一致（默认、hover、选中状态）
- ✅ 布局方式一致（Grid或Flex）
- ✅ 交互功能正常
- ✅ 使用开发者工具验证像素级一致
---

### 任务4: Element UI组件替换（通用流程）

**目标：** 将原生HTML元素替换为Element UI组件，保持视觉效果一致

**通用执行步骤：**
1. **识别原组件** - 记录HTML结构和样式
2. **替换为Element UI组件** - 配置组件属性，绑定事件处理器
3. **删除原有代码** - 删除被替换的原HTML代码
4. **样式匹配** - 使用深度选择器覆盖组件样式
5. **功能实现（必须同步完成）** - **在替换组件的同时，立即在 `data()` 中定义所需数据，在 `methods` 中实现所有事件处理方法**
   - ⚠️ **可点击的按钮必须添加点击方法**：页面中所有可点击的按钮（如「上传」「预览」「确定」「取消」「智能合成」等）须在 template 中绑定 `@click="handleXxx"`，并在 `methods` 中实现对应的 `handleXxx` 方法
   - ⚠️ **禁止只写template不写methods**：每个组件的事件绑定（如 `@click`、`@change`、`@size-change`）都必须有对应的处理方法
   - ⚠️ **禁止只写methods不写data**：所有方法中使用的数据变量都必须在 `data()` 中定义初始值
   - ⚠️ **方法命名规范**：使用 `handle` 前缀 + 事件类型或按钮功能（如 `handleSizeChange`、`handleDialogClose`、`handleUploadImage`、`handlePreview`）
6. **验证测试** - 确保样式和功能完全一致，所有方法正常工作

#### 4.1 分页组件 (el-pagination)

**识别特征：** 页码按钮、上下页按钮、总条数显示、每页条数选择器

**替换示例：**
```vue
<template>
  <div class="mount_pagination_container">
    <el-pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 50]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 分页相关数据（必须定义）
      currentPage: 1,      // 当前页码
      pageSize: 10,        // 每页显示条数
      total: 0             // 总数据条数
    }
  },
  methods: {
    // 每页条数改变时触发（必须实现）
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1  // 重置到第一页
      // 这里可以调用数据加载方法，如：this.loadData()
    },
    // 当前页改变时触发（必须实现）
    handleCurrentChange(val) {
      this.currentPage = val
      // 这里可以调用数据加载方法，如：this.loadData()
    }
  }
}
</script>

<style scoped>
.mount_pagination_container ::v-deep .el-pagination {
  /* 匹配原始样式 */
}
.mount_pagination_container ::v-deep .el-pagination__total {
  color: #333;
  font-size: 14px;
}
</style>
```

**验证标准：**
- ✅ 使用el-pagination组件，配置正确
- ✅ 原有分页代码已全部删除
- ✅ 所有样式完全一致
- ✅ **data()中已定义所有必需数据**：`currentPage`、`pageSize`、`total` 等
- ✅ **methods中已实现所有事件处理方法**：`handleSizeChange`、`handleCurrentChange` 等
- ✅ 分页功能正常，所有方法可以正常调用

#### 4.2 弹窗组件 (el-dialog)

**识别特征：** 固定定位的弹窗结构、遮罩层、关闭按钮

**替换示例：**
```vue
<template>
  <el-dialog
    :visible.sync="dialogVisible"
    width="600px"
    :show-close="true"
    @close="handleDialogClose"
  >
    <template #title>
      <div class="mount_dialog_title">标题</div>
    </template>
    <div class="mount_dialog_content">
      <!-- 弹窗内容 -->
    </div>
    <template #footer>
      <el-button @click="handleDialogCancel">取消</el-button>
      <el-button type="primary" @click="handleDialogConfirm">确定</el-button>
    </template>
  </el-dialog>
</template>

<script>
export default {
  data() {
    return {
      // 弹窗显示状态（必须定义）
      dialogVisible: false
    }
  },
  methods: {
    // 打开弹窗方法（可选，根据实际需求）
    handleOpenDialog() {
      this.dialogVisible = true
    },
    // 关闭弹窗时触发（必须实现）
    handleDialogClose() {
      // 可以在这里执行关闭前的清理操作
      this.dialogVisible = false
    },
    // 取消按钮点击（必须实现）
    handleDialogCancel() {
      this.dialogVisible = false
    },
    // 确定按钮点击（必须实现）
    handleDialogConfirm() {
      // 执行确认操作
      // 例如：保存数据、提交表单等
      this.dialogVisible = false
    }
  }
}
</script>
```

#### 4.3 输入框组件 (el-input)

**识别特征：** `<input>` 标签、带字数限制的文本框。若为**带外框的搜索框**（如「搜索资源标题、ID」），除本小节外须同时符合 **2.4.5 搜索框（带外框的 el-input）样式规范**。

**替换示例：**
```vue
<template>
  <!-- 普通输入框 -->
  <el-input 
    v-model="inputValue" 
    placeholder="请输入内容"
    class="mount_input"
    @change="handleInputChange"
    @blur="handleInputBlur"
  />
  
  <!-- 带字数限制的输入框 -->
  <el-input
    v-model="textValue"
    type="textarea"
    :maxlength="20"
    show-word-limit
    class="mount_textarea"
    @change="handleTextareaChange"
  />
</template>

<script>
export default {
  data() {
    return {
      // 输入框数据（必须定义）
      inputValue: '',    // 普通输入框的值
      textValue: ''       // 文本域的值
    }
  },
  methods: {
    // 输入框值改变时触发（可选，根据实际需求）
    handleInputChange(val) {
      // 可以在这里执行验证、格式化等操作
      console.log('输入值改变:', val)
    },
    // 输入框失去焦点时触发（可选，根据实际需求）
    handleInputBlur() {
      // 可以在这里执行验证操作
    },
    // 文本域值改变时触发（可选，根据实际需求）
    handleTextareaChange(val) {
      // 可以在这里执行字数检查、内容验证等操作
      console.log('文本域值改变:', val)
    }
  }
}
</script>

<style scoped>
.mount_input ::v-deep .el-input__inner {
  height: 40px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>
```

#### 4.4 其他常用组件

**下拉选择 (el-select)：**
```vue
<template>
  <el-select v-model="selectedValue" placeholder="请选择" @change="handleSelectChange">
    <el-option
      v-for="item in selectOptions"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script>
export default {
  data() {
    return {
      // 下拉选择数据（必须定义）
      selectedValue: '',           // 选中的值
      selectOptions: [             // 选项列表
        { value: 'option1', label: '选项1' },
        { value: 'option2', label: '选项2' }
      ]
    }
  },
  methods: {
    // 选择改变时触发（必须实现）
    handleSelectChange(val) {
      console.log('选中的值:', val)
      // 可以在这里执行根据选择值进行的操作
    }
  }
}
</script>
```

**下拉菜单 (el-dropdown)：**
```vue
<template>
  <el-dropdown @command="handleDropdownCommand">
    <span class="mount_dropdown_trigger">下拉菜单</span>
    <el-dropdown-menu slot="dropdown">
      <el-dropdown-item command="a">选项1</el-dropdown-item>
      <el-dropdown-item command="b">选项2</el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
export default {
  methods: {
    // 下拉菜单命令处理（必须实现）
    handleDropdownCommand(command) {
      console.log('选择的命令:', command)
      // 根据command执行不同的操作
      if (command === 'a') {
        // 执行选项1的操作
      } else if (command === 'b') {
        // 执行选项2的操作
      }
    }
  }
}
</script>
```

**进度条 (el-progress)：**
```vue
<template>
  <el-progress :percentage="progressPercentage" :stroke-width="10" />
</template>

<script>
export default {
  data() {
    return {
      // 进度条数据（必须定义）
      progressPercentage: 0  // 进度百分比（0-100）
    }
  },
  methods: {
    // 更新进度的方法（可选，根据实际需求）
    updateProgress(value) {
      this.progressPercentage = value
    }
  }
}
</script>
```

**日期选择器 (el-date-picker)：**
```vue
<template>
  <el-date-picker
    v-model="selectedDate"
    type="date"
    placeholder="选择日期"
    @change="handleDateChange"
  />
</template>

<script>
export default {
  data() {
    return {
      // 日期数据（必须定义）
      selectedDate: null  // 选中的日期
    }
  },
  methods: {
    // 日期改变时触发（必须实现）
    handleDateChange(val) {
      console.log('选择的日期:', val)
      // 可以在这里执行日期相关的操作
    }
  }
}
</script>
```

**提示 (el-tooltip)：**
```vue
<template>
  <el-tooltip content="提示文字" placement="top">
    <span>鼠标悬停显示提示</span>
  </el-tooltip>
</template>

<script>
// tooltip组件通常不需要额外的data和methods，但如果需要动态内容，可以这样：
export default {
  data() {
    return {
      tooltipContent: '提示文字'  // 动态提示内容（可选）
    }
  }
}
</script>
```

**单选框 (el-radio)：**
```vue
<template>
  <el-radio-group v-model="radioValue" @change="handleRadioChange">
    <el-radio :label="1">选项1</el-radio>
    <el-radio :label="2">选项2</el-radio>
  </el-radio-group>
</template>

<script>
export default {
  data() {
    return {
      // 单选框数据（必须定义）
      radioValue: 1  // 选中的值
    }
  },
  methods: {
    // 单选框改变时触发（必须实现）
    handleRadioChange(val) {
      console.log('选中的值:', val)
      // 可以在这里执行根据选择值进行的操作
    }
  }
}
</script>
```

**多选框 (el-checkbox)：**
```vue
<template>
  <el-checkbox-group v-model="checkboxList" @change="handleCheckboxChange">
    <el-checkbox label="选项1"></el-checkbox>
    <el-checkbox label="选项2"></el-checkbox>
  </el-checkbox-group>
</template>

<script>
export default {
  data() {
    return {
      // 多选框数据（必须定义）
      checkboxList: []  // 选中的值数组，如：['选项1', '选项2']
    }
  },
  methods: {
    // 多选框改变时触发（必须实现）
    handleCheckboxChange(val) {
      console.log('选中的值:', val)
      // 可以在这里执行根据选择值进行的操作
    }
  }
}
</script>
```

**其他可用组件：**
- `el-switch` - 开关
- `el-slider` - 滑块
- `el-rate` - 评分
- `el-tag` - 标签
- `el-badge` - 徽标
- `el-alert` - 警告提示

#### 4.5 评分组件 (el-rate) 的特殊注意事项

**核心原则：完全以原始页面为准**

1. **星星颜色对照原始页面**
   - 打开 `{sourcePath}/index.vue` 查看原始页面的星星颜色效果
   - 选中状态的星星颜色是什么颜色（黄色、橙色、金色？）就配置什么颜色
   - 未选中状态的星星颜色也必须与原始页面一致

2. **评分数值对照原始页面**
   - 观察原始页面每个评分维度显示几颗实心星
   - 例如：色彩5颗、构图5颗、想象力3颗，改造后数据也必须这样设置
   - ❌ 不要全部默认设为5星或全部设为3星

3. **文字样式对照原始页面**
   - "超赞"或其他评分文字的颜色、大小、位置必须与原始页面一致
   - 使用浏览器开发者工具对比，确保像素级匹配

4. **样式覆盖方法**
   - Element UI组件的默认样式必须使用深度选择器 `::v-deep` 才能覆盖
   - 星星图标、文字、间距等所有样式都需要通过深度选择器精确匹配

**常见错误：**
- ❌ 所有评分维度都默认设为5星（忽略了原始页面的实际显示）
- ❌ 星星颜色使用橙色，但原始页面是黄色
- ❌ 忘记使用深度选择器，导致样式无法覆盖

---

### 任务5: 其他页面部分渲染

**目标：** 渲染尚未处理的静态部分，视觉效果一致

**执行步骤：**
1. **识别未处理部分**
   - 页面头部 (header)
   - 页面底部 (footer)
   - 侧边栏 (sidebar)
   - 其他静态内容区域

2. **复制HTML结构** - 从源文件复制完整HTML

3. **重命名class** - 按命名规范重命名所有class

4. **匹配样式** - 从源CSS复制样式，更新选择器

5. **验证一致性** - 使用开发者工具对比

**验证标准：**
- ✅ 所有页面部分都已处理（无遗漏）
- ✅ 所有 class 已重命名为规范格式（sourceName_*，仅下划线、无数字）
- ✅ 所有样式完全一致
- ✅ 页面完整可正常显示
- ✅ **Custom.vue 未引用 index.css**：不得使用 `<style src="./assets/index.css">` 或 `@import "./assets/index.css"`；样式须全部写在 `<style scoped>` 内，且选择器为已重命名类名（若未替换，按 `data/class-naming.md` 2.5 节识别与修复）

---
