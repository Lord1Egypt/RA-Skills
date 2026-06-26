# 🦞 灵犀 (Lingxi) - 新手小白养虾助手

> **心有灵犀，一点就通** ✨  
> **版本：** v3.3.6  
> **作者：** Scarlett (斯嘉丽)  
> **最后更新：** 2026-03-13

---

## 🔐 安全与配置声明

**⚠️ 重要提示：** 灵犀需要配置外部凭证才能完整运行。详细信息请阅读 [SECURITY_AND_CONFIG.md](SECURITY_AND_CONFIG.md)

### 无需凭证即可运行的功能
- ✅ 本地 Dashboard 访问（http://localhost:8765）
- ✅ 记忆管理、任务记录、技能管理
- ✅ Layer0 规则管理
- ✅ SQLite 数据库操作

### 需要外部凭证的功能（可选）
| 功能 | 凭证 | 存储位置 | 风险等级 |
|------|------|---------|---------|
| Dashboard 公开访问 | Dashboard Token | `~/.openclaw/workspace/.lingxi/dashboard_token.txt` | 🟢 低 |
| GitHub 推送 | GitHub Token | `~/.github_token` | 🔴 高 |
| 飞书/钉钉/QQ 机器人 | 各自平台 Token | 各平台后台配置 | 🟡 中 |
| 大模型调用 | 阿里云 API Key | 环境变量 | 🔴 高 |

**安全承诺：**
- ✅ 明确声明所有外部依赖
- ✅ 不隐藏任何网络请求
- ✅ 不收集用户隐私数据
- ✅ 提供完整的凭证管理指南

---

## 📋 简介

灵犀是一个基于 OpenClaw 的 AI 智能调度系统，专为多渠道消息处理和智能任务管理设计。

### 核心特性

- 🧠 **MindCore 记忆核心** - 三级记忆系统（STM/MTM/LTM）
- 🔄 **EvoMind 自改进** - 系统持续优化和进化
- 🕷️ **SmartFetch 智能抓取** - 自动学习新知识
- 🤖 **Multi-Agent 架构** - 支持飞书、钉钉、QQ、企业微信等多渠道
- 📊 **Dashboard 可视化** - MemOS 风格管理界面
- ⚡ **快速响应层** - 简单问题 <5ms 秒回
- 💾 **LRU 缓存** - 重复问题秒回
- 🚀 **并行执行** - 复杂任务处理快 9x
- 💰 **Token 优化** - 57% 请求零 LLM 消耗

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 18+
- OpenClaw 2026.3.8+
- SQLite 3.0+

### 安装步骤

```bash
# 1. 克隆仓库
cd /root/lingxi-ai-latest

# 2. 安装依赖
pip3 install -r requirements.txt --break-system-packages

# 3. 配置 Token
echo "your_dashboard_token" > ~/.openclaw/workspace/.lingxi/dashboard_token.txt

# 4. 启动 Dashboard
cd dashboard/v3 && python3 server.py &

# 5. 访问 Dashboard
# http://localhost:8765/?token=your_dashboard_token
```

### 目录结构

```
lingxi-ai-latest/
├── core/                    # 核心模块
│   ├── config_manager.py    # 配置管理
│   ├── task_queue.py        # 任务队列
│   ├── memory_llm.py        # 记忆管理
│   └── dashboard_enhanced.py # Dashboard 增强
├── scripts/                 # 功能脚本
│   ├── orchestrator_v2.py   # 智慧调度器 v2
│   ├── dashboard_client.py  # Dashboard 客户端
│   ├── fast_response_layer_v2.py # 快速响应层
│   └── performance_patch.py # 性能优化补丁
├── dashboard/               # Dashboard 前端
│   └── v3/
│       ├── index.html       # 主页面
│       └── server.py        # API 服务器
├── data/                    # 数据目录
│   └── dashboard_v3.db      # SQLite 数据库
└── README.md                # 本文档
```

---

## 📊 Dashboard 功能

### 7 大功能模块

1. **📊 概览** - 系统状态总览
2. **🧠 MindCore 记忆** - 记忆管理（支持搜索/过滤/分页）
3. **📋 任务列表** - 任务记录（支持渠道/时间/类型筛选）
4. **🛠️ 技能中心** - 技能管理（显示使用次数/活跃状态）
5. **⚡ Layer0 规则** - 响应规则管理（191 条规则）
6. **📈 数据分析** - 调用统计/Token 消耗
7. **⚙️ 系统设置** - 主题/时区/数据管理

### 访问地址

- **本地访问：** http://localhost:8765/?token=YOUR_TOKEN
- **远程访问：** http://YOUR_SERVER_IP:8765/?token=YOUR_TOKEN（需配置防火墙和域名）

---

## 🔧 核心组件

### 1. 智慧调度器 (orchestrator_v2.py)

灵犀的核心调度引擎，负责：
- 快速响应层匹配（<5ms）
- LRU 缓存查询
- 技能路由和调用
- 大模型选择（qwen3.5-plus/qwen3-max 等）
- 结果缓存和性能监控

### 2. Dashboard 客户端 (dashboard_client.py)

