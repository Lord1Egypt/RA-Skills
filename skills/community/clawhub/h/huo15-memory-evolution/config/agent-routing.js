/**
 * huo15-memory-evolution: Agent 路径路由配置
 * 
 * 功能: 根据 OC_AGENT_ID 环境变量，确定当前 agent 的记忆路径
 * 
 * 使用方式:
 *   const routing = require('./agent-routing.js');
 *   const paths = routing.getMemoryPaths();
 *   console.log(paths.memoryMd);    // MEMORY.md 路径
 *   console.log(paths.memoryDir);    // memory/ 目录路径
 *   console.log(paths.indexJson);    // index.json 路径
 */

function getMemoryPaths(agentId) {
    const home = process.env.HOME || '/tmp';
    const openclawDir = `${home}/.openclaw`;
    
    // 默认值：主 agent
    let base = `${openclawDir}/workspace`;
    let type = 'private';  // private | shared
    let agentScope = 'main';
    
    if (agentId) {
        if (agentId === 'main') {
            base = `${openclawDir}/workspace`;
            type = 'private';
            agentScope = 'main';
        } else if (agentId.startsWith('wecom-dm-')) {
            // 企微私聊 agent
            base = `${openclawDir}/workspace-${agentId}`;
            type = 'private';
            agentScope = 'personal';
        } else if (agentId.startsWith('wecom-group-')) {
            // 企微群聊 agent
            base = `${openclawDir}/workspace-${agentId}`;
            type = 'shared';
            agentScope = 'team';
        } else if (agentId.startsWith('discord-')) {
            // Discord agent
            base = `${openclawDir}/workspace-${agentId}`;
            type = agentId.includes('group') ? 'shared' : 'private';
            agentScope = agentId.includes('group') ? 'team' : 'personal';
        } else {
            // 其他 agent
            base = `${openclawDir}/workspace-${agentId}`;
            type = 'private';
            agentScope = 'personal';
        }
    }
    
    return {
        base,           // 工作区根目录
        memoryDir: `${base}/memory`,      // memory/ 目录
        memoryMd: `${base}/MEMORY.md`,       // MEMORY.md 路径
        indexJson: `${base}/memory/index.json`,      // index.json 路径
        type,           // private | shared
        agentScope,     // main | personal | team
        agentId: agentId || 'main'
    };
}

// 兼容 CommonJS 和 ES Module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getMemoryPaths };
}
