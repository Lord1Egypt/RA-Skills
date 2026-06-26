# Private Secrets Skill

用于安全存储和管理你的私密信息（如 API Key、密码、令牌等）。

## 功能

- **添加私密信息**：记录名称 + 内容
- **查看列表**：查看已存储的信息名称（不含内容）
- **读取内容**：查看具体的私密内容

## 存储位置

`/workspace/skills/private-secrets-1.0.0/secrets.json`

## 使用方式

### 添加 secret
```
添加 secret: [名称] = [内容]
例：添加 secret: openai_key = sk-xxx
```

### 查看列表
```
列出所有 secrets
```

### 读取内容
```
查看 secret: [名称]
```

## 安全注意

- 此文件存储在本地，未加密
- 建议定期备份
- 如需更高安全性，可使用加密工具手动加密文件
