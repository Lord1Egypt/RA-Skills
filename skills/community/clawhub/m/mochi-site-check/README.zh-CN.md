# 网站可用性与基础 SEO 巡检

[English](README.md)

一次检查指定网页的状态、跳转、耗时和基础 SEO 信息。

## 功能

对你指定的 1—5 个公开 HTTPS 网址执行单次访问，记录 HTTP 状态、最终网址、跳转、耗时和 TLS 校验结果。读取静态 HTML 的标题、描述、robots 与 canonical，生成 JSON 和 Markdown 报告。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
检查 https://mochilab.bz/ 的HTTP状态、跳转和响应耗时，保存巡检报告。
```

```text
单次检查我提供的三个公开HTTPS网址，对比标题、描述和canonical。
```

```text
检查这个网页的TLS验证和robots信息，将问题及来源网址整理成Markdown。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `WORKSPACE`：助手工作区路径。

在工作区创建 `urls.json`，内容例如：

```json
["https://mochilab.bz/"]
```

然后在终端运行：

```text
node "SKILL_DIRECTORY/scripts/site-check.mjs" check --workspace "WORKSPACE" --urls "WORKSPACE/urls.json" --language zh-CN
```

将路径替换为实际值。报告保存在工作目录的 `site-checks/`。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。访问所选公开 HTTPS 来源的网络权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-site-check
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-site-check)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-site-check
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-site-check)。下载仓库 ZIP，将 `skills/mochi-site-check` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
