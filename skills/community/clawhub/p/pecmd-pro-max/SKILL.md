---
name: pecmd-pro-max
version: 1.8.1
description: |
  PECMD2012 WinPE 脚本编程 — 轻量级 Windows GUI、系统工具、启动/初始化
  脚本、自动化。适用于 .wcs/.wci/.wce 文件、磁盘分区、批处理转 PECMD、
  系统信息收集、PE/预安装环境工具、PECMD 代码调试。
  参考文件：references/commands-full.md、references/pecmd-gui.md、references/pe-startup.md、
  references/how-tos/storage.md、references/how-tos/system.md、references/how-tos/gui.md、references/how-tos/net.md、
  references/troubleshooting.md。内置 bin/（PECMD 1.88 解释器）与 examples/（43 个完整示例）。
compatibility: 需要 PECMD2012 v1.88+ 解释器。脚本运行于 PECMD/WinCMD 环境，非 cmd.exe。
---

# PECMD Pro Max

你是 PECMD 专家程序员。PECMD 是从 XCMD V2.2 演进而来的 WinPE 命令解释器与脚本语言——可将其视为 Windows PE 系统管理和轻量级 GUI 工具的领域特定语言。

## $1 心智模型

PECMD 有两种执行模式：
- **命令行模式**：`PECMD.EXE ENVI $PPPoE=OK` — 单条命令，注释默认关闭
- **脚本模式**：`PECMD.EXE LOAD C:\PECMD.INI` — 多命令文件，注释默认开启

PECMD 脚本是一组平铺的顶层语句。从上到下顺序执行。`_SUB` 块在解析时声明，仅在 CALL 时运行。所有 GUI 由定义窗口函数的 `_SUB` 块创建（通过 `CALL @窗口名` 调用）。

关键运行时事实：
- `PECMD.EXE MAIN 路径\PECMD.INI` — 标准 WinPE 入口，执行 INI 并启动消息循环
- 可在 PECMD 内运行 PECMD：`EXEC =!"%MyNAME%" <命令>` — 用于隔离的子操作
- `EXIT FILE` 退出当前脚本文件/LOAD 层并返回调用者（多文件嵌套时不是终止整个进程）；`EXIT _SUB` 从当前函数返回
- 循环体内 `EXIT CONTINUE` 继续下一次迭代；`EXIT -` 跳到当前 `{}` 块尾部；`EXIT LOOP` / `EXIT FORX` / `EXIT BREAK` 跳出循环；`EXIT ToWin` 中止函数返回窗口消息循环
- 脚本文件常用 `.wcs` 扩展名（也支持 `.wce`、`.wci`、`.wcx`、`.ini`、`.inf`、`.txt`、`.log` 等）。编码声明必须与文件实际字节一致：GBK 用 `#code=936`（PE 生态默认），UTF-8 用 `#code=65001`；有 BOM 时以 BOM 为准。若首行以 `#!` 开头，编码指令放在第二行。
- 技能内置解释器：`bin/PECMD64.exe`（x64）、`bin/PECMD32.exe`（x86），均为 1.88.05.94 完整版；控制台 I/O 用 `bin/PECMD*-cli.exe`。本地验证不需要外部 SDK，见 `bin/README.md`。

**标准 I/O（stdin/stdout/stderr）：**
- `READ -,n,&var` — 从 stdin 读取一行
- `WRIT -,$+0,text` — 写入 stdout
- `WRIT --,$+0,text` — 写入 stderr
- `LOGS * CONOUT$` — 输出到控制台（调试终端输出）

## $2 变量系统

PECMD 有**四种访问前缀**，对应三种存储层级，外加逐级查找。最常见的错误是把 `%var%` 当成“永远是环境变量”。

| 层级 | 语法 | 设置方式 | 作用域 |
|------|------|----------|--------|
| 环境变量 | `%^var%`（显式）或 `%var%`（模式相关） | `ENVI ^var=val`、`ENVI-env var=val`；`ForceLocal=0` 时 `ENVI var=val` | 进程级；`EXEC` 子进程会继承 |
| PE 全局变量 | `%&::var%` | `ENVI &::var=val` 或 `SET &::var=val` | 跨函数、跨线程、文件级，永不自动销毁 |
| PE 局部变量（本级） | `%&&var%` | `SET &&var=val`、`ENVI &&var=val`、`SET-def var=` | 当前 `_SUB`/`{}` 块，退出自动销毁 |
| PE 变量（逐级查找） | `%&var%` | `ENVI &var=val` 或 `SET var=val` | 当前级→外层→全局；读取未定义返回空，赋值时才创建 |

**`&a` 解析顺序**（由内向外）：
1. 当前范围的 `&&a`
2. 逐层向外的 `&&a`
3. 全局 `&::a`
4. 都没有：读取为空（`EnviMode=1`）；只有赋值时才在当前级创建

**关键规则：**
1. `ENVI^ ForceLocal=1` 放在文件顶部——强制所有变量按 PE 变量处理（`ENVI var=` 等价 `ENVI &var=`），**不会**把变量提升为本级 `&&`。默认 `ForceLocal=0`。要保证本级新建，用 `SET &var=` / `ENVI &&var=` / `SET-def`。
2. `ENVI^ EnviMode=1` — 未定义变量解释为空字符串，顺序解释一遍。推荐始终使用。默认 `EnviMode=0` 兼容 4.0：未定义变量保留字面量，多轮次非顺序解释。
3. `SET` 等价于 `ENVI &`（PE 变量、逐级查找），**不等于** `ENVI &&`；`SET &var=` 才等价于本级新建。ForceLocal 只影响 ENVI 的默认解释方式，不改变 SET 的本义。
4. `%Desktop%` 是内置环境变量；没有内置 `%&Desktop%`。需要 PE 版本时先 `ENVI &Desktop=%Desktop%`。
5. 多线程代码中务必使用 PE 变量（`&var`）——环境变量跨线程共享会竞态。跨线程通信用 `&::` 类变量。
6. `SET~ &&dest=T[%i%]` — `~` 把等号后的值再解释一次，并把结果作为变量名取它的值；伪数组用 `T[%i%]` 形式，不是点号成员。
7. `^` 前缀（`^SET`、`^ENVI`、`^CALC`、`^IFEX` 等）— 把本命令预先解释一遍（`^^` 两遍），用于 TEAM/事件字符串中拼接动态变量名；不是“推迟到执行时”。
8. `ENVI-ret %~1=%var%` — 将值设置到*名称*存储在 `%~1` 中的变量（引用返回）。
9. `SET-def var=value` — 仅在变量未定义时设置（安全默认值）。
10. `ENVI $var=val`（`$` 后有空格）= 系统级环境变量并广播，最多等待 5 秒；`ENVI$var=val`（无空格）= 十六进制转字符串。普通进程环境用 `ENVI var=`（ForceLocal=0）或 `ENVI ^var=`。
11. `ENVI-ex 返回名=[&|&&]变量名` — 检查变量是否存在（`&`=PE，`&&`=本级 PE，省略=环境）。
12. `ENVI^ EXPORTLOCAL=1` — 允许 `EXEC` 子进程继承 PE 变量（默认 0 不继承）。

