# OpenClaw 一键部署技能包

OpenClaw 三种标准部署方案的完整自动化部署脚本，包含环境检测、防火墙配置、服务部署、开机自启等功能。

## 三种部署方案

### 方案一：云端网关 + Tailscale + SSH 隧道控制本地

**适用场景：** 个人开发者，追求简单，云端 24 小时在线

```
通讯软件 → 云端网关 (18789) ← SSH 隧道 ← 本地编辑器
                ↓
            AI 模型 API
```

**部署命令：**

```bash
# 云端（Linux）
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/openclaw-deploy/main/plan1-cloud-gateway.sh
bash plan1-cloud-gateway.sh

# 本地（Windows PowerShell）
.\plan1-local-tunnel.ps1
```

---

### 方案二：云端网关 + Tailscale + 本地节点

**适用场景：** 需要本地独立运行，同时利用云端通道

```
通讯软件 → 云端网关 (Remote 模式) ← WebSocket ← 本地节点
                ↓
            AI 模型 API
```

**部署命令：**

```bash
# 云端（Linux）
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/openclaw-deploy/main/plan2-cloud-remote-gateway.sh
bash plan2-cloud-remote-gateway.sh

# 本地（Windows PowerShell）
.\plan2-local-node.ps1 -CloudIP "<YOUR_CLOUD_IP>" -Token "your-token"
```

---

### 方案三：云端网关 + 本地网关双部署

**适用场景：** 需要完全独立的两套系统，数据隔离，同步备份

```
通讯软件 → 云端网关 ←───同步───→ 本地网关
    ↓                               ↓
AI 模型 API                      AI 模型 API
```

**部署命令：**

```bash
# 云端（Linux）
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/openclaw-deploy/main/plan3-cloud-gateway.sh
bash plan3-cloud-gateway.sh

# 本地（Windows PowerShell）
.\plan3-local-gateway.ps1 -CloudIP "<YOUR_CLOUD_IP>"
```

---

## 快速开始

### 前置要求

1. **Tailscale 账号**：两端使用同一账号
2. **Node.js 18+**：自动安装
3. **管理员/root 权限**：用于防火墙和服务配置

### 一键部署

```bash
# Linux 云端服务器
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/openclaw-deploy/main/diagnostic.sh
chmod +x diagnostic.sh
bash diagnostic.sh  # 先运行诊断

# 选择方案部署
bash plan1-cloud-gateway.sh  # 方案一
bash plan2-cloud-remote-gateway.sh  # 方案二
bash plan3-cloud-gateway.sh  # 方案三
```

```powershell
# Windows 本地电脑
.\plan1-local-tunnel.ps1   # 方案一
.\plan2-local-node.ps1     # 方案二
.\plan3-local-gateway.ps1  # 方案三
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 完整技能文档（含详细架构图） |
| `plan1-cloud-gateway.sh` | 方案一云端网关脚本 |
| `plan1-local-tunnel.ps1` | 方案一本地 SSH 隧道脚本 |
| `plan2-cloud-remote-gateway.sh` | 方案二云端远程网关脚本 |
| `plan2-local-node.ps1` | 方案二本地节点脚本 |
| `plan3-cloud-gateway.sh` | 方案三云端网关脚本 |
| `plan3-local-gateway.ps1` | 方案三本地网关脚本 |
| `diagnostic.sh` | 通用诊断脚本 |

---

## 故障排查

### 运行诊断脚本

```bash
bash diagnostic.sh
```

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 端口不通 | 检查防火墙和云安全组 |
| Tailscale 断开 | `tailscale up --force` |
| 服务无法启动 | 查看 `journalctl -u openclaw-gateway -f` |

---

## License

MIT
