# 文件整理规划与重复报告

[English](README.md)

扫描指定目录，生成文件分类方案和基于 SHA256 的重复文件报告。

## 功能

读取指定目录，用文件大小和 SHA256 识别相同文件，按扩展名生成分类建议，处理同名文件的目标路径。输出 `plan.json` 和 `report.md`，供你查看整理方案；原文件保持原位。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
扫描我指定的下载目录，按扩展名生成分类方案，先展示目标路径。
```

```text
检查这两个目录里的重复文件，用SHA256核对，生成重复报告。
```

```text
为这些同名文件生成不冲突的目标名称，保存plan.json和report.md供我查看。
```

## 高级用法：在终端手动运行

下面是开发者手动运行命令。在安装 OpenClaw 的电脑或服务器终端执行；日常使用直接发送上面的对话示例即可。

先把命令中的占位名称换成实际路径：

- `SKILL_DIRECTORY`：已安装的这个Skill文件夹。
- `INPUT_DIRECTORY`：要扫描的目录。
- `NEW_REPORT_DIRECTORY`：新建的报告目录。

也可直接运行：

```text
node "SKILL_DIRECTORY/scripts/organize.mjs" --root "INPUT_DIRECTORY" --out "NEW_REPORT_DIRECTORY"
```

将路径替换为实际目录，报告目录放在扫描目录之外。包内 `samples/sample-input` 可用于初次练习。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+ 或 26.1+，以及本地命令和工作目录读写权限。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-file-organizer
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-file-organizer)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-file-organizer
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-file-organizer)。下载仓库 ZIP，将 `skills/mochi-file-organizer` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。