### ENVI^ / ENVI @@ 运行时控制命令

| 命令 | 功能 |
|------|------|
| `ENVI^ EnviMode=1` | 标准模式：空变量解释为空字符串，顺序解释1遍 |
| `ENVI^ ForceLocal=1` | 强制所有变量为 PE 变量，最简多线程/并行窗口 |
| `ENVI^ EXPORTLOCAL=1\|0\|&1\|&0` | PE 变量继承：1=继承，0=隔离（默认），&1=仅本级及以下继承，&0=仅本级及以下隔离 |
| `ENVI^ Alias name=cmd` | 命令别名：替代命令前半部（可包装 DLL 调用为伪命令） |
| `ENVI^ WndProc[1\|2\|3][C][,ptr]` | Win32 回调绑定（C=C 调用约定） |
| `ENVI^ memvar=[?返回名,][:字节数:]偏移,值` | 修改/查询 PECMD 内存变量 |
| `ENVI^ LoadPlugin=basename` | 加载插件 |
| `ENVI^ DisX64=1[,Old]` | 禁用/恢复 WOW64 文件系统重定向 |
| `ENVI^ zero=0\|1` | 私密模式：内存用完清零 |
| `ENVI^ Arg=*[字符集]字符串` | 词语分断 |
| `ENVI^ Clipboard=text\|?=var` | 读写剪贴板 |
| `ENVI^ EnviBroad=0\|1\|-` | 环境变量广播开关 |
| `ENVI^ __arg=0\|1` | 兼容模式：启用 `&&__arg` 参数表 |
| `ENVI^ LoadEnvi [路径\|-] [变量名]` | 从注册表刷新环境变量 |
| `ENVI^ HelpColor=[*高度] [前景色][#背景色]` | HELP 显示颜色 |
| `ENVI @@DeskTopFresh=[clearicon][;][1\|2\|4\|8\|16][;[-+]path]` | 桌面刷新 |
| `ENVI @@TaskIcoMenu=0\|1\|2` | 托盘菜单切换（0=关闭, 1=开启, 2=切换） |

> 完整 ENVI^ 控制命令、二进制缓冲区操作（SET-cmp、SET-tom、SET-copy、SET?int 等）和函数参数引用，参见 [commands-full.md](references/commands-full.md)。

### ENVI-env / SET-env — 临时关闭 ForceLocal

`ENVI-env` 和 `SET-env` 是**临时关闭 ForceLocal 的模式后缀**（必须紧跟命令），不是“直接写环境变量”的独立命令。关闭后仍按目标变量是否带 `&` 决定层级：
- `ENVI-env A1=...` 写环境变量；`SET-env &A2B=...` 仍写 PE 变量。
- 右侧 `%A1%` 在 `-env` 模式下优先按环境变量解析——这是读取父窗口环境上下文的用法。

```wcs
SET-env &hwnd0=%__WinID%    // 右侧 %__WinID% 优先按环境变量解析，结果写入 PE 变量 &hwnd0
ENVI-env MyName=%MyName%    // 写入进程环境变量
```

```wcs
#code=65001
ENVI^ EnviMode=1
ENVI^ ForceLocal=1
SET$ &NL=0d 0a
SET$ &TAB=09
```

### 十六进制数据与原始内存

```wcs
SET$ &NL=0d 0a                  // 十六进制转宽字符串（Unicode）
SET$# &buf=*4096 0              // 十六进制转原始字节（二进制缓冲区）
ENVI$ &data=*1M 30 0d 0a        // 可变长度十六进制分配
```

## $3 代码组织

### 函数与 CALL 变体

```wcs
_SUB 函数名 [*]                   // * = this-call（在调用者栈中运行）
    SET &param1=%~1                 // %~1 剥离外层引号
    ENVI-ret %~3=%&result%          // 通过引用参数返回值
    // 函数参数：%0=函数名, %1~%n=各参数, %#=参数个数, %*=全部参数, %~=去掉引号
_END
```

```
CALL 函数名 [参数]                 // 调用函数
CALL *函数名 [参数]                // this-call（调用者栈）
CALL @窗口名 [参数]                // 创建/显示窗口（模态，阻塞）
CALL @*窗口名 [参数]               // 并行窗口（可同时操作，但关闭前阻塞后续命令）
CALL @-窗口名 [参数]               // 后台窗口
CALL @~窗口名 [参数]               // 后台，完全非阻塞
CALL @~~窗口名 [参数]              // 后台快速调用（非阻塞）
CALL @^窗口名 [参数]               // 类似 @*，父窗口不遮挡子窗口（Z 序），仍阻塞后续命令
CALL @+窗口名 [参数]               // 弃养子窗口
CALL @--                           // 卸载当前 Win 环境（不接窗口名；关窗用 KILL）
CALL @--popmenu[:x.y[:对齐]] 菜单名 // 弹出菜单（对齐：1=左 2=上 4=右 8=下）
CALL --mem &变量名 [*] [参数]      // 执行内存中的动态函数代码
```

### 窗口（GUI）

```wcs
_SUB 窗口名,L200T100W400H300,窗口标题,[关闭命令],[图标],[样式],[遮罩] [-标志1 -标志2 ...]
_END
```

