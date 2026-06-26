/**
 * 字段定义获取 + label↔name 映射工具
 * 被 records/fields handler 内部调用
 */
import { type HttpClientConfig } from './http-client.js';
import { type BqFilter } from './bq-builder.js';
export interface OptionItem {
    value: string;
    content: string;
    display: string;
}
export interface FieldDef {
    name: string;
    label: string;
    type: string;
    required: boolean;
    defaultValue: string;
    editable: boolean;
    queryType: 'string' | 'region';
    valueDesc: string;
    options?: OptionItem[];
    maxlen?: string;
    maxvalue?: string;
    minvalue?: string;
    pointnum?: string;
    unique?: boolean;
    dependOn?: string;
    sourceFormId?: string;
    sourceFieldName?: string;
}
/**
 * 从 API 获取字段定义并解析为 FieldDef[]
 */
export declare function fetchFieldDefs(config: HttpClientConfig, spaceId: string, formId: string): Promise<{
    success: boolean;
    message: string;
    fields: FieldDef[];
}>;
/**
 * 构建 label→name 和 name→label 映射
 */
export declare function buildFieldMaps(fields: FieldDef[]): {
    labelToName: Map<string, string>;
    nameToLabel: Map<string, string>;
    nameSet: Set<string>;
};
/**
 * 将 data 对象的 key 从 label 或 name 统一映射为 name
 * 同时支持中文 label 和英文 name 作为 key
 */
export declare function mapDataKeys(fields: FieldDef[], data: Record<string, any>): {
    mapped: Record<string, any>;
    warnings: string[];
};
/**
 * 将 filters 中的 fieldName 从 label 转为 name（如果需要）
 */
export declare function mapFilterFieldNames(fields: FieldDef[], filters: BqFilter[]): {
    mapped: BqFilter[];
    warnings: string[];
};
/**
 * 生成可编辑字段的映射摘要（用于返回给 Agent）
 */
export declare function buildMappingSummary(fields: FieldDef[]): string;
//# sourceMappingURL=field-defs.d.ts.map