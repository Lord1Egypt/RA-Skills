# PinchTab 安全模型

## 本地运行

PinchTab 完全在本地运行：
- 不联系外部服务
- 不发送遥测数据
- 不外泄数据

## 风险

PinchTab 控制真实的 Chrome 实例，存在以下风险：

1. **配置文件访问** - 如果指向包含已保存登录信息的配置文件，代理可以访问认证网站
2. **API 暴露** - 如果暴露到公网 without 认证，任何人都可以控制你的浏览器
3. **恶意网站** - 代理可能访问恶意网站，导致 XSS 或其他攻击

## 最佳实践

### 1. 使用专用配置文件

```bash
# 创建新的空配置文件
BRIDGE_PROFILE=~/.pinchtab/automation-profile pinchtab &
```

**不要**使用你的日常 Chrome 配置文件。

### 2. 设置认证令牌

```bash
# 暴露 API 时始终设置令牌
BRIDGE_TOKEN="your-strong-secret-token" pinchtab &
```

### 3. 绑定到本地

```bash
# 默认绑定到 127.0.0.1（仅本地访问）
BRIDGE_BIND=127.0.0.1 pinchtab &
```

**不要**暴露到 `0.0.0.0` 除非必要。

### 4. 防火墙规则

如果必须暴露到网络：

```bash
# 仅允许特定 IP
ufw allow from 192.168.1.100 to any port 9867
```

### 5. 阻止图片

节省带宽并减少攻击面：

```bash
BRIDGE_BLOCK_IMAGES=true pinchtab &
```

## 检查清单

- [ ] 使用专用空配置文件
- [ ] 设置 `BRIDGE_TOKEN`
- [ ] 绑定到 `127.0.0.1`
- [ ] 不使用日常 Chrome 配置文件
- [ ] 定期清理配置文件数据
- [ ] 监控 API 访问日志

## 事件响应

如果怀疑安全事件：

1. 停止 PinchTab：`pkill pinchtab`
2. 删除配置文件：`rm -rf ~/.pinchtab/automation-profile`
3. 更改所有可能泄露的密码
4. 检查浏览器扩展和保存的密码
