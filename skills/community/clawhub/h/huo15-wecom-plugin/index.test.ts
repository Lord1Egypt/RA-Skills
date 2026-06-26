import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { describe, expect, it, vi } from "vitest";
import plugin from "./index.js";

describe("wecom plugin register", () => {
  it("registers both recommended and legacy webhook route prefixes", () => {
    const registerChannel = vi.fn();
    const registerHttpRoute = vi.fn();
    const registerTool = vi.fn();
    const on = vi.fn();
    const api = {
      runtime: {},
      registerChannel,
      registerHttpRoute,
      registerTool,
      on,
    } as unknown as OpenClawPluginApi;

    plugin.register(api);

    expect(registerChannel).toHaveBeenCalledTimes(1);
    expect(registerHttpRoute).toHaveBeenCalledTimes(2);
    expect(registerHttpRoute).toHaveBeenCalledWith(
      expect.objectContaining({
        path: "/plugins/wecom",
        auth: "plugin",
        match: "prefix",
      }),
    );
    expect(registerHttpRoute).toHaveBeenCalledWith(
      expect.objectContaining({
        path: "/wecom",
        auth: "plugin",
        match: "prefix",
      }),
    );
  });
});
