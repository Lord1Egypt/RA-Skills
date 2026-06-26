import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import {
  getActiveBatch,
  getBatchProgress,
  getUnlockedTasks,
  syncTasksWithContracts,
  updateTask,
  writeBatch
} from "../tasks";
import { TaskStatus, type ActiveTasksFile } from "../types";

test("updateTask uses atomic writes under concurrent updates", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-tasks-"));
  const nexumDir = path.join(projectDir, "nexum");
  const activeTasksPath = path.join(nexumDir, "active-tasks.json");

  await mkdir(nexumDir, { recursive: true });

  const initialTasks: ActiveTasksFile = {
    tasks: [
      {
        id: "NX-001",
        name: "Task 1",
        status: TaskStatus.Pending,
        contract_path: "docs/nexum/contracts/NX-001.yaml",
        depends_on: []
      },
      {
        id: "NX-002",
        name: "Task 2",
        status: TaskStatus.Pending,
        contract_path: "docs/nexum/contracts/NX-002.yaml",
        depends_on: []
      }
    ]
  };

  await writeFile(activeTasksPath, JSON.stringify(initialTasks, null, 2) + "\n", "utf8");

  await Promise.all([
    updateTask(projectDir, "NX-001", { status: TaskStatus.Done }),
    updateTask(projectDir, "NX-002", { status: TaskStatus.Running })
  ]);

  const rawContents = await readFile(activeTasksPath, "utf8");
  const parsed = JSON.parse(rawContents) as ActiveTasksFile;

  assert.equal(parsed.tasks.length, 2);
  assert.equal(
    parsed.tasks.find((task) => task.id === "NX-001")?.status,
    TaskStatus.Done
  );
  assert.equal(
    parsed.tasks.find((task) => task.id === "NX-002")?.status,
    TaskStatus.Running
  );
});

test("updateTask writes current and role-specific ACP session fields", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-tasks-"));
  const nexumDir = path.join(projectDir, "nexum");
  const activeTasksPath = path.join(nexumDir, "active-tasks.json");

  await mkdir(nexumDir, { recursive: true });

  const initialTasks: ActiveTasksFile = {
    tasks: [
      {
        id: "NX-001",
        name: "Task 1",
        status: TaskStatus.Pending,
        contract_path: "docs/nexum/contracts/NX-001.yaml",
        depends_on: []
      }
    ]
  };

  await writeFile(activeTasksPath, JSON.stringify(initialTasks, null, 2) + "\n", "utf8");

  await updateTask(projectDir, "NX-001", {
    acp_session_key: "session-abc123",
    acp_stream_log: "/tmp/stream.log",
    generator_acp_session_key: "gen-session-abc123",
    generator_acp_stream_log: "/tmp/gen-stream.log",
    evaluator_acp_session_key: "eval-session-xyz789",
    evaluator_acp_stream_log: "/tmp/eval-stream.log",
  });

  const rawContents = await readFile(activeTasksPath, "utf8");
  const parsed = JSON.parse(rawContents) as ActiveTasksFile;
  const task = parsed.tasks.find((t) => t.id === "NX-001");

  assert.equal(task?.acp_session_key, "session-abc123");
  assert.equal(task?.acp_stream_log, "/tmp/stream.log");
  assert.equal(task?.generator_acp_session_key, "gen-session-abc123");
  assert.equal(task?.generator_acp_stream_log, "/tmp/gen-stream.log");
  assert.equal(task?.evaluator_acp_session_key, "eval-session-xyz789");
  assert.equal(task?.evaluator_acp_stream_log, "/tmp/eval-stream.log");
});

test("getUnlockedTasks returns pending tasks whose dependencies are now satisfied", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-tasks-"));
  const nexumDir = path.join(projectDir, "nexum");
  const activeTasksPath = path.join(nexumDir, "active-tasks.json");

  await mkdir(nexumDir, { recursive: true });

  const tasks: ActiveTasksFile = {
    tasks: [
      {
        id: "NX-001",
        name: "Foundation",
        status: TaskStatus.Done,
        contract_path: "docs/nexum/contracts/NX-001.yaml",
        depends_on: []
      },
      {
        id: "NX-002",
        name: "Freshly completed",
        status: TaskStatus.Running,
        contract_path: "docs/nexum/contracts/NX-002.yaml",
        depends_on: []
      },
      {
        id: "NX-003",
        name: "Unlocked now",
        status: TaskStatus.Pending,
        contract_path: "docs/nexum/contracts/NX-003.yaml",
        depends_on: ["NX-001", "NX-002"]
      },
      {
        id: "NX-004",
        name: "Still blocked elsewhere",
        status: TaskStatus.Pending,
        contract_path: "docs/nexum/contracts/NX-004.yaml",
        depends_on: ["NX-002", "NX-999"]
      },
      {
        id: "NX-005",
        name: "Does not depend on completed task",
        status: TaskStatus.Pending,
        contract_path: "docs/nexum/contracts/NX-005.yaml",
        depends_on: ["NX-001"]
      }
    ]
  };

  await writeFile(activeTasksPath, JSON.stringify(tasks, null, 2) + "\n", "utf8");

  const unlocked = await getUnlockedTasks(projectDir, "NX-002");

  assert.deepEqual(
    unlocked.map((task) => task.id),
    ["NX-003"]
  );
});

