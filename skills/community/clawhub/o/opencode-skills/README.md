# Opencode 技能 - 使用指南

## 🎯 技能概述

这个技能提供了完整的 opencode 自动化能力，可以帮助您：

- 🚀 快速创建网站和网页
- 📊 分析项目结构和内容
- 🛠️ 运行自动化任务
- 📁 管理文件（复制、压缩、解压）
- 🌐 启动本地预览服务器
- 🔍 生成项目报告

---

## 📖 使用方法

### 1. 基本使用

**触发方式：**
- 直接提及 "opencode" 
- 请求创建网站/网页
- 需要分析项目时
- 需要运行 opencode 任务时

**示例请求：**
```
"帮我创建一个科技公司官网"
"分析这个项目的结构"
"启动 opencode 服务器"
"运行 opencode 任务创建网站"
```

---

### 2. 核心功能

#### 启动 opencode 服务器

```bash
# Web 界面
opencode web --port 4096 --hostname 127.0.0.1

# 后台服务
opencode serve --port 4096

# ACP 模式
opencode acp --port 4096
```

#### 运行 opencode 任务

```bash
# 直接运行
opencode run "任务描述..."

# 等待完成
opencode run --wait "任务描述..."

# 查看输出
opencode run --output "任务描述..."
```

#### 连接到运行的服务器

```bash
# 基本连接
opencode attach http://127.0.0.1:4096

# 指定端口
opencode attach http://localhost:8080
```

---

### 3. 常用任务

#### 创建网站

```bash
opencode run "
创建一个科技公司官网，包含：
- 导航栏 + Hero 区域
- 公司简介 + 核心服务
- 产品展示 + 技术优势
- 客户案例 + 团队介绍
- 新闻动态 + 联系我们
- 科技感配色，响应式设计

保存到：/home/linshui/.openclaw/workspace/project-name
"
```

#### 分析项目

```bash
# 查看文件数量
find /path/to/project -type f | wc -l

# 查看项目大小
du -sh /path/to/project

# 查看文件类型
find /path/to/project -type f | xargs file | sort | uniq -c | sort -rn
```

#### 预览项目

```bash
# 启动本地服务器
python3 -m http.server 8000 -d /path/to/project

# 在浏览器中打开
# http://127.0.0.1:8000
```

---

### 4. 文件操作

#### 复制文件

```bash
# 复制整个项目
cp -r /source/project /destination/project

# 复制特定文件
cp /source/file.txt /destination/
```

#### 压缩/解压

```bash
# 压缩项目
tar -czf /path/to/project.tar.gz /path/to/project

# 解压文件
tar -xzf /path/to/archive.tar.gz

# 查看压缩包内容
tar -tzf /path/to/archive.tar.gz
```

#### 创建压缩包

```bash
# 创建 zip 压缩包
cd /path/to/project
zip -r ../project.zip .

# 压缩特定文件
cd /path/to/project
zip -r ../files.zip *.html *.css *.js
```

---

### 5. 项目报告

#### 生成详细报告

```bash
# 项目统计
echo "========================================"
echo "项目名称：$(basename "$PROJECT_DIR")"
echo "创建时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""
echo "📁 项目统计:"
echo "  - 文件数量：$(find "$PROJECT_DIR" -type f | wc -l)"
echo "  - 目录数量：$(find "$PROJECT_DIR" -type d | wc -l)"
echo "  - 项目大小：$(du -sh "$PROJECT_DIR" | cut -f1)"
echo ""
echo "📊 文件类型分布:"
find "$PROJECT_DIR" -type f | xargs file | sort | uniq -c | sort -rn | head -10
```

---

### 6. 监控进程

```bash
# 查看 opencode 进程
ps aux | grep opencode | grep -v grep

# 监控进程状态
watch -n 5 'ps aux | grep opencode | grep -v grep'
```

---

## 📋 配置文件

### 位置

```bash
# 主配置文件
~/.config/opencode/config.json

# 环境变量文件
~/.config/opencode/environment
```

### 示例配置

```bash
# 查看当前配置
cat ~/.config/opencode/config.json

# 编辑配置
nano ~/.config/opencode/config.json
```

---

## 🎨 配色方案

Opencode 提供了丰富的配色方案：

### 默认主题
```css
--primary: #0a1628;        /* 深蓝 - 主色 */
--primary-light: #132238;  /* 浅蓝 - 辅助色 */
--accent: #00d4ff;         /* 科技蓝 - 强调色 */
--accent-secondary: #7c3aed; /* 紫色 - 渐变色 */
```

### 自定义主题

在项目中创建 `theme.json` 文件：

```json
{
  "name": "科技蓝",
  "colors": {
    "--primary": "#0a1628",
    "--accent": "#00d4ff",
    "--text-primary": "#ffffff"
  },
  "fonts": {
    "--font-main": "Inter, Noto Sans SC, sans-serif"
  }
}
```

---

## 📊 性能监控

### 查看资源使用情况

```bash
# 内存使用
free -h

# CPU 使用
top -bn1 | head -20

# 磁盘使用
df -h

# 网络使用
netstat -an | grep LISTEN
```

### 监控 opencode 性能

```bash
# 查看 opencode 进程
ps -o pid,ppid,%cpu,%mem,command -C opencode

# 查看 opencode 日志
tail -f ~/.local/share/opencode/log/opencode.log
```

---

## 🔧 故障排除

### 常见问题

#### 问题 1：端口被占用

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

#### 问题 2：权限拒绝

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

#### 问题 3：网络连接问题

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

---

## 📚 参考资源

### 官方文档
- [Opencode 官方文档](https://opencode.ai/docs)
- [Opencode GitHub](https://github.com/opencode)
- [Opencode 社区论坛](https://forum.opencode.ai)

### 相关技能
- **web_search** - 搜索 opencode 相关资源
- **coding-agent** - 生成 opencode 脚本
- **browser** - 在浏览器中查看 opencode 生成的内容
- **exec** - 执行 opencode 命令

---

## 🎯 最佳实践

1. **使用固定端口** - 配置固定的端口号，避免冲突
2. **定期清理缓存** - 定期清理 opencode 的缓存文件
3. **监控资源使用** - 定期检查 opencode 的资源使用情况
4. **使用配置文件** - 将常用配置保存到配置文件中
5. **记录操作日志** - 记录重要的 opencode 操作

---

**版本**: 1.0.0  
**最后更新**: 2026-03-17  
**作者**: linshui
