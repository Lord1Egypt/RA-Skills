# 💻 MVP 开发示例 - 电商网站

> 使用晴晴自动激活 + 多模型并行 + 安全内置

---

## 🎯 场景

你想开发一个电商网站 MVP，包括：
- 前端：商品列表、购物车、结账页面
- 后端：用户认证、订单管理、支付集成
- 数据库：商品、用户、订单数据
- 设计：UI/UX 设计
- 测试：质量保证

---

## 🚀 晴晴自动激活流程

### 步骤 1：一句话启动

```bash
# 直接说需求
"我想开发一个电商网站 MVP"

# 晴晴自动识别：产品开发场景
# 自动激活技能组合：
# 1. agency-agents --orchestrator (项目编排)
# 2. agency-agents --engineering (工程开发)
# 3. agency-agents --design (设计)
# 4. agency-agents --testing (测试)
# 5. ironclaw-guardian-evolved (安全检测)
# 6. todolist (任务管理)
# 7. feishu-file-delivery (文件交付)
```

---

### 步骤 2：项目编排 (自动)

```
orchestrator 自动分解任务:
├─ 前端开发 (React + Tailwind CSS)
│   ├─ 首页
│   ├─ 商品列表
│   ├─ 购物车
│   └─ 结账页面
│
├─ 后端开发 (Node.js + Express)
│   ├─ 用户认证 (JWT)
│   ├─ 订单管理
│   └─ 支付集成 (Stripe)
│
├─ 数据库设计 (MongoDB)
│   ├─ 商品 Schema
│   ├─ 用户 Schema
│   └─ 订单 Schema
│
├─ UI/UX 设计
│   ├─ 配色方案
│   ├─ 组件设计
│   └─ 响应式布局
│
└─ 测试 QA
    ├─ 单元测试
    ├─ 集成测试
    └─ E2E 测试
```

---

### 步骤 3：多模型并行开发

```
并行任务分配:
├─ frontend-developer → qwen3-coder:480b-cloud (编码专用)
├─ backend-architect → qwen3.5:397b-cloud (主模型)
├─ database-designer → qwen3.5:397b-cloud
├─ ui-designer → minimax-m2.5:cloud (创意)
└─ testing-engineer → qwen3.5:35b-a3b (本地)

预计耗时：20 分钟 (vs 单模型 60 分钟，提升 3x)
```

---

### 步骤 4：安全检测 (免费本地)

```bash
# 自动生成代码后，ironclaw 自动扫描
python3 skills/ironclaw-guardian-evolved/scripts/ironclaw_audit.py scan src/

# 检测项:
# - 危险命令 (rm -rf, sudo)
# - 硬编码密钥 (API keys)
# - Prompt injection
# - 本地路径泄露

# 输出:
# ✅ 所有文件安全 (Label 0, Confidence 99%)
```

---

### 步骤 5：质量验证

```
reality-checker 最终审核:
├─ 代码质量检查
├─ 功能完整性验证
├─ 性能基准测试
└─ 安全漏洞扫描

通过率：99% (生成 + 审查 + 优化流程)
```

---

### 步骤 6：任务管理

```bash
# todolist 自动创建任务清单
├─ [x] 前端开发 - 完成
├─ [x] 后端开发 - 完成
├─ [x] 数据库设计 - 完成
├─ [x] UI/UX 设计 - 完成
├─ [ ] 测试 QA - 进行中
└─ [ ] 部署上线 - 待开始
```

---

### 步骤 7：文件交付

```bash
# feishu-file-delivery 自动交付到飞书
├─ 代码仓库 (ZIP)
├─ 设计文件 (Figma 链接)
├─ 数据库 Schema (JSON)
├─ API 文档 (Markdown)
└─ 部署指南 (PDF)
```

---

## 📋 完整命令示例

### 自动激活 (推荐)

```bash
# 一句话启动全流程
"我想开发一个电商网站 MVP，目标用户是年轻人，预算 10 万，使用 React 和 Node.js"

# 晴晴自动执行:
# 1. 识别：产品开发场景
# 2. 激活：orchestrator + engineering + design + testing
# 3. 并行：多模型协作
# 4. 检测：ironclaw 安全扫描
# 5. 管理：todolist 任务追踪
# 6. 交付：feishu-file-delivery
```

### 手动调用 (可选)

```bash
# 启动编排器
/orchestrator "开发一个电商网站，包括前端、后端、数据库、设计、测试"

# 查看任务分解
orchestrator 输出任务树

# 并行开发
/frontend-developer "创建 React 商品列表页面，使用 Tailwind CSS"
/backend-architect "设计 Node.js REST API，包括用户认证和订单管理"
/ui-designer "设计电商网站 UI，配色年轻活泼"

# 安全检测
/ironclaw-guardian-evolved "扫描 src/ 目录"

# 任务管理
/todolist "创建电商网站开发任务清单"
```

---

## 🎯 输出成果

### 代码结构

```
ecommerce-mvp/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProductList.jsx
│   │   │   ├── ShoppingCart.jsx
│   │   │   └── Checkout.jsx
│   │   └── pages/
│   │       ├── Home.jsx
│   │       └── ProductDetail.jsx
│   └── package.json
│
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   ├── auth.js
│   │   │   ├── products.js
│   │   │   └── orders.js
│   │   └── models/
│   │       ├── User.js
│   │       ├── Product.js
│   │       └── Order.js
│   └── package.json
│
├── database/
│   └── schema.json
│
├── design/
│   └── ui-design.fig
│
└── docs/
    ├── API.md
    └── DEPLOYMENT.md
```

### 交付文件

- ✅ 完整代码 (前端 + 后端)
- ✅ 数据库 Schema
- ✅ UI 设计文件
- ✅ API 文档
- ✅ 部署指南
- ✅ 测试报告
- ✅ 安全审计报告

---

## ⚡ 性能指标

| 指标 | 数值 |
|------|------|
| 开发时间 | 20 分钟 (多模型并行) |
| 代码行数 | ~2,000 行 |
| 测试覆盖率 | 85%+ |
| 安全通过率 | 100% |
| 质量评分 | 4.8/5 |

---

## 💡 技巧与建议

### 1. 提供明确需求

```
✅ "我想开发一个电商网站 MVP，目标用户是年轻人，预算 10 万，使用 React 和 Node.js，需要商品列表、购物车、结账功能"
❌ "做个网站"
```

### 2. 接受主动建议

```
✅ 让晴晴建议技术栈、架构、最佳实践
❌ 拒绝所有主动建议
```

### 3. 迭代优化

```
第一轮：生成初稿
  ↓
反馈：调整配色、优化性能
  ↓
第二轮：优化改进
  ↓
反馈：添加搜索功能
  ↓
第三轮：最终完善
```

### 4. 安全优先

```
# 所有代码自动经过 ironclaw 检测
# 无需额外 API，免费本地执行
# 隐私保护，数据不出境
```

---

## 🎉 完成！

现在你有一个完整的电商网站 MVP：
- ✅ 前端：React + Tailwind CSS
- ✅ 后端：Node.js + Express
- ✅ 数据库：MongoDB
- ✅ 设计：UI/UX 完整
- ✅ 测试：85%+ 覆盖率
- ✅ 安全：100% 通过检测
- ✅ 文档：API + 部署指南

**下一步**: 部署上线！🚀

---

*最后更新：2026-03-15*  
*版本：1.0.0 晴晴 MVP 示例*
