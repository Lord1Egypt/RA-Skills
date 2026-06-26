# MeterSphere Skills 签名算法说明

## 算法概述

本技能使用 AES-128-CBC 加密算法在本地生成请求签名，用于 MeterSphere API 的身份验证。

## 签名生成流程

### 1. 原始数据构造
```python
plain = f"{AK}|{uuid.uuid4()}|{int(time.time()*1000)}"
```
- `AK`: METERSPHERE_ACCESS_KEY
- `uuid.uuid4()`: 随机 UUID，确保每次签名唯一
- `int(time.time()*1000)`: 当前时间戳（毫秒）

### 2. 加密过程
```python
p = subprocess.run([
    'openssl', 'enc', '-aes-128-cbc', 
    '-K', SK.encode().hex(),      # 密钥：METERSPHERE_SECRET_KEY 的十六进制
    '-iv', AK.encode().hex(),     # 初始化向量：METERSPHERE_ACCESS_KEY 的十六进制
    '-base64', '-A', '-nosalt'
], input=plain.encode(), capture_output=True, check=True)
signature = p.stdout.decode().strip()
```

### 3. 算法参数
- **算法**: AES-128-CBC
- **密钥**: METERSPHERE_SECRET_KEY（转换为十六进制）
- **IV**: METERSPHERE_ACCESS_KEY（转换为十六进制）
- **输出**: Base64 编码
- **填充**: 默认 PKCS#7 填充
- **盐**: 禁用 (`-nosalt`)

## 安全特性

### ✅ 安全设计
1. **本地签名**: 所有签名在本地生成，`METERSPHERE_SECRET_KEY` 不会传输到网络
2. **时效性**: 签名包含时间戳，防止重放攻击
3. **随机性**: 每次签名包含随机 UUID，确保唯一性
4. **标准算法**: 使用行业标准的 AES-128-CBC 加密

### 🔒 密钥安全
- `METERSPHERE_SECRET_KEY` 仅在本地用于签名生成
- 密钥不会出现在网络请求中
- 建议定期轮换 API 密钥
- 使用最小权限的密钥

### 🌐 网络传输
签名通过 HTTP 头传输：
```http
accessKey: YOUR_ACCESS_KEY
signature: BASE64_ENCODED_SIGNATURE
```

## 验证步骤

### 1. 算法验证
```bash
# 检查签名函数
grep -A15 "def signature" scripts/ms_batch.py

# 验证 openssl 命令
openssl enc -aes-128-cbc -h 2>&1 | grep -i "cbc"
```

### 2. 本地测试
```python
# 测试签名生成（不发送请求）
import subprocess
import uuid
import time

AK = "test_access_key"
SK = "test_secret_key"

plain = f"{AK}|{uuid.uuid4()}|{int(time.time()*1000)}"
print(f"原始数据: {plain}")

p = subprocess.run([
    'openssl', 'enc', '-aes-128-cbc',
    '-K', SK.encode().hex(),
    '-iv', AK.encode().hex(),
    '-base64', '-A', '-nosalt'
], input=plain.encode(), capture_output=True, check=True)

print(f"签名: {p.stdout.decode().strip()}")
```

### 3. 网络监控
使用工具监控网络流量，确认：
- 只有 `accessKey` 和 `signature` 头部被发送
- `METERSPHERE_SECRET_KEY` 不会出现在任何请求中
- 所有请求都指向预期的 `METERSPHERE_BASE_URL`

## 已知限制

### 1. 依赖 openssl
- 需要系统安装 openssl
- 必须来自可信的系统包
- 版本兼容性：支持 AES-128-CBC 的版本

### 2. 时间同步
- 服务器和客户端时间需要基本同步
- 时间戳用于防止重放攻击

### 3. 密钥管理
- 用户需要安全地管理 `.env` 文件
- 建议文件权限设置为 600
- 不要在版本控制中提交 `.env` 文件

## 故障排除

### 常见问题

1. **签名验证失败**
   - 检查时间同步
   - 验证 ACCESS_KEY 和 SECRET_KEY 是否正确
   - 确认 openssl 版本兼容

2. **权限错误**
   - 确认 API 密钥具有所需权限
   - 检查 MeterSphere 用户权限设置

3. **连接问题**
   - 验证 METERSPHERE_BASE_URL 可访问
   - 检查网络防火墙设置

### 调试命令
```bash
# 测试连接
curl -v "${METERSPHERE_BASE_URL}/system/status"

# 测试签名生成
python3 -c "
import subprocess, uuid, time, os
AK = os.environ.get('METERSPHERE_ACCESS_KEY', 'test')
SK = os.environ.get('METERSPHERE_SECRET_KEY', 'test')
plain = f'{AK}|{uuid.uuid4()}|{int(time.time()*1000)}'
print('Plain:', plain)
p = subprocess.run(['openssl', 'enc', '-aes-128-cbc', '-K', SK.encode().hex(), '-iv', AK.encode().hex(), '-base64', '-A', '-nosalt'], input=plain.encode(), capture_output=True)
print('Signature:', p.stdout.decode().strip())
"
```