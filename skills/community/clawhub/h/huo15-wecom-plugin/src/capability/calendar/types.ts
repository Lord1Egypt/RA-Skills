// ============================================================================
// Calendar Types (日历类型定义)
// 完整参考企业微信官方 API 文档：https://developer.work.weixin.qq.com/document/path/93329
// ============================================================================

// --- Calendar Interfaces ---

export interface CalendarSharesEntry {
    userid: string;
    permission?: 1 | 3;  // 1: 可查看，3: 仅查看闲忙状态
}

export interface CalendarPublicRange {
    userids?: string[];   // 公开的成员列表，最多 1000 个
    partyids?: number[];  // 公开的部门列表，最多 100 个
}

export interface CreateCalendarRequest {
    calendar: {
        admins?: string[];           // 日历管理员，最多 3 人
        set_as_default?: 0 | 1;      // 是否设为默认日历，第三方应用不支持
        summary: string;             // 日历标题，1-128 字符
        color: string;               // RGB 颜色编码，如 "#0000FF"
        description?: string;        // 日历描述，0-512 字符
        shares?: CalendarSharesEntry[];  // 通知范围成员，最多 2000 人
        is_public?: 0 | 1;           // 是否公共日历
        public_range?: CalendarPublicRange;  // 公开范围
        is_corp_calendar?: 0 | 1;    // 是否全员日历
    };
    agentid?: number;
}

export interface UpdateCalendarRequest {
    skip_public_range?: 0 | 1;
    calendar: {
        cal_id: string;
        admins?: string[];
        summary: string;
        color: string;
        description?: string;
        shares?: CalendarSharesEntry[];
        public_range?: CalendarPublicRange;
    };
}

export interface GetCalendarRequest {
    cal_id_list: string[];
}

export interface DeleteCalendarRequest {
    cal_id: string;
}

export interface CalendarInfo {
    cal_id: string;
    admins?: string[];
    summary: string;
    color: string;
    description?: string;
    shares?: CalendarSharesEntry[];
    is_public?: 0 | 1;
    public_range?: CalendarPublicRange;
    is_corp_calendar?: 0 | 1;
}

// --- Schedule Interfaces ---

export interface ScheduleAttendee {
    userid: string;
}

export interface ScheduleReminders {
    is_remind?: 0 | 1;
    is_repeat?: 0 | 1;
    remind_before_event_secs?: number;
    remind_time_diffs?: number[];
    repeat_type?: 0 | 1 | 2 | 5 | 7;
    repeat_until?: number;
    is_custom_repeat?: 0 | 1;
    repeat_interval?: number;
    repeat_day_of_week?: number[];
    repeat_day_of_month?: number[];
    timezone?: number;
    exclude_time_list?: Array<{ start_time: number }>;
}

export interface CreateScheduleRequest {
    schedule: {
        admins?: string[];
        start_time: number;
        end_time: number;
        is_whole_day?: 0 | 1;
        attendees?: ScheduleAttendee[];
        summary?: string;
        description?: string;
        reminders?: ScheduleReminders;
        location?: string;
        cal_id?: string;
    };
    agentid?: number;
}

export interface UpdateScheduleRequest {
    skip_attendees?: 0 | 1;
    op_mode?: 0 | 1 | 2;
    op_start_time?: number;
    schedule: {
        schedule_id: string;
        admins?: string[];
        start_time: number;
        end_time: number;
        is_whole_day?: 0 | 1;
        attendees?: ScheduleAttendee[];
        summary?: string;
        description?: string;
        reminders?: ScheduleReminders;
        location?: string;
    };
}

export interface AddScheduleAttendeesRequest {
    schedule_id: string;
    attendees: ScheduleAttendee[];
}

export interface DeleteScheduleAttendeesRequest {
    schedule_id: string;
    attendees: ScheduleAttendee[];
}

export interface GetScheduleByCalendarRequest {
    cal_id: string;
    offset?: number;
    limit?: number;
}

export interface GetScheduleRequest {
    schedule_id_list: string[];
}

export interface DeleteScheduleRequest {
    schedule_id: string;
    op_mode?: 0 | 1 | 2;
    op_start_time?: number;
}

export interface ScheduleAttendeeWithStatus {
    userid: string;
    response_status: 0 | 1 | 2 | 3 | 4;
}

