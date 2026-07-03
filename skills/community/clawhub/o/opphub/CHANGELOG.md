# Changelog

偶合 OppHub skill 的版本历史。

## [1.0.14] - 2026-07-03

### Fixed · opphub status 区分 401 错误类型

- 之前：所有 401 都提示「token 无效或过期，请重新登录」
- 现在：区分 4 种错误，给针对性提示
  - `session_revoked` → 「token 已被吊销（在新设备登录过？被人登出？）」
  - `token_expired` → 「token 已过期（30 天）」
  - `invalid_token` → 「token 无效（可能是服务端密钥轮换）」
  - 其他 → 通用提示

### 配套服务端 v1.0.15

- `active_jti` 改 Set：多设备共存，新登录不再顶掉旧设备的 jti
- `logout` 遍历 Set 中所有 jti 注销
- 老 `/api/auth/me` 补 jti 校验（与 `/v1/auth/me` 对齐）

## [1.0.13] - 2026-07-03

### Added · 路径解析（兼容各种机器/容器/K8s）

- 新增 `lib/opphub-paths.sh`，所有 bin 脚本统一 source
- 解析顺序（命中即返回）：
  1. `$OPPHUB_HOME`（用户显式指定，最优先）
  2. `$XDG_STATE_HOME/opphub`（XDG Base Dir）
  3. `$OPPHUB_DATA_DIR`（容器/K8s 专用，只读 rootfs 友好）
  4. `$HOME/.opphub`（传统兜底）
  5. `/tmp/opphub-$UID`（无 HOME / HOME 不可写时）
- 启动时一行 debug：`export OPPHUB_DEBUG=1` 可见解析路径
- 8 个 bin 脚本全部接入

## [1.0.12] - 2026-07-03

### Added · 注册首次可选设密码

- `opphub register` 第 1 步完成后问「是否设置登录密码」（8-32 位）
- 设了 → 后续可用密码 OR 验证码登录
- 不设 → 只能验证码登录（后续 `opphub passwd` 可补设）
- `opphub login` 已有 4 个选项（邮箱/手机 × 验证码/密码）

### Added · Session 管理（jti 黑名单）

- 后端 JWT 含 jti，存 Redis（30 天）
- `opphub logout` 调 `/v1/auth/logout` 兑水当前 jti，后续请求报「已注销」
- 新设备登录顶掉旧设备的 active_jti（防多端刷）
- `state.json` 同时存 opphubToken + jti

### Fixed · SKILL.md 补「验证码 vs 密码」说明

- 补「两种登录方式」章+「Session 管理」章
- 注册段加「首次可选设密码」

### Fixed · 验证码双轨不一致

- `auth.sendCode` 同时写 Redis + DB（之前只写 Redis）
- register / login / kyc / passwd 校验同时查 Redis 优先，fallback DB

## [1.0.11] - 2026-07-03

### Fixed · API 路径 v1 → api 对齐

- 6 个子脚本中 `/v1/auth/*` `/v1/channel` `/v1/profile` `/v1/company` `/v1/onboarding` 全部改为 `/api/auth/*` `/api/channel` `/api/profile` `/api/company` `/api/onboarding`
- 根因：后端真实路由在 `/app/api/...`，`/v1/...` 是 trpc REST 网关需要 Bearer token，register 走不到第 2 步

### Fixed · SKILL.md 注册定义补全

- 「MVP 必走两步」→「6 步交互式」（脚本实测 6 步）
- `agent.json` → `state.json`（与脚本一致）
- 补 `OPPHUB_HOME` 前置说明（wrapper 从 `$OPPHUB_HOME/bin/opphub-*` 加载）

## [1.0.10] - 2026-07-03

### Fixed · install.sh 路径纠正

- 1.0.9 猜路径 `/install.sh` → 404
- 实际路径 `/install/skill.sh` → HTTP 200, 1124 bytes
- 方式 2 URL 更正为 `https://api.opphub.ruiplus.cn/install/skill.sh`

## [1.0.9] - 2026-07-03

