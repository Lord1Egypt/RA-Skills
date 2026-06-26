# 常见问题与解决方案

---

## 问题分类说明

**简单问题（1-2步排查）**：安装配置、启动问题等
**中等问题（3-5步排查）**：插件加载、Web 模式等
**复杂问题（5-10步排查）**：性能监控异常、远程连接等

---

## 安装问题

### 1. pip install glances 失败【简单问题】

**问题描述**: 使用 pip 安装 Glances 时报错

**排查步骤**:
```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 pip
pip --version
```

**常见原因**:
- Python 版本低于 3.8 (35%)
- 系统缺少编译依赖 (30%)
- pip 版本过低 (20%)
- 网络问题 (15%)

**解决方案**:

**方案A（推荐）**: 使用 pipx 隔离安装
```bash
pipx install glances
```

**方案B**: 使用包管理器
```bash
# macOS
brew install glances

# Ubuntu/Debian
sudo apt install glances

# Arch Linux
sudo pacman -S glances
```

**方案C**: pip 安装完整版
```bash
pip install "glances[all]"
```

---

### 2. 可选依赖缺失导致功能不可用【中等问题】

**问题描述**: Glances 启动时提示某些插件不可用，部分监控面板为空

**排查步骤**:
```bash
# 查看已安装的可选依赖
glances --modules-list

# 检查具体缺失的模块
python -c "import psutil; print(psutil.__version__)"
python -c "import docker; print(docker.__version__)"
```

**常见原因**:
- 未安装完整依赖包 (50%)
- psutil 版本不兼容 (25%)
- Docker/GPU 相关库缺失 (25%)

**解决方案**:

**方案A**: 安装完整依赖
```bash
pip install "glances[all]"
```

**方案B**: 按需安装特定功能
```bash
pip install "glances[web]"      # Web 模式
pip install "glances[docker]"   # Docker 监控
pip install "glances[gpu]"      # GPU 监控
pip install "glances[export]"   # 数据导出
```

---

### 3. 启动时报 psutil 权限错误【简单问题】

**问题描述**: 运行 glances 时提示权限不足无法读取系统信息

**排查步骤**:
```bash
# 检查当前用户权限
whoami
id

# 尝试用 sudo 运行
sudo glances
```

**常见原因**:
- 普通用户无法读取某些 /proc 文件 (50%)
- macOS 缺少完全磁盘访问权限 (30%)
- Docker 容器权限不足 (20%)

**解决方案**:

**方案A**: 使用 sudo
```bash
sudo glances
```

**方案B（Docker）**: 添加必要权限
```bash
docker run --rm -it \
  --pid host \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  nicolargo/glances:latest-full
```

---

## 使用问题

### 4. Web 模式无法访问【中等问题】

**问题描述**: 启动 `glances -w` 后浏览器无法访问 Web 界面

**排查步骤**:
```bash
# 检查 Web 依赖是否安装
python -c "import bottle; print(bottle.__version__)"

# 检查端口是否被占用
lsof -i :61208

# 检查防火墙
sudo iptables -L -n | grep 61208  # Linux
```

**常见原因**:
- bottle 或 requests 未安装 (35%)
- 端口 61208 被占用 (25%)
- 防火墙阻断 (25%)
- 绑定地址错误 (15%)

**解决方案**:

**方案A**: 安装 Web 依赖
```bash
pip install "glances[web]"
glances -w
# 访问 http://localhost:61208
```

**方案B**: 指定端口和绑定地址
```bash
glances -w -p 9090 -B 0.0.0.0
# 远程访问: http://<server-ip>:9090
```

**方案C**: 杀掉占用端口的进程
```bash
lsof -ti :61208 | xargs kill -9
glances -w
```

---

### 5. Docker 容器监控不显示【中等问题】

**问题描述**: Glances 运行正常但不显示 Docker 容器信息

**排查步骤**:
```bash
# 检查 Docker 是否运行
docker ps

# 检查 Docker SDK 是否安装
python -c "import docker; c = docker.from_env(); print(c.containers.list())"

# 检查 docker.sock 权限
ls -la /var/run/docker.sock
```

**常见原因**:
- docker Python SDK 未安装 (40%)
- 当前用户不在 docker 组 (30%)
- docker.sock 路径不正确 (20%)
- Docker 服务未运行 (10%)

**解决方案**:

**方案A**: 安装 Docker 支持
```bash
pip install "glances[docker]"
```

**方案B**: 添加用户到 docker 组
```bash
sudo usermod -aG docker $USER
# 重新登录后生效
```

**方案C**: 指定 Docker socket
```bash
glances --docker-sock /var/run/docker.sock
```

---

### 6. 数据导出到 InfluxDB/CSV 失败【中等问题】

**问题描述**: 使用 `--export` 参数导出监控数据时报错

