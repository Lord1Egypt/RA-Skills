import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { getUnlockedTasks, updateTask } from "../tasks";
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

test("updateTask writes acp_session_key and acp_stream_log fields", async () => {
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
    acp_stream_log: "/tmp/stream.log"
  });

  const rawContents = await readFile(activeTasksPath, "utf8");
  const parsed = JSON.parse(rawContents) as ActiveTasksFile;
  const task = parsed.tasks.find((t) => t.id === "NX-001");

  assert.equal(task?.acp_session_key, "session-abc123");
  assert.equal(task?.acp_stream_log, "/tmp/stream.log");
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
