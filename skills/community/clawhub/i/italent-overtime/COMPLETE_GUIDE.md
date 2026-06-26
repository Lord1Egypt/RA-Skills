# 🚀 北森 iTalent 加班管理 Skill - 完整发布和使用指南

## 📋 概述

这是一个完整的北森 iTalent 加班管理 Skill，可以发布到 ClawHub 中央仓库，让其他用户通过一条命令安装并使用自然语言管理加班。

---

## 🎯 完整流程

```mermaid
graph LR
    A[创建 Skill] --> B[本地测试]
    B --> C[发布到 ClawHub]
    C --> D[用户安装]
    D --> E[自然语言使用]
```

---

## 📦 第一部分：发布者指南

### 1. 准备 Skill

Skill 已经创建完成，位于：
```
~/.openclaw/skills/italent-overtime/
```

**目录结构：**
```
italent-overtime/
├── SKILL.md                      # 主文档
├── skill.json                    # 元数据
├── publish-to-clawhub.sh         # 发布脚本
├── CLAWHUB_PUBLISHING.md         # 详细发布指南
├── scripts/
│   └── italent-overtime-simple.py  # CLI 主程序
└── references/
    ├── api-docs.md               # API 文档
    └── troubleshooting.md        # 故障排查
```

---

### 2. 发布到 ClawHub

#### 方式 A：使用发布脚本（推荐）

```bash
cd ~/.openclaw/skills/italent-overtime
bash publish-to-clawhub.sh
```

脚本会：
1. ✅ 检查必要文件
2. ✅ 验证登录状态
3. ✅ 显示 Skill 信息
4. ✅ 确认发布
5. ✅ 执行发布

#### 方式 B：手动发布

```bash
# 1. 登录 ClawHub
npx clawhub login

# 2. 验证登录
npx clawhub whoami

# 3. 发布 Skill
cd ~/.openclaw/skills/italent-overtime
npx clawhub publish .
```

---

### 3. 验证发布

```bash
# 搜索 Skill
npx clawhub search italent-overtime

# 查看详情
npx clawhub inspect italent-overtime

# 查看统计
npx clawhub skill stats italent-overtime
```

---

## 📥 第二部分：用户安装指南

### 1. 安装 Skill

用户只需要一条命令：

```bash
npx clawhub install italent-overtime
```

安装完成后，Skill 会自动加载到 OpenClaw。

---

### 2. 首次配置

安装后需要认证（获取北森 API 访问令牌）：

```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key "你的 AppKey" \
    --secret "你的 AppSecret" \
    --save
```

**如何获取 AppKey/AppSecret：**
1. 登录北森开放平台：https://open.italent.cn
2. 创建应用
3. 获取 AppKey 和 AppSecret

---

### 3. 使用（自然语言对话）

安装完成后，用户可以直接用自然语言对话：

#### 推送加班

```
帮我推送一个加班，今晚 6 点到 9 点，原因是项目上线
```

OpenClaw 会自动执行：
```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py push \
    --email "zhangsan@company.com" \
    --start "2026-03-31 18:00:00" \
    --end "2026-03-31 21:00:00" \
    --reason "项目上线"
```

---

#### 查询加班

```
查询一下我本周的加班记录
```

或者查询特定员工：
```
查询张三和李三上周的加班情况
```

---

#### 撤销加班

```
撤销我昨天提交的加班申请
```

---

#### 查看帮助

```
加班管理有哪些功能
```

---

## 🔄 第三部分：更新和维护

### 更新 Skill（发布者）

```bash
# 1. 修改代码和文档
# 编辑 SKILL.md, scripts/, references/ 等

# 2. 更新版本号
# 编辑 skill.json，增加 version 号
# 例如：1.1.0 -> 1.2.0

# 3. 重新发布
cd ~/.openclaw/skills/italent-overtime
npx clawhub publish .
```

---

### 更新 Skill（用户）

```bash
# 更新到最新版本
npx clawhub update italent-overtime

# 更新到特定版本
npx clawhub install italent-overtime@1.2.0
```

---

## 📊 第四部分：统计数据

### 查看 Skill 数据

```bash
# 下载量
npx clawhub skill stats italent-overtime --downloads

# 评分
npx clawhub skill stats italent-overtime --rating

# 用户反馈
npx clawhub skill reviews italent-overtime
```

---

## 🔐 第五部分：安全最佳实践

### 1. 不要提交敏感信息

❌ **错误：**
```json
{
  "app_key": "真实的 Key",
  "app_secret": "真实的 Secret"
}
```

✅ **正确：**
```json
{
  "auth_required": true,
  "auth_instructions": "用户需要自己提供 AppKey 和 AppSecret"
}
```

---

### 2. 说明权限需求

在 SKILL.md 中明确说明：
- ✅ 需要北森开放平台账号
- ✅ 需要申请加班管理权限
- ✅ Token 有效期 2 小时

---

### 3. 隐私保护

说明：
- ✅ 数据存储在本地（`~/.italent-overtime.conf`）
- ✅ 不会上传用户数据
- ✅ 所有 API 调用直接到北森服务器

---

## 🎓 第六部分：完整示例

### 场景：HR 需要批量查询加班

**1. 安装 Skill**
```bash
npx clawhub install italent-overtime
```

**2. 认证**
```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key "你的 AppKey" \
    --secret "你的 AppSecret" \
    --save
```

**3. 使用自然语言查询**

用户说：
```
查询研发部所有员工本周的加班情况
```

OpenClaw 自动执行：
```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py list \
    --staff-ids 10001,10002,10003,10004,10005 \
    --start 2026-03-30 \
    --end 2026-04-05
```

返回结果：
```
找到 8 条加班记录：

  员工 ID: 10001
  排班日期：2026-03-30
  加班时间：2026-03-30 18:00 - 2026-03-30 20:00
  ----------------------------------------
  
  员工 ID: 10002
  排班日期：2026-03-30
  加班时间：2026-03-30 19:00 - 2026-03-30 21:00
  ----------------------------------------
  
  ... (共 8 条)
```

---

## 📞 第七部分：技术支持

### 资源链接

| 资源 | 链接 |
|------|------|
| ClawHub | https://clawhub.com |
| ClawHub 文档 | https://clawhub.com/docs |
| OpenClaw 文档 | https://docs.openclaw.ai |
| 北森开放平台 | https://open.italent.cn |

---

### 故障排查

| 问题 | 解决方案 |
|------|---------|
| 安装失败 | 检查网络连接，确认 clawhub 登录 |
| 认证失败 | 检查 AppKey/AppSecret 是否正确 |
| API 调用失败 | 检查 access_token 是否过期 |
| 权限错误 | 确认北森账号有加班管理权限 |

详细故障排查见：`references/troubleshooting.md`

---

## 🎉 总结

通过这个完整的发布和使用流程，你可以：

### 对发布者
✅ 一次发布，全球可用  
✅ 自动版本管理  
✅ 统计和反馈  
✅ 简单的更新流程  

### 对用户
✅ 一键安装  
✅ 自然语言使用  
✅ 自动更新  
✅ 完整的文档支持  

---

## 📝 快速参考

### 发布命令
```bash
cd ~/.openclaw/skills/italent-overtime
bash publish-to-clawhub.sh
```

### 安装命令
```bash
npx clawhub install italent-overtime
```

### 更新命令
```bash
npx clawhub update italent-overtime
```

### 使用示例
```
帮我推送一个加班，今晚 6 点到 9 点
```

---

**版本：** 1.1.0  
**最后更新：** 2026-03-31  
**作者：** 佳敏  
**许可：** MIT
