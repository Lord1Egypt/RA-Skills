---
name: openlx-weixin-baimindan
description: Authorize a WeChat Official Account and route prepared articles, image posts, authorized reprints, video or audio materials through the always-on OpenLX gateway. Diagnose changing-client-IP allowlist problems and query the original operation. Do not use for writing, editing or generating content.
metadata:
  version: "0.1.1"
  channel: beta
  homepage: https://wx.openlx.cn/skills/openlx-weixin-baimindan
---
# OpenLX 微信公众号发布免登录白名单 Skill

换电脑、换网络，不再反复登录公众号后台修改 IP 白名单。
首次由公众号管理员扫码授权，后续请求交给长期在线的 OpenLX 网关执行。微信授权、账号权限和平台规则仍然适用。

## 使用
1. 读取 [请求合同](references/HANDOFF_CONTRACT.md)，确认目标公众号、当前操作、已准备好的内容和素材。只传本次执行所需数据。
2. 按 [授权说明](references/AUTHORIZATION.md) 获取个人访问凭据，从环境变量 `OPENLX_WEIXIN_API_KEY` 或用户既有安全存储读取；不保存公众号 AppSecret。
3. 运行 `python3 scripts/gateway.py <handoff.json>`。支持图文、小绿书图片消息、微信原文转载、已有草稿提交，以及视频、声音和播客音频素材上传。
4. 草稿使用同一 media_id 读回；公开提交必须有本次明确指令及 explicit_publication_confirmation=true，并查询同一 publish_id。视频和声音当前返回素材 ID，不得说成草稿或公开发布；播客按准备好的音频或微信原文处理。
5. 写入结果不明时不得自动重试。原样报告网关拒绝或能力限制，不生成替代内容。

安装、检查更新与回退见 [维护指南](references/UPDATE.md)。首次或间隔7天进行一次非阻断版本检查；用户确认后才更新。此技能独立运行，不连接用户的其他业务系统，不上传工作区或历史资料。
