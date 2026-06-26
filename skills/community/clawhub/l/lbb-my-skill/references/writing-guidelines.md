# 技术写作规范

## 文档结构

### 标题层级
- 使用清晰的标题层级（H1-H6）
- 每个文档只有一个 H1 标题
- 标题层级不跳级（H2 后面不直接跟 H4）
- 标题简洁明了，能概括内容

### 文档组织
```
# 文档标题 (H1)

## 概述 (H2)
简短介绍文档内容和目标读者

## 先决条件 (H2)
列出使用前需要的知识或准备工作

## 主要内容 (H2)
### 子主题 1 (H3)
### 子主题 2 (H3)

## 后续步骤 (H2)
引导读者进行下一步操作

## 相关资源 (H2)
提供相关文档链接
```

## 写作风格

### 清晰简洁
- 使用简单直接的语言
- 避免行话和复杂词汇
- 一个句子表达一个主要观点
- 避免冗长的从句

**示例：**
- ✓ "Click **Save** to save your changes."
- ✗ "In order to ensure that your modifications are properly persisted to the database, please proceed to click on the Save button located at the bottom of the form."

### 主动语态
- 优先使用主动语态
- 明确指出操作的执行者
- 使操作步骤更清晰

**示例：**
- ✓ "The system sends a confirmation email."
- ✗ "A confirmation email is sent by the system."
- ✓ "Click the button to start the process."
- ✗ "The process can be started by clicking the button."

### 现在时态
- 描述功能和行为时使用现在时
- 描述操作结果时使用现在时
- 仅在必要时使用将来时

**示例：**
- ✓ "The API returns a JSON response."
- ✗ "The API will return a JSON response."
- ✓ "When you click Save, the system stores your data."
- ✗ "When you click Save, the system will store your data."

### 第二人称
- 使用"you"直接与读者对话
- 避免使用"we"、"us"
- 创建更直接的交互感

**示例：**
- ✓ "You can configure the settings in the dashboard."
- ✗ "We can configure the settings in the dashboard."
- ✓ "To get started, you need to install the SDK."
- ✗ "To get started, one needs to install the SDK."

## 格式规范

### 代码和技术元素

#### 内联代码
使用反引号标记代码、命令、参数、文件名：
- 函数名：`functionName()`
- 参数：`--verbose`
- 文件路径：`/path/to/file`
- 变量：`userName`

#### 代码块
使用三个反引号和语言标识符：

```python
def example_function():
    return "Hello, World!"
```

#### 命令行
清楚标识命令提示符和输出：

```bash
$ npm install package-name
# Output:
added 1 package in 2.3s
```

### UI 元素标记

#### 按钮和菜单
使用粗体标记 UI 元素：
- 英文："Click **Save**."
- 中文："点击**保存**按钮。"

#### 导航路径
使用箭头或 > 符号：
- 英文："Go to **Settings** > **Security** > **Access Keys**."
- 中文："转到**设置** > **安全** > **访问密钥**。"

#### 输入字段
明确标识用户需要输入的内容：
- 英文："In the **Name** field, enter `my-project`."
- 中文："在**名称**字段中输入 `my-project`。"

### 列表

#### 无序列表
用于无特定顺序的项目：
- 使用破折号或星号
- 保持格式一致
- 每项首字母大写（英文）

#### 有序列表
用于步骤说明或有顺序要求的内容：
1. 第一步操作
2. 第二步操作
3. 第三步操作

#### 列表标点
- 如果列表项是完整句子，使用句号
- 如果列表项是短语或单词，可以不用标点
- 保持整个列表风格一致

### 链接

#### 内部链接
使用描述性文本：
- ✓ "See [Authentication Guide](./auth.md) for details."
- ✗ "Click [here](./auth.md) for more information."

#### 外部链接
明确标识外部资源：
- 提供完整的链接文本
- 考虑在括号中注明"外部链接"

### 图片和图表

#### Alt 文本
为所有图片提供有意义的 alt 文本：
```markdown
![Dashboard overview showing three main panels](dashboard.png)
```

#### 图片说明
在图片下方提供说明：
```markdown
![Dashboard screenshot](dashboard.png)
*Figure 1: Main dashboard with navigation menu*
```

## 提示和警告

### 标准格式

#### Note / 注意
用于补充信息或提示：

**Note:** This feature is available in version 2.0 and later.

> **注意**：此功能在 2.0 及更高版本中可用。

#### Important / 重要
用于重要信息：

**Important:** Back up your data before proceeding.

> **重要**：继续操作前请备份数据。

