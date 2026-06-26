# 常见问题排查

## 1. agent-browser 报 "Unknown command"

**原因**：给子命令加了 `--timeout` 参数，agent-browser 子命令不支持此参数。

**错误写法**：
```python
cmd = [AGENT, "--cdp", "9222", "snapshot", "--timeout", "30000", "-i", "-c"]
```

**正确写法**：
```python
cmd = [AGENT, "--cdp", "9222", "snapshot", "-i", "-c"]
```

---

## 2. snapshot 输出为空

**原因**：通常是 `--timeout` 导致命令失败，或 Chrome CDP 未连接。

**排查**：
1. 确认 Chrome 以 `--remote-debugging-port=9222` 启动
2. 浏览器已导航到 `https://www.iwencai.com/unifiedwh/stockpicker/`
3. 访问 `http://localhost:9222/json` 确认 CDP 可用

---

## 3. 找不到搜索框（search_ref 为 None）

**原因**：问财页面用 `textbox` 元素类型，而不是 `input` 或 `textarea`。

**排查**：打印 snapshot 前 1000 字节，查看实际元素类型：
```python
snap = ab("snapshot", "-i", "-c")
print(snap[:1000])
```

**关键词**：找 `textbox` 且包含 "筛选条件" 或 "请输入您的" 的行。

---

## 4. 翻页无效（点击后还是第1页数据）

**原因**：问财用 Vue.js，普通 DOM `click()` 不触发 Vue 响应式事件。

**错误方式**：
```javascript
element.click();  // 无效
```

**正确方式**：
```javascript
element.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
```

---

## 5. 分页元素找不到（JS_PAGE_INFO 返回 max:1）

**原因**：分页 CSS class 用错了。

**错误**：`.iw-asidetable-page-item`  
**正确**：`.page-item`（每页50条以上才出现分页）

---

## 6. Python 中文乱码 / GBK 编码错误

**原因**：Windows 终端默认 GBK，Python 输出中文会报错。

**解决**：
```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

运行时用 `cmd /c python script.py`（不直接用 PowerShell）。

---

## 7. PowerShell CLIXML 包装导致 stdout 污染

**症状**：输出包含 `#< CLIXML` 和大量 XML 标签。

**解决**：用 `cmd /c` 代替 PowerShell 直接调用：
```
cmd /c python D:\path\to\script.py
```

---

## 8. eval 返回数据解析失败

**原因**：agent-browser eval 输出被额外包一层 JSON 字符串。

**原始输出示例**：`"\"[...]\""` （字符串里包字符串）

**解决**：双层解析
```python
step1 = json.loads(raw)       # 第一层：得到字符串
result = json.loads(step1)    # 第二层：得到实际列表/对象
```

---

## 9. 数据库有重复记录

**原因**：重复爬取同一日期。

**预防**：`save_records` 函数先查已有 `stock_code`，跳过重复插入。  
**检查**：`SELECT trade_date, COUNT(*) FROM zt_stocks GROUP BY trade_date`

---

## 10. 某日数据不完整（只有50条，实际有100条）

**原因**：只抓了第1页，翻页逻辑未触发或翻页失败。

**排查**：检查 `JS_PAGE_INFO` 返回的 `max` 值，如 `max:2` 说明有2页。  
**重抓**：设置 `force=True` 或删掉该日数据后重新执行。
