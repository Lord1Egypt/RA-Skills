---
name: "ida-reverse"
description: "使用 IDA Pro MCP 做任何逆向工作时必须加载：规范化分析流程——先反编译再下结论、边分析边标注落库、防幻觉重命名。"
---

# IDA 逆向分析技能（ida-reverse）

> 定位：**流程规范**，不是场景手册。无论分析对象是崩溃转储、可疑样本、闭源协议还是自家二进制，只要通过 IDA MCP 做逆向，本技能即生效。

## 触发条件
- ida-pro-mcp 可用（`http://127.0.0.1:13337/mcp`，无鉴权仅本机），且任务涉及反编译/函数分析/崩溃转储/二进制研究，任一即触发。
- 典型场景：崩溃 dump 归因、漏洞挖掘与补丁比对、恶意样本行为分析、闭源库/协议算法还原、CTF、内部产品逆向审计。
- 适用产品示例：clr_4.8.4795.dll（.NET CLR 崩溃链）等——示例仅参考，不限定场景。

## 行为准则（分析纪律，全场景通用）

1. **永远先 decompile 再下结论**。禁止只看函数名/汇编片段就推断行为。
2. **判断即标注**：任何「这个函数/变量是干 X 的」结论，必须伴随一次 `rename`（或 `set_comments`）。分析不落库 = 白干，下个会话全丢。
3. **一次只深度处理 1-3 个函数**，避免大批量误改。
4. **不确定时**：改名加 `guess_` 前缀，注释标 `TODO(user)`。
5. **禁止幻觉重命名**：没跑过 `xrefs_to` 确认调用关系，不改全局名/导出名。
6. **批次收尾**：把本次新增的「地址 → 新名字/注释」清单写进当天的 memory 日志（`memory/YYYY-MM-DD.md`），保证跨会话可追溯。
7. **命名分层与辅助手段**：
   - **函数名按调用链分组**：`链路前缀__阶段_动作`（如 clr 逆向的 `PrepareMethod__GetArgInfo1`、`PrepMD_Queue_ExecuteGate`），开链时定一次前缀约定（如 `PrepMD_`），全链统一，聚合阅读/检索两便。
   - **局部变量命名**（实证配方，2026-09-10 clr 逆向验证）：`import ida_hexrays; ida_hexrays.init_hexrays_plugin(); ida_hexrays.rename_lvar(func_ea, "v9", "pMD_records")` —— 先 decompile 确认用途再改；IDA 9.4 MCP 的 `set_type.edits` variable 路径报参数错，用 rename_lvar 替代。
   - **结构体/枚举**：用 `declare_type` 落库——只写在注释里的结构等于没还原；vtable/状态表用 data rename + set_comments 标偏移含义。
   - **高频辅助函数即时命名**：全链路触达 >3 次的（GetModule/LockEnter 类），首次 decompile 确认语义后立即命名，不等收尾——收尾补课是审计发现的最大缺口。
   - **注释禁自造词**（防幻觉）：结构指针用中性名（modulestruct），枚举值未定名时写数值（classification=6）不编枚举名；个人博客/文章不进项目分析注释。

## 调用方式（痛点修复：速度）

- **不要用 mcporter CLI 做多步分析**（每调用冷启动 1~2s，十步就是半分钟纯等待）。
- 用直连客户端（同进程保持连接，~0.2s/次，支持批量）：

```bash
S=~/.openclaw/workspace/scripts/ida-mcp/ida_mcp_client.py
# 单步
python3 $S decompile '{"addr":"0x18005a8bc"}'
# 多步分析一次跑完（decompile → 注释 → 改名）
printf '%s\n' \
 '{"tool":"decompile","args":{"addr":"0x18005a8bc"}}' \
 '{"tool":"set_comments","args":{"items":[{"addr":"0x18005a8e6","comment":"crash: [rax+70h] 未判空"}]}}' \
 '{"tool":"rename","args":{"batch":{"func":[{"addr":"0x18000e968","name":"Module__FindDomainFile"}]}}}' \
 | python3 $S --batch
```

