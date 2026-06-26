---
name: product-design-workflow
description: |
  完整的产品设计全流程（含每日定时任务+汇报机制）：
  1. 每日定时生成3个产品idea（按市场行情/A股/基金主题，1个小白向+2个普通向）
  2. 生成PRD产品设计文档
  3. 制作HTML原型页面
  4. 上传到服务器
  5. 分步骤汇报到指定群

  【需要用户提供的参数】：
  - 服务器配置：server-host, server-user, server-pass, server-path, preview-domain
  - 汇报群ID：target-group-id
  - 每日定时时间：schedule-time（默认08:50开始）

  使用场景：快速产品设计、产品创意头脑风暴、原型制作发布、每日产品提案生成
---

# 产品设计工作流（完整流程版）

完整的产品设计全流程：定时任务 → 头脑风暴 → PRD文档 → HTML原型 → 上传服务器 → 分步骤汇报

---

## 🚨 必须先看！其他agent操作指南

### 第一步：确认用户已提供所有必要参数
在开始执行任何任务前，**必须先确认用户已提供以下所有参数**：

| 参数名 | 说明 | 是否必填 | 示例 |
|--------|------|---------|------|
| `server-host` | 服务器IP地址 | ✅ 必填 | `192.168.****` |
| `server-user` | 服务器用户名 | ✅ 必填 | `*****` |
| `server-pass` | 服务器密码 | ✅ 必填 | `your-password` |
| `server-path` | 服务器上Demo存放路径 | ✅ 必填 | `/www/wwwroot/demo/` |
| `preview-domain` | Demo预览域名 | ✅ 必填 | `http://demo.yourdomain.com` |
| `target-group-id` | 汇报群ID（飞书等） | ✅ 必填 | `oc_b5b****7498` |
| `schedule-time` | 每日定时开始时间 | ⚠️ 可选（默认08:50） | `08:50` |
| `work-dir` | 工作目录 | ⚠️ 可选（默认当前目录） | `./` |

如果用户未提供任何必填参数，**必须先询问用户**，不要直接开始执行！

---

### 第二步：完整工作流程（严格遵守）

| 时间（默认） | 任务 | 输出 | 汇报内容 |
|-------------|------|------|---------|
| 08:50 | 生成3个头脑风暴点子 | 每个点子对应目录+idea.md | 【步骤1/3】Idea生成汇报 |
| 08:55 | 生成PRD产品设计文档 | 每个点子对应product-design.md | 【步骤2/3】PRD生成汇报 |
| 09:10 | 制作HTML Demo+上传服务器 | Demo页面+上线URL | 【步骤3/3】Demo上线汇报 |

---

## 🛑 强制规则（违反必究！）

### 1. 每日3个点子的方向规则
**主题覆盖要求**：每日生成的3个点子必须固定覆盖以下三个主题方向：
- 第1个点子：**市场行情**方向（C端用户向）
- 第2个点子：**A股**方向（C端用户向）
- 第3个点子：**基金**方向（C端用户向）

**受众配比要求**：3个点子的受众配比必须为：
- 1个：**Z世代小白向**（绝对通俗易懂，禁止专业术语）
- 2个：**普通正常向**（无需特别小白，正常表达即可）

**标签规范**：每个点子的`idea.md`头部必须包含正确的标签：
- 格式：`**标签**: [市场行情/A股/基金] · [小白向/普通向]`
- 示例：`**标签**: 市场行情 · 小白向`

**内容红线**：
- ❌ 禁止出现加密货币相关内容
- ❌ 小白向内容绝对通俗易懂，禁止专业术语
- ✅ 所有点子从用户需求出发，不纠结技术实现难度
- ✅ 都是C端面向普通用户的，不是B端企业服务

---

## 📋 分步骤执行指南（其他agent必须严格按照这个来！）

### 步骤0：任务开始前的准备
1. 确认在正确的工作目录
2. 确认所有必填参数已获取
3. 先向用户/群说明总目标：
   > 「我现在开始执行[任务名称，比如：每日产品设计全流程]，按照规范分3步完成，每步完成后立即汇报。」

---

### 步骤1：生成3个头脑风暴点子
1. 按照「强制规则」生成3个点子
2. 每个点子创建单独目录：`YYYY-MM-DD-[slug]/`
3. 在每个目录下创建`idea.md`，内容参考 `references/idea-template.md`
4. 运行 `scripts/rules-check.py` 检查规则是否符合
5. 检查通过后，立即汇报！

**汇报模板**：参考 `references/step-by-step-report-spec.md` 中的「第一次汇报模板」

---

### 步骤2：生成PRD产品设计文档
1. 为每个点子生成详细的PRD文档
2. 文档保存为：`YYYY-MM-DD-[slug]/product-design.md`
3. 内容参考 `references/prd-template.md` 和 `references/prd-design-spec.md`
4. 为每个点子选择合适的HTML模板：
   | 模板名称 | 适用场景 |
   |---------|---------|
   | `base.html` | 简单单页、活动页、说明页 |
   | `list-template.html` | 列表页、卡片列表、榜单类页面 |
   | `detail-template.html` | 详情页、文章页、分析报告页 |
   | `tool-template.html` | 工具页、计算器、查询类功能页 |
5. PRD完成后，立即汇报！

**汇报模板**：参考 `references/step-by-step-report-spec.md` 中的「第二次汇报模板」

---

### 步骤3：制作HTML Demo+上传服务器
1. 按照PRD和选择的HTML模板，制作Demo页面
2. Demo保存到：`YYYY-MM-DD-[slug]/demo/`
3. 运行 `scripts/upload_demos.py` 上传到服务器
4. 上传成功后，立即汇报！

**汇报模板**：参考 `references/step-by-step-report-spec.md` 中的「第三次汇报模板」

---

## 📁 完整目录结构（执行后生成）
```
./
├── ideas/
│   └── YYYY-MM-DD-[slug1]/
│       ├── idea.md
│       ├── product-design.md
│       └── demo/
│           ├── index.html
│           └── assets/
├── YYYY-MM-DD-[slug2]/...
└── YYYY-MM-DD-[slug3]/...
```

---

## 🔧 脚本使用说明

### rules-check.py
**强制使用**：每次生成idea后必须运行！
```bash
python scripts/rules-check.py [YYYY-MM-DD]
```

### upload_demos.py
上传Demo到服务器（所有参数必填）：
```bash
python scripts/upload_demos.py \
    --date 2026-05-07 \
    --slugs slug1 slug2 slug3 \
    --server-host 192.168.**** \
    --server-user ***** \
    --server-pass your-password \
    --server-path /www/wwwroot/demo/ \
    --preview-domain http://demo.yourdomain.com
```

---

## 📚 参考文档（必须阅读！）
- `references/idea-template.md`：点子模板
- `references/prd-template.md`：PRD模板
- `references/idea-content-spec.md`：点子内容规范
- `references/prd-design-spec.md`：PRD设计规范
- `references/report-template-spec.md`：汇报文案模板
- `references/step-by-step-report-spec.md`：分步骤汇报流程规范

---

## ⚠️ 前置依赖（用户需要安装）
需要安装 `sshpass` 工具（用于免密SSH/SCP）：
- Ubuntu/Debian：`sudo apt install sshpass`
- CentOS/RHEL：`sudo yum install sshpass`
