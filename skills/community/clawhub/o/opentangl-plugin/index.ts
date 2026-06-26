import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";
import { spawnSync } from "child_process";
import { existsSync } from "fs";
import { resolve } from "path";

// ---------------------------------------------------------------------------
// Config helpers
// ---------------------------------------------------------------------------

interface PluginConfig {
  workdir?: string;
  bin?: string;
  timeout?: number;
}

/**
 * Resolved binary: a fixed executable + zero or more base arguments.
 * Stored as separate fields so they are passed as distinct argv elements
 * to spawnSync — never concatenated into a shell string.
 */
interface ResolvedBin {
  file: string;
  baseArgs: string[];
}

function resolveWorkdir(config: PluginConfig): string {
  return config.workdir ? resolve(config.workdir) : process.cwd();
}

/**
 * Resolve how to invoke the OpenTangl CLI.
 * Priority: explicit `bin` config → `opentangl` in PATH → `npx tsx src/cli.ts` → `node dist/cli.js`.
 *
 * Returns a ResolvedBin so the file and arguments are never joined into a
 * shell string and are safe to pass directly to spawnSync.
 */
function resolveBin(config: PluginConfig, workdir: string): ResolvedBin {
  if (config.bin) {
    // config.bin is admin-controlled; split on the first space so users can
    // supply e.g. "npx tsx" without introducing a shell invocation.
    const [file, ...baseArgs] = config.bin.split(" ").filter(Boolean);
    return { file, baseArgs };
  }

  // Try the installed opentangl binary first.
  const probe = spawnSync("opentangl", ["--version"], { stdio: "ignore" });
  if (probe.status === 0) {
    return { file: "opentangl", baseArgs: [] };
  }

  const srcCli = resolve(workdir, "src", "cli.ts");
  if (existsSync(srcCli)) {
    return { file: "npx", baseArgs: ["tsx", srcCli] };
  }

  const distCli = resolve(workdir, "dist", "cli.js");
  if (existsSync(distCli)) {
    return { file: "node", baseArgs: [distCli] };
  }

  throw new Error(
    `OpenTangl CLI not found. Set plugin config 'workdir' to the OpenTangl workspace root, or install opentangl globally.`
  );
}

// ---------------------------------------------------------------------------
// Input validation — defense-in-depth
// ---------------------------------------------------------------------------

/** Letters, digits, hyphens, underscores only. */
const RE_IDENTIFIER = /^[a-zA-Z0-9_-]+$/;
/** Comma-separated identifiers (project lists). */
const RE_PROJECT_LIST = /^[a-zA-Z0-9_,-]+$/;
/** var keys: letters, digits, underscores. */
const RE_VAR_KEY = /^[a-zA-Z0-9_]+$/;

function assertIdentifier(value: string, name: string): void {
  if (!RE_IDENTIFIER.test(value)) {
    throw new Error(
      `Invalid ${name} "${value}": only letters, digits, hyphens and underscores are allowed.`
    );
  }
}

function assertProjectList(value: string, name: string): void {
  if (!RE_PROJECT_LIST.test(value)) {
    throw new Error(
      `Invalid ${name} "${value}": expected comma-separated identifiers (letters, digits, hyphens, underscores).`
    );
  }
}

function assertWorkflowPath(value: string): void {
  if (value.includes("..") || value.includes("\0")) {
    throw new Error(`Invalid workflow path: path traversal is not allowed.`);
  }
}

function assertVar(value: string): void {
  const eq = value.indexOf("=");
  if (eq <= 0) {
    throw new Error(`Invalid var "${value}": expected key=value format.`);
  }
  const key = value.slice(0, eq);
  if (!RE_VAR_KEY.test(key)) {
    throw new Error(
      `Invalid var key "${key}": only letters, digits, and underscores are allowed.`
    );
  }
}

// ---------------------------------------------------------------------------
// CLI runner — no shell, no string concatenation
// ---------------------------------------------------------------------------

/**
 * Execute the OpenTangl CLI via spawnSync, bypassing the shell entirely.
 * Each element of `args` is passed as a separate argv entry to the OS,
 * so shell metacharacters in user-supplied values are never interpreted.
 */
function runCli(
  args: string[],
  workdir: string,
  bin: ResolvedBin,
  timeout: number
): string {
  const result = spawnSync(bin.file, [...bin.baseArgs, ...args], {
    cwd: workdir,
    encoding: "utf-8",
    timeout,
    env: { ...process.env },
    // No `shell: true` — this is intentional and critical.
  });

  if (result.error) throw result.error;

  const stdout = (result.stdout as string) ?? "";
  const stderr = (result.stderr as string) ?? "";

  if (result.status !== 0) {
    // Surface stdout if the CLI wrote useful output before failing.
    if (stdout.trim()) return stdout;
    throw new Error(
      stderr.trim() || `opentangl exited with code ${String(result.status)}`
    );
  }

  return stdout;
}

