# 教程：用 mubu-integration 把幕布变成你的本地 Markdown 知识库

## ① 为什么要把幕布变成 Markdown
幕布适合梳理大纲，但搜索弱、难备份、不易进 Obsidian 等知识管理工具，更没法让 AI 直接读。mubu-integration 解决这三件事：一键全量备份、进 Obsidian、给 AI 当长期记忆。

## ② 5 分钟配置凭据
密码不进命令行。用环境变量或仓库外文件：
```bash
export MUBU_PHONE=你的手机号
export MUBU_PASSWORD=你的密码
# 可选：仅 save 写回需要
# export MUBU_MEMBER_ID=你的幕布 colla 成员 ID
```
或写入 `~/.workbuddy/.env.mubu`（脚本自动加载，权限 0o600）。

## ③ 一键把整本幕布导出为本地备份
```bash
python3 scripts/mubu_api.py export-tree --folder <根文件夹id> --output ./backup
```
每个文档写成 `<名称>.md`，子文件夹生成同级目录，递归整树。单点失败不中断，记入统计。

## ④ 在 Obsidian 里管理这些大纲
把 `./backup` 作为 Obsidian 仓库的笔记目录，大纲即普通 Markdown，双向链接、全文搜索、图谱视图都能用。

## ⑤ 让 AI Agent 直接读 / 写你的幕布
作为 Agent Skill 接入后，让 AI「把这份大纲导出」「读我的周会文档」即可。注意：`save` 写回需要 `MUBU_MEMBER_ID`（幕布服务端限制，任何 API 都不返回，需手动设置），缺失时 `save` 会明确报错，不影响读取 / 导出。

## ⑥ 常见问题
- 非官方逆向，服务端可能调整接口；某端点失效以抓包为准并反馈 Issue。
- `save` 报 code 17 / memberId → 设置 `MUBU_MEMBER_ID`。
- 更多见项目 README 的 Troubleshooting。
