# 🔧 六、常见问题及解决方案

| 问题 | 解决方案 |
|------|---------|
| **Custom.vue 未生成或生成位置错误** | 1. **检查源文件路径**：确认 `src/views/${文件夹名称}/index.vue` 存在<br>2. **检查目标路径**：确认在 `src/views/${文件夹名称}/Custom.vue` 生成，而非根目录<br>3. **查看详细修复指南**：见下方 **「Custom.vue 生成失败专项」** |
| **样式无法覆盖Element UI组件** | 1. 使用深度选择器 `::v-deep` 或 `/deep/`<br>2. 检查选择器路径是否正确<br>3. 必要时使用 `!important`（不推荐） |
| **循环渲染后样式不一致** | 1. 检查key绑定唯一性<br>2. 检查数据字段与模板字段一致<br>3. 检查动态class绑定<br>4. 确保样式在 `<style scoped>` 中 |
| **图片路径问题** | 1. ⚠️ **Template 中的 &lt;img&gt; 标签**：必须使用 `./assets/img/`，正确用法：`:src="require('./assets/img/图片名.png')"`<br>2. ⚠️ **CSS 中的 background-image**：必须保持原始路径 `./img/` 不变，**不得修改为 `./assets/img/`**<br>3. 动态绑定：`:src="require(\`./assets/img/\${item.img}\`)"`<br>4. 检查图片文件是否存在于 `src/views/custom/assets/img/` 目录<br>5. **详细规则**：见 `data/render.md` 第 2.3.6 节「CSS 背景图片路径处理」 |
| **布局错乱** | 1. 检查容器宽度（100%或正确百分比）<br>2. 检查flex/grid属性<br>3. 检查position定位<br>4. 检查overflow溢出处理 |
| **交互功能不工作** | 1. 检查事件绑定和方法名是否一致<br>2. **检查方法是否在methods中定义**（禁止只写template不写methods）<br>3. **检查方法中使用的数据是否在data()中定义**（禁止只写methods不写data）<br>4. 检查v-model绑定的数据在data()中定义<br>5. 检查Element UI组件属性配置<br>6. 确保组件替换时同时完成template、data、methods三部分 |
| **样式优先级问题** | 1. 提高选择器优先级（更具体的选择器）<br>2. 检查样式定义顺序<br>3. Element UI组件必须用 `::v-deep`<br>4. 避免使用!important |
| **响应式布局问题** | 1. 使用百分比宽度而非固定px<br>2. 必要时添加媒体查询<br>3. 测试不同屏幕尺寸 |
| **搜索框样式异常（高度错位、双边框、图标或占位符不对齐）** | 1. 按 **2.4.5 搜索框（带外框的 el-input）样式规范** 执行：外层容器使用 flex + align-items: center + box-sizing: border-box；el-input 高度 100%；el-input__inner 高度略小于容器、无重复边框、背景透明、border-radius 与容器一致；placeholder 颜色用 ::placeholder 单独设置；el-input__prefix 使用 flex 垂直居中，自定义图标用 inline-flex 居中<br>2. 确保同一页面/项目内所有带外框的搜索框均采用该规范 |

---

## Custom.vue 生成失败专项

### 问题现象
执行 `/ui-ux-pro-max /lanhu-code-2-el-vue 执行xxx文件夹` 后，Custom.vue 未生成或生成在错误位置。

### 根本原因
**路径混淆**：项目根目录的 `/${文件夹名称}/` 与 `src/views/${文件夹名称}/` 是两个不同的位置。

### 识别步骤

**步骤1: 确认源文件位置**
```bash
# 必须读取的源文件
src/views/${文件夹名称}/index.vue
src/views/${文件夹名称}/assets/index.css

# 检查这些文件是否存在
ls src/views/${文件夹名称}/index.vue
ls src/views/${文件夹名称}/assets/index.css
```

**步骤2: 检查是否存在路径混淆**
```bash
# 错误：在项目根目录查找（❌）
ls ${文件夹名称}/index.vue  # 这可能是旧的或错误的文件

# 正确：在 src/views/ 下查找（✅）
ls src/views/${文件夹名称}/index.vue  # 这是真正的源文件
```

**步骤3: 确认目标输出位置**
```bash
# 正确输出位置
src/views/${文件夹名称}/Custom.vue

# 错误输出位置（常见问题）
${文件夹名称}/Custom.vue  # ❌ 根目录错误
```

### 修复流程

**情况A: 源文件在正确位置，Custom.vue 未生成**
1. 确认已读取 `src/views/${文件夹名称}/index.vue`
2. 确认在 `src/views/${文件夹名称}/` 目录创建 Custom.vue
3. 重新执行转换流程

**情况B: 存在根目录混淆（如 /shushi/Custom.vue 已存在）**
1. 检查根目录的 `${文件夹名称}/` 是否是之前错误创建的
2. 确认真正的源文件在 `src/views/${文件夹名称}/`
3. 在正确的位置 `src/views/${文件夹名称}/Custom.vue` 重新生成
4. （可选）删除根目录的错误文件以避免混淆

**情况C: src/views/ 下不存在对应文件夹**
1. 确认用户提供的文件夹名称是否正确
2. 检查是否存在拼写错误
3. 确认源文件确实存在于项目中

### 预防规则

**执行前必须验证：**
- [ ] 源文件路径：`src/views/${文件夹名称}/index.vue` 存在
- [ ] 样式文件路径：`src/views/${文件夹名称}/assets/index.css` 存在
- [ ] 目标路径：`src/views/${文件夹名称}/Custom.vue`（不是根目录）
- [ ] 图片路径：使用 `./assets/img/` 相对路径

**路径验证代码示例：**
```javascript
// 执行前验证路径
const sourcePath = `src/views/${folderName}/index.vue`
const cssPath = `src/views/${folderName}/assets/index.css`
const targetPath = `src/views/${folderName}/Custom.vue`

// 必须确认这些路径存在且正确
// 禁止在根目录的 ${folderName}/ 下操作
```

---
