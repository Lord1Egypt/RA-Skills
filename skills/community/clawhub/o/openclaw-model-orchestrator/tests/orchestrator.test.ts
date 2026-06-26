/**
 * Integration tests for openclaw-model-orchestrator
 *
 * T-001: Validate api.inference with model aliases (routing logic, mocked LLM calls)
 * T-003: Timeout and error recovery for workers
 * T-004: Progress reporting during execution
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  parseModelsStatus,
  resolveModel,
  resolveModelId,
  classifyTask,
  createHandoff,
  parseArgs,
  showHelp,
  formatModelList,
  formatRecommendation,
  withTimeout,
  isTransientError,
  extractContent,
  inferWithRetry,
  executeFanOut,
  executePipeline,
  executeConsensus,
  type ModelInfo,
  type OrchestrateRequest,
  type ProgressEvent,
  type InferenceRequest,
  type InferenceResponse,
  type WorkerOptions,
} from "../index.js";

// ---------------------------------------------------------------------------
// Helpers / fixtures
// ---------------------------------------------------------------------------

const SAMPLE_MODELS_STATUS = `
OpenClaw Models Status

Aliases (3) :
  opus -> anthropic/claude-opus-4-6, sonnet -> anthropic/claude-sonnet-4-6, fast -> openai/gpt-4o-mini
Configured models (4) :
  anthropic/claude-opus-4-6, anthropic/claude-sonnet-4-6, openai/gpt-4o-mini, openai/gpt-4o

Auth / Credentials
Providers w/ OAuth/tokens (2): anthropic (2), openai (1)
`;

/** Creates a minimal mock api.inference that resolves immediately with given content. */
function makeMockApi(
  responses: Record<string, string | Error | (() => Promise<string>)>,
): {
  inference: (req: InferenceRequest) => Promise<InferenceResponse>;
  calls: Array<{ model: string; messages: Array<{ role: string; content: string }> }>;
} {
  const calls: Array<{ model: string; messages: Array<{ role: string; content: string }> }> = [];
  return {
    calls,
    inference: async (req: InferenceRequest): Promise<InferenceResponse> => {
      calls.push({ model: req.model, messages: req.messages });
      const key = req.model;
      const val = responses[key] ?? responses["*"];
      if (val === undefined) {
        throw new Error(`No mock response defined for model: ${key}`);
      }
      if (val instanceof Error) throw val;
      if (typeof val === "function") {
        const content = await val();
        return { content };
      }
      return { content: val as string };
    },
  };
}

// ---------------------------------------------------------------------------
// T-001: Model alias resolution
// ---------------------------------------------------------------------------

describe("T-001: parseModelsStatus", () => {
  it("parses aliases correctly", () => {
    const { aliases } = parseModelsStatus(SAMPLE_MODELS_STATUS);
    expect(aliases.get("opus")).toBe("anthropic/claude-opus-4-6");
    expect(aliases.get("sonnet")).toBe("anthropic/claude-sonnet-4-6");
    expect(aliases.get("fast")).toBe("openai/gpt-4o-mini");
  });

  it("parses models correctly", () => {
    const { models } = parseModelsStatus(SAMPLE_MODELS_STATUS);
    const ids = models.map((m) => m.id);
    expect(ids).toContain("anthropic/claude-opus-4-6");
    expect(ids).toContain("anthropic/claude-sonnet-4-6");
    expect(ids).toContain("openai/gpt-4o-mini");
    expect(ids).toContain("openai/gpt-4o");
  });

  it("annotates model auth correctly", () => {
    const { models } = parseModelsStatus(SAMPLE_MODELS_STATUS);
    const opus = models.find((m) => m.id === "anthropic/claude-opus-4-6");
    expect(opus?.auth).toBe(true);
  });

  it("attaches alias to model when alias points to it", () => {
    const { models } = parseModelsStatus(SAMPLE_MODELS_STATUS);
    const opus = models.find((m) => m.id === "anthropic/claude-opus-4-6");
    expect(opus?.alias).toBe("opus");
  });

  it("returns empty models/aliases on empty input", () => {
    const { models, aliases } = parseModelsStatus("");
    expect(models).toHaveLength(0);
    expect(aliases.size).toBe(0);
  });
});

