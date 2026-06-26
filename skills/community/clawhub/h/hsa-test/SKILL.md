---
name: ezviz-restaurant-inspection
description: 萤石餐饮行业智能巡检技能。通过设备抓图 + 智能体分析接口，实现对餐厅/厨房场景的 AI 巡检，包括地面卫生、动火离人、垃圾桶状态、货品存放和口罩佩戴等关键指标。
metadata:
  openclaw:
    emoji: "🍽️"
    requires: { "env": ["EZVIZ_APP_KEY", "EZVIZ_APP_SECRET", "EZVIZ_DEVICE_SERIAL", "EZVIZ_AGENT_ID"], "pip": ["requests"] }
    primaryEnv: "EZVIZ_APP_KEY"
---

# Ezviz Restaurant Inspection (萤石餐饮智能巡检)

通过萤石设备抓图 + 智能体分析接口，实现对餐饮场所的 AI 智能巡检。

## 快速开始

### 安装依赖

```bash
pip install requests
```

### 设置环境变量

```bash
export EZVIZ_APP_KEY="your_app_key"
export EZVIZ_APP_SECRET="your_app_secret"
export EZVIZ_DEVICE_SERIAL="dev1,dev2,dev3"
export EZVIZ_AGENT_ID="your_agent_id"
```

可选环境变量：
```bash
export EZVIZ_CHANNEL_NO="1" # 通道号，默认 1
export EZVIZ_ANALYSIS_TEXT="请对这张餐饮场所图片进行智能巡检，重点关注：1.地面卫生（污渍、积水、垃圾）2.动火离人（厨房明火无人看管）3.垃圾桶状态（是否盖紧盖子）4.货品存放（食品/原料是否离地存放）5.口罩佩戴（员工口罩佩戴合规性）。请按风险等级分类输出结果，动火离人属于高危告警。"
```

**注意**: 不需要设置 `EZVIZ_ACCESS_TOKEN`！技能会自动获取 Token（每次运行自动获取）。

### 运行

```bash
python3 {baseDir}/scripts/restaurant_inspection.py
```

命令行参数：
```bash
# 单个设备
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret dev1 1 agentId

# 多个设备（逗号分隔）
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret "dev1,dev2,dev3" 1 agentId

# 自定义分析提示词
python3 {baseDir}/scripts/restaurant_inspection.py appKey appSecret dev1 1 agentId "请检查厨房安全：地面清洁、明火监管、垃圾桶密封、食材存放规范、员工防护"
```

## 工作流程

```
1. 获取 Token (appKey + appSecret → accessToken)
 ↓
2. 设备抓图 (accessToken + deviceSerial → picUrl)
 ↓
3. AI 分析 (使用accessToken + appId + 图片URL + 提示词 → 巡检结果)
 ↓
4. 输出结果 (JSON + 控制台)
```

## Token 自动获取说明

**你不需要手动获取或配置 `EZVIZ_ACCESS_TOKEN`！**

技能会自动处理 Token 的获取：

```
每次运行:
 appKey + appSecret → 调用萤石 API → 获取 accessToken (有效期 7 天)
 ↓
使用 Token 完成抓图和AI分析请求
 ↓
Token 在内存中使用，不保存到磁盘
```

**Token 管理特性**:
- ✅ **自动获取**: 每次运行自动调用萤石 API 获取
- ✅ **有效期 7 天**: 获取的 Token 7 天内有效
- ✅ **无需配置**: 不需要手动设置 `EZVIZ_ACCESS_TOKEN` 环境变量
- ✅ **安全**: Token 不写入日志，不保存到磁盘
- ⚠️ **注意**: 每次运行会重新获取 Token（不跨运行缓存）

## 输出示例

```
======================================================================
Ezviz Restaurant Inspection Skill (萤石餐饮智能巡检)
======================================================================
[Time] 2026-03-16 15:30:00
[INFO] Target devices: 2
 - kitchen_cam (Channel: 1)
 - dining_area (Channel: 1)
[INFO] Agent ID: 98af3e...
[INFO] Analysis: 请对这张餐饮场所图片进行智能巡检...

======================================================================
[Step 1] Getting access token...
[SUCCESS] Token obtained, expires: 2026-03-23 15:30:00

======================================================================
[Step 2] Capturing and analyzing images...
======================================================================

[Device] kitchen_cam (Channel: 1)
[SUCCESS] Image captured: https://opencapture.ys7.com/...
[SUCCESS] Analysis completed!

[Inspection Result]
{
  "高危告警": ["动火离人：检测到灶台明火但无人看管"],
  "一般问题": ["地面卫生：发现地面有积水", "垃圾桶状态：垃圾桶未盖紧"],
  "合规项": ["货品存放：食材已离地存放", "口罩佩戴：员工均正确佩戴口罩"]
}

======================================================================
INSPECTION SUMMARY
======================================================================
 Total devices: 2
 Success: 2
 Failed: 0
 High Risk: 1
 Medium Risk: 2
======================================================================
```

## 多设备格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 单设备 | `dev1` | 默认通道 1 |
| 多设备 | `dev1,dev2,dev3` | 全部使用默认通道 |
| 指定通道 | `dev1:1,dev2:2` | 每个设备独立通道 |
| 混合 | `dev1,dev2:2,dev3` | 部分指定通道 |

