# 一、项目配置信息

### 1.1 文件路径配置
| 配置项 | 值 | 说明 |
|-------|-----|------|
| 文件夹名称(sourceName) | `${文件夹名称}` | 项目标识符，用作CSS类名前缀 |
| 源文件路径(sourcePath) | `src/views/${文件夹名称}` | 源文件所在目录 |
| 源文件输入 | `index.vue` + **由 index.vue 引用的**样式文件（常见 `assets/index.css`） | **⚠️只读不改；生成时不得再读取其他工程文件作稿源** |
| 目标文件输出 | `Custom.vue` | **新建文件，改造后的结果** |
| 完整路径 | `src/views/${文件夹名称}/Custom.vue` | 目标文件完整路径 |

**⚠️ 关键约束：**
- ❌ **绝对禁止修改** `index.vue` 及其引用的样式文件
- ❌ **生成 Custom.vue 时禁止**参考其他视图、`create.md`、路由、`package.json` 等（仅认当前 `index.vue` + 其引用 CSS + 资源路径）
- ✅ **只能创建和修改** `Custom.vue`
- ✅ `Custom.vue` 必须是**完全独立的单文件组件**（包含template、script、style三部分）
- ⚠️ **图片路径必须使用相对路径** `./assets/img/` 而不是 `@/assets/img/`

### 1.1.1 执行前路径验证（⭐新增）

**⚠️ 必须验证以下路径，否则可能导致生成失败：**

```bash
# 步骤1: 确认源文件存在
必须存在: src/views/${文件夹名称}/index.vue
# 步骤1b: 据 index.vue 引用确认各样式文件存在（常见为 assets/index.css）

# 步骤2: 确认目标路径正确
目标文件: src/views/${文件夹名称}/Custom.vue

# 步骤3: 检查常见错误
❌ 错误: 在项目根目录创建 /${文件夹名称}/Custom.vue
✅ 正确: 在 src/views/${文件夹名称}/Custom.vue 创建
```

**路径验证检查清单：**
- [ ] 源文件 `src/views/${文件夹名称}/index.vue` 存在且可读
- [ ] `index.vue` 所引用的每个样式文件均存在且可读
- [ ] 目标目录 `src/views/${文件夹名称}/` 存在（不存在则创建）
- [ ] 确认不是在项目根目录的 `${文件夹名称}/` 下操作

**常见路径错误：**
| 错误类型 | 错误路径 | 正确路径 | 后果 |
|---------|---------|---------|------|
| 根目录混淆 | `/shushi/Custom.vue` | `src/views/shushi/Custom.vue` | 生成的文件位置错误，项目无法引用 |
| 源文件缺失 | 读取根目录 `/shushi/index.vue` | 读取 `src/views/shushi/index.vue` | 转换的是错误的源文件 |
| 路径不存在 | 直接写入不存在的目录 | 先创建目录再写入 | 文件写入失败 |

### 1.2 技术栈
- **Vue 2.0** - 前端框架
- **Element UI 2.15.14** - UI组件库
  - 安装命令: `npm i element-ui@2.15.14 -S`
  - 已在项目中全局引入，可直接使用所有组件

### 1.3 核心改造目标
将静态HTML页面改造为**数据驱动的动态页面**，要求：
1. ✅ **视觉效果像素级一致** - 改造前后视觉效果完全相同（最高优先级）
2. ✅ **循环渲染** - 重复结构使用v-for循环替代静态重复代码
3. ✅ **Element UI组件化** - 用Element UI组件替换原生HTML元素
4. ✅ **规范命名** - 所有CSS类名遵循统一命名规范
5. ✅ **数据驱动** - 所有交互通过Vue数据和方法实现

### 1.4 改造前后对比示例

**改造前（静态）:**
```vue
<div class="box_1">项目1</div>
<div class="box_2">项目2</div>
<div class="box_3">项目3</div>
```

**改造后（动态）:**
```vue
<div 
  v-for="item in projectList" 
  :key="item.id"
  class="custom_project_item"
>
  {{ item.name }}
</div>
```
