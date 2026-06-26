# 合规性检查

## 支持的标准

| 标准 | 说明 |
|------|------|
| **等保 2.0** | 中国网络安全等级保护 2.0 |
| **GDPR** | 欧盟通用数据保护条例 |
| **ISO 27001** | 信息安全管理体系 |
| **SOC 2** | 服务组织控制 2.0 |

## 等保 2.0 检查项（第三级）

### 访问控制

| 检查项 | 要求 | 检查方法 |
|--------|------|---------|
| 用户身份鉴别 | 密码复杂度 ≥ 8位，含大小写+数字+特殊字符 | `GET /users` 检查密码策略 |
| 匿名访问 | 禁止匿名拉取私有镜像 | 项目 `public=false` |
| 会话超时 | 无操作 30 分钟后登出 | 检查系统配置 |
| 多因素认证 | 管理员必须开启 MFA | `GET /users/{id}` |

### 安全审计

| 检查项 | 要求 | 检查方法 |
|--------|------|---------|
| 操作日志 | 记录所有操作，保留 ≥ 6 个月 | `GET /audit-logs` |
| 日志完整性 | 防止篡改 | 审计日志存储在独立系统 |
| 异常行为 | 记录暴力破解等异常 | 日志分析 |

### 镜像安全

| 检查项 | 要求 | 检查方法 |
|--------|------|---------|
| 漏洞扫描 | 所有生产镜像必须扫描 | `GET /projects/{id}/scanAll` |
| 高危漏洞 | 禁止拉取 CRITICAL/HIGH 漏洞镜像 | 项目设置 `prevent_vulnerable_images=true` |
| 镜像签名 | 重要镜像必须签名验证 | 检查 Notary 服务状态 |
| 扫描覆盖率 | 生产项目覆盖率 ≥ 95% | 扫描报告统计 |

### 网络安全

| 检查项 | 要求 | 检查方法 |
|--------|------|---------|
| HTTPS | 强制 HTTPS，禁用 HTTP | `GET /system/configurations` |
| TLS 版本 | TLS ≥ 1.2 | nginx/proxy 配置 |
| 外部访问 | 仅允许白名单 IP | Harbor 认证代理配置 |

### 数据安全

| 检查项 | 要求 | 检查方法 |
|--------|------|---------|
| 存储加密 | 镜像数据加密存储 | 存储后端配置 |
| 备份 | 定期备份，异地保存 | 备份日志检查 |
| 密钥管理 | Robot Token 定期轮换 | `GET /robots` 检查过期时间 |

## GDPR 检查项

| 检查项 | 要求 |
|--------|------|
| 数据最小化 | 只保留必要的数据 |
| 删除权 | 支持彻底删除镜像和关联数据 |
| 数据保留 | 审计日志保留期限符合当地法律 |
| 第三方共享 | 复制到第三方时的数据保护协议 |

## 合规检查脚本

```python
# scripts/compliance_check.py 核心逻辑

STANDARDS = {
    "等保2级": [
        CheckItem("禁止匿名拉取", "public", False,
                  "GET /projects", lambda p: p.get('metadata', {}).get('public') == 'false'),
        CheckItem("强制扫描", "auto_scan", True,
                  "GET /projects/{id}", lambda p: p.get('metadata', {}).get('auto_scan') == 'true'),
        CheckItem("阻止高危漏洞镜像", "prevent_vulnerable", True,
                  "GET /projects/{id}", lambda p: p.get('metadata', {}).get('prevent_vulnerable_images') == 'true'),
        CheckItem("HTTPS强制", "https", True,
                  "GET /system/configurations", lambda c: c.get('httpauth') == ''),
        CheckItem("Robot账号未过期", "robot_expires", True,
                  "GET /projects/{id}/robots", lambda r: r.get('expires_at', 0) > now),
        CheckItem("管理员开启MFA", "admin_mfa", True,
                  "GET /users?page_size=1", lambda u: u[0].get('mfa_enabled')),
        CheckItem("备份已配置", "backup", True,
                  "shell: ls /data/harbor-backup/*.sql.gz | head -1"),
    ],
    "GDPR": [
        CheckItem("删除权-支持彻底删除", "delete_gc", True,
                  "GET /system/gc", lambda g: len(g) > 0),
        CheckItem("审计日志保留>=30天", "log_retention", True,
                  "GET /audit-logs?page_size=1", lambda l: check_date_range(l)),
    ]
}
```

## 合规报告格式

```html
<!-- 合规报告 HTML 模板 -->
<!DOCTYPE html>
<html>
<head>
  <title>Harbor 合规检查报告</title>
  <style>
    .pass { color: green; }
    .fail { color: red; }
    .warn { color: orange; }
  </style>
</head>
<body>
  <h1>Harbor 合规检查报告</h1>
  <p>检查时间: {{timestamp}}</p>
  <p>标准: {{standard}}</p>
  <p>整体评分: {{score}}/100</p>

  <h2>详细结果</h2>
  <table>
    <tr><th>检查项</th><th>状态</th><th>说明</th></tr>
    {% for item in results %}
    <tr class="{{item.status}}">
      <td>{{item.name}}</td>
      <td>{{item.status}}</td>
      <td>{{item.detail}}</td>
    </tr>
    {% endfor %}
  </table>
</body>
</html>
```

## 整改优先级

| 优先级 | 问题类型 | 建议修复时间 |
|--------|---------|------------|
| 🔴 紧急 | 未开启 HTTPS / 匿名拉取开放 | 24 小时内 |
| 🟠 高 | 未启用漏洞扫描 / Robot 未设过期 | 7 天内 |
| 🟡 中 | 备份未配置 / MFA 未开启 | 30 天内 |
| 🟢 低 | 日志保留时长配置 | 90 天内 |
