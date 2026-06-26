# 📦 北森 iTalent 加班管理 Skill - 发布指南

## ✅ 打包完成

**压缩包：** `~/.openclaw/skills/releases/italent-overtime-v1.1.0.tar.gz`  
**大小：** 11KB  
**版本：** v1.1.0

---

## 📁 Skill 结构

```
italent-overtime/
├── SKILL.md                      # ⭐ 主文档（OpenClaw 加载）
├── skill.json                    # ⭐ 元数据配置
├── publish.sh                    # 发布脚本
├── scripts/
│   └── italent-overtime-simple.py  # ⭐ CLI 主程序
├── references/
│   ├── api-docs.md               # API 接口文档
│   └── troubleshooting.md        # 故障排查指南
└── assets/                       # 资源文件（可选）
```

---

## 🚀 发布方式

### 方式 1：发布到 OpenClaw Skill 仓库（推荐）

#### 步骤 1：上传到仓库

```bash
# 克隆技能仓库
git clone git@github.com:openclaw/skills.git
cd skills

# 复制 Skill
cp ~/.openclaw/skills/releases/italent-overtime-v1.1.0.tar.gz .

# 解压
tar -xzvf italent-overtime-v1.1.0.tar.gz

# 提交
git add italent-overtime/
git commit -m "Add italent-overtime skill v1.1.0"
git push origin main
```

#### 步骤 2：更新技能索引

在技能仓库的 `README.md` 或 `skills-index.json` 中添加：

```json
{
  "name": "italent-overtime",
  "version": "1.1.0",
  "description": "北森 iTalent 加班管理",
  "author": "佳敏",
  "package": "italent-overtime-v1.1.0.tar.gz"
}
```

#### 步骤 3：通知用户安装

```markdown
## 新技能发布：北森 iTalent 加班管理 🎉

**功能：**
- 推送加班数据到北森系统
- 查询员工加班记录
- 撤销加班申请

**安装：**
```bash
openclaw skills install italent-overtime
```

**使用：**
```bash
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key 你的 AppKey --secret 你的 AppSecret --save
```
```

---

### 方式 2：内部共享

#### 步骤 1：上传到内部服务器

```bash
# 上传到文件服务器
scp ~/.openclaw/skills/releases/italent-overtime-v1.1.0.tar.gz \
    user@file-server:/shared/skills/

# 或上传到内部网站
# http://internal/skills/italent-overtime-v1.1.0.tar.gz
```

#### 步骤 2：提供安装说明

```markdown
# 北森加班 Skill 安装说明

## 下载
http://internal/skills/italent-overtime-v1.1.0.tar.gz

## 安装
cd ~/.openclaw/skills/
tar -xzvf italent-overtime-v1.1.0.tar.gz

## 验证
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py help

## 使用
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key 你的 AppKey --secret 你的 AppSecret --save
```

---

### 方式 3：Git 标签发布

```bash
cd ~/.openclaw/skills/italent-overtime

# 初始化 Git（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 创建远程仓库（GitHub/GitLab/Gitee）
git remote add origin git@github.com:your-org/italent-overtime-skill.git

# 打标签发布
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
```

用户可以直接克隆：
```bash
git clone git@github.com:your-org/italent-overtime-skill.git ~/.openclaw/skills/italent-overtime
```

---

## 📋 用户安装流程

### 从 OpenClaw 仓库安装

```bash
# 自动安装（如果 OpenClaw 支持）
openclaw skills install italent-overtime
```

### 手动安装

```bash
# 1. 下载压缩包
cd ~/.openclaw/skills/
tar -xzvf italent-overtime-v1.1.0.tar.gz

# 2. 验证安装
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py help

# 3. 首次认证
python3 ~/.openclaw/skills/italent-overtime/scripts/italent-overtime-simple.py auth \
    --key 你的 AppKey --secret 你的 AppSecret --save
```

---

## 🔐 安全建议

### 1. 不要包含敏感信息

✅ 正确：
```json
{
  "auth_required": true,
  "auth_method": "oauth2_client_credentials"
}
```

❌ 错误：
```json
{
  "app_key": "实际的 Key",
  "app_secret": "实际的 Secret"
}
```

### 2. 用户自行认证

每个用户应该使用自己的 AppKey/AppSecret 认证，不要共享认证信息。

### 3. 说明权限需求

在文档中明确说明需要的权限：
- 加班管理权限
- 员工信息查询权限

---

## 📊 版本管理

### 语义化版本

遵循 [Semantic Versioning](https://semver.org/)：

- **MAJOR.MINOR.PATCH** (1.1.0)
- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

### 更新流程

```bash
# 1. 更新版本号
# 编辑 skill.json 和 publish.sh

# 2. 重新打包
bash publish.sh

# 3. 提交发布
git add .
git commit -m "Release v1.2.0"
git tag v1.2.0
git push --tags
```

---

## 🧪 测试清单

发布前验证：

- [ ] SKILL.md 格式正确
- [ ] skill.json 配置完整
- [ ] 主程序可以运行
- [ ] 所有命令帮助正常
- [ ] 认证功能正常
- [ ] 文档完整
- [ ] 压缩包可以正常解压
- [ ] 安装后可以使用

---

## 📞 技术支持

- **Skill 文档：** `SKILL.md`
- **API 文档：** `references/api-docs.md`
- **故障排查：** `references/troubleshooting.md`
- **作者：** 佳敏

---

## 📝 发布记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-03-30 | 初始版本 |
| v1.1.0 | 2026-03-31 | 支持认证，完善文档 |

---

**最后更新：** 2026-03-31  
**作者：** 佳敏