窗口形状：`L<左>T<上>W<宽>H<高>`。省略 L/T 则居中。
窗口样式：`-` = 无标题栏，`#` = 无边框，数字 1-99 = 透明度，`$` = 0-255 刻度，100/$255 = 隐藏，`:`透明色。
常用标志：`-trap`（关闭按钮不退出）、`-nocap`（无标题栏）、`-nosysmenu`、`-top`、`-size`、`-maxb`、`-disminb`、`-discloseb`、`-nfocus`、`-ntab`、`-forcenomin`、`-scalef`、`-scale[:DPI]`、`-nxp`、`-csize`、`-na`、`-layer`（支持渐透明）、`-disaltmv`（禁用 ALT 拖动）

### IMPORT 与代码块

```wcs
IMPORT 路径\库文件.wcs          // 将可复用函数加载到当前脚本
_ENDFILE-IMPORT                // 此行以下内容在 IMPORT 时被丢弃

{                               // 带独立 PE 变量栈的代码块
    SET temp=仅此处有效
}
{*                              // this-call 代码块（在调用者栈中运行）
    LOCK .ole                   // COM 初始化等需要在当前作用域执行的操作
}
```

文件级和函数级的 `{` 必须是该行第一个非空白字符（可缩进）。嵌套 `_SUB` 用双冒号访问：`类名::子函数名`。点号用于数据成员访问（如 `类名.属性`）。

## $4 流程控制

### FIND — 条件判断（`*c` 是命令级后缀）

```wcs
FIND $%var%=hello, 命令               // 相等（不区分大小写）
FIND*c $%var%=hello, 命令             // 相等（区分大小写；*c 紧跟 FIND）
FIND $%var%<>hello, 命令              // 不等
FIND $%var%=, 命令                    // 字符串为空
FIND *=var, 命令                      // * 模式：PE 变量为空（也可写 FIND *&var=）
FIND *<>var, 命令                     // * 模式：PE 变量非空（也可写 FIND *<>&var）
FIND $'%a%'='%b%', 命令               // 单引号保护：值含空格/比较符时使用
FIND |%a%>%b%, 命令                   // | 前缀 = 浮点数比较
FIND #%a%>%b%, 命令                   // # 前缀 = 整数比较（INT64）
FIND [ $A & $B ], 命令                // 复合 AND
FIND [ $A | $B ], 命令                // 复合 OR（| 分隔）
FIND --pid &var,                     // 仅系统时间 5 值，不是 PID；按名取 PID 用 --pid*@
FIND --pid*@ &var,                   // 进程列表（用于 TABL）
FIND --class:Shell_TrayWnd --wid*@ &var  // 按类名过滤窗口列表
FIND --forpid:PID --wid*@ &var       // 按进程 ID 过滤窗口
FIND --sub --wid*@ &var              // 递归子窗口
FIND --menu &var,窗口ID              // 查询窗口的 MENU 句柄
FIND --menu#Index &var,MenuID        // 按索引查询子 MENU
```

### IFEX — 文件测试 / 数值比较

```wcs
IFEX C:\boot.ini, 命令                // 文件/目录存在
IFEX C:\boot.ini,! 命令               // 不存在
IFEX x:\, 命令                        // 盘符存在且有文件系统
IFEX $%val%>=5, 命令                  // $=浮点数比较（#=整数比较，|=字符串比较）
IFEX |'%a%'='%b%', 命令               // | 或单引号 = 字符串比较（含空格时安全）
IFEX [$%v%>5 & $%w%<10], 命令        // [ 后跟 $：后续全部按浮点比较
IFEX [|'%a%'='x' & %b%=1], 命令      // [ 后跟 |：后续全部按字符串比较
IFEX [ 条件1 & 条件2 ], 命令          // AND 复合条件
IFEX [ 条件1 | 条件2 ], 命令          // OR 复合条件（| 分隔）
IFEX MEMU=?,&var                     // 查询可用内存
IFEX C:\=?,&可用空间                  // 查询磁盘可用空间
```

### LOOP / FORX / TEAM / LOCK

```wcs
SET &&I=0
LOOP #%&I%<=10,
{
    MESS %&I%
    CALC &I=%&I% + 1
}
LOOP #1=1,
{
    ...                                             // # = 整数比较；#1=1 即无限循环
}
LOOP $%&a%=done,
{
    ...                                             // $ = 字符串比较
}
LOOP |%&f%<1.5,
{
    ...                                             // 省略或 | = 浮点比较
}

FORX * %&list%,&&item,
{
    MESS %&item%
}
FORX *NL &多行变量,&&line, { ... }                    // *NL = 换行分隔
FORX *NL:| &数据,&&item, { ... }                     // *NL:分隔符 = 自定义分隔符
FORX *L 0 2 10,&&val, { ... }                        // *L = 数值循环（起始 步长 结束）
FORX /S C:\Windows\*.exe,&&file,0, { ... }           // 次数后必须有逗号再跟命令/块
FORX @\Windows,&&winDir,1, { ... }                   // @=仅搜索目录，\=所有盘符

// FORX 循环变量：块内引用 %&item%（单&）；同一作用域也可用 %&&item%（官方示例），
// 但跨 {} 子块会失效，统一写 %&item% 最稳。

TEAM SET &a=1| SET &b=2| CALC &c=%&a% + %&b%         // 多命令链

// 线程
THREAD* CALL WorkerFunc                             // * = 保持父子关系；仅窗口/*函数才共享变量
THREAD CALL WorkerFunc                              // 独立模式（复制变量到子线程）
THREAD& CALL WorkerFunc                             // & = 强制 PE 变量模式（最简多线程）
THREAD+ CALL WorkerFunc                             // + = 抛弃式线程（不等待退出）
THREAD# CALL WorkerFunc                             // # = 代理模式（线程结束则退出）
THREAD $ CALL WorkerFunc                            // $ = 预先解释命令组
THREAD -link CALL WorkerFunc                        // 保持父子关系（类似 *）
THREAD -wait CALL WorkerFunc                        // 等待完成（阻塞消息循环）
THREAD -waitx CALL WorkerFunc                       // 等待完成（不阻塞消息循环）
THREAD -here CALL WorkerFunc                        // 当前栈的孩子（可修改父栈临时PE变量）
THREAD -waitp CALL WorkerFunc                       // 进程结束前等待该线程
THREAD -tid:&tid CALL WorkerFunc                    // 获取线程 ID
THREAD --st:128K CALL WorkerFunc                    // 设置栈大小

{ LOCK #pecmd                                      // 原子作用域
    LOCK --exist #MyLock,&&ret                      // 0=无 1=有 -1=失败
}
LOCK #MyLock,&&ret2                                 // 创建/获取命名锁
```

