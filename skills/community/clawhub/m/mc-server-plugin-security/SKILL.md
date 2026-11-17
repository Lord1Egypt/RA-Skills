---
name: mc-server-plugin-security
description: "我的世界（Minecraft）服务器插件安全经验库。记录已验证有效的加固做法（经验）和踩过的安全坑（漏洞原理+判定+解法），全部脱敏。涉及 AuthMe 登录插件、Bukkit/Spigot/Paper/Leaf/Folia/Arclight/NeoForge 插件安全、登录绕过、session 劫持、ForceOp、插件消息伪造、权限漏洞、0day 排查、jar 静态检查、插件版本比对与升级时使用；搭建或维护 MC 服务器前先查看，避免重蹈覆辙。触发词：AuthMe、登录插件、MC 插件安全、ForceOp、session 劫持、插件 0day、绕登录、Bukkit、Paper、Leaf、插件升级、jar 检查。"
version: "0.1.5"
author: "莫问 的 MC 服务器插件安全实战总结"
created: "2026-09-04"
updated: "2026-09-04"
---

# MC 服务器插件安全经验库

> 从用户云服务器（Leaf 26.2-90，单服直连无代理）的 AuthMe 0day 漏洞排查与修复实战中总结，随后续插件安全维护持续扩展。
> 适用于：MC 服务器（Bukkit/Spigot/Paper/Leaf/Folia/Arclight/NeoForge）插件漏洞排查、加固、升级选型。

## 0. 持续更新协议（活文档，强制）

**本 skill 是活文档，必须随经验与错误持续累加更新，不是一次性产物。**

触发更新的时机（遇到即记，事后补）：
- 排查/修复 MC 插件漏洞或安全问题时踩到新坑、发现新现象、找到新对策
- 用户提出新的插件安全需求，带来新的最佳实践
- 实测（服务器实测/官方 release 交叉核对）暴露了纯静态分析发现不了的问题

更新规则：
1. **追加到对应章节**（插件专题→§1 起、方法论→§2、命令→§3、铁律→§4），没有合适章节就新增小节。新增/修订章节后必须同步更新 §0.1 快速索引表，索引行从章节正文提炼一句话，不复述细节。
2. **每条记录格式**：`问题 | 现象/报错 | 对策`（表格行或列表），注明来源（如 "v0.2 AuthMe 6.0.1 实战"）。
3. **同步更新** `version`（小改+0.0.1、新增章节+0.1.0）与 `updated` 日期。
4. 每次使用本 skill 后，若对话中出现了值得沉淀的经验，**主动补录**，并在回复中告知"已更新 skill"。
5. **更新前必过脱敏核查（强制）**：对照下方「脱敏核查清单」逐项排查，命中即改写/删除后再落盘。
6. **修改后必做自查（强制）**：写完/改完即对照下方「修改后自查清单」逐项核验，未全部通过不自认任务完成。
7. **每次修改必须更新版本号（强制）**：frontmatter `version`（语义化 +0.0.1=小修订/补条，+0.1.0=新增章节/新实战）、`updated` 日期、更新日志（倒序）顶部新增条目，三者一致。

**脱敏与隐私协议（强制）：**
- 本 skill 只沉淀技术经验与安全根因，不承载任何可溯源到具体环境/个人的信息。
- **禁止落盘**：服务器真实 IP/端口、云服务商账号、面板登录信息、内网/私有 IP、管理员账号名、邮箱/电话/微信/QQ 等个人身份、本机绝对路径（`E:\我的世界\...`、`/home/<user>/...` 等特指本机的路径）。
- **允许保留**：通用技术示例、代码/配置范式、纯技术名词、已公开的项目名与版本号（如 "AuthMe 6.0.1"、"Leaf 26.2"）。
- **沉淀前自检**：写任何记录前先问"这条是否暴露了某次具体会话/某台机器/某个账号？"——若是，改写为去标识化的技术描述再落盘。

