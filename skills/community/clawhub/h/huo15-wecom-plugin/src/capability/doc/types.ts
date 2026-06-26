
export interface DocMemberEntry {
    userid?: string;
    partyid?: string;
    tagid?: string;
    /**
     * 权限位：1-查看，2-编辑，7-管理
     */
    auth?: number;
    type?: number; // 1:用户, 2:部门
    tmp_external_userid?: string;
}

export interface Node {
    begin: number;
    end: number;
    property: Property;
    type: NodeType;
    children: Node[];
    text?: string;
}

export enum NodeType {
    Document = "Document",
    MainStory = "MainStory",
    Section = "Section",
    Paragraph = "Paragraph",
    Table = "Table",
    TableRow = "TableRow",
    TableCell = "TableCell",
    Text = "Text",
    Drawing = "Drawing"
}

export interface Property {
    section_property?: SectionProperty;
    paragraph_property?: ParagraphProperty;
    run_property?: RunProperty;
    table_property?: TableProperty;
    table_row_property?: TableRowProperty;
    table_cell_property?: TableCellProperty;
    drawing_property?: DrawingProperty;
}

export interface SectionProperty {
    page_size?: PageSize;
    page_margins?: PageMargins;
}

export interface PageSize {
    width: number;
    height: number;
    orientation?: PageOrientation;
}

export interface PageOrientation {
    orientation: "PAGE_ORIENTATION_PORTRAIT" | "PAGE_ORIENTATION_LANDSCAPE" | "PAGE_ORIENTATION_UNSPECIFIED";
}

export interface PageMargins {
    top: number;
    right: number;
    bottom: number;
    left: number;
}

export interface ParagraphProperty {
    number_property?: NumberProperty;
    spacing?: Spacing;
    indent?: Indent;
    alignment_type?: AlignmentType;
    text_direction?: TextDirection;
}

export interface NumberProperty {
    nesting_level: number;
    number_id: string;
}

export interface Spacing {
    before?: number;
    after?: number;
    line?: number;
    line_rule?: LineSpacingRule;
}

export enum LineSpacingRule {
    UNSPECIFIED = "LINE_SPACING_RULE_UNSPECIFIED",
    AUTO = "LINE_SPACING_RULE_AUTO",
    EXACT = "LINE_SPACING_RULE_EXACT",
    AT_LEAST = "LINE_SPACING_RULE_AT_LEAST"
}

export interface Indent {
    left?: number;
    left_chars?: number;
    right?: number;
    right_chars?: number;
    hanging?: number;
    hanging_chars?: number;
    first_line?: number;
    first_line_chars?: number;
}

export enum AlignmentType {
    UNSPECIFIED = "ALIGNMENT_TYPE_UNSPECIFIED",
    CENTER = "ALIGNMENT_TYPE_CENTER",
    BOTH = "ALIGNMENT_TYPE_BOTH", // Justified
    DISTRIBUTE = "ALIGNMENT_TYPE_DISTRIBUTE",
    LEFT = "ALIGNMENT_TYPE_LEFT",
    RIGHT = "ALIGNMENT_TYPE_RIGHT"
}

export enum TextDirection {
    UNSPECIFIED = "TEXT_DIRECTION_UNSPECIFIED",
    RTL = "TEXT_DIRECTION_RIGHT_TO_LEFT",
    LTR = "TEXT_DIRECTION_LEFT_TO_RIGHT"
}

export interface RunProperty {
    font?: string;
    bold?: boolean;
    italics?: boolean;
    underline?: boolean;
    strike?: boolean;
    color?: string; // RRGGBB
    spacing?: number;
    size?: number; // half-points
    shading?: Shading;
    vertical_align?: TextVerticalAlign;
    is_placeholder?: boolean;
}

export interface Shading {
    foreground_color: string; // RRGGBB
    background_color: string; // RRGGBB
}

