package com.teamtodo.sync;

/**
 * 服务器 API 接口定义（统一存放）。
 * 暂不实现，后续扩展多人协作功能时在此添加。
 */
public interface ServerApi {

    // ========== 待办相关 ==========
    // GET  /api/todos              - 获取待办列表
    // GET  /api/todos/{id}         - 获取单个待办
    // POST /api/todos              - 创建待办
    // PUT  /api/todos/{id}         - 更新待办
    // DELETE /api/todos/{id}       - 删除待办

    // ========== 用户相关 ==========
    // GET  /api/users              - 获取用户列表
    // POST /api/users              - 创建/更新用户

    // ========== 评论相关 ==========
    // GET  /api/todos/{id}/comments - 获取评论
    // POST /api/todos/{id}/comments - 添加评论

    // ========== 提醒相关 ==========
    // GET  /api/todos/{id}/reminders - 获取提醒
    // POST /api/todos/{id}/reminders - 创建提醒

    // ========== 同步相关 ==========
    // POST /api/sync/push          - 推送本地变更
    // POST /api/sync/pull          - 拉取远程变更
    // GET  /api/sync/status        - 同步状态
}
