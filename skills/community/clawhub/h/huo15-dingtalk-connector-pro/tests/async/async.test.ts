import { describe, expect, it } from "vitest";
import { raceWithTimeoutAndAbort } from "../../src/utils/async";

describe("raceWithTimeoutAndAbort", () => {
  it("returns success when promise resolves first", async () => {
    const result = await raceWithTimeoutAndAbort(Promise.resolve("ok"), { timeoutMs: 100 });
    expect(result).toEqual({ status: "success", value: "ok" });
  });

  it("returns timeout when promise is too slow", async () => {
    const slowPromise = new Promise<string>((resolve) => {
      setTimeout(() => resolve("late"), 30);
    });
    const result = await raceWithTimeoutAndAbort(slowPromise, { timeoutMs: 1 });
    expect(result).toEqual({ status: "timeout" });
  });

  it("returns aborted when signal is already aborted", async () => {
    const controller = new AbortController();
    controller.abort();
    const slowPromise = new Promise<string>((resolve) => {
      setTimeout(() => resolve("late"), 30);
    });
    const result = await raceWithTimeoutAndAbort(slowPromise, {
      timeoutMs: 100,
      abortSignal: controller.signal,
    });
    expect(result).toEqual({ status: "aborted" });
  });

  it("returns aborted when signal aborts before resolve", async () => {
    const controller = new AbortController();
    const slowPromise = new Promise<string>((resolve) => {
      setTimeout(() => resolve("late"), 50);
    });

    setTimeout(() => controller.abort(), 5);
    const result = await raceWithTimeoutAndAbort(slowPromise, {
      timeoutMs: 1000,
      abortSignal: controller.signal,
    });
    expect(result).toEqual({ status: "aborted" });
  });

  it("propagates errors from main promise", async () => {
    const rejectPromise = new Promise<string>((_, reject) => {
      setTimeout(() => reject(new Error("boom")), 1);
    });
    await expect(
      raceWithTimeoutAndAbort(rejectPromise, {
        timeoutMs: 100,
      }),
    ).rejects.toThrow("boom");
  });
});
