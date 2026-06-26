import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * OpenCode plugin for mukun-md-push-wechat
 *
 * Registers the skills directory so OpenCode can discover
 * and load the SKILL.md file via the native skill tool.
 */
export const MkuNOpenCodePlugin = async ({ directory }) => {
  const skillsDir = path.resolve(__dirname, '../../');

  return {
    name: 'mukun-md-push-wechat',

    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) {
        config.skills.paths.push(skillsDir);
      }

      // Inject CODEBUDDY_SKILL_DIR so SKILL.md script paths work across platforms
      if (!process.env.CODEBUDDY_SKILL_DIR) {
        process.env.CODEBUDDY_SKILL_DIR = skillsDir;
      }
    },
  };
};

export default MkuNOpenCodePlugin;
