import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';

export interface GlobalConfig {
  projects: string[];
  watch: {
    intervalMin: number;
    timeoutMin: number;
  };
}

const DEFAULT_GLOBAL_CONFIG: GlobalConfig = {
  projects: [],
  watch: {
    intervalMin: 5,
    timeoutMin: 30,
  },
};

export function globalConfigPath(): string {
  return path.join(os.homedir(), '.nexum', 'config.json');
}

export async function readGlobalConfig(): Promise<GlobalConfig> {
  const configPath = globalConfigPath();
  try {
    const contents = await readFile(configPath, 'utf8');
    const parsed = JSON.parse(contents) as Partial<GlobalConfig>;
    return {
      projects: parsed.projects ?? [],
      watch: {
        intervalMin: parsed.watch?.intervalMin ?? DEFAULT_GLOBAL_CONFIG.watch.intervalMin,
        timeoutMin: parsed.watch?.timeoutMin ?? DEFAULT_GLOBAL_CONFIG.watch.timeoutMin,
      },
    };
  } catch {
    return { ...DEFAULT_GLOBAL_CONFIG, watch: { ...DEFAULT_GLOBAL_CONFIG.watch } };
  }
}

export async function writeGlobalConfig(config: GlobalConfig): Promise<void> {
  const configPath = globalConfigPath();
  await mkdir(path.dirname(configPath), { recursive: true });
  await writeFile(configPath, JSON.stringify(config, null, 2) + '\n', 'utf8');
}

export async function addProject(dir: string): Promise<void> {
  const absDir = path.resolve(dir);
  const config = await readGlobalConfig();
  if (!config.projects.includes(absDir)) {
    config.projects.push(absDir);
    await writeGlobalConfig(config);
  }
}

export async function removeProject(dir: string): Promise<void> {
  const absDir = path.resolve(dir);
  const config = await readGlobalConfig();
  config.projects = config.projects.filter((p) => p !== absDir);
  await writeGlobalConfig(config);
}
