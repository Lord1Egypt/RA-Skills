/**
 * POWPOW Simple Skill v1.0.0
 * 简化版 POWPOW 数字人创建 Skill
 */
declare const LOG_LEVELS: {
    DEBUG: number;
    INFO: number;
    WARN: number;
    ERROR: number;
};
declare function setLogLevel(level: keyof typeof LOG_LEVELS): void;
declare function setLogFile(filePath: string): void;
declare const logger: {
    debug: (msg: string, ...args: any[]) => void;
    info: (msg: string, ...args: any[]) => void;
    warn: (msg: string, ...args: any[]) => void;
    error: (msg: string, ...args: any[]) => void;
    setLevel: typeof setLogLevel;
    setLogFile: typeof setLogFile;
};
interface OpenClawContext {
    userId?: string;
    powpowAuth?: {
        userId: string;
        username: string;
        token: string;
        badges: number;
    };
    emit: (event: string, data: any) => void;
    [key: string]: any;
}
interface SkillConfig {
    powpowBaseUrl: string;
    amapKey: string;
    defaultAvatar: string;
    logLevel?: keyof typeof LOG_LEVELS;
    logFile?: string;
    feedbackEmail?: string;
}
export declare function createSkill(config?: Partial<SkillConfig>): {
    name: string;
    version: string;
    description: string;
    init: (context: OpenClawContext) => void;
    commands: {
        'powpow.start': () => Promise<{
            message: string;
            options: string[];
        }>;
        'powpow.register': (params: any) => Promise<{
            success: boolean;
            message: string;
            user: any;
            error?: undefined;
        } | {
            success: boolean;
            error: any;
            message?: undefined;
            user?: undefined;
        }>;
        'powpow.login': (params: any) => Promise<{
            success: boolean;
            message: string;
            user: any;
            error?: undefined;
        } | {
            success: boolean;
            error: any;
            message?: undefined;
            user?: undefined;
        }>;
        'powpow.logout': () => Promise<{
            success: boolean;
            message: string;
        }>;
        'powpow.status': () => Promise<{
            loggedIn: boolean;
            message: string;
            username?: undefined;
            badges?: undefined;
        } | {
            loggedIn: boolean;
            username: string;
            badges: number;
            message?: undefined;
        }>;
        'powpow.create': () => Promise<{
            error: string;
            step?: undefined;
            message?: undefined;
        } | {
            step: string;
            message: string;
            error?: undefined;
        }>;
        'powpow.create.submit': (params: any) => Promise<{
            error: string;
            success?: undefined;
            message?: undefined;
            digitalHuman?: undefined;
            badgesRemaining?: undefined;
        } | {
            success: boolean;
            message: string;
            digitalHuman: any;
            badgesRemaining: any;
            error?: undefined;
        } | {
            success: boolean;
            error: any;
            message?: undefined;
            digitalHuman?: undefined;
            badgesRemaining?: undefined;
        }>;
        'powpow.list': () => Promise<{
            error: string;
            success?: undefined;
            digitalHumans?: undefined;
            badges?: undefined;
        } | {
            success: boolean;
            digitalHumans: any;
            badges: number;
            error?: undefined;
        } | {
            success: boolean;
            error: any;
            digitalHumans?: undefined;
            badges?: undefined;
        }>;
        'powpow.renew': (params: any) => Promise<{
            error: string;
            success?: undefined;
            message?: undefined;
            badgesRemaining?: undefined;
        } | {
            success: boolean;
            message: string;
            badgesRemaining: any;
            error?: undefined;
        } | {
            success: boolean;
            error: any;
            message?: undefined;
            badgesRemaining?: undefined;
        }>;
        'powpow.uploadAvatar': (params: any) => Promise<{
            error: string;
            success?: undefined;
            url?: undefined;
        } | {
            success: boolean;
            url: any;
            error?: undefined;
        } | {
            success: boolean;
            error: any;
            url?: undefined;
        }>;
        'powpow.searchLocation': (params: any) => Promise<{
            success: boolean;
            locations: any;
            error?: undefined;
        } | {
            success: boolean;
            error: string;
            locations?: undefined;
        }>;
        'powpow.feedback': (params: any) => Promise<{
            success: boolean;
            message: string;
            error?: undefined;
        } | {
            success: boolean;
            error: string;
            message?: undefined;
        }>;
    };
};
export { logger };
export default createSkill;
//# sourceMappingURL=index.d.ts.map