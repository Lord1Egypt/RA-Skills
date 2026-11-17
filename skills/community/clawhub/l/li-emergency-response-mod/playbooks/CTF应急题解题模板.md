# CTF 应急题（Solar 风格）解题模板（可复现 / 可复盘）

> 目标：把“应急题解题”当成一次桌面演练：**题目问题 = 子任务**，每个答案都必须指向证据锚点（VBR）。  
> 输出：题目答案清单（flags/字段值）+ 时间线 + IOC + 最短复现路径（相当于 WP）。

---

## 1) 开始前：先把“题目问题”转成任务板

建议先整理成表格（不要直接开干）：

| 题目问题 | 需要的数据源 | 预期证据锚点 | 当前状态 |
|---|---|---|---|
| 攻击者 IP 是什么 | Web 访问日志 / pcap | 某段日志行/某条流量会话 | 未解 |
| 恶意文件名是什么 | 上传日志/目录 | 文件名/路径/哈希 | 未解 |
| 首次成功登录时间 | MSSQL/安全日志 | 事件 ID/日志行 | 未解 |

并把这张任务板的结论写入 WAL（notes/next_steps）。

---

## 2) 数据源优先级（Solar 题常见组合）

1) **流量（pcap/pcapng）**：HTTP 对象、上传文件、webshell 交互、可疑外联  
2) **Web/应用日志**：扫描行为、可疑路径、参数、状态码差异  
3) **系统日志（Windows/Linux）**：登录/提权/计划任务/服务/进程创建  
4) **数据库日志（如 MSSQL ERRORLOG）**：暴破→首次成功登录→执行命令链  
5) **内存取证线索**：驻留/无落地（建议先导出再“清理”，避免丢线索）  

---

## 3) 解题主线（推荐顺序）

### Step A：时间线锚点（先定“什么时候”）
- 找到关键时间窗口：首次扫描/首次成功登录/首次命令执行/首次外联/持久化落地
- 记录到 WAL：`--timeline`

### Step B：入侵路径（再定“怎么进来”）
- Webshell：上传→落地→交互（结合日志与 pcap）
- 弱口令/暴破：大量失败→首次成功→后续行为
- 漏洞利用：特征请求（典型 payload）+ 后续落地

### Step C：主机侧证据（“做了什么”）
- 进程/命令：计划任务、systemd、powershell、bash_history（按题目要求）
- 文件/后门用户：可疑 UID0、/etc/passwd 变更、服务 unit

### Step D：输出答案（每题必须给 VBR 证据）
1) 每个答案都要有：命令/查询语句 + 输出片段（证据文件）  
2) 每个答案写入 WAL：`--flag "问题=答案"` 并关联 `--evidence`

示例：
```bash
python3 scripts/note.py --flag "攻击者IP=10.0.100.22" --evidence "./evidence/accesslog-snippet.txt"
python3 scripts/note.py --flag "恶意文件名=helloworld.zip" --evidence "./evidence/upload-log.txt"
```

---

## 4) 常见题型“最小验证（VBR）提示”

1) **攻击者 IP**：访问日志中扫描行为 + 与 webshell 文件交互频繁；pcap 中对应会话  
2) **恶意文件名/路径**：上传日志/HTTP multipart、解密流量后提取对象、或磁盘目录  
3) **首次成功登录时间**：MSSQL/安全日志中“登录成功”事件 + 前序暴破失败事件  
4) **持久化点**：计划任务/systemd/service/注册表 run 键（写证据文件与路径）  
5) **外联 IP:PORT**：ss/netstat/tcpdump/pcap 中外联连接（注意区分噪声）  

---

## 5) 解题结束交付（相当于 WP）

建议至少产出：
- `reports/ir-ctf-report.md`：报告草稿（含 IOC、关键动作、证据清单）
- `reports/timeline.md`：时间线

命令：
```bash
python3 scripts/generate_report.py --out reports/ir-ctf-report.md
```
