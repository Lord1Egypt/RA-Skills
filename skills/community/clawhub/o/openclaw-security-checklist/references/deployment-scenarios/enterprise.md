# 企业部署检查清单

**适用场景**: 中大型企业生产环境部署 OpenClaw

## 架构要求

### 高可用架构

```
                    ┌─────────────┐
                    │  负载均衡器  │
                    │ (ALB/SLB)   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
    │  Gateway  │   │  Gateway  │   │  Gateway  │
    │  Node 1   │   │  Node 2   │   │  Node 3   │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                    ┌──────▼──────┐
                    │  共享存储    │
                    │ (Redis/DB)  │
                    └─────────────┘
```

### 最小部署规模

| 组件 | 数量 | 配置 | 用途 |
|------|------|------|------|
| 负载均衡器 | 2 | 主备 | 流量分发 |
| Gateway | 3+ | 4 核 8GB | API 网关 |
| Node | 3+ | 8 核 16GB | AI 推理 |
| Redis | 3 | 主从 + 哨兵 | 会话存储 |
| 数据库 | 2 | 主从 | 配置存储 |

## 安全检查项

### 1. 身份认证

- [ ] **集成企业 SSO/LDAP**
  ```yaml
  # config.yaml
  auth:
    provider: ldap
    ldap:
      url: ldap://ad.company.com:389
      base_dn: dc=company,dc=com
      bind_dn: cn=openclaw,ou=services,dc=company,dc=com
      bind_password: ${LDAP_BIND_PASSWORD}
      user_filter: (sAMAccountName={{username}})
      group_filter: (memberOf=cn=openclaw-users,ou=groups,dc=company,dc=com)
  ```

- [ ] **配置多因素认证（MFA）**
  ```yaml
  auth:
    mfa:
      enabled: true
      provider: totp  # 或 duosecurity, okta
      grace_period: 30s
  ```

- [ ] **实施 RBAC 权限模型**
  ```yaml
  rbac:
    roles:
      - name: admin
        permissions: ["*"]
      - name: developer
        permissions: ["model:read", "model:write", "session:read"]
      - name: viewer
        permissions: ["session:read"]
    
    role_assignments:
      - role: admin
        groups: ["openclaw-admins"]
      - role: developer
        groups: ["openclaw-devs"]
  ```

- [ ] **配置会话管理**
  ```yaml
  session:
    timeout: 3600  # 1 小时
    max_concurrent: 5
    secure_cookies: true
    same_site: strict
  ```

### 2. 网络安全

- [ ] **部署在 VPC 私有子网**
  ```
  网络架构：
  - 公有子网：负载均衡器
  - 私有子网：Gateway、Node
  - 数据库子网：Redis、DB（无公网访问）
  
  NAT Gateway: 用于出站访问（API 调用）
  ```

- [ ] **配置网络安全组/ACL**
  ```
  安全组规则：
  
  Gateway SG:
  - 入站：443/tcp from ALB SG
  - 出站：7002/tcp to Node SG
  
  Node SG:
  - 入站：7002/tcp from Gateway SG
  - 出站：443/tcp to API endpoints
  
  Database SG:
  - 入站：6379/tcp from Gateway SG (Redis)
  - 入站：5432/tcp from Gateway SG (PostgreSQL)
  - 无出站规则
  ```

- [ ] **启用 WAF（Web 应用防火墙）**
  ```
  防护规则：
  - SQL 注入防护
  - XSS 防护
  - 请求频率限制（1000 次/分钟/IP）
  - 地理位置限制（如仅限中国大陆）
  - 自定义规则（阻止特定 User-Agent）
  ```

- [ ] **配置 TLS/SSL**
  ```bash
  # 使用 Let's Encrypt 或企业 CA
  certbot certonly --webroot -w /var/www/html \
    -d openclaw.company.com \
    --agree-tos --email admin@company.com
  
  # 配置证书自动续期
  echo "0 0 1 * * certbot renew --quiet" | crontab -
  ```

### 3. 数据安全

- [ ] **启用数据加密（传输中）**
  ```yaml
  # 强制 HTTPS
  server:
    ssl:
      enabled: true
      cert: /etc/ssl/certs/openclaw.crt
      key: /etc/ssl/private/openclaw.key
      min_version: "TLS1.2"
  
  # HSTS
  headers:
    Strict-Transport-Security: "max-age=31536000; includeSubDomains"
  ```

