---
name: hook-system
description: >
  工具钩子系统。在工具执行前后注入自定义逻辑，支持：
  - PreToolUse: 工具执行前调用，可修改输入或阻止执行
  - PostToolUse: 工具执行后调用，可修改输出或记录日志
  当用户说"添加钩子"、"hook"、"拦截工具"、"工具前后处理"时触发。
  依赖：Node.js 18+
---

# Hook System - 工具钩子框架

## 核心概念

```
工具调用流程（带Hook）:
User Message → [PreToolUse Hook] → Tool Executor → [PostToolUse Hook] → Response
                       ↓                        ↓
                  可以阻止执行             可以修改输出
```

## Hook 类型

| 类型 | 时机 | 用途 |
|------|------|------|
| PreToolUse | 工具执行前 | 验证输入、日志记录、阻止执行 |
| PostToolUse | 工具执行后 | 修改输出、错误处理、通知 |

## 快速使用

```javascript
const { HookRunner } = require('./scripts/hook-runner.mjs');

const runner = new HookRunner({
  preToolUse: ['echo "Calling $HOOK_TOOL_NAME"'],
  postToolUse: ['echo "Done: $HOOK_TOOL_NAME"']
});

// 执行前钩子
const preResult = runner.runPreToolUse('read_file', '{"path":"README.md"}');
console.log(preResult.allow); // true/false
console.log(preResult.messages); // 钩子输出

// 执行后钩子
const postResult = runner.runPostToolUse('read_file', '{"path":"README.md"}', 'file content...', false);
```

## Hook 命令格式

```bash
# 标准输出 = 钩子消息（会被注入到结果）
# 退出码 = 结果
#   0 = 允许/成功
#   2 = 拒绝（仅PreToolUse）
#   其他 = 警告（不阻止执行）
```

## 环境变量

钩子运行时自动注入：

| 变量 | 说明 |
|------|------|
| `HOOK_EVENT` | 事件类型：`PreToolUse` 或 `PostToolUse` |
| `HOOK_TOOL_NAME` | 工具名称 |
| `HOOK_TOOL_INPUT` | 工具输入（原始JSON字符串） |
| `HOOK_TOOL_INPUT_PARSED` | 解析后的JSON（美化格式） |
| `HOOK_TOOL_OUTPUT` | 工具输出（PostToolUse才有） |
| `HOOK_TOOL_IS_ERROR` | 是否错误：`0` 或 `1` |

## 权限模式

| 退出码 | 结果 | 说明 |
|--------|------|------|
| 0 | Allow | 工具正常执行/继续 |
| 2 | Deny | 阻止工具执行 |
| 其他 | Warn | 显示警告但继续执行 |

## 配置文件格式

```json
{
  "hooks": {
    "preToolUse": [
      "node ./hooks/validate-input.mjs",
      "echo 'PreHook: $HOOK_TOOL_NAME'"
    ],
    "postToolUse": [
      "node ./hooks/log-output.mjs"
    ]
  }
}
```

## 内置钩子示例

### 1. 日志钩子
```bash
# pre-log.sh
echo "[$(date)] Calling $HOOK_TOOL_NAME with $HOOK_TOOL_INPUT" >> hooks.log
```

### 2. 输入验证钩子
```javascript
// validate-input.mjs
const input = JSON.parse(process.env.HOOK_TOOL_INPUT || '{}');
if (input.path?.includes('..')) {
  console.error('Path traversal detected');
  process.exit(2); // Deny
}
console.log('Input valid');
process.exit(0);
```

### 3. 敏感信息过滤钩子
```javascript
// filter-secrets.mjs
const output = process.env.HOOK_TOOL_OUTPUT || '';
const filtered = output.replace(/sk-\w{32,}/g, '[REDACTED_API_KEY]');
console.log(filtered);
process.exit(0);
```

## 文件结构

```
hook-system/
├── SKILL.md              # 本文件
├── scripts/
│   ├── hook-runner.mjs   # 核心钩子运行器
│   └── hooks/
│       ├── pre-log.mjs   # 日志示例
│       ├── validate-path.mjs  # 路径验证
│       └── filter-secrets.mjs # 敏感信息过滤
└── references/
    └── hook-examples.md  # 更多示例
```

---

_龙虾王子自我进化的成果 🦞_
