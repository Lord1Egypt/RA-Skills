import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  clearDingtalkWebhookRateLimitStateForTest,
  getDingtalkMonitorState,
  getDingtalkWebhookRateLimitStateSizeForTest,
  isWebhookRateLimitedForTest,
  setDingtalkMonitorState,
  stopDingtalkMonitorState,
} from "../../src/core/state";

describe("core/state", () => {
  beforeEach(() => {
    stopDingtalkMonitorState();
  });

  it("sets and gets monitor state", () => {
    const controller = new AbortController();
    setDingtalkMonitorState("acc-1", { running: true, abortController: controller });

    expect(getDingtalkMonitorState("acc-1")).toEqual({
      running: true,
      abortController: controller,
    });
  });

  it("stops and deletes one account", () => {
    const controller = { abort: vi.fn() } as any;
    setDingtalkMonitorState("acc-1", { running: true, abortController: controller });

    stopDingtalkMonitorState("acc-1");

    expect(controller.abort).toHaveBeenCalledTimes(1);
    expect(getDingtalkMonitorState("acc-1")).toBeUndefined();
  });

  it("stops all accounts and clears state", () => {
    const c1 = { abort: vi.fn() } as any;
    const c2 = { abort: vi.fn() } as any;
    setDingtalkMonitorState("acc-1", { running: true, abortController: c1 });
    setDingtalkMonitorState("acc-2", { running: true, abortController: c2 });

    stopDingtalkMonitorState();

    expect(c1.abort).toHaveBeenCalledTimes(1);
    expect(c2.abort).toHaveBeenCalledTimes(1);
    expect(getDingtalkMonitorState("acc-1")).toBeUndefined();
    expect(getDingtalkMonitorState("acc-2")).toBeUndefined();
  });

  it("no-op test utilities stay deterministic", () => {
    clearDingtalkWebhookRateLimitStateForTest();
    expect(getDingtalkWebhookRateLimitStateSizeForTest()).toBe(0);
    expect(isWebhookRateLimitedForTest()).toBe(false);
  });
});
