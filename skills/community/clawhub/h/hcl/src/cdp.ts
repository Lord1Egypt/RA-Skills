import { RawData, WebSocket } from "ws";

export type CdpConfig = {
  host: string;
  port: number;
};

export type CdpFrameMetadata = {
  offsetTop: number;
  pageScaleFactor: number;
  deviceWidth: number;
  deviceHeight: number;
  scrollOffsetX: number;
  scrollOffsetY: number;
};

type CdpTarget = {
  type?: string;
  webSocketDebuggerUrl?: string;
};

type CdpResponse = {
  id?: number;
  result?: unknown;
  error?: { message?: string };
  method?: string;
  params?: unknown;
};

type PendingRequest = {
  resolve: (value: unknown) => void;
  reject: (reason?: unknown) => void;
};

type ScreencastFrameParams = {
  data: string;
  metadata: CdpFrameMetadata;
  sessionId: number;
};

async function fetchPageTarget(config: CdpConfig): Promise<CdpTarget> {
  const response = await fetch(`http://${config.host}:${config.port}/json/list`);
  if (!response.ok) {
    throw new Error(`Failed to discover CDP targets: ${response.status}`);
  }

  const targets = await response.json() as CdpTarget[];
  const pageTarget = targets.find((target) => target.type === "page" && typeof target.webSocketDebuggerUrl === "string");
  if (!pageTarget?.webSocketDebuggerUrl) {
    throw new Error("No CDP page target found");
  }

  return pageTarget;
}

export async function discoverCdpTarget(config: CdpConfig): Promise<string> {
  const pageTarget = await fetchPageTarget(config);
  return pageTarget.webSocketDebuggerUrl as string;
}

function isScreencastFrameParams(value: unknown): value is ScreencastFrameParams {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  const metadata = candidate.metadata;
  if (!metadata || typeof metadata !== "object") {
    return false;
  }

  return typeof candidate.data === "string" && typeof candidate.sessionId === "number";
}

export class CdpClient {
  private readonly config: CdpConfig;
  private ws: WebSocket | null = null;
  private nextId = 1;
  private readonly pending = new Map<number, PendingRequest>();
  private screencastHandler: ((data: string, metadata: CdpFrameMetadata) => void) | null = null;
  private targetWebSocketUrl: string | null = null;

  constructor(config: CdpConfig) {
    this.config = config;
  }

  getTargetWebSocketUrl(): string | null {
    return this.targetWebSocketUrl;
  }

  async connect(): Promise<void> {
    const pageTarget = await fetchPageTarget(this.config);
    const targetUrl = pageTarget.webSocketDebuggerUrl as string;
    this.targetWebSocketUrl = targetUrl;

    await new Promise<void>((resolve, reject) => {
      const ws = new WebSocket(targetUrl);
      let settled = false;

      ws.once("open", () => {
        settled = true;
        this.ws = ws;
        ws.on("message", (message: RawData) => {
          this.handleMessage(message.toString());
        });
        ws.on("close", () => {
          this.rejectPending(new Error("CDP connection closed"));
          this.ws = null;
        });
        ws.on("error", (error) => {
          this.rejectPending(error);
        });
        resolve();
      });

      ws.once("error", (error) => {
        if (!settled) {
          settled = true;
          reject(error);
        }
      });
    });
  }

  async startScreencast(onFrame: (data: string, metadata: CdpFrameMetadata) => void): Promise<void> {
    this.screencastHandler = onFrame;
    await this.send("Page.enable");
    await this.send("Page.startScreencast", {
      format: "jpeg",
      quality: 70,
      maxWidth: 1280,
      maxHeight: 720,
    });
  }

  async stopScreencast(): Promise<void> {
    this.screencastHandler = null;
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      return;
    }
    await this.send("Page.stopScreencast");
  }

  async dispatchMouse(
    type: "mousePressed" | "mouseReleased" | "mouseMoved",
    x: number,
    y: number,
    button = "none",
    buttons = 0,
  ): Promise<void> {
    await this.send("Input.dispatchMouseEvent", { type, x, y, button, buttons });
  }

  async dispatchKey(
    type: "keyDown" | "keyUp" | "char",
    key: string,
    code: string,
    text?: string,
    modifiers = 0,
  ): Promise<void> {
    const params: Record<string, unknown> = { type, key, code, modifiers };
    if (text !== undefined) {
      params.text = text;
    }
    await this.send("Input.dispatchKeyEvent", params);
  }

  disconnect(): void {
    this.screencastHandler = null;
    this.rejectPending(new Error("CDP disconnected"));
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  private async send(method: string, params?: Record<string, unknown>): Promise<unknown> {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error("CDP socket is not connected");
    }

    const id = this.nextId++;
    const payload = JSON.stringify(params ? { id, method, params } : { id, method });

    return await new Promise<unknown>((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws?.send(payload, (error) => {
        if (error) {
          this.pending.delete(id);
          reject(error);
        }
      });
    });
  }

  private handleMessage(rawMessage: string): void {
    const message = JSON.parse(rawMessage) as CdpResponse;

    if (typeof message.id === "number") {
      const pending = this.pending.get(message.id);
      if (!pending) {
        return;
      }

      this.pending.delete(message.id);
      if (message.error) {
        pending.reject(new Error(message.error.message || "CDP request failed"));
      } else {
        pending.resolve(message.result);
      }
      return;
    }

    if (message.method === "Page.screencastFrame" && isScreencastFrameParams(message.params)) {
      void this.send("Page.screencastFrameAck", { sessionId: message.params.sessionId }).catch(() => {});
      if (this.screencastHandler) {
        this.screencastHandler(message.params.data, message.params.metadata);
      }
    }
  }

  private rejectPending(error: Error): void {
    for (const [id, pending] of this.pending) {
      pending.reject(error);
      this.pending.delete(id);
    }
  }
}