负责将任务记录到 Dashboard：
```python
from scripts.dashboard_client import record_to_dashboard

record_to_dashboard(
    user_input="用户输入",
    user_id="用户 ID",
    channel="feishu",
    llm_model="qwen3.5-plus",
    skill_name="lingxi",
    status="completed",
    response_time_ms=123.45
)
```

### 3. 快速响应层 (fast_response_layer_v2.py)

提供 <5ms 的快速响应：
- 问候语匹配（你好/在吗/早上好）
- 简单问题缓存
- 正则表达式匹配

### 4. 性能优化补丁 (performance_patch.py)

v3.0.2 新增：
- LazyTrinityState - 懒加载状态管理
- BatchLearningWriter - 批量学习写入
- PerformanceMonitor - 性能监控

---

## 🛠️ 常见问题 (Q&A)

### Q1: Dashboard 任务列表不更新，但记忆文件有记录？

**问题现象：**
- 记忆文件（`memory/items/memories.jsonl`）有完整对话记录
- Dashboard 任务列表一直不更新
- 最新任务停留在某个时间点

**排查步骤：**

1. **检查 Dashboard API 是否正常**
```bash
curl http://localhost:8765/api/stats?token=YOUR_TOKEN
```

2. **检查数据库连接**
```bash
python3 -c "import sqlite3; conn=sqlite3.connect('/root/lingxi-ai-latest/data/dashboard_v3.db'); print('Tables:', [t[0] for t in conn.cursor().execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall()])"
```

3. **检查灵犀日志**
```bash
tail -100 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep -i "dashboard\|task"
```

**根本原因：**
灵犀的 `dashboard_client.py` 依赖 `httpx` 模块发送 HTTP 请求到 Dashboard，但该模块未安装。

**解决方案：**

```bash
# 1. 安装 httpx 模块
pip3 install httpx --break-system-packages

# 2. 验证安装
python3 -c "import httpx; print('✅ httpx installed')"

# 3. 测试 Dashboard 客户端
python3 << 'EOF'
import sys
sys.path.insert(0, '/root/lingxi-ai-latest')
from scripts.dashboard_client import get_dashboard_client

client = get_dashboard_client()
print("Base URL:", client.base_url)
print("Token:", client.token[:20] + "...")

result = client.record_task({
    "user_id": "test",
    "channel": "feishu",
    "user_input": "测试任务",
    "status": "completed"
})
print("Record result:", result)
EOF
```

**验证：**
```bash
python3 -c "import sqlite3; conn=sqlite3.connect('/root/lingxi-ai-latest/data/dashboard_v3.db'); cur=conn.cursor(); cur.execute('SELECT datetime(created_at, \"unixepoch\", \"localtime\"), user_input FROM tasks ORDER BY created_at DESC LIMIT 3'); [print(f'{r[0]} - {r[1][:50]}') for r in cur.fetchall()]"
```

---

### Q2: Dashboard 时间显示错误（显示 3 月 14 日而非 3 月 13 日）？

**问题现象：**
- 数据库时间戳正确（如 `1773389873`）
- Dashboard 显示时间错误（放大 1000 倍）

**根本原因：**
JavaScript 的 `new Date()` 期望毫秒级时间戳，但数据库存储的是秒级时间戳。

**解决方案：**

修改 `/root/lingxi-ai-latest/dashboard/v3/index.html` 中的 `formatTimeBeijing` 函数：

```javascript
function formatTimeBeijing(ts) {
    if (!ts) return '';
    try {
        if (typeof ts === 'number') {
            var d = new Date(ts * 1000);  // 秒转毫秒
        } else if (typeof ts === 'string') {
            if (ts.match(/^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$/)) {
                return ts;  // 直接返回字符串格式
            }
            var num = parseFloat(ts);
            if (!isNaN(num)) {
                d = new Date(num * 1000);
            } else {
                d = new Date(ts);
            }
        } else {
            d = new Date(ts);
        }
        var year = d.getUTCFullYear();
        var month = ('0' + (d.getUTCMonth() + 1)).slice(-2);
        var day = ('0' + d.getUTCDate()).slice(-2);
        var hour = ('0' + d.getUTCHours()).slice(-2);
        var minute = ('0' + d.getUTCMinutes()).slice(-2);
        var second = ('0' + d.getUTCSeconds()).slice(-2);
        return year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second;
    } catch (e) {
        return ts;
    }
}
```

---

### Q3: Dashboard 无法从公网访问？

**问题现象：**
- 本地访问正常（http://127.0.0.1:8765）
- 公网访问拒绝连接（检查防火墙和服务器 IP 配置）

**解决方案：**

1. **检查 Dashboard 监听地址**
```bash
netstat -tlnp | grep 8765
# 应该显示：0.0.0.0:8765 而非 127.0.0.1:8765
```

2. **重启 Dashboard**
```bash
pkill -f "python3 server.py"
cd /root/lingxi-ai-latest/dashboard/v3 && python3 server.py > /tmp/dashboard.log 2>&1 &
```