### Changed · 官方 install 脚本 URL 对齐

- frontmatter homepage 从 `https://github.com/mtty123456/opphub` 改为 `https://api.opphub.ruiplus.cn`
- 方式 2 从 npx 模式（1.0.8）改为偶合官方 install.sh 模式
- 命令：`curl -fsSL https://api.opphub.ruiplus.cn/install.sh | bash`
- 加 OpenClaw runtime 安全提示说明

### Note
- 后端域名拍板：`api.opphub.ruiplus.cn`（老板 11:39 拍）
- install.sh 路径待验证：当前 curl 该 URL 返回 404

## [1.0.8] - 2026-07-03

### Changed · 方式 2 重写

- 原“安装前自检”4 步 SOP 取消
- 新方式 2：“一行 curl/npx 装（无需预装 clawhub）”
- 适用场景：工具不认 clawhub CLI（codex / claudecode / 其他 agent 框架）
- 实际命令：`npx --yes clawhub@latest install @mtty123456/opphub`
- 前提：Node ≥ 22 + npm registry 可访问
- 经本地 npx 验证 --help 输出确认语法正确（`@owner/slug` 格式）

## [1.0.7] - 2026-07-03

### Changed · 方式 2 自检调整

- 重构为 4 步 SOP 思路，不再死翻 ClawHub 平台 prompt
- 1. 查元数据 → 2. 验依赖 → 3. 限范围 → 4. 严使用
- 删除与原问告述重复的“以上检查通过后”表述
- “严使用”步明确为对 agent 说话、不是对终端用户说话

## [1.0.6] - 2026-07-03

### Changed · 安装段重排

- “安装前自检”由原“方式 0”下调为“方式 2”
- 顺序：方式 1 ClawHub 商店 → 方式 2 安装前自检
- 两者都是“安装方式之一”，不划分为“必走”与“可选”

## [1.0.5] - 2026-07-03

### Removed · GitHub 源码安装方式

- SKILL.md / README.md 的"## 安装"段删除"方式 2 · GitHub 源码"整段
- 现在安装段只保留"方式 0 · 安装前自检（必走）"和"方式 1 · ClawHub 商店"
- 其他位置的 GitHub 链接（frontmatter homepage、安全报告、issue 反馈）保留

## [1.0.4] - 2026-07-03

### Added · 安装前自检（必走）

- 安装段顶部新增"方式 0 · 安装前自检（必走）"
- 中文翻译的 ClawHub 平台安装安全 prompt（8 句一一对应）
- 新增 `clawhub skill inspect` 验证命令，列出 owner / homepage / description 字段
- 强调"只基于 ClawHub 可验证元数据、不臆造依赖、范围外改动先问用户"
- README.md 同步加"方式 0"

## [1.0.3] - 2026-07-03

### 重构发布

- SKILL.md 全面精简：移除冗余的 first run 步骤、命令分级、反例清单
- 文档结构重整：核心命令 / 5 通道 / 错误码 / 安全披露 / 反馈 五段式
- README.md 同步重写：30 秒决策表 + 它能做什么 + 命令速查
- TRUST.md 同步重写：可信度表 + 数据与隐私 + 安全披露 + 机器可验证
- frontmatter license 备注移除
- frontmatter 描述保持 55 字符精简版

## [1.0.0] - 2026-07-03

### 首次发布

- OPC 账号体系（邮箱 / 手机号注册）
- 5 通道独立 IM 通知绑定：feishu / dingtalk / wecom / sms / email
- OPC profile（个人 / 公司 / 能力）
- 需求池 / 商机展示
- 撮合引擎入口（命令名 `opphub matches`）
- IM 推送查看
- First run 引导（`opphub status` → `register`）
- skill 自更新机制（`check-update` + `update`）
- ClawHub 元数据（categories / topics / homepage）
- README / CHANGELOG / TRUST / .clawhubignore

### 安全

- token 存 `~/.opphub/agent.json`，权限 `0600`
- GitHub Security Advisories 作为私下披露通道
- ClawHub 自动安全扫描 + VirusTotal
