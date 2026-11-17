import { randomBytes, randomUUID, createHash } from "node:crypto";
import { open, readFile, rm, stat } from "node:fs/promises";
import { atomicWrite } from "./operations.js";
import { migratorError } from "./errors.js";

function now() {
  return new Date().toISOString();
}

function tokenHash(token) {
  return createHash("sha256").update(token, "utf8").digest("hex");
}

export class RunState {
  constructor(path, data) {
    this.path = path;
    this.data = data;
  }

  static async create(path, runId = null) {
    try {
      await stat(path);
      throw new Error(`run-state already exists: ${path}`);
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    const state = new RunState(path, {
      version: 1,
      run_id: runId || randomUUID(),
      created_at: now(),
      updated_at: now(),
      steps: {},
      approvals: {},
    });
    await state.save();
    return state;
  }

  static async load(path) {
    const value = JSON.parse(await readFile(path, "utf8"));
    if (!value || typeof value !== "object" || typeof value.run_id !== "string"
      || !value.steps || !value.approvals) {
      throw migratorError("MANIFEST_INVALID", `invalid run-state file: ${path}`);
    }
    return new RunState(path, value);
  }

  get runId() {
    return this.data.run_id;
  }

  async save() {
    this.data.updated_at = now();
    await atomicWrite(this.path, `${JSON.stringify(this.data, null, 2)}\n`, {
      overwrite: true,
    });
  }

  async mutateLocked(mutate) {
    const lockPath = `${this.path}.lock`;
    let lock;
    try {
      lock = await open(lockPath, "wx", 0o600);
      const latest = JSON.parse(await readFile(this.path, "utf8"));
      if (latest.run_id !== this.runId) throw new Error("run-state changed identity");
      this.data = latest;
      const result = mutate();
      await this.save();
      return result;
    } catch (error) {
      if (error.code === "EEXIST") throw new Error(`run-state is busy: ${this.path}`);
      throw error;
    } finally {
      if (lock) {
        await lock.close().catch(() => {});
        await rm(lockPath, { force: true }).catch(() => {});
      }
    }
  }

  async completeStep(step, details = {}) {
    await this.mutateLocked(() => {
      this.data.steps[step] = { completed_at: now(), details };
    });
  }

  isComplete(step) {
    return Object.hasOwn(this.data.steps, step);
  }

  async issueApproval(action) {
    if (!String(action).trim()) throw migratorError("APPROVAL_INVALID", "approval action must be non-empty");
    const token = `${this.runId}.${randomBytes(24).toString("base64url")}`;
    await this.mutateLocked(() => {
      this.data.approvals[tokenHash(token)] = {
        run_id: this.runId,
        action: String(action),
        issued_at: now(),
        used_at: null,
      };
    });
    return token;
  }

  async consumeApproval(action, token) {
    await this.mutateLocked(() => {
      const approval = this.data.approvals[tokenHash(String(token))];
      if (!approval
        || approval.run_id !== this.runId
        || approval.action !== action
        || approval.used_at !== null
        || !String(token).startsWith(`${this.runId}.`)) {
        throw migratorError(
          "APPROVAL_INVALID",
          "approval token is invalid, used, or bound to another action/run",
        );
      }
      approval.used_at = now();
    });
  }
}
