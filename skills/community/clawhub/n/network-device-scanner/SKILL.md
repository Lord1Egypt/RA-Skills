---
name: network-device-scanner
description: 扫描局域网内活跃设备及其开放端口，返回格式化Markdown表格。触发场景：(1) 用户说"查一下周边设备有哪些"、"扫描周边设备"、"看看网络有哪些设备"、"局域网有哪些设备" (2) 用户提到IP地址、MAC地址、端口扫描相关的查询
---

# Network Scanner

扫描当前局域网内的活跃设备及其开放端口，返回格式化表格。

**用途**：仅用于管理用户自有网络，发现和识别局域网内的设备。

## 执行方式

### Linux
```bash
python3 skills/network-device-scanner/scripts/scan.py
```

### macOS
```bash
python3 skills/network-device-scanner/scripts/scan.py
```

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File skills/network-device-scanner/scripts/scan.ps1
```

## 环境要求

- Python 3.7+
- 可选: `arp` 命令 (Linux/macOS), `fping` 或 `nmap` (更快发现)

## 输出格式

严格按照以下格式返回：

| IP 地址 | MAC | 开放端口 | 设备类型 |
|---------|-----|----------|----------|
| 172.16.10.1 | e4-68-a3-95-f9-16 | 21, 23, 80 | 小米路由器 (Telnet+FTP) |
| 172.16.10.24 | 94-e6-f7-be-c8-0a | 22, 80, 443, 3389, 8080, 8443, 9000 | Linux服务器 (SSH/RDP/Web) |
| 172.16.10.196 | 40-31-3c-db-06-7d | 80, 8080, 8443 | 小米设备 (智能电视/IoT) |
| 172.16.10.219 | 30-9c-23-07-1b-ea | 135, 139, 445 | Windows电脑 (SMB/远程管理) |

## 功能说明

1. **设备发现** (按优先级):
   - 读取 /proc/net/arp (Linux)
   - 使用 arp 命令
   - Ping 扫描 (fping > nmap > basic ping)
2. 使用TCP端口扫描验证设备活跃状态
3. 扫描常用端口: 21, 22, 23, 53, 80, 135, 139, 443, 445, 554, 8000, 8080, 8443, 9000, 37777
4. 根据MAC前缀和开放端口自动识别设备类型

## 设备类型识别规则

- MAC前缀 `e4-68-a3` → 小米路由器
- MAC前缀 `40-31-3c` → 小米设备
- 开放 135,139,445 端口 → Windows电脑
- 开放 22,80 端口 → Linux服务器
- 开放 80/8080 端口 → Web服务器/设备
