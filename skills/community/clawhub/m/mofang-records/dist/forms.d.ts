/**
 * mofang_list_forms — 列出空间下所有表单
 * 接受 spaceHint（自然语言空间名），内部自动解析为 spaceId
 */
export interface ListFormsParams {
    spaceHint?: string;
}
export interface FormItem {
    label: string;
    id: string;
    updated?: string;
    version?: string;
}
export interface FormsResult {
    success: boolean;
    message: string;
    data?: FormItem[];
    spaceLabel?: string;
}
export declare function handler(params: ListFormsParams, context: {
    config: Record<string, string>;
}): Promise<FormsResult>;
//# sourceMappingURL=forms.d.ts.map