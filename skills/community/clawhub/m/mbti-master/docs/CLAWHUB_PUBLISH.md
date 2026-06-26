# 发布到 ClawHub 官方市场

## 前提条件

1. 安装 ClawHub CLI
```bash
npm i -g clawhub
```

2. 注册/登录账号
```bash
clawhub login
```

3. 验证登录
```bash
clawhub whoami
```

## 准备你的 Skill

### 1. 确保符合规范

你的项目目录结构：
```
mbti-master/
├── SKILL.md              # 必须（包含metadata）
├── scripts/              # 可选
├── README.md             # 可选但推荐
└── LICENSE               # 可选但推荐
```

### 2. 检查 metadata

SKILL.md 头部必须包含：
```yaml
---
name: mbti-master
description: MBTI personality analysis tool with quick testing, cognitive function analysis, and compatibility matching. Use when users want to explore their personality type, understand 16 personalities, check compatibility with others, or play MBTI-related interactive games.
metadata:
  author: ShenJian
  version: 1.0.0
  license: MIT
---
```

### 3. 打包

```bash
cd /workspace/projects/workspace/skills/mbti-master

# 打包为 .skill 文件
tar -czf mbti-master.skill SKILL.md scripts/ README.md LICENSE
```

## 发布到 ClawHub

### 方法1：直接发布（推荐）

```bash
# 进入skill目录
cd /workspace/projects/workspace/skills/mbti-master

# 发布（会自动读取SKILL.md）
clawhub publish

# 或指定版本
clawhub publish --version 1.0.0
```

### 方法2：从GitHub发布

```bash
# 如果你的代码在GitHub
clawhub publish --from-github shven273-design/mbti-master
```

### 方法3：从本地文件发布

```bash
clawhub publish --file mbti-master.skill
```

## 发布后

### 验证发布

```bash
# 搜索你的skill
clawhub search "mbti"

# 应该能看到
# mbti-master - MBTI personality analysis tool...
```

### 其他用户安装

```bash
# 用户搜索
clawhub search mbti

# 用户安装
clawhub install mbti-master

# 或指定版本
clawhub install mbti-master --version 1.0.0
```

## 更新 Skill

```bash
# 修改代码后，更新版本号
cd mbti-master

# 编辑 SKILL.md，更新 version: 1.0.1

# 重新发布
clawhub publish --version 1.0.1
```

## 最佳实践

1. **版本号规范**：使用语义化版本（semver）
   - 1.0.0 - 初始版本
   - 1.0.1 - 修复bug
   - 1.1.0 - 新功能
   - 2.0.0 - 重大更新

2. **描述清晰**：SKILL.md 的 description 要详细说明用途

3. **文档完整**：提供 README.md 和示例

4. **测试充分**：确保在干净环境测试通过

## 故障排除

### 发布失败
```bash
# 检查skill格式
clawhub validate

# 查看详细错误
clawhub publish --verbose
```

### 搜索不到
- 发布可能有延迟，等待几分钟
- 检查是否登录正确账号
- 确认skill名称正确

### 权限问题
```bash
# 重新登录
clawhub logout
clawhub login
```

## 相关链接

- ClawHub: https://clawhub.com
- OpenClaw 文档: https://docs.openclaw.ai
- 你的项目: https://github.com/shven273-design/mbti-master