**脱敏核查清单（每次落盘前必过，命中即改/删）：**
- [ ] **服务器识别信息**：真实 IP/域名/端口 → 删除或改 `<服务器>` 泛指
- [ ] **账号信息**：管理员名/玩家名/邮箱/密码 → 删除或改 `<管理员>` 泛指
- [ ] **云服务商信息**：面板地址/账号/订单号 → 删除
- [ ] **本机绝对路径**：`E:\...`、`/home/<user>/...`、`C:\Users\<user>\...` 等 → 改泛指（`<插件目录>`/`plugins/` 范式）或删除
- [ ] **真实签名/哈希/令牌**：具体密钥、token、commit hash 原文 → 删除或改技术描述
- [ ] **允许保留**：已公开项目名/版本号、插件名、API 名词、通用路径范式

**修改后自查清单（强制，每次写完即执行）：**
- [ ] **脱敏复查**：全文档扫描真实 IP/路径/账号名；对无法确认的识别信息一律删除
- [ ] **版本与日志同步（每次必 bump）**：frontmatter `version` 等于更新日志最新条目，且本次修改已按规则 bump、`updated` 已更新
- [ ] **格式完好**：Markdown 未断裂——表格行列对齐、代码块成对、列表层级正确
- [ ] **内容自洽**：新增/修改的"对策/修复"须与官方 release/commit 或实测一致，不写未验证的断言

---

## 0.1 按问题快速索引（遇到问题先查这里）

| 症状/任务 | 优先读 | 备注 |
|------|--------|------|
| 登录插件可被绕登录 / 未输密码进服 | §1.1, §2.2 | 先分清攻击面：单服 or 代理；pre-join 对话框开没开 |
| 有人说某插件有 0day / 视频演示 exploit | §2（全流程）| 先核官方 release 时间线 + jar 内 class 编译时间，别信文件名 |
| 判断手里 jar 是否安全 | §2.2, §3 | jar tf + 官方 release/commit 交叉核对 |
| 插件要不要升级 / 选哪个平台的 jar | §2.3 | 按服务端核心选型：Leaf=Paper fork 选 Paper 版 |
| 插件缺依赖闪退 | §3 | 检查 softdepend 是否内嵌（PacketEvents 等）|
| Wurst ForceOP / 弱密码爆破 | §1.3 | 这是爆破不是漏洞，靠强密码+失败次数限制 |
| 日志狂刷 Exception / 主线程被拖慢 | §1.4 | 优先看发布/停更插件；换新维护分支修复版 |
| Mojang 429 皮肤请求失败 | §1.5 | 共享 IP 限流，可忽略，勿当漏洞处理 |
| 服务器卡死 / Watchdog 60s 崩溃 / 玩家多就崩 | §1.6 | **先核 Xmx vs 物理内存**，面板自动分配是常见坑 |
| 服务端报 TextureSheetParticle 类找不到 | §1.7 | 客户端粒子类被引用的启动噪音，多不致命 |
| Fetching packet for removed entity 刷屏 | §1.8 | 空物品实体警告，看坐标定是否处理 |
| 上游源码编不过 / 想自己重建修复版 | §1.9, §3 | git log 找污染前干净 commit 做基线；修复常可数据驱动 |
| 实体 tick 崩服（NPE on entity AI） | §1.9, §1.6 | 条带实体的 mod mixin 未判空；先查版本+上游分支状态 |
| 客户端启动即崩 / descriptor 不匹配 | §1.10 | Connector 构造器注入 mixin remap 缺陷；删冗余 mixin 或改 ASCII 文件名 |
| 中文文件名 mod 加载崩 | §1.10 | Connector 缓存错乱；清 .connector + 改纯 ASCII 名 |
| ServerHangWatchdog + 插件堆栈 | §1.11 | 先看内存(非 OOM)；插件主线程同步加载区块 → getChunkNow 换同步 |
| 想改插件字节码/加密码 | §1.11, §3 | ASM 等长替换(iconst_0→nop)；SRG 名查 mappings.dev 别猜 |

