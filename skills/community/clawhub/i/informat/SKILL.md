---
name: informat
description: "Informat AI intelligent development platform system method calling skill. Core rules (strictly follow): 1. Before any creation or modification operation, you must first query the existing structure, not only query the list but also query the complete field structure of each related table. After obtaining the real ID, you can operate. It is strictly forbidden to construct ID out of thin air. For example, before creating a data table, you must first call _query_table_list_designer to get the table list, and then call _query_table_define_designer for each possibly related table to get the field ID. 2. Before calling a method with parameters, you must first use cat to read the corresponding parameter document in the {baseDir}/references/ directory (file name format system_<method name without prefix_>.json), and strictly pass parameters according to the document definition. Failure to read the document and directly construct parameters will lead to failure. 3. Use methods with designer suffix to query and confirm for designer operations, and use methods without designer for application-side operations. 4. The id field must not use system reserved fields such as id, seq, etc. 5. Before executing any creation or modification operation, you must first query the existing system structure to obtain the real ID. It is strictly forbidden to construct any ID or field name out of thin air. 6. Must strictly follow the parameter type, required fields, enumeration values, and nested structure in the parameter document to construct parameters, do not fabricate."
---

# Informat Platform System Methods

There are 119 methods in total. The parameter definition file for each method is under `{baseDir}/references/`.


## Agent Interface Calling Rules

According to the different method names, the system will automatically select the corresponding agent interface:

1. **Team Agent Interface**: Methods starting with `_company` will call the `company_agent` interface
2. **Application Agent Interface**: Other methods will call the `app_agent/{appId}` interface

### Get Application ID

Before calling the application agent interface, you need to get `appId`, you can get it through the following steps:

```bash
# 1. Call the team agent interface to get all application list
node {baseDir}/scripts/call.js company_agent _company_app_list

# 2. Find the target application ID from the returned result
# 3. Use the obtained appId to call the application agent interface
node {baseDir}/scripts/call.js app_agent <appId> _query_table_define --file params.json
```

## Configuration

Edit `{baseDir}/scripts/.env`:

```
host=https://ai.ainformat.com/
agentToken=<your-agent-token>
```

## Query First Before Operation -- The Most Important Rule

Before executing any creation or modification operation, you must first query the existing system structure to obtain the real ID. It is strictly forbidden to construct any ID or field name out of thin air.

Querying cannot stop at just the list, you must further query the complete field structure of each related table. Because when creating associated fields, you need the field ID of the target table, knowing only the table ID is not enough.

### Before Creating an Application

```
1. _company_app_list          -> Get all existing applications, including unique application identifiers
```

### Before Creating a Data Table

```
1. _query_table_list_designer          -> Get all existing tables and their IDs
2. Call separately for each table that may be associated
   _query_table_define_designer        -> Get the complete field list of the table (field ID, field type, option values, etc.)
   This step cannot be omitted, because the associated field requires the field ID of the target table
3. cat {baseDir}/references/system_create_table_module.json  -> Read parameter documentation
4. Construct parameters using the queried real table IDs and field IDs, create the new table
```

Why must query the field structure of each table:
- RelationRecord field requires tableId (target table ID) and nameFieldId (target table display field ID)
- RelationRecordField field requires fieldId (this table foreign key field ID), targetTableId, targetFieldId
- LookupList field requires sub-table ID and foreign key field ID in the sub-table
- LookupRollup field requires sub-table ID and aggregation field ID in the sub-table
- These IDs can only be obtained through _query_table_define_designer query

### Before Creating Dashboard Card

```
1. _query_table_list_designer          -> Get all table IDs
2. Call on the target data source table
   _query_table_define_designer        -> Get all field IDs and field types of the table
   Without querying the field structure, you cannot correctly configure aggregation fields, grouping fields, filter conditions
3. _read_informat_dashboard_document   -> Get dashboard documentation
4. cat {baseDir}/references/system_save_dashboard_prochart_card.json
   or system_save_dashboard_number_card.json  -> Read parameter documentation
5. Construct card parameters using the queried real field IDs
```

