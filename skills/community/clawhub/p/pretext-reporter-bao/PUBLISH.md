# 发布指南

## 发布到 ClawHub

### 前置条件

1. ✅ 已创建 GitHub 仓库
2. ✅ 已构建 TypeScript 代码 (`npm run build`)
3. ✅ 已创建必要的元数据文件 (`_meta.json`, `.clawhub/origin.json`)
4. ✅ 已编写完整的 `SKILL.md` 和 `README.md`

### 步骤 1: 创建 GitHub 仓库

```bash
cd C:/Users/jovi_/clawd/skills/pretext-reporter-bao

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Pretext Reporter Bao v0.1.0"

# 创建 GitHub 仓库后，添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/pretext-reporter-bao.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 2: 更新 package.json

将以下字段替换为实际值：

```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/YOUR_USERNAME/pretext-reporter-bao.git"
  },
  "bugs": {
    "url": "https://github.com/YOUR_USERNAME/pretext-reporter-bao/issues"
  },
  "homepage": "https://github.com/YOUR_USERNAME/pretext-reporter-bao#readme"
}
```

### 步骤 3: 发布到 ClawHub

**方式 1: 通过 ClawHub CLI**

```bash
# 安装 ClawHub CLI
npm i -g clawhub

# 登录 ClawHub
clawhub login

# 发布技能
clawhub publish
```

**方式 2: 通过网页**

1. 访问 https://clawhub.ai
2. 点击 "Submit Skill"
3. 填写技能信息：
   - 名称: `pretext-reporter-bao`
   - 描述: 文本测量和Canvas布局报告工具
   - 仓库 URL: https://github.com/YOUR_USERNAME/pretext-reporter-bao
   - 分类: Development / Utilities
4. 提交审核

### 步骤 4: 验证发布

```bash
# 搜索技能
clawhub search pretext-reporter-bao

# 或在网页搜索
https://clawhub.ai/skills?search=pretext-reporter-bao
```

### 步骤 5: 测试安装

```bash
# 用户安装测试
clawhub install pretext-reporter-bao

# 验证文件
ls -la ~/.clawhub/skills/pretext-reporter-bao
```

---

## 集成到 OpenClaw

### 在本地使用

**方式 1: 直接引用**

```bash
cd C:/Users/jovi_/clawd

# 已在 skills/pretext-reporter-bao 目录中
# OpenClaw 会自动加载
```

**方式 2: 通过 SKILL.md 加载**

确保 `skills/pretext-reporter-bao/SKILL.md` 存在且格式正确。

### 在代码中使用

```typescript
import { measureText, generateCanvasReport } from './skills/pretext-reporter-bao/dist/index.js'

// 测量文本
const result = await measureText('你好世界 🚀', {
  font: '16px Inter',
  maxWidth: 320,
  lineHeight: 24
})

console.log(result)
// {
//   text: '你好世界 🚀',
//   characterCount: 5,
//   lineCount: 1,
//   height: 24,
//   width: 87.5,
//   lines: [...]
// }

// 生成 Canvas 报告
const canvasConfig = await generateCanvasReport('你好世界 🚀', {
  font: '16px Inter',
  maxWidth: 320,
  lineHeight: 24,
  backgroundColor: '#ffffff',
  textColor: '#000000'
})

// 在浏览器环境中使用 canvasConfig
```

### 作为 OpenClaw 工具使用

创建一个包装工具：

```typescript
// tools/pretext-tool.ts
import { measureText, generateCanvasReport, generateMarkdownReport, generateJSONReport } from '../skills/pretext-reporter-bao/dist/index.js'

export async function textMeasurementTool(text: string, options: any = {}) {
  return await measureText(text, options)
}

export async function canvasReportTool(text: string, options: any = {}) {
  return await generateCanvasReport(text, options)
}

export async function markdownReportTool(text: string, options: any = {}) {
  const result = await measureText(text, options)
  return generateMarkdownReport(result)
}

export async function jsonReportTool(text: string, options: any = {}) {
  const result = await measureText(text, options)
  return generateJSONReport(result)
}
```

---

## 维护和更新

### 发布新版本

```bash
# 更新版本号
npm version patch  # 0.1.0 -> 0.1.1
npm version minor  # 0.1.0 -> 0.2.0
npm version major  # 0.1.0 -> 1.0.0

# 提交和推送
git add .
git commit -m "Release v0.1.1"
git tag v0.1.1
git push
git push --tags

# 更新 ClawHub
clawhub publish
```

### 版本号规范

遵循 Semantic Versioning (semver):

- `MAJOR.MINOR.PATCH` (如: 0.1.0)
  - **MAJOR**: 不兼容的 API 变更
  - **MINOR**: 向后兼容的功能新增
  - **PATCH**: 向后兼容的 bug 修复

---

## 相关资源

- **ClawHub**: https://clawhub.ai
- **ClawHub 文档**: https://docs.openclaw.ai/tools/clawhub
- **OpenClaw 技能文档**: https://docs.openclaw.ai
- **awesome-openclaw-skills**: https://github.com/VoltAgent/awesome-openclaw-skills