- [ ] **启用数据加密（静态）**
  ```yaml
  # 数据库加密
  database:
    encryption:
      enabled: true
      key_provider: aws_kms  # 或 azure_key_vault, hashicorp_vault
  
  # 文件存储加密
  storage:
    encryption:
      enabled: true
      algorithm: AES-256-GCM
  ```

- [ ] **实施数据脱敏**
  ```yaml
  # 敏感数据脱敏规则
  data_masking:
    enabled: true
    rules:
      - field: "user.email"
        pattern: "^(.){1}(.*)@(.*)$"
        replacement: "$1***@$3"
      - field: "user.phone"
        pattern: "^(\\d{3})\\d{4}(\\d{4})$"
        replacement: "$1****$2"
      - field: "api_key"
        pattern: "^(.{8}).*(.{4})$"
        replacement: "$1...$2"
  ```

- [ ] **配置数据保留策略**
  ```yaml
  retention:
    conversation_logs: 90d  # 对话日志保留 90 天
    audit_logs: 365d        # 审计日志保留 1 年
    metrics: 30d            # 指标数据保留 30 天
    backup: 365d            # 备份保留 1 年
  ```

### 4. 审计和合规

- [ ] **启用详细审计日志**
  ```yaml
  audit:
    enabled: true
    events:
      - authentication.success
      - authentication.failure
      - authorization.deny
      - config.change
      - user.create
      - user.delete
      - api_key.use
    output:
      - file:/var/log/openclaw/audit.log
      - syslog:udp://siem.company.com:514
  ```

- [ ] **配置 SIEM 集成**
  ```yaml
  # Splunk 集成
  splunk:
    hec_url: https://splunk.company.com:8088
    token: ${SPLUNK_HEC_TOKEN}
    index: openclaw
    source: openclaw
  
  # 或 ELK Stack
  elk:
    elasticsearch:
      hosts: ["https://es.company.com:9200"]
      username: openclaw
      password: ${ES_PASSWORD}
    index_pattern: "openclaw-*"
  ```

- [ ] **实施变更管理**
  ```
  变更流程：
  1. 提交变更申请（Jira/ServiceNow）
  2. 安全团队审批
  3. 在测试环境验证
  4. 变更窗口执行（维护时间）
  5. 变更后验证
  6. 更新配置管理数据库（CMDB）
  ```

- [ ] **定期合规审计**
  ```
  审计频率：
  - 每日：自动安全扫描
  - 每周：日志审查
  - 每月：配置基线检查
  - 每季度：渗透测试
  - 每年：等保测评/外部审计
  ```

### 5. 监控告警

- [ ] **配置应用性能监控（APM）**
  ```yaml
  apm:
    provider: datadog  # 或 newrelic, dynatrace
    service_name: openclaw
    environment: production
    trace_sampling_rate: 0.1
    log_injection: true
  ```

- [ ] **定义关键指标**
  ```yaml
  metrics:
    availability:
      - name: api_uptime
        threshold: 99.9%
        window: 30d
    performance:
      - name: api_latency_p99
        threshold: 500ms
        window: 5m
      - name: error_rate
        threshold: 0.1%
        window: 5m
    capacity:
      - name: cpu_usage
        threshold: 70%
        window: 15m
      - name: memory_usage
        threshold: 80%
        window: 15m
  ```

- [ ] **配置多级告警**
  ```yaml
  alerts:
    - name: HighErrorRate
      condition: error_rate > 1%
      severity: P1
      channels: [pagerduty, slack, sms]
    
    - name: HighLatency
      condition: latency_p99 > 1000ms
      severity: P2
      channels: [slack, email]
    
    - name: DiskSpaceLow
      condition: disk_usage > 85%
      severity: P3
      channels: [email]
  ```

- [ ] **建立值班制度**
  ```
  值班安排：
  - P1 告警：5 分钟内响应，15 分钟内处理
  - P2 告警：30 分钟内响应，1 小时内处理
  - P3 告警：4 小时内响应，24 小时内处理
  
  工具：
  - PagerDuty/OpsGenie：告警路由
  - 钉钉/企业微信：通知
  - 电话：P1 告警升级
  ```

