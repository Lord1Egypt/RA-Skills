# 持久化数据 API 全集

> 来源：掘金官方文档 `持久化数据`（https://myquant.cn/docs2/sdk/python/API介绍/持久化数据.html）
> 官方更新时间：2026-10-23
> **SDK 要求：gm ≥ 3.0.191**
> 实测环境：gm-api 3.0.193 / c sdk 3.9.10，2026-11-27 全项通过

---

## 一句话定位

策略运行期间的 **key-value 持久化存储**。用于保存股票池、动态参数、策略级持仓记录等需要**跨 bar、跨进程重启**保留的状态。

> 和 `add_parameter` 的区别：`add_parameter` 是终端 UI 上的参数面板，重启策略会重置；`persist_*` 是真正落盘的数据文件，重启后还在。

---

## 通用约定

| 约定 | 说明 |
|------|------|
| **调用时机** | 允许在策略运行（`init` 初始化 + `run` 运行）**和数据研究场景**调用；非策略运行期间调用将被拒绝 |
| **策略隔离** | 每个策略运行时可绑定并使用 **1 个 bucket**，对应 1 个持久化数据文件 |
| **模式切换** | 同一策略的 1 个 bucket 对应文件**不区分回测（MODE_BACKTEST）与实时（MODE_LIVE）**，切换模式 bucket 不变会访问同一份数据 |
| **返回约定** | 写操作类接口统一返回 `status`，`0` 成功，非 0 失败 |

---

## 错误码

```python
ERR_PERSIST_INIT_ERROR      71001   # Persist组件初始化失败
ERR_PERSIST_NOT_INIT        71002   # Persist组件未初始化
ERR_PERSIST_KEY_ERROR       71003   # KEY太长或为空
ERR_PERSIST_STSTEM_ERROR    71004   # Persist系统错误
ERR_PERSIST_USING           71005   # bucket正在使用中，无法删除
ERR_PERSIST_INIT_ALREADY    71006   # Persist组件已初始化，不能再初始化别的bucket
```

---

## API 清单

| 函数 | 功能 | 返回 |
|------|------|------|
| `persist_init(bucket, is_async=True)` | 初始化并绑定 bucket | int status |
| `persist_set(key, value)` | 写入字符串 | int status |
| `persist_get(key)` | 读取字符串 | str \| None |
| `persist_set_obj(key, value)` | 写入 JSON 可序列化对象 | int status |
| `persist_get_obj(key)` | 读取并反序列化对象 | Any \| None |
| `persist_delete(key)` | 删除指定 key | int status |
| `persist_clear()` | 清空当前 bucket 全部 key | int status |
| `persist_delete_bucket(bucket)` | 删除**非当前绑定**的 bucket | int status |
| `persist_get_all_buckets()` | 查询本地全部 bucket 列表 | list[str] |
| `persist_get_all_keys()` | 查询当前 bucket 全部 key | list[str] |

---

## persist_init — 初始化持久化数据

初始化指定 bucket，限定一个策略运行周期只能操作一个持久化数据。

```python
persist_init(bucket, is_async=True)
```

### 参数

| 参数名 | 类型 | 中文名称 | 必填 | 默认值 | 说明 |
|--------|------|---------|:---:|--------|------|
| `bucket` | str | 持久化数据标识（命名空间） | Y | 无 | 用于定位当前策略的持久化数据文件；初始化成功后当前策略运行周期内绑定并使用该 bucket，后续 set/get/delete/clear 无需再指定 bucket |
| `is_async` | bool | 是否异步持久化 | N | `True` | 见下方说明 |

### is_async 怎么选

- **`True`（默认）**：异步持久化。`persist_set` 立即返回，数据延时几毫秒写入硬盘（取决于硬件性能）。适合**盘中交易时随时写入大量数据**（实时行情、持仓变化、资金变化），避免 `persist_set` 耗时过长阻塞行情与回报处理
- **`False`**：同步持久化。`persist_set` 确保数据已写入硬盘才返回，数据多时总耗时较长。适合**写入数据少**、或**写入后进程需要立即退出**的场景。**策略非实时模式（回测模式与数据查询模式）请设置为 `False`**

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | int | `0` 初始化成功；非 0 失败，对应错误码 |

