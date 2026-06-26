# GitHub Reader Skill — 安全说明

**v3.2 安全架构说明**
*最后更新: 2026-05-24*

---

## 🔒 安全设计原则

本 skill 仅使用 **GitHub 官方 REST API**（`api.github.com`），不经过任何第三方服务。
所有安全防护措施在 `github_reader_v3_secure.py` 中有对应的代码实现。

---

## 🛡️ 安全防护清单（代码对应）

### 输入验证
- **函数**: `validate_repo_name()` (github_reader_v3_secure.py)
- **规则**: 正则 `^[a-zA-Z0-9][a-zA-Z0-9._-]{0,99}$` + 路径遍历检测（`..` 拒绝）
- **覆盖**: owner 和 repo 名称均经过验证

### SSRF 防护
- **函数**: `safe_url_join()` (github_reader_v3_secure.py)
- **实现**: 使用 `urllib.parse.quote()` 对所有路径组件编码
- **覆盖**: 所有 GitHub API URL 构造

### 路径遍历防护
- **函数**: `safe_file_path()` (github_reader_v3_secure.py)
- **实现**: `os.path.abspath()` + `os.path.normpath()` + `startswith()` 检查
- **覆盖**: 所有缓存文件路径

### 缓存防投毒
- **类**: `SecureGitHubReaderCache` (github_reader_v3_secure.py)
- **措施**: 文件大小限制、JSON 结构验证、原子写入（temp file + rename）
- **覆盖**: 所有缓存读写操作

### 速率限制
- **方法**: `_rate_limit()` (github_reader_v3_secure.py)
- **实现**: 滑动窗口，默认 1 秒间隔
- **覆盖**: 所有 GitHub API 调用

### 并发控制
- **实现**: `asyncio.Semaphore`，默认最多 3 个并发请求
- **覆盖**: API 调用和 README 获取

### 超时控制
- **实现**: HTTP 客户端 timeout + API 级超时（默认 10 秒）
- **覆盖**: 所有网络请求

### 数据隐私
- **策略**: 仅与 `api.github.com` 通信，不向任何第三方发送数据
- **透明**: 分析报告中包含数据流向声明
- **用户控制**: 缓存目录和 TTL 通过环境变量可配

---

## 🔧 安全配置

```bash
# 缓存安全
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"  # 缓存目录
export GITVIEW_CACHE_TTL="24"                   # 缓存时间（小时）
export GITVIEW_CACHE_MAX_SIZE="1"               # 最大缓存文件（MB）

# 性能安全
export GITVIEW_GITHUB_DELAY="1.0"               # API 调用间隔（秒）
export GITVIEW_GITHUB_TIMEOUT="10"              # API 超时（秒）
```

---

## 🧪 安全测试

如需自行验证安全防护，可用以下测试用例：

```python
# 1. 输入验证 — 路径遍历应被拒绝
assert validate_repo_name("../etc/passwd") == False
assert validate_repo_name("repo..config") == False
assert validate_repo_name("microsoft/BitNet") == False  # 不含 /
assert validate_repo_name("valid-repo") == True

# 2. URL 拼接 — 特殊字符应被编码
result = safe_url_join("https://api.github.com/repos", "user", "repo%00evil")
assert "%2500evil" in result  # % → %25

# 3. 文件路径 — 不能逃逸出基础目录
import os
base = "/tmp/test"
unsafe = os.path.join(base, "../../etc/passwd")
try:
    safe_file_path(base, unsafe)
    assert False, "Should have raised"
except ValueError:
    pass
```

---

## 📂 依赖审查

| 依赖 | 用途 | 风险 |
|------|------|------|
| `httpx` | HTTP 客户端 | 低 — 仅用于 GitHub API |
| `asyncio` | 异步编程 | 低 — Python 标准库 |
| `hashlib`, `json`, `re`, `os` | 工具 | 低 — Python 标准库 |
| `urllib.parse` | URL 编码 | 低 — Python 标准库 |

本 skill **不依赖**任何第三方数据源（Zread、GitView 等已移除）。

---

## 🚨 应急响应

如遇到安全问题：

1. **停止服务**
   ```bash
   openclaw gateway stop
   ```

2. **清除缓存**
   ```bash
   rm -rf /tmp/gitview_cache
   ```

3. **检查日志**
   ```bash
   tail -n 100 ~/.openclaw/logs/gateway.log
   ```

4. **更新到最新版本**
   ```bash
   clawhub update github-reader
   ```

---

*版本: v3.2 — 安全说明与代码实现一一对应*
