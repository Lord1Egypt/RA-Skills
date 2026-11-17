# SerpApi (Google Search) node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `SerpApi (Google Search) node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.toolserpapi`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the SerpApi (Google Search) node in n8n. Follow technical documentation to integrate SerpApi (Google Search) node into your workflows.

## 关键操作 / 参数线索

- Node options
- Templates and examples
- Related resources

## 常用选项线索

- **Country**: Enter the country code you'd like to use. Refer to Google GL Parameter: Supported Google Countries for supported countries and country codes.
- **Device**: Select the device to use to get the search results.
- **Explicit Array**: Choose whether to force SerpApi to fetch the Google results even if a cached version is already present (turned on) or not (turned off).
- **Google Domain**: Enter the Google Domain to use. Refer to Supported Google Domains for supported domains.
- **Language**: Enter the language code you'd like to use. Refer to Google HL Parameter: Supported Google Languages for supported languages and language codes.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

