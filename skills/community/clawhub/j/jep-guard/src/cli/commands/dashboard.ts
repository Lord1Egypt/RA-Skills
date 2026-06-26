import { Command } from 'commander';
import { AuditStreamService } from '../../daemon/audit';
import { SkillRegistryService } from '../../daemon/registry';

export const dashboardCommand = new Command('dashboard')
  .description('Show interactive dashboard')
  .action(async () => {
    const audit = new AuditStreamService();
    const registry = new SkillRegistryService();

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