# 自动识别与召回（1.2.13）

Hui-Yi 保留为低频冷记忆层。高频个人信息由 OpenClaw 原生记忆负责，不要求用户先说“回忆一下”或 `/hui-yi`。识别、保存候选、晋升与回答前召回是不同步骤：发现一句话不等于它已成为可靠的长期事实。

## OpenClaw 2026.9.5 的接入方式

- `memory-core` 的 dreaming 从有来源标记的会话提取候选、累计真实使用证据并整理记忆。默认本地时间 03:00 运行；有后台模型调用。高频事实归入主记忆，不自动复制到冷记忆。
- 适配器通过公开的 `openclaw/plugin-sdk/memory-host-search` 获取原生记忆管理器，在 `before_prompt_build` 阶段检查本轮话题与可信主记忆 trigger 的匹配，并注入最多三条、1,800 字符的有关背景。只接收 `MEMORY.md` / `USER.md` 的可信条目，不调用模型做额外摘要，也不从用户话语直接写入事实。无命中时继续由主 agent 按需要使用 `memory_search` / `memory_get`，不额外启动深度召回子运行。
- deep 晋升保留至少 `minScore=0.75 / minRecallCount=3 / minUniqueQueries=3`，必须有可信 owner/agent 来源；`maxPriorEntryLossFraction=0` 避免自动整理丢失既有条目。计数不是事实正确性的证明。明确更正优先于旧记录，历史状态不能冒充当前状态。
- 提取与晋升是异步过程，不能承诺每条消息立即变成长期记忆。用户明确要求记住的事实仍应及时按宿主记忆流程保存；不要等待夜间任务才响应用户。

## 本次保守接入范围

配置工具接通 WebChat 网页会话（默认 main 和 explicit），排除配置中的外部渠道、群组、频道和外部 hook 内容；保持 `memory.search.rememberAcrossConversations=false`。未知来源不会凭交流次数自动认定为主人。外部本人私聊需要明确身份配置与独立隔离验证后才能扩大范围。

工作区 `MEMORY.md`、`USER.md` 和冷记忆均是共享资料，不具备按 peer 隔离的存储。会话哈希仅用于去重，不能授权读写私人资料。后续新增外部渠道时必须重新核对 exclusion 配置。

接入由技能包内 `templates/native-memory-plugin/` 的持久适配插件 `hui-yi-native-memory` 承担。真正的原生 `active-memory` 插件保持禁用；适配器使用公开 SDK 的主记忆候选接口，不执行私有入口，也不投影启用配置。既有原生配置可以保留作回退参考，但不会由本适配器执行。

适配器在加载及每次召回前后校验宿主版本、兼容性基准入口 SHA-256 和自身文件，并要求可信宿主提供 `messageProvider=webchat`、配置所允许 agent 的私有会话及本轮工具授权。未知来源、外部渠道、群组及运行时不匹配都会跳过召回。版本校验不等于全部传递依赖防篡改。WebChat 客户端鉴权仍由 OpenClaw 入口负责，这不是 owner/admin 检查；dreaming 的 owner 晋升检查是另一条边界。

第三方插件还需要宿主明确允许 `plugins.entries.hui-yi-native-memory.hooks.allowConversationAccess=true` 和 `allowPromptInjection=true`。配置工具仅对本适配器设置这两个授权，用于读取本轮对话和添加已核实的缓存背景；适配器仍独立执行上述范围检查。缺少会话权限时，宿主会拒绝注册回调，即使模块加载与隔离测试已通过也不会自动召回。

首次共享记忆管理器初始化可能需要约 8 秒，随后复用通常很快。因此缓存等待上限为 15 秒，回调上限为 25 秒；超时跳过，不阻止主 agent 常规检索。不能把每轮误设为 `purpose: status`：那会创建应由调用方清理的独立管理器；本实现使用 `default` 共享实例且不关闭它。