### Before Creating Automation

```
1. _query_app_define_designer          -> Get module list, existing automation groups
2. _query_table_list_designer          -> Get all table IDs
3. Call separately for each table involved in automation
   _query_table_define_designer        -> Get field IDs (field mapping and filter conditions in automation steps require real field IDs)
4. _automatic_doc                      -> Get automation documentation
5. cat {baseDir}/references/system_automatic_save_define.json  -> Read parameter documentation
6. Construct automation steps using the queried real IDs
```

### Before Creating Workflow

```
1. _query_app_define_designer -> Get module list
2. _query_table_list_designer + _query_table_define_designer -> Get tables and fields
3. _read_informat_expression_doc -> Get expression documentation (workflow extensively uses expressions)
4. Read the corresponding parameter documentation
5. Create in order: module -> process definition -> startup configuration -> node -> flow
```

### Before Creating Script

```
1. _query_informat_script_list -> Get existing scripts and directories
2. _read_informat_script_sdk -> Get script SDK documentation
3. Create directory first if needed _create_informat_script_directory
4. Read cat {baseDir}/references/system_save_informat_script.json
5. Create or edit script (when editing, must pass the existing script ID, do not create repeatedly)
```

### Before Editing a Field

```
1. _query_table_list_designer -> Find the target table
2. _query_table_define_designer -> Get the complete field list of the table
3. _read_informat_expression_doc -> If you need to configure expressions
4. Read cat {baseDir}/references/system_edit_table_field.json
5. Operate with real tableId and fieldId
```

### Before Operating Data Records

```
1. _query_all_table_list -> Get published table IDs (application side)
2. _query_table_define -> Get published field structure
3. Read the corresponding parameter documentation
4. Construct record data with real field IDs
```

## Calling Steps

### Step 1 - Read Parameter Documentation

```bash
cat {baseDir}/references/system_query_table_define.json
```

The file contains parameter types, required fields, enumeration values, and nested structures. Not reading and directly constructing parameters will cause the call to fail.

### Step 2 - Write Parameter File

Write the parameters to a JSON file (you can choose the current working directory for the file location):

```bash
echo '{"tableId":"myTable"}' > params.json
```

### Step 3 - Execute

```bash
# With parameters (passed via --file parameter file, avoid shell quote issues)
node {baseDir}/scripts/call.js _query_table_define --file params.json

# No parameters
node {baseDir}/scripts/call.js _get_current_time
```

## Team Agent Method List

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Team] | `_company_app_list` | Query application list | `references/system_company_app_list.json` MUST READ |
| [Team] | `_company_app_create` | Create application | `references/system_company_app_create.json` MUST READ |
| [Team] | `_company_role_list` | Query role list | `references/system_company_role_list.json` MUST READ |


## Application Agent Method List

> [Designer] = Draft environment. [Application] = Published environment. [User Operation] = Manual execution by user.

### API Management

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_api_create_define` | Create API definition | `references/system_api_create_define.json` MUST READ |
| [Designer] | `_api_delete_define` | Delete API definition (dangerous operation) | `references/system_api_delete_define.json` MUST READ |
| [Designer] | `_api_doc` | Query Informat API documentation | none |
| [Designer] | `_api_query_define_designer` | Query single API detailed definition | `references/system_api_query_define_designer.json` MUST READ |
| [Designer] | `_api_query_define_list` | Query API definition list under application | none |
| [Designer] | `_api_update_define` | Update API definition, updateFieldList declares the fields to be modified | `references/system_api_update_define.json` MUST READ |

### Application Management

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_app_check_setting` | Validate draft configuration legality before publishing | none |
| [Designer] | `_app_create_role` | Create application role | `references/system_app_create_role.json` MUST READ |
| [Designer] | `_app_delete_draft_define` | Delete draft version Define (unrecoverable) | `references/system_app_delete_draft_define.json` MUST READ |
| [Designer] | `_app_get_define_list` | Get application definition object list | `references/system_app_get_define_list.json` MUST READ |
| [Designer] | `_app_get_define_object` | Get single definition object details | `references/system_app_get_define_object.json` MUST READ |
| [Designer] | `_app_get_define_type` | Get supported definition object types | none |
| [Designer] | `_app_get_draft_define_count` | Draft change count statistics | none |
| [Designer] | `_app_get_draft_define_list` | Draft object list | none |
| [Designer] | `_app_get_web_url` | Get application web root URL | none |
| [User Operation] | `_app_publish` | Publish application to production environment (AI should not call this, remind user to operate) | `references/system_app_publish.json` MUST READ |
| [Designer] | `_app_save_define_object` | Save definition object structure | `references/system_app_save_define_object.json` MUST READ |