describe("T-001: resolveModel - alias resolution", () => {
  let models: ModelInfo[];

  beforeEach(() => {
    const { models: m } = parseModelsStatus(SAMPLE_MODELS_STATUS);
    models = m;
  });

  it("resolves alias to full model ID", () => {
    const resolved = resolveModel("opus", models);
    expect(resolved?.id).toBe("anthropic/claude-opus-4-6");
  });

  it("resolves direct model ID", () => {
    const resolved = resolveModel("openai/gpt-4o", models);
    expect(resolved?.id).toBe("openai/gpt-4o");
  });

  it("returns undefined for unknown name", () => {
    const resolved = resolveModel("nonexistent-model", models);
    expect(resolved).toBeUndefined();
  });

  it("resolveModelId returns alias target", () => {
    const id = resolveModelId("sonnet", models);
    expect(id).toBe("anthropic/claude-sonnet-4-6");
  });

  it("resolveModelId falls back to input if not found", () => {
    const id = resolveModelId("unknown-alias", models);
    expect(id).toBe("unknown-alias");
  });
});

// ---------------------------------------------------------------------------
// T-001: Task classification
// ---------------------------------------------------------------------------

describe("T-001: classifyTask", () => {
  it("classifies coding tasks", () => {
    expect(classifyTask("Build a REST API endpoint")).toBe("coding");
    expect(classifyTask("Implement a database migration")).toBe("coding");
    expect(classifyTask("Fix the bug in the authentication module")).toBe("coding");
  });

  it("classifies research tasks", () => {
    expect(classifyTask("Research and compare vector database options")).toBe("research");
    expect(classifyTask("Analyze the state of the art in LLM routing")).toBe("research");
  });

  it("classifies security tasks", () => {
    expect(classifyTask("Security audit for GDPR compliance NIS-2 hardening")).toBe("security");
    expect(classifyTask("CVE patch vulnerability penetration encryption audit")).toBe("security");
  });

  it("classifies review tasks", () => {
    // Use multiple review keywords to clearly win over other categories
    expect(classifyTask("Review check verify inspect feedback refine critique")).toBe("review");
    expect(classifyTask("Review optimize refine quality feedback")).toBe("review");
  });

  it("classifies bulk tasks", () => {
    expect(classifyTask("Batch migrate all users to new schema")).toBe("bulk");
  });

  it("defaults to coding for ambiguous tasks", () => {
    expect(classifyTask("Do the thing")).toBe("coding");
  });
});

// ---------------------------------------------------------------------------
// T-001: parseArgs
// ---------------------------------------------------------------------------

describe("T-001: parseArgs", () => {
  it("parses --key value pairs", () => {
    const args = parseArgs('--mode fan-out --task "Build REST API"');
    expect(args.mode).toBe("fan-out");
    expect(args.task).toBe("Build REST API");
  });

  it("parses bare subcommand", () => {
    const args = parseArgs("help");
    expect(args._subcommand).toBe("help");
  });

  it("parses models subcommand", () => {
    const args = parseArgs("models");
    expect(args._subcommand).toBe("models");
  });

  it("handles missing args gracefully", () => {
    const args = parseArgs("");
    expect(args._subcommand).toBe(undefined);
  });
});

// ---------------------------------------------------------------------------
// T-001: AAHP handoff creation
// ---------------------------------------------------------------------------

