# 仓库规范与数据安全准则 (AI Agent Rules)

## 1. 核心属性：公开开源代码库
- 本项目 `01_projects/mpress` 是托管在 GitHub 上的开源公共项目（仓库 https://github.com/shxuk/mpress ，旧名 wechat-article-publisher）。
- 严禁在此仓库内创建、存放任何用户的私人文章内容、草稿正文、私密配图或个人凭据（如 AppID / AppSecret）。

## 2. 数据与凭证隔离机制
- 个人运行凭据位于：`Y:/06_services/mpress/credentials`。
- 运行生成的产物（HTML、图片缓存、drafts 状态）必须统一存放于：`Y:/06_services/mpress/work`。
- 本地环境配置文件 `.env` 已被 `.gitignore` 忽略，仅用于桥接外部服务目录，严禁提交到远端仓库。

## 3. Git 操作防御守则
- 严禁在未经用户明确要求和审查的情况下擅自执行 `git push`。
- 执行 `git add` 前必须先执行 `git status` 严格审查待提交文件，禁止盲目全量提交。