### Application Query

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_query_app_define` | Query published application configuration (module list, roles, API, etc.) | none |
| [Designer] | `_query_app_define_designer` | Query designer application configuration (module list, roles, API, automation groups, etc.) | none |
| [Application] | `_query_app_user_list` | Query account information (ID, email, superior, department) | `references/system_query_app_user_list.json` MUST READ |


### Data Table

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_table_module` | Create data table (must query existing tables and field structure before creation) | `references/system_create_table_module.json` MUST READ |
| [Designer] | `_create_table_field_group` | Create data table field group | `references/system_create_table_field_group.json` MUST READ |
| [Designer] | `_create_table_filter_condition` | Generate data table filter | `references/system_create_table_filter_condition.json` MUST READ |
| [Designer] | `_table_save_filter_condition` | Set data table view filter condition | `references/system_table_save_filter_condition.json` MUST READ |
| [Designer] | `_table_create_tool_bar_button` | Create data table toolbar button | `references/system_table_create_tool_bar_button.json` MUST READ |

### Data Table Query

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_query_all_table_list` | Query all published data tables (does not return table field structure) | none |
| [Application] | `_query_table_define` | Query field structure of published table (used for record operations) | `references/system_query_table_define.json` MUST READ |
| [Designer] | `_query_table_list_designer` | Query all tables in designer (including unpublished, does not return table field structure) | none |
| [Designer] | `_query_table_define_designer` | Query data table field structure in designer | `references/system_query_table_define_designer.json` MUST READ |
| [Designer] | `_query_table_field_designer` | Query detailed configuration of a single field in data table | `references/system_query_table_field_designer.json` MUST READ |
| [Application] | `_query_table_record_list` | Query data table records by conditions | `references/system_query_table_record_list.json` MUST READ |
| [Application] | `_query_table_record_list_count` | Count the number of records matching conditions | `references/system_query_table_record_list_count.json` MUST READ |

### Data Table Editing

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_edit_table_field` | Edit field (must query table structure first to get real ID before operation) | `references/system_edit_table_field.json` MUST READ |
| [Designer] | `_edit_table_module` | Modify data table module information | `references/system_edit_table_module.json` MUST READ |

### Data Table Record Operations

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_table_record_batch_insert` | Batch insert records (query table structure first to get field IDs) | `references/system_table_record_batch_insert.json` MUST READ |
| [Application] | `_table_record_batch_update` | Batch update records | `references/system_table_record_batch_update.json` MUST READ |
| [Application] | `_table_record_batch_delete` | Batch delete records (dangerous operation) | `references/system_table_record_batch_delete.json` MUST READ |

### Workflow (BPMN)

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_bpmn_create_module` | Create workflow module | `references/system_bpmn_create_module.json` MUST READ |
| [Designer] | `_bpmn_create_process_define` | Create process definition | `references/system_bpmn_create_process_define.json` MUST READ |
| [Designer] | `_bpmn_update_start_setting` | Update process startup configuration | `references/system_bpmn_update_start_setting.json` MUST READ |
| [Designer] | `_bpmn_create_or_update_node` | Create/update process node | `references/system_bpmn_create_or_update_node.json` MUST READ |
| [Designer] | `_bpmn_create_or_update_flow` | Create/update sequence flow | `references/system_bpmn_create_or_update_flow.json` MUST READ |
| [Designer] | `_bpmn_delete_node` | Delete process node | `references/system_bpmn_delete_node.json` MUST READ |
| [Designer] | `_bpmn_delete_flow` | Delete sequence flow | `references/system_bpmn_delete_flow.json` MUST READ |
| [Designer] | `_bpmn_query_process_define` | Query process definition details | `references/system_bpmn_query_process_define.json` MUST READ |
| [Designer] | `_bpmn_query_process_define_list` | Query process definition list under module | `references/system_bpmn_query_process_define_list.json` MUST READ |

