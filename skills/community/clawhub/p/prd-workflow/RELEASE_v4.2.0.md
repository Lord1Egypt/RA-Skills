# PRD Workflow v4.2.0 发布说明

**发布日期**: 2026-04-05  
**版本类型**: Feature Release  
**上一版本**: v4.1.0

---

## 🚀 核心特性

### 验收标准 GWT 格式优化

**问题背景**：
- v4.1.0 及之前版本，需求拆解阶段生成顶层验收标准（12 条中文 GWT）
- 但 PRD 模板未正确接收，导致验收标准丢失
- 顶层验收标准与功能级验收标准重复

**解决方案**：
1. **需求拆解阶段** → 不再生成验收标准
   - `decomposition_module.js` 删除 `generateAcceptanceCriteria()` 方法
   - `decomposition.json` 只保留 `features` + `userStories`

2. **PRD 生成阶段** → 每个功能生成 GWT 验收标准
   - `prd_module.js` 提示词明确要求基于业务规则生成 GWT 格式
   - `prd_template.js` 兼容字符串数组格式（Given-When-Then）
   - 每条验收标准包含三要素：前置条件/操作/预期结果

3. **质量检查** → 添加 GWT 格式检查项
   - `checker.md` 添加 `COMPLETE-6: 验收标准格式（GWT）`
   - 检查点：Given/When/Then 完整性、中文描述
   - 验收标准：GWT 格式覆盖率 ≥ 90%

---

## 📦 变更清单

### 核心文件

| 文件 | 变更 | 说明 |
|------|------|------|
| `workflows/version.js` | 更新 | 版本号 v4.2.0，添加 changelog |
| `workflows/modules/decomposition_module.js` | 重构 | 删除验收标准生成逻辑 |
| `workflows/modules/prd_module.js` | 增强 | 提示词添加 GWT 格式要求 |
| `workflows/prd_template.js` | 增强 | `buildAcceptanceCriteria()` 兼容字符串数组 |
| `docs/checker.md` | 新增 | COMPLETE-6 检查项 |
| `test_v4.2.0.js` | 新增 | v4.2.0 测试脚本 |

### 配套文件

| 文件 | 变更 | 说明 |
|------|------|------|
| `workflows/check_items_loader.js` | v1.1.0 | 新增 `loadForChapter()` 方法 |
| `workflows/data_bus.js` | 增强 | 数据总线功能扩展 |
| `workflows/ai_diagram_extractor.js` | 优化 | 图表提取逻辑改进 |
| `workflows/ai_entry.js` | 清理 | 入口文件简化 |
| `workflows/main.js` | 调整 | 主流程优化 |

---

## ✅ 测试结果

```bash
📋 测试 1: 需求拆解不生成验收标准     ✅ 通过
📋 测试 2: PRD 模板兼容 GWT          ✅ 通过
📋 测试 3: checker 包含 GWT 检查项    ✅ 通过

总计：3/3 通过 (100%)
```

**测试脚本**: `test_v4.2.0.js`

---

## 📊 预期效果

### 需求拆解输出（decomposition.json）

```json
{
  "features": [
    {
      "id": "MOD-001",
      "name": "客群画像雷达图",
      "priority": "P0",
      "businessRules": [...],
      "userStories": [...]
    }
    // 7 个功能模块
  ],
  "userStories": [...],  // 6 个用户故事
  // ✅ 不再生成 acceptanceCriteria
}
```

### PRD 输出（每个功能章节）

```markdown
### 3.1 客群画像雷达图

#### 业务规则
- BR-001-01: 权限校验
- BR-001-02: 数据更新

#### 用户故事
- As a 理财经理，I want 查看客群画像雷达图...

#### 验收标准（GWT 格式）✨ 新增
1. Given 理财经理打开产品详情页，When 页面加载完成，Then 显示客群画像雷达图卡片入口
2. Given 理财经理点击雷达图卡片，When 进入客群画像详情页，Then 显示总体雷达图和 5 大维度得分
3. Given 理财经理无权限查看某产品，When 访问该产品画像，Then 显示无权限提示

#### 输入输出定义
...
```

---

## 🔧 技术细节

### GWT 格式兼容性

`prd_template.js` 的 `buildAcceptanceCriteria()` 现在支持两种格式：

**格式 1: GWT 字符串数组（新）**
```javascript
const criteria = [
  'Given 用户已登录，When 点击保存，Then 成功保存数据',
  'Given 用户未登录，When 点击保存，Then 显示登录提示'
];
```

**格式 2: 对象数组（旧，向后兼容）**
```javascript
const criteria = {
  functional: [
    { method: '点击保存按钮', expected: '数据保存成功' }
  ]
};
```

### 质量门禁

v4.2.0 新增验收标准质量检查：

- ✅ GWT 格式覆盖率 ≥ 90%
- ✅ 三要素（Given/When/Then）完整率 100%
- ✅ 中文描述率 100%
- ✅ 覆盖所有业务规则

---

## 📝 升级指南

### 从 v4.1.0 升级

1. **拉取最新代码**
   ```bash
   git pull origin main
   ```

2. **验证版本**
   ```bash
   node -e "console.log(require('./workflows/version.js').full)"
   # 输出：v4.2.0
   ```

3. **运行测试**
   ```bash
   node test_v4.2.0.js
   ```

4. **重新生成 PRD**（如需要）
   ```bash
   node workflows/main.js "你的需求描述"
   ```

### 兼容性

- ✅ **向后兼容**: 旧的 decomposition.json 仍可处理
- ✅ **模板兼容**: prd_template.js 同时支持新旧格式
- ⚠️ **行为变更**: 需求拆解不再生成顶层验收标准

---

## 🎯 下一步计划

### v4.3.0 规划

- [ ] PRD 评审模块自动化
- [ ] 流程图自动生成（Mermaid → PNG）
- [ ] Word 导出优化（嵌入图片）
- [ ] 多页面原型系统

### 长期目标

- [ ] prd-workflow 产品化（独立 CLI 工具）
- [ ] 支持多需求并行处理
- [ ] 需求版本对比工具
- [ ] AI 贡献率分析可视化

---

## 📞 反馈与支持

**问题反馈**: GitHub Issues  
**讨论**: Discord #prd-workflow  
**文档**: `/Users/lifan/.openclaw/workspace/skills/prd-workflow/docs/`

---

**发布人**: 红曼为帆 🧣  
**审核人**: 李帆
