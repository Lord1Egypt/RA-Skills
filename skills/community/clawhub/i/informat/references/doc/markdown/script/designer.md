# informat.designer Application Design Related Operations

## Overview

Use the `informat.designer` object to perform application design related operations

## getDefineObject

Query application design model definition by ID

```javascript
informat.designer.getDefineObject(scope, id)
```

| Parameter | Type     | Description                                            |
|-----------|----------|--------------------------------------------------------|
| scope     | `String` | Scope, default scope is `App`, otherwise scope is the module ID |
| id        | `String` | Model definition ID                                    |

**Return Value**

Type is [DefineObject](/guide/script/model.md#defineobject)

**Example: Query the employee data table module definition**

::: code-group

```javascript [Call]
informat.designer.getDefineObject('App', 'ho3o7sqabzkc1');
```

```json [Return Value]
{
  "build": 47,
  "createTime": "Fri Nov 24 10:23:16 CST 2023",
  "disableModuleTitle": false,
  "disableModuleVisitHistory": false,
  "disableNavBreadcrumb": false,
  "draftVersion": 86,
  "enableModuleTitleRichtext": false,
  "icon": "table",
  "id": "ho3o7sqabzkc1",
  "isDeleted": false,
  "isHiddenMobile": false,
  "isHiddenWeb": false,
  "key": "staffs",
  "name": "员工",
  "noteList": [
  ],
  "scope": "App",
  "tableSetting": {
    "bpmnDeleteRecordWithInstance": false,
    "bpmnShowInstance": false,
    "createToolBarButtonList": [
    ],
    "dataSourceType": "default",
    "enableBpmn": false,
    "enableChangeLog": true,
    "enableChangeLogOnCreate": false,
    "enableComment": true,
    "enableDependAccess": false,
    "enableDependDelete": false,
    "enableDependInsert": false,
    "enableDependUpdate": false,
    "enableRecycleBin": false,
    "fieldGroupList": [
      {
        "expand": false,
        "id": "rqjtx84wlbn4r",
        "isDirectory": false,
        "key": "rqjtx84wlbn4r",
        "name": "获奖情况"
      },
      {
        "expand": false,
        "id": "hbi07rszx5bjy",
        "isDirectory": false,
        "key": "hbi07rszx5bjy",
        "name": "请假情况"
      },
      {
        "expand": false,
        "id": "l4v7chhzagyj8",
        "isDirectory": false,
        "key": "l4v7chhzagyj8",
        "name": "系统字段"
      }
    ],
    "fieldList": [
      {
        "expand": false,
        "icon": "functions",
        "id": "i3zmrlz7q633g",
        "isDirectory": false,
        "key": "recordId",
        "name": "ID",
        "type": "Formula"
      },
      {
        "expand": false,
        "icon": "functions",
        "id": "o3wdmzzwy4lbh",
        "isDirectory": false,
        "key": "seqno",
        "name": "seq",
        "type": "Formula"
      },
      {
        "expand": false,
        "icon": "hashtag",
        "id": "r3rjdlv21qddw",
        "isDirectory": false,
        "key": "staffNo",
        "name": "工号",
        "type": "ID"
      },
      {
        "expand": false,
        "icon": "text",
        "id": "kcv33zajbr6qn",
        "isDirectory": false,
        "key": "name",
        "name": "姓名",
        "type": "SingleText"
      },
      {
        "expand": false,
        "icon": "checkbox-circle",
        "id": "pyypptbpcdvop",
        "isDirectory": false,
        "key": "sex",
        "name": "性别",
        "type": "ListSelect"
      },
      {
        "expand": false,
        "icon": "number-1",
        "id": "urx7djdqnp7mf",
        "isDirectory": false,
        "key": "age",
        "name": "年龄",
        "type": "Integer"
      },
      {
        "expand": false,
        "icon": "star",
        "id": "w0xci8e3xl8v9",
        "isDirectory": false,
        "key": "grade",
        "name": "级别",
        "type": "Rate"
      },
      {
        "expand": false,
        "icon": "checkbox-circle",
        "id": "nnw2iiycbpghu",
        "isDirectory": false,
        "key": "status",
        "name": "状态",
        "type": "ListSelect"
      },
      {
        "expand": false,
        "icon": "attachment",
        "id": "qpxzoe9tlo92m",
        "isDirectory": false,
        "key": "attachment",
        "name": "附件",
        "type": "Attachment"
      },
      {
        "expand": false,
        "icon": "node-tree",
        "id": "rebf9ipbjj2jb",
        "isDirectory": false,
        "key": "area",
        "name": "所在地区",
        "type": "Cascader"
      },
      {
        "expand": false,
        "icon": "pencil",
        "id": "bsfu7evwrqi4v",
        "isDirectory": false,
        "key": "signature",
        "name": "手写签名",
        "type": "Signature"
      },
      {
        "expand": false,
        "icon": "link",
        "id": "ff76vrkqz02hc",
        "isDirectory": false,
        "key": "deptRel",
        "name": "所在部门",
        "type": "RelationRecord"
      },
      {
        "expand": false,
        "icon": "link",
        "id": "cce1xkp45cjhb",
        "isDirectory": false,
        "key": "rewardCount",
        "name": "获奖次数",
        "type": "RelationRollup"
      },
      {
        "expand": false,
        "icon": "link",
        "id": "vp1c87b94u4lg",
        "isDirectory": false,
        "key": "rewardList",
        "name": "奖励列表",
        "type": "Relation"
      },
      {
        "expand": false,
        "icon": "link",
        "id": "qrnaq2o3uffbj",
        "isDirectory": false,
        "key": "leaveLogRel",
        "name": "请假列表",
        "type": "LookupList"
      },
      {
        "expand": false,
        "icon": "link",
        "id": "a7nr1z1y871n6",
        "isDirectory": false,
        "key": "totalLevelDays",
        "name": "请假总天数",
        "type": "LookupRollup"
      },
      {
        "expand": false,
        "icon": "time",
        "id": "xspynt2y38x4s",
        "isDirectory": false,
        "key": "createTime",
        "name": "创建时间",
        "type": "CreateTime"
      },
      {
        "expand": false,
        "icon": "time",
        "id": "ychzl2fr9vrta",
        "isDirectory": false,
        "key": "updateTime",
        "name": "最后修改时间",
        "type": "LastModifyTime"
      },
      {
        "expand": false,
        "icon": "user",
        "id": "drjw345d7d6o9",
        "isDirectory": false,
        "key": "createUser",
        "name": "创建人",
        "type": "CreateUser"
      },
      {
        "expand": false,
        "icon": "user",
        "id": "ol07czcyxvzwi",
        "isDirectory": false,
        "key": "updateUser",
        "name": "最后更新人",
        "type": "LastModifyUser"
      }
    ],
    "fieldStyleList": [
    ],
    "formDisplayWidth": 700,
    "formDisplayWidthUnit": "px",
    "formFieldStyle": "border",
    "formFullSaveAutoClose": false,
    "formLabelAlign": "left",
    "formLabelWidth": 100,
    "formSaveMode": "Field",
    "formStyle": "Simple",
    "formToolBarButtonList": [
    ],
    "listenerList": [
    ],
    "returnFieldList": [
    ],
    "tableIndexList": [
    ],
    "tableView": {
      "bottomToolBarButtonList": [
      ],
      "childrenAsyncLoadAutomaticVarList": [
      ],
      "childrenAsyncLoadEnable": false,
      "childrenAutoExpandLevel": 0,
      "childrenExpandLevel": 1,
      "childrenSelectionStrictly": false,
      "childrenShowParent": false,
      "childrenShowPathbar": false,
      "contextMenuButtonList": [
      ],
      "defaultPageSize": 50,
      "disableAutoLoad": false,
      "disableFilterCache": false,
      "filterConditionList": [
      ],
      "filterList": [
      ],
      "filterPosition": "toolbar",
      "filterViewLabelPosition": "top",
      "filterViewLabelWidth": 120,
      "filterViewType": "none",
      "filterViewWidth": 240,
      "formCommentVisibleRoleList": [
      ],
      "formDetailVisibleRoleList": [
      ],
      "formFieldConfigList": [
      ],
      "formShowDialogModal": false,
      "formShowType": "dialog",
      "gridDisplaySetting": {
        "autoExpendWhenGroup": true,
        "border": "full",
        "cellEditMode": "dblclick",
        "cellStyleList": [
        ],
        "columnList": [
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "functions",
            "id": "i3zmrlz7q633g",
            "name": "ID",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "functions",
            "id": "o3wdmzzwy4lbh",
            "name": "seq",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "hashtag",
            "id": "r3rjdlv21qddw",
            "name": "工号",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "text",
            "id": "kcv33zajbr6qn",
            "name": "姓名",
            "type": "field",
            "width": "200"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "checkbox-circle",
            "id": "pyypptbpcdvop",
            "name": "性别",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "checkbox-circle",
            "id": "nnw2iiycbpghu",
            "name": "状态",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "number-1",
            "id": "urx7djdqnp7mf",
            "name": "年龄",
            "type": "field",
            "width": "100"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "star",
            "id": "w0xci8e3xl8v9",
            "name": "级别",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "link",
            "id": "ff76vrkqz02hc",
            "name": "所在部门",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "attachment",
            "id": "qpxzoe9tlo92m",
            "name": "附件",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "node-tree",
            "id": "rebf9ipbjj2jb",
            "name": "所在地区",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "link",
            "id": "cce1xkp45cjhb",
            "name": "获奖次数",
            "type": "field",
            "width": "150"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "user",
            "id": "drjw345d7d6o9",
            "name": "创建人",
            "type": "field",
            "width": "100"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "time",
            "id": "xspynt2y38x4s",
            "name": "创建时间",
            "type": "field",
            "width": "130"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "user",
            "id": "ol07czcyxvzwi",
            "name": "最后更新人",
            "type": "field",
            "width": "100"
          },
          {
            "buttonList": [
            ],
            "children": [
            ],
            "edit": false,
            "icon": "time",
            "id": "ychzl2fr9vrta",
            "name": "最后修改时间",
            "type": "field",
            "width": "130"
          }
        ],
        "customLineHeight": 32,
        "defaultShowDetailOpt": false,
        "enableHighlightCurrent": false,
        "footerAggregateType": "currentPage",
        "hideFieldIcon": false,
        "hideFooter": false,
        "hideHeader": false,
        "lineHeight": "min",
        "scrollBarPosition": "keep",
        "selectionMode": "checkbox",
        "stripe": true,
        "tableButtonList": [
        ],
        "tableDragSort": false,
        "tableIndex": false,
        "tableStripe": true
      },
      "hideToolbar": false,
      "listenerList": [
      ],
      "orderByFieldList": [
      ],
      "orderByList": [
      ],
      "paginationPosition": "top",
      "paginationStyle": "simple",
      "pathFilterList": [
      ],
      "returnFieldList": [
      ],
      "searchChildrenExpandLevel": 0,
      "showBottomToolbar": false,
      "toolBarButtonList": [
        {
          "action": "RecordCreate",
          "actionSetting": {
            "readonlyFieldList": [
            ],
            "valueList": [
            ],
            "hideFieldList": [
            ],
            "hideContinueCreate": false,
            "tableId": "ho3o7sqabzkc1",
            "defaultContinueCreate": false,
            "keepFieldList": [
            ],
            "dialogModal": false
          },
          "buttonSetting": {
            "badgeType": "danger",
            "enableConfirm": false,
            "hideName": false,
            "plain": false,
            "round": false,
            "type": "default"
          },
          "cardSetting": {
            "alignItems": "flex-start",
            "flexDirection": "row",
            "justifyContent": "flex-start"
          },
          "children": [
          ],
          "componentSetting": {
            "disableShadowDom": false,
            "eventHandlerList": [
            ],
            "props": [
            ]
          },
          "controlType": "button",
          "id": "swj3tg8iesu6",
          "inputSetting": {
            "width": 200
          },
          "isDirectory": false,
          "labelSetting": {
            "bold": false,
            "fontSize": 13
          },
          "name": "创建",
          "richtextSetting": {
          },
          "selectSetting": {
            "multiple": false,
            "optionList": [
            ],
            "width": 200
          },
          "switchSetting": {
            "type": "primary"
          }
        },
        {
          "action": "RecordDelete",
          "actionSetting": {
            "recordIdExpression": "${tableSelectedIdList}",
            "tableId": "ho3o7sqabzkc1"
          },
          "buttonSetting": {
            "badgeType": "danger",
            "confirmMessageExpression": "确定要彻底删除选中的记录吗？",
            "enableConfirm": true,
            "hideName": false,
            "icon": "delete-bin-6",
            "plain": false,
            "round": false,
            "type": "danger"
          },
          "cardSetting": {
            "alignItems": "flex-start",
            "flexDirection": "row",
            "justifyContent": "flex-start"
          },
          "children": [
          ],
          "componentSetting": {
            "disableShadowDom": false,
            "eventHandlerList": [
            ],
            "props": [
            ]
          },
          "controlType": "button",
          "disableExpression": "${Array.isEmpty(tableSelectedIdList)}",
          "id": "me81s2ptrb30",
          "inputSetting": {
            "width": 200
          },
          "isDirectory": false,
          "labelSetting": {
            "bold": false,
            "fontSize": 13
          },
          "name": "删除记录",
          "richtextSetting": {
          },
          "selectSetting": {
            "multiple": false,
            "optionList": [
            ],
            "width": 200
          },
          "switchSetting": {
            "type": "primary"
          }
        }
      ]
    }
  },
  "type": "Table",
  "updateTime": "Fri Feb 28 16:29:55 CST 2025",
  "updateUser": "zhangsan",
  "viewSplitSetting": {
    "splitPosition": "right",
    "splitSize": 300,
    "splitSizeUnit": "px",
    "websiteComponentSetting": {
      "disableShadowDom": false,
      "eventHandlerList": [
      ],
      "props": [
      ]
    },
    "websiteType": "website"
  }
}
```

:::

## getDefineObjectByKey

Query application design model definition by identifier

```javascript
informat.designer.getDefineObjectByKey(scope, key)
```

| Parameter | Type     | Description                                            |
|-----------|----------|--------------------------------------------------------|
| scope     | `String` | Scope, default scope is `App`, otherwise scope is the module ID |
| key       | `String` | Model identifier                                       |

**Return Value**

Type is [DefineObject](/guide/script/model.md#defineobject)

**Example: Query the employee data table module definition**

::: code-group

```javascript [Call]
informat.designer.getDefineObject('App', 'staff');
```

```text [Return Value]
Same as above
```

:::

## getDefineObjectList

Query application design model definition list

```javascript
informat.designer.getDefineObjectList(query)
```

Type definitions are as follows
| Parameter | Type | Description |
| -------- | --------------------------------------------------------- | ---------------- |
| ApiDefine | `String` | API definition |
| ApplicationOptionDefine | `String` | Application option value definition |
| ApplicationDefine | `String` | Application definition |
| AutomaticDefine | `String` | Automation definition |
| BpmnProcessDefine | `String` | Workflow process definition |
| DashboardCardDefine | `String` | Dashboard card definition |
| DataSourceDefine | `String` | Data source definition |
| FormDesignerDefine | `String` | Form designer definition |
| I18nDefine | `String` | Internationalization translation definition |
| ModuleDefine | `String` | Application module definition |
| PageDesignerDefine | `String` | Print module definition |
| RoleDefine | `String` | Application role definition |
| ScheduleDefine | `String` | Scheduled task definition |
| ScriptDefine | `String` | Script definition |
| SurveyItemDefine | `String` | Survey definition |
| TableFieldDefine | `String` | Data table field definition |
| TableFieldGroupDefine | `String` | Data table field group definition |
| TableIndexDefine | `String` | Data table index definition |
| VersionDefine | `String` | Application version description definition |
| WebsiteResourceDefine | `String` | Website static resource definition |

| Parameter | Type                                                     | Description  |
|-----------|----------------------------------------------------------|--------------|
| query     | [DefineObjectQuery](/guide/script/model.md#defineobjectquery) | Query object |

**Return Value**

Type is Array<[DefineObject](/guide/script/model.md#defineobject)>

**Example: Query all module list under the application**

::: code-group

```javascript [Call]
informat.designer.getDefineObjectList({
    type: 'ModuleDefine',
    pageSize: 10000
});
```

```json [Return Value]
[
  {
    "build": 60,
    "createTime": "Fri Nov 24 12:11:04 CST 2023",
    "createUser": "李四",
    "disableModuleTitle": false,
    "disableModuleVisitHistory": false,
    "disableNavBreadcrumb": false,
    "draftVersion": 143,
    "enableModuleTitleRichtext": false,
    "floatButtonList": [
      {
        "action": "OpenSplitDrawer",
        "actionSetting": {
          "splitSize": "1000px",
          "dialogCloseOnClickModal": false,
          "splitWithHeader": false,
          "splitDirection": "right",
          "splitModal": true,
          "splitShowClose": true,
          "splitType": "External",
          "dialogHideClose": false,
          "dialogModal": false,
          "websiteType": "website",
          "splitCloseOnPressEscape": true,
          "dialogCloseOnPressEscape": false,
          "showType": "drawer",
          "externalUrlVar": "/designer/${app.id}/module/${module.type.toLowerCase()}/${module.id}/Field?nonav=true",
          "splitWrapperClosable": true
        },
        "buttonSetting": {
          "badgeType": "danger",
          "enableConfirm": false,
          "hideName": false,
          "icon": "question",
          "plain": false,
          "round": true,
          "type": "danger"
        },
        "cardSetting": {
          "alignItems": "flex-start",
          "flexDirection": "row",
          "justifyContent": "flex-start"
        },
        "children": [
        ],
        "componentSetting": {
          "disableShadowDom": false,
          "eventHandlerList": [
          ],
          "props": [
          ]
        },
        "controlType": "button",
        "id": "nszejc2sxhid",
        "inputSetting": {
          "width": 200
        },
        "isDirectory": false,
        "labelSetting": {
          "bold": false,
          "fontSize": 13
        },
        "name": "查看配置项",
        "richtextSetting": {
        },
        "selectSetting": {
          "multiple": false,
          "optionList": [
          ],
          "width": 200
        },
        "switchSetting": {
          "type": "primary"
        }
      },
      {
        "action": "OpenSplitDrawer",
        "actionSetting": {
          "splitSize": "1000px",
          "dialogCloseOnClickModal": false,
          "splitWithHeader": false,
          "splitDirection": "right",
          "splitModal": true,
          "splitShowClose": true,
          "splitType": "External",
          "dialogHideClose": false,
          "dialogModal": false,
          "websiteType": "website",
          "splitCloseOnPressEscape": true,
          "dialogCloseOnPressEscape": false,
          "showType": "drawer",
          "externalUrlVar": "/doc/guide/table/relation.html",
          "splitWrapperClosable": true
        },
        "buttonSetting": {
          "badgeType": "danger",
          "enableConfirm": false,
          "hideName": false,
          "icon": "question",
          "plain": false,
          "round": true,
          "type": "danger"
        },
        "cardSetting": {
          "alignItems": "flex-start",
          "flexDirection": "row",
          "justifyContent": "flex-start"
        },
        "children": [
        ],
        "componentSetting": {
          "disableShadowDom": false,
          "eventHandlerList": [
          ],
          "props": [
          ]
        },
        "controlType": "button",
        "id": "k6k7mlqq57l5",
        "inputSetting": {
          "width": 200
        },
        "isDirectory": false,
        "labelSetting": {
          "bold": false,
          "fontSize": 13
        },
        "name": "查看文档",
        "richtextSetting": {
        },
        "selectSetting": {
          "multiple": false,
          "optionList": [
          ],
          "width": 200
        },
        "switchSetting": {
          "type": "primary"
        }
      }
    ],
    "icon": "node-tree",
    "id": "qgzs6s9pk3i50",
    "isDeleted": false,
    "isHiddenMobile": false,
    "isHiddenWeb": false,
    "key": "dataModelOneToManyMain",
    "name": "关联列表-主表",
    "noteList": [
    ],
    "readme": "### 模块介绍： 一对多关系指一个模型的一条数据和另一个模型的多条数据存在关系，在织信平台中可以通过**关联列表**和**查找列表**两个类型的字段来构建一对多关系。一对多关系最终将会以列表的形式在表单中进行展示。 **关联列表的特性：** 关联列表类型的字段可直接构建数据间的一对多关系，其在数据库中会使用邻接表单独存储，在自动化和脚本中查询记录信息不会返回`关联列表` 的值，需要单独调用自动化步骤或者脚本函数查询。 **查找列表的特性：** 查找列表其实就是将另一个模块的数据以列表的形式展示在当前表单中，需要通过查找列表实现一对多关系的建立需要构建一个数据表作为子表。一般我们都会在子表中使用关联记录关联主表，然后在主表中使用查找列表实现一对多关系的构建。 **关联列表汇总：** 关联列表-子表分组中的`数量`字段是通过关联列表汇总类型字段实现的，此字段可对指定关联列表类型的字段进行汇总计算，支持数量、求和、平均值、最大值、最小值、平均值五种汇总函数。 **查找汇总：** 查找列表-子表汇总分组中的`数量`、`求和`、`数量-条件`字段是通过查找列表汇总类型字段实现的，此字段可对指定数据表中关联到本表的关联记录字段进行查询并汇总计算，支持数量、求和、平均值、最大值、最小值、平均值五种汇总函数。`数量`是对子表中数据的数据进行数量计算；`求和`是对子表中的`数值`进行求和计算；`数量-条件`是对子表中类型为类型1和类型2的数据进行数量计算。 ### 参考文档： 关联列表帮助文档：[关联列表](https://next.informat.cn/doc/guide/table/relation.html) 查找列表帮助文档：[查找列表](https://next.informat.cn/doc/guide/table/lookup-list.html)",
    "remark": "该模块展示【关联列表】字段的多种使用样例。可点击工具栏中的<创建记录>按钮进行体验。",
    "scope": "App",
    "tableSetting": {
      "bpmnDeleteRecordWithInstance": false,
      "bpmnShowInstance": false,
      "createToolBarButtonList": [
      ],
      "dataSourceType": "default",
      "enableBpmn": false,
      "enableChangeLog": false,
      "enableChangeLogOnCreate": false,
      "enableComment": false,
      "enableDependAccess": false,
      "enableDependDelete": false,
      "enableDependInsert": false,
      "enableDependUpdate": false,
      "enableRecycleBin": false,
      "fieldGroupList": [
        {
          "expand": false,
          "id": "xy484h1bq4ja4",
          "isDirectory": false,
          "key": "xy484h1bq4ja4",
          "name": "创建完子表的操作"
        }
      ],
      "fieldList": [
        {
          "expand": false,
          "icon": "link",
          "id": "u038ld3bhymoh",
          "isDirectory": false,
          "key": "relationListCreate",
          "name": "关联列表",
          "remark": "<div>新增子表行数据，并提交后设置数值字段的值为100</div>",
          "type": "Relation"
        },
        {
          "expand": false,
          "icon": "text",
          "id": "pd44z71kxht2z",
          "isDirectory": false,
          "key": "pd44z71kxht2z",
          "name": "名称",
          "type": "SingleText"
        }
      ],
      "fieldStyleList": [
      ],
      "formDisplayWidth": 700,
      "formDisplayWidthUnit": "px",
      "formFieldStyle": "border",
      "formFullSaveAutoClose": false,
      "formLabelAlign": "left",
      "formLabelWidth": 100,
      "formSaveMode": "Field",
      "formStyle": "Simple",
      "formToolBarButtonList": [
      ],
      "listenerList": [
        {
          "automaticList": [
            "wb2y0zcpea02n"
          ],
          "automaticVarList": [
            {
              "value": "${formRecord.id}"
            }
          ],
          "eventList": [
            "form.field.list.loaded",
            "form.field.list.reloaded"
          ],
          "id": "mnva0qlta4u8",
          "isEnable": true,
          "name": "表单子表数据加载完成后调用",
          "tableFieldSetting": {
            "tableFieldList": [
            ]
          }
        }
      ],
      "returnFieldList": [
      ],
      "tableIndexList": [
      ],
      "tableView": {
        "bottomToolBarButtonList": [
        ],
        "childrenAsyncLoadAutomaticVarList": [
        ],
        "childrenAsyncLoadEnable": false,
        "childrenAutoExpandLevel": 0,
        "childrenExpandLevel": 1,
        "childrenSelectionStrictly": false,
        "childrenShowParent": false,
        "childrenShowPathbar": false,
        "contextMenuButtonList": [
        ],
        "defaultPageSize": 50,
        "disableAutoLoad": false,
        "disableFilterCache": false,
        "filterConditionList": [
        ],
        "filterList": [
        ],
        "filterPosition": "toolbar",
        "filterViewLabelPosition": "top",
        "filterViewLabelWidth": 120,
        "filterViewType": "none",
        "filterViewWidth": 240,
        "formCommentVisibleRoleList": [
        ],
        "formDetailVisibleRoleList": [
        ],
        "formFieldConfigList": [
        ],
        "formShowDialogModal": false,
        "formShowType": "dialog",
        "gridDisplaySetting": {
          "autoExpendWhenGroup": true,
          "border": "full",
          "cellEditMode": "dblclick",
          "cellStyleList": [
          ],
          "columnList": [
            {
              "buttonList": [
              ],
              "children": [
              ],
              "edit": false,
              "icon": "text",
              "id": "pd44z71kxht2z",
              "name": "名称",
              "type": "field",
              "width": "200"
            },
            {
              "buttonList": [
              ],
              "children": [
              ],
              "edit": false,
              "icon": "link",
              "id": "u038ld3bhymoh",
              "name": "关联列表",
              "type": "field",
              "width": "150"
            }
          ],
          "customLineHeight": 32,
          "defaultShowDetailOpt": false,
          "enableHighlightCurrent": false,
          "footerAggregateType": "currentPage",
          "hideFieldIcon": false,
          "hideFooter": false,
          "hideHeader": false,
          "lineHeight": "min",
          "scrollBarPosition": "keep",
          "selectionMode": "checkbox",
          "stripe": true,
          "tableButtonList": [
          ],
          "tableDragSort": false,
          "tableIndex": false,
          "tableStripe": true
        },
        "hideToolbar": false,
        "listenerList": [
        ],
        "orderByFieldList": [
        ],
        "orderByList": [
        ],
        "paginationPosition": "top",
        "paginationStyle": "simple",
        "pathFilterList": [
        ],
        "returnFieldList": [
        ],
        "searchChildrenExpandLevel": 0,
        "showBottomToolbar": false,
        "toolBarButtonList": [
          {
            "action": "RecordCreate",
            "actionSetting": {
              "readonlyFieldList": [
              ],
              "valueList": [
              ],
              "hideFieldList": [
              ],
              "hideContinueCreate": false,
              "tableId": "qgzs6s9pk3i50",
              "defaultContinueCreate": false,
              "keepFieldList": [
              ],
              "dialogModal": false
            },
            "buttonSetting": {
              "badgeType": "danger",
              "enableConfirm": false,
              "hideName": false,
              "icon": "menu-add",
              "plain": false,
              "round": false,
              "type": "primary"
            },
            "cardSetting": {
              "alignItems": "flex-start",
              "flexDirection": "row",
              "justifyContent": "flex-start"
            },
            "children": [
            ],
            "componentSetting": {
              "disableShadowDom": false,
              "eventHandlerList": [
              ],
              "props": [
              ]
            },
            "controlType": "button",
            "id": "huldgy7bm7ff",
            "inputSetting": {
              "width": 200
            },
            "isDirectory": false,
            "labelSetting": {
              "bold": false,
              "fontSize": 13
            },
            "name": "创建记录",
            "richtextSetting": {
            },
            "selectSetting": {
              "multiple": false,
              "optionList": [
              ],
              "width": 200
            },
            "switchSetting": {
              "type": "primary"
            }
          },
          {
            "action": "RecordDelete",
            "actionSetting": {
              "recordIdExpression": "${tableSelectedIdList}",
              "tableId": "qgzs6s9pk3i50"
            },
            "buttonSetting": {
              "badgeType": "danger",
              "confirmMessageExpression": "确定要彻底删除选中的记录吗？",
              "enableConfirm": true,
              "hideName": false,
              "icon": "delete-bin-6",
              "plain": false,
              "round": false,
              "type": "danger"
            },
            "cardSetting": {
              "alignItems": "flex-start",
              "flexDirection": "row",
              "justifyContent": "flex-start"
            },
            "children": [
            ],
            "componentSetting": {
              "disableShadowDom": false,
              "eventHandlerList": [
              ],
              "props": [
              ]
            },
            "controlType": "button",
            "disableExpression": "${Array.isEmpty(tableSelectedIdList)}",
            "id": "ypozortrus0y",
            "inputSetting": {
              "width": 200
            },
            "isDirectory": false,
            "labelSetting": {
              "bold": false,
              "fontSize": 13
            },
            "name": "删除记录",
            "richtextSetting": {
            },
            "selectSetting": {
              "multiple": false,
              "optionList": [
              ],
              "width": 200
            },
            "switchSetting": {
              "type": "primary"
            }
          }
        ]
      }
    },
    "type": "Table",
    "updateTime": "Mon Apr 07 15:17:03 CST 2025",
    "updateUser": "李四",
    "viewSplitSetting": {
      "splitPosition": "right",
      "splitSize": 300,
      "splitSizeUnit": "px",
      "websiteComponentSetting": {
        "disableShadowDom": false,
        "eventHandlerList": [
        ],
        "props": [
        ]
      },
      "websiteType": "website"
    }
  }
]
```

:::


## getRefEntity

Query the **reference relationships** in the application designer, used to retrieve dependency and association information between various design objects within the application.


```javascript
informat.designer.getRefEntity()
```

**Return Value**

Type is Array<[RefEntity](/guide/script/model.md#refentity)>

### Supported Reference Relationship Types

Currently covers the following objects and their mutual reference relationships (including both **direct references** and **indirect references**):

#### Data Tables
- Data Table <-> Data Table (relation fields, reference fields)
- Data Table <-> Field

#### Fields
- Field <-> Automation
- Field <-> Script
- Field <-> Control

#### Automations
- Automation <-> Data Table / Field
- Automation <-> Script

#### Scripts
- Script <-> Data Table
- Script <-> Field
- Script <-> Automation

#### Pages / Controls
- Control <-> Field
- Control <-> Automation
- Control <-> Script

> Reference relationships may be created through field bindings, expressions, parameter configurations, etc.,
> including both **explicit references** and potentially **implicit references**.
