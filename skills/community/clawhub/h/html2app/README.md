# html2app

将本地 HTML/CSS/JavaScript 网页或已构建的前端项目打包为可离线运行的 Electron 桌面应用。适合需要交付 macOS `.app` / `.dmg` / `.zip` 或 Windows `.exe`，但不希望部署服务器的场景。

## 能做什么

- 打包单个 HTML 文件、多个静态页面，或 Vite / React / Vue 等项目的生产构建产物
- 生成安全的 Electron 壳：默认启用 `contextIsolation`、`sandbox`，并禁用 `nodeIntegration`
- 为没有品牌素材的项目生成默认应用图标
- 支持 SQLite 本地数据：数据库写入 Electron `userData` 目录，不写入应用包
- 识别 CDN、远程 API、OAuth、localhost companion service 等会影响离线交付的依赖
- 生成 macOS 缓存 Electron 运行时的兜底包，并提供回归用例

## 使用方式

将本目录安装到 Codex skills 目录，例如：

```bash
git clone https://github.com/wink-run/html2app.git ~/.codex/skills/html2app
```

然后在 Codex 中使用：

```text
使用 $html2app 将当前本地网页打包成 macOS 应用。
```

或：

```text
使用 $html2app 将这个多页面项目打成 Windows 和 macOS 安装包，并使用 SQLite 做离线存储。
```

## 打包流程

1. 检查网页入口、构建命令以及外部依赖。
2. 对框架项目执行生产构建；静态项目直接使用本地页面和资源。
3. 创建最小 Electron 主进程和受限 preload API。
4. 配置默认图标、应用 ID、目标架构与安装包类型。
5. 构建并检查产物、签名状态和数据持久化。

## 多页面与 SQLite

多页面静态站点可通过 Electron 的 `loadFile` 与普通相对链接运行。

SQLite 必须在 Electron 主进程中访问，并保存到：

```js
path.join(app.getPath('userData'), 'app.sqlite')
```

不要将 SQLite 数据库放在 `Contents/Resources` 或渲染层目录，也不要向页面暴露任意 SQL。应通过 preload 暴露有限的、已校验的业务操作，例如 `task:list`、`task:add`。

## 图标和签名

未提供品牌图标时，skill 会生成默认高对比度图标：

- macOS: `.icns`
- Windows: 需提供或转换为 `.ico`

本地临时签名只用于验证应用包完整性。正式分发仍需要：

- macOS: Apple Developer ID 签名与 notarization
- Windows: 代码签名证书

没有公证的 macOS 应用可能被 Gatekeeper 拦截；不要绕过系统安全机制。

## 测试

运行内置回归检查：

```bash
./scripts/run_fixture_checks.sh
```

覆盖的场景包括：

- 多静态页面和本地资源
- 本地持久化数据
- 远程后端依赖检测

更完整的验收标准见 [references/test-cases.md](references/test-cases.md)。

## 目录结构

```text
SKILL.md                         # Codex 工作流
agents/openai.yaml               # Skills UI 信息
scripts/                         # 检查、图标、缓存运行时打包、回归脚本
references/                      # 平台矩阵与验收用例
```

## 重要限制

本地打包不等于自动离线化。依赖远程 API、OAuth、CDN 资源、服务器数据库或密钥的项目，仍必须明确网络可用性、凭据存储与离线体验后再交付。
