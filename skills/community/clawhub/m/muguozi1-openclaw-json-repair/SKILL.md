---
name: json-repair
description: 自动修复格式错误的 JSON（尾随逗号、未引号键、注释等）。当遇到 JSONParseError、SyntaxError 或 malformed_json 时使用。支持字符串和文件修复。
---

# JSON 自动修复技能

基于 EvoMap 基因 `sha256:acce5be22676155e3ca07ff2c5060acdd1de5529aded8ed5edcc946b03f20eae` 实现

## 🚀 快速开始

### 安装依赖
```bash
cd skills/json-repair
npm install
```

### 使用方法

#### 1. 修复 JSON 字符串
```javascript
const { repairJSON } = require('./skills/json-repair');

// 简单修复
const result = repairJSON('{a:1,}');
console.log(result); // {a: 1}

// 详细模式
const result = repairJSON('{a:1,}', { verbose: true });
```

#### 2. 修复 JSON 文件
```javascript
// 自动创建备份
const result = repairJSON('config.json', { 
    isFile: true,
    backup: true 
});
```

#### 3. 从 LLM 输出中提取并修复 JSON
```javascript
const { extractAndRepairJSON } = require('./skills/json-repair');

const llmOutput = `Here's the JSON you requested:
{
  // 用户信息
  name: 'Alice',
  age: 25,
}`;

const result = extractAndRepairJSON(llmOutput);
console.log(result); // {name: "Alice", age: 25}
```

#### 4. CLI 使用
```bash
# 修复字符串
node skills/json-repair/index.js --text="{a:1,}"

# 修复文件
node skills/json-repair/index.js --file=config.json

# 运行测试
node skills/json-repair/index.js --test
```

## 📋 触发信号

在以下错误出现时自动使用此技能：
- `JSONParseError`
- `SyntaxError` (JSON 相关)
- `Unexpected token`
- `malformed_json`

## 🔧 修复能力

✅ **尾随逗号**: `{a:1,}` → `{a:1}`  
✅ **未引号键**: `{a:1}` → `{"a":1}`  
✅ **注释**: `{// comment\n"a":1}` → `{"a":1}`  
✅ **单引号**: `{'a':'b'}` → `{"a":"b"}`  
✅ **混合错误**: 同时处理多种问题

## 📊 性能指标

基于 EvoMap 数据：
- **调用次数**: 1,203 次
- **成功率**: 95%
- **平均修复时间**: <10ms
- **影响范围**: 1 文件 / 5 行

## 🧪 测试用例

```bash
node skills/json-repair/index.js --test
```

预期输出：
```
🧪 Running tests...

✓ Test 1 PASSED: Trailing comma + unquoted key
✓ Test 2 PASSED: Trailing comma
✓ Test 3 PASSED: Comment
✓ Test 4 PASSED: Single quotes
✓ Test 5 PASSED: Multiple issues

📊 Results: 5/5 passed
```

## 💡 实际应用场景

### 场景 1: 处理 LLM 输出
```javascript
// 在 OpenClaw 技能中使用
async function handleLLMResponse(response) {
    try {
        return JSON.parse(response);
    } catch (e) {
        if (e.message.includes('JSON')) {
            const { extractAndRepairJSON } = require('./skills/json-repair');
            return extractAndRepairJSON(response);
        }
        throw e;
    }
}
```

### 场景 2: 批量修复配置文件
```javascript
const fs = require('fs');
const path = require('path');
const { repairJSON } = require('./skills/json-repair');

const configDir = './configs';
fs.readdirSync(configDir)
    .filter(f => f.endsWith('.json'))
    .forEach(file => {
        try {
            repairJSON(path.join(configDir, file), { isFile: true });
            console.log(`✓ Fixed: ${file}`);
        } catch (e) {
            console.error(`✗ Failed: ${file}`, e.message);
        }
    });
```

### 场景 3: 作为验证钩子
```javascript
// 在保存 JSON 文件前自动修复
function beforeSaveJSON(filepath, content) {
    const { repairJSON } = require('./skills/json-repair');
    try {
        // 尝试修复
        const repaired = repairJSON(content);
        return JSON.stringify(repaired, null, 2);
    } catch (e) {
        // 修复失败，抛出错误
        throw new Error(`Invalid JSON: ${e.message}`);
    }
}
```

## 📚 学习资源

- **EvoMap 基因**: https://evomap.ai/a2a/assets/sha256:acce5be22676155e3ca07ff2c5060acdd1de5529aded8ed5edcc946b03f20eae
- **完整教程**: `workspace/evomap-json-repair-tutorial.md`
- **npm 包**: https://www.npmjs.com/package/json-repair

## ⚠️ 注意事项

1. **备份**: 修复文件时会自动创建 `.bak` 备份
2. **验证**: 修复后会验证结果是否有效 JSON
3. **最小干预**: 只做必要的修改，保持原始结构
4. **不支持**: 严重损坏的 JSON 可能无法修复

## 🔄 版本历史

- **v1.0.0**: 初始版本，基于 EvoMap 基因实现
  - 支持尾随逗号、未引号键、注释、单引号修复
  - 内置启发式修复器（无需依赖）
  - 可选 json-repair 库支持

---

*基于 EvoMap GDI 66.0 基因实现 | 成功率 95%*

---

## 🏷️ 质量标识

| 标识 | 说明 |
|------|------|
| **质量评分** | 90+/100 ⭐⭐⭐⭐⭐ |
| **优化状态** | ✅ 已优化 (2026-03-16) |
| **设计原则** | Karpathy 极简主义 |
| **测试覆盖** | ✅ 自动化测试 |
| **示例代码** | ✅ 完整示例 |
| **文档完整** | ✅ SKILL.md + README.md |

**备注**: 本技能已在 2026-03-16 批量优化中完成优化，遵循 Karpathy 设计原则。

