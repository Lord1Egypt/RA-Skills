# Patterns Reference — 模式库参考

> v2.1 模式库 `scripts/patterns/red_flags.yml` 的完整索引。
> 维护：左运来 | 最后更新：2026-08-19

## 📊 总览

| 类别 | 数量 | 严重度默认 | 触发场景 |
|---|---|---|---|
| **Security（安全）** | 24 条 | high | 代码执行/网络/凭据/混淆/系统/持久化 |
| **Performance（性能）** | 5 条 | medium | SKILL.md 大小/行数/token 用量 |
| **Quality（质量）** | 9 条 | low/info | frontmatter/结构/文档 |

合计 **38 条** 自动审计规则。

---

## 🔒 Security（24 条）

### EXEC — 动态代码执行（4 条）

| ID | 名称 | 严重度 |
|---|---|---|
| SEC-EXEC-001 | `eval()` 调用 | 🔴 critical |
| SEC-EXEC-002 | `exec()` / `execSync()` 调用 | 🔴 critical |
| SEC-EXEC-003 | `os.system` / `subprocess shell=True` | 🔴 critical |
| SEC-EXEC-004 | `new Function()` 构造器 | 🔴 critical |

### NET — 网络外发（4 条）

| ID | 名称 | 严重度 |
|---|---|---|
| SEC-NET-001 | 外发 `curl`/`wget` | 🟠 high |
| SEC-NET-002 | Python `requests`/`aiohttp` | 🟡 medium |
| SEC-NET-003 | 硬编码 IP 地址 | 🟠 high |
| SEC-NET-004 | URL 短链 / Pastebin | 🟠 high |

### CRED — 凭据泄露（6 条）

| ID | 名称 | 严重度 |
|---|---|---|
| SEC-CRED-001 | 硬编码 API key/secret/token | 🔴 critical |
| SEC-CRED-002 | 硬编码密码字段 | 🔴 critical |
| SEC-CRED-003 | AWS Access Key ID | 🔴 critical |
| SEC-CRED-004 | Private Key 头 | 🔴 critical |
| SEC-CRED-005 | 访问敏感路径（`~/.ssh` 等） | 🟠 high |
| SEC-CRED-006 | 读取 OpenClaw 核心记忆文件 | 🟠 high |

### OBFUSC — 混淆（4 条）

| ID | 名称 | 严重度 |
|---|---|---|
| SEC-OBFUSC-001 | `base64 -d` 解码 | 🟠 high |
| SEC-OBFUSC-002 | Python `base64.b64decode` | 🟠 high |
| SEC-OBFUSC-003 | 压缩/编码字符串 | 🟡 medium |
| SEC-OBFUSC-004 | 超长十六进制串 | 🟡 medium |

### SYS — 系统权限（4 条）

| ID | 名称 | 严重度 |
|---|---|---|
| SEC-SYS-001 | `sudo` / `setuid` | 🟠 high |
| SEC-SYS-002 | `rm -rf` 危险删除 | 🔴 critical |
| SEC-SYS-003 | `chmod 777` 全开 | 🟡 medium |
| SEC-SYS-004 | `dd` 块设备覆写 | 🔴 critical |

### PERSIST — 持久化（2 条）

| ID | 名称 | 严重度 |
|---|---|---|
| SEC-PERSIST-001 | 修改 `rc`/`crontab`/`systemd` | 🔴 critical |
| SEC-PERSIST-002 | 系统级包安装 | 🟡 medium |

---

## ⚡ Performance（5 条）

| ID | 名称 | 阈值 | 严重度 |
|---|---|---|---|
| PERF-SIZE-001 | SKILL.md body 行数过多 | > 500 行 | 🟡 medium |
| PERF-SIZE-002 | frontmatter description 过长 | > 500 字符 | 🔵 low |
| PERF-SIZE-003 | SKILL.md body 字符数过多 | > 30K 字符（~5000 tokens） | 🟡 medium |
| PERF-SIZE-004 | references/ 单文件过大 | > 800 行 | 🟡 medium |
| PERF-STRUCT-001 | scripts/ 缺少 shebang | 无 `#!/...` | 🔵 low |

---

## ✨ Quality（9 条）

| ID | 名称 | 严重度 |
|---|---|---|
| QUAL-FM-001 | frontmatter 缺少必填字段（`name`/`description`） | 🟠 high |
| QUAL-FM-002 | frontmatter YAML 解析失败 | 🟠 high |
| QUAL-FM-003 | `name` 包含非法字符 | 🟡 medium |
| QUAL-STRUCT-001 | 包含禁用文件（README.md/CHANGELOG.md 等） | ⚪ info |
| QUAL-STRUCT-003 | 缺少 license 声明 | ⚪ info |
| QUAL-DOC-001 | SKILL.md 缺少使用示例 | 🔵 low |
| QUAL-DOC-002 | SKILL.md 缺少「When to Use」段 | 🔵 low |
| QUAL-DOC-003 | SKILL.md description 触发词不足 | 🔵 low |

> 注：QUAL-STRUCT-002 已规划但未实现（scripts 可执行权限检测，audit.py 当前不强制）。

---

## 🛡️ 豁免机制

### 1. `exception_pattern`（YAML 内）

模式定义中的 `exception_pattern` 字段提供正则豁免：

```yaml
- id: SEC-CRED-001
  regex: '...'
  exception_pattern: '\$\{?[A-Z_]+\}?'  # 环境变量引用 ${API_KEY} 不命中
```

### 2. `# safe-pattern:` 注释（代码内）

任意一行带 `# safe-pattern:`（Python/Shell）或 `// safe-pattern:`（JS）注释即豁免：

```python
# 安全示例：演示 setuid 用法（仅文档）
os.setuid(0)  # safe-pattern: doc-example，非真实调用
```

### 3. 默认跳过目录（`audit.py` 内置）

- `scripts/patterns/` — 模式定义目录（避免自指）
- `scripts/audit.py` — 审计器自身代码

---

## ✏️ 自定义模式

### 添加新规则

编辑 `scripts/patterns/red_flags.yml`：

```yaml
security:
  groups:
    - id: SEC-CUSTOM-001
      category: custom
      name: "我的自定义规则"
      severity: medium
      regex: '\b我的危险模式\b'
      description: "为什么危险"
      file_glob:           # 可选，只匹配某些文件
        - "*.py"
      exception_pattern:   # 可选，豁免正则
        '注释标记'
```

### 调整阈值

`performance.metrics` 改字段值：

```yaml
- id: PERF-SIZE-001
  max_lines: 500  # 改为 800 更宽松，或 300 更严格
```

修改后无需重新编译——`audit.py` 每次加载模式库。

---

## 📐 模式库版本

| 版本 | 日期 | 变更 |
|---|---|---|
| 2.1.0 | 2026-08-19 | 修 .key 词边界（SEC-CRED-005）；file_glob 风格统一 |
| 2.0.1 | 2026-08-19 | 3 个误判修复 + severity-cap 机制 |
| 2.0.0 | 2026-08-19 | 初版，从 v1.0 人工红线机械化扩展 + 性能/质量维度 |

---

*模式库是 lz-skill-vetter-plus 的核心，所有变更必须经过 v2.1 自身的 audit.py 自扫描验证。*