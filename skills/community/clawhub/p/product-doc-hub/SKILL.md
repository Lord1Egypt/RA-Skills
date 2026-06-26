---
name: product-doc-hub
description: "面向 AI 产品团队的一站式文档解决方案，一套工具覆盖从产品定义到 API 上线的全链路文档：PRD（功能规格说明书）、Product Brief（投资人/团队轻量介绍）、Experience Framework（体验验证方法论，含四维模型+埋点指标+SUS/EV/NPS/SAM量表设计）、API Console（配置化在线调试台）。PRD/Brief/体验框架为内容模板（保留结构换内容），API Console 为零代码配置（改 JS 对象即可定义端点）。适用于：产品立项、团队交接、投资人演示、API 调试。创新点：四类文档统一风格、统一入口，API Console 支持在线发送真实请求并查看响应。"
---

# Product Doc Hub Skill — 产品知识库聚合器 v2（API Console 可配置版）

## 🎯 5 分钟上手

### 最简配置（API Console，复制即用）

```html
<script src="api-console-config.js"></script>
<script>
  window.API_CONSOLE_CONFIG = {
    productName: '我的产品',
    baseUrl:     'https://api.my-product.com',
    groups: [
      {
        name: '用户',
        apis: [
          { method: 'POST', path: '/users', desc: '创建用户',
            params: [
              { name:'name',  type:'text',   required:true,  placeholder:'姓名' },
              { name:'email', type:'text',   required:true,  placeholder:'邮箱' }
            ]
          },
          { method: 'GET',  path: '/users/:id', desc: '查询用户',
            params: [
              { name:'id', type:'text', required:true, placeholder:'用户ID' }
            ]
          }
        ]
      }
    ]
  };
</script>
<script src="api.html"></script>
```

### 其他页面

| 页面 | 定制方式 |
|------|---------|
| **PRD** | 复制 `prd.html`，替换章节内容 |
| **产品简介** | 复制 `product-brief.html`，替换内容 |
| **体验框架** | 复制 `experience-framework.html`，替换四维模型内容 |
| **Hub 导航** | 复制 `hub.html`，修改四个入口链接 |

---

## 概述

本 Skill 提供一套**可配置的产品文档黄页**，包含 PRD/Brief/体验框架/API调试台四类页面。

| 页面 | 文件 | 用途 | 定制方式 |
|------|------|------|---------|
| **PRD** | `prd.html` | 功能规格说明书 | 内容替换 |
| **产品简介** | `product-brief.html` | 面向投资人轻量介绍 | 内容替换 |
| **体验框架** | `experience-framework.html` | AI产品体验验证方法论 | 章节模板 |
| **API 控制台** | `api.html` | 在线 API 调试 | **配置化** ⭐ |
| **Hub 导航** | `hub.html` | 四页面导航入口 | 内容替换 |

---

## ⭐ API Console 配置化（重点）

### 快速使用

```html
<!-- Step 1: 引入配置 -->
<script src="api-console-config.js"></script>

<!-- Step 2: 修改配置 -->
<script>
  window.API_CONSOLE_CONFIG.productName = '我的产品';
  window.API_CONSOLE_CONFIG.baseUrl = 'https://api.my-product.com';

  // 修改端点列表
  window.API_CONSOLE_CONFIG.groups = [
    {
      name: '用户模块',
      icon: '<svg ...>',          // 可选 SVG
      apis: [
        {
          method: 'POST',
          path: '/users',
          desc: '创建用户',
          params: [
            { name: 'name',     type: 'text',   required: true,  desc: '用户名' },
            { name: 'email',    type: 'text',   required: true,  desc: '邮箱' },
            { name: 'role',     type: 'select', required: false, default: 'user',
              options: ['user','admin','vip'], desc: '用户角色' }
          ]
        },
        {
          method: 'GET',
          path: '/users/:id',
          desc: '查询用户详情',
          params: [
            { name: 'id', type: 'text', required: true, desc: '用户 ID' }
          ]
        }
      ]
    }
  ];
</script>

<!-- Step 3: 引入页面 -->
<script src="api.html"></script>
```

页面会自动读取 `API_CONSOLE_CONFIG` 并渲染端点列表、发送请求。

