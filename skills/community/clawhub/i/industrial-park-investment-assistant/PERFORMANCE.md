# 产业园招商助手 · 性能优化指南

> **版本**：v1.0.0 | **适用版本**：v2.12.0+ | **更新日期**：2026-06-12

---

## 📋 目录

1. [性能瓶颈分析](#性能瓶颈分析)
2. [优化方案](#优化方案)
3. [性能指标](#性能指标)
4. [监控和调优](#监控和调优)
5. [最佳实践](#最佳实践)

---

## 🔍 性能瓶颈分析

### 当前架构性能瓶颈

| 瓶颈类型 | 具体表现 | 影响程度 | 根本原因 |
|---------|---------|---------|---------|
| **MCP调用延迟** | 每次查询都调用腾讯文档API | 🔴 高 | 网络往返 + API限流 |
| **数据解析开销** | MCP原始格式解析复杂 | 🟡 中 | 嵌套结构 + 字段映射 |
| **文件I/O瓶颈** | 频繁读写本地JSON文件 | 🟡 中 | 同步I/O + 大文件 |
| **并发能力不足** | 串行执行多个MCP调用 | 🔴 高 | 工具调用策略不当 |
| **内存占用** | 全量数据加载到内存 | 🟢 低 | 数据量较小（<1000条） |

### 典型场景性能分析

#### 场景1：房源推荐（smart_recommend.py）

**当前流程**：
```
1. 调用 MCP 读取房源销控表（~2-3秒）
2. 解析 MCP 原始格式（~0.5秒）
3. 匹配客户需求（~0.1秒）
4. 生成推荐报告（~0.3秒）
总耗时：~3-4秒
```

**瓶颈点**：
- MCP调用占总体时间的70%
- 每次推荐都要重新读取全量数据

#### 场景2：跟进预警（每次对话启动）

**当前流程**：
```
1. 调用 MCP 读取客户管理表（~2-3秒）
2. 解析100+条客户记录（~0.5秒）
3. 逐条计算跟进时效（~0.2秒）
4. 生成预警列表（~0.1秒）
总耗时：~3-4秒
```

**瓶颈点**：
- 每次对话都要重新读取客户数据
- 无缓存机制

---

## ⚡ 优化方案

### 方案1：Session级数据缓存（优先级：🔴 高）

> **目标**：避免同一对话中重复调用MCP读取相同数据

**实现方式**：

```python
# 在 AI 上下文中维护缓存字典
context.cache = {
    "meilan-center": {
        "房源销控表": {"data": [...], "timestamp": 1718188800},
        "客户管理": {"data": [...], "timestamp": 1718188800}
    }
}

# 读取数据时先检查缓存
def load_data_with_cache(project_id, sheet_name):
    cache_key = f"{project_id}_{sheet_name}"
    
    # 检查缓存是否存在且未过期（30分钟）
    if cache_key in context.cache:
        cache_age = time.now() - context.cache[cache_key]["timestamp"]
        if cache_age < 1800:  # 30分钟
            return context.cache[cache_key]["data"]
    
    # 缓存未命中，调用MCP
    data = call_mcp(project_id, sheet_name)
    
    # 更新缓存
    context.cache[cache_key] = {
        "data": data,
        "timestamp": time.now()
    }
    
    return data
```

**效果预估**：
- 同一对话中重复查询：从 3秒 → 0.1秒（30倍提升）
- MCP API调用次数减少50%

**实施步骤**：

1. **AI执行规则**（在SKILL.md中添加）：
   ```
   ## Session缓存规则（AI自动执行）
   
   1. 首次读取数据后，将数据保存在上下文（标记为「{项目ID}_{表名}_已缓存」）
   2. 后续需要相同数据时，直接使用上下文中的数据
   3. 数据时效性：超过30分钟建议重新读取
   4. 用户明确说「刷新数据」「重新读取」时，强制刷新缓存
   ```

2. **缓存失效策略**：
   - 时间失效：30分钟自动过期
   - 主动失效：用户说「刷新」「重新读取」
   - 写入失效：调用 `add_records` / `update_records` 后，立即失效相关缓存

---

### 方案2：并发MCP调用（优先级：🔴 高）

> **目标**：多个MCP调用并行执行，减少总等待时间

**当前问题**：
```python
# ❌ 错误：串行调用（总耗时 = 3+2+2 = 7秒）
data1 = call_mcp("销控表")  # 3秒
data2 = call_mcp("租金报价")  # 2秒
data3 = call_mcp("配套资源")  # 2秒
```

**优化方案**：
```python
# ✅ 正确：并行调用（总耗时 = max(3,2,2) = 3秒）
# 在同一 response 中同时发起多个 tool call
tool_calls = [
    call_mcp("销控表"),
    call_mcp("租金报价"),
    call_mcp("配套资源")
]
# AI 会自动并行执行，等待所有结果返回
```

**实施规则**（在SKILL.md中添加）：
```
## 并发调用规则（AI自动执行）

1. 同一个 file_id 下的多个 sheet，必须并发调用
2. 不同 file_id 的调用，若无需依赖，也必须并发
3. 只有存在依赖关系时，才串行调用
   - 示例：先获取 sheet_id，再用 sheet_id 读取数据（必须串行）

并发调用示例：
✅ 正确：
  同时调用：
  - mcp__tencent-docs__smartsheet.list_records(file_id, sheet_A)
  - mcp__tencent-docs__smartsheet.list_records(file_id, sheet_B)

❌ 错误：
  先调用 sheet_A → 等待结果 → 再调用 sheet_B
```

**效果预估**：
- 读取3个sheet：从 7秒 → 3秒（2.3倍提升）
- 读取5个sheet：从 12秒 → 4秒（3倍提升）

---

### 方案3：增量更新（优先级：🟡 中）

> **目标**：只获取变更数据，减少数据传输量

**当前问题**：
- `list_records(limit=100)` 每次返回全量数据（即使只有1条记录变更）

**优化方案**：

#### 3.1 使用 `modified_time` 过滤（若API支持）

```python
# 只获取最近7天修改的记录
mcp__tencent-docs__smartsheet.list_records(
    file_id: "{CONFIG.tencent_doc.客户管理}",
    sheet_id: "{CONFIG.tencent_doc.客户管理_sheet_id}",
    filter: "最后跟进日期 >= '2026-06-05'",
    limit: 100
)
```

#### 3.2 本地缓存 + 差异对比

```python
# 第1次：全量读取，保存到本地
data_full = call_mcp("客户管理")
save_to_local("data/客户管理_全量.json", data_full)

# 第2次：读取本地缓存，只获取可能变更的记录
data_cached = load_from_local("data/客户管理_全量.json")
data_new = call_mcp("客户管理", limit=10)  # 只获取最近10条

# 合并数据
data_merged = merge_records(data_cached, data_new)
```

**效果预估**：
- 数据量减少70%（只传输变更部分）
- MCP调用耗时减少50%

---

### 方案4：数据格式优化（优先级：🟡 中）

> **目标**：减少数据解析开销，提升脚本执行速度

**当前问题**：
- MCP原始格式嵌套深，解析慢
- 每次都要做字段映射（`field_values[0].text_value.items[0].text`）

**优化方案**：

#### 4.1 使用紧凑格式（已在v2.12.0实现）

**MCP原始格式**（解析慢）：
```json
{
  "records": [
    {
      "record_id": "xxx",
      "field_values": [
        {"field": "楼层", "text_value": {"items": [{"text": "7F"}]}},
        {"field": "面积(㎡)", "text_value": {"items": [{"text": "143.92"}]}}
      ]
    }
  ]
}
```

**紧凑格式**（解析快）：
```json
{
  "records": [
    {
      "record_id": "xxx",
      "楼层": "7F",
      "面积(㎡)": 143.92,
      "底价(元/㎡/天)": 1.85
    }
  ]
}
```

**效果预估**：
- 解析速度提升3倍（减少JSON遍历）
- 文件大小减少70%（减少磁盘占用）

#### 4.2 预解析数据（脚本优化）

```python
# 在 knowledge_base.py 中添加预解析逻辑
class KnowledgeBase:
    def load(self, sheet_name):
        data = self.source.load(sheet_name)
        
        # 预解析：将MCP格式转为紧凑格式
        if self._is_mcp_format(data):
            data = self._convert_to_compact(data)
        
        # 预计算：生成索引
        self._build_index(data)
        
        return data
    
    def _convert_to_compact(self, mcp_data):
        # 转换逻辑
        ...
    
    def _build_index(self, data):
        # 构建索引：按面积排序、按楼层分组
        self.area_index = sorted(data["records"], key=lambda x: x["面积(㎡)"])
        self.floor_groups = groupby(data["records"], key=lambda x: x["楼层"])
```

---

### 方案5：异步I/O（优先级：🟢 低）

> **目标**：文件读写不阻塞主线程

**当前问题**：
- `save_to_file()` 是同步操作，大文件写入慢

**优化方案**：

```python
import asyncio

async def save_to_file_async(data, filepath):
    """异步保存数据到文件"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, save_to_file, data, filepath)

# 使用方式
async def main():
    # 并发执行：数据读取 + 文件保存
    results = await asyncio.gather(
        load_data_from_mcp(),
        save_previous_data_to_file()  # 不阻塞主流程
    )
```

**效果预估**：
- 文件保存不阻塞主流程
- 用户体验提升（响应更快）

---

## 📊 性能指标

### 目标性能指标

| 指标 | 当前值 | 目标值 | 优化方案 |
|------|--------|--------|---------|
| **MCP调用延迟** | 2-3秒/次 | <1秒/次 | Session缓存 + 并发调用 |
| **房源推荐耗时** | 3-4秒 | <1秒 | Session缓存 |
| **跟进预警耗时** | 3-4秒 | <1秒 | Session缓存 |
| **数据解析耗时** | 0.5秒 | <0.2秒 | 紧凑格式 |
| **文件保存耗时** | 0.3秒 | <0.1秒 | 异步I/O |

### 性能测试脚本

创建 `scripts/performance_test.py` 用于基准测试：

```python
#!/usr/bin/env python3
"""性能基准测试"""

import time
import json

def test_mcp_call_latency():
    """测试MCP调用延迟"""
    start = time.time()
    # 调用MCP读取数据
    data = call_mcp("销控表")
    elapsed = time.time() - start
    print(f"MCP调用延迟: {elapsed:.2f}秒")
    return elapsed

def test_cache_hit_latency():
    """测试缓存命中延迟"""
    # 第1次：缓存未命中
    test_mcp_call_latency()
    
    # 第2次：缓存命中
    start = time.time()
    data = load_from_cache("销控表")
    elapsed = time.time() - start
    print(f"缓存命中延迟: {elapsed:.2f}秒")
    return elapsed

def test_parse_performance():
    """测试数据解析性能"""
    # 读取MCP原始格式
    with open("data/房源销控表_mcp.json", "r") as f:
        mcp_data = json.load(f)
    
    start = time.time()
    compact_data = convert_to_compact(mcp_data)
    elapsed = time.time() - start
    print(f"数据解析耗时: {elapsed:.2f}秒")
    return elapsed

if __name__ == "__main__":
    print("=== 性能基准测试 ===")
    test_mcp_call_latency()
    test_cache_hit_latency()
    test_parse_performance()
```

---

## 📈 监控和调优

### 性能监控指标

| 指标 | 监控方式 | 告警阈值 |
|------|---------|---------|
| MCP调用次数 | 上下文计数器 | >100次/对话 |
| 缓存命中率 | 缓存命中次数/总查询次数 | <50% |
| 平均响应时间 | 时间戳差分 | >5秒 |
| 错误率 | 错误次数/总调用次数 | >5% |

### AI执行规则（自动监控）

```
## 性能监控规则（AI自动执行）

1. 每次调用MCP工具前，计数器+1
2. 缓存命中时，记录「缓存命中」
3. 若同一对话中MCP调用次数>20次，提示用户：
   「⚠️ 当前对话已调用MCP 20+次，建议整理需求后批量查询」
4. 若响应时间>5秒，自动切换到本地缓存模式
```

### 性能调优建议

#### 建议1：批量查询（减少MCP调用次数）

**❌ 错误示例**：
```
用户：「查一下A公司」
  → AI调用MCP查询客户管理表
用户：「再查一下B公司」
  → AI再次调用MCP查询客户管理表
```

**✅ 正确示例**：
```
用户：「查一下A公司和B公司」
  → AI一次性调用MCP，获取全量客户数据
  → 从缓存中筛选A公司和B公司
```

#### 建议2：预加载（预测用户需求）

**场景**：用户问「推荐房源」时，大概率接下来会问「租金多少」

**优化方案**：
```
用户：「推荐房源」
  → AI调用MCP读取：销控表 + 租金报价表（并发）
  → 将两个表的数据都缓存起来
  
用户：「租金多少」（5分钟后）
  → AI直接使用缓存中的租金报价表，无需调用MCP
```

---

## 💡 最佳实践

### 1. MCP调用优化

| 实践 | 说明 |
|------|------|
| **并发调用** | 同一file_id的多个sheet，必须并发 |
| **指定fields** | 只获取需要的字段，减少数据传输 |
| **合理limit** | 跟进预警用100，单个查询用10 |
| **Session缓存** | 同一对话中，数据缓存30分钟 |

### 2. 数据格式选择

| 场景 | 推荐格式 | 理由 |
|------|---------|------|
| 团队协作 | 腾讯文档（MCP） | 实时同步 |
| 个人使用 | 本地紧凑格式 | 解析快 |
| 大数据量 | 紧凑格式 + 分页 | 减少内存占用 |

### 3. 脚本优化

| 实践 | 说明 |
|------|------|
| **预解析** | 在`KnowledgeBase.load()`中预解析数据 |
| **构建索引** | 按面积排序、按楼层分组，加速查询 |
| **异步保存** | 文件保存不阻塞主流程 |
| **增量更新** | 只更新变更数据，减少I/O |

### 4. 多项目架构优化

| 实践 | 说明 |
|------|------|
| **项目隔离** | 每个项目独立缓存，避免数据混淆 |
| **懒加载** | 只在需要时加载项目数据 |
| **配置校验** | 启动时校验项目配置，提前发现错误 |

---

## 📝 优化实施计划

### 阶段1：Session缓存（1天）

- [ ] 在SKILL.md中添加Session缓存规则
- [ ] AI自动在上下文中维护缓存字典
- [ ] 测试验证：同一对话中重复查询命中缓存

### 阶段2：并发调用（1天）

- [ ] 在SKILL.md中添加并发调用规则
- [ ] AI自动识别可并发的MCP调用
- [ ] 测试验证：3个sheet并发调用，总耗时<最高单项耗时

### 阶段3：增量更新（2天）

- [ ] 实现本地缓存 + 差异对比逻辑
- [ ] 添加 `modified_time` 过滤（若API支持）
- [ ] 测试验证：数据量减少70%

### 阶段4：数据格式优化（1天）

- [ ] 完善紧凑格式转换逻辑
- [ ] 添加预解析和索引构建
- [ ] 测试验证：解析速度提升3倍

### 阶段5：异步I/O（1天）

- [ ] 实现异步文件保存
- [ ] 测试验证：文件保存不阻塞主流程

---

## 📚 参考资料

- [腾讯文档MCP工具文档](https://docs.qq.com/open/wiki/)
- [Python异步编程指南](https://docs.python.org/3/library/asyncio.html)
- [性能优化最佳实践](https://example.com/performance-best-practices)

---

**文档版本历史**：

- v1.0.0 (2026-06-12): 初始版本，包含5大优化方案 + 性能指标 + 实施计划