export enum TextVerticalAlign {
    UNSPECIFIED = "RUN_VERTICAL_ALIGN_UNSPECIFIED",
    BASELINE = "RUN_VERTICAL_ALIGN_BASELINE",
    SUPER_SCRIPT = "RUN_VERTICAL_ALIGN_SUPER_SCRIPT",
    SUB_SCRIPT = "RUN_VERTICAL_ALIGN_SUB_SCRIPT"
}

export interface TableProperty {
    table_width?: TableWidth;
    horizontal_alignment_type?: TableHorizontalAlignmentType;
    table_layout?: TableLayoutType;
}

export interface TableWidth {
    width: number;
    type: TableWidthType;
}

export enum TableHorizontalAlignmentType {
    UNSPECIFIED = "TABLE_HORIZONTAL_ALIGNMENT_TYPE_UNSPECIFIED",
    CENTER = "TABLE_HORIZONTAL_ALIGNMENT_TYPE_CENTER",
    LEFT = "TABLE_HORIZONTAL_ALIGNMENT_TYPE_LEFT",
    START = "TABLE_HORIZONTAL_ALIGNMENT_TYPE_START"
}

export enum TableLayoutType {
    UNSPECIFIED = "TABLE_LAYOUT_TYPE_UNSPECIFIED",
    FIXED = "TABLE_LAYOUT_TYPE_FIXED",
    AUTO_FIT = "TABLE_LAYOUT_TYPE_AUTO_FIT"
}

export enum TableWidthType {
    UNSPECIFIED = "TABLE_LAYOUT_TYPE_UNSPECIFIED",
    FIXED = "TABLE_LAYOUT_TYPE_FIXED",
    AUTO_FIT = "TABLE_LAYOUT_TYPE_AUTO_FIT"
}

export interface TableRowProperty {
    is_header?: boolean;
}

export interface TableCellProperty {
    table_cell_borders?: Borders;
    vertical_alignment?: VerticalAlignment;
}

export interface Borders {
    top?: BorderProperty;
    left?: BorderProperty;
    bottom?: BorderProperty;
    right?: BorderProperty;
}

export interface BorderProperty {
    color: string; // RRGGBB
    width: number;
}

export enum VerticalAlignment {
    UNSPECIFIED = "VERTICAL_ALIGNMENT__UNSPECIFIED",
    TOP = "VERTICAL_ALIGNMENT_TOP",
    CENTER = "VERTICAL_ALIGNMENT_CENTER",
    BOTH = "VERTICAL_ALIGNMENT_BOTH",
    BOTTOM = "VERTICAL_ALIGNMENT_BOTTOM"
}

export interface DrawingProperty {
    inline_keyword?: Inline;
    anchor?: Anchor;
    is_placeholder?: boolean;
}

export interface Inline {
    picture?: InlinePicture;
    addon?: InlineAddon;
}

export interface InlinePicture {
    uri: string;
    relative_rect?: RelativeRect;
    shape?: ShapeProperties;
}

export interface RelativeRect {
    left: number;
    top: number;
    right: number;
    bottom: number;
}

export interface ShapeProperties {
    transform?: Transform2D;
}

export interface Transform2D {
    extent?: PositiveSize2D;
    rotation?: number;
}

export interface PositiveSize2D {
    cx: number;
    cy: number;
}

export interface InlineAddon {
    addon_id: string;
    addon_source: AddonSourceType;
}

export enum AddonSourceType {
    UNSPECIFIED = "ADDON_SOURCE_TYPE_UNSPECIFIED",
    NONE = "ADDON_SOURCE_TYPE_NONE",
    LATEX = "ADDON_SOURCE_TYPE_LATEX",
    SIGN = "ADDON_SOURCE_TYPE_SIGN",
    SIGN_BAR = "ADDON_SOURCE_TYPE_SIGN_BAR"
}

export interface Anchor {
    picture?: AnchorPicture;
}