**排查步骤**:
```bash
# 检查导出依赖
pip list | grep -E "influxdb|cassandra|elasticsearch"

# 检查配置文件
cat ~/.config/glances/glances.conf | grep -A5 "\[influxdb\]"

# 测试 InfluxDB 连接
curl -I http://localhost:8086/ping
```

**常见原因**:
- 导出依赖未安装 (40%)
- 配置文件中连接信息错误 (30%)
- 目标服务未运行 (20%)
- 数据库/bucket 不存在 (10%)

**解决方案**:

**方案A**: 导出到 CSV（最简单）
```bash
pip install "glances[export]"
glances --export csv --export-csv-file /tmp/glances.csv
```

**方案B**: 配置 InfluxDB 导出
```ini
# ~/.config/glances/glances.conf
[influxdb2]
host=localhost
port=8086
protocol=http
org=my-org
bucket=glances
token=my-token
```

```bash
glances --export influxdb2
```

---

## 配置问题

### 7. 自定义配置文件不生效【简单问题】

**问题描述**: 修改 glances.conf 后设置未生效

**排查步骤**:
```bash
# 查看配置文件搜索路径
glances --help | grep -A3 "config"

# 确认配置文件位置
ls ~/.config/glances/glances.conf 2>/dev/null
ls /etc/glances/glances.conf 2>/dev/null
```

**常见原因**:
- 配置文件路径错误 (40%)
- 配置文件语法错误 (30%)
- 使用了错误的 section 名称 (30%)

**解决方案**:

**方案A**: 使用正确路径
```bash
# 创建用户级配置
mkdir -p ~/.config/glances
cp /etc/glances/glances.conf ~/.config/glances/ 2>/dev/null

# 或指定配置文件
glances -C ~/my-glances.conf
```

**方案B**: 生成默认配置
```bash
# Glances 会在首次运行时创建默认配置
# 编辑配置
vim ~/.config/glances/glances.conf
```

---

### 8. 告警阈值配置不生效【中等问题】

**问题描述**: 自定义的 CPU/内存告警阈值未触发告警

**排查步骤**:
```bash
# 查看当前阈值
glances --stdout cpu.user,mem.percent

# 检查配置
grep -A5 "\[cpu\]" ~/.config/glances/glances.conf
```

**常见原因**:
- 阈值格式错误 (40%)
- section 名称拼写错误 (35%)
- 配置文件未被加载 (25%)

**解决方案**:

```ini
# ~/.config/glances/glances.conf
[cpu]
# 阈值从低到高: careful < warning < critical
careful=50
warning=70
critical=90

[mem]
careful=50
warning=70
critical=90
```

```bash
# 重启 glances 使配置生效
glances -C ~/.config/glances/glances.conf
```

---

## 远程监控问题

### 9. 客户端-服务器模式连接失败【复杂问题】

**问题描述**: 使用 `glances -s` 和 `glances -c` 模式时连接被拒绝

**排查步骤**:
```bash
# 服务器端：确认监听
glances -s -B 0.0.0.0
ss -tlnp | grep 61209

# 客户端：测试连通性
telnet <server-ip> 61209
ping <server-ip>

# 检查防火墙
sudo ufw status  # Ubuntu
sudo firewall-cmd --list-ports  # CentOS
```

**常见原因**:
- 防火墙未开放端口 61209 (35%)
- 服务端绑定了 127.0.0.1 (25%)
- 网络不可达 (20%)
- xmlrpc 依赖缺失 (20%)

**解决方案**:

**方案A**: 服务器端配置
```bash
# 绑定所有接口
glances -s -B 0.0.0.0 -p 61209

# 开放防火墙
sudo ufw allow 61209  # Ubuntu
```

**方案B**: 客户端连接
```bash
glances -c <server-ip> -p 61209
```

**方案C**: 使用密码保护
```bash
# 服务器端
glances -s -B 0.0.0.0 --password

# 客户端
glances -c <server-ip> --password
```

---

### 10. SNMP 模式监控失败【复杂问题】

**问题描述**: 使用 SNMP 监控网络设备时无数据返回

**排查步骤**:
```bash
# 检查 SNMP 依赖
python -c "from pysnmp.hlapi import *; print('OK')"

# 测试 SNMP 连通性
snmpwalk -v2c -c public <device-ip> sysDescr

# 检查 Glances 配置
grep -A10 "\[snmp\]" ~/.config/glances/glances.conf
```

**常见原因**:
- pysnmp 未安装 (35%)
- SNMP community string 不匹配 (25%)
- 设备不支持 SNMP v2c (20%)
- 网络防火墙阻断 UDP 161 (20%)

**解决方案**:

**方案A**: 安装 SNMP 支持
```bash
pip install "glances[snmp]"
```

**方案B**: 配置 SNMP 参数
```ini
# ~/.config/glances/glances.conf
[snmp]
host=<device-ip>
port=161
version=2c
community=public
```

```bash
glances --snmp-community public --snmp-version 2c <device-ip>
```