### API_CONSOLE_CONFIG 完整字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `productName` | string | `'本产品'` | 页面标题 |
| `baseUrl` | string | — | API 基础地址 |
| `timeout` | number | `30000` | 请求超时（ms） |
| `showStats` | boolean | `true` | 是否显示统计卡片 |
| `initialStats` | object | 见下方 | 初始统计数据 |
| `groups` | array | 内置默认 | 端点分组列表 |
| `theme` | string | `'dark'` | `'dark'` / `'light'` |

**initialStats 默认值**：
```javascript
{
  totalCalls: 0,    // 总调用次数
  successRate: 100, // 成功率%
  avgLatency: 0,   // 平均延迟ms
  activeTasks: 0   // 活跃任务数
}
```

### 端点参数格式

```javascript
{
  method:   'GET' | 'POST' | 'PUT' | 'DELETE',
  path:     '/endpoint/:param',      // :param 会被识别为路径参数
  desc:     '端点描述',
  params: [                           // 请求参数（用于构造器）
    {
      name:     'paramName',          // 参数名
      type:     'text' | 'file' | 'select',
      required: true | false,
      default:  '默认值',              // 可选
      options:  ['a','b','c'],         // type=select 时必填
      desc:     '参数说明'              // 可选
    }
  ]
}
```

---

## 文件结构

```
product-doc-hub/
├── SKILL.md                          # 本文档
└── assets/
    ├── prd.html                     # 产品需求文档（可直接修改内容）
    ├── product-brief.html            # 产品简介（可直接修改内容）
    ├── experience-framework.html    # 体验框架（保留结构换内容）
    ├── api.html                      # API 调试台（配置化）
    ├── api-console-config.js         # API Console 配置模板 ⭐
    ├── hub.html                      # Hub 导航页
    └── (其他产品文档资源)
```

---

## PRD / Brief 定制指南

### PRD 定制（最快）

1. 复制 `prd.html` 作为 `my-product-prd.html`
2. 全局替换产品名称为"我的产品"
3. 修改各章节的功能规格描述
4. 保留 Callout / Flow / 目录等组件结构

### Brief 定制

1. 复制 `product-brief.html` 作为 `my-product-brief.html`
2. 全局替换产品名称为"我的产品"
3. 修改产品定位、目标用户、核心流程
4. 调整功能状态表（已完成 → 进行中 → 待开发）

### 体验框架 定制

1. 复制 `experience-framework.html` 作为 `my-ef.html`
2. 保留"四维体验验证模型"的结构框架
3. 替换每个维度的具体内容为新产品的设计策略
4. 更新 SUS/EV/SAM/NPS 的具体题目文本
5. 调整埋点指标映射

---

## 设计系统（四个页面共享）

### 暗色主题变量

```css
background: #08080c
surface: rgba(255,255,255,0.02~0.08)
text-primary: #e2e8f0
text-secondary: #94a3b8
accent-blue: #818cf8
accent-green: #10b981
accent-amber: #f59e0b
accent-purple: #a855f7
border: rgba(255,255,255,0.05~0.10)
```

### 通用组件类

| 组件 | CSS 类 | 说明 |
|------|--------|------|
| Callout | `.callout .callout-blue/green/yellow/purple` | 左色条信息卡片 |
| Flow 步骤 | `.flow-step` + `.flow-arrow` | 流程图 |
| 表格 | 标准 `<table>` + th/td | 数据表格 |
| 代码 | `<code>` 半透明底 | 内联代码 |
| 等宽框 | `.diagram` | ASCII 架构图 |

---

## 如何为新产品构建 Product Hub

### 推荐顺序

1. **Brief 先行**（半天）— 写清楚"为什么做"，给所有人看
2. **PRD 跟进**（1-2天）— 写清楚"做什么怎么做"，给实现团队
3. **EF 并行**（1-2天）— 同时设计体验验证方案
4. **API Console 最后**（1小时配置）— 有接口了再配置端点

### 定制检查清单

- [ ] 全局替换产品名称为新产品名
- [ ] 更新 Brief 的产品定义和目标用户
- [ ] 重写 PRD 的功能规格（保留章节结构）
- [ ] 调整 EF 的四维模型内容（保留验证方法论）
- [ ] 更新 API Console 的 `groups` 端点列表
- [ ] 调整配色（如果品牌色不同）
- [ ] 更新版本号和日期

---

## 发布到 GitHub

```bash
cd ~/.codebuddy/skills/product-doc-hub
git init
git add .
git commit -m "feat: product-doc-hub v2"
git remote add origin https://github.com/YOUR_USERNAME/product-doc-hub.git
git push -u origin main
```
