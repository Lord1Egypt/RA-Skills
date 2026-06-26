---
name: huawei-obs-sdk
description: 华为云 OBS 对象存储 SDK 使用指南。包含 SDK 安装、初始化客户端、文件上传/下载、管理存储桶、管理对象等核心操作的最佳实践和代码示例。使用当需要操作华为云 OBS 对象存储时。
---

# 华为云 OBS SDK 使用指南

本技能提供华为云 OBS（对象存储服务）Python SDK 的核心使用方法和最佳实践。

## 快速开始

### 1. 安装 SDK
```bash
pip install huaweicloud-sdk-python-obs
```

### 2. 初始化客户端
```python
from obs import ObsClient

# 初始化 OBS 客户端
obs_client = ObsClient(
    access_key_id='YOUR_ACCESS_KEY',
    secret_access_key='YOUR_SECRET_KEY',
    server='obs.cn-east-3.myhuaweicloud.com'  # 根据实际区域填写
)
```

### 3. 关闭客户端
```python
obs_client.close()
```

## 核心操作

### 存储桶管理
参考 [references/bucket_operations.md](references/bucket_operations.md)
- 创建/删除存储桶
- 存储桶权限配置
- 存储桶生命周期管理
- 存储桶跨域配置

### 对象操作
参考 [references/object_operations.md](references/object_operations.md)
- 上传文件/文件夹
- 下载文件/文件夹
- 删除/复制/移动对象
- 列举对象
- 断点续传
- 预签名 URL 生成

### 高级功能
参考 [references/advanced_features.md](references/advanced_features.md)
- 版本控制
- 服务器端加密
- 跨域资源共享 (CORS)
- 事件通知
- 生命周期规则

## 安全最佳实践
1. 不要硬编码 AK/SK，使用环境变量或配置文件管理
2. 为 OBS 账户分配最小必要权限
3. 定期轮换访问密钥
4. 使用 HTTPS 协议访问 OBS 服务
5. 敏感数据上传前建议客户端加密

## 错误处理
```python
try:
    resp = obs_client.putFile('bucket_name', 'object_key', 'local_file_path')
    if resp.status < 300:
        print('上传成功')
    else:
        print(f'上传失败: {resp.errorMessage}')
except Exception as e:
    print(f'操作异常: {e}')
```