export interface AnchorPicture {
    uri: string;
    relative_rect?: RelativeRect;
    shape?: ShapeProperties;
    position_horizontal?: PositionHorizontal;
    position_vertical?: PositionVertical;
    wrap_none?: boolean;
    wrap_square?: WrapSquare;
    wrap_top_and_bottom?: boolean;
    behind_doc?: boolean;
    allow_overlap?: boolean;
}

export interface PositionHorizontal {
    pos_offset: number;
    relative_from: RelativeFromHorizontal;
}

export enum RelativeFromHorizontal {
    UNSPECIFIED = "RELATIVE_FROM_HORIZONTAL_UNSPECIFIED",
    MARGIN = "RELATIVE_FROM_HORIZONTAL_MARGIN",
    PAGE = "RELATIVE_FROM_HORIZONTAL_PAGE",
    COLUMN = "RELATIVE_FROM_HORIZONTAL_COLUMN",
    CHARACTER = "RELATIVE_FROM_HORIZONTAL_CHARACTER",
    LEFT_MARGIN = "RELATIVE_FROM_HORIZONTAL_LEFT_MARGIN",
    RIGHT_MARGIN = "RELATIVE_FROM_HORIZONTAL_RIGHT_MARGIN",
    INSIDE_MARGIN = "RELATIVE_FROM_HORIZONTAL_INSIDE_MARGIN",
    OUTSIDE_MARGIN = "RELATIVE_FROM_HORIZONTAL_OUTSIDE_MARGIN"
}

export interface PositionVertical {
    pos_offset: number;
    relative_from: RelativeFromVertical;
}

export enum RelativeFromVertical {
    UNSPECIFIED = "RELATIVE_FROM_VERTICAL_UNSPECIFIED",
    MARGIN = "RELATIVE_FROM_VERTICAL_MARGIN",
    PAGE = "RELATIVE_FROM_VERTICAL_PAGE",
    PARAGRAPH = "RELATIVE_FROM_VERTICAL_PARAGRAPH",
    LINE = "RELATIVE_FROM_VERTICAL_LINE",
    TOP_MARGIN = "RELATIVE_FROM_VERTICAL_TOP_MARGIN",
    BOTTOM_MARGIN = "RELATIVE_FROM_VERTICAL_BOTTOM_MARGIN",
    INSIDE_MARGIN = "RELATIVE_FROM_VERTICAL_INSIDE_MARGIN",
    OUTSIDE_MARGIN = "RELATIVE_FROM_VERTICAL_OUTSIDE_MARGIN"
}

export interface WrapSquare {
    wrap_text: WrapText;
}

export enum WrapText {
    UNSPECIFIED = "WRAP_TEXT_BOTH_UNSPECIFIED",
    BOTH_SIDES = "WRAP_TEXT_BOTH_SIDES",
    LEFT = "WRAP_TEXT_LEFT",
    RIGHT = "WRAP_TEXT_RIGHT",
    LARGEST = "WRAP_TEXT_LARGEST"
}


// --- Update Requests ---

export interface Location {
    index: number;
}

export interface Range {
    start_index: number;
    length: number;
}

export interface ReplaceTextRequest {
    text: string;
    ranges: Range[];  // 最多 10 个范围
}

export interface InsertTextRequest {
    text: string;
    location: Location;
}

export interface DeleteContentRequest {
    range: Range;
}

export interface InsertImageRequest {
    image_id: string;
    location: Location;
    width?: number;
    height?: number;
}

export interface InsertPageBreakRequest {
    location: Location;
}

export interface InsertTableRequest {
    rows: number;
    cols: number;
    location: Location;
}

export interface InsertParagraphRequest {
    location: Location;
}

export interface TextProperty {
    bold?: boolean;
    italics?: boolean;
    underline?: boolean;
    strikethrough?: boolean;
    color?: string;
    background_color?: string;
    font_size?: number;
}

export interface UpdateTextPropertyRequest {
    text_property: TextProperty;
    ranges: Range[];  // 最多 10 个范围
}

