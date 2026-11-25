# PECMD Pro Max 审计修复对照表

本表逐项核销 `E:\Material\PE-Dev` 审查报告中的 136 项问题：5 个领域报告 128 项，加合并报告的 8 项跨文档一致性问题。

- 基线：PECMD2012 1.88.05.94 `help.txt`、639 份去重 `.wcs`/`.ini` 语料、43 个内置示例。
- 修复版本：`1.8.1`；基线提交：`a4b3b74`；本表随后续发布提交入库。
- 复验命令：`python -I tools/verify_skill.py`；覆盖围栏、链接、行数、示例数量、清单哈希与已知反模式。
- 说明：P2/P3 的“修复位置”按当前章节记录；P0 给出精确行号。原报告 P1/P2/P3 个别条目为同一段落的重复表述，按 ID 保留，不合并计数。

## 1. P0（26 项）

| ID | 原位置 | 修复位置 | 核销结果 |
|---|---|---|---|
| V-01 | SKILL.md:44-48 | SKILL.md:44-77 | 变量表改为模式相关；补 `ENVI-env`、`%^var%`、`EXPORTLOCAL`，并说明 ForceLocal 生成 PE 变量、EXEC 默认不继承。 |
| G-01 | SKILL.md:282 / pecmd-gui.md:1246 | SKILL.md:312 / pecmd-gui.md:1241-1247 | MSG 前缀表改为：无前缀=前部、`_`=后部、`$`=屏蔽/替代；删除“处理后丢弃”断言。 |
| G-02 | pecmd-gui.md:570,622-625 | pecmd-gui.md:565 / SKILL.md:327 | TABL 签名改为 `[名称],<形状>[,格式数据][,数据][,状态]`；第 4 参数据、第 5 参状态。 |
| G-03 | SKILL.md:292 / pecmd-gui.md:130-131 | pecmd-gui.md:132 / SKILL.md:321 | POS 查询改为 `=?&L:&T:&W:&H`（冒号分隔，`?` 后无 `;`）。 |
| G-04 | pecmd-gui.md:23,54-56 | pecmd-gui.md:23 / SKILL.md:157 | 窗口 style 改为 `[-][#][$数值][:透明色]`；`#`=无边框、`$`=0-255 刻度、100/$255 隐藏。 |
| D-01 | SKILL.md:468-478 | SKILL.md:513 / commands-full.md:550 | 单实例改为 `LOCK --try #名,&v` 并在同作用域判断；不再把 `&&exists` 建在 `{}` 内。 |
| D-02 | net.md:124-132 | how-tos/net.md:137-138 | 删除 `CODE *HEX`，CLSID/IID 改用 `SET#$$` 4+2+2+2×8 分组构造。 |
| D-03 | system.md:622-623 | how-tos/system.md:624 / how-tos/storage.md:90 | GUID 改用 `SET#$$` 一次构造 16 字节，不再把 HEX 文本当 GUID。 |
| D-04 | system.md:632-635 | how-tos/system.md:635 | `SP_DEVICE_INTERFACE_DATA` cbSize 改为 x86 28 / x64 32。 |
| D-05 | system.md:652-670 | how-tos/system.md:637,671 | 详情头改为 6/8；Flags 直接读 offset 20；DevicePath 用 `SET-make &&devicePath=&detailBuf@4`。 |
| D-06 | net.md:36-37 | how-tos/net.md:36-37 | 删除三段式 FIND；改用 `LPOS &&p=TTL,,%&result%` + `IFEX`。 |
| D-07 | net.md:17-18 | how-tos/net.md:17 | 删除第二次 `MSTR <2>`；最后字段已是纯 IP。 |
| D-08 | system.md:748-752 | how-tos/system.md:751 | GetComputerNameW 缓冲区改用 `SET$`（宽字符），不再用按字节的 `SET$#`。 |
| D-09 | commands-full.md:465 | commands-full.md:465-466 | 裸 `--pid` 明确为 5 个系统时间值；按名取 PID 用 `--pid*@`。 |
| S-01 | storage.md:182 / commands-full.md:1296 / pe-startup.md:211 | SKILL.md:488,497 / commands-full.md:1285 | 明确 `REGI .`=任意类型且读活注册表；离线必须先 `HIVE`。 |
| S-02 | commands-full.md:1334-1350 | commands-full.md:1319 / storage.md:527 | HIVE 改为 `HIVE 子项名,[文件]`，参数顺序纠正。 |
| S-03 | commands-full.md:616 | commands-full.md:618-620 | FILE 操作符改为 `=>` 复制、`->` 移动、`>>` 改名。 |
| S-04 | commands-full.md:1202-1212 | commands-full.md:1210-1219 | SITE 设置统一为 `SITE 路径,属性`；删除 `SITE +R,path`。 |
| S-05 | commands-full.md:897-899 | commands-full.md:904-911 | DISK 功能号改为 1/4 按序号重排、2/22 先主分区、3 只整 U 盘。 |
| S-06 | commands-full.md:1130-1131 | commands-full.md:1133-1145 | PATH 改为建/删/切换工作目录；环境变量用 ENVI。 |
| S-07 | commands-full.md:610 / storage.md:159 | commands-full.md:611 / storage.md:161 | 写 PE 变量改用命令后缀 `PUTF#`；`#` 仅表示 EXEDATA 资源号。 |
| S-08 | storage.md:15 | storage.md:15 / SKILL.md:472 / commands-full.md:676 | PART 字段改为 2=大小、7=媒体、8=签名、9=总线、10=分区类型。 |
| S-09 | storage.md:366 | storage.md:368 | IOCTL 计算改为 `shl(0x2D,16)|shl(0,14)|shl(0x500,2)` = 0x2D1400。 |
| PS-01 | pe-startup.md:17 | pe-startup.md:15-18 | 启动链改为 `Setup\CmdLine` + `winpeshl.ini` 两条真实入口，删除 `MiniNT\WinPEShell`。 |
| PS-02 | pe-startup.md:25 | pe-startup.md:39 / commands-full.md:1437 | WinXShell 改用 `SHEL`/`EXEC`；`EXEC*` 明确必须 `变量名=`。 |
| C-MSTR | SKILL.md:499 / commands-full.md:1528 | SKILL.md:541 / troubleshooting.md:88 | `<N*>` 改为“第 N 段到末尾”；单字段用 `<N>`。 |

