# Security Policy

## 不要提交的内容

- API key、访问令牌、私有网关地址
- 真人照片、个人音频、聊天截图
- 未公开的商业素材、客户名称、内部项目代号

本仓库的 `.gitignore` 已默认忽略：

- `scripts/config.json`
- `scripts/material-uploader/config.json`
- `assets/output/`（生成的项目目录）
- `.env`

## 如果密钥误提交

1. **先轮换密钥**，再处理仓库。删除提交不能撤回已经泄露的凭证。
2. 用 `git filter-repo` 或 GitHub 的 secret scanning 清理历史。
3. 检查 fork、Actions 日志、Release 附件、Issue 评论里是否还有副本。

## 报告问题

请通过仓库的 **Security → Report a vulnerability**（GitHub Security Advisory）私下报告，不要在公开 Issue 里贴密钥、素材链接或可复现的私有地址。

## 使用边界

- 上传到公网的素材是公开可访问的，不要上传身份证、私密照、聊天记录。
- 真人图片需取得本人授权；不影射在世公众人物、明星、IP、品牌。
- 不克隆可识别真人的声音；不下载、不翻唱受版权保护的歌曲。
- 对外发布请标注 AI 生成。