export interface UpdateRequest {
    replace_text?: ReplaceTextRequest;
    insert_text?: InsertTextRequest;
    delete_content?: DeleteContentRequest;
    insert_image?: InsertImageRequest;
    insert_page_break?: InsertPageBreakRequest;
    insert_table?: InsertTableRequest;
    insert_paragraph?: InsertParagraphRequest;
    update_text_property?: UpdateTextPropertyRequest;
}

export interface BatchUpdateDocResponse {
    errcode: number;
    errmsg: string;
    responses?: Array<{
        insert_text_response?: { end_location: Location };
        delete_content_response?: { end_location: Location };
        replace_text_response?: { occurances: number };
        insert_image_response?: { image_id: string };
        insert_table_response?: { table_id: string };
        insert_paragraph_response?: { paragraph_id: string };
        update_text_property_response?: Record<string, never>;
    }>;
}

export interface GetDocContentResponse {
    errcode: number;
    errmsg: string;
    version: number;
    document: Node;
}

// --- Collect Form (收集表) Types ---

export interface FormQuestionOption {
    key: number;           // 必填，选项 key 从 1 开始
    value: string;         // 必填，选项内容
    status?: number;       // 1 正常，2 删除。创建时不传则自动填充为 1
}

export interface FormQuestion {
    question_id: number;                           // 必填，问题 ID 从 1 开始（家校从 2 开始）
    title: string;                                 // 必填，问题标题
    pos: number;                                   // 必填，问题序号从 1 开始
    status?: number;                               // 1 正常，2 删除。创建时不传则自动填充为 1
    reply_type: number;                            // 必填，问题类型（1-22）
    must_reply: boolean;                           // 必填，是否必答
    note?: string;                                 // 可选，备注
    placeholder?: string;                          // 可选，输入提示
    question_extend_setting?: FormQuestionExtendSetting;  // 可选，题型扩展设置
    option_item?: FormQuestionOption[];            // 单选/多选/下拉列表必填，创建时不传 status 则自动填充为 1
}

export interface FormQuestionExtendSetting {
    // 文本（reply_type=1）
    text_setting?: {
        validation_type?: number;      // 0 字符个数，1 数字，2 邮箱，3 网址，4 身份证，5 手机号，6 固定电话
        validation_detail?: number;    // 根据 validation_type 选择
        char_len?: number;             // 字符长度 ≤4000
        number_min?: number;           // 数字最小值
        number_max?: number;           // 数字最大值
    };
    // 单选（reply_type=2）
    radio_setting?: {
        add_other_option?: boolean;    // 是否增加"其他"选项
    };
    // 多选（reply_type=3）
    checkbox_setting?: {
        add_other_option?: boolean;    // 是否增加"其他"选项
        type?: number;                 // 0 不限制，1 至少，2 最多，3 固定
        number?: number;               // 当 type=1/2/3 时必填
    };
    // 位置（reply_type=5）
    location_setting?: {
        location_type?: number;        // 0 省市区街道 + 详细，1 省/市，2 省/市/区，3 省/市/区/街道，4 自动定位
        distance_type?: number;        // 0 当前，1 附近 100 米，2 附近 200 米，3 附近 300 米
    };
    // 图片（reply_type=9）
    image_setting?: {
        camera_only?: boolean;         // 是否仅限手机拍照
        upload_image_limit?: {
            count_limit_type?: number; // 0 等于，1 小于等于
            count?: number;            // 1~9
            max_size?: number;         // MB，最大 3000
        };
    };
    // 文件（reply_type=10）
    file_setting?: {
        upload_file_limit?: {
            count_limit_type?: number;
            count?: number;
            max_size?: number;
        };
    };
    // 日期（reply_type=11）
    date_setting?: {
        date_format_type?: number;     // 0 年月日时分，1 年月日，2 年月
    };
    // 时间（reply_type=14）
    time_setting?: {
        time_format_type?: number;     // 0 时分，1 时分秒
    };
    // 体温（reply_type=16）
    temperature_setting?: {
        unit_type?: number;            // 0 摄氏度，1 华氏度
    };
    // 部门（reply_type=18）
    department_setting?: {
        allow_multiple_selection?: boolean;  // 是否允许多选
    };
    // 成员（reply_type=19）
    member_setting?: {
        allow_multiple_selection?: boolean;  // 是否允许多选
    };
    // 时长（reply_type=22）
    duration_setting?: {
        time_scale?: number;           // 1 按天，2 按小时
        date_type?: number;            // 1 自然日，2 工作日
        day_range?: number;            // 1~24，默认 24
    };
}