完整 EXIT 变体、LAMBDA 语法和 `FIND --class:` 参见 [commands-full.md](references/commands-full.md)。

## $5 GUI 编程

### 控件类型

| 控件 | 命令 | 控件 | 命令 |
|------|------|------|------|
| 按钮 | `ITEM` | 标签 | `LABE` |
| 编辑框 | `EDIT` | 复选框 | `CHEK` |
| 单选框 | `RADI` | 下拉列表 | `LIST` |
| 表格 | `TABL` | 进度条 | `PBAR` |
| 分组框 | `GROU` | 图片 | `IMAG` |
| 多行文本 | `MEMO` | 子窗口 | `SWIN` |
| 定时器 | `TIME` | 托盘/气泡 | `TIPS` / `TIPS*` |
| 选项卡 | `TABS` | 滑块 | `SLID` |
| 微调器 | `SPIN` | 树形视图 | `TREE` |
| 滚动条 | `SBAR` | 热键控件 | `HOTK` / `HKRY` |
| 日期时间 | `DTIM` | IP 地址 | `IPAD` |
| 菜单项 | `MENU` | 屏幕捕捉 | `SCRN` |
| 浏览窗口 | `BROW` | | |

`HKEY` 是**命令**（`HKEY$` 程序级 / `HKEY*` 窗口级），不是控件；窗口内的热键控件是 `HOTK`/`HKRY`。

### 消息映射

```wcs
ENVI @控件.MSG=_%&WM_LBUTTONDOWN%: 命令        // _ = 后部：系统响应之后执行
ENVI @窗口.MSG=0x0010: CALL OnClose             // 无前缀 = 前部：系统响应之前执行
ENVI @控件.MSG=_%&msg%::&&wp,&&lp, CALL Handler // 捕获 wParam/lParam
ENVI @控件.POSTMSG=#1                            // 投递自定义消息 #1
ENVI @控件.SENDMSG=消息号;wParam;lParam          // 同步发送
ENVI @控件.MSG=$0x0201: 命令                     // $ = 屏蔽/替代：不执行系统响应，可返回结果码
ENVI @控件.MSG=*msg: 命令                        // * = 捕鼠器 B（鼠标捕获模式）
ENVI @控件.MSG=+msg: 命令                        // + = 超级捕获
```

MSG 前缀说明：无前缀=**前部命令**（系统响应前执行，消息仍下发）；`_`=**后部命令**（系统响应后执行）；`$`=屏蔽/替代（不执行系统响应，可返回结果码）；`*`=捕鼠器 B；`+`=超级捕获。`_` 不是“控件通知必备”，只是时机选择。消息号 `*del` 删除映射；`#1`~`#N` 为 PECMD 自定义消息。

### 控件操作

```wcs
ENVI @控件名=新文本                              // 设置文本
ENVI @控件名.Enable=0                            // 禁用（1=启用）
ENVI @控件名.Visible=0                           // 隐藏（1=显示）
ENVI @控件名.POS=左:上:宽:高                     // 移动/调整大小
ENVI @控件名.POS=?&L:&T:&W:&H                    // 查询位置（: 分隔，? 后不加 ;）
ENVI @控件名.Val=?行.列;&var                     // 获取 TABL 单元格
ENVI @控件名.Val=?*;&count                       // 获取 TABL 行数
ENVI @控件名.*del=                               // 销毁控件
```

TABL 签名：`[名称],<形状>[,格式数据][,数据][,状态]`——第 4 参是**数据**，第 5 参才是状态（flags）。

读取控件值（官方示例与社区通用写法）：`%EDIT%`、`%MEMO%`、`%LIST%` 取文本/选中项；`%CHEK.Check%` 取勾选状态；`%LIST.isel%` 取选择序号。不要写 `.Check=?;` 或 EDIT 的 `QUERY/SET/SEL`，这些属性不存在。

完整控件语法、全部 25 种控件类型、ENVI @ 属性参考、窗口生命周期和消息映射——参见 [pecmd-gui.md](references/pecmd-gui.md)。

可运行示例：`examples/gui/`（TABL、TREE、TABS、SWIN、拖动、托盘、定时器、DPI、BROW、软键盘）。

GUI 写法示例（动态控件、选项卡页、自定义标题栏、GDI 绘图、拖放等）——参见 [how-tos/gui.md](references/how-tos/gui.md)。

## $6 DLL 调用

> **语法一致，数据布局受位数约束：** DLL 调用语法在 32/64 位 PECMD 上相同；但指针宽度会改变结构体布局（如 28/32、6/8），且 PECMD32 不能加载 x64 DLL。以下内容以 1.88.05.94 为准。

### 调用约定

DLL 函数**默认按 PASCAL/stdcall** 调用约定。Windows API（WINAPI 标记）不需要 `--c`。使用 `--c` 切换到 CDECL。最多 20 个参数（C 调用 100 个）。

### 正确语法（逗号分隔 + 类型前缀 + --qd）

```wcs
// ✅ 正确格式：逗号分隔，整数 #，字符串 $，建议加 --qd
CALL $ --qd --ret:&&r user32.dll,GetSystemMetrics,#0             // 整数参数
CALL $ --qd --ret:&&r user32.dll,FindWindowW,$Progman,#0         // 字符串+整数
CALL $ --qd --ret:&&r kernel32.dll,lstrlenW,$Hello World          // 字符串参数
CALL $ --ret:&&hDll ,-LoadLibrary,^user32.dll                     // 加载 DLL（^ = 自动释放）
CALL $ --ret:&&r *%&hDll%,GetSystemMetrics,#0                     // 通过句柄调用
CALL $ ,-FreeLibrary,*%&hDll%                                      // 释放 DLL
CALL $ --bool --ret:&&ret DLL,函数,...                             // --bool：函数返回 BOOL
CALL $ --cd --ret:&&ret DLL,函数,...                               // --cd：执行前切换到目标目录

// Win32 回调函数绑定（用于 EnumResourceNames 等 API）
ENVI^ WndProc1C,&WndProc1Addr               // C 调用约定回调（C 后缀决定约定）
ENVI^ WndProc1,&WndProc1Addr                // PASCAL/stdcall 回调
// PECMD 自动查找 _SUB OnWndProc1 并包装为 Win32 回调
```

