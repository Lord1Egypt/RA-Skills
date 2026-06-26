import { describe, expect, it, vi } from "vitest";
import { createLogger, createLoggerFromConfig } from "../../src/utils/logger";

describe("utils/logger", () => {
  it("info only outputs in debug mode", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const logger = createLogger(false, "T");
    logger.info("msg");
    expect(spy).not.toHaveBeenCalled();

    const debugLogger = createLogger(true, "T");
    debugLogger.info("msg");
    expect(spy).toHaveBeenCalledWith("[T]", "msg");
    spy.mockRestore();
  });

  it("info without prefix", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const logger = createLogger(true);
    logger.info("msg");
    expect(spy).toHaveBeenCalledWith("msg");
    spy.mockRestore();
  });

  it("warn always outputs", () => {
    const spy = vi.spyOn(console, "warn").mockImplementation(() => {});
    const logger = createLogger(false, "T");
    logger.warn("w");
    expect(spy).toHaveBeenCalledWith("[T]", "w");
    spy.mockRestore();
  });

  it("warn without prefix", () => {
    const spy = vi.spyOn(console, "warn").mockImplementation(() => {});
    const logger = createLogger(false);
    logger.warn("w");
    expect(spy).toHaveBeenCalledWith("w");
    spy.mockRestore();
  });

  it("error always outputs", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    const logger = createLogger(false, "T");
    logger.error("e");
    expect(spy).toHaveBeenCalledWith("[T]", "e");
    spy.mockRestore();
  });

  it("error without prefix", () => {
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    const logger = createLogger(false);
    logger.error("e");
    expect(spy).toHaveBeenCalledWith("e");
    spy.mockRestore();
  });

  it("debug only outputs in debug mode with prefix", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const logger = createLogger(false, "T");
    logger.debug("d");
    expect(spy).not.toHaveBeenCalled();

    const debugLogger = createLogger(true, "T");
    debugLogger.debug("d");
    expect(spy).toHaveBeenCalledWith("[DEBUG][T]", "d");
    spy.mockRestore();
  });

  it("debug without prefix", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const logger = createLogger(true);
    logger.debug("d");
    expect(spy).toHaveBeenCalledWith("[DEBUG]", "d");
    spy.mockRestore();
  });

  it("createLoggerFromConfig delegates to createLogger", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const logger = createLoggerFromConfig({ debug: true }, "Cfg");
    logger.info("x");
    expect(spy).toHaveBeenCalledWith("[Cfg]", "x");
    spy.mockRestore();
  });
});
