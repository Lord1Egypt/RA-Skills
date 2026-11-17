# n8n Form Trigger node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `n8n Form Trigger node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.formtrigger`
- node group: `core-nodes`

## 核心要点

- Learn how to use the n8n Form Trigger node in n8n. Follow technical documentation to integrate n8n Form Trigger node into your workflows.

## 关键操作 / 参数线索

- **Basic Auth**
- **None**
- The **Username** you use to access the app or service your HTTP Request is targeting.
- The **Password** that goes with that username.
- **Test URL**: n8n registers a test webhook when you select **Execute Step** or **Execute Workflow**, if the workflow isn't active. When you call the URL, n8n displays the data in the workflow.
- **Production URL**: n8n registers a production webhook when you publish the workflow. When using the production URL, n8n doesn't display the data in the workflow. You can still view workflow data for a production execution. Select the **Executions** tab in the workflow, then select the workflow execution you want to view.
- **Field Label**: Enter the label that appears above the input field on the rendered form.
- **Field Name**: This name is used in the output of the Form Trigger node. Use it to reference a form field in downstream nodes.
- **Element Type**: Choose from **Checkboxes**, **Custom HTML**, **Date**, **Dropdown**, **Email**, **File**, **Hidden Field**, **Number**, **Password**, **Radio Buttons**, **Text**, or **Textarea**.
- Select **Checkboxes** to include checkbox elements in the form. By default, there is no limit on how many checkboxes a form user can select. You can set the limit by specifying a value for the **Limit Selection** option as **Exact Number**, **Range**, or **Unlimited**.
- Select **Custom HTML** to insert arbitrary HTML.
- You can include elements like links, images, video, and more. You can't include ``, ``, or `` elements. For more information, see HTML security and allowed tags.
- By default, Custom HTML fields aren't included in the node output. To include the Custom HTML content in the output, fill out the associated **Element Name** field.
- Select **Date** to include a date picker in the form. Refer to Date and time with Luxon for more information on formatting dates.
- Select **Dropdown List** > **Add Field Option** to add multiple options. By default, the dropdown is single-choice. To make it multiple-choice, turn on **Multiple Choice**.
- Select **Radio Buttons** to include radio button elements in the form.
- Select **Hidden Field** to include a form element without displaying it on the form. You can set a default value using the **Field Value** parameter or pass values for the field using query parameters.
- **Placeholder**: Define a sample text to display inside compatible form elements. Placeholders are supported in **Email**, **Number**, **Password**, **Text** and **Textarea**.

## 常用选项线索

- **Append n8n Attribution**: Turn off to hide the **Form automated with n8n** attribute at the bottom of the form.
- **Button Label**: The label to use for your form's submit button. n8n displays the **Button Label** as the name of the submit button.
- **Form Path**: The final segment of the form's URL, for both testing and production. Replaces the automatically generated UUID as the final component.
- **Ignore Bots**: Turn on to ignore requests from bots like link previewers and web crawlers.
- **Use Workflow Timezone**: Turn on to use the timezone in the Workflow settings instead of UTC (default). This affects the value of the `submittedAt` timestamp in the node output.
- **Custom Form Styling**: Override the default styling of the public form interface with CSS. The field pre-populates with the default styling so you can change only what you need to.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