### 示例

```python
bucket = "strategy_demo"   # 持久化数据标识，同一策略全局唯一

status = persist_init(bucket)
if status == 0:
    print("初始化成功")
else:
    print("初始化失败, 错误码:", status)
```

### 注意事项

1. `persist_init` 必须在策略运行期间调用（`init` 策略初始化阶段），且每个策略运行周期内**只允许初始化 1 个 bucket**；重复初始化同一 bucket **幂等返回成功**，初始化不同 bucket 会报错
2. `persist_init` 成功后，才能调用 `persist_set` / `persist_get` / `persist_delete` / `persist_clear`，且这些方法**无需再指定 bucket**
3. 同一持久化数据文件可被多个策略访问，但**同一时间只能被一个策略进程访问读写**，后访问的策略会在初始化时报错并被拒绝访问

---

## persist_set — 写入持久化数据

向当前绑定的 bucket 写入数据。

```python
persist_set(key, value)
```

### 参数

| 参数名 | 类型 | 中文名称 | 必填 | 默认值 | 说明 |
|--------|------|---------|:---:|--------|------|
| `key` | str | 数据键 | Y | 无 | 同一 bucket 下唯一；**长度限制 512** |
| `value` | str | 字符串数据值 | Y | 无 | 写入时按 UTF-8 编码为 bytes |

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | int | `0` 写入成功；非 0 失败 |

### 示例

```python
key = "stock_pool"
value = "SHSE.600519,SZSE.000001"

status = persist_set(key, value)
if status == 0:
    print("写入成功")
else:
    print("写入失败, 错误码:", status)
```

### 注意事项

1. 首次向当前绑定的 bucket 写入数据，会**新创建**该 bucket 的持久化数据文件
2. 向当前绑定的 bucket 再次写入数据时，若指定 key 已存在会**覆盖写入**，若不存在会创建新的数据键

---

## persist_get — 读取持久化数据

从当前绑定的 bucket 读取数据。

```python
persist_get(key)
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `key` | str | Y | 同一 bucket 下唯一；长度限制 512 |

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `value` | str | key 存在时返回对应的字符串数据值 |
| `None` | None | key 不存在（或该持久化数据文件中无此 key）时返回 `None`，**不视为错误** |

### 示例

```python
value = persist_get("stock_pool")
if value is not None:
    print("读取成功:", value)
else:
    print("该 key 不存在")
```

---

## persist_delete — 删除指定 key

删除当前绑定 bucket 中指定 key-value 的数据。

```python
persist_delete(key)
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `key` | str | Y | key 不存在时视为删除成功（幂等处理），返回 `status = 0` |

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | int | `0` 成功；非 0 失败 |

### 示例

```python
status = persist_delete("stock_pool")
if status == 0:
    print("删除成功")
```

### 注意事项

此接口只能删除当前绑定 bucket 中的 key，不会删除其他 bucket 中的 key；删除当前 bucket 中不存在的 key（例如其他 bucket 的 key），也会返回 `status = 0`。

---

## persist_clear — 清空当前 bucket

清空当前绑定 bucket 中全部 key-value 数据。

```python
persist_clear()
```

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | int | `0` 删除成功；非 0 失败 |

### 示例

```python
status = persist_clear()
if status == 0:
    print("清空成功")
```

---

## persist_delete_bucket — 删除 bucket

删除**非当前绑定**的持久化数据 bucket。

```python
persist_delete_bucket(bucket)
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `bucket` | str | Y | 只能删除**非**当前策略运行周期内通过 `persist_init` 绑定的 bucket；数据文件为空或不存在时视为删除成功（幂等） |

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | int | `0` 成功；非 0 失败（删当前绑定的 bucket 返回 `71005`） |

### 示例

```python
status = persist_delete_bucket(bucket="other_strategy_bucket")
if status == 0:
    print("删除成功")