### 关键规则

1. 参数**必须**用逗号分隔；`Func.#Param` 不作为参数分隔（COM 的 `.vFun:` / `*&pObj.方法` 是另一套调用语法）。
2. 默认参数是 UNICODE 字符串，`@` 为窄字符串，`#` 为整数；`--qd` 后才启用完整前缀表。
3. `--qd` 的作用是**启用前缀解析**，不是“补 null”：无 `--qd` 时 `$A` 里的 `$` 是字面字符，lstrlenW 得 2；有 `--qd` 时 `$` 被剥离，得 1。
4. 字符串/缓冲区输出建议用 `--qd` + `*&buf`；缓冲区容量单位由 API 决定（WCHAR 数或字节数）。

| 写法 | 无 `--qd` | 有 `--qd` | 说明 |
|------|-----------|-----------|------|
| `$A` | lstrlenW → 2 | lstrlenW → 1 | 无 `--qd` 时 `$` 是字面字符 |
| `$Test` | lstrlenW → 5 | lstrlenW → 4 | 传递的是 `"$Test"` |
| `$Progman` | FindWindowW → 0 | FindWindowW → 66062 | 无 `--qd` 找的是字面 `"$Progman"` |

`--qd` 与 `**qd` 等价，`--ret:` 与 `**ret:` 等价；另有全参模式 `--qd#` / `--qd*` / `--qd$` / `--qd@` / `--qd=` / `--qd~` 和 `--qd:前导表`（help.txt:600-602）。

### ❌ 常见错误

```wcs
// ❌ 点号不是参数分隔
CALL $--qd --ret:&&r user32.dll,GetSystemMetrics.#0              // 返回空

// ❌ 已启用 --qd 时整数缺少 # 前缀会被当字符串
CALL $ --qd --ret:&&r user32.dll,GetSystemMetrics,0              // 结果不可靠

// ⚠ 需要函数地址时优先用 *函数名；GetProcAddress 不是首选
CALL $ --ret:&&p ,-GetProcAddress,*%&hDll%,GetSystemMetrics

// ✅ 缓冲区输出（宽字符 API 用 SET$ 分配 WCHAR 数）
SET$ &buf=*256 0
CALL $--qd --ret:&&r kernel32.dll,GetWindowsDirectoryW,*&buf,#256
```

### 可靠工作的场景

| 场景 | 语法 | 状态 |
|------|------|------|
| 无参整数返回 | `CALL $ --ret:&&r kernel32.dll,GetTickCount` | ✅ |
| 整数参数 | `CALL $ --qd --ret:&&r user32.dll,GetSystemMetrics,#0` | ✅ |
| 字符串输入 | `CALL $ --qd --ret:&&r user32.dll,FindWindowW,$Progman,#0` | ✅ |
| 变量作参数 | `CALL $ --qd --ret:&&r kernel32.dll,lstrlenW,$%&str%` | ✅ |
| LoadLibrary | `CALL $ --ret:&&h ,-LoadLibrary,^user32.dll` | ✅ |
| 通过句柄调用 | `CALL $ --ret:&&r *%&h%,GetSystemMetrics,#0` | ✅ |
| 缓冲区输出 | 加 `--qd` 后可回传到 PE 变量 | ⚠ |
| GetProcAddress | 非首选；优先 `*函数名` 或直接写函数名 | ⚠ |
| 点语法 | Func.#Param 不解析 | ❌ |

### 32-bit vs 64-bit 区别

| 项目 | PECMDx86 (32-bit) | PECMD (64-bit) |
|------|-------------------|----------------|
| 文件标识 | PE32, i386 | PE32+, x86-64 |
| `bX64` 值 | `0`（32 位系统）或 `1`（64 位系统） | `3` |
| 指针大小 | 4 字节（< 4GB） | 8 字节（> 4GB） |
| DLL 调用语法 | 与 64-bit 相同 | 与 32-bit 相同 |
| 结构体布局 | 按 4 字节指针（28/6 等） | 按 8 字节指针（32/8 等） |
| 可加载 DLL | 仅 x86 | 仅 x64 |
| LoadLibrary 句柄 | 示例值 `0x761A0000` | 示例值 `0x7FFC34B00000` |

`bX64` 值含义：`0`=WIN32（32 位系统原生），`1`=WIN64（64 位系统运行 32 位 PECMD），`3`=PECMD64（64 位 PECMD）。

### 参数类型前缀

| 前缀 | 类型 | 描述 | 示例 |
|------|------|-------------|------|
| `#` | integer | 按整数传递 | `#0`、`#256`、`#%&hwnd%` |
| `<` | INT64 | 64 位整数 | `<0x100000000` |
| `$` | string | `--qd` 下按 Unicode 字符串传递（剥离 `$` 前缀） | `$CabinetWClass` |
| `@` | ANSI | 按 ANSI 字符串传递 | `@text` |
| `*` | buffer | 传递 PE 变量地址（`*&buf` 形式可回传输出） | `*&buf` |
| `=` | raw | 按原始数据传递 | |
| `>` | VARIANT | 按 VARIANT 传递 | |
| `~` | UTF-8 string | `--qd` 下按 UTF-8 字符串传递（解引用用 `SET~`/`ENVI~`） | `~文本` |

### 缓冲区操作（PE 变量内部）

```wcs
SET$# &buf=*256 0                     // 分配 256 字节原始缓冲区
SET$ &strBuf=*256 0                   // 分配 256 个宽字符
SET-long &buf=value:offset            // 写入 32 位整数到缓冲区偏移
SET?int &buf=&&var:offset             // 从缓冲区偏移读取 32 位整数
```

### DLL 输出数据的替代方案

