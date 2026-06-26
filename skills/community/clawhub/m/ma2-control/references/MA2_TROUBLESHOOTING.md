# MA2 故障排查指南

## 控台连接问题

### 1. 超时错误
```
Command '['nc', '-w', '8', '192.168.1.110', '30001']' timed out
```

**原因**: 控台IP或端口错误

**排查**:
1. 确认控台IP地址
2. 确认Telnet端口 (通常是 30000)
3. 确认网络连通性: `ping 192.168.1.x`

### 2. 连接被拒绝
```
Connection refused
```

**原因**: 控台未开启Remote

**解决**:
1. 在控台 Settings → Network → Enable Remote
2. 设置正确的端口 (默认 30000)

### 3. 桥接服务未运行
```
Error: no ma2_bridge server found
```

**解决**:
```bash
python3 ~/ma2_bridge/ma2_telnet_server.py
```

---

## 命令执行问题

### 1. 命令不生效
- 确认命令格式正确
- 确认控台处于可接收状态

### 2. 选灯失败
- 确认灯具已Patch
- 检查Fixture ID是否正确

### 3. 存Cue失败
- 确认编程器有内容
- 检查Executor是否被占用

---

## 网络配置

### 检查本机IP和控台是否同网段
```bash
ifconfig | grep 192.168
```

### 测试Telnet连通
```bash
nc -zv 192.168.1.1 30000
```

---

## 常用诊断命令

```bash
# 检查桥接服务
curl http://127.0.0.1:40100/health

# 查看控台状态
~/ma2_bridge/ma2_cmd.sh "Status"

# 查看所有灯具
~/ma2_bridge/ma2_cmd.sh "List Fixture"
```
