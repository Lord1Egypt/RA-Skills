import { RouteRequest, RouteResult } from '../core/types';
import { JEPCore } from '../core/jep-core';
import { CausalGateService } from './gate';
export declare class CausalRouterService {
    private core;
    private gate;
    constructor(core: JEPCore, gate: CausalGateService);
    route(req: RouteRequest): Promise<RouteResult>;
}
