# PRD Workflow 技能包 - 安装说明

---

## 📦 压缩包内容

```
prd-workflow.tar.gz (10KB)
├── prd-workflow/
│   ├── SKILL.md                 # 技能定义（6.3KB）
│   ├── README.md                # 使用说明（2.6KB）
│   ├── workflows/
│   │   └── README.md           # 工作流编排（4.6KB）
│   ├── templates/
│   │   └── questions-template.json  # 访谈问题库（4.2KB）
│   └── examples/
│       └── pension-example.md  # 完整示例（2.6KB）
```

---

## 🔧 安装步骤

### Step 1: 解压到技能目录

**macOS / Linux**:
```bash
# 解压到 OpenClaw 技能目录
tar -xzf prd-workflow.tar.gz \
    -C ~/.openclaw/workspace/skills/
```

**Windows (PowerShell)**:
```powershell
# 解压到 OpenClaw 技能目录
Expand-Archive prd-workflow.tar.gz \
    -DestinationPath ~\.openclaw\workspace\skills\
```

---

### Step 2: 验证安装

```bash
# 检查技能文件是否存在
ls ~/.openclaw/workspace/skills/prd-workflow/

# 应该看到：
# SKILL.md  README.md  workflows/  templates/  examples/
```

---

### Step 3: 开始使用

**基础用法**:
```
用 prd-workflow 生成一个养老规划功能的 PRD
```

**指定模板**:
```
用 prd-workflow 生成 PRD，使用金融模板
```

**指定输出**:
```
用 prd-workflow 生成 PRD，导出为 Word 文档
```

---

## 📋 使用示例

### 完整流程示例

```
用户：我想做个养老规划功能

AI: 让我先深入了解你的需求。

【Step 1: 深度访谈】
1. 目标用户年龄段？
2. 收入水平定位？
3. 养老测算精度？
4. 是否需要产品推荐？
5. 数据来源？
[... 20 个问题后 ...]

✅ 共享理解确认！

【Step 2: 需求拆解】
✅ 功能清单（MoSCoW 优先级）
✅ 用户故事（10+ 条）
✅ 验收标准（Given-When-Then）

【Step 3: PRD 生成】
✅ 完整 PRD 文档（9 个章节）
✅ 合规检查点（15 个）
✅ 原型描述
✅ Word 文档导出
```

---

## 🎯 适用场景

### ✅ 推荐使用
- 需求模糊，需要深度澄清
- 复杂业务，涉及多个模块
- 金融 PRD，需要合规检查点
- 正式交付，需要完整文档

### ❌ 不推荐
- 简单功能，需求明确 → 用 prd-generator
- 紧急需求，当天上线 → 用 prd-generator（快速模式）

---

## 📖 文档说明

| 文件 | 说明 |
|------|------|
| **SKILL.md** | 技能完整定义，包含工作流、模板、示例 |
| **README.md** | 快速开始指南，安装和使用说明 |
| **workflows/README.md** | 工作流编排逻辑详解 |
| **templates/questions-template.json** | 6 维度访谈问题库 |
| **examples/pension-example.md** | 养老规划完整示例 |

---

## 🆘 常见问题

### Q1: 解压后找不到技能？
**A**: 检查解压路径是否正确：
```bash
ls ~/.openclaw/workspace/skills/prd-workflow/
```

### Q2: 使用时提示找不到技能？
**A**: 重启 OpenClaw 或重新加载技能：
```bash
openclaw skills reload
```

### Q3: 如何更新技能？
**A**: 重新解压新版本覆盖即可：
```bash
tar -xzf prd-workflow-new.tar.gz \
    -C ~/.openclaw/workspace/skills/ --overwrite
```

---

## 📞 技术支持

- **技能版本**: 4.2.5
- **创建日期**: 2026-03-24
- **更新日期**: 2026-04-08
- **作者**: gotomanutd
- **许可**: MIT

**问题反馈**:
- 查看 SKILL.md 了解详细信息
- 查看 README.md 获取使用指南
- 查看 examples/ 获取完整示例

---

## 🎁 技能亮点

1. ✅ **一站式完成** - 无需切换多个技能
2. ✅ **深度访谈** - 16-50 个问题，探索设计树
3. ✅ **双模板支持** - 金融/通用两种
4. ✅ **合规检查** - 15 个金融行业合规点
5. ✅ **完整示例** - 养老规划完整案例
6. ✅ **可分享** - 完整文档，易于传播
7. ✅ **图片渲染** - Mermaid 自动渲染为 PNG（v3.0.0）
8. ✅ **Word 导出** - 自动嵌入图表图片（v3.0.0）

---

🎉 欢迎使用和反馈！

---

## 📝 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| **v4.1.0** | **2026-04-05** | **🔍 内容检查问答引导** - 13项内容检查 + 问答引导修补 + 三种处理方式 |
| **v4.0.0** | **2026-04-05** | **🚀 多页面原型系统** - 页面树推断 + 导航组件 + 路由注入 + 多端截图 |
| **v3.0.0** | **2026-04-04** | **🖼️ 图片渲染服务** - Mermaid → PNG 自动渲染 + Word 导出嵌入图片 |
| **v2.8.9** | **2026-04-04** | **🏗️ 架构图表** - 系统架构图 + 功能框架图 + htmlPrototype 配置动态生成 |
| **v2.8.8** | **2026-04-04** | **🤖 AI 图表提取** - 流程图从 inputs/outputs 推断 + 原型布局动态生成 |
| **v2.8.7** | **2026-04-04** | **🔧 依赖完善** - postinstall 自动安装 mermaid-cli（必需）+ 截图方案优化 |
| **v2.8.6** | **2026-04-04** | **📄 模板库扩展** - 6种页面类型(list/form/dashboard/login/landing/checkout) + 完整设计系统集成 |
| **v2.8.5** | **2026-04-04** | **🎨 设计系统集成** - htmlPrototype 与 ui-ux-pro-max 协作 + 设计系统自动注入 |
| **v2.8.4** | **2026-04-04** | **📸 智能截图** - html2image 优先 + Safari 零依赖 + Playwright 备选 + 自动依赖安装 |
| **v2.8.3** | **2026-04-04** | **🔧 可移植性** - 移除硬编码路径 + 动态路径检测 + 添加测试套件 |
| **v2.8.1** | **2026-04-04** | **🔧 Bug 修复** - 降级策略修复 + 文档与实现一致性修复 |
| **v2.7.1** | **2026-04-04** | **🚀 准备发布** - 统一版本号 + 刷新版本历史 |
| **v2.7.0** | **2026-04-04** | **🤖 AI 集成优化** - 新增 ai_entry.js + 错误处理增强 |
| **v2.6.0** | **2026-04-01** | **🔧 迭代支持** - 版本管理 + 需求对比 + 回滚 |
| **v2.0** | **2026-03-30** | **🔄 真正集成** - 内置调用 6 个技能 |
| **v1.0** | **2026-03-24** | **📦 初始版本** - 基础工作流 |

---

**最后更新**: 2026-04-08