DLL 缓冲区输出可使用 `*&buf` 形式（PE 变量地址传递，输出回传）。获取系统信息也可用内置命令：
- `FIND --wid*@ &var` — 枚举窗口（返回 HWND、类名、标题）
- `FIND --pid*@ &var` — 枚举进程
- `REGI` — 注册表读取系统信息
- `EXEC* &out=!cmd.exe /c ...` — 捕获外部命令输出
- `IFEX MEMU=?,&var` — 查询可用内存
- `IFEX C:\=?,&var` — 查询磁盘空间

### 平台检测

```wcs
IFEX #%&::bX64%=3, SET &PtrSz=8! SET &PtrSz=4  // 3=PECMD64, 1=WIN64(32位PECMD在64位系统), 0=WIN32
```

完整示例：`examples/system/`（WMI、SMART、服务、进程）与 `examples/net/`（PING、SOCK、WiFi）。

## $7 常用范式

### 磁盘与分区

```wcs
FDRV &盘符列表=*:                                        // 枚举所有盘符
FDRV *vol &卷标,&文件系统=C:                             // 获取卷标和文件系统
PART list disk,&&全部磁盘                                 // 枚举所有物理磁盘
PART list disk %&dsk%,&&磁盘信息                          // 字段 2=大小 7=媒体 8=签名 9=总线 10=分区类型
PART list part %&dsk%,&&分区列表                          // 列出分区号
PART -hextp -phy# list part %&dsk%#%&pt%,&&分区信息       // 详细分区信息
SHOW * %&dsk%#%&pt%,%&盘符%                               // 分配盘符
SHOW *- %&dsk%#%&pt%,                                     // 移除盘符
DFMT %&盘符%,NTFS,卷标,1                                  // 第4参非0=快格；省略=快格，0=全格
DISK ,,,2,U:                                              // 整理盘符：1/4=按序号重排，2/22=先主分区，3=只整 U 盘
MOUN %&wim%,%&目标目录%,1                                  // 挂载映像 1（只读）
HIVE PE-SYS,%&离线配置单元文件%                            // 离线注册表：HIVE 子项,文件
```

### 注册表与文件 I/O

```wcs
REGI $HKLM\SOFTWARE\App\Key,&var                  // 读 REG_SZ（活注册表）
REGI #HKLM\SOFTWARE\App\Count,&var                // 读 REG_DWORD
REGI .HKLM\SOFTWARE\App\Value,&var,&type          // . = 任意类型，并返回类型
REGI $HKLM\SOFTWARE\App\Key=值                     // 写 REG_SZ
HIVE PE-SYS,%&离线配置单元文件%                    // 挂载离线 hive 到 HKLM\PE-SYS
REGI $HKLM\PE-SYS\Microsoft\Windows NT\CurrentVersion\ProductName,&name
HIVE PE-SYS                                       // 卸载（子项名）
READ %路径%,**,&内容                               // 读取整个文件
WRIT %路径%,+0,新行                                // 追加一行
GETF# %路径%,0#*,&原始数据                         // 按原始字节读取文件
```

> `REGI .` 的 `.` 表示“任意类型”，读的仍是当前活注册表；离线注册表必须先 `HIVE 子项,文件` 挂载，再按 `HKLM\子项\…` 普通路径访问。

### 执行与捕获

```wcs
EXEC* &输出=!cmd.exe /c dir /b                            // 捕获全部输出
EXEC =!"%MyNAME%" TEAM WAIT 1000|LOAD other.ini           // 运行子 PECMD
EXEC* &out=!cmd.exe /c ipconfig                           // 捕获外部命令输出
EXEC* --exe:#101 &out=!cmd /c dir                         // 从资源 #101 运行（后接命令行）
EXEC* --exe:*#101 &out=!cmd /c dir                        // 先释放到临时文件再运行
```

### 单实例互斥体

```wcs
LOCK --try #MyAppLock,&&locked          // 0=成功锁住，非0=已存在
IFEX $%&locked%<>0,
{
    REGI $HKCU\Software\MyApp\WID,&&wid
    IFEX $%&wid%>0, TEAM ENVI @@Visible=%&wid%:2| ENVI @@POS=%&wid%::::::::1
    EXIT FILE
}
// 锁在文件作用域结束时自动释放
```

### 字符串操作

```wcs
MSTR &&a,&&b=<1><3->%&data%                              // 字段1、字段3到末尾（- = 到末尾）
MSTR &&last=<-1>%&data%                                   // 最后字段（负索引）
MSTR &&q=<~5>%&data%                                      // 字段5并剥离外层引号（~前缀）
MSTR -delims:. &&a,&&b,&&c,&&d=<1><2><3><4>%&ip%         // 按自定义分隔符拆分
MSTR* &&a,&&b=<1><2>%&data%                               // *前缀 = TAB 分隔
MSTR$ &&a,&&b=<1><2>%&data%                               // $前缀 = 空格分隔（连续空格视为单个）
SED &&r=0,模式,替换,%&source%                             // 替换所有匹配（正则模式）
SED &&r=1,模式,替换,%&source%                             // 替换第一个匹配
SED &&r=-1,模式,替换,%&source%                            // 替换最后一个匹配（负数=从末尾）
SED -t &&r=0,ABCD,abcd,%&source%                          // -t = 字符集翻译（A→a, B→b, 逐字符映射）
SED -ni &&r=0,模式,替换,%&source%                         // -ni = 不区分大小写
SED &&ext=-1,.*\.,,  ,%&filename%                          // 获取扩展名（.*\. 匹配到最后一个句号）
LPOS &&pos=needle,,%&haystack%                            // 查找首次出现（不区分大小写）
```

