# OpenClaw Web 管理界面

为 OpenClaw 多用户系统提供的可视化管理界面，支持子代理状态查看、用户配额管理和使用统计。

## 📁 文件位置

- **技能目录**: `~/.openclaw/skills/web-admin/`
- **工作区副本**: `~/.openclaw/workspace/web-admin/`

## 🚀 快速启动

### 方法 1：直接启动

```bash
cd ~/.openclaw/skills/web-admin
node server.js
```

### 方法 2：使用启动脚本

```bash
~/.openclaw/skills/web-admin/scripts/start.sh
```

### 方法 3：自定义端口

```bash
WEB_ADMIN_PORT=8080 node ~/.openclaw/skills/web-admin/server.js
```

## 🌐 访问界面

启动后，打开浏览器访问：**http://localhost:3456**

## ✨ 主要功能

### 1. 查看子代理状态

- 📊 总用户数统计
- 🟢 活跃子代理数量
- 💬 总消息数
- 🔢 总 Token 使用量
- 用户列表（ID、名称、状态、消息数、最后活跃时间）
- 实时刷新数据

### 2. 调整用户配额

- 💾 磁盘配额（MB）
- 🎫 Token 配额
- 📧 每日消息配额
- ⏱️ Session 超时时间
- 📈 可视化使用进度条

### 3. 查看使用统计

- 整体统计概览
- 单个用户详细使用情况
- 磁盘使用进度
- Token 使用进度
- 消息配额使用进度

### 4. 用户管理

- ➕ 创建新用户
- 🗑️ 删除用户
- ✏️ 修改配额
- 📝 操作日志记录

## 📋 使用示例

### 创建新用户

1. 点击右上角 "+ 新建用户" 按钮
2. 填写用户信息：
   - 用户 ID：`ou_xxxxxxxxxx`
   - 用户名：`张三`
   - 磁盘配额：`100` MB
   - Token 配额：`100000`
   - 每日消息配额：`1000`
3. 点击 "✅ 创建用户"

### 修改用户配额

1. 在右侧 "配额管理" 面板选择用户
2. 修改各项配额值
3. 查看使用情况图表
4. 点击 "💾 保存配额"

### 删除用户

1. 在用户列表中找到目标用户
2. 点击 "删除" 按钮
3. 确认删除操作

## 🔌 API 接口

### 获取数据
```bash
curl http://localhost:3456/api/data
```

### 更新配额
```bash
curl -X POST http://localhost:3456/api/quota \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "ou_xxx",
    "quota": {
      "diskQuotaMB": 200,
      "tokenQuota": 200000,
      "messageQuota": 2000,
      "sessionTimeoutHours": 48
    }
  }'
```

### 创建用户
```bash
curl -X POST http://localhost:3456/api/user \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "ou_new_user",
    "userName": "新用户",
    "quota": {
      "diskQuotaMB": 100,
      "tokenQuota": 100000,
      "messageQuota": 1000
    }
  }'
```

### 删除用户
```bash
curl -X DELETE http://localhost:3456/api/user \
  -H "Content-Type: application/json" \
  -d '{"userId": "ou_xxx"}'
```

### 健康检查
```bash
curl http://localhost:3456/api/health
```

## 🔧 集成到系统服务

### Systemd 服务

创建 `/etc/systemd/system/openclaw-web-admin.service`:

```ini
[Unit]
Description=OpenClaw Web Admin Server
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/.openclaw/skills/web-admin
ExecStart=/usr/bin/node server.js
Restart=always
Environment=WEB_ADMIN_PORT=3456

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-web-admin
sudo systemctl start openclaw-web-admin
```

### PM2 部署

```bash
npm install -g pm2
cd ~/.openclaw/skills/web-admin
pm2 start server.js --name openclaw-web-admin
pm2 startup
pm2 save
```

## 🔒 安全建议

⚠️ **重要**：当前版本默认无身份验证，仅限本地访问！

### 推荐配置：

1. **使用反向代理**（Nginx/Apache）
2. **配置 HTTPS**
3. **添加基本认证**
4. **限制访问 IP**
5. **不要暴露到公网**

详见 `SKILL.md` 中的安全配置示例。

## 📊 数据文件

Web 管理界面使用以下数据文件（与 multi-user-privacy 技能共享）：

- `~/.openclaw/skills/multi-user-privacy/.router-db.json` - 子代理路由数据
- `~/.openclaw/skills/multi-user-privacy/.quota-db.json` - 用户配额数据

## 🛠️ 故障排除

### 端口被占用
```bash
lsof -i :3456
WEB_ADMIN_PORT=8080 node server.js
```

### 无法访问数据
```bash
chmod 644 ~/.openclaw/skills/multi-user-privacy/.router-db.json
chmod 644 ~/.openclaw/skills/multi-user-privacy/.quota-db.json
```

### 查看日志
服务器运行日志会直接输出到终端。

## 📝 更新日志

### v1.0.0 (2026-03-12)
- ✨ 初始版本发布
- ✅ 子代理状态查看
- ✅ 用户配额管理
- ✅ 使用统计图表
- ✅ 实时数据刷新
- ✅ 用户创建/删除功能

## 📚 相关文档

- [SKILL.md](./SKILL.md) - 完整技能文档
- [multi-user-privacy](../multi-user-privacy/SKILL.md) - 多用户隐私保护系统

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**版本**: 1.0.0  
**创建日期**: 2026-03-12  
**作者**: OpenClaw Community
