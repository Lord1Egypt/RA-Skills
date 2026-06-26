# 模型加载机制统一迁移 (2026-03-20)

## 变更概述

彻底统一模型加载机制，移除 `/model/download` 相关代码，全面采用 `/model/create + checkFromCloud:true`。

## 为什么迁移

| 对比项 | 旧方案 `/model/download` | 新方案 `/model/create + checkFromCloud` |
|--------|------------------------|----------------------------------------|
| **接口数量** | 需要两个接口（download + create） | 一个接口搞定 |
| **本地优先** | ❌ 总是从云端下载 | ✅ 本地有则直接加载 |
| **代码复杂度** | 需要处理 taskId 轮询 | 同步返回，无需轮询 |
| **官方推荐** | ❌ 已废弃 | ✅ 官方推荐方式 |

## 变更清单

### 1. SKILL.md
- ✅ 删除 `/model/download` 工具示例
- ✅ 更新模型加载机制说明（唯一推荐方式）
- ✅ 添加决策树
- ✅ 更新 API 参考表
- ✅ 添加 `scripts/model-loader.js` 使用示例

### 2. kunwu-tool.js
- ✅ 删除 `downloadModel()` 函数
- ✅ 删除 `downloadModelsParallel()` 函数
- ✅ 从 exports 中移除相关导出

### 3. 新增 scripts/model-loader.js
- ✅ 批量模型加载工具
- ✅ 进度显示
- ✅ 自动重试机制
- ✅ 错误恢复
- ✅ 示例配置文件 `models-example.json`

### 4. 测试文件更新
- ✅ `test-assemble-correct.js` - 改用 `createModel`
- ✅ `test-assemble-final-correct.js` - 改用 `createModel`
- ✅ `test-assemble-smart.js` - 移除未使用导入
- ✅ `test-camera-bracket-assemble.js` - 本地函数改用 `/model/create`
- ✅ `test-query-task.js` - 简化为同步创建
- ✅ `test-auto-wait-wrapper.js` - 更新注释
- ✅ `task-builder.js` - 改用 `createModel`

### 5. 废弃文件归档
- ✅ 移动所有 `test-download*.js` 到 `tests-deprecated/` 目录

## 迁移后用法

### 单个模型加载
```bash
kunwu_call endpoint="/model/create" data='{
  "id": "M900iB_280L",
  "rename": "机器人_1",
  "position": [0, 2500, 515],
  "checkFromCloud": true
}'
```

### 批量模型加载
```bash
# 准备 models.json
node scripts/model-loader.js models.json
```

### JavaScript 代码
```javascript
import { createModel } from './kunwu-tool.js';

await createModel({
  id: 'M900iB_280L',
  rename: '机器人_1',
  position: [0, 2500, 515],
  checkFromCloud: true  // 关键：本地有则快，没有自动下载
});
```

## 影响范围

- **破坏性变更**: 是（`downloadModel` 函数已删除）
- **向后兼容**: 否（调用旧函数的代码会失败）
- **建议**: 所有使用 `downloadModel` 的代码应立即迁移到 `createModel`

## 验证清单

- [x] JavaScript 语法检查通过
- [ ] 实际运行测试（需要 Kunwu Builder 环境）
- [ ] 更新相关文档

---

**执行日期**: 2026-03-20  
**执行人**: Claw 🦞
