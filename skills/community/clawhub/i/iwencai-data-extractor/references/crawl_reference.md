# 爬取脚本完整参考

## 核心函数说明

### ab(*args) — agent-browser 封装

```python
def ab(*args):
    cmd = [AGENT, "--cdp", CDP_PORT] + list(args)
    r = subprocess.run(cmd, capture_output=True)
    out = r.stdout.decode("utf-8", errors="replace").strip()
    return out
```

**注意**：agent-browser 子命令（snapshot/eval/click/fill/press）**不支持 --timeout 参数**，加了会报 `Unknown command`。

### ab_eval(js) — JS 执行

```python
def ab_eval(js):
    raw = ab("eval", js)
    # agent-browser eval 输出被额外包一层 JSON 字符串，需双层解析
    step1 = json.loads(raw)
    return json.loads(step1) if isinstance(step1, str) else step1
```

### JS_EXTRACT — 提取表格数据

```javascript
(function(){
  var rows = document.querySelectorAll('tr');
  var result = [];
  rows.forEach(function(row){
    var cells = row.querySelectorAll('td');
    if(cells.length < 5) return;
    var cellData = Array.from(cells).map(function(c){
      return c.innerText.replace(/[\n\r]/g,' ').replace(/\|/g,'/').trim();
    });
    // 过滤：只保留含6位数字代码的行
    var hasCode = cellData.some(function(c){ return /^\d{6}$/.test(c); });
    if(hasCode){ result.push(cellData); }
  });
  return JSON.stringify(result);
})()
```

### JS_PAGE_INFO — 获取分页信息

```javascript
(function(){
  var active = document.querySelector('.page-item.active');
  var items  = document.querySelectorAll('.page-item');  // 正确class
  var nums = [];
  items.forEach(function(el){
    var t = el.innerText.trim();
    if(/^\d+$/.test(t)) nums.push(parseInt(t));
  });
  return JSON.stringify({
    current: active ? active.innerText.trim() : '1',
    pages: nums,
    max: nums.length > 0 ? Math.max.apply(null, nums) : 1
  });
})()
```

**注意**：分页 class 是 `.page-item`，不是 `.iw-asidetable-page-item`。

### 翻页 JS — Vue 兼容

```javascript
(function(){
  var items = document.querySelectorAll('.page-item');
  var target = null;
  items.forEach(function(el){
    if(el.innerText.trim() === '2' && !el.classList.contains('active')){
      target = el;
    }
  });
  if(!target){ return 'not found'; }
  var a = target.querySelector('a') || target;
  // 必须用 dispatchEvent，普通 click() 不触发 Vue 响应式事件
  a.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
  return 'ok:' + a.tagName;
})()
```

## 数据列索引映射（row[]）

问财涨停表格列顺序（通过 querySelectorAll('td') 获取）：

| 索引 | 字段 | 说明 |
|------|------|------|
| 2 | stock_code | 股票代码（6位） |
| 3 | stock_name | 股票名称 |
| 4 | price | 收盘价 |
| 5 | change_pct | 涨跌幅(%) |
| 6 | zt_time | 涨停时间 |
| 7 | zt_status | 涨停状态 |
| 9 | volume | 成交量 |
| 10 | amount | 成交额 |
| 11 | first_zt_time | 首次涨停时间 |
| 13 | zt_type | 涨停类型 |
| 14 | float_mv | 流通市值 |
| 15 | vol_ratio | 量比 |
| 16 | themes | 所属题材（+分隔） |
| 17 | zt_tags | 涨停标签 |
| 18 | lb_count | 连板数 |
| 19 | total_mv | 总市值 |

## 搜索查询格式

```python
# 日期转为中文，如 "2026年3月2日涨停股票"
d = date.fromisoformat("2026-03-02")
query = f"{d.year}年{d.month}月{d.day}日涨停股票"
```

## 等待时间建议

- 搜索后等待：`time.sleep(7)`（等 AI 解析 + 结果加载）
- 翻页后等待：`time.sleep(3)`
- 日期间隔：`time.sleep(3)`（避免请求过快）
