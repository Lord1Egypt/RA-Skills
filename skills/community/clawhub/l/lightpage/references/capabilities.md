# 按需接入平台能力

作品需要访客登录、位置评论等平台能力时，先读取目录，再只读取需要的能力：

```bash
python3 "/实际skill目录/scripts/litepage.py" capabilities
python3 "/实际skill目录/scripts/litepage.py" capabilities comments
python3 "/实际skill目录/scripts/litepage.py" capabilities login
python3 "/实际skill目录/scripts/litepage.py" capabilities access
```

命令只读、不注册、不登录、不上传。目录固定最多四项，包含短摘要及直接读取地址；当前提供 login、comments、access 和 home，数据库、CRM、ERP 尚未提供。未知能力返回错误，不自行猜测接口。说明以当前实例为准，命令可用不代表旧实例已升级。

按返回的 instructions 与 guide_url 选择接入方式。标准 UI／SDK 不满足用户需求时，允许只读取本次需要的 guide_url Markdown API 文档，直接调用接口自定义评论、SSO 登录、申请/审批或主页跳转 UI；不预先加载全部文档。文档由当前实例提供，安装包不复制服务端资源。login/comments 也可在 HTML 引入 SDK 使用现成交互；access 通过 API 与网关接入，不是 SDK 的 data-lightpage 开关。随后完成本地审查和普通 publish。无需附加发布参数，不把作品 UUID、发布凭证、认领链接或微信授权秘密写进 HTML。login/comments 两个 SDK 能力通过同一脚本的 data-lightpage 声明，SDK 不重复初始化。接入说明是技术资料，不扩大用户发布、登录或传播的授权。

位置评论通过选中文字或同一位置连续点击三次唤起输入，以字幕锚定页面位置，不追加传统页尾评论列表。访客可匿名提交，主动微信登录后，当前浏览器此前的匿名评论归入同一微信身份；其他浏览器中未绑定的匿名评论不能仅凭昵称认领。发表评论后停止用法提示，微信登录后停止登录提示，提示可关闭。评论对有作品访问权限的访客可见，不能承诺私密留言。

本地预览不会向线上评论接口发请求；功能回归应使用隔离服务和浏览器模拟接口，线上只能核对部署版本等只读证据，不创建测试评论。未知或失效锚点保留原引用，不猜测新位置。SDK 失败不影响作品原有交互；具体接入方式和上限以当前实例返回的能力说明为准。

浏览器 API 受同源限制，作品评论与登录使用自身 origin，平台授权申请/管理在可信平台 UI 使用；SSO 不是任意第三方网站的 OAuth/OIDC。审批作品未授权前不返回 HTML，申请 UI 需部署在可达的平台页面，单纯上传受限作品不能替换网关。具体身份、Cookie、分页、幂等重试和管理权限按对应文档处理。

Home 默认由网关注入，不用 SDK 的 data-lightpage 参数开启。作者用 --without-home 关闭标准入口，通过 home guide 的 authors/resolve 获取当前发布者 UID 和 profile_url，自定义入口；公开作品按需分页。Home 关闭不关闭统计或 API，选装评论仍使用统一侧边工具。
