import {
  collectSimpleChannelFieldAssignments,
  getChannelSurface,
  type ResolverContext,
  type SecretDefaults,
  type SecretTargetRegistryEntry,
} from "openclaw/plugin-sdk/channel-secret-basic-runtime";

export const secretTargetRegistryEntries = [
  {
    id: "channels.zulip.accounts.*.apiKey",
    targetType: "channels.zulip.accounts.*.apiKey",
    configFile: "openclaw.json",
    pathPattern: "channels.zulip.accounts.*.apiKey",
    secretShape: "secret_input",
    expectedResolvedValue: "string",
    includeInPlan: true,
    includeInConfigure: true,
    includeInAudit: true,
  },
  {
    id: "channels.zulip.apiKey",
    targetType: "channels.zulip.apiKey",
    configFile: "openclaw.json",
    pathPattern: "channels.zulip.apiKey",
    secretShape: "secret_input",
    expectedResolvedValue: "string",
    includeInPlan: true,
    includeInConfigure: true,
    includeInAudit: true,
  },
] satisfies SecretTargetRegistryEntry[];

export function collectRuntimeConfigAssignments(params: {
  config: { channels?: Record<string, unknown> };
  defaults: SecretDefaults | undefined;
  context: ResolverContext;
}): void {
  const resolved = getChannelSurface(params.config, "zulip");
  if (!resolved) {
    return;
  }

  const { channel: zulip, surface } = resolved;
  collectSimpleChannelFieldAssignments({
    channelKey: "zulip",
    field: "apiKey",
    channel: zulip,
    surface,
    defaults: params.defaults,
    context: params.context,
    topInactiveReason: "no enabled account inherits this top-level Zulip API key.",
    accountInactiveReason: "Zulip account is disabled.",
  });
}

export const channelSecrets = {
  secretTargetRegistryEntries,
  collectRuntimeConfigAssignments,
};
