# 平台账号信息管理命令

## 概述

平台账号信息管理命令用于查看和配置保利威账号的基本信息和开关配置。

## 命令列表

| 命令 | 描述 |
|------|------|
| `platform get` | 获取账号基本信息 |
| `platform switch get` | 获取账号开关配置 |
| `platform switch update` | 更新账号开关配置 |
| `platform callback get` | 获取回调设置 |
| `platform callback update` | 更新回调设置 |
| `platform setting get` | 获取全局频道设置 |
| `platform setting update` | 更新全局频道设置 |

## platform get

获取账号基本信息，包括用户ID、邮箱、频道数、连麦限制等。

### 用法

```bash
<CLI> platform get [选项]
```

### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出格式 (table\|json) | table |

### 示例

```bash
# 获取账号基本信息（表格格式）
<CLI> platform get

# 获取账号基本信息（JSON格式）
<CLI> platform get -o json
```

### 输出字段说明

| 字段 | 描述 |
|------|------|
| 用户 ID | 保利威账号的用户ID |
| 邮箱 | 账号绑定的邮箱地址 |
| 最大频道数 | 账号可创建的最大频道数量 |
| 总频道数 | 当前已创建的频道总数 |
| 可用频道数 | 剩余可创建的频道数量 |
| 连麦限制 | 连麦功能的限制数 |
| 观看域名 | 自定义观看域名（如已配置） |

### JSON 输出示例

```json
{
  "userId": "user123",
  "email": "admin@example.com",
  "maxChannels": 100,
  "totalChannels": 10,
  "availableChannels": 90,
  "linkMicLimit": 10,
  "watchDomain": "https://live.example.com"
}
```

---

## platform switch get

获取账号的开关配置状态。返回项中的 `type` 值可作为 `platform switch update --param` 的参数。

### 用法

```bash
<CLI> platform switch get [选项]
```

### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出格式 (table\|json) | table |

### 示例

```bash
# 获取开关配置（表格格式）
<CLI> platform switch get

# 获取开关配置（JSON格式）
<CLI> platform switch get -o json
```

### 输出字段说明

| 字段 | 描述 |
|------|------|
| `type` | 开关参数名 |
| `enabled` | 开关状态（Y/N） |

### JSON 输出示例

```json
[
  {
    "type": "isClosePreview",
    "enabled": "N"
  },
  {
    "type": "mobileWatch",
    "enabled": "Y"
  }
]
```

---

## platform switch update

更新账号的开关配置。

### 用法

```bash
<CLI> platform switch update --param <参数名> --enabled <Y|N> [选项]
```

### 选项

| 选项 | 简写 | 描述 | 必需 | 默认值 |
|------|------|------|------|--------|
| `--param` | - | 开关参数名称 | 是 | - |
| `--enabled` | - | 启用状态 (Y\|N) | 是 | - |
| `--force` | `-f` | 跳过确认提示 | 否 | - |
| `--output` | `-o` | 输出格式 (table\|json) | 否 | table |

### 可用参数

| 参数名 | 描述 |
|--------|------|
| `isClosePreview` | 系统观看页开关（Y 表示关闭系统观看页） |
| `mobileWatch` | 移动端观看开关 |
| `mobileAudio` | 移动端音频开关 |
| `autoPlay` | 自动播放开关 |
| `booking` | 预约开关 |
| `redPack` | 红包开关 |
| `shareBtnEnabled` | 分享按钮开关 |
| `chat` | 聊天开关 |
| `chatPlayBack` | 回放聊天开关 |
| `closeChaterList` | 在线列表开关（Y 表示关闭在线列表） |
| `consultingMenu` | 咨询菜单开关 |
| `closeDanmu` | 弹幕开关（Y 表示关闭弹幕） |
| `praise` | 点赞开关 |
| `welcome` | 欢迎语开关 |
| `viewerSendImgEnabled` | 观众发图开关 |
| `sendFlowersEnabled` | 送花开关 |
| `pushSharingEnabled` | 推送分享开关 |
| `qaMenuEnabled` | 问答菜单开关 |
| `filterManagerMsgEnabled` | 过滤管理员消息开关 |
| `showCustomMessageEnabled` | 自定义消息显示开关 |
| `chatOnlineNumberEnable` | 聊天在线人数开关 |
| `pvShowEnabled` | PV 展示开关 |
| `rtsEnabled` | RTS 开关 |

