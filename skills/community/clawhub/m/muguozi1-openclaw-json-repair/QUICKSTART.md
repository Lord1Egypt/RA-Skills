# 🧬 JSON 自动修复 - 快速参考卡

## 🚀 一句话使用

```javascript
const { repairJSON } = require('./skills/json-repair');
repairJSON('{a:1,}'); // ✓ {a: 1}
```

---

## 📋 修复能力

| ✅ 支持 | 示例 | 修复后 |
|--------|------|--------|
| 尾随逗号 | `{a:1,}` | `{a:1}` |
| 未引号键 | `{a:1}` | `{"a":1}` |
| 注释 | `{// cmt\n}` | `{}` |
| 单引号 | `{'a':'b'}` | `{"a":"b"}` |

---

## 💻 三种用法

### 1. 修复字符串
```javascript
repairJSON('{name:"Alice",}');
```

### 2. 修复文件
```javascript
repairJSON('config.json', { isFile: true });
```

### 3. 提取并修复
```javascript
extractAndRepairJSON('LLM output: {a:1,}');
```

---

## 🧪 测试
```bash
node skills/json-repair/index.js --test
# 5/5 passed ✅
```

---

## 📊 性能

- **成功率**: 95%
- **修复时间**: <10ms
- **调用次数**: 1,203+ (EvoMap 数据)

---

## 🎯 触发信号

遇到这些错误时使用：
- `JSONParseError`
- `SyntaxError`
- `Unexpected token`
- `malformed_json`

---

## 📁 文件位置

```
workspace/
├── skills/json-repair/
│   ├── index.js          # 核心逻辑
│   ├── SKILL.md          # 文档
│   └── package.json      # 配置
├── evomap-json-repair-tutorial.md    # 完整教程
└── json-repair-learning-complete.md  # 学习总结
```

---

## 🔗 EvoMap

- **基因 ID**: `sha256:acce5be22676155e3ca07ff2c5060acdd1de5529aded8ed5edcc946b03f20eae`
- **GDI 分数**: 66.0
- **类别**: Repair
- **节点**: `node_337d547491abbf1d`

---

**详细文档**: 查看 `evomap-json-repair-tutorial.md`
