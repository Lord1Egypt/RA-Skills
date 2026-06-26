# Google Scholar API 技能安装指南

## 快速安装

### 1. 获取 SerpAPI 密钥
1. 访问 [SerpAPI 官网](https://serpapi.com/)
2. 点击 "Sign up" 注册账号
3. 完成邮箱验证
4. 在 Dashboard 中获取 API 密钥
5. 免费计划提供每月 100 次搜索

### 2. 设置环境变量
```bash
# Linux/macOS
export SERP_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:SERP_API_KEY="your_api_key_here"

# Windows (CMD)
set SERP_API_KEY=your_api_key_here
```

### 3. 安装 Python 依赖
```bash
pip install google-search-results requests
```

或使用 requirements.txt:
```bash
pip install -r scripts/requirements.txt
```

## 验证安装

### 方法1: 运行测试脚本
```bash
cd skills/google-scholar-api
python test_skill.py
```

应该看到所有测试通过。

### 方法2: 简单功能测试
```python
from scripts.google_scholar_search import GoogleScholarSearch

# 测试导入
client = GoogleScholarSearch()
print("✅ 导入成功")

# 测试搜索（不实际调用API）
print("✅ 类结构正确")
```

## 基本使用

### 命令行使用
```bash
# 基本搜索
python scripts/google_scholar_search.py "machine learning" --num 5

# 指定输出目录
python scripts/google_scholar_search.py "deep learning" --output ./my_papers --num 10

# 使用年份过滤
python scripts/google_scholar_search.py "transformer" --year-from 2020 --year-to 2024

# 按日期排序
python scripts/google_scholar_search.py "reinforcement learning" --sort date
```

### Python 脚本中使用
```python
from scripts.google_scholar_search import GoogleScholarSearch

# 初始化客户端
client = GoogleScholarSearch()

# 搜索论文
results = client.search("artificial intelligence", num_results=10)

# 解析结果
papers = client.parse_results(results)

# 下载PDF
for paper in papers:
    if 'pdf_link' in paper:
        client.download_pdf(paper['pdf_link'], f"{paper['title'][:50]}.pdf")
```

## 在 OpenClaw 中使用

### 作为技能使用
当用户请求学术搜索时：
1. 检查环境变量 `SERP_API_KEY` 是否设置
2. 根据用户请求构建搜索查询
3. 调用 `google_scholar_search.py` 脚本
4. 格式化输出结果

### 示例响应
```markdown
## 学术搜索完成

**关键词**: 机器学习
**找到论文**: 15篇
**有PDF的**: 8篇

### 推荐论文
1. **论文标题1** (2023)
   - 作者: 作者1, 作者2
   - 引用: 150次
   - PDF: ✅ 可用

2. **论文标题2** (2022)
   - 作者: 作者3, 作者4
   - 引用: 89次
   - PDF: ✅ 可用

### 下载命令
```bash
python scripts/google_scholar_search.py "机器学习" --num 8 --output ./ml_papers
```
```

## 故障排除

### 常见问题

#### 问题1: API 密钥错误
```
Error: SerpAPI key is required.
```
**解决方案**:
```bash
# 检查环境变量
echo $SERP_API_KEY

# 重新设置
export SERP_API_KEY="your_correct_key"
```

#### 问题2: 模块导入错误
```
ModuleNotFoundError: No module named 'google_search_results'
```
**解决方案**:
```bash
pip install google-search-results
```

#### 问题3: 网络连接问题
```
requests.exceptions.ConnectionError
```
**解决方案**:
- 检查网络连接
- 尝试使用代理
- 等待一段时间后重试

#### 问题4: API 额度不足
```
Error: API quota exceeded
```
**解决方案**:
- 升级 SerpAPI 计划
- 等待下个月重置
- 减少搜索次数

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from scripts.google_scholar_search import GoogleScholarSearch
client = GoogleScholarSearch()
```

## 高级配置

### 使用配置文件
创建 `config.py`:
```python
import os

# API 配置
SERP_API_KEY = os.getenv('SERP_API_KEY', 'your_fallback_key')

# 搜索默认值
DEFAULT_NUM_RESULTS = 10
DEFAULT_SORT = "relevance"
DEFAULT_DOWNLOAD_DIR = "./scholar_papers"

# 网络设置
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
```

### 自定义用户代理
```python
from scripts.google_scholar_search import GoogleScholarSearch
import requests

class CustomScholarSearch(GoogleScholarSearch):
    def download_pdf(self, pdf_url, save_path):
        headers = {
            "User-Agent": "Mozilla/5.0 (ResearchBot/1.0; +http://example.com/bot)",
            "Accept": "application/pdf",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        response = requests.get(pdf_url, headers=headers, timeout=30)
        # ... 其余代码
```

## 性能优化

### 缓存搜索结果
```python
import json
import hashlib
from functools import lru_cache

class CachedScholarSearch(GoogleScholarSearch):
    @lru_cache(maxsize=100)
    def search(self, query, num_results=10, **kwargs):
        # 生成缓存键
        cache_key = hashlib.md5(f"{query}_{num_results}_{kwargs}".encode()).hexdigest()
        cache_file = f".cache/{cache_key}.json"
        
        # 检查缓存
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # 执行搜索
        result = super().search(query, num_results, **kwargs)
        
        # 保存缓存
        os.makedirs(".cache", exist_ok=True)
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        
        return result
```

### 批量处理
```python
def batch_search(queries, output_dir="./batch_results"):
    """批量搜索多个查询"""
    client = GoogleScholarSearch()
    os.makedirs(output_dir, exist_ok=True)
    
    all_results = {}
    for query in queries:
        print(f"处理: {query}")
        result = client.search_and_download(
            query=query,
            download_dir=os.path.join(output_dir, query.replace(" ", "_")),
            max_papers=5
        )
        all_results[query] = result
        
        # 避免频繁请求
        import time
        time.sleep(2)
    
    return all_results
```

## 安全注意事项

1. **保护 API 密钥**: 不要将密钥提交到版本控制系统
2. **遵守使用条款**: 仅用于个人学术研究
3. **尊重版权**: 不要大规模下载受版权保护的内容
4. **控制频率**: 避免过于频繁的请求

## 更新和维护

### 检查更新
```bash
# 更新 Python 包
pip install --upgrade google-search-results requests

# 检查技能更新
cd skills/google-scholar-api
git pull origin main  # 如果使用 git
```

### 备份配置
```bash
# 备份 API 密钥
echo "export SERP_API_KEY='$SERP_API_KEY'" > ~/.scholar_api_backup.sh

# 备份下载的论文
tar -czf scholar_papers_backup_$(date +%Y%m%d).tar.gz ./downloads/
```

---

**支持**: 如有问题，请参考 `references/api_guide.md` 或创建 issue。