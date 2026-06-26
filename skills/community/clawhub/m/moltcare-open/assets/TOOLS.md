# TOOLS.md - 环境工具清单

> 🔧 **本地工具与环境配置** | 与 OpenClaw 系统对应

---

## 🏠 工作环境

### 主机信息
| 属性 | 值 |
|------|-----|
| **主机名** | {{HOSTNAME}} |
| **操作系统** | {{OS}} |
| **架构** | {{ARCH}} |
| **工作目录** | {{WORKSPACE_DIR}} |

### Shell 环境
| 属性 | 值 |
|------|-----|
| **Shell** | {{SHELL}} |
| **终端** | {{TERMINAL}} |
| **编辑器** | {{EDITOR}} |

---

## 🔌 已配置工具

### 核心工具（必需）
| 工具 | 版本 | 用途 | 状态 |
|------|------|------|------|
| Python | {{PYTHON_VERSION}} | 脚本运行 | ✅ |
| Node.js | {{NODE_VERSION}} | 前端/工具 | {{STATUS}} |
| Git | {{GIT_VERSION}} | 版本控制 | ✅ |

### OpenClaw 特定工具
| 工具 | 状态 | 说明 |
|------|------|------|
| **read** | ✅ | 读取文件内容 |
| **edit** | ✅ | 编辑文件 |
| **write** | ✅ | 创建新文件 |
| **exec** | ✅ | 执行 shell 命令 |
| **memory_search** | ✅ | 语义检索记忆 |
| **sessions_spawn** | ✅ | 创建子代理 |
| **web_search** | {{STATUS}} | 网络搜索 |
| **browser** | {{STATUS}} | 浏览器控制 |

### 编程语言支持
| 语言 | 版本 | 包管理器 | 状态 |
|------|------|----------|------|
| Python | {{VERSION}} | pip/uv | ✅ |
| JavaScript | {{VERSION}} | npm/pnpm | {{STATUS}} |
| Bash | {{VERSION}} | - | ✅ |

---

## 🔑 API Keys 与凭证

### 已配置的 API Keys
| 服务 | 状态 | 用途 | 备注 |
|------|------|------|------|
| GitHub | {{STATUS}} | 代码仓库 | {{NOTE}} |
| OpenAI | {{STATUS}} | AI 服务 | {{NOTE}} |
| Other | {{STATUS}} | {{PURPOSE}} | {{NOTE}} |

### 凭证管理
```bash
# 凭证存储位置
~/.config/openclaw/credentials/
~/.env
~/.ssh/
```

**安全提示**：凭证文件已添加到 .gitignore，不会意外提交

---

## 📝 常用命令速查

```bash
# MoltCare 自检
cat ~/.openclaw/workspace/SOUL.md | head -20

# 查看今日记忆
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md

# 系统状态
openclaw status

# 健康检查
HEARTBEAT
```

---

## 🎯 任务分层工具

### L0: 纯脚本层 (零 Token)

```bash
# 数据采集与处理
curl -s "https://api.example.com/data" | jq '.'
python process_data.py
node fetch-and-save.js

# 定时任务配置
crontab -e
crontab -l
```

### L1: 查询展示层 (零 Token)

```bash
# 读取缓存数据
cat cache/status.json
cat logs/metrics.log | tail -50

# 数据聚合
jq '.items | length' data.json
awk '{sum+=$1} END {print sum}' numbers.txt
```

### L2: 条件触发层 (按需 Token)

```bash
# 阈值检查脚本
node check-threshold.js --metric=cpu --limit=80

# 异常时触发通知
./alert-wrapper.sh "$(node monitor.js)"

# 条件执行
[ -f "alert.flag" ] && node notify.js
```

### L3: AI 决策层 (正常 Token)

```bash
# 仅在脚本层无法处理时调用
# 由 Agent 自动判断，无需手动触发
```

**设计检查清单**:
- [ ] 这个任务能用脚本完成吗？
- [ ] 是否需要实时判断？能否改为条件触发？
- [ ] 数据是否已缓存？能否增量更新？
- [ ] AI 调用是否携带了最小必要上下文？

---

## 🔧 待配置工具

| 工具 | 用途 | 优先级 | 计划时间 |
|------|------|--------|----------|
| {{TOOL}} | {{PURPOSE}} | {{PRIORITY}} | {{DATE}} |

---

*此文件由 Agent 根据环境自动更新*
*配合 OpenClaw 使用*