3. **检查防火墙/安全组**
- 云服务器控制台开放 8765 端口
- 系统防火墙：`ufw allow 8765` 或 `firewall-cmd --add-port=8765/tcp`

---

### Q4: 如何添加 POST /api/tasks 接口？

**问题背景：**
Dashboard 默认只有 GET 接口，灵犀需要 POST 接口记录任务。

**解决方案：**

在 `/root/lingxi-ai-latest/dashboard/v3/server.py` 添加：

```python
import time

@app.post("/api/tasks")
async def create_task(task_data: dict, token: str = ""):
    """创建/记录任务"""
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Token 无效")
    
    import sqlite3
    db_path = LINGXI_AI_DIR / "data" / "dashboard_v3.db"
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        now = time.time()
        task_id = task_data.get("id", f"task_{int(now)}")
        
        cursor.execute("""
            INSERT OR REPLACE INTO tasks (
                id, user_id, channel, user_input, status, task_type, 
                created_at, updated_at, completed_at, skill_name, llm_model, 
                response_time_ms, llm_tokens_in, llm_tokens_out, final_output
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            task_id,
            task_data.get("user_id", "unknown"),
            task_data.get("channel", "unknown"),
            task_data.get("user_input", "")[:500],
            task_data.get("status", "completed"),
            task_data.get("task_type", "realtime"),
            task_data.get("created_at", now),
            now,  # updated_at
            task_data.get("completed_at", now),
            task_data.get("skill_name", ""),
            task_data.get("llm_model", ""),
            task_data.get("response_time_ms", 0),
            task_data.get("llm_tokens_in", 0),
            task_data.get("llm_tokens_out", 0),
            task_data.get("final_output", "")[:1000]
        ])
        
        conn.commit()
        conn.close()
        
        return {"ok": True, "id": task_id}
    except Exception as e:
        print(f"创建任务失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

### Q5: 如何修改时区显示为 Asia/Beijing？

**解决方案：**

修改 `/root/lingxi-ai-latest/dashboard/v3/index.html`：

```javascript
// 时钟显示
function updateClock() {
    var now = new Date();
    var tz = 'Asia/Beijing';  // 改为 Beijing
    var timeStr = now.toLocaleTimeString('zh-CN', {hour12: false});
    var dateStr = now.toLocaleDateString('zh-CN');
    var el = document.getElementById('clockDisplay');
    if (el) {
        el.innerHTML = tz + ' ' + dateStr + ' ' + timeStr;
    }
}

// 默认时区
function initTheme() {
    var saved = localStorage.getItem('lingxi-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    document.getElementById('themeSelect').value = saved;
    var tzSaved = localStorage.getItem('lingxi-timezone') || 'Asia/Beijing';  // 改为 Beijing
    document.getElementById('timezoneSelect').value = tzSaved;
}
```

---

## 📈 性能监控

### 查看任务统计

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('/root/lingxi-ai-latest/data/dashboard_v3.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM tasks')
print('总任务数:', cur.fetchone()[0])
cur.execute('SELECT channel, COUNT(*) FROM tasks GROUP BY channel')
print('按渠道统计:', cur.fetchall())
cur.execute('SELECT datetime(created_at, \"unixepoch\", \"localtime\") FROM tasks ORDER BY created_at DESC LIMIT 1')
print('最新任务:', cur.fetchone()[0])
"
```

### 查看 Dashboard 日志

```bash
tail -f /tmp/dashboard.log
```

### 查看 OpenClaw 日志

```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

## 🔐 安全建议

1. **Token 保护**
   - Token 文件权限：`chmod 600 ~/.openclaw/workspace/.lingxi/dashboard_token.txt`
   - 不要在代码中硬编码 Token

2. **防火墙配置**
   - 仅开放必要端口（8765）
   - 使用安全组限制访问 IP

3. **定期备份**
   ```bash
   cp /root/lingxi-ai-latest/data/dashboard_v3.db /backup/dashboard_v3_$(date +%Y%m%d).db
   ```

---

## 📝 更新日志

### v3.3.6 (2026-03-13)

**新增功能：**
- ✅ Dashboard v3 MemOS 风格界面
- ✅ 7 大功能模块完整实现
- ✅ 支持 191 条 Layer0 规则管理
- ✅ 记忆/任务/技能 CRUD 操作
- ✅ 数据分析/Token 消耗统计

**Bug 修复：**
- ✅ 修复任务列表时间显示错误（秒级→毫秒级转换）
- ✅ 修复 Dashboard 客户端 httpx 模块缺失
- ✅ 添加 POST /api/tasks 接口
- ✅ 修复时区显示（Asia/Shanghai → Asia/Beijing）

**性能优化：**
- ✅ 快速响应层 <5ms
- ✅ LRU 缓存命中率提升
- ✅ 并行执行复杂任务

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/lingxi-ai-latest.git
cd lingxi-ai-latest

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

---

## 📞 联系方式

- **作者：** Scarlett (斯嘉丽)
- **邮箱：** scarlett@example.com
- **GitHub:** https://github.com/YOUR_USERNAME/lingxi-ai-latest

---

## 📄 许可证

MIT License

---

*心有灵犀，一点就通* 🦞✨
