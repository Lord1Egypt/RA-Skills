---
name: huazhuhelper
description: 查询华住酒店列表。通过华住OpenAPI获取酒店数据，需要用户提供clientId和clientSecret进行OAuth2认证。当用户提到华住酒店、酒店列表、华住API、查酒店时使用。
---

# 华住酒店列表查询

查询华住OpenAPI的酒店列表，自动处理OAuth2认证和Token管理。

## 前置条件

向用户询问以下信息（必需）：
- **clientId**: 华住分配的客户端ID
- **clientSecret**: 华住分配的客户端密钥
- **distributorId**: 渠道Code（默认 MEITUAN，可选）

## 工作流程

### Step 1: 安装依赖

```bash
pip install requests
```

### Step 2: 确认环境

- 测试环境（默认）: `https://test-oauth2-api.huazhu.com`
- 生产环境: `https://openapi.huazhu.com`

### Step 3: 运行查询脚本

在用户项目根目录执行以下 Python 代码（将凭证替换为用户提供的真实值）：

```python
import base64, time, uuid, requests

# === 用户凭证 ===
CLIENT_ID = "用户提供的clientId"
CLIENT_SECRET = "用户提供的clientSecret"
DISTRIBUTOR_ID = "MEITUAN"
IS_TEST = True

# === Step 1: 获取 Token ===
auth_domain = "https://test-oauth2-api.huazhu.com" if IS_TEST else "https://openapi.huazhu.com"
biz_domain = "http://test-crs-distributor.huazhu.com" if IS_TEST else "https://openapi.huazhu.com"

raw_cred = f"{CLIENT_ID}:{CLIENT_SECRET}"
basic_auth = f"Basic {base64.b64encode(raw_cred.encode()).decode()}"

headers = {
    "Authorization": basic_auth,
    "Content-Type": "application/x-www-form-urlencoded",
}
if IS_TEST:
    headers["X-Lane-Tag"] = "preview"

resp = requests.post(
    f"{auth_domain}/oauth/token",
    data={"scope": "ALL", "grant_type": "client_credentials"},
    headers=headers,
    timeout=10,
)
resp.raise_for_status()
token = resp.json()["access_token"]
print(f"Token: {token[:20]}...")

# === Step 2: 查询酒店列表 ===
hotel_headers = {
    "Authorization": f"Bearer {token}",
    "distributorId": DISTRIBUTOR_ID,
    "timestamp": str(int(time.time() * 1000)),
    "traceId": str(uuid.uuid4()),
}

resp = requests.get(f"{biz_domain}/hotels", headers=hotel_headers, timeout=10)
resp.raise_for_status()
data = resp.json()

hotels = data if isinstance(data, list) else data.get("content", data.get("data", []))
print(f"共 {len(hotels)} 个酒店:")
for i, h in enumerate(hotels[:20], 1):
    print(f"  {i}. {h.get('hotelName','')} (ID: {h.get('hotelId','')})")
if len(hotels) > 20:
    print(f"  ... 还有 {len(hotels)-20} 个")
```

## 使用本项目模块

本 Skill 安装后，脚本位于 `{baseDir}/scripts/` 目录下。

### 方式一：直接使用模块（推荐）

```python
import sys
sys.path.insert(0, "{baseDir}/scripts")

from huazhuhelper_auth import HuazhuhelperAuth
from huazhuhelper_hotel import HuazhuhelperHotel

# distributor_id 默认为 MEITUAN，可省略
auth = HuazhuhelperAuth(
    client_id="用户的clientId",
    client_secret="用户的clientSecret",
    is_test=True,
)
hotel = HuazhuhelperHotel(auth)
hotels = hotel.get_hotel_list()
for h in hotels:
    print(h.get("hotelName"), h.get("hotelId"))
```

其中 `{baseDir}` 是 Skill 安装后的根目录，通常为 `~/.openclaw/skills/huazhuhelper`。

### 方式二：直接复制脚本代码

如果不想安装 Skill，可以直接复制以下两个脚本文件的内容到您的项目中：

#### 脚本1: huazhuhelper_auth.py（认证模块）