## API 接口

| 接口 | URL | 文档 |
|------|-----|------|
| 获取 Token | `POST /api/lapp/token/get` | https://open.ys7.com/help/81 |
| 设备抓图 | `POST /api/lapp/device/capture` | https://open.ys7.com/help/687 |
| 智能体分析 | `POST /api/service/open/intelligent/agent/engine/agent/anaylsis` | https://open.ys7.com/help/5006 |

## 网络端点

| 域名 | 用途 |
|------|------|
| `open.ys7.com` | 萤石开放平台 API（Token、抓图） |
| `aidialoggw.ys7.com` | 萤石 AI 智能体分析接口 |

## 巡检内容说明

| 巡检项 | 检测要点 | 风险等级 |
|--------|----------|----------|
| 地面卫生 | 识别污渍、积水、垃圾 | 中风险 |
| 动火离人 | 监测厨房明火无人看管 | **高危告警** |
| 垃圾桶状态 | 检测是否盖紧盖子 | 中风险 |
| 货品存放 | 检查食品/原料是否离地存放 | 中风险 |
| 口罩佩戴 | 记录员工口罩佩戴合规性 | 低风险 |

## 分析提示词优化

**默认提示词**:
"请对这张餐饮场所图片进行智能巡检，重点关注：1.地面卫生（污渍、积水、垃圾）2.动火离人（厨房明火无人看管）3.垃圾桶状态（是否盖紧盖子）4.货品存放（食品/原料是否离地存放）5.口罩佩戴（员工口罩佩戴合规性）。请按风险等级分类输出结果，动火离人属于高危告警。"

**自定义提示词建议**:
- **厨房专项**: "重点检查厨房区域的安全隐患：明火监管、地面防滑、食材存储规范"
- **用餐区专项**: "检查用餐区域的卫生状况：桌面清洁、地面垃圾、员工服务规范"
- **全面巡检**: "进行全面的食品安全巡检，按HACCP标准评估各关键控制点"

## 注意事项

⚠️ **频率限制**: 萤石抓图接口建议间隔 4 秒以上，频繁调用可能触发限流（错误码 10028）

⚠️ **隐私合规**: 使用摄像头监控可能涉及隐私问题，确保符合当地法律法规

⚠️ **Token 安全**: Token 仅在内存中使用，不写入日志，不发送到非萤石端点

⚠️ **分析超时**: AI 分析可能耗时较长，默认超时 60 秒

## 数据流出说明

**本技能会向第三方服务发送数据**：

| 数据类型 | 发送到 | 用途 | 是否必需 |
|----------|--------|------|----------|
| 摄像头抓拍图片 | `open.ys7.com` (萤石) | AI 智能体分析 | ✅ 必需 |
| appKey/appSecret | `open.ys7.com` (萤石) | 获取访问 Token | ✅ 必需 |
| 设备序列号 | `open.ys7.com` (萤石) | 请求抓图 | ✅ 必需 |
| 智能体 ID | `aidialoggw.ys7.com` (萤石) | AI 分析请求 | ✅ 必需 |
| **EZVIZ_ACCESS_TOKEN** | **自动生成** | **每次运行自动获取** | **✅ 自动** |

**数据流出说明**:
- ✅ **萤石开放平台** (`open.ys7.com`): Token 请求、设备抓图 - 萤石官方 API
- ✅ **萤石 AI 智能体** (`aidialoggw.ys7.com`): 图片分析 - 萤石官方 API  
- ❌ **无其他第三方**: 不会发送数据到其他服务

**凭证权限建议**:
- 使用**最小权限**的 appKey/appSecret
- 仅开通必要的 API 权限（设备抓图、AI 分析）
- 定期轮换凭证
- 不要使用主账号凭证

**本地处理**:
- ✅ Token 在内存中使用，不写入磁盘
- ✅ 不记录完整 API 响应
- ✅ 图片 URL 只显示前 50 字符
- ✅ 不跨运行缓存 Token（每次运行重新获取）

## 应用场景

| 场景 | 说明 |
|------|------|
| 🍳 厨房安全 | 实时监测明火离人、地面湿滑、食材存储 |
| 🍽️ 用餐区域 | 检查桌面清洁、地面卫生、服务规范 |
| 🏪 连锁餐饮 | 多门店统一巡检标准，远程质量管控 |
| 🏢 食堂管理 | 员工食堂食品安全自动化检查 |

## API 调用详情

**AI 智能体分析接口调用格式**:

```bash
curl --location --request POST 'https://aidialoggw.ys7.com/api/service/open/intelligent/agent/engine/agent/anaylsis' \
--header 'accessToken: YOUR_ACCESS_TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "YOUR_AGENT_ID",
    "mediaType": "image",
    "text": "分析提示词",
    "dataType": "url",
    "data": "图片URL"
}'
```

**关键参数说明**:
- `accessToken`: 从萤石API获取的访问令牌（Header中传递）
- `appId`: 智能体ID（原Agent ID）
- `mediaType`: 固定为 "image"
- `dataType`: 固定为 "url" 
- `data`: 图片的完整URL地址
- `text`: 分析提示词