## 2. P1（40 项）

| ID | 原位置 | 修复位置 | 状态 |
|---|---|---|---|
| V-02 | SKILL.md:46 | SKILL.md §2（变量系统） | 已修正 |
| V-03 | SKILL.md:57 | SKILL.md §2（变量系统） | 已修正 |
| V-04 | SKILL.md:59,529 | SKILL.md §2（变量系统） | 已修正 |
| V-11 | SKILL.md:90-96 | SKILL.md §2（变量系统） | 已修正 |
| V-12 | SKILL.md:40-64（缺） | SKILL.md §2（变量系统） | 已修正 |
| V-13 | SKILL.md:175 | SKILL.md §4（FIND/IFEX/LOOP/FORX） | 已修正 |
| V-15 | references/commands-full.md:459-460 | SKILL.md §4（FIND/IFEX/LOOP/FORX） | 已修正 |
| V-16 | SKILL.md:193-204 | SKILL.md §4（FIND/IFEX/LOOP/FORX） | 已修正 |
| V-17 | SKILL.md:206-210；references/commands-full.md:507-515 | SKILL.md §4（FIND/IFEX/LOOP/FORX） | 已修正 |
| V-18 | SKILL.md:216-217 | SKILL.md §4（FIND/IFEX/LOOP/FORX） | 已修正 |
| G-05 | references/pecmd-gui.md:1406 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-06 | references/pecmd-gui.md:37；references/how-tos/gui.md:187 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-07 | references/pecmd-gui.md:968,986 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-08 | references/pecmd-gui.md:332-338 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-09 | references/pecmd-gui.md:1484,1492,1498 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-10 | references/pecmd-gui.md:62-64 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-11 | references/pecmd-gui.md:1092 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-12 | references/pecmd-gui.md:153-157,2170 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-13 | references/pecmd-gui.md:1973,1977,2178 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-14 | references/pecmd-gui.md:487-489 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-15 | references/pecmd-gui.md:270,420,446,1479,2159 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| G-16 | references/pecmd-gui.md:668 | references/pecmd-gui.md §2/§4（窗口/控件） | 已修正 |
| D-10 | SKILL.md:332-339,395 | SKILL.md §6（DLL） | 已修正 |
| D-11 | 全篇（SKILL.md:313-320、net.md:3） | SKILL.md §6（DLL） | 已修正 |
| D-12 | references/how-tos/net.md:57-112 | references/commands-full.md:1454 / references/how-tos/net.md §65 | 已修正 |
| D-13 | references/how-tos/system.md:265-279 | references/how-tos/system.md:279 | 已修正 |
| S-10 | references/commands-full.md:619-620 | references/commands-full.md（对应命令小节） | 已修正 |
| S-11 | references/commands-full.md:633-634 | references/commands-full.md（对应命令小节） | 已修正 |
| S-12 | references/commands-full.md:934-941 | references/commands-full.md（对应命令小节） | 已修正 |
| S-13 | references/commands-full.md:1080-1081 | references/commands-full.md（对应命令小节） | 已修正 |
| S-14 | references/commands-full.md:1405 | references/commands-full.md（对应命令小节） | 已修正 |
| S-15 | references/how-tos/storage.md 全文（无 DFMT/DISK/MOUN/RAMD/PART -devid 示例） | references/how-tos/storage.md / commands-full.md | 已修正 |
| PS-03 | references/pe-startup.md:209（示例 73 行） | references/pe-startup.md | 已修正 |
| PS-04 | references/pe-startup.md:28 | references/pe-startup.md | 已修正 |
| PS-05 | references/pe-startup.md:60 | references/pe-startup.md | 已修正 |
| PS-06 | references/pe-startup.md:247 | references/pe-startup.md | 已修正 |
| PS-07 | references/pe-startup.md:196-205 | references/pe-startup.md | 已修正 |
| X-02 | references/troubleshooting.md:304 | troubleshooting.md §12（WRIT/LOOP 独立行） | 删除 `TEAM ... WRIT` 的 ✅ 示例；改为独立 WRIT 行。 |
| X-03 | SKILL.md:264 / pecmd-gui.md:98 | SKILL.md §5 控件表 / pecmd-gui.md §1 控件表 | 控件表改为 `HOTK`/`HKRY`；HKEY 作为命令保留，不再列为控件。 |
| X-04 | SKILL.md:573 / pe-startup.md:36,201 | SKILL.md:31 / pe-startup.md:212 | 编码规则改为“声明与字节一致；PE 生态默认 936；65001 可选并需实测”。 |

