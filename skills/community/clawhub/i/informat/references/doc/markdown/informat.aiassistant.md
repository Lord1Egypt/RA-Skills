<!-- DOCKEY: aia-7a2c6 -->
This document is the AI Assistant module documentation for the Informat low-code platform.

## Overview

The AI Assistant integrates multiple large language models, allowing quick switching and usage of different language models through simple configuration. While fully leveraging the advantages of large language models, the AI Assistant also supports deep interaction with the system through custom plugins, enabling more complex assistants that better fit actual usage scenarios.

:::tip AI Agent
**_Automation includes steps for calling the AI Assistant. Automation combined with the AI Assistant can implement complex AI agents._**
:::

## Configuration

### Basic Settings

On the basic settings page, you can name the AI Assistant, select an icon and icon color, and write a description.

- **Name**: Set the name of the AI Assistant. For example: "GPT"
- **Icon**: Select an icon to represent your AI Assistant.
- **Icon Color**: Select the icon's background color to distinguish different models.
- **Description**: Briefly describe the function and purpose of the AI Assistant. For example: "I am a large language model developed by OpenAI. I can help you answer questions."

### Scenario Guided Questions

You can preset some common questions and the language model's response strategies to help users quickly understand and use the model.

- **Input Placeholder**: Enter placeholder text, for example: "Enter your question"
- **Add Question**: Click the "Add" button to add common questions and their brief descriptions. For example:
  - "How to plan your life" (6/200 characters)
  - "Help me write a resume" (9/200 characters)

![Basic Settings](images/base-setting.png)

### Q&A Logic Settings

In the persona and response logic settings, you can define the model's response strategy.<br />
For example: "You are an office assistant who needs to answer questions based on user inquiries. When a user asks a question that requires thinking, think step by step, and after you have organized your thoughts, call external tools."<br/>
In this way, the AI Assistant will follow the configured [Persona and Response Logic] to act as an office assistant, calling external tools only after thorough deliberation.

#### Writing Recommendations

To achieve a better experience with the AI Assistant, it is recommended to include the following in your prompts:

- **Define the Persona**: Describe the role or responsibilities of the AI Assistant and the response style. <br />For example: You are a project management assistant who needs to accurately answer questions based on user inquiries.
- **Describe Functions and Workflow**: Describe the AI Assistant's functions and workflow, specifying how the AI Assistant should respond to user questions in different scenarios.
  <br />For example: `When a user queries a task by its code, call the "get_task_by_code" tool to look up the task.`
  <br />Although the AI Assistant will automatically select plugins based on the prompt content, it is still recommended to explicitly specify which tool to call in which scenario through natural language to improve constraint on the AI Assistant and ensure more accurate responses by selecting the expected plugin.
  <br />For example: `When a user asks about the latest unfinished tasks of ongoing projects, call "get_projects" to search for ongoing projects, then call "get_tasks" to query unfinished tasks of ongoing projects, and finally organize all the data for the user.`
  <br />Additionally, you can provide response format examples for the AI Assistant. The AI Assistant will mimic the provided response format when replying to users.
  <br />For example:

```md
Please follow this format for responses:
**Task Name**
Start Time: yyyy-MM-dd hh:mm
End Time: yyyy-MM-dd hh:mm
Task Description: Task description within 20 characters
```

- **Instruct the AI Assistant to Answer Within a Specified Scope**: If you want to limit the response scope, directly tell the AI Assistant what it should and should not answer.
  <br />For example: `Refuse to answer topics unrelated to project management; if no results are found, tell the user you did not find relevant data instead of fabricating content.`

### Language Model Settings

In this section, you can select the language model provider, specific model version, and model parameter configuration.

| Setting | Description |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Model Provider | Select or enter the model provider, such as `OpenAI` |
| Language Model | Select or enter the specific language model, such as `gpt-4-turbo` |
| API Key | The API Key required to call the model interface |
| API Address | Select the language model API address, such as `https://api.openai.com/v1/chat/completions` |
| Randomness | A value between 0-2. The higher the Temperature value, the more random the response. The lower the value, the less randomness and the more deterministic the result. When the value approaches zero, the model becomes deterministic and repetitive. |
| Maximum Response Tokens | 0 means unlimited. The maximum number of tokens generated by both the prompt and response completion combined. Different models have different token limits. Specifying a maximum length can prevent overly long or irrelevant responses and control costs. |
| Topic Freshness | The higher the presence_penalty value, the more likely it is to expand to new topics. |
| Frequency Penalty | The higher the frequency_penalty value, the more likely it is to reduce repeated words. |
| Conversation Turns Carried | The number of context rounds the model can remember with each question. |

