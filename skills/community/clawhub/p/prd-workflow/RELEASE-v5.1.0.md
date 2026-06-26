# PRD Workflow v5.1.0 发布说明

**发布日期**: 2026-04-20  
**类型**: 功能增强 + Bug 修复  
**兼容性**: 与 v5.0.0 完全兼容，可直接升级

---

## ✨ 新功能

### 🧠 Wiki 知识库增强（可选）

- 新增 `wiki_search_module.js`，智能匹配业务知识库
- 支持 6 大业务模块自动匹配：产品中心、产品研究、财富规划、基金投顾、投顾展业、监控中心
- Wiki 增强完全可选，无 Wiki 目录不影响正常使用
- `smart_router.js`、`main.js`、`prd_module.js` 完整集成

**效果**：
- 访谈问题数从 16-50 个 → 8-20 个
- PRD 生成时自动注入业务规则和已有数据模型

### 🎨 AI 驱动原型 v6.1.0

- 废弃模板渲染（~800 行硬编码代码）
- 改为单次 AI 调用读取完整上下文（PRD + 设计系统 + UX 指南）
- 页面结构、导航关系、跳转逻辑由 AI 自主判断
- Chart.js CDN 集成，真实图表替代占位符
- 业务规则内化为 JS 校验逻辑（权重 100%、情景数量、成立年限等）

**验证通过**：
- 6 个 Chart.js 图表（折线/柱状/饼图/雷达/环形）
- 4 条业务规则 JS 校验到位
- 无业务规则裸露展示

### 🎯 设计系统持久化

- `ui-ux-pro-max` 设计系统持久化到 `design-system/` 目录
- `MASTER.md` 全局规则 + `tokens.json` 设计 tokens
- 原型生成自动引用设计系统规范

---

## 🔧 变更清单

| 文件 | 变更 |
|------|------|
| `workflows/main.js` | Wiki 搜索执行 + 进度显示优化 |
| `workflows/smart_router.js` | wiki_search 技能注册 + 依赖更新 |
| `workflows/modules/wiki_search_module.js` | **新增** Wiki 查询模块 |
| `workflows/modules/prd_segmented_module.js` | **新增** PRD 分段确认模块 |
| `workflows/modules/prototype_module.js` | 升级到 v6.1.0（AI 驱动 + Chart.js + JS 校验） |
| `workflows/modules/design_module.js` | 升级到 v3.0.0（持久化 MASTER.md） |
| `workflows/modules/prd_module.js` | Wiki 增强支持 |
| `SKILL.md` | 更新为 v5.1.0，增加 Wiki 增强章节 |
| `clawhub.json` | 版本 4.2.5 → 5.1.0 |
| `install.json` | 版本 4.2.5 → 5.1.0 |

---

## 📦 依赖变更

**新增可选依赖**：无  
**删除依赖**：无  
**兼容 OpenClaw**: >=2026.2.26

---

## ⚠️ 注意事项

1. **Wiki 目录**: `wiki-ai/` 目录是可选的，没有它不影响正常使用
2. **原型生成**: AI 驱动原型需要 LLM 调用，确保 AI 执行器可用
3. **向后兼容**: v5.0.0 的 `prd-segmented` 模式仍然可用

---

## 🚀 升级步骤

1. 备份现有 `prd-workflow` 目录
2. 覆盖安装新版本
3. 无需修改配置，直接使用

---

**许可**: MIT-0  
**作者**: gotomanutd + 红曼为帆
