---
name: jf-open-pro-ai-smart-search
description: JF Tech Pro AI 智搜技能。根据语义内容（如"带帽子的人"、"车"、"狗"）搜索杰峰云存报警视频，获取匹配的视频片段列表。使用场景：智能视频检索、AI 事件搜索、语义化视频查找。

# 必需凭证声明 - 平台元数据
credentials:
  required:
    - name: JF_UUID
      type: string
      description: 杰峰开放平台用户唯一标识
      source: https://open.jftech.com/
    - name: JF_APPKEY
      type: string
      description: 杰峰开放平台应用 Key
      source: https://open.jftech.com/
    - name: JF_APPSECRET
      type: string
      description: 杰峰开放平台应用密钥
      source: https://open.jftech.com/
    - name: JF_MOVECARD
      type: integer
      description: 签名算法偏移量 (0-9)
      source: https://open.jftech.com/
  optional:
    - name: JF_SN
      type: string
      description: 设备序列号
    - name: JF_USER
      type: string
      description: 用户 ID
      default: admin
    - name: JF_ENDPOINT
      type: string
      description: API 端点
      default: api.jftechws.com

# 网络端点声明
endpoints:
  - url: https://api.jftechws.com
    description: 杰峰官方 API (国际)
  - url: https://api-cn.jftech.com
    description: 杰峰官方 API (中国大陆)

# 安全声明
security:
  credentials_required: true
  env_vars_only: true  # 凭据仅通过环境变量读取
  language: python  # Python 脚本
  network_access:
    - api.jftechws.com  # 杰峰官方 API (国际)
    - api-cn.jftech.com  # 杰峰官方 API (中国大陆)
  file_access: none  # 不读取本地文件
---

# JF Open Pro AI Smart Search

> **面向开发者杰峰 AI 智搜工具 (Python)**
> 
> 根据语义内容搜索杰峰云存报警视频，获取匹配的视频片段列表及播放信息。

---

## 🔒 安全说明

**凭据存储：仅支持环境变量**

| 方式 | 支持 | 说明 |
|------|------|------|
| **环境变量** | ✅ 支持 | 推荐方式，避免凭据出现在进程列表或日志中 |
| **命令行参数** | ❌ 不支持 | 避免凭据泄露风险 |
| **配置文件** | ❌ 不支持 | 避免明文存储凭据 |

**网络访问：**
- ✅ 仅访问杰峰官方 API 端点 (`api.jftechws.com` / `api-cn.jftech.com`)
- ❌ 不访问第三方服务
- ❌ 不读取本地文件系统

**脚本行为：**
- ✅ 本地执行 Python 脚本（技能本身）
- ✅ 仅向指定的杰峰 API 端点发起 HTTPS 请求
- ❌ 不执行外部命令
- ❌ 不读取敏感系统文件

---

## 🚀 快速开始

### 设置环境变量

```bash
export JF_UUID="your-uuid"              # 开放平台用户唯一标识
export JF_APPKEY="your-appkey"          # 开放平台应用 Key
export JF_APPSECRET="your-appsecret"    # 开放平台应用密钥
export JF_MOVECARD=5                    # 签名算法偏移量 (0-9)
export JF_SN="your-device-sn"           # 设备序列号
export JF_USER="admin"                  # 用户 ID（可选，默认：admin）
```

### 使用技能

```bash
# AI 智搜 - 搜索"人"相关的视频
python scripts/search_video.py --search "人"

# AI 智搜 - 搜索"车"相关的视频
python scripts/search_video.py --search "车"

# AI 智搜 - 搜索"狗"相关的视频
python scripts/search_video.py --search "狗"

# AI 智搜 - 搜索"戴帽子的人"
python scripts/search_video.py --search "戴帽子的人"

# 获取云存回放地址（指定时间）
python scripts/get_playback_url.py --start-time "2026-04-07 12:00:00" --stop-time "2026-04-07 12:45:00"

# 完整流程：AI 智搜 + 播放地址（推荐）
python scripts/ai_search_playback.py --search "人" --video-index 0
```

---

## 📋 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `JF_UUID` | 开放平台用户唯一标识 | 是 | - |
| `JF_APPKEY` | 开放平台应用 Key | 是 | - |
| `JF_APPSECRET` | 开放平台应用密钥 | 是 | - |
| `JF_MOVECARD` | 签名算法偏移量 (0-9)，用于时间戳偏移增加签名安全性 | 是 | - |
| `JF_SN` | 设备序列号 | 是 | - |
| `JF_USER` | 用户 ID | 否 | `admin` |
| `JF_ENDPOINT` | API 端点 | 否 | `api.jftechws.com` |

---

## 🛠️ 功能

### 1. AI 智搜视频

根据语义内容搜索 AI 标记的云存报警视频。

**支持的搜索类型：**

| 搜索类型 | 示例查询 | 说明 |
|----------|----------|------|
| 人物 | "人"、"戴帽子的人"、"穿红色衣服的人" | 基于人形 + 属性检测 |
| 车辆 | "车"、"白色轿车"、"卡车" | 基于车辆检测 |
| 动物 | "狗"、"猫" | 基于动物检测 |
| 行为 | "跑步的人"、"摔倒" | 基于行为分析 |

