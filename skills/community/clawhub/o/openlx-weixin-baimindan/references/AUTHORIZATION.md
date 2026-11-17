# 扫码授权

进入 https://wx.openlx.cn/account 登录，点击扫码绑定公众号，由公众号管理员完成授权。授权入口：https://wx.openlx.cn/account?authorize=1 。

从当前账号获取个人访问凭据，以环境变量 `OPENLX_WEIXIN_API_KEY` 供客户端使用。每次明确目标公众号 AppID，网关验证凭据与公众号的归属。
凭据不得写入请求示例、技能目录、安装状态或公开日志。客户不向智能体提供公众号 AppSecret。授权失效时返回用户中心重新扫码；不自动切换其他账号。