### 示例

```bash
# 启用聊天功能
<CLI> platform switch update --param chat --enabled Y

# 关闭弹幕
<CLI> platform switch update --param closeDanmu --enabled Y

# JSON输出
<CLI> platform switch update --param autoPlay --enabled N -o json
```

### 错误处理

| 错误情况 | 错误信息 |
|----------|----------|
| 参数为空 | `param (配置项名称) 是必需的` |
| enabled 值无效 | `enabled 必须是 Y 或 N` |
| 不支持的参数 | `不支持的配置项: xxx。可用配置项: isClosePreview, mobileWatch, mobileAudio, autoPlay, booking, redPack, shareBtnEnabled, chat, chatPlayBack, closeChaterList, consultingMenu, closeDanmu, praise, welcome, viewerSendImgEnabled, sendFlowersEnabled, pushSharingEnabled, qaMenuEnabled, filterManagerMsgEnabled, showCustomMessageEnabled, chatOnlineNumberEnable, pvShowEnabled, rtsEnabled` |

---

## API 映射

| CLI 命令 | SDK 方法 | API 端点 |
|----------|----------|----------|
| `platform get` | `account.getUserInfo()` | `/live/v3/user/get-info` |
| `platform switch get` | `account.switchGet()` | `/live/v3/user/switch/get` |
| `platform switch update` | `account.switchUpdate()` | `/live/v3/user/switch/update` |
| `platform callback get` | `v4User.getCallback()` | `/live/v4/user/callback/get` |
| `platform callback update` | `v4User.updateCallback()` | `/live/v4/user/callback/update` |
| `platform setting get` | `v4User.getGlobalChannelSettings()` | `/live/v4/user/global-setting/switch/get` |
| `platform setting update` | `v4User.updateGlobalChannelSettings()` | `/live/v4/user/global-setting/switch/update` |

---

## platform callback get

获取回调设置，包括回调URL和启用状态。

### 用法

```bash
<CLI> platform callback get [选项]
```

### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出格式 (table\|json) | table |

### 示例

```bash
# 获取回调设置（表格格式）
<CLI> platform callback get

# 获取回调设置（JSON格式）
<CLI> platform callback get -o json
```

### 输出字段说明

| 字段 | 描述 |
|------|------|
| 回调 URL | 接收回调通知的URL地址 |
| 是否启用 | 回调功能是否启用（是/否） |

### JSON 输出示例

```json
{
  "url": "https://example.com/callback",
  "enabled": true
}
```

---

## platform callback update

更新回调设置，可以更新回调URL和启用状态。

### 用法

```bash
<CLI> platform callback update [选项]
```

### 选项

| 选项 | 简写 | 描述 | 必需 | 默认值 |
|------|------|------|------|--------|
| `--url` | - | 直播状态回调URL（写入 `streamCallbackUrl`，必须以 http:// 或 https:// 开头） | 否 | - |
| `--clear-url` | - | 清空直播状态回调URL（写入空字符串到 `streamCallbackUrl`） | 否 | - |
| `--enabled` | - | 回放生成回调启用状态 (Y\|N)，对应 `rebirthVodCallbackEnabled` | 否 | - |
| `--force` | `-f` | 跳过确认提示 | 否 | - |
| `--output` | `-o` | 输出格式 (table\|json) | 否 | table |

**注意：** 至少需要提供一个选项（`--url`、`--clear-url` 或 `--enabled`）。

### 示例

