# Local Memory 本地记忆技能
## 功能说明
纯本地运行的AI记忆管理技能，完全免费、数据本地存储，解决AI对话健忘、上下文不足的问题：
- 自动从对话中提取关键事实、用户偏好、项目进展、待办事项等记忆点
- 每轮对话前自动检索相关记忆注入上下文，让AI永远记得你的信息
- 支持手动管理记忆的命令
- 自动处理记忆更新、冲突和过期，不需要人工维护
- 纯本地运行，不需要任何外部API或付费服务，隐私安全
## 触发规则
自动全局触发，所有对话自动启用记忆功能，无需手动调用
## 使用命令
| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `/remember <内容>` | 手动保存信息到记忆库 | `/remember 我喜欢用TypeScript写代码` |
| `/recall <关键词>` | 查询相关记忆 | `/recall 部署相关的命令` |
| `/forget <关键词>` | 删除相关记忆 | `/forget 旧的服务器密码` |
| `/memory-list` | 查看所有记忆列表 | `/memory-list` |
## 配置
所有配置在`config.json`中修改：
```json
{
  "auto_extract": true, // 自动提取记忆
  "auto_inject": true, // 自动注入上下文
  "max_memory_results": 5, // 每次最多注入的记忆数量
  "embedding_model": "bge-small-zh", // 本地embedding模型
  "expire_days": 90 // 记忆默认过期时间（天）
}
```
## 存储路径
- 数据库：`db/memory.db`
- 向量模型：`lib/models/`