此方式避免 2026.9.5 原生第一层缓存遗漏 chatType 检查的问题，并在宿主自动更新后默认停止未经复核的召回。不能从第三方插件直接 require 整个私有 Active Memory 入口：宿主的插件源码捕获会复制大量 OpenClaw 依赖，已在真实启动中造成运行时准备超时；standalone Node 加载成功不足以证明宿主兼容。无需关闭 OpenClaw 自动更新，也无需修改新安装的宿主文件。升级后重新审计版本/hash与公开 SDK 合同并回归，才恢复自动召回。`scripts/patch_native_memory.py` 仅保留为精确版本补丁工具。

```text
python scripts/configure_native_memory.py --config-path <openclaw.json> --runtime-entry <openclaw/dist/extensions/active-memory/index.js> --plugin-dir <installed-skill/templates/native-memory-plugin> --backup-dir <private-backup-directory>
```

配置脚本校验已审计运行时和适配器身份；默认预览，追加 `--apply` 才写入。写前保存具有原访问权限的完整配置备份，保留模型、凭据、渠道访问策略及其他插件设置。配置可能含秘密，备份不可打包或共享。接入会启用原生 dreaming 与适配器召回、停用原生 `active-memory` 直接入口及旧 `hui-yi-signal-hook`，并需要重启 Gateway。原生模型/embedding 使用宿主已配置的服务，可能产生网络请求和费用；读取候选也可能触发宿主索引来源修复及后台 embedding 同步，不能承诺整个接入完全离线。Hui-Yi 自身的词法匹配不联网。

## 旧 hook 的兼容边界

`templates/hook/` 保留给已有自定义宿主。它只响应可信 skill-selection 或映射正文开头的显式命令，不是本次自动记忆入口。当前原生 mapper 不提供 selection metadata，渠道包装或 slash-command 截获也可能使文本命令不到达 hook；因此不能把旧 hook 的启用状态当作自动检测已经生效。

## 检索质量与证据

原生快速缓存要求 `MEMORY.md` / `USER.md` 的可信条目带有行尾 `<!-- trigger: … -->`。旧 Markdown 没有这些元数据时，即使全文已经索引也只能走普通/深度检索。既有缓存维修可使用 `scripts/annotate_primary_cache.py`：计划仅指定文件名、文件及原文行 SHA-256、行号、触发短语；默认预演，`--apply` 才追加元数据。只允许既有 bullet、禁止在代码块中操作，原文、日期和计数不变，写前保存受保护的原始文件备份。

触发词应从经核实的稳定事实或偏好中整理，不按交流次数推断身份，不给过期状态加长期触发标签，也不为了测试编造用户事实。新对话的候选提取仍由原生 dreaming 与宿主记忆流程承担；本脚本不会后台扫描全部消息。适配器清除检索用文本中的外部引用、代码与元数据噪声，再扩展有限、去重的中文词；清空后跳过匹配，不回退到被清除的原文，不改主对话消息或事实。

- 中文自然句用规范化双字片段匹配，英文用完整词边界；剔除常见问法，重复同一个词不会增加证据。
- 先满足内容相关度，再以有日期的重复证据有限加分；无关高频记录不能越过门槛。
- `fixture/is_fixture=true`、`active=false`、`status` 为 superseded/retracted/deleted/inactive 或设置 `superseded_by` 的记录不进入正常候选。
- 重建索引保留会话去重记录、别名和失效标记，读取完整 TL;DR 和多级目录。新笔记计数从零开始，不补造过去的交流次数。
- 词法相似度不会自行理解事实矛盾。带日期的来源、最新明确更正与人工反馈仍是判断事实的依据。

验证应分别报告：隔离回归、真实数据只读检索、运行时启用状态、真实渠道一轮对话。前三者通过不能冒充最后一项通过。

宿主轨迹中的 prompt 可能已经脱敏，无法用脱敏字符串中没有 marker 来判定注入失败。可在授权审计时追加 `--diagnostics`：只记录选中条数及模型输入中缓存 marker/引用的数量，不记录正文、触发词、路径或原始会话/运行 ID。默认不启用；标记出现在模型输入与仅在选择阶段命中是不同证据。