describe("T-001: createHandoff", () => {
  it("creates a valid AAHP v3.0 handoff", () => {
    const h = createHandoff("Build API", undefined, "user", "opus", "fan-out");
    expect(h.version).toBe("3.0");
    expect(h.context.task).toBe("Build API");
    expect(h.routing.targetModel).toBe("opus");
    expect(h.routing.mode).toBe("fan-out");
    expect(h.phase).toBe("planning");
    expect(h.taskId).toMatch(/^orch-/);
  });

  it("sets phase to 'execution' when subtask provided", () => {
    const h = createHandoff("Build API", "Implement endpoints", "planner", "worker", "pipeline");
    expect(h.phase).toBe("execution");
    expect(h.context.subtask).toBe("Implement endpoints");
  });

  it("includes state", () => {
    const h = createHandoff("task", undefined, "src", "dst", "consensus", { key: "val" });
    expect(h.state).toEqual({ key: "val" });
  });
});

// ---------------------------------------------------------------------------
// T-001: Integration test - api.inference routing with model aliases
// ---------------------------------------------------------------------------

describe("T-001: api.inference routing - fan-out", () => {
  it("calls planner and workers with correct model identifiers", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do sub A", expectedOutput: "Result A" },
      { id: 2, title: "Sub B", description: "Do sub B", expectedOutput: "Result B" },
    ]);

    const mock = makeMockApi({
      "opus": plannerResponse,
      "sonnet": "Worker result here",
      "fast": "Review complete. Merged output.",
    });

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Build a REST API",
      planner: "opus",
      workers: ["sonnet", "sonnet"],
      reviewer: "fast",
    };

    const result = await executeFanOut(req, mock);

    // Verify planner was called
    const plannerCall = mock.calls.find((c) => c.model === "opus");
    expect(plannerCall).toBeDefined();
    expect(plannerCall!.messages[0].content).toContain("Build a REST API");

    // Verify workers were called
    const workerCalls = mock.calls.filter((c) => c.model === "sonnet");
    expect(workerCalls.length).toBeGreaterThanOrEqual(1);

    // Verify reviewer was called
    const reviewerCall = mock.calls.find((c) => c.model === "fast");
    expect(reviewerCall).toBeDefined();

    // Result should contain completion markers
    expect(result).toContain("Fan-Out Orchestration");
    expect(result).toContain("Final Result:");
  });

  it("resolves full model IDs when passed directly", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
    ]);

    const mock = makeMockApi({
      "anthropic/claude-opus-4-6": plannerResponse,
      "anthropic/claude-sonnet-4-6": "Worker done",
      "openai/gpt-4o-mini": "Review done",
    });

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Test with full IDs",
      planner: "anthropic/claude-opus-4-6",
      workers: ["anthropic/claude-sonnet-4-6"],
      reviewer: "openai/gpt-4o-mini",
    };

    const result = await executeFanOut(req, mock);
    expect(result).toContain("Fan-Out Orchestration");
    expect(mock.calls.some((c) => c.model === "anthropic/claude-opus-4-6")).toBe(true);
  });
});

describe("T-001: api.inference routing - pipeline", () => {
  it("chains models in sequence", async () => {
    const callOrder: string[] = [];
    const mock = {
      calls: [] as Array<{ model: string; messages: Array<{ role: string; content: string }> }>,
      inference: async (req: InferenceRequest): Promise<InferenceResponse> => {
        callOrder.push(req.model);
        mock.calls.push({ model: req.model, messages: req.messages });
        return { content: `Output from ${req.model}` };
      },
    };

    const req: OrchestrateRequest = {
      mode: "pipeline",
      task: "Build and test a feature",
      planner: "opus",
      workers: ["sonnet"],
      reviewer: "fast",
    };

    const result = await executePipeline(req, mock);

    // Verify sequential order: planner -> worker -> reviewer
    expect(callOrder[0]).toBe("opus");
    expect(callOrder[1]).toBe("sonnet");
    expect(callOrder[2]).toBe("fast");

    expect(result).toContain("Pipeline Orchestration");
    expect(result).toContain("Final Result:");
  });

  it("passes previous output to next step", async () => {
    const mock = makeMockApi({
      "opus": "Initial plan content",
      "sonnet": "Refined content",
      "fast": "Final polished output",
    });

    const req: OrchestrateRequest = {
      mode: "pipeline",
      task: "Refine iteratively",
      planner: "opus",
      workers: ["sonnet"],
      reviewer: "fast",
    };

    await executePipeline(req, mock);

    // The second call (sonnet) should have received the first output in its prompt
    const sonnetCall = mock.calls.find((c) => c.model === "sonnet");
    expect(sonnetCall!.messages[0].content).toContain("Initial plan content");

    // The third call (fast) should have received the second output
    const fastCall = mock.calls.find((c) => c.model === "fast");
    expect(fastCall!.messages[0].content).toContain("Refined content");
  });
});