本级别小计：40 项。

## 3. P2（50 项）

| ID | 原位置 | 修复位置 | 状态 |
|---|---|---|---|
| V-05 | SKILL.md:58 | SKILL.md §2（变量系统） | 已修正 |
| V-06 | SKILL.md:46,49 | SKILL.md §2（变量系统） | 已修正 |
| V-07 | SKILL.md:49,53-54 | SKILL.md §2（变量系统） | 已修正 |
| V-08 | SKILL.md:60 | SKILL.md §2（变量系统） | 已修正 |
| V-09 | SKILL.md:61 | SKILL.md §2（变量系统） | 已修正 |
| V-10 | SKILL.md:62,542 | SKILL.md §2（变量系统） | 已修正 |
| V-14 | SKILL.md:178-179,537 | SKILL.md §4（FIND/IFEX/LOOP/FORX） | 已修正 |
| V-19 | SKILL.md:219-222,547 | SKILL.md §4/§8（变量与陷阱） | 已修正 |
| V-20 | SKILL.md:227,544 | SKILL.md §4/§8（变量与陷阱） | 已修正 |
| V-21 | SKILL.md:135 | SKILL.md §4/§8（变量与陷阱） | 已修正 |
| V-22 | SKILL.md:138；references/commands-full.md:53 | references/pecmd-gui.md:1070 / SKILL.md §5 | 已修正 |
| V-23 | SKILL.md:527 | SKILL.md §4/§8（变量与陷阱） | 已修正 |
| G-17 | references/pecmd-gui.md:696 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-18 | references/pecmd-gui.md:701 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-19 | references/pecmd-gui.md:637 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-20 | references/pecmd-gui.md:686-687 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-21 | SKILL.md:543；pecmd-gui.md:1245 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-22 | references/how-tos/gui.md:269 | references/pecmd-gui.md:1287（0x02A3） | 已修正 |
| G-23 | references/how-tos/gui.md:249 | references/commands-full.md:221 / references/pecmd-gui.md @@SENDMSG 小节 | 已修正 |
| G-24 | references/pecmd-gui.md:1085-1086 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-25 | references/pecmd-gui.md:1088-1090 | references/pecmd-gui.md:1084 | 已修正 |
| G-26 | references/pecmd-gui.md:219-222 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-27 | references/pecmd-gui.md:165 | references/pecmd-gui.md §4（TABL/控件/消息） | 已修正 |
| G-28 | references/pecmd-gui.md:3,297 | references/pecmd-gui.md:1208（4.25 BROW） | 已修正 |
| D-14 | SKILL.md:383-385 | SKILL.md §6（DLL） | 已修正 |
| D-15 | SKILL.md:350-352 | SKILL.md §6（DLL） | 已修正 |
| D-16 | SKILL.md:227 | SKILL.md §6（DLL） | 已修正 |
| D-17 | SKILL.md:399 | SKILL.md §6（DLL） | 已修正 |
| D-18 | SKILL.md:330 | SKILL.md §6（DLL） | 已修正 |
| D-19 | SKILL.md:523 | SKILL.md §6（DLL） | 已修正 |
| D-20 | SKILL.md:461-474；system.md:162-163 | references/how-tos/system.md:163,363 | 已修正 |
| D-21 | references/how-tos/net.md:62-83 | references/how-tos/net.md §65（TCP accept 循环） | 已修正 |
| D-22 | references/commands-full.md:70 | references/commands-full.md:72 | 已修正 |
| S-16 | references/how-tos/storage.md:31,33 | references/how-tos/storage.md:31-36 | 已修正 |
| S-17 | references/commands-full.md:832-833,837-849 | references/how-tos/storage.md / commands-full.md | 已修正 |
| S-18 | references/commands-full.md:745-746 | references/how-tos/storage.md / commands-full.md | 已修正 |
| S-19 | references/commands-full.md:879-880 | references/how-tos/storage.md / commands-full.md | 已修正 |
| S-20 | references/commands-full.md:561-562；references/how-tos/storage.md:133 | references/how-tos/storage.md / commands-full.md | 已修正 |
| S-21 | references/commands-full.md:1411；1445-1453 | references/how-tos/storage.md / commands-full.md | 已修正 |
| S-22 | references/how-tos/storage.md:500 | references/how-tos/storage.md / commands-full.md | 已修正 |
| S-23 | references/commands-full.md:1308 | references/how-tos/storage.md:491（`REGI ?` 为官方查询前缀） | 已修正 |
| S-24 | references/pe-startup.md:192 | references/pe-startup.md:178-179 | 已修正 |
| S-25 | SKILL.md:458 | SKILL.md:507 | 已修正 |
| PS-08 | references/pe-startup.md:67 | references/pe-startup.md | 已修正 |
| PS-09 | references/pe-startup.md:192 | references/pe-startup.md:178-179 | 已修正 |
| PS-10 | references/pe-startup.md:5 | references/pe-startup.md | 已修正 |
| PS-11 | references/pe-startup.md:84 | references/pe-startup.md:91 | 已修正 |
| PS-12 | references/pe-startup.md:231 | references/pe-startup.md:223 | 已修正 |
| X-05 | references/troubleshooting.md:237-245 | troubleshooting.md §9 | 整行注释无需前导空格；只有行尾注释需要空格。 |
| X-06 | SKILL.md:576 | SKILL.md §10 规则 4 | TEAM 改为短序列建议；明确禁止把 `_SUB`/`WRIT`/`LOOP` 塞进 TEAM/FIND/IFEX。 |

