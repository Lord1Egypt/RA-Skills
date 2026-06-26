import type {
  GuardScannerConstructor,
  GuardScannerInstance,
  RuntimeCheckStats,
  RuntimeDecision,
  ScannerOptions,
  } from "./types.js";
export {
  GuardScanner,
  VERSION,
  THRESHOLDS,
  SEVERITY_WEIGHTS,
  scanToolCall,
  RUNTIME_CHECKS,
  getCheckStats,
  LAYER_NAMES,
} from "./scanner.js";
export {
  MCPServer,
  startServer,
  TOOLS,
} from "./mcp-server.js";

export function createScanner(options: ScannerOptions = {}): GuardScannerInstance {
  return new GuardScanner(options) as unknown as GuardScannerInstance;
}

import { GuardScanner } from "./scanner.js";

export type {
  CapabilityMetrics,
  CustomRule,
  Finding,
  GuardMode,
  GuardScannerConstructor,
  GuardScannerInstance,
  McpRequest,
  PluginConfig,
  RuntimeDecision,
  RuntimeCheckStats,
  ScanReport,
  SarifReport,
  ScanResult,
  ScannerOptions,
  Severity,
} from "./types.js";
