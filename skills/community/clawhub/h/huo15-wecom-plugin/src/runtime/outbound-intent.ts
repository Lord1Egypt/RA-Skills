export type OutboundIntent =
  | { kind: "text"; text: string }
  | { kind: "media"; mediaUrl: string; text?: string }
  | { kind: "card"; card: Record<string, unknown> };
