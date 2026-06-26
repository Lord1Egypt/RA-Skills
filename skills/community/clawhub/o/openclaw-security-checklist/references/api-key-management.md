# API 密钥管理规范

**目标**: 防止 API 密钥泄露、滥用和未授权访问

## 密钥存储最佳实践

### ✅ 推荐方式

#### 1. 环境变量（首选）

```bash
# ~/.zshrc 或 ~/.bashrc
export OPENCLAW_API_KEY="sk-..."
export DASHSCOPE_API_KEY="sk-..."

# 使用后重新加载
source ~/.zshrc
```

**优点**:
- 不会提交到版本控制
- 进程隔离，不同用户不可见
- 易于轮换（修改后重启服务）

**检查命令**:
```bash
# 确认环境变量已设置
echo $OPENCLAW_API_KEY

# 检查是否泄露到历史命令
grep -i "api_key\|sk-" ~/.zsh_history
```

#### 2. 加密的 .env 文件

```bash
# 创建 .env 文件
cat > ~/.openclaw/.env << EOF
OPENCLAW_API_KEY=sk-...
DASHSCOPE_API_KEY=sk-...
EOF

# 设置严格权限
chmod 600 ~/.openclaw/.env
```

**权限检查**:
```bash
# 查看权限（应为 600 或 400）
stat -c %a ~/.openclaw/.env  # Linux
stat -f %A ~/.openclaw/.env  # macOS

# 修复权限
chmod 600 ~/.openclaw/.env
```

#### 3. 密钥管理服务（企业级）

| 服务 | 适用场景 | 集成方式 |
|------|----------|----------|
| AWS Secrets Manager | AWS 部署 | SDK 自动拉取 |
| Azure Key Vault | Azure 部署 | Managed Identity |
| HashiCorp Vault | 自建/混合云 | API 集成 |
| 1Password CLI | 个人/小团队 | `op read` 命令 |

### ❌ 禁止方式

#### 1. 硬编码到代码/配置

```javascript
// ❌ 错误示例
const apiKey = "sk-1234567890abcdef";

// ✅ 正确示例
const apiKey = process.env.OPENCLAW_API_KEY;
```

**检测命令**:
```bash
# 扫描代码库中的硬编码密钥
grep -rn "sk-[a-zA-Z0-9]\{20,\}" ~/.openclaw/workspace/
grep -rn "api_key.*=.*['\"][a-zA-Z0-9]" ~/.openclaw/workspace/
grep -rn "Bearer [a-zA-Z0-9]" ~/.openclaw/workspace/
```

#### 2. 提交到版本控制

```bash
# .gitignore 必须包含
.env
*.key
*.secret
config.local.json
```

**检查是否已泄露**:
```bash
# 查看 git 历史中是否有敏感文件
git log --all --full-history -- "*.key" "*.secret" ".env"

# 如已泄露，立即轮换密钥并清理历史
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

#### 3. 明文日志输出

```javascript
// ❌ 错误示例
console.log("Using API key:", apiKey);

// ✅ 正确示例
console.log("Using API key:", apiKey.substring(0, 8) + "...");
```

## 密钥轮换策略

### 轮换周期

| 密钥类型 | 建议周期 | 触发条件 |
|----------|----------|----------|
| 生产环境 API 密钥 | 90 天 | 定期轮换 |
| 开发/测试密钥 | 180 天 | 人员离职/项目结束 |
| 疑似泄露密钥 | 立即 | 检测到异常使用 |
| 管理员密钥 | 30-60 天 | 高权限，缩短周期 |

### 轮换流程

```bash
# 1. 生成新密钥（在对应平台操作）
# MiniMax: https://platform.minimaxi.com/user-center/api-key
# Aliyun: https://ram.console.aliyun.com/manage/ak

# 2. 更新环境变量
export OPENCLAW_API_KEY="sk-new-key-here"

# 3. 重启服务
openclaw gateway restart

# 4. 验证新密钥
openclaw status

# 5. 禁用旧密钥（在平台操作）
# 等待 24-48 小时确认无异常后删除
```

### 自动化轮换（高级）

```bash
#!/bin/bash
# scripts/rotate-api-key.sh

KEY_NAME="openclaw-api-key"
NEW_KEY=$(aliyun ram CreateAccessKey --UserName openclaw-service | jq -r '.AccessKey.AccessKeyId')

# 更新环境变量
echo "export OPENCLAW_API_KEY=$NEW_KEY" >> ~/.zshrc

