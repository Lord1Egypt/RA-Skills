# 规则文档（_rules_documentation.md）

> **本文件由 scanner 自动排除**（路径 `references/_*.md`），是 scanner 自身的规则说明。文件内故意列出真实危险模式做参考，但全部用 markdown 代码块包裹，**scanner 跳过代码块**；即使未来规则变更导致 scanner 读取本文件，也不会产生误报。
>
> 维护：左运来 | 最后更新：2026-08-20

---

## 🔒 Security（24 条）

### EXEC — 动态代码执行（4 条 · critical）

```
- SEC-EXEC-001  eval() 调用
- SEC-EXEC-002  exec() / execSync() 调用
- SEC-EXEC-003  os.system / subprocess shell=True
- SEC-EXEC-004  new Function() 构造器
```

### NET — 网络外发（4 条）

```
- SEC-NET-001  外发 curl / wget          (high)
- SEC-NET-002  Python requests / aiohttp (medium)
- SEC-NET-003  硬编码 IP 地址            (high)
- SEC-NET-004  URL 短链 / Pastebin       (high)
```

### CRED — 凭据泄露（6 条）

```
- SEC-CRED-001  硬编码 API key / secret / password
- SEC-CRED-002  AWS Access Key ID
- SEC-CRED-003  私钥头 (BEGIN RSA / OPENSSH / PRIVATE)
- SEC-CRED-004  敏感路径 (~/.../id_rsa, ~/.../.aws/credentials 等)
- SEC-CRED-005  1Password op:// URI 误报豁免
- SEC-CRED-006  环境变量批量读取
```

### OBFU — 混淆（3 条 · high）

```
- SEC-OBFU-001  base64 解码
- SEC-OBFU-002  压缩编码 (gzip / zlib)
- SEC-OBFU-003  超长 hex 串
```

### SYS — 系统权限（3 条 · critical）

```
- SEC-SYS-001  sudo / rm -rf
- SEC-SYS-002  chmod 777
- SEC-SYS-003  dd 覆写
```

### PERSIST — 持久化（2 条 · high）

```
- SEC-PERSIST-001  修改 rc / crontab / systemd
- SEC-PERSIST-002  系统包安装 (apt / yum / pip)
```

### INJECT — 注入（2 条 · high）

```
- SEC-INJECT-001  Prompt 注入标记
- SEC-INJECT-002  隐藏指令（HTML 注释藏指令等）
```

### HIDDEN — 隐藏 / 外发（2 条 · high）

```
- SEC-HIDDEN-001  外发到非白名单域
- SEC-HIDDEN-002  文件系统枚举
```

---

## ⚡ Performance（5 条 · medium）

```
- PERF-001  SKILL.md body 行数 > 500
- PERF-002  frontmatter description > 500 字符
- PERF-003  body 字符数 > 30K（~5000 tokens）
- PERF-004  references/ 单文件 > 800 行
- PERF-005  scripts/ 缺少 shebang
```

---

## ✨ Quality（9 条 · low/info）

```
- QUAL-001  frontmatter 必填字段
- QUAL-002  YAML 解析
- QUAL-003  name 格式（kebab-case）
- QUAL-004  禁用文件（.env / 私钥等）
- QUAL-005  license 声明
- QUAL-006  scripts 可执行权限
- QUAL-007  使用示例
- QUAL-008  "When to Use" 段
- QUAL-009  description 触发词
```

---

## 🛡️ 豁免机制（4 层 · v2.1.2 起）

```
1. file_glob（模式库 YAML）        → 限制规则只扫描特定文件类型
2. exception_pattern（模式库 YAML）→ 同行正则豁免
3. <!-- safe-pattern: <reason> -->  → 单行豁免（reason 必须白名单，v2.1.2 起强制）
4. .safe-pattern-manifest.json     → 文件级白名单（v2.1.2 新增，scanner 只在白名单文件认 safe-pattern）
```

> **v2.1.2 关键变更**：本文件即在排除路径（`references/_*.md`）内，是 Step A「移位」的具体落地。scanner 不再需要在本文件上声明 safe-pattern 豁免——直接从扫描范围排除。