## 0.2 章节主题地图

| 主题域 | 章节 | 说明 |
|--------|------|------|
| 插件漏洞专题 | §1 | AuthMe 等登录插件的历史漏洞与修复（每次新插件安全事件在此加小节）|
| 排查方法论 | §2 | 漏洞排查全流程、版本判定、选型逻辑 |
| 常用命令 | §3 | jar 静态检查、GitHub API 版本核对命令 |
| 铁律 | §4 | 本 skill 沉淀的最重要原则 |

---

## 1. 插件漏洞专题

### 1.1 AuthMe：pre-join session takeover（2026-09 披露，高危）

**影响范围**：Paper 1.21+ / Folia 1.21+ 的**离线服（offline-mode）**且开启 **pre-join 登录/注册对话框**的场景。视频演示攻击手法：在受害者登出/认证瞬间用同名疯狂重连，抢走其登录会话，无需密码进服（ForceOp 管理员账号）。

**根因**：认证中的临时状态（正在输入的密码、注册数据、恢复邮箱、pending kick、force-login future）按**玩家 UUID** 存储；离线服所有同名连接解析为同一个离线 UUID → 第二连接可继承/读取/清空第一连接仍在认证中的状态。

**判定**：服务端是否为离线服 + 是否用 pre-join 对话框 + AuthMe 版本是否 ≤ 6.0.0。旧版 fork（如 2024 年的 b53）编译早于修复 commit，受影响。

**修复**：升级到官方 **AuthMe 6.0.1**（2026-09-03 发布，紧急安全修复版）。核心改动：
- pre-join 状态改按**连接会话**隔离（不再是玩家名/UUID）
- 新增 `PendingConnectionRegistry`：连接建立期间独占玩家名，第二同名连接收到 "already online"，名字被夺走的连接直接拒绝
- 空 `proxySharedSecret` 现在**拒绝所有**伪造 `perform.login` 消息
- premium 认证加 `enablePremium` 门控

**验证**：升级后 `jar tf` 应能看到 `fr/xephi/authme/service/PendingConnectionRegistry.class`。

### 1.2 AuthMe：插件消息伪造绕过登录（2022-07 披露，issue #2571）

**原理**：客户端伪装 BungeeCord 代理端，发假插件消息（`BungeeCord` channel + `AuthMe.v2/perform.login`），欺骗 AuthMe 认为该玩家已通过代理登录验证，从而绕过登录直接进服。

**判定**：仅当 `Hooks.bungeecord: true` 且服务端开启 BungeeCord 模式时才受影响；**单服直连（无代理）不受影响**。

**修复**：`config.yml` 中 `Hooks.bungeecord: false`；新版已从根源加固（6.0.1 空密钥全拒）。

### 1.3 Wurst ForceOP / AuthMe Cracker（弱密码爆破）

**本质**：Wurst 客户端的 ForceOP 模块是**爆破工具不是漏洞**——收集管理员用户名后，用常见弱密码表尝试登录（约 1 次/秒，常见密码成功率约 10%）。视频标题里的 "ForceOp" 有时指这个。

**防护**（与版本无关，配置层）：
- 管理员强制强密码（长度/复杂度下限，`settings.security.passwordMinLen` 等）
- 开启登录失败次数限制（`settings.security.maxLoginPerIp`、临时封禁 `temporaryBan`）
- 提示 "Too many failed attempts" 即说明服务器已开反爆破

### 1.4 Galactifun：官方停更 → 新维护分支修复（2026-09 实战）

**现象**：Leaf 26.2 服务端日志每 5 秒刷一次 `IllegalArgumentException: Cannot set time in world without world clock`（完整堆栈 20+ 行），持续数十分钟，日志暴涨、主线程被堆栈文本生成拖累、GC 压力增大。

**根因**：Galactifun（Slimefun 星际拓展）Build 27 的 `DayCycle.tick()` **裸调** `World.setTime()`；新版 API 对无世界时钟的世界直接抛异常。旧版无捕获 → 每 tick 刷堆栈。

