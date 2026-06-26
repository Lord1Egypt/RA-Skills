# 设备分组管理摘要

## 接口列表

- 新增组：`POST /api/v1/open/basic/groups/create`
- 删除组：`POST /api/v1/open/basic/groups/delete?groupNo=...`
- 更新组：`POST /api/v1/open/basic/groups/update`
- 查询单个组详情：`GET /api/v1/open/basic/groups/get?groupNo=...`
- 查询所有组织：`GET /api/v1/open/basic/groups/actions/listAll`
- 查询下级组：`GET /api/v1/open/basic/groups/actions/childrenList?parentNo=...`
- 设备转移分组：`POST /v1/carrier/device/open/devices/actions/deviceTransfer`

## 关键参数

- `groupNo`：组编号，常用于删除、更新、单组查询
- `groupId`：组 ID，通常出现在返回体中
- `parentNo`：父组编号，空表示根组织
- `targetGroupId`：设备转组时的目标组 ID
- `deviceSerial`：设备序列号

## 约束与注意事项

- 组织数量默认最大支持 5000 个
- 组织层级最大支持 5 级
- 删除组前，目标组不能包含下级节点，也不能包含设备
- 设备转移分组接口使用的是 `targetGroupId`，不是 `groupNo`