```

### 注意事项

删除非当前绑定的 bucket 将删除对应的持久化数据文件；删除后该 bucket 不存在，策略重启后重新 `persist_init` 绑定该 bucket 并用 `persist_set` 重新写入数据时，会重新创建该 bucket 的数据文件。

---

## persist_get_all_buckets — 查询 bucket 列表

查询当前已创建的全部持久化数据标识（bucket），用于盘点本地持久化数据文件。

```python
persist_get_all_buckets()
```

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `buckets` | list[str] | 本策略已创建的全部持久化数据标识；没有任何持久化数据时返回空列表 `[]`，不视为错误 |

### 示例

```python
ids = persist_get_all_buckets()
print("本地持久化数据标识:", ids)   # 例如 ['strategy_demo', 'signal_cache']
```

### 注意事项

1. 查询接口只读取本地持久化数据目录的**元数据**（标识列表），不读写具体数据文件内容，**不受「单次运行进程内最多只能读写 1 个持久化数据 bucket」限制**
2. 仅策略运行期间可调用，**可在 `persist_init()` 初始化前被调用**

---

## persist_get_all_keys — 查询当前 bucket 所有 key

查询当前绑定的 bucket 下已保存的全部数据键。

```python
persist_get_all_keys()
```

### 返回值

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `keys` | list[str] | 当前绑定的 bucket 下已保存的全部数据键；bucket 不存在或数据文件为空时返回空列表 `[]`，不视为错误 |

### 示例

```python
keys = persist_get_all_keys()
print("bucket 下全部 key:", keys)   # 例如 ['stock_pool', 'strategy_name']
```

### 注意事项

1. 查询接口只读取元数据（键名列表），不读取数据值
2. **必须在 `persist_init()` 之后调用**。实测未 init 直接调用会抛 `UnicodeDecodeError`（SDK 3.0.193 缺陷）

---

## persist_set_obj / persist_get_obj — JSON 对象读写

自动将 dict / list 等 JSON 可序列化对象序列化后写入，读取时反序列化还原，适合保存股票池、实时动态参数、策略级持仓等结构化数据。

```python
persist_set_obj(key, value)
persist_get_obj(key)
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|:---:|------|
| `key` | str | Y | 同一 bucket 下唯一；长度限制 512 |
| `value` | Any | Y | JSON 可序列化对象（dict、list、str、int、float、bool、None 等），仅 set 接口 |

### 返回值

| 接口 | 字段名 | 类型 | 说明 |
|------|--------|------|------|
| set | `status` | int | `0` 成功；非 0 失败 |
| get | `value` | Any \| None | 反序列化还原后的对象；key 不存在时返回 `None` |

### 示例

```python
pool = {"stocks": ["SHSE.600519", "SZSE.000001"], "updated_at": 20260928}
status = persist_set_obj("stock_pool", pool)
if status == 0:
    print("写入成功")

data = persist_get_obj("stock_pool")
print(data["stocks"])   # ["SHSE.600519", "SZSE.000001"]
```

---

## 典型用法

### 1. 股票池跨运行保持

```python
BUCKET = 'my_stock_pool'

def init(context):
    persist_init(BUCKET, is_async=False)
    pool = persist_get('pool')
    if pool is None:
        persist_set('pool', 'SHSE.600519,SZSE.000001')
        print('首次写入股票池')
    else:
        print(f'复用已有股票池: {pool}')
    subscribe(symbols=persist_get('pool'), frequency='1d', count=20)
```

### 2. 策略运行计数 / 断点续跑

```python
def init(context):
    persist_init('state_bucket', is_async=False)
    cnt = persist_get('bar_count')
    context.bar_count = int(cnt) if cnt else 0
    print(f'恢复 bar_count = {context.bar_count}')

def on_bar(context, bars):
    context.bar_count += 1
    persist_set('bar_count', str(context.bar_count))
```