export interface FormSetting {
    fill_out_auth?: number;                    // 0 所有人，1 指定人/部门，4 家校所有范围
    fill_in_range?: {                          // 当 fill_out_auth=1 时必填
        userids?: string[];                    // 成员列表
        departmentids?: number[];              // 部门列表
    };
    setting_manager_range?: {                  // 可选，管理员
        userids?: string[];
    };
    timed_repeat_info?: {                      // 可选，定时重复设置
        enable?: boolean;                      // 是否开启
        remind_time?: number;                  // 提醒时间戳（秒）
        repeat_type?: number;                  // 0 每周，1 每天，2 每月
        week_flag?: number;                    // 每周几，bit 组合（周一至周日对应 bit0-6）
        skip_holiday?: boolean;                // 是否跳过节假日（repeat_type=1 有效）
        day_of_month?: number;                 // 每月第几天（repeat_type=2 有效）
        fork_finish_type?: number;             // 补填：0 允许，1 仅当天，2 最后五天，3 一个月内，4 下一次生成前
    };
    allow_multi_fill?: boolean;                // 是否允许多人提交多份
    timed_finish?: number;                     // 定时关闭时间戳（秒，与定时重复互斥）
    can_anonymous?: boolean;                   // 是否支持匿名
    can_notify_submit?: boolean;               // 是否有回复时提醒
}

export interface FormInfo {
    form_title: string;                        // 必填，收集表标题
    form_desc?: string;                        // 可选，收集表描述
    form_header?: string;                      // 可选，背景图链接
    form_question: {                           // 必填，问题列表
        items: FormQuestion[];                 // 问题数组 ≤200
    };
    form_setting?: FormSetting;                // 可选，收集表设置
}

export interface CreateCollectRequest {
    spaceid?: string;                          // 可选，空间 ID
    fatherid?: string;                         // 可选，父目录 fileid
    form_info: FormInfo;                       // 必填，收集表信息
}

export interface CreateCollectResponse {
    errcode: number;
    errmsg: string;
    formid: string;
}

// --- Spreadsheet (在线表格) Types ---

export interface SheetProperties {
    sheet_id: string;
    title: string;
    row_count: number;
    column_count: number;
}

export interface GetSheetPropertiesResponse {
    errcode: number;
    errmsg: string;
    properties: SheetProperties[];
}

export interface GridData {
    start_row: number;       // 起始行号（从 0 开始）
    start_column: number;    // 起始列号（从 0 开始）
    rows: RowData[];         // 行数据列表
}

export interface RowData {
    values: CellData[];      // 该行各列单元格数据
}

export interface CellData {
    cell_value?: CellValue;    // 单元格数据内容（可选）
    cell_format?: CellFormat;  // 单元格样式（可选）
}

export interface CellValue {
    text?: string;           // 纯文本
    link?: Link;             // 超链接（与 text 互斥）
}

export interface Link {
    url: string;             // 链接地址
    text: string;            // 链接显示文本
}

export interface CellFormat {
    text_format?: TextFormat;  // 文字样式
}

export interface TextFormat {
    font?: string;           // 字体名称（如 "Microsoft YaHei"）
    font_size?: number;      // 字号，最大 72
    bold?: boolean;
    italic?: boolean;
    strikethrough?: boolean;
    underline?: boolean;
    color?: Color;           // 文字颜色（RGBA）
}

export interface Color {
    red: number;     // 0~255
    green: number;   // 0~255
    blue: number;    // 0~255
    alpha?: number;  // 0~255，默认 255（不透明），可选
}