#### Warning / 警告
用于可能导致问题的操作：

**Warning:** This action cannot be undone.

> **警告**：此操作无法撤销。

#### Tip / 提示
用于最佳实践或建议：

**Tip:** Use keyboard shortcuts to improve efficiency.

> **提示**：使用键盘快捷键可提高效率。

## 操作步骤

### 步骤编写原则
- 每个步骤一个操作
- 使用祈使句
- 包含预期结果
- 按逻辑顺序排列

### 步骤格式

**基本格式：**
1. Open the application.
2. Click **New Project**.
3. Enter a project name.
4. Click **Create**.

**包含说明的格式：**
1. **Open the application**: Launch the app from your desktop or taskbar.
2. **Create a new project**: Click **New Project** in the toolbar.
3. **Configure settings**: Enter the following information:
   - **Name**: Your project name
   - **Location**: Where to save the project
4. **Finish setup**: Click **Create** to complete the process.

### 条件步骤
明确标识可选或条件性步骤：

**If you want to enable advanced features:**
1. Click **Advanced Settings**.
2. Select the features you need.
3. Click **Apply**.

## API 文档规范

### 端点描述
```markdown
### Get User Profile

Retrieves the profile information for a specific user.

**Endpoint:** `GET /api/v1/users/{userId}`

**Parameters:**
- `userId` (string, required): The unique identifier of the user

**Response:**
- **200 OK**: Returns user profile object
- **404 Not Found**: User does not exist

**Example Request:**
```bash
curl -X GET https://api.example.com/v1/users/12345 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response:**
```json
{
  "id": "12345",
  "name": "John Doe",
  "email": "john@example.com"
}
```
```

### 参数文档
- **名称**：参数名称
- **类型**：数据类型（string, number, boolean 等）
- **必需性**：required 或 optional
- **描述**：简短说明参数用途
- **默认值**（如适用）
- **示例**（如适用）

### 错误代码
列出所有可能的错误响应：

**Error Responses:**
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource does not exist
- `500 Internal Server Error`: Server error

## 代码示例

### 示例原则
- 提供完整可运行的示例
- 包含必要的注释
- 使用真实场景
- 展示最佳实践

### 多语言支持
为不同语言提供示例：

**Python:**
```python
import requests

response = requests.get('https://api.example.com/v1/users/12345')
user = response.json()
print(f"User name: {user['name']}")
```

**JavaScript:**
```javascript
const response = await fetch('https://api.example.com/v1/users/12345');
const user = await response.json();
console.log(`User name: ${user.name}`);
```

### 注释风格
- 英文代码注释使用英文
- 中文文档中的代码注释使用中文
- 注释解释"为什么"而不是"是什么"

## 表格

### 表格使用
- 用于结构化数据展示
- 用于参数列表
- 用于对比信息

### 表格格式
```markdown
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userId | string | Yes | User identifier |
| includeDetails | boolean | No | Include detailed info |
```

### 表格对齐
- 左对齐：文本内容
- 右对齐：数字
- 居中对齐：状态标识

## 版本和弃用

### 版本说明
标识功能的适用版本：

**Added in v2.0:** This feature was introduced in version 2.0.

> **2.0 版本新增**：此功能在 2.0 版本中引入。

### 弃用通知
清楚标识已弃用的功能：

**Deprecated:** This method is deprecated as of v3.0. Use `newMethod()` instead.

> **已弃用**：此方法自 3.0 版本起已弃用。请改用 `newMethod()`。

## 可访问性

### 无障碍写作
- 使用清晰的语言
- 提供替代文本
- 确保颜色不是唯一的信息传达方式
- 使用语义化的标题结构

### 国际化考虑
- 避免文化特定的引用
- 使用国际日期格式（YYYY-MM-DD）
- 明确时区信息
- 避免俚语和习语

## 质量检查清单

写完文档后，检查以下项目：

**内容：**
- [ ] 目标读者明确
- [ ] 信息准确完整
- [ ] 步骤可重现
- [ ] 示例可运行

**结构：**
- [ ] 标题层级正确
- [ ] 逻辑流程清晰
- [ ] 章节组织合理

**格式：**
- [ ] 代码正确标记
- [ ] UI 元素使用粗体
- [ ] 链接描述清晰
- [ ] 图片有 alt 文本

**语言：**
- [ ] 使用主动语态
- [ ] 使用现在时态
- [ ] 术语一致
- [ ] 拼写和语法正确

**可用性：**
- [ ] 导航便利
- [ ] 搜索友好
- [ ] 移动端友好
