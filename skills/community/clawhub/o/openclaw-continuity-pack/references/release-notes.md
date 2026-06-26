# Release Notes

## OpenClaw Continuity Pack v0.5.0

这是一轮面向 ClawHub 的**修复型重新发布**。目标不是换产品方向，而是把当前 workspace 里真正维护的 continuity source pack 整理成一个比线上 `0.4.0` 更完整、结构更一致的可分发版本。

### 这次收口重点

1. **以当前维护中的 source pack 为准重新发布**  
   不再让 registry 包与 workspace 里的主维护目录长期分叉。当前发布包以本地正在维护的 source 结构为准。

2. **补回升级维护链路**  
   重新纳入：
   - `README.md`
   - `references/upgrade-maintenance.md`
   - `scripts/continuity_doctor.py`

3. **保留当前 source 中更完整的分发产物**  
   本轮继续包含并分发：
   - `assets/patch/thread-continuity.patch`
   - `LICENSE`
   - silent continuity / hidden handoff / same-thread rollover 的文档与模板体系

4. **发布元数据与包内实际结构重新对齐**  
   `SKILL.md`、`distribution.md`、资源清单与阅读顺序都已同步到当前目录结构，减少安装后“文档提到但包里没有”或“包里有但入口没写”的不一致。

### 适合谁升级到这一版

- 需要一个**结构自洽**的 continuity pack 分发包
- 需要 runtime patch 文件本体而不是只看说明文档
- 需要在 OpenClaw 升级后先跑 doctor / 再看 patch 锚点的人

## OpenClaw Continuity Pack v0.3.0

这是一轮把 **live 已验收通过的 silent continuity / rollover 行为** 回灌进分发包的同步发布。重点不是新增一整套新产品线，而是让 ClawHub 上的 skill 与当前真正跑通的 live 行为重新对齐。

### 这次收口重点

1. **普通聊天页不再显示 continuity/context 两类提示**  
   前台 UX 改成静默准备，避免在用户界面里暴露“上下文紧张”“即将 compact”之类的提示条。

2. **运行时阈值更新为 80 / 85 / 88 / 90 策略**  
   - 80%：静默 durability refresh  
   - 85%：`compact_prepare` / successor preparation  
   - 88%：若预测下一轮会冲到 90%+，提前准备切换  
   - 90%：`rollover_required`

3. **workspace continuity 规则不再靠 visible compression tactics 控制上下文**  
   `AGENTS.md` 与 `SESSION_CONTINUITY.md` 已同步为“静默准备、不中断回答质量”的版本，移除了 `shorten prose` / `compact user update` / `convergence mode` 这类旧表述。

4. **source-side 对齐测试一起纳入 pack**  
   `thread-rollover.test.ts` 已与最新运行时语义对齐，方便后续在匹配源码树里复验。

### live 验收对齐结果

已对齐到以下 live 结果：
- visible thread 保持不变
- successor rollover 真实发生
- successor transcript 内存在 hidden handoff
- 用户可见历史里看不到 hidden handoff
- `noticeSeen = false`
- `compactPrepareHintSeen = false`
- `contextUsedHintSeen = false`
- rollover 附近的复杂回复仍保持完整质量，不再走“先降智后切”的策略

## OpenClaw Continuity Pack v0.2.1

这是一轮基于真实安装复验的安装体验硬化。重点不是增加新能力，而是让现有能力更容易装对、装稳、装到正确 workspace。

### 这次收口重点

1. 统一安装入口  
   现在优先使用 `scripts/install_continuity_pack.py`，而不是让安装者自己拼多条 bootstrap / patch 命令。

2. 自动识别 workspace  
   `bootstrap_workspace.py` 现在支持 `--workspace auto`，会优先从当前 workspace 语境或常见路径解析目标 workspace。

3. 首次安装心理预期更清楚  
   文档已明确说明 ClawHub 可能出现的静态安全提示，以及为什么这个 skill 会触发该提示。

## OpenClaw Continuity Pack v0.2.0

这是一份面向分发的 continuity / rollover 复用包，目标是把以下能力从单机验证成果整理成别人可部署、可复查、可回滚的发布形态：

- 热层 continuity 闭环
- thread continuity
- successor rollover
- hidden handoff
- continuity notice
- token 缺失 / successor 创建失败 / handoff 注入失败时的诚实降级

## 这次发布重点

1. 规则/模板层收成真正的 skill 入口  
   普通用户可以直接用脚本 scaffold workspace，或只安装 continuity 规则层。

2. 源码补丁层补齐正式安装脚本  
   愿意自己编译部署的人，可以直接做 patch check / apply / rebuild，而不是只靠手工命令。

3. 去现场化、去个人化  
   包里不包含：
   - 真实 memory / plans / status / handoff 实例
   - 真实 token / key / channel / logs
   - 真实路径、用户名、会话名
   - 验收脚本、临时故障注入代码、`.bak_*`

## 已知限制

- 这不是“无限上下文”
- 这是“前台同一对话、后台自动续接”的 continuity 方案
- 最终效果仍受 OpenClaw 版本、安装方式、provider 封装和 UI/runtime 结构影响
