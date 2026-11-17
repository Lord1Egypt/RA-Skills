"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.dashboardCommand = void 0;
const commander_1 = require("commander");
const audit_1 = require("../../daemon/audit");
const registry_1 = require("../../daemon/registry");
exports.dashboardCommand = new commander_1.Command('dashboard')
    .description('Show interactive dashboard')
    .action(async () => {
    const audit = new audit_1.AuditStreamService();
    const registry = new registry_1.SkillRegistryService();
    const stats = audit.stats();
    const skills = registry.list();
    console.log('\n┌─ JEP Guard Dashboard ─────────────────────┐');
    console.log('│                                           │');
    console.log(`│  📊 Activity                               │`);
    console.log(`│  Total Events: ${stats.total.toString().padStart(5)}                    │`);
    console.log(`│  J (Judge):    ${(stats.byVerb['J'] || 0).toString().padStart(5)}                    │`);
    console.log(`│  D (Delegate):  ${(stats.byVerb['D'] || 0).toString().padStart(5)}                    │`);
    console.log(`│  V (Verify):    ${(stats.byVerb['V'] || 0).toString().padStart(5)}                    │`);
    console.log(`│  T (Terminate): ${(stats.byVerb['T'] || 0).toString().padStart(5)}                    │`);
    console.log('│                                           │');
    console.log(`│  🔧 Registered Skills: ${skills.length.toString().padStart(2)}                  │`);
    for (const s of skills.slice(0, 3)) {
        const line = `│    ${s.skill_id.slice(0, 15).padEnd(15)} ${s.risk_level.padEnd(8)} │`;
        console.log(line);
    }
    if (skills.length > 3) {
        console.log(`│    ... and ${skills.length - 3} more                  │`);
    }
    console.log('│                                           │');
    console.log('│  [Export]  [View Chain]  [Settings]       │');
    console.log('└───────────────────────────────────────────┘\n');
});
//# sourceMappingURL=dashboard.js.map