export enum Dimension {
    ROW = "ROW",         // 行
    COLUMN = "COLUMN"    // 列
}

// Batch Update Requests
export interface AddSheetRequest {
    add_sheet_request: {
        title: string;
        row_count?: number;
        column_count?: number;
    };
}

export interface DeleteSheetRequest {
    delete_sheet_request: {
        sheet_id: string;
    };
}

export interface UpdateRangeRequest {
    update_range_request: {
        sheet_id: string;
        grid_data: GridData;
    };
}

export interface DeleteDimensionRequest {
    delete_dimension_request: {
        sheet_id: string;
        dimension: Dimension;
        start_index: number;    // 从 1 开始
        end_index: number;      // 从 1 开始，不包含
    };
}

export type SpreadsheetUpdateRequest = 
    | AddSheetRequest
    | DeleteSheetRequest
    | UpdateRangeRequest
    | DeleteDimensionRequest;

export interface SpreadsheetBatchUpdateResponse {
    errcode: number;
    errmsg: string;
    data?: {
        responses: Array<{
            add_sheet_response?: {
                properties: SheetProperties;
            };
            delete_sheet_response?: {
                sheet_id: string;
            };
            update_range_response?: {
                updated_cells: number;
            };
            delete_dimension_response?: {
                deleted: number;
            };
        }>;
    };
}

export interface GetSheetRangeDataResponse {
    errcode: number;
    errmsg: string;
    data: {
        result: GridData;
    };
}

// --- Smart Table Records & Fields Types ---

export interface SmartTableRecord {
    record_id: string;
    create_time?: string;
    update_time?: string;
    values: Record<string, any>;
    creator_name?: string;
    updater_name?: string;
}

export interface SmartTableGetRecordsResponse {
    errcode: number;
    errmsg: string;
    records?: SmartTableRecord[];
    total?: number;
    has_more?: boolean;
    next?: number;
    ver?: number;
}

export interface SmartTableField {
    field_id: string;
    field_title: string;
    field_type: string;
    property_number?: any;
    property_checkbox?: any;
    property_date_time?: any;
    property_attachment?: any;
    property_user?: any;
    property_url?: any;
    property_select?: any;
    property_created_time?: any;
    property_modified_time?: any;
    property_progress?: any;
    property_single_select?: any;
    property_reference?: any;
    property_location?: any;
    property_auto_number?: any;
    property_currency?: any;
    property_ww_group?: any;
    property_percentage?: any;
    property_barcode?: any;
    property_image?: any;
    property_phone_number?: any;
    property_email?: any;
}

export interface SmartTableGetFieldsResponse {
    errcode: number;
    errmsg: string;
    fields?: SmartTableField[];
    total?: number;
    has_more?: boolean;
    next?: number;
}

export interface SmartTableView {
    view_id: string;
    view_title: string;
    view_type: string;
    is_visible?: boolean;
    type?: string;
    property?: any;
}

export interface SmartTableGetViewsResponse {
    errcode: number;
    errmsg: string;
    views?: SmartTableView[];
    total?: number;
    has_more?: boolean;
    next?: number;
}

export interface SmartTableFieldGroup {
    field_group_id: string;
    name: string;
    children?: { field_id: string }[];
}

export interface SmartTableGetGroupsResponse {
    errcode: number;
    errmsg: string;
    field_groups?: SmartTableFieldGroup[];
    total?: number;
    has_more?: boolean;
    next?: number;
}

export interface SmartTableSheetPriv {
    sheet_id: string;
    priv: number;
    can_insert_record?: boolean;
    can_delete_record?: boolean;
    can_create_modify_delete_view?: boolean;
    field_priv?: any;
    record_priv?: any;
    clear?: boolean;
}

export interface SmartTableGetSheetPrivResponse {
    errcode: number;
    errmsg: string;
    rule_list?: any[];
}

export interface SmartTableCreateRuleResponse {
    errcode: number;
    errmsg: string;
    rule_id?: number;
}
