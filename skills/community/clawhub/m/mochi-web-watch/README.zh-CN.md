# 网页变化订阅

[English](README.md)

订阅指定网页区域，保存基线、过滤无关变化，生成差异记录并接入定时检查与消息通知。

## 功能

订阅指定网页区域，保存基线、过滤无关变化，生成差异记录并接入定时检查与消息通知。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
订阅我提供的公告网址，只监测main区域，先保存基线并展示提取结果。
```

```text
检查这个订阅有没有变化，列出新增和删除内容，附上原网页链接。
```

```text
为这个订阅配置每小时检查，只在出现报名相关变化时通知当前聊天，完成后核对任务计划。
```

首次建立基线，后续保存新增与删除内容；定时任务和通知绑定当前助手及指定聊天账号。

## 运行要求

OpenClaw、已连接模型、当前工作区读写权限；Node.js 24.16+。定时检查需要 OpenClaw 原生调度和消息工具。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-web-watch
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-web-watch)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-web-watch
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-web-watch)。下载仓库 ZIP，将 `skills/mochi-web-watch` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
