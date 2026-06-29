---
name: mingdata-dmp-auth
description: 明日DMP API凭证管理和统一API调用网关。负责AK/SK凭证的配置、验证和管理，提供统一的API签名生成和HTTP请求封装，作为所有明日DMP技能（人群圈选、人群洞察、人群投放等）的API调用基础设施。
version: 1.0.1
---

# 明日DMP鉴权技能

## 概述

本技能是明日DMP技能体系的**核心基础设施**，提供两大核心功能：

1. **凭证管理**：配置、验证和管理明日DMP的Access Key和Secret Key
2. **统一API调用**：为所有明日DMP业务技能提供统一的API签名生成和HTTP请求封装

## 架构说明

### 集中式API调用架构

```
┌─────────────────────────────────────────────────────────────┐
│                     明日DMP技能体系                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ 人群圈选技能  │  │ 人群洞察技能  │  │人群投放/同步技能  │ │
│  │              │  │              │  │              │    │
│  │ 业务脚本      │  │ 业务脚本      │  │ 业务脚本      │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │            │
│         └─────────────────┼─────────────────┘            │
│                           │                              │
│                           ▼                              │
│              ┌────────────────────────┐                  │
│              │   mingdata-dmp-auth    │                  │
│              │   (鉴权技能)            │                  │
│              ├────────────────────────┤                  │
│              │ • 凭证管理              │                  │
│              │ • 签名生成              │                  │
│              │ • HTTP请求封装          │                  │
│              │ • 错误处理              │                  │
│              └────────┬───────────────┘                  │
│                       │                                  │
│                       ▼                                  │
│              ┌────────────────────────┐                  │
│              │  明日DMP开放平台API     │                  │
│              └────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### 调用流程

1. **业务技能**调用本技能的scripts/minri_dmp_api.py脚本
2. **鉴权技能**加载凭证、生成签名、发送HTTP请求
3. **返回结果**给业务技能，并设置相应的退出码

## 核心脚本

### 1. setup_credentials.py - 凭证配置脚本

**功能**：引导用户配置Access Key和Secret Key

**使用方式**：
```bash
python setup_credentials.py
```

**交互流程**：
1. 展示凭证申请指引（包含申请入口、申请步骤、凭证格式说明）
2. 提示用户输入Access Key
3. 提示用户输入Secret Key
4. 验证凭证格式（非空检查）
5. 保存凭证到`~/.mingdata_dmp_credentials`
6. 设置文件权限为600（仅所有者可读写）

**退出码**：
- 0：配置成功
- 1：配置失败（用户取消或输入错误）

### 2. scripts/minri_dmp_api.py - 统一API调用模块

**功能**：提供统一的API签名生成和HTTP请求封装

**使用方式**：
```bash
python minri_dmp_api.py <endpoint> <request_body_json>
```

**参数说明**：
- `endpoint`：API路径（如`/audience/manage/list`）
- `request_body_json`：请求体JSON字符串

**示例**：
```bash
# 查询人群列表
python minri_dmp_api.py /audience/manage/list '{"current":1,"pageSize":10}'

# 创建组合人群
python minri_dmp_api.py /audience/manage/combine/create '{"name":"测试人群","trackType":"MOBILE","idTypes":["MD5_IDFA"],"data":[...]}'
```

**核心功能**：

1. **凭证加载**：
   - 从`~/.mingdata_dmp_credentials`读取AK/SK
   - 验证凭证文件存在性和完整性
   - 凭证缺失时返回特定退出码（2），触发业务技能引导用户配置

2. **签名生成**：
   - 生成10位秒级时间戳
   - 生成4位随机数
   - 计算32位大写MD5签名：`MD5(timestamp + randStr + secret_key)`

3. **HTTP请求**：
   - 构建完整URL：`BASE_URL + endpoint + ?ts=<>&randStr=<>&accessKey=<>&sign=<>`
   - 设置请求头：`Content-Type: application/json; charset=UTF-8`
   - 发送POST请求
   - 解析响应结果

4. **错误处理**：
   - 凭证错误：退出码2，提示调用鉴权技能配置
   - HTTP错误：退出码5，输出HTTP状态码和错误信息
   - 网络错误：退出码6，输出网络异常信息
   - API业务错误：退出码4，输出API返回的错误信息
   - 成功：退出码0，输出API返回的完整结果

**退出码说明**：
- 0：API调用成功
- 1：参数错误（缺少必需参数或JSON格式错误）
- 2：凭证不存在或无效（需要调用setup_credentials.py配置）
- 3：鉴权技能未安装（业务技能找不到本技能）
- 4：API返回业务错误（如参数校验失败、人群不存在等）
- 5：HTTP错误（如404、500等）
- 6：网络错误或未知错误

## 技能依赖关系

### 本技能是以下技能的必需依赖

- **明日dmp人群圈选**：所有人群圈选功能都需要通过本技能调用API
- **明日dmp人群洞察**：所有人群洞察功能都需要通过本技能调用API
- **明日dmp人群投放**：所有人群投放功能都需要通过本技能调用API

### 依赖检查机制

业务技能在调用API前会检查本技能是否已安装：

```python
auth_skill_path = Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py"

