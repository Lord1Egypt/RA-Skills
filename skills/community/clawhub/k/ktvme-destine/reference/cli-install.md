# CLI 安装与校验

⚠️ This step installs and executes external code from npm. Only proceed if you trust the package source.

## 前置条件

- `npm` 命令可用
- `npm config set registry https://registry.npmjs.org/`
- `@ktvme/km-bot` CLI 工具已安装。**优先检测本地是否已安装**：先执行 `which km-bot`，如已存在则跳过安装

## 客户端运行时要求

**客户端只需 Node.js，无需安装任何 npm 包**

| 项目         | 要求                                 |
| ------------ | ------------------------------------ |
| Node.js 版本 | `>= 14.0.0`（推荐 `16.x` 或 `18.x`） |
| 磁盘空间     | ~50KB（只有编译后的字节码）          |
| 网络         | 需要（调用 API）                     |

**发布产物分析**（根据 `package.json` 的 `files` 字段）：

```
node_modules/.bin/km-bot → bin/cli.cjs
node_modules/@ktvme/km-bot/dist/bundle.jsc  ← 所有依赖已打包
```

**验证安装**：

```bash
km-bot --version   # 应该输出版本号
km-bot --help      # 应该显示帮助
```

## 来源说明

`@ktvme/km-bot` 是 KTV 行业 SaaS 服务通信工具，由 `K米` 官方维护。npm 的 `@ktvme` 是官方 scoped package 命名空间。

## 安装流程（未安装时执行）

### 0. 用户确认（安装前必须执行）

- 即将安装的外部包：`@ktvme/km-bot`（npm 官方包）
- 安装方式：`npm install -g @ktvme/km-bot`（全局安装）
- 安装后会提供 `km-bot` CLI 工具
- 如用户不同意，终止流程并提示用户可手动安装

### 1. 完整性校验（必须先于安装执行）

```bash
npm view @ktvme/km-bot dist.integrity
```

**校验失败处理**：如果哈希值不匹配或 `npm view` 命令失败，**立即终止安装**，向用户报告"包完整性校验失败，禁止安装"。

### 2. 安装（仅在校验通过后执行）

```bash
npm install -g @ktvme/km-bot
```

> 使用 `-g` 全局安装，以便在任意目录使用 `km-bot` 命令。

---

## km-bot 使用说明

### 命令格式

```bash
km-bot --help
km-bot call <category> <method> "<json>"
km-bot call <category> <method> "<json>" --account <accountId>
```

> ⚠️ **JSON 参数必须使用双引号包裹**，内部双引号需转义。详见下方"km-bot 命令参数格式要求"章节。

### km-bot 命令参数格式要求

⚠️ **跨平台兼容性重点**：JSON 参数在不同操作系统中的引号处理方式不同，请务必遵循以下规范：

#### 单引号 vs 双引号

| 操作系统  | Shell 类型 | 单引号 `'`                       | 双引号 `"` |
| --------- | ---------- | -------------------------------- | ---------- |
| Linux/Mac | bash/zsh   | 原样保留                         | 变量展开   |
| Windows   | CMD        | 原样保留（**不识别为特殊字符**） | 原样保留   |
| Windows   | PowerShell | 原样保留                         | 变量展开   |

**结论**：Windows CMD 不识别单引号为字符串定界符，因此 **必须使用双引号包裹 JSON**，并在 JSON 内部的双引号前加转义符。

#### 正确格式（跨平台通用）

```bash
# ✅ 正确格式：外层双引号 + 内层转义双引号
km-bot call saasktv searchCompany "{\"keyword\":\"NEO KTV\"}"

# ❌ 错误格式：外层单引号（Windows CMD 不兼容）
km-bot call saasktv searchCompany '{"keyword":"NEO KTV"}'
```

#### 快速判断方法

生成的命令应满足：**在任何终端中直接粘贴执行都能成功**。

---

### 调用示例

```bash
# ✅ 推荐格式（跨平台兼容）
# 预订相关接口（saasktv 类别）
查询门店列表： km-bot call saasktv searchCompany "{\"keyword\":\"NEO KTV\"}"
切换当前门店： km-bot call saasktv switchCompany "{\"company_code\":\"01171\"}"
查询可预订情况： km-bot call saasktv queryRoomAvailability "{\"company_id\":1265,\"use_date\":\"2026-07-31\",\"begintime\":\"2026-07-31 17:00:00\",\"endtime\":\"2026-07-31 19:00:00\"}"
创建订单： km-bot call saasktv roomHourCreateOrder "{\"roomid\":62,\"begintime\":\"2026-07-31 17:00\",\"endtime\":\"2026-07-31 18:00\",\"id\":1001,\"source\":7,\"charge\":\"10\",\"protocolcharge\":\"10\"}"
# 创建订单成功后直接返回 payment_link / qr_code / expire_time，无需调用独立支付接口
查询登录状态： km-bot call saasktv sessionInfo "{}"
发送验证码： km-bot call saasktv sendVerifyCode "{\"phone\":\"13800138000\"}"
验证码登录： km-bot call saasktv loginByCode "{\"phone\":\"13800138000\",\"verify_code\":\"123456\"}"
# 指定账号调用（使用 --account 参数）
km-bot call saasktv searchCompany "{\"keyword\":\"NEO KTV\"}" --account xxx@wechat.im
```

---

### 适用场景

本技能（km-destine）通过 km-bot 调用 **saasktv** 类别完成全部流程：

| 类别 (category) | 说明                                                    | API 文件                                                                            |
| --------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `saasktv`       | KTV 预订完整流程接口（门店/包厢/订单/登录等，下单即返回支付信息） | api-store.md, api-room.md, api-order.md, api-session.md |

### 账号格式

| 类型 | 格式             | 示例              |
| ---- | ---------------- | ----------------- |
| 微信 | `openid@wechat`  | `oxxxxxx@wechat`  |
| 飞书 | `user_id@feishu` | `xxxxxxxx@feishu` |
| KM   | `user_id@km`     | `123456@km`       |

### 环境变量

| 变量         | 说明     | 默认值 |
| ------------ | -------- | ------ |
| `KM_ACCOUNT` | 默认账号 | -      |

---

## 校验失败处理

安装或校验过程中如遇错误，按以下等级处理：

| 错误类型                       | 处理方式                   |
| ------------------------------ | -------------------------- |
| 完整性校验失败                 | **立即终止**，禁止安装     |
| 网络错误（npm 无法访问）       | 提示用户检查网络或手动安装 |
| 安装失败                       | 提示用户手动执行安装命令   |
| 已安装但 `which km-bot` 找不到 | 提示用户检查 PATH 配置     |