describe("T-001: api.inference routing - consensus", () => {
  it("queries all workers in parallel and synthesizes", async () => {
    const mock = makeMockApi({
      "opus": "Opus response on the topic",
      "sonnet": "Sonnet response on the topic",
      "fast": "Synthesis: both models agree on the key points",
    });

    const req: OrchestrateRequest = {
      mode: "consensus",
      task: "What is the best approach for API design?",
      planner: "opus",
      workers: ["sonnet"],
      reviewer: "fast",
    };

    const result = await executeConsensus(req, mock);

    // Both workers queried
    expect(mock.calls.some((c) => c.model === "opus")).toBe(true);
    expect(mock.calls.some((c) => c.model === "sonnet")).toBe(true);

    // Synthesizer called with both responses
    const synthCall = mock.calls.find((c) => c.model === "fast");
    expect(synthCall!.messages[0].content).toContain("Opus response");
    expect(synthCall!.messages[0].content).toContain("Sonnet response");

    expect(result).toContain("Consensus Orchestration");
    expect(result).toContain("Consensus Result:");
  });
});

// ---------------------------------------------------------------------------
// T-003: withTimeout
// ---------------------------------------------------------------------------

describe("T-003: withTimeout", () => {
  it("resolves when promise completes before timeout", async () => {
    const result = await withTimeout(Promise.resolve("ok"), 500);
    expect(result).toBe("ok");
  });

  it("rejects with timeout error when promise is too slow", async () => {
    const slow = new Promise<string>((resolve) => setTimeout(() => resolve("late"), 200));
    await expect(withTimeout(slow, 50)).rejects.toThrow("timed out after 50ms");
  });

  it("rejects with the original error if promise rejects before timeout", async () => {
    const failing = Promise.reject(new Error("network error"));
    await expect(withTimeout(failing, 1000)).rejects.toThrow("network error");
  });
});

// ---------------------------------------------------------------------------
// T-003: isTransientError
// ---------------------------------------------------------------------------

