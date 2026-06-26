# 平台适配指南

本文档提供 AI Doc Generator 在各大 AI 平台的使用指南。

---

## 一、GitHub 开源

### 上传步骤

```bash
# 1. 初始化 Git（如果尚未初始化）
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "v2.0: 通用型文档生成工具"

# 4. 添加远程仓库
git remote add origin https://github.com/your-username/AI-Doc-Generator.git

# 5. 推送到 GitHub
git push -u origin main
```

### 项目亮点

- 纯 Python 实现，无依赖
- 支持 CLI 和模块调用
- 符合 GitHub 开源最佳实践

---

## 二、Claude 适配

### 方式一：直接对话使用

将 `app.py` 中的函数代码复制到 Claude 对话中，即可直接调用：

```python
# 复制以下函数到 Claude 对话中使用
from app import generate_changelog_from_input, generate_readme

# 生成 Changelog
result = generate_changelog_from_input(
    content="",
    old_version="v1.0.0",
    commits_text="feat: 新功能\nfix: 修复bug"
)
print(result["content"])
```

### 方式二：Claude Custom Tools 配置

创建 `claude-tools.json`：

```json
{
  "name": "ai_doc_generator",
  "description": "生成 README 和 Changelog 文档",
  "input_schema": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "enum": ["changelog", "readme"],
        "description": "生成类型"
      },
      "content": {
        "type": "string",
        "description": "更新内容或项目描述"
      },
      "old_version": {
        "type": "string",
        "description": "旧版本号（changelog时）"
      }
    },
    "required": ["command", "content"]
  }
}
```

### 方式三：Claude Code 本地工具

在项目目录运行：

```bash
# 让 Claude 直接调用本地 Python 脚本
claude --local
```

---

## 三、Hubble 适配

### 技能配置

创建 `hubble-skill.json`：

```json
{
  "name": "ai-doc-generator",
  "version": "2.0.0",
  "description": "一键生成专业 README 和 Changelog",
  "entry_point": "app.py",
  "commands": [
    {
      "name": "changelog",
      "description": "生成版本更新日志",
      "params": ["content", "old_version"]
    },
    {
      "name": "readme",
      "description": "生成项目说明文档",
      "params": ["project_name", "description", "features"]
    }
  ],
  "runtime": "python3",
  "install": {
    "type": "none",
    "dependencies": []
  }
}
```

### Hubble 发布步骤

1. 登录 Hubble 开发者平台
2. 创建新技能
3. 上传 `hubble-skill.json` 和 `app.py`
4. 配置触发词：「生成文档」「生成日志」
5. 测试发布

---

## 四、本地测试

### 运行测试

```bash
# 测试 Changelog 生成
python app.py changelog "feat: 新增登录功能\nfix: 修复bug" v1.0.0

# 测试 README 生成
python app.py readme "我的项目" "项目描述" "功能A|功能B"
```

### 预期输出

**Changelog:**
```
v1.1.0 (2026-04-02)

### 新增功能
- feat: 新增登录功能

### 问题修复
- fix: 修复bug
```

**README:**
```markdown
# 我的项目

项目描述

## 特性
- 功能A
- 功能B
...
```

---

## 五、后续迭代

### 添加新功能

1. 修改 `app.py` 添加新函数
2. 更新 `CHANGELOG.md`
3. 更新版本号
4. 提交并推送

### 版本发布

```bash
git tag v2.1.0
git push origin v2.1.0
```
