# 飞书知识库配置（拓展阅读文档库）

## 配置值（已确认）

| 配置项 | 值 | 说明 |
|--------|------|------|
| space_id | `7621391289904516315` | 个人知识库 |
| node_token | `DFmiwdgn4ic2D2kJPK6ca1XLnhd` | 拓展阅读节点唯一标识 |
| obj_token | `DQpOdZaWMoB4K6xA8UMcz8bRnLf` | 云文档 token（用于读写内容）|
| obj_type | `docx` | 文档类型 |
| parent_node_token | `SrtVwBvGFiMEAFkbevrcr34xnlb` | 父节点（一级节点） |

## 写入流程

1. 在「拓展阅读」节点下创建新文档：
   ```
   feishu_wiki(action=create, space_id=7621391289904516315, parent_node_token=DFmiwdgn4ic2D2kJPK6ca1XLnhd, obj_type=docx, title=...)
   ```
2. 用返回的 doc_token 写入内容：
   ```
   feishu_doc(action=write, doc_token=<返回的doc_token>, content=...)
   ```

## 安全说明

- `space_id` 是飞书公开导航 ID，本身不提供访问权限
- 权限控制由飞书机器人授权体系决定（机器人需加入知识库成员）
- Get笔记 API Key 等敏感信息不存储在此文件