import {
  DmPolicySchema,
  buildChannelConfigSchema,
} from "openclaw/plugin-sdk/channel-config-schema";
import { z } from "openclaw/plugin-sdk/zod";

export const ZulipConfigSchema = z
  .object({
    realm: z.string().optional(),
    email: z.string().optional(),
    streams: z.array(z.string()).optional(),
    defaultStream: z.string().optional(),
    defaultTopic: z.string().optional(),
    dmPolicy: DmPolicySchema.optional().default("pairing"),
    allowFrom: z.array(z.union([z.string(), z.number()])).optional(),
  })
  .strict();

export const ZulipChannelConfigSchema: ReturnType<typeof buildChannelConfigSchema> = buildChannelConfigSchema(ZulipConfigSchema);