### Supported Model List

| Model Name | Official Documentation URL | API Key Application URL |
| :--- | :--- | :--- |
| DeepSeek | https://deepseek.com/ | https://platform.deepseek.com/api_keys |
| Volcengine Ark LLM | https://www.volcengine.com/ | https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey |
| Tongyi Qianwen | https://tongyi.aliyun.com/ | https://bailian.console.aliyun.com/?spm=5176.29619931.J_SEsSjsNv72yRuRFS2VknO.2.74cd10d7DbAknf&tab=app#/api-key |
| Zhipu ChatGLM | https://chatglm.cn/ | https://chatglm.cn/developersPanel/apiSet |
| Ollama Local Model | https://ollama.com/ | - |
| OpenAI | https://openai.com/ | https://platform.openai.com/account/api-keys |
| Claude | https://claude.ai/ | https://console.anthropic.com/account/api-keys |

## How to Define Plugins

If the language model is the brain of AI, then plugins are like AI organs, providing AI with more input or output capabilities. Informat provides one-click system plugins for the AI Assistant, giving it basic capabilities.
It also provides custom plugins, enabling designers to create richer and more diverse AI capabilities.

### Plugin Definition

- **Name**: The name of the plugin.
- **Identifier**: The unique identifier of the plugin.
- **Enabled**: Controls whether the plugin is enabled in the AI Assistant.
- **Invocation Description**: The functional description of the plugin.
- **Invocation Automation**: The automation executed when the AI Assistant calls the plugin.

### System Plugins

System plugins provide the AI Assistant with the ability to deeply interact with the system, implementing core functions such as time retrieval and data operations. The specific plugin list is as follows:

| Name | Identifier | Invocation Description |
| ------------------------ | -------------------------------- | ------------------------------------------------ |
| Get Current Time | `_get_current_time` | Get the current time; the AI model needs to call this method before querying |
| Query Available Data Tables | `_query_all_table_list` | Get a list of all data tables and their basic information in the current application |
| Query Specified Data Table Configuration | `_query_table_define` | Get the complete structure definition of a specified data table (including all field information) |
| Query Data Table Record List | `_query_table_record_list` | Query data table records by conditions, supporting filtering, pagination, sorting, etc. |
| Query Data Table Record List Count | `_query_table_record_list_count` | Count the number of data table records matching conditions |
| Send System Email | `_send_system_email` | Send emails using the system mailbox |
| Query App Member Account Basic Info | `_query_app_user_list` | Get member account basic information (including account ID, email, etc.) |
| Web Access | `_web_content` | Get web page content via URL, allowing access to network resources |
| Code Executor | `_javascript_eval` | Execute JavaScript code, suitable for complex calculations and data processing |
| Render HTML | `-render_html` | Render HTML code into a visual interface, supporting interactive content display |
| Insert Specified Data Table Records | `_table_record_batch_insert` | Batch insert records into a specified data table |
| Edit Specified Data Table Records | `_table_record_batch_update` | Modify record content in a specified data table |
| Delete Specified Data Table Records | `_table_record_batch_delete` | Delete records in a specified data table based on conditions |
| Query All Search Engine Modules | `_query_all_textindex_list` | Get all search engine module information (including data source configuration) |
| Search Engine Data Retrieval | `_textindex_search` | Call the search engine to perform data retrieval operations |
| Send Notification | `_send_notification` | Call script to send notifications to web, WeCom, DingTalk, Feishu, and other platforms |
| Read Office Files | `_read_office_file` | Support reading PDF and Word file content |
| Query Informat Script File List | `_query_informat_script_list` | Get Informat script file list |
| Query Specified Informat Script Content | `_query_informat_script_content` | Get script content by script ID |
| Execute Informat Script | `_execute_informat_script` | Execute Informat script by script ID and function name |
| Query Designer Data Table Definition | `_designer_query_table_define` | Query data table definitions in unpublished applications |

### Custom Plugins

**Invocation Automation**  
When a custom plugin is called, it will execute a preset automation workflow to meet personalized needs.

### Plugin Definition Example

Suppose you want to define a plugin to help create tasks, the definition is as follows:

## Enable MCP Server Service

One-click deployment as MCP Server, supporting cross-model invocation and empowerment

 ![Enable MCP Server](images/aiagent-enable-mcp-server.png)
 
 MCP Server Address: `${host}/web0/aiagent/${appId}/${moduleId}/event`
 
 X-INFORMAT-APIKEY: Supports both default application apiKey and custom apiKey
 
