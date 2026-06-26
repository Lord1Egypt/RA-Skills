# 日志易 (LogEase) 搜索工具

通过日志易平台搜索各类日志数据，支持安全告警分析、网络设备日志、系统日志等多种场景。

## 连接信息

- **API 地址**: `http://10.20.51.16`
- **认证方式**: HTTP BasicAuth
- **用户名**: `admin`
- **密码**: `MIma@sec2025`
- **搜索 API**: `GET /api/v3/search/sheets/`
- **索引**: `yotta`（默认）

## 搜索脚本

- **路径**: `scripts/logeasy_search.py`
- **用法**:
  ```bash
  python logeasy_search.py "query" --time 1h --limit 100
  python logeasy_search.py "appname:sip alarm" --time 12h --limit 50
  ```
- **参数**: `--time` (1h/24h/7d/30m), `--limit` (条数，默认100), `--index` (默认yotta), `--raw` (原始JSON)

## ⚠️ 重要限制

### 时间格式
- ✅ **唯一可用**: `time_range=now-1h,now`（相对时间）
- ❌ ISO格式 → 返回0条
- ❌ 时间戳格式 → 返回0条

### 返回条数
- API 硬限制返回 **100 条**（不管 limit 设多少）
- 聚合查询（`| top`）不受 limit 限制，可统计全量分布
- 统计用聚合，详情用原始查询（最多100条样本）

### 内容审核
- 大量原始告警内容可能触发 `data_inspection_failed` 500 错误
- 触发后减少单次查询的数据量或分批查询

## 已知日志源

| 日志源 | 查询条件 | 关键字段 | 说明 |
|--------|----------|----------|------|
| **SIP 态势感知** | `appname:sip` | sip.attack_ip, sip.suffer_ip, sip.attack_type_name 等 | 安全告警，详见 logeasy-sip skill |
| **飞廉** | `logtype:feilian` | feilian.content.client_ip, feilian.content.connection_ip | VPN/连接日志 |
| **H3C 交换机** | `appname:switch tag:h3c_newbase` | raw_message（非结构化） | 交换机 syslog |
| **日志易自身** | `appname:rizhiyi` | remote_addr | 系统日志 |
| **其他网络设备** | `appname:switch` | raw_message | 各类交换机/路由器 |

## 查询模板

### SIP 安全告警（用 logeasy-sip skill）
```bash
# 所有 SIP 告警
python logeasy_search.py "appname:sip alarm" --time 12h --limit 50

# 攻击成功的高危告警
python logeasy_search.py "appname:sip sip.attack_state:1" --time 1h --limit 20
```

### H3C 交换机日志
```bash
# 所有 H3C 交换机日志
python logeasy_search.py "appname:switch tag:h3c_newbase" --time 12h --limit 100

# 特定告警类型（ARP冲突、风扇异常等）
python logeasy_search.py "appname:switch tag:h3c_newbase ARP_SENDER_IPCONFLICT" --time 12h --limit 20

# 特定设备
python logeasy_search.py "appname:switch tag:h3c_newbase hostname:10.5.1.43" --time 1h --limit 20
```

### 飞廉日志
```bash
# 飞廉连接日志
python logeasy_search.py "logtype:feilian" --time 1h --limit 20

# 特定客户端IP
python logeasy_search.py "logtype:feilian client_ip:10.45.123.44" --time 1h --limit 20
```

### 通用搜索
```bash
# 关键词搜索（全文匹配）
python logeasy_search.py "关键词" --time 1h --limit 20

# 按主机搜索
python logeasy_search.py "hostname:10.20.51.11" --time 1h --limit 20

# 字段搜索（部分字段支持）
python logeasy_search.py "appname:sip sip.suffer_ip:10.10.185.8" --time 1h --limit 20
```

## 聚合查询模板

聚合查询用于全量统计，不受 100 条限制：

```python
# 按攻击类型分布
search("appname:sip sip.attack_type_name:* | top sip.attack_type_name", time_range="now-12h,now")

# 按主机分布
search("appname:switch tag:h3c_newbase hostname:* | top hostname", time_range="now-12h,now")

# 按日志级别分布
search("appname:switch tag:h3c_newbase %%*/*/* | ...", time_range="now-12h,now")
```

## H3C 交换机日志分析要点

### 日志格式
```
<priority>Mar 25 11:45:52 2026 设备名 %%模块/级别/事件: 事件详情
```
- **priority**: syslog 优先级
- **设备名**: 如 `ITC-C15-U16-Border-Leaf-1`、`DMZ-C13-U38-10G-ASW-2`
- **模块**: 如 `ARP`（ARP事件）、`DEV`（设备）、`SEC`（安全）

### 常见告警类型
| 告警关键词 | 严重度 | 说明 |
|------------|--------|------|
| `ARP_SENDER_IPCONFLICT` | ⚠️ 中 | ARP发送者IP冲突 |
| `DUPIFIP` | ⚠️ 中 | 重复地址检测 |
| `FAN_DIRECTION_NOT_PREFERRED` | ℹ️ 低 | 风扇方向非首选 |
| `LINK_UPDOWN` | ⚠️ 中 | 链路上下行变化 |
| `CPU_HIGH` | 🔴 高 | CPU使用率过高 |

### 已知设备清单
- 核心交换机：10.5.1.11（日志量最大）
- 边界交换机：10.5.1.43（ITC-C15-U16-Border-Leaf-1）
- DMZ 区域：10.5.1.51/52（DMZ-C12/C13）
- STM 区域：10.5.2.23/24（STM-D01/D02）

## Python 调用模板

```python
import urllib.request, urllib.parse, json, sys, base64

sys.stdout.reconfigure(encoding='utf-8')

USER = 'admin'
PASS = 'MIma@sec2025'
CRED = base64.b64encode(f'{USER}:{PASS}'.encode()).decode()
HEADERS = {'Authorization': f'Basic {CRED}'}
BASE = 'http://10.20.51.16/api/v3/search/sheets/'

def search(query, time_range='now-1h,now', limit=100):
    """搜索日志"""
    url = f'{BASE}?query={urllib.parse.quote(query)}&time_range={urllib.parse.quote(time_range)}&index_name=yotta&limit={limit}'
    req = urllib.request.Request(url, headers=HEADERS)
    resp = urllib.request.urlopen(req, timeout=60)
    return json.loads(resp.read())

def count(query, time_range='now-1h,now'):
    """计数"""
    r = search(query, time_range, limit=1)
    return r.get('results', {}).get('total_hits', 0)
```

## 踩坑记录

1. **字段搜索不一定有效**: `client_ip:10.x.x.x` 这类字段搜索可能返回0条，用关键词搜索代替
2. **搜索日志污染**: 每次搜索操作会被日志易自身记录，大量搜索后分析需排除 appname:rizhiyi
3. **PowerShell 环境**: 命令连接符用 `;` 不要用 `&&`，多行代码写文件再执行
4. **event_type 字段不存在**: SIP 日志没有结构化 event_type，用 `alarm` 关键字全文匹配
5. **飞廉字段需前缀**: 飞廉关键字段需要 `feilian.content.` 前缀，如 `feilian.content.client_ip`
6. **攻击源IP字段**: SIP 用 `sip.attack_ip`（不是 `sip.ip`，sip.ip 是探针自身IP）
