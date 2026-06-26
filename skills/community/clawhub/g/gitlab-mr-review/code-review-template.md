# Code Review 模板

## 📋 AI 代码审查

### 概述
本 MR 增加了 **[功能名称]**，涉及 X 个文件。

### ✅ 优点
1. 列出整体正向评价（如：实现完整、逻辑清晰、测试覆盖合理等）
2. 代码结构改进: 把列选择功能从 slot 移到 props，使 API 更简洁
3. 新增 `disabledPopover` prop 提供了更好的灵活性
4. 多个 view 文件的改动模式一致，整体风格统一

### 💡 建议 (具体位置)
1. **Props 命名** - `disabledPopover` 语义不够清晰，建议改为 `disabledColumns`（更贴近“列禁用/列选择”的含义）
2. **全局组件影响** - `globalModal` 移除了 `bodyStyle`，需要确认其他调用方是否依赖该样式，避免产生 UI 回归
3. **交互一致性** - `create.vue` 中关闭按钮由 `@on-icon-close` 改为 `@click`，需要确认交互行为（包括事件触发时机和副作用）与原实现完全一致

### 🤔 问题 (具体位置)
1. **Debug 代码未清理** 🔴  
   ```vue
   // [文件路径，例如: src/views/factory/create.vue]
   console.log(123123)
   ```  
   > 建议: 删除这行 `console.log`，避免将调试信息带入生产环境。

2. **类型标注错误** 🟡  
   ```typescript
   @change-columns="(columns: []) => (showColumns = columns)"
   ```  
   > 此处的 `columns: []` 类型不明确，建议改为 `columns: TableColumnData[]` 以保证类型安全和可读性。

### 🎯 结论 (待办事项)
- [ ] [待办事项1]
- [ ] [待办事项2]
- [ ] [待办事项3]
- [ ] [待办事项4]

**LGTM** ✅ / **需要修改** ❌

---
*AI 审查由 OpenClaw 提供*

---

## 使用说明

### 审查流程
1. 使用 glab 获取 MR 的 changes
2. 分析 diff，找出:
   - TODO 注释
   - 未完成的代码
   - 硬编码值
   - 潜在的 bug
3. 标注具体文件和行号
4. 列出可执行的待办事项

### 命令示例
```bash
# 获取 MR 信息
glab api projects/[project]/merge_requests/[iid] --hostname gitlab.xxx.com

# 获取 MR diff
glab api projects/[project]/merge_requests/[iid]/changes --hostname gitlab.xxx.com

# 发送审查评论
glab api projects/[project]/merge_requests/[iid]/notes --hostname gitlab.xxx.com \
  --method POST \
  --raw-field body="$(cat review-template.md)"
```
