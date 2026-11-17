---
name: kingdoc
displayName: 金山文档 KingDoc
slug: kingdoc
version: 2.1.0
description: >
  金山文档 AI 协作助手 — 6 品类在线文档全生命周期管理
  （文字/电子表格/演示文稿/多维表格/收集表/附件），覆盖创建、编辑、
  管理、权限、版本历史、回收站全链路。对标腾讯文档、覆盖其全部 8 大功能。
  额外支持：回收站、版本历史、格式转换、纯文本提取、通知推送、
  多维表格 Webhook、批量异步任务。
description_zh: "金山文档 AI 协作助手 — 6 品类在线文档全生命周期管理"
category: 办公效率
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: [文档处理, 表格处理, PPT生成, 多维表格, 表单收集, 政企合规]
license: MIT
requires_api_key: true
---

# KingDoc — 金山文档 AI 协作助手 v2.1.0

## ⚠️ 首次使用必读

### 1. 申请金山开放平台 App（免费）

**不申请 App，所有 API 调用都会报 KD001 鉴权失败。**

申请步骤：
1. 访问 [金山开放平台](https://developer.kdocs.cn) 并登录你的金山文档账号
2. 进入「应用管理」→「创建应用」
3. 填写应用名称（如：`KingDoc`）和应用描述
4. 获取 **`App ID`** 和 **`App Secret`**
5. 选择应用权限（OAuth Scope）：
   - 必须勾选：`user:file:write`、`user:file:read`、`team:file:write`、`team:file:read`
   - 建议勾选：`user:team:read`（查看团队信息）、`user:notification:write`（推送通知）
6. 应用审核通常 1 个工作日通过，测试阶段限速 500 次/天，申请正式版后 10 万次/天

### 2. 配置 KingDoc

拿到 App ID 和 Secret 后执行：
```bash
# Linux/macOS
bash setup.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File setup.ps1
```
脚本会引导你输入 App ID 和 Secret。

---

## 快速开始

| 你想做什么 | 直接对 AI 说 |
|-----------|-------------|
| 新建一个会议纪要 | `"帮我写一份会议纪要"` |
| 创建 Excel 数据表 | `"建一个销售数据表格，含产品/销量/金额"` |
| 生成 PPT | `"帮我做一份产品发布 PPT"` |
| 查看文档内容 | `"看看这个文档说了什么"` |
| 找一个文件 | `"搜一下上个月的合同"` |
| 上传本地文件 | `"把这个 PDF 上传到云端"` |
| 恢复误删文件 | `"回收站里有没有昨天删的 Word？"` |
| 回滚到历史版本 | `"这份文档改坏了，回退到上周版本"` |
| 分享文档权限 | `"给张三发个可编辑的链接"` |
| 归档到文件夹 | `"把文件移到 2026 项目文件夹"` |
| 提取文字 | `"把这张发票的文字提取出来"` |
| 格式转换 | `"把这份文档转成 PDF"` |

---

## 安全声明

| 保护项 | 方式 |
|--------|------|
| 🔒 删除确认 | 删除操作走回收站 API，不物理删除 |
| 🗑️ 软删除+恢复 | `trash.list → trash.recover` |
| 📝 版本冲突检测 | 写入前获取最新版本号，冲突时提示用户合并 |
| 🔐 权限前置校验 | 所有写入操作前自动检查权限，无权限拒绝 |
| ⚡ 限流保护 | 429 自动指数退避重试（最多 5 次） |
| 🛡️ 文件类型拦截 | 默认禁止上传 .exe/.bat/.ps1 等可执行文件 |
| 🔑 Token 安全 | Token 仅存在于内存，不落盘 |
| 📋 审计日志 | 所有写操作记录到本地日志 |
| 🔀 批量合并 | 50ms 窗口内连续写入自动合并为一次请求 |

---

## 支持的文档类型（6 品类）

| 类型 | doc_type | 推荐度 | 创建方式 | 编辑方式 | 说明 |
|------|----------|--------|---------|---------|------|
| 文字文档 | doc | ⭐⭐⭐ | API 自动创建 | 本地生成+上传覆盖 | 自动排版，支持 DOCX 输出 |
| 电子表格 | sheet | ⭐⭐⭐ | API 自动创建 | API 精细编辑 | 单元格/公式/图表/筛选/排序 |
| 演示文稿 | ppt | ⭐⭐⭐ | API 自动创建 | 本地生成+上传覆盖 | 自动排版，支持 PPTX 输出 |
| 多维表格 | smartsheet | ⭐⭐⭐ | API 自动创建 | API 精细编辑 | 记录/字段/视图管理 |
| 收集表 | form | ⭐⭐⭐ | API 自动创建 | API 自动编辑 | 表单创建/答卷查询/提交 |
| 附件 | attachment | ⭐⭐⭐ | API 自动上传 | — | 本地文件/图片直接上传 |

---

## 场景路由表

先判断用户的操作意图属于以下 4 大类中的哪一类，再按子表路由到对应工具集。

### 1️⃣ 文档创建（从无到有）

| 用户意图 / 关键词 | 品类 | 首选创建方法 | 编辑方法 |
|------------------|------|------------|---------|
| 报告/笔记/文章/总结/会议纪要 | doc | `kdoc.file.create` | `kdoc.local.docx.generate` → 上传覆盖 |
| PPT/幻灯片/演示文稿 | ppt | `kdoc.file.create` | `kdoc.local.pptx.generate` → 上传覆盖 |
| 数据表格/计算/统计/Excel | sheet | `kdoc.et.create` | `kdoc.et.*` 精细编辑 |
| 多维表格/轻维表 | smartsheet | `kdoc.dbt.create` | `kdoc.dbt.*` 精细编辑 |
| 表单/收集表/问卷 | form | `kdoc.form.create` | `kdoc.form.*` 配置 |
| 上传文件/图片/附件 | attachment | `kdoc.file.upload` | — |

### 2️⃣ 文档编辑（改内容）

先通过 `kdoc.file.info` 或链接前缀确定原始文档类型，再路由到对应编辑工具集。**严禁用 A 品类的工具改 B 品类文档。**

| 原始文档类型 | 编辑工具集 |
|------------|-----------|
| 文字文档 | `kdoc.local.docx.generate` → 上传覆盖（整文件替换） |
| 电子表格 | `kdoc.et.*` 精细编辑（单元格/公式/图表） |
| 演示文稿 | `kdoc.local.pptx.generate` → 上传覆盖（整文件替换） |
| 多维表格 | `kdoc.dbt.*` 精细编辑（记录/字段/视图） |
| 收集表 | `kdoc.form.*` 配置修改 |

### 3️⃣ 文件管理（不动内容，只动文件/目录/权限）

| 动作 | 工具 |
|------|------|
| 重命名/移动/删除/复制 | `kdoc.file.*` |
| 导入（本地→云端） | `kdoc.file.upload` |
| 导出（云端→本地） | `kdoc.file.download` |
| 权限变更/分享链接 | `kdoc.file.permission` / `kdoc.share.*` |
| 回收站查询/恢复 | `kdoc.trash.list` / `kdoc.trash.recover` |
| 版本历史/回滚 | `kdoc.version.list` / `kdoc.version.restore` |
| 批量操作 | `kdoc.batch.create` → `kdoc.batch.query` |
| 空间管理 | `kdoc.space.*` / `kdoc.folder.*` |

### 4️⃣ 格式转换（文档↔其他格式）

| 场景 | 工具 |
|------|------|
| 文档→PDF/Word/Excel/PPT | `kdoc.office.convert` |
| 文档纯文本提取 | `kdoc.office.extract` |
| 通知推送（企微/钉钉/金山协作） | `kdoc.notification.send` |
| 多维表格 Webhook 设置 | `kdoc.dbt.webhook.set` |

---

## 公共能力

| 场景 | 工具 |
|------|------|
| 获取文档内容 | `kdoc.file.content` |
| 文档纯文本提取 | `kdoc.office.extract` |
| 格式转换 | `kdoc.office.convert` |
| 搜索文档 | `kdoc.file.search` |
| 获取文档元信息 | `kdoc.file.info` |
| 上传图片 | `kdoc.file.upload` |
| 用户信息 | `kdoc.user.info` |
| 空间用量 | `kdoc.space.quota` |
| 能力上报 | `kdoc.report.unsupported` |
| SKILL 更新检查 | `kdoc.skill.update_check` |

---

## 常见工作流

### 1. 创建+编辑文字文档
```
步骤1: kdoc.file.create(name="会议纪要", type="doc")
步骤2: kdoc.local.docx.generate(content="会议内容...", template="meeting_notes")
步骤3: kdoc.file.upload(file_path="output.docx", file_id=<file_id>)
返回: docs.qq.com/doc/<file_id>
```

### 2. 创建+编辑电子表格
```
步骤1: kdoc.et.create(name="销售数据")
步骤2: kdoc.et.range.write(sheet_id=<id>, range="A1:C10", values=[...])
步骤3: kdoc.et.formula.set(sheet_id=<id>, cell="D1", formula="=SUM(C1:C10)")
返回: docs.qq.com/sheet/<file_id>
```

### 3. 创建多维表格
```
步骤1: kdoc.dbt.create(name="客户管理")
步骤2: kdoc.dbt.field.add(table_id=<id>, name="客户名", type="text")
步骤3: kdoc.dbt.field.add(table_id=<id>, name="签约金额", type="number")
步骤4: kdoc.dbt.record.add_batch(table_id=<id>, records=[{...}])
返回: docs.qq.com/dbt/<file_id>
```

### 4. 搜索并读取文档
```
步骤1: kdoc.file.search(keyword="合同", limit=10)
步骤2: kdoc.file.info(file_id=<file_id>)
步骤3: kdoc.file.content(file_id=<file_id>)
返回: 文档内容
```

### 5. 恢复误删文件
```
步骤1: kdoc.trash.list(limit=20)
步骤2: kdoc.trash.recover(file_id=<file_id>)
返回: 已恢复文件信息
```

### 6. 回滚到历史版本
```
步骤1: kdoc.version.list(file_id=<file_id>)
步骤2: kdoc.version.restore(file_id=<file_id>, version=<target_version>)
返回: 回滚结果
```

### 7. 本地文件上传
```
步骤1: kdoc.space.list()  → 选择目标文件夹
步骤2: kdoc.file.upload(file_path="D:\docs\报告.pdf", folder_id=<id>)
步骤3: kdoc.file.permission(file_id=<id>, members=[{email: "xxx", role: "editor"}])
返回: 上传成功 + 文档链接
```

### 8. 格式转换
```
步骤1: kdoc.office.convert(file_id=<id>, target_format="pdf")
步骤2: kdoc.file.download(file_id=<转换后的file_id>, save_path="D:\output.pdf")
返回: 下载成功
```

### 9. 多维表格 Webhook 设置
```
步骤1: kdoc.dbt.webhook.set(table_id=<id>, callback_url="https://your-app.com/webhook", events=["record.add", "record.update"])
步骤2: kdoc.dbt.webhook.list(table_id=<id>)
返回: Webhook 配置确认
```

### 10. 批量导入数据
```
步骤1: kdoc.batch.create(operation="import", files=[...])
步骤2: kdoc.batch.query(task_id=<task_id>)  → 轮询直到完成
返回: 导入结果 + 成功/失败统计
```

---

## 核心规则（铁律）

1. 🚨 **品类隔离**：通过 `kdoc.file.info` 识别品类后按路由表选择对应工具集。**严禁用 A 品类的工具改 B 品类文档。**
2. 📦 **批量优先**：电子表格/多维表格连续 3 次及以上写入**必须**用批量接口（`kdoc.et.range.write` / `kdoc.dbt.record.add_batch`）。
3. 🔒 **权限前置**：所有写入操作前**必须**调用前置权限校验。
4. 🔄 **异步轮询**：批量任务、格式转换等异步操作，**必须**使用子会话轮询，主会话保持响应。
5. 🗑️ **软删除**：删除**必须**走回收站 API（`kdoc.file.delete` → 回收站），不物理删除。
6. 📝 **审计日志**：所有写操作**必须**记录到本地审计日志。
7. ⚡ **限流退避**：收到 429 **必须**自动指数退避重试（间隔 2^n 秒 + 随机抖动，最多 5 次）。
8. 🔀 **版本防冲突**：写入前获取 `file.version`，写入时带版本号，冲突时提示用户合并。

---

## 风险项与限制

| 风险项 | 影响 | 规避措施 |
|--------|------|---------|
| 🔑 账号权限未配置 | 无法调用任何 API | 首次使用弹出授权页引导绑定金山开放平台 App |
| 💰 API 配额不足（测试应用 500 次/天） | 写入操作被拒绝 | 提示用户申请正式应用（100,000 次/天） |
| 📝 文字/演示只能文件级远程编辑 | 无法逐段/逐页编辑 | 自动降级为"本地生成 → 上传覆盖"模式 |
| 🗑️ 图片 OCR 不支持 | 无法直接识别图中文字 | 仅支持在线文档→纯文本提取；图片需先转在线文档 |
| 📦 大文件上传超时（>100MB） | 上传失败 | 自动切换为异步上传 + 进度轮询 |
| 🔀 版本冲突 | 多人同时编辑导致数据丢失 | 写入前校验版本号，冲突时提示手动合并 |
| 📵 网络依赖 | 所有功能需联网 | 提示用户确保网络连接；关键操作支持离线暂存 |

---

## 错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| KD001 | Token 鉴权失败 | 重新执行 `setup.sh` 授权 |
| KD002 | 权限不足 | 升级应用权限或联系管理员 |
| KD003 | 配额不足 | 申请提额或购买配额 |
| KD004 | 文档类型不匹配 | 执行 `kdoc.file.info` 确认品类后按路由表 |
| KD005 | 文档不存在 | 检查 `file_id` 是否正确 |
| KD006 | 限流触发（429） | 自动指数退避重试 |
| KD007 | 版本冲突 | 获取最新版本后重新写入 |
| KD008 | 文件过大 | 走异步上传 |
| KD009 | 文件类型被拦截 | 检查 MIME 类型，可执行文件禁止上传 |
| KD010 | 服务暂时不可用 | 稍后重试或联系支持 |
| KD011 | 参数错误 | 检查 file_id、content 等必填参数 |
| KD012 | 文件夹不存在 | 检查 `folder_id` 是否正确 |
| KD013 | 表单已截止 | 收集表已过截止日期 |
| KD014 | Webhook 回调失败 | 检查回调 URL 是否可访问 |
| KD015 | 转换失败 | 格式不支持或文件损坏 |

---

## 🔄 自动更新提示

**每天首次使用 KingDoc 时自动检查更新。** 发现新版本时，AI 会主动提示您升级，不会自动安装。

```bash
# 手动检查更新
python -m engine.update_check --version 2.1.0
```

---

## 📋 更新历史

### v2.1.0 — 2026-07-02
**新增功能**
- ✅ 新增每日首次使用自动检查更新提示
- ✅ 新增文档纯文本提取 API（`kdoc.office.extract`）
- ✅ 新增格式转换 API（`kdoc.office.convert`）
- ✅ 新增多维表格 Webhook 事件监听（`kdoc.dbt.webhook.set`）
- ✅ 新增批量异步任务（`kdoc.batch.create` / `kdoc.batch.query`）
- ✅ 新增通知推送（`kdoc.notification.send` 支持企微/钉钉/金山协作）
- ✅ 新增版本历史回滚（`kdoc.version.list` / `kdoc.version.restore`）
- ✅ 新增回收站完整操作（`kdoc.trash.*`）

**体验优化**
- 🔧 SKILL.md 新增「⚠️ 首次使用必读」两步引导
- 🔧 安装脚本自动生成 mcp-config.json、模板文件和占位图标
- 🔧 错误码从 KD001-KD015 扩展到 15 个精确定位
- 🔧 11 个常见工作流全部基于真实金山 API

**安全增强**
- 🛡️ 5 层安全防御模型（用户确认/权限前置/输入校验/操作保护/限流配额）
- 🛡️ 文件 ID 正则校验
- 🛡️ 可执行文件 MIME 双层拦截
- 🛡️ 限流指数退避重试（2^n + 随机抖动）
- 🛡️ 操作审计日志

---

### v2.0.0 — 2026-07-02
**初始版本**
- 🎭 6 品类全功能（文字/电子表格/演示文稿/多维表格/收集表/附件）
- 📄 40+ MCP 工具实现
- 🔗 OAuth Client Credentials 鉴权
- 📝 DOCX/PPTX 本地生成 + 上传覆盖
- 🧭 场景路由表（4 大类 × 6 品类）
- 🗃️ 电子表格精细编辑（单元格/公式/图表/筛选/排序）
- 🗃️ 多维表格精细编辑（记录/字段/视图）
- 📋 11 个可运行工作流
- 📖 6 个参考文档

---

## 详细文档参考

| 文档 | 路径 |
|------|------|
| 鉴权流程 | `references/auth.md` |
| 多维表格 API | `references/dbt_references.md` |
| 电子表格 API | `references/et_references.md` |
| 文本提取/格式转换 | `references/office_references.md` |
| 限流策略 | `references/rate_limit.md` |
| 安全设计 | `references/security.md` |

---

## 安装说明

**前置要求**：
- Python 3.10+
- 金山开放平台 App（AppID + AppSecret）

**快速安装**：
```bash
# Linux / macOS
bash setup.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File setup.ps1
```

安装完成后重启 WorkBuddy 即可生效。

---

*最后更新：2026-07-02 | v2.1.0*
