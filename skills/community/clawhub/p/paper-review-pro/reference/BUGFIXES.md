# 重要修复说明

## 1. arXiv 网页爬取修复

### 问题描述
API 失败回退到网页爬取时程序无响应。

### 根因分析
- `html.split('<li class="arxiv-result">')` 导致每个 entry 包含大量冗余 HTML
- 正则表达式 `.*?` 在大文本块上回溯爆炸
- 无进度输出，无法追踪卡死位置

### 修复内容

**模块**: `scripts/search/arxiv.py`

**修复要点**:
1. 使用精确的 `re.findall` 提取条目
2. 限制单个条目最大长度（50KB）
3. 添加详细进度输出
4. 增加超时时间（30s → 60s）

**关键代码**:
```python
# 使用精确的 re.findall 提取条目
entry_pattern = r'<li class="arxiv-result">(.*?)</li>'
entry_matches = re.findall(entry_pattern, html, re.DOTALL)

# 限制单个条目最大长度
entry = entry[:50000]

# 添加详细进度输出
print(f"  [arXiv Web] 页面大小：{len(html)} 字节")
print(f"  [arXiv Web] 找到 {len(entry_matches)} 个条目，处理前 {min(max_results, len(entry_matches))} 个...")

# 增加超时时间
html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
```

---

## 2. 卡死检测与自动终止保护

### 问题描述
程序长时间无输出时无法自动终止，导致资源浪费。

### 修复内容

**模块**: `scripts/review.py`

**新增**: `TimeoutMonitor` 类

**功能**:
- 监控程序输出活动
- 超时自动终止（默认 10 分钟）
- 覆盖所有关键步骤

**监控点**:
- 检索开始/结束
- arXiv / Semantic Scholar 检索
- 相关性过滤
- 发表状态查询
- 相似度计算
- 扩展词生成
- 扩展检索（每个扩展词）
- 论文保存（Top-K + 扩展）
- BibTeX 导出
- 最终报告

**使用示例**:
```python
class TimeoutMonitor:
    """监控程序输出，超时自动终止"""
    
    def __init__(self, timeout_seconds=600):  # 10 分钟
        self.timeout = timeout_seconds
        self.last_activity = None
        self.alive = True
        
    def touch(self):
        """记录活动"""
        self.last_activity = time.time()
        
    def check(self):
        """检查是否超时"""
        elapsed = time.time() - self.last_activity
        if elapsed > self.timeout:
            print(f"\n\n⚠️  卡死检测：超过 {self.timeout} 秒无输出，强制终止程序")
            sys.exit(1)
```

### 配置
卡死保护默认 600 秒（10 分钟），可根据需要调整：
```python
TimeoutMonitor(timeout_seconds=XXX)
```

---

## 注意事项

1. **arXiv API 速率限制**较严格，网页爬取作为回退方案现在更可靠。

2. **所有关键步骤**都有 `activity_hook()` 调用，确保监控准确。

3. **进度输出**现在覆盖所有主要操作，便于追踪程序状态。