**使用示例：**

```bash
# 搜索"人"相关的视频
python scripts/search_video.py --search "人"

# 搜索"车"相关的视频
python scripts/search_video.py --search "车"

# 搜索"戴帽子的人"
python scripts/search_video.py --search "戴帽子的人"
```

**返回字段说明：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `st` | 录像开始时间（秒） | 1703275200 |
| `et` | 录像结束时间（秒） | 1703275260 |
| `matchRate` | 匹配度（0-1） | 0.95 |
| `queryTags` | 检测到的标签列表 | ["person", "hat"] |
| `eventTime` | 事件触发时间 | "2024-12-23 10:00:00" |

---

### 2. 云存回放地址获取

获取云存报警视频回放/播放地址。

**使用示例：**

```bash
# 指定时间范围获取回放地址
python scripts/get_playback_url.py --start-time "2026-04-07 12:00:00" --stop-time "2026-04-07 12:45:00"

# 完整流程：AI 智搜 + 播放地址（推荐）
python scripts/ai_search_playback.py --search "人" --video-index 0
```

**工作流程：**

```
1. AI 智搜搜索视频
   ↓
   获取云存报警信息视频列表
   ↓
2. 选择目标视频
   ↓
   提取 st（开始时间）和 et（结束时间）
   ↓
3. 调用云存报警视频回放 API
   ↓
   st 对应 startTime
   et 对应 stopTime
   ↓
4. 获取播放链接
```

---

## 📖 使用场景示例

### 场景 1: 搜索特定人员的活动记录

```bash
# 搜索"人"相关的视频
python scripts/search_video.py --search "人"

# 查看返回结果，选择感兴趣的视频片段
# 使用返回的 st 和 et 获取回放地址
python scripts/get_playback_url.py --start-time "2026-04-07 12:00:00" --stop-time "2026-04-07 12:45:00"
```

### 场景 2: 搜索车辆进出记录

```bash
# 搜索"车"相关的视频
python scripts/search_video.py --search "车"
```

### 场景 3: 完整流程 - 搜索并播放

```bash
# 一步完成：搜索"人"并获取第一个视频的回放地址
python scripts/ai_search_playback.py --search "人" --video-index 0
```

---

## ⚠️ 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `2000` | 成功 | - |
| `12504` | 授权失败 - 设备未开通 AI 智搜套餐 | 登录开放平台为设备绑定 AI 智搜套餐卡 |
| `10001` | 参数错误 | 检查请求参数格式 |
| `10002` | 签名失败 | 检查 appKey/appSecret 和时间戳 |

### 错误码 12504 处理

**错误信息：** `authorize failed, Please check it in the open platform`

**原因：** 设备未开通 AI 智搜服务，或未绑定套餐卡

**解决步骤：**

1. 登录杰峰开放平台：https://developer.jftech.com
2. 进入 **套餐管理** / **服务管理**
3. 找到 **AI 智搜** 或 **云存视频搜索** 套餐
4. 为设备购买并绑定套餐卡
5. 等待配置生效（通常 1-5 分钟）
6. 重新调用 API 测试

---

## ⚠️ 注意事项

1. **设备需开通云存服务** - AI 智搜需要云存套餐支持
2. **设备需开通 AI 智搜套餐** - 需在开放平台绑定套餐卡
3. **时间范围** - 只能搜索云存有效期内的视频
4. **搜索精度** - 受 AI 算法识别精度影响

---

## 📚 官方参考资料

- **杰峰开放平台**: https://open.jftech.com/
- **API 文档**: https://docs.jftech.com/
- **AI 智搜文档**: https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557
- **API 端点**: `api.jftechws.com` (国际) / `api-cn.jftech.com` (中国大陆)

---

## 📁 脚本工具

**可用脚本：**

| 脚本 | 功能 |
|------|------|
| `search_video.py` | AI 智搜 - 搜索云存报警视频 |
| `get_playback_url.py` | 获取云存回放地址（指定时间或完整流程） |
| `ai_search_playback.py` | 完整流程 - AI 智搜 + 播放地址一键获取 |

```bash
# 获取帮助
python scripts/search_video.py --help
python scripts/get_playback_url.py --help
python scripts/ai_search_playback.py --help

# AI 智搜
python scripts/search_video.py --search <搜索内容>

# 获取回放地址（指定时间）
python scripts/get_playback_url.py --start-time "YYYY-MM-DD HH:MM:SS" --stop-time "YYYY-MM-DD HH:MM:SS"

# 完整流程：AI 智搜 + 播放地址（推荐）
python scripts/ai_search_playback.py --search <搜索内容> --video-index <索引>
```

脚本路径：`scripts/search_video.py`, `scripts/get_playback_url.py`, `scripts/ai_search_playback.py`

---

**技能版本：** v1.0.0  
**语言：** Python  
**最后更新：** 2026-04-07