### 3. 结构化持仓记录

```python
def on_order_status(context, order):
    pos = persist_get_obj('my_positions') or {}
    sym = order['symbol']
    pos[sym] = {
        'volume': order['volume'],
        'price': order['price'],
        'updated': str(order['created_at'])
    }
    persist_set_obj('my_positions', pos)
```

### 4. 实时模式高频写入（用异步）

```python
def init(context):
    # 实时模式用默认 is_async=True，避免阻塞行情处理
    persist_init('live_state')
    subscribe(symbols='SHSE.600519', frequency='tick')

def on_tick(context, tick):
    # 高频写入，异步落盘不阻塞
    persist_set_obj('last_tick', {'price': tick['price'], 'ts': str(tick['created_at'])})
```

---

## 实测验证记录（2026-11-27，gm-api 3.0.193）

### 数据查询模式（set_token 后直接调用）

| # | 测试项 | 结果 |
|---|--------|------|
| 1 | `persist_init(bucket, is_async=False)` 在数据查询模式可用 | PASS，status=0 |
| 2 | `persist_set` 写入字符串 | PASS，status=0 |
| 3 | `persist_get` 读回一致 | PASS |
| 4 | `persist_get` 读不存在的 key | PASS，返回 `None` |
| 5 | `persist_set` 覆盖写入已有 key | PASS，值被替换 |
| 6 | `persist_set_obj` / `persist_get_obj` 对象往返 | PASS，dict 完全一致 |
| 7 | `persist_get_all_keys` | PASS，返回 `['stock_pool', 'stock_pool_obj']` |
| 8 | `persist_get_all_buckets` | PASS，返回已有 bucket 列表 |
| 9 | `persist_delete` 删除 key | PASS，之后 get 返回 None |
| 10 | `persist_delete` 删不存在的 key（幂等） | PASS，返回 0 |
| 11 | `persist_clear` 清空 | PASS，keys 变 `[]` |
| 12 | `persist_init` 重复 init 同一 bucket（幂等） | PASS，返回 0 |
| 13 | `persist_init` init 不同 bucket | PASS，返回 `71006` |
| 14 | `persist_delete_bucket` 删非绑定 bucket | PASS，返回 0 |
| 15 | `persist_delete_bucket` 删当前绑定 bucket | PASS，返回 `71005` |

### 策略 run 场景（真实回测）

```
[init] persist_init status=0
[init] 首次写入 stock_pool = SHSE.600519
[init] 恢复 bar_count = 0
[on_bar] bar#1 set_status=0 keys=['bar_count', 'meta', 'stock_pool']
...
=== 回测结束 ===
最终 bar_count = 9
bucket 内全部 key = ['bar_count', 'meta', 'stock_pool']
```

### 跨运行持久化（核心价值验证）

第二次跑同一策略：

```
[init] persist_init status=0
[init] 已存在 stock_pool = SHSE.600519     ← 上次的数据还在
[init] 恢复 bar_count = 9                   ← 从上次的值接着跑
[init] 已有 meta = {'strategy': 'persist_run_test', 'bars': 9}
...
最终 bar_count = 18                          ← 9 + 9
```

**结论：跨进程重启的状态保持正常工作。**

### 边界与坑

| 场景 | 实测结果 |
|------|---------|
| 未 init 直接 `persist_set` | 返回 `71002`，**不抛异常**（容易静默失败） |
| 未 init 直接 `persist_get` | 返回 `None`，不报错 |
| 未 init 直接 `persist_get_all_keys` | **抛 `UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80`**（SDK 缺陷） |
| 删当前绑定 bucket | 返回 `71005`，符合文档 |

---

## 版本与兼容性

- **gm ≥ 3.0.191**：持久化 API 首次引入
- 低于该版本调用会直接 `NameError: name 'persist_init' is not defined`
- 检查版本：`import importlib.metadata as md; md.version('gm')`
- 升级：`pip install gm --upgrade`
