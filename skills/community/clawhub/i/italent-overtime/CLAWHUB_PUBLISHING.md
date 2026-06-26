# 🚀 北森 iTalent 加班管理 Skill - 发布到 ClawHub 中央仓库

## 📋 目标

将 `italent-overtime` Skill 发布到 ClawHub 中央仓库，让其他用户可以通过一条命令安装：

```bash
npx clawhub install italent-overtime
```

安装完成后，用户可以直接用自然语言使用：

```
帮我推送一个加班，今晚 6 点到 9 点，原因是项目上线
```

---

## 🎯 发布流程

### 步骤 1：注册 ClawHub 账号

1. 访问 https://clawhub.com
2. 注册账号（支持 GitHub/Google 登录）
3. 记住你的用户名

---

### 步骤 2：登录 ClawHub CLI

```bash
# 方式 A：浏览器登录（推荐）
npx clawhub login

# 方式 B：使用 Token 登录
# 1. 在 https://clawhub.com/settings/tokens 获取 Token
# 2. 运行
npx clawhub auth --token YOUR_TOKEN
```

**验证登录：**
```bash
npx clawhub whoami
```

---

### 步骤 3：准备发布

#### 3.1 检查 Skill 结构

确保目录结构正确：

```
italent-overtime/
├── SKILL.md                      # ✅ 必需
├── skill.json                    # ✅ 必需（元数据）
├── scripts/
│   └── italent-overtime-simple.py  # ✅ 主程序
├── references/
│   ├── api-docs.md               # ✅ 参考文档
│   └── troubleshooting.md        # ✅ 故障排查
└── publish.sh                    # 发布脚本
```

#### 3.2 更新 skill.json

确保包含正确的元数据：

```json
{
  "name": "italent-overtime",
  "version": "1.1.0",
  "description": "北森 iTalent 加班管理。当用户需要推送加班、查询加班、撤销加班、管理考勤时使用此技能。",
  "author": "佳敏",
  "license": "MIT",
  "homepage": "https://github.com/your-org/italent-overtime",
  "keywords": ["北森", "iTalent", "加班", "考勤", "HR"],
  "main": "SKILL.md",
  "scripts": {
    "main": "scripts/italent-overtime-simple.py"
  },
  "references": [
    "references/api-docs.md",
    "references/troubleshooting.md"
  ],
  "requirements": {
    "python": ">=3.6",
    "external_deps": []
  },
  "triggers": [
    "加班",
    "推送加班",
    "查询加班",
    "撤销加班",
    "北森",
    "iTalent",
    "考勤"
  ],
  "examples": [
    "帮我推送一个加班",
    "查询本周的加班记录",
    "撤销昨天的加班申请"
  ]
}
```

---

### 步骤 4：发布到 ClawHub

```bash
# 进入 Skill 目录
cd ~/.openclaw/skills/italent-overtime

# 发布
npx clawhub publish .
```

**或者使用发布脚本：**

```bash
cd ~/.openclaw/skills/italent-overtime
bash publish.sh
```

---

### 步骤 5：验证发布

```bash
# 搜索已发布的 Skill
npx clawhub search italent-overtime

# 查看 Skill 详情
npx clawhub inspect italent-overtime
```

---

## 📦 用户安装和使用

### 安装

用户安装只需要一条命令：

```bash
npx clawhub install italent-overtime
```

安装完成后，Skill 会自动加载到 OpenClaw。

---

### 首次配置

安装后，用户需要认证：

```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key "你的 AppKey" \
    --secret "你的 AppSecret" \
    --save
```

---

### 使用（自然语言）

安装完成后，用户可以直接用自然语言对话：

```
# 推送加班
帮我推送一个加班，今晚 6 点到 9 点，原因是项目上线

# 查询加班
查询一下我本周的加班记录

# 撤销加班
撤销我昨天提交的加班申请

# 批量查询
查询张三和李三上周的加班情况
```

OpenClaw 会自动：
1. 识别用户意图
2. 触发 `italent-overtime` Skill
3. 调用相应的 CLI 命令
4. 返回结果给用户

---

## 🔄 更新 Skill

当你需要更新 Skill 时：