### Automation Process

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_automatic_create_group` | Create automation group (query _query_app_define_designer first to avoid duplication) | `references/system_automatic_create_group.json` MUST READ |
| [Designer] | `_automatic_delete_group` | Delete automation group | `references/system_automatic_delete_group.json` MUST READ |
| [Designer] | `_automatic_update_group` | Edit automation group | `references/system_automatic_update_group.json` MUST READ |
| [Designer] | `_automatic_save_define` | Save automation configuration (must query table structure to get field IDs before creation) | `references/system_automatic_save_define.json` MUST READ |
| [Designer] | `_automatic_query_define` | Query automation configuration | `references/system_automatic_query_define.json` MUST READ |
| [Designer] | `_automatic_run_once` | Execute automation immediately (high risk, confirm first) | `references/system_automatic_run_once.json` MUST READ |
| [Designer] | `_automatic_doc` | Read automation documentation | none |

### Dashboard

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_dashboard_module` | Create dashboard module | `references/system_create_dashboard_module.json` MUST READ |
| [Designer] | `_query_dashboard_list_designer` | Query all dashboards | none |
| [Designer] | `_query_dashboard_card_list` | Query dashboard card list | `references/system_query_dashboard_card_list.json` MUST READ |
| [Designer] | `_query_dashboard_card_detail` | Query card details | `references/system_query_dashboard_card_detail.json` MUST READ |
| [Designer] | `_save_dashboard_number_card` | Create/edit number card (query table structure first to get field ID) | `references/system_save_dashboard_number_card.json` MUST READ |
| [Designer] | `_save_dashboard_prochart_card` | Create/edit chart card (query table structure first to get field ID) | `references/system_save_dashboard_prochart_card.json` MUST READ |

### Script

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_informat_script_directory` | Create script directory | `references/system_create_informat_script_directory.json` MUST READ |
| [Designer] | `_save_informat_script` | Save script (must pass existing ID when editing) | `references/system_save_informat_script.json` MUST READ |
| [Designer] | `_query_informat_script_list` | Query script list | none |
| [Designer] | `_query_informat_script_content` | Query script content | `references/system_query_informat_script_content.json` MUST READ |
| [Application] | `_execute_informat_script` | Execute published script | `references/system_execute_informat_script.json` MUST READ |
| [Designer] | `_execute_informat_script_designer` | Execute script in designer | `references/system_execute_informat_script_designer.json` MUST READ |
| [Designer] | `_generation_informat_script` | Generate script via prompt | `references/system_generation_informat_script.json` MUST READ |

### Scheduled Task

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_schedule_create_define` | Create scheduled task | `references/system_schedule_create_define.json` MUST READ |
| [Designer] | `_schedule_update_define` | Update scheduled task | `references/system_schedule_update_define.json` MUST READ |
| [Designer] | `_schedule_delete_define` | Delete scheduled task | `references/system_schedule_delete_define.json` MUST READ |
| [Designer] | `_schedule_query_define_designer` | Query scheduled task details | `references/system_schedule_query_define_designer.json` MUST READ |
| [Designer] | `_schedule_query_define_list` | Query scheduled task list | none |
| [Designer] | `_schedule_run_once` | Trigger immediately once | `references/system_schedule_run_once.json` MUST READ |
| [Designer] | `_schedule_doc` | Query scheduled task documentation | none |

