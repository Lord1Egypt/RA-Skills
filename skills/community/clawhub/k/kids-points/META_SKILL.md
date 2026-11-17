# 🎯 kids-points 元技能说明

> **版本**: v1.2 | **最后更新**: 2026-03-14

本文档说明 kids-points 作为**元技能**的依赖管理机制。

---

## 🎯 什么是元技能？

**元技能（Meta-Skill）** 是一种特殊类型的技能，它：

1. **声明依赖** - 通过 `skill.json` 声明所需的其他技能
2. **自动检查** - 首次使用时自动检查依赖
3. **友好提示** - 提供清晰的安装引导
4. **可选依赖** - 核心功能独立，高级功能可选

---

## 📦 依赖管理

### 依赖声明

在 `skill.json` 中声明：

```json
{
  "dependencies": {
    "skills": [
      {
        "id": "kid-point-voice-component",
        "name": "SenseAudio TTS",
        "required": false,
        "features": ["语音播报", "语音识别"]
      }
    ]
  }
}
```

### 依赖类型

| 类型 | required | 说明 | 示例 |
|------|----------|------|------|
| **必需** | true | 技能无法运行 | 无 |
| **可选** | false | 核心功能可用，高级功能需依赖 | kid-point-voice-component |

### 当前依赖

| 技能 | 必需 | 用途 | 状态 |
|------|------|------|------|
| **kid-point-voice-component** | ❌ 可选 | TTS 语音合成 | ⚠️ 推荐安装 |
| **kid-point-voice-component** | ❌ 可选 | ASR 语音识别 | ⚠️ 推荐安装 |

---

## 🔧 自动安装机制

### 首次运行检查

技能首次运行时自动执行：

```javascript
// agent-handler.js
const { checkSkillDependencies } = require('./scripts/install-dependencies');

// 初始化时检查依赖
checkSkillDependencies();
```

### 检查流程

```
1. 读取 skill.json
   ↓
2. 检查依赖技能是否安装
   ↓
3. 检查 API Key 配置
   ↓
4. 显示检查结果
   ↓
5. 提供安装引导
```

### 检查结果示例

```
🔍 检查 kids-points 依赖...

✅ SenseAudio TTS 已安装
⚠️  SenseAudio ASR 未安装
✅ SenseAudio API Key 已配置

============================================================
📦 发现未安装的依赖技能
============================================================

  • SenseAudio ASR (kid-point-voice-component)
    用途：音频消息识别
    说明：语音功能需要此依赖

💡 提示：这些是可选依赖，不影响文字功能使用
   但安装后可以解锁语音功能，体验更好哦！

🔧 快速安装命令：
   clawhub install kid-point-voice-component
```

---

## 📊 功能可用性

### 无依赖技能

| 功能 | 可用性 | 说明 |
|------|--------|------|
| 文字记账 | ✅ 可用 | 核心功能 |
| 积分查询 | ✅ 可用 | 核心功能 |
| 规则修改 | ✅ 可用 | 核心功能 |
| 语音记账 | ❌ 不可用 | 需要 kid-point-voice-component |
| 语音播报 | ❌ 不可用 | 需要 kid-point-voice-component |

### 有依赖技能

| 功能 | 可用性 | 说明 |
|------|--------|------|
| 文字记账 | ✅ 可用 | 核心功能 |
| 积分查询 | ✅ 可用 | 核心功能 |
| 规则修改 | ✅ 可用 | 核心功能 |
| 语音记账 | ✅ 可用 | 发送音频自动识别 |
| 语音播报 | ✅ 可用 | 积分变动自动鼓励 |

---

## 🚀 安装指南

### 自动安装（推荐）

技能会自动提示安装命令：

```bash
clawhub install kid-point-voice-component
clawhub install kid-point-voice-component
```

### 手动安装

1. 访问 [ClawHub](https://clawhub.com)
2. 搜索技能名称
3. 点击安装

### 验证安装

```bash
# 运行依赖检查
node scripts/install-dependencies.js
```

---

## 🔑 API Key 配置

### 检查 API Key

```javascript
const { checkApiKey } = require('./scripts/install-dependencies');
const status = checkApiKey();
console.log(status.configured ? '✅ 已配置' : '⚠️ 未配置');
```

### 配置方法

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "env": {
    "SENSE_API_KEY": "sk-your-api-key-here"
  }
}
```

### 获取 API Key

1. 访问 [SenseAudio](https://senseaudio.cn)
2. 免费注册账号
3. 创建应用
4. 复制 API Key

---

## 📋 技能间通信

### 依赖技能调用

```javascript
// 调用 kid-point-voice-component
const TTS_SCRIPT = path.join(WORKSPACE, 'skills/kid-point-voice-component/scripts/tts.py');
const cmd = `python3 "${TTS_SCRIPT}" --play "${text}"`;
```

### 错误处理

```javascript
if (!checkSenseApiKey()) {
  // API Key 未配置，返回友好提示
  return {
    message: '💡 提示：配置 API Key 后可解锁语音功能...'
  };
}
```

---

## 🎯 最佳实践

### 1. 声明可选依赖

```json
{
  "dependencies": {
    "skills": [
      {
        "id": "kid-point-voice-component",
        "required": false,  // 可选依赖
        "reason": "语音功能需要"
      }
    ]
  }
}
```

### 2. 提供友好提示

```javascript
if (!dependencyInstalled) {
  return {
    message: '💡 提示：安装 XXX 后可解锁此功能...'
  };
}
```

### 3. 核心功能独立

```javascript
// 文字功能不依赖任何技能
function handlePointsInput(input) {
  // 直接处理，无需检查依赖
}
```

### 4. 首次运行检查

```javascript
// 仅首次运行检查，避免重复提示
if (isFirstRun()) {
  checkDependencies();
  markFirstRunComplete();
}
```

---

## 📊 元技能优势

| 优势 | 说明 | 用户受益 |
|------|------|---------|
| **模块化** | 技能独立开发维护 | 更新不影响其他技能 |
| **可选依赖** | 核心功能无需依赖 | 降低使用门槛 |
| **自动检查** | 首次使用自动提示 | 用户无需手动检查 |
| **友好引导** | 清晰的安装步骤 | 降低配置难度 |
| **灵活扩展** | 轻松添加新依赖 | 功能可扩展 |

---

## 🧪 测试

```bash
# 测试依赖检查
node scripts/install-dependencies.js

# 测试首次运行
rm scripts/.first-run-check
node agent-handler.js

# 测试功能
node scripts/test-prompts.js
```

---

## 📝 更新日志

### v1.2.0 (2026-03-14)
- ✅ 实现元技能依赖管理
- ✅ 自动检查依赖技能
- ✅ 友好的安装引导
- ✅ 可选依赖机制

---

_让技能像乐高积木一样灵活组合！_ 🧱