```bash
# 1. 修改代码和文档
# 编辑 SKILL.md, scripts/, references/ 等

# 2. 更新版本号
# 编辑 skill.json，增加 version 号

# 3. 重新发布
cd ~/.openclaw/skills/italent-overtime
npx clawhub publish .

# 4. 通知用户更新
# 用户可以通过以下命令更新
npx clawhub update italent-overtime
```

---

## 📊 查看统计数据

```bash
# 查看 Skill 的下载量、评分等
npx clawhub skill stats italent-overtime

# 查看 Skill 信息
npx clawhub skill info italent-overtime
```

---

## 🔐 安全建议

### 1. 不要提交敏感信息

❌ **错误：** 在 skill.json 中包含真实的 Key/Secret
```json
{
  "app_key": "真实的 Key",  // ❌ 不要这样做
  "app_secret": "真实的 Secret"  // ❌ 不要这样做
}
```

✅ **正确：** 只包含示例
```json
{
  "auth_required": true,
  "auth_instructions": "用户需要自己提供 AppKey 和 AppSecret"
}
```

### 2. 说明权限需求

在 SKILL.md 中明确说明：
- 需要北森开放平台账号
- 需要申请加班管理权限
- Token 有效期 2 小时

### 3. 提供隐私说明

说明：
- 数据存储在本地（`~/.italent-overtime.conf`）
- 不会上传用户数据
- 所有 API 调用直接到北森服务器

---

## 🐛 故障排查

### 发布失败：权限不足

**错误：**
```
Error: Authentication required. Please run `clawhub login`
```

**解决：**
```bash
npx clawhub login
```

---

### 发布失败：Skill 已存在

**错误：**
```
Error: Skill 'italent-overtime' already exists
```

**解决：** 增加版本号后重新发布
```bash
# 编辑 skill.json，增加 version
# 例如：1.1.0 -> 1.2.0
npx clawhub publish .
```

---

### 安装失败：找不到 Skill

**错误：**
```
Error: Skill 'italent-overtime' not found
```

**解决：**
1. 确认发布成功：`npx clawhub search italent-overtime`
2. 检查 Skill 名称是否正确
3. 等待几分钟（可能有缓存延迟）

---

## 📝 最佳实践

### 1. 语义化版本

遵循 [Semantic Versioning](https://semver.org/)：
- **MAJOR.MINOR.PATCH** (1.1.0)
- 重大变更增加 MAJOR
- 新功能增加 MINOR
- Bug 修复增加 PATCH

### 2. 清晰的文档

- SKILL.md 要简洁明了
- 提供使用示例
- 包含故障排查指南

### 3. 测试充分

发布前测试：
- ✅ 所有命令可以正常运行
- ✅ 文档中的示例可以执行
- ✅ 错误提示清晰友好

### 4. 响应用户反馈

- 及时修复 Bug
- 根据反馈改进功能
- 定期更新文档

---

## 🎓 示例：完整的用户旅程

### 场景：新员工需要提交加班

**1. 安装 Skill**
```bash
npx clawhub install italent-overtime
```

**2. 首次认证**
```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key "7C4D767784DA4A1F8867E273EC4FB4C1" \
    --secret "C954062B461A4FF1A8F917F95B74D3B8AE88439641604014B8A643FFF07C0044" \
    --save
```

**3. 使用自然语言提交加班**

用户说：
```
帮我提交一个加班，今天晚上 6 点到 9 点，原因是项目上线
```

OpenClaw 自动执行：
```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py push \
    --email "zhangsan@company.com" \
    --start "2026-03-31 18:00:00" \
    --end "2026-03-31 21:00:00" \
    --reason "项目上线"
```

返回结果：
```
✅ 加班提交成功！
加班 ID: ccd2ca1e-xxxx-xxxx-xxxx-b2ca3b580bbc
审批流程已启动
```

---

## 📞 技术支持

- **ClawHub 文档：** https://clawhub.com/docs
- **OpenClaw 文档：** https://docs.openclaw.ai
- **Skill 问题：** 查看 `references/troubleshooting.md`
- **作者：** 佳敏

---

## 🎉 总结

通过 ClawHub 中央仓库，你可以：

✅ **一次发布，全球可用**
✅ **用户一键安装**
✅ **自动更新机制**
✅ **版本管理**
✅ **统计和反馈**

让你的 Skill 帮助更多人！🚀

---

**最后更新：** 2026-03-31  
**作者：** 佳敏
