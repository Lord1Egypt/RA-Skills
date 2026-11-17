# Windows 应急响应现场手册（企业版）

> 来源吸收：`NOPTrace-Windows-应急响应手册-整理版`  
> 目标：把 Windows 现场排查动作沉淀成“日志优先、证据优先、低误用”的企业 SOP。

## 1. 常见事件类型
- 挖矿病毒
- 远控后门 / 木马
- 隧道事件
- 非持续性事件
- 暴力破解（RDP / SMB / SNMP / FTP / MSSQL）
- 钓鱼事件
- 勒索事件
- BadUSB 投毒
- MSSQL 事件

## 2. Windows 现场通用顺序
1. 确认告警真实性并固定日志/取证副本
2. 由 IOC / 文件路径 / 端口 / 登录日志 / 勒索信定位线索
3. 由 PID / 会话 / 登录用户反查：
   - 进程路径
   - 命令行
   - 启动时间
   - 关联网络连接
   - 登录类型
4. 必要时先暂停进程验证
5. 采样恶意文件与关键日志
6. 再做隔离、杀进程、删除、恢复
7. 做常规安全检查与横向定损

## 3. 高频命令清单

### 3.1 进程与时间
```powershell
Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 5 ProcessName, Id, CPU
Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object -Property Id, ProcessName, WorkingSet -First 5
$process = Get-Process -Id <pid>
$process.StartTime
```

```cmd
wmic process where ProcessId=<PID> get ProcessId, CreationDate
wmic process where ProcessId=<PID> get Name, ExecutablePath, CommandLine /format:list
tasklist
tasklist /svc
tasklist /v
```

### 3.2 网络与会话
```cmd
netstat -ano | findstr "ip/端口"
query user
query session
```

```powershell
Get-SmbSession
```

### 3.3 安全日志
```powershell
Get-WinEvent -LogName Security -FilterXPath '*/System/EventID=4624'
Get-WinEvent -LogName Security -FilterXPath '*/System/EventID=4625'
```

```cmd
wevtutil qe Security /q:"Event/System/EventID=4624" /f:text /rd:false /c:10
wevtutil qe Security /q:"Event/System/EventID=4625" /f:text /rd:false /c:10
```

高价值事件 ID：
- `4624` 登录成功
- `4625` 登录失败
- `4634` 注销成功
- `4647` 用户主动注销
- `4648` runas 登录
- `4672` 特权登录
- `4720` 创建用户
- `4722` 启用用户
- `4726` 删除用户
- `4778` 会话重新连接
- `4779` 会话结束
- `1102` 日志被清理
- `7045` 新服务安装

### 3.4 计划任务、服务、启动项
```cmd
schtasks /query
schtasks /query /fo LIST /v
net user
set
wmic qfe list
systeminfo
```

重点注册表路径：
- `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run`
- `HKU\{SID}\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`

### 3.5 WMI 持久化
```powershell
Get-CimInstance -ClassName __Namespace -Namespace "root" | Select-Object Name
Get-WmiObject -Namespace "root\\subscription" -Query "SELECT * FROM __EventFilter"
Get-WmiObject -Namespace "root\\subscription" -Query "SELECT * FROM __EventConsumer"
Get-WmiObject -Namespace "root\\subscription" -Class "__FilterToConsumerBinding"
```

## 4. 事件分流重点

### 4.1 暴力破解
- 以日志为主，不要迷信 `netstat`
- RDP 失败不要只筛 `LogonType=10`；很多场景登录失败看 `4625` 且类型是 `3`
- 成功登录后要继续查：
  - 新会话
  - 新服务
  - 横向访问
  - 新用户/提权

### 4.2 勒索
- 先确认家族、后缀、勒索信、加密时间段
- 先做取证，再恢复
- 解密工具必须先测试，已加密文件先备份

### 4.3 钓鱼
- 先切断传播与继续点击
- 确认邮件/IM 来源、链接、附件、点击用户、下载行为
- 继续判断是否凭据泄露、是否被控、是否横向

### 4.4 非持续性事件
- 现场可能没有明显进程与文件
- 更适合短期监控与等待再次触发，抓到稳定线索后再处置

### 4.5 MSSQL
- 重点看：
  - 登录日志
  - 执行 SQL
  - 存储过程
  - 程序集
  - 作业（Job）
  - OLE 接口

## 5. 取证与保全要点
- 先备份日志，再分析。
- 需要内存态时，快照不能替代内存取证。
- 重要证据：
  - 进程路径/命令行
  - 登录日志
  - 网络连接
  - 恶意样本
  - 计划任务/服务/WMI
- 现场不应过早删除文件或清理日志。

## 6. 暂停与终止
必要时先暂停验证：
```cmd
pssuspend.exe <pid>
pssuspend.exe -r <pid>
```

终止：
```cmd
taskkill /pid <pid>
taskkill /f /pid <pid>
taskkill /t /pid <pid>
```

```powershell
Stop-Process -Id <pid> -Force
```

## 7. 高风险误区
- 不要一上来就强制结束进程
- 不要只依赖单一日志源
- 不要把“有微软签名”视为无害
- 不要在生产现场贸然运行会触发程序执行的检测工具
- 不要把杀毒白名单范围自动视为安全区域

## 8. 善后与扩面
至少检查：
- 同密码服务器
- 同漏洞版本/同服务资产
- 同一管理员维护的服务器
- 可直接互信访问的资产
- 受害期间高频交互的主机

恢复动作最低要求：
- 改密 / 吊销高风险凭据
- 加固邮件与终端策略
- 做同类资产横向排查
- 把事件转化为培训和检测规则
