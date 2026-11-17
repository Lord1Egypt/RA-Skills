# lan-knowledge-share

一键将本地文件目录部署为局域网可访问的 Web 知识库，开启 HTTP 服务实现局域网内知识共享。

- 任意目录即知识库：Markdown / Excel/CSV 表格 / HTML 报告 / 图片 / 音视频混合内容开箱即用
- 动态侧边栏（文件夹名单击展开/收起、双击进入目录页）、自动目录页、图片画廊（键盘切换）、表格在线预览、HTML 报告就地查看、全站全文搜索（含 HTML 报告正文）
- 目录增删改实时生效，刷新即更新，无需建库、无需预生成配置
- 内容目录**零写入**：不生成 README 或任何站点文件，不修改你的任何数据
- 零第三方依赖（仅需 Node.js 12+）

## 语言与内置依赖说明 · Locale & Bundled Libraries

- **语言/区域**：本技能面向中文使用者，界面文案、运行日志与源码注释**有意默认使用简体中文**（`SKILL.md` 元数据 `locale: zh-CN`，且每个源文件头部均带 `Locale: zh-CN` 声明），关键说明附英文对照。这是显式声明的设计取向，如需其他语言界面，直接修改 `assets/runtime/` 内的文案与注释即可，功能不受影响。
  (This skill targets Chinese-speaking users; UI text, logs and comments intentionally default to Simplified Chinese — declared in SKILL.md metadata and in a `Locale: zh-CN` header atop every source file — with English paraphrases. Replace the copy under `assets/runtime/` to localize; behaviour is unaffected.)
- **内置前端库**（均为上游官方发行版原样拷贝，仅在浏览器本地运行，无网络外发/遥测）：docsify、docsify-zoom-image、marked、mammoth.js、SheetJS、Prism、vue.css。完整清单、上游地址、许可证与每个文件的 SHA-256 校验值见 `assets/runtime/assets/vendor/THIRD-PARTY.md`。

## 安全与隐私 · 使用前必读

> ⚠️ **本服务无鉴权**：启动后，局域网内任何可达设备都能打开链接浏览所选目录，无需登录。

- **只分享范围受限、仅含拟共享文件的子目录**；切勿将家目录、代码仓库、含密钥/凭据/内部报告/个人数据的目录交给本工具发布。HTTP 暴露是单向广播式的，删除文件前页面/链接无法即时回收。
- 服务仅监听局域网（默认 `0.0.0.0`），地址离开本网段即不可达；**不要把局域网地址转发到公网**或不可信的公共网络。
- Windows 首次启动会弹出防火墙授权，建议仅勾选「专用网络」（不要勾选公用网络），降低暴露面。
- 内容目录始终只读共享（零写入）；如需自定义首页，在内容目录自行创建 `README.md` 即可。

## 目录结构

```
lan-knowledge-share/
├── SKILL.md                 # 技能定义（触发说明与使用流程）
├── scripts/
│   └── deploy.js            # 一键部署入口（node deploy.js <目录> [选项]）
├── assets/
│   └── runtime/             # 内置前端运行时（index.html 模板 + assets）
└── references/
    └── skillhub-listing.md  # SkillHub 网页发布表单填写模板
```

## 快速开始

```
node scripts/deploy.js "<要分享的目录>" -n "站名" -p 8089
```

启动后按终端提示把局域网地址（http://<IP>:<端口>）发给同事即可访问。`node scripts/deploy.js --help` 查看全部选项。

## 部署形态

- **纯内容目录**（根目录无 index.html）：运行时注入，内容目录零写入、不落任何站点文件；根目录无 README 时由服务端在内存渲染温和默认首页（`--no-readme` 可改为纯目录索引页）
- **自包含知识库**（已有 index.html+assets）：按原站点逻辑托管

## 发布到 SkillHub

如需把本技能发布/更新到社区（skillhub.cn / clawhub.ai 等），**请通过官方渠道获取并安装 CLI，不要直接执行「从网络管道下载的脚本」**：

1. 安装 CLI：到官网（skillhub.cn → 个人设置）下载官方安装包/命令行工具，或用包管理器安装；安装前先查看安装脚本内容确认来源与意图。Windows 用户见官网安装指引。
2. `skillhub login` 完成登录与实名认证
3. `skillhub init --name lan-knowledge-share --category 知识管理`（或直接在官网网页发布）
4. `skillhub push` 上传文件，`skillhub publish` 提交审核

网页发布可参考 `references/skillhub-listing.md` 的表单文案。