# 通知服务重载
systemctl restart openclaw-gateway

# 禁用旧密钥（记录日志）
echo "$(date): Rotated API key to $NEW_KEY" >> /var/log/key-rotation.log
```

## 访问控制

### 最小权限原则

**RAM 策略示例**（阿里云）:

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bss:DescribeAccountBalance",
        "dashscope:GenerateText"
      ],
      "Resource": "*"
    }
  ]
}
```

**避免使用**:
- ❌ `AdministratorAccess`（完全管理权限）
- ❌ `AliyunOSSFullAccess`（除非确实需要）

### 密钥隔离

| 环境 | 密钥 | 用途 |
|------|------|------|
| 生产 | `PROD_API_KEY` | 正式服务 |
| 开发 | `DEV_API_KEY` | 本地调试 |
| 测试 | `TEST_API_KEY` | CI/CD 测试 |
| 监控 | `MONITOR_API_KEY` | 健康检查（只读权限） |

## 监控和告警

### 异常检测指标

- **使用量突增**: 日调用量 > 3 倍平均值
- **地理位置异常**: 来自未授权国家/地区
- **时间异常**: 非工作时间大量调用
- **失败率异常**: 认证失败率 > 5%

### 告警配置

**阿里云监控示例**:

```bash
# 创建告警规则
aliyun cms PutMetricRuleTemplate \
  --RuleName "API 密钥异常使用" \
  --RuleDescription "检测 API 调用量突增" \
  --Rules '[{
    "MetricName": "QPS",
    "ComparisonOperator": "GreaterThanThreshold",
    "Threshold": 100,
    "Statistics": "Average",
    "Period": 300
  }]'
```

### 审计日志

```bash
# 启用 OpenClaw 访问日志
echo "LOG_LEVEL=info" >> ~/.openclaw/.env
echo "LOG_FILE=~/.openclaw/logs/access.log" >> ~/.openclaw/.env

# 定期审计（每周）
grep "401\|403" ~/.openclaw/logs/access.log | awk '{print $1}' | sort | uniq -c
```

## 泄露应急响应

### 检测泄露

```bash
# 1. 检查 GitHub 是否泄露
# 访问：https://github.com/search?q=你的密钥前缀

# 2. 检查本地历史
grep -r "sk-" ~/.zsh_history ~/.bash_history

# 3. 监控异常调用
tail -f ~/.openclaw/logs/access.log | grep -E "401|403|429"
```

### 响应流程

1. **立即禁用密钥**（在对应平台操作）
2. **生成新密钥**并更新配置
3. **重启服务**使新密钥生效
4. **审计日志**确认泄露范围
5. **通知相关人员**（如影响他人）
6. **更新文档**记录事件

### 事后复盘

```markdown
## 泄露事件报告

**日期**: YYYY-MM-DD
**影响范围**: [受影响的密钥和服务]
**泄露原因**: [如：误提交到 GitHub]
**响应时间**: [发现到禁用的时间]
**改进措施**:
- [ ] 添加 pre-commit hook 检测密钥
- [ ] 启用 GitHub secret scanning
- [ ] 缩短密钥轮换周期
```

## 检查清单

### 日常检查（每日）

- [ ] 检查 API 调用量是否异常
- [ ] 查看认证失败日志
- [ ] 确认密钥未过期

### 定期检查（每月）

- [ ] 审计密钥使用记录
- [ ] 检查密钥剩余有效期
- [ ] 验证备份密钥可用
- [ ] 更新密钥文档

### 部署前检查

- [ ] 确认使用环境变量而非硬编码
- [ ] 验证 .env 文件权限为 600
- [ ] 检查 .gitignore 包含敏感文件
- [ ] 测试密钥轮换流程

## 工具推荐

| 工具 | 用途 | 平台 |
|------|------|------|
| git-secrets | Git 提交前检测密钥 | 通用 |
| truffleHog | 扫描代码库历史 | 通用 |
| AWS Config | 监控密钥使用 | AWS |
| Azure Policy | 密钥合规检查 | Azure |
| 1Password | 安全存储和共享 | 通用 |

## 相关资源

- MiniMax API 密钥管理：https://platform.minimaxi.com/user-center/api-key
- 阿里云 RAM 访问控制：https://ram.console.aliyun.com/
- GitHub Secret Scanning: https://docs.github.com/en/code-security/secret-scanning

## 更新记录

- 2026-03-15: 初始版本
