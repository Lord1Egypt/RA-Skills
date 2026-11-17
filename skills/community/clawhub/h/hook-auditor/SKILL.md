---
name: hook-auditor
description: 审计并清理 Claude Code 中「你不知道自己装了」的 hook。安装 skill 或 plugin 会自带 hook，它们安装即常驻、每轮对话都跑、持续烧 token 并可能拦截或改写工具调用——即使你从未调用过那个 skill。本 skill 枚举全部真正生效的 hook、标注来源与可信度、量化每轮成本，并在你确认后清理。触发场景：用户说「清理」「提速」「省 token」「变慢了」「token 消耗太快」「怎么这么慢」「清理配置」「检查 hook」「有哪些 hook」「audit hooks」「清理插件」「为什么会自动触发」「莫名其妙弹出」「我没让它这么做」，或用户抱怨出现了未预期的自动行为、权限询问、注入文字。也在安装来源不明的 skill/plugin 后主动建议运行。
---

# Hook Auditor

审计并清理未预期的 hook。

## 为什么需要它

Hook 是 Claude Code 的生命周期回调。**装一个 skill，它自带的 hook 就常驻生效——不需要你调用那个 skill。**这带来三类你未同意的后果：

1. **烧 token**：`prompt` 型 hook 直接往上下文注入文字；`UserPromptSubmit`/`Stop` 每轮都跑
2. **拖慢**：`PreToolUse`/`PostToolUse` 在每次工具调用前后各跑一次子进程
3. **改行为**：`PreToolUse` 能返回 `deny`/`ask` **拦截工具调用**，或注入 `additionalContext` 影响判断

来自网上安装的 skill 尤其值得查——它的 hook 可能为作者的场景（评测、CI、特定工作流）设计，套在你身上就是纯噪音甚至阻塞。

## 核心事实（判断生效与否的唯一依据）

`hooks.json` 存在 **≠** 生效。四种来源截然不同：

| 位置 | 是否生效 |
|---|---|
| `~/.claude/settings.json`、`settings.local.json` | **生效**（用户自己配的，默认可信） |
| `~/.claude/skills/<name>/hooks/hooks.json` | **生效**，安装即常驻 ← 意外 hook 主要来源 |
| `~/.claude/plugins/cache/<mkt>/<plugin>/hooks/hooks.json` | **仅当** settings 的 `enabledPlugins["<plugin>@<mkt>"]` 为 `true` |
| `~/.claude/plugins/marketplaces/**/hooks/hooks.json` | **永不生效**——marketplace 仓库缓存 ← 最易误判 |

**别靠 `find` 数 hooks.json 文件数下结论**，会把仓库缓存当成生效项（实测常见 11+ 个纯缓存文件）。

## 工作流程

### 第一步：扫描

```bash
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python ~/.claude/skills/hook-auditor/scripts/scan_hooks.py
```

Windows GBK 终端必须带 `PYTHONIOENCODING=utf-8`，否则 emoji/中文报 `UnicodeEncodeError`。加 `--json` 得机器可读输出。

脚本输出：生效 hook（按来源分组、标每轮触发）· 成本提示 · 不生效项 · 缓存文件数。

### 第二步：判定每个 hook 的去留

对每个**生效**的 hook 问三个问题：

1. **是我配的吗？** 用户 settings 里的 → 保留，除非用户主动要删
2. **它服务于我在用的功能吗？** 来自从未调用的 skill → 删除首选项
3. **它每轮都跑吗？** `UserPromptSubmit`/`PreToolUse`/`PostToolUse`/`Stop` → 成本最高，优先处置

事件语义速查见 [references/hook-events.md](references/hook-events.md)——需要向用户解释某个事件何时触发、matcher 什么含义、能造成什么影响时读它。

### 第三步：dry run（不确定影响时必做）

hook 是从 stdin 读 JSON 的普通脚本，可脱离 Claude 单独测，零副作用：

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"},"transcript_path":""}' | bash <hook脚本路径>
```

有输出 = 会干预（看 `permissionDecision`：`ask`/`deny`）；无输出 = 放行。

**穷举参数再下结论**。同一 hook 常因参数不同而结果相反——例如某 guard 对 `du ~/memory` 放行，但对 `ls ~/memory > o.txt` 拦截（多了重定向即判定为写操作）。只测一条命令会得出错误结论。

不确定 hook 的激活条件时，读它的脚本源码找判定函数（常见形如 `is_active()`），看它依赖环境变量、配置文件还是扫描 transcript 关键词。**扫 transcript 关键词的实现容易自我误触发**——skill 清单里出现该 skill 的名字就可能命中。

### 第四步：报告并等确认

按此结构报告，**然后停下等用户点头**：

- **生效的 hook**：来源 · 事件 · 每轮是否触发 · 干什么
- **建议清理**：哪些、为什么（token/延迟/行为干预）
- **建议保留**：用户自己配的、正在用的
- **不生效的**：说明清楚，避免用户误以为需要处理

删 hook 属修改用户全局配置，**必须先确认**。

### 第五步：清理（获准后）

**始终先备份**：

```bash
cp <hooks.json> <hooks.json>.disabled-<YYYY-MM-DD>-full
```

三种粒度，按需选：

| 目标 | 做法 |
|---|---|
| 删单个事件 | 从 `hooks` 对象里移除该事件键 |
| 删某 skill 全部 hook | 把 `hooks` 置为 `{}`，并在 `description` 写明停用日期、原状、备份文件名、恢复方法 |
| 停用整个 plugin | 把 settings 的 `enabledPlugins["<id>"]` 设为 `false`（比删文件干净，且不被更新覆盖） |

**保留 skill 本体和 hook 脚本文件**——只摘掉注册。用户仍可主动调用该 skill，将来也能一键恢复。

**不要动 `plugins/marketplaces/` 下的任何文件**：不生效，且会被下次 marketplace 同步覆盖。

### 第六步：验证

```bash
python -c "import json;print(list(json.load(open(r'<path>',encoding='utf-8'))['hooks']) or '(empty)')"
```

再跑一次 `scan_hooks.py` 确认目标 hook 已消失、该留的还在。

**必须告知用户：hook 配置在会话启动时加载，改动要重启 Claude Code 才生效。**当前会话里被删的 hook 可能继续响应，那是内存残留不是失败——不解释清楚，用户会以为清理无效。

## 反向验证脚本改动

改过 `scan_hooks.py` 后，用备份文件验证它仍能抓到 skill hook：临时把完整备份拷成 `hooks.json` → 跑扫描确认抓到 → **立刻还原**。只在空配置上测，无法证明检出能力。
