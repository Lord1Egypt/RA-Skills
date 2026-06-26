# Hooks - 生命周期钩子

本目录包含 OpenClaw 生命周期钩子脚本，实现"安装即运行"的自动化能力。

## 钩子列表

### postinstall.py

**触发时机**：技能安装完成后自动执行

**功能**：
- 检测系统架构（x64/ARM64）
- 从 CNB 仓库克隆私有增强包
- 部署到 `src/privileged/` 目录
- 验证包完整性
- 记录安装日志

**执行方式**：
```bash
# 自动执行（安装时）
clawhub install llm-memory-integration

# 手动执行
python3 hooks/postinstall.py
```

**输出日志**：`.privileged_install.log`

---

### onStartup.py

**触发时机**：OpenClaw Gateway 服务每次启动时

**功能**：
- 检查私有包是否存在
- 检查是否有更新版本
- 记录状态日志
- 提示用户更新（不自动执行）

**执行方式**：
```bash
# 自动执行（Gateway 启动时）
openclaw gateway start

# 手动执行
python3 hooks/onStartup.py
```

**输出日志**：`.privileged_status.log`

---

## 安全说明

| 钩子 | 网络访问 | 文件写入 | 用户确认 |
|------|---------|---------|---------|
| postinstall.py | ✅ Git 克隆 | ✅ 安装私有包 | ❌ 自动执行 |
| onStartup.py | ✅ Git fetch | ❌ 仅读取 | ❌ 自动执行 |

**权限范围**：
- ✅ 读取技能目录
- ✅ 写入 `src/privileged/` 目录
- ✅ Git 网络访问（CNB 仓库）
- ❌ 不修改系统配置
- ❌ 不执行外部 API 调用
- ❌ 不访问用户数据

---

## 故障排查

### postinstall.py 失败

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

### onStartup.py 提示需要更新

**解决方案**：
```bash
cd ~/.openclaw/workspace/skills/llm-memory-integration/src/privileged
git pull
```

---

## 架构支持

- ✅ x64 (x86_64)
- ✅ ARM64 (aarch64)

钩子会自动检测系统架构并选择对应的实现。