if not auth_skill_path.exists():
    print("未找到鉴权技能，请先安装mingdata-dmp-auth技能")
    sys.exit(3)
```

## 凭证配置说明

### ✅ 唯一推荐方式：OpenClaw 环境变量

**优势**：
- ✅ **不写本地文件**，凭证不散落在磁盘上
- ✅ **跨 session 共享**，所有对话自动生效
- ✅ **统一管理**，由 OpenClaw 配置中心统一维护
- ✅ **重启生效**，gateway 重启后自动注入

**配置步骤**：

在对话框中告诉 AI：
```
帮我配置 DMP 凭证，AK=你的AK，SK=你的SK
```

AI 会调用 `save-credentials` 命令，并**直接自动执行**以下配置：

```bash
openclaw config set env.DMP_AK "你的AK"
openclaw config set env.DMP_SK "你的SK"
openclaw gateway restart
```

全程对话完成，无需用户手动执行任何命令。

---

### ❌ 不推荐：文件存储（已废弃）

> 旧版本使用 `~/.mingdata_dmp_credentials` 文件存储凭证，已不推荐。
> 鉴权脚本仍兼容读取旧文件（向后兼容），但新用户请使用 OpenClaw 环境变量方式。

**旧版凭证文件格式**（仅供参考）：

```json
{
  "access_key": "your_access_key_here",
  "secret_key": "your_secret_key_here"
}
```

**配置方法**：

```bash
python scripts/minri_dmp_api.py save-credentials <access_key> <secret_key>
```

---

### 凭证加载优先级

系统按以下优先级加载凭证：

| 优先级 | 方式 | 环境变量/路径 | 跨对话共享 |
|--------|------|--------------|-----------|
| **1** | 环境变量（推荐） | `DMP_AK`, `DMP_SK` | ✅ 是 |
| 2 | 环境变量（兼容） | `MINGDATA_ACCESS_KEY`, `MINGDATA_SECRET_KEY` | ✅ 是 |
| 3 | 文件存储 | `~/.mingdata_credentials` | ❌ 否 |

---

### 安全措施

1. **环境变量注入**：推荐使用环境变量，避免明文存储
2. **文件权限**：凭证文件权限设置为600（仅所有者可读写）
3. **隐藏文件**：使用`.`开头的隐藏文件，避免误操作
4. **本地存储**：凭证仅存储在本地，不会上传到云端
5. **集中管理**：所有明日DMP技能共享同一份凭证，避免重复配置

### 凭证申请指引

**申请入口**：
- 登录明日DMP平台：https://open.mingdata.com
- 进入"开放平台" → "API凭证管理"

**申请步骤**：
1. 点击"创建凭证"按钮
2. 填写凭证用途说明
3. 提交申请，等待审核
4. 审核通过后，复制Access Key和Secret Key

**凭证格式**：
- Access Key：32位字符串（示例：`a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`）
- Secret Key：32位字符串（示例：`p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1`）

**安全提示**：
- 请妥善保管您的凭证，不要泄露给他人
- 如发现凭证泄露，请立即在平台上重置凭证
- 定期更换凭证，提高安全性

## 使用示例

### 场景1：首次使用明日DMP技能

```
用户：帮我圈选一个人群
  ↓
业务技能检测到凭证不存在
  ↓