**排查要点**：
- 官方仓库 `Slimefun-Addon-Community/Galactifun` **已停更**（最后 commit 2025-06-30）
- 新维护分支 **`Slimefun5/Galactifun`**（2026 年仍活跃），最新 v2.0.2.10
- 验证修复：`unzip -o` 出新版 jar 的 `DayCycle.class`，`javap -c -p` 看 `setTimeSafely` 异常表捕获 `IllegalArgumentException`；并确认 `AlienWorld` 无其他裸 `setTime/setFullTime` 调用

**修复**：升级到 `Galactifun-2.0.2.10.jar`（依赖 Slimefun，api-version 1.16，兼容 Paper 系）。替换后刷屏消失。

**铁律补充**：日志疯狂刷完整堆栈（非单次报错）时，优先怀疑**已停更的附属插件**——查官方仓库更新时间，若停更去找新维护分支/fork。

### 1.5 Slimefun 皮肤 429：共享 IP 限流，非漏洞（2026-09 实战）

**现象**：日志出现 `[dough: skins] Exception while requesting skin: ...sessionserver.mojang.com/...` + `Slimefun Attempted to refresh skin cache` + `HTTP response code: 429`。

**判定**：Mojang 对 `sessionserver.mojang.com` 按 IP 限流。出口是共享 IP（CGNAT 等）时频繁触发；服务端外联网络慢/超时也会加重。Slimefun 自动重试，**不是漏洞、不是配置错，可忽略**。

**应对**：
- 无需改代码/配置，5-15 分钟限流自然解除
- 若持续不断且影响头颅/皮肤显示，可考虑在 Slimefun 配置里关掉在线皮肤刷新或换镜像源
- 不要为"429 报错"去升级 Slimefun 或降级——与版本无关

### 1.6 ServerHangWatchdog 崩溃：先查 Xmx 是否超物理内存（2026-09 实战，重要）

**现象**：Forge 模组服（1.20.1，200+ mod）崩溃，crash 报告开头：
`java.lang.Error: ServerHangWatchdog detected that a single server tick took 60.00 seconds`。
崩溃报告线程转储里**没有主线程 / 只有 DestroyJavaVM**（JVM 正在退出），`Memory: 621 MiB / 5352 MiB up to 15360 MiB`，`JVM Flags: -Xms1024M -Xmx15360M`。

**根因（高频）**：**物理内存 16G，面板（MCSManager 等）自动分配 Xmx=15G**。JVM 还有 1-2G 固定开销（Metaspace/CodeCache/线程栈），于是：
`15G 堆 + 2G 开销 + 系统/cache ≈ 超物理内存 → 玩家进出触发全维度保存 → 堆冲高 → 触顶 swap → 主线程卡死 60s → Watchdog 强杀`。

**判定技巧**：
- 看 crash 报告 `JVM Flags` 的 Xmx，与物理内存对比——**Xmx+2G > 物理内存 = 必崩**
- 崩溃时堆"只用了 5.3G 但已崩" = 不是堆需求不足，是换页（swap）拖死，不是 GC 问题
- 主线程不在线程转储里 = 已经死了/在关闭，别在"谁卡住主线程"上浪费时间

**修复**：把 Xmx 调到 `物理内存 − 4G` 左右（16G 机 → 10G；堆峰值实测 8G 足够）。堆不是越大越好：大堆 Full GC 停顿更长。留出的内存给 Metaspace/CodeCache/page cache（模组服频繁读区块，缓存命中比直读 NVMe 更快）。

**排除逻辑**：模组服崩溃时，日志里各种 ClassNotFound/NoClassDefFound（如客户端粒子类）= 启动噪音，先修内存再看它们。

### 1.7 服务端引用客户端粒子类：TextureSheetParticle 系列错误（2026-09 实战）