### Internationalization

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_i18n_query_define_designer` | Query internationalization configuration | none |
| [Designer] | `_i18n_save_define_designer` | Save translation definition | `references/system_i18n_save_define_designer.json` MUST READ |
| [Designer] | `_i18n_save_locale_designer` | Save language list | `references/system_i18n_save_locale_designer.json` MUST READ |
| [Designer] | `_i18n_set_app_name` | Set application internationalization name | `references/system_i18n_set_app_name.json` MUST READ |
| [Designer] | `_i18n_set_module_name` | Set module internationalization name | `references/system_i18n_set_module_name.json` MUST READ |
| [Designer] | `_i18n_set_table_field_name` | Set field internationalization name | `references/system_i18n_set_table_field_name.json` MUST READ |
| [Designer] | `_i18n_set_field_option_name` | Set option value internationalization name | `references/system_i18n_set_field_option_name.json` MUST READ |

### Website Resources

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_website_create_module` | Create website module (query first to avoid duplication) | `references/system_website_create_module.json` MUST READ |
| [Designer] | `_website_create_directory` | Create resource directory | `references/system_website_create_directory.json` MUST READ |
| [Designer] | `_website_save_resource` | Create/edit resource (query ID first when editing) | `references/system_website_save_resource.json` MUST READ |
| [Designer] | `_website_delete_resource` | Delete resource | `references/system_website_delete_resource.json` MUST READ |
| [Designer] | `_website_query_define_designer` | Query website module details | `references/system_website_query_define_designer.json` MUST READ |
| [Designer] | `_website_query_list_designer` | Query all website modules | none |
| [Designer] | `_website_query_resource` | Query resource details | `references/system_website_query_resource.json` MUST READ |
| [Designer] | `_website_read_informat_doc` | Read website designer documentation | none |

### Designer

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_designer_get_app_info` | Query application configuration | none |
| [Designer] | `_designer_get_module_list` | Query module list | none |
| [Designer] | `_designer_get_module_info` | Query module configuration | `references/system_designer_get_module_info.json` MUST READ |
| [Designer] | `_designer_knowledge_database` | Query knowledge base | `references/system_designer_knowledge_database.json` MUST READ |

### Module Management

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_create_module_group` | Create module group | `references/system_create_module_group.json` MUST READ |
| [Designer] | `_update_module_and_group_order` | Update module sorting | `references/system_update_module_and_group_order.json` MUST READ |

### System Information

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_get_current_time` | Get current time | none |
| [Application] | `_get_current_user` | Get current user | none |

### Documentation

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_read_informat_expression_doc` | Informat expression documentation | none |
| [Designer] | `_read_informat_script_sdk` | Informat script SDK documentation | none |
| [Designer] | `_read_informat_dashboard_document` | Informat dashboard chart documentation | none |
| [Application] | `_read_office_file` | Read Office document content | `references/system_read_office_file.json` MUST READ |

### Search

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_query_all_textindex_list` | Query search engine module list | none |
| [Application] | `_textindex_search` | Search engine keyword search | `references/system_textindex_search.json` MUST READ |
| [Application] | `_knowledgebase_search` | Knowledge base keyword search | `references/system_knowledgebase_search.json` MUST READ |

### Notification and Email

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_send_notification` | Send notification | `references/system_send_notification.json` MUST READ |
| [Application] | `_send_system_email` | Send email | `references/system_send_system_email.json` MUST READ |

### Survey

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Designer] | `_survey_create_module` | Create survey module | `references/system_survey_create_module.json` MUST READ |
| [Designer] | `_survey_create_item` | Create survey question | `references/system_survey_create_item.json` MUST READ |
| [Designer] | `_survey_update_item` | Update survey question | `references/system_survey_update_item.json` MUST READ |
| [Designer] | `_survey_delete_item` | Delete survey question | `references/system_survey_delete_item.json` MUST READ |
| [Designer] | `_survey_query_define_designer` | Query survey configuration | `references/system_survey_query_define_designer.json` MUST READ |

### Task

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_task_doc` | Query task documentation | none |
| [Application] | `_task_list` | Query task list | `references/system_task_list.json` MUST READ |
| [Application] | `_task_create` | Create task | `references/system_task_create.json` MUST READ |
| [Application] | `_task_finish` | Finish task | `references/system_task_finish.json` MUST READ |

### Thread

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_thread_create` | Create thread | `references/system_thread_create.json` MUST READ |

