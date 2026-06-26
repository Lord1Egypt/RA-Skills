# prd-workflow v4.2.2 发布说明

**发布日期**: 2026-04-07  
**版本**: v4.2.2  
**类型**: 依赖修复

---

## 📦 更新内容

### 主要变更

**postinstall 脚本添加 adm-zip 依赖检测**

- ✅ 更新 `scripts/postinstall.js`，添加 adm-zip 自动检测
- ✅ Word 文档图片检查功能现在可以正常使用
- ✅ 安装时会自动提示安装 adm-zip（可选依赖）

### 问题背景

**v4.2.1 及之前版本**：
- ⚠️ postinstall 脚本未包含 adm-zip 检测
- ⚠️ Word 导出功能正常，但图片检查跳过
- ⚠️ 环境检查显示：`adm-zip 未安装，Word 图片检查将跳过`

**v4.2.2 修复**：
- ✅ postinstall 脚本自动检测 adm-zip
- ✅ 安装时会提示用户安装 adm-zip
- ✅ Word 图片检查功能完整可用

---

## 🔧 依赖说明

### 必需依赖
| 依赖 | 用途 | 安装方式 |
|------|------|---------|
| mermaid-cli | 流程图渲染 | 自动安装 |
| Node.js | 核心运行环境 | 系统自带 |
| Python 3 | 核心运行环境 | 系统自带 |

### 可选依赖
| 依赖 | 用途 | 安装方式 |
|------|------|---------|
| adm-zip | Word 图片检查 | postinstall 自动提示 |
| html2image | HTML 截图（推荐） | postinstall 自动提示 |
| playwright | HTML 截图（备选） | postinstall 自动提示 |

---

## 📋 完整依赖列表

```javascript
// scripts/postinstall.js

const NODE_DEPS = {
  'mermaid-cli': {
    required: true  // 必需，自动安装
  },
  'adm-zip': {
    required: false  // 可选，提示安装
  },
  'playwright': {
    required: false  // 可选，提示安装
  }
};

const PYTHON_DEPS = {
  'html2image': {
    required: false  // 可选，提示安装
  }
};
```

---

## 🚀 安装说明

### 全新安装
```bash
clawhub install prd-workflow
```

安装后会自动运行 postinstall 脚本，提示安装可选依赖。

### 更新安装
```bash
clawhub update prd-workflow
```

### 手动安装 adm-zip
如果已经安装但缺少 adm-zip：
```bash
cd ~/.openclaw/workspace/skills/prd-workflow
npm install adm-zip
```

---

## ✅ 验证安装

```bash
# 检查 adm-zip 是否可用
node -e "const AdmZip = require('adm-zip'); console.log('✅ adm-zip 已安装')"

# 运行环境检查
cd ~/.openclaw/workspace/skills/prd-workflow
node tests/test.js
```

预期输出：
```
📊 环境检查完成：6/6 可用
✅ mermaid
✅ chrome
✅ python
✅ dotnet
✅ admZip
✅ nodeVersion
```

---

## 📊 版本对比

| 版本 | adm-zip | postinstall | Word 图片检查 |
|------|---------|-------------|-------------|
| v4.2.0 | ❌ | ❌ | ❌ 跳过 |
| v4.2.1 | ❌ | ❌ | ❌ 跳过 |
| **v4.2.2** | ✅ | ✅ | ✅ 正常 |

---

## 🎯 影响范围

**受影响的功能**：
- ✅ Word 文档导出（不受影响，一直可用）
- ✅ 流程图渲染（不受影响）
- ✅ **Word 图片检查**（v4.2.2 新增）

**不受影响的功能**：
- ✅ PRD 生成
- ✅ 流程图绘制
- ✅ UI 设计
- ✅ 原型生成

---

## 📝 更新文件清单

| 文件 | 变更 |
|------|------|
| `workflows/version.js` | 版本号更新为 4.2.2，添加 changelog |
| `scripts/postinstall.js` | 添加 adm-zip 检测逻辑 |
| `clawhub.json` | 版本号更新 |
| `install.json` | 版本号更新 |
| `_meta.json` | 版本号更新 |

---

## 🔗 相关链接

- ClawHub: `clawhub install prd-workflow`
- 技能目录：`~/.openclaw/workspace/skills/prd-workflow/`
- 输出目录：`~/.openclaw/workspace/output/{用户}/{项目}/`

---

**发布状态**: ✅ 安全扫描中  
**预计完成**: 几分钟内  
**安装命令**: `clawhub install prd-workflow`
