import { Command } from 'commander';
import { SkillRegistryService } from '../../daemon/registry';

export const skillsCommand = new Command('skills')
  .description('Manage registered skills')
  .argument('<action>', 'list, reputation')
  .action(async (action) => {
    const registry = new SkillRegistryService();

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