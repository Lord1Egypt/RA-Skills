# XML

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `XML` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.xml`
- node group: `core-nodes`

## 核心要点

- Documentation for the XML node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Mode**: The format the data should be converted from and to.
- **JSON to XML**: Converts data from JSON to XML.
- **XML to JSON**: Converts data from XML to JSON.
- **Property Name**: Enter the name of the property which contains the data to convert.

## 常用选项线索

- **Attribute Key**: Enter the prefix used to access the attributes. Default is `$`.
- **Character Key**: Enter the prefix used to access the character content. Default is `_`.
- **Allow Surrogate Chars**: Set whether to allow using characters from the Unicode surrogate blocks (turned on) or not (turned off).
- **Cdata**: Set whether to wrap text nodes in `` instead of escaping when it's required (turned on) or not (turned off).
- Turning this option on doesn't add `` if it's not required.
- **Headless**: Set whether to omit the XML header (turned on) or include it (turned off).
- **Root Name**: Enter the root element name to use.
- **Explicit Array**: Set whether to put child nodes in an array (turned on) or create an array only if there's more than one child node (turned off).
- **Explicit Root**: Set whether to get the root node in the resulting object (turned on) or not (turned off).
- **Ignore Attributes**: Set whether to ignore all XML attributes and only create text nodes (turned on) or not (turned off).

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