```bash
# 更新直播状态回调URL
<CLI> platform callback update --url https://example.com/callback

# 清空直播状态回调URL
<CLI> platform callback update --clear-url

# 启用回放生成回调
<CLI> platform callback update --enabled Y

# 禁用回放生成回调
<CLI> platform callback update --enabled N

# 同时更新直播状态回调URL和回放生成回调状态
<CLI> platform callback update --url https://example.com/callback --enabled Y

# JSON格式输出
<CLI> platform callback update --url https://example.com/callback -o json
```

### 错误处理

| 错误情况 | 错误信息 |
|----------|----------|
| 无参数提供 | `至少需要提供一个参数 (url 或 enabled)` |
| URL格式错误 | `url 必须以 http:// 或 https:// 开头` |
| enabled值无效 | `enabled 必须是 Y 或 N` |

---

## platform setting get

获取全局频道设置，包括并发观看人数、自动转码、打赏等功能的状态。

### 用法

```bash
<CLI> platform setting get [选项]
```

### 选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--output` | `-o` | 输出格式 (table\|json) | table |

### 示例

```bash
# 获取全局频道设置（表格格式）
<CLI> platform setting get

# 获取全局频道设置（JSON格式）
<CLI> platform setting get -o json
```

### 输出字段说明

| 设置项 | 描述 |
|--------|------|
| 最大并发观看人数 | 最大并发观看人数开关（开启/禁用） |
| 自动转码 | 自动转码功能开关 |
| 打赏功能 | 打赏功能开关 |
| 转存自动上传 | 转存自动上传PPT开关 |
| 转存自动转码 | 转存自动转码开关 |
| PPT全屏 | PPT全屏显示开关 |
| 封面图片类型 | 播放器封面图片类型（contain/cover） |

**注意：** `testModeButtonEnabled` 只能通过 `platform setting update --test-mode-button-enabled` 写入，`platform setting get` 不返回该字段。

### JSON 输出示例

```json
{
  "channelConcurrencesEnabled": "Y",
  "timelyConvertEnabled": "Y",
  "donateEnabled": "N",
  "rebirthAutoUploadEnabled": "N",
  "rebirthAutoConvertEnabled": "N",
  "pptCoveredEnabled": "N",
  "coverImgType": "contain"
}
```

---

## platform setting update

更新全局频道设置，可以同时更新多个设置项。

### 用法

```bash
<CLI> platform setting update [选项]
```

### 选项

| 选项 | 描述 | 值 |
|------|------|------|
| `--channel-concurrences-enabled` | 最大并发观看人数开关 | Y/N |
| `--timely-convert-enabled` | 自动转码开关 | Y/N |
| `--donate-enabled` | 打赏功能开关 | Y/N |
| `--rebirth-auto-upload-enabled` | 转存自动上传PPT | Y/N |
| `--rebirth-auto-convert-enabled` | 转存自动转码 | Y/N |
| `--ppt-covered-enabled` | PPT全屏开关 | Y/N |
| `--cover-img-type` | 封面图片类型 | contain/cover |
| `--test-mode-button-enabled` | 测试模式按钮（只写，不会由 `platform setting get` 返回） | Y/N |
| `--force` | 跳过确认提示 | - |
| `--output` | 输出格式 (table\|json) | table |

**注意：** 至少需要提供一个设置选项。

### 示例

```bash
# 更新单个设置
<CLI> platform setting update --channel-concurrences-enabled Y

# 更新多个设置
<CLI> platform setting update \
  --channel-concurrences-enabled Y \
  --timely-convert-enabled Y \
  --donate-enabled N

# 更新封面图片类型
<CLI> platform setting update --cover-img-type contain

# JSON格式输出
<CLI> platform setting update --donate-enabled Y -o json
```

### 错误处理

| 错误情况 | 错误信息 |
|----------|----------|
| 无参数提供 | `至少需要提供一个参数 (At least one parameter is required)` |
| Y/N值无效 | `xxx 必须是 Y 或 N` |
| 封面类型无效 | `coverImgType 必须是 contain 或 cover` |

---

## API 映射

- [身份认证配置](authentication.md)
- [频道管理](channel-management.md)
- [录制设置](record-settings.md)
