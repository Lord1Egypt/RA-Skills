---
name: mihomo-proxy
description: 管理 mihomo (Clash Meta) 代理服务。当用户需要配置、更新、重启代理、切换节点、更新订阅或排查代理连接问题时使用。适用于已有 mihomo 二进制和配置的 Linux 服务器。
---

# Mihomo 代理管理

## 环境信息（首次使用请根据实际修改）

- **二进制**: `/opt/mihomo`（或实际路径）
- **配置目录**: `/opt/mihomo-config/`
- **配置文件**: `config.yaml`
- **服务管理**: systemd (`systemctl start/stop/restart/status mihomo`)
- **混合代理端口**: `7890` (HTTP + SOCKS5)
- **API 控制台**: `127.0.0.1:9090`

## 常用操作

### 测试代理连通性

```bash
curl -s --max-time 10 -x http://127.0.0.1:7890 https://httpbin.org/ip
```

### 验证配置

```bash
/opt/mihomo -d /opt/mihomo-config -t
```

### 重载配置

```bash
systemctl restart mihomo
```

### 查看状态

```bash
systemctl status mihomo
journalctl -u mihomo -n 50 --no-pager
```

## 节点管理（通过 API）

### 查看所有代理节点

```bash
curl -s http://127.0.0.1:9090/proxies
```

### 查看某个组

```bash
curl -s http://127.0.0.1:9090/proxies/PROXY
```

### 切换节点

```bash
curl -X PUT http://127.0.0.1:9090/proxies/PROXY -d '{"name": "节点名"}'
```

## 更新订阅

当用户提供新的订阅链接时：

1. 下载订阅内容：
   ```bash
   curl -sL '<订阅URL>' -o /tmp/sub_raw.txt
   ```

2. 运行配置生成脚本（如已配置）：
   ```bash
   node scripts/gen_config.js
   ```
   脚本会自动解析节点并生成配置。如无脚本，需手动将订阅转换为 mihomo 配置。

3. 验证配置：
   ```bash
   /opt/mihomo -d /opt/mihomo-config -t
   ```

4. 重启服务：
   ```bash
   systemctl restart mihomo
   ```

5. 测试连通性

## 支持的协议

- **vless** (reality + xtls-rprx-vision)
- **hysteria2** (含 salamander obfs)
- **trojan** (含 ws + tls)
- **ss** (shadowsocks)
- **vmess**

## 配置结构参考

```yaml
proxies:          # 节点列表
proxy-groups:     # 按地区/用途分组
  - PROXY         # 总出口组（手动选择/自动测速）
  - 地区子组      # 按地区分类
rules:            # 分流规则
  - 常见国内域名 → DIRECT
  - 特定地区域名 → 对应节点
  - 其他国外域名 → PROXY
  - 兜底 → DIRECT
```

## 注意事项

- mihomo 运行在 systemd 下，不要用 nohup 手动启动
- 修改配置后先验证（`-t`）再重启
- trojan ws 节点如果 Host 为空会导致配置验证失败
- 订阅内容可能是无换行的 base64，需先解码处理

## 首次部署（供新用户参考）

1. 下载 mihomo 二进制放到 `/opt/mihomo`
2. 创建配置目录 `/opt/mihomo-config/` 并放入 `config.yaml`
3. 创建 systemd service 文件（参考 mihomo 官方文档）
4. `systemctl enable --now mihomo`
5. 验证：`curl -x http://127.0.0.1:7890 https://httpbin.org/ip`
