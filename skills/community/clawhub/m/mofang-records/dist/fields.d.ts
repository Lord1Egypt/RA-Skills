/**
 * mofang_get_field_definitions — 获取表单字段结构定义
 * 接受 formHint + spaceHint，内部自动解析为 spaceId + formId
 */
import { type FieldDef } from './utils/field-defs.js';
export type { FieldDef, OptionItem } from './utils/field-defs.js';
export interface GetFieldDefsParams {
    formHint: string;
    spaceHint?: string;
}
export interface FieldDefsResult {
    success: boolean;
    message: string;
    data?: FieldDef[];
    fieldMapping?: string;
    spaceLabel?: string;
    formLabel?: string;
}
export declare function handler(params: GetFieldDefsParams, context: {
    config: Record<string, string>;
}): Promise<FieldDefsResult>;
//# sourceMappingURL=fields.d.ts.map