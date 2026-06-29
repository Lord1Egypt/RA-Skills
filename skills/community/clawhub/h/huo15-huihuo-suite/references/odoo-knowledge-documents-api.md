# Odoo 19 知识库 + 文档 模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/`
> 知识库 `knowledge/models/knowledge_article.py`（标准 addon）；文档 `documents/models/documents_document.py`（企业 OPL）。

---

## 一、知识库 knowledge.article

`_parent_store=True`，`_order="favorite_count desc, write_date desc, id desc"`。

### 关键字段
| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char | 标题（index trigram，全文用） |
| `body` | Html (prefetch=False) | 正文；create 空时自动填 `<h1>{name}</h1>` |
| `icon` | Char | emoji 图标（纯字符串如 "📘"） |
| `parent_id` / `child_ids` | M2o(self) / O2m | 层级父/子（顶级 parent_id=False） |
| `root_article_id` | M2o(self, compute store) | 最高祖先 |
| `internal_permission` | Selection | `write`/`read`/`none`，**根文章必填** |
| `is_user_favorite` | Boolean (compute, **可搜**) | 当前用户是否收藏 |
| `user_has_access` / `user_has_write_access` | Boolean (compute, **可搜**) | 可读/可写 |
| `category` | Selection (compute store) | `workspace`/`private`/`shared` |
| `last_edition_uid` / `last_edition_date` | M2o / Datetime | 最后编辑人/时间 |
| `favorite_count` | Integer | 收藏数 |
| `active` / `to_delete` | Boolean | 归档 / 回收站 |

### 创建 / 查询 / 方法
- **建文章**：`create({'name':..,'body':..,'icon':..})`——根文章不传 internal_permission 会自动补 `'write'`；建子文章传 `parent_id`（需对父有 write 权限，无需 internal_permission）。也可用助手 `article_create(title=, parent_id=)`（自动加创建者为 write 成员）。
- **查询 domain**：我收藏 `[('is_user_favorite','=',True)]`；我可访问 `[('user_has_access','=',True)]`；顶级 `[('parent_id','=',False)]`；我编辑的 `[('last_edition_uid','=',uid)]`；全文搜 `['|',('name','ilike',kw),('body','ilike',kw)]`。
- **方法**：`action_toggle_favorite()`(收藏/取消,返回bool) · `move_to(parent_id=, before_article_id=, category=)`(移动,优先用它不要裸写 parent_id) · `set_internal_permission(permission)` · `invite_members(partners, permission)` · `action_archive/unarchive` · `action_send_to_trash`。
- `get_user_sorted_articles(query, limit=40)`：空 query 返回收藏列表，有 query 走 ts_rank 全文搜，返回 `[{id,icon,name,is_user_favorite,root_article_id}]`。

### 避坑
1. **根文章必须有 internal_permission**（DB 约束）；直接 create 自动补 'write'。
2. **member/inherited_permission 不能普通用户直接写**——member 表对 group_user 只读；改权限/加成员必须调模型方法（内部 sudo）。
3. body 是 Html，ilike 搜含标签；优先 `get_user_sorted_articles`。
4. `is_user_favorite` 的 search **只支持 in/=True**，别用 `!=`。
5. 移动用 `move_to()`（处理 resequence + 权限重置），别裸 `write({'parent_id'})`。
6. `active=False`=归档；`to_delete=True`=回收站（强制 active=False，查回收站带 `context={'active_test':False}`）。

### 示例
```python
# 建文章 / 子文章
aid = call('knowledge.article','create',[{'name':'产品手册','body':'<h1>产品手册</h1><p>...</p>','icon':'📘'}])
call('knowledge.article','create',[{'name':'第一章','parent_id':aid,'icon':'📄'}])
# 我收藏的 / 全文搜 / 读正文 / 收藏切换 / 移动
call('knowledge.article','search_read',[[('is_user_favorite','=',True)]],{'fields':['name','icon']})
call('knowledge.article','search_read',[['|',('name','ilike','退款'),('body','ilike','退款')]],{'fields':['name'],'limit':40})
call('knowledge.article','read',[[aid]],{'fields':['name','body']})
call('knowledge.article','action_toggle_favorite',[[aid]])     # 返回 bool
call('knowledge.article','move_to',[[child_id]],{'parent_id':other_id})
```

---

## 二、文档 documents.document

### ⚠️ Odoo 19 重大架构变化（先看）
| 旧版(16/17) | Odoo 19 |
|---|---|
| `documents.folder` 独立模型 | **删除**。文件夹 = `documents.document` 且 `type='folder'`，父用 `folder_id` 自关联 |
| `documents.tag` + `documents.facet` 两级 | 扁平化为单一 `documents.tag` |
| `documents.share` + workflow.rule | **删除**。改 `documents.access`(文档↔partner) + `access_internal` |
| `folder_id` → documents.folder | `folder_id` → documents.document(type=folder) |

