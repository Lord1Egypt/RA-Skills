---
name: l
description: Short alias skill for listing files, directories, processes, or system information. Use when you need to see what's present in a directory or system state.
---

# l（List 简写）

这是一个快速"列出" Skill，用字母 **l** 触发。让你随时查看文件、进程、网络状态等一切存在的项目。

---

## 适用场景

当你说：
- "查看当前目录文件"
- "列出所有文件"
- "显示运行中的进程"
- "有哪些端口在监听？"
- "列出安装的包"
- "show me what's here"

---

## 文件/目录列表

**基础ls**
```bash
ls                    # 简单列表
ls -l                 # 详细信息（权限、大小、时间）
ls -a                 # 显示隐藏文件
ls -lh                # 人类可读大小（KB/MB/GB）
ls -lt                # 按时间排序（最新在前）
ls -1                 # 每行一个（适合管道）
ls -ltr               # 按时间反向（最旧在前）
```

**高级选项**
```bash
ls -lAh               # 详细信息+隐藏+人类可读（不显示.和..）
ls -S                 # 按大小排序（最大在前）
ls -r                 # 反向排序
ls -X                 # 按扩展名排序
ls --color=auto       # 彩色输出（默认）
ls -F                 # 附加类型指示符（/目录 *可执行 @链接）
```

**tree（树状结构）**
```bash
tree                  # 显示目录树
tree -L 2             # 限制深度为2层
tree -a               # 显示隐藏文件
tree -d              # 只显示目录
tree -f               # 显示完整路径
tree -s              # 显示文件大小
```

**macOS/BSD兼容**
```bash
# macOS的ls默认不显示颜色，需要-G
ls -G                 # 彩色输出
ls -l@                # 显示扩展属性
ls -le                # 显示ACL权限
```

---

## Windows等效命令

```cmd
dir                   # 列表（简略）
dir /a                # 显示所有文件（含隐藏）
dir /q                # 显示所有者
dir /s                # 递归子目录
dir /b                # 仅文件名（简洁）
attrib                # 显示属性（只读、隐藏等）
tree /f               # 树状+文件
```

**PowerShell**
```powershell
ls                    # 等同于dir（Get-ChildItem）
ls -Force             # 显示隐藏
ls -Recurse          # 递归
ls -Directory        # 仅目录
ls -File             # 仅文件
gci -Recurse | ? {$_.Length -gt 1MB}  # 查找大文件
```

---

## 进程列表

**ps（详细信息）**
```bash
ps aux                # 所有进程详情（BSD风格）
ps -ef                # 所有进程详情（System V风格）
ps -eo pid,comm,%cpu,%mem  # 自定义字段
ps -u $USER           # 当前用户进程
ps -C node            # 按命令名过滤
ps -F                 # 完整格式（更多信息）
```

**top/htop（实时）**
```bash
top                   # 实时进程监控
htop                  # 增强版top（更友好）
top -u username       # 只看某用户
top -p 1234,5678     # 只看特定PID
```

**按资源排序**
```bash
ps aux --sort=-%mem   # 按内存降序
ps aux --sort=-%cpu   # 按CPU降序
ps -eo pid,comm,%mem,%cpu --sort=-%mem | head -10  # 前10内存大户
```

---

## 网络连接

**netstat（传统）**
```bash
netstat -tulpn        # 监听端口
netstat -an | grep :3000  # 查看特定端口
netstat -rn           # 路由表
netstat -i            # 接口统计
```

**ss（更快更现代）**
```bash
ss -tuln              # 所有监听端口
ss -p                 # 显示进程信息
ss -a state established  # 已建立连接
ss -m                 # 显示内存使用
ss -o state time-wait # 查看TIME_WAIT连接
```

**lsof（端口占用）**
```bash
lsof -i :3000         # 查看端口占用（进程）
lsof -iTCP -sTCP:LISTEN -n -P  # 监听端口（数字端口）
lsof -i4              # 仅IPv4
lsof -i6              # 仅IPv6
lsof -p 1234          # 查看进程打开文件
```

**netstat替代方案**
```bash
lsof -i -P -n | grep LISTEN  # 监听端口列表
ss -tulpn                      # 推荐，更快
```

---

## 其他列表

**内核模块**
```bash
lsmod                 # 加载的内核模块
modprobe -l           # 可用模块列表
```

**环境变量**
```bash
printenv              # 所有环境变量
env                   # 同上
set                   # 包含函数等（bash内置）
```

**路由表**
```bash
route -n              # Linux
netstat -rn           # macOS/Windows
ip route show         # 推荐
```

**防火墙规则**
```bash
iptables -L           # iptables规则
ufw status verbose    # ufw（Ubuntu）
firewall-cmd --list-all  # firewalld
pfctl -s rules        # macOS PF
```

---

## 格式化输出

**列对齐**
```bash
ls -l | column -t      # 列对齐
ps aux | column -t -x  # 横向排列
```

**分页查看**
```bash
ls -lR . | less        # 分页
ls -la | more          # 更简单的分页
```

**统计汇总**
```bash
ls | wc -l             # 文件总数
ls -l | grep '^-' | wc -l  # 普通文件数
ls -d */ | wc -l       # 目录数
```

**自定义格式**
```bash
# 只列出目录
ls -d */

# 只列出文件
ls -p | grep -v /

# 按扩展名分组
ls *.{js,ts,jsx,tsx} 2>/dev/null
```

---

## 跨平台差异摘要

| 功能 | Linux | macOS | Windows |
|------|-------|-------|---------|
| 文件列表 | ls -la | ls -la (需-G颜色) | dir /a |
| 递归列表 | ls -R | ls -R | dir /s |
| 进程列表 | ps aux | ps aux | tasklist |
| 端口占用 | lsof -i :PORT | lsof -i :PORT | netstat -ano |
| 树状结构 | tree | tree (需brew install) | tree /f |

---

> l 技能是最常用的工具。记住：ls -la 是你的好朋友，ps aux 是进程杀手锏，lsof -i 是端口侦探！
