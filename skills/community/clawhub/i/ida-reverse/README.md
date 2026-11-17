# ida-reverse

使用 IDA Pro MCP 做任何逆向工作时必须加载的规范化分析流程技能。

## 定位

**流程规范**，不是场景手册。无论分析对象是崩溃转储、可疑样本、闭源协议还是自家二进制，只要通过 IDA MCP 做逆向，本技能即生效。

## 核心纪律

1. **先 decompile 再下结论**——禁止只看函数名/汇编片段推断行为
2. **判断即标注**——「这个函数是干 X 的」结论必须伴随 rename/set_comments 落库
3. **一次 1-3 个函数**——避免大批量误改
4. **不确定加 guess_ 前缀**，注释标 TODO(user)
5. **禁幻觉重命名**——没跑 xrefs_to 不改全局名/导出名
6. **批次收尾落 memory**——地址→名字/注释清单进当天日志
7. **命名分层与辅助手段**——函数按调用链前缀分组（`链路__阶段_动作`）；局部变量用 `ida_hexrays.rename_lvar(func_ea, "v9", "语义名")`（实证配方）；结构体/枚举 declare_type 落库；高频辅助函数（触达>3次）首次确认即命名；注释禁自造词

## 场景工作流

- **A. 崩溃 dump 归因**：原生栈 → lookup_funcs → decompile → xrefs 验证 → 落库
- **B. 漏洞挖掘/补丁比对**：攻击面清单 → xrefs 反向定位 → 成对 decompile 标 PATCH-DELTA
- **C. 样本行为分析**：list_funcs+imports+find 三轮初判 → 关键分支 decompile
- **D. 算法还原/协议逆向**：特征常量定位 → set_type+declare_type 修类型
- **E. 管线/状态机链路还原**：特征码定位入口 → disasm 分页还原 → 静态扫描命中回 IDA 验指令边界 → 收口判据=每条边有名字且行为差落到具体 gate

完整规范见 SKILL.md。

## 组成

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 流程规范全文（纪律 7 条 + 工具坑 8 条 + 场景 A-E + 收尾） |
| `scripts/ida_mcp_client.py` | OpenClaw 会话内直连 ida-pro-mcp 的 HTTP 客户端（绕过 mcporter 冷启动，~0.2s/次，支持 --batch JSON Lines 批量、--list-tools 自省；仅依赖 Python 3 标准库） |

## 环境要求

- IDA Pro 9.x + ida-pro-mcp 插件（默认 `http://127.0.0.1:13337/mcp`，无鉴权仅本机，可用环境变量 `IDA_MCP_URL` 覆盖）
- Python 3（客户端零第三方依赖）

## 实战背景

本技能在 2026-09-05~09-10 的 .NET Framework clr.dll（4.8 x64/x86 多版本）逆向中实战打磨：PrepareMethod 管线全链还原（30+ 函数命名落库）、分类位分流机制定案（mdcStatic 位手术如何让 PrepareMethod 真正 JIT）。技能内的工具坑位（decompile 失败降级、disasm 不可跨函数边界、batch 防御式解析等）均为实测踩坑沉淀。
