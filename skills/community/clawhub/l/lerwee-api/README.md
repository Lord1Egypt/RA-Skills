# Lerwee API Skill

乐维运维监控平台 API 集成技能。

## 功能特性

- ✅ 完整的 API 端点封装
- ✅ 自动签名生成
- ✅ 监控对象管理
- ✅ 告警查询
- ✅ 事件查询
- ✅ 用户管理
- ✅ Agent 管理

## 快速开始

### 配置

编辑 `references/config.json`：

```json
{
  "base_url": "http://192.168.1.79:8081/api/v6",
  "secret": "",
  "admin": {
    "username": "admin",
    "password": "ITIM_p@ssw0rd"
  }
}
```

### 使用 Python 客户端

```python
from scripts.lerwee_api import LerweeAPI

# 初始化客户端
api = LerweeAPI(
    base_url='http://192.168.1.79:8081/api/v6',
    secret=''
)

# 获取监控对象列表
hosts = api.get_host_list(keyword='linux', page=1, page_size=10)
print(hosts)

# 获取告警列表
alarms = api.get_alarm_list(page=1, page_size=20)
print(alarms)
```

### 测试签名生成

```bash
cd /home/node/.openclaw/workspace/skills/lerwee-api
python3 scripts/sign_test.py
```

## API 模块

| 模块 | 说明 |
|------|------|
| 监控中心 | 监控对象管理、资源查询 |
| 设备探测 | Agent 管理、设备发现 |
| 告警管理 | 告警查询、问题管理 |
| 事件平台 | 事件查询、AI 告警 |
| 用户管理 | 用户列表、用户详情 |

## 文档

- `SKILL.md` - 完整技能文档
- `references/api_endpoints.md` - API 端点列表
- `references/monitoring_types.md` - 监控类型对照表
- `references/error_codes.md` - 错误码详解

## 脚本

- `scripts/lerwee_api.py` - Python API 客户端
- `scripts/sign_test.py` - 签名测试工具

## 签名算法

1. 将请求参数按字母顺序排序（排除 `sign` 字段）
2. 拼接: `key1value1key2value2...` (无等号，无分隔符)
3. 加密钥前缀: `secret + 参数串`
4. SHA1 加密转小写

示例:
```
参数: { aa: 111, bb: 222, timestamp: 1654825429 }
排序: aa, bb, timestamp
拼接: aa111bb222timestamp1654825429
加前缀: aa111bb222timestamp1654825429
签名: 5bb575edea620452d3b03ccefaf76c9bdd8241a2
```

## 注意事项

1. 所有 API 请求使用 POST 方法
2. 请求头必须设置为 `Content-Type: application/json`
3. 所有请求必须包含 `timestamp` 和 `sign` 参数
4. 时间戳使用 Unix 时间戳（秒）
5. 签名计算时跳过 `sign` 字段本身、空值和数组类型参数
