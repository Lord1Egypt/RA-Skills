# Aligenie Genie2 部署指南

**适用范围**：腾讯云 Windows Server，OpenClaw agent 双向通信

---

## 架构概览

```
天猫精灵 ←→ 阿里云 Aligenie ←→ 腾讯云 (:58472) ←→ OpenClaw Agent
                                              ↓
                                        SQLite 数据库
                                      (账户/设备/API Key)
```

---

## 快速部署

### 1. 下载依赖到腾讯云

在 `C:\temp\` 目录下：

```powershell
# 下载 SQLite JDBC（如果没有）
# 从 https://github.com/xerial/sqlite-jdbc/releases 下载 sqlite-jdbc-xxx.jar

# 上传文件（在本机执行）
scp -i ~/.ssh/id_rsa_workspace_backup sqlite-jdbc-xxx.jar Administrator@101.43.110.225:C:/temp/
scp -i ~/.ssh/id_rsa_workspace_backup AligenieServer.java Administrator@101.43.110.225:C:/temp/
```

### 2. 编译

```powershell
cd C:\temp
javac -encoding UTF-8 -cp .;sqlite-jdbc-xxx.jar AligenieServer.java
```

### 3. 初始化数据库

服务器首次启动时自动创建 `C:\temp\aligenie.db`。

### 4. 启动

```powershell
cd C:\temp
java -cp ".;sqlite-jdbc-xxx.jar" AligenieServer --port 58472
```

### 5. 配置开机自启（可选）

```powershell
# 创建计划任务
schtasks /create /tn AligenieServer /tr "java -cp C:\temp AligenieServer --port 58472" /sc onlogon /ru Administrator
```

---

## CLI 管理工具

位置：`C:\temp\aligenie-cli.bat`

### 配置

创建 `C:\temp\aligenie-cli-config.json`：

```json
{
  "server": "http://127.0.0.1:58472",
  "apiKey": "ak_xxx",
  "userId": "uuid"
}
```

### 使用示例

```bash
# 创建管理员账户
aligenie-cli.bat account register admin "你的密码"

# 登录（获取 API Key）
aligenie-cli.bat account login admin "你的密码"

# 创建 Agent
aligenie-cli.bat agent create lobster

# 生成验证码（绑定天猫精灵）
aligenie-cli.bat verify create

# 查看设备
aligenie-cli.bat device list
```

---

## 安全配置

### 腾讯云安全组

| 协议 | 端口 | 来源 | 用途 |
|------|------|------|------|
| TCP | 58472 | 0.0.0.0/0 | HTTP API |
| TCP | 22 | 你的IP | SSH 管理 |

### 密码要求

- 最少 8 字符
- PBKDF2-SHA256 存储（100,000 次迭代，256-bit 输出）
- 永不明文存储

---

## API 基础 URL

- 本地：`http://127.0.0.1:58472`
- 公网：`http://101.43.110.225:58472`

### 认证

管理接口使用 `X-Api-Key` header：

```bash
curl -H "X-Api-Key: ak_xxx" http://101.43.110.225:58472/api/v1/devices
```

---

## 详细 API 文档

参见 `SPEC.md`。
