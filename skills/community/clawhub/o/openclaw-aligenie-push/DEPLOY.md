# 部署指南 — openclaw-aligenie-push

> 完整部署步骤，供一次性配置使用。日常使用只看 SKILL.md。

## 架构

```
OpenClaw (杭州家里 WSL)
    │  HTTPS POST
    ▼
腾讯云服务器 (:58472)  ← 公网IP，需开放58472端口
    │  Java 内置 HTTP 服务器
    ▼
阿里云 Aligenie 推送 API
    ▼
天猫精灵设备 → 语音播报
```

> **注意**：云服务器上运行的是 Java 版本 PushServer（已预装 Java 17），无需安装 Python/Flask。

---

## 一、腾讯云安全组配置

**必须操作**：在腾讯云控制台开放端口 `58472`

| 协议 | 端口 | 来源 |
|------|------|------|
| TCP | 58472 | 0.0.0.0/0 |

---

## 二、阿里云技能配置

### 1.1 申请消息推送权限

在 iap.aligenie.com 创建「OpenClaw主动播报」技能后：

1. 进入「技能配置」→「能力市场」
2. 搜索「消息推送_定制机版」
3. 提交申请，等待审核（通常1-3个工作日）

### 1.2 获取 AppSecret（审核通过后）

1. 登录 https://iap.aligenie.com
2. 进入「OpenClaw主动播报」→「基本配置」
3. 记录 **AppSecret**

### 1.3 获取设备 openId

天猫精灵 App → 我的 → 智能家居 → 点击设备 → 设备信息 → openId

---

## 三、腾讯云服务器部署（已预装 Java）

云服务器已安装 Java 17 (`C:\Program Files\Java\jdk-17\bin\java.exe`)。

### 3.1 上传 PushServer

Java 源码已通过 SSH 上传至 `C:\temp\PushServer.java`，
编译好的 class 文件在 `C:\temp\PushServer.class`。

### 3.2 启动服务器

SSH 登录后运行：

```powershell
cd C:\temp
java -cp . PushServer --port 58472
```

### 3.3 持久化（开机自启）

腾讯云 Windows Server 重启后自动启动：

```powershell
# 用 Windows 任务计划程序创建开机任务（管理员 PowerShell）
$action = New-ScheduledTaskAction -Execute 'java' -Argument '-cp C:\temp PushServer --port 58472'
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName 'AligeniePushServer' -Action $action -Trigger $trigger -Settings $settings
```

### 3.4 验证

```powershell
# 本地验证
curl http://127.0.0.1:58472/health
# 返回: {"status":"ok","service":"aligenie-push-server"}

# 从外部验证（安全组开放后）
curl http://你的腾讯云公网IP:58472/health
```

---

## 四、OpenClaw 端配置

在 OpenClaw workspace 的 `TOOLS.md` 中添加：

```markdown
### 天猫精灵推送配置
ALIGENIE_PUSH_SERVER=http://你的腾讯云公网IP:58472/push
ALIGENIE_APP_ID=2026032918608
ALIGENIE_APP_SECRET=审批通过后获取
ALIGENIE_DEVICE_OPEN_ID=天猫精灵设备openId
```

---

## 五、API 端点（参考）

| 用途 | URL | 方法 |
|------|-----|------|
| 获取 access_token | `https://oauth.taobao.com/token` | GET |
| 推送消息 | `https://api.aligenie.com/v1.0/push/pushMsg` | POST |

> ⚠️ API 端点待 Aligenie 审批通过后实际验证。

---

## 六、故障排查

### 端口访问不通

1. 确认 Java 进程在运行：`netstat -ano | Select-String "58472"`
2. 确认腾讯云安全组已开放 58472 端口

### 推送失败

```powershell
# 查看服务器日志（stderr）
# stderr 输出到控制台，重定向方式：
java -cp . PushServer --port 58472 2>&1 | Tee-Object server.log
```

### 天猫精灵没有播报

- 确认技能已添加（天猫精灵App → 技能中心 → 我的技能）
- 确认 openId 与设备匹配
- 确认 openId 与 AppId/AppSecret 属于同一账号