本级别小计：50 项。

## 4. P3（20 项）

| ID | 原位置 | 修复位置 | 状态 |
|---|---|---|---|
| V-24 | SKILL.md:167,534 | SKILL.md §4/§8（变量与陷阱） | 已修正 |
| V-25 | SKILL.md:45 | SKILL.md:29 | 已修正 |
| V-26 | references/commands-full.md:121 | references/commands-full.md EXIT 小节（`_SIB` 已删除） | 已修正 |
| G-29 | references/pecmd-gui.md:1383 | references/pecmd-gui.md §1/§4（窗口/调用） | 已修正 |
| G-30 | references/pecmd-gui.md:19 | references/pecmd-gui.md §1/§4（窗口/调用） | 已修正 |
| G-31 | references/pecmd-gui.md:1386 | references/pecmd-gui.md §1/§4（窗口/调用） | 已修正 |
| G-32 | references/pecmd-gui.md:34 | references/pecmd-gui.md §1/§4（窗口/调用） | 已修正 |
| G-33 | references/pecmd-gui.md:1078 | references/pecmd-gui.md §1/§4（窗口/调用） | 已修正 |
| D-23 | SKILL.md:465 | SKILL.md:270 / commands-full.md:549 | 已修正 |
| D-24 | SKILL.md:323-324 | SKILL.md:359 | 已修正 |
| D-25 | SKILL.md:517 | SKILL.md:566 | 已修正 |
| D-26 | references/how-tos/net.md:129 | references/how-tos/net.md:140-141 | 已修正 |
| S-26 | SKILL.md:531 | SKILL.md:580 | 已修正 |
| S-27 | references/commands-full.md:1310 | references/commands-full.md:1299 | 已修正 |
| S-28 | references/how-tos/storage.md:29-31 | references/how-tos/storage.md:29-31 | 已修正 |
| PS-13 | references/pe-startup.md:96 | references/pe-startup.md:103 | 已修正 |
| PS-14 | references/pe-startup.md:234 | references/pe-startup.md:224 | 已修正 |
| PS-15 | 全篇 | references/pe-startup.md:18 | 已修正 |
| X-07 | SKILL.md:210,212,216 | SKILL.md §4（LOOP/FORX 示例） | inline `LOOP {...}` 示例改为多行块。 |
| X-08 | references/troubleshooting.md:259 | troubleshooting.md §10 | 统一 PE 变量 `&I`，LOOP 改多行。 |

