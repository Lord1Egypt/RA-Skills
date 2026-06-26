import * as fs from "node:fs/promises";
import * as path from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

export const getKeyPath = (api: OpenClawPluginApi) =>
  path.join(api.runtime.state.resolveStateDir(), "omni_key.txt");

export const getToolsPath = (api: OpenClawPluginApi) =>
  path.join(api.runtime.state.resolveStateDir(), "intercepted_tools.json");

// Path for the environment mode flag
export const getModePath = (api: OpenClawPluginApi) =>
  path.join(api.runtime.state.resolveStateDir(), "omni_mode.json");

export const getSavedKey = async (api: OpenClawPluginApi) => {
  try {
    const key = await fs.readFile(getKeyPath(api), "utf-8");
    return key.trim();
  } catch {
    return null;
  }
};

export const saveInterceptedTools = async (api: OpenClawPluginApi, tools: string[]) => {
  const toolsPath = getToolsPath(api);
  await fs.mkdir(path.dirname(toolsPath), { recursive: true });
  await fs.writeFile(toolsPath, JSON.stringify(tools, null, 2), "utf-8");
};

/**
 * Saves the OmniPersona UUID key
 */
export const saveKey = async (api: OpenClawPluginApi, key: string) => {
  const keyPath = getKeyPath(api);
  await fs.mkdir(path.dirname(keyPath), { recursive: true });
  await fs.writeFile(keyPath, key, "utf-8");
};

export const getInterceptedTools = async (api: OpenClawPluginApi): Promise<string[]> => {
  try {
    const data = await fs.readFile(getToolsPath(api), "utf-8");
    return JSON.parse(data);
  } catch {
    return [];
  }
};

/**
 * Saves the environment mode (prod or dev)
 */
export const saveMode = async (api: OpenClawPluginApi, mode: "prod" | "dev") => {
  const modePath = getModePath(api);
  await fs.mkdir(path.dirname(modePath), { recursive: true });
  await fs.writeFile(modePath, JSON.stringify({ mode }), "utf-8");
};

/**
 * Retrieves the current mode, defaults to "prod"
 */
export const getMode = async (api: OpenClawPluginApi): Promise<"prod" | "dev"> => {
  try {
    const data = await fs.readFile(getModePath(api), "utf-8");
    return JSON.parse(data).mode;
  } catch {
    return "prod";
  }
};
