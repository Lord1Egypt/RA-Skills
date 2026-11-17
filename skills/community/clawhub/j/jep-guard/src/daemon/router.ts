import {RouteRequest,RouteResult} from '../core/types';
import {JEPCore} from '../core/jep-core';
import {CausalGateService} from './gate';
export class CausalRouterService {
  constructor(private core:JEPCore,private gate:CausalGateService) {}
  async route(req:RouteRequest):Promise<RouteResult> {
    return {success:false,error:'Cross-skill execution requires a separately authenticated receiver; legacy /tmp routing is disabled'};
  }
}