describe("T-003: isTransientError", () => {
  it("identifies 429 rate limit as transient", () => {
    expect(isTransientError(new Error("HTTP 429 rate limit exceeded"))).toBe(true);
  });

  it("identifies 503 service unavailable as transient", () => {
    expect(isTransientError(new Error("503 Service Unavailable"))).toBe(true);
  });

  it("identifies 502 as transient", () => {
    expect(isTransientError(new Error("502 Bad Gateway"))).toBe(true);
  });

  it("identifies ECONNRESET as transient", () => {
    expect(isTransientError(new Error("ECONNRESET connection reset"))).toBe(true);
  });

  it("identifies timeout as transient", () => {
    expect(isTransientError(new Error("Inference timed out after 5000ms"))).toBe(true);
  });

  it("identifies overloaded as transient", () => {
    expect(isTransientError(new Error("Model is overloaded"))).toBe(true);
  });

  it("does NOT classify auth errors as transient", () => {
    expect(isTransientError(new Error("401 Unauthorized"))).toBe(false);
  });

  it("does NOT classify unknown errors as transient", () => {
    expect(isTransientError(new Error("Model not found"))).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// T-003: extractContent
// ---------------------------------------------------------------------------

describe("T-003: extractContent", () => {
  it("extracts top-level content", () => {
    expect(extractContent({ content: "hello" })).toBe("hello");
  });

  it("extracts nested message.content", () => {
    expect(extractContent({ message: { content: "nested" } })).toBe("nested");
  });

  it("prefers content over message.content", () => {
    expect(extractContent({ content: "top", message: { content: "nested" } })).toBe("top");
  });

  it("returns placeholder if both absent", () => {
    expect(extractContent({})).toBe("(no output)");
  });
});

// ---------------------------------------------------------------------------
// T-003: inferWithRetry - timeout
// ---------------------------------------------------------------------------

describe("T-003: inferWithRetry - timeout", () => {
  it("raises timeout error when inference exceeds timeoutMs", async () => {
    const slowApi = {
      inference: (_req: InferenceRequest): Promise<InferenceResponse> =>
        new Promise((resolve) => setTimeout(() => resolve({ content: "late" }), 300)),
    };

    const opts: WorkerOptions = { timeoutMs: 50, maxRetries: 0 };
    await expect(inferWithRetry(slowApi, { model: "m", messages: [] }, opts))
      .rejects.toThrow("timed out");
  });

  it("succeeds when inference completes within timeoutMs", async () => {
    const fastApi = makeMockApi({ "m": "fast response" });
    const opts: WorkerOptions = { timeoutMs: 5000, maxRetries: 0 };
    const result = await inferWithRetry(fastApi, { model: "m", messages: [] }, opts);
    expect(extractContent(result)).toBe("fast response");
  });
});

// ---------------------------------------------------------------------------
// T-003: inferWithRetry - retry with backoff
// ---------------------------------------------------------------------------

describe("T-003: inferWithRetry - retry on transient errors", () => {
  it("retries on 429 and succeeds on second attempt", async () => {
    let attempt = 0;
    const api = {
      inference: async (_req: InferenceRequest): Promise<InferenceResponse> => {
        attempt++;
        if (attempt === 1) throw new Error("HTTP 429 rate limit exceeded");
        return { content: "success after retry" };
      },
    };

    const opts: WorkerOptions = { timeoutMs: 5000, maxRetries: 2, backoffBaseMs: 10 };
    const result = await inferWithRetry(api, { model: "m", messages: [] }, opts);
    expect(extractContent(result)).toBe("success after retry");
    expect(attempt).toBe(2);
  });

  it("retries on 503 and succeeds on third attempt", async () => {
    let attempt = 0;
    const api = {
      inference: async (_req: InferenceRequest): Promise<InferenceResponse> => {
        attempt++;
        if (attempt < 3) throw new Error("503 Service Unavailable");
        return { content: "recovered" };
      },
    };

    const opts: WorkerOptions = { timeoutMs: 5000, maxRetries: 2, backoffBaseMs: 10 };
    const result = await inferWithRetry(api, { model: "m", messages: [] }, opts);
    expect(extractContent(result)).toBe("recovered");
    expect(attempt).toBe(3);
  });

  it("does NOT retry on non-transient errors", async () => {
    let attempt = 0;
    const api = {
      inference: async (_req: InferenceRequest): Promise<InferenceResponse> => {
        attempt++;
        throw new Error("401 Unauthorized");
      },
    };

    const opts: WorkerOptions = { timeoutMs: 5000, maxRetries: 3, backoffBaseMs: 10 };
    await expect(inferWithRetry(api, { model: "m", messages: [] }, opts))
      .rejects.toThrow("401 Unauthorized");
    expect(attempt).toBe(1); // No retries
  });

  it("throws last error after exhausting retries", async () => {
    let attempt = 0;
    const api = {
      inference: async (_req: InferenceRequest): Promise<InferenceResponse> => {
        attempt++;
        throw new Error(`HTTP 503 attempt ${attempt}`);
      },
    };

    const opts: WorkerOptions = { timeoutMs: 5000, maxRetries: 2, backoffBaseMs: 10 };
    await expect(inferWithRetry(api, { model: "m", messages: [] }, opts))
      .rejects.toThrow("503");
    expect(attempt).toBe(3); // 1 initial + 2 retries
  });
});

// ---------------------------------------------------------------------------
// T-003: Graceful degradation - worker failure in fan-out
// ---------------------------------------------------------------------------

describe("T-003: Worker failure graceful degradation", () => {
  it("continues fan-out if one worker fails and reports partial results", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
      { id: 2, title: "Sub B", description: "Do B", expectedOutput: "B" },
    ]);

    let workerCallCount = 0;
    const api = {
      calls: [] as Array<{ model: string; messages: Array<{ role: string; content: string }> }>,
      inference: async (req: InferenceRequest): Promise<InferenceResponse> => {
        api.calls.push({ model: req.model, messages: req.messages });
        if (req.model === "planner") return { content: plannerResponse };
        if (req.model === "worker-a") {
          workerCallCount++;
          // First worker fails with non-retryable error
          throw new Error("Model not available");
        }
        if (req.model === "worker-b") return { content: "Worker B succeeded" };
        // reviewer
        return { content: "Review done" };
      },
    };

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Test graceful degradation",
      planner: "planner",
      workers: ["worker-a", "worker-b"],
      reviewer: "reviewer",
    };

    const result = await executeFanOut(req, api, { timeoutMs: 5000, maxRetries: 0 });

    // Should complete and include error info for failed worker
    expect(result).toContain("Sub A -- failed: Model not available");
    // Should still run reviewer with partial results
    expect(api.calls.some((c) => c.model === "reviewer")).toBe(true);
  });

  it("pipeline stops on first failure and returns partial result", async () => {
    const api = {
      calls: [] as Array<{ model: string; messages: Array<{ role: string; content: string }> }>,
      inference: async (req: InferenceRequest): Promise<InferenceResponse> => {
        api.calls.push({ model: req.model, messages: req.messages });
        if (req.model === "planner") return { content: "Plan done" };
        if (req.model === "worker") throw new Error("Worker crashed");
        return { content: "Should not reach here" };
      },
    };

    const req: OrchestrateRequest = {
      mode: "pipeline",
      task: "Pipeline test",
      planner: "planner",
      workers: ["worker"],
      reviewer: "reviewer",
    };

    const result = await executePipeline(req, api, { timeoutMs: 5000, maxRetries: 0 });

    // Should not have called reviewer
    expect(api.calls.some((c) => c.model === "reviewer")).toBe(false);
    expect(result).toContain("Failed: Worker crashed");
  });
});