**别再找 documents.folder / documents.share / documents.workflow.rule，19 版不存在。**

### 关键字段
| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char | 文档名 |
| `type` | Selection | `url`/`binary`(默认)/`folder` |
| `folder_id` | M2o(self, type=folder) | 所属文件夹（=父） |
| `datas` | Binary (related attachment) | 文件内容 base64（写它即写附件） |
| `mimetype` / `file_size` / `checksum` | related / Integer | 附件元信息 |
| `index_content` | Text (related) | 全文索引（搜内容用） |
| `url` | Char | 外链（type=url） |
| `tag_ids` | M2m(documents.tag) | 标签 |
| `owner_id` / `partner_id` | M2o | 拥有者/联系人 |
| `res_model` / `res_id` | Char / Reference | 关联业务记录 |
| `access_internal` | Selection | `view`/`edit`/`none` 内部默认权限 |
| `access_token` | Char (compute) | 下载令牌 = `document_token+'o'+hex(id)` |
| `access_url` | Char (compute) | UI 链接 `{base_url}/odoo/documents/{access_token}` |
| `user_permission` | Selection (compute, **可搜**) | 当前用户权限 view/edit/none |
| `active` | Boolean | 归档(回收站) |

### 查询 / 上传 / 下载
- **列文件夹**：`[('type','=','folder')]`；**列文档**：`[('folder_id','=',fid),('type','!=','folder')]`；递归 `('folder_id','child_of',fid)`(**单值**)。
- **按标签/类型/全文**：`[('tag_ids','in',[tid])]` / `[('type','=','binary')]` / `['|',('name','ilike',kw),('index_content','ilike',kw)]`。
- **上传**：`create({'name':..,'datas':<base64>,'folder_id':fid,'mimetype':..})`——自动建 ir.attachment 回填，不必先建 attachment。
- **下载**：`/web/content/<attachment_id>?download=true`（需登录）或公开 `/documents/content/<access_token>?download=true`（凭 token）；UI 用 `access_url`（直接 read 出来）。
- **标签**：`documents.tag` 列 `search_read([],['name'])`；打标签写 `tag_ids` 用 `(4,id)`/`(6,0,[ids])`。**建标签需 group_documents_manager**，普通用户只能用已有标签。
- **移动/归档/分享**：`write({'folder_id':fid})` 移动；`action_archive()` 归档；`action_update_access_rights(partners={pid:('view',False)})` 分享。
- **关联记录**：`{'res_model':'crm.lead','res_id':id}`；反查 `[('res_model','=','project.task'),('res_id','=',id)]`。

### 避坑
1. **folder 就是 document(type=folder)**——列文件夹 `type='folder'`，建文件夹 `create({'name':..,'type':'folder','folder_id':parent})`。
2. **无 documents.folder/share/workflow.rule**（19 删）。
3. **建标签需文档管理员**；普通用户只能用已有标签。
4. `('folder_id','child_of',x)` 的 x **只能单值**。
5. 上传直接传 `datas`(base64)，create 自动建 attachment。
6. 下载令牌 `access_token` 直接 read 出来用，不必自己拼。

### 示例
```python
call('documents.document','search_read',[[('type','=','folder')]],{'fields':['name','folder_id']})  # 文件夹
call('documents.document','search_read',[[('folder_id','=',fid),('type','!=','folder')]],{'fields':['name','file_size']})  # 文件夹内文档
import base64
b64 = base64.b64encode(open('report.pdf','rb').read()).decode()
did = call('documents.document','create',[{'name':'report.pdf','datas':b64,'folder_id':fid,'mimetype':'application/pdf'}])
d = call('documents.document','read',[[did]],{'fields':['access_token','attachment_id']})[0]
# 下载: {url}/documents/content/{d['access_token']}?download=true 或 {url}/web/content/{d['attachment_id'][0]}?download=true
call('documents.document','write',[[did],{'tag_ids':[(4,tid)]}])  # 打标签
```

---

## 三、每日总览（briefing.py，聚合非新模型）

不引入新模型，聚合查询：
- 待办 `project.task`：`[('user_ids','in',[uid]),('project_id','=',False),('parent_id','=',False),('is_closed','=',False),('date_deadline','<=',范围末UTC)]`
- 活动 `mail.activity`：`[('user_id','=',uid),('active','=',True),('date_deadline','<=',范围末Date)]`
- 会议 `calendar.event`：`['&','|',('user_id','=',uid),('partner_ids','in',[my_partner]),'&',('start','>=',lo),('start','<',hi)]`

三者汇总成"我今天/本周要做什么"。待办 date_deadline 是 datetime、活动是 date——比较时分别处理。