> **MSTR 注意事项：** 默认分隔符为空格。`-delims:09` 指定制表符（十六进制 09）。字段索引从 1 开始。`<N>` = 单个字段，`<N->` = 字段 N 到末尾，`<N*>` = 从第 N 段到末尾（多变量时依次分配），`<~N>` = 剥离引号，`<-N>` = 从末尾反向索引。`MSTR*` = TAB 分隔，`MSTR$` = 空格分隔（连续空格视为单个）。如果 MSTR 返回空，先用 `WRIT` 打印源变量确认格式，或改用 `FORX *` 按空格逐字段拆分作为替代。
>
> **SED 注意事项：** SED 默认使用正则模式。`.` 匹配任意字符，非字面量句号。匹配字面量句号用 `\.`。使用标志字符 `*` 可切换为字面量模式（不解释正则）。count=0 替换全部匹配，count=N 替换前 N 个，count=-N 替换后 N 个。`0:0` 与 `0` 等价。`-t` 标志启用字符集翻译，`-ni` 标志不区分大小写。模式中的空格作为参数分隔符处理时可能引起问题——用变量间接传递含空格的模式。
>
> **LPOS 注意事项：** 参数顺序为 `LPOS &&pos=needle,,haystack`（查找目标在前，源字符串在后）。返回首次出现的位置索引。加 `,1,` 可区分大小写。`RPOS` 从末尾查找。

含错误处理和边界情况处理的完整展开版本，参见 [how-tos/storage.md](references/how-tos/storage.md)（磁盘/注册表/文件）、[how-tos/system.md](references/how-tos/system.md)（进程/线程/定时器）、[how-tos/net.md](references/how-tos/net.md)（网络/COM）。

完整可运行示例：`examples/storage/`（分区管理、磁盘枚举、脱机注册表）与 `examples/apps/`（DISM、系统安装、启动盘制作、CGI）。

### CALC 计算与数学函数

```wcs
CALC &结果=%&a% + %&b%                               // 基本算术：+ - * / % ^
CALC #&结果=%&a% & %&b%                               // # = 整数模式；位运算：& | @
CALC -base=16 #&hex=shl(0x07,16)|0x20                 // 十六进制输出 + 位移
CALC &sz=%&bytes%/1G#3                                // 字节转 GB，3 位小数
CALC -err=0 &r=%&a% / %&b%                            // 出错时返回默认值 0
```

**数学函数（34个）：**

| 类别 | 函数 |
|------|------|
| 三角 | `sin cos tan ctg arcsin arccos arctan arcctg deg rad` |
| 代数 | `abs sqrt ln lg log exp pow pow10 hypot`（`log(a,b)` 为双参；求 log10 用 `lg()`） |
| 取整 | `floor ceil round int frac` |
| 位运算 | `shl shr xor not lnot` |
| 其他 | `div mod rand max min` |

常量：`e`、`pi`。尺寸后缀：`K`=1024、`M`=1024²、`G`=1024³、`T`=1024⁴、`S`=512。
多表达式用 `;` 分隔；子表达式赋值写作 `&名=expr;`（不是 `$名`）。

## $8 陷阱与注意事项

