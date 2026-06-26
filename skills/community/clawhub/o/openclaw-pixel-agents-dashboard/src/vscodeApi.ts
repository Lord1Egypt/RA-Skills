// Stub: replaces VS Code API with no-ops for standalone dashboard
export const vscode = {
  postMessage(_msg: unknown): void {
    // No-op in standalone mode — messages go via WebSocket instead
  },
};
