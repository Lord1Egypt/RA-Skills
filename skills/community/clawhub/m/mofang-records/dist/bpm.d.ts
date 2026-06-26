/**
 * BPM / Activiti：待办列表、条件查询、任务详情、提交(complete)、转办(delegate)、认领/归还(claim/resolve)、跳转(abort/rollback/recovery)、事务(加签等前置)。
 */
/** GET /runtime/tasks 分页列表（个人待办 / 组待办 / 委托待办） */
export declare function listBpmTasksHandler(params: {
    mode?: 'assignee' | 'candidate' | 'delegated';
    page?: number;
    pageSize?: number;
    processDefinitionKey?: string;
    descriptionLike?: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
/** POST /query/tasks，可按表单/记录/流程名等定位（与 Java MFBPMGETTASK 条件一致） */
export declare function queryBpmTasksHandler(params: {
    formHint?: string;
    spaceHint?: string;
    recordId?: string;
    processDefinitionKey?: string;
    processDefinitionName?: string;
    taskName?: string;
    taskDefinitionKey?: string;
    assigneeUserId?: string;
    includeProcessVariables?: boolean;
    page?: number;
    pageSize?: number;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
/** 任务详情 + 变量（定位办理上下文） */
export declare function getBpmTaskHandler(params: {
    taskId: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
/**
 * 完成任务（提交）：默认按服务端公式逻辑同步变量后 complete；可简化为仅 POST complete。
 */
export declare function completeBpmTaskHandler(params: {
    taskId: string;
    /** 为 true 且提供 variables 时，只 POST {action:complete, variables}，不做 DELETE/回写变量 */
    simple?: boolean;
    /** 与 simple 联用，或直接作为 complete 体中的 variables */
    variables?: unknown[];
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
export declare function delegateBpmTaskHandler(params: {
    taskId: string;
    assignee: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
export declare function claimBpmTaskHandler(params: {
    taskId: string;
    assignee?: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
export declare function resolveBpmTaskHandler(params: {
    taskId: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
/** abort：默认识别第一个 endEvent；rollback：可按用户任务显示名解析；recovery：必须提供 jumpTargetId */
export declare function jumpBpmTaskHandler(params: {
    taskId: string;
    kind: 'abort' | 'rollback' | 'recovery';
    jumpTargetId?: string;
    targetTaskName?: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
/**
 * 开启 BPM 事务（如并行加签前），对应 RecordPanel.beforeSaveForBpm。
 * 返回 transactionId，关闭事务时需原样传入 mofang_bpm_close_transaction。
 */
export declare function openBpmTransactionHandler(params: {
    processKey?: string;
    processInstId?: string;
    taskId?: string;
    processName?: string;
    taskName?: string;
    taskAction: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
export declare function closeBpmTransactionHandler(params: {
    transactionId: string;
}, context: {
    config: Record<string, string>;
}): Promise<{
    success: boolean;
    message: string;
    data?: any;
}>;
//# sourceMappingURL=bpm.d.ts.map