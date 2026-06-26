# 云盘与文件 API（Drive）

## 快速调用

# 获取云盘根目录 token
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_explorer_v2_root_folder_meta '{}'

# 获取文件夹内文件列表
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_explorer_v2_fileList '{"order_by":3,"direction":"DESC"}'

# 创建文件夹
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_v1_files_create_folder '{"name":"新文件夹名称"}'

# 移动文件
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_v1_files_move '{"file_token":"文件token","folder_token":"目标文件夹token"}'

## API 分类

文件夹管理：root_folder_meta folder_meta files_list create_folder
文件操作：move delete copy rename
权限管理：permissionMember_create list update delete transfer_owner

## 权限 Scope

drive:drive - 查看、评论、编辑和管理云空间所有文件
drive:drive.metadata:readonly - 只读文件元数据
space:folder:create - 创建文件夹
space:document:move - 移动文件/文件夹
space:document:delete - 删除文件/文件夹
