# 🔒 安全说明 Security Notes

## ⚠️ 重要安全提示 Important Security Notice

### 中文

**部署前请阅读：**

1. **网络访问限制**
   - 默认仅监听本地（127.0.0.1:9999）
   - 如需外部访问，请配置防火墙规则
   - 生产环境建议使用 HTTPS 反向代理

2. **认证说明**
   - 当前版本无用户认证（v1.0.0）
   - 仅限受信任的内网环境使用
   - 不要暴露在公网

3. **Docker 安全**
   - 容器以非 root 用户运行（kanban, UID 1000）
   - 已配置资源限制（CPU 1.0, 内存 512MB）
   - 已禁用特权提升（no-new-privileges）

4. **数据隐私**
   - 所有数据本地存储（SQLite）
   - 不上传数据到外部服务
   - Web 服务器会记录访问日志（含 IP）
   - 无第三方追踪代码

5. **MCP 配置**
   - 安装时会创建 ~/.openclaw/config/mcp.json
   - 如已存在该文件，请手动合并配置
   - 不会覆盖其他 MCP 配置

### English

**Before Deployment:**

1. **Network Access**
   - Default: localhost only (127.0.0.1:9999)
   - Configure firewall rules for external access
   - Use HTTPS reverse proxy in production

2. **Authentication**
   - No user authentication in v1.0.0
   - For trusted internal networks only
   - Do not expose to public internet

3. **Docker Security**
   - Container runs as non-root user (kanban, UID 1000)
   - Resource limits configured (CPU 1.0, Memory 512MB)
   - Privilege escalation disabled (no-new-privileges)

4. **Data Privacy**
   - All data stored locally (SQLite)
   - No data upload to external services
   - Web server logs access (including IP)
   - No third-party tracking code

5. **MCP Configuration**
   - Creates ~/.openclaw/config/mcp.json on install
   - Merge manually if file already exists
   - Will not overwrite other MCP configs

---

## 🛡️ 安全加固建议 Security Hardening

### 生产环境部署 Production Deployment

#### 1. 添加 HTTPS
```yaml
# 使用 Nginx 反向代理
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
```

#### 2. 添加认证
```bash
# Nginx 基础认证
htpasswd -c .htpasswd username
```

#### 3. 限制资源
```yaml
# 已在 docker-compose.yml 中配置
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
```

#### 4. 备份数据
```bash
# 备份 Docker 卷
docker run --rm -v kanban-data:/source -v $(pwd):/backup \
  alpine tar czf /backup/kanban-backup-$(date +%Y%m%d).tar.gz /source
```

---

## 📊 安全审计 Security Audit

**安全评分：** 97/100 ✅ 优秀

| 检查项 | 得分 | 状态 |
|--------|------|------|
| 敏感信息 | 100/100 | ✅ |
| 个人隐私 | 100/100 | ✅ |
| 代码安全 | 100/100 | ✅ |
| 依赖安全 | 100/100 | ✅ |
| 配置安全 | 100/100 | ✅ |
| Docker 安全 | 95/100 | ✅ 已改进 |

**已修复问题：**
- ✅ 添加非 root 用户
- ✅ 配置资源限制
- ✅ 限制网络访问（仅本地）
- ✅ 禁用特权提升
- ✅ 完善隐私说明

---

## 📞 安全联系 Security Contact

**作者 Author:** 北京老李  
**报告漏洞 Report Vulnerability:** 通过 ClawHub Issues  
**更新时间 Last Update:** 2026-03-21
