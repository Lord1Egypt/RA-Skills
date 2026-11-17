---
name: oia-skill
description: 使用 oia 框架（npm 包 @oia-ai/oia-fresh）初始化 Deno + Fresh Web 项目。当用户要求「创建 oia 项目」「初始化 oia / oia-fresh」「用 oia 框架搭一个应用」时触发。完成 Deno 环境检查、npx @oia-ai/oia-fresh init 脚手架、启动开发服务器并验证的完整流程。
---

# 初始化 oia 框架项目

oia 框架以 `@oia-ai/oia-fresh` 为名发布在 npm 仓库，初始化命令为 `npx @oia-ai/oia-fresh init`。
生成的项目基于 **Deno + Fresh 2（Vite 构建）**，开发服务器端口为 **5173**。

本 skill 自身也发布为 npm 包 `@oia-ai/oia-skill`，安装方式：

```bash
npx -y @oia-ai/oia-skill           # 安装到当前项目
npx -y @oia-ai/oia-skill --global  # 安装到用户目录（所有项目可用）
```

## 标准流程

### 1. 环境检查

- `deno --version`：要求 Deno 2.x。未安装时引导安装：
  - Windows：`winget install Denoland.Deno`
  - macOS / Linux：`curl -fsSL https://deno.land/install.sh | sh`
- `npx --version`：确认 Node / npx 可用（仅用于执行 init 脚本，项目运行不依赖 Node）。

### 2. 生成脚手架

在期望放置项目的父目录下执行：

```bash
npx -y @oia-ai/oia-fresh@latest init <项目名>
```

注意事项：

- 目标目录已存在且非空时，先和用户确认处理方式（当前文件夹 / 换目录名）；选择「当前文件夹」时改用 `npx -y @oia-ai/oia-fresh@latest init .` 在当前目录直接释放模板（不删除已有文件，仅写入/覆盖模板文件，`.git` 等一律保留）。
- 连不上 npm registry 时，先探测本地代理常见端口（7890 / 7897 / 1080 / 10809），命中后以
  `npm_config_proxy=http://127.0.0.1:<端口> npm_config_https_proxy=http://127.0.0.1:<端口> npx ...` 重试。

### 3. 启动并验证

```bash
cd <项目名>
deno task dev   # 后台启动
```

轮询 `http://127.0.0.1:5173/` 直到返回 HTTP 200，确认页面内容正常后停掉后台服务器，向用户汇报验证结果。

### 4. 收尾（按用户需要进行）

- git init / 提交：不直接向默认分支提交，先建特性分支。
- 告知用户日常命令：开发 `deno task dev`；生产 `deno task build` 后 `deno task start`。

## 常见坑

- 开发端口是 **5173**（Vite），不是 Fresh 1.x 的 8000，别验错端口。
- Deno 首次运行自动拉取依赖并生成 `deno.lock`；`deno.json` 使用 `nodeModulesDir: manual`，不要手动删除 `node_modules/`。
- Windows 下 git 的 LF/CRLF 警告可忽略。
- 直连 github.com / registry 被重置时，优先怀疑网络问题并走本地代理（见第 2 步）。
