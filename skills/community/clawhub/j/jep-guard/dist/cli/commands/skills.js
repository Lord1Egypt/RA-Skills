"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.skillsCommand = void 0;
const commander_1 = require("commander");
const registry_1 = require("../../daemon/registry");
exports.skillsCommand = new commander_1.Command('skills')
    .description('Manage registered skills')
    .argument('<action>', 'list, reputation')
    .action(async (action) => {
    const registry = new registry_1.SkillRegistryService();
    if (action === 'list') {
        const skills = registry.list();
        console.table(skills.map(s => ({
            ID: s.skill_id,
            Version: s.version,
            Risk: s.risk_level,
            Capabilities: s.capabilities.join(', '),
            LastSeen: new Date(s.last_seen).toISOString()
        })));
    }
});
//# sourceMappingURL=skills.js.map