// ---------------------------------------------------------------------------
// T-004: Progress reporting
// ---------------------------------------------------------------------------

describe("T-004: Progress reporting - fan-out", () => {
  it("emits started and completed events for planner", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
    ]);

    const mock = makeMockApi({
      "planner": plannerResponse,
      "worker": "Worker output",
      "reviewer": "Review done",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Test progress",
      planner: "planner",
      workers: ["worker"],
      reviewer: "reviewer",
    };

    await executeFanOut(req, mock, {}, (evt) => { events.push(evt); });

    const plannerEvents = events.filter((e) => e.phase === "planning");
    expect(plannerEvents.some((e) => e.status === "started")).toBe(true);
    expect(plannerEvents.some((e) => e.status === "completed")).toBe(true);
  });

  it("emits worker events with correct index and total", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
      { id: 2, title: "Sub B", description: "Do B", expectedOutput: "B" },
    ]);

    const mock = makeMockApi({
      "planner": plannerResponse,
      "w1": "Worker 1 output",
      "w2": "Worker 2 output",
      "reviewer": "Review done",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Test worker progress",
      planner: "planner",
      workers: ["w1", "w2"],
      reviewer: "reviewer",
    };

    await executeFanOut(req, mock, {}, (evt) => { events.push(evt); });

    const execEvents = events.filter((e) => e.phase === "execution");
    expect(execEvents.length).toBeGreaterThan(0);

    // Should have workerTotal set
    const workerEvts = execEvents.filter((e) => e.workerTotal != null);
    expect(workerEvts.length).toBeGreaterThan(0);
    expect(workerEvts[0].workerTotal).toBe(2);
  });

  it("emits review started and completed events", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
    ]);

    const mock = makeMockApi({
      "planner": plannerResponse,
      "worker": "Worker output",
      "reviewer": "Review done",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Test review progress",
      planner: "planner",
      workers: ["worker"],
      reviewer: "reviewer",
    };

    await executeFanOut(req, mock, {}, (evt) => { events.push(evt); });

    const reviewEvents = events.filter((e) => e.phase === "review");
    expect(reviewEvents.some((e) => e.status === "started")).toBe(true);
    expect(reviewEvents.some((e) => e.status === "completed")).toBe(true);
  });

  it("emits failed event when worker fails", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
    ]);

    const api = {
      inference: async (req: InferenceRequest): Promise<InferenceResponse> => {
        if (req.model === "planner") return { content: plannerResponse };
        if (req.model === "worker") throw new Error("Worker failed");
        return { content: "Review done" };
      },
    };

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Test failure progress",
      planner: "planner",
      workers: ["worker"],
      reviewer: "reviewer",
    };

    await executeFanOut(req, api, { maxRetries: 0 }, (evt) => { events.push(evt); });

    const failedEvents = events.filter((e) => e.status === "failed" && e.phase === "execution");
    expect(failedEvents.length).toBeGreaterThan(0);
    expect(failedEvents[0].error).toContain("Worker failed");
    expect(failedEvents[0].model).toBe("worker");
  });
});

