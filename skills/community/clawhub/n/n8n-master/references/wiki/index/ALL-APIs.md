# ALL-APIs

Updated: 2026-05-17

Total API cards: 91

| API | Method | Endpoint | Tags | Card |
|---|---|---|---|---|
| 列出字段 | `GET` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/fields` | feishu, lark | `references/wiki/api-cards/feishu-get-bitable-v1-apps-app-token-tables-table-id-fields.md` |
| 批量更新块的内容 | `PATCH` | `https://open.feishu.cn/open-apis/docx/v1/documents/:document_id/blocks/batch_update` | feishu, lark | `references/wiki/api-cards/feishu-patch-docx-v1-documents-document-id-blocks-batch-update.md` |
| 新增多条记录 | `POST` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_create` | feishu, lark | `references/wiki/api-cards/feishu-post-bitable-v1-apps-app-token-tables-table-id-records-batch-create.md` |
| 新增字段 | `POST` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/fields` | feishu, lark | `references/wiki/api-cards/feishu-post-bitable-v1-apps-app-token-tables-table-id-fields.md` |
| 新增记录 | `POST` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records` | feishu, lark | `references/wiki/api-cards/feishu-post-bitable-v1-apps-app-token-tables-table-id-records.md` |
| 更新块的内容 | `PATCH` | `https://open.feishu.cn/open-apis/docx/v1/documents/:document_id/blocks/:block_id` | feishu, lark | `references/wiki/api-cards/feishu-patch-docx-v1-documents-document-id-blocks-block-id.md` |
| 更新多条记录 | `POST` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/batch_update` | feishu, lark | `references/wiki/api-cards/feishu-post-bitable-v1-apps-app-token-tables-table-id-records-batch-update.md` |
| 更新字段 | `PUT` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/fields/:field_id` | feishu, lark | `references/wiki/api-cards/feishu-put-bitable-v1-apps-app-token-tables-table-id-fields-field-id.md` |
| 更新记录 | `PUT` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/:record_id` | feishu, lark | `references/wiki/api-cards/feishu-put-bitable-v1-apps-app-token-tables-table-id-records-record-id.md` |
| 查询记录 | `POST` | `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/search` | feishu, lark | `references/wiki/api-cards/feishu-post-bitable-v1-apps-app-token-tables-table-id-records-search.md` |
| 自建应用获取 tenant access token | `POST` | `Feishu auth endpoint path omitted in wiki-only package; see official Feishu docs` | feishu, lark | `references/wiki/api-cards/feishu-post-auth-v3-tenant-access-token-internal.md` |
| 获取文档所有块 | `GET` | `https://open.feishu.cn/open-apis/docx/v1/documents/:document_id/blocks` | feishu, lark | `references/wiki/api-cards/feishu-get-docx-v1-documents-document-id-blocks.md` |
| 解决/恢复评论 | `PATCH` | `https://open.feishu.cn/open-apis/drive/v1/files/:file_token/comments/:comment_id` | feishu, lark | `references/wiki/api-cards/feishu-patch-drive-v1-files-file-token-comments-comment-id.md` |
| Add a column to a data table | `POST` | `/data-tables/{dataTableId}/columns` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-data-tables-datatableid-columns.md` |
| Add one or more users to a project | `POST` | `/projects/{projectId}/users` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-projects-projectid-users.md` |
| Archive a workflow | `POST` | `/workflows/{id}/archive` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-workflows-id-archive.md` |
| Change a user's global role | `PATCH` | `/users/{id}/role` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-users-id-role.md` |
| Change a user's role in a project | `PATCH` | `/projects/{projectId}/users/{userId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-projects-projectid-users-userid.md` |
| Create a credential | `POST` | `/credentials` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-credentials.md` |
| Create a folder | `POST` | `/projects/{projectId}/folders` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-projects-projectid-folders.md` |
| Create a new data table | `POST` | `/data-tables` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-data-tables.md` |
| Create a project | `POST` | `/projects` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-projects.md` |
| Create a tag | `POST` | `/tags` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-tags.md` |
| Create a variable | `POST` | `/variables` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-variables.md` |
| Create a workflow | `POST` | `/workflows` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-workflows.md` |
| Create multiple users | `POST` | `/users` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-users.md` |
| Deactivate a workflow | `POST` | `/workflows/{id}/deactivate` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-workflows-id-deactivate.md` |
| Delete a column | `DELETE` | `/data-tables/{dataTableId}/columns/{columnId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-data-tables-datatableid-columns-columnid.md` |
| Delete a data table | `DELETE` | `/data-tables/{dataTableId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-data-tables-datatableid.md` |
| Delete a folder | `DELETE` | `/projects/{projectId}/folders/{folderId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-projects-projectid-folders-folderid.md` |
| Delete a project | `DELETE` | `/projects/{projectId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-projects-projectid.md` |
| Delete a tag | `DELETE` | `/tags/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-tags-id.md` |
| Delete a user | `DELETE` | `/users/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-users-id.md` |
| Delete a user from a project | `DELETE` | `/projects/{projectId}/users/{userId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-projects-projectid-users-userid.md` |
| Delete a variable | `DELETE` | `/variables/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-variables-id.md` |
| Delete a workflow | `DELETE` | `/workflows/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-workflows-id.md` |
| Delete an execution | `DELETE` | `/executions/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-executions-id.md` |
| Delete credential by ID | `DELETE` | `/credentials/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-credentials-id.md` |
| Delete rows from a data table | `DELETE` | `/data-tables/{dataTableId}/rows/delete` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-data-tables-datatableid-rows-delete.md` |
| Discover available API capabilities | `GET` | `/discover` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-discover.md` |
| Generate an audit | `POST` | `/audit` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-audit.md` |
| Get a data table | `GET` | `/data-tables/{dataTableId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-data-tables-datatableid.md` |
| Get credential by ID | `GET` | `/credentials/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-credentials-id.md` |
| Get execution tags | `GET` | `/executions/{id}/tags` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-executions-id-tags.md` |
| Get folder details | `GET` | `/projects/{projectId}/folders/{folderId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-projects-projectid-folders-folderid.md` |
| Get user by ID/Email | `GET` | `/users/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-users-id.md` |
| Get workflow tags | `GET` | `/workflows/{id}/tags` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-workflows-id-tags.md` |
| Insert rows into a data table | `POST` | `/data-tables/{dataTableId}/rows` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-data-tables-datatableid-rows.md` |
| Install a community package | `POST` | `/community-packages` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-community-packages.md` |
| List all data tables | `GET` | `/data-tables` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-data-tables.md` |
| List columns of a data table | `GET` | `/data-tables/{dataTableId}/columns` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-data-tables-datatableid-columns.md` |
| List credentials | `GET` | `/credentials` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-credentials.md` |
| List installed community packages | `GET` | `/community-packages` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-community-packages.md` |
| List project members | `GET` | `/projects/{projectId}/users` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-projects-projectid-users.md` |
| Publish a workflow | `POST` | `/workflows/{id}/activate` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-workflows-id-activate.md` |
| Pull changes from the remote repository | `POST` | `/source-control/pull` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-source-control-pull.md` |
| Retrieve a workflow | `GET` | `/workflows/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-workflows-id.md` |
| Retrieve all executions | `GET` | `/executions` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-executions.md` |
| Retrieve all tags | `GET` | `/tags` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-tags.md` |
| Retrieve all users | `GET` | `/users` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-users.md` |
| Retrieve all workflows | `GET` | `/workflows` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-workflows.md` |
| Retrieve an execution | `GET` | `/executions/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-executions-id.md` |
| Retrieve folders | `GET` | `/projects/{projectId}/folders` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-projects-projectid-folders.md` |
| Retrieve insights summary | `GET` | `/insights/summary` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-insights-summary.md` |
| Retrieve projects | `GET` | `/projects` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-projects.md` |
| Retrieve rows from a data table | `GET` | `/data-tables/{dataTableId}/rows` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-data-tables-datatableid-rows.md` |
| Retrieve variables | `GET` | `/variables` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-variables.md` |
| Retrieves a specific version of a workflow | `GET` | `/workflows/{id}/{versionId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-workflows-id-versionid.md` |
| Retrieves a tag | `GET` | `/tags/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-tags-id.md` |
| Retry an execution | `POST` | `/executions/{id}/retry` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-executions-id-retry.md` |
| Show credential data schema | `GET` | `/credentials/schema/{credentialTypeName}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-get-credentials-schema-credentialtypename.md` |
| Stop an execution | `POST` | `/executions/{id}/stop` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-executions-id-stop.md` |
| Stop multiple executions | `POST` | `/executions/stop` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-executions-stop.md` |
| Test credential by ID | `POST` | `/credentials/{id}/test` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-credentials-id-test.md` |
| Transfer a credential to another project. | `PUT` | `/credentials/{id}/transfer` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-credentials-id-transfer.md` |
| Transfer a workflow to another project | `PUT` | `/workflows/{id}/transfer` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-workflows-id-transfer.md` |
| Unarchive a workflow | `POST` | `/workflows/{id}/unarchive` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-workflows-id-unarchive.md` |
| Uninstall a community package | `DELETE` | `/community-packages/{name}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-delete-community-packages-name.md` |
| Update a column | `PATCH` | `/data-tables/{dataTableId}/columns/{columnId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-data-tables-datatableid-columns-columnid.md` |
| Update a community package | `PATCH` | `/community-packages/{name}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-community-packages-name.md` |
| Update a data table | `PATCH` | `/data-tables/{dataTableId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-data-tables-datatableid.md` |
| Update a folder | `PATCH` | `/projects/{projectId}/folders/{folderId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-projects-projectid-folders-folderid.md` |
| Update a project | `PUT` | `/projects/{projectId}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-projects-projectid.md` |
| Update a tag | `PUT` | `/tags/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-tags-id.md` |
| Update a variable | `PUT` | `/variables/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-variables-id.md` |
| Update a workflow | `PUT` | `/workflows/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-workflows-id.md` |
| Update credential by ID | `PATCH` | `/credentials/{id}` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-credentials-id.md` |
| Update rows in a data table | `PATCH` | `/data-tables/{dataTableId}/rows/update` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-patch-data-tables-datatableid-rows-update.md` |
| Update tags of a workflow | `PUT` | `/workflows/{id}/tags` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-workflows-id-tags.md` |
| Update tags of an execution | `PUT` | `/executions/{id}/tags` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-put-executions-id-tags.md` |
| Upsert a row in a data table | `POST` | `/data-tables/{dataTableId}/rows/upsert` | n8n, public-api | `references/wiki/api-cards/n8n-public-api-post-data-tables-datatableid-rows-upsert.md` |
