---
name: harness-dev-standards
description: Harness Engineering 开发规范体系 - 全流程质量门禁与自动治理标准。基于企业级全AI研发实践改进，提供完整的代码交付质量保障框架。Use when: (1) 启动新项目开发前, (2) 代码交付前做质量检查, (3) 需要标准化开发流程, (4) 执行架构评审、代码评审, (5) 排查依赖/环境问题
---

# Harness Engineering 开发规范体系

## 核心哲学

> **"质量不是检查出来的，是构建出来的"**

基于 Harness Engineering 理念 + 企业级全AI研发实践，构建从需求到交付的全链路质量保障体系。

---

## 🚀 快速启动

### 新项目初始化检查清单

**每次启动新项目必须执行：**

```bash
# 1. 检查目录结构是否符合标准
# 2. 检查 package.json 依赖完整性
# 3. 检查 .env.example 配置完整性
# 4. 检查 README 文档完整性
```

---

## 🔐 质量门禁 (Quality Gates)

**每次交付必须通过以下 6 道门禁：**

### 1. 需求门禁 (Requirement Gate)
- ✅ 需求完整清晰，无模糊点
- ✅ 所有需求点已记录到任务追踪
- ✅ 技术可行性已验证
- ✅ 依赖边界已明确

### 2. 架构门禁 (Architecture Gate)
- ✅ 技术选型适合单人开发
- ✅ 文件结构清晰，符合标准化规范
- ✅ 依赖最小化，无冗余包
- ✅ 扩展性设计合理

**参考：** 查看 [references/standards.md](references/standards.md) 标准化文件结构

### 3. 编码门禁 (Coding Gate)
- ✅ 语法正确，无 TypeScript/JavaScript 错误
- ✅ import 路径全部正确
- ✅ 命名规范清晰（camelCase 变量、PascalCase 组件）
- ✅ 不遗漏任何功能点
- ✅ 类型定义完整，无 `any` 滥用

### 4. 依赖门禁 (Dependency Gate)
- ✅ package.json 包含所有需要的依赖
- ✅ 无多余依赖（`depcheck` 验证）
- ✅ 依赖版本稳定（非 alpha/beta）
- ✅ lockfile 已提交（pnpm-lock.yaml / package-lock.json）

**工具：** 运行 `scripts/depcheck.sh` 自动检查

### 5. 环境门禁 (Environment Gate)
- ✅ .env.example 包含所有需要的配置
- ✅ 每个配置项有说明注释
- ✅ 敏感信息不提交到 git
- ✅ .gitignore 配置正确

### 6. 交付门禁 (Delivery Gate)
- ✅ 所有需求点都已实现
- ✅ 项目能正常启动
- ✅ README 写清楚使用方法
- ✅ 构建无错误（`npm run build` 验证）

---

## 🤖 自动治理 (Auto Remediation)

出现以下问题时，**自动修复，无需人工干预：**

| 问题类型 | 自动修复策略 |
|---------|------------|
| 依赖安装报错 | 分析错误 → 修改版本号或移除多余依赖 |
| import 路径错误 | 自动查找正确路径修复 |
| 语法错误 | 自动修正 TypeScript/JavaScript 语法 |
| 启动失败 | 读取错误日志 → 修复后重新检查 |
| 类型错误 | 补全类型定义或修正类型不匹配 |

**修复流程：**
1. 识别错误信息
2. 定位问题代码位置
3. 应用修复策略
4. 验证修复结果
5. 重复直到问题解决

---

## 📁 标准化文件结构

### Next.js 项目标准结构

```
project-name/
├── app/                    # Next.js App Router
│   ├── page.tsx            # 首页
│   ├── layout.tsx          # 全局布局
│   └── globals.css         # 全局样式
├── lib/                   # 工具库、第三方客户端
├── public/                 # 静态资源
├── .env.example            # 环境变量示例
├── .gitignore              # git忽略规则
├── package.json
├── tsconfig.json
├── README.md               # 必须写清楚
└── *-init.sql              # 数据库初始化SQL
```

**README 必须包含：**
- 项目介绍
- 配置步骤
- 启动命令
- 环境变量说明

**详细规范：** 查看 [references/standards.md](references/standards.md)

---

## ✅ 代码质量标准

### TypeScript 规范

- ✅ 类型正确，无隐式 `any`
- ✅ 命名清晰，变量名表达用途
- ✅ 注释够用，不冗余
- ✅ 函数单一职责
- ✅ 避免深层嵌套（超过 3 层考虑重构）

### 项目规范

- ✅ README 完整，新人能按文档启动
- ✅ 环境配置说明清晰
- ✅ 依赖干净，无未使用包
- ✅ gitignore 正确，不提交敏感文件

---

## 🛠️ 内置工具脚本

### 依赖检查脚本
```bash
# 运行依赖检查
./scripts/depcheck.sh
```

功能：
- 检测未使用的依赖
- 检测缺失的依赖
- 检测版本冲突
- 生成修复建议

### 代码质量扫描脚本
```bash
# 运行代码质量扫描
./scripts/quality-scan.sh
```

功能：
- TypeScript 类型检查
- ESLint 规则检查
- 命名规范检查
- import 路径验证

---

## 📋 交付前检查清单

**交付前逐项确认：**

- [ ] 需求门禁：所有需求点实现完毕
- [ ] 架构门禁：文件结构符合标准
- [ ] 编码门禁：无语法/类型错误
- [ ] 依赖门禁：依赖干净无冗余
- [ ] 环境门禁：.env.example 完整
- [ ] 交付门禁：项目能正常启动构建
- [ ] README：包含完整使用说明

---

## 📚 参考文档

| 文档 | 内容 |
|-----|------|
| [references/standards.md](references/standards.md) | 详细文件结构规范 + 命名规范 |
| [references/checklist.md](references/checklist.md) | 完整交付检查清单模板 |
| [references/remediation.md](references/remediation.md) | 常见问题自动修复策略库 |

---

## 💡 设计理念

### 为什么这样设计？

1. **前置质量** - 把质量检查左移到开发过程每个环节，不是最后才检查
2. **自动修复** - 能自动修的绝不麻烦人，解放生产力
3. **标准化** - 降低认知负担，所有项目看起来都一样
4. **渐进式** - 不追求完美，每次交付比上一次更好

### 和传统开发流程的区别

| 传统流程 | Harness Engineering |
|---------|-------------------|
| 最后统一测试 | 每一步都有质量门禁 |
| 人找问题 | 问题自动暴露并修复 |
| 每个项目结构都不一样 | 标准化结构，上手成本为0 |
| 依赖问题靠经验解决 | 自动检测并给出修复方案 |

---

*"The best code is the code you don't have to think about."* - Harness Engineering Philosophy
