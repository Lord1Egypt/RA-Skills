# Changelog

## 1.8.1 — 2026-11-24

- 修复发布包字节稳定性：新增 `.gitattributes`，将 `examples/**` 与 `bin/**` 标记为 `-text`，避免跨平台 checkout 转换 CRLF 导致 SHA256 清单失配。
- 审计报告改为稳定文件名 `AUDIT.md`，版本写入正文，不再随每次发版重命名。
- `v1.8.0` 标签因上述换行符问题在 CI 校验失败，未发布到 ClawHub；本版为可发布版本。

## 1.8.0 — 2026-11-24

这是 ClawHub 已发布 1.7.1 之后的下一个版本。历史 `v1.6.0`–`v1.7.1` 标签的 `SKILL.md` frontmatter 一直停在 1.5.5；本版起由 CI 强制校验 tag 与 frontmatter 一致。

对照 `PE-Dev` 语料（259 个脚本）与 PECMD 1.88.05.94 `help.txt` 的全量审查结果，修正文档中不可执行的语法与自相矛盾的说明，并内置解释器、示例和校验工具。

### 变量与流程控制

- 明确 `%var%` 的解析取决于 `EnviMode`，环境变量用 `%^var%` 显式读取；修正 `ForceLocal` 下 `ENVI`/`SET` 的作用域说明。
- 修正 `SET = ENVI &`（不是 `ENVI &&`）、`SET-def`、`ENVI-ret`、`SET~` 的用法与示例。
- 修正 `FIND`/`IFEX` 的 `$` 字符串与浮点比较、`|` 数值比较、`*c` 命令级后缀、`[]` 复合条件、`,!!` 无 ELSE 语义。
- 修正 `FORX` 的 `*`/`*NL`/`*L`/`/S`/`@` 选项、逗号位置与 `%&&item%` 错误引用。
- 修正 `THREAD` 标志、`LOCK --try/--exist`、`LOOP` 前缀与 `EXIT` 变体。

### GUI 与消息

- 窗口类型改为 `[-][#][$数值][:透明色]`，删除不存在的 `-minb`，补充 `-bottom`/`-mv`/`-altmv`。
- `POS` 查询改为 `=?&L:&T:&W:&H`（冒号分隔）。
- `TABL` 签名改为 `[名称],<形状>[,格式数据][,数据][,状态]`，明确第 4 参是数据、第 5 参是状态。
- `MSG` 前缀语义改为：无前缀=前部、`_`=后部、`$`=阻塞；删除错误的反向说明。
- 控件读取改为 `%Ctrl%`、`%Ctrl.Check%`、`%Ctrl.isel%`；删除不存在的 `.Check=?;`、EDIT `QUERY/SET/SEL` 与 `PBAR.Value`。
- 弹出菜单统一为 `CALL @--popmenu[:x.y[:对齐]] 菜单名`；明确 `CALL @--` 卸载 Win 环境、关窗用 `KILL`。

### 存储、执行与系统

- `FILE` 操作符改正：`=>` 复制、`->` 移动、`>>` 改名。
- `REGI .` 明确为“任意类型”，离线注册表改用 `HIVE 子项,文件`。
- 补充 `PUTF#`、`DFMT`、`DISK` 函数号、`MOUN` 读写第 4 参、`PART` 字段索引。
- `EXEC` 补充 `--exe:*#资源号`、`-cmd` 与输出捕获写法。
- `MSTR <N*>` 明确为“N 到末尾”，单字段用 `<N>`。

### DLL 与 COM

- `--qd` 改为正确语义：启用前缀表；无 `--qd` 时 `$A` 是字面字符串，不是“多传 null”。
- 修正 32/64 位结构体大小（`SP_DEVICE_INTERFACE_DATA` 28/32、详情头 6/8）与回调绑定 `ENVI^ WndProc1C,&addr`。
- 删除不存在的 `CODE *HEX` 目标格式，GUID/CLSID/IID 统一用 `SET#$$` 构造。
- COM 调用统一 `CALL $--qd --16 ...` 与 `.vFun:` 虚表语法。

### WinPE 启动

- 重写启动链：仅保留 `Setup\CmdLine` 与 `winpeshl.ini` 两条真实入口，删除虚构的 `MiniNT\WinPEShell`/`SetupComplete.cmd` 路径。
- WinXShell 配置改为 `.jcfg` + `.lua`，安装位置改为 `%ProgramFiles%\WinXShell`。
- 明确 `MAIN` 自驻留、不需要 `WAIT -1`；`PCIP` 不加载网络栈；FBWF 下注册表可写但重启丢失。
- 编码策略：声明必须匹配文件字节，PE 生态默认 `#code=936`，UTF-8 用 `#code=65001`。

### 资产与工具

- 新增 `bin/`：PECMD 1.88.05.94 x86/x64、GUI/CLI 四个可执行文件及 SHA256 清单。
- 新增 `examples/`：43 个按域组织的完整示例、索引、风险标注与哈希清单。
- 新增 `tools/verify_skill.py` 与 `.github/workflows/verify-skill.yml`：检查必需文件、围栏平衡、相对链接、版本徽章、清单哈希和已知反模式。

### 审计闭环（1.8.0 补充）

- 新增 `AUDIT.md`：5 份领域报告 128 项 + 8 项跨文档一致性问题，共 136 项逐项记录修复位置；26 个 P0 全部给出精确行号。
- 补齐 `EXIT FILE` 仅退出当前 LOAD 层、inline `LOOP` 多行示例、`TIME` 回调主线程串行说明、`LOCK --exist -1=失败`、`CoCreateInstance --ret`、`ENVI @@POS` 第 9 字段、`@`/`-` 分区项过滤、`STRL` 的 `*`/`-8`/`-bin` 变体。
- 校验器新增审计表检查：必须覆盖 136 个唯一 ID，其中 P0 恰为 26 项。
- 发布 workflow 新增 `verify` job：发布前运行校验器，并强制 tag 版本与 `SKILL.md` frontmatter 一致。

### 已知限制

- 内置二进制仅校验哈希与来源，未在 CI 中执行。
- 示例保留原始编码，未全部在 32/64 位 PE 环境做运行时回归；高风险示例已在 `examples/README.md` 标注。
- 本次以静态审查和语料交叉验证为主，`help.txt` 与社区脚本冲突处优先采用可执行证据。