本级别小计：20 项。

## 5. 覆盖度建议（不计入 136 项）

- 已补：`STRL` 的 `*`/`-8`/`-bin`、`LSTR`/`RSTR` 的整串语义、`RPOS` 参数顺序；`SHUT`/`HOTK` 已在启动文档中使用。
- 已确认无需新增：`NAME`、`SITE`、`FONT` 已有独立小节；`FPOS`/`PWIN`/`SYSCMD` 在语料中调用为 0。
- `FIXNUM`/`BYTE`/`UNSIGNED`/`__VIRTUAL`/`DSPW`/`RMDIR` 经核实不是 PECMD 命令，未加入。

## 6. 验证与限制

- 静态验证：`tools/verify_skill.py` 全部通过；P0 反模式（`POS=?;`、`FILE ->` 复制、`CODE *HEX`、`-minb`、`CALL @--WinName` 等）已纳入校验器。
- 语料交叉验证：GUID 用 `SET#$$`、结构体 28/32 与 6/8、`FILE`/`SITE`/`HIVE`/`DISK` 语义均有 1.88.05.94 官方帮助或真实脚本证据。
- 未执行：内置二进制与 43 个示例未做运行时回归；破坏性示例仍需在虚拟机/可丢弃介质验证。
- 未覆盖：P2/P3 中依赖具体 build 的经验性断言，若与其它 PECMD 版本冲突，以对应版本 `help.txt` 为准。