describe("T-004: Progress reporting - pipeline", () => {
  it("emits events for each step", async () => {
    const mock = makeMockApi({
      "planner": "Plan",
      "worker": "Execution",
      "reviewer": "Final",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "pipeline",
      task: "Pipeline progress test",
      planner: "planner",
      workers: ["worker"],
      reviewer: "reviewer",
    };

    await executePipeline(req, mock, {}, (evt) => { events.push(evt); });

    const phases = events.map((e) => e.phase);
    expect(phases).toContain("planning");
    expect(phases).toContain("execution");
    expect(phases).toContain("review");

    // Each phase should have started + completed
    const planningStarted = events.find((e) => e.phase === "planning" && e.status === "started");
    const planningDone = events.find((e) => e.phase === "planning" && e.status === "completed");
    expect(planningStarted).toBeDefined();
    expect(planningDone).toBeDefined();
  });

  it("includes model name in each progress event", async () => {
    const mock = makeMockApi({
      "plan-model": "Plan",
      "work-model": "Work",
      "rev-model": "Review",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "pipeline",
      task: "Model name in events",
      planner: "plan-model",
      workers: ["work-model"],
      reviewer: "rev-model",
    };

    await executePipeline(req, mock, {}, (evt) => { events.push(evt); });

    const modelNames = events.map((e) => e.model);
    expect(modelNames).toContain("plan-model");
    expect(modelNames).toContain("work-model");
    expect(modelNames).toContain("rev-model");
  });
});

describe("T-004: Progress reporting - consensus", () => {
  it("emits synthesis events", async () => {
    const mock = makeMockApi({
      "m1": "Response 1",
      "m2": "Response 2",
      "synth": "Synthesis result",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "consensus",
      task: "Consensus progress test",
      planner: "m1",
      workers: ["m2"],
      reviewer: "synth",
    };

    await executeConsensus(req, mock, {}, (evt) => { events.push(evt); });

    const synthEvents = events.filter((e) => e.phase === "synthesis");
    expect(synthEvents.some((e) => e.status === "started")).toBe(true);
    expect(synthEvents.some((e) => e.status === "completed")).toBe(true);
    expect(synthEvents[0].model).toBe("synth");
  });

  it("emits execution events for all parallel workers", async () => {
    const mock = makeMockApi({
      "m1": "Response from m1",
      "m2": "Response from m2",
      "m3": "Response from m3",
      "synth": "All synthesized",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "consensus",
      task: "Three-way consensus",
      planner: "m1",
      workers: ["m2", "m3"],
      reviewer: "synth",
    };

    await executeConsensus(req, mock, {}, (evt) => { events.push(evt); });

    const execEvents = events.filter((e) => e.phase === "execution");
    // 3 models queried: m1, m2, m3 -- each gets started + completed
    expect(execEvents.filter((e) => e.status === "started").length).toBe(3);
    expect(execEvents.filter((e) => e.status === "completed").length).toBe(3);
  });

  it("emits resultSummary on completion", async () => {
    const mock = makeMockApi({
      "m1": "A reasonably long response from model 1 about the topic",
      "synth": "Final synthesis",
    });

    const events: ProgressEvent[] = [];

    const req: OrchestrateRequest = {
      mode: "consensus",
      task: "Result summary test",
      planner: "m1",
      workers: [],
      reviewer: "synth",
    };

    await executeConsensus(req, mock, {}, (evt) => { events.push(evt); });

    const completedExec = events.find((e) => e.phase === "execution" && e.status === "completed");
    expect(completedExec?.resultSummary).toMatch(/\d+ chars/);
  });
});

// ---------------------------------------------------------------------------
// T-004: Progress callback does not break orchestration when it throws
// ---------------------------------------------------------------------------

describe("T-004: Progress callback resilience", () => {
  it("fan-out completes even if onProgress throws", async () => {
    const plannerResponse = JSON.stringify([
      { id: 1, title: "Sub A", description: "Do A", expectedOutput: "A" },
    ]);

    const mock = makeMockApi({
      "p": plannerResponse,
      "w": "Worker result",
      "r": "Review done",
    });

    const req: OrchestrateRequest = {
      mode: "fan-out",
      task: "Progress throws test",
      planner: "p",
      workers: ["w"],
      reviewer: "r",
    };

    // onProgress throws -- but orchestration should still complete
    const throwingProgress = async (_evt: ProgressEvent) => {
      throw new Error("Progress handler error");
    };

    // Should NOT throw
    await expect(executeFanOut(req, mock, {}, throwingProgress))
      .resolves.toContain("Final Result:");
  });
});

// ---------------------------------------------------------------------------
// T-001: Help and model list formatting
// ---------------------------------------------------------------------------

describe("T-001: showHelp and formatModelList", () => {
  const models: ModelInfo[] = [
    { id: "anthropic/claude-opus-4-6", alias: "opus", provider: "anthropic", auth: true, tags: [] },
    { id: "github-copilot/gpt-4o", alias: "copilot", provider: "github-copilot", auth: true, tags: ["free"] },
  ];

  it("showHelp includes all three modes", () => {
    const help = showHelp(models, {});
    expect(help).toContain("fan-out");
    expect(help).toContain("pipeline");
    expect(help).toContain("consensus");
  });

  it("showHelp includes usage examples", () => {
    const help = showHelp(models, {});
    expect(help).toContain("/orchestrate");
    expect(help).toContain("help");
    expect(help).toContain("models");
  });

  it("formatModelList includes providers and auth icons", () => {
    const list = formatModelList(models);
    expect(list).toContain("anthropic");
    expect(list).toContain("✅");
    expect(list).toContain("github-copilot");
    expect(list).toContain("FREE");
  });

  it("formatRecommendation classifies and shows recommendation", () => {
    const profile = "coding";
    const taskProfile = {
      planner: "opus",
      workers: ["copilot"],
      reviewer: "opus",
    };
    const rec = formatRecommendation("Build a REST API", profile, taskProfile, models);
    expect(rec).toContain("coding");
    expect(rec).toContain("Build a REST API");
    expect(rec).toContain("Planner:");
    expect(rec).toContain("Workers:");
  });
});