function ok(text: string) {
  return { content: [{ type: "text" as const, text: text.trim() }] };
}

function fail(text: string) {
  return { content: [{ type: "text" as const, text: text.trim() }], isError: true };
}

// ---------------------------------------------------------------------------
// Plugin entry
// ---------------------------------------------------------------------------

export default definePluginEntry({
  id: "opentangl",
  name: "OpenTangl",
  description:
    "Autonomous multi-repo development engine. Proposes tasks, runs autopilot cycles, manages workflows and the merge pipeline.",

  register(api) {
    const config = api.pluginConfig as PluginConfig;
    const workdir = resolveWorkdir(config);
    const timeout = config.timeout ?? 120_000;

    let bin: ResolvedBin;
    try {
      bin = resolveBin(config, workdir);
    } catch (err) {
      // Log once at startup; individual tool calls will surface a clear error.
      console.error(`[opentangl] ${String(err)}`);
      bin = { file: "opentangl", baseArgs: [] };
    }

    const run = (args: string[]) => runCli(args, workdir, bin, timeout);

    // -----------------------------------------------------------------------
    // READ-ONLY TOOLS (always available, no side effects)
    // -----------------------------------------------------------------------

    api.registerTool({
      name: "opentangl_queue",
      description:
        "Show the current OpenTangl task queue: pending, running, completed, and failed tasks with dependency status.",
      parameters: Type.Object({}),
      async execute(_id, _params) {
        try {
          return ok(run(["queue"]));
        } catch (err) {
          return fail(`Failed to read queue: ${String(err)}`);
        }
      },
    });

    api.registerTool({
      name: "opentangl_projects",
      description:
        "List all projects registered in projects.yaml with their resolved paths and configuration.",
      parameters: Type.Object({}),
      async execute(_id, _params) {
        try {
          return ok(run(["projects"]));
        } catch (err) {
          return fail(`Failed to list projects: ${String(err)}`);
        }
      },
    });

    api.registerTool({
      name: "opentangl_list_executions",
      description:
        "List recent workflow executions and their status (completed, failed, running).",
      parameters: Type.Object({}),
      async execute(_id, _params) {
        try {
          return ok(run(["list"]));
        } catch (err) {
          return fail(`Failed to list executions: ${String(err)}`);
        }
      },
    });

    // -----------------------------------------------------------------------
    // MUTATING TOOLS (optional — user must add to tools.allow)
    // -----------------------------------------------------------------------

    api.registerTool(
      {
        name: "opentangl_propose",
        description:
          "Ask OpenTangl to analyze the codebase and propose new development tasks. Use mode='preview' to see what would be queued without writing anything, or mode='queue' to append tasks to tasks/queue.yaml.",
        parameters: Type.Object({
          mode: Type.Union(
            [Type.Literal("preview"), Type.Literal("queue")],
            {
              description: "preview = dry run, queue = write to tasks/queue.yaml",
              default: "preview",
            }
          ),
          projects: Type.Optional(
            Type.String({
              description:
                "Comma-separated list of project IDs to include (e.g. 'web,api'). Omit to use the default project.",
            })
          ),
          featureRatio: Type.Optional(
            Type.Number({
              minimum: 0,
              maximum: 1,
              description:
                "Target ratio of feature tasks vs maintenance tasks (0–1). Defaults to 0.7.",
            })
          ),
        }),
        async execute(_id, params) {
          try {
            const projects = params["projects"] as string | undefined;
            if (projects) assertProjectList(projects, "projects");
            const args = ["propose", params["mode"] as string];
            if (projects) args.push("--projects", projects);
            if (params["featureRatio"] != null)
              args.push("--feature-ratio", String(params["featureRatio"]));
            return ok(run(args));
          } catch (err) {
            return fail(`Task proposal failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_autopilot",
        description:
          "Run OpenTangl autopilot: propose tasks and execute them in autonomous cycles. This writes code, creates commits, opens PRs, and merges. High impact — use with care.",
        parameters: Type.Object({
          cycles: Type.Optional(
            Type.Integer({
              minimum: 1,
              maximum: 10,
              description: "Number of propose+execute cycles to run. Defaults to 1.",
              default: 1,
            })
          ),
          projects: Type.Optional(
            Type.String({
              description:
                "Comma-separated project IDs to target. Omit for the default project.",
            })
          ),
          featureRatio: Type.Optional(
            Type.Number({
              minimum: 0,
              maximum: 1,
              description: "Feature task ratio (0–1). Defaults to 0.7.",
            })
          ),
        }),
        async execute(_id, params) {
          try {
            const projects = params["projects"] as string | undefined;
            if (projects) assertProjectList(projects, "projects");
            const args = ["autopilot"];
            if (params["cycles"]) args.push("--cycles", String(params["cycles"]));
            if (projects) args.push("--projects", projects);
            if (params["featureRatio"] != null)
              args.push("--feature-ratio", String(params["featureRatio"]));
            return ok(run(args));
          } catch (err) {
            return fail(`Autopilot failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_run_workflow",
        description:
          "Run a workflow YAML file through OpenTangl. In 'run' mode the agent produces outputs but does not commit. In 'auto' mode it writes, verifies, and commits autonomously.",
        parameters: Type.Object({
          workflow: Type.String({
            description:
              "Path to the workflow YAML file (relative to workdir or absolute).",
          }),
          mode: Type.Union(
            [Type.Literal("run"), Type.Literal("auto")],
            {
              description:
                "run = generate outputs only, auto = write + verify + commit",
              default: "run",
            }
          ),
          vars: Type.Optional(
            Type.Array(
              Type.String({
                description: "Variable in key=value format",
              }),
              {
                description:
                  "Workflow variables as key=value pairs (e.g. ['feature_name=auth', 'target=src/auth.ts']).",
              }
            )
          ),
          project: Type.Optional(
            Type.String({
              description: "Project ID to target.",
            })
          ),
        }),
        async execute(_id, params) {
          try {
            const workflow = params["workflow"] as string;
            const project = params["project"] as string | undefined;
            const vars = (params["vars"] as string[]) ?? [];
            assertWorkflowPath(workflow);
            if (project) assertIdentifier(project, "project");
            for (const v of vars) assertVar(v);
            const mode = (params["mode"] as string) ?? "run";
            const args = [mode, workflow];
            if (project) args.push("--project", project);
            for (const v of vars) args.push("--var", v);
            return ok(run(args));
          } catch (err) {
            return fail(`Workflow failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_next",
        description:
          "Execute the next eligible pending task from the queue. Respects dependency ordering.",
        parameters: Type.Object({
          project: Type.Optional(
            Type.String({
              description: "Limit execution to tasks for this project ID.",
            })
          ),
        }),
        async execute(_id, params) {
          try {
            const project = params["project"] as string | undefined;
            if (project) assertIdentifier(project, "project");
            const args = ["next"];
            if (project) args.push("--project", project);
            return ok(run(args));
          } catch (err) {
            return fail(`Next task failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_wire",
        description:
          "Run a read-only cross-repo wiring audit. Analyzes how multiple projects connect and surfaces integration gaps or mismatches. Does not write any code.",
        parameters: Type.Object({
          projects: Type.String({
            description:
              "Comma-separated list of project IDs to audit (e.g. 'web,api,mobile').",
          }),
        }),
        async execute(_id, params) {
          try {
            const projects = params["projects"] as string;
            assertProjectList(projects, "projects");
            return ok(run(["wire", "--projects", projects]));
          } catch (err) {
            return fail(`Wiring audit failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_merge",
        description:
          "Run the OpenTangl merge pipeline for completed tasks: creates PRs, waits for CI, reviews diffs with LLM, and merges or escalates.",
        parameters: Type.Object({}),
        async execute(_id, _params) {
          try {
            return ok(run(["merge"]));
          } catch (err) {
            return fail(`Merge pipeline failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_prune",
        description:
          "Remove terminal tasks (completed, merged, failed) from the queue and commit the cleaned queue state.",
        parameters: Type.Object({}),
        async execute(_id, _params) {
          try {
            return ok(run(["prune"]));
          } catch (err) {
            return fail(`Prune failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );

    api.registerTool(
      {
        name: "opentangl_resume",
        description:
          "Resume a failed or interrupted workflow execution by its execution ID.",
        parameters: Type.Object({
          executionId: Type.String({
            description: "The workflow execution ID to resume (from opentangl_list_executions).",
          }),
        }),
        async execute(_id, params) {
          try {
            const executionId = params["executionId"] as string;
            assertIdentifier(executionId, "executionId");
            return ok(run(["resume", executionId]));
          } catch (err) {
            return fail(`Resume failed: ${String(err)}`);
          }
        },
      },
      { optional: true }
    );
  },
});
