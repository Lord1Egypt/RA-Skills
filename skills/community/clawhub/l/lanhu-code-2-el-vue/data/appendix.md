# 📚 十、附录

### 10.1 常用Element UI组件参考

**详细文档**: https://element.eleme.cn/#/zh-CN/component/installation

**快速索引**:
- [Input 输入框](https://element.eleme.cn/#/zh-CN/component/input)
- [Select 选择器](https://element.eleme.cn/#/zh-CN/component/select)
- [Pagination 分页](https://element.eleme.cn/#/zh-CN/component/pagination)
- [Dialog 对话框](https://element.eleme.cn/#/zh-CN/component/dialog)
- [Checkbox 多选框](https://element.eleme.cn/#/zh-CN/component/checkbox)

### 10.2 Vue 2.0参考

**详细文档**: https://cn.vuejs.org/v2/guide/

**核心概念**:
- [模板语法](https://cn.vuejs.org/v2/guide/syntax.html)
- [列表渲染](https://cn.vuejs.org/v2/guide/list.html)
- [事件处理](https://cn.vuejs.org/v2/guide/events.html)
- [表单输入绑定](https://cn.vuejs.org/v2/guide/forms.html)

### 10.3 问题排查指南

**问题分类及解决方案**:

1. **样式问题**
   - 样式不生效 → 检查是否使用::v-deep
   - 样式被覆盖 → 检查选择器优先级
   - 布局错乱 → 检查容器宽度和flex/grid设置

2. **功能问题**
   - 方法未定义 → 检查methods是否定义
   - 数据未定义 → 检查data()是否定义
   - 事件不触发 → 检查事件名和方法名是否一致

3. **渲染问题**
   - v-for不显示 → 检查数据是否为空数组
   - 图片不显示 → 检查图片路径和require用法
   - 组件不显示 → 检查Element UI是否正确引入

### 10.4 最佳实践建议

**开发建议**:
1. 先完成一个小模块，验证通过后再继续
2. 频繁使用浏览器开发者工具对比样式
3. 保持代码整洁，及时删除无用代码
4. 使用有意义的变量名和方法名
5. 添加必要的注释说明复杂逻辑

**性能建议**:
1. v-for列表数据不要过大（建议<1000项）
2. 避免在v-for中使用复杂计算
3. 合理使用v-if和v-show
4. 图片使用合适的尺寸，避免过大

---