**现象**：日志反复出现 `ClassNotFoundException / NoClassDefFoundError: net.minecraft.client.particle.TextureSheetParticle`，来源五花八门——如 EventSubclassTransformer 构建事件处理器、mod mixin 反射 getDeclaredMethod、实体寻路时触发。典型调用链：`RandomStrollGoal → WalkNodeEvaluator → ... → Caused by: ClassNotFoundException TextureSheetParticle`（生物 AI 寻路时触发）。

**根因**：某个 Fabric/跨平台 mod（经 Connector 转译到 Forge）的类**继承/引用了客户端专属类**（`net.minecraft.client.particle.TextureSheetParticle`），服务端 jar 没有这些类。如 `com.cerbon.cerbons_api` 的 `SimpleParticle extends TextureSheetParticle`。

**判定**：`unzip -o` 出该 mod 的 jar，`javap -p` 看类的继承/接口引用是否指向 `net.minecraft.client.*`。注意：**这类错误往往是启动噪音，不直接崩服**（mod 通常 try-catch 降级；昨天今天都报过但服务器照样 Done）。

**应对**：
- 不致命：明确"部分功能降级、不影响运行"即可，可忽略或排后处理
- 若刷屏影响主线程：更新对应 mod（官方可能有适配）；失效则停用该 mod
- **不要**把时间花在"让服务器通过"上——服务端本来就不该加载这些类，让它失败是正常现象

### 1.8 `Fetching packet for removed entity` 警告：无害但值得看坐标（2026-09 实战）

**现象**：`[minecraft/ServerEntity] Fetching packet for removed entity ItemEntity['Air'/616, ... removed=DISCARDED]`，同一坐标大量空物品实体。

**判定**：实体被 DISCARDED 后相邻的区块同步周期还去取它的网络包 → 打印一行 WARN。空物品实体（`ItemEntity['Air']`）集中在同一坐标 = 该处有掉落物堆积/清理逻辑循环，或玩家快速捡丢物品。**不致命、不会崩服**，但会刷屏。

**应对**：偶发十几条 → 直接忽略；持续刷屏提到某个坐标 → 去该坐标看是否有自动化掉落回收装置，`kill @e[type=item,distance=..30]` 清场。优先级低于 1.6/1.7。

### 1.9 上游源码分支被污染 → 用历史干净 commit 重建修复版（2026-09 实战）

**现象**：Forge 1.20.1 服（Connector 跑 Fabric mod），玩家手持非食物物品 + 狼 BegGoal 时崩服：`NPE: Cannot invoke "FoodProperties.isMeat()" because "Item.getFoodProperties()" is null`（`WolfEntityMixin` / `feedMulchToWolf`）。这是 bountifulfares 1.2.1（1.20.1 官方最高发布版）的 bug。

**排查关键**：
- 官方 1.20.1 分支最新 HEAD **编不过**：fork 源码发现混入大量 **1.21 API**（`net.minecraft.component`/`recipe.input`）。看 git 历史才明白——作者 2025-03 在 1.20.1 分支上执行过 `remove everything → move 1.21 to 1.20 → rerestart 1.20 version`，**把 1.21 代码搬回 1.20 时搬坏了，分支从此不可编译**。1.3.0-1.20.1 源码里明明已修 wolf bug，但从未发布 jar。
- **解法**：从 1.20.1 分支历史里找**污染前的干净 commit**（`git log` 定位到 2025-02-12 的 `Fix compat when using synitra`），用那个版本做基线构建 ✅

**修复复刻**（数据驱动，官方 1.3.0 同法）：
1. 删 `WolfEntityMixin.java` + 从 `mixins.json` 移除条目
2. 新增 `data/minecraft/tags/item/wolf_food.json` = `{"values":["#bountifulfares:mulch"]}` —— 把覆盖物挂到原版 `#minecraft:wolf_food` 标签，原版狼喂食逻辑自带判空，无需自定义 mixin
3. 陷阱：删 mixins.json 条目后**会留尾随逗号 → JSON 非法**,必须同时修掉,否则 mod 加载即崩

