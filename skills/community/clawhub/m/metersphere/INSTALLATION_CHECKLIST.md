# MeterSphere Skills 安装前检查清单

## 📋 安装前必须完成的步骤

### 1. 确认元数据一致性
**问题**: 包注册表摘要可能未列出必需的环境变量/二进制文件，而 SKILL.md 和 skill-metadata.json 需要凭证和工具
**验证**:
- [ ] 确认 `skill-metadata.json` 中的 `requiredEnvVars` 包含: `METERSPHERE_BASE_URL`, `METERSPHERE_ACCESS_KEY`, `METERSPHERE_SECRET_KEY`
- [ ] 确认 `skill-metadata.json` 中的 `requiredBinaries` 包含: `python3`, `openssl`, `curl`
- [ ] 确认 SKILL.md 中的环境变量说明与 metadata 一致
- [ ] 联系发布者确认签名算法和元数据差异的解释

### 2. 使用最小权限凭证
**要求**: 创建具有最小必要范围的 MeterSphere API 密钥
**操作**:
- [ ] 为查询操作创建只读 API 密钥
- [ ] 为创建/写入操作创建单独的、有限权限的密钥
- [ ] 记录每个密钥的权限范围和有效期
- [ ] 在生产环境中使用前，在测试环境中验证权限

### 3. 检查和控制 .env 文件
**警告**: 脚本会从技能目录加载 .env 文件
**验证**:
- [ ] 确保 .env 文件仅包含预期的环境变量
- [ ] 检查 .env 文件中没有额外的敏感信息
- [ ] 使用 `.env.example` 作为模板创建安全的 .env 文件
- [ ] 设置适当的文件权限 (chmod 600 .env)

### 4. 警惕 HEADERS_JSON
**风险**: METERSPHERE_HEADERS_JSON 可以注入任意 HTTP 头
**防护**:
- [ ] 如果设置 METERSPHERE_HEADERS_JSON，确保不包含可能泄露数据的头部
- [ ] 不要包含可能向其他服务进行身份验证的头部
- [ ] 定期审查 HEADERS_JSON 的内容
- [ ] 考虑是否真的需要设置此变量

### 5. 审查硬编码 ID
**风险**: 脚本包含硬编码的项目/模板/版本 ID
**防护**:
- [ ] 设置 METERSPHERE_DEFAULT_TEMPLATE_ID 环境变量
- [ ] 设置 METERSPHERE_DEFAULT_VERSION_ID 环境变量
- [ ] 设置 METERSPHERE_PROJECT_ID 环境变量（如需要）
- [ ] 验证这些 ID 对应正确的项目，避免意外写入他人项目

### 6. 先在沙箱中运行
**要求**: 在非生产环境中测试并监控网络流量
**操作**:
- [ ] 在隔离的测试环境中首次运行
- [ ] 使用网络监控工具确认技能仅调用预期的 BASE_URL
- [ ] 验证所有 API 调用都指向正确的 MeterSphere 实例
- [ ] 测试查询和写入操作，确保数据归属正确

### 7. 确保二进制文件来自可信源
**要求**: openssl/curl/python3 必须来自可信的系统包
**验证**:
- [ ] 检查 openssl 版本和来源: `openssl version`
- [ ] 检查 curl 版本和来源: `curl --version`
- [ ] 检查 python3 版本和来源: `python3 --version`
- [ ] 确认这些二进制文件来自操作系统官方仓库或可信的包管理器

### 8. 签名算法验证（如需更强保证）
**可选**: 如果需要更强的保证，请求发布者签字或维护者解释
**操作**:
- [ ] 请求发布者解释元数据差异
- [ ] 请求维护者解释用于签名头的签名算法
- [ ] 审查 scripts/ms_batch.py 中的 `signature()` 函数
- [ ] 验证签名算法是否符合安全标准

## 🔍 快速验证命令

```bash
# 1. 运行完整验证脚本
./scripts/verify_installation.py

# 2. 检查元数据
cat skill-metadata.json | jq '.requiredEnvVars, .requiredBinaries'

# 3. 检查二进制文件
which python3 openssl curl
python3 --version
openssl version
curl --version

# 4. 检查环境变量模板
cat .env.example

# 5. 检查硬编码ID警告
grep -r "1163437937827840\|警告" scripts/

# 6. 检查签名算法
grep -A10 "def signature" scripts/ms_batch.py
```

## 🛡️ 安全配置示例

### 最小权限 .env 配置
```bash
# 查询专用（只读）
METERSPHERE_BASE_URL=http://your-metersphere-instance:8081
METERSPHERE_ACCESS_KEY=readonly_key_here
METERSPHERE_SECRET_KEY=readonly_secret_here

# 可选：避免硬编码ID问题
METERSPHERE_DEFAULT_TEMPLATE_ID=your_template_id
METERSPHERE_DEFAULT_VERSION_ID=your_version_id
METERSPHERE_PROJECT_ID=your_project_id

# 注意：不要设置 METERSPHERE_HEADERS_JSON 除非必要
```

### 创建专用 .env 配置
```bash
# 创建专用（有限权限）
METERSPHERE_BASE_URL=http://your-metersphere-instance:8081
METERSPHERE_ACCESS_KEY=create_only_key_here
METERSPHERE_SECRET_KEY=create_only_secret_here

# 必须设置以避免数据错误归属
METERSPHERE_DEFAULT_TEMPLATE_ID=your_template_id
METERSPHERE_DEFAULT_VERSION_ID=your_version_id
METERSPHERE_PROJECT_ID=your_project_id
```