/**
 * OpenClaw plugin: mac-ai-optimizer
 * Register tools to optimize macOS for AI workloads (OpenClaw, Docker, Ollama).
 */
import { execSync } from "child_process";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const TOOLS_DIR = resolve(__dirname, "tools");

function runScript(scriptName) {
  try {
    const output = execSync(`bash "${TOOLS_DIR}/${scriptName}"`, {
      encoding: "utf-8",
      timeout: 60000,
    });
    return { success: true, output };
  } catch (err) {
    return { success: false, output: err.stdout || err.message };
  }
}

export default function (api) {
  // system_report - safe, read-only
  api.registerTool(
    {
      name: "mac_system_report",
      description:
        "Show current Mac system resource usage: memory, CPU, swap, disk, and background service count. Use to assess whether optimization is needed.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("system_report.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );

  // optimize_memory
  api.registerTool(
    {
      name: "mac_optimize_memory",
      description:
        "Reduce macOS idle memory by disabling Spotlight, Siri, photo analysis, iCloud sync, and analytics. Saves 1-2GB RAM. Requires sudo for some operations.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("optimize_memory.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );

  // reduce_ui
  api.registerTool(
    {
      name: "mac_reduce_ui",
      description:
        "Lower GPU and RAM usage by disabling macOS animations, transparency, and Dock effects. Saves 300-500MB RAM.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("reduce_ui.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );

  // docker_optimize
  api.registerTool(
    {
      name: "mac_docker_optimize",
      description:
        "Configure Docker Desktop resource limits based on available RAM. Prevents Docker from consuming all memory. Also cleans unused containers and images.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("docker_optimize.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );

  // enable_ssh
  api.registerTool(
    {
      name: "mac_enable_ssh",
      description:
        "Enable SSH remote login so this Mac can be managed remotely as an AI compute node. Returns connection info and SSH config snippet.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("enable_ssh.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );

  // full_optimize
  api.registerTool(
    {
      name: "mac_full_optimize",
      description:
        "Run all Mac optimizations: system report, memory, UI, Docker, SSH. One command to turn a Mac into an AI server node for OpenClaw/Ollama/Docker.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("full_optimize.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );

  // revert_all
  api.registerTool(
    {
      name: "mac_revert_optimizations",
      description:
        "Revert all Mac optimizations back to macOS defaults. Restores Spotlight, Siri, UI animations, and transparency.",
      parameters: { type: "object", properties: {} },
      async execute() {
        const result = runScript("revert_all.sh");
        return {
          content: [{ type: "text", text: result.output }],
        };
      },
    },
    { optional: true }
  );
}