test("writeBatch persists currentBatch and getBatchProgress counts done tasks per batch", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-tasks-"));
  const nexumDir = path.join(projectDir, "nexum");
  const activeTasksPath = path.join(nexumDir, "active-tasks.json");

  await mkdir(nexumDir, { recursive: true });

  const tasks: ActiveTasksFile = {
    tasks: [
      {
        id: "NX-001",
        name: "Alpha done",
        status: TaskStatus.Done,
        batch: "alpha",
        contract_path: "docs/nexum/contracts/NX-001.yaml",
        depends_on: []
      },
      {
        id: "NX-002",
        name: "Alpha pending",
        status: TaskStatus.Pending,
        batch: "alpha",
        contract_path: "docs/nexum/contracts/NX-002.yaml",
        depends_on: []
      },
      {
        id: "NX-003",
        name: "Beta done",
        status: TaskStatus.Done,
        batch: "beta",
        contract_path: "docs/nexum/contracts/NX-003.yaml",
        depends_on: []
      }
    ]
  };

  await writeFile(activeTasksPath, JSON.stringify(tasks, null, 2) + "\n", "utf8");

  await writeBatch(projectDir, "alpha");

  assert.equal(await getActiveBatch(projectDir), "alpha");
  assert.deepEqual(await getBatchProgress(projectDir, "alpha"), {
    batch: "alpha",
    done: 1,
    total: 2
  });

  const rawContents = await readFile(activeTasksPath, "utf8");
  const parsed = JSON.parse(rawContents) as ActiveTasksFile;
  assert.equal(parsed.currentBatch, "alpha");
  assert.equal(parsed.tasks.length, 3);
});

test("syncTasksWithContracts registers contracts and derives blocked status from depends_on", async () => {
  const projectDir = await mkdtemp(path.join(tmpdir(), "nexum-tasks-"));
  const contractDir = path.join(projectDir, "docs", "nexum", "contracts");
  const nexumDir = path.join(projectDir, "nexum");
  const activeTasksPath = path.join(nexumDir, "active-tasks.json");

  await mkdir(contractDir, { recursive: true });
  await mkdir(nexumDir, { recursive: true });
  await writeFile(activeTasksPath, JSON.stringify({ tasks: [] }, null, 2) + "\n", "utf8");
  await writeFile(
    path.join(contractDir, "TASK-001.yaml"),
    [
      "id: TASK-001",
      'name: "First task"',
      "type: coding",
      "scope:",
      "  files:",
      "    - src/one.ts",
      "  boundaries: []",
      "  conflicts_with: []",
      "deliverables:",
      '  - "src/one.ts"',
      "eval_strategy:",
      "  type: review",
      "  criteria:",
      "    - id: C1",
      '      desc: "ok"',
      "generator: codex-gen-01",
      "evaluator: claude-eval-01",
      "max_iterations: 3",
      "depends_on: []",
      ""
    ].join("\n"),
    "utf8"
  );
  await writeFile(
    path.join(contractDir, "TASK-002.yaml"),
    [
      "id: TASK-002",
      'name: "Second task"',
      "type: coding",
      "scope:",
      "  files:",
      "    - src/two.ts",
      "  boundaries: []",
      "  conflicts_with: []",
      "deliverables:",
      '  - "src/two.ts"',
      "eval_strategy:",
      "  type: review",
      "  criteria:",
      "    - id: C1",
      '      desc: "ok"',
      "generator: codex-gen-01",
      "evaluator: claude-eval-01",
      "max_iterations: 3",
      "depends_on:",
      "  - TASK-001",
      ""
    ].join("\n"),
    "utf8"
  );

  const result = await syncTasksWithContracts(projectDir);

  assert.deepEqual(result.created.sort(), ["TASK-001", "TASK-002"]);
  const parsed = JSON.parse(await readFile(activeTasksPath, "utf8")) as ActiveTasksFile;
  assert.equal(parsed.tasks.find((task) => task.id === "TASK-001")?.status, TaskStatus.Pending);
  assert.equal(parsed.tasks.find((task) => task.id === "TASK-002")?.status, TaskStatus.Blocked);

  await updateTask(projectDir, "TASK-001", { status: TaskStatus.Done });
  const resynced = await syncTasksWithContracts(projectDir, { taskId: "TASK-002" });
  assert.deepEqual(resynced.updated, ["TASK-002"]);

  const afterResync = JSON.parse(await readFile(activeTasksPath, "utf8")) as ActiveTasksFile;
  assert.equal(afterResync.tasks.find((task) => task.id === "TASK-002")?.status, TaskStatus.Pending);
});