### Others

| End | Method Name | Description | Parameter Document |
|----|--------|------|----------|
| [Application] | `_javascript_eval` | Execute JavaScript code | `references/system_javascript_eval.json` MUST READ |
| [Application] | `_render_html` | Render HTML content | `references/system_render_html.json` MUST READ |
| [Application] | `_web_content` | Get web URL content | `references/system_web_content.json` MUST READ |

## Error Handling

When calling the Informat API, you may encounter the following common errors:

### 1. 500 Internal Server Error
- **Cause**: Server internal error, may be due to application not initialized, too frequent API calls, or temporary server failure
- **Solution**: Wait a while and retry, or check application status

### 2. -32601 Exception Error
- **Cause**: Parameter format error, incorrect field configuration or ID does not exist
- **Solution**: Check parameter format is correct, ensure all IDs are real IDs obtained from system query

### 3. Permission Error
- **Cause**: Insufficient agentToken permissions or application access permission issue
- **Solution**: Ensure the agentToken used has sufficient permissions, check application access settings

### 4. Network Error
- **Cause**: Network connection problem or API server unreachable
- **Solution**: Check network connection, ensure host configuration is correct

## Best Practices

### 1. Always Query First Then Operate
- Before executing any creation or modification operation, you must first query the existing system structure
- Get real IDs (table ID, field ID, module ID, etc.)
- Avoid constructing IDs out of thin air, this will cause API call failure

### 2. Strictly Follow Parameter Documentation for Parameters
- Before calling a method with parameters, you must first read the corresponding parameter documentation
- Ensure parameter types, required fields, enumeration values and nested structures are correct
- Use JSON file to pass parameters, avoid shell quote issues

### 3. Error Handling and Retry Mechanism
- Implement appropriate error handling, capture and analyze API errors
- For temporary errors (such as 500 errors), you can implement a retry mechanism
- Record detailed operation logs, easy to troubleshoot problems

### 4. Performance Optimization
- Batch operations: Use batch API to reduce the number of calls
- Reasonable caching: Cache query results, avoid repeated queries
- On-demand query: Only query necessary data, reduce data transmission

## Example Workflow

### Complete Process to Create a Project Management System

1. **Create Application**
   ```bash
   # 1. Prepare parameter file
   echo '{"name": "Project Management System", "appDefineId": "pms2026", "icon": "task", "color": "#1890ff"}' > create_app.json

   # 2. Create application
   node {baseDir}/scripts/call.js _company_app_create --file create_app.json
   ```

2. **Create Data Tables**
   ```bash
   # 1. Prepare project table parameters
   echo '{"id": "project", "name": "Project", "fields": [{"id": "projectName", "name": "Project Name", "type": "SingleText", "singleTextSetting": {"nullable": false}}]}' > create_project_table.json

   # 2. Create project table
   node {baseDir}/scripts/call.js _create_table_module <appId> --file create_project_table.json

   # 3. Prepare task table parameters
   echo '{"id": "task", "name": "Task", "fields": [{"id": "taskName", "name": "Task Name", "type": "SingleText", "singleTextSetting": {"nullable": false}}]}' > create_task_table.json

   # 4. Create task table
   node {baseDir}/scripts/call.js _create_table_module <appId> --file create_task_table.json
   ```

3. **Create Dashboard**
   ```bash
   # 1. Prepare dashboard parameters
   echo '{"id": "dashboard", "name": "Project Management Dashboard"}' > create_dashboard.json

   # 2. Create dashboard
   node {baseDir}/scripts/call.js _create_dashboard_module <appId> --file create_dashboard.json
   ```

## FAQ

### Q: Why does it prompt "Application module identifier already exists" when creating a data table?
A: This means the module ID is already in use, you need to use a different module ID.

### Q: Why does the API return 500 error?
A: The application may not be initialized, it is recommended to wait a while and retry, or check the application status.

### Q: How to get the module list of an application?
A: Use the `_designer_get_module_list` method to query the module list of the application.

### Q: How to get the access address of the application?
A: {host}/app/{appId}