```python
"""华住OpenAPI认证模块 - 获取access_token"""

import base64
import time
import requests


class HuazhuhelperAuth:
    """华住认证客户端"""

    def __init__(self, client_id: str, client_secret: str,
                 distributor_id: str = "MEITUAN", is_test: bool = True):
        """
        Args:
            client_id: 客户端ID（从华住申请）
            client_secret: 客户端密钥（从华住申请）
            distributor_id: 渠道Code（默认 MEITUAN）
            is_test: 是否测试环境
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.distributor_id = distributor_id
        self.is_test = is_test
        self.auth_domain = "https://test-oauth2-api.huazhu.com" if is_test else "https://openapi.huazhu.com"
        self._token = None
        self._expires_at = 0

    def _basic_auth(self) -> str:
        """将 clientId:clientSecret 进行Base64编码"""
        raw = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(raw.encode()).decode()
        return f"Basic {encoded}"

    def get_token(self) -> str:
        """获取access_token（自动缓存，到期前120秒刷新）"""
        if self._token and time.time() < self._expires_at - 120:
            return self._token

        headers = {
            "Authorization": self._basic_auth(),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if self.is_test:
            headers["X-Lane-Tag"] = "preview"

        resp = requests.post(
            f"{self.auth_domain}/oauth/token",
            data={"scope": "ALL", "grant_type": "client_credentials"},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        if "access_token" not in data:
            raise Exception(f"获取token失败: {data}")

        self._token = data["access_token"]
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return self._token
```

#### 脚本2: huazhuhelper_hotel.py（酒店查询模块）

```python
"""华住OpenAPI酒店查询模块"""

import time
import uuid
import requests
from huazhuhelper_auth import HuazhuhelperAuth


class HuazhuhelperHotel:
    """华住酒店查询客户端"""

    def __init__(self, auth: HuazhuhelperAuth,
                 biz_domain: str = "http://test-crs-distributor.huazhu.com"):
        self.auth = auth
        self.biz_domain = biz_domain

    def get_hotel_list(self) -> list:
        """
        获取酒店列表

        Returns:
            list[dict]，每个元素包含 hotelId、hotelName 等字段
        """
        token = self.auth.get_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "distributorId": self.auth.distributor_id,
            "timestamp": str(int(time.time() * 1000)),
            "traceId": str(uuid.uuid4()),
        }

        resp = requests.get(f"{self.biz_domain}/hotels", headers=headers, timeout=10)
        if not resp.ok:
            raise Exception(
                f"酒店列表请求失败 [HTTP {resp.status_code}]: {resp.text}"
            )
        data = resp.json()

        if isinstance(data, list):
            return data

        code = data.get("code")
        if code and code != 1000:
            raise Exception(f"API错误 [code={code}]: {data.get('message', '未知错误')}")

        return data.get("content", data.get("data", []))
```

#### 使用示例

将以上两个脚本保存为 `huazhuhelper_auth.py` 和 `huazhuhelper_hotel.py`，然后：

```python
from huazhuhelper_auth import HuazhuhelperAuth
from huazhuhelper_hotel import HuazhuhelperHotel

# 创建认证实例（distributor_id 默认为 MEITUAN）
auth = HuazhuhelperAuth(
    client_id="573d8245-5ec0-4172-92aa-5e1a8de1e507",
    client_secret="您的clientSecret",
    is_test=True  # 测试环境设为True，生产环境设为False
)

# 查询酒店列表
hotel_client = HuazhuhelperHotel(auth)
hotels = hotel_client.get_hotel_list()

print(f"共查询到 {len(hotels)} 个酒店")
for h in hotels[:10]:  # 显示前10个
    print(f"  - {h.get('hotelName')} (ID: {h.get('hotelId')})")
```

## API 请求头说明

### 获取 Token
| 头 | 值 | 说明 |
|---|---|---|
| Authorization | `Basic {base64(clientId:secret)}` | clientId:secret 的 Base64 编码 |
| Content-Type | `application/x-www-form-urlencoded` | - |
| X-Lane-Tag | `preview` | 仅测试环境需要 |

### 查询酒店
| 头 | 值 | 说明 |
|---|---|---|
| Authorization | `Bearer {token}` | 上一步获取的token |
| distributorId | 渠道Code | 如 MEITUAN |
| timestamp | 毫秒时间戳 | 自动生成 |
| traceId | UUID | 自动生成 |

## 错误处理

- **401**: clientId 或 clientSecret 错误
- **403**: IP 不在白名单，需联系华住添加
- **Token过期**: 重新执行 Step 1 获取新 token
