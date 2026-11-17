import { JPEvent, AuditFilter } from '../core/types';
export declare class AuditStreamService {
    private streamPath;
    private events;
    private maxMemoryEvents;
    constructor(configDir?: string);
    emit(event: JPEvent): Promise<void>;
    query(filter: AuditFilter): Promise<JPEvent[]>;
    export(format?: 'jep' | 'json', events?: JPEvent[]): string;
    stats(): {
        total: number;
        byVerb: Record<string, number>;
        sizeBytes: number;
    };
    private load;
}
