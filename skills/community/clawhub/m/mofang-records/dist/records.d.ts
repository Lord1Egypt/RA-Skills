/**
 * mofang_query_records — 查询记录
 * mofang_create_record — 创建记录
 * mofang_update_record — 修改记录
 * mofang_delete_record — 删除记录
 *
 * 所有 handler 接受 formHint + spaceHint，内部自动 resolve + 字段映射
 */
import { type BqFilter, type BqOrderBy } from './utils/bq-builder.js';
/** 魔方前端/部分文档里的 filter 结构（非 CLI 标准）；仅在未传 filters 时尝试转换 */
type LegacyFilterItem = {
    fieldName?: string;
    filterType?: string;
    value?: string;
    value2?: string;
};
export interface QueryRecordsParams {
    formHint: string;
    spaceHint?: string;
    page?: number;
    pageSize?: number;
    all?: boolean;
    filters?: BqFilter[];
    /** @deprecated 误用前端结构时请改 filters；无 filters 时本 handler 会尝试解析此项 */
    filter?: {
        items?: LegacyFilterItem[];
    };
    orderBy?: BqOrderBy;
}
export interface QueryRecordsResult {
    success: boolean;
    message: string;
    data?: {
        totalCount: number;
        records: Record<string, any>[];
        fieldLabels?: Record<string, string>;
    };
    spaceLabel?: string;
    formLabel?: string;
}
export declare function queryRecordsHandler(params: QueryRecordsParams, context: {
    config: Record<string, string>;
}): Promise<QueryRecordsResult>;
export interface CreateRecordParams {
    formHint: string;
    spaceHint?: string;
    data: Record<string, any>;
}
export interface MutationResult {
    success: boolean;
    message: string;
    data?: {
        errcode: string;
        errmsg: string;
        id?: string;
    };
    spaceLabel?: string;
    formLabel?: string;
}
export declare function createRecordHandler(params: CreateRecordParams, context: {
    config: Record<string, string>;
}): Promise<MutationResult>;
export interface UpdateRecordParams {
    formHint: string;
    spaceHint?: string;
    recordId: string;
    data: Record<string, any>;
}
export declare function updateRecordHandler(params: UpdateRecordParams, context: {
    config: Record<string, string>;
}): Promise<MutationResult>;
export interface DeleteRecordParams {
    formHint: string;
    spaceHint?: string;
    recordId: string;
}
export declare function deleteRecordHandler(params: DeleteRecordParams, context: {
    config: Record<string, string>;
}): Promise<MutationResult>;
export {};
//# sourceMappingURL=records.d.ts.map