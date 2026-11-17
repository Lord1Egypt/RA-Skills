# 🤖 销售行为管理助手 - 公开发布指南

> Skill 版本：v1.1.0 (公开版)  
> 创建日期：2026-03-11

---

## 📦 Skill 文件

**文件名：** `sales-assistant.skill`

**文件大小：** 9.6KB

**包含内容：**
- `SKILL.md` - 核心指令（自动初始化架构）
- `scripts/init.sh` - 自动初始化脚本
- `templates/cold-start.md` - 冷启动模板
- `templates/moment-library.md` - 朋友圈素材库
- `evals/evals.json` - 测试用例

---

## 🚀 安装方式

### 方法 1：本地安装（推荐测试）

```bash
# 1. 下载 skill 文件
cp sales-assistant.skill ~/.openclaw/skills/

# 2. 验证安装
ls ~/.openclaw/skills/sales-assistant.skill

# 3. 重启 OpenClaw Gateway
openclaw gateway restart
```

### 方法 2：通过 ClawHub 发布（公开分享）

```bash
# 1. 解压 skill 文件
cd ~/.openclaw/workspace/skills/
tar -xzf sales-assistant.skill

# 2. 发布到 ClawHub
clawhub publish sales-assistant

# 3. 其他人可以安装
clawhub install sales-assistant
```

---

## 🎯 首次使用流程

### 步骤 1：安装 Skill

```bash
# 用户安装 skill 后，第一次提到相关功能时自动触发
```

### 步骤 2：自动初始化

当检测到用户首次使用时，自动执行：

1. **创建飞书多维表格（3 个）**
   - 🔥 暖客池管理系统
   - 📅 约访管理系统
   - 🏆 业绩追踪系统

2. **创建飞书文档（2 个）**
   - 🔥 暖客池 - 冷启动模板
   - 📝 朋友圈素材库

3. **创建表单视图（3 个）**
   - 📝 每日签单反馈
   - 📝 周复盘问卷
   - 📝 月复盘问卷

4. **保存配置文件**
   - 路径：`~/.openclaw/workspace/sales-assistant-config.json`
   - 包含所有资源链接和配置参数

### 步骤 3：填写冷启动模板

用户填写冷启动模板文档：
- 至少 10-20 个客户/线索
- 包含姓名、微信、关系状态、需求等
- 发回给助手批量导入

### 步骤 4：配置 Cron 任务

```bash
# 销售任务包推送（工作日 9:30）
openclaw cron add --name "销售任务包" --schedule "0 9:30 * * 1-5"

# 每日签单反馈（工作日 18:00）
openclaw cron add --name "签单反馈" --schedule "0 18 * * 1-5"

# 周复盘问卷（周日 20:00）
openclaw cron add --name "周复盘" --schedule "0 20 * * 0"

# 月复盘问卷（月末 20:00）
openclaw cron add --name "月复盘" --schedule "0 20 L * *"
```

### 步骤 5：开始使用

第二天早上 9:30 开始接收第一个任务包！

---

## 📊 用户数据结构

### 数据隔离

每个用户拥有独立的资源：
- ✅ 独立的多维表格（app_token 不同）
- ✅ 独立的飞书文档（doc_id 不同）
- ✅ 独立的配置文件（本地存储）

### 权限说明

| 资源类型 | 默认权限 | 谁能访问 |
|---------|---------|---------|
| 多维表格 | 私有 | 仅创建者 + 邀请的人 |
| 飞书文档 | 私有 | 仅创建者 + 分享的人 |
| 表单数据 | 私有 | 仅创建者可查看所有提交 |

### 配置文件示例

```json
{
  "initialized": true,
  "init_date": "2026-03-11T13:27:00+08:00",
  "version": "1.1.0",
  "resources": {
    "bitable": {
      "warm_pool": "FslSbnx82asAbesk9encAt5Vnjb",
      "visit_tracking": "DarabZwTmaovUDsmM0hckILpnFb",
      "performance": "LsmYbhgmeako0PsB6rxcxCyOnkd"
    },
    "docs": {
      "cold_start_template": "UdzVdAreWo0HNixe0e3c23XynKb",
      "moment_library": "AZCHdjeIEoaXbsxnpghcSiJknRh"
    }
  },
  "settings": {
    "warmup_count": 3,
    "visit_target": 5,
    "moment_frequency": 5
  }
}
```

---

## 🔧 初始化脚本说明

### 自动初始化（推荐）

Skill 会在首次使用时自动调用飞书 API 创建资源。

**触发条件：**
- 配置文件不存在
- 或 `initialized: false`

**创建的资源：**
- 3 个飞书多维表格
- 2 个飞书文档
- 3 个表单视图

### 手动初始化（备选）

如果自动初始化失败，可以运行手动脚本：