**构建**：`git checkout <干净commit>` → 打补丁 → `./gradlew build -x test`（JDK 21 + Gradle 8.6 + fabric-loom；国内网络切腾讯云 gradle + 阿里云 maven 镜像）。产物 `build/libs/<mod>-<ver>.jar`。

**通用铁律**：上游仓库分支被作者搞坏/停更时，先看 `git log` 找污染前的干净 commit；修复往往可数据驱动（tag/json）而非改字节码。

### 1.10 Sinytra Connector 的两个崩溃坑（2026-09-05 实战，客户端）

**坑 A：Connector 对「构造器注入型 mixin」的 remap 缺陷 → 客户端启动即崩**

现象：客户端（Forge + Connector 跑 Fabric mod）在 `Initializing game` 阶段崩，`MixinTransformerError → InvalidInjectionException`，报 `Expected (ClientLevel;DDDDDD;BlockState;CallbackInfo)V but found (ClientLevel;DDDDDD;BlockState;BlockPos;CallbackInfo)V`。

根因：mod 里某个 `@Inject(method = "<init>*")`（构造器通配符注入）的 mixin，Connector 在 remap 成 `_mapped_srg` 中间产物时**把构造器的 `BlockPos` 参数映射错位** → 签名对不上 → 必崩。**服务端没事**（构造器注入只影响客户端渲染类），**客户端必崩**。

解法：这类 mixin 若只是纯视觉/渲染微调（如粒子染色），**直接删掉**——从 `mixins.json` 的 `client` 列表移除 + 删源码 + 清理其唯一依赖的 accessor，重建 jar。功能零损失。

**坑 B：mod 文件名用中文 → Connector 缓存生成错误的 `_mapped_srg` 中间产物 → 同样签名错位崩溃**

现象：把修复版 jar 用**中文文件名**（如 `bountifulfares-1.3.0-1.20.1（修复版）.jar`）放进客户端 mods，Connector 在 `.connector/` 隐藏目录生成 remap 缓存时把中文名原样带入，加载到的是**未完成最终映射的中间版** → mixin 签名错位 → 崩。

解法：mod 文件名**必须纯 ASCII**；已发生则**删除 `mods/.connector/` 缓存目录**后重启（Connector 会用干净文件名重新 remap）。

**通用铁律**：Connector 环境下遇到"签名错位/descriptor 不匹配"类崩溃，先想两条——① 构造器注入型 mixin 是不是 remap 缺陷；② 文件名是不是非 ASCII。两者都是"删缓存/删冗余 mixin/改 ASCII 名"就能解决，不用动核心逻辑。

### 1.11 插件主线程同步区块加载 → watchdog 崩服，ASM 字节码修复（2026-09-07 实战）

**现象**：Forge 1.20.1 服，`ServerHangWatchdog detected that a single server tick took 60.00 seconds`。堆栈指向 `com.itemban.ItemBanHandler.scanNearbyChunks` → `ChunkSource.getChunk`。内存充足（堆仅用 ~1.7G/6G）——**不是 OOM，是插件阻塞**。

**根因**：封禁物品插件 `ItemBan 1.0.3` 在**主线程**对玩家周围 5×5=25 个区块逐个同步 `ChunkSource.getChunk(x,z,false)`。区块加载线程繁忙时主线程逐块阻塞，累计 >60s → watchdog 杀服。**插件主线程做同步区块加载是 Forge 大忌**。

**诊断流程**：
1. 看到 `ServerHangWatchdog` + 堆栈在某个 mod → **先看内存**（`Memory: xx / xx up to`）：内存充裕 → 不是 OOM，是阻塞
2. **反编译堆栈里的类**（`javap -c -p`）确认是不是在 `getChunk`/`ServerChunkCache` 上同步等待

