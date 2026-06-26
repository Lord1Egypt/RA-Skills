# Opencode 使用指南

## 目录

- [快速开始](#快速开始)
- [基本命令](#基本命令)
- [高级功能](#高级功能)
- [常见任务](#常见任务)
- [故障排除](#故障排除)

---

## 快速开始

### 1. 检查 opencode 是否已安装

```bash
opencode --version
```

**输出示例：**
```
1.2.27
```

### 2. 启动 opencode Web 服务器

```bash
opencode web --port 4096 --hostname 127.0.0.1
```

**输出示例：**
```
[93m[1m!  OPENCODE_SERVER_PASSWORD is not set; server is unsecured.
[94m[1m  Web interface:     [0m http://127.0.0.1:4096/
```

### 3. 运行 opencode 任务

```bash
opencode run "任务描述..."
```

**示例：**
```bash
opencode run "创建一个科技公司官网"
```

---

## 基本命令

### 启动服务器

#### Web 界面模式
```bash
# 基本用法
opencode web

# 指定端口
opencode web --port 4096

# 指定主机
opencode web --hostname 127.0.0.1

# 完整示例
opencode web --port 4096 --hostname 127.0.0.1 --mdns
```

#### 后台服务模式
```bash
# 启动后台服务
opencode serve

# 指定端口
opencode serve --port 4096

# 完整示例
opencode serve --port 4096 --hostname 127.0.0.1
```

#### ACP 模式
```bash
# 启动 ACP 服务器
opencode acp

# 指定端口
opencode acp --port 4096

# 完整示例
opencode acp --port 4096 --hostname 127.0.0.1
```

### 运行任务

#### 直接运行
```bash
opencode run "任务描述..."
```

#### 等待完成
```bash
opencode run --wait "任务描述..."
```

#### 查看输出
```bash
opencode run --output "任务描述..."
```

#### 查看帮助
```bash
opencode run --help
```

---

## 高级功能

### 连接到运行的服务器

```bash
# 基本连接
opencode attach http://127.0.0.1:4096

# 使用不同的端口
opencode attach http://localhost:8080

# 连接到远程服务器
opencode attach http://192.168.1.100:4096
```

### 查看模型列表

```bash
# 查看所有可用模型
opencode models

# 查看特定提供商的模型
opencode models anthropic

# 刷新模型列表
opencode models --refresh

# 查看详细输出
opencode models --verbose
```

### 查看使用统计

```bash
# 查看所有时间的使用统计
opencode stats

# 查看最近 7 天的统计
opencode stats --days 7

# 查看特定项目的统计
opencode stats --project /path/to/project

# 查看工具使用情况
opencode stats --tools

# 查看模型使用分布
opencode stats --models
```

### 导出和导入会话

#### 导出会话
```bash
# 导出当前会话
opencode export

# 导出指定会话
opencode export <session_id>

# 导出为 JSON 格式
opencode export --format json <session_id>

# 导出为 Markdown 格式
opencode export --format markdown <session_id>
```

#### 导入会话
```bash
# 从文件导入
opencode import session.json

# 从 URL 导入
opencode import https://opncd.ai/s/abc123

# 导入并继续会话
opencode import --continue session.json
```

---

## 常见任务

### 任务 1：创建网站

#### 步骤 1：定义需求

```bash
opencode run "
创建一个科技公司官网，包含：
- 导航栏 + Hero 区域
- 公司简介 + 核心服务（6 项）
- 产品展示（4 款产品）
- 技术优势（4 项）
- 客户案例（3 个）
- 团队介绍（4 人）
- 新闻动态（3 条）
- 联系我们（表单 + 信息）
- 底部页脚

设计特点：
- 深蓝科技配色 + 渐变强调色
- 动态网格背景 + 发光效果
- 滚动动画（reveal effect）
- 响应式设计（适配移动端）
- 悬停交互效果

保存到：/home/linshui/.openclaw/workspace/linshui-tech
"
```

#### 步骤 2：查看生成的文件

```bash
# 列出文件
ls -la /home/linshui/.openclaw/workspace/linshui-tech/

# 查看文件大小
du -sh /home/linshui/.openclaw/workspace/linshui-tech/

# 查看文件内容
head -100 /home/linshui/.openclaw/workspace/linshui-tech/index.html
```

#### 步骤 3：预览网站

```bash
# 启动本地服务器
python3 -m http.server 8000 -d /home/linshui/.openclaw/workspace/linshui-tech

# 在浏览器中打开
# http://127.0.0.1:8000
```

### 任务 2：分析项目

#### 步骤 1：查看项目结构

```bash
# 查看项目树
find /path/to/project -type f | head -50

# 统计文件数量
find /path/to/project -type f | wc -l

# 查看项目大小
du -sh /path/to/project
```

#### 步骤 2：分析技术栈

```bash
# 查看 package.json
if [ -f /path/to/project/package.json ]; then
    cat /path/to/project/package.json
fi

# 查看 requirements.txt
if [ -f /path/to/project/requirements.txt ]; then
    cat /path/to/project/requirements.txt
fi

# 查看 go.mod
if [ -f /path/to/project/go.mod ]; then
    cat /path/to/project/go.mod
fi
```

#### 步骤 3：生成项目报告

```bash
# 统计代码行数
wc -l /path/to/project/**/*.py

# 查找特定模式的文件
grep -r "import.*opencode" /path/to/project

# 查找特定类型的文件
find /path/to/project -type f -name "*.html" -o -name "*.css" -o -name "*.js"
```

### 任务 3：文件操作

#### 复制文件

```bash
# 复制整个项目
cp -r /source/project /destination/project

# 复制特定文件
cp /source/file.txt /destination/

# 复制特定类型的文件
cp /source/*.html /destination/
```

#### 压缩项目

```bash
# 创建 tar.gz 压缩包
cd /path/to/project

# 查看文件大小
ls -lh

# 压缩项目
tar -czf /path/to/project.tar.gz /path/to/project

# 压缩特定文件
tar -czf /path/to/files.tar.gz /path/to/file1.txt /path/to/file2.txt
```

#### 解压文件

```bash
# 解压 tar.gz 文件
tar -xzf /path/to/project.tar.gz

# 解压到指定目录
tar -xzf /path/to/project.tar.gz -C /destination/

# 查看压缩包内容
tar -tzf /path/to/project.tar.gz
```

#### 创建压缩包

```bash
# 使用 zip 压缩
cd /path/to/project
zip -r ../project.zip .

# 压缩到指定位置
zip -r /path/to/project.zip /path/to/project

# 压缩特定文件
cd /path/to/project
zip -r ../project_files.zip *.html *.css *.js
```

### 任务 4：预览项目

#### 方法 1：使用 Python HTTP 服务器

```bash
# 基本用法
python3 -m http.server 8000 -d /path/to/project

# 指定主机
python3 -m http.server 8000 --bind 127.0.0.1 -d /path/to/project

# 使用不同的端口
python3 -m http.server 3000 -d /path/to/project
```

#### 方法 2：使用 Node.js 静态文件服务器

```bash
# 使用 npx
npx http-server -p 8080 -c-1 /path/to/project

# 使用 nodemon
npx nodemon --open /path/to/project/index.html
```

#### 方法 3：使用 Python 的内置模块

```bash
# 使用内置模块
python3 -m http.server 8000

# 使用开发服务器（需要安装 flask）
flask run --host 127.0.0.1 --port 8000
```

---

## 故障排除

### 问题 1：端口被占用

**错误信息：**
```
Failed to start server on port 4096
```

**解决方案：**

```bash
# 查看占用端口的进程
lsof -i :4096

# 杀死占用端口的进程
kill -9 <PID>

# 使用其他端口
opencode web --port 8080
```

### 问题 2：权限拒绝

**错误信息：**
```
Permission denied
```

**解决方案：**

```bash
# 查看文件权限
ls -la /path/to/file

# 修改文件权限
chmod 755 /path/to/directory
chmod 644 /path/to/file

# 修改文件所有者
sudo chown -R $USER:$USER /path/to/directory
```

### 问题 3：网络连接问题

**错误信息：**
```
Connection refused
```

**解决方案：**

```bash
# 检查防火墙
sudo ufw status

# 允许 opencode 通过防火墙
sudo ufw allow 4096/tcp

# 检查路由
ping 127.0.0.1
```

### 问题 4：磁盘空间不足

**解决方案：**

```bash
# 检查磁盘空间
df -h

# 清理临时文件
rm -rf /tmp/*

# 清理 opencode 缓存
rm -rf ~/.local/share/opencode/cache/*
```

### 问题 5：内存不足

**解决方案：**

```bash
# 检查内存使用情况
free -h

# 限制 opencode 的内存使用
export OPENCODE_MAX_MEMORY=4096

# 重启 opencode 服务
pkill -f "opencode serve"
opencode serve --port 4096
```

---

## 性能优化

### 1. 使用缓存

```bash
# 启用缓存
export OPENCODE_CACHE=1

# 设置缓存大小
export OPENCODE_CACHE_SIZE=1024
```

### 2. 使用多线程

```bash
# 使用多线程处理
opencode run --threads 4 "任务描述..."
```

### 3. 优化网络请求

```bash
# 使用代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

---

## 安全提示

1. **不要在生产环境使用 opencode** - 仅在开发环境使用

2. **保护 API 密钥** - 不要将 API 密钥提交到版本控制系统

3. **限制访问** - 使用防火墙限制 opencode 的访问

4. **定期清理缓存** - 定期清理 opencode 的缓存文件

5. **监控资源使用** - 定期检查 opencode 的资源使用情况

---

## 参考资源

- [Opencode 官方文档](https://opencode.ai/docs)
- [Opencode GitHub](https://github.com/opencode)
- [Opencode 社区论坛](https://forum.opencode.ai)
- [Opencode 用户指南](https://opencode.ai/docs/user-guide)

---

**版本**: 1.0.0
**最后更新**: 2026-03-17
