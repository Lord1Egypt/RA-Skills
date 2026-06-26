---
name: opencode

---

# Opencode 自动化技能

## 关于 Opencode 技能

Opencode 是一个强大的 AI 工作流引擎，可以帮助您：

- 🚀 **快速创建网站和网页** - 从概念到成品，一键生成
- 📊 **分析项目** - 查看项目结构、文件内容、统计信息
- 🛠️ **运行脚本和任务** - 执行自动化任务
- 📁 **文件管理** - 创建、复制、移动、删除文件
- 🌐 **Web 服务器管理** - 启动本地服务器预览项目
- 📝 **代码生成** - 生成各种类型的代码文件
- 🔍 **项目分析** - 分析项目状态、依赖关系

### 使用场景

**当您需要：**

1. **快速创建网站/网页** - "帮我创建一个电商网站"、"生成一个个人博客"、"设计一个公司官网"

2. **分析现有项目** - "查看这个项目的结构"、"分析这个文件夹的内容"、"统计项目文件"

3. **运行自动化任务** - "执行这个项目的所有测试"、"运行 linting 检查"

4. **文件操作** - "复制这些文件到另一个位置"、"压缩这个项目"、"提取项目中的图片"

5. **启动预览服务器** - "我想在浏览器中查看这个网站"、"启动本地服务器"

6. **代码生成** - "生成一个 REST API"、"创建数据库模型"、"编写单元测试"

7. **项目分析** - "这个项目使用了哪些技术？"、"分析项目的依赖关系"

### 核心功能

#### 1. 启动 opencode 服务器

```bash
# 启动 Web 界面
opencode web --port 4096 --hostname 127.0.0.1

# 启动后台服务
opencode serve --port 4096

# 启动 ACP 服务器
opencode acp --port 4096
```

#### 2. 运行 opencode 任务

```bash
# 直接运行任务
opencode run "任务描述..."

# 运行并等待完成
opencode run --wait "任务描述..."

# 运行并查看输出
opencode run --output "任务描述..."
```

#### 3. 连接到 opencode 服务器

```bash
# 连接到正在运行的服务器
opencode attach http://127.0.0.1:4096

# 使用不同的端口
opencode attach http://localhost:8080
```

#### 4. 分析项目

```bash
# 查看项目结构
tree -L 2 /path/to/project

# 统计项目大小
du -sh /path/to/project

# 查看文件列表
find /path/to/project -type f -name "*.py" | wc -l

# 查看 Git 状态
cd /path/to/project && git status

# 查看依赖
cd /path/to/project && npm list  # 或 yarn list / pip list
```

#### 5. 文件操作

```bash
# 复制文件
cp -r /source /destination

# 压缩项目
tar -czf /path/to/project.tar.gz /path/to/project

# 创建压缩包
cd /path/to/project && zip -r ../project.zip .

# 提取压缩包
tar -xzf /path/to/archive.tar.gz

# 查看文件内容
cat /path/to/file
head -100 /path/to/file
tail -50 /path/to/file

# 搜索文件
grep -r "pattern" /path/to/project

# 查找特定类型的文件
find /path/to/project -type f -name "*.html"
```

#### 6. 启动预览服务器

```bash
# Python HTTP 服务器
python3 -m http.server 8000 -d /path/to/project

# 使用不同的端口
python3 -m http.server 3000 -d /path/to/project

# Node.js 静态文件服务器
npx http-server -p 8080 -c-1 /path/to/project

# 使用 Python 的内置模块
python3 -m http.server 8000 --bind 127.0.0.1
```

### 工作流程

#### 创建网站/网页的工作流

```
1. 定义需求 → 2. 启动 opencode → 3. 输入任务 → 4. 等待生成 → 5. 查看结果
```

**示例：**
```
opencode run "创建一个科技公司官网，包含导航栏、Hero 区域、公司简介、核心服务、产品展示、技术优势、客户案例、团队介绍、新闻动态、联系我们。科技感配色，响应式设计。保存到 /home/linshui/.openclaw/workspace/project-name"
```

#### 分析项目的工作流

```
1. 选择项目 → 2. 查看结构 → 3. 分析内容 → 4. 生成报告
```

**示例：**
```
# 查看项目结构
find /path/to/project -type f | head -50

# 分析技术栈
# 查看 package.json / requirements.txt / go.mod 等

# 统计代码行数
wc -l /path/to/project/**/*.py
```

#### 预览项目的工作流

```
1. 选择项目 → 2. 启动服务器 → 3. 打开浏览器 → 4. 查看效果
```

**示例：**
```
# 启动服务器
python3 -m http.server 8000 -d /path/to/project

# 在浏览器中打开
# http://127.0.0.1:8000
```

### 常用命令速查表

| 命令 | 说明 | 示例 |
|------|------|------|
| `opencode run` | 运行任务 | `opencode run "创建网站"` |
| `opencode web` | 启动 Web 界面 | `opencode web --port 4096` |
| `opencode serve` | 启动后台服务 | `opencode serve --port 4096` |
| `opencode attach` | 连接到服务器 | `opencode attach http://localhost:4096` |
| `opencode acp` | 启动 ACP 服务器 | `opencode acp --port 4096` |
| `opencode models` | 查看模型列表 | `opencode models` |
| `opencode stats` | 查看使用统计 | `opencode stats --days 7` |
| `opencode export` | 导出会话 | `opencode export <session_id>` |
| `opencode import` | 导入会话 | `opencode import file.json` |

### 注意事项

1. **端口占用** - 确保使用的端口没有被其他程序占用
2. **权限** - 某些操作可能需要 sudo 权限
3. **网络** - opencode 可能需要网络连接来下载模型
4. **存储** - 确保有足够的磁盘空间用于缓存和临时文件

### 系统集成

该技能可以与 OpenClaw 的其他技能配合使用：

- **web_search** - 搜索 opencode 相关资源
- **coding-agent** - 生成 opencode 脚本
- **browser** - 在浏览器中查看 opencode 生成的内容
- **exec** - 执行 opencode 命令

---

**版本**: 1.0.0
**最后更新**: 2026-03-17
**作者**: linshui
