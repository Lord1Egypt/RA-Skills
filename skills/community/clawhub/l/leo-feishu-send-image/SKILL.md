---
name: feishu-send-image
description: Send images via Feishu (Lark) messaging platform using the underlying API. Supports sending local image files to users or group chats. Use when the user wants to send images through Feishu, share generated images via Feishu messages, or automate image delivery to Feishu conversations. Triggers on phrases like "send image to feishu", "飞书发图", "feishu发送图片", "飞书发送图片", "用飞书发图", or when explicitly requesting to send images via Feishu API.
---

# Feishu Send Image

通过飞书 API 发送图片消息。支持发送本地图片文件给指定用户或群聊。

## 安装

### 方式1：通过 OpenClaw 对话安装

在飞书（或其他渠道）的 OpenClaw 对话框中直接说：

```
安装 leo-feishu-send-image skill
```

或

```
帮我装一下 leo-feishu-send-image
```

OpenClaw 会自动从 ClawHub 下载并安装 skill。

### 方式2：通过命令行安装

```bash
clawhub install leo-feishu-send-image
```

## 前置要求

### 1. 飞书应用配置

在 `~/.openclaw/openclaw.json` 中添加飞书应用配置：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "appId": "cli_xxxxxxxxxxxxxxxx",
          "appSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
      }
    }
  }
}
```

**如何获取 App ID 和 App Secret：**
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 进入应用详情 → 凭证与基础信息
4. 复制 `App ID` 和 `App Secret`
5. 确保应用有 `im:chat:readonly` 和 `im:message:send_as_bot` 权限

### 2. 安装依赖工具

需要 `jq` 工具处理 JSON：

```bash
# Ubuntu/Debian
sudo apt-get install jq

# CentOS/RHEL
sudo yum install jq

# macOS
brew install jq
```

## 使用方法

### 方式1：通过 OpenClaw 对话使用（推荐）

安装 skill 后，直接在对话框中说：

```
用飞书发图 skill 发送 /path/to/image.jpg 给 ou_xxxxxxxx
```

或

```
用 leo-feishu-send-image 发图给 ou_xxxxxxxx
```

或

```
飞书发送图片 /path/to/image.jpg 给 ou_xxxxxxxx
```

**参数说明：**
- `/path/to/image.jpg` - 本地图片文件路径
- `ou_xxxxxxxx` - 接收者的 open_id（用户）或 `oc_xxxxxxxx`（群聊）

### 方式2：直接调用脚本

```bash
# 进入 skill 目录
cd ~/.openclaw/workspace/skills/leo-feishu-send-image

# 基本用法
./scripts/send-image.sh <图片路径> <接收者ID>

# 指定账户
./scripts/send-image.sh <图片路径> <接收者ID> <账户ID>
```

**示例：**

```bash
# 发送给用户
./scripts/send-image.sh ./output.jpg ou_114db42b481a66952fceb246da9c7bd7

# 发送到群聊
./scripts/send-image.sh ./output.jpg oc_e4bc81fe9899665019af2cccaa7bb30d

# 使用指定账户（如果配置了多个账户）
./scripts/send-image.sh ./output.jpg ou_xxxxxxxx prompt
```

## 完整使用场景示例

### 场景1：AI 生成图片后自动发送

```
用户：用即梦生成一张风景图，然后发给我

OpenClaw：
1. 调用即梦 skill 生成图片
2. 保存到 workspace
3. 调用 leo-feishu-send-image 发送图片给用户
```

### 场景2：批量发送图片

```
用户：把这 5 张图都发给我

OpenClaw：
for i in 1 2 3 4 5; do
    ./scripts/send-image.sh ./image_$i.jpg ou_xxxxxxxx
done
```

### 场景3：发送到群聊

```
用户：把这张图发到游戏开发群

OpenClaw：
./scripts/send-image.sh ./design.png oc_xxxxxxxx
```

## API 流程说明

本 skill 底层调用飞书开放平台的三个 API：

1. **获取 Access Token**
   - 接口：`POST /auth/v3/tenant_access_token/internal`
   - 使用 app_id 和 app_secret 换取 tenant_access_token

2. **上传图片**
   - 接口：`POST /im/v1/images`
   - 上传图片文件，返回 image_key

3. **发送消息**
   - 接口：`POST /im/v1/messages`
   - 使用 image_key 发送图片消息
   - ⚠️ 注意：content 字段必须是 JSON 字符串（使用 `jq tojson` 转换）

## 支持的图片格式

- JPEG / JPG
- PNG
- WEBP
- GIF
- TIFF
- BMP
- ICO

## 故障排查

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `缺少 app_id` | 飞书配置未找到 | 检查 `~/.openclaw/openclaw.json` 中的 `channels.feishu.accounts` 配置 |
| `获取 token 失败` | App ID / Secret 错误 | 确认应用凭证正确，且应用已启用 |
| `上传失败` | 图片格式不支持 | 转换为 JPEG/PNG 格式后重试 |
| `发送失败` | 接收者 ID 错误 | 确认 open_id 或 chat_id 正确，且机器人有权限发送给该用户/群聊 |
| `未安装 jq` | 缺少依赖工具 | 执行 `sudo apt-get install jq` 或对应系统的安装命令 |

## 获取接收者 ID

### 获取用户 open_id

1. 在飞书开放平台 → 应用详情 → 权限管理
2. 确保有 `contact:user.read` 权限
3. 调用 API 或通过事件订阅获取

### 获取群聊 chat_id

1. 将机器人添加到群聊
2. 在群设置 → 群机器人 中查看
3. 或通过 `im.chat.list` API 获取

## 相关链接

- [飞书开放平台文档](https://open.feishu.cn/document/home/index)
- [发送消息 API](https://open.feishu.cn/document/server-docs/im-v1/message/create)
- [上传图片 API](https://open.feishu.cn/document/server-docs/im-v1/image/create)
- [ClawHub Skill 页面](https://clawhub.com/skills/leo-feishu-send-image)

## 更新日志

### v1.0.0
- 初始版本发布
- 支持发送图片到用户和群聊
- 支持多账户配置

---

**作者**: @leo-jiqimao  
**ClawHub**: https://clawhub.com/skills/leo-feishu-send-image  
**问题反馈**: 请在 ClawHub 页面提交 issue