- 37 个工具完整签名与坑点：`~/.openclaw/workspace/references/IDA-MCP-工具速查.md`

## 工具层坑位（实测 2026-09-05，避免重复踩）

1. **decompile 无分页且可能失败**：先 `disasm(addr, include_total=true)` 估函数规模，超大函数改用 `py_eval` 局部取伪码，防止挤爆上下文；hex-rays 直接报错时改用 disasm 分页 + 行号区间本地 grep 还原（2026-09-10 PrepareMethod 链路全函数还原即走此路）。
2. **py_eval 只支持单表达式**：`import x; print(y)` ❌；用 `__import__('idaapi').get_func(...)` ✅。
3. **参数 union 容器**：`rename.batch` / `set_comments.items` / `set_type.edits` 是「对象或数组」二选一，单条传对象、批量传数组。
4. **callgraph 必须限深**：`max_depth`/`max_nodes` 不设会刷回巨量边。
5. **list_funcs/list_globals 必须带 count 分页**，禁止 count=0 全量。
6. **disasm 不可跨函数边界**：addr 一旦越过函数边界，返回会从函数头重取——取不到任意偏移区间，跨函数按函数逐段调用。
7. **batch 输出防御式解析**：json/文本可能混排，逐行尝试 parse，别假定单一格式。
8. **hex-rays 不可用时 decompile 也可能失败**：`init_hexrays_plugin()` 先行；对 0x1012B77D 等函数 decompile 成功率随会话恢复（重进 IDA 或多试）。

## 场景化工作流

### A. 崩溃 dump 归因
1. 从原生栈取崩溃地址/模块偏移 → `lookup_funcs` 定位函数边界。
2. `decompile` 崩溃函数 + 一层 callees，形成假设。
3. `xrefs_to` 验证调用方 → 确认后 `rename` + `set_comments` 落库（含崩溃指令注记）。
4. 沿调用链向上一层，重复 2-3，直到还原完整业务链。

### B. 漏洞挖掘 / 补丁比对
1. 先 `imports`/`find_regex` 建立攻击面清单（危险 API、可疑字符串）。
2. 用 `xrefs_to` 反向定位可达路径，再 `decompile` 确认——**自底向上**，不逐函数扫。
3. 补丁比对：两版同一函数成对 decompile，差异处用 `set_comments` 标 `PATCH-DELTA:`。
4. 结论必须包含「触发前提 + 可达路径」，单点函数片段不足以定性。

### C. 样本行为分析（恶意/未知二进制）
1. 入口：`list_funcs`（带分页）+ `imports` + `find`（string/immediate）三轮建立初判。
2. 关键分支（解密、C2、持久化嫌疑点）逐个 decompile，1-3 个/批。
3. 数据/字符串解码用 `py_eval` 单表达式验证，结论落 `set_comments`。
4. 所有命名带置信度：确证用语义名，推测加 `guess_` 前缀。

### D. 算法还原 / 协议逆向
1. `find`（常量）+ `find_bytes` 定位特征常量（魔数、S-box、CRC 表）。
2. decompile 核心变换函数后，先用 `set_type` + `declare_type` 修类型，让伪码先「变干净」再解读。
3. 还原出的结构体/枚举必须 `declare_type` 落库，只写在注释里的结构等于没还原。

### E. 管线/状态机链路还原（2026-09-10 新增，clr PrepareMethod 实战提炼）
1. 特征码定位链路入口（如 `68 88 00 00 00 B8 ...` 序列 find_bytes）→ 逐函数 disasm 分页还原，grep 过滤时保留原始行文件（grep 会丢指令，误报需用原始数据复核）。
2. 每 call 落一个名字：主链命名 + 谓词 `*_pred` + gate `*_Gate`，用注释记录 A/B 状态差（如「+3: 0x0B(登记)→0x39(JIT)」）。
3. 静态扫描（test/cmp 特定立即数）定位分类位消费点后，必须回 IDA 确认该地址是指令边界（线性扫会命中指令内部字节产生误报）。
4. 收口判据：入口→出口每条边都有名字，A/B 行为差能落到具体 compare/gate。
