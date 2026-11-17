# 请求合同

必需字段：target_account、requested_action、prepared_payload_or_reference（已解析的原始 JSON 对象）、user_intent。
payload.appid 必须与 target_account 一致。凭据从 OPENLX_WEIXIN_API_KEY 读取，HTTP 使用 x-api-key。

| 操作 | 输入 | 网关动作与结果 |
|---|---|---|
| CREATE_DRAFT | type=article/newspic/reproduce，is_draft=true | POST /v2/proxy/publish，返回草稿 media_id |
| SUBMIT_EXPLICIT_PUBLISH | type=article/newspic/reproduce/existing，is_draft=false，explicit_publication_confirmation=true | POST /v2/proxy/publish，返回 publish_id 后查询状态 |
| UPLOAD_MEDIA | type=video/voice，media_url，title（视频必需） | POST /v2/proxy/publish，返回微信永久素材 media_id；不是草稿或公开发布 |
| QUERY_STATUS | media_id 或 publish_id | /v2/proxy/draft-get 或 /v2/proxy/publish-status |
| CHECK_AUTHORIZATION | appid | /v2/proxy/draft-count，验证本次接口调用是否获准 |

图文 article：title、content（准备好的 HTML）、cover_media_id 或准备好的封面；可带 author、digest、content_source_url。
小绿书 newspic：title、content（纯文本）、images（有序素材 media_id 对象或现有网关支持的图片输入）。
微信原文转载 reproduce：title、source_url；仅处理用户有权转载的微信原文。
已有草稿 existing：media_id，使用明确发布操作。
视频 video：media_url、title、digest；声音 voice：media_url。播客音频使用 voice，微信公众号原文转载使用 reproduce；不抓取播客目录、不订阅转播、不下载未指定内容。

图片可以通过已有 /v2/proxy/upload 和 /v2/proxy/upload-permanent-images 接口直接上传到微信；已准备素材可以通过网关既有字段交接。不添加其他存储依赖。
本技能不进行写作、排版、素材生成或内容转换。只传本次操作需要的内容和素材，不附加内部流程字段、工作区文件或历史上下文。

素材上传成功只报告 MATERIAL_UPLOADED；微信公开发布必须查询原 publish_id 后确认。没有对应能力时返回限制，不把素材 ID 当作发布证明。超时返回 SUBMITTED_UNVERIFIED，不盲重试。