**修复（ASM 字节码 patch，保功能）**：
- `ChunkSource.getChunk(x,z,false)`（同步，等加载）→ `getChunkNow(x,z)`（异步非阻塞，未加载返回 null）
- **关键坑**：删除 `iconst_0`（false 参数）会让字节码长度变化 → stack map frame 失效 → JVM 校验错误。**正确做法是 `iconst_0` → `nop`（同 1 字节，长度不变，frame 全有效）**
- **方法名必须查 SRG 映射**（`mappings.dev/1.20.1/...?load=srg`）：`getChunkNow` 是 `m_7131_` 不是 `m_62225_`（后者是另一个方法 getChunk(IIZChunkStatus) 的参数名）——**猜名字必 NoSuchMethodError**
- 验证：① javap 确认新方法引用就位、无旧方法残留；② 其他方法 md5 必须一致（证明零误伤）；③ `javap -v` 看 StackMapTable 仍有效

**通用铁律**：
- "主线程同步 load chunk" 是插件坏实践的标志——遇到先想能否换 `getEntities`（纯实体查询，无区块加载）或 `getChunkNow`
- 字节码 patch 保持长度不变（指令等长替换）是最稳的，避免重新算 frame
- JS 改前 `javap` 全量记录，改后逐项对比（iconst_0 计数、其他方法 md5、StackMapTable 数量）

---

## 2. 排查方法论

### 2.1 完整排查流程（遇插件 0day 情报时按此走）

1. **定位插件**：确认用户服务器用的插件文件与版本（`jar tf` / plugin.yml）
2. **查漏洞情报**：搜索官方 issue / release notes / 第三方披露，**多源交叉**，别只信视频标题
3. **核版本时间线**（关键）：用 GitHub API 查官方 release 日期 + 修复 commit 日期，与手里 jar 的 class 编译时间对比
4. **确认攻击面**：问清/查清服务器架构（服务端核心、是否接代理、关键配置项如 bungeecord、pre-join 对话框）
5. **给出修复**：升级到含修复的官方版本 + 按需配置加固
6. **验证**：升级后 jar 静态检查（关键类/版本号）+ 有条件时测试服验证

### 2.2 版本安全判定（核心技巧）

**不能只看文件名**。判定一个 jar 是否含安全修复：
- **看编译时间**：`jar xf` 解出 class，看文件时间戳；早于官方修复 commit 日期的构建必不含该修复
- **看关键类**：`jar tf` 检查官方修复引入的标志性类（如 `PendingConnectionRegistry`）
- **看官方时间线**：`api.github.com/repos/<owner>/<repo>/commits/<hash>` 拿修复 commit 日期；`/releases` 拿各版本发布时间
- **fork 要警惕停更**：社区 fork 可能停在某个版本后只有 CI/构建提交、不再同步官方安全修复（如 AuthMeReReloaded 在 b53 后停更安全修复）

### 2.3 按服务端核心选型（升级时怎么选 jar）

| 服务端核心 | 选哪个 jar | 说明 |
|-----------|-----------|------|
| Leaf / Paper / Purpur 等 Paper fork | **Paper 版** | 完全兼容 Paper/Spigot 插件 |
| Folia | **Folia 版** | 异步分片核心，API 不同 |
| 原版 Spigot（未 fork）| **Spigot 版** | 按 MC 版本选 |
| 旧版 MC（< 1.16）| **Legacy 版** | 注意 Java 版本要求 |

选错平台 jar 的常见后果：启动报错 / 功能静默失效 / API 不兼容。

### 2.4 依赖判断

- 插件的 **depend** 缺失：启动即失败（明确报错）
- 插件的 **softdepend** 缺失：多数功能照常，但依赖它的特性降级/不可用
- **先查是否内嵌**：`jar tf` 搜依赖包名（如 `retrooper`=PacketEvents）。未内嵌才需要额外装

---

## 3. 常用命令

