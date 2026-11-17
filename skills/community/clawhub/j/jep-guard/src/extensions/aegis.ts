import {Extension} from '../core/types';
const extension:Extension={name:'ext.aegis',version:'2.0',async init(){},async evaluate(){return {action:'review',rule_matched:'explicit_trusted_adapter_required'};}};
export default extension;