### 6. 灾备和恢复

- [ ] **配置多可用区部署**
  ```
  部署架构：
  - 可用区 A：Gateway × 2, Node × 2
  - 可用区 B：Gateway × 1, Node × 1
  - 跨可用区负载均衡
  - 数据库主从跨可用区
  ```

- [ ] **制定 RTO/RPO 目标**
  ```
  恢复目标：
  - RTO（恢复时间目标）: 4 小时
  - RPO（恢复点目标）: 15 分钟
  
  实现方式：
  - 数据库：主从复制 + 延迟备库
  - 文件存储：跨区域复制
  - 配置：Git 版本控制 + 自动化部署
  ```

- [ ] **定期灾备演练**
  ```
  演练计划：
  - 每月：数据库故障切换演练
  - 每季度：完整灾备演练（含业务验证）
  - 每年：跨区域灾难恢复演练
  
  演练内容：
  1. 模拟主可用区故障
  2. 切换到备可用区
  3. 验证业务功能
  4. 切换回主可用区
  5. 总结改进
  ```

- [ ] **配置自动备份**
  ```yaml
  backup:
    schedule: "0 2 * * *"  # 每天凌晨 2 点
    retention: 365d
    destinations:
      - type: s3
        bucket: openclaw-backup
        region: cn-north-1
        encryption: AES256
      - type: local
        path: /backup/openclaw
    pre_backup:
      - "pg_dump -U openclaw > /tmp/db.sql"
    post_backup:
      - "rm -f /tmp/db.sql"
  ```

### 7. DevSecOps

- [ ] **实施 CI/CD 安全扫描**
  ```yaml
  # .gitlab-ci.yml 示例
  stages:
    - security
    - test
    - deploy
  
  security_scan:
    stage: security
    script:
      - trivy fs --exit-code 1 .
      - git-secrets --scan
      - npm audit --audit-level=high
  ```

- [ ] **配置基础设施即代码（IaC）**
  ```
  工具选择：
  - Terraform：云资源编排
  - Ansible：配置管理
  - Helm:Kubernetes 部署
  
  安全要求：
  - 所有代码版本控制（Git）
  - Code Review 必须
  - 自动化测试
  - 审批后合并
  ```

- [ ] **实施蓝绿部署/金丝雀发布**
  ```yaml
  # Kubernetes 金丝雀发布
  apiVersion: argoproj.io/v1alpha1
  kind: Rollout
  spec:
    strategy:
      canary:
        steps:
        - setWeight: 10
        - pause: {duration: 10m}
        - setWeight: 50
        - pause: {duration: 30m}
        - setWeight: 100
  ```

## 合规认证

### 等保 2.0（中国）

| 等级 | 适用场景 | 要求 |
|------|----------|------|
| 二级 | 中小企业内部系统 | 基础安全保护 |
| 三级 | 重要信息系统 | 强制要求，年费 8-15 万 |
| 四级 | 关键信息基础设施 | 金融、电信等 |

### ISO 27001

- [ ] 建立信息安全管理体系（ISMS）
- [ ] 实施风险评估和处理
- [ ] 定期内部审核和管理评审
- [ ] 外部认证审计

### SOC 2

- [ ] 安全性（Security）
- [ ] 可用性（Availability）
- [ ] 处理完整性（Processing Integrity）
- [ ] 保密性（Confidentiality）
- [ ] 隐私性（Privacy）

## 检查清单汇总

### 部署前

- [ ] 完成架构设计和安全评审
- [ ] 配置 SSO/LDAP 集成
- [ ] 准备 TLS 证书
- [ ] 配置监控和告警
- [ ] 制定灾备方案
- [ ] 完成渗透测试

### 部署中

- [ ] 按照 IaC 脚本部署
- [ ] 验证安全组规则
- [ ] 测试故障切换
- [ ] 验证备份恢复
- [ ] 配置日志收集

### 部署后

- [ ] 基线安全扫描
- [ ] 性能压力测试
- [ ] 更新 CMDB
- [ ] 培训运维团队
- [ ] 制定值班计划

## 资源链接

- 等保 2.0 标准：https://www.djbh.net/
- ISO 27001 实施指南：https://www.iso.org/isoiec-27001-information-security.html
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks

## 更新记录

- 2026-03-15: 初始版本
