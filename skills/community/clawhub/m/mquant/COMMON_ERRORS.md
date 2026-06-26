# MQuant 常见报错总结

**生成代码前必读 - 对照检查清单**

> 💡 **提示**：这是 Skill 文档。如果你想添加个人踩过的坑而不被更新覆盖，请创建 COMMON_ERRORS.user.md 文件。
> 
> 详见 README.md

---

## ❌ 错误1：结构体字段不存在

**报错：** `'Tick' object has no attribute 'last'`

**原因：** 使用了文档中不存在的字段

**解决：**
- ✅ `tick.current` (最新价)
- ❌ `tick.last` (不存在)
- ✅ `pos.symbol` (持仓代码)
- ❌ `pos.code` (不存在)

---

## ❌ 错误2：API返回类型错误

**报错：** `'str' object has no attribute 'symbol'` 或 `'dict' object is not iterable`

**原因：** `get_positions()` 返回字典 `dict<symbol, Position>`，不是列表

**错误用法：**
```python
positions = get_positions()
for pos in positions:  # ❌ 遍历得到的是symbol字符串
    pos.symbol  # 报错！
```

**正确用法：**
```python
# 方法1: 使用get()从字典获取（推荐）
positions = get_positions()
pos = positions.get(g_security)
amount = pos.amount if pos else 0

# 方法2: 遍历字典的items()
positions = get_positions()
for symbol, pos in positions.items():
    if symbol == g_security:
        amount = pos.amount

# 方法3: 使用get_positions_ex()返回列表
positions = get_positions_ex()  # 返回 list<Position>
for pos in positions:
    if pos.symbol == g_security:
        amount = pos.amount
```

---

## ❌ 错误3：subscribe参数错误

**报错：** 没有行情数据 / 策略不运行

**原因：** 使用了不支持的频率参数

**错误：** `subscribe(symbol, '1d')`

**正确：** `subscribe(symbol, MarketDataType.KLINE_1M)`

---

## ❌ 错误4：文件名超过11字符

**报错：** Matic无法加载策略

**原因：** Python文件名限制11字符（不含扩展名）

**错误：** `ultra_grid_v1.py` (13字符)

**正确：** `ugrid_v1.py` (9字符)

---

## ❌ 错误5：缺少必要导入

**报错：** `name 'log' is not defined`

**原因：** 没有导入mquant_api

**正确：**
```python
from mquant_api import *
from mquant_struct import *
```

---

## ❌ 错误6：回调函数参数不匹配

**报错：** `handle_tick() takes 3 positional arguments but 4 were given`

**原因：** 回调函数参数与文档不符

**正确：**
```python
def handle_tick(context, tick, msg_type):  # 3个参数
def handle_data(context, kline_data):      # 2个参数
```

---

## ❌ 错误7：全局变量未声明global

**报错：** `UnboundLocalError: local variable referenced before assignment`

**原因：** 修改全局变量没有声明 `global`

**正确：**
```python
def handle_tick(context, tick, msg_type):
    global g_last_idx  # 必须声明
    g_last_idx = 0
```

---

## API调用核对表

生成代码时，必须严格按照 `mquant_api.py` 中的定义：

| API | 文档定义 | 常见错误 |
|-----|----------|----------|
| subscribe | `subscribe(security, MarketDataType.XXX)` | 使用字符串'1d' ❌ |
| handle_tick | `handle_tick(context, tick, msg_type)` | 参数顺序错误 ❌ |
| handle_data | `handle_data(context, kline_data)` | 参数名错误 ❌ |
| order | `order(symbol, amount)` | 参数类型错误 ❌ |
| get_positions | `get_positions()` | 无参数 ✅ |

---

## 结构体字段核对表

| 结构体 | 正确字段 | 常见错误 |
|--------|----------|----------|
| Tick | `tick.code`, `tick.current` | `tick.last` ❌ |
| Tick | `tick.open`, `tick.high`, `tick.low` | - |
| Position | `pos.symbol`, `pos.amount` | `pos.code` ❌ |
| KLineDataPush | `kline.close`, `kline.high` | - |

---

## 详细日志记录要求

所有策略必须记录以下信息到日志：

### 1. 初始化阶段
- 策略启动时间
- 订阅的标的和行情类型
- 策略参数值（网格价格、数量等）
- 初始状态（持仓、资金等）

### 2. 行情数据阶段
- 每次接收到的行情数据（tick价格/kline收盘价）
- 计算的中间值（均线、网格索引等）
- 当前持仓状态

### 3. 判断逻辑阶段
- 每个判断条件的结果（True/False）
- 触发交易的具体条件
- 未触发交易的原因

### 4. 交易执行阶段
- 下单参数（标的、数量、价格）
- 下单返回值（成功/失败）
- 错误信息（如有）

### 日志级别规范
- `DEBUG` - 详细数据（tick价格、计算过程、判断条件）
- `INFO` - 关键事件（初始化、交易触发、参数变化）
- `WARN` - 警告（数据异常、条件不满足但仍继续）
- `ERROR` - 错误（API调用失败、异常抛出）

### 排查问题时的日志检查点
1. 行情数据是否接收？→ 检查DEBUG日志的tick/kline数据
2. 计算是否正确？→ 检查计算的索引、均线值等
3. 判断条件是否满足？→ 检查条件判断的True/False
4. 交易是否执行？→ 检查order()调用和返回值

---

## 错误诊断与修复

当用户粘贴错误日志时，执行以下诊断流程：

### Step 1: 错误识别
分析错误日志，分类问题类型：
- **Syntax Error**：语法错误（括号不匹配、缩进错误等）
- **Import Error**：模块导入失败
- **API Error**：Matic API调用错误（参数错误、未订阅行情等）
- **Logic Error**：逻辑错误（变量未定义、除零等）
- **Runtime Error**：运行时错误（内存、超时等）

### Step 2: 定位问题
根据错误堆栈定位到具体代码行，结合`.log`文件中的生成元数据：
- 查看代码版本
- 查看使用的模板类型
- 查看用户自定义参数

### Step 3: 一键修复
提供修复方案：

```
===== ERROR DIAGNOSIS =====
错误类型：API Error
错误原因：未订阅行情就调用get_kline_data()
位置：第42行

修复方案：
在initialize()中添加订阅：
    subscribe('000001.SZ', '1m')

修复后的代码：
[展示修复后的完整代码片段]
```

### 常见错误速查表

| 错误信息 | 可能原因 | 解决方案 |
|----------|----------|----------|
| NameError: name 'X' is not defined | 变量未定义 | 检查变量初始化 |
| TypeError: 'NoneType' | 函数返回None被使用 | 添加判空处理 |
| API not subscribed | 未订阅行情 | 在initialize中添加subscribe |
| Order failed: -1 | 下单失败 | 检查账户余额、持仓限制 |

---

## ✅ 生成代码前自检清单

- [ ] 结构体字段核对 `mquant_struct.py`
- [ ] `get_positions()` 按字典访问
- [ ] `subscribe()` 使用 `MarketDataType`
- [ ] 文件名 ≤ 11 字符
- [ ] 已导入 `mquant_api` 和 `mquant_struct`
- [ ] 回调函数参数与文档一致
- [ ] 全局变量声明 `global`
- [ ] 日志记录完整

---

**完整文档：** `reference/mquant_inside_python_document/`
