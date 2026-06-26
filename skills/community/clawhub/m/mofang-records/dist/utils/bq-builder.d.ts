/**
 * bq 查询条件构造器
 *
 * 语法: filter (CONCAT filter)*
 * filter: [!!]fieldName(operator):value
 * CONCAT: && | ||
 *
 * 文本值需要 _Base64 编码，数字/日期直接使用
 */
export interface BqFilter {
    fieldName: string;
    operator: string;
    value: string;
    not?: boolean;
    concat?: '&&' | '||';
}
export interface BqOrderBy {
    fieldName: string;
    direction: 'asc' | 'desc';
}
type QueryType = 'string' | 'region';
/**
 * 根据字段类型和名称判断查询类型
 */
export declare function getQueryType(fieldType: string, fieldName: string): QueryType;
export interface BuildBqOptions {
    filters?: BqFilter[];
    orderBy?: BqOrderBy;
    fieldQueryTypes?: Map<string, QueryType>;
}
/**
 * 构建完整的 bq 查询字符串（未经 encodeURIComponent）
 */
export declare function buildBq(options: BuildBqOptions): string;
/**
 * 构建完整的 bq 查询字符串并进行 URL 编码
 */
export declare function buildEncodedBq(options: BuildBqOptions): string;
export {};
//# sourceMappingURL=bq-builder.d.ts.map