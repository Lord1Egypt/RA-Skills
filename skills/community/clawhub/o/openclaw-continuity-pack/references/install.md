# 安装说明

## ClawHub 页面来的先看这里

如果你是从 ClawHub 链接点进来的，先做这 3 步：

### 第 1 步：把 skill 装进 OpenClaw

优先用 OpenClaw 原生命令：

```bash
openclaw skills install openclaw-continuity-pack
```

如果你更习惯单独的 ClawHub CLI，也可以：

```bash
clawhub install openclaw-continuity-pack
```

### 第 2 步：开一个新会话

安装后的 skill 会在**新会话**里被 OpenClaw 识别。

### 第 3 步：立刻选安装路线

- 只想复用工作风格 / continuity 模板：走“方式一”
- 只想装 `memory / plans / status / handoff`：走“方式二”
- 想做真正的 thread continuity / rollover：走“方式三”

现在优先使用统一安装脚本，而不是自己手拼多条命令：

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route workspace
```

如果你是让另一个 OpenClaw 助手来帮你做，最短可复制指令是：

```text
Install the skill openclaw-continuity-pack, then help me choose the shortest safe path between workspace-only install, continuity-only install, and full runtime continuity.
```

## 适用对象

这份 pack 适合三类人：

1. **想复制工作风格 + continuity 工作流的人**  
   不改源码，先把 workspace 层 scaffold 起来。

2. **想只装 continuity 规则包的人**  
   只接入 `memory / plans / status / handoff` 相关规则。

3. **想让 OpenClaw 真正具备 silent same-thread continuity / rollover 能力的人**  
   需要应用源码补丁、构建并部署。

---

## 方式一：安装可迁移 workspace 层（推荐起步方式）

适合：
- 想让另一个 OpenClaw assistant 更接近这套工作风格
- 想复制 reasoning/style/continuity 的公开可迁移部分
- 不想手工一个个复制模板文件

### 安装方法

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route workspace
```

如果你的 OpenClaw workspace 不在默认位置，也可以显式指定：

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route workspace --workspace <OPENCLAW_WORKSPACE>
```

如需覆盖已有文件：

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route workspace --force
```

如果你只想装 continuity 工作流，不想覆盖更完整的 operating layer：

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route continuity
```

底层等价命令仍然可用：

```bash
python3 <PACK_ROOT>/scripts/bootstrap_workspace.py --workspace auto
```

### 这一步会安装什么

- `SOUL.md`
- `HEARTBEAT.md`
- `AGENTS.md`
- `SESSION_CONTINUITY.md`
- `plans/status/handoff` 模板
- `memory/README.md`
- `temp/README.md`
- 通用 `USER.md` / `TOOLS.md` 模板

### 这一步不会安装什么

- 真实用户资料
- 真实 memory / plans / status / handoff
- provider API key / gateway token
- live channel 配置
- hidden system prompts
- 当前会话状态

---

## 方式二：只装 continuity 规则包

适合：
- 先把 `memory / plans / status / handoff` 连续性流程跑起来
- 暂时不改 OpenClaw 运行时代码

### 安装内容

优先用统一脚本：

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route continuity
```

底层等价命令：

```bash
python3 <PACK_ROOT>/scripts/bootstrap_workspace.py --workspace auto --profile continuity
```

如果你必须手工复制，再复制下面这些文件/目录：
- `assets/workspace/AGENTS.md`
- `assets/workspace/SESSION_CONTINUITY.md`
- `assets/workspace/plans/TEMPLATE.md`
- `assets/workspace/status/TEMPLATE.md`
- `assets/workspace/handoff/TEMPLATE.md`
- `assets/workspace/memory/README.md`
- `assets/workspace/temp/README.md`

### 说明

只装规则包后，你会得到：
- 长任务计划/状态/handoff 规范
- 热层 continuity 规则

但你**不会**自动得到：
- successor session 自动切换
- hidden handoff 注入
- 普通聊天页下的 silent same-thread continuity UX

这些属于源码补丁层。

---

## 方式三：workspace 层 + 源码补丁层

适合：
- 想要“前台同一对话、后台自动续接”的完整 continuity 体验
- 愿意自己编译和部署 OpenClaw
- 持有**匹配的 OpenClaw 源码树**，而不是只有 npm 安装产物目录

这一路线当前面向的行为是：
- 普通聊天页不显示 continuity/context 两类提示
- 高 context 时采用 80/85/88/90 的静默准备与 rollover 策略
- 回答质量不再依赖“先缩短、先敷衍、先压缩”来换上下文余量

### 部署前必须先做的事

先备份：
- `<OPENCLAW_INSTALL_ROOT>/dist/`
- `<OPENCLAW_INSTALL_ROOT>/dist/control-ui/`
- `<OPENCLAW_CONFIG_PATH>`
- `<OPENCLAW_WORKSPACE>/AGENTS.md`
- `<OPENCLAW_WORKSPACE>/SESSION_CONTINUITY.md`
- `<OPENCLAW_WORKSPACE>/plans/`
- `<OPENCLAW_WORKSPACE>/status/`
- `<OPENCLAW_WORKSPACE>/handoff/`
- `<OPENCLAW_WORKSPACE>/memory/`
- `<OPENCLAW_WORKSPACE>/temp/`

### 构建顺序

必须按这个顺序：

```bash
python3 <PACK_ROOT>/scripts/install_continuity_pack.py --route full --source-root <OPENCLAW_SOURCE_ROOT> --apply-runtime-patch --rebuild
```

如果你只想先检查 patch 是否适配你的源码树：

```bash
python3 <PACK_ROOT>/scripts/apply_runtime_patch.py --source-root <OPENCLAW_SOURCE_ROOT>
```

如果你更喜欢底层拆开的命令，也可以：

```bash
python3 <PACK_ROOT>/scripts/bootstrap_workspace.py --workspace auto
python3 <PACK_ROOT>/scripts/apply_runtime_patch.py --source-root <OPENCLAW_SOURCE_ROOT> --apply --rebuild
```

### 为什么不能漏掉 UI 构建

`pnpm build` 只生成 runtime `dist/*.js`。  
如果你不执行 `pnpm ui:build`，就可能丢失 `dist/control-ui/`，导致 live 启动后报：
- `Control UI assets not found`

所以源码补丁部署时，**必须同时执行**：
- `pnpm build`
- `pnpm ui:build`

### 正式部署

1. 停止 live service
2. 用新构建出的整套 `dist/` 替换 live 对应 `dist/`
3. 确认 `dist/control-ui/index.html` 存在
4. 启动 live service

不要只热替换单个 bundle。

### 需要自己填写/调整的配置

参考 `../assets/config/openclaw.example.json`。

用户必须自行填写的通常包括：
- provider id
- upstream base URL
- API key
- gateway token
- workspace 路径
- service 名

详见 `./deploy-notes.md` 和 `./verify.md`。

---

## 关于安全提示

如果 ClawHub 在安装时提示该 skill 为 `VirusTotal Code Insight suspicious`，通常是因为包内包含：
- 本地文件复制脚本
- `git apply` 补丁检查/应用脚本
- 可选的 `pnpm build` / `pnpm ui:build` 重建流程

这不是自动证明它有恶意代码，但意味着安装者应该先看一眼 `scripts/` 与 `references/source-audit.md` 再确认安装。

如果你是作者自己在做发布后回归测试，这一提示目前属于“预期摩擦”，不是安装失败。

## 使用建议

如果你已经维护自己的 `AGENTS.md`，建议**合并 continuity 相关规则**，而不是盲目整文件覆盖。其余模板文件可以直接按需复制。