```bash
# jar 内容清单（找 plugin.yml / 关键类 / 可疑条目）
jar tf "<插件.jar>"

# 提取 plugin.yml 看版本、main、api-version
unzip -p "<插件.jar>" plugin.yml | head -30

# 提取某类看编译时间（用清单路径）
jar xf "<插件.jar>" <路径>/<类名>.class && ls -la <类名>.class

# 可疑条目快速扫描（backdoor/hack/shell 等）
jar tf "<插件.jar>" | grep -iE "backdoor|hack|exploit|shell|payload|webshell|forceop"

# 官方仓库最新 release 与日期
curl -s "https://api.github.com/repos/<owner>/<repo>/releases?per_page=8" | grep -E '"tag_name"|"published_at"'

# 官方某个 commit 的日期（核对修复是否早于手里的 jar）
curl -s "https://api.github.com/repos/<owner>/<repo>/commits/<hash>" | grep '"date"'

# 下载 GitHub release 资产
curl -sL -o "<目标名.jar>" "<browser_download_url>"
```

---

## 4. 铁律（最重要）

1. **先核官方，再信传言**：视频/帖子标题说 "0day"、"ALL VERSIONS" 时，第一时间看官方 issue + release notes + commit，多源交叉，不采信单来源结论。
2. **版本新旧看时间线，不看文件名**：文件名里写着 5.7.0-FORK 也可能缺 2026 年的修复；class 编译时间 + 官方 release 日期才是硬依据。
3. **先问清架构再动手**：攻击面由部署形态决定（单服 vs 代理、pre-join 对话框开没开、核心是 Paper 还是 Folia），不知道就先问，别猜。
4. **升级前必备份**：插件 jar + 插件数据目录（配置/账号库），升级有风险时要能回滚。
5. **安全修复版优先于花哨 fork**：社区 fork 停更后安全风险随时间累积，回归官方主线常是最稳选择。
6. **配置文件即安全边界**：很多"漏洞"其实是配置暴露（bungeecord 开着、弱密码、无失败限制），加固配置和升级插件同样重要。

---

## 更新日志（倒序）

- **0.1.5（2026-09-07）**：新增 §1.11 插件主线程同步区块加载→watchdog 崩服的诊断与 ASM 字节码修复（ItemBan 实战）——先看内存区分 OOM/阻塞、`getChunk`→`getChunkNow` 换同步、`iconst_0`→`nop` 等长替换保 frame、SRG 名查 mappings.dev 别猜、验证用 md5+StackMapTable；索引表加两行。
- **0.1.4（2026-09-05）**：新增 §1.10 Sinytra Connector 两个崩溃坑——① 构造器注入型 mixin 的 remap 缺陷（客户端 `Initializing game` 崩，descriptor 不匹配，删冗余 mixin 解决）；② mod 文件名用中文导致 Connector 生成错误 `_mapped_srg` 缓存（清 `.connector` + 改纯 ASCII 名解决）；索引表加两行。
- **0.1.3（2026-09-04）**：新增 §1.9 bountifulfares Wolf NPE 崩服实战——上游分支被 1.21 污染无法编译时，用 git log 找污染前干净 commit 作基线重建修复版；修复复刻（删 mixin + wolf_food tag 数据驱动）+ 删 mixins.json 条目留尾随逗号的陷阱；索引表加两行。
- **0.1.2（2026-09-04）**：新增 §1.6 Forge 服 ServerHangWatchdog 崩溃排查（面板 Xmx 自动分配超物理内存→swap→主线程 60s 卡死，判定技巧+修复）、§1.7 服务端引用客户端粒子类（TextureSheetParticle 系列，含 Cerbons API 实例）、§1.8 空物品实体警告；索引表加三行。
- **0.1.1（2026-09-04）**：新增 §1.4 Galactifun 停更迁移实战（Build 27→2.0.2.10 修复 world clock 刷屏）、§1.5 Slimefun 皮肤 429 共享 IP 限流判定；索引表加两行。
- **0.1.0（2026-09-04）**：初版。沉淀 AuthMe 0day 排查修复实战：pre-join session takeover（§1.1）、插件消息伪造（§1.2）、ForceOP 爆破（§1.3）、排查方法论与选型逻辑（§2）、常用命令（§3）、铁律（§4）。