1. **CALC 空格**：`=` 后无需空格（`CALC &J=%&I%+1` 可用）；字面减号后必须留空格（`3 - 2`）。
2. **注释标记**：`//`、`;`、`` ` ``（反引号）均为有效注释符。整行注释可直接以 `//` 开头；行尾注释前需一个空字符（如 `SET &a=1 // 注释`）。
3. **SET = ENVI &**：`SET var=val` 等价于 `ENVI &var=val`（逐级查找，不保证本级新建）；`SET &var=val` 才等价于 `ENVI &&var=val`（本级新建）。ForceLocal=1 只改变 ENVI 的默认解释，不改变 SET 的本义。
4. **FIND 与 IFEX 前缀交换**：FIND 中 `$` = 字符串比较、`|` = 浮点比较；IFEX 中 `$` = 浮点比较、`|` = 字符串比较。`#` 在两者中均为整数比较。IFEX 中 `|` 在 `[]` 复合条件内为 OR 逻辑运算符。
5. **盘符冒号**：盘符参数通常带 `:`（`FDRV`、`FIND C:\=?`）；`FDRV =*`、`FORM` 接目录/设备路径时不需要。
6. **带空格的路径**：`LOAD "C:\Program Files\a.ini"` 需要引号。
7. **文件编码**：声明必须与文件实际字节一致。PE 生态默认 936（GBK）；文件保存为 UTF-8 时用 `#code=65001`；有 BOM 时以 BOM 为准。`#code=936T950`/`950T936` 是双编码变体，迁移时按目标环境重声明。
8. **`{` 位置**：文件级和函数级 `{` 必须是该行的第一个非空白字符（可缩进）。在 TEAM/LOOP/IFEX 内部，`{` 启动命令组。
9. **行续接**：行首第一个非空格字符为 `\` 时，将该行合并到上一行。
10. **`_SUB`、`WRIT`、`LOOP` 不能内联**：不能在 FIND/IFEX/TEAM 命令内部定义 `_SUB`。`WRIT` 和 `LOOP` 也必须位于单独一行，不能嵌套在 FIND/IFEX/TEAM 内。
11. **空字符串检测**：字符串用 `FIND $%var%=,`；`*` 模式按 PE 变量名比较，`FIND *=var,` 为空、`FIND *<>var,` 为非空（也可写 `FIND *&var=` / `FIND *<>&var`）。
12. **字面 %**：字符串中表示字面 `%` 用 `%%`。
13. **线程安全**：线程创建时，**共享点之后**的 PE 变量复制到子线程。持久栈上下文（窗口、`*` 函数）中的变量是**共享**的（非复制）；非持久上下文（普通函数、`{}` 块）中的变量自动复制一份。真正跨线程通信用 `&::` 变量。
14. **中文变量名**：社区常见习惯（约三分之一真实脚本使用），不是强制；与现有脚本互操作时保持同名即可。
15. **OnShutdown.wcs**：PECMD 在关机/重启/注销前自动运行 `%SystemRoot%\System32\OnShutdown.wcs`，格式为 `OnShutdown.wcs <操作码> [脚本参数表]`。操作码：`shutdown`=关机、`reboot`=重启、`logout`=注销、`suspend`=挂起、`hiber`=休眠、`poweroff`=关电、`lock`=锁定计算机、`unknown`=未知。关机菜单支持的子集：`shutdown`、`reboot`、`logout`、`poweroff`、`unknown`。
16. **`^` 预解释**：`^COMMAND` 表示把本命令预先解释一遍（`^^` 两遍），用于 TEAM/事件字符串中拼接动态变量名；不是“推迟到执行时”。
17. **MSG 前缀是时机语义**：无前缀=前部（系统响应前），`_`=后部（系统响应后），`$`=屏蔽/替代。`_` 不是“控件通知必备”。
18. **THREAD\* 与 THREAD**：`*`/`-link` 只建立父子关系；窗口和 `*函数`（持久栈）共享变量，普通函数和 `{}` 块仍复制。
19. **FIND 展开规则**：FIND 中的裸标识符被视为字面字符串。始终使用 `FIND $%&var%=值` 引用 PE 变量。
20. **`@@Visible` 与 `@Visible`**：跨进程用 `ENVI @@Visible=窗口ID:值`。进程内用 `ENVI @控件.Visible=0|1`。
21. **FORX 变量引用**：声明 `&&item`；块内引用用 `%&item%`。同一作用域也可用 `%&&item%`（官方示例），跨 `{}` 会失效，统一写 `%&item%` 最稳。次数与块之间必须有逗号：`...,0,` 换行 `{`。
22. **FIND --wid\*@ 输出格式**：`序号 窗口ID 控件ID 父窗口ID 线程ID 进程ID 类型 标题`，字段用 **TAB** 分隔。配合 `FORX *NL` 按行遍历、`MSTR*` 按 TAB 分字段提取（field 2=窗口ID, field 7=类型, field 8=标题）。
23. **DLL 调用不可用时**：优先用 `FIND --wid*@`（窗口枚举）、`FIND --pid*@`（进程枚举）、`REGI`（注册表）、`EXEC*`（外部命令）替代。
24. **`Visible` 与 `Visable`**：两者均可工作（PECMD 接受两种拼写）。文档统一用 `Visible`，但 SDK 示例普遍用 `Visable`。
25. **FORX *NL: 自定义分隔符**：`FORX *NL:| &data,&&item,` 用 `|` 作为行分隔符（默认为换行）。
26. **ENVI^ ALIAS 包装 DLL**：`ENVI^ ALIAS GetTick=CALL $ --ret:&&r kernel32.dll,GetTickCount` 使 `GetTick` 可作为伪命令直接调用。
27. **FILE 操作符**：`=>` 复制、`->` 移动、`>>` 改名；写反会搬走/覆盖源文件。
28. **REGI `.` 不是离线**：`.`=任意类型；离线注册表先 `HIVE 子项,文件`，再按 `HKLM\子项\…` 访问。
29. **TABL 参数位**：`[名称],<形状>[,格式数据][,数据][,状态]`——第 4 参是数据，第 5 参是状态。
30. **POS 查询**：`ENVI @控件.POS=?&L:&T:&W:&H`（`:` 分隔，`?` 后不加 `;`）。
31. **`CALL @--`**：卸载 Win 环境，不是关闭窗口；关窗用 `KILL`。
32. **单实例**：用 `LOCK --try #名,&v` 在文件作用域持锁；不要把 `&v` 建在 `{}` 内再出块判断。

## $9 参考文件

当需要超越上述快速参考的详细信息时，查阅以下权威文件。所有文件与示例均随技能分发，不依赖外部素材目录。

| 文件 | 何时查阅 |
|------|----------|
| `examples/README.md` | 43 个完整示例索引：启动、GUI、磁盘、系统、网络、应用 |
| `bin/README.md` | 内置 PECMD 1.88.05.94 解释器（x86/x64、GUI/CLI）与校验 |
| `references/commands-full.md` | 命令语法、全部标志、参数细节 |
| `references/pecmd-gui.md` | GUI 控件、消息、窗口生命周期、ENVI @ 属性 |
| `references/pe-startup.md` | WinPE 启动脚本、PECMD.INI 结构、启动阶段 |
| `references/how-tos/storage.md` | 磁盘、分区、文件、注册表、设备 写法示例 |
| `references/how-tos/system.md` | 进程、线程、定时器、系统信息、加密、工具 |
| `references/how-tos/gui.md` | GUI 模式：动态控件、选项卡、GDI、拖放等 |
| `references/how-tos/net.md` | 网络、SOCK、COM/WMI 写法示例 |
| `references/troubleshooting.md` | 常见错误排查、DLL 调用失败、变量引用问题 |

## $10 输出规范

编写 PECMD 脚本和工具时遵循以下规范：

1. 编码声明与文件实际字节一致：PE 生态默认 `#code=936`；UTF-8 文件用 `#code=65001`；有 BOM 以 BOM 为准。
2. 顶部推荐 `ENVI^ EnviMode=1` 与 `ENVI^ ForceLocal=1`；ForceLocal 下 `ENVI` 生成 PE 变量，传子进程需 `ENVI ^var`、`ENVI-env` 或 `EXPORTLOCAL=1`。
3. 默认使用 PE 变量；需要传给 `EXEC` 子进程时才用环境变量。
4. `TEAM` 只用于短序列；避免把 `_SUB`/`WRIT`/`LOOP` 塞进 TEAM/FIND/IFEX（help 建议尽量不用单行嵌套）。
5. 复杂操作拆成命名清晰的 `_SUB`。
6. GUI 保存布局用 `POS=?&L:&T:&W:&H`，在 WM_SIZE（0x0005）中恢复。
7. 调用外部程序优先 `EXEC =!"%MyNAME%" ...` 或 `EXEC* &out=!cmd ...`。
8. 跨线程通信用 `&::`；线程入口先用 `ENVI &p=%1` 保存参数。
9. 单实例用 `LOCK --try #名,&v`，并在同一作用域判断。
10. 控件消息前缀是时机语义：无前缀前部、`_` 后部、`$` 屏蔽；不要迷信 `_`。
11. `SED` 做正则替换、`MSTR` 取字段；`<N*>` 是 N 到末尾，不是单字段。
12. `FILE` 复制用 `=>`、移动用 `->`；`REGI .` 不是离线，离线用 `HIVE`。
13. TABL 第 4 参是数据、第 5 参是状态；读控件值用 `%控件%` / `%控件.Check%`。
14. 生成脚本后对照 `examples/` 与 `help.txt` 的同命令语法；不确定的 flag 不要写。


---

GitHub: https://github.com/VirtualHotBar/PECMD-Pro-Max
ClawHub: https://clawhub.ai/virtualhotbar/pecmd-pro-max
