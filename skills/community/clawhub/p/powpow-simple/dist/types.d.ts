/**
 * POWPOW Simple Skill - 类型定义
 */
export interface OpenClawContext {
    userId?: string;
    powpowAuth?: PowpowAuthSession;
    emit: (event: string, data: any) => void;
    [key: string]: any;
}
export interface PowpowAuthSession {
    userId: string;
    username: string;
    token: string;
    badges: number;
    expiresAt: number;
}
export interface PowpowUser {
    id: string;
    username: string;
    nickname?: string;
    avatarUrl?: string;
    badges: number;
    firstVisit?: string;
}
export interface RegisterResponse {
    success: boolean;
    data?: {
        user_id: string;
        username: string;
        nickname?: string;
        avatar_url?: string;
        badges: number;
        created_at?: string;
    };
    error?: string;
}
export interface LoginResponse {
    success: boolean;
    user?: PowpowUser;
    token?: string;
    error?: string;
}
export interface DigitalHuman {
    id: string;
    name: string;
    description?: string;
    avatarUrl?: string;
    lat: number;
    lng: number;
    locationName?: string;
    userId: string;
    status: 'active' | 'inactive' | 'expired';
    expiresAt: string;
    createdAt: string;
    updatedAt: string;
}
export interface CreateDigitalHumanRequest {
    name: string;
    description?: string;
    avatarUrl?: string;
    lat: number;
    lng: number;
    locationName?: string;
    userId: string;
}
export interface CreateDigitalHumanResponse {
    success: boolean;
    digitalHuman?: DigitalHuman;
    badgesRemaining?: number;
    error?: string;
}
export interface ListDigitalHumansResponse {
    success: boolean;
    data?: DigitalHuman[];
    error?: string;
}
export interface RenewDigitalHumanResponse {
    success: boolean;
    digitalHuman?: DigitalHuman;
    badgesRemaining?: number;
    error?: string;
}
export interface UploadAvatarResponse {
    success: boolean;
    url?: string;
    error?: string;
}
export interface AmapGeocodeResult {
    formatted_address: string;
    location: string;
    province: string;
    city: string;
    district: string;
    street?: string;
    number?: string;
}
export interface AmapGeocodeResponse {
    status: string;
    info: string;
    infocode: string;
    count?: string;
    geocodes?: AmapGeocodeResult[];
}
export interface SkillConfig {
    powpowBaseUrl: string;
    amapKey: string;
    defaultAvatar: string;
}
export interface RegisterParams {
    username: string;
    password: string;
}
export interface LoginParams {
    username: string;
    password: string;
}
export interface RenewParams {
    digitalHumanId: string;
}
export interface UploadAvatarParams {
    filePath: string;
}
export interface SearchLocationParams {
    keyword: string;
}
export type CommandHandler<T = any> = (params: T, context: OpenClawContext) => Promise<any>;
export interface SkillCommand {
    name: string;
    description: string;
    parameters: Record<string, {
        type: string;
        required: boolean;
        description: string;
        default?: any;
    }>;
    handler: CommandHandler;
}
export interface SkillPlugin {
    name: string;
    version: string;
    description: string;
    commands: Record<string, SkillCommand>;
    init: (context: OpenClawContext) => void;
    destroy: () => void;
}
export declare class PowpowError extends Error {
    code: string;
    statusCode?: number | undefined;
    constructor(message: string, code: string, statusCode?: number | undefined);
}
export type LogLevel = 'debug' | 'info' | 'warn' | 'error';
export interface Logger {
    debug: (message: string, ...args: any[]) => void;
    info: (message: string, ...args: any[]) => void;
    warn: (message: string, ...args: any[]) => void;
    error: (message: string, ...args: any[]) => void;
}
//# sourceMappingURL=types.d.ts.map