export interface ScheduleInfo {
    schedule_id: string;
    sequence?: number;
    admins?: string[];
    organizer?: string;
    attendees?: ScheduleAttendeeWithStatus[];
    summary?: string;
    description?: string;
    reminders?: ScheduleReminders;
    location?: string;
    start_time: number;
    end_time: number;
    status?: 0 | 1;
    cal_id?: string;
    is_whole_day?: 0 | 1;
    meetingroom_id?: string;
}

// --- System Calendar Interfaces ---

export interface GetSystemCalendarIdRequest {
    userid: string;
}

export interface CreateSystemScheduleRequest {
    schedule: {
        organizer: string;
        start_time: number;
        end_time: number;
        is_whole_day?: 0 | 1;
        attendees?: ScheduleAttendee[];
        summary?: string;
        description?: string;
        reminders?: ScheduleReminders;
        location?: string;
    };
}

export interface RespondScheduleRequest {
    schedule_id: string;
    op_mode?: 0 | 1 | 2;
    op_start_time?: number;
    attendee: string;
    response_status: 1 | 2 | 4;
}

export interface SyncScheduleRequest {
    cal_id: string;
    cursor?: string;
    limit?: number;
}

// --- Response Interfaces ---

export interface CreateCalendarResponse {
    errcode: number;
    errmsg: string;
    cal_id: string;
    fail_result?: { shares?: Array<{ errcode: number; errmsg: string; userid: string; }>; };
}

export interface UpdateCalendarResponse {
    errcode: number;
    errmsg: string;
    fail_result?: { shares?: Array<{ errcode: number; errmsg: string; userid: string; }>; };
}

export interface GetCalendarResponse {
    errcode: number;
    errmsg: string;
    calendar_list: CalendarInfo[];
}

export interface DeleteCalendarResponse {
    errcode: number;
    errmsg: string;
}

export interface CreateScheduleResponse {
    errcode: number;
    errmsg: string;
    schedule_id: string;
}

export interface UpdateScheduleResponse {
    errcode: number;
    errmsg: string;
    schedule_id?: string;
}

export interface GetScheduleByCalendarResponse {
    errcode: number;
    errmsg: string;
    schedule_list: ScheduleInfo[];
}

export interface GetScheduleResponse {
    errcode: number;
    errmsg: string;
    schedule_list: ScheduleInfo[];
    meeting_code?: string;
    meeting_link?: string;
}

export interface DeleteScheduleResponse {
    errcode: number;
    errmsg: string;
}

export interface AddScheduleAttendeesResponse {
    errcode: number;
    errmsg: string;
}

export interface DeleteScheduleAttendeesResponse {
    errcode: number;
    errmsg: string;
}

export interface GetSystemCalendarIdResponse {
    errcode: number;
    errmsg: string;
    cal_id: string;
}

export interface RespondScheduleResponse {
    errcode: number;
    errmsg: string;
}

export interface SyncScheduleResponse {
    errcode: number;
    errmsg: string;
    next_cursor: string;
    schedule_list: ScheduleInfo[];
}

// --- Callback Event Types ---

export interface CalendarCallbackEvent {
    ToUserName: string;
    FromUserName: string;
    CreateTime: number;
    MsgType: "event";
    Event: "delete_calendar" | "modify_calendar" | "modify_schedule" | "delete_schedule" | "respond_schedule" | "add_schedule";
    CalId: string;
    ScheduleId?: string;
}

// --- Constants ---

export const REMINDER_BEFORE_EVENT_VALUES = [0, 300, 900, 3600, 86400] as const;
export const REMINDER_TIME_DIFFS_VALUES = [0, -300, -900, -3600, -86400, 32400, -172800, -604800] as const;
export const REPEAT_TYPE = { DAILY: 0, WEEKLY: 1, MONTHLY: 2, YEARLY: 5, WORKDAY: 7 } as const;
export const PERMISSION_TYPE = { VIEW: 1, BUSY_ONLY: 3 } as const;
export const SCHEDULE_RESPONSE_STATUS = { UNPROCESSED: 0, TENTATIVE: 1, ACCEPTED: 2, ACCEPTED_ONCE: 3, DECLINED: 4 } as const;
export const OP_MODE = { ALL: 0, THIS_ONLY: 1, FUTURE: 2 } as const;
export const SCHEDULE_STATUS = { NORMAL: 0, CANCELLED: 1 } as const;