业务技能：检测到您尚未配置明日DMP凭证，正在调用鉴权技能...
  ↓
鉴权技能：展示凭证申请指引，引导用户输入AK/SK
  ↓
用户：输入Access Key和Secret Key
  ↓
鉴权技能：凭证配置成功
  ↓
业务技能：继续执行人群圈选任务
```

### 场景2：凭证已配置，正常调用API

```
用户：查询人群列表
  ↓
业务技能调用鉴权技能的minri_dmp_api.py
  ↓
鉴权技能：加载凭证 → 生成签名 → 发送HTTP请求
  ↓
明日DMP API：返回人群列表数据
  ↓
鉴权技能：输出结果，退出码0
  ↓
业务技能：展示人群列表给用户
```

### 场景3：凭证失效，需要重新配置

```
用户：创建人群
  ↓
业务技能调用鉴权技能的minri_dmp_api.py
  ↓
鉴权技能：加载凭证 → 生成签名 → 发送HTTP请求
  ↓
明日DMP API：返回401认证失败
  ↓
鉴权技能：输出错误信息，退出码4
  ↓
业务技能：检测到认证失败，引导用户重新配置凭证
  ↓
用户：重新输入Access Key和Secret Key
  ↓
业务技能：重试创建人群任务
```

## 技术说明

### API基础配置

- **BASE_URL**：`https://open.mingdata.com/api/open-api`
- **请求方法**：POST
- **请求头**：`Content-Type: application/json; charset=UTF-8`
- **超时时间**：30秒

### 签名算法

```python
def generate_signature(timestamp, rand_str, secret_key):
    """
    签名算法：32位大写MD5(timestamp + randStr + secret_key)
    
    Args:
        timestamp: 10位秒级时间戳
        rand_str: 4位随机数
        secret_key: SK密钥
    
    Returns:
        str: 32位大写MD5签名
    """
    sign_str = f"{timestamp}{rand_str}{secret_key}"
    return hashlib.md5(sign_str.encode()).hexdigest().upper()
```

### URL构建

```
完整URL格式：
https://open.mingdata.com/api/open-api{endpoint}?ts={timestamp}&randStr={rand_str}&accessKey={access_key}&sign={sign}

示例：
https://open.mingdata.com/api/open-api/audience/manage/list?ts=1234567890&randStr=5678&accessKey=a1b2c3d4...&sign=A1B2C3D4...
```

## 版本历史

### v2.0.0（当前版本）- 架构优化版

**重大变更**：
- 新增scripts/minri_dmp_api.py统一API调用模块
- 实现集中式API签名生成和HTTP请求封装
- 所有业务技能通过本技能调用API，不再各自实现鉴权逻辑

**优势**：
- 代码复用：避免每个业务技能重复实现鉴权逻辑
- 集中管理：凭证和API调用逻辑统一维护，降低维护成本
- 安全性提升：凭证管理更加规范，减少泄露风险
- 易于升级：API调用逻辑变更时，只需更新本技能

### v1.0.0 - 初始版本

**功能**：
- 提供凭证配置脚本`setup_credentials.py`
- 提供基础的凭证验证功能

## 常见问题

### Q1：如何重新配置凭证？

A：直接运行`python setup_credentials.py`，输入新的Access Key和Secret Key即可覆盖旧凭证。

### Q2：凭证文件丢失怎么办？

A：业务技能会自动检测凭证缺失，并引导您重新配置。您也可以手动运行`python setup_credentials.py`。

### Q3：多个明日DMP技能需要分别配置凭证吗？

A：不需要。所有明日DMP技能共享同一份凭证（`~/.mingdata_dmp_credentials`），只需配置一次。

### Q4：如何验证凭证是否有效？

A：运行任意明日DMP业务技能（如查询人群列表），如果返回认证失败，说明凭证无效，需要重新配置。

### Q5：本技能可以单独使用吗？

A：可以。您可以直接调用scripts/minri_dmp_api.py脚本测试API调用，但通常建议通过业务技能（人群圈选、人群洞察等）使用。

## 后续规划

- [ ] 支持凭证有效期检查和自动刷新
- [ ] 提供凭证加密存储选项
- [ ] 支持多账号凭证管理
- [ ] 提供API调用日志记录功能
- [ ] 支持API调用频率限制和重试机制