```bash
# 进入 skill 目录
cd ~/.openclaw/workspace/skills/sales-assistant/

# 运行初始化脚本
bash scripts/init.sh
```

---

## 🧪 测试用例

已包含 6 个测试用例（`evals/evals.json`）：

1. ✅ 搭建客户管理系统
2. ✅ 今日暖客任务
3. ✅ 朋友圈素材
4. ✅ 签单记录
5. ✅ 周复盘
6. ✅ 销售懒散求建议

**运行测试：**

```bash
# 使用 skill-creator 测试
cd ~/.openclaw/workspace/skills/skill-creator/
python -m scripts.run_loop \
  --eval-set ../sales-assistant/evals/evals.json \
  --skill-path ../sales-assistant/
```

---

## 📝 更新日志

### v1.1.0 - 公开版（2026-03-11）

**重大改进：**
- ✅ 重构为自动初始化架构
- ✅ 移除硬编码资源链接
- ✅ 添加配置文件管理
- ✅ 支持多用户独立使用
- ✅ 添加自动/手动初始化脚本
- ✅ 完善模板文件

**安全性：**
- ✅ 数据完全隔离
- ✅ 每个用户独立资源
- ✅ 无跨用户数据泄露风险

### v1.0.0 - 初始版（2026-03-11）

- ✅ 暖客池管理系统
- ✅ 约访管理系统
- ✅ 业绩追踪系统
- ✅ 每日任务推送
- ✅ 周/月复盘问卷

---

## 📞 发布到 ClawHub

### 步骤 1：准备发布

```bash
# 检查 skill 结构
cd ~/.openclaw/workspace/skills/sales-assistant/
ls -la

# 应该包含：
# - SKILL.md
# - scripts/
# - templates/
# - evals/
```

### 步骤 2：发布

```bash
# 发布到 clawhub.com
clawhub publish sales-assistant

# 输入信息：
# - 名称：sales-assistant
# - 描述：保险代理人销售行为管理助手
# - 版本：1.1.0
# - 标签：sales, insurance, feishu, crm
```

### 步骤 3：验证发布

```bash
# 搜索已发布的 skill
clawhub search sales

# 应该能看到 sales-assistant
```

### 步骤 4：安装说明

告诉用户如何安装：

```bash
# 安装 skill
clawhub install sales-assistant

# 验证安装
ls ~/.openclaw/skills/sales-assistant/
```

---

## 🎯 用户使用流程

### 新用户

1. **安装 Skill**
   ```bash
   clawhub install sales-assistant
   ```

2. **首次对话**
   ```
   用户：帮我搭建一个客户管理系统
   助手：检测到您首次使用，正在自动创建资源...
        ✅ 暖客池管理系统已创建
        ✅ 约访管理系统已创建
        ✅ 业绩追踪系统已创建
        ✅ 冷启动模板已创建
        ✅ 朋友圈素材库已创建

        📝 下一步：请填写冷启动模板文档
        🔗 链接：https://www.feishu.cn/docx/xxx
   ```

3. **填写模板**
   - 打开冷启动模板
   - 填写 10-20 个客户
   - 发回给助手

4. **开始使用**
   - 第二天 9:30 收到第一个任务包
   - 执行任务 → 反馈结果
   - 每周日填写周复盘
   - 每月末填写月复盘

---

## ⚠️ 注意事项

### 依赖要求

- ✅ OpenClaw Gateway v2026.3.8+
- ✅ 飞书开放平台 API 权限
- ✅ 飞书用户 OAuth 授权

### 权限要求

飞书应用需要以下权限：
- `bitable:app` - 创建/管理多维表格
- `docs:document` - 创建/管理云文档
- `calendar:event` - 创建日程（可选）

### 兼容性

- ✅ OpenClaw 所有版本
- ✅ 飞书个人版/企业版
- ❌ 不支持钉钉/企业微信（需要适配）

---

## 📊 预期效果

**使用 4 周后：**

| 指标 | 使用前 | 使用后 | 提升 |
|------|-------|-------|------|
| 每日暖客数 | 0-1 个 | 3 个 | +300% |
| 每周朋友圈 | 0-2 条 | 5 条 | +250% |
| 每周约访 | 1-2 个 | 5 个 | +250% |
| 月签单数 | 2-3 个 | 4-6 个 | +100% |
| 客户跟进率 | 30% | 80% | +50% |

---

## 📞 支持与反馈

**问题反馈：**
- GitHub Issues: https://github.com/your-repo/sales-assistant/issues
- 飞书联系：@your-contact

**更新计划：**
- v1.2.0 - 添加更多话术模板
- v1.3.0 - 支持钉钉/企业微信
- v2.0.0 - AI 智能话术生成

---

**版本：** v1.1.0 (公开版)  
**许可：** MIT License  
**维护者：